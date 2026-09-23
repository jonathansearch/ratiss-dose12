#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DOSE-10 : split-2q (memes angles, 2x portes bruitees) -> gap style-M."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
AMP = [0.4460787069115025, 0.44719883566759633, 0.4460787069115025, 0.4368599914740287,
       0.3827120239843609, 0.23212680322424556, 0.09747745185172646, 0.03661862928022039]
SHOTS = 3000
def cell(split):
    c = QuantumCircuit(6)
    c.initialize(AMP, [0, 1, 2]); c.initialize(AMP, [3, 4, 5])
    for _ in range(2):
        c.rx(0.2, range(6))
        for x, y in ((0, 1), (1, 2), (3, 4), (4, 5)):
            c.rzz(0.2, x, y) if not split else (c.rzz(0.1, x, y), c.rzz(0.1, x, y))
        c.rzz(1.2, 2, 3) if not split else (c.rzz(0.6, 2, 3), c.rzz(0.6, 2, 3))
    return transpile(c, basis_gates=['rz', 'sx', 'x', 'cz'], optimization_level=0)
def zz_of(counts):
    n = sum(counts.values()); z = w = zzw = 0.0
    for k, v in counts.items():
        a = 1 if k[5 - 2] == '0' else -1; b = 1 if k[5 - 3] == '0' else -1
        z += v / n * a; w += v / n * b; zzw += v / n * a * b
    return float(zzw - z * w)
def run_qc(qc, nm):
    tot = {}
    for sd in (7, 123, 999):
        m = qc.copy(); m.measure_all()
        c = AerSimulator(noise_model=nm, seed_simulator=sd).run(m, shots=SHOTS).result().get_counts()
        for k, v in c.items(): tot[k] = tot.get(k, 0) + v
    return tot
nm = NoiseModel()
nm.add_all_qubit_quantum_error(depolarizing_error(0.004, 1), ['rz', 'sx', 'x'])
nm.add_all_qubit_quantum_error(depolarizing_error(0.012, 2), ['cz'])
nm.add_all_qubit_readout_error(ReadoutError([[0.995, 0.005], [0.005, 0.995]]))
zx = zz_of(run_qc(cell(False), None))
zb = zz_of(run_qc(cell(False), nm))
zs = zz_of(run_qc(cell(True), nm))
print(f'exact={zx:.4f} base={zb:.4f} ({zb / zx:.0%}) split2x={zs:.4f} ({zs / zx:.0%})')
OUT = {'zz_exact': round(zx, 4), 'base': round(zb, 4), 'split2x': round(zs, 4)}
json.dump(OUT, open('/home/user/ratiss-dose12/dose-10-gap/dose10.json', 'w'))
plt.figure(figsize=(6, 4))
plt.bar(['base (style-K?)', 'split 2x (style-M?)'], [zb / zx, zs / zx], color=['darkgreen', 'firebrick'])
plt.axhline(0.88, c='darkgreen', ls='--'); plt.axhline(0.60, c='black', ls=':')
plt.ylabel('zz / exact'); plt.title('DOSE-10 : doubler les portes bruitees -> gap M'); plt.tight_layout()
plt.savefig('/home/user/ratiss-dose12/dose-10-gap/fig_dose10.png', dpi=100)
print('[dose10] ok')
