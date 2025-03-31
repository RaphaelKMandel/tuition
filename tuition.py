from rates import WaterFall, Progressive


class Family:
    def __init__(self, agi: int, students: dict):
        self.agi = agi
        self.students = students
        self.rate = (
            Progressive([300_000, 400_000], [0.15, 0.175, 0.20]).evaluate(agi)
            / self.agi
        )
        self.max_tuition = self.rate * self.agi


class Tuition:
    def __init__(self, tuition_file):
        with open(tuition_file, "r") as f:
            lines = f.read().strip().split("\n")[1:]

        self.grades = {}
        for line in lines:
            grade, subs, tuition, frac = line.split(",")
            self.grades[grade] = {
                "YesSubsidy": float(subs),
                "NoSubsidy": float(tuition),
                "Fraction": float(frac),
            }

    def get_tuitions(self, family: Family, subsidy: bool = False):
        if subsidy:
            subsidy = "YesSubsidy"
        else:
            subsidy = "NoSubsidy"

        s1 = 0
        s2 = 0
        for key, value in family.students.items():
            grade = self.grades[key]
            s1 += value * grade[subsidy] * grade["Fraction"]
            s2 += value * grade[subsidy] * (1 - grade["Fraction"])

        return s1, s2

    def get_total_tuition(self, family: Family, subsidy: bool = False):
        cappable, uncappable = self.get_tuitions(family, subsidy)
        return uncappable + min(cappable, family.max_tuition)


if __name__ == "__main__":
    from matplotlib.pyplot import subplots, show

    tuition = Tuition("2025tuition.csv")
    students = {"ECC5F": 1, "G25": 1, "G78": 1}
    print(tuition.get_total_tuition(Family(200000, students)))
    x = []
    y = []
    z = []
    for agi in range(20000, 500_000, 1000):
        x.append(agi / 1000)
        family = Family(agi, students)
        y.append(family.max_tuition / 1000)
        z.append(tuition.get_total_tuition(family) / 1000)

    fig, ax = subplots()
    ax.plot(x, y)
    # ax.plot(x, z)
    ax.grid()
    ax.set_xlabel("AGI (k$)")
    ax.set_ylabel("Max Tuition (k$)")
    show()
