# -*- coding: utf-8 -*-
"""Score a remote-sensing transition against the calendar it is validating.

One region produces two signed differences in days -- one per transition --
plus an agreement class, a pass/fail assessment and a quality flag. Those are
aggregated per crop into the summary table, and the whole population is
summarised by a circular correlation between the two sets of days.

Two delta columns, deliberately
-------------------------------
``delta_*`` reproduces ``util_cal.diff_GEOGLAM_RS`` so published thresholds and
figures stay comparable. Its wrap branch returns ``365 - max + min``, which is
**always non-negative**, so roughly half the population has its sign discarded
and the column cannot be averaged or mapped as a bias. ``delta_*_signed`` is a
proper circular difference in ``(-182, 182]`` and is what every signed
statistic, map and model target uses.
"""
from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from typing import Iterable, Optional, Sequence

import numpy as np
import pandas as pd

from geocif.cropcal import circular

logger = logging.getLogger(__name__)

#: ``Assessment`` value meaning both transitions landed within ``max_delta``.
#: Must stay 1: the original's summary computes "% works" with ``.sum()``.
ALGO_WORKS = 1

#: Default tolerance, in days, for calling a transition a match.
MAX_DELTA = 45

#: Upper edges of the agreement classes, in days. Right-closed, so |delta| = 15
#: is class 1. The original also computed a second, left-closed set of columns
#: via ``pd.cut(..., right=False)`` that disagreed at every boundary; only this
#: one survives here.
AGREEMENT_EDGES = (15, 30, 45)
AGREEMENT_LABELS = {1: "Excellent", 2: "Good", 3: "Fair", 4: "Poor"}


def agreement_class(delta: float, edges: Sequence[int] = AGREEMENT_EDGES) -> float:
    """1 (excellent) .. 4 (poor) from an absolute difference in days."""
    if not np.isfinite(delta):
        return float("nan")
    magnitude = abs(delta)
    for index, edge in enumerate(edges, start=1):
        if magnitude <= edge:
            return float(index)
    return float(len(edges) + 1)


@dataclass
class RegionScore:
    """One row of the result frame."""

    country: str
    region: str
    key: str
    crop: str
    season: int
    cm_group: str = ""
    climate_zone: str = ""
    hemisphere: str = ""

    doy_GEOGLAM_midgreenup: float = float("nan")
    doy_GEOGLAM_midgreendown: float = float("nan")
    doy_GEOGLAM_plant: float = float("nan")
    doy_GEOGLAM_harvest: float = float("nan")
    doy_RS_midgreenup: float = float("nan")
    doy_RS_midgreendown: float = float("nan")

    delta_midgreenup: float = float("nan")
    delta_midgreendown: float = float("nan")
    delta_midgreenup_signed: float = float("nan")
    delta_midgreendown_signed: float = float("nan")
    combined_delta: float = float("nan")

    doy_Peak: float = float("nan")
    num_peaks: int = 0
    Peak_in_2ndStage: Optional[bool] = None
    depeaked: Optional[bool] = None

    len_growth_stage1: float = float("nan")
    len_growth_stage2: float = float("nan")
    len_growth_stage3: float = float("nan")

    ndvi_midgreenup: float = float("nan")
    ndvi_peak: float = float("nan")
    ndvi_midgreendown: float = float("nan")
    gdd_in_2ndStage: float = float("nan")

    Assessment: float = float("nan")
    Assessment_midgreenup: float = float("nan")
    Assessment_midgreendown: float = float("nan")
    Agreement_midgreenup: float = float("nan")
    Agreement_midgreendown: float = float("nan")
    Agreement: float = float("nan")

    n_years: int = 0
    params_trusted: bool = True
    skip_reason: str = ""
    notes: str = ""


