#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DOSE-07 : GCR-V4 boite fermee (derive de GCR/univers/collision.py, MIT, meme auteur).
MODS V4 : boite reflechissante +-BOXM + suivi E_tot (U=-g/r+k/3r3) + gamma=0."""
import json
import numpy as np
from scipy.spatial import Delaunay
from gcrv4_base import alpha_beta1, etincelle
BOXM = 3.2
def run_v4(v_rel, w, A=3.0, x0=4.0, n_side=16, g=0.3, k=0.108, gamma=0.0, dt=0.01, seed=7):
    rng = np.random.default_rng(seed)
    L = np.linspace(-3, 3, n_side)
    gx, gy = np.meshgrid(L, L)
    X = np.column_stack([gx.ravel(), gy.ravel()]) + rng.normal(0, 0.02, (n_side**2, 2))
    V = np.zeros_like(X)
    def box():
        over = np.abs(X) > BOXM
        X[over] = np.sign(X[over]) * (2 * BOXM - np.abs(X[over]))
        V[over] *= -1
    def epot_of(rs):
        U = -g / rs + k / (3 * rs**3)
        return float(U.sum() / 2)
    v = v_rel / 2
    T = int(2 * (x0 / v) / dt) + 400 if v > 0 else 800
    for _ in range(600):
        d = X[:, None, :] - X[None, :, :]
        r = np.sqrt((d**2).sum(-1)); np.fill_diagonal(r, 1e9)
        rs = np.maximum(r, 0.2)
        f = (-g / rs**2 + k / rs**4) / rs
        F = (f[:, :, None] * d).sum(1) - gamma * V
        V += F * dt; X += V * dt; box()
    d = X[:, None, :] - X[None, :, :]
    r = np.sqrt((d**2).sum(-1)); np.fill_diagonal(r, 1e9)
    E_ref = float(0.5 * (V**2).sum()) + epot_of(np.maximum(r, 0.2))
    series = []
    for n in range(T):
        t = n * dt
        d = X[:, None, :] - X[None, :, :]
        r = np.sqrt((d**2).sum(-1)); np.fill_diagonal(r, 1e9)
        rs = np.maximum(r, 0.2)
        f = (-g / rs**2 + k / rs**4) / rs
        F = (f[:, :, None] * d).sum(1)
        F[:, 0] += A * np.exp(-((X[:, 0] - (-x0 + v * t)) / w)**2)
        F[:, 0] -= A * np.exp(-((X[:, 0] - (x0 - v * t)) / w)**2)
        F -= gamma * V
        fn = np.sqrt((F**2).sum(1))
        F *= np.minimum(1, 200 / np.maximum(fn, 1e-9))[:, None]
        V += F * dt; X += V * dt; box()
        if n % 10 == 0:
            b1, drop = alpha_beta1(X)
            E = float(0.5 * (V**2).sum()) + epot_of(rs)
            series.append({'t': round(t, 3), 'b1': b1, 'E': round(E, 3)})
    Es = np.array([s['E'] for s in series])
    drift = float(np.abs(Es - E_ref).max() / max(abs(E_ref), 1e-9))
    an = etincelle([{'t': s['t'], 'b1': s['b1'], 'ekin': 0} for s in series])
    return {'b1_max': an['b1_max'], 'vie': an['vie'], 'etincelle': an['etincelle'],
            'E_ref': round(E_ref, 2), 'E_fin': round(float(Es[-1]), 2), 'drift': round(drift, 5)}
OUT = {}
for tag, kw in (('temoin', dict(v_rel=0.0, w=0.5, A=0.0)),
                ('spark_v3_A10', dict(v_rel=3.0, w=0.5, A=10.0)),
                ('spark_v5_A20', dict(v_rel=5.0, w=0.5, A=20.0))):
    OUT[tag] = run_v4(**kw)
    print(tag, OUT[tag], flush=True)
json.dump(OUT, open('/home/user/ratiss-dose12/dose-07-gcrv4/dose07.json', 'w'), indent=0)
print('[dose07] ok')
