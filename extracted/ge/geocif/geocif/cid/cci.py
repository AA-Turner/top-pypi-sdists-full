"""
Load USDA NASS QuickStats Crop Condition Index (CCI) as a per-region monthly
predictor.

The cleaned source CSV (``metadata/crop_condition/quickstats_corn_soy_condition_state.csv``)
has one row per (crop, state, year, week) with columns::

    crop, region, state_alpha, year, woy, week_ending, cci, ...

where ``crop`` is the geocif name (``maize``, ``soybean``, ``rice``,
``sorghum``, ``cotton``, ``winter_wheat``, ``spring_wheat``), ``region`` is the
geocif lowercase-underscore state name (e.g. ``iowa``, ``north_carolina``), and
``cci`` is the 0-100 crop-condition index (weighted from poor/fair/good/excellent).
State-level (admin_1), weekly, 1996 onward.

``get_cci_frame`` collapses the weekly values to a MONTHLY MEAN per
(region, year, month) and returns a long frame ``[region, year, Month, cci]``
ready to merge onto the CID input frame in
``indices.CIDs.preprocess_input_df`` on ``(adm1_name, year/Season, Month)``.
Downstream, ``compute_eo_indices`` aggregates ``cci`` over each stage window
exactly like the EO CIDs (MEAN/MAX/MIN), so no future weeks leak into an
in-season stage.

Because CCI is state-level, an ``admin_2`` (county) run cannot join on
``adm1_name`` (= county). ``get_region_state_map`` maps each county's
``region_id`` (= boundary ``ADM_ID``) to its parent state via the boundary
shapefile, and the caller broadcasts the state CCI onto every county of that
state.

Only the requested crop is returned; crops without CCI coverage yield an empty
frame, so the merge becomes a no-op (no ``cci`` column appears and the CCI
branch is skipped).
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
        crop: geocif crop name (``maize``, ``soybean``, ``rice``,
            ``winter_wheat``, ``spring_wheat``, ``sorghum``, ``cotton``).
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

    # %Good+Excellent, the farmdoc daily (2026) metric: across six peanut
    # states they found the plain G+E share consistently beat weighted
    # condition indices for yield forecasting. The QuickStats extract carries
    # the raw category shares, so expose G+E alongside the weighted index and
    # let the ML stage choose the representation ([ML] cci_windows =
    # current_ge). Absent category columns (older extracts) -> no cci_ge
    # column, downstream no-ops.
    val_cols = ["cci"]
    if "good" in df.columns and "excellent" in df.columns:
        df["cci_ge"] = (
            pd.to_numeric(df["good"], errors="coerce")
            + pd.to_numeric(df["excellent"], errors="coerce")
        )
        val_cols.append("cci_ge")

    monthly = df.groupby(["region", "year", "Month"], as_index=False)[val_cols].mean()
    if years is not None:
        keep = set(int(y) for y in years)
        monthly = monthly[monthly["year"].isin(keep)]
    return monthly[["region", "year", "Month"] + val_cols].reset_index(drop=True)


def _norm_id(x) -> str:
    """Canonicalise an ADM_ID / region_id to a comparable string.

    The crop_t0 CSV may read region_id as int or float, so ``188018001`` and
    ``188018001.0`` must compare equal to the shapefile's ADM_ID. Non-numeric
    ids (rare) pass through as their stripped string.
    """
    s = str(x).strip()
    try:
        f = float(s)
        if f.is_integer():
            return str(int(f))
    except (TypeError, ValueError):
        pass
    return s


def get_region_state_map(parser, country: str, boundary_path) -> dict:
    """Map each admin_2 (county) ``region_id`` to its admin_1 (state) name.

    CCI is reported at the state (admin_1) level, but an ``admin_2`` crop_t0
    keys rows by county (``adm1_name`` = county after standardisation) and only
    carries ``region_id`` (= the boundary ``ADM_ID``). To broadcast the state
    CCI onto county rows we build ``{region_id -> state}`` from the country's
    boundary shapefile, where each county row also carries its parent
    ``ADM1_NAME``. State names are normalised to geocif's lowercase-underscore
    form so they join the CCI frame's ``region`` column.

    Returns an empty dict on any problem (missing shapefile/columns) — the
    caller then skips the CCI merge rather than crashing.
    """
    try:
        from geocif.utils import load_country_boundary_gdf

        gdf = load_country_boundary_gdf(parser, boundary_path, country=country)
        if gdf is None or gdf.empty or "ADM_ID" not in gdf.columns:
            return {}
        adm1_col = next(
            (c for c in ("ADM1_NAME", "ADMIN1", "name1") if c in gdf.columns), None
        )
        if adm1_col is None:
            return {}
        gdf = gdf.dropna(subset=["ADM_ID", adm1_col])
        return {
            _norm_id(rid): str(st).lower().replace(" ", "_")
            for rid, st in zip(gdf["ADM_ID"], gdf[adm1_col])
        }
    except Exception as e:  # noqa: BLE001
        logger.warning(
            f"CCI region->state map unavailable: {type(e).__name__}: {e}"
        )
        return {}