def score_region(
    *,
    geoglam: dict,
    rs_midgreenup: float,
    rs_midgreendown: float,
    fitted: np.ndarray,
    masked: np.ndarray,
    gdd: np.ndarray,
    max_delta: int = MAX_DELTA,
) -> dict:
    """Compare one region's calendar and remote-sensing transitions.

    Args:
        geoglam: ``{plant, midgreenup, midgreendown, harvest}`` in days.
        rs_midgreenup, rs_midgreendown: the remote-sensing transitions.
        fitted: the **unmasked** fitted curve, used for the peak position.
        masked: the season-masked curve, used to read NDVI at each transition.
        gdd: daily growing degree days.
        max_delta: tolerance in days for ``Assessment``.

    Returns:
        The scoring fields, ready to merge into a :class:`RegionScore`.

    The NDVI values are read from the **masked** curve. The original read them
    from the unmasked one -- not by choice, but because the masked array was a
    local inside ``validate_by_crop_country_region`` and never returned -- which
    also meant its diagnostic figure's "de-peaked" panel showed the original
    curve.
    """
    cal_up = geoglam["midgreenup"]
    cal_down = geoglam["midgreendown"]

    delta_up = circular.legacy_difference(cal_up, rs_midgreenup)
    delta_down = circular.legacy_difference(cal_down, rs_midgreendown)
    signed_up = circular.signed_difference(cal_up, rs_midgreenup)
    signed_down = circular.signed_difference(cal_down, rs_midgreendown)

    peak = int(np.nanargmax(fitted)) if np.isfinite(fitted).any() else -1
    peak_in_season = (
        bool(circular.check_between(peak, cal_up, cal_down)) if peak >= 0 else None
    )

    ok_up = np.isfinite(delta_up) and abs(delta_up) <= max_delta
    ok_down = np.isfinite(delta_down) and abs(delta_down) <= max_delta

    agree_up = agreement_class(delta_up)
    agree_down = agreement_class(delta_down)

    def _at(day: float) -> float:
        if not np.isfinite(day):
            return float("nan")
        index = int(day) % masked.size
        return float(masked[index])

    return {
        "doy_GEOGLAM_midgreenup": cal_up,
        "doy_GEOGLAM_midgreendown": cal_down,
        "doy_GEOGLAM_plant": geoglam["plant"],
        "doy_GEOGLAM_harvest": geoglam["harvest"],
        "doy_RS_midgreenup": rs_midgreenup,
        "doy_RS_midgreendown": rs_midgreendown,
        "delta_midgreenup": delta_up,
        "delta_midgreendown": delta_down,
        "delta_midgreenup_signed": signed_up,
        "delta_midgreendown_signed": signed_down,
        "combined_delta": abs(delta_up) + abs(delta_down),
        "doy_Peak": float(peak),
        "Peak_in_2ndStage": peak_in_season,
        "len_growth_stage1": geoglam["len_stage1"],
        "len_growth_stage2": geoglam["len_stage2"],
        "len_growth_stage3": geoglam["len_stage3"],
        "ndvi_midgreenup": _at(rs_midgreenup),
        "ndvi_peak": _at(peak),
        "ndvi_midgreendown": _at(rs_midgreendown),
        "gdd_in_2ndStage": circular.sum_between(gdd, rs_midgreenup, rs_midgreendown),
        "Assessment": float(ALGO_WORKS) if (ok_up and ok_down) else float("nan"),
        "Assessment_midgreenup": float(ALGO_WORKS) if ok_up else float("nan"),
        "Assessment_midgreendown": float(ALGO_WORKS) if ok_down else float("nan"),
        "Agreement_midgreenup": agree_up,
        "Agreement_midgreendown": agree_down,
        "Agreement": float(np.nanmax([agree_up, agree_down]))
        if np.isfinite([agree_up, agree_down]).any()
        else float("nan"),
    }


# --------------------------------------------------------------------------
# Circular correlation
# --------------------------------------------------------------------------
def _to_radians(days: np.ndarray, period: float = circular.DAYS_IN_YEAR) -> np.ndarray:
    return np.asarray(days, dtype=float) * 2.0 * np.pi / period


def circ_corrcc(alpha: np.ndarray, beta: np.ndarray) -> tuple[float, float]:
    """Jammalamadaka-Sarma circular-circular correlation, with a normal-approx p.

    Equivalent to ``pingouin.circ_corrcc`` on
    ``convert_angles(..., low=0, high=365, positive=True)`` inputs, implemented
    here so the package does not take a dependency for fifteen lines of
    trigonometry. Non-finite pairs are dropped.
    """
    a, b = np.asarray(alpha, dtype=float), np.asarray(beta, dtype=float)
    keep = np.isfinite(a) & np.isfinite(b)
    a, b = a[keep], b[keep]
    if a.size < 3:
        return float("nan"), float("nan")

    a_mean = np.arctan2(np.sin(a).sum(), np.cos(a).sum())
    b_mean = np.arctan2(np.sin(b).sum(), np.cos(b).sum())
    sin_a, sin_b = np.sin(a - a_mean), np.sin(b - b_mean)

    denominator = np.sqrt((sin_a**2).sum() * (sin_b**2).sum())
    if denominator == 0:
        return float("nan"), float("nan")
    r = float((sin_a * sin_b).sum() / denominator)

    # Normal approximation (Jammalamadaka & SenGupta, eq. 8.2.2).
    n = a.size
    l20, l02 = (sin_a**2).mean(), (sin_b**2).mean()
    l22 = ((sin_a**2) * (sin_b**2)).mean()
    if l22 <= 0:
        return r, float("nan")
    z = np.sqrt((n * l20 * l02) / l22) * r
    from math import erfc, sqrt

    p = erfc(abs(z) / sqrt(2))
    return r, float(p)


