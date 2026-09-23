#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DOSE-04 : canari virtuel (prediciton calib -> verif simu fraiche)."""
import json, os
import numpy as np
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService(channel='ibm_quantum_platform', token=os.environ['IBM_TOKEN'])
CHAINS = {'K': ('ibm_kingston', [10, 11, 18, 9, 31, 30]), 'M': ('ibm_marrakesh', [5, 6, 4, 3, 7, 8])}
OUT = {}
for tag, (name, ch) in CHAINS.items():
    be, P = service.backend(name), service.backend(name).properties()
    ro = [P.readout_error(q) for q in ch]
    t1 = [P.t1(q) for q in ch]
    g2 = []
    for a, b in zip(ch[:-1], ch[1:]):
        for gn in ('cz', 'ecr', 'cx'):
            try: g2.append(P.gate_error(gn, [a, b])); break
            except Exception: pass
    S = float(1 / (1 + 100 * (float(np.mean(ro)) + float(np.mean(g2)))))
    OUT[tag] = {'readout_moy': round(float(np.mean(ro)), 5), 't1_moy_us': round(float(np.mean(t1)) * 1e6, 1),
                'g2_moy': round(float(np.mean(g2)), 5), 'SANTE_S': round(S, 4)}
    print(f"{tag} ({name}, chaine {ch}): readout={np.mean(ro):.4f} T1={np.mean(t1) * 1e6:.0f}us 2q={np.mean(g2):.4f} -> S={S:.4f}")
json.dump(OUT, open('/home/user/ratiss-dose12/dose-04-canari/dose04.json', 'w'), indent=0)
print(f"PREDICTION PRE-ENREGISTREE 2026-09-24 : K meilleur que M par S_K/S_M = {OUT['K']['SANTE_S'] / OUT['M']['SANTE_S']:.2f} (a verifier au prochain tir reel)")
print('[dose04] ok')
