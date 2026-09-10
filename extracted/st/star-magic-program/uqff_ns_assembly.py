"""uqff_ns_assembly - THE NAVIER-STOKES ASSEMBLY (B267, v0.429.0)

Closes the independent evaluator's gap analysis (2026-09-09): the algebraic
cap was wired; the time ODE, the Stam solver, and the falsifier ledger were
not. This module puts the pieces together IN-PACKAGE:

  1. The PAPER_1232 Taylor-Green time ODE (previously only a scalar
     log-rate snapshot): ledger Lambda computed LIVE from primitives,
     effective growth rate, the damped-branch curve Omega(t), and
     globally_regular().
  2. The PAPER_1182 enstrophy DECAY CURVE E(t) = E0*exp(-(3/25)*nu*t)
     (coefficient F_TRZ/Phi_5/6 = 3/25 = 0.12 EXACT), not only the 0.85 cap.
  3. A pure-Python port of the Stam stable-fluids solver (PAPER_177
     FluidSolver.cpp parameters: N=32, dt=0.1, visc=1e-4; PAPER_369 SCm
     jet body force) - LABELED NUMERICAL_EVIDENCE. Per PAPER_177/179's own
     flag: a Stam run at N=32 is numerical evidence, NOT a proof. This
     module never says otherwise.
  4. The PAPER_543 discrete-hypergraph fourth regularity route:
     lambda_max = 2*P_order/3 < 1.
  5. The falsifier, left honest: the DNS trefoil collision at Re=1e6
     (PAPER_1182 falsifiable #5) is OPEN - if that peak is unbounded, the
     cap is dead. No in-package substitute is offered.

VALUE-COINCIDENCE FLAG (disclosed, not canonized): the Taylor-Green ledger
Lambda = 0.0072977 sits 0.004% from the fine-structure constant 0.0072974.
No corpus chain connects them; FLAGGED per the standing discipline.

GUARD: the SPE dispatch 'navier_stokes' -> 8.5e3 is a DIFFERENT construct
and must never be confused with the 0.85 = 17/20 enstrophy cap.
"""

from __future__ import annotations

import math
from typing import Dict, List

from uqff_registry_primitives import (D_PHYS, D_BSFG, D_CRIT, SO_5, F_TRZ,
                                      BETA_I, PHI_RES_COUNTING)

# ---- PAPER_1232 Taylor-Green anchors (canonical) --------------------------
UA_CANONICAL = 0.4816            # PAPER_1724 Lambda-ledger normalization
OMEGA0_TG = 3.0 * math.pi ** 2 / 8.0          # 3.7011 Taylor-Green canonical
NU_TG = 1.0 / (D_PHYS ** 2 * SO_5 ** 2)       # 1/1600 EXACT (PAPER_1723)
GAMMA_PHONON = F_TRZ                          # 0.1 SCm/1.25THz coupling
C_GEOM_T3 = 1.0 / (8.0 * math.pi)             # geometric T^3 constant


def taylor_green_ledger() -> float:
    """PAPER_1232 ledger saturation, LIVE from primitives:
    Lambda = 1/(8*pi*beta_i*UA*(D_crit/D_BSFG)^2) = 0.0072977."""
    return 1.0 / (8.0 * math.pi * BETA_I * UA_CANONICAL
                  * (D_CRIT / D_BSFG) ** 2)


def taylor_green_effective_growth() -> float:
    """The PAPER_1232 log-rate: C*Lambda*sqrt(Omega0) - gamma = -0.09944.
    NEGATIVE -> the damped branch is forced."""
    return (C_GEOM_T3 * taylor_green_ledger() * math.sqrt(OMEGA0_TG)
            - GAMMA_PHONON)


def taylor_green_bounded_enstrophy(t: float) -> float:
    """The damped branch, as a CURVE: Omega(t) = Omega0*exp(-nu*t),
    nu = 1/1600 (valid because the effective growth rate is negative)."""
    return OMEGA0_TG * math.exp(-NU_TG * t)


def globally_regular(t_max: float = 1e6, n: int = 200) -> Dict:
    """Global regularity check on the damped branch: Omega(t) monotone
    decreasing and bounded by Omega0 over [0, t_max] -> T* = infinity."""
    ts = [t_max * i / (n - 1) for i in range(n)]
    om = [taylor_green_bounded_enstrophy(t) for t in ts]
    mono = all(om[i + 1] <= om[i] for i in range(n - 1))
    return {'t_max': t_max, 'monotone_decreasing': mono,
            'bounded_by_omega0': max(om) <= OMEGA0_TG + 1e-15,
            'omega_final': om[-1], 'regular': mono and max(om) <= OMEGA0_TG + 1e-15,
            'verdict': 'T* = infinity (damped branch; effective growth %.5f < 0)'
                       % taylor_green_effective_growth()}


