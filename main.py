import matplotlib.pyplot as plt
import numpy as np

from Simulator.NetlistParser import SpiceParser
from Simulator.Simulator import Simulator

spice_text = """
V1 1 0 SIN(0 5 1k)
D1 1 2 DIODE
R1 2 0 1k
C1 2 0 47u
.model DIODE D(Is=1e-14 n=1.0 Vt=0.02585)
.tran 1e-6 0.005
"""

def main():
    parser = SpiceParser(spice_text)
    ckt, dt, t_end = parser.to_circuit()
    sim = Simulator(ckt, dt)
    history = sim.run(t_end)

    # 出力電圧プロット
    plt.plot(np.arange(len(history)) * sim.dt * 1000, history[:, 2])
    plt.title("Half-Wave Rectifier Output")
    plt.xlabel("Time [ms]")
    plt.ylabel("Vout [V]")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
