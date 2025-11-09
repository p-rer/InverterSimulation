from .CircuitElement import CircuitElement

class Inductor(CircuitElement):
    def __init__(self, n1, n2, inductance, r_ser=1e-3):
        # value を L に使う既存仕様を踏襲するなら:
        super().__init__(n1, n2, inductance)
        self.r_ser = r_ser  # 直列抵抗（Ω）

    def stamp(self, G, C, B=None, E=None, k=None, x_prev=None, t=None):
        """
        B に枝接続を書き込み、さらに直列抵抗 Rser を G にスタンプする。
        返り値として L を返す（Circuit.build_matrices が収集する）
        """
        # 返り値のみ要求されたケース
        if B is None or k is None:
            return self.value

        n1, n2 = self.n1, self.n2
        L = self.value
        Rser = self.r_ser

        # B マトリクス: 正極 +1, 負極 -1（電圧源と同じルール）
        if n1 != 0:
            B[n1-1, k] += 1.0
        if n2 != 0:
            B[n2-1, k] -= 1.0

        # 直列抵抗を G にスタンプ（抵抗と同じスタンプ）
        if Rser is not None and Rser > 0.0:
            g = 1.0 / Rser
            if n1 != 0:
                G[n1-1, n1-1] += g
            if n2 != 0:
                G[n2-1, n2-1] += g
            if n1 != 0 and n2 != 0:
                G[n1-1, n2-1] -= g
                G[n2-1, n1-1] -= g

        return L