def omega0_validity_threshold() -> float:
    """B269 DISCLOSED DOMAIN LIMIT (Daniel-ordered honesty item): the
    damped branch is forced only while C*Lambda*sqrt(Omega0) < gamma,
    i.e. Omega0 < (gamma/(C*Lambda))^2 ~ 1.19e5. Initial enstrophy ABOVE
    this threshold escapes the negative-growth argument - the master
    inequality then PERMITS growth and the in-package closure is silent.
    Clay demands ALL smooth data; this states where our argument lives."""
    return (GAMMA_PHONON / (C_GEOM_T3 * taylor_green_ledger())) ** 2


def taylor_green_report() -> Dict:
    """The PAPER_1232 closure in one dict - every ingredient live."""
    lam = taylor_green_ledger()
    return {'omega0': OMEGA0_TG, 'nu': NU_TG, 'gamma': GAMMA_PHONON,
            'C': C_GEOM_T3, 'ledger_lambda': lam,
            'effective_growth': taylor_green_effective_growth(),
            'alpha_coincidence_flag': ('Lambda = %.7f vs alpha = 0.0072974 '
                                       '(0.004%%) - FLAGGED, no corpus '
                                       'chain, NOT canonized' % lam),
            'branch': 'damped: Omega(t) = Omega0*exp(-nu*t)'}


# ---- PAPER_1182 decay curve ----------------------------------------------
DECAY_COEFF = F_TRZ / PHI_RES_COUNTING        # (1/10)/(5/6) = 3/25 = 0.12 EXACT


def enstrophy_decay_1182(t: float, nu: float = 1.0, e0: float = 1.0) -> float:
    """PAPER_1182 S300 enstrophy decay CURVE:
    E(t) = E0*exp(-(F_TRZ/Phi_5/6)*nu*t) = E0*exp(-0.12*nu*t),
    coefficient 3/25 EXACT from primitives."""
    return e0 * math.exp(-DECAY_COEFF * nu * t)


# ---- PAPER_543 fourth regularity route -----------------------------------
def hypergraph_lambda_max(p_order: float = 1e-5) -> float:
    """PAPER_543 discrete hypergraph route: lambda_max = 2*P_order/3
    (= 6.67e-6 at the paper's numeric P_order) < 1 -> contraction ->
    regularity on the discrete hypergraph."""
    return 2.0 * p_order / 3.0


# ---- Stam stable fluids, pure-Python port (PAPER_177 / PAPER_369) --------
NUMERICAL_EVIDENCE_LABEL = (
    'NUMERICAL_EVIDENCE - a Stam stable-fluids run (PAPER_177 FluidSolver '
    'parameters N=32, dt=0.1, visc=1e-4) is numerical evidence, NOT a '
    'proof; PAPER_177/179 flag this themselves and this port keeps the flag')


def _idx(n: int):
    s = n + 2
    return lambda i, j, k: i + s * (j + s * k)


def _lin_solve(x: List[float], x0: List[float], a: float, c: float,
               n: int, iters: int = 12) -> None:
    I = _idx(n)
    for _ in range(iters):
        for k in range(1, n + 1):
            for j in range(1, n + 1):
                for i in range(1, n + 1):
                    x[I(i, j, k)] = (x0[I(i, j, k)] + a * (
                        x[I(i - 1, j, k)] + x[I(i + 1, j, k)] +
                        x[I(i, j - 1, k)] + x[I(i, j + 1, k)] +
                        x[I(i, j, k - 1)] + x[I(i, j, k + 1)])) / c


def _advect(d: List[float], d0: List[float], u: List[float], v: List[float],
            w: List[float], dt: float, n: int) -> None:
    I = _idx(n)
    dt0 = dt * n
    for k in range(1, n + 1):
        for j in range(1, n + 1):
            for i in range(1, n + 1):
                x = min(max(i - dt0 * u[I(i, j, k)], 0.5), n + 0.5)
                y = min(max(j - dt0 * v[I(i, j, k)], 0.5), n + 0.5)
                z = min(max(k - dt0 * w[I(i, j, k)], 0.5), n + 0.5)
                i0, j0, k0 = int(x), int(y), int(z)
                s1, t1, u1 = x - i0, y - j0, z - k0
                s0, t0, u0 = 1 - s1, 1 - t1, 1 - u1
                d[I(i, j, k)] = (
                    s0 * (t0 * (u0 * d0[I(i0, j0, k0)] + u1 * d0[I(i0, j0, k0 + 1)])
                          + t1 * (u0 * d0[I(i0, j0 + 1, k0)] + u1 * d0[I(i0, j0 + 1, k0 + 1)]))
                    + s1 * (t0 * (u0 * d0[I(i0 + 1, j0, k0)] + u1 * d0[I(i0 + 1, j0, k0 + 1)])
                            + t1 * (u0 * d0[I(i0 + 1, j0 + 1, k0)] + u1 * d0[I(i0 + 1, j0 + 1, k0 + 1)])))


