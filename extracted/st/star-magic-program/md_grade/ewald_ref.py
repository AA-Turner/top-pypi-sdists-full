"""ewald_ref.py - explicit Ewald reference (direct k-sum) for validating pair_kernel.c + PME."""
import numpy as np, math
from scipy.special import erfc, erf
from md_engine import FCOUL, SIG, EPS

def ewald_energy_forces(s4, q4, L, rc, alpha, kmax_n=12, lj=True):
    """s4: (N,4,3) sites (O,H1,H2,M); q4 charges per site. All charge pairs of DIFFERENT molecules
    in real space within rc (site cutoff), reciprocal by direct k-sum over ALL charges, self term,
    intramolecular exclusion correction. Returns E, F(N,4,3), parts dict."""
    N = s4.shape[0]; F = np.zeros_like(s4)
    # --- real space + LJ, all-pairs minimum image ---
    rO = s4[:, 0]; d = rO[:, None] - rO[None, :]; d -= L * np.round(d / L)
    iu = np.triu_indices(N, 1); I, J = iu
    shift = d[I, J] - (rO[I] - rO[J])
    E_lj = 0.0
    if lj:
        r2 = (d[I, J] ** 2).sum(1); m = r2 < rc * rc
        inv6 = (SIG ** 2 / r2[m]) ** 3
        E_lj = float((4 * EPS * (inv6 ** 2 - inv6)).sum()) - m.sum() * 4 * EPS * ((SIG / rc) ** 12 - (SIG / rc) ** 6)
        fl = 24 * EPS * (2 * inv6 ** 2 - inv6) / r2[m]
        fv = fl[:, None] * d[I, J][m]
        np.add.at(F[:, 0], I[m], fv); np.add.at(F[:, 0], J[m], -fv)
    E_real = 0.0
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            dv = s4[I, a] - s4[J, b] + shift; r2 = (dv ** 2).sum(1); m = r2 < rc * rc
            r = np.sqrt(r2[m]); qq = FCOUL * q4[a] * q4[b]; ec = erfc(alpha * r)
            E_real += float((qq * ec / r).sum())
            fs = qq * (ec / r + 2 * alpha / math.sqrt(math.pi) * np.exp(-(alpha * r) ** 2)) / r2[m]
            fv = fs[:, None] * dv[m]
            np.add.at(F[:, a], I[m], fv); np.add.at(F[:, b], J[m], -fv)
    # --- reciprocal, direct sum ---
    rq = s4[:, 1:, :].reshape(-1, 3); q = np.tile(q4[1:], N)
    n = np.arange(-kmax_n, kmax_n + 1)
    nx, ny, nz = np.meshgrid(n, n, n, indexing='ij'); nv = np.stack([nx, ny, nz], -1).reshape(-1, 3)
    nv = nv[(nv ** 2).sum(1) > 0]
    kv = nv * (2 * math.pi / L); k2 = (kv ** 2).sum(1)
    E_rec = 0.0; Fq = np.zeros_like(rq)
    for c in range(0, len(kv), 2000):
        kk = kv[c:c + 2000]; kk2 = k2[c:c + 2000]
        ph = np.exp(1j * (rq @ kk.T))                          # (Nq,K)
        S = (q[:, None] * ph).sum(0)                           # (K,)
        g = (2 * math.pi * FCOUL / L ** 3) * np.exp(-kk2 / (4 * alpha ** 2)) / kk2
        E_rec += float((g * np.abs(S) ** 2).sum())
        # F_i = -dE/dr_i = -(2 g) q_i Im[ conj(S) ... ]: dE/dr_i = 2 g q_i Re[ i k e^{ik r_i} conj(S) ] = -2 g q_i k Im[e^{ikr_i} conj(S)]
        t = (ph * np.conj(S)[None, :]).imag * (2 * g)[None, :]  # (Nq,K)
        Fq += q[:, None] * (t @ kk)
    F[:, 1:, :] += Fq.reshape(N, 3, 3)
    E_self = -FCOUL * alpha / math.sqrt(math.pi) * float((q ** 2).sum())
    # --- intramolecular exclusion ---
    E_excl = 0.0
    for a in (1, 2, 3):
        for b in range(a + 1, 4):
            dv = s4[:, a] - s4[:, b]; r2 = (dv ** 2).sum(1); r = np.sqrt(r2); qq = FCOUL * q4[a] * q4[b]
            ef = erf(alpha * r); E_excl -= float((qq * ef / r).sum())
            fs = qq * (2 * alpha / math.sqrt(math.pi) * np.exp(-(alpha * r) ** 2) / r - ef / r2) / r
            F[:, a] += fs[:, None] * dv; F[:, b] -= fs[:, None] * dv
    parts = dict(lj=E_lj, real=E_real, rec=E_rec, self=E_self, excl=E_excl)
    return E_lj + E_real + E_rec + E_self + E_excl, F, parts
