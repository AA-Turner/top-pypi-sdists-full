"""md_pme.py - rigid TIP4P/2005 water MD with smooth particle-mesh Ewald (SPME) electrostatics
for the front-4 RECORD RUN. Real-space pair forces (LJ + erfc Coulomb, site cutoff, cell list)
in C (pair_kernel.c via ctypes); reciprocal space in numpy (order-n B-spline SPME, FFT);
constraints, integrator and virtual site from md_engine.Water (B286b, validated).
Units: nm, ps, amu, kJ/mol, e.
"""
import ctypes, math, os, numpy as np
from md_engine import Water, KB, FCOUL, M_O, M_H, Q_H, Q_M, SIG, EPS, W_M

_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pair_kernel.so'))
_lib.pair_forces.restype = ctypes.c_double
_dp = ctypes.POINTER(ctypes.c_double)
_lib.pair_forces.argtypes = [ctypes.c_int, _dp, _dp, ctypes.c_double, ctypes.c_double, ctypes.c_double,
                             ctypes.c_double, ctypes.c_double, _dp, ctypes.c_double, ctypes.c_double, _dp, _dp, _dp]
_lib.table_check.restype = ctypes.c_double; _lib.table_check.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
_lib.rattle_positions.restype = ctypes.c_int
_lib.rattle_positions.argtypes = [ctypes.c_int, _dp, _dp, _dp, _dp, _dp, ctypes.c_double, ctypes.c_double, ctypes.c_int]
_lib.rattle_velocities.restype = ctypes.c_int
_lib.rattle_velocities.argtypes = [ctypes.c_int, _dp, _dp, _dp, _dp, ctypes.c_double, ctypes.c_int]
_lib.pme_spread.argtypes = [ctypes.c_int, _dp, _dp, ctypes.c_double, ctypes.c_int, _dp]
_lib.pme_gather.argtypes = [ctypes.c_int, _dp, _dp, ctypes.c_double, ctypes.c_int, _dp, _dp]
Q4 = np.array([0.0, Q_H, Q_H, Q_M])


def Mn_eval(u, n):
    """M_n(u) by the explicit recursion evaluated for all shifts (u array, returns M_n(u))."""
    if n == 1:
        return np.where((u >= 0) & (u < 1), 1.0, 0.0)
    return (u * Mn_eval(u, n - 1) + (n - u) * Mn_eval(u - 1, n - 1)) / (n - 1)


def dMn_eval(u, n):
    return Mn_eval(u, n - 1) - Mn_eval(u - 1, n - 1)


class PME:
    def __init__(self, L, K, alpha, order=4):
        self.L, self.K, self.alpha, self.n = L, K, alpha, order
        m = np.fft.fftfreq(K, 1.0 / K)                       # integer m in [-K/2, K/2)
        # |b(m)|^2 per dimension
        k = np.arange(order - 1)
        Mk = Mn_eval(k + 1.0, order)                         # M_n(k+1), k=0..n-2
        denom = (Mk[None, :] * np.exp(2j * np.pi * m[:, None] * k[None, :] / K)).sum(1)
        b2 = 1.0 / np.abs(denom) ** 2
        mx, my, mz = np.meshgrid(m, m, m, indexing='ij')
        kx, ky, kz = (2 * np.pi / L) * mx, (2 * np.pi / L) * my, (2 * np.pi / L) * mz
        k2 = kx * kx + ky * ky + kz * kz
        B = b2[:, None, None] * b2[None, :, None] * b2[None, None, :]
        V = L ** 3
        with np.errstate(divide='ignore', invalid='ignore'):
            th = (4 * np.pi * FCOUL / V) * np.exp(-k2 / (4 * alpha * alpha)) / k2 * B
        th[0, 0, 0] = 0.0
        self.theta = th

    def _spread_setup(self, r):
        """r: (Nq,3) positions. Returns grid index arrays and weights for order-n spreading."""
        K, n = self.K, self.n
        u = (r / self.L) * K
        u -= K * np.floor(u / K)                              # 0 <= u < K
        m0 = np.floor(u).astype(np.int64)                     # base grid point
        idx = []; W = []; dW = []
        for d in range(3):
            js = m0[:, d][:, None] - np.arange(n)[None, :]    # grid points floor(u)-j, j=0..n-1
            x = u[:, d][:, None] - js                         # u - k in (0, n)
            idx.append(js % K); W.append(Mn_eval(x, n)); dW.append(dMn_eval(x, n))
        return idx, W, dW

    def energy_forces(self, r, q):
        if self.n == 4:
            return self.energy_forces_c(r, q)
        return self.energy_forces_np(r, q)

    def energy_forces_c(self, r, q):
        K = self.K
        r = np.ascontiguousarray(r, dtype=np.float64); q = np.ascontiguousarray(q, dtype=np.float64)
        Q = np.empty((K, K, K)); _lib.pme_spread(len(q), r.ctypes.data_as(_dp), q.ctypes.data_as(_dp), self.L, K, Q.ctypes.data_as(_dp))
        Qh = np.fft.fftn(Q)
        E = 0.5 * float(np.sum(self.theta * (Qh.real ** 2 + Qh.imag ** 2)))
        phi = np.ascontiguousarray(np.fft.ifftn(self.theta * Qh).real * K ** 3)
        F = np.empty_like(r); _lib.pme_gather(len(q), r.ctypes.data_as(_dp), q.ctypes.data_as(_dp), self.L, K, phi.ctypes.data_as(_dp), F.ctypes.data_as(_dp))
        return E, F

    def energy_forces_np(self, r, q):
        K, n = self.K, self.n
        idx, W, dW = self._spread_setup(r)
        Nq = len(q)
        # spread: Q[ix,iy,iz] += q * Wx*Wy*Wz over n^3 combos
        ix = idx[0][:, :, None, None]; iy = idx[1][:, None, :, None]; iz = idx[2][:, None, None, :]
        flat = ((ix * K + iy) * K + iz)                       # (Nq,n,n,n)
        w3 = W[0][:, :, None, None] * W[1][:, None, :, None] * W[2][:, None, None, :]
        Q = np.bincount(flat.ravel(), weights=(q[:, None, None, None] * w3).ravel(), minlength=K ** 3).reshape(K, K, K)
        Qh = np.fft.fftn(Q)
        E = 0.5 * float(np.sum(self.theta * (Qh.real ** 2 + Qh.imag ** 2)))
        phi = np.fft.ifftn(self.theta * Qh).real * K ** 3     # dE/dQ[k]
        ph = phi.ravel()[flat]                                # (Nq,n,n,n)
        s = K / self.L
        gx = (dW[0][:, :, None, None] * W[1][:, None, :, None] * W[2][:, None, None, :] * ph).sum((1, 2, 3))
        gy = (W[0][:, :, None, None] * dW[1][:, None, :, None] * W[2][:, None, None, :] * ph).sum((1, 2, 3))
        gz = (W[0][:, :, None, None] * W[1][:, None, :, None] * dW[2][:, None, None, :] * ph).sum((1, 2, 3))
        F = -q[:, None] * s * np.stack([gx, gy, gz], 1)
        return E, F


