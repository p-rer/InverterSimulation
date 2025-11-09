class CircuitElement:
    def __init__(self, n1, n2, value=None, time_func=None):
        self.n1 = n1
        self.n2 = n2
        self.value = value
        self.time_func = time_func

    # すべての素子が共通で持つインタフェース
    # 派生クラスは使わない引数を無視してよい
    def stamp(self, G, C, B, E, k, x_prev, t):
        raise NotImplementedError

