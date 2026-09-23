#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DOSE-03 v2 : Rips de la variete dose->reponse (frais, bruit generique)."""
import json
import numpy as np
from ripser import ripser
from persim import bottleneck
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
AMP = [0.4460787069115025, 0.44719883566759633, 0.4460787069115025, 0.4368599914740287,
       0.3827120239843609, 0.23212680322424556, 0.09747745185172646, 0.03661862928022039]
SHOTS = 2000
def fresh_noise(p, q):
    nm = NoiseModel()
    nm.add_all_qubit_quantum_error(depolarizing_error(p, 1), ['rz', 'sx', 'x', 'ry', 'h'])
    nm.add_all_qubit_quantum_error(depolarizing_error(p * 3, 2), ['cx', 'cz', 'rzz'])
    nm.add_all_qubit_readout_error(ReadoutError([[1 - q, q], [q, 1 - q]]))
    return nm
NOISE = {'exact': None, 'faible': fresh_noise(0.01, 0.005), 'fort': fresh_noise(0.04, 0.03)}
def cell(lam, nl):
    c = QuantumCircuit(6)
    c.initialize(AMP, [0, 1, 2]); c.initialize(AMP, [3, 4, 5])
    for _ in range(nl):
        c.rx(0.2, range(6))
        for x, y in ((0, 1), (1, 2), (3, 4), (4, 5)): c.rzz(0.2, x, y)
        if lam: c.rzz(lam, 2, 3)
    return c
def hist(counts):
    n = sum(counts.values()); h = np.zeros(64)
    for k, v in counts.items(): h[int(k, 2)] = v / n
    return h
def run_circ(qc, nm):
    m = qc.copy(); m.measure_all()
    c = AerSimulator(noise_model=nm).run(m, shots=SHOTS, seed_simulator=7).result().get_counts()
    return hist(c)
GRID = [(lam, nl) for lam in (0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6) for nl in (1, 2, 3, 4)]
def hellinger(H):
    S = np.sqrt(H)
    G = S @ S.T
    return np.sqrt(np.maximum(0.0, 1 - G))
OUT = {}
for tag, nm in NOISE.items():
    H = np.array([run_circ(cell(lam, nl), nm) for lam, nl in GRID])
    D = hellinger(H)
    dg = ripser(D, maxdim=1, distance_matrix=True)['dgms']
    h0 = dg[0][np.isfinite(dg[0][:, 1])]; h1 = dg[1]
    tp0 = float((h0[:, 1] - h0[:, 0]).sum()) if len(h0) else 0.0
    tp1 = float((h1[:, 1] - h1[:, 0]).sum()) if len(h1) else 0.0
    OUT[tag] = {'H0_n': int(len(h0)), 'H0_persist': round(tp0, 3), 'H1_n': int(len(h1)),
                'H1_persist': round(tp1, 3), 'H1_max': round(float((h1[:, 1] - h1[:, 0]).max()) if len(h1) else 0.0, 3),
                'diam': round(float(D.max()), 3)}
    OUT[tag]['H'] = H.tolist()
    print(f"{tag}: H0 n={len(h0)} persist={tp0:.3f} | H1 n={len(h1)} persist={tp1:.3f} max={OUT[tag]['H1_max']} | diam={D.max():.3f}")
json.dump({t: {k: v for k, v in d.items()} for t, d in OUT.items()}, open('/home/user/ratiss-dose12/dose-03-rips/dose03.json', 'w'), indent=0)
print('[dose03] ok')
