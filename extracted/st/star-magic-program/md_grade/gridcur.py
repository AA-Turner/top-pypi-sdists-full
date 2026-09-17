"""gridcur.py - transverse currents j_T(k,t) for a SET of k-vectors via order-4 B-spline spreading + FFT
(the SPME machinery applied to the momentum density), deconvolved with the Euler-spline factors b(m).
Exact up to aliasing from |k'| >= 2pi/h - |k| (checked in validate_gridcur.py)."""
import numpy as np, ctypes, math
from md_pme import _lib, _dp, Mn_eval

class GridCurrents:
    def __init__(self, L, K, nvec, e1, e2, order=4):
        self.L, self.K, self.n = L, K, order
        self.nvec = nvec.astype(int); self.e1 = e1; self.e2 = e2
        m = np.fft.fftfreq(K, 1.0 / K)
        k = np.arange(order - 1); Mk = Mn_eval(k + 1.0, order)
        denom = (Mk[None, :] * np.exp(2j * np.pi * m[:, None] * k[None, :] / K)).sum(1)
        b = np.exp(2j * np.pi * (order - 1) * m / K) / denom          # b(m), m in fftfreq order (index = m mod K)
        ix, iy, iz = [self.nvec[:, d] % K for d in range(3)]
        self.idx = (ix, iy, iz)
        self.bfac = b[ix] * b[iy] * b[iz]

    def currents3(self, r, v, m, e3):
        """As currents(), plus the projection on a third direction set e3 (K,3) - e.g. k-hat for the longitudinal current."""
        K = self.K; r = np.ascontiguousarray(r, dtype=np.float64)
        J = np.empty((3, len(self.nvec)), np.complex128); Q = np.empty((K, K, K))
        for d in range(3):
            w = np.ascontiguousarray(m * v[:, d])
            _lib.pme_spread(len(w), r.ctypes.data_as(_dp), w.ctypes.data_as(_dp), self.L, K, Q.ctypes.data_as(_dp))
            J[d] = np.conj(np.fft.fftn(Q)[self.idx]) * self.bfac
        return (J * self.e1.T).sum(0), (J * self.e2.T).sum(0), (J * e3.T).sum(0)

    def currents(self, r, v, m):
        """r,v: (Na,3); m: (Na,). Returns j1, j2 complex (K,) = sum m (v.e) exp(i k.r) for the k set."""
        K = self.K; r = np.ascontiguousarray(r, dtype=np.float64)
        J = np.empty((3, len(self.nvec)), np.complex128)
        Q = np.empty((K, K, K))
        for d in range(3):
            w = np.ascontiguousarray(m * v[:, d])
            _lib.pme_spread(len(w), r.ctypes.data_as(_dp), w.ctypes.data_as(_dp), self.L, K, Q.ctypes.data_as(_dp))
            J[d] = np.conj(np.fft.fftn(Q)[self.idx]) * self.bfac
        j1 = (J * self.e1.T).sum(0); j2 = (J * self.e2.T).sum(0)
        return j1, j2
