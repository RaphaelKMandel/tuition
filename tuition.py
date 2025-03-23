class Family:
    RATES = {
        "K": 10000,
        "P": 12000,
        1: 10000,
        2: 10000,
    }

    def __init__(self, agi: int, students: dict):
        self.agi = agi
        self.students = students
        self.rate = self.get_rate()
        self.max_tuition = self.rate * self.agi

    def get_rate(self):
        if self.agi < 300_000:
            return 0.15

        if self.agi < 400_000:
            return 0.175

        return 0.20

    def get_uncapped_tuition(self):
        s = 0
        for key, value in self.students:
            s += value * self.RATES[key]

        return s


if __name__ == "__main__":
    from matplotlib.pyplot import plot, show

    x = []
    y = []
    for agi in range(20000, 1_000_000, 10000):
        x.append(agi)
        f = Family(agi, {})
        y.append(f.max_tuition)

    plot(x, y)
    show()
