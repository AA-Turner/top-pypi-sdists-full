import numpy as np, math, ctypes, os, time
KB = 0.0083144626; SIG, EPS, M = 0.3405, 0.9961, 39.948
_lib = ctypes.CDLL('./lj_kernel.so'); _dp = ctypes.POINTER(ctypes.c_double); _lib.lj_forces.restype = ctypes.c_double
_lib.lj_forces.argtypes = [ctypes.c_int, _dp, _dp, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, _dp]
def forces(pos, L, rc):
    F = np.zeros_like(pos); W = ctypes.c_double(); E = _lib.lj_forces(len(pos), pos.ctypes.data_as(_dp), F.ctypes.data_as(_dp), L, rc, SIG, EPS, ctypes.byref(W)); return F, E, W.value
def ref(pos, L, rc):
    N = len(pos); d = pos[:, None] - pos[None, :]; d -= L * np.round(d / L); iu = np.triu_indices(N, 1); dv = d[iu]; r2 = (dv ** 2).sum(1); m = r2 < rc * rc
    inv6 = (SIG ** 2 / r2[m]) ** 3; E = float((4 * EPS * (inv6 ** 2 - inv6)).sum()) - m.sum() * 4 * EPS * ((SIG / rc) ** 12 - (SIG / rc) ** 6)
    fl = 24 * EPS * (2 * inv6 ** 2 - inv6) / r2[m]; F = np.zeros_like(pos); fv = fl[:, None] * dv[m]; np.add.at(F, iu[0][m], fv); np.add.at(F, iu[1][m], -fv); return F, E
rng = np.random.default_rng(3); n = 8; N = n ** 3; rho = 21.25; L = (N / rho) ** (1 / 3); rc = 0.85
a = L / n; pos = np.stack(np.meshgrid(*[np.arange(n)] * 3, indexing='ij'), -1).reshape(-1, 3) * a + a / 2 + rng.normal(0, 0.03, (N, 3)); pos -= L * np.floor(pos / L)
F, E, W = forces(pos, L, rc); Fr, Er = ref(pos, L, rc)
print('1. C kernel vs numpy all-pairs: dE %.2e kJ/mol (E %.4f)  max dF %.2e' % (E - Er, E, np.abs(F - Fr).max()))
h = 1e-6; errs = []
for i, dd in ((0, 0), (77, 1), (500, 2)):
    p = pos.copy(); p[i, dd] += h; Ep = forces(p, L, rc)[1]; p[i, dd] -= 2 * h; Em = forces(p, L, rc)[1]
    errs.append(abs(-(Ep - Em) / (2 * h) - F[i, dd]) / max(abs(F[i, dd]), 1))
print('2. F = -grad E, max rel err %.2e' % max(errs))
# NVE at N=4096
n = 16; N = n ** 3; L = (N / rho) ** (1 / 3); a = L / n
pos = np.stack(np.meshgrid(*[np.arange(n)] * 3, indexing='ij'), -1).reshape(-1, 3) * a + a / 2 + rng.normal(0, 0.02, (N, 3)); v = rng.normal(0, math.sqrt(KB * 85 / M), (N, 3)); v -= v.mean(0)
dt = 0.004
def run(pos, v, nsteps, tau=None, rec=None):
    F, E, W = forces(pos, L, rc)
    for s in range(nsteps):
        v += 0.5 * dt * F / M; pos += dt * v; pos -= L * np.floor(pos / L); F, E, W = forces(pos, L, rc); v += 0.5 * dt * F / M
        T = M * (v * v).sum() / ((3 * N - 3) * KB)
        if tau: v *= math.sqrt(1 + dt / tau * (85 / T - 1))
        if rec is not None and s % 5 == 0: rec.append((E + 0.5 * M * (v * v).sum()) / N)
    return pos, v, E, W
t0 = time.time(); pos, v, E, W = run(pos, v, 2000, 0.05); pos, v, E, W = run(pos, v, 4000, 0.2); pos, v, E, W = run(pos, v, 4000, 1.0)
T = M * (v * v).sum() / ((3 * N - 3) * KB); print('3. equil N=%d L=%.3f: T %.2f  E/N %.4f kJ/mol (%.3f eps)  P %.0f bar  %.0f s (%.4f s/step)' % (N, L, T, E / N, E / N / EPS, (N * KB * T + W / 3) / L ** 3 * 16.6054, time.time() - t0, (time.time() - t0) / 10000))
rec = []; pos, v, E, W = run(pos, v, 2500, None, rec); rec = np.array(rec); print('4. NVE 10 ps at 4 fs: dE_tot/N = %+.5f kJ/mol (std %.5f)  T %.2f' % (rec[-1] - rec[0], rec.std(), M * (v * v).sum() / ((3 * N - 3) * KB)))
