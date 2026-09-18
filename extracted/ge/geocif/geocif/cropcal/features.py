# -*- coding: utf-8 -*-
"""Turn a region's NDVI/GDD climatology into a row of model features.

The machine-learning comparison asks whether a model can predict the **GEOGLAM
calendar's** transition days from the satellite record, with the rule-based port
as the zero-parameter baseline. That makes the delta and the prediction error
the same quantity, so every method is scored on one metric.

Targets are days of year, which are circular: 1 and 365 are one day apart, and a
regressor trained on the raw number treats them as 364 apart. Both targets are
therefore emitted as a ``(sin, cos)`` pair on the unit circle -- see
:func:`day_to_circle` -- and recombined with ``atan2`` after prediction, which
is what :mod:`geocif.cropcal.models` does.

Features are deliberately descriptors of the *shape* of the year, not the
answers: the unconstrained derivative extrema are included (they are what the
rule-based method starts from), but nothing downstream of the calendar is.
"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

import numpy as np
import pandas as pd

from geocif.cropcal import circular

logger = logging.getLogger(__name__)

#: Categorical columns handed to the model as-is.
CATEGORICAL_FEATURES = ("crop", "hemisphere", "climate_zone", "cm_group")

#: Fractions of annual accumulated GDD whose crossing day becomes a feature.
AGDD_QUANTILES = (0.25, 0.50, 0.75)

TARGETS = ("midgreenup", "midgreendown")


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


def _safe(fn, values, default=float("nan")):
    arr = np.asarray(values, dtype=float)
    if not np.isfinite(arr).any():
        return default
    with np.errstate(all="ignore"):
        return float(fn(arr))


def curve_features(ndvi: np.ndarray, peaks: Sequence[int], valleys: Sequence[int]) -> dict:
    """Shape descriptors of the per-day NDVI climatology."""
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

    # Circular encodings, so a model sees 1 January and 31 December as adjacent.
    for name in ("doy_peak", "doy_max_rise", "doy_max_fall"):
        sin_value, cos_value = day_to_circle(out[name])
        out[f"{name}_sin"], out[f"{name}_cos"] = sin_value, cos_value

    return out


def gdd_features(gdd: np.ndarray, agdd: np.ndarray) -> dict:
    """Thermal descriptors of the year."""
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
        sin_value, cos_value = day_to_circle(out[key])
        out[f"{key}_sin"], out[f"{key}_cos"] = sin_value, cos_value
    return out


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
    targets: Optional[dict] = None,
) -> dict:
    """One design-matrix row, features plus optional targets."""
    row = {
        "key": key,
        "country": country,
        "region": region,
        "crop": crop,
        "season": int(season),
        "cm_group": cm_group,
        "climate_zone": climate_zone,
        "hemisphere": hemisphere,
        "lat": float(lat),
        "lon": float(lon),
        "abs_lat": abs(float(lat)),
    }
    row.update(curve_features(ndvi, peaks, valleys))
    row.update(gdd_features(gdd, agdd))

    if targets:
        for name in TARGETS:
            day = targets.get(name, float("nan"))
            row[f"target_{name}"] = float(day)
            sin_value, cos_value = day_to_circle(day)
            row[f"target_{name}_sin"] = sin_value
            row[f"target_{name}_cos"] = cos_value
    return row


def feature_columns(frame: pd.DataFrame) -> list[str]:
    """Model inputs: everything that is neither an identifier nor a target."""
    identifiers = {"key", "country", "region"}
    return [
        column
        for column in frame.columns
        if column not in identifiers and not column.startswith("target_")
    ]


def design_matrix(rows: Sequence[dict]) -> pd.DataFrame:
    """Assemble rows into a frame, dropping any with a missing target."""
    frame = pd.DataFrame(list(rows))
    if frame.empty:
        return frame
    target_cols = [f"target_{name}" for name in TARGETS]
    present = [c for c in target_cols if c in frame.columns]
    if present:
        before = len(frame)
        frame = frame.dropna(subset=present).reset_index(drop=True)
        if len(frame) < before:
            logger.info(f"design matrix: dropped {before - len(frame)} row(s) with no target")
    for column in CATEGORICAL_FEATURES:
        if column in frame.columns:
            frame[column] = frame[column].fillna("unknown").astype("category")
    return frame
