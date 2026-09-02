"""uqff_forward_model - Part 2 of the subsurface surveying tool: THE SENSING
KERNEL, K2 (Daniel's ruling, 2026-08-29: the buoyancy column first).

v1.75.0. The forward model answers: given a strata column, what does the
gravity channel read? - and its inverse-lite answers: given measured borehole
gravity, what density column does the ground imply? Every constant in the
chain is UQFF-COMPOSED, with its paper and honest residual named:

    g_U  = N_CH + Phi_5/6 - F_TRZ^2 * K_MEX = 9.8125 m/s^2   PAPER_1598 (0.025%)
    G_U  = 6.669e-11 m^3/kg/s^2 (parameter-free derivation)  PAPER_593  (0.08%)
    R_U  = 6371 km = A5*SO5^2 + A5*D_BSFG + SO5 + F*SO5      PAPER_1209CC S603 (EXACT)
    free-air gradient F_U = 2*g_U/R_U = 0.30804 mGal/m       (composed from the above)

RULE 4 STANDING (PAPER_2148 SM-validity boundary, Daniel's canonized ruling):
the interstation borehole-gravity envelope dg = (F_U - 4*pi*G_U*rho)*dz is the
classical limit that PAPER_2148 explicitly permits "when known massive
astronomical objects are the anchor... G's classical limit (U_g1 emergent)
applies faithfully at classical scale" - here the anchor is the Earth itself,
and every constant entering the envelope is UQFF-derived.

HONESTY
    - The KTB validation is partly circular BY THE ARCHIVE'S NATURE: BHGM
      density is itself derived from measured gravity by the vendor's own
      inversion, so agreement measures how closely the UQFF constant chain
      {g_U, G_U, R_U} reproduces the vendor's constants - a CONSTANTS test
      (still falsifiable: a wrong g_U, G_U or R_U shows up directly), not an
      independent strata test. Stated here and in the returned report.
    - Archive null stations (RHO recorded as 0.00 g/cc) are excluded from
      filtered statistics WITH the exclusion counted and disclosed; raw
      statistics are reported alongside - nothing silently dropped.
"""

from __future__ import annotations

import math
import statistics
from typing import Dict, List, Optional

from .uqff_profile_catalog import CATALOG

# UQFF-composed constants (papers + honest residuals in the module docstring)
G_UQFF = 6.669e-11                 # PAPER_593
G_SURFACE_UQFF = 9.8125            # PAPER_1598
R_EARTH_UQFF_M = 6371.0e3          # PAPER_1209CC S603 EXACT (km -> m)
FREE_AIR_UQFF = 2.0 * G_SURFACE_UQFF / R_EARTH_UQFF_M      # s^-2
MGAL = 1.0e5                       # 1 m/s^2 = 1e5 mGal

RHO_NULL_GCC = 0.5                 # below this the archive cell is a null, not rock


def predict_delta_g_mgal(rho_gcc: float, dz_m: float) -> float:
    """Forward kernel: interstation gravity change for a slab of density
    rho [g/cc] over dz [m], UQFF constants throughout."""
    rho = rho_gcc * 1000.0
    return (FREE_AIR_UQFF - 4.0 * math.pi * G_UQFF * rho) * dz_m * MGAL


def implied_density_gcc(dg_mgal: float, dz_m: float) -> float:
    """Inverse-lite: the density the ground implies for a measured
    interstation gravity change - the sensing direction."""
    return (FREE_AIR_UQFF - dg_mgal / MGAL / dz_m) / (4.0 * math.pi * G_UQFF) / 1000.0


def forward_gravity_profile(depths_m: List[float], rho_gcc: List[float]) -> List[float]:
    """Predicted gravity profile (mGal, relative to the first station) from a
    density column, UQFF constants throughout."""
    g = [0.0]
    for i in range(1, len(depths_m)):
        mid = 0.5 * (rho_gcc[i] + rho_gcc[i - 1])
        g.append(g[-1] + predict_delta_g_mgal(mid, depths_m[i] - depths_m[i - 1]))
    return g


def ktb_gravity_test(entry: str = 'ktb_hb_bhgm_density') -> Dict:
    """The K2 validation against REAL borehole gravimetry (KTB BHGM, 197
    stations to 8,400 m): predict interstation gravity from the tool's
    density column with UQFF constants; invert measured gravity back to an
    implied density column; report raw AND null-filtered statistics with the
    circularity caveat stated in the result itself."""
    st = CATALOG[entry].stream()
    z = [float(v) for v in st.index]
    grav = [float(v) for v in st.channels['GRAV'].values]
    rho = [float(v) for v in st.channels['RHO'].values]
    raw, filt = [], []
    for i in range(1, len(z)):
        dz = z[i] - z[i - 1]
        if dz <= 0:
            continue
        rho_mid = 0.5 * (rho[i] + rho[i - 1])
        rec = {
            'depth_m': z[i], 'dz_m': dz, 'rho_gcc': rho_mid,
            'dg_pred_mgal': predict_delta_g_mgal(rho_mid, dz),
            'dg_meas_mgal': grav[i] - grav[i - 1],
        }
        rec['residual_mgal'] = rec['dg_pred_mgal'] - rec['dg_meas_mgal']
        rec['rho_implied_gcc'] = implied_density_gcc(rec['dg_meas_mgal'], dz)
        raw.append(rec)
        if rho[i] > RHO_NULL_GCC and rho[i - 1] > RHO_NULL_GCC:
            filt.append(rec)

    def _stats(rows):
        if len(rows) < 3:
            return {'n': len(rows), 'status': 'REFUSED_THIN_DATA'}
        p = [r['dg_pred_mgal'] for r in rows]
        m = [r['dg_meas_mgal'] for r in rows]
        res = [r['residual_mgal'] for r in rows]
        dr = [r['rho_implied_gcc'] - r['rho_gcc'] for r in rows]
        mp, mm = statistics.mean(p), statistics.mean(m)
        num = sum((a - mp) * (b - mm) for a, b in zip(p, m))
        den = math.sqrt(sum((a - mp) ** 2 for a in p) * sum((b - mm) ** 2 for b in m))
        return {
            'n': len(rows),
            'correlation': num / den if den else float('nan'),
            'mean_residual_mgal': statistics.mean(res),
            'stdev_residual_mgal': statistics.pstdev(res),
            'worst_residual_mgal': max(abs(r) for r in res),
            'implied_density_mean_offset_gcc': statistics.mean(dr),
            'implied_density_stdev_gcc': statistics.pstdev(dr),
        }

    return {
        'entry': entry,
        'constants': {'G_UQFF': G_UQFF, 'g_UQFF': G_SURFACE_UQFF,
                      'R_earth_UQFF_m': R_EARTH_UQFF_M,
                      'free_air_UQFF_mgal_per_m': FREE_AIR_UQFF * MGAL},
        'raw': _stats(raw),
        'null_filtered': _stats(filt),
        'null_stations_excluded': len(raw) - len(filt),
        'intervals': raw,
        'circularity_caveat': (
            'BHGM density is itself gravity-derived by the vendor inversion; '
            'this test validates the UQFF constant chain {g_U, G_U, R_U} '
            'against the vendor loop - a constants test, not an independent '
            'strata test. It remains falsifiable: an incorrect UQFF g, G or '
            'R appears directly as bias here.'),
    }
