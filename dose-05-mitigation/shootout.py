#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DOSE-05 : shootout mitigation (brut vs readout vs ZNE), bruit generique."""
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import StatePreparation
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
AMP = [0.4460787069115025, 0.44719883566759633, 0.4460787069115025, 0.4368599914740287,
       0.3827120239843609, 0.23212680322424556, 0.09747745185172646, 0.03661862928022039]
P, Q, SHOTS = 0.005, 0.005, 4000
def cell():
    c = QuantumCircuit(6)
    c.append(StatePreparation(AMP), [0, 1, 2]); c.append(StatePreparation(AMP), [3, 4, 5])
    for _ in range(2):
        c.rx(0.2, range(6))
        for x, y in ((0, 1), (1, 2), (3, 4), (4, 5)): c.rzz(0.2, x, y)
        c.rzz(0.8, 2, 3)
    return c
def zz_of(counts):
    n = sum(counts.values()); z = w = zzw = 0.0
    for k, v in counts.items():
        a = 1 if k[5 - 2] == '0' else -1; b = 1 if k[5 - 3] == '0' else -1
        z += v / n * a; w += v / n * b; zzw += v / n * a * b
    return float(zzw - z * w)
def run_qc(qc, nm):
    m = qc.copy(); m.measure_all()
    return AerSimulator(noise_model=nm, seed_simulator=7).run(m, shots=SHOTS).result().get_counts()
nm = NoiseModel()
nm.add_all_qubit_quantum_error(depolarizing_error(P, 1), ['rz', 'sx', 'x'])
nm.add_all_qubit_quantum_error(depolarizing_error(P * 3, 2), ['cz'])
nm.add_all_qubit_readout_error(ReadoutError([[1 - Q, Q], [Q, 1 - Q]]))
base = transpile(cell(), basis_gates=['rz', 'sx', 'x', 'cz'], optimization_level=1)
zx = zz_of(run_qc(base, None))
zb = zz_of(run_qc(base, nm))
M1 = np.array([[1 - Q, Q], [Q, 1 - Q]])
M = M1
for _ in range(5): M = np.kron(M, M1)
def counts_vec(c):
    v = np.zeros(64)
    for k, val in c.items(): v[int(k, 2)] = val
    return v
raw = counts_vec(run_qc(base, nm))
mit = np.linalg.pinv(M) @ raw
mit = np.clip(mit, 0, None); mit /= mit.sum()
zm = zz_of({format(i, '06b'): mit[i] * SHOTS for i in range(64)})
zs = []
for f in (1, 3, 5):
    cf = base.copy()
    for _ in range((f - 1) // 2): cf = cf.compose(base.inverse()).compose(base)
    zs.append(zz_of(run_qc(cf, nm)))
A = np.vander([1, 3, 5], 2, increasing=True)
zzne = float(np.linalg.lstsq(A, zs, rcond=None)[0][0])
OUT = {'zz_exact': round(zx, 4), 'brut': round(zb, 4), 'readout_mit': round(zm, 4),
       'zne': round(zzne, 4), 'zne_pts': [round(v, 4) for v in zs]}
json.dump(OUT, open('/home/user/ratiss-dose12/dose-05-mitigation/dose05.json', 'w'))
for k in ('brut', 'readout_mit', 'zne'):
    print(f"{k}: zz={OUT[k]} err={abs(OUT[k] - zx):.4f}")
print(f'[dose05] exact={zx:.4f} ok')
plt.figure(figsize=(7, 4))
ks = ['brut', 'readout_mit', 'zne']
plt.bar(ks, [abs(OUT[k] - zx) for k in ks], color=['firebrick', 'orange', 'darkgreen'])
plt.axhline(0.01, c='black', ls=':', label='seuil 0.01')
plt.ylabel('|zz - exact|'); plt.title('DOSE-05 : shootout mitigation (cellule 2L, p=q=0.02)')
plt.legend(); plt.tight_layout()
plt.savefig('/home/user/ratiss-dose12/dose-05-mitigation/fig_dose05.png', dpi=100)
