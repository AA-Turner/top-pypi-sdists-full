"""front4_record.py - the front-4 RECORD RUN: rigid TIP4P/2005 water with SPME (md_pme.WaterPME),
transverse currents j_T(k,t) on ATOMS and on molecular CENTRES OF MASS every `every` steps (B-spline/FFT
momentum-density transform, gridcur.GridCurrents, validated against the exact sum: 3.5e-3 rms at k 12-14.5), with an
on-the-fly autocorrelator (lags to tmax_lag) accumulated per block for error bars; multi-origin MSD
subset for D; checkpoint/restart.
usage: python front4_record.py <n_side> <prod_ps> <tag> [--restart] [--every 2] [--seed 11] [--cap 40] [--nshell 40]
"""
import sys, os, time, math, argparse, numpy as np, ctypes
from md_pme import WaterPME, _lib, _dp
from gridcur import GridCurrents
from md_engine import KB, M_O, M_H

ap = argparse.ArgumentParser()
ap.add_argument('n_side', type=int); ap.add_argument('prod_ps', type=float); ap.add_argument('tag')
ap.add_argument('--restart', action='store_true'); ap.add_argument('--every', type=int, default=2)
ap.add_argument('--seed', type=int, default=11); ap.add_argument('--cap', type=int, default=40); ap.add_argument('--nshell', type=int, default=40)
ap.add_argument('--kmax', type=float, default=14.0); ap.add_argument('--tlag', type=float, default=10.0)
ap.add_argument('--nblock', type=int, default=6); ap.add_argument('--fine_lag', type=float, default=0.8); ap.add_argument('--coarse', type=int, default=10); ap.add_argument('--ckpt_ps', type=float, default=10.0)
A = ap.parse_args()
_lib.currents.argtypes = [ctypes.c_int, _dp, _dp, _dp, ctypes.c_int, _dp, _dp, _dp, _dp]
log = open(f'rec_{A.tag}.log', 'a')
def P(*a):
    print(*a, file=log, flush=True)

w = WaterPME(A.n_side, T=298.0, rc=0.9, seed=A.seed, alpha=3.5, grid_spacing=0.1, order=4)
L, N = w.L, w.N
dt = 0.002; every = A.every; dts = dt * every
nring = int(round(A.tlag / dts)) + 1
nfine = int(round(A.fine_lag / dts))
lags = np.concatenate([np.arange(0, nfine + 1), np.arange(nfine + A.coarse, nring, A.coarse)])   # fine to fine_lag, then every `coarse` samples
nlag = len(lags)
nsamp = int(round(A.prod_ps / dts))
# ---- k-vectors: all half-space integer n with |k| <= kmax, capped per n^2 shell ----
rng = np.random.default_rng(1234)
nmax = int(A.kmax * L / (2 * math.pi)) + 1
shells = {}
for nx in range(-nmax, nmax + 1):
    for ny in range(-nmax, nmax + 1):
        for nz in range(0, nmax + 1):
            n2 = nx * nx + ny * ny + nz * nz
            if n2 == 0 or math.sqrt(n2) * 2 * math.pi / L > A.kmax: continue
            if nz == 0 and (ny < 0 or (ny == 0 and nx < 0)): continue
            shells.setdefault(n2, []).append((nx, ny, nz))
keys = sorted(shells)
if len(keys) > A.nshell:                       # log-spaced selection of n^2 shells between k_min and kmax
    targets = np.exp(np.linspace(math.log(keys[0]), math.log(keys[-1]), A.nshell))
    sel = sorted(set(min(keys, key=lambda x: abs(math.log(x) - math.log(t))) for t in targets))
    keys = sel
nv = []; n2l = []
for n2 in keys:
    vs = shells[n2]
    if len(vs) > A.cap: vs = [vs[i] for i in rng.choice(len(vs), A.cap, replace=False)]
    nv += vs; n2l += [n2] * len(vs)
nv = np.array(nv, float); n2 = np.array(n2l); kvec = np.ascontiguousarray(nv * (2 * math.pi / L))
ref = np.where(np.abs(kvec[:, 2:3]) < 0.9 * np.linalg.norm(kvec, axis=1, keepdims=True), [[0, 0, 1.0]], [[1.0, 0, 0]])
e1 = np.cross(kvec, ref); e1 /= np.linalg.norm(e1, axis=1, keepdims=True); e1 = np.ascontiguousarray(e1)
e2 = np.cross(kvec, e1); e2 /= np.linalg.norm(e2, axis=1, keepdims=True); e2 = np.ascontiguousarray(e2)
K = len(kvec)
gc = GridCurrents(L, w.K, nv, e1, e2)
mass3 = np.array([M_O, M_H, M_H]); mA = np.ascontiguousarray(np.tile(mass3, N)); mC = np.full(N, mass3.sum())
msd_sub = min(N, 2000); msd_every = int(round(0.5 / dts))

ck = f'rec_{A.tag}_ckpt.npz'
if A.restart and os.path.exists(ck):
    z = np.load(ck)
    w.pos = z['pos']; w.v = z['v']; s0 = int(z['s']); unwrap = z['unwrap']
    CA = z['CA']; CC = z['CC']; nacc = z['nacc']; ringA = z['ringA']; ringC = z['ringC']; ringpos = int(z['ringpos']); ringfill = int(z['ringfill'])
    comtraj = list(z['comtraj']); Tacc = list(z['Tacc']); Eacc = list(z['Eacc'])
    assert z['K'] == K and abs(float(z['L']) - L) < 1e-9 and np.array_equal(z['lags'], lags)
    P('RESTART at sample', s0, 'of', nsamp, 'T %.1f' % w.temperature())
