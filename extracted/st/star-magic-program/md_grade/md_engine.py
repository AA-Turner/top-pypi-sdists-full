"""md_engine.py - self-contained rigid TIP4P/2005 water MD in numpy (no MD package).
Units: nm, ps, amu, kJ/mol, e.  k_B = 0.0083144626 kJ/mol/K.  f_coul = 138.935458.
Model (Abascal & Vega 2005): r_OH 0.09572 nm, HOH 104.52 deg, r_OM 0.01546 nm,
q_H +0.5564, q_M -1.1128, LJ(O) sigma 0.31589 nm eps 0.7749 kJ/mol.
Integration: velocity Verlet + RATTLE (3 distance constraints per molecule),
M = virtual site on the bisector (force redistributed to O,H,H).
Electrostatics: reaction-field Coulomb (eps_rf = inf) with a SITE-based cutoff r < rc
on every charge pair (molecule prelist on O-O < rc + 0.2 nm). A molecule-based cutoff
was tried first and HEATED the box (+1.5 kJ/mol per molecule per 2 ps, dt-independent):
the RF pair force is ~50 kJ/mol/nm at r = rc for the site pairs a group cutoff switches on
together. With eps_rf = inf both V and F vanish at rc per site pair, so the site cutoff is
smooth; verified: forces = -grad E to machine precision, dE/N = -0.006 kJ/mol over 2 ps.
"""
import numpy as np, math, time

KB = 0.0083144626
FCOUL = 138.935458
M_O, M_H = 15.9994, 1.008
R_OH, R_OM = 0.09572, 0.01546
TH = math.radians(104.52)
R_HH = 2 * R_OH * math.sin(TH / 2)
Q_H, Q_M = 0.5564, -1.1128
SIG, EPS = 0.31589, 0.7749
# virtual site: r_M = r_O + wM * ((r_H1 - r_O) + (r_H2 - r_O)),  wM = R_OM / (2 R_OH cos(TH/2))
W_M = R_OM / (2 * R_OH * math.cos(TH / 2))


