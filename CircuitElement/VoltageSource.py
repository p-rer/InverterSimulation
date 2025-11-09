from .CircuitElement import CircuitElement

class VoltageSource(CircuitElement):
    def __init__(self, n1, n2, voltage_func):
        super().__init__(n1, n2, None, voltage_func)

    def stamp(self, G, C, B=None, E=None, k=None, x_prev=None, t=0.0):
        if B is None or E is None or k is None:
            return 0.0
        n1, n2 = self.n1, self.n2
        if n1 != 0:
            B[n1-1, k] = 1.0
        if n2 != 0:
            B[n2-1, k] = -1.0
        return 0.0
