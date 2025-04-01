class Dollar(float):
    def __repr__(self):
        return f"${self:,.2f}"


class Percent(float):
    def __repr__(self):
        return f"{(self*100):.2f}%"


class Progressive:
    def __init__(self, thresholds, rates):
        self.thresholds = [Dollar(x)
                           for x in [0] + thresholds + [float("inf")]]
        self.rates = rates

    def evaluate(self, amount):
        results = {"AGI": Dollar(amount), "bands": []}
        for n, (rate, threshold) in enumerate(
            zip(self.rates, self.thresholds[1:]), start=1
        ):
            result = {
                "band": [self.thresholds[n - 1], threshold],
                "rate": Percent(rate),
            }
            if amount > threshold:
                diff = Dollar(threshold - self.thresholds[n - 1])
                result["diff"] = diff
                result["value"] = Dollar(rate * diff)
                results["bands"].append(result)
            else:
                diff = Dollar(amount - self.thresholds[n - 1])
                result["diff"] = diff
                result["value"] = Dollar(rate * diff)
                results["bands"].append(result)
                break

        max_tuition = 0
        for result in results["bands"]:
            max_tuition += result["value"]

        results["rate"] = Percent(max_tuition / amount)
        results["max tuition"] = Dollar(max_tuition)

        return results


class Tuition:
    def __init__(self, tuition_file):
        with open(tuition_file, "r") as f:
            lines = f.read().strip().split("\n")[1:]

        self.grades = []
        self.subsidized = []
        self.unsubsidized = []
        self.capfrac = []
        for line in lines:
            grade, subs, tuition, capfrac = line.split(",")
            self.grades.append(grade)
            self.subsidized.append(int(subs))
            self.unsubsidized.append(int(tuition))
            self.capfrac.append(float(capfrac))

    def get_tuitions(self, students: dict, max_tuition: int, subsidized: bool = False):
        tuitions = self.unsubsidized
        if subsidized:
            tuitions = self.subsidized

        results = {"grades": {}}

        for grade, quantity in students.items():
            index = self.grades.index(grade)
            tuition = quantity * tuitions[index]
            qualified = self.capfrac[index] * tuition
            results["grades"][grade] = {
                "each": Dollar(tuitions[index]),
                "count": quantity,
                "tuition": Dollar(tuition),
                "qualified": Dollar(qualified),
            }

        total_tuition = 0
        total_qualified = 0
        for data in results["grades"].values():
            total_tuition += data["tuition"]
            total_qualified += data["qualified"]

        unqualified = total_tuition - total_qualified

        results["totals"] = {
            "subtotal": Dollar(total_tuition),
            "qualified": Dollar(total_qualified),
            "unqualified": Dollar(unqualified),
            "total": Dollar(unqualified + min(total_qualified, max_tuition)),
        }

        return results


if __name__ == "__main__":
    # from matplotlib.pyplot import subplots, show

    tuition = Tuition("2025tuition.csv")

    print(tuition.get_tuitions({"ECC 5 Full Days": 1, "Grades 2-5": 2}, 10000))
    prog = Progressive([300_000, 400_000], [0.15, 0.175, 0.2])
    print(prog.evaluate(301_000))

    # students = {"ECC5F": 1, "G25": 1, "G78": 1}
    # print(tuition.get_total_tuition(Family(200000, students)))
    # x = []
    # y = []
    # z = []
    # for agi in range(20000, 500_000, 1000):
    #     x.append(agi / 1000)
    #     family = Family(agi, students)
    #     y.append(family.max_tuition / 1000)
    #     z.append(tuition.get_total_tuition(family) / 1000)
    #
    # fig, ax = subplots()
    # ax.plot(x, y)
    # # ax.plot(x, z)
    # ax.grid()
    # ax.set_xlabel("AGI (k$)")
    # ax.set_ylabel("Max Tuition (k$)")
    # show()
