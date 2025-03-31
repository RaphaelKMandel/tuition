class WaterFall:
    def __init__(self, thresholds, rates):
        self.thresholds = thresholds + [float("inf")]
        self.rates = rates

    def evaluate(self, amount):
        for threshold, rate in zip(self.thresholds, self.rates):
            if amount < threshold:
                return rate * amount


class Progressive:
    def __init__(self, thresholds, rates):
        self.thresholds = [0] + thresholds + [float("inf")]
        self.rates = rates

    def evaluate(self, amount):
        result = 0
        for n, (rate, threshold) in enumerate(
            zip(self.rates, self.thresholds[1:]), start=1
        ):
            if amount > threshold:
                result += rate * (threshold - self.thresholds[n - 1])
            else:
                return result + rate * (amount - self.thresholds[n - 1])


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    xs = []
    ys = []
    p = Progressive([5, 10], [0.1, 0.2, 0.3])
    for x in range(20):
        y = p.evaluate(x)
        xs.append(x)
        ys.append(y)

    plt.plot(xs, ys)

    xs = []
    ys = []
    w = WaterFall([5, 10], [0.1, 0.2, 0.3])
    for x in range(20):
        y = w.evaluate(x)
        xs.append(x)
        ys.append(y)

    plt.plot(xs, ys)
    plt.show()
