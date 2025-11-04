class CircuitElement:
    def __init__(self, n1, n2, value):
        self.n1 = n1
        self.n2 = n2
        self.value = value

    # MNA対応の共通シグネチャ。派生クラスは使わない引数を無視してよい。
    def stamp(self, G, C, B, E, k, x_prev):
        raise NotImplementedError