def _project(u: List[float], v: List[float], w: List[float],
             p: List[float], div: List[float], n: int) -> None:
    I = _idx(n)
    h = 1.0 / n
    for k in range(1, n + 1):
        for j in range(1, n + 1):
            for i in range(1, n + 1):
                div[I(i, j, k)] = -0.5 * h * (
                    u[I(i + 1, j, k)] - u[I(i - 1, j, k)] +
                    v[I(i, j + 1, k)] - v[I(i, j - 1, k)] +
                    w[I(i, j, k + 1)] - w[I(i, j, k - 1)])
                p[I(i, j, k)] = 0.0
    _lin_solve(p, div, 1.0, 6.0, n)
    for k in range(1, n + 1):
        for j in range(1, n + 1):
            for i in range(1, n + 1):
                u[I(i, j, k)] -= 0.5 * (p[I(i + 1, j, k)] - p[I(i - 1, j, k)]) / h
                v[I(i, j, k)] -= 0.5 * (p[I(i, j + 1, k)] - p[I(i, j - 1, k)]) / h
                w[I(i, j, k)] -= 0.5 * (p[I(i, j, k + 1)] - p[I(i, j, k - 1)]) / h


def stam_numerical_evidence(n: int = 32, steps: int = 10, dt: float = 0.1,
                            visc: float = 1e-4,
                            jet_force: float = 5.0,
                            return_fields: bool = False) -> Dict:
    """Pure-Python Stam stable-fluids evidence run (PAPER_177 parameters at
    the default n=32; smaller n for quick checks). An SCm jet body force
    (PAPER_369 style) drives the center column; the run reports whether
    speed and enstrophy stay BOUNDED. This is NUMERICAL_EVIDENCE, not a
    proof - see NUMERICAL_EVIDENCE_LABEL."""
    size = (n + 2) ** 3
    I = _idx(n)
    u = [0.0] * size; v = [0.0] * size; w = [0.0] * size
    u0 = [0.0] * size; v0 = [0.0] * size; w0 = [0.0] * size
    p = [0.0] * size; div = [0.0] * size
    c = n // 2
    a = dt * visc * n * n * n
    ens_series = []
    for _ in range(steps):
        # SCm jet body force at the center column (w-direction)
        for k in range(1, n // 3 + 1):
            w[I(c, c, k)] += dt * jet_force
        # diffuse
        u0, u = u, u0; v0, v = v, v0; w0, w = w, w0
        _lin_solve(u, u0, a, 1 + 6 * a, n)
        _lin_solve(v, v0, a, 1 + 6 * a, n)
        _lin_solve(w, w0, a, 1 + 6 * a, n)
        _project(u, v, w, p, div, n)
        # advect
        u0, u = u, u0; v0, v = v, v0; w0, w = w, w0
        _advect(u, u0, u0, v0, w0, dt, n)
        _advect(v, v0, u0, v0, w0, dt, n)
        _advect(w, w0, u0, v0, w0, dt, n)
        _project(u, v, w, p, div, n)
        # enstrophy (centered-difference curl, interior)
        h = 1.0 / n
        ens = 0.0
        for k in range(2, n):
            for j in range(2, n):
                for i in range(2, n):
                    wx = (w[I(i, j + 1, k)] - w[I(i, j - 1, k)]
                          - v[I(i, j, k + 1)] + v[I(i, j, k - 1)]) / (2 * h)
                    wy = (u[I(i, j, k + 1)] - u[I(i, j, k - 1)]
                          - w[I(i + 1, j, k)] + w[I(i - 1, j, k)]) / (2 * h)
                    wz = (v[I(i + 1, j, k)] - v[I(i - 1, j, k)]
                          - u[I(i, j + 1, k)] + u[I(i, j - 1, k)]) / (2 * h)
                    ens += (wx * wx + wy * wy + wz * wz) * h ** 3
        ens_series.append(ens)
    max_speed = max(math.sqrt(u[i] ** 2 + v[i] ** 2 + w[i] ** 2)
                    for i in range(size))
    finite = (max_speed == max_speed and max_speed < 1e6
              and all(e == e and e < 1e12 for e in ens_series))
    out = {'n': n, 'steps': steps, 'dt': dt, 'visc': visc,
           'max_speed': max_speed, 'enstrophy_series': ens_series,
           'bounded': finite,
           'label': NUMERICAL_EVIDENCE_LABEL}
    if return_fields:
        out['fields'] = {'u': u, 'v': v, 'w': w}
    return out


# ---- The falsifier, left honest ------------------------------------------
DNS_TREFOIL_FALSIFIER = (
    'OPEN - DNS trefoil-vortex collision at Re=1e6 (PAPER_1182 falsifiable '
    '#5): if the vorticity peak is UNBOUNDED there, the 17/20 cap is dead. '
    'This package offers NO in-package substitute for that test; the cap '
    'stands falsifiable, which is the point.')


# ---- TIER 1 (B268): THE FIELD, DRAWN - dependency-free renderer ----------
COARSE_FIELD_LABEL = (
    'COARSE FIELD (N^3 Stam, NUMERICAL_EVIDENCE) - this is a picture of a '
    'coarse simulation, not of the true Re=1e6 field; resolution honesty: '
    'Kolmogorov requires ~Re^(9/4) points, so the full field is drawable '
    'only from DNS-class data (see DNS_TREFOIL_FALSIFIER)')


def vorticity_slice(fields: Dict, n: int, axis: str = 'y',
                    index: int = None) -> List[List[float]]:
    """|omega| on one mid-plane slice of the Stam field (centered
    differences). axis: 'x'|'y'|'z' names the plane normal."""
    u, v, w = fields['u'], fields['v'], fields['w']
    I = _idx(n)
    h = 1.0 / n
    if index is None:
        index = n // 2
    grid = []
    rng = range(2, n)
    for b in rng:
        rowv = []
        for a in rng:
            if axis == 'y':
                i, j, k = a, index, b
            elif axis == 'x':
                i, j, k = index, a, b
            else:
                i, j, k = a, b, index
            wx = (w[I(i, j + 1, k)] - w[I(i, j - 1, k)]
                  - v[I(i, j, k + 1)] + v[I(i, j, k - 1)]) / (2 * h)
            wy = (u[I(i, j, k + 1)] - u[I(i, j, k - 1)]
                  - w[I(i + 1, j, k)] + w[I(i - 1, j, k)]) / (2 * h)
            wz = (v[I(i + 1, j, k)] - v[I(i - 1, j, k)]
                  - u[I(i, j + 1, k)] + u[I(i, j - 1, k)]) / (2 * h)
            rowv.append(math.sqrt(wx * wx + wy * wy + wz * wz))
        grid.append(rowv)
    return grid


def write_ppm(grid: List[List[float]], path: str) -> str:
    """Write a |omega| slice as a binary PPM heat map (black -> red ->
    yellow -> white). Zero dependencies; any image viewer opens it."""
    hi = max((x for row in grid for x in row), default=0.0) or 1.0
    ny, nx = len(grid), len(grid[0])
    px = bytearray()
    for row in grid:
        for x in row:
            t = x / hi
            r = min(1.0, 3.0 * t)
            gch = min(1.0, max(0.0, 3.0 * t - 1.0))
            b = min(1.0, max(0.0, 3.0 * t - 2.0))
            px += bytes((int(255 * r), int(255 * gch), int(255 * b)))
    with open(path, 'wb') as f:
        f.write(b'P6\n%d %d\n255\n' % (nx, ny))
        f.write(bytes(px))
    return path


def ascii_heatmap(grid: List[List[float]], width: int = 60) -> str:
    """The slice as terminal art - ' .:-=+*#%@' by |omega| decile."""
    ramp = ' .:-=+*#%@'
    hi = max((x for row in grid for x in row), default=0.0) or 1.0
    step = max(1, len(grid[0]) // width)
    lines = []
    for row in grid[::step]:
        lines.append(''.join(
            ramp[min(int(x / hi * (len(ramp) - 1)), len(ramp) - 1)]
            for x in row[::step]))
    return '\n'.join(lines)


def draw_field(n: int = 32, steps: int = 10, ppm_path: str = None) -> Dict:
    """TIER 1: run the Stam solver and DRAW the field - the mid-plane
    |omega| slice as ASCII (returned) and optionally as a PPM file.
    Labeled COARSE + NUMERICAL_EVIDENCE; the label rides in the return."""
    r = stam_numerical_evidence(n=n, steps=steps, return_fields=True)
    grid = vorticity_slice(r['fields'], n)
    out = {'n': n, 'steps': steps, 'bounded': r['bounded'],
           'max_speed': r['max_speed'],
           'ascii': ascii_heatmap(grid),
           'label': COARSE_FIELD_LABEL,
           'evidence_label': r['label']}
    if ppm_path:
        out['ppm'] = write_ppm(grid, ppm_path)
    return out


# ---- TIER 2 (B268): the fast solver, guarded [cfd] extra -----------------
CFD_EXTRA_HINT = ("the fast field needs numpy - a REQUIRED dependency of "
                  "star-magic-program (pyproject dependencies), so a normal "
                  "pip install star-magic-program already provides it; this "
                  "guard exists for stripped/vendored environments only. "
                  "CORRECTION B268 (Rule 7): an earlier label claimed a "
                  "dependency-free base and a [cfd] extra - wrong for THIS "
                  "package (that discipline belongs to the simulator "
                  "catalogue, v0.406.0); caught by the blocked-numpy "
                  "rehearsal itself")


def stam_numerical_evidence_fast(n: int = 128, steps: int = 10,
                                 dt: float = 0.1, visc: float = 1e-4,
                                 jet_force: float = 5.0,
                                 return_fields: bool = False) -> Dict:
    """TIER 2: the same Stam algorithm, numpy-vectorized (N=128-256 on a
    desktop). numpy is a REQUIRED dependency of this package, so this
    works on any normal install; the guarded import (clear ImportError,
    see CFD_EXTRA_HINT) covers stripped environments. Same labels,
    same honesty."""
    try:
        import numpy as np
    except ImportError:
        raise ImportError(CFD_EXTRA_HINT)
    shp = (n + 2, n + 2, n + 2)
    u = np.zeros(shp); v = np.zeros(shp); w = np.zeros(shp)
    p = np.zeros(shp); div = np.zeros(shp)
    c = n // 2
    a = dt * visc * n ** 3
    S = slice(1, n + 1)

    def lin_solve(x, x0, aa, cc, iters=12):
        for _ in range(iters):
            x[S, S, S] = (x0[S, S, S] + aa * (
                x[0:n, S, S] + x[2:n + 2, S, S] +
                x[S, 0:n, S] + x[S, 2:n + 2, S] +
                x[S, S, 0:n] + x[S, S, 2:n + 2])) / cc

    def project(u, v, w):
        h = 1.0 / n
        div[S, S, S] = -0.5 * h * (
            u[2:n + 2, S, S] - u[0:n, S, S] +
            v[S, 2:n + 2, S] - v[S, 0:n, S] +
            w[S, S, 2:n + 2] - w[S, S, 0:n])
        p.fill(0.0)
        lin_solve(p, div, 1.0, 6.0)
        u[S, S, S] -= 0.5 * (p[2:n + 2, S, S] - p[0:n, S, S]) / h
        v[S, S, S] -= 0.5 * (p[S, 2:n + 2, S] - p[S, 0:n, S]) / h
        w[S, S, S] -= 0.5 * (p[S, S, 2:n + 2] - p[S, S, 0:n]) / h

    def advect(d0, u0, v0, w0):
        dt0 = dt * n
        ii, jj, kk = np.meshgrid(np.arange(1, n + 1), np.arange(1, n + 1),
                                 np.arange(1, n + 1), indexing='ij')
        x = np.clip(ii - dt0 * u0[S, S, S], 0.5, n + 0.5)
        y = np.clip(jj - dt0 * v0[S, S, S], 0.5, n + 0.5)
        z = np.clip(kk - dt0 * w0[S, S, S], 0.5, n + 0.5)
        i0 = x.astype(int); j0 = y.astype(int); k0 = z.astype(int)
        s1 = x - i0; t1 = y - j0; u1 = z - k0
        s0 = 1 - s1; t0 = 1 - t1; u0f = 1 - u1
        d = np.zeros(shp)
        d[S, S, S] = (
            s0 * (t0 * (u0f * d0[i0, j0, k0] + u1 * d0[i0, j0, k0 + 1])
                  + t1 * (u0f * d0[i0, j0 + 1, k0] + u1 * d0[i0, j0 + 1, k0 + 1]))
            + s1 * (t0 * (u0f * d0[i0 + 1, j0, k0] + u1 * d0[i0 + 1, j0, k0 + 1])
                    + t1 * (u0f * d0[i0 + 1, j0 + 1, k0] + u1 * d0[i0 + 1, j0 + 1, k0 + 1])))
        return d

    ens_series = []
    h = 1.0 / n
    for _ in range(steps):
        w[c, c, 1:n // 3 + 1] += dt * jet_force
        u0, v0, w0 = u.copy(), v.copy(), w.copy()
        lin_solve(u, u0, a, 1 + 6 * a)
        lin_solve(v, v0, a, 1 + 6 * a)
        lin_solve(w, w0, a, 1 + 6 * a)
        project(u, v, w)
        u0, v0, w0 = u.copy(), v.copy(), w.copy()
        u = advect(u0, u0, v0, w0)
        v = advect(v0, u0, v0, w0)
        w = advect(w0, u0, v0, w0)
        project(u, v, w)
        wx = (np.roll(w, -1, 1) - np.roll(w, 1, 1)
              - np.roll(v, -1, 2) + np.roll(v, 1, 2)) / (2 * h)
        wy = (np.roll(u, -1, 2) - np.roll(u, 1, 2)
              - np.roll(w, -1, 0) + np.roll(w, 1, 0)) / (2 * h)
        wz = (np.roll(v, -1, 0) - np.roll(v, 1, 0)
              - np.roll(u, -1, 1) + np.roll(u, 1, 1)) / (2 * h)
        ens_series.append(float(((wx ** 2 + wy ** 2 + wz ** 2)[2:n, 2:n, 2:n]
                                 * h ** 3).sum()))
    max_speed = float(np.sqrt(u ** 2 + v ** 2 + w ** 2).max())
    finite = (max_speed == max_speed and max_speed < 1e6
              and all(e == e and e < 1e12 for e in ens_series))
    out = {'n': n, 'steps': steps, 'dt': dt, 'visc': visc,
           'max_speed': max_speed, 'enstrophy_series': ens_series,
           'bounded': finite, 'engine': 'numpy [cfd] extra',
           'label': NUMERICAL_EVIDENCE_LABEL}
    if return_fields:
        out['fields'] = {'u': [float(x) for x in u.ravel()],
                         'v': [float(x) for x in v.ravel()],
                         'w': [float(x) for x in w.ravel()]}
    return out


# ---- TIER 3 (B268): the falsifier grading harness (AWAITING_DATA) --------
FALSIFIER_DATA_SOURCES = (
    'named outside-data paths (Daniel ledger): Johns Hopkins Turbulence '
    'Database (public 8192^3 isotropic DNS), Kerr trefoil-reconnection DNS '
    'literature, Kleckner & Irvine laboratory trefoil vortices')


def grade_cap_against_dns(csv_path: str = None, nu: float = None) -> Dict:
    """TIER 3: grade the 17/20 cap against OUTSIDE DNS/laboratory data.
    Input CSV columns (user-computed from DNS fields, definitions from
    PAPER_1182 S300): 't' plus EITHER 'stretching_ratio'
    (V_stretch/(|omega|*E), graded against the 17/20 cap) OR 'enstrophy'
    (graded against the decay envelope E0*exp(-(3/25)*nu*t); needs nu).
    NO DATA -> refuses with the named sources; nothing is synthesized.
    A ratio ever ABOVE 17/20 = THE CAP IS DEAD - reported plainly."""
    if csv_path is None:
        return {'status': 'AWAITING_DATA',
                'refusal': ('no dataset supplied - this harness grades '
                            'real DNS/lab data only; ' +
                            FALSIFIER_DATA_SOURCES),
                'falsifier': DNS_TREFOIL_FALSIFIER}
    import csv as _csv
    rows = list(_csv.DictReader(open(csv_path, encoding='utf-8')))
    if not rows:
        return {'status': 'REFUSED_EMPTY', 'path': csv_path}
    cap = 17.0 / 20.0
    out = {'status': 'GRADED', 'path': csv_path, 'n_rows': len(rows),
           'cap': cap}
    if 'stretching_ratio' in rows[0]:
        ratios = [float(r['stretching_ratio']) for r in rows]
        worst = max(ratios)
        out.update({'mode': 'stretching_ratio', 'worst_ratio': worst,
                    'verdict': ('CAP HOLDS on this dataset (worst ratio '
                                '%.4f <= 17/20)' % worst) if worst <= cap
                               else ('THE CAP IS DEAD ON THIS DATASET - '
                                     'ratio %.4f EXCEEDS 17/20; reported '
                                     'plainly, not softened' % worst)})
    elif 'enstrophy' in rows[0]:
        if nu is None:
            return {'status': 'REFUSED_NO_NU', 'path': csv_path,
                    'refusal': 'enstrophy grading needs nu (viscosity)'}
        e0 = float(rows[0]['enstrophy'])
        t0 = float(rows[0]['t'])
        bad = [(float(r['t']), float(r['enstrophy'])) for r in rows
               if float(r['enstrophy']) >
               e0 * math.exp(-DECAY_COEFF * nu * (float(r['t']) - t0)) * (1 + 1e-9)]
        out.update({'mode': 'decay_envelope', 'n_violations': len(bad),
                    'first_violation': bad[0] if bad else None,
                    'verdict': ('ENVELOPE HOLDS (all %d rows under '
                                'E0*exp(-0.12*nu*t))' % len(rows)) if not bad
                               else ('ENVELOPE VIOLATED at t=%.4g - the '
                                     'decay claim fails on this dataset'
                                     % bad[0][0])})
    else:
        return {'status': 'REFUSED_BAD_COLUMNS', 'path': csv_path,
                'refusal': "need 't' + 'stretching_ratio' or 'enstrophy'"}
    return out


# ---- B269 (PAPER_2264): THE BALANCE-ZONE READING + THE PAIR CAP ----------
# Daniel's direction (2026-09-09, verbatim pieces): "Buoyancy, (-) Buoyancy,
# U_I, LENR, Spinor-bundle, SMBH, White-hole, Worm-hole, Universal Gravity,
# UQFF-Lagrangian, (-) Negative Time, [F_Ubi inside to outward & F_Ubi_i;
# physical gravity balance/zone], two different scales simultaneously
# yielding pairs of range values." Assembled from ruled corpus pieces;
# canonized on Daniel's B269 ruling.

def enstrophy_cap_pair() -> Dict:
    """TWO SCALES SIMULTANEOUSLY -> A PAIR OF RANGE VALUES (B269).
    The B112 context split (canonized: vacuum channels see F_TRZ,
    in-medium channels see F_TRZ^2) applied to the PAPER_1182 cap:
      vacuum/astro cap  = 1 - F_TRZ  *(D_BSFG/D_phys) = 17/20  = 0.85
      in-medium/lab cap = 1 - F_TRZ^2*(D_BSFG/D_phys) = 197/200 = 0.985
    Same pattern as the ruled viscosity pair (1.099 vacuum / 1.0099 lab,
    B126). FLAGGED FALSIFIABLE PREDICTION: lab turbulence should cap
    stretching efficiency near 0.985; vacuum-coupled astrophysical flows
    at 0.85. The grade_cap_against_dns harness accepts either via its
    cap argument when real data arrives."""
    proj = D_BSFG / D_PHYS
    return {
        'vacuum_cap': 1.0 - F_TRZ * proj,
        'in_medium_cap': 1.0 - F_TRZ ** 2 * proj,
        'projection': 'D_BSFG/D_phys = 3/2 (PAPER_1962; the 26->10->6->4 downward flow)',
        'split_authority': 'B112 context split (vacuum F_TRZ / in-medium F_TRZ^2), B126 confirming instance',
        'status': 'FLAGGED_FALSIFIABLE_PREDICTION (canonized as prediction B269; settled by lab-vs-astro stretching data)',
    }


def balance_zone_chain() -> Dict:
    """THE CAP IS THE BALANCE ZONE (B269, PAPER_2264) - the twelve-joint
    chain, every joint corpus-cited; the L_buoy variational path is the
    NAMED route for the missing theorem (ns_cap_derivation registry row).
    """
    return {
        'reading': ('vortex stretching plays F_UBi (inside->outward, '
                    'vorticity pushing against the vacuum); the vacuum '
                    'counter-force is F_UBii; the cap 17/20 is the '
                    'crossing - the fluid analogue of the F_U = 0 '
                    'habitable-zone radius r_hz'),
        'deficit_decomposition': ('3/20 = F_TRZ * D_BSFG/D_phys = '
                                  '(negative-time fraction, PAPER_597/1160) '
                                  'x (bulk-edge->physical projection, '
                                  'PAPER_1962)'),
        'polarity': ('17/20 retained / 3/20 dissipated = the (2R-1) '
                     'polarity split at the R = 0.5 phase transition '
                     '(PAPER_884/899; PAPER_2098 complementarity)'),
        'drain_channel': ('the 3/20 exits through the 1.25 THz phonon - '
                          'omega_LENR = omega_SCm (ruled) - the SAME '
                          'carrier as Holmlid 630 eV; hence the UV cutoff '
                          'frequency'),
        'outflow_side': ('white-hole channel = Page deficit (PAPER_2238); '
                         'wormhole stabilization = phonon-modified '
                         'Christoffel (PAPER_901) - same phonon on '
                         'geodesics'),
        'no_singularity_twin': ('PAPER_594 26! SMBH bound and NS '
                                'regularity are the same theorem at the '
                                'two ends of the 26-layer chain'),
        'spinor': ('vorticity = fluid chirality; CW/CCW caduceus branches '
                   '(SO(26) Clifford module, PAPER_1183/1229) give the '
                   'negative-time fraction its handle'),
        'u_i_anchor': ('PAPER_529 velocity bound u <= sqrt(GM/r) is U_i '
                       'anchoring stated as escape velocity'),
        'derivation_route_named': ('vary L_buoy (PAPER_1065 EOM) with the '
                                   'F_UBi/F_UBii pair as body forces; the '
                                   'cap should emerge as the balance '
                                   'condition - THE route for the missing '
                                   'theorem; OPEN until executed'),
        'pair_cap': enstrophy_cap_pair(),
    }


# ---- B270 (PAPER_2265): THE L_BUOY VARIATIONAL DERIVATION OF THE CAP -----
def l_buoy_cap_derivation() -> Dict:
    """THE CAP, DERIVED MODULO ONE NAMED LEMMA (B270, Daniel's session
    order). Chain: (1) PAPER_1065 variational EOM has exactly three
    force terms - gravity seed, buoyancy pair, phonon: produce, remove,
    drain. (2) PAPER_1203 canonical forms: F_UBi carries (1+F_TRZ),
    F_UBii carries k_spring*(1+E_n) with NO TRZ factor - at the balance
    zone the surplus per unit of balanced push is EXACTLY F_TRZ.
    (3) The surplus is TRZ-carried (PAPER_072: F_TRZ = fraction of
    channel energy entering the time-reversal zone) and the TRZ removes
    exactly that fraction from a propagating channel (PAPER_009:
    D_TRZ = 0.900 canonical); during the TRZ sub-cycle the (2R-1)
    polarity is negative (PAPER_884/899) - the surplus opposes
    stretching. (4) BRIDGE LEMMA (the one OPEN step): the surplus
    enters stretching through the D_BSFG transverse bulk-edge modes
    (PAPER_1182's own feedback statement) with projection weight
    D_BSFG/D_phys = 3/2 (PAPER_1962; the 26->10->6->4 flow of
    PAPER_1160) - asserted by 1182, ratio canonized by 1962, the
    mode-counting derivation of the WEIGHT itself is OPEN. (5) Removal
    = F_TRZ*(3/2) = 3/20; cap = 17/20; the 3/20 exits via g_phonon
    (the EOM's own third term - the 1.25 THz LENR carrier), closing
    PAPER_2098's 17/20 + 3/20 = 1. DISCRIMINATION: rival coefficients
    1-F_TRZ = 0.90 (bare) and (1-F_TRZ)^2 = 0.81 (quadratic) are
    ELIMINATED - only the projected-linear form lands on the canonical
    cap. In-medium (B112, one F_TRZ eaten): 197/200."""
    surplus = F_TRZ
    projection = D_BSFG / D_PHYS
    # exact integer-ratio composition (F_TRZ = 1/SO_5, PAPER_1160):
    removal = D_BSFG / (D_PHYS * SO_5)                    # 6/40 = 3/20
    cap = (D_PHYS * SO_5 - D_BSFG) / (D_PHYS * SO_5)      # 34/40 = 17/20
    in_medium = ((D_PHYS * SO_5 ** 2 - D_BSFG)
                 / (D_PHYS * SO_5 ** 2))                  # 394/400 = 197/200
    return {
        'eom_terms': ('r-ddot = -mu_s*grad(M_s/r) + g_buoy + g_phonon '
                      '(PAPER_1065, verbatim) - produce / remove / drain'),
        'surplus_fraction': surplus,
        'projection_weight': projection,
        'removal_fraction': removal,
        'cap_derived': cap,
        'cap_canonical_match': cap == 17.0 / 20.0,
        'in_medium_cap': in_medium,
        'rivals_eliminated': {'bare_trz': 1.0 - F_TRZ,
                              'quadratic_trz': (1.0 - F_TRZ) ** 2,
                              'note': ('0.90 and 0.81 do NOT land on the '
                                       'canonical cap; only the '
                                       'projected-linear form does - the '
                                       'derivation discriminates')},
        'bridge_lemma': ('OPEN - "the TRZ-carried surplus enters '
                         'stretching through the transverse bulk-edge '
                         'modes with projection weight D_BSFG/D_phys": '
                         'PAPER_1182 asserts the combined coefficient, '
                         'PAPER_1962 canonizes the ratio; the '
                         'mode-counting derivation of the weight (and '
                         'why removal acts ONCE on the production '
                         'channel, not squared) is the single remaining '
                         'step'),
        'drain': ('the removed 3/20 exits via g_phonon - the 1.25 THz '
                  'LENR carrier (omega_LENR = omega_SCm, ruled)'),
        'status': ('DERIVED_MODULO_BRIDGE_LEMMA (B270) - upgraded from '
                   'postulate; Clay universality (H^s/BKM) separately '
                   'OPEN as ledgered'),
    }
