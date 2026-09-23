#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DOSE-01 : microscope QAOA (MaxCut anneau 6, p=1..6, exact vs bruit K/M)."""
import json, os
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
EDGES = [(i, (i + 1) % 6) for i in range(6)]
SHOTS = 2000
def build_qaoa(p, th):
    c = QuantumCircuit(6)
    c.h(range(6))
    for l in range(p):
        g, b = th[2 * l], th[2 * l + 1]
        for a, x in EDGES:
            c.rzz(2 * g, a, x)
        c.rx(2 * b, range(6))
    return c
def metrics_from_probs(prob):
    C = sum((1 - sum(prob[k] * (1 if (k >> a & 1) == (k >> b & 1) else -1)
                       for k in range(64))) / 2 for a, b in EDGES) / 6
    H = float(-sum(v * np.log2(v) for v in prob if v > 0))
    pl = np.zeros(8); pr = np.zeros(8)
    for k in range(64):
        pl[(k >> 3) & 7] += prob[k]; pr[k & 7] += prob[k]
    HL = float(-sum(v * np.log2(v) for v in pl if v > 0))
    HR = float(-sum(v * np.log2(v) for v in pr if v > 0))
    return C, H, HL + HR - H
def metrics_from_counts(counts):
    n = sum(counts.values())
    prob = np.zeros(64)
    for k, v in counts.items():
        prob[int(k, 2)] = v / n
    return metrics_from_probs(prob)
def negC(th, p):
    sv = Statevector.from_instruction(build_qaoa(p, th))
    return -metrics_from_probs(sv.probabilities())[0]
OUT = {}
service = QiskitRuntimeService(channel='ibm_quantum_platform', token=os.environ['IBM_TOKEN'])
BES = {'K': ('ibm_kingston', [10, 11, 18, 9, 31, 30]), 'M': ('ibm_marrakesh', [5, 6, 4, 3, 7, 8])}
sims = {}
for tag, (name, chain) in BES.items():
    be = service.backend(name)
    sims[tag] = (AerSimulator.from_backend(be),
                 generate_preset_pass_manager(backend=be, optimization_level=1, initial_layout=chain))
print('p | r_ex r_K r_M | H_ex H_K H_M | MI_ex MI_K MI_M | depth_K')
for p in range(1, 7):
    best = min((minimize(negC, x0=x0, args=(p,), method='COBYLA',
                         options={'maxiter': 300}) for x0 in
                (np.tile([0.4, 0.4], p), np.tile([0.7, 0.2], p))), key=lambda r: r.fun)
    th = best.x
    sv = Statevector.from_instruction(build_qaoa(p, th))
    rex, Hex, MIex = metrics_from_probs(sv.probabilities())
    row = {'theta': [round(float(t), 4) for t in th], 'exact': [round(rex, 4), round(Hex, 3), round(MIex, 3)]}
    line = f'{p} | {rex:.3f}'
    for tag in ('K', 'M'):
        sim, pm = sims[tag]
        m = build_qaoa(p, th).copy()
        m.measure_all()
        t = pm.run(m)
        counts = sim.run(t, shots=SHOTS, seed_simulator=7).result().get_counts()
        r, H, MI = metrics_from_counts(counts)
        row[tag] = [round(r, 4), round(H, 3), round(MI, 3)]
        line += f' {r:.3f}'
    OUT[p] = row
    rK, HK, MIK = row['K']
    rM, HM, MIM = row['M']
    print(f'{p} | {rex:.3f} {rK:.3f} {rM:.3f} | {Hex:.2f} {HK:.2f} {HM:.2f} | {MIex:.3f} {MIK:.3f} {MIM:.3f} | {pm.run(build_qaoa(p, th)).depth()}')
json.dump(OUT, open('/home/user/ratiss-dose12/dose-01-qaoa/dose01.json', 'w'), indent=0)
print('[dose01] ok')
