import numpy as np, math, time, ctypes
from md_engine import FCOUL, W_M
from md_pme import WaterPME, PME, Q4, _lib, _dp
from ewald_ref import ewald_energy_forces
from scipy.special import erfc
np.set_printoptions(precision=6, suppress=True)
out = []
def P(*a):
    print(*a); out.append(' '.join(str(x) for x in a))

# ---- 1. Madelung constant: NaCl lattice, explicit Ewald reciprocal + real via PME class + C real-space? Use ewald_ref parts on point charges.
# Build as 'molecules' is awkward; do a direct Ewald on point charges with the same formulas.
def ewald_points(r, q, L, alpha, rc, kmax_n=10):
    N = len(r); d = r[:, None] - r[None, :]; d -= L * np.round(d / L)
    iu = np.triu_indices(N, 1); rr = np.sqrt((d[iu] ** 2).sum(1)); m = rr < rc
    E_real = float((FCOUL * (q[iu[0]] * q[iu[1]])[m] * erfc(alpha * rr[m]) / rr[m]).sum())
    n = np.arange(-kmax_n, kmax_n + 1); nx, ny, nz = np.meshgrid(n, n, n, indexing='ij')
    nv = np.stack([nx, ny, nz], -1).reshape(-1, 3); nv = nv[(nv ** 2).sum(1) > 0]
    kv = nv * 2 * math.pi / L; k2 = (kv ** 2).sum(1)
    S = (q[:, None] * np.exp(1j * (r @ kv.T))).sum(0)
    E_rec = float(((2 * math.pi * FCOUL / L ** 3) * np.exp(-k2 / (4 * alpha ** 2)) / k2 * np.abs(S) ** 2).sum())
    E_self = -FCOUL * alpha / math.sqrt(math.pi) * float((q ** 2).sum())
    return E_real + E_rec + E_self
a = 0.564; nc = 2; L = nc * a; r = []; q = []
for i in range(2 * nc):
    for j in range(2 * nc):
        for k in range(2 * nc):
            r.append([i, j, k]); q.append(1.0 if (i + j + k) % 2 == 0 else -1.0)
r = np.array(r) * a / 2; q = np.array(q)
E = ewald_points(r, q, L, alpha=6.0 / L * 2, rc=L / 2 * 0.999, kmax_n=12)
n_pairs = len(q) / 2; r_nn = a / 2
madelung = -E / (n_pairs * FCOUL / r_nn)
P('1. Madelung (NaCl) from Ewald: %.6f  (literature 1.747565)  rel err %.1e' % (madelung, abs(madelung - 1.747565) / 1.747565))

# ---- 2. water box: C kernel + PME vs explicit reference
w = WaterPME(8, T=298.0, rc=0.9, seed=3, alpha=3.5, grid_spacing=0.1, order=4)   # N=512, L=2.486 -> L/2=1.24 >= rc+skin=1.1
w.run(200, dt=0.0005, tau_T=0.05); w.run(500, dt=0.001, tau_T=0.1)             # get off the lattice
s4 = w.sites4()
Fc, Ec = w.forces(); parts = w.E_parts
Er, Fr, pr = ewald_energy_forces(s4, Q4, w.L, w.rc, w.alpha, kmax_n=16)
# reference F on 3 atoms after M redistribution
F3 = Fr[:, :3].copy(); FM = Fr[:, 3]; F3[:, 0] += (1 - 2 * W_M) * FM; F3[:, 1] += W_M * FM; F3[:, 2] += W_M * FM
P('2a. real-space + LJ + excl: C kernel vs numpy reference: dE = %.3e kJ/mol (E_real %.4f vs %.4f; lj %.4f vs %.4f; excl %.4f vs %.4f)' %
  (parts['lj'] + parts['real'] + parts['excl'] - (pr['lj'] + pr['real'] + pr['excl']), parts['real'], pr['real'], parts['lj'], pr['lj'], parts['excl'], pr['excl']))
