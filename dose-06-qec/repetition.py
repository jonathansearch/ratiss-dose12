#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DOSE-06 : repetition d=3/5 vs physique (seuil), bruit generique."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
SHOTS = 4000
def run_rep(d, p):
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p, 1), ['x', 'id'])
    nm.add_all_qubit_readout_error(ReadoutError([[1 - p, p], [p, 1 - p]]))
    c = QuantumCircuit(d, d)
    c.x(range(d)); c.measure(range(d), range(d))
    counts = AerSimulator(noise_model=nm).run(c, shots=SHOTS, seed_simulator=7).result().get_counts()
    err = sum(v for k, v in counts.items() if k.count('1') < (d + 1) // 2 + (d % 2 == 0)) / SHOTS
    return err
PS = [0.005, 0.01, 0.02, 0.03, 0.05, 0.08]
OUT = {'p': PS, 'phys': [], 'd3': [], 'd5': []}
for p in PS:
    OUT['phys'].append(round(run_rep(1, p), 4))
    OUT['d3'].append(round(run_rep(3, p), 4))
    OUT['d5'].append(round(run_rep(5, p), 4))
    print(f"p={p}: phys={OUT['phys'][-1]} d3={OUT['d3'][-1]} d5={OUT['d5'][-1]}")
json.dump(OUT, open('/home/user/ratiss-dose12/dose-06-qec/dose06.json', 'w'))
plt.figure(figsize=(7, 4))
for k, c in (('phys', 'black'), ('d3', 'steelblue'), ('d5', 'darkgreen')):
    plt.loglog(PS, OUT[k], 'o-', c=c, label={'phys': 'physique', 'd3': 'repetition d=3', 'd5': 'repetition d=5'}[k])
plt.loglog(PS, PS, ':', c='gray', label='y=x')
plt.xlabel('p (depolarisant+readout)'); plt.ylabel('taux erreur logique'); plt.legend(fontsize=8)
plt.title('DOSE-06 : repetition — logique < physique sous le seuil'); plt.grid(True, alpha=0.3); plt.tight_layout()
plt.savefig('/home/user/ratiss-dose12/dose-06-qec/fig_dose06.png', dpi=100)
print('[dose06] ok')
