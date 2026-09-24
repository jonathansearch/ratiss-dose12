"""Vrais visuels animés du repo (matplotlib -> GIF). Données : dose-02 (H2 VQE),
dose-09 (QV) = RÉELLES ; Si diamant Fd-3m (banque Mat3ra) + phonon illustratif."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

R = '/home/user/ratiss-dose12'
OUT = R + '/visuals'
import os
os.makedirs(OUT, exist_ok=True)

# ---------- GIF 1 : H2 VQE (courbes RÉELLES dose-02) ----------
d02 = json.load(open(R + '/dose-02-vqe/dose02.json'))
ds = np.array(sorted(float(k) for k in d02))
series = {'E0 exact': [d02[str(d)]['E0'] for d in ds],
          'VQE exact': [d02[str(d)]['Evqe'] for d in ds],
          'K bruité': [d02[str(d)]['K'] for d in ds],
          'M bruité': [d02[str(d)]['M'] for d in ds]}
fig, ax = plt.subplots(figsize=(5, 3.2), dpi=80)
lines = {k: ax.plot([], [], 'o-', ms=3, label=k)[0] for k in series}
ax.set_xlim(0.3, 2.7); ax.set_ylim(-2.2, -1.05)
ax.set_xlabel('distance H-H (Å)'); ax.set_ylabel('énergie (Ha)')
ax.set_title('H2 VQE — données RÉELLES dose-02'); ax.legend(fontsize=7); ax.grid(alpha=0.3)
NF = 60
xs = np.linspace(ds[0], ds[-1], NF)
ys = {k: np.interp(xs, ds, v) for k, v in series.items()}
def f1(i):
    for k, ln in lines.items():
        ln.set_data(xs[:i + 1], ys[k][:i + 1])
    return list(lines.values())
FuncAnimation(fig, f1, frames=NF, interval=60).save(OUT + '/h2_vqe.gif', writer='pillow')
plt.close(fig)

# ---------- GIF 2 : Si diamant + phonon (structure RÉELLE, dyna. illust.) ----------
a = 5.431  # Si diamant, Fd-3m (banque Mat3ra)
base = np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0],
                 [.25, .25, .25], [.25, .75, .75], [.75, .25, .75], [.75, .75, .25]]) * a
subs = np.array([0, 0, 0, 0, 1, 1, 1, 1])  # 2 sous-réseaux
cells = np.array([[i, j, k] for i in range(2) for j in range(2) for k in range(2)]) * a
P = np.array([b + c for c in cells for b in base])
S = np.tile(subs, 8)
u = np.array([1, 1, 1]) / np.sqrt(3)
fig = plt.figure(figsize=(4.2, 4.2), dpi=80)
ax = fig.add_subplot(111, projection='3d')
NF = 48
def f2(i):
    ax.clear()
    t = 2 * np.pi * i / NF
    Q = P + (0.35 * np.sin(t)) * u * (1 - 2 * S)[:, None]
    ax.scatter(Q[:, 0], Q[:, 1], Q[:, 2], c=np.where(S == 0, 'royalblue', 'tomato'), s=18)
    # liaisons 1er voisin (< 2.6 Å)
    for n in range(len(Q)):
        d = np.linalg.norm(Q - Q[n], axis=1)
        for m in np.where((d > 0.1) & (d < 2.6))[0]:
            if m > n:
                ax.plot([Q[n, 0], Q[m, 0]], [Q[n, 1], Q[m, 1]], [Q[n, 2], Q[m, 2]], 'k-', lw=0.4, alpha=0.5)
    ax.set_title('Si diamant Fd-3m — phonon optique')
    ax.view_init(elev=18, azim=i * 360 / NF)
    ax.set_axis_off()
    return []
FuncAnimation(fig, f2, frames=NF, interval=70).save(OUT + '/si_phonon.gif', writer='pillow')
plt.close(fig)

# ---------- GIF 3 : Rabi sur Bloch (sim, illustratif) ----------
fig = plt.figure(figsize=(5.4, 2.8), dpi=80)
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122)
th = np.linspace(0, 2 * np.pi, 40); ph = np.linspace(0, np.pi, 20)
X = np.outer(np.cos(th), np.sin(ph)); Y = np.outer(np.sin(th), np.sin(ph)); Z = np.outer(np.ones(40), np.cos(ph))
tt = np.linspace(0, 4 * np.pi, 80)
NF = 80
def f3(i):
    ax1.clear(); ax2.clear()
    ax1.plot_wireframe(X, Y, Z, color='gray', alpha=0.15, linewidths=0.4)
    t = tt[i]
    v = np.array([np.sin(t) * np.sin(0.6 * t), np.sin(t) * np.cos(0.6 * t), np.cos(t)])
    ax1.quiver(0, 0, 0, *v, color='crimson', length=1.0, arrow_length_ratio=0.15)
    ax1.set_title('Rabi — sphère de Bloch'); ax1.set_axis_off(); ax1.view_init(elev=15, azim=i * 2)
    ax2.plot(tt[:i + 1], (1 - np.cos(tt[:i + 1])) / 2, 'b-')
    ax2.set_xlim(0, 4 * np.pi); ax2.set_ylim(-0.05, 1.05)
    ax2.set_xlabel('temps'); ax2.set_ylabel('P(|1>)'); ax2.grid(alpha=0.3)
    return []
FuncAnimation(fig, f3, frames=NF, interval=50).save(OUT + '/rabi.gif', writer='pillow')
plt.close(fig)
print('[viz] ok')
