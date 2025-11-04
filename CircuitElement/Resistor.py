from .CircuitElement import CircuitElement

class Resistor(CircuitElement):
    def __init__(self, n1, n2, resistance):
        super().__init__(n1, n2, resistance)

    def stamp(self, G, C, B=None, E=None, k=None, x_prev=None):
        g = 1.0 / self.value
        n1, n2 = self.n1, self.n2
        if n1 != 0:
            G[n1-1, n1-1] += g
        if n2 != 0:
            G[n2-1, n2-1] += g
        if n1 != 0 and n2 != 0:
            G[n1-1, n2-1] -= g
            G[n2-1, n1-1] -= g
        return 0.0   # stamp は何か返しても良い（ここでは意味なし）
