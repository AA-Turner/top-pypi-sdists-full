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

# In-season gap-fill (see ``fill_cci_gaps``). A month is "normal" for a state when it is
# reported in at least NORMAL_MONTH_SHARE of that state's years; gaps longer than
# MAX_GAP_MONTHS stay missing; persistence only from a report at most MAX_STALENESS_DAYS
# before the gap (winter wheat's fall reports describe a NEW crop, so its June report
# must never be carried into October); states with fewer than MIN_YEARS years are skipped.
NORMAL_MONTH_SHARE = 0.8
MAX_GAP_MONTHS = 2
MAX_STALENESS_DAYS = 21
MIN_YEARS = 5


def _report_dates(df: pd.DataFrame) -> pd.Series:
    """Observation date per row: ``week_ending``, else Jan 1 + (woy - 1) weeks."""
    dates = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
    if "week_ending" in df.columns:
        dates = pd.to_datetime(df["week_ending"], errors="coerce")
    if dates.isna().all() and "woy" in df.columns:
        woy = pd.to_numeric(df["woy"], errors="coerce")
        dates = (
            pd.to_datetime(df["year"].astype(str) + "-01-01", errors="coerce")
            + pd.to_timedelta((woy - 1) * 7, unit="D")
        )
    return dates


def fill_cci_gaps(
    weekly: pd.DataFrame,
    monthly: pd.DataFrame,
    val_cols,
    vintage,
) -> pd.DataFrame:
    """Rows to add for in-season months NASS did not report: the last weekly report.

    NASS sometimes publishes no condition for weeks that are normally covered: the
    Oct 1 - Nov 12 2025 federal shutdown cancelled every Crop Progress release from
    Oct 6 to Nov 10, so October 2025 carries no condition for any state or crop. A
    missing month leaves every October-only CCI window empty, and the ML stage fills
    empty CIDs with 0 -- for a 0-100 condition index that reads as total crop failure
    (it pulled soybean 2025 17-43% low whenever ``MAX_CCI Oct`` was selected). Holding
    out October 2005-2024, the last weekly report landed within ~1.2 (``cci``) and
    ~2.3 (``cci_ge``) index points of the real October mean, against ~60 for zero.

    A (region, year, month) is filled only when all hold:
      * the month is normal for that region (reported in >= NORMAL_MONTH_SHARE of years);
      * the region reported earlier that year (the season had started);
      * it belongs to a run of <= MAX_GAP_MONTHS consecutive missing normal months;
      * the month ended before ``vintage`` (the file's latest report), so the current
        season's future months are never fabricated;
      * the last report before the gap is at most MAX_STALENESS_DAYS old.

    Args:
        weekly: one crop's weekly rows with ``region, year, _date`` and ``val_cols``.
        monthly: that crop's monthly means ``[region, year, Month] + val_cols``.
        val_cols: condition columns to fill (``cci``, optionally ``cci_ge``).
        vintage: latest report date in the whole file (any crop).

    Returns:
        DataFrame ``[region, year, Month] + val_cols`` of filled months (may be empty).
    """
    filled = []
    if monthly.empty or pd.isna(vintage):
        return pd.DataFrame(columns=["region", "year", "Month"] + list(val_cols))
    reported = monthly.groupby(["region", "year"])["Month"].apply(set)
    for region, g in monthly.groupby("region"):
        years = sorted(g["year"].unique())
        if len(years) < MIN_YEARS:
            continue
        share = g.groupby("Month")["year"].nunique() / len(years)
        normal = sorted(int(m) for m in share[share >= NORMAL_MONTH_SHARE].index)
        if not normal:
            continue
        wk = weekly[weekly["region"] == region]
        for y in years:
            months = reported[(region, y)]
            missing = [m for m in normal if m not in months and m > min(months)]
            runs = []
            for m in missing:  # consecutive calendar months form one gap
                if runs and m == runs[-1][-1] + 1:
                    runs[-1].append(m)
                else:
                    runs.append([m])
            for run in runs:
                gap_start = pd.Timestamp(year=int(y), month=run[0], day=1)
                gap_end = pd.Timestamp(year=int(y), month=run[-1], day=1) + pd.offsets.MonthEnd(0)
                if len(run) > MAX_GAP_MONTHS or gap_end >= vintage:
                    continue
                prior = wk[(wk["year"] == y) & (wk["_date"] < gap_start)].sort_values("_date")
                last = {}
                for v in val_cols:
                    obs = prior.dropna(subset=[v])
                    if not obs.empty and (gap_start - obs["_date"].iloc[-1]).days <= MAX_STALENESS_DAYS:
                        last[v] = float(obs[v].iloc[-1])
                if "cci" not in last:
                    continue
                for m in run:
                    filled.append({"region": region, "year": int(y), "Month": int(m),
                                   **{v: last.get(v) for v in val_cols}})
    return pd.DataFrame(filled, columns=["region", "year", "Month"] + list(val_cols))


def get_cci_frame(
    csv_path,
    crop: str,
    years: Optional[Iterable[int]] = None,
    gap_fill: bool = True,
) -> Optional[pd.DataFrame]:
    """Monthly-mean CCI per (region, year, month) for a single crop.

    Args:
        csv_path: path to the cleaned crop-condition CSV.
        crop: geocif crop name (``maize``, ``soybean``, ``rice``,
            ``winter_wheat``, ``spring_wheat``, ``sorghum``, ``cotton``).
        years: optional iterable of years to keep (harvest years).
        gap_fill: fill unreported in-season months with the last weekly report
            (``fill_cci_gaps``); ``[DEFAULT] cci_gap_fill``, on by default.

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

    # The data vintage comes from the WHOLE file: other crops keep reporting after a
    # crop's season ends (e.g. winter wheat in November), which is what tells a gap in
    # a finished season apart from months that simply have not happened yet.
    df["_date"] = _report_dates(df)
    vintage = df["_date"].max()

    df = df[df["crop"].astype(str) == str(crop)].copy()
    if df.empty:
        return df.drop(columns=["_date"])  # crop not covered (e.g. wheat/rice) -> caller no-ops

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
    # Fill BEFORE the ``years`` filter: which months are normal for a state is judged
    # over every year in the file, not just the years this run asked for.
    if gap_fill:
        fills = fill_cci_gaps(df, monthly, val_cols, vintage)
        if not fills.empty:
            shown = ", ".join(
                f"{r.region} {r.year}-{r.Month:02d}={r.cci:.1f}"
                for r in fills.head(12).itertuples(index=False)
            )
            more = f" (+{len(fills) - 12} more)" if len(fills) > 12 else ""
            logger.warning(
                f"CCI gap-fill ({crop}): {len(fills)} unreported in-season month(s) "
                f"set to the last weekly report: {shown}{more}"
            )
            monthly = (
                pd.concat([monthly, fills], ignore_index=True)
                .sort_values(["region", "year", "Month"])
                .reset_index(drop=True)
            )
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
