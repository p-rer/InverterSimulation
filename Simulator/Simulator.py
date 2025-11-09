import numpy as np

class Simulator:
    def __init__(self, circuit, dt):
        self.circuit = circuit
        self.dt = dt

    def run(self, t_end, tol=1e-6, max_iter=20):
        G_base, C_base, B, branch_elems, L_values = self.circuit.build_matrices()
        n = G_base.shape[0]
        m = B.shape[1]
        L_vals = np.array(L_values, dtype=float)

        C_expanded = np.block([
            [C_base, np.zeros((n, m))],
            [np.zeros((m, n)), np.diag(-L_vals)]
        ])

        steps = int(t_end / self.dt)
        x = np.zeros((n + m, 1))
        history = []

        for kstep in range(steps):
            t = kstep * self.dt

            # 電圧源ベクトル E
            E = np.zeros((m, 1))
            for i, elem in enumerate(branch_elems):
                E[i, 0] = elem.time_func(t) if callable(elem.time_func) else 0.0

            # NR反復
            x_old = x.copy()
            for it in range(max_iter):
                # 毎回G, Cを再生成
                G = G_base.copy()
                C = C_base.copy()
                Ieq_total = np.zeros((n, 1))

                # 各素子スタンプ
                for elem in self.circuit.elements:
                    Ieq = elem.stamp(G, C, B, E, None, x_prev=x_old, t=t)
                    if np.isscalar(Ieq):
                        continue
                    n1, n2 = elem.n1, elem.n2
                    if n1 != 0:
                        Ieq_total[n1 - 1, 0] -= Ieq
                    if n2 != 0:
                        Ieq_total[n2 - 1, 0] += Ieq

                # 展開行列
                G_exp = np.block([
                    [G, B],
                    [B.T, np.zeros((m, m))]
                ])
                C_exp = np.block([
                    [C, np.zeros((n, m))],
                    [np.zeros((m, n)), np.diag(-L_vals)]
                ])

                A = G_exp + (C_exp / self.dt)
                b = (C_exp / self.dt) @ x_old
                b[n:, :] += E
                b[:n, :] -= Ieq_total

                x_new = np.linalg.solve(A, b)

                # 収束判定
                err = np.linalg.norm(x_new - x_old)
                if err < tol:
                    x_old = x_new
                    break
                x_old = x_new

            x = x_old
            V_full = np.zeros((self.circuit.num_nodes, 1))
            if n > 0:
                V_full[1:, 0] = x[:n, 0]
            history.append(V_full.copy())

        return np.array(history).reshape(steps, -1)