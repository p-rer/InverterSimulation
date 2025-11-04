from .CircuitElement import CircuitElement
import numpy as np

class Diode(CircuitElement):
    def __init__(self, n1, n2, Is=1e-14, n=1.0, Vt=0.02585):
        super().__init__(n1, n2, None)
        self.Is = Is
        self.n = n
        self.Vt = Vt

    def stamp(self, G, C, B=None, E=None, k=None, x_prev=None):
        """
        線形素子と同一シグネチャ。非線形でも対応できるようx_prevを追加。
        他は無視してOK。
        """
        if x_prev is None:
            return 0.0  # 初回は何もスタンプしない

        n1, n2 = self.n1, self.n2
        p = n1 - 1 if n1 != 0 else None
        m = n2 - 1 if n2 != 0 else None

        # ノード電圧
        Vp = x_prev[p, 0] if p is not None else 0.0
        Vm = x_prev[m, 0] if m is not None else 0.0
        Vd = Vp - Vm

        # ダイオード方程式 (指数特性)
        Id = self.Is * (np.exp(Vd / (self.n * self.Vt)) - 1.0)
        Gd = (self.Is / (self.n * self.Vt)) * np.exp(Vd / (self.n * self.Vt))
        Ieq = Id - Gd * Vd

        # Conductance stamp
        if p is not None:
            G[p, p] += Gd
        if m is not None:
            G[m, m] += Gd
        if p is not None and m is not None:
            G[p, m] -= Gd
            G[m, p] -= Gd

        # 等価電流を返す（シミュレータ側でbに反映）
        return Ieq
