# -*- coding: utf-8 -*-
"""Score a remote-sensing transition against the calendar it is validating.

One region produces two signed differences in days -- one per transition --
plus an agreement class, a within-tolerance flag and a quality flag. Those are
aggregated per crop into the summary table, and the whole population is
summarised by a circular correlation between the two sets of days.

Column naming
-------------
Every column of the result frame is lowercase ``snake_case`` and follows one
rule, written out here because the original's ``doy_GEOGLAM_midgreenup`` /
``Peak_in_2ndStage`` / ``Assessment`` mixture was the reason nobody could
read the outputs without the source open:

* ``calendar_<event>_doy``   a day the GEOGLAM workbook asserts
* ``satellite_<event>_doy``  a day the rule-based port derived from EO
* ``<transition>_<stat>``    a per-transition comparison statistic
  (``midgreenup_diff_days``, ``midgreenup_agreement_class``, ...)
* bare ``<stat>``            the two transitions combined
  (``within_tolerance``, ``agreement_class``, ``combined_abs_diff_days``)
* a ``calendar_`` / ``satellite_`` qualifier on anything else that could be
  read either way (``calendar_stage2_length_days`` is the workbook's stage
  length; ``satellite_stage2_gdd`` is the GDD between the two satellite days)

Differences are **calendar minus satellite**, in days, positive when the
calendar is later. :data:`LEGACY_FRAME_COLUMNS` maps the original's names onto
these, and :func:`modernise_columns` renames a frame written by an earlier
version.

Two difference columns, deliberately
------------------------------------
``<transition>_diff_legacy_days`` reproduces ``util_cal.diff_GEOGLAM_RS`` so
published thresholds and figures stay comparable. Its wrap branch returns
``365 - max + min``, which is **always non-negative**, so roughly half the
population has its sign discarded and the column cannot be averaged or mapped
as a bias. ``<transition>_diff_days`` is a proper circular difference in
``(-182, 182]`` and is what every signed statistic, map and model target uses.
The two agree in absolute value.
"""
from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, fields
from typing import Iterable, Optional, Sequence

import numpy as np
import pandas as pd

from geocif.cropcal import circular

logger = logging.getLogger(__name__)

#: Value of a ``*within_tolerance*`` column when the transition is within
#: ``tolerance_days``. Must stay 1: the summary counts passes with ``.eq(1)``.
ALGO_WORKS = 1

#: Default tolerance, in days, for calling a transition a match.
MAX_DELTA = 45

#: Upper edges of the agreement classes, in days. Right-closed, so |diff| = 15
#: is class 1. The original also computed a second, left-closed set of columns
#: via ``pd.cut(..., right=False)`` that disagreed at every boundary; only this
#: one survives here.
AGREEMENT_EDGES = (15, 30, 45)
AGREEMENT_LABELS = {1: "Excellent", 2: "Good", 3: "Fair", 4: "Poor"}

TRANSITIONS = ("midgreenup", "midgreendown")


def classify_agreement(diff_days: float, edges: Sequence[int] = AGREEMENT_EDGES) -> float:
    """1 (excellent) .. 4 (poor) from an absolute difference in days."""
    if not np.isfinite(diff_days):
        return float("nan")
    magnitude = abs(diff_days)
    for index, edge in enumerate(edges, start=1):
        if magnitude <= edge:
            return float(index)
    return float(len(edges) + 1)


