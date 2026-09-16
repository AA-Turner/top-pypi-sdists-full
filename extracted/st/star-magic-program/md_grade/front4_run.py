"""front4_run.py - equilibrate a TIP4P/2005 box with md_engine, then production
with on-the-fly transverse current j_T(k,t) for every integer k-shell up to n2max.
Writes a checkpoint .npz every N samples; analysis is in front4_analyze.py.
usage: python front4_run.py <n_side> <prod_ps> <tag> [n2max]
"""
import sys, time, math, numpy as np
from md_engine import Water, KB, M_O, M_H

n_side = int(sys.argv[1]); prod_ps = float(sys.argv[2]); tag = sys.argv[3]
n2max = int(sys.argv[4]) if len(sys.argv) > 4 else 30
w = Water(n_side, T=298.0, rc=0.9, seed=11)
L = w.L; N = w.N
log = open(f'f4_{tag}.log', 'w')
def P(*a):
    print(*a, file=log, flush=True)
P('N', N, 'L', round(L, 4), 'nm  k_min', round(2 * math.pi / L, 3), 'nm^-1  rc', w.rc)

# ---- equilibration: soft start, then Berendsen ----
t0 = time.time()
w.run(400, dt=0.0005, tau_T=0.05)
w.run(2500, dt=0.001, tau_T=0.1)
def cb(step, E):
    if step % 500 == 0: P('eq step', step, 'T %.1f' % w.temperature(), 'E/N %.2f' % (E / N), '%.0f s' % (time.time() - t0))
w.run(10000, dt=0.002, tau_T=0.2, callback=cb, cb_every=500)    # 20 ps
w.run(10000, dt=0.002, tau_T=1.0, callback=cb, cb_every=500)    # 20 ps, weaker
P('equilibrated: T %.1f  E/N %.2f  %.0f s' % (w.temperature(), w.run(1, dt=0.002) / N, time.time() - t0))

# ---- k-vectors: half-space integer n with 1 <= |n|^2 <= n2max ----
nv = []
r = int(math.sqrt(n2max)) + 1
for nx in range(-r, r + 1):
    for ny in range(-r, r + 1):
        for nz in range(0, r + 1):
            n2 = nx * nx + ny * ny + nz * nz
            if n2 == 0 or n2 > n2max: continue
            if nz == 0 and (ny < 0 or (ny == 0 and nx < 0)): continue
            nv.append((nx, ny, nz))
nv = np.array(nv, float); n2 = (nv ** 2).sum(1).astype(int)
kvec = nv * (2 * math.pi / L)
# transverse basis
ref = np.where(np.abs(kvec[:, 2:3]) < 0.9 * np.linalg.norm(kvec, axis=1, keepdims=True), [[0, 0, 1.0]], [[1.0, 0, 0]])
e1 = np.cross(kvec, ref); e1 /= np.linalg.norm(e1, axis=1, keepdims=True)
e2 = np.cross(kvec, e1); e2 /= np.linalg.norm(e2, axis=1, keepdims=True)
P('k-vectors', len(kvec), 'shells', sorted(set(n2.tolist())))

# ---- production: sample every 10 steps (20 fs) ----
dt = 0.002; every = 10
nsamp = int(prod_ps / (dt * every))
J = np.zeros((nsamp, len(kvec), 2), np.complex64)
com0 = None; msd_t = []; msd = []
mass = np.array([M_O, M_H, M_H])
s = 0
def sample(step, E):
    global s, com0
    if s >= nsamp: return
    r = w.pos.reshape(-1, 3); v = w.v.reshape(-1, 3); m = np.tile(mass, N)
    ph = np.exp(1j * (r @ kvec.T))                     # (3N, K)
    mv = m[:, None] * v
    J[s, :, 0] = np.einsum('nk,nk->k', ph, mv @ e1.T)
    J[s, :, 1] = np.einsum('nk,nk->k', ph, mv @ e2.T)
    com = (w.pos * mass[None, :, None]).sum(1) / mass.sum()
    if com0 is None: com0 = com.copy()
    if s % 50 == 0:
        msd_t.append(s * dt * every); msd.append(float(((com - com0) ** 2).sum(1).mean()))
    if s % 500 == 0:
        P('prod sample', s, '/', nsamp, 'T %.1f' % w.temperature(), 'E/N %.2f' % (E / N), '%.0f s' % (time.time() - t0))
        np.savez_compressed(f'f4_{tag}_ckpt.npz', J=J[:s], kvec=kvec, n2=n2, L=L, N=N, dt=dt * every, msd_t=msd_t, msd=msd, T=w.temperature())
    s += 1
w.run(nsamp * every, dt=dt, tau_T=5.0, callback=sample, cb_every=every)
np.savez_compressed(f'f4_{tag}.npz', J=J, kvec=kvec, n2=n2, L=L, N=N, dt=dt * every, msd_t=msd_t, msd=msd, T=w.temperature())
P('DONE', nsamp, 'samples', '%.0f s' % (time.time() - t0))
