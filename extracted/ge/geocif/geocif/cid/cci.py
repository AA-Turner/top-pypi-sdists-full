"""
Load USDA NASS QuickStats Crop Condition Index (CCI) as a per-region monthly
predictor.

The cleaned source CSV (``metadata/crop_condition/quickstats_corn_soy_condition_state.csv``)
has one row per (crop, state, year, week) with columns::

    crop, region, state_alpha, year, woy, week_ending, cci, ...

where ``crop`` is the geocif name (``maize``/``soybean``), ``region`` is the
geocif lowercase-underscore state name (e.g. ``iowa``, ``north_carolina``), and
``cci`` is the 0-100 crop-condition index (weighted from poor/fair/good/excellent).
State-level, weekly, 1996 onward, corn (maize) and soybean only.

``get_cci_frame`` collapses the weekly values to a MONTHLY MEAN per
(region, year, month) and returns a long frame ``[region, year, Month, cci]``
ready to merge onto the CID input frame in
``indices.CIDs.preprocess_input_df`` on ``(adm1_name, year/Season, Month)``.
Downstream, ``compute_eo_indices`` aggregates ``cci`` over each stage window
exactly like the EO CIDs (MEAN/MAX/MIN), so no future weeks leak into an
in-season stage.

Only the requested crop is returned; crops without CCI coverage (everything
except maize/soybean) yield an empty frame, so the merge becomes a no-op (no
``cci`` column appears and the CCI branch is skipped).
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def get_cci_frame(
    csv_path,
    crop: str,
    years: Optional[Iterable[int]] = None,
) -> Optional[pd.DataFrame]:
    """Monthly-mean CCI per (region, year, month) for a single crop.

    Args:
        csv_path: path to the cleaned crop-condition CSV.
        crop: geocif crop name (``maize`` / ``soybean``).
        years: optional iterable of years to keep (harvest years).

    Returns:
        DataFrame with columns ``[region, year, Month, cci]`` (monthly mean),
        or ``None`` if the file/columns are missing, or an empty DataFrame if
        the crop has no CCI coverage.
    """
    p = Path(csv_path)
    if not p.exists():
        logger.warning(f"CCI file not found: {p}")
        return None
    df = pd.read_csv(p)
    if "crop" not in df.columns or "cci" not in df.columns or "region" not in df.columns:
        logger.warning(f"CCI file missing required columns (have {list(df.columns)})")
        return None

    df = df[df["crop"].astype(str) == str(crop)].copy()
    if df.empty:
        return df  # crop not covered (e.g. wheat/rice) -> caller no-ops

    # Month from the observation date; fall back to week-of-year if absent.
    if "week_ending" in df.columns:
        wk = pd.to_datetime(df["week_ending"], errors="coerce")
        df["Month"] = wk.dt.month
    if "Month" not in df.columns or df["Month"].isna().all():
        # woy -> month via a nominal calendar (Jan 1 + (woy-1) weeks)
        woy = pd.to_numeric(df.get("woy"), errors="coerce")
        df["Month"] = (
            pd.to_datetime(df["year"].astype(str) + "-01-01")
            + pd.to_timedelta((woy - 1) * 7, unit="D")
        ).dt.month

    df["cci"] = pd.to_numeric(df["cci"], errors="coerce")
    df = df.dropna(subset=["region", "year", "Month", "cci"])
    df["year"] = df["year"].astype(int)
    df["Month"] = df["Month"].astype(int)

    monthly = df.groupby(["region", "year", "Month"], as_index=False)["cci"].mean()
    if years is not None:
        keep = set(int(y) for y in years)
        monthly = monthly[monthly["year"].isin(keep)]
    return monthly[["region", "year", "Month", "cci"]].reset_index(drop=True)
