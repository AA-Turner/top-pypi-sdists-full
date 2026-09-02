"""uqff_structural_ladder - the K1 kernel: PAPER_1209CC's Earth-shell frame
as the surveying tool's STRUCTURAL PRIOR.

v1.76.0. The Geophysics Unified Proof Set (PAPER_1209CC, closures S603-S610)
derives the planet's structural column from the locked integer primitives
with zero free parameters - seven of the eight EXACT. This module composes
those closures LIVE from `uqff_registry_primitives` (Rule A: the registry is
the single source of truth; nothing re-typed), and puts them to work:

  - ladder(): every rung with its primitive composition, target, and honest
    residual, recomputed on import - a drifted primitive breaks the ladder;
  - shell_of(z_ref_m): classify any elevation-referenced height into its
    shell (space / atmosphere / topography / ocean-water / crust / mantle /
    outer-core-and-below) using ONLY ladder rungs as boundaries;
  - earth_model_audit(): sweep every registered Earth Model site and value
    against the ladder - the map checked against the frame.

The ladder's rungs are heights/depths RELATIVE TO SEA LEVEL, matching the
Earth Model's common vertical frame. Mean-value rungs (ocean depth 3.7 km,
crust 35 km) are global averages, disclosed as such: local seafloor deeper
than 3.7 km is geography, not a violation - the HARD bounds are Everest
(no land higher) and Mariana (no seafloor deeper).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:                      # registry lives at repo root
    sys.path.insert(0, str(_ROOT))
from uqff_registry_primitives import (A_5, SO_5, D_BSFG, D_PHYS, D_CRIT,
                                      N_CH, F_TRZ, SSQ, K_MEX)


def ladder() -> List[Dict]:
    """The PAPER_1209CC structural rungs, composed live from primitives."""
    rows = [
        ('karman_line_km', 'S610', SO_5 * SO_5, 100.0,
         'SO_5^2'),
        ('everest_km', 'S609', K_MEX * D_PHYS + SSQ - F_TRZ * SSQ, 8.848,
         'K_MEX*D_phys + SSq - F_TRZ*SSq'),
        ('ocean_mean_depth_km', 'S606', D_PHYS - F_TRZ * D_PHYS + F_TRZ, 3.7,
         'D_phys - F_TRZ*D_phys + F_TRZ'),
        ('oceanic_moho_km', 'S607', D_BSFG + F_TRZ * SO_5, 7.0,
         'D_BSFG + F_TRZ*SO_5'),
        ('mariana_trench_km', 'S608', SO_5 + F_TRZ * SO_5, 11.0,
         'SO_5 + F_TRZ*SO_5'),
        ('continental_crust_km', 'S605', D_CRIT + N_CH, 35.0,
         'D_crit + N_CH'),
        ('core_radius_km', 'S604', A_5 * SO_5 * D_BSFG - SO_5 ** 2 - D_BSFG - N_CH,
         3485.0, 'A_5*SO_5*D_BSFG - SO_5^2 - D_BSFG - N_CH'),
        ('earth_radius_km', 'S603',
         A_5 * SO_5 ** 2 + A_5 * D_BSFG + SO_5 + F_TRZ * SO_5, 6371.0,
         'A_5*SO_5^2 + A_5*D_BSFG + SO_5 + F_TRZ*SO_5'),
    ]
    out = []
    for name, sid, derived, target, formula in rows:
        resid = abs(derived - target) / target * 100.0
        out.append({'rung': name, 'closure': sid, 'formula': formula,
                    'uqff_km': derived, 'target_km': target,
                    'residual_pct': resid,
                    'exact': resid < 1e-12})
    return out


_L = {r['rung']: r['uqff_km'] for r in ladder()}


def shell_of(z_ref_m: float) -> str:
    """Shell classification of an elevation-referenced height (m rel. sea
    level), boundaries from ladder rungs only. Mean rungs are averages;
    the crust base uses the CONTINENTAL 35 km rung as the deepest crustal
    bound the ladder offers (disclosed simplification of a laterally
    varying Moho)."""
    z_km = z_ref_m / 1000.0
    if z_km > _L['karman_line_km']:
        return 'SPACE'
    if z_km > _L['everest_km']:
        return 'ATMOSPHERE_ABOVE_TOPOGRAPHY'
    if z_km > 0.0:
        return 'TOPOGRAPHY_OR_ATMOSPHERE'
    if z_km > -_L['mariana_trench_km']:
        return 'OCEAN_WATER_OR_UPPER_CRUST'
    if z_km > -_L['continental_crust_km']:
        return 'CRUST'
    if z_km > -(_L['earth_radius_km'] - _L['core_radius_km']):
        return 'MANTLE'
    return 'CORE'


def earth_model_audit() -> Dict:
    """Sweep the registered Earth Model against the ladder: every site's
    reference elevation and every record's deepest value classified; the
    hard bounds asserted (no site above Everest, no seafloor below Mariana);
    the library's vertical reach measured against the crust."""
    from .uqff_earth_model import EarthModel
    em = EarthModel()
    site_rows, violations = [], []
    deepest = (0.0, None)
    for s in em.sites.values():
        if s.elevation_m is None:
            site_rows.append({'site': s.key, 'status': 'NO_DATUM'})
            continue
        e_km = s.elevation_m / 1000.0
        if e_km > _L['everest_km']:
            violations.append((s.key, 'site elevation above Everest rung'))
        if e_km < -_L['mariana_trench_km']:
            violations.append((s.key, 'seafloor below Mariana rung'))
        zmin = min((min(r.z_ref_m) for r in s.records if r.z_ref_m), default=None)
        if zmin is not None and zmin < deepest[0]:
            deepest = (zmin, s.key)
        site_rows.append({'site': s.key, 'elevation_km': e_km,
                          'surface_shell': shell_of(s.elevation_m),
                          'deepest_z_km': (zmin / 1000.0 if zmin is not None else None),
                          'deepest_shell': (shell_of(zmin) if zmin is not None else None)})
    crust_base_km = _L['continental_crust_km']
    return {
        'sites_audited': len(site_rows),
        'violations': violations,
        'deepest_registered_z_km': deepest[0] / 1000.0,
        'deepest_site': deepest[1],
        'crust_base_km': crust_base_km,
        'library_reach_pct_of_crust': abs(deepest[0] / 1000.0) / crust_base_km * 100.0,
        'all_measurements_in_crust_or_above': deepest[0] / 1000.0 > -crust_base_km,
        'sites': site_rows,
    }
