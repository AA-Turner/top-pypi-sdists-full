"""argon_record.py - B288, the Q-251 pre-stated test: Lennard-Jones argon at the NIST 85 K / 0.101325 MPa state
point (rho 1409.6 kg/m^3 -> 21.25 nm^-3; sigma 0.3405 nm, eps 0.9961 kJ/mol), velocity Verlet, weak Berendsen,
transverse AND longitudinal currents by the B287 FFT momentum-density transform (gridcur), on-the-fly
autocorrelator in blocks (same design as front4_record.py), multi-origin MSD, checkpoint/restart.
usage: python argon_record.py <n_side> <prod_ps> <tag> [--seed N] [--restart] [--kmax 26] [--h 0.08]"""
import sys, os, time, math, argparse, ctypes, numpy as np
from gridcur import GridCurrents
from md_pme import Mn_eval
ap = argparse.ArgumentParser()
ap.add_argument('n_side', type=int); ap.add_argument('prod_ps', type=float); ap.add_argument('tag')
ap.add_argument('--seed', type=int, default=1); ap.add_argument('--restart', action='store_true')
ap.add_argument('--kmax', type=float, default=26.0); ap.add_argument('--h', type=float, default=0.08)
ap.add_argument('--cap', type=int, default=40); ap.add_argument('--nshell', type=int, default=44)
ap.add_argument('--dt', type=float, default=0.004); ap.add_argument('--every', type=int, default=1)
ap.add_argument('--tlag', type=float, default=20.0); ap.add_argument('--fine_lag', type=float, default=2.0); ap.add_argument('--coarse', type=int, default=10)
ap.add_argument('--nblock', type=int, default=6); ap.add_argument('--ckpt_min', type=float, default=10.0)
ap.add_argument('--T', type=float, default=85.0); ap.add_argument('--rho', type=float, default=21.25); ap.add_argument('--rc', type=float, default=0.85)
A = ap.parse_args()
KB = 0.0083144626; SIG, EPS, M = 0.3405, 0.9961, 39.948
_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lj_kernel.so'))
_dp = ctypes.POINTER(ctypes.c_double); _lib.lj_forces.restype = ctypes.c_double
_lib.lj_forces.argtypes = [ctypes.c_int, _dp, _dp, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, _dp]
log = open(f'ar_{A.tag}.log', 'a')
def P(*a): print(*a, file=log, flush=True)
N = A.n_side ** 3; L = (N / A.rho) ** (1 / 3); dt = A.dt; dts = dt * A.every
rng = np.random.default_rng(A.seed)
def forces(pos):
    F = np.zeros_like(pos); W = ctypes.c_double()
    E = _lib.lj_forces(N, pos.ctypes.data_as(_dp), F.ctypes.data_as(_dp), L, A.rc, SIG, EPS, ctypes.byref(W)); return F, E, W.value
def temperature(v): return M * (v * v).sum() / ((3 * N - 3) * KB)
def run(pos, v, nsteps, tau_T=None, cb=None, cb_every=1, F=None):
    if F is None: F, E, W = forces(pos)
    for s in range(nsteps):
        v += 0.5 * dt * F / M; pos += dt * v; pos -= L * np.floor(pos / L)
        F, E, W = forces(pos); v += 0.5 * dt * F / M
        if tau_T: v *= math.sqrt(1 + dt / tau_T * (A.T / max(temperature(v), 1e-9) - 1))
        if cb and s % cb_every == 0: cb(s, E, W)
    return pos, v, F
# ---- k-vectors: log-spaced n^2 shells from k_min to kmax, capped ----
nmax = int(A.kmax * L / (2 * math.pi)) + 1; shells = {}
for nx in range(-nmax, nmax + 1):
    for ny in range(-nmax, nmax + 1):
        for nz in range(0, nmax + 1):
            n2 = nx * nx + ny * ny + nz * nz
            if n2 == 0 or math.sqrt(n2) * 2 * math.pi / L > A.kmax: continue
            if nz == 0 and (ny < 0 or (ny == 0 and nx < 0)): continue
            shells.setdefault(n2, []).append((nx, ny, nz))