else:
    P('N', N, 'L %.4f nm  k_min %.4f  K %d vectors in %d shells (cap %d, nshell %d)  kmax %.1f  sample every %d steps (%.1f fs)  lags %d (fine to %.1f ps, then every %d samples to %.1f ps)  blocks %d  grid K %d  seed %d' %
      (L, 2 * math.pi / L, K, len(set(n2l)), A.cap, A.nshell, A.kmax, every, dts * 1000, nlag, A.fine_lag, A.coarse, A.tlag, A.nblock, w.K, A.seed))
    t0 = time.time()
    w.run(400, dt=0.0005, tau_T=0.05); w.run(1500, dt=0.001, tau_T=0.1)
    def cb(step, E):
        if step % 1000 == 0: P('eq step', step, 'T %.1f' % w.temperature(), 'E/N %.3f' % (E / N), '%.0f s' % (time.time() - t0))
    w.run(10000, dt=0.002, tau_T=0.2, callback=cb, cb_every=1000)      # 20 ps
    w.run(10000, dt=0.002, tau_T=1.0, callback=cb, cb_every=1000)      # 20 ps
    P('equilibrated: T %.1f  E/N %.3f  %.0f s' % (w.temperature(), w.forces()[1] / N, time.time() - t0))
    s0 = 0
    CA = np.zeros((A.nblock, K, 2, nlag), np.complex128); CC = np.zeros_like(CA); nacc = np.zeros((A.nblock, nlag), np.int64)
    ringA = np.zeros((nring, K, 2), np.complex128); ringC = np.zeros_like(ringA); ringpos = 0; ringfill = 0
    unwrap = np.zeros((N, 3)); comtraj = []; Tacc = []; Eacc = []

prev_com = None
JA = np.zeros((K, 2, 2)); JC = np.zeros((K, 2, 2))
state = dict(s=s0, ringpos=ringpos, ringfill=ringfill, prev_com=None, t0=time.time(), last_ck=time.time())
bl = nsamp // A.nblock

def sample(step, E):
    s = state['s']
    if s >= nsamp: return
    r = w.pos.reshape(-1, 3); v = w.v.reshape(-1, 3)
    a1, a2 = gc.currents(r, v, mA)
    com = (w.pos * mass3[None, :, None]).sum(1) / mass3.sum(); vcom = (w.v * mass3[None, :, None]).sum(1) / mass3.sum()
    c1, c2 = gc.currents(com, vcom, mC)
    jA = np.stack([a1, a2], 1); jC = np.stack([c1, c2], 1)
    # correlator: C[lag] += j(t) conj(j(t-lag)); ring holds the last nlag samples
    rp = state['ringpos']; fill = state['ringfill']
    ringA[rp] = jA; ringC[rp] = jC
    b = min(s // bl, A.nblock - 1)
    ok = lags <= fill                                   # lags available so far
    idx = (rp - lags[ok]) % nring
    CA[b][:, :, ok] += (jA[:, :, None] * np.conj(ringA[idx]).transpose(1, 2, 0)); CC[b][:, :, ok] += (jC[:, :, None] * np.conj(ringC[idx]).transpose(1, 2, 0)); nacc[b][ok] += 1
    state['ringpos'] = (rp + 1) % nring; state['ringfill'] = min(fill + 1, nring)
    # unwrapped COM for MSD
    if state['prev_com'] is not None:
        d = com - state['prev_com']; d -= L * np.round(d / L); unwrap[:] += d
    state['prev_com'] = com
    if s % msd_every == 0: comtraj.append(unwrap[:msd_sub].astype(np.float32).copy())
    if s % 250 == 0: Tacc.append(w.temperature()); Eacc.append(E / N)
    if s % 2500 == 0:
        P('prod sample %d / %d  t=%.1f ps  T %.1f  E/N %.3f  %.0f s (%.3f s/step)' % (s, nsamp, s * dts, w.temperature(), E / N, time.time() - state['t0'], (time.time() - state['t0']) / max(1, (s - s0) * every)))
    if time.time() - state['last_ck'] > A.ckpt_ps * 60 or s == nsamp - 1:   # ckpt_ps used as minutes here
        np.savez(ck + '.tmp.npz', pos=w.pos, v=w.v, s=s + 1, unwrap=unwrap, CA=CA, CC=CC, nacc=nacc, ringA=ringA, ringC=ringC, ringpos=state['ringpos'], ringfill=state['ringfill'],
                 comtraj=np.array(comtraj), Tacc=np.array(Tacc), Eacc=np.array(Eacc), K=K, L=L, N=N, dts=dts, kvec=kvec, n2=n2, nlag=nlag, lags=lags, nblock=A.nblock, nsamp=nsamp, every=every, T=w.temperature())
        os.replace(ck + '.tmp.npz', ck); state['last_ck'] = time.time()
    state['s'] = s + 1

remaining = (nsamp - s0) * every
w.run(remaining, dt=dt, tau_T=5.0, callback=sample, cb_every=every)
np.savez_compressed(f'rec_{A.tag}.npz', CA=CA, CC=CC, nacc=nacc, comtraj=np.array(comtraj), Tacc=np.array(Tacc), Eacc=np.array(Eacc), K=K, L=L, N=N, dts=dts, kvec=kvec, n2=n2, nlag=nlag, lags=lags, nblock=A.nblock, nsamp=nsamp, every=every, T=w.temperature(), msd_every_ps=msd_every * dts, seed=A.seed)
P('DONE', nsamp, 'samples', '%.0f s' % (time.time() - state['t0']))
