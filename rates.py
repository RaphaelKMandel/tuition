class WaterFall:
    def __init__(self, thresholds, rates):
        self.thresholds = thresholds + [float("inf")]
        self.rates = rates

    def evaluate(self, amount):
        for threshold, rate in zip(self.thresholds, self.rates):
            if amount < threshold:
                return rate * amount


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    xs = []
    ys = []
    w = WaterFall([5, 10], [0.1, 0.2, 0.3])
    for x in range(20):
        y = w.evaluate(x)
        xs.append(x)
        ys.append(y)

    plt.plot(xs, ys)
    plt.show()