keys = sorted(shells)
if len(keys) > A.nshell:
    targets = np.exp(np.linspace(math.log(keys[0]), math.log(keys[-1]), A.nshell)); keys = sorted(set(min(keys, key=lambda x: abs(math.log(x) - math.log(t))) for t in targets))
srng = np.random.default_rng(1234); nv = []; n2l = []
for n2 in keys:
    vs = shells[n2]
    if len(vs) > A.cap: vs = [vs[i] for i in srng.choice(len(vs), A.cap, replace=False)]
    nv += vs; n2l += [n2] * len(vs)
nv = np.array(nv, float); n2 = np.array(n2l); kvec = nv * (2 * math.pi / L); K = len(kvec)
khat = kvec / np.linalg.norm(kvec, axis=1, keepdims=True)
ref = np.where(np.abs(khat[:, 2:3]) < 0.9, [[0, 0, 1.0]], [[1.0, 0, 0]])
e1 = np.cross(kvec, ref); e1 /= np.linalg.norm(e1, axis=1, keepdims=True); e2 = np.cross(kvec, e1); e2 /= np.linalg.norm(e2, axis=1, keepdims=True)
Kg = int(math.ceil(L / A.h)); Kg += Kg % 2
gcT = GridCurrents(L, Kg, nv, e1, e2); khat = np.ascontiguousarray(khat)
mass = np.full(N, M)
nring = int(round(A.tlag / dts)) + 1; nfine = int(round(A.fine_lag / dts))
lags = np.concatenate([np.arange(0, nfine + 1), np.arange(nfine + A.coarse, nring, A.coarse)]); nlag = len(lags)
nsamp = int(round(A.prod_ps / dts)); bl = nsamp // A.nblock; msd_sub = min(N, 2000); msd_every = int(round(0.5 / dts))
ck = f'ar_{A.tag}_ckpt.npz'
if A.restart and os.path.exists(ck):
    z = np.load(ck); pos = z['pos']; v = z['v']; s0 = int(z['s']); unwrap = z['unwrap']; CT = z['CT']; CL = z['CL']; nacc = z['nacc']
    ringT = z['ringT']; ringL = z['ringL']; ringpos = int(z['ringpos']); ringfill = int(z['ringfill']); comtraj = list(z['comtraj']); Tacc = list(z['Tacc']); Eacc = list(z['Eacc']); Pacc = list(z['Pacc'])
    assert np.array_equal(z['lags'], lags) and z['K'] == K; P('RESTART at sample', s0, 'of', nsamp)
else:
    P('ARGON LJ  N %d  L %.4f nm  rho %.3f nm^-3 (rho* %.3f)  T %.1f K (T* %.3f)  rc %.2f  k_min %.4f  K %d vectors in %d shells (cap %d)  kmax %.1f  grid %d (h %.3f)  dt %.1f fs  sample every %d  lags %d (fine to %.1f ps, every %d to %.1f ps)  blocks %d  seed %d' %
      (N, L, A.rho, A.rho * SIG ** 3, A.T, A.T / (EPS / KB), A.rc, 2 * math.pi / L, K, len(keys), A.cap, A.kmax, Kg, L / Kg, dt * 1000, A.every, nlag, A.fine_lag, A.coarse, A.tlag, A.nblock, A.seed))
    a = L / A.n_side; g = np.stack(np.meshgrid(*[np.arange(A.n_side)] * 3, indexing='ij'), -1).reshape(-1, 3) * a + a / 2
    pos = g + rng.normal(0, 0.02, g.shape); v = rng.normal(0, math.sqrt(KB * A.T / M), (N, 3)); v -= v.mean(0)
    t0 = time.time()
    pos, v, F = run(pos, v, 2000, tau_T=0.05); pos, v, F = run(pos, v, 5000, tau_T=0.2)          # 8 + 20 ps
    def cb(s, E, W):
        if s % 2500 == 0: P('eq step', s, 'T %.2f' % temperature(v), 'E/N %.4f' % (E / N), '%.0f s' % (time.time() - t0))
    pos, v, F = run(pos, v, 10000, tau_T=1.0, cb=cb, cb_every=2500)                                # 40 ps
    F, E, W = forces(pos); P('equilibrated: T %.2f  E/N %.4f kJ/mol  P %.1f bar  %.0f s' % (temperature(v), E / N, (N * KB * temperature(v) + W / 3) / L ** 3 * 16.6054, time.time() - t0))
    s0 = 0; CT = np.zeros((A.nblock, K, 2, nlag), np.complex128); CL = np.zeros((A.nblock, K, nlag), np.complex128); nacc = np.zeros((A.nblock, nlag), np.int64)
    ringT = np.zeros((nring, K, 2), np.complex128); ringL = np.zeros((nring, K), np.complex128); ringpos = 0; ringfill = 0
    unwrap = np.zeros((N, 3)); comtraj = []; Tacc = []; Eacc = []; Pacc = []
