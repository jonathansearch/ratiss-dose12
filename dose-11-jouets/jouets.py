#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DOSE-11 : sweep k autour de 0.108 (S03) — rebond robuste ? (base: s03_base.py)."""
import json
import numpy as np
src = open('/home/user/ratiss-dose12/dose-11-jouets/s03_base.py').read().split('out = {}')[0]
ns = {}
exec(src, ns)
run, G = ns['run'], ns['G']
OUT = {}
for tag, k in (('GR_k0', 0.0), ('k08', 0.0864), ('k10', 0.108), ('k12', 0.1296)):
    s = run(k)
    OUT[tag] = {'r_min': round(min(r['r_rms'] for r in s), 3),
                'r_fin': round(s[-1]['r_rms'], 3),
                'rho_max': round(max(r['rho'] for r in s), 1),
                'H1_init': round(s[0]['H1'], 2), 'H1_fin': round(s[-1]['H1'], 3),
                'retour_H1': round(s[-1]['H1'] / s[0]['H1'] if s[0]['H1'] else 0, 3),
                'r_eq_theorie': round(float(np.sqrt(k / G)) if k else 0.0, 3)}
    print(tag, OUT[tag], flush=True)
json.dump(OUT, open('/home/user/ratiss-dose12/dose-11-jouets/dose11.json', 'w'), indent=0)
print('[dose11] ok')
