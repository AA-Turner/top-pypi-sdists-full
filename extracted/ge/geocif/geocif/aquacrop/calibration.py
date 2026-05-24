"""
calibration.py — LOOCV region_anomaly bias correction of AquaCrop
predictions against observed yields.

Despite the filename, no internal AquaCrop parameter (HI, WP, CCx, ...)
is being calibrated. AquaCrop runs with its built-in default parameter
set for the canonical crop name passed (Maize, Wheat, PaddyRice, ...).
What this module does is fit a single additive offset per admin region
on top of the raw AquaCrop output:

    calibrated = raw_aquacrop_yield + region_offset

It mirrors geocif's ``target_mode = region_anomaly`` pattern from
``ml/trainers.py``: subtract per-region train-mean from y, predict the
deviation, add back at inference. AquaCrop's systematic biases against
smallholder yields are dominated by effects AquaCrop cannot model
(fertilizer scarcity, weed/pest pressure, harvest losses); an additive
offset absorbs all of those in one number per region.

Pool options:
- ``cross_country`` — Empirical-Bayes shrinkage of each per-region mean
  residual toward the pooled mean across ALL countries in the training
  set. Stable for data-sparse regions.
- ``within_country`` — pure per-(country, region) mean, no cross-country
  pooling.

LOOCV: for each forecast year Y, training data = all (region, year)
rows except year Y. Calibration is fit separately for each forecast
year so the training set never contains the held-out year.
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def fit_region_anomaly_calibration(
    historical_df: pd.DataFrame,
    *,
    forecast_year: int,
    pool: str = "cross_country",
) -> dict:
    """Fit a LOOCV region_anomaly calibration model.

    Args:
        historical_df: DataFrame with columns Country, Region, Region_ID,
            Harvest Year, Predicted Yield (tn per ha),
            Observed Yield (tn per ha). Should contain ALL years EXCEPT
            the forecast year (the caller is responsible for excluding it).
        forecast_year: Held-out year — used only to verify it's not in the
            training data; not used for fitting.
        pool: 'cross_country' or 'within_country'.

    Returns:
        Dict with:
            'region_offsets': pd.Series indexed by (Country, Region) →
                offset to add to a raw AquaCrop prediction.
            'global_offset': float — fallback for regions with no
                historical data.
            'pool': echoed pool name.
            'n_regions': int — number of regions with a fitted offset.
    """
    df = historical_df.copy()

    # Sanity: no forecast-year rows in training data
    if (df["Harvest Year"] == forecast_year).any():
        logger.warning(
            f"Calibration training set contains forecast year {forecast_year} rows — dropping"
        )
        df = df[df["Harvest Year"] != forecast_year]

    df = df.dropna(subset=[
        "Predicted Yield (tn per ha)", "Observed Yield (tn per ha)",
    ])
    if df.empty:
        logger.warning("No paired AquaCrop+HarvestStat rows for calibration")
        return {
            "region_offsets": pd.Series(dtype=float),
            "global_offset": 0.0,
            "pool": pool,
            "n_regions": 0,
        }

    # Compute residuals (Observed - Predicted)
    df["_resid"] = (
        df["Observed Yield (tn per ha)"]
        - df["Predicted Yield (tn per ha)"]
    )

    # Global fallback offset — mean residual across all (region, year)
    # pairs in the training set.
    global_offset = float(df["_resid"].mean())

    sum_per_region = df.groupby(["Country", "Region"])["_resid"].sum()
    n_per_region = df.groupby(["Country", "Region"]).size()

    if pool == "within_country":
        # Pure per-(country, region) mean — no cross-country pooling.
        region_offsets = sum_per_region / n_per_region
    elif pool == "cross_country":
        # Empirical-Bayes shrinkage toward the cross-country pooled offset:
        #   posterior = (n * sample_mean + k * global_offset) / (n + k)
        # k acts as a prior weight in "equivalent observations". k=3 is
        # mild — regions with N≥15 keep ~83% of their own signal; regions
        # with N=2 are pulled ~60% toward the cross-country mean. This is
        # what makes 'cross_country' meaningfully different from
        # 'within_country' for data-sparse regions.
        k = 3.0
        region_offsets = (sum_per_region + k * global_offset) / (n_per_region + k)
    else:
        raise ValueError(f"Unknown pool: {pool!r}")

    _r_min = region_offsets.min() if not region_offsets.empty else 0.0
    _r_max = region_offsets.max() if not region_offsets.empty else 0.0
    logger.info(
        f"Calibration fitted: {len(region_offsets)} regions, "
        f"global offset {global_offset:+.3f} tn/ha, "
        f"region offset range [{_r_min:+.3f}, {_r_max:+.3f}]"
    )

    return {
        "region_offsets": region_offsets,
        "global_offset": global_offset,
        "pool": pool,
        "n_regions": len(region_offsets),
    }


def apply_region_anomaly_calibration(
    df_predictions: pd.DataFrame,
    model: dict,
    *,
    pred_col: str = "Predicted Yield (tn per ha)",
    calibrated_col: str = "Predicted Yield (tn per ha)",
) -> pd.DataFrame:
    """Apply a fitted calibration model to a new prediction frame.

    Args:
        df_predictions: DataFrame with at least Country, Region, and the
            raw AquaCrop prediction column.
        model: dict returned by ``fit_region_anomaly_calibration``.
        pred_col: Column with raw AquaCrop predictions.
        calibrated_col: Column to write calibrated predictions into. If
            same as ``pred_col``, overwrites in place. Default behaviour
            is overwrite (matches how geocif consumes a single
            'Predicted Yield' column).

    Returns:
        Same DataFrame (modified in place) with calibrated predictions.
    """
    if model["n_regions"] == 0:
        logger.warning("Empty calibration model — leaving predictions raw")
        return df_predictions

    region_offsets = model["region_offsets"]
    global_offset = model["global_offset"]

    def _lookup(row):
        key = (row["Country"], row["Region"])
        if key in region_offsets.index:
            return region_offsets.loc[key]
        return global_offset

    df_predictions = df_predictions.copy()
    offsets = df_predictions.apply(_lookup, axis=1)
    df_predictions[calibrated_col] = df_predictions[pred_col] + offsets

    # Yields can't be negative — clip below 0 since the calibration
    # offset can push very low raw predictions below 0.
    df_predictions[calibrated_col] = df_predictions[calibrated_col].clip(lower=0.0)

    return df_predictions


def loocv_calibrate(
    df_all_years: pd.DataFrame,
    *,
    pool: str = "cross_country",
    pred_col: str = "Predicted Yield (tn per ha)",
) -> pd.DataFrame:
    """Apply LOOCV region_anomaly calibration year-by-year.

    For each unique Harvest Year Y in the input:
        1.  Train on all rows where Harvest Year != Y.
        2.  Apply the fitted model to rows where Harvest Year == Y.

    Args:
        df_all_years: DataFrame with columns Country, Region, Harvest Year,
            Predicted (raw), Observed.
        pool: Calibration pool — 'cross_country' or 'within_country'.

    Returns:
        DataFrame with the calibrated prediction column overwriting the
        raw one. Original raw values preserved under 'Predicted Yield Raw
        (tn per ha)'.
    """
    df = df_all_years.copy()
    df["Predicted Yield Raw (tn per ha)"] = df[pred_col]

    years = sorted(df["Harvest Year"].dropna().unique())
    calibrated_frames = []
    for forecast_year in years:
        train = df[df["Harvest Year"] != forecast_year]
        test = df[df["Harvest Year"] == forecast_year].copy()
        if test.empty:
            continue

        model = fit_region_anomaly_calibration(
            train, forecast_year=int(forecast_year), pool=pool,
        )
        test_calibrated = apply_region_anomaly_calibration(
            test, model, pred_col=pred_col, calibrated_col=pred_col,
        )
        calibrated_frames.append(test_calibrated)

    if not calibrated_frames:
        return df

    return pd.concat(calibrated_frames, ignore_index=False).sort_index()
