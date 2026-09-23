#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DOSE-09 : meme budget erreur, destins differents (portes vs readout)."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
AMP = [0.4460787069115025, 0.44719883566759633, 0.4460787069115025, 0.4368599914740287,
       0.3827120239843609, 0.23212680322424556, 0.09747745185172646, 0.03661862928022039]
SHOTS = 3000
def cell(lam):
    c = QuantumCircuit(6)
    c.initialize(AMP, [0, 1, 2]); c.initialize(AMP, [3, 4, 5])
    for _ in range(2):
        c.rx(0.2, range(6))
        for x, y in ((0, 1), (1, 2), (3, 4), (4, 5)): c.rzz(0.2, x, y)
        if lam: c.rzz(lam, 2, 3)
    return transpile(c, basis_gates=['rz', 'sx', 'x', 'cz'], optimization_level=1)
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
nD = NoiseModel()
nD.add_all_qubit_quantum_error(depolarizing_error(0.02, 1), ['rz', 'sx', 'x'])
nD.add_all_qubit_quantum_error(depolarizing_error(0.06, 2), ['cz'])
nR = NoiseModel()
nR.add_all_qubit_readout_error(ReadoutError([[0.98, 0.02], [0.02, 0.98]]))
OUT = {}
for lam in (0.0, 0.4, 0.8, 1.2, 1.6):
    zx = zz_of(run_qc(cell(lam), None))
    zd = zz_of(run_qc(cell(lam), nD))
    zr = zz_of(run_qc(cell(lam), nR))
    OUT[str(lam)] = [round(zx, 4), round(zd, 4), round(zr, 4)]
    print(f'lam={lam}: exact={zx:.3f} portes={zd:.3f} readout={zr:.3f}')
json.dump(OUT, open('/home/user/ratiss-dose12/dose-09-qv/dose09.json', 'w'))
xs = sorted(float(k) for k in OUT)
plt.figure(figsize=(7, 4))
plt.plot(xs, [OUT[str(v)][0] for v in xs], 's--k', label='exact')
plt.plot(xs, [OUT[str(v)][1] for v in xs], 'o-', c='firebrick', label='bruit PORTES (2%)')
plt.plot(xs, [OUT[str(v)][2] for v in xs], 'o-', c='steelblue', label='bruit READOUT (2%)')
plt.xlabel('lambda'); plt.ylabel('zz'); plt.legend(fontsize=8); plt.grid(True, alpha=0.3)
plt.title('DOSE-09 : meme budget 2%, destins differents'); plt.tight_layout()
plt.savefig('/home/user/ratiss-dose12/dose-09-qv/fig_dose09.png', dpi=100)
print('[dose09] ok')