P('2b. reciprocal: PME (K=%d, order 4) vs direct k-sum: E_rec %.5f vs %.5f  rel %.2e' % (w.K, parts['rec'], pr['rec'], abs(parts['rec'] - pr['rec']) / abs(pr['rec'])))
P('2c. total E: %.5f vs %.5f  (dE/N %.2e kJ/mol)' % (Ec, Er, (Ec - Er) / w.N))
ferr = np.sqrt(((Fc - F3) ** 2).sum(-1)).max(); frms = np.sqrt((F3 ** 2).sum(-1).mean())
P('2d. forces: max |F_pme - F_ref| = %.4f kJ/mol/nm  vs rms |F| = %.2f  (rel %.1e)' % (ferr, frms, ferr / frms))

for gs, order in ((0.1, 4), (0.08, 4), (0.12, 4), (0.1, 6)):
    pm = PME(w.L, int(math.ceil(w.L / gs)) + int(math.ceil(w.L / gs)) % 2, w.alpha, order)
    rq = s4[:, 1:, :].reshape(-1, 3); qq = np.tile(Q4[1:], w.N)
    Ep, Fp = pm.energy_forces(rq, qq) if order == 4 else pm.energy_forces_np(rq, qq)
    # reference reciprocal forces = Fr recip part: recompute via ewald_ref parts? approximate: compare total force
    P('2e. PME spacing %.2f order %d K=%d: E_rec %.5f (ref %.5f, rel %.1e)' % (gs, order, pm.K, Ep, pr['rec'], abs(Ep - pr['rec']) / abs(pr['rec'])))
# ---- 3. finite-difference check of the engine's own energy (displace an O atom; M follows the geometry)
h = 1e-5; errs = []
for (i, d) in [(0, 0), (7, 1), (100, 2), (511, 0), (50, 1)]:
    p0 = w.pos.copy()
    w.pos = p0.copy(); w.pos[i, 0, d] += h; Ep = w.forces()[1]
    w.pos = p0.copy(); w.pos[i, 0, d] -= h; Em = w.forces()[1]
    w.pos = p0.copy(); F0 = w.forces()[0]
    fd = -(Ep - Em) / (2 * h); errs.append(abs(fd - F0[i, 0, d]) / max(abs(F0[i, 0, d]), 1))
    P('3. FD O-atom %3d dim %d: -dE/dx = %10.4f   F = %10.4f' % (i, d, fd, F0[i, 0, d]))
for (i, a, d) in [(3, 1, 2), (77, 2, 0)]:
    p0 = w.pos.copy()
    w.pos = p0.copy(); w.pos[i, a, d] += h; Ep = w.forces()[1]
    w.pos = p0.copy(); w.pos[i, a, d] -= h; Em = w.forces()[1]
    w.pos = p0.copy(); F0 = w.forces()[0]
    fd = -(Ep - Em) / (2 * h); errs.append(abs(fd - F0[i, a, d]) / max(abs(F0[i, a, d]), 1))
    P('3. FD H-atom %3d site %d dim %d: -dE/dx = %10.4f   F = %10.4f' % (i, a, d, fd, F0[i, a, d]))
P('3. max relative FD error %.2e' % max(errs))

# ---- 4. timing at production sizes
import os
for ns in (13, 20, 26):
    t = WaterPME(ns, T=298.0, rc=0.9, seed=1, alpha=3.5, grid_spacing=0.1, order=4)
    t0 = time.time(); t.forces(); t1 = time.time(); t.forces(); t2 = time.time()
    P('4. N=%d L=%.3f K=%d threads=%s: forces %.3f s (2nd call %.3f s)' % (t.N, t.L, t.K, os.environ.get('OMP_NUM_THREADS', '?'), t1 - t0, t2 - t1))
    t0 = time.time(); t.run(5, dt=0.002); P('   full step %.3f s' % ((time.time() - t0) / 5))
open('validate.out', 'w').write('\n'.join(out) + '\n')