def resultant_length(days: Iterable[float]) -> float:
    """Mean resultant length of a set of days, in ``[0, 1]``.

    A concentration measure. It is the sanity check on :func:`circular_r2`:
    that statistic is built around the circular mean, which is **undefined**
    when the days are spread evenly around the year -- the resultant vector
    collapses to zero and the mean angle becomes numerical noise. A group whose
    transitions occur in every month will report an r-squared that means
    nothing, so the value is carried alongside it in the summary table.
    """
    angles = _to_radians(np.asarray(list(days), dtype=float))
    angles = angles[np.isfinite(angles)]
    if angles.size == 0:
        return float("nan")
    return float(np.hypot(np.sin(angles).sum(), np.cos(angles).sum()) / angles.size)


def circular_r2(days_a: Iterable[float], days_b: Iterable[float]) -> tuple[float, float]:
    """``(r_squared, p_value)`` between two sets of days of year.

    Read it together with :func:`resultant_length`; see that docstring for when
    the statistic is not interpretable.
    """
    r, p = circ_corrcc(_to_radians(np.asarray(list(days_a))), _to_radians(np.asarray(list(days_b))))
    return (r * r if np.isfinite(r) else float("nan")), p


# --------------------------------------------------------------------------
# Summary
# --------------------------------------------------------------------------
def summarise(
    frame: pd.DataFrame, *, max_delta: int = MAX_DELTA, by: str = "crop"
) -> pd.DataFrame:
    """Per-group and overall summary of a scored frame.

    Returns one row per group plus an ``All`` row, with median absolute delta
    per transition, the share of regions the algorithm works for (overall and
    per transition), the same three over the ``Peak_in_2ndStage`` subset, and
    the circular r-squared between calendar and remote-sensing days.

    The shares use ``len()`` on the passing subset rather than the original's
    ``.sum()`` over an indicator column, which happened to agree only because
    ``ALGO_WORKS == 1``.
    """
    rows = []

    def _block(label: str, sub: pd.DataFrame) -> dict:
        scored = sub[sub["doy_RS_midgreenup"].notna()]
        subset = scored[scored["Peak_in_2ndStage"] == True]  # noqa: E712

        def _share(part: pd.DataFrame, column: str) -> float:
            if len(part) == 0:
                return float("nan")
            return 100.0 * float(part[column].eq(ALGO_WORKS).sum()) / len(part)

        r2_up, _ = circular_r2(scored["doy_RS_midgreenup"], scored["doy_GEOGLAM_midgreenup"])
        r2_down, _ = circular_r2(
            scored["doy_RS_midgreendown"], scored["doy_GEOGLAM_midgreendown"]
        )
        return {
            by if label != "All" else by: label,
            "n": len(scored),
            "n_peak_in_stage2": len(subset),
            "median_abs_delta_midgreenup": scored["delta_midgreenup"].abs().median(),
            "median_abs_delta_midgreendown": scored["delta_midgreendown"].abs().median(),
            "pct_works": _share(scored, "Assessment"),
            "pct_works_midgreenup": _share(scored, "Assessment_midgreenup"),
            "pct_works_midgreendown": _share(scored, "Assessment_midgreendown"),
            "pct_works_subset": _share(subset, "Assessment"),
            "pct_works_subset_midgreenup": _share(subset, "Assessment_midgreenup"),
            "pct_works_subset_midgreendown": _share(subset, "Assessment_midgreendown"),
            "circular_r2_midgreenup": r2_up,
            "circular_r2_midgreendown": r2_down,
            # Below ~0.3 the circular mean is poorly defined and the r-squared
            # above it should not be quoted. See score.resultant_length.
            "concentration_midgreenup": resultant_length(scored["doy_GEOGLAM_midgreenup"]),
            "concentration_midgreendown": resultant_length(scored["doy_GEOGLAM_midgreendown"]),
            "max_delta": max_delta,
        }

    rows.append(_block("All", frame))
    for label, sub in frame.groupby(by, dropna=False):
        rows.append(_block(str(label), sub))
    return pd.DataFrame(rows)