class WaterPME(Water):
    def __init__(self, n_side, density=33.33, T=298.0, rc=0.9, seed=1, alpha=3.5, grid_spacing=0.1, order=4, skin=0.2):
        super().__init__(n_side, density, T, rc, seed)
        self.alpha, self.skin = alpha, skin
        K = int(math.ceil(self.L / grid_spacing))
        K += K % 2                                            # even grid
        self.pme = PME(self.L, K, alpha, order)
        self.K = K
        self.E_self = -FCOUL * alpha / math.sqrt(math.pi) * self.N * float((Q4 ** 2).sum())
        self.E_parts = {}

    D0 = None

    def _rattle_positions(self, ref=None, tol=1e-7, maxit=50):
        from md_engine import R_OH, R_HH
        d0 = np.array([R_OH, R_OH, R_HH]); mass = np.ascontiguousarray(self.mass, dtype=np.float64)
        pos = np.ascontiguousarray(self.pos); vel = np.ascontiguousarray(self.v)
        refp = np.ascontiguousarray(ref) if ref is not None else None
        _lib.rattle_positions(self.N, pos.ctypes.data_as(_dp), refp.ctypes.data_as(_dp) if ref is not None else None,
                              vel.ctypes.data_as(_dp) if ref is not None else None, mass.ctypes.data_as(_dp), d0.ctypes.data_as(_dp),
                              getattr(self, 'dt', 0.002), 1e-9, maxit)
        self.pos = pos; self.v = vel

    def _rattle_velocities(self, tol=1e-9, maxit=50):
        from md_engine import R_OH, R_HH
        d0 = np.array([R_OH, R_OH, R_HH]); mass = np.ascontiguousarray(self.mass, dtype=np.float64)
        pos = np.ascontiguousarray(self.pos); vel = np.ascontiguousarray(self.v)
        _lib.rattle_velocities(self.N, pos.ctypes.data_as(_dp), vel.ctypes.data_as(_dp), mass.ctypes.data_as(_dp), d0.ctypes.data_as(_dp), tol, maxit)
        self.pos = pos; self.v = vel

    def sites4(self):
        p = self.pos; rO = p[:, 0]
        rM = rO + W_M * ((p[:, 1] - rO) + (p[:, 2] - rO))
        return np.concatenate([p, rM[:, None, :]], 1)         # (N,4,3)

    def forces(self):
        s4 = np.ascontiguousarray(self.sites4(), dtype=np.float64)
        F4 = np.zeros_like(s4)
        elj = ctypes.c_double(); ereal = ctypes.c_double(); eexcl = ctypes.c_double()
        E = _lib.pair_forces(self.N, s4.ctypes.data_as(_dp), F4.ctypes.data_as(_dp), self.L, self.rc, self.skin,
                             self.alpha, FCOUL, Q4.ctypes.data_as(_dp), SIG, EPS,
                             ctypes.byref(elj), ctypes.byref(ereal), ctypes.byref(eexcl))
        # reciprocal on the 3N charges (H1,H2,M)
        rq = s4[:, 1:, :].reshape(-1, 3); q = np.tile(Q4[1:], self.N)
        Erec, Fq = self.pme.energy_forces(rq, q)
        F4[:, 1:, :] += Fq.reshape(self.N, 3, 3)
        E += Erec + self.E_self
        self.E_parts = dict(lj=elj.value, real=ereal.value, excl=eexcl.value, rec=Erec, self=self.E_self)
        # redistribute M force to O, H1, H2
        F = F4[:, :3, :].copy(); FM = F4[:, 3, :]
        F[:, 0] += (1 - 2 * W_M) * FM; F[:, 1] += W_M * FM; F[:, 2] += W_M * FM
        return F, E