state = dict(s=s0, ringpos=ringpos, ringfill=ringfill, prev=None, t0=time.time(), last_ck=time.time())
def sample(step, E, W):
    s = state['s']
    if s >= nsamp: return
    t1, t2, jl = gcT.currents3(pos, v, mass, khat)
    jT = np.stack([t1, t2], 1); rp = state['ringpos']; fill = state['ringfill']; ringT[rp] = jT; ringL[rp] = jl
    b = min(s // bl, A.nblock - 1); ok = lags <= fill; idx = (rp - lags[ok]) % nring
    CT[b][:, :, ok] += jT[:, :, None] * np.conj(ringT[idx]).transpose(1, 2, 0); CL[b][:, ok] += jl[:, None] * np.conj(ringL[idx]).T; nacc[b][ok] += 1
    state['ringpos'] = (rp + 1) % nring; state['ringfill'] = min(fill + 1, nring)
    if state['prev'] is not None:
        d = pos - state['prev']; d -= L * np.round(d / L); unwrap[:] += d
    state['prev'] = pos.copy()
    if s % msd_every == 0: comtraj.append(unwrap[:msd_sub].astype(np.float32).copy())
    if s % 250 == 0: Tacc.append(temperature(v)); Eacc.append(E / N); Pacc.append((N * KB * temperature(v) + W / 3) / L ** 3 * 16.6054)
    if s % 5000 == 0: P('prod sample %d / %d  t=%.1f ps  T %.2f  E/N %.4f  P %.0f bar  %.0f s (%.4f s/step)' % (s, nsamp, s * dts, temperature(v), E / N, Pacc[-1], time.time() - state['t0'], (time.time() - state['t0']) / max(1, (s - s0) * A.every)))
    if time.time() - state['last_ck'] > A.ckpt_min * 60 or s == nsamp - 1:
        np.savez(ck + '.tmp.npz', pos=pos, v=v, s=s + 1, unwrap=unwrap, CT=CT, CL=CL, nacc=nacc, ringT=ringT, ringL=ringL, ringpos=state['ringpos'], ringfill=state['ringfill'], comtraj=np.array(comtraj), Tacc=np.array(Tacc), Eacc=np.array(Eacc), Pacc=np.array(Pacc), K=K, L=L, N=N, dts=dts, kvec=kvec, n2=n2, lags=lags, nblock=A.nblock, nsamp=nsamp)
        os.replace(ck + '.tmp.npz', ck); state['last_ck'] = time.time()
    state['s'] = s + 1
pos, v, F = run(pos, v, (nsamp - s0) * A.every, tau_T=5.0, cb=sample, cb_every=A.every)
np.savez_compressed(f'ar_{A.tag}.npz', CT=CT, CL=CL, nacc=nacc, comtraj=np.array(comtraj), Tacc=np.array(Tacc), Eacc=np.array(Eacc), Pacc=np.array(Pacc), K=K, L=L, N=N, dts=dts, kvec=kvec, n2=n2, lags=lags, nblock=A.nblock, nsamp=nsamp, seed=A.seed, T=A.T, rho=A.rho, msd_every_ps=msd_every * dts, mass=M)
P('DONE', nsamp, 'samples', '%.0f s' % (time.time() - state['t0']))
