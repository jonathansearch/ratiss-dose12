#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""GCR-V : ultra-collision de 2 murs tanh dans nappe libre 2D (N=256).
Micro-loi S03 : F=-g/r2+k/r4 (coeur Planck k=0.108 = RAIDEUR du tissu)
+ friction gamma. Murs cinematiques : F=+-A*exp(-((x-xw)/w)^2).
Detecteur : beta1 exact (Euler sur Delaunay : b1=1-V+E-T) + E_kin + densite.
Brutalite B = v_rel/w. Unites jouet (pas de GeV : capacite a deformer)."""
import numpy as np
from scipy.spatial import Delaunay

def alpha_beta1(X, alpha=0.5):
    """beta1 du complexe alpha (trous = mailles etirees > alpha)."""
    try:
        T = Delaunay(X).simplices
    except Exception:
        return float('nan'), float('nan')
    keep = []
    for a, b, c in T:
        pa, pb, pc = X[a], X[b], X[c]
        la, lb, lc = (float(((pb-pc)**2).sum())**0.5,
                      float(((pa-pc)**2).sum())**0.5,
                      float(((pa-pb)**2).sum())**0.5)
        ar = abs((pb[0]-pa[0])*(pc[1]-pa[1])-(pc[0]-pa[0])*(pb[1]-pa[1]))/2
        R = la*lb*lc/max(4*ar, 1e-12)
        if R < alpha:
            keep.append((a, b, c))
    if not keep:
        return 0, 1.0
    E = set()
    V = set()
    parent = {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b, c in keep:
        for q in (a, b, c):
            V.add(q)
            if q not in parent:
                parent[q] = q
        for u, v in ((a, b), (b, c), (a, c)):
            E.add((u, v) if u < v else (v, u))
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
    b0 = len({find(q) for q in V})
    b1 = b0 - len(V) + len(E) - len(keep)
    return b1, 1-len(keep)/len(T)

def run(v_rel, w, A=3.0, x0=4.0, n_side=16, g=0.3, k=0.108, gamma=0.3,
        dt=0.01, seed=7, Fmax_log=None, sample_every=10, snap_every=0):
    rng = np.random.default_rng(seed)
    L = np.linspace(-3, 3, n_side)
    gx, gy = np.meshgrid(L, L)
    X = np.column_stack([gx.ravel(), gy.ravel()]) + rng.normal(0, 0.02, (n_side**2, 2))
    V = np.zeros_like(X)
    v = v_rel/2
    T = int(2*(x0/v)/dt)+400 if v > 0 else 800
    for _ in range(600):  # EQUILIBRAGE sans murs (etat initial physique)
        d = X[:, None, :] - X[None, :, :]
        r = np.sqrt((d**2).sum(-1))
        np.fill_diagonal(r, 1e9)
        rs = np.maximum(r, 0.2)
        f = (-g/rs**2 + k/rs**4)/rs
        F = (f[:, :, None]*d).sum(1) - gamma*V
        V += F*dt
        X += V*dt
    eq_ekin = float(0.5*(V**2).sum())
    series, snaps = [], {}
    for n in range(T):
        t = n*dt
        d = X[:, None, :] - X[None, :, :]
        r = np.sqrt((d**2).sum(-1))
        np.fill_diagonal(r, 1e9)
        rs = np.maximum(r, 0.2)  # soft-core S01 (anti-explosion)
        f = (-g/rs**2 + k/rs**4)/rs
        F = (f[:, :, None]*d).sum(1)
        F[:, 0] += A*np.exp(-((X[:, 0]-(-x0+v*t))/w)**2)
        F[:, 0] -= A*np.exp(-((X[:, 0]-(x0-v*t))/w)**2)
        F -= gamma*V
        fn = np.sqrt((F**2).sum(1))
        clips = int((fn > 200).sum())
        F *= np.minimum(1, 200/np.maximum(fn, 1e-9))[:, None]
        V += F*dt
        X += V*dt
        if snap_every and n % snap_every == 0:
            snaps[round(t,3)] = X.copy()
        if n % sample_every == 0:
            dd = np.sort(r, axis=1)[:, 5]
            b1, drop = alpha_beta1(X)
            if Fmax_log is not None:
                Fmax_log.append(clips)
            series.append({'t': round(t, 3), 'b1': b1, 'drop': round(drop, 4),
                           'ekin': round(float(0.5*(V**2).sum()), 3),
                           'vmax': round(float(np.sqrt((V**2).sum(1)).max()), 3),
                           'd5min': round(float(dd.min()), 4)})
    return series, eq_ekin, snaps

def etincelle(series):
    b = np.array([s['b1'] for s in series], float)
    e = np.array([s['ekin'] for s in series], float)
    base = np.nanmedian(b[:10])
    bmax = np.nanmax(b)
    imax = int(np.nanargmax(b))
    thr = max(base+1, 1.5)
    up = np.where(b >= max(bmax/2, thr))[0] if bmax >= thr else []
    if len(up):
        j = np.where(up == np.arange(up[0], up[0]+len(up)))[0]
        vie = (len(j)*10*0.02) if len(j) else 0.0
    else:
        vie = 0.0
    t_rel = None
    for s in series[imax:]:
        if s['b1'] <= base:
            t_rel = round(s['t']-series[imax]['t'], 2)
            break
    return {'b1_base': float(base), 'b1_max': float(bmax),
            't_pic': series[imax]['t'], 'etincelle': bool(bmax >= thr),
            'vie': round(vie, 2), 'T_relax': t_rel,
            'ekin_burst': round(float(e.max()/max(np.median(e[:10]), 1e-9)), 1)}
