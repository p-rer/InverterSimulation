import numpy as np
from CircuitElement.VoltageSource import VoltageSource
from CircuitElement.Inductor import Inductor

class Circuit:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.elements = []

    def add_element(self, elem):
        self.elements.append(elem)

    # MNA用に G, C, B, branch_elements, L_values を生成して返す
    def build_matrices(self):
        n = self.num_nodes - 1
        # branch elements: VoltageSource および Inductor (枝電流未知数を必要とするもの)
        branch_elements = [e for e in self.elements if isinstance(e, (VoltageSource, Inductor))]
        m = len(branch_elements)

        G = np.zeros((n, n))
        C = np.zeros((n, n))
        B = np.zeros((n, m))
        E = np.zeros((m, 1))

        L_values = [0.0] * m

        k = 0
        for e in self.elements:
            if isinstance(e, (VoltageSource, Inductor)):
                L_val = e.stamp(G, C, B, E, k)
                L_values[k] = float(L_val) if L_val is not None else 0.0
                k += 1
            else:
                e.stamp(G, C, B, E, None)

        return G, C, B, branch_elements, L_values
