# -*- coding: utf-8 -*-
"""Turn a region's EO climatology into a row of model features.

The machine-learning comparison asks whether a model can predict the **GEOGLAM
calendar's** four transition days -- planting, mid-greenup, mid-greendown,
harvest -- from the satellite record. For the two interior transitions the
rule-based port is a zero-parameter baseline, so its delta and a model's
prediction error are the same quantity; for planting and harvest there is no
satellite rule, and the null reference is the out-of-fold climatology baseline
in :mod:`geocif.cropcal.models`.

Features are descriptors of the *shape* of the climatological year, and
**nothing downstream of the calendar** is among them. That rule is enforced,
not assumed: :func:`feature_columns` is an allow-list built from the feature
functions below, so the rule-based satellite days -- which are computed inside
a window the calendar defines and therefore carry the target -- can never enter
a model by being present in the frame.

Naming
------
Two conventions coexist in one design matrix, on purpose:

* ``doy_<descriptor>`` is a **shape feature**: the day the raw median NDVI
  peaks, the day the 30-day rainfall sum is largest, the day 25% of annual GDD
  has accumulated. It describes the year.
* ``<source>_<event>_doy`` is an **event day being compared**: the calendar's
  planting day, the satellite rule's mid-greenup. It is a target or a baseline,
  never a feature.

Encodings of a day
------------------
A day of year is circular: 1 and 365 are one day apart, and a regressor
trained on the raw number treats them as 364 apart. Every day-valued feature
therefore also carries a ``(sin, cos)`` pair, and every target is emitted three
ways: the raw day, its ``(sin, cos)`` pair (recombined with ``atan2`` after
prediction), and an **anchored offset** -- the signed circular distance from a
calendar-free landmark of the same year, the steepest rise of the NDVI median.
Planting sits a few months before that rise and harvest a few months after it
for every crop in every hemisphere, so the offset is unimodal and far from the
+/-182 wrap, and one regressor predicts it. Which encoding wins is reported,
not assumed.
"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

import numpy as np
import pandas as pd

from geocif.cropcal import circular, series

logger = logging.getLogger(__name__)

#: Categorical columns handed to the model as-is (one-hot encoded downstream).
#: ``season`` is the crop-sheet index, not a calendar value; as an integer it
#: would be an ordinal a tree can split on as "later in the year", which does
#: not transfer across hemispheres.
CATEGORICAL_FEATURES = ("crop", "hemisphere", "climate_zone", "cm_group", "season", "precip_regime")

#: Columns that identify a row and are never features.
IDENTIFIER_COLUMNS = ("key", "country", "region")

#: Calendar flags carried for the evaluation, never features: both are
#: properties of the calendar row, i.e. of the target.
METADATA_COLUMNS = ("calendar_wraps_year", "calendar_wall_to_wall")

#: The four calendar transitions the models predict, in season order.
TARGETS = ("planting", "midgreenup", "midgreendown", "harvest")

#: Target name -> key in the calendar day dict (``calendar.to_days``). The
#: calendar module says ``plant``; the outputs say ``planting``. This is the
#: one place the two vocabularies meet.
CALENDAR_KEY = {
    "planting": "plant",
    "midgreenup": "midgreenup",
    "midgreendown": "midgreendown",
    "harvest": "harvest",
}

#: Target -> design-matrix column holding the rule-based satellite day. Only
#: the two interior transitions have one. The single source for pipeline,
#: models and the feature allow-list.
BASELINE_COLUMNS = {
    "midgreenup": "satellite_midgreenup_doy",
    "midgreendown": "satellite_midgreendown_doy",
}

#: Landmark for the anchored target encoding: the steepest rise of the
#: Fourier-FITTED NDVI curve, computed with no calendar input. The raw
#: median's steepest single-day rise (``doy_max_rise``) is a spiky, unstable
#: day and anchoring on it made the encoding worse than the null on real data
#: (smoke run 2026-09-23: MAE 63-87 d); the fitted curve is what the
#: rule-based method differentiates, for the same reason.
ANCHOR_FEATURE = "doy_fitted_max_rise"

#: Fractions of annual accumulated GDD / rainfall whose crossing day is a feature.
ACCUMULATION_QUANTILES = (0.10, 0.25, 0.50, 0.75, 0.90)
AGDD_QUANTILES = (0.25, 0.50, 0.75)
PRECIP_QUANTILES = (0.10, 0.50, 0.90)

#: Smoothing and differencing windows, in days, for the moisture variables.
SMOOTH_DAYS = 15
DIFF_DAYS = 30

#: Rainfall regime thresholds.
ARID_TOTAL_MM = 100.0            # below this the year has no wet season to time
EVERWET_TROUGH_FRACTION = 0.5    # driest 30-d sum above this share of the mean 30-d sum
WET_SEASON_MIN_HEIGHT = 0.3      # a rainfall peak counts if >= this share of the largest
WET_SEASON_MIN_SEPARATION = 90   # days between distinct wet seasons
#: ... AND it must stand this share of the largest peak above the troughs
#: either side. Height alone called every bump on a flat temperate curve a
#: season: on real data the whole US Corn Belt came out bimodal/multimodal.
#: With prominence, Corn Belt / Thailand / northern Ethiopia are unimodal and
#: Kenya / southern Ethiopia keep their two seasons (checked 2026-09-23).
WET_SEASON_MIN_PROMINENCE = 0.35
WET_SEASON_EDGE_FRACTION = 0.25  # onset/end where the 30-d sum crosses this share of the peak
PRECIP_REGIMES = ("arid", "unimodal", "bimodal", "multimodal", "everwet", "unknown")

#: Per-year rain-onset detector (the season monitor's rule, one-dimensional).
ONSET_MM = 20.0
ONSET_WINDOW_DAYS = 3
ONSET_DRY_SPELL_DAYS = 10
ONSET_DRY_DAY_MM = 1.0
ONSET_VALIDATION_DAYS = 30
MIN_YEAR_COVERAGE = 0.8          # share of finite days for a year to yield an onset


# --------------------------------------------------------------------------
# Day-of-year encodings
# --------------------------------------------------------------------------
def day_to_circle(day: float, period: float = circular.DAYS_IN_YEAR) -> tuple[float, float]:
    """Day of year -> ``(sin, cos)`` on the unit circle."""
    if not np.isfinite(day):
        return float("nan"), float("nan")
    angle = 2.0 * np.pi * float(day) / period
    return float(np.sin(angle)), float(np.cos(angle))


def circle_to_day(sin_value: float, cos_value: float, period: float = circular.DAYS_IN_YEAR) -> float:
    """``(sin, cos)`` -> day of year in ``[0, period)``."""
    if not (np.isfinite(sin_value) and np.isfinite(cos_value)):
        return float("nan")
    angle = np.arctan2(sin_value, cos_value)
    return float((angle % (2.0 * np.pi)) * period / (2.0 * np.pi))


def anchored_to_day(anchor: float, offset: float, period: float = circular.DAYS_IN_YEAR) -> float:
    """Landmark day + signed offset -> day of year in ``[0, period)``."""
    if not (np.isfinite(anchor) and np.isfinite(offset)):
        return float("nan")
    return float((anchor + offset) % period)


def circular_median_day(days: Sequence[float], period: float = circular.DAYS_IN_YEAR) -> float:
    """The day minimising the summed circular distance to every other day.

    The circular MEAN direction is undefined for a dispersed or bimodal set and
    is not the estimator that minimises circular absolute error; the medoid is
    both well defined and what a MAE metric rewards. O(n^2), n is small.
    """
    arr = np.asarray(list(days), dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan")
    gaps = np.abs(arr[:, None] - arr[None, :]) % period
    gaps = np.minimum(gaps, period - gaps)
    return float(arr[int(np.argmin(gaps.sum(axis=1)))])


def circular_std_days(days: Sequence[float], period: float = circular.DAYS_IN_YEAR) -> float:
    """Circular standard deviation of a set of days, in days."""
    arr = np.asarray(list(days), dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size < 2:
        return float("nan")
    angles = 2.0 * np.pi * arr / period
    resultant = float(np.hypot(np.sin(angles).mean(), np.cos(angles).mean()))
    if resultant <= 0.0:
        return float("nan")
    if resultant >= 1.0:
        return 0.0
    return float(np.sqrt(-2.0 * np.log(resultant)) * period / (2.0 * np.pi))


# --------------------------------------------------------------------------
# NaN-aware circular array helpers
# --------------------------------------------------------------------------
def _safe(fn, values, default=float("nan")):
    arr = np.asarray(values, dtype=float)
    if not np.isfinite(arr).any():
        return default
    with np.errstate(all="ignore"):
        return float(fn(arr))


def _argext(arr: np.ndarray, fn) -> float:
    """``nanargmax``/``nanargmin`` as a float day, NaN when nothing is finite."""
    a = np.asarray(arr, dtype=float)
    if not np.isfinite(a).any():
        return float("nan")
    return float(fn(a))


def _circular_window(arr: np.ndarray, window: int, *, how: str, min_frac: float) -> np.ndarray:
    """Centred rolling statistic over a wrapped year, NaN-aware.

    ``how="mean"`` averages the finite values in the window; ``how="sum"``
    returns the sum scaled by ``window / n_finite`` so a window with a few
    missing rasters is not read as a drier one. A window with fewer than
    ``min_frac * window`` finite days is NaN -- a missing day is not a dry day.
    """
    a = np.asarray(arr, dtype=float)
    n = a.size
    if n == 0:
        return a.copy()
    half = window // 2
    padded = np.concatenate([a[n - half:], a, a[: window - half - 1]])
    finite = np.isfinite(padded)
    values = np.where(finite, padded, 0.0)
    kernel = np.ones(window)
    sums = np.convolve(values, kernel, "valid")
    counts = np.convolve(finite.astype(float), kernel, "valid")
    with np.errstate(all="ignore"):
        if how == "mean":
            out = sums / counts
        elif how == "sum":
            out = sums * window / counts
        else:
            raise ValueError(how)
    out = np.where(counts >= min_frac * window, out, np.nan)
    return out[:n]


def rolling_mean(arr: np.ndarray, window: int = SMOOTH_DAYS, min_frac: float = 0.6) -> np.ndarray:
    return _circular_window(arr, window, how="mean", min_frac=min_frac)


def rolling_sum(arr: np.ndarray, window: int = DIFF_DAYS, min_frac: float = 0.8) -> np.ndarray:
    return _circular_window(arr, window, how="sum", min_frac=min_frac)


def _lagged_difference(arr: np.ndarray, lag: int) -> np.ndarray:
    """``arr[i] - arr[i - lag]`` around the circle."""
    a = np.asarray(arr, dtype=float)
    return a - np.roll(a, lag)


def _coverage_scaled_total(arr: np.ndarray) -> float:
    """Annual total from a daily series with gaps, scaled to a full year."""
    a = np.asarray(arr, dtype=float)
    finite = np.isfinite(a)
    if finite.sum() < MIN_YEAR_COVERAGE * a.size:
        return float("nan")
    return float(np.nansum(a) * a.size / finite.sum())


def _with_circle(out: dict, name: str) -> None:
    """Add ``{name}_sin`` / ``{name}_cos`` next to a day-valued feature."""
    sin_value, cos_value = day_to_circle(out[name])
    out[f"{name}_sin"], out[f"{name}_cos"] = sin_value, cos_value


def _nan_days(out: dict, names: Sequence[str]) -> None:
    for name in names:
        out[name] = float("nan")
        _with_circle(out, name)


# --------------------------------------------------------------------------
# Feature groups
# --------------------------------------------------------------------------
def curve_features(
    ndvi: np.ndarray,
    peaks: Sequence[int],
    valleys: Sequence[int],
    fitted: Optional[np.ndarray] = None,
) -> dict:
    """Shape descriptors of the per-day NDVI climatology.

    ``peaks``/``valleys`` were detected on the fitted curve; when that curve is
    passed the two multi-cropping indicators read peak heights from it, else
    from the median.
    """
    arr = np.asarray(ndvi, dtype=float)
    finite = np.isfinite(arr)
    diff = np.diff(arr)

    out = {
        "ndvi_min": _safe(np.nanmin, arr),
        "ndvi_max": _safe(np.nanmax, arr),
        "ndvi_mean": _safe(np.nanmean, arr),
        "ndvi_std": _safe(np.nanstd, arr),
        "ndvi_amplitude": _safe(np.nanmax, arr) - _safe(np.nanmin, arr),
        "ndvi_integral": _safe(np.nansum, arr),
        "ndvi_days_observed": int(finite.sum()),
        "n_peaks": len(peaks),
        "n_valleys": len(valleys),
        "max_rise": _safe(np.nanmax, diff),
        "max_fall": _safe(np.nanmin, diff),
    }

    if np.isfinite(diff).any():
        rise_day = int(np.flatnonzero(diff == np.nanmax(diff))[-1])
        fall_day = int(np.nanargmin(diff))
        out["doy_max_rise"] = float(rise_day)
        out["doy_max_fall"] = float(fall_day)
        out["season_span"] = float(circular.circular_gap(fall_day, rise_day))
    else:
        out["doy_max_rise"] = out["doy_max_fall"] = out["season_span"] = float("nan")

    peak_day = int(np.nanargmax(arr)) if finite.any() else -1
    out["doy_peak"] = float(peak_day) if peak_day >= 0 else float("nan")
    out["ndvi_at_peak"] = float(arr[peak_day]) if peak_day >= 0 else float("nan")

    # The same landmarks on the smooth fitted curve. These are the stable
    # versions the anchored target encoding needs; the raw ones above are kept
    # because they are what the original rule starts from.
    fitted_arr = np.asarray(fitted, dtype=float) if fitted is not None else np.full(arr.size, np.nan)
    fitted_diff = np.diff(fitted_arr)
    if np.isfinite(fitted_diff).any():
        out["doy_fitted_max_rise"] = float(np.flatnonzero(fitted_diff == np.nanmax(fitted_diff))[-1])
        out["doy_fitted_max_fall"] = float(np.nanargmin(fitted_diff))
        out["doy_fitted_peak"] = float(np.nanargmax(fitted_arr))
    else:
        out["doy_fitted_max_rise"] = out["doy_fitted_max_fall"] = out["doy_fitted_peak"] = float("nan")

    # Multi-cropping indicators: a strong second peak well separated from the
    # first is a second cycle the season-masked rule handles and the unmasked
    # shape features otherwise cannot express.
    heights_source = np.asarray(fitted if fitted is not None else arr, dtype=float)
    peak_list = [int(p) for p in peaks if 0 <= int(p) < heights_source.size]
    if len(peak_list) >= 2:
        heights = heights_source[peak_list]
        order = np.argsort(heights)[::-1]
        first, second = peak_list[order[0]], peak_list[order[1]]
        top = heights[order[0]]
        out["ndvi_second_peak_ratio"] = float(heights[order[1]] / top) if top > 0 else float("nan")
        out["ndvi_peak_separation_days"] = float(circular.circular_gap(first, second))
    else:
        out["ndvi_second_peak_ratio"] = 0.0 if len(peak_list) == 1 else float("nan")
        out["ndvi_peak_separation_days"] = float("nan")

    for name in ("doy_peak", "doy_max_rise", "doy_max_fall",
                 "doy_fitted_peak", "doy_fitted_max_rise", "doy_fitted_max_fall"):
        _with_circle(out, name)
    return out


def gdd_features(gdd: np.ndarray, agdd: np.ndarray) -> dict:
    """Thermal accumulation descriptors of the year."""
    gdd_arr = np.asarray(gdd, dtype=float)
    agdd_arr = np.asarray(agdd, dtype=float)
    total = _safe(np.nanmax, agdd_arr)

    out = {
        "agdd_total": total,
        "gdd_max": _safe(np.nanmax, gdd_arr),
        "gdd_mean": _safe(np.nanmean, gdd_arr),
        "gdd_days_positive": int(np.nansum(gdd_arr > 0)),
    }
    for fraction in AGDD_QUANTILES:
        key = f"doy_agdd_p{int(fraction * 100)}"
        if np.isfinite(total) and total > 0:
            reached = np.flatnonzero(agdd_arr >= fraction * total)
            out[key] = float(reached[0]) if reached.size else float("nan")
        else:
            out[key] = float("nan")
        _with_circle(out, key)
    return out


def _runs(mask: np.ndarray) -> list[tuple[int, int]]:
    """``(start, length)`` of every run of True in a boolean array."""
    runs, start = [], None
    for index, flag in enumerate(mask):
        if flag and start is None:
            start = index
        elif not flag and start is not None:
            runs.append((start, index - start))
            start = None
    if start is not None:
        runs.append((start, mask.size - start))
    return runs


def thermal_features(tmean: Optional[np.ndarray], gdd: np.ndarray, min_run_days: int = 10) -> dict:
    """Thermal TIMING anchors: when the year is coldest and when growth can start.

    For temperate, continental and snowmelt systems planting follows soil thaw
    and harvest the autumn decline, not rainfall. The rule-based port encodes
    that as its "GDD resumes" rule; this hands the same information to the
    models as features. Everything is counted circularly from the coldest day so
    it means the same thing in both hemispheres.
    """
    out: dict = {}
    gdd_arr = np.asarray(gdd, dtype=float)
    n = gdd_arr.size
    if tmean is None or not np.isfinite(np.asarray(tmean, dtype=float)).any() or n == 0:
        out["tmean_min"] = out["tmean_max"] = out["gdd_season_length_days"] = float("nan")
        _nan_days(out, ("doy_tmean_min", "doy_tmean_max", "doy_gdd_onset", "doy_gdd_end"))
        return out

    smooth = rolling_mean(np.asarray(tmean, dtype=float), SMOOTH_DAYS)
    out["tmean_min"] = _safe(np.nanmin, smooth)
    out["tmean_max"] = _safe(np.nanmax, smooth)
    out["doy_tmean_min"] = _argext(smooth, np.nanargmin)
    out["doy_tmean_max"] = _argext(smooth, np.nanargmax)

    onset = end = float("nan")
    if np.isfinite(out["doy_tmean_min"]):
        start = int(out["doy_tmean_min"])
        order = (start + np.arange(n)) % n
        positive = np.where(np.isfinite(gdd_arr), gdd_arr > 0.0, False)[order]
        runs = [(s, length) for s, length in _runs(positive) if length >= min_run_days]
        length_days = float("nan")
        if runs:
            onset_pos = runs[0][0]
            last_start, last_length = runs[-1]
            end_pos = last_start + last_length - 1
            onset, end = float(order[onset_pos]), float(order[end_pos])
            # Length in WALK positions, inclusive. Taking (end - onset) mod 365
            # on 366-index day labels made a year-round season read as 0 or
            # 364 days depending on which day happened to be coldest.
            length_days = float(end_pos - onset_pos + 1)
    out["doy_gdd_onset"], out["doy_gdd_end"] = onset, end
    out["gdd_season_length_days"] = length_days
    for name in ("doy_tmean_min", "doy_tmean_max", "doy_gdd_onset", "doy_gdd_end"):
        _with_circle(out, name)
    return out


def _wet_season_peaks(rs30: np.ndarray) -> list[int]:
    """Days of the distinct rainfall peaks, largest first, from a 30-day sum."""
    from scipy.signal import find_peaks

    a = np.where(np.isfinite(rs30), rs30, 0.0)
    n = a.size
    top = float(a.max()) if n else 0.0
    if top <= 0:
        return []
    tripled = np.concatenate([a, a, a])
    idx, _ = find_peaks(
        tripled,
        height=WET_SEASON_MIN_HEIGHT * top,
        distance=WET_SEASON_MIN_SEPARATION,
        prominence=WET_SEASON_MIN_PROMINENCE * top,
    )
    middle = sorted({int(i - n) for i in idx if n <= i < 2 * n})
    return sorted(middle, key=lambda d: -a[d])


def _rain_onset_1d(year: np.ndarray, order: np.ndarray) -> float:
    """First day, in ``order``, where the season monitor's onset rule fires.

    Candidate: ``ONSET_MM`` or more in the ``ONSET_WINDOW_DAYS`` ending that
    day. Valid if no run of ``ONSET_DRY_SPELL_DAYS`` dry days (< ``ONSET_DRY_DAY_MM``)
    occurs in the following ``ONSET_VALIDATION_DAYS``. A NaN day contributes no
    rain and does not count as dry. ``order`` arranges the year circularly
    from the anchor so a season crossing 31 December is one season.
    """
    p = np.asarray(year, dtype=float)[order]
    n = p.size
    filled = np.where(np.isfinite(p), p, 0.0)
    csum = np.concatenate([[0.0], np.cumsum(filled)])
    dry = (filled < ONSET_DRY_DAY_MM) & np.isfinite(p)
    for t in range(ONSET_WINDOW_DAYS - 1, n - ONSET_VALIDATION_DAYS):
        if csum[t + 1] - csum[t + 1 - ONSET_WINDOW_DAYS] < ONSET_MM:
            continue
        ahead = dry[t + 1 : t + 1 + ONSET_VALIDATION_DAYS]
        longest = max((length for _s, length in _runs(ahead)), default=0)
        if longest < ONSET_DRY_SPELL_DAYS:
            return float(order[t])
    return float("nan")


def precip_features(precip: Optional[np.ndarray], precip_years: Optional[pd.DataFrame] = None) -> dict:
    """Rainfall regime, wet-season timing and per-year onset.

    Built for hemisphere robustness: every day is measured circularly from
    the centre of the driest 90-day window, and the regime is classified
    before any timing is attempted. Arid and ever-wet years have no wet season
    to time, so every ``doy_*`` is NaN there rather than an argmin over a flat
    line. Bimodal regimes (East Africa, Sri Lanka, much of Indonesia) get their
    two largest wet seasons separately, ordered from the anchor, so a
    second-season calendar row can be learned from ``season x wet2``.
    """
    out: dict = {"precip_regime": "unknown"}
    scalar_names = (
        "precip_total_mm", "precip_max_30d_mm", "precip_seasonality",
        "precip_wet_days_per_year", "precip_n_wet_seasons",
        "wet1_onset_std_days", "wet1_onset_n_years",
        "wet2_onset_std_days", "wet2_onset_n_years",
    )
    day_names = (
        "doy_precip_p10", "doy_precip_p50", "doy_precip_p90", "doy_precip_anchor",
        "doy_wet1_onset", "doy_wet1_peak", "doy_wet1_end", "doy_wet1_onset_median",
        "doy_wet2_onset", "doy_wet2_peak", "doy_wet2_end", "doy_wet2_onset_median",
    )
    for name in scalar_names:
        out[name] = float("nan")
    _nan_days(out, day_names)

    if precip is None:
        return out
    p = np.asarray(precip, dtype=float)
    n = p.size
    if n == 0 or not np.isfinite(p).any():
        return out

    total = _coverage_scaled_total(p)
    rs30 = rolling_sum(p, 30)
    rs90 = rolling_sum(p, 90)
    out["precip_total_mm"] = total
    out["precip_max_30d_mm"] = _safe(np.nanmax, rs30)
    if np.isfinite(total) and total > 0:
        out["precip_seasonality"] = out["precip_max_30d_mm"] / (total / 12.0)

    if precip_years is not None and precip_years.shape[1]:
        wet = []
        for column in precip_years.columns:
            year = precip_years[column].to_numpy(dtype=float)
            finite = np.isfinite(year)
            if finite.sum() >= MIN_YEAR_COVERAGE * year.size:
                wet.append(float((year[finite] > ONSET_DRY_DAY_MM).sum() * year.size / finite.sum()))
        out["precip_wet_days_per_year"] = float(np.mean(wet)) if wet else float("nan")

    if not np.isfinite(total) or total < ARID_TOTAL_MM:
        out["precip_regime"] = "arid" if np.isfinite(total) else "unknown"
        out["precip_n_wet_seasons"] = 0.0 if np.isfinite(total) else float("nan")
        return out

    anchor = _argext(rs90, np.nanargmin)
    if not np.isfinite(anchor):
        return out
    anchor = int(anchor)
    out["doy_precip_anchor"] = float(anchor)
    _with_circle(out, "doy_precip_anchor")
    order = (anchor + np.arange(n)) % n

    trough, mean30 = _safe(np.nanmin, rs30), _safe(np.nanmean, rs30)
    if np.isfinite(trough) and np.isfinite(mean30) and mean30 > 0 and trough > EVERWET_TROUGH_FRACTION * mean30:
        out["precip_regime"] = "everwet"
        out["precip_n_wet_seasons"] = float("nan")
        return out

    # Cumulative-fraction crossing days, from the dry anchor.
    cumulative = np.cumsum(np.where(np.isfinite(p[order]), p[order], 0.0))
    cumulative = cumulative / cumulative[-1] if cumulative[-1] > 0 else cumulative
    for fraction in PRECIP_QUANTILES:
        key = f"doy_precip_p{int(fraction * 100)}"
        hit = np.flatnonzero(cumulative >= fraction)
        out[key] = float(order[hit[0]]) if hit.size else float("nan")
        _with_circle(out, key)

    peaks = _wet_season_peaks(rs30)
    out["precip_n_wet_seasons"] = float(len(peaks))
    if not peaks:
        return out
    out["precip_regime"] = {1: "unimodal", 2: "bimodal"}.get(len(peaks), "multimodal")

    # The two largest wet seasons, in circular order from the anchor.
    chosen = sorted(peaks[:2], key=lambda d: (d - anchor) % n)
    rs30_ordered = rs30[order]
    position = {int(d): int(((d - anchor) % n)) for d in chosen}
    previous_edge = 0
    for k, peak in enumerate(chosen, start=1):
        pos = position[int(peak)]
        height = rs30_ordered[pos]
        edge = WET_SEASON_EDGE_FRACTION * height if np.isfinite(height) else float("nan")
        # A second season riding on the first's shoulder can put wet1's edge
        # crossing past wet2's peak; clamp so the trough search is never empty.
        segment_start = min(previous_edge, pos)
        segment = rs30_ordered[segment_start : pos + 1]
        trough_pos = segment_start + int(np.nanargmin(segment)) if np.isfinite(segment).any() else segment_start
        onset_pos = next(
            (i for i in range(trough_pos, pos + 1) if np.isfinite(rs30_ordered[i]) and rs30_ordered[i] >= edge),
            pos,
        )
        end_pos = next(
            (i for i in range(pos, n) if np.isfinite(rs30_ordered[i]) and rs30_ordered[i] < edge),
            n - 1,
        )
        out[f"doy_wet{k}_peak"] = float(peak)
        out[f"doy_wet{k}_onset"] = float(order[onset_pos])
        out[f"doy_wet{k}_end"] = float(order[end_pos])
        for name in (f"doy_wet{k}_peak", f"doy_wet{k}_onset", f"doy_wet{k}_end"):
            _with_circle(out, name)

        # Per-year onset: the season monitor's rule, run from this season's
        # trough on each year's own daily series.
        if precip_years is not None and precip_years.shape[1]:
            # Search THIS season only: from its trough to its end plus the
            # validation window a late onset needs. Running to the end of the
            # year let a failed first season borrow the second season's onset.
            season_order = order[trough_pos : min(n, end_pos + 1 + ONSET_VALIDATION_DAYS)]
            onsets = []
            for column in precip_years.columns:
                year = precip_years[column].to_numpy(dtype=float)
                if np.isfinite(year).sum() < MIN_YEAR_COVERAGE * year.size:
                    continue
                onset = _rain_onset_1d(year, season_order)
                if np.isfinite(onset):
                    onsets.append(onset)
            out[f"wet{k}_onset_n_years"] = float(len(onsets))
            out[f"doy_wet{k}_onset_median"] = circular_median_day(onsets)
            out[f"wet{k}_onset_std_days"] = circular_std_days(onsets)
            _with_circle(out, f"doy_wet{k}_onset_median")
        previous_edge = end_pos
    return out


def esi_features(esi_years: Optional[pd.DataFrame]) -> dict:
    """What an anomaly product can say about phenology: variability and coverage.

    ESI is a standardised anomaly -- its seasonal cycle is removed by
    construction -- so a per-day level of it describes which recent weeks were
    wetter or drier than the long-term baseline, not when crops are planted.
    Two things do carry seasonality: the interannual SPREAD of the anomaly,
    which peaks inside the growing season when ET is limited by water, and the
    retrieval availability, which follows cloud and sun angle.
    """
    out = {
        "esi_std_max": float("nan"),
        "esi_std_min": float("nan"),
        "esi_std_mean": float("nan"),
        "esi_frac_observed_mean": float("nan"),
        "esi_frac_observed_min": float("nan"),
    }
    _nan_days(out, ("doy_esi_std_max",))
    if esi_years is None or esi_years.shape[1] < 2:
        return out

    frac = series.per_day_fraction_observed(esi_years)
    out["esi_frac_observed_mean"] = _safe(np.nanmean, frac)
    out["esi_frac_observed_min"] = _safe(np.nanmin, rolling_mean(frac, SMOOTH_DAYS))

    filled = esi_years.interpolate(axis=0, limit_area="inside", limit=series.WEEKLY_INTERPOLATION_LIMIT)
    with np.errstate(all="ignore"):
        spread = filled.std(axis=1, skipna=True).to_numpy(dtype=float)
    spread = np.where(filled.notna().sum(axis=1).to_numpy() >= 2, spread, np.nan)
    smooth = rolling_mean(spread, SMOOTH_DAYS)
    out["esi_std_max"] = _safe(np.nanmax, smooth)
    out["esi_std_min"] = _safe(np.nanmin, smooth)
    out["esi_std_mean"] = _safe(np.nanmean, smooth)
    out["doy_esi_std_max"] = _argext(smooth, np.nanargmax)
    _with_circle(out, "doy_esi_std_max")
    return out


def soil_moisture_features(
    sm: Optional[np.ndarray],
    prefix: str,
    sm_years: Optional[pd.DataFrame] = None,
    *,
    rise: bool = False,
    fall: bool = False,
) -> dict:
    """Level and timing descriptors of a soil-moisture climatology.

    Surface moisture wets up at the start of the rains (``rise=True``: the day
    of the largest 30-day increase, plus its per-year median and spread);
    root-zone moisture draws down through the season (``fall=True``: the day
    of the largest 30-day decrease). The mirrored pair is deliberately not
    emitted -- root-zone rise trails surface rise by weeks and adds nothing.
    """
    out = {f"{prefix}_min": float("nan"), f"{prefix}_max": float("nan"), f"{prefix}_mean": float("nan")}
    day_names = [f"doy_{prefix}_min", f"doy_{prefix}_max"]
    if rise:
        day_names += [f"doy_{prefix}_max_rise", f"doy_{prefix}_rise_median"]
        out[f"{prefix}_rise_std_days"] = float("nan")
        out[f"{prefix}_rise_n_years"] = float("nan")
    if fall:
        day_names += [f"doy_{prefix}_max_fall"]
    _nan_days(out, day_names)

    if sm is None or not np.isfinite(np.asarray(sm, dtype=float)).any():
        return out
    smooth = rolling_mean(np.asarray(sm, dtype=float), SMOOTH_DAYS)
    out[f"{prefix}_min"] = _safe(np.nanmin, smooth)
    out[f"{prefix}_max"] = _safe(np.nanmax, smooth)
    out[f"{prefix}_mean"] = _safe(np.nanmean, smooth)
    out[f"doy_{prefix}_min"] = _argext(smooth, np.nanargmin)
    out[f"doy_{prefix}_max"] = _argext(smooth, np.nanargmax)
    diff = _lagged_difference(smooth, DIFF_DAYS)
    if rise:
        out[f"doy_{prefix}_max_rise"] = _argext(diff, np.nanargmax)
        if sm_years is not None and sm_years.shape[1]:
            rises = []
            for column in sm_years.columns:
                year = sm_years[column].to_numpy(dtype=float)
                if np.isfinite(year).sum() < MIN_YEAR_COVERAGE * year.size:
                    continue
                day = _argext(_lagged_difference(rolling_mean(year, SMOOTH_DAYS), DIFF_DAYS), np.nanargmax)
                if np.isfinite(day):
                    rises.append(day)
            out[f"{prefix}_rise_n_years"] = float(len(rises))
            out[f"doy_{prefix}_rise_median"] = circular_median_day(rises)
            out[f"{prefix}_rise_std_days"] = circular_std_days(rises)
    if fall:
        out[f"doy_{prefix}_max_fall"] = _argext(diff, np.nanargmin)
    for name in day_names:
        _with_circle(out, name)
    return out


# --------------------------------------------------------------------------
# Terrain, humidity and season-block features (Franch et al. 2022 set)
# --------------------------------------------------------------------------
#: Month (1..12) of each day-of-year index 0..365 on a non-leap year; the
#: 366th index is 31 December.
_MONTH_OF_DOY = np.array(
    [(pd.Timestamp(2025, 1, 1) + pd.Timedelta(days=d)).month for d in range(365)] + [12],
    dtype=int,
)

#: Meteorological seasons in NORTHERN-hemisphere months. Southern-hemisphere
#: rows use the same names shifted six months, so "winter" always means the
#: cold season. Franch et al. use calendar DJF for "winter", which is summer in
#: Argentina, so their feature means opposite things either side of the equator.
SEASON_MONTHS_N = {"winter": (12, 1, 2), "spring": (3, 4, 5), "summer": (6, 7, 8), "fall": (9, 10, 11)}


def terrain_features(elevation: Optional[float], slope: Optional[float]) -> dict:
    """Crop-weighted mean elevation (m) and 5 km-grid slope (rise/run)."""
    def _num(v):
        return float(v) if v is not None and np.isfinite(v) else float("nan")

    return {"elevation_m": _num(elevation), "terrain_slope": _num(slope)}


def dewpoint_features(tdew: Optional[np.ndarray], tmean: Optional[np.ndarray]) -> dict:
    """Humidity descriptors: dew point and dew-point depression (T - Td).

    Dew point was the most important input in Franch et al.'s maize models. The
    depression is the drying power of the air -- small in the humid season,
    large in the dry one -- and its minimum marks the most humid part of the year.
    """
    out = {k: float("nan") for k in (
        "tdew_min", "tdew_max", "tdew_mean", "tdew_amplitude",
        "dewpoint_depression_min", "dewpoint_depression_max", "dewpoint_depression_mean",
    )}
    day_names = ("doy_tdew_min", "doy_tdew_max", "doy_dewpoint_depression_min")
    _nan_days(out, day_names)
    if tdew is None or not np.isfinite(np.asarray(tdew, dtype=float)).any():
        return out
    smooth = rolling_mean(np.asarray(tdew, dtype=float), SMOOTH_DAYS)
    out["tdew_min"], out["tdew_max"] = _safe(np.nanmin, smooth), _safe(np.nanmax, smooth)
    out["tdew_mean"] = _safe(np.nanmean, smooth)
    out["tdew_amplitude"] = out["tdew_max"] - out["tdew_min"]
    out["doy_tdew_min"], out["doy_tdew_max"] = _argext(smooth, np.nanargmin), _argext(smooth, np.nanargmax)
    if tmean is not None and np.isfinite(np.asarray(tmean, dtype=float)).any():
        dep = rolling_mean(np.asarray(tmean, dtype=float) - np.asarray(tdew, dtype=float), SMOOTH_DAYS)
        out["dewpoint_depression_min"] = _safe(np.nanmin, dep)
        out["dewpoint_depression_max"] = _safe(np.nanmax, dep)
        out["dewpoint_depression_mean"] = _safe(np.nanmean, dep)
        out["doy_dewpoint_depression_min"] = _argext(dep, np.nanargmin)
    for name in day_names:
        _with_circle(out, name)
    return out


def _monthly_means(daily: Optional[np.ndarray]) -> np.ndarray:
    """12 monthly means of a 366-long daily climatology (NaN-aware)."""
    out = np.full(12, np.nan)
    if daily is None:
        return out
    arr = np.asarray(daily, dtype=float)
    months = _MONTH_OF_DOY[: arr.size]
    for m in range(1, 13):
        vals = arr[months == m]
        if vals.size and np.isfinite(vals).sum() >= 0.6 * vals.size:
            out[m - 1] = np.nanmean(vals)
    return out


def season_block_features(
    tmean: Optional[np.ndarray],
    precip: Optional[np.ndarray],
    tdew: Optional[np.ndarray],
    hemisphere: str = "N",
) -> dict:
    """Min / max / amplitude of monthly means within each season and the year.

    Franch et al. (2022)'s climate features -- e.g. their top maize input
    ``dewpoint_avgSeasonMin-winter``, the lowest monthly-mean dew point of the
    winter months. Seasons are hemisphere-aligned (see SEASON_MONTHS_N).
    Precipitation is the monthly mean rate in mm/day.
    """
    shift = 6 if str(hemisphere).upper().startswith("S") else 0
    seasons = {
        name: tuple(((m - 1 + shift) % 12) + 1 for m in months)
        for name, months in SEASON_MONTHS_N.items()
    }
    out: dict = {}
    for var, daily in (("tmean", tmean), ("precip", precip), ("tdew", tdew)):
        monthly = _monthly_means(daily)
        blocks = {name: [monthly[m - 1] for m in months] for name, months in seasons.items()}
        blocks["annual"] = list(monthly)
        for block, values in blocks.items():
            v = np.asarray(values, dtype=float)
            lo, hi = _safe(np.nanmin, v), _safe(np.nanmax, v)
            out[f"{var}_{block}_min"] = lo
            out[f"{var}_{block}_max"] = hi
            out[f"{var}_{block}_amplitude"] = hi - lo
    return out


# --------------------------------------------------------------------------
# Row assembly
# --------------------------------------------------------------------------
def build_row(
    *,
    key: str,
    country: str,
    region: str,
    crop: str,
    season: int,
    cm_group: str,
    climate_zone: str,
    hemisphere: str,
    lat: float,
    lon: float,
    ndvi: np.ndarray,
    gdd: np.ndarray,
    agdd: np.ndarray,
    peaks: Sequence[int],
    valleys: Sequence[int],
    fitted: Optional[np.ndarray] = None,
    tmean: Optional[np.ndarray] = None,
    precip: Optional[np.ndarray] = None,
    precip_years: Optional[pd.DataFrame] = None,
    esi_years: Optional[pd.DataFrame] = None,
    sm_surface: Optional[np.ndarray] = None,
    sm_surface_years: Optional[pd.DataFrame] = None,
    sm_rootzone: Optional[np.ndarray] = None,
    sm_rootzone_years: Optional[pd.DataFrame] = None,
    tdew: Optional[np.ndarray] = None,
    elevation: Optional[float] = None,
    slope: Optional[float] = None,
    calendar_wraps_year: Optional[bool] = None,
    calendar_wall_to_wall: Optional[bool] = None,
    targets: Optional[dict] = None,
) -> dict:
    """One design-matrix row: identifiers, features, metadata, optional targets.

    ``targets`` maps a :data:`TARGETS` name to a calendar day. Each becomes
    ``target_<name>`` plus its ``_sin``/``_cos`` pair and its ``_anchored``
    offset from :data:`ANCHOR_FEATURE`.
    """
    row = {
        "key": key,
        "country": country,
        "region": region,
        "crop": crop,
        "season": str(int(season)),
        "cm_group": cm_group,
        "climate_zone": climate_zone,
        "hemisphere": hemisphere,
        "lat": float(lat),
        "lon": float(lon),
        "abs_lat": abs(float(lat)),
    }
    row.update(curve_features(ndvi, peaks, valleys, fitted=fitted))
    row.update(gdd_features(gdd, agdd))
    row.update(thermal_features(tmean, gdd))
    row.update(precip_features(precip, precip_years))
    row.update(esi_features(esi_years))
    row.update(soil_moisture_features(sm_surface, "sm_surface", sm_surface_years, rise=True))
    row.update(soil_moisture_features(sm_rootzone, "sm_rootzone", sm_rootzone_years, fall=True))
    row["precip_available"] = int(precip is not None)
    row["esi_available"] = int(esi_years is not None)
    row["sm_surface_available"] = int(sm_surface is not None)
    row["sm_rootzone_available"] = int(sm_rootzone is not None)
    row.update(terrain_features(elevation, slope))
    row.update(dewpoint_features(tdew, tmean))
    row.update(season_block_features(tmean, precip, tdew, hemisphere))
    row["terrain_available"] = int(elevation is not None and bool(np.isfinite(elevation)))
    row["tdew_available"] = int(tdew is not None)

    row["calendar_wraps_year"] = calendar_wraps_year
    row["calendar_wall_to_wall"] = calendar_wall_to_wall

    if targets:
        anchor = row.get(ANCHOR_FEATURE, float("nan"))
        for name in TARGETS:
            day = float(targets.get(name, float("nan")))
            row[f"target_{name}"] = day
            sin_value, cos_value = day_to_circle(day)
            row[f"target_{name}_sin"] = sin_value
            row[f"target_{name}_cos"] = cos_value
            row[f"target_{name}_anchored"] = (
                circular.signed_difference(day, anchor)
                if np.isfinite(day) and np.isfinite(anchor)
                else float("nan")
            )
    return row


def _probe_feature_names() -> tuple[str, ...]:
    """Every feature :func:`build_row` can emit, in emission order.

    Built by running the feature functions on empty inputs, so the allow-list
    can never drift from what the row actually contains.
    """
    nan_year = np.full(circular.N_DOY, np.nan)
    probe = build_row(
        key="", country="", region="", crop="", season=1, cm_group="",
        climate_zone="", hemisphere="", lat=float("nan"), lon=float("nan"),
        ndvi=nan_year, gdd=nan_year, agdd=nan_year, peaks=[], valleys=[],
    )
    excluded = set(IDENTIFIER_COLUMNS) | set(METADATA_COLUMNS)
    return tuple(name for name in probe if name not in excluded)


#: The allow-list. Anything not in here -- a target, a baseline day, a calendar
#: flag, a column someone adds to the frame by hand -- is not a model input.
FEATURE_NAMES: tuple[str, ...] = _probe_feature_names()

def _probe_group(fn, *args, **kwargs) -> tuple[str, ...]:
    """The keys one feature function emits on empty input."""
    return tuple(fn(*args, **kwargs))


_NAN_YEAR = np.full(circular.N_DOY, np.nan)

#: Feature names grouped by the function that emits them, for the run manifest.
#: Built by probing each function, not by prefix matching -- a prefix rule put
#: ``gdd_season_length_days`` (a thermal feature) under ``gdd``.
FEATURE_GROUPS = {
    "geography": ("lat", "lon", "abs_lat", "hemisphere", "climate_zone", "cm_group", "crop", "season"),
    "curve": _probe_group(curve_features, _NAN_YEAR, [], []),
    "gdd": _probe_group(gdd_features, _NAN_YEAR, _NAN_YEAR),
    "thermal": _probe_group(thermal_features, None, _NAN_YEAR),
    "precip": _probe_group(precip_features, None, None) + ("precip_available",),
    "esi": _probe_group(esi_features, None) + ("esi_available",),
    "sm_surface": _probe_group(soil_moisture_features, None, "sm_surface", rise=True) + ("sm_surface_available",),
    "sm_rootzone": _probe_group(soil_moisture_features, None, "sm_rootzone", fall=True) + ("sm_rootzone_available",),
    "terrain": _probe_group(terrain_features, None, None) + ("terrain_available",),
    "dewpoint": _probe_group(dewpoint_features, None, None) + ("tdew_available",),
    "season_blocks": _probe_group(season_block_features, None, None, None),
}
assert set(FEATURE_NAMES) == set().union(*FEATURE_GROUPS.values()), "feature groups must partition FEATURE_NAMES"
assert sum(len(v) for v in FEATURE_GROUPS.values()) == len(FEATURE_NAMES), "a feature is in two groups"


def feature_columns(frame: pd.DataFrame) -> list[str]:
    """Model inputs: the allow-listed feature names present in ``frame``.

    An allow-list rather than "everything that is not an identifier or a
    target": the previous deny-list let the rule-based satellite days through
    as features, and those are computed inside a window the calendar defines.
    """
    present = set(frame.columns)
    return [name for name in FEATURE_NAMES if name in present]


def target_columns(frame: pd.DataFrame) -> list[str]:
    return [f"target_{name}" for name in TARGETS if f"target_{name}" in frame.columns]


def design_matrix(rows: Sequence[dict]) -> pd.DataFrame:
    """Assemble rows into a frame.

    Rows are kept even when a target is missing: the evaluation masks per
    target, so a calendar row lacking a harvest never shrinks the mid-greenup
    comparison. Only a row with NO target at all is dropped.
    """
    frame = pd.DataFrame(list(rows))
    if frame.empty:
        return frame
    present = target_columns(frame)
    if present:
        before = len(frame)
        frame = frame.dropna(subset=present, how="all").reset_index(drop=True)
        if len(frame) < before:
            logger.info(f"design matrix: dropped {before - len(frame)} row(s) with no target at all")
    for column in CATEGORICAL_FEATURES:
        if column in frame.columns:
            frame[column] = frame[column].fillna("unknown").astype(str).astype("category")
    return frame
