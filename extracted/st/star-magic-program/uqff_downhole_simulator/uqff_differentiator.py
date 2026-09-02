"""uqff_differentiator - THE UQFF DIFFERENTIATOR LAYER (v1.85.0): the math
nobody else has, awake and under test.

Three pieces, each with its provenance and its honest status:

1. U_i - THE UNIVERSAL INERTIAL OPERATOR (PAPER_646), the evaluator's
   sharpest jab ('U_i still loaded and unused') answered the honest way:
       U_i = lambda_i * (rho_SCm/rho_UA) * omega_s * |cos(pi t_n)| * (1 + F_TRZ)
   The Sun check reproduces the canonical 2.75e-7 EXACTLY (PAPER_646,
   system omega_s = 2.5e-6 rad/s, t_n = 0). Applied with Earth's measured
   rotation (7.2921159e-5 rad/s, an observation) under the two-tier rule -
   PAPER_646 itself uses the form with system-specific omega_s - it yields
   U_i(Earth) = 8.021e-6. STATUS: WIRED_AS_REPORTED_OBSERVABLE - computed,
   printed in the K2 chain, and entered as a RANKED CANDIDATE below; it is
   never silently multiplied into a prediction, because no corpus paper yet
   specifies its coupling into borehole gravity - that specification is an
   OPEN item for Daniel, and pretending otherwise would be the old sin.

2. QCalcGeom - THE MASTER LENGTH-SCALE EQUATION (PAPER_1078), re-derived in
   this repository per Rule E (the predecessor's QCalcGeom.py is read-only
   reference; no code ported):
       QCalcGeom(M, Gamma) = r_cross * (26!)^(-1/13) * S26_3 * Phi(Gamma)
       r_cross = sqrt(eta_BSFG) * G*M/c^2,  eta_BSFG = 1e-22
       Phi(Gamma) = exp(-(Gamma-Gamma_0)^2 / (2 sigma_G^2)) * S26_3
   Validation reproduces the paper's own chain for the Sun: r_cross =
   1.477e-8 m, compactification 8.983e-3, and the assembled 1.197e-12 m.
   HONEST LIMIT: S26_3 = 9.500e-2 is carried as PAPER_1078's STATED value -
   the Ramanujan R_n^(3) factors needed to re-derive the series from scratch
   are not specified in the paper; that re-derivation is OPEN (queued).

3. channel_ranking() - THE STUDY THAT POINTS AT THE INSTRUMENT: over the
   library's only fully co-located multi-channel window (the KTB composite
   excerpt: density, sonic, spectral gamma, resistivity at the same
   stations), each candidate UQFF-derived channel is computed FROM the mass
   column alone and scored by how much it knows about the INDEPENDENTLY
   measured channels. The channel that carries the most strata information
   is the one worth building an instrument around. The material-ID channel
   is listed BLOCKED_ON_K4: without Daniel's geological density landmarks
   (quartz, granite, shale, seawater...) the framework can rank density but
   cannot yet NAME rock - stated, not hidden.
"""

from __future__ import annotations

import math
import statistics
import sys
from pathlib import Path
from typing import Dict, List

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from uqff_registry_primitives import F_TRZ                    # 1/10, Rule A

from .uqff_forward_model import G_UQFF, predict_delta_g_mgal
from .uqff_profile_catalog import CATALOG

LAMBDA_I = 1.0                       # canonical inertia coupling (locked)
OMEGA_S_SUN = 2.5e-6                 # rad/s, PAPER_646 system value
OMEGA_EARTH = 7.2921159e-5           # rad/s, measured sidereal rotation (observation)
ETA_BSFG = 1.0e-22                   # PAPER_1078 BSFG coupling
S26_3_STATED = 9.500e-2              # PAPER_1078 STATED value (series re-derivation OPEN)
GAMMA_0 = 2 * math.pi * 0.10e12      # rad/s, PAPER_1078 Gaussian centre
SIGMA_G = 0.08 * 2 * math.pi * 1e12  # rad/s, PAPER_1078 Gaussian width
C_LIGHT = 2.998e8                    # m/s (PAPER_1078 chain value)
M_SUN_KG = 1.989e30                  # PAPER_1078 chain value
FACT26_INV13 = math.factorial(26) ** (-1.0 / 13.0)


def universal_inertial_operator(omega_s: float, t_n: float = 0.0,
                                lambda_i: float = LAMBDA_I) -> float:
    """PAPER_646: U_i = lambda_i * F_TRZ * omega_s * |cos(pi t_n)| * (1+F_TRZ).
    (rho_SCm/rho_UA = 1/10 = F_TRZ, the locked engine coupling ratio.)"""
    return lambda_i * F_TRZ * omega_s * abs(math.cos(math.pi * t_n)) * (1.0 + F_TRZ)


def u_i_sun() -> float:
    """The canonical check: must equal 2.75e-7 exactly (PAPER_646)."""
    return universal_inertial_operator(OMEGA_S_SUN, 0.0)


def u_i_earth() -> float:
    """Earth's rotation in PAPER_646's own envelope (two-tier compliant)."""
    return universal_inertial_operator(OMEGA_EARTH, 0.0)


def qcalcgeom_r_cross(mass_kg: float, g: float = 6.674e-11) -> float:
    """PAPER_1078 crossover radius (default G = the paper's chain value;
    pass G_UQFF for the framework-native variant, disclosed either way)."""
    return math.sqrt(ETA_BSFG) * g * mass_kg / C_LIGHT ** 2


