import numpy as np, math, ctypes, time
from md_pme import WaterPME, _lib, _dp
from gridcur import GridCurrents
_lib.currents.argtypes = [ctypes.c_int, _dp, _dp, _dp, ctypes.c_int, _dp, _dp, _dp, _dp]
w = WaterPME(13, seed=3); w.run(300, dt=0.0005, tau_T=0.05); w.run(500, dt=0.002, tau_T=0.2)
L = w.L; K = w.K
rng = np.random.default_rng(0)
nv = []
for _ in range(400):
    n = rng.integers(-9, 10, 3)
    if (n ** 2).sum() > 0 and math.sqrt((n ** 2).sum()) * 2 * math.pi / L <= 14.5: nv.append(n)
nv = np.array(nv); kvec = np.ascontiguousarray(nv * 2 * math.pi / L)
ref = np.where(np.abs(kvec[:, 2:3]) < 0.9 * np.linalg.norm(kvec, axis=1, keepdims=True), [[0, 0, 1.0]], [[1.0, 0, 0]])
e1 = np.cross(kvec, ref); e1 /= np.linalg.norm(e1, axis=1, keepdims=True); e1 = np.ascontiguousarray(e1)
e2 = np.cross(kvec, e1); e2 /= np.linalg.norm(e2, axis=1, keepdims=True); e2 = np.ascontiguousarray(e2)
r = np.ascontiguousarray(w.pos.reshape(-1, 3)); v = np.ascontiguousarray(w.v.reshape(-1, 3)); m = np.ascontiguousarray(np.tile([15.9994, 1.008, 1.008], w.N))
J = np.zeros((len(kvec), 2, 2)); t0 = time.time()
_lib.currents(3 * w.N, r.ctypes.data_as(_dp), v.ctypes.data_as(_dp), m.ctypes.data_as(_dp), len(kvec), kvec.ctypes.data_as(_dp), e1.ctypes.data_as(_dp), e2.ctypes.data_as(_dp), J.ctypes.data_as(_dp))
t1 = time.time(); ex1 = J[:, 0, 0] + 1j * J[:, 0, 1]; ex2 = J[:, 1, 0] + 1j * J[:, 1, 1]
gc = GridCurrents(L, K, nv, e1, e2); t2 = time.time(); g1, g2 = gc.currents(r, v, m); t3 = time.time()
kk = np.linalg.norm(kvec, axis=1); err = np.abs(g1 - ex1) / np.sqrt(np.mean(np.abs(ex1) ** 2))
for lo, hi in ((0, 3), (3, 6), (6, 9), (9, 12), (12, 14.5)):
    s = (kk >= lo) & (kk < hi)
    print('k in [%4.1f,%4.1f): n=%3d  rms rel err |j_fft - j_exact| / rms|j| = %.2e  max %.2e   |ratio| mean %.4f' % (lo, hi, s.sum(), np.sqrt(np.mean(err[s] ** 2)), err[s].max(), np.mean(np.abs(g1[s]) / np.abs(ex1[s]))))
print('time exact %.3f s (K=%d vectors, %d atoms)  fft %.3f s (all k at once)' % (t1 - t0, len(kvec), 3 * w.N, t3 - t2))