@dataclass
class RegionScore:
    """One row of the result frame -- the single source of its column names.

    Every row the pipeline emits, scored or skipped, is built through this
    class and written with ``asdict``, so the frame's header IS this field
    list. A skipped row carries its ``skip_reason`` and NaN everywhere else.
    """

    # identity and geography
    key: str
    country: str
    region: str
    crop: str
    season: int
    cm_group: str = ""
    grouping: str = ""
    climate_zone: str = ""
    hemisphere: str = ""
    lat: float = float("nan")
    lon: float = float("nan")

    # what the calendar asserts
    calendar_planting_doy: float = float("nan")
    calendar_midgreenup_doy: float = float("nan")
    calendar_midgreendown_doy: float = float("nan")
    calendar_harvest_doy: float = float("nan")
    calendar_stage1_length_days: float = float("nan")
    calendar_stage2_length_days: float = float("nan")
    calendar_stage3_length_days: float = float("nan")
    calendar_wraps_year: Optional[bool] = None
    calendar_wall_to_wall: Optional[bool] = None

    # what the satellite record says (rule-based port)
    satellite_midgreenup_doy: float = float("nan")
    satellite_midgreendown_doy: float = float("nan")
    #: Peak of the FITTED (unmasked) curve, not of the raw median.
    satellite_peak_doy: float = float("nan")

    # the comparison
    midgreenup_diff_days: float = float("nan")
    midgreendown_diff_days: float = float("nan")
    midgreenup_diff_legacy_days: float = float("nan")
    midgreendown_diff_legacy_days: float = float("nan")
    combined_abs_diff_days: float = float("nan")
    midgreenup_within_tolerance: float = float("nan")
    midgreendown_within_tolerance: float = float("nan")
    within_tolerance: float = float("nan")
    midgreenup_agreement_class: float = float("nan")
    midgreendown_agreement_class: float = float("nan")
    agreement_class: float = float("nan")

    # curve diagnostics
    peak_in_calendar_stage2: Optional[bool] = None
    n_peaks: int = 0
    depeaked: Optional[bool] = None
    ndvi_at_satellite_midgreenup: float = float("nan")
    ndvi_at_satellite_peak: float = float("nan")
    ndvi_at_satellite_midgreendown: float = float("nan")
    satellite_stage2_gdd: float = float("nan")

    # provenance
    n_years: int = 0
    crop_params_trusted: bool = True
    skip_reason: str = ""
    notes: str = ""


#: Column order of the result frame.
COLUMNS: tuple[str, ...] = tuple(f.name for f in fields(RegionScore))


def make_row(**values) -> dict:
    """A complete result row (every column present) from partial values."""
    return asdict(RegionScore(**values))


# --------------------------------------------------------------------------
# Legacy names
# --------------------------------------------------------------------------
#: The original's result-frame names -> current names. Exactly the columns
#: that changed; identity columns kept their names.
LEGACY_FRAME_COLUMNS = {
    "doy_GEOGLAM_plant": "calendar_planting_doy",
    "doy_GEOGLAM_midgreenup": "calendar_midgreenup_doy",
    "doy_GEOGLAM_midgreendown": "calendar_midgreendown_doy",
    "doy_GEOGLAM_harvest": "calendar_harvest_doy",
    "doy_RS_midgreenup": "satellite_midgreenup_doy",
    "doy_RS_midgreendown": "satellite_midgreendown_doy",
    "doy_Peak": "satellite_peak_doy",
    "delta_midgreenup_signed": "midgreenup_diff_days",
    "delta_midgreendown_signed": "midgreendown_diff_days",
    "delta_midgreenup": "midgreenup_diff_legacy_days",
    "delta_midgreendown": "midgreendown_diff_legacy_days",
    "combined_delta": "combined_abs_diff_days",
    "Peak_in_2ndStage": "peak_in_calendar_stage2",
    "num_peaks": "n_peaks",
    "len_growth_stage1": "calendar_stage1_length_days",
    "len_growth_stage2": "calendar_stage2_length_days",
    "len_growth_stage3": "calendar_stage3_length_days",
    "ndvi_midgreenup": "ndvi_at_satellite_midgreenup",
    "ndvi_peak": "ndvi_at_satellite_peak",
    "ndvi_midgreendown": "ndvi_at_satellite_midgreendown",
    "gdd_in_2ndStage": "satellite_stage2_gdd",
    "Assessment": "within_tolerance",
    "Assessment_midgreenup": "midgreenup_within_tolerance",
    "Assessment_midgreendown": "midgreendown_within_tolerance",
    "Agreement_midgreenup": "midgreenup_agreement_class",
    "Agreement_midgreendown": "midgreendown_agreement_class",
    "Agreement": "agreement_class",
    "params_trusted": "crop_params_trusted",
}