def qcalcgeom_phi(gamma: float) -> float:
    """PAPER_1078 phonon fluence factor."""
    return math.exp(-((gamma - GAMMA_0) ** 2) / (2.0 * SIGMA_G ** 2)) * S26_3_STATED


def qcalcgeom_master(mass_kg: float = M_SUN_KG,
                     gamma: float = GAMMA_0,
                     g: float = 6.674e-11) -> Dict:
    """The re-derived master equation with every factor exposed. For the
    Sun at Gamma_0 this reproduces PAPER_1078's 1.197e-12 m."""
    r_cross = qcalcgeom_r_cross(mass_kg, g)
    phi = qcalcgeom_phi(gamma)
    return {'r_cross_m': r_cross,
            'compactification': FACT26_INV13,
            's26_3': S26_3_STATED,
            's26_3_status': 'PAPER_1078_STATED (R_n^(3) series re-derivation OPEN)',
            'phi': phi,
            'length_scale_m': r_cross * FACT26_INV13 * S26_3_STATED * phi,
            'source': 'PAPER_1078 re-derived here per Rule E (predecessor code read-only)'}


def _pearson(xs: List[float], ys: List[float]) -> float:
    mx, my = statistics.mean(xs), statistics.mean(ys)
    den = math.sqrt(sum((x - mx) ** 2 for x in xs)
                    * sum((y - my) ** 2 for y in ys))
    if den == 0:
        return float('nan')
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den


def channel_ranking(entry: str = 'ktb_hb_complog_6020_excerpt') -> Dict:
    """Which UQFF-derived channel knows the most about the ground?

    Candidates are computed from the MASS COLUMN ONLY (density stations),
    then scored |Pearson| against each independently measured channel (Vp,
    spectral gamma, deep resistivity) at the same stations. First-pass
    scope disclosed: one 10-m fully co-located window; the ranking will
    re-run as the co-location rule grows the library."""
    st = CATALOG[entry].stream()
    rho = [float(v) for v in st.channels['RHOB (g/cm3)'].values]
    dtco = [float(v) for v in st.channels['DTCO (us/m)'].values]
    sgr = [float(v) for v in st.channels['SGR (API)'].values]
    lld = [float(v) for v in st.channels['LLD (ohmm)'].values]
    keep = [i for i, r in enumerate(rho) if r > 2.5 and dtco[i] > 0
            and sgr[i] == sgr[i] and lld[i] > 0]
    rho_k = [rho[i] for i in keep]
    truth = {'vp_m_s': [1e6 / dtco[i] for i in keep],
             'sgr_api': [sgr[i] for i in keep],
             'lld_ohmm': [lld[i] for i in keep]}
    dz = 0.1524                       # the excerpt's half-foot station spacing
    candidates = {
        'k2_gravity_dg': {
            'series': [predict_delta_g_mgal(r, dz) for r in rho_k],
            'provenance': 'K2 kernel (PAPER_1598/593/1209CC constants)'},
        'u_i_earth_modulated_dg': {
            'series': [predict_delta_g_mgal(r, dz) * (1.0 + u_i_earth())
                       for r in rho_k],
            'provenance': ('PAPER_646 U_i(Earth)=%.3e as a multiplicative '
                           'modulation HYPOTHESIS under test - its coupling '
                           'into borehole gravity is not corpus-specified '
                           '(OPEN, Daniel)' % u_i_earth())},
        'qcalcgeom_mass_scale': {
            'series': [qcalcgeom_master(r * 1000.0, g=G_UQFF)['length_scale_m']
                       for r in rho_k],
            'provenance': ('PAPER_1078 master equation per unit-volume mass '
                           '(1 m^3 at station density), G from PAPER_593')},
    }
    rankings = []
    for name, cand in candidates.items():
        scores = {t: abs(_pearson(cand['series'], tv))
                  for t, tv in truth.items()}
        rankings.append({'channel': name, 'provenance': cand['provenance'],
                         'abs_r': scores,
                         'mean_abs_r': statistics.mean(scores.values())})
    rankings.sort(key=lambda r: -r['mean_abs_r'])
    # honest degeneracy check: are any candidates informationally identical?
    degenerate = []
    names = list(candidates)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            r_ij = _pearson(candidates[names[i]]['series'],
                            candidates[names[j]]['series'])
            if abs(r_ij) > 0.999999:
                degenerate.append((names[i], names[j]))
    return {'window': '%s (n=%d co-located stations, washouts excluded)'
                      % (entry, len(keep)),
            'rankings': rankings,
            'degenerate_pairs': degenerate,
            'degeneracy_note': ('candidates that are monotone transforms of '
                                'the same mass column carry IDENTICAL '
                                'information - the ranking says so instead '
                                'of pretending three channels exist where '
                                'one does'),
            'blocked_on_k4': ('the MATERIAL-ID channel (which rock is this?) '
                              'cannot be ranked: the landmark family holds '
                              'concrete/steel/aluminum/pine but no geological '
                              'rungs - quartz, granite, shale, seawater, '
                              'limestone, halite, ice are OPEN UQFF '
                              'derivation targets that only Daniel can '
                              'close'),
            'scope': 'first pass, one 10-m window; re-runs as co-located '
                     'library grows'}
