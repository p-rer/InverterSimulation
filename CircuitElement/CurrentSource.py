from CircuitElement.CircuitElement import CircuitElement
class CurrentSource(CircuitElement):
    def __init__(self, n1, n2, current_func):
        super().__init__(n1, n2, None, current_func)

    def stamp(self, G, C, B=None, E=None, k=None, x_prev=None, t=0.0):
        # 電流源は構造を変えないが、時刻依存電流を返す
        if callable(self.time_func):
            I = self.time_func(t)
        else:
            I = self.value if self.value is not None else 0.0
        return I