class Water:
    def __init__(self, n_side, density=33.33, T=298.0, rc=0.9, seed=1):
        rng = np.random.default_rng(seed)
        N = n_side ** 3
        self.N = N; self.T = T; self.rc = rc
        self.L = (N / density) ** (1 / 3)
        a = self.L / n_side
        # lattice of O positions, random orientations
        g = np.stack(np.meshgrid(*[np.arange(n_side)] * 3, indexing='ij'), -1).reshape(-1, 3) * a + a / 2
        self.rO = g.copy()
        # molecule frame: O at origin, H1/H2 in plane
        h1 = np.array([R_OH * math.sin(TH / 2), R_OH * math.cos(TH / 2), 0.0])
        h2 = np.array([-R_OH * math.sin(TH / 2), R_OH * math.cos(TH / 2), 0.0])
        self.rH1 = np.empty_like(g); self.rH2 = np.empty_like(g)
        for i in range(N):
            R = self._rand_rot(rng)
            self.rH1[i] = g[i] + R @ h1; self.rH2[i] = g[i] + R @ h2
        # velocities: Maxwell on atoms, then remove constraint components via RATTLE later
        m = np.array([M_O, M_H, M_H])
        self.v = np.stack([rng.normal(0, math.sqrt(KB * T / mm), (N, 3)) for mm in m], 1)  # (N,3atoms,3)
        self.v -= self.v.mean(axis=(0, 1))
        self.mass = np.array([M_O, M_H, M_H])
        self.k_rf = 1.0 / (2 * rc ** 3)
        self.c_rf = 3.0 / (2 * rc)
        self.pos = np.stack([self.rO, self.rH1, self.rH2], 1)  # (N,3,3)
        self._iu = np.triu_indices(N, 1)
        self._rattle_positions()
        self._rattle_velocities()

    @staticmethod
    def _rand_rot(rng):
        q = rng.normal(size=4); q /= np.linalg.norm(q); a, b, c, d = q
        return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                         [2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)],
                         [2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d]])

    # ---------------- constraints (RATTLE) ----------------
    PAIRS = ((0, 1, R_OH), (0, 2, R_OH), (1, 2, R_HH))

    def _rattle_positions(self, ref=None, tol=1e-7, maxit=50):
        """SHAKE on self.pos (and velocities if ref given: standard RATTLE stage 1)."""
        p = self.pos
        for it in range(maxit):
            maxdev = 0.0
            for (i, j, d0) in self.PAIRS:
                rij = p[:, i] - p[:, j]
                d2 = np.einsum('ni,ni->n', rij, rij)
                dev = d0 * d0 - d2
                maxdev = max(maxdev, float(np.abs(dev).max()))
                if ref is None:
                    g = dev / (2 * (1 / self.mass[i] + 1 / self.mass[j]) * d2)
                    corr = g[:, None] * rij
                else:
                    r0 = ref[:, i] - ref[:, j]
                    g = dev / (2 * (1 / self.mass[i] + 1 / self.mass[j]) * np.einsum('ni,ni->n', r0, rij))
                    corr = g[:, None] * r0
                    self.v[:, i] += corr / self.mass[i] / self.dt; self.v[:, j] -= corr / self.mass[j] / self.dt
                p[:, i] += corr / self.mass[i]; p[:, j] -= corr / self.mass[j]
            if maxdev < 1e-9: break

    def _rattle_velocities(self, tol=1e-9, maxit=50):
        p = self.pos; v = self.v
        for it in range(maxit):
            maxv = 0.0
            for (i, j, d0) in self.PAIRS:
                rij = p[:, i] - p[:, j]; vij = v[:, i] - v[:, j]
                k = np.einsum('ni,ni->n', rij, vij) / (d0 * d0 * (1 / self.mass[i] + 1 / self.mass[j]))
                maxv = max(maxv, float(np.abs(k).max()))
                v[:, i] -= (k / self.mass[i])[:, None] * rij; v[:, j] += (k / self.mass[j])[:, None] * rij
            if maxv < tol: break

    # ---------------- forces ----------------
    def forces(self):
        L, rc = self.L, self.rc
        p = self.pos; rO = p[:, 0]
        rM = rO + W_M * ((p[:, 1] - rO) + (p[:, 2] - rO))
        # molecule prelist with O-O < rc + 0.2 nm (site offsets <= 0.096 nm each), then SITE-based cutoff r < rc:
        # with eps_rf = inf both V and F vanish at rc, so each site pair switches on smoothly (no group-cutoff jumps)
        d = rO[:, None, :] - rO[None, :, :]
        d -= L * np.round(d / L)
        r2 = np.einsum('ijk,ijk->ij', d, d)
        iu = self._iu
        sel = r2[iu] < (rc + 0.2) ** 2
        I, J = iu[0][sel], iu[1][sel]
        F = np.zeros_like(p); FM = np.zeros((self.N, 3))
        # LJ O-O (site cutoff = O-O distance)
        dOO = d[I, J]; r2o = r2[I, J]
        mlj = r2o < rc * rc
        inv6 = (SIG * SIG / r2o[mlj]) ** 3
        fl = 24 * EPS * (2 * inv6 * inv6 - inv6) / r2o[mlj]
        fvec = fl[:, None] * dOO[mlj]
        np.add.at(F[:, 0], I[mlj], fvec); np.add.at(F[:, 0], J[mlj], -fvec)
        E = float(np.sum(4 * EPS * (inv6 * inv6 - inv6))) - float(mlj.sum()) * 4 * EPS * ((SIG / rc) ** 12 - (SIG / rc) ** 6)
        shift = dOO - (rO[I] - rO[J])
        sites = [(p[:, 1], Q_H), (p[:, 2], Q_H), (rM, Q_M)]
        for a, (ra, qa) in enumerate(sites):
            for b, (rb, qb) in enumerate(sites):
                dv = ra[I] - rb[J] + shift
                r2s = np.einsum('ni,ni->n', dv, dv)
                m = r2s < rc * rc
                r2s = r2s[m]; dv = dv[m]; Im = I[m]; Jm = J[m]
                r = np.sqrt(r2s)
                qq = FCOUL * qa * qb
                E += float(np.sum(qq * (1 / r + self.k_rf * r2s - self.c_rf)))
                fs = qq * (1 / (r2s * r) - 2 * self.k_rf)
                fv = fs[:, None] * dv
                if a < 2: np.add.at(F[:, a + 1], Im, fv)
                else: np.add.at(FM, Im, fv)
                if b < 2: np.add.at(F[:, b + 1], Jm, -fv)
                else: np.add.at(FM, Jm, -fv)
        # redistribute M force to O, H1, H2
        F[:, 0] += (1 - 2 * W_M) * FM; F[:, 1] += W_M * FM; F[:, 2] += W_M * FM
        return F, E

    # ---------------- integration ----------------
    def kinetic(self):
        return 0.5 * float(np.einsum('a,nai,nai->', self.mass, self.v, self.v))

    def temperature(self):
        ndof = 6 * self.N - 3
        return 2 * self.kinetic() / (ndof * KB)

    def run(self, nsteps, dt=0.002, tau_T=None, callback=None, cb_every=10):
        self.dt = dt
        F, E = self.forces()
        for step in range(nsteps):
            ref = self.pos.copy()
            self.v += 0.5 * dt * F / self.mass[None, :, None]
            self.pos += dt * self.v
            self._rattle_positions(ref=ref)
            F, E = self.forces()
            self.v += 0.5 * dt * F / self.mass[None, :, None]
            self._rattle_velocities()
            if tau_T:
                lam = math.sqrt(1 + dt / tau_T * (self.T / max(self.temperature(), 1e-9) - 1))
                self.v *= lam
            if callback and step % cb_every == 0:
                callback(step, E)
        return E
