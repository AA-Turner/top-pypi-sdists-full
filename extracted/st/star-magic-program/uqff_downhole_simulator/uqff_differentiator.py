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




# ---------------------------------------------------------------------------
# THE U_i COUPLING HARNESS (Daniel's DO-ALL-THREE order, 2026-09-08)
# ---------------------------------------------------------------------------
# The RANKED CANDIDATE above waits on one thing: a corpus specification of
# HOW U_i couples into borehole gravity. This harness is the socket that
# specification plugs into. It defines a small registered family of coupling
# forms; the moment Daniel's ruling selects a form and its parameters, the
# coupled channel is computed over the co-located KTB window and scored
# against the independently measured channels - same discipline as
# channel_ranking(), same honesty checks. Until then the harness reports
# AWAITING_DANIEL_SPEC, verifies itself with a null coupling (a = 0 must
# reproduce the K2 baseline bit-exactly), and states plainly the structural
# fact the degeneracy check already implies: any DEPTH-CONSTANT coupling is
# a monotone transform of the K2 channel and cannot add strata information -
# only a coupling that varies along the column can move the score.

U_I_COUPLING_FORMS = {
    'multiplicative': 'dg_coupled = dg_k2 * (1 + a * U_i)',
    'additive':       'dg_coupled = dg_k2 + a * U_i * dz  [mGal via MGAL scale]',
    'phase_modulated': 'dg_coupled = dg_k2 * (1 + a * U_i * cos(pi * t_n(z)))',
    'density_coupled': 'dg_coupled = dg_k2 * (1 + a * U_i * (rho/rho_ref - 1))',
}


def _u_i_coupled_series(rho_k, dz, spec):
    """Compute the coupled dg series for a given spec over the mass column."""
    form = spec.get('form')
    a = float(spec.get('a', 0.0))
    u_i = float(spec.get('u_i', u_i_earth()))
    base = [predict_delta_g_mgal(r, dz) for r in rho_k]
    if form == 'multiplicative' or form is None:
        return [b * (1.0 + a * u_i) for b in base]
    if form == 'additive':
        return [b + a * u_i * dz * 1e5 for b in base]
    if form == 'phase_modulated':
        tn0 = float(spec.get('t_n0', 0.0))
        dtn = float(spec.get('dt_n_per_station', 0.0))
        return [b * (1.0 + a * u_i * math.cos(math.pi * (tn0 + i * dtn)))
                for i, b in enumerate(base)]
    if form == 'density_coupled':
        rho_ref = float(spec.get('rho_ref_gcc', 2.65))
        return [b * (1.0 + a * u_i * (r / rho_ref - 1.0))
                for b, r in zip(base, rho_k)]
    raise ValueError('unknown coupling form %r (registered: %s)'
                     % (form, sorted(U_I_COUPLING_FORMS)))


def u_i_coupling_harness(spec: Dict | None = None,
                         entry: str = 'ktb_hb_complog_6020_excerpt') -> Dict:
    """Score a U_i borehole-gravity coupling the moment it is specified.

    spec = None  -> AWAITING_DANIEL_SPEC + baseline scores + null self-check.
    spec = {'form': <registered form>, 'a': <coupling constant>, ...}
                 -> the coupled channel scored against the measured channels,
                    with the information DELTA vs the pure-K2 baseline and
                    the degeneracy verdict reported honestly.
    """
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
    dz = 0.1524
    base = [predict_delta_g_mgal(r, dz) for r in rho_k]
    base_scores = {t: abs(_pearson(base, tv)) for t, tv in truth.items()}
    base_mean = statistics.mean(base_scores.values())

    # harness self-check: the null coupling must reproduce K2 bit-exactly
    null = _u_i_coupled_series(rho_k, dz, {'form': 'multiplicative', 'a': 0.0})
    null_ok = all(abs(n - b) < 1e-18 for n, b in zip(null, base))

    out = {
        'window': '%s (n=%d co-located stations)' % (entry, len(keep)),
        'registered_forms': dict(U_I_COUPLING_FORMS),
        'u_i_earth': u_i_earth(),
        'baseline_k2_scores': base_scores,
        'baseline_k2_mean_abs_r': base_mean,
        'null_coupling_self_check': null_ok,
        'structural_note': ('a depth-CONSTANT coupling is a monotone '
                            'transform of the K2 channel (degenerate, adds '
                            'no strata information); only a coupling varying '
                            'along the column can move the score'),
    }
    if spec is None:
        out['status'] = 'AWAITING_DANIEL_SPEC'
        out['open_item'] = ('the U_i -> borehole-gravity coupling form and '
                            'constant are not corpus-specified; Daniel '
                            'supplies the spec, this harness scores it '
                            '(Rule 10: Daniel provides, the harness assembles)')
        return out
    coupled = _u_i_coupled_series(rho_k, dz, spec)
    scores = {t: abs(_pearson(coupled, tv)) for t, tv in truth.items()}
    mean = statistics.mean(scores.values())
    degen = abs(_pearson(coupled, base)) > 0.999999
    out.update({
        'status': 'SCORED',
        'spec': dict(spec),
        'coupled_scores': scores,
        'coupled_mean_abs_r': mean,
        'information_delta': mean - base_mean,
        'degenerate_with_k2': degen,
        'verdict': ('DEGENERATE - the specified coupling is a monotone '
                    'transform of K2 and adds no information' if degen else
                    ('ADDS_INFORMATION' if mean > base_mean else
                     'REDUCES_INFORMATION')),
    })
    return out


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
            'blocked_on_k4': ('CLOSED 2026-09-08 by Daniel\'s K4 derivation '
                              'order: uqff_rock_inventory carries seventeen '
                              'geological landmarks (primitive-composed, '
                              'anchors cited, ranges disclosed) and the '
                              'material-ID channel flows as RANKED '
                              'candidates with overlap honesty - see '
                              'rock_candidate_stream()'),
            'scope': 'first pass, one 10-m window; re-runs as co-located '
                     'library grows'}
