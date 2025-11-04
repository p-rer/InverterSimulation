from .CircuitElement import CircuitElement

class Capacitor(CircuitElement):
    def __init__(self, n1, n2, capacitance):
        super().__init__(n1, n2, capacitance)

    def stamp(self, G, C, B=None, E=None, k=None, x_prev=None):
        c = self.value
        n1, n2 = self.n1, self.n2
        if n1 != 0:
            C[n1-1, n1-1] += c
        if n2 != 0:
            C[n2-1, n2-1] += c
        if n1 != 0 and n2 != 0:
            C[n1-1, n2-1] -= c
            C[n2-1, n1-1] -= c
        return 0.0