#: The original's summary-table names -> current names.
LEGACY_SUMMARY_COLUMNS = {
    "median_abs_delta_midgreenup": "median_abs_diff_days_midgreenup",
    "median_abs_delta_midgreendown": "median_abs_diff_days_midgreendown",
    "pct_works": "pct_within_tolerance",
    "pct_works_midgreenup": "pct_within_tolerance_midgreenup",
    "pct_works_midgreendown": "pct_within_tolerance_midgreendown",
    "pct_works_subset": "pct_within_tolerance_subset",
    "pct_works_subset_midgreenup": "pct_within_tolerance_subset_midgreenup",
    "pct_works_subset_midgreendown": "pct_within_tolerance_subset_midgreendown",
    "n_peak_in_stage2": "n_peak_in_calendar_stage2",
    "max_delta": "tolerance_days",
}

#: The original's design-matrix baseline names -> current names.
LEGACY_DESIGN_COLUMNS = {
    "rule_midgreenup": "satellite_midgreenup_doy",
    "rule_midgreendown": "satellite_midgreendown_doy",
}

LEGACY_COLUMNS = {**LEGACY_FRAME_COLUMNS, **LEGACY_SUMMARY_COLUMNS, **LEGACY_DESIGN_COLUMNS}


def modernise_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Rename a frame written by an earlier version onto the current names.

    Idempotent, and a no-op on a current frame. Warns if a legacy name survives
    (which can only happen when both spellings are present).
    """
    out = frame.rename(columns={k: v for k, v in LEGACY_COLUMNS.items() if k in frame.columns})
    stale = [c for c in out.columns if c in LEGACY_COLUMNS]
    if stale:
        logger.warning(f"legacy column(s) still present after modernising: {stale}")
    return out


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------
def _flag(ok: bool, diff_days: float) -> float:
    """1 within tolerance, 0 outside, NaN when there is no difference to test."""
    if not np.isfinite(diff_days):
        return float("nan")
    return float(ALGO_WORKS) if ok else 0.0


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
        geoglam: ``{plant, midgreenup, midgreendown, harvest, len_stage1..3}``
            in days.
        rs_midgreenup, rs_midgreendown: the remote-sensing transitions.
        fitted: the **unmasked** fitted curve, used for the peak position.
        masked: the season-masked curve, used to read NDVI at each transition.
        gdd: daily growing degree days.
        max_delta: tolerance in days for the within-tolerance flags.

    Returns:
        The scoring fields, ready for :func:`make_row`.

    The NDVI values are read from the **masked** curve. The original read them
    from the unmasked one -- not by choice, but because the masked array was a
    local inside ``validate_by_crop_country_region`` and never returned -- which
    also meant its diagnostic figure's "de-peaked" panel showed the original
    curve.
    """
    cal_up = geoglam["midgreenup"]
    cal_down = geoglam["midgreendown"]

    legacy_up = circular.legacy_difference(cal_up, rs_midgreenup)
    legacy_down = circular.legacy_difference(cal_down, rs_midgreendown)
    diff_up = circular.signed_difference(cal_up, rs_midgreenup)
    diff_down = circular.signed_difference(cal_down, rs_midgreendown)

    peak = int(np.nanargmax(fitted)) if np.isfinite(fitted).any() else -1
    peak_in_season = (
        bool(circular.check_between(peak, cal_up, cal_down)) if peak >= 0 else None
    )

    ok_up = np.isfinite(diff_up) and abs(diff_up) <= max_delta
    ok_down = np.isfinite(diff_down) and abs(diff_down) <= max_delta
    flag_up, flag_down = _flag(ok_up, diff_up), _flag(ok_down, diff_down)
    if np.isnan(flag_up) or np.isnan(flag_down):
        flag_both = float("nan")
    else:
        flag_both = float(ALGO_WORKS) if (ok_up and ok_down) else 0.0

    agree_up = classify_agreement(diff_up)
    agree_down = classify_agreement(diff_down)

    def _at(day: float) -> float:
        if not np.isfinite(day):
            return float("nan")
        index = int(day) % masked.size
        return float(masked[index])

    return {
        "calendar_midgreenup_doy": cal_up,
        "calendar_midgreendown_doy": cal_down,
        "calendar_planting_doy": geoglam["plant"],
        "calendar_harvest_doy": geoglam["harvest"],
        "calendar_stage1_length_days": geoglam["len_stage1"],
        "calendar_stage2_length_days": geoglam["len_stage2"],
        "calendar_stage3_length_days": geoglam["len_stage3"],
        "satellite_midgreenup_doy": rs_midgreenup,
        "satellite_midgreendown_doy": rs_midgreendown,
        "satellite_peak_doy": float(peak),
        "midgreenup_diff_days": diff_up,
        "midgreendown_diff_days": diff_down,
        "midgreenup_diff_legacy_days": legacy_up,
        "midgreendown_diff_legacy_days": legacy_down,
        "combined_abs_diff_days": abs(diff_up) + abs(diff_down),
        "midgreenup_within_tolerance": flag_up,
        "midgreendown_within_tolerance": flag_down,
        "within_tolerance": flag_both,
        "midgreenup_agreement_class": agree_up,
        "midgreendown_agreement_class": agree_down,
        "agreement_class": float(np.nanmax([agree_up, agree_down]))
        if np.isfinite([agree_up, agree_down]).any()
        else float("nan"),
        "peak_in_calendar_stage2": peak_in_season,
        "ndvi_at_satellite_midgreenup": _at(rs_midgreenup),
        "ndvi_at_satellite_peak": _at(peak),
        "ndvi_at_satellite_midgreendown": _at(rs_midgreendown),
        "satellite_stage2_gdd": circular.sum_between(gdd, rs_midgreenup, rs_midgreendown),
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

    Returns one row per group plus an ``All`` row, with median absolute
    difference per transition, the share of regions within tolerance (overall
    and per transition), the same three over the ``peak_in_calendar_stage2``
    subset, and the circular r-squared between calendar and satellite days.

    The shares use ``len()`` on the passing subset rather than the original's
    ``.sum()`` over an indicator column, which happened to agree only because
    ``ALGO_WORKS == 1``.
    """
    rows = []

    def _block(label: str, sub: pd.DataFrame) -> dict:
        scored = sub[sub["satellite_midgreenup_doy"].notna()]
        subset = scored[scored["peak_in_calendar_stage2"] == True]  # noqa: E712

        def _share(part: pd.DataFrame, column: str) -> float:
            if len(part) == 0:
                return float("nan")
            return 100.0 * float(part[column].eq(ALGO_WORKS).sum()) / len(part)

        r2_up, _ = circular_r2(scored["satellite_midgreenup_doy"], scored["calendar_midgreenup_doy"])
        r2_down, _ = circular_r2(
            scored["satellite_midgreendown_doy"], scored["calendar_midgreendown_doy"]
        )
        return {
            by: label,
            "n": len(scored),
            "n_peak_in_calendar_stage2": len(subset),
            "median_abs_diff_days_midgreenup": scored["midgreenup_diff_days"].abs().median(),
            "median_abs_diff_days_midgreendown": scored["midgreendown_diff_days"].abs().median(),
            "pct_within_tolerance": _share(scored, "within_tolerance"),
            "pct_within_tolerance_midgreenup": _share(scored, "midgreenup_within_tolerance"),
            "pct_within_tolerance_midgreendown": _share(scored, "midgreendown_within_tolerance"),
            "pct_within_tolerance_subset": _share(subset, "within_tolerance"),
            "pct_within_tolerance_subset_midgreenup": _share(subset, "midgreenup_within_tolerance"),
            "pct_within_tolerance_subset_midgreendown": _share(subset, "midgreendown_within_tolerance"),
            "circular_r2_midgreenup": r2_up,
            "circular_r2_midgreendown": r2_down,
            # Below ~0.3 the circular mean is poorly defined and the r-squared
            # above it should not be quoted. See score.resultant_length.
            "concentration_midgreenup": resultant_length(scored["calendar_midgreenup_doy"]),
            "concentration_midgreendown": resultant_length(scored["calendar_midgreendown_doy"]),
            "tolerance_days": max_delta,
        }

    rows.append(_block("All", frame))
    for label, sub in frame.groupby(by, dropna=False):
        rows.append(_block(str(label), sub))
    return pd.DataFrame(rows)
