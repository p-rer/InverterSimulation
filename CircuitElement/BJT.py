from CircuitElement.CircuitElement import CircuitElement
import numpy as np

class BJT(CircuitElement):
    def __init__(self, nb, nc, ne, Is=1e-15, beta_f=100, beta_r=1, Vt=0.02585):
        # value は使わない
        super().__init__(nb, ne, None)
        self.nc = nc
        self.Is = Is
        self.beta_f = beta_f
        self.beta_r = beta_r
        self.Vt = Vt

    def stamp(self, G, C, B=None, E=None, k=None, x_prev=None, t=None):
        if x_prev is None:
            return 0.0

        nb, nc, ne = self.n1, self.nc, self.n2
        pB = nb - 1 if nb != 0 else None
        pC = nc - 1 if nc != 0 else None
        pE = ne - 1 if ne != 0 else None

        Vb = x_prev[pB, 0] if pB is not None else 0.0
        Vc = x_prev[pC, 0] if pC is not None else 0.0
        Ve = x_prev[pE, 0] if pE is not None else 0.0

        Vbe = Vb - Ve
        Vbc = Vb - Vc

        # Ebers-Moll電流
        I_f = self.Is * (np.exp(Vbe / self.Vt) - 1)
        I_r = self.Is * (np.exp(Vbc / self.Vt) - 1)

        Gbe = self.Is / self.Vt * np.exp(Vbe / self.Vt)
        Gbc = self.Is / self.Vt * np.exp(Vbc / self.Vt)

        # 小信号導電率行列スタンプ（ベース、コレクタ、エミッタ）
        def add(g, i, j, val):
            if i is not None and j is not None:
                g[i, j] += val

        add(G, pB, pB, Gbe + Gbc)
        add(G, pB, pE, -Gbe)
        add(G, pB, pC, -Gbc)
        add(G, pE, pB, -Gbe / self.beta_f)
        add(G, pE, pE, Gbe / self.beta_f)
        add(G, pC, pB, -Gbc / self.beta_r)
        add(G, pC, pC, Gbc / self.beta_r)

        # 等価電流
        Ieq = I_f - Gbe * Vbe - (I_r - Gbc * Vbc)
        return Ieq
