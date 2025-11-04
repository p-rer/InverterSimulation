from Circuit.Circuit import Circuit
from CircuitElement.Capacitor import Capacitor
from CircuitElement.Resistor import Resistor
from CircuitElement.VoltageSource import VoltageSource
from CircuitElement.Diode import Diode
from Simulator.Simulator import Simulator
import numpy as np
import matplotlib.pyplot as plt

def main():
    # ノード: 0=GND, 1=入力側, 2=整流後
    ckt = Circuit(num_nodes=3)

    # 入力電圧源（5V振幅、1kHzサイン波）
    ckt.add_element(VoltageSource(1, 0, lambda t: 5.0 * np.sin(2 * np.pi * 1000 * t)))

    # ダイオード（理想モデル）
    ckt.add_element(Diode(1, 2, Is=1e-14, n=1.0, Vt=0.02585))

    # 負荷抵抗と平滑コンデンサ
    ckt.add_element(Resistor(2, 0, 1e3))
    ckt.add_element(Capacitor(2, 0, 470e-6))

    # シミュレーション設定
    sim = Simulator(ckt, dt=1e-6)
    history = sim.run(t_end=0.005)  # 5ms分（5周期くらい）

    # 出力電圧プロット
    plt.plot(np.arange(len(history)) * sim.dt * 1000, history[:, 2])
    plt.title("Half-Wave Rectifier Output")
    plt.xlabel("Time [ms]")
    plt.ylabel("Vout [V]")
    plt.grid(True)
    plt.show()

    print("Sample Vout at end:", history[-1, 2])

if __name__ == "__main__":
    main()
