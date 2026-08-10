"""Yield Outlook Map Generator.

Runs the ML pipeline for the current year and last N historical years,
then generates a diverging choropleth map showing current forecast yield
as a percentage of the historical mean/median prediction per region.
"""

import ast
import logging
import os
import sqlite3
import warnings
from pathlib import Path
from typing import Optional

import arrow as ar
import geopandas as gpd
import numpy as np
import palettable as pal
import pandas as pd

from geocif import geocif_runner as gc
from geocif import logger as log
from geocif import utils as ut
from .viz import plot
from .utils import friendly_stage_label

warnings.simplefilter(action="ignore", category=FutureWarning)

logger = logging.getLogger(__name__)

# Module-level gate for figure rendering, set by run() from [ML] make_maps
# (default False). Kept at module scope so the shared _generate_outlook_map
# renderer can honor it without threading a flag through every call site.
# Default True preserves behavior for any direct caller that bypasses run().
_MAKE_MAPS = True

# Re-export for local use
_display_model_name = ut.display_model_name

# Show usage info on import
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

_console = Console()
_table = Table(show_header=False, box=None, padding=(0, 1))
_table.add_column(style="bold cyan", no_wrap=True)
_table.add_column()
_table.add_row("Usage", "from geocif import yield_outlook; yield_outlook.run(cfg)")
_table.add_row("cfg", "\\[geobase.txt, countries.txt, crops.txt, geocif.txt]")
_table.add_row("reuse_db", "yield_outlook.run(cfg, reuse_db='/path/to/outlook_MM_DD_YYYY.db')")
_console.print(
    Panel(
        _table,
        title="[bold bright_white]GeoCIF Yield Outlook[/]",
        border_style="bright_blue",
        padding=(1, 2),
    )
)


def _load_shapefiles(parser):
    """Load and concatenate shapefiles for all countries.

    Reuses the shapefile loading pattern from analysis.py Geoanalysis.setup().

    Returns:
        dg: Combined GeoDataFrame with 'Country Region' merge column.
        dict_config: Per country_crop config dict with method, crops, models, etc.
    """
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    dir_boundary_files = Path(parser.get("PATHS", "dir_boundary_files"))
    pool_countries = parser.getboolean("ML", "pool_countries", fallback=False)

    dict_config = {}
    all_shapefiles = []

    for country in countries:
        crops = ast.literal_eval(parser.get(country, "crops"))
        models = ast.literal_eval(parser.get(country, "models"))
        method = parser.get(country, "method")
        admin_zone = parser.get(country, "admin_level")

        for crop in crops:
            dict_config[f"{country}_{crop}"] = {
                "method": method,
                "crops": crop,
                "models": models,
                "admin_zone": admin_zone,
            }

        # Load + standardize shapefile via shared helper (Tanzania fix etc.)
        from geocif.utils import load_country_boundary_gdf
        shp_file = parser.get(country, "boundary_file")
        dg_country = load_country_boundary_gdf(
            parser, dir_boundary_files / shp_file
        )

        if "ADM0_NAME" not in dg_country.columns:
            dg_country.loc[:, "ADM0_NAME"] = country.title().replace("_", " ")

        # Filter to current country before dissolve (avoids processing entire gpkg)
        country_display = country.title().replace("_", " ")
        mask = dg_country["ADM0_NAME"].str.lower().str.replace("_", " ") == country_display.lower()
        dg_country = dg_country[mask].copy()

        # Dissolve admin_2 → admin_1 per country when running at admin_1
        if admin_zone == "admin_1":
            n_before = len(dg_country)
            dg_country = ut.dissolve_to_admin1(dg_country)
            logger.info(f"Dissolved {country} admin_2→admin_1: {n_before}→{len(dg_country)} rows")

        # Create "Country Region" merge column per country's admin level
        if admin_zone == "admin_2" and "ADM2_NAME" in dg_country.columns:
            dg_country["Country Region"] = (
                dg_country["ADM0_NAME"] + " " + dg_country["ADM2_NAME"]
            ).str.lower()
        else:
            dg_country["Country Region"] = (
                dg_country["ADM0_NAME"] + " " + dg_country["ADM1_NAME"]
            ).str.lower()

        all_shapefiles.append(dg_country)

    # Add pooled table entries when pool_countries is enabled
    if pool_countries:
        all_crops = set()
        for country in countries:
            crops = ast.literal_eval(parser.get(country, "crops"))
            all_crops.update(crops)
        first_models = ast.literal_eval(parser.get(countries[0], "models"))
        first_method = parser.get(countries[0], "method")
        first_admin = parser.get(countries[0], "admin_level")
        for crop in all_crops:
            dict_config[f"pooled_{crop}"] = {
                "method": first_method,
                "crops": crop,
                "models": first_models,
                "admin_zone": first_admin,
            }

    dg = pd.concat(all_shapefiles, ignore_index=True)

    return dg, dict_config


_CANON_PRED = "Predicted Yield (tn per ha)"
_CANON_OBS = "Observed Yield (tn per ha)"


def _resolve_yield_columns(table_cols):
    """Find the actual Predicted/Observed yield column names in the DB.

    With ``rename_target = True`` + ``new_name_target = Yield`` the DB
    stores ``"Predicted Yield"`` / ``"Observed Yield"`` instead of the
    canonical ``"Predicted Yield (tn per ha)"`` / ``"Observed Yield
    (tn per ha)"``.  We detect the actual names by prefix match and
    rename them to the canonical form in the returned DataFrame so all
    downstream code can keep using the canonical strings.
    """
    pred_col = next(
        (c for c in table_cols if c.startswith("Predicted ") and "Yield" in c),
        None,
    )
    obs_col = next(
        (c for c in table_cols if c.startswith("Observed ") and "Yield" in c),
        None,
    )
    return pred_col, obs_col


def _query_predictions(db_path, table, model, experiment_name="default"):
    """Query predictions from the SQLite database for a specific model.

    Returns DataFrame with canonical columns: Country, Region, Harvest Year,
    Stage Name, Predicted Yield (tn per ha), Observed Yield (tn per ha), and
    optionally "lower CI" / "upper CI" / "Area (ha)" when present.  The
    Predicted/Observed columns are renamed to canonical form even when the
    user's config sets ``rename_target = True``.
    """
    if not db_path.exists():
        logger.error(f"Database not found: {db_path}")
        return pd.DataFrame()

    con = sqlite3.connect(db_path)
    try:
        table_cols = pd.read_sql(f'PRAGMA table_info("{table}")', con)["name"].tolist()

        pred_col, obs_col = _resolve_yield_columns(table_cols)
        if pred_col is None or obs_col is None:
            logger.warning(
                f"Table '{table}' missing Predicted/Observed yield columns"
            )
            return pd.DataFrame()

        # "Stage Window Display" is a newer calendar-order label emitted
        # alongside the load-bearing "Stage Name". Older DBs won't have it;
        # include only when the column exists. "Season" is present only for
        # multi-season countries (e.g. Somalia: 1=Gu, 2=Deyr); single-season
        # / older DBs lack it and stay on the pre-season code path.
        optional_cols = [
            c for c in ("lower CI", "upper CI", "Area (ha)", "Stage Window Display", "Season")
            if c in table_cols
        ]
        extra_select = (
            ("," + ",".join(f'"{c}"' for c in optional_cols))
            if optional_cols else ""
        )

        df = pd.read_sql(
            f'SELECT "Country", "Region", "Harvest Year", "Stage Name", '
            f'"{pred_col}", "{obs_col}"{extra_select} '
            f'FROM "{table}" WHERE "Experiment Name" = ? AND "Model" = ?',
            con,
            params=(experiment_name, model),
        )
    except (pd.errors.DatabaseError, sqlite3.OperationalError) as e:
        logger.warning(f"Failed to query table '{table}': {e}")
        df = pd.DataFrame()
    finally:
        con.close()
    if not df.empty:
        # Rename DB-specific column names to canonical form so downstream
        # code (plots, compute_outlook_index, FDW export) works unchanged.
        rename_map = {}
        if pred_col and pred_col != _CANON_PRED:
            rename_map[pred_col] = _CANON_PRED
        if obs_col and obs_col != _CANON_OBS:
            rename_map[obs_col] = _CANON_OBS
        if rename_map:
            df = df.rename(columns=rename_map)

        if "Harvest Year" in df.columns:
            df["Harvest Year"] = df["Harvest Year"].astype(int)
        numeric_cols = (
            _CANON_PRED, _CANON_OBS,
            "lower CI", "upper CI", "Area (ha)",
        )
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        # Season is a small integer label (1=Gu, 2=Deyr, ...). Coerce to a
        # nullable Int64 so downstream grouping/tokens stay integral even when
        # the DB stored it as float/text; absent for single-season DBs.
        if "Season" in df.columns:
            df["Season"] = pd.to_numeric(df["Season"], errors="coerce").astype("Int64")
    return df


def _compute_outlook_index(df, current_year, n_years, aggregation,
                           use_latest_stage=True, stage_name=None):
    """Compute yield outlook index per region.

    Args:
        use_latest_stage: If True (default), use the latest stage per
            (Country, Region, Harvest Year) so stage name mismatches
            between current and historical years don't matter.
            If False, filter by exact stage_name.

    outlook_index = (current_predicted / agg(historical_predicted)) * 100

    Returns DataFrame with columns: Country, Region, Country Region,
    current_predicted, hist_predicted, outlook_index.

    Season handling: when the input df carries a "Season" column (multi-season
    countries such as Somalia — 1=Gu, 2=Deyr), "Season" is added to EVERY
    grouping key so the result has one row per (Country, Region, Season) plus a
    "Season" column. When "Season" is absent (single-season / older DBs) the
    original single-row-per-region path runs unchanged (byte-for-byte).
    """
    has_season = "Season" in df.columns
    # Grouping keys gain "Season" only when the column is present, so the
    # single-season code path is identical to before.
    latest_keys = (
        ["Country", "Region", "Season", "Harvest Year"] if has_season
        else ["Country", "Region", "Harvest Year"]
    )
    region_keys = (
        ["Country", "Region", "Season"] if has_season
        else ["Country", "Region"]
    )

    if use_latest_stage:
        # For each region(+season)+year, keep only the latest (last) stage
        df_work = (
            df.sort_values("Stage Name")
            .groupby(latest_keys)
            .last()
            .reset_index()
        )
    else:
        df_work = df[df["Stage Name"] == stage_name].copy()

    # Current year predictions per region(+season)
    df_current = df_work[df_work["Harvest Year"] == current_year]
    current_pred = (
        df_current.groupby(region_keys)["Predicted Yield (tn per ha)"]
        .mean()
        .rename("current_predicted")
    )

    # Historical years per region(+season)
    min_year = current_year - n_years
    df_hist = df_work[
        (df_work["Harvest Year"] < current_year)
        & (df_work["Harvest Year"] >= min_year)
    ]
    agg_func = "median" if aggregation == "median" else "mean"
    hist_agg = (
        df_hist.groupby(region_keys)["Predicted Yield (tn per ha)"]
        .agg(agg_func)
        .rename("hist_predicted")
    )

    # Compute index
    df_outlook = pd.concat([current_pred, hist_agg], axis=1).dropna()
    df_outlook["outlook_index"] = np.where(
        df_outlook["hist_predicted"] != 0,
        (df_outlook["current_predicted"] - df_outlook["hist_predicted"])
        / df_outlook["hist_predicted"] * 100,
        np.nan,
    )
    df_outlook = df_outlook.reset_index()

    # Create merge column (same pattern as analysis.py:1410-1414). Region-only
    # (NOT season-scoped): shapefile geometry is per region, and both seasons
    # of a region share the same polygon.
    df_outlook["Country Region"] = (
        df_outlook["Country"].str.lower().str.replace("_", " ")
        + " "
        + df_outlook["Region"].str.lower()
    )

    return df_outlook


def _season_iter(df):
    """Yield ``(season, sub_df, fname_token, label_suffix)`` per season present.

    Backward-compatible splitter used by every outlook-map block:

    * No "Season" column (or all-NaN) -> a single ``(None, df, "", "")`` tuple,
      so callers reproduce the pre-season output byte-for-byte (same paths).
    * Exactly one season present      -> a single ``(s, sub, "", "")`` tuple;
      still no filename token / label suffix (single-season stays unchanged).
    * Two or more seasons              -> one tuple per season, each with a
      ``"_s{n}"`` filename token and a ``" — Season {n}"`` label suffix so the
      maps are distinguishable (e.g. Somalia 1=Gu, 2=Deyr).
    """
    seasons = (
        sorted(df["Season"].dropna().unique())
        if "Season" in df.columns else []
    )
    if not seasons:
        yield None, df, "", ""
        return
    multi = len(seasons) > 1
    for s in seasons:
        sub = df[df["Season"] == s]
        if multi:
            yield s, sub, f"_s{int(s)}", f" — Season {int(s)}"
        else:
            yield s, sub, "", ""


# Default effective parameter counts per model, used by _bma_bic_blend to
# compute BIC = N log(RMSE^2) + p log(N). These are order-of-magnitude
# estimates — foundation models like TabPFN have 100M+ raw parameters
# but "effective" complexity for the in-context few-shot regime is far
# smaller. Users override per-project via [ML] bma_effective_params
# in geocif.txt. Models NOT in this dict (or in the config override)
# are SKIPPED by _bma_bic_blend with a warning — we won't fabricate
# a p_k when we have no basis for the value.
_BMA_BIC_DEFAULT_PARAMS = {
    "null":     1,   # rolling mean baseline
    "trend":    2,   # slope + intercept (Theil-Sen 10yr)
    "catboost": 50,  # boosted trees; effective params << total leaf count
    "tabpfn":  100,  # foundation model, in-context few-shot ≈ context width
    "cubist":   30,  # rules × committees (n_committees=10, ~3 rules each)
}


def _collect_per_region_rmse(
    df_all: pd.DataFrame,
    df_pred_store: dict,
    min_history_years: int = 3,
):
    """Iterator: yields (group_keys, grp, rmse_by_model, N_by_model) tuples.

    Shared prep for both _inv_rmse_stack and _bma_bic_blend. Computes each
    model's per-region RMSE on leak-safe history (Harvest Year < Forecast
    Year), plus the number of historical rows (N) used — BIC needs N.

    Yields nothing for a group when fewer than 2 models have valid history.
    """
    group_keys = ["Country", "Region", "Country Region", "Crop", "Forecast Year"]
    for keys, grp in df_all.groupby(group_keys):
        country, region, _cr, crop, forecast_year = keys
        try:
            forecast_year_int = int(forecast_year)
        except (TypeError, ValueError):
            continue
        models = grp["Model"].tolist()
        if len(models) < 2:
            continue

        rmse_by_model = {}
        n_by_model = {}
        for m in models:
            df_hist_all = df_pred_store.get((country, crop, m))
            if df_hist_all is None or df_hist_all.empty:
                continue
            df_hist = df_hist_all[df_hist_all["Region"] == region].copy()
            if df_hist.empty:
                continue
            hy = pd.to_numeric(df_hist["Harvest Year"], errors="coerce")
            df_hist = df_hist[hy < forecast_year_int].copy()
            df_hist = df_hist.dropna(
                subset=["Observed Yield (tn per ha)", "Predicted Yield (tn per ha)"]
            )
            if len(df_hist) < min_history_years:
                continue
            obs = df_hist["Observed Yield (tn per ha)"].astype(float).values
            pred = df_hist["Predicted Yield (tn per ha)"].astype(float).values
            rmse_by_model[m] = float(np.sqrt(np.mean((pred - obs) ** 2)))
            n_by_model[m] = int(len(df_hist))

        if len(rmse_by_model) < 2:
            continue  # need >=2 models with valid history to blend
        yield keys, grp, rmse_by_model, n_by_model


def _apply_weights_and_emit_row(
    keys, grp, weights, model_name: str,
) -> Optional[dict]:
    """Shared row emitter: blends current_predicted + hist_predicted using
    the supplied ``weights`` dict, computes outlook_index from the blend,
    returns a row dict tagged with ``Model = model_name`` (plus per-model
    weight diagnostic columns).
    """
    country, region, cr, crop, forecast_year = keys
    cur = 0.0
    hist = 0.0
    w_sum = 0.0
    for _, row in grp.iterrows():
        m = row["Model"]
        w = weights.get(m)
        if w is None:
            continue
        cp = float(row["current_predicted"]) if pd.notna(row["current_predicted"]) else None
        hp = float(row["hist_predicted"])    if pd.notna(row["hist_predicted"])    else None
        if cp is None or hp is None:
            continue
        cur += w * cp
        hist += w * hp
        w_sum += w
    if w_sum <= 0:
        return None
    cur /= w_sum
    hist /= w_sum
    outlook_idx = ((cur - hist) / hist * 100.0) if hist != 0 else np.nan

    out = {
        "Country": country,
        "Region": region,
        "Country Region": cr,
        "Crop": crop,
        "Forecast Year": forecast_year,
        "current_predicted": cur,
        "hist_predicted": hist,
        "outlook_index": outlook_idx,
        "Model": model_name,
        "Stage Name": grp["Stage Name"].iloc[-1] if "Stage Name" in grp.columns else "",
    }
    if "Stage Window Display" in grp.columns:
        out["Stage Window Display"] = grp["Stage Window Display"].iloc[-1]
    for m, w in weights.items():
        out[f"w_{m}"] = w
    return out


def _inv_rmse_stack(
    df_all: pd.DataFrame,
    df_pred_store: dict,
    min_history_years: int = 3,
    epsilon: float = 1e-6,
) -> pd.DataFrame:
    """Per-(region, forecast_year) inverse-RMSE weighted stack across models.

    This is the "engineering flavor" ensemble sometimes called BMA in
    applied papers, but it is NOT proper Bayesian Model Averaging — no
    likelihood, no complexity penalty, no parameter integration. It's a
    stacking method where weights are proportional to precision (1/RMSE)
    estimated on per-region leak-safe history (Harvest Year < Forecast Year).

    For real BMA (BIC-based), see :func:`_bma_bic_blend`.

    Args, kwargs, and return schema mirror the original BMA function; the
    emitted pseudo-model name is ``'inv_rmse'``.
    """
    rows = []
    for keys, grp, rmse_by_model, _n_by_model in _collect_per_region_rmse(
        df_all, df_pred_store, min_history_years=min_history_years
    ):
        # Inverse-RMSE weights, normalized to unit sum
        inv = {m: 1.0 / (r + epsilon) for m, r in rmse_by_model.items()}
        total = sum(inv.values())
        weights = {m: w / total for m, w in inv.items()}
        row = _apply_weights_and_emit_row(keys, grp, weights, model_name="inv_rmse")
        if row is not None:
            rows.append(row)
    return pd.DataFrame(rows)


def _bma_bic_blend(
    df_all: pd.DataFrame,
    df_pred_store: dict,
    effective_params: Optional[dict] = None,
    min_history_years: int = 3,
) -> pd.DataFrame:
    """Per-(region, forecast_year) BIC-weighted Bayesian Model Averaging.

    Under Gaussian residuals and flat prior over models, BMA weights are
    approximated by exp(-BIC/2). BIC = N log(RMSE^2) + p log(N), where
    N is the per-region historical sample size and p is the model's
    effective parameter count.

    Weight computation (numerically stable via log-sum-exp):
        log w_k  = -N log(RMSE_k) - (p_k / 2) log(N)
        w_k      = softmax(log w_k)  over models with valid p_k

    Models NOT present in ``effective_params`` are SKIPPED with a warning
    — BIC requires p_k, and fabricating a value would corrupt the ranking.
    Defaults for common geocif models are in ``_BMA_BIC_DEFAULT_PARAMS``.

    Emits pseudo-model name ``'bma'`` (the classical BMA label).

    Args:
        df_all: same as _inv_rmse_stack.
        df_pred_store: same as _inv_rmse_stack.
        effective_params: dict {model_name: p_k}. Merged with
            :data:`_BMA_BIC_DEFAULT_PARAMS`, then user-provided values win.
        min_history_years: same as _inv_rmse_stack.
    """
    params = dict(_BMA_BIC_DEFAULT_PARAMS)
    if effective_params:
        params.update(effective_params)

    rows = []
    skipped_models = set()
    for keys, grp, rmse_by_model, n_by_model in _collect_per_region_rmse(
        df_all, df_pred_store, min_history_years=min_history_years
    ):
        # Compute log-weight = -N log(RMSE) - (p/2) log(N) for each model
        # that has an effective_params entry. Skip unknowns.
        log_w = {}
        for m, rmse in rmse_by_model.items():
            p = params.get(m)
            if p is None:
                skipped_models.add(m)
                continue
            N = n_by_model[m]
            if N <= 0 or rmse <= 0:
                continue
            log_w[m] = -N * np.log(rmse) - 0.5 * p * np.log(N)

        if len(log_w) < 2:
            continue  # need >=2 valid models to blend

        # Softmax normalization (numerically stable)
        log_w_max = max(log_w.values())
        exp_shifted = {m: np.exp(v - log_w_max) for m, v in log_w.items()}
        total = sum(exp_shifted.values())
        weights = {m: v / total for m, v in exp_shifted.items()}

        row = _apply_weights_and_emit_row(keys, grp, weights, model_name="bma")
        if row is not None:
            rows.append(row)

    if skipped_models:
        logger.warning(
            f"BMA-BIC: skipped {len(skipped_models)} model(s) with no "
            f"effective_params entry: {sorted(skipped_models)}. Add them "
            f"to [ML] bma_effective_params in geocif.txt if you want them "
            f"in the BMA blend."
        )
    return pd.DataFrame(rows)


def _load_observed_baselines(countries, crop, parser, current_year=None):
    """Load observed yield baselines from statistics CSVs.

    Returns dict: {period_label -> DataFrame(Region, obs_mean)}
    Periods: '2013-2017', '2018-2022', '10yr' (10 years prior to current_year),
    and a rolling last-5-observed-years window ending the year before the
    forecast year (e.g. current_year 2026 -> '2021-2025', 2014 -> '2009-2013').
    The current season is always excluded from the rolling windows.
    Returns empty dict if no statistics CSVs found.
    """
    from geocif import utils

    dir_output = Path(parser.get("PATHS", "dir_output"))
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    method = parser.get("DEFAULT", "method", fallback="monthly_r")
    dir_out = dir_output / project_name

    frames = []
    for country in countries:
        f = utils.statistics_file_path(dir_out, method, country, crop)
        if f.exists():
            df = pd.read_csv(f)
            if {"Region", "Harvest Year", "Yield (tn per ha)"}.issubset(df.columns):
                frames.append(df[["Region", "Harvest Year", "Yield (tn per ha)"]])

    if not frames:
        return {}

    df_all = pd.concat(frames, ignore_index=True).dropna(subset=["Yield (tn per ha)"])
    max_year = int(df_all["Harvest Year"].max())
    # 10yr upper bound: exclude current forecast year (use current_year-1 if known,
    # otherwise fall back to max_year-1 which may exclude the last observed season)
    y2_10yr = (current_year - 1) if current_year is not None else (max_year - 1)
    # Rolling last-5-observed-years window ending the year BEFORE the forecast
    # year (the forecast year isn't observed yet): current_year 2026 -> 2021-2025,
    # 2014 -> 2009-2013. Falls back to the last observed year if current_year is
    # unknown. Anomaly maps built from this show the current prediction's %
    # departure from the most recent 5-year observed norm.
    last5_y2 = (current_year - 1) if current_year is not None else max_year
    last5_y1 = last5_y2 - 4
    last5_label = f"{last5_y1}-{last5_y2}"
    baselines = {}
    for label, y1, y2 in [
        ("2013-2017", 2013, 2017),
        ("2018-2022", 2018, 2022),
        ("10yr", max_year - 10, y2_10yr),
        (last5_label, last5_y1, last5_y2),
    ]:
        sub = df_all[(df_all["Harvest Year"] >= y1) & (df_all["Harvest Year"] <= y2)]
        if sub.empty:
            continue
        baselines[label] = (
            sub.groupby("Region")["Yield (tn per ha)"]
            .mean()
            .reset_index()
            .rename(columns={"Yield (tn per ha)": "obs_mean"})
        )
    return baselines


def _generate_diagnostics_for_stage(df, country, crop, model, dg, dir_outlook,
                                    stage_name="", forecast_year=None,
                                    admin_level="admin_1", yield_units="Mg/ha"):
    """Generate scatter, MAPE bar chart, and MAPE map for one stage.

    Args:
        df: DataFrame with obs/pred columns for this stage.
        country, crop, model: Identifiers.
        dg: GeoDataFrame for choropleth maps.
        dir_outlook: Base output directory.
        stage_name: Stage name suffix for filenames/subdirectories.
    """
    import matplotlib.pyplot as plt
    from .viz import diagnostics as diag
    import scienceplots  # noqa: F401

    obs_col = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"
    df = df.dropna(subset=[obs_col, pred_col]) if obs_col in df.columns else pd.DataFrame()
    if df.empty:
        return

    countries_display = [country.title().replace("_", " ")]
    friendly = friendly_stage_label(stage_name) if stage_name else ""
    stage_safe = friendly.replace(" - ", "-").replace(" ", "_") if friendly else ""
    stage_suffix = f"_{stage_safe}" if stage_safe else ""

    dir_plots = dir_outlook / "plots" / model / country / crop
    dir_maps = dir_outlook / "maps" / model / country / crop
    dir_csvs = dir_outlook / "csvs" / model / country / crop
    if stage_safe:
        dir_plots = dir_plots / stage_safe
        dir_maps = dir_maps / stage_safe
        dir_csvs = dir_csvs / stage_safe
    os.makedirs(dir_plots, exist_ok=True)
    os.makedirs(dir_maps, exist_ok=True)
    os.makedirs(dir_csvs, exist_ok=True)

    title = f"{country.title().replace('_', ' ')} {crop.title().replace('_', ' ')} — {model}"
    if stage_name:
        title += f" ({diag.friendly_stage_label(stage_name)})"

    with plt.style.context(["science", "no-latex"]):
        diag.scatter_obs_pred(df, title, dir_plots,
                              f"scatter_{country}_{crop}_{model}{stage_suffix}.png",
                              yield_units=yield_units)
        df.to_csv(dir_csvs / f"scatter_{country}_{crop}_{model}{stage_suffix}.csv", index=False)

        # National scatter (area-weighted)
        df_national = _aggregate_national_yields(df)
        if len(df_national) >= 2:
            title_nat = f"{title} — National"
            diag.scatter_obs_pred(df_national, title_nat, dir_plots,
                                  f"scatter_national_{country}_{crop}_{model}{stage_suffix}.png",
                                  yield_units=yield_units)
            df_national.to_csv(dir_csvs / f"scatter_national_{country}_{crop}_{model}{stage_suffix}.csv", index=False)

        # Per-year scatter (one PNG per Harvest Year). Sliced from `df`;
        # reuses diag.scatter_obs_pred so RMSE/MAPE/r²/N annotations are
        # auto-computed per year. Skipped for years with <2 valid points.
        if "Harvest Year" in df.columns:
            dir_scatter_year = dir_plots / "scatter_by_year"
            dir_csv_year = dir_csvs / "scatter_by_year"
            os.makedirs(dir_scatter_year, exist_ok=True)
            os.makedirs(dir_csv_year, exist_ok=True)
            for yr, df_year in df.groupby("Harvest Year"):
                df_year = df_year.dropna(subset=[obs_col, pred_col])
                if len(df_year) < 2:
                    continue
                yr_int = int(yr) if pd.notna(yr) else yr
                title_year = f"{title} — {yr_int}"
                fname_year = (
                    f"scatter_{country}_{crop}_{model}{stage_suffix}_{yr_int}.png"
                )
                # Per-year scatter: every point shares a single Harvest Year,
                # so color by Region instead — that's the only dimension that
                # varies within the panel.
                diag.scatter_obs_pred(
                    df_year, title_year, dir_scatter_year, fname_year,
                    color_by="region", yield_units=yield_units,
                )
                df_year.to_csv(
                    dir_csv_year / fname_year.replace(".png", ".csv"),
                    index=False,
                )

        # Per-(Region, Harvest Year) MAPE rows — feeds the box plot
        # directly (distribution per region) and is aggregated to per-region
        # mean below for the choropleth that needs one value per region.
        df_mape_raw = df.assign(
            MAPE=lambda d: (
                (d[pred_col] - d[obs_col]).abs() / d[obs_col].replace(0, np.nan) * 100
            )
        ).dropna(subset=["MAPE"])
        prod_pct = diag.compute_production_pct(df, country)
        diag.mape_box_by_region(
            df_mape_raw, title, dir_plots,
            f"mape_box_region_{country}_{crop}_{model}{stage_suffix}.png",
            production_pct=prod_pct,
        )
        df_mape_raw.to_csv(
            dir_csvs / f"mape_box_region_{country}_{crop}_{model}{stage_suffix}.csv",
            index=False,
        )
        df_mape = df_mape_raw.groupby("Region", as_index=False)["MAPE"].mean()

    df_mape["Country Region"] = (
        country.lower().replace("_", " ") + " " + df_mape["Region"].str.lower()
    )
    df_mape = df_mape.rename(columns={"MAPE": "Mean Absolute Percentage Error"})
    # Case-INSENSITIVE country filter. ``countries_display`` is built with
    # ``str.title()`` ("United States Of America"), but the shapefile stores
    # the natural-English form ("United States of America"). A case-sensitive
    # ``.isin`` matched zero rows there, so the choropleth drew an empty
    # country (outline + colorbar only, no filled regions). Lower-casing both
    # sides fixes every country with a lowercase connector word (of/and/the).
    _cd_lower = {c.lower() for c in countries_display}
    dg_sub = dg[dg["ADM0_NAME"].str.lower().isin(_cd_lower)].copy()
    logger.info(f"Map GeoDataFrame: {len(dg_sub)} rows, geom types: {dg_sub.geometry.type.unique()}")
    diag.mape_choropleth(
        dg_sub, df_mape, countries_display, False,
        dir_maps, f"mape_map_{country}_{crop}_{model}{stage_suffix}.png",
    )

    # Per-region RMSE and R² choropleths (companions to the MAPE map). Both
    # are computed across the historical years present in `df` for this stage:
    # RMSE = sqrt(mean((pred-obs)^2)); R² via sklearn (needs >=2 years and
    # >1 distinct observed value, else NaN → region grayed out). Same merge
    # key and dg_sub as the MAPE map so the fix above covers them too.
    from sklearn.metrics import r2_score
    _metric_rows = []
    for _region, _g in df.groupby("Region"):
        _g = _g.dropna(subset=[obs_col, pred_col])
        if _g.empty:
            continue
        _err = _g[pred_col].to_numpy() - _g[obs_col].to_numpy()
        _rmse = float(np.sqrt(np.mean(_err ** 2)))
        _r2 = np.nan
        if len(_g) >= 2 and _g[obs_col].nunique() > 1:
            try:
                _r2 = float(r2_score(_g[obs_col], _g[pred_col]))
            except ValueError:
                _r2 = np.nan
        _metric_rows.append({"Region": _region, "RMSE": _rmse, "R2": _r2})
    if _metric_rows:
        df_metrics = pd.DataFrame(_metric_rows)
        df_metrics["Country Region"] = (
            country.lower().replace("_", " ") + " " + df_metrics["Region"].str.lower()
        )
        df_metrics.to_csv(
            dir_csvs / f"metric_map_{country}_{crop}_{model}{stage_suffix}.csv",
            index=False,
        )
        # RMSE: lower is better → same reversed Bamako as MAPE (low = light).
        diag.metric_choropleth(
            dg_sub, df_metrics, countries_display, False,
            dir_maps, f"rmse_map_{country}_{crop}_{model}{stage_suffix}.png",
            col="RMSE", label=f"RMSE ({yield_units})", vmin=0.0,
        )
        # R²: higher is better → non-reversed Bamako (high = light). Cap the
        # top of the scale at 1.0 (perfect); negative-skill regions keep their
        # data-driven floor.
        diag.metric_choropleth(
            dg_sub, df_metrics, countries_display, False,
            dir_maps, f"r2_map_{country}_{crop}_{model}{stage_suffix}.png",
            col="R2", label="R²", vmax=1.0, higher_is_better=True,
        )

    # Combined: predicted yield map + MAPE bar chart
    _plot_combined_map_mape(
        df, df_mape, dg_sub, country, crop, model, dir_plots,
        f"combined_{country}_{crop}_{model}{stage_suffix}.png",
        title, prod_pct,
        forecast_year=forecast_year, admin_level=admin_level,
        yield_units=yield_units,
    )


def _plot_combined_map_mape(df, df_mape, dg_sub, country, crop, model,
                            dir_out, fname, title, prod_pct,
                            forecast_year=None, admin_level="admin_1",
                            yield_units="Mg/ha"):
    """Side-by-side: predicted yield choropleth (left) + MAPE box plot (right).

    Reuses ``viz.plot.plot_map`` with ``ax=`` for the map panel. The
    right panel mirrors ``diag.mape_box_by_region`` (boxes + jittered
    per-(Region, Year) dots) so year-to-year MAPE variability stays
    visible — the legacy mean-bar variant collapsed that distribution.

    df_mape is unused (kept for backward signature compat); the box
    panel pulls per-(Region, Year) MAPE directly from raw ``df``.
    """
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    import palettable as pal
    import scienceplots  # noqa: F401
    from .viz import diagnostics as diag
    from .viz.diagnostics import _label_with_pct

    pred_col = "Predicted Yield (tn per ha)"
    obs_col = "Observed Yield (tn per ha)"

    # Use forecast_year if provided, else latest year in data
    if forecast_year and "Harvest Year" in df.columns:
        df_latest = df[df["Harvest Year"] == forecast_year].copy()
        display_year = forecast_year
    elif "Harvest Year" in df.columns:
        display_year = df["Harvest Year"].max()
        df_latest = df[df["Harvest Year"] == display_year].copy()
    else:
        df_latest = df.copy()
        display_year = ""

    if df_latest.empty or pred_col not in df_latest.columns:
        return

    df_latest["Country Region"] = (
        country.lower().replace("_", " ") + " " + df_latest["Region"].str.lower()
    )
    df_pred_region = df_latest.groupby(["Region", "Country Region"])[pred_col].mean().reset_index()

    # Per-(Region, Harvest Year) MAPE for the right-panel box distribution.
    df_box = df.dropna(subset=[obs_col, pred_col]).copy()
    df_box = df_box[df_box[obs_col] != 0]
    if df_box.empty:
        return
    df_box["MAPE"] = (df_box[pred_col] - df_box[obs_col]).abs() / df_box[obs_col] * 100
    by_region = {r: g["MAPE"].dropna().values for r, g in df_box.groupby("Region")}
    by_region = {r: v for r, v in by_region.items() if len(v) > 0}
    if not by_region:
        return

    # Sort by production share descending (largest at top of horizontal box).
    if prod_pct:
        regions_sorted = sorted(by_region.keys(),
                                key=lambda r: prod_pct.get(r, 0))
        labels = _label_with_pct(regions_sorted, prod_pct)
    else:
        regions_sorted = sorted(by_region.keys(),
                                key=lambda r: float(np.median(by_region[r])),
                                reverse=True)
        labels = list(regions_sorted)

    countries_display = [country.title().replace("_", " ")]
    annot_col = "ADM2_NAME" if admin_level == "admin_2" else "ADM1_NAME"

    with plt.style.context(["science", "no-latex"]):
        fig = plt.figure(figsize=(14, max(5, len(regions_sorted) * 0.5)))
        ax_map = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
        ax_box = fig.add_subplot(1, 2, 2)

        # Left: predicted yield map via plot_map
        plot.plot_map(
            dg_sub,
            df_pred_region,
            merge_col="Country Region",
            name_country=countries_display,
            name_col=pred_col,
            label=f"Predicted yield ({yield_units})",
            title=f"Predicted Yield — {display_year}",
            vmin=float(df_pred_region[pred_col].min()),
            vmax=float(df_pred_region[pred_col].max()),
            cmap=pal.scientific.sequential.Bamako_20_r,
            series="sequential",
            annotate_regions=True,
            annotate_region_column=annot_col,
            ax=ax_map,
        )

        # Right: MAPE distribution per region (box + jittered dots). Only
        # cap+break when a per-(Region, Year) MAPE exceeds MAPE_CAP*1.5.
        MAPE_CAP = 100.0
        overall_max = float(max(
            (np.nanmax(v) for v in by_region.values() if len(v)),
            default=0.0,
        ))
        do_cap = overall_max > MAPE_CAP * 1.5
        data_clipped = [
            (np.minimum(by_region[r], MAPE_CAP) if do_cap else by_region[r])
            for r in regions_sorted
        ]
        bp = ax_box.boxplot(
            data_clipped, vert=False, tick_labels=labels,
            patch_artist=True, widths=0.6, showfliers=False,
            medianprops={"color": "black", "linewidth": 1.4},
        )
        for patch in bp["boxes"]:
            patch.set_facecolor("steelblue")
            patch.set_alpha(0.35)
            patch.set_edgecolor("steelblue")

        rng = np.random.default_rng(42)
        for i, vals in enumerate(data_clipped):
            if len(vals) == 0:
                continue
            ys = (i + 1) + rng.uniform(-0.18, 0.18, size=len(vals))
            ax_box.scatter(
                vals, ys, s=14, color="#1f4e79", alpha=0.65,
                edgecolors="none", zorder=3,
            )

        if do_cap:
            for i, r in enumerate(regions_sorted):
                rmax = float(np.max(by_region[r]))
                if rmax > MAPE_CAP:
                    ax_box.text(
                        MAPE_CAP + 1, i + 1, f"max={rmax:.0f}% →",
                        va="center", fontsize=7, color="#b53b3b",
                        fontweight="bold",
                    )
            ax_box.set_xlim(0, MAPE_CAP + 18)
            diag._draw_axis_break(ax_box, axis="x", position=MAPE_CAP)
        ax_box.set_xlabel("Mean Absolute Percentage Error (%)")
        ax_box.set_title("MAPE Distribution by Region", fontsize=10, fontweight="bold")
        ax_box.tick_params(axis='y', which='minor', length=0)
        ax_box.grid(True, axis='x', linestyle=':', alpha=0.4)

        fig.suptitle(title, fontsize=12, fontweight="bold", y=1.02)
        fig.subplots_adjust(wspace=0.3)

        Path(dir_out).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(dir_out) / fname, dpi=250, bbox_inches="tight")
        plt.close(fig)


_MONTH_ORDER = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


def _infer_planting_month(stage_names):
    """Return the planting month inferred from pre-season Stage Names.

    Pre-season init months always form a contiguous block in the calendar
    (set by ``utils.get_pre_season_init_months``); planting is the calendar
    month immediately after the latest init in the block, with year wrap.

    Returns ``None`` when no Pre-Season stages are present — callers fall
    back to the legacy ordering.
    """
    import re

    months = set()
    for name in stage_names:
        if isinstance(name, str) and name.startswith("Pre-Season"):
            match = re.search(r"init (\w+)", name)
            if match:
                mn = _MONTH_ORDER.get(match.group(1))
                if mn:
                    months.add(mn)
    if not months:
        return None
    for candidate in range(1, 13):
        prev = 12 if candidate == 1 else candidate - 1
        if candidate not in months and prev in months:
            return candidate
    return None


_MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MONTH_NUM = {m: i + 1 for i, m in enumerate(_MONTH_ABBR)}
_NUM_MONTH = {i + 1: m for i, m in enumerate(_MONTH_ABBR)}


def _swd_month(token):
    """Month number from a Stage-Window-Display token.

    Tokens look like ``"Jun 1"`` / ``"Mar 31"`` (calendar-order endpoints
    from ``geocif.utils.dict_growth_stages_monthly[_end]``); a bare month
    name like ``"March"`` also works. Returns ``None`` if unparseable.
    """
    if not isinstance(token, str) or not token.strip():
        return None
    return _MONTH_NUM.get(token.strip()[:3].title())


_CAL_MONTH_PREFIX = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"])}


def _window_bounds(swd):
    """('Mar 1-Jun 30') -> (3, 6); (None, None) if unparseable."""
    if not isinstance(swd, str) or "-" not in swd:
        return (None, None)
    left, right = swd.split("-", 1)
    return (_swd_month(left), _swd_month(right))


def _season_bounds_from_windows(windows):
    """Planting & harvest months = start/end of the longest cumulative window.

    Each Stage Window Display is calendar-order ('<plant> 1-<as-of> 31'); the
    full-season step has the widest span, so its start = planting and its end =
    harvest. Fallback for when the crop calendar lacks the crop/season. Returns
    (plant_month, harvest_month) ints, or (None, None).
    """
    best, best_span = None, -1
    for swd in set(w for w in windows if isinstance(w, str)):
        p, e = _window_bounds(swd)
        if p is None or e is None:
            continue
        span = (e - p) % 12
        if span > best_span:
            best_span, best = span, (p, e)
    return best if best is not None else (None, None)


def _calendar_bounds(calendar_path, country, crop, season):
    """(planting_month, harvest_month) ints from an EWCM-style crop calendar.

    Sheet ``{crop}_{season}`` (or ``{crop}`` for wheat); half-month columns
    ``jan_1..dec_15`` encode 1=planting, 2=growing, 3=harvest. Reads the
    country's admin/livelihood-zone rows that grow the crop, then takes
    planting = first month flagged 1 and harvest = first month flagged 3
    walking forward from planting (cross-year aware). (None, None) if the
    file/sheet/country is absent — caller then falls back to stage windows.
    """
    from pathlib import Path

    calendar_path = Path(calendar_path)
    if not calendar_path.exists():
        return (None, None)
    try:
        xl = pd.ExcelFile(calendar_path)
    except Exception:
        return (None, None)
    sheet = f"{crop}_{season}"
    if sheet not in xl.sheet_names:
        if crop in xl.sheet_names:          # wheat-style single-season sheet
            sheet = crop
        else:
            xl.close()
            return (None, None)
    try:
        df = pd.read_excel(xl, sheet_name=sheet)
    finally:
        xl.close()

    ccol = next((c for c in df.columns if c.lower() == "country"), None)
    monthcols = [c for c in df.columns
                 if "_" in c and c.split("_")[0].lower() in _CAL_MONTH_PREFIX]
    if ccol is None or not monthcols:
        return (None, None)
    rows = df[df[ccol].astype(str).str.lower().str.strip()
              == country.lower().replace("_", " ")]
    grown = rows[(rows[monthcols] > 0).any(axis=1)] if not rows.empty else rows
    if grown.empty:
        return (None, None)

    def _month_has(val):
        has = {}
        for c in monthcols:
            m = _CAL_MONTH_PREFIX[c.split("_")[0].lower()]
            has[m] = has.get(m, False) or bool((grown[c] == val).any())
        return has

    plant_has, harv_has = _month_has(1), _month_has(3)
    plant = next((m for m in range(1, 13) if plant_has.get(m)), None)
    if plant is None:
        return (None, None)
    harvest = next((((plant - 1 + i) % 12) + 1 for i in range(12)
                    if harv_has.get(((plant - 1 + i) % 12) + 1)), None)
    return (plant, harvest)


def _add_calendar_columns(df, season_bounds=None):
    """Add ``Planting Month`` / ``Harvest Month`` / ``Prediction Month``.

    * ``Prediction Month`` – as-of month of THIS row's window (its later
      endpoint in ``Stage Window Display``, i.e. the month data ran through).
    * ``Planting`` / ``Harvest Month`` – season constants. Taken from
      ``season_bounds`` — a dict keyed ``(Country, Crop, Season) -> (plant,
      harvest)`` built from each country's crop calendar (see
      ``_calendar_bounds``) — so the live in-season year's truncated windows
      don't understate the harvest. Falls back to the longest window in each
      group of this frame when no bound is supplied.

    No-op if the three columns already exist or ``Stage Window Display`` is
    absent. Rows with an unparseable window get blank calendar cells.
    """
    if "Stage Window Display" not in df.columns:
        return df
    if {"Planting Month", "Harvest Month", "Prediction Month"}.issubset(df.columns):
        return df

    df = df.copy()
    swd = df["Stage Window Display"]
    df["Prediction Month"] = swd.map(lambda s: _NUM_MONTH.get(_window_bounds(s)[1]))

    has_season = "Season" in df.columns

    def _season_val(v):
        try:
            return int(v) if v is not None and v == v else None  # NaN-safe
        except (TypeError, ValueError):
            return None

    if season_bounds:
        plant_out, harv_out = [], []
        countries = df["Country"] if "Country" in df.columns else [None] * len(df)
        crops = df["Crop"] if "Crop" in df.columns else [None] * len(df)
        seasons = df["Season"] if has_season else [None] * len(df)
        for c, cr, s in zip(countries, crops, seasons):
            p, h = season_bounds.get((c, cr, _season_val(s)), (None, None))
            plant_out.append(_NUM_MONTH.get(p))
            harv_out.append(_NUM_MONTH.get(h))
        df["Planting Month"] = plant_out
        df["Harvest Month"] = harv_out
    else:
        grp_cols = [c for c in ("Country", "Region", "Crop", "Season") if c in df.columns]
        lookup = {}
        for gk, sub in df.groupby(grp_cols, dropna=False):
            key = gk if isinstance(gk, tuple) else (gk,)
            lookup[key] = _season_bounds_from_windows(sub["Stage Window Display"])
        keys = [tuple(r) for r in df[grp_cols].to_numpy()]
        df["Planting Month"] = [_NUM_MONTH.get(lookup.get(k, (None, None))[0]) for k in keys]
        df["Harvest Month"] = [_NUM_MONTH.get(lookup.get(k, (None, None))[1]) for k in keys]

    return df


_MONTHLY_HISTORY_COLS = [
    "Crop", "Region", "Season", "Harvest Year",
    "Planting Month", "Prediction Month", "Harvest Month",
    "Predicted Yield (tn per ha)", "Observed Yield (tn per ha)",
    "lower CI", "upper CI", "Area (ha)", "Stage Window Display",
]


def _write_monthly_history(df_pred_store, season_bounds, dir_outlook):
    """Write the full per-model forecast history, one row per time step.

    The headline ``yield_outlook_*.csv`` collapses to the live forecast year,
    so the hindcast series that every skill metric is computed from is only
    recoverable by stitching the per-stage files back together. This writes it
    directly: one row per crop x region x season x harvest year x prediction
    month, predicted alongside observed, as
    ``{country}_{model}_monthly_{first}_{last}.csv``.

    Rows are ordered by months-since-planting rather than calendar month so a
    season that wraps the new year stays in forecast order. Returns the paths
    written.
    """
    by_country_model = {}
    for (country, crop, model), df in df_pred_store.items():
        if df is None or df.empty or "Stage Window Display" not in df.columns:
            continue
        part = df.copy()
        part["Crop"] = crop
        by_country_model.setdefault((country, model), []).append(part)

    written = []
    for (country, model), parts in by_country_model.items():
        out = _add_calendar_columns(pd.concat(parts, ignore_index=True), season_bounds)
        for col in _MONTHLY_HISTORY_COLS:
            if col not in out.columns:
                out[col] = pd.NA
        out = out[_MONTHLY_HISTORY_COLS]

        years = pd.to_numeric(out["Harvest Year"], errors="coerce")
        if years.dropna().empty:
            continue

        plant_num = out["Planting Month"].map(_MONTH_NUM)
        pred_num = out["Prediction Month"].map(_MONTH_NUM)
        out = out.assign(
            _yr=years,
            _step=(pred_num - plant_num) % 12,  # season-relative, wrap-safe
        ).sort_values(
            ["Crop", "Region", "Season", "_yr", "_step"], kind="mergesort"
        ).drop(columns=["_yr", "_step"])

        path = (dir_outlook /
                f"{country}_{model}_monthly_"
                f"{int(years.min())}_{int(years.max())}.csv")
        out.to_csv(path, index=False)
        logger.info(f"Monthly history CSV saved to {path} ({len(out):,} rows)")
        written.append(path)
    return written


def _stage_sort_key(name, planting_month=None):
    """Sort stage names chronologically.

    Pre-Season stages sort first (before any in-season stage). When
    ``planting_month`` is provided, init months are ordered by
    "months-before-planting" descending — i.e. earliest forecast first,
    latest pre-season init right before planting last. Works for any
    hemisphere / cross-year season.

    When ``planting_month`` is ``None``, falls back to the legacy
    hardcoded wrap-around (assumes ~March planting) for backward
    compatibility with callers that haven't been updated.
    """
    import re

    if name.startswith("Pre-Season") or name.startswith("In-Season"):
        match = re.search(r"init (\w+)", name)
        if match:
            m = _MONTH_ORDER.get(match.group(1), 0)
            if planting_month is not None and 1 <= planting_month <= 12:
                # Months-before-planting (mod 12); negate so ascending sort
                # puts the *earliest* (furthest-from-planting) init first.
                return -((planting_month - m) % 12)
            # Legacy fallback — March-planting wrap.
            return m - 24 if m >= 7 else m - 12
        return -1
    parts = name.split("-")
    if len(parts) == 2:
        s = _MONTH_ORDER.get(parts[0].strip().split()[0], 0)
        e = _MONTH_ORDER.get(parts[1].strip().split()[0], 0)
        if s or e:
            return (s - e) % 12 if s >= e else s - e + 12
    # Season-normalized numeric labels ("10%-100%", "Stages 1-3", "10-100"):
    # order by the leading integer (decile / growth-stage code).
    nums = re.findall(r"\d+", name)
    return int(nums[0]) if nums else 0


def _compute_region_metric(df, stages_sorted, metric_col):
    """Compute per-region metric at each stage."""
    return (
        df.groupby(["Stage Name", "Region"])[metric_col]
        .mean()
        .reset_index()
    )


def _compute_rrmsep(df, obs_col, pred_col):
    """Paper-conformant rRMSEp (arxiv:2506.19046, sec 5).

    Returns ``(mean_rrmsep, std_rrmsep, n_years)``.

    Denominator: **pooled** ``mean(obs)`` across the entire df (one
    constant per call — "the mean yield per crop").
    Numerator (per LOOCV year): RMSE across all regions in that year.
    Output: mean and stdev of the per-year rRMSEp series.
    """
    d = df.dropna(subset=[obs_col, pred_col]).copy()
    d = d[d[obs_col] != 0]
    if d.empty or "Harvest Year" not in d.columns:
        return np.nan, np.nan, 0
    pooled_mean = float(d[obs_col].mean())
    if pooled_mean <= 0:
        return np.nan, np.nan, 0
    rrmsep_by_year = []
    for _y, g in d.groupby("Harvest Year"):
        err = g[pred_col] - g[obs_col]
        rmse_y = float(np.sqrt((err ** 2).mean()))
        rrmsep_by_year.append(100.0 * rmse_y / pooled_mean)
    if not rrmsep_by_year:
        return np.nan, np.nan, 0
    return (
        float(np.mean(rrmsep_by_year)),
        float(np.std(rrmsep_by_year)),
        len(rrmsep_by_year),
    )


def _aggregate_national_yields(df):
    """Area-weighted national observed/predicted yield per year."""
    obs_col = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"
    has_area = "Area (ha)" in df.columns and df["Area (ha)"].notna().any()

    if has_area:
        df = df.copy()
        df["_prod_obs"] = df[obs_col] * df["Area (ha)"]
        df["_prod_pred"] = df[pred_col] * df["Area (ha)"]
        nat = df.groupby("Harvest Year").agg(
            _prod_obs=("_prod_obs", "sum"),
            _prod_pred=("_prod_pred", "sum"),
            _area=("Area (ha)", "sum"),
        )
        nat[obs_col] = nat["_prod_obs"] / nat["_area"]
        nat[pred_col] = nat["_prod_pred"] / nat["_area"]
    else:
        nat = df.groupby("Harvest Year").agg({obs_col: "mean", pred_col: "mean"})

    return nat.reset_index()


def _compute_national_metric(df, stages_sorted, metric_col, has_area):
    """Compute true national-scale metric per stage.

    When the dataframe carries raw yield columns we aggregate per-region yield
    × area into a national time series per year (so regional over/under-
    prediction can cancel in aggregation, the standard meaning of
    "national-scale error") and then evaluate the metric on that series.

    Without raw yields we fall back to area-weighted regional means using the
    multi-year average area as the weight (``first`` would pick an arbitrary
    year's area).
    """
    obs_col = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"
    has_yields = obs_col in df.columns and pred_col in df.columns

    rows = []
    for stage in stages_sorted:
        ds = df[df["Stage Name"] == stage]
        if has_yields:
            if has_area:
                nat = _aggregate_national_yields(ds)
            else:
                nat = (
                    ds.groupby("Harvest Year")
                    .agg({obs_col: "mean", pred_col: "mean"})
                    .reset_index()
                )
            nat = nat[nat[obs_col] != 0]
            if nat.empty or (metric_col == "R2" and len(nat) < 2):
                rows.append({"Stage Name": stage, "National": np.nan})
                continue
            if metric_col == "MAPE":
                val = ((nat[pred_col] - nat[obs_col]).abs() / nat[obs_col] * 100).mean()
            elif metric_col == "RMSE":
                val = float(np.sqrt(((nat[pred_col] - nat[obs_col]) ** 2).mean()))
            elif metric_col == "RRMSE":
                obs_mean = float(nat[obs_col].mean())
                rmse = float(np.sqrt(((nat[pred_col] - nat[obs_col]) ** 2).mean()))
                val = (100.0 * rmse / obs_mean) if obs_mean else np.nan
            elif metric_col == "R2":
                from sklearn.metrics import r2_score
                val = r2_score(nat[obs_col], nat[pred_col])
            else:
                val = ds[metric_col].mean() if metric_col in ds.columns else np.nan
            rows.append({"Stage Name": stage, "National": val})
        elif has_area:
            stats = ds.groupby("Region").agg(
                val=(metric_col, "mean"),
                area=("Area (ha)", "mean"),
            ).dropna()
            if stats.empty or stats["area"].sum() == 0:
                rows.append({"Stage Name": stage, "National": ds[metric_col].mean()})
            else:
                weighted = (stats["val"] * stats["area"]).sum() / stats["area"].sum()
                rows.append({"Stage Name": stage, "National": weighted})
        else:
            rows.append({"Stage Name": stage, "National": ds[metric_col].mean()})
    return pd.DataFrame(rows)


def _plot_metric_progression(df, stages_sorted, metric_col, ylabel, title,
                             country, crop, model, dir_out, fname,
                             prod_pct, has_area, df_for_national=None):
    """Generic progression plot for any per-region metric across time steps.

    ``df_for_national`` lets callers supply a raw-yield dataframe even when
    ``df`` is a pre-aggregated metric frame (RMSE, R²) — so the National line
    is computed on production-aggregated yields rather than on the area-
    weighted average of per-region scores.
    """
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401

    region_vals = _compute_region_metric(df, stages_sorted, metric_col)

    excluded = set()
    if metric_col == "MAPE":
        median_by_region = region_vals.groupby("Region")[metric_col].median()
        keep_regions = set(median_by_region[median_by_region <= 100].index)
        excluded = set(region_vals["Region"].unique()) - keep_regions
        if excluded:
            logger.info(
                f"Progression: excluding {len(excluded)} regions with median "
                f"{metric_col} > 100%: {sorted(excluded)}"
            )
        region_vals = region_vals[region_vals["Region"].isin(keep_regions)]

    df_nat_src = df_for_national if df_for_national is not None else df
    if excluded and "Region" in df_nat_src.columns:
        df_nat_src = df_nat_src[~df_nat_src["Region"].isin(excluded)]
    df_national = _compute_national_metric(df_nat_src, stages_sorted, metric_col, has_area)

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(10, 6))

        regions = sorted(region_vals["Region"].unique(),
                         key=lambda r: prod_pct.get(r, 0), reverse=True)
        n_regions = len(regions)

        if n_regions <= 20:
            cmap = plt.cm.get_cmap("tab20", max(n_regions, 1))
        else:
            import matplotlib.colors as mcolors
            colors_b = plt.cm.tab20b(np.linspace(0, 1, 20))
            colors_c = plt.cm.tab20c(np.linspace(0, 1, 20))
            cmap = mcolors.ListedColormap(np.vstack([colors_b, colors_c]))

        from .viz.diagnostics import is_production_share_shown
        _show_pct = is_production_share_shown()
        markers = ["o", "s", "D", "^", "v", "<", ">", "p", "h", "X", "*", "P"]
        for i, region in enumerate(regions):
            rdf = region_vals[region_vals["Region"] == region]
            rdf = rdf.set_index("Stage Name").reindex(stages_sorted)
            rlabel = (f"{region} ({prod_pct[region]:.1f}%)"
                      if (_show_pct and region in prod_pct) else region)
            ax.plot(stages_sorted, rdf[metric_col].values, color=cmap(i),
                    alpha=0.65, linewidth=1.8, marker=markers[i % len(markers)],
                    markersize=5, label=rlabel)

        df_national = df_national.set_index("Stage Name").reindex(stages_sorted)
        nat_label = "National (area-weighted)" if has_area else "National (mean)"
        if excluded:
            nat_label = f"{nat_label}, excl. {len(excluded)} outlier region(s)"
        ax.plot(stages_sorted, df_national["National"].values,
                color="black", linewidth=3, marker="o", markersize=7,
                label=nat_label, zorder=10)

        friendly_labels = [friendly_stage_label(s) for s in stages_sorted]
        ax.set_xticks(range(len(stages_sorted)))
        ax.set_xticklabels(friendly_labels, rotation=45, ha="right", fontsize=8)

        # Dashed vertical line at the boundary between pre-season and in-season/normal
        n_pre = sum(1 for s in stages_sorted if s.startswith("Pre-Season"))
        if 0 < n_pre < len(stages_sorted):
            ax.axvline(x=n_pre - 0.5, color="gray", linestyle="--", linewidth=1.2, zorder=5)
            ax.text(n_pre - 0.5, ax.get_ylim()[1] * 0.97, " Start of planting",
                    fontsize=7, color="gray", ha="left", va="top")

        ax.set_xlabel("")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ncol = 2 if n_regions > 10 else 1
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=7, ncol=ncol)
        plt.tight_layout()

        os.makedirs(dir_out, exist_ok=True)
        fig.savefig(dir_out / fname, dpi=250, bbox_inches="tight")
        plt.close(fig)


def _plot_national_progression(df, stages_sorted, metric_col, ylabel, title,
                               dir_out, fname, has_area,
                               df_for_national=None, clip_zero=True):
    """National-only progression plot: one line + a gray ±1 std band.

    A decluttered companion to :func:`_plot_metric_progression`. Instead of
    one line per region, it draws only the national metric (from
    :func:`_compute_national_metric`) and shades ±1 standard deviation of the
    per-region metric values across regions at each stage — the gray band
    conveys the regional spread the individual state lines used to show.

    ``clip_zero`` floors the lower band at 0 for non-negative metrics
    (MAPE/RMSE/RRMSE); pass False for R² (can be negative).
    """
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401

    region_vals = _compute_region_metric(df, stages_sorted, metric_col)
    # Mirror the MAPE>100 outlier exclusion of the full progression plot so
    # the national line + band match between the two figures.
    if metric_col == "MAPE":
        median_by_region = region_vals.groupby("Region")[metric_col].median()
        keep_regions = set(median_by_region[median_by_region <= 100].index)
        excluded = set(region_vals["Region"].unique()) - keep_regions
        region_vals = region_vals[region_vals["Region"].isin(keep_regions)]
    else:
        excluded = set()

    std_by_stage = (
        region_vals.groupby("Stage Name")[metric_col].std()
        .reindex(stages_sorted)
    )

    df_nat_src = df_for_national if df_for_national is not None else df
    if excluded and "Region" in df_nat_src.columns:
        df_nat_src = df_nat_src[~df_nat_src["Region"].isin(excluded)]
    df_national = (
        _compute_national_metric(df_nat_src, stages_sorted, metric_col, has_area)
        .set_index("Stage Name").reindex(stages_sorted)
    )

    nat = df_national["National"].to_numpy(dtype=float)
    std = std_by_stage.to_numpy(dtype=float)
    lower = nat - std
    upper = nat + std
    if clip_zero:
        lower = np.maximum(lower, 0.0)

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(10, 6))
        x = np.arange(len(stages_sorted))

        # Gray ±1 std band (only where both the value and std are finite).
        band_mask = np.isfinite(nat) & np.isfinite(std)
        if band_mask.any():
            ax.fill_between(
                x, lower, upper, where=band_mask, color="gray", alpha=0.25,
                linewidth=0, label="±1 std across regions",
            )
        ax.plot(x, nat, color="black", linewidth=3, marker="o", markersize=7,
                label="National", zorder=10)

        friendly_labels = [friendly_stage_label(s) for s in stages_sorted]
        ax.set_xticks(x)
        ax.set_xticklabels(friendly_labels, rotation=45, ha="right", fontsize=8)

        n_pre = sum(1 for s in stages_sorted if s.startswith("Pre-Season"))
        if 0 < n_pre < len(stages_sorted):
            ax.axvline(x=n_pre - 0.5, color="gray", linestyle="--",
                       linewidth=1.2, zorder=5)
            ax.text(n_pre - 0.5, ax.get_ylim()[1] * 0.97, " Start of planting",
                    fontsize=7, color="gray", ha="left", va="top")

        ax.set_xlabel("")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend(loc="best", fontsize=8)
        plt.tight_layout()

        os.makedirs(dir_out, exist_ok=True)
        fig.savefig(dir_out / fname, dpi=250, bbox_inches="tight")
        plt.close(fig)


def _plot_all_progressions(df, country, crop, model, dir_outlook, yield_units="Mg/ha"):
    """Plot MAPE, R², and RMSE progression across time steps."""
    from sklearn.metrics import r2_score

    obs_col = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"
    df = df.dropna(subset=[obs_col, pred_col])
    if df.empty or "Stage Name" not in df.columns:
        return

    df = df[df[obs_col] != 0].copy()
    df["MAPE"] = (df[pred_col] - df[obs_col]).abs() / df[obs_col] * 100
    df["RMSE_sq"] = (df[pred_col] - df[obs_col]) ** 2

    _stage_names = df["Stage Name"].dropna().unique()
    _planting = _infer_planting_month(_stage_names)
    stages_sorted = sorted(_stage_names, key=lambda s: _stage_sort_key(s, _planting))
    if len(stages_sorted) < 2:
        return

    has_area = "Area (ha)" in df.columns and df["Area (ha)"].notna().any()

    from .viz import diagnostics as diag
    prod_pct = diag.compute_production_pct(df, country)

    dir_progression = dir_outlook / "plots" / model / country / crop / "progression"
    dir_csvs_prog = dir_outlook / "csvs" / model / country / crop / "progression"
    os.makedirs(dir_csvs_prog, exist_ok=True)
    base_title = f"{country.title().replace('_', ' ')} {crop.title().replace('_', ' ')} ({model})"

    # MAPE
    _plot_metric_progression(
        df, stages_sorted, "MAPE", "MAPE (%)",
        f"MAPE Progression — {base_title}",
        country, crop, model, dir_progression,
        f"mape_progression_{country}_{crop}_{model}.png",
        prod_pct, has_area,
    )
    _plot_national_progression(
        df, stages_sorted, "MAPE", "MAPE (%)",
        f"National MAPE Progression — {base_title}",
        dir_progression,
        f"mape_progression_national_{country}_{crop}_{model}.png",
        has_area,
    )
    df[["Region", "Stage Name", "Harvest Year", "MAPE"]].to_csv(
        dir_csvs_prog / f"mape_progression_{country}_{crop}_{model}.csv", index=False)

    # RMSE — compute per (Stage Name, Region)
    rmse_data = []
    for stage in stages_sorted:
        for region in df["Region"].unique():
            mask = (df["Stage Name"] == stage) & (df["Region"] == region)
            ds = df[mask]
            if len(ds) >= 2:
                rmse = np.sqrt((ds["RMSE_sq"]).mean())
                rmse_data.append({"Stage Name": stage, "Region": region, "RMSE": rmse})
    if rmse_data:
        df_rmse = pd.DataFrame(rmse_data)
        # Merge multi-year-average area onto df_rmse for downstream consumers
        # of the saved CSV. National line itself is computed via df_for_national
        # below, not from this column.
        if has_area:
            area_map = df.groupby("Region")["Area (ha)"].mean()
            df_rmse = df_rmse.merge(area_map, on="Region", how="left")
        df["RMSE"] = np.sqrt(df["RMSE_sq"])
        _plot_metric_progression(
            df_rmse, stages_sorted, "RMSE", f"RMSE ({yield_units})",
            f"RMSE Progression — {base_title}",
            country, crop, model, dir_progression,
            f"rmse_progression_{country}_{crop}_{model}.png",
            prod_pct, has_area,
            df_for_national=df,
        )
        _plot_national_progression(
            df_rmse, stages_sorted, "RMSE", f"RMSE ({yield_units})",
            f"National RMSE Progression — {base_title}",
            dir_progression,
            f"rmse_progression_national_{country}_{crop}_{model}.png",
            has_area, df_for_national=df,
        )
        df_rmse.to_csv(dir_csvs_prog / f"rmse_progression_{country}_{crop}_{model}.csv", index=False)

    # R² — compute per (Stage Name, Region)
    r2_data = []
    for stage in stages_sorted:
        for region in df["Region"].unique():
            mask = (df["Stage Name"] == stage) & (df["Region"] == region)
            ds = df[mask]
            if len(ds) >= 2:
                try:
                    r2 = r2_score(ds[obs_col], ds[pred_col])
                    r2_data.append({"Stage Name": stage, "Region": region, "R2": r2})
                except ValueError:
                    pass
    if r2_data:
        df_r2 = pd.DataFrame(r2_data)
        if has_area:
            df_r2 = df_r2.merge(area_map, on="Region", how="left")
        _plot_metric_progression(
            df_r2, stages_sorted, "R2", "R²",
            f"R² Progression — {base_title}",
            country, crop, model, dir_progression,
            f"r2_progression_{country}_{crop}_{model}.png",
            prod_pct, has_area,
            df_for_national=df,
        )
        _plot_national_progression(
            df_r2, stages_sorted, "R2", "R²",
            f"National R² Progression — {base_title}",
            dir_progression,
            f"r2_progression_national_{country}_{crop}_{model}.png",
            has_area, df_for_national=df, clip_zero=False,
        )
        df_r2.to_csv(dir_csvs_prog / f"r2_progression_{country}_{crop}_{model}.csv", index=False)

    # RRMSE — compute per (Stage Name, Region)
    rrmse_data = []
    for stage in stages_sorted:
        for region in df["Region"].unique():
            mask = (df["Stage Name"] == stage) & (df["Region"] == region)
            ds = df[mask]
            if len(ds) >= 2:
                obs_mean = ds[obs_col].mean()
                if obs_mean and obs_mean > 0:
                    rmse = float(np.sqrt(ds["RMSE_sq"].mean()))
                    rrmse_data.append({
                        "Stage Name": stage, "Region": region,
                        "RRMSE": 100.0 * rmse / obs_mean,
                    })
    if rrmse_data:
        df_rrmse = pd.DataFrame(rrmse_data)
        if has_area:
            df_rrmse = df_rrmse.merge(area_map, on="Region", how="left")
        _plot_metric_progression(
            df_rrmse, stages_sorted, "RRMSE", "RRMSE (%)",
            f"RRMSE Progression — {base_title}",
            country, crop, model, dir_progression,
            f"rrmse_progression_{country}_{crop}_{model}.png",
            prod_pct, has_area,
            df_for_national=df,
        )
        _plot_national_progression(
            df_rrmse, stages_sorted, "RRMSE", "RRMSE (%)",
            f"National RRMSE Progression — {base_title}",
            dir_progression,
            f"rrmse_progression_national_{country}_{crop}_{model}.png",
            has_area, df_for_national=df,
        )
        df_rrmse.to_csv(dir_csvs_prog / f"rrmse_progression_{country}_{crop}_{model}.csv", index=False)


# ---------------------------------------------------------------------------
# FEATURE SELECTION BY CID TYPE ACROSS TIME STEPS
# ---------------------------------------------------------------------------

def _build_cid_type_map():
    """Build feature-name → CID-Type lookup from definitions."""
    from geocif.cid import definitions as di
    m = {}
    for d in [di.dict_indices, di.dict_ndvi, di.dict_gcvi, di.dict_esi4wk,
              di.dict_etref, di.dict_hindex, di.dict_aef, di.dict_fldas, di.dict_s2s,
              di.dict_fldas_engineered, di.dict_s2s_engineered]:
        for k, (typ, _) in d.items():
            m[k] = typ
    return m


def _feature_to_cid_type(feature_name, type_map):
    """Map a human-readable feature name back to its CID Type.

    Feature names in DB look like "WW Aug 1-Mar 31" or
    "MEAN_FLDAS_SoilMoist_tavg_LEAD0 Pre-Season LEAD0".
    Strip the stage/time suffix to match dictionary keys.
    """
    # Engineered / regional trend features
    if feature_name.startswith("t -") or feature_name.startswith("t-"):
        return "Regional Trends"
    if feature_name.startswith("median"):
        return "Regional Trends"
    if feature_name in ("lat", "lon"):
        return "Regional Trends"

    # Try exact match first
    if feature_name in type_map:
        return type_map[feature_name]

    # Strip stage suffix: "WW Aug 1-Mar 31" → "WW"
    # CID names don't contain month names, so split at first space followed
    # by a month abbreviation or "Pre-Season" or "In-Season".
    import re
    cleaned = re.split(
        r"\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|Pre-Season|In-Season)",
        feature_name
    )[0].strip()
    if cleaned in type_map:
        return type_map[cleaned]

    return "Regional Trends"


def _query_selected_features(db_path, table, model, experiment_name="outlook"):
    """Query Selected Features + Stage Name from DB, one row per unique stage."""
    import ast as _ast

    if not db_path.exists():
        return pd.DataFrame()

    con = sqlite3.connect(db_path)
    try:
        table_cols = pd.read_sql(f'PRAGMA table_info("{table}")', con)["name"].tolist()
        if "Selected Features" not in table_cols:
            return pd.DataFrame()

        df = pd.read_sql(
            f'SELECT DISTINCT "Stage Name", "Selected Features" '
            f'FROM "{table}" WHERE "Experiment Name" = ? AND "Model" = ?',
            con,
            params=(experiment_name, model),
        )
    except Exception:
        return pd.DataFrame()
    finally:
        con.close()

    if df.empty:
        return pd.DataFrame()

    # Parse JSON feature lists
    def _parse(s):
        try:
            return _ast.literal_eval(s) if isinstance(s, str) else (s if s else [])
        except (ValueError, SyntaxError):
            return []

    df["features"] = df["Selected Features"].apply(_parse)
    return df[["Stage Name", "features"]]


def _plot_feature_selection_by_stage(df_features, country, crop, model, dir_outlook):
    """Plot heatmap + stacked bar of CID Types selected at each time step.

    Args:
        df_features: DataFrame with "Stage Name" and "features" (list of str).
    """
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401

    if df_features.empty:
        return

    type_map = _build_cid_type_map()

    # Build stage → type → count matrix
    rows = []
    for _, row in df_features.iterrows():
        stage = row["Stage Name"]
        for feat in row["features"]:
            cid_type = _feature_to_cid_type(feat, type_map)
            rows.append({"Stage Name": stage, "CID Type": cid_type, "Feature": feat})

    if not rows:
        return

    df_long = pd.DataFrame(rows)

    # Sort stages chronologically (planting-month-aware for pre-season inits)
    _stage_names = df_long["Stage Name"].unique()
    _planting = _infer_planting_month(_stage_names)
    stages_sorted = sorted(_stage_names, key=lambda s: _stage_sort_key(s, _planting))
    friendly_labels = [friendly_stage_label(s) for s in stages_sorted]

    # Pivot: count of features per (stage, type)
    df_pivot = (
        df_long.groupby(["Stage Name", "CID Type"])
        .size()
        .reset_index(name="Count")
        .pivot_table(index="CID Type", columns="Stage Name", values="Count", fill_value=0)
    )
    # Reorder columns by stage sort
    df_pivot = df_pivot[[s for s in stages_sorted if s in df_pivot.columns]]

    # Determine pre-season boundary for vertical line
    n_pre = sum(1 for s in stages_sorted if s.startswith("Pre-Season"))

    dir_plots = dir_outlook / "plots" / model / country / crop / "feature_selection"
    dir_csvs = dir_outlook / "csvs" / model / country / crop / "feature_selection"
    os.makedirs(dir_plots, exist_ok=True)
    os.makedirs(dir_csvs, exist_ok=True)

    base_title = f"{country.title().replace('_', ' ')} {crop.title().replace('_', ' ')} ({model})"

    with plt.style.context(["science", "no-latex"]):
        # --- Heatmap ---
        import matplotlib.colors as mcolors

        fig, ax = plt.subplots(figsize=(max(10, len(stages_sorted) * 0.9), 6))

        # Mask zeros as white; colorbar starts at 1
        data = df_pivot.values.astype(float)
        masked = np.ma.masked_where(data == 0, data)
        vmax = max(data.max(), 1)
        cmap_heat = plt.cm.get_cmap("YlOrRd").copy()
        cmap_heat.set_bad(color="white")

        im = ax.imshow(masked, aspect="auto", cmap=cmap_heat, vmin=1, vmax=vmax,
                        interpolation="nearest")

        ax.set_xticks(range(len(stages_sorted)))
        ax.set_xticklabels(friendly_labels, rotation=45, ha="right", fontsize=8)
        ax.set_yticks(range(len(df_pivot.index)))
        ax.set_yticklabels(df_pivot.index, fontsize=8)
        ax.tick_params(axis="both", which="both", length=0)

        # Thin gridlines between cells
        for i in range(len(df_pivot.index) + 1):
            ax.axhline(y=i - 0.5, color="#e0e0e0", linewidth=0.5)
        for j in range(len(stages_sorted) + 1):
            ax.axvline(x=j - 0.5, color="#e0e0e0", linewidth=0.5)

        ax.set_title(f"Selected CID Types by Stage — {base_title}")

        # Annotate cells with count
        for i in range(len(df_pivot.index)):
            for j in range(len(stages_sorted)):
                val = data[i, j]
                if val > 0:
                    ax.text(j, i, str(int(val)), ha="center", va="center",
                            fontsize=7, color="white" if val > vmax / 2 else "black")

        if 0 < n_pre < len(stages_sorted):
            ax.axvline(x=n_pre - 0.5, color="gray", linestyle="--", linewidth=1.2)

        plt.colorbar(im, ax=ax, label="# features selected", shrink=0.8)
        plt.tight_layout()
        fig.savefig(dir_plots / f"feature_selection_heatmap_{country}_{crop}_{model}.png",
                    dpi=250, bbox_inches="tight")
        plt.close(fig)

        # --- Stacked bar ---
        fig, ax = plt.subplots(figsize=(max(10, len(stages_sorted) * 0.9), 6))
        cid_types = df_pivot.index.tolist()
        n_types = len(cid_types)
        cmap = plt.cm.get_cmap("tab20", max(n_types, 1))
        x = np.arange(len(stages_sorted))
        bottom = np.zeros(len(stages_sorted))

        for i, cid_type in enumerate(cid_types):
            vals = df_pivot.loc[cid_type].values
            ax.bar(x, vals, bottom=bottom, label=cid_type, color=cmap(i), width=0.8)
            bottom += vals

        ax.set_xticks(x)
        ax.set_xticklabels(friendly_labels, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("Number of features selected")
        ax.set_title(f"Feature Selection by CID Type — {base_title}")
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=7)

        if 0 < n_pre < len(stages_sorted):
            ax.axvline(x=n_pre - 0.5, color="gray", linestyle="--", linewidth=1.2)
            ax.text(n_pre - 0.5, ax.get_ylim()[1] * 0.97, " Start of planting",
                    fontsize=7, color="gray", ha="left", va="top")

        plt.tight_layout()
        fig.savefig(dir_plots / f"feature_selection_stacked_{country}_{crop}_{model}.png",
                    dpi=250, bbox_inches="tight")
        plt.close(fig)

    # --- CSV ---
    df_csv = (
        df_long.groupby(["Stage Name", "CID Type"])
        .agg(Count=("Feature", "size"), Features=("Feature", lambda x: "; ".join(sorted(x))))
        .reset_index()
    )
    # Sort by stage order
    stage_order = {s: i for i, s in enumerate(stages_sorted)}
    df_csv["_order"] = df_csv["Stage Name"].map(stage_order)
    df_csv = df_csv.sort_values(["_order", "CID Type"]).drop(columns="_order")
    df_csv.to_csv(dir_csvs / f"feature_selection_by_stage_{country}_{crop}_{model}.csv", index=False)

    logger.info(
        f"Feature selection plots saved: {dir_plots}, CSV: {dir_csvs}"
    )

    # --- Lead-time value heatmap (FLDAS + S2S leads, one row per lead) ---
    _plot_lead_time_value(df_long, stages_sorted, friendly_labels, n_pre,
                          base_title, country, crop, model, dir_plots, dir_csvs)

    # --- Variable-level heatmaps: aggregate leads, one row per variable ---
    # Separate heatmaps per source so the variable names (FLDAS soil moisture/
    # precip/temp/evap/TWS vs S2S t2m/tprate) stay legible.
    for source in ("FLDAS", "S2S"):
        _plot_variable_value_by_source(
            df_long, stages_sorted, friendly_labels, n_pre,
            base_title, country, crop, model, dir_plots, dir_csvs, source,
        )


def _render_feature_heatmap(
    df_pivot, row_labels, stages_sorted, friendly_labels, n_pre,
    *, title, cbar_label, output_path,
):
    """Render a (rows x stages) heatmap with the project's standard styling.

    Shared by ``_plot_lead_time_value`` and ``_plot_variable_value_by_source``.
    Zero-count cells render as white; non-zero cells are annotated with the
    integer count; a dashed vertical line separates pre-season from in-season.
    """
    import matplotlib.pyplot as plt

    with plt.style.context(["science", "no-latex"]):
        fig, ax = plt.subplots(figsize=(
            max(10, len(stages_sorted) * 0.9),
            max(3, len(row_labels) * 0.6),
        ))
        data = df_pivot.values.astype(float)
        masked = np.ma.masked_where(data == 0, data)
        vmax = max(data.max(), 1)
        cmap_heat = plt.cm.get_cmap("YlGnBu").copy()
        cmap_heat.set_bad(color="white")

        im = ax.imshow(masked, aspect="auto", cmap=cmap_heat,
                       vmin=1, vmax=vmax, interpolation="nearest")

        ax.set_xticks(range(len(df_pivot.columns)))
        ax.set_xticklabels(
            [friendly_labels[stages_sorted.index(s)] for s in df_pivot.columns],
            rotation=45, ha="right", fontsize=8,
        )
        ax.set_yticks(range(len(row_labels)))
        ax.set_yticklabels(row_labels, fontsize=8)
        ax.tick_params(axis="both", which="both", length=0)

        for i in range(len(row_labels) + 1):
            ax.axhline(y=i - 0.5, color="#e0e0e0", linewidth=0.5)
        for j in range(len(df_pivot.columns) + 1):
            ax.axvline(x=j - 0.5, color="#e0e0e0", linewidth=0.5)

        for i in range(len(row_labels)):
            for j in range(len(df_pivot.columns)):
                val = data[i, j]
                if val > 0:
                    ax.text(j, i, str(int(val)), ha="center", va="center",
                            fontsize=7,
                            color="white" if val > vmax / 2 else "black")

        if 0 < n_pre < len(df_pivot.columns):
            ax.axvline(x=n_pre - 0.5, color="gray", linestyle="--", linewidth=1.2)

        ax.set_title(title)
        plt.colorbar(im, ax=ax, label=cbar_label, shrink=0.8)
        plt.tight_layout()

        fig.savefig(output_path, dpi=250, bbox_inches="tight")
        plt.close(fig)


def _plot_lead_time_value(df_long, stages_sorted, friendly_labels, n_pre,
                          base_title, country, crop, model, dir_plots, dir_csvs):
    """Heatmap showing which FLDAS/S2S lead times are selected at each stage."""
    import re

    # Filter to FLDAS/S2S features only
    df_fc = df_long[df_long["CID Type"].isin(["FLDAS", "S2S"])].copy()
    if df_fc.empty:
        return

    # Extract lead number and source from feature name
    def _parse_lead(feat):
        match = re.search(r"(FLDAS|S2S).*LEAD(\d+)", feat)
        if match:
            return f"{match.group(1)} LEAD{match.group(2)}"
        return None

    df_fc["Lead"] = df_fc["Feature"].apply(_parse_lead)
    df_fc = df_fc.dropna(subset=["Lead"])
    if df_fc.empty:
        return

    df_pivot = (
        df_fc.groupby(["Stage Name", "Lead"])
        .size()
        .reset_index(name="Count")
        .pivot_table(index="Lead", columns="Stage Name", values="Count", fill_value=0)
    )
    df_pivot = df_pivot[[s for s in stages_sorted if s in df_pivot.columns]]

    # Sort leads: FLDAS LEAD0-5 then S2S LEAD1-6
    def _lead_sort(name):
        parts = name.split()
        src = 0 if parts[0] == "FLDAS" else 1
        lead_num = int(parts[1].replace("LEAD", ""))
        return (src, lead_num)

    sorted_leads = sorted(df_pivot.index, key=_lead_sort)
    df_pivot = df_pivot.loc[sorted_leads]

    _render_feature_heatmap(
        df_pivot, sorted_leads, stages_sorted, friendly_labels, n_pre,
        title=f"Forecast Lead Times Selected — {base_title}",
        cbar_label="# times selected",
        output_path=dir_plots / f"lead_time_heatmap_{country}_{crop}_{model}.png",
    )

    # CSV
    df_lead_csv = (
        df_fc.groupby(["Stage Name", "Lead"])
        .agg(Count=("Feature", "size"),
             Variables=("Feature", lambda x: "; ".join(sorted(set(x)))))
        .reset_index()
    )
    stage_order = {s: i for i, s in enumerate(stages_sorted)}
    df_lead_csv["_order"] = df_lead_csv["Stage Name"].map(stage_order)
    df_lead_csv = df_lead_csv.sort_values(["_order", "Lead"]).drop(columns="_order")
    df_lead_csv.to_csv(dir_csvs / f"lead_time_by_stage_{country}_{crop}_{model}.csv", index=False)


def _plot_variable_value_by_source(df_long, stages_sorted, friendly_labels, n_pre,
                                   base_title, country, crop, model,
                                   dir_plots, dir_csvs, source):
    """Heatmap: leads summed per variable, one row per variable, for one source.

    ``source`` is "FLDAS" or "S2S".  Reveals which physical variables (soil
    moisture / precip / temperature / evap / TWS for FLDAS; t2m / tprate
    for S2S) the model leans on as the season progresses, irrespective of
    which lead horizon supplied them.
    """
    import re

    df_src = df_long[df_long["CID Type"] == source].copy()
    if df_src.empty:
        return

    # Capture the variable name between the source tag and the LEAD suffix.
    var_re = re.compile(rf"{source}_(.+?)_LEAD\d+")

    def _parse_var(feat):
        m = var_re.search(feat)
        return m.group(1) if m else None

    df_src["Variable"] = df_src["Feature"].apply(_parse_var)
    df_src = df_src.dropna(subset=["Variable"])
    if df_src.empty:
        return

    df_pivot = (
        df_src.groupby(["Stage Name", "Variable"])
        .size()
        .reset_index(name="Count")
        .pivot_table(index="Variable", columns="Stage Name",
                     values="Count", fill_value=0)
    )
    df_pivot = df_pivot[[s for s in stages_sorted if s in df_pivot.columns]]
    df_pivot = df_pivot.sort_index()

    _render_feature_heatmap(
        df_pivot, list(df_pivot.index), stages_sorted, friendly_labels, n_pre,
        title=f"{source} Variables Selected (all leads aggregated) — {base_title}",
        cbar_label="# times selected (summed across leads)",
        output_path=dir_plots /
            f"variable_{source.lower()}_heatmap_{country}_{crop}_{model}.png",
    )

    # CSV: include which leads contributed, for traceability
    lead_re = re.compile(r"LEAD\d+")

    def _leads(features):
        leads = {lead_re.search(f).group() for f in features if lead_re.search(f)}
        return "; ".join(sorted(leads))

    df_var_csv = (
        df_src.groupby(["Stage Name", "Variable"])
        .agg(Count=("Feature", "size"), Leads=("Feature", _leads))
        .reset_index()
    )
    stage_order = {s: i for i, s in enumerate(stages_sorted)}
    df_var_csv["_order"] = df_var_csv["Stage Name"].map(stage_order)
    df_var_csv = df_var_csv.sort_values(["_order", "Variable"]).drop(columns="_order")
    df_var_csv.to_csv(
        dir_csvs / f"variable_{source.lower()}_by_stage_{country}_{crop}_{model}.csv",
        index=False,
    )


def _generate_diagnostics(df_pred_store, dg, dir_outlook, current_year=None,
                          dict_config=None, db_path=None, parser=None):
    """Generate scatter, MAPE bar chart, and MAPE map per (country, crop, model, stage).

    When multi-step results are present (multiple Stage Names), produces
    separate plots per stage, an aggregate, and a MAPE progression plot.
    """
    # Per-project yield-unit label for plots (Mg/ha default, QQ/ha for
    # wolayita, kg/ha for poppy). Threaded through to helpers that produce
    # user-facing labels.
    yield_units = (
        parser.get("ML", "yield_units", fallback="Mg/ha")
        if parser is not None else "Mg/ha"
    )

    # Optional trigger-evaluation outputs. Same gate for the per-model
    # plot+table (computed inside the loop below) and the cross-model
    # comparison panel emitted by _generate_model_comparison.
    make_trigger_plot = (
        parser.getboolean("ML", "make_trigger_plot", fallback=False)
        if parser is not None else False
    )
    trigger_threshold = (
        parser.getfloat("ML", "trigger_threshold", fallback=18.9)
        if parser is not None else 18.9
    )

    for (country, crop, model), df in df_pred_store.items():
        if df.empty:
            continue

        # Get admin_level for this country/crop
        admin_level = "admin_1"
        if dict_config:
            cfg = dict_config.get(f"{country}_{crop}", {})
            admin_level = cfg.get("admin_zone", "admin_1")

        # Check for multiple stages
        stages = df["Stage Name"].dropna().unique() if "Stage Name" in df.columns else []

        if len(stages) > 1:
            for stage_name in sorted(stages):
                df_stage = df[df["Stage Name"] == stage_name]
                _generate_diagnostics_for_stage(
                    df_stage, country, crop, model, dg, dir_outlook, stage_name,
                    forecast_year=current_year, admin_level=admin_level,
                    yield_units=yield_units,
                )
            _plot_all_progressions(df, country, crop, model, dir_outlook, yield_units=yield_units)
        else:
            # Single stage or no stages — generate once
            _generate_diagnostics_for_stage(
                df, country, crop, model, dg, dir_outlook,
                forecast_year=current_year, admin_level=admin_level,
                yield_units=yield_units,
            )

        # Feature selection by CID Type across stages
        if db_path is not None:
            table = f"{country}_{crop}"
            df_feat = _query_selected_features(db_path, table, model)
            if not df_feat.empty:
                _plot_feature_selection_by_stage(
                    df_feat, country, crop, model, dir_outlook
                )

        # Optional per-(country, crop, model) trigger-evaluation plot for
        # index-insurance threshold analysis. Gated by [ML] make_trigger_plot
        # (default off; computed once at function entry). Off for most
        # projects; on for wolayita and wolayita_dt.
        if make_trigger_plot:
            from .viz import diagnostics as diag
            dir_plots_tr = dir_outlook / "plots" / model / country / crop
            dir_csvs_tr = dir_outlook / "csvs" / model / country / crop
            os.makedirs(dir_plots_tr, exist_ok=True)
            os.makedirs(dir_csvs_tr, exist_ok=True)
            stem = f"trigger_eval_{country}_{crop}_{model}"
            confusion_df = diag.trigger_eval_plot(
                df,
                title=f"Trigger Evaluation — {country.title().replace('_', ' ')} "
                      f"{crop.title().replace('_', ' ')} ({model})",
                dir_out=dir_plots_tr,
                fname=f"{stem}.png",
                threshold=trigger_threshold,
                yield_units=yield_units,
            )
            if confusion_df is not None and not confusion_df.empty:
                confusion_df.to_csv(dir_csvs_tr / f"{stem}.csv", index=False)
                # Companion PNG of the same table, same gate.
                diag.trigger_eval_table_image(
                    confusion_df,
                    title=f"Trigger Evaluation — {country.title().replace('_', ' ')} "
                          f"{crop.title().replace('_', ' ')} ({model}) "
                          f"— confusion summary (threshold = {trigger_threshold:g} {yield_units})",
                    dir_out=dir_plots_tr,
                    fname=f"{stem}_table.png",
                )

    # Model comparison plots (only when multiple models)
    _generate_model_comparison(df_pred_store, dg, dir_outlook, yield_units=yield_units,
                               make_trigger_plot=make_trigger_plot,
                               trigger_threshold=trigger_threshold)

    # Cross-country comparison plots (only when multiple countries)
    _generate_cross_country_comparison(df_pred_store, dir_outlook)

    # Per-country breakpoint diagnostics (BEAST CP + segment-aware trend)
    if parser is not None:
        _generate_breakpoint_plots(df_pred_store, dir_outlook, parser)


def _generate_breakpoint_plots(df_pred_store, dir_outlook, parser):
    """Per-region observed-yield series with BEAST changepoint + segment-
    aware linear trend overlaid.  One figure per (country, crop).

    Loads observed yields from the per-country statistics CSV (full
    history from ``[DEFAULT] start_year``) — NOT from df_pred_store,
    which is limited to the LOOCV outlook window.  BEAST changepoint
    detection works better on longer series.

    Saved to ``outlook/plots/breakpoints/{country}/`` with sibling CSV
    in ``outlook/csvs/breakpoints/{country}/``.
    """
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    import scienceplots  # noqa: F401
    from geocif import utils as _ut
    from .ml import trend as _trend

    obs_col = "Yield (tn per ha)"  # stats-CSV column name

    country_crop_set = set()
    for (country, crop, _model) in df_pred_store.keys():
        if country == "pooled":
            continue
        country_crop_set.add((country, crop))
    if not country_crop_set:
        return

    dir_output = Path(parser.get("PATHS", "dir_output"))
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    method = parser.get("DEFAULT", "method", fallback="monthly_r")
    dir_out = dir_output / project_name

    cp_threshold = parser.getfloat("BEAST", "strong_cp_threshold", fallback=0.5)
    import ast as _ast
    tcp_minmax = _ast.literal_eval(
        parser.get("BEAST", "tcp_minmax", fallback="[0, 8]")
    )
    tseg_minlength = parser.getint("BEAST", "tseg_minlength", fallback=5)
    mcmc_seed = parser.getint("BEAST", "mcmc_seed", fallback=42)

    for (country, crop) in country_crop_set:
        f = _ut.statistics_file_path(dir_out, method, country, crop)
        if not f.exists():
            continue
        df = pd.read_csv(f, usecols=["Region", "Harvest Year", obs_col])
        df = df.dropna(subset=["Region", "Harvest Year", obs_col])
        if df.empty:
            continue
        series_by_region = {}
        for region, rdf in df.groupby("Region"):
            yr = (rdf.groupby("Harvest Year")[obs_col]
                  .mean().sort_index())
            yr = yr[yr > 0]
            if len(yr) >= 5:
                series_by_region[region] = yr
        if not series_by_region:
            continue

        results = {}
        for region, yr in series_by_region.items():
            try:
                intercept, slope, cp_used, n_used = _trend.segment_aware_trend(
                    yr.index.values.astype(float),
                    yr.values.astype(float),
                    cp_threshold=cp_threshold,
                    tcp_minmax=tcp_minmax,
                    tseg_minlength=tseg_minlength,
                    mcmc_seed=mcmc_seed,
                )
            except Exception:
                continue
            results[region] = {
                "yields": yr,
                "intercept": intercept,
                "slope": slope,
                "cp_used": cp_used,
                "n_used": n_used,
            }

        if not results:
            continue

        n = len(results)
        ncols = min(3, n)
        nrows = (n + ncols - 1) // ncols
        with plt.style.context(["science", "no-latex"]):
            fig, axes = plt.subplots(
                nrows, ncols,
                figsize=(4.5 * ncols, 3 * nrows),
                squeeze=False,
            )
            country_disp = country.title().replace('_', ' ')
            crop_disp = crop.title().replace('_', ' ')
            fig.suptitle(
                f"Yield breakpoints — {country_disp} {crop_disp}",
                fontsize=13, fontweight="bold",
            )
            regions_sorted = sorted(results.keys())
            for i, region in enumerate(regions_sorted):
                r = results[region]
                yr = r["yields"]
                ax = axes[i // ncols][i % ncols]
                ax.plot(
                    yr.index.astype(int), yr.values,
                    color="steelblue", linewidth=1.2, marker="o",
                    markersize=3, label="Observed",
                )
                if r["cp_used"] is not None:
                    x_fit = yr.index[yr.index >= r["cp_used"]].astype(int)
                    ax.axvline(
                        r["cp_used"], color="darkorange",
                        linestyle="--", linewidth=1.2,
                        label=f"CP {r['cp_used']}",
                    )
                else:
                    x_fit = yr.index.astype(int)
                if len(x_fit) >= 2:
                    trend_y = r["intercept"] + r["slope"] * x_fit
                    ax.plot(
                        x_fit, trend_y, color="firebrick",
                        linewidth=1.5,
                        label=f"Trend (slope={r['slope']:.3f})",
                    )
                ax.set_title(region, fontsize=10, fontweight="bold")
                ax.set_xlabel("Harvest Year", fontsize=8)
                ax.set_ylabel(obs_col, fontsize=8)
                ax.legend(fontsize=7, frameon=False)
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                ax.tick_params(axis='both', which='minor', length=0)

            for j in range(n, nrows * ncols):
                axes[j // ncols][j % ncols].axis("off")

            plt.tight_layout(rect=(0, 0, 1, 0.97))

            out_dir = dir_outlook / "plots" / "breakpoints" / country
            out_dir.mkdir(parents=True, exist_ok=True)
            fig.savefig(
                out_dir / f"breakpoints_{country}_{crop}.png",
                dpi=200, bbox_inches="tight",
            )
            plt.close(fig)

        cp_counts = {}
        for region, r in results.items():
            if r["cp_used"] is not None:
                cp_counts.setdefault(int(r["cp_used"]), []).append(region)

        if cp_counts:
            years_sorted = sorted(cp_counts.keys())
            counts = [len(cp_counts[y]) for y in years_sorted]
            with plt.style.context(["science", "no-latex"]):
                fig, ax = plt.subplots(
                    figsize=(max(8, len(years_sorted) * 0.5), 5)
                )
                bars = ax.bar(
                    [str(y) for y in years_sorted], counts,
                    color="steelblue",
                )
                for bar, y in zip(bars, years_sorted):
                    regions = cp_counts[y]
                    if len(regions) <= 4:
                        label = "\n".join(regions)
                    else:
                        label = "\n".join(regions[:3]) + f"\n+{len(regions)-3} more"
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.05,
                        label, ha="center", va="bottom", fontsize=7,
                        color="dimgray",
                    )
                ax.set_xlabel("Breakpoint year")
                ax.set_ylabel("Number of regions")
                ax.set_title(
                    f"Breakpoint year frequency — {country_disp} {crop_disp}",
                    fontsize=12, fontweight="bold",
                )
                ax.tick_params(axis='both', which='minor', length=0)
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                fig.savefig(
                    out_dir / f"breakpoints_count_{country}_{crop}.png",
                    dpi=200, bbox_inches="tight",
                )
                plt.close(fig)

        out_csv_dir = dir_outlook / "csvs" / "breakpoints" / country
        out_csv_dir.mkdir(parents=True, exist_ok=True)
        if cp_counts:
            count_rows = [
                {"country": country, "crop": crop, "cp_year": y,
                 "n_regions": len(cp_counts[y]),
                 "regions": ";".join(cp_counts[y])}
                for y in sorted(cp_counts.keys())
            ]
            pd.DataFrame(count_rows).to_csv(
                out_csv_dir / f"breakpoints_count_{country}_{crop}.csv",
                index=False,
            )
        rows = [
            {
                "country": country, "crop": crop, "region": region,
                "cp_used": r["cp_used"],
                "slope": r["slope"], "intercept": r["intercept"],
                "n_used": r["n_used"],
                "year_first": int(r["yields"].index.min()),
                "year_last": int(r["yields"].index.max()),
            }
            for region, r in results.items()
        ]
        pd.DataFrame(rows).to_csv(
            out_csv_dir / f"breakpoints_{country}_{crop}.csv", index=False,
        )


def _generate_cross_country_comparison(df_pred_store, dir_outlook):
    """Cross-country comparison: MAPE distribution KDE + national MAPE
    time series, one figure per (crop, model) when >=2 real countries
    are present in df_pred_store.
    """
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401

    obs_col = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"

    # Group by (crop, model) across countries; skip the synthetic
    # "pooled" entry.
    crop_model_countries = {}
    for (country, crop, model), df in df_pred_store.items():
        if country == "pooled":
            continue
        crop_model_countries.setdefault((crop, model), {})[country] = df

    dir_plots = dir_outlook / "plots" / "cross_country"
    dir_csvs = dir_outlook / "csvs" / "cross_country"

    _PALETTE = [
        (0.122, 0.467, 0.706, 1.0), (0.839, 0.153, 0.157, 1.0),
        (0.173, 0.627, 0.173, 1.0), (0.580, 0.404, 0.741, 1.0),
        (1.000, 0.498, 0.055, 1.0), (0.549, 0.337, 0.294, 1.0),
        (0.890, 0.467, 0.761, 1.0), (0.498, 0.498, 0.498, 1.0),
    ]

    for (crop, model), country_dfs in crop_model_countries.items():
        if len(country_dfs) < 2:
            continue
        countries_sorted = sorted(country_dfs.keys())
        country_colors = {
            c: _PALETTE[i % len(_PALETTE)]
            for i, c in enumerate(countries_sorted)
        }

        region_mape = {}
        nat_ts = {}
        for country, df in country_dfs.items():
            df = df.dropna(subset=[obs_col, pred_col])
            df = df[df[obs_col] != 0].copy()
            if df.empty:
                continue
            df["_ape"] = (df[pred_col] - df[obs_col]).abs() / df[obs_col] * 100

            r_mape = df.groupby("Region")["_ape"].mean().dropna()
            region_mape[country] = r_mape

            has_area = (
                "Area (ha)" in df.columns and df["Area (ha)"].notna().any()
            )
            if has_area:
                ry = (
                    df.groupby(["Region", "Harvest Year"])
                    .agg(ape=("_ape", "mean"), area=("Area (ha)", "mean"))
                    .reset_index()
                )
            else:
                ry = (
                    df.groupby(["Region", "Harvest Year"])
                    .agg(ape=("_ape", "mean"))
                    .reset_index()
                )
                ry["area"] = np.nan

            def _wmean(g, _has_area=has_area):
                if _has_area:
                    w = g["area"].fillna(0)
                    if w.sum() > 0:
                        return (g["ape"] * w).sum() / w.sum()
                return g["ape"].mean()

            nat = (
                ry.groupby("Harvest Year").apply(_wmean).sort_index()
            )
            if not nat.empty:
                nat_ts[country] = nat

        if not region_mape and not nat_ts:
            continue

        dir_plots.mkdir(parents=True, exist_ok=True)
        dir_csvs.mkdir(parents=True, exist_ok=True)

        if region_mape:
            with plt.style.context(["science", "no-latex"]):
                fig, ax = plt.subplots(figsize=(9, 5.5))
                from scipy.stats import gaussian_kde
                for country in countries_sorted:
                    if country not in region_mape:
                        continue
                    vals = region_mape[country].values
                    kde = gaussian_kde(vals)
                    x_min = max(0.0, float(np.nanmin(vals)) - 10)
                    x_max = float(np.nanmax(vals)) + 10
                    xs = np.linspace(x_min, x_max, 200)
                    ax.plot(
                        xs, kde(xs),
                        color=country_colors[country], linewidth=2,
                        label=f"{country.title().replace('_', ' ')} (n={len(vals)})",
                    )
                ax.set_xlabel("Per-region Mean Absolute Percentage Error (%)")
                ax.set_ylabel("Density")
                ax.set_title(
                    f"MAPE distribution by country — {crop} ({model})",
                    fontsize=11, fontweight="bold",
                )
                ax.legend(title="Country", fontsize=8, frameon=False)
                plt.tight_layout()
                fig.savefig(
                    dir_plots / f"mape_kde_{crop}_{model}.png",
                    dpi=250, bbox_inches="tight",
                )
                plt.close(fig)

            pd.concat(
                {c: s.rename("MAPE") for c, s in region_mape.items()},
                names=["Country", "Region"],
            ).reset_index().to_csv(
                dir_csvs / f"mape_kde_{crop}_{model}.csv", index=False,
            )

        if nat_ts:
            with plt.style.context(["science", "no-latex"]):
                fig, ax = plt.subplots(figsize=(11, 5.5))
                for country in countries_sorted:
                    if country not in nat_ts:
                        continue
                    s = nat_ts[country]
                    ax.plot(
                        s.index.astype(int), s.values,
                        color=country_colors[country], linewidth=2,
                        marker="o", markersize=4,
                        label=country.title().replace('_', ' '),
                    )
                ax.set_xlabel("Harvest Year")
                ax.set_ylabel("National Mean Absolute Percentage Error (%, area-weighted)")
                ax.set_title(
                    f"National MAPE over time — {crop} ({model})",
                    fontsize=11, fontweight="bold",
                )
                ax.legend(title="Country", fontsize=8, frameon=False)
                all_years = sorted({
                    int(y) for s in nat_ts.values() for y in s.index
                })
                ax.set_xticks(all_years)
                ax.set_xticklabels([str(y) for y in all_years],
                                   rotation=45, ha='right')
                ax.tick_params(axis='x', length=0)
                plt.tight_layout()
                fig.savefig(
                    dir_plots / f"national_mape_timeseries_{crop}_{model}.png",
                    dpi=250, bbox_inches="tight",
                )
                plt.close(fig)

            pd.DataFrame(nat_ts).sort_index().to_csv(
                dir_csvs / f"national_mape_timeseries_{crop}_{model}.csv",
            )


def _generate_model_comparison(df_pred_store, dg, dir_outlook, yield_units="Mg/ha",
                                make_trigger_plot=False, trigger_threshold=18.9):
    """Compare model performance when multiple models are available.

    Produces grouped bar charts of MAPE, RMSE, and R² by region and by year,
    plus a choropleth map showing which model has the lowest MAPE per region.
    Saved to ``outlook/plots/model_comparison/{country}/``.

    When ``make_trigger_plot`` is True, also produces a 2×2 panel comparing
    models on the trigger-evaluation metrics (Missed payout %, False payout %,
    Overall accuracy %, RMSE in ``yield_units``) using ``trigger_threshold``
    on both axes.
    """
    import matplotlib.pyplot as plt
    import scienceplots  # noqa: F401
    from sklearn.metrics import r2_score
    from .viz import diagnostics as diag

    obs_col = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"

    # Group by (country, crop) across models
    country_crop_models = {}
    for (country, crop, model), df in df_pred_store.items():
        key = (country, crop)
        if key not in country_crop_models:
            country_crop_models[key] = {}
        country_crop_models[key][model] = df

    for (country, crop), model_dfs in country_crop_models.items():
        if len(model_dfs) < 2:
            continue

        dir_comp = dir_outlook / "plots" / "model_comparison" / country
        dir_csvs_comp = dir_outlook / "csvs" / "model_comparison" / country
        os.makedirs(dir_comp, exist_ok=True)
        os.makedirs(dir_csvs_comp, exist_ok=True)

        # Build metrics per model × region and model × year
        rows_region = []
        rows_year = []
        for model, df in model_dfs.items():
            df = df.dropna(subset=[obs_col, pred_col])
            if df.empty:
                continue
            df = df[df[obs_col] != 0].copy()
            df["MAPE"] = (df[pred_col] - df[obs_col]).abs() / df[obs_col] * 100
            df["SE"] = (df[pred_col] - df[obs_col]) ** 2

            # By region
            for region, rdf in df.groupby("Region"):
                if len(rdf) < 2:
                    continue
                try:
                    r2 = r2_score(rdf[obs_col], rdf[pred_col])
                except ValueError:
                    r2 = np.nan
                _obs_mean = rdf[obs_col].mean()
                _rmse = float(np.sqrt(rdf["SE"].mean()))
                _rrmse = (100.0 * _rmse / _obs_mean) if _obs_mean else np.nan
                rows_region.append({
                    "Model": model, "Region": region,
                    "MAPE": rdf["MAPE"].mean(),
                    "RMSE": _rmse,
                    "RRMSE": _rrmse,
                    "R2": r2,
                })

            # By year
            for year, ydf in df.groupby("Harvest Year"):
                if len(ydf) < 2:
                    continue
                try:
                    r2 = r2_score(ydf[obs_col], ydf[pred_col])
                except ValueError:
                    r2 = np.nan
                _yobs_mean = ydf[obs_col].mean()
                _yrmse = float(np.sqrt(ydf["SE"].mean()))
                _yrrmse = (100.0 * _yrmse / _yobs_mean) if _yobs_mean else np.nan
                rows_year.append({
                    "Model": model, "Harvest Year": year,
                    "MAPE": ydf["MAPE"].mean(),
                    "RRMSE": _yrrmse,
                    "RMSE": np.sqrt(ydf["SE"].mean()),
                    "R2": r2,
                })

        if not rows_region:
            continue

        df_region = pd.DataFrame(rows_region)
        df_year = pd.DataFrame(rows_year)
        df_region.to_csv(dir_csvs_comp / f"metrics_by_region_{country}_{crop}.csv", index=False)
        df_year.to_csv(dir_csvs_comp / f"metrics_by_year_{country}_{crop}.csv", index=False)
        base_title = f"{country.title().replace('_', ' ')} {crop.title().replace('_', ' ')}"

        # ------------------------------------------------------------------
        # Error-vs-area scatter: per-region model error against the region's
        # share of national cropland area. Answers "how well do we predict
        # the regions that MATTER most?" Latest stage only (matches
        # yield_outlook map default of use_latest_stage=True). Panels: one
        # per model. Area weight = mean of last-5-years of non-null Area (ha).
        # ------------------------------------------------------------------
        # Compute per-region last-5-year mean area from any model_df (Area
        # column is a target-side attribute, so it's identical across models).
        _sample_df = next(iter(model_dfs.values()))
        _area_cols_needed = {"Region", "Harvest Year", "Area (ha)"}
        if _area_cols_needed.issubset(_sample_df.columns):
            # Include observed yield so we can compute production =
            # area * yield on the same 5-year slice. Both columns must
            # be non-null for a row to count.
            _cols_for_prod = ["Region", "Harvest Year", "Area (ha)", obs_col]
            _area_src = (
                _sample_df[_cols_for_prod]
                .dropna(subset=["Area (ha)", obs_col])
                .query("`Area (ha)` > 0")
                .drop_duplicates(subset=["Region", "Harvest Year"])
                .sort_values("Harvest Year", ascending=False)
            )
            _recent = _area_src.groupby("Region", group_keys=False).head(5)
            _area_5yr = (
                _recent.groupby("Region")["Area (ha)"].mean()
                .rename("area_5yr_mean_ha")
            )
            # Production per (region, year) = area * yield. Mean of the 5-year
            # slice gives an annualized-production stat comparable across
            # regions. Country total = sum across regions.
            _prod_rows = _recent.assign(
                _prod=lambda x: x["Area (ha)"] * x[obs_col]
            )
            _prod_5yr = (
                _prod_rows.groupby("Region")["_prod"].mean()
                .rename("production_5yr_mean_tons")
            )
            # Mean observed yield across the same 5-year slice.
            _yield_5yr = (
                _recent.groupby("Region")[obs_col].mean()
                .rename("obs_yield_5yr_mean")
            )
            _country_area_total = float(_area_5yr.sum()) if not _area_5yr.empty else 0.0
            _country_prod_total = float(_prod_5yr.sum()) if not _prod_5yr.empty else 0.0
            _area_pct = (
                100.0 * _area_5yr / _country_area_total
            ).rename("area_pct_of_country") if _country_area_total > 0 else None
            _prod_pct = (
                100.0 * _prod_5yr / _country_prod_total
            ).rename("production_pct_of_country") if _country_prod_total > 0 else None
        else:
            _area_pct = None
            _prod_pct = None
            _area_5yr = None
            _prod_5yr = None
            _yield_5yr = None
            logger.info(
                f"error_vs_area: skipping {country}/{crop} — no 'Area (ha)' "
                f"in df_pred_store (production stats CSV lacks area column)"
            )

        if _area_pct is not None and not _area_pct.empty:
            # Recompute per-region MAPE/RMSE using LATEST stage only (matches
            # map default). Reuses model_dfs but filters each to its own
            # last-stage rows. If no Stage Name column, uses all rows.
            _rows_area = []
            for _mdl, _mdf in model_dfs.items():
                _d = _mdf.dropna(subset=[obs_col, pred_col])
                _d = _d[_d[obs_col] != 0].copy()
                if _d.empty:
                    continue
                if "Stage Name" in _d.columns and _d["Stage Name"].notna().any():
                    _stages_sorted = sorted(_d["Stage Name"].dropna().unique())
                    _latest = _stages_sorted[-1]
                    _d = _d[_d["Stage Name"] == _latest]
                for _reg, _rd in _d.groupby("Region"):
                    if len(_rd) < 2:
                        continue
                    _mape = float(
                        ((_rd[pred_col] - _rd[obs_col]).abs() / _rd[obs_col]).mean() * 100
                    )
                    _rmse = float(np.sqrt(((_rd[pred_col] - _rd[obs_col]) ** 2).mean()))
                    _apct = float(_area_pct.get(_reg, np.nan))
                    _area = float(_area_5yr.get(_reg, np.nan))
                    _prod = float(_prod_5yr.get(_reg, np.nan)) if _prod_5yr is not None else np.nan
                    _ppct = float(_prod_pct.get(_reg, np.nan)) if _prod_pct is not None else np.nan
                    _yield_mean = float(_yield_5yr.get(_reg, np.nan)) if _yield_5yr is not None else np.nan
                    if not np.isnan(_apct):
                        _rows_area.append({
                            "Region": _reg, "Model": _mdl,
                            "area_5yr_mean_ha": _area,
                            "area_pct_of_country": _apct,
                            "production_5yr_mean_tons": _prod,
                            "production_pct_of_country": _ppct,
                            "obs_yield_5yr_mean": _yield_mean,
                            "MAPE": _mape, "RMSE": _rmse,
                            "n_years_used": int(len(_rd)),
                        })
            if _rows_area:
                _df_area = pd.DataFrame(_rows_area).sort_values(
                    ["Model", "area_pct_of_country"], ascending=[True, False]
                )
                _df_area.to_csv(
                    dir_csvs_comp / f"error_vs_area_{country}_{crop}.csv",
                    index=False,
                )
                # Model column order: baselines (null, trend) on the LEFT, then
                # the ML models grouped on the right.
                _all_models = sorted(_df_area["Model"].unique())
                _models_ordered = [m for m in _all_models if m in ("null", "trend")] + [
                    m for m in _all_models if m not in ("null", "trend")
                ]
                _n_models = len(_models_ordered)
                # Local palette — can't reference the later _MODEL_COLORS
                # definition from here because Python's function-scope name
                # resolution treats it as local (UnboundLocalError).
                _EV_PALETTE = [
                    (0.122, 0.467, 0.706, 1.0),  # steel blue
                    (0.839, 0.153, 0.157, 1.0),  # brick red
                    (0.173, 0.627, 0.173, 1.0),  # forest green
                    (0.580, 0.404, 0.741, 1.0),  # muted purple
                    (1.000, 0.498, 0.055, 1.0),  # orange
                    (0.549, 0.337, 0.294, 1.0),  # brown
                    (0.890, 0.467, 0.761, 1.0),  # pink
                    (0.498, 0.498, 0.498, 1.0),  # grey
                ]
                # Key colors off the SORTED model list so each model keeps a
                # stable color regardless of the (baseline-first) column order.
                _ev_colors = {
                    m: _EV_PALETTE[i % len(_EV_PALETTE)]
                    for i, m in enumerate(_all_models)
                }
                # Per-region error diagnostic. ONE figure PER (metric,
                # regional-scale attribute): each row of the old combined grid
                # is now its own standalone plot (1 × N-models). Columns are
                # per-model panels sharing Y and X. No Pearson r annotations
                # (removed per user request 2026-07-04).
                from .viz.diagnostics import is_production_share_shown
                _row_dims = [
                    ("area_pct_of_country", "Region % of country area"),
                    ("obs_yield_5yr_mean", f"Mean obs yield ({yield_units})"),
                ]
                if is_production_share_shown():
                    _row_dims.insert(
                        1,
                        ("production_pct_of_country", "Region % of country production"),
                    )
                # Filter out rows whose column is missing / all-NaN
                _row_dims = [
                    (c, l) for (c, l) in _row_dims
                    if c in _df_area.columns and _df_area[c].notna().any()
                ]
                _metrics = [
                    ("MAPE", "MAPE (%)"),
                    ("RMSE", f"RMSE ({yield_units})"),
                ]
                for _metric, _ylabel in _metrics:
                    _global_mean = float(_df_area[_metric].mean())
                    for _xcol, _xlabel in _row_dims:
                        _fname = f"region_error_{_metric}_{_xcol}_{country}_{crop}.png"
                        with plt.style.context(["science", "no-latex"]):
                            fig, axes = plt.subplots(
                                1, _n_models,
                                figsize=(max(10.0, 3.0 * _n_models), 3.8),
                                sharey=True, sharex=True,
                                squeeze=False,
                            )
                            for _ci, _mdl in enumerate(_models_ordered):
                                _ax = axes[0, _ci]
                                _sub = _df_area[_df_area["Model"] == _mdl].dropna(subset=[_xcol])
                                _color = _ev_colors.get(_mdl, "steelblue")
                                if not _sub.empty:
                                    _ax.scatter(
                                        _sub[_xcol], _sub[_metric],
                                        s=45, color=_color, edgecolor="black",
                                        linewidth=0.4, alpha=0.85, zorder=3,
                                    )
                                    for _, _r in _sub.iterrows():
                                        _ax.annotate(
                                            _r["Region"][:12],
                                            xy=(_r[_xcol], _r[_metric]),
                                            xytext=(3, 2), textcoords="offset points",
                                            fontsize=6.5, alpha=0.75,
                                        )
                                _ax.axhline(
                                    _global_mean, color="gray", linestyle="--",
                                    linewidth=0.8, alpha=0.7,
                                )
                                _ax.grid(True, linestyle="--", alpha=0.4)
                                _ax.set_title(_display_model_name(_mdl), fontsize=10)
                                _ax.set_xlabel(_xlabel)
                                if _ci == 0:
                                    _ax.set_ylabel(_ylabel)
                            fig.suptitle(
                                f"Per-region {_metric} vs {_xlabel} — {base_title} (latest stage)",
                                fontweight="bold", fontsize=11,
                            )
                            plt.tight_layout()
                            fig.savefig(
                                dir_comp / _fname,
                                dpi=250, bbox_inches="tight",
                            )
                            plt.close(fig)

        # Consistent model colors across all plots
        all_models_sorted = sorted(df_region["Model"].unique())
        # Hand-picked high-contrast palette for small model counts
        _FIXED_PALETTE = [
            (0.122, 0.467, 0.706, 1.0),  # steel blue
            (0.839, 0.153, 0.157, 1.0),  # brick red
            (0.173, 0.627, 0.173, 1.0),  # forest green
            (0.580, 0.404, 0.741, 1.0),  # muted purple
            (1.000, 0.498, 0.055, 1.0),  # orange
            (0.549, 0.337, 0.294, 1.0),  # brown
            (0.890, 0.467, 0.761, 1.0),  # pink
            (0.498, 0.498, 0.498, 1.0),  # grey
        ]
        _MODEL_COLORS = {
            m: _FIXED_PALETTE[i % len(_FIXED_PALETTE)]
            for i, m in enumerate(all_models_sorted)
        }

        # Area share per region (reuse existing utility)
        first_df = next(iter(model_dfs.values()))
        area_pct = diag.compute_area_pct(first_df, country)


        with plt.style.context(["science", "no-latex"]):
            # By region: grouped bar for each metric
            for metric, ylabel in [("MAPE", "Mean Absolute Percentage Error (%)"), ("RMSE", f"RMSE ({yield_units})"), ("RRMSE", "RRMSE (%)"), ("R2", "R²")]:
                pivot = df_region.pivot_table(index="Region", columns="Model", values=metric)
                if pivot.empty:
                    continue
                # Sort ascending by area share so matplotlib's barh (row 0 at
                # bottom) renders the largest area at the TOP visually.
                if area_pct:
                    order = sorted(pivot.index, key=lambda r: area_pct.get(r, 0))
                    pivot = pivot.reindex(order)
                    pivot.index = [
                        f"{r} ({area_pct[r]:.1f}%)" if r in area_pct else r
                        for r in pivot.index
                    ]
                # Rename columns to include national metric
                # Use consistent model colors
                bar_colors = [_MODEL_COLORS.get(m, "steelblue") for m in pivot.columns]
                pivot.columns = [_display_model_name(m) for m in pivot.columns]
                fig, ax = plt.subplots(figsize=(10, max(4, len(pivot) * 0.5)))

                # Conditional cap: only clip + break when MAPE/RRMSE
                # exceeds the cap by a LARGE amount (>= 1.5x). Below
                # that, just draw bars naturally. Clip annotations only
                # fire when we actually cap.
                METRIC_CAP = 100.0
                metric_max = float(np.nanmax(pivot.values)) if not pivot.empty else 0.0
                do_cap = metric in ("MAPE", "RRMSE") and metric_max > METRIC_CAP * 1.5
                pivot_plot = pivot.clip(upper=METRIC_CAP) if do_cap else pivot
                pivot_plot.plot.barh(ax=ax, color=bar_colors)

                if do_cap:
                    # Annotate clipped bars with their actual values
                    for m_idx, container in enumerate(ax.containers):
                        for r_idx, patch in enumerate(container):
                            actual = pivot.iloc[r_idx, m_idx]
                            if pd.notna(actual) and actual > METRIC_CAP:
                                ax.annotate(
                                    f"{actual:.0f}→",
                                    xy=(METRIC_CAP,
                                        patch.get_y() + patch.get_height() / 2),
                                    xytext=(2, 0), textcoords="offset points",
                                    fontsize=7, fontweight="bold",
                                    color="#b53b3b",
                                    va="center", ha="left",
                                )
                    ax.set_xlim(0, METRIC_CAP + 10)
                    diag._draw_axis_break(ax, axis="x", position=METRIC_CAP)

                # (Winner-star markers removed per user request 2026-07-04.)

                # Per-model mean across regions (dashed vertical line, same
                # color as bars, numeric value annotated at the top edge).
                # Arithmetic mean of the plotted values — not area-weighted.
                y_top = ax.get_ylim()[1]
                for col, c in zip(pivot.columns, bar_colors):
                    m_mean = pivot[col].dropna().mean()
                    if pd.notna(m_mean):
                        # Keep the line on-axis when capping; annotation
                        # still shows the actual mean value.
                        line_x = min(m_mean, METRIC_CAP) if do_cap else m_mean
                        ax.axvline(line_x, color=c, linestyle="--",
                                   linewidth=1.2, alpha=0.8)
                        unit = "%" if metric in ("MAPE", "RRMSE") else ""
                        ax.annotate(
                            f"{m_mean:.1f}{unit}",
                            xy=(line_x, y_top),
                            xytext=(3, -3),
                            textcoords="offset points",
                            color=c, fontsize=8, ha="left", va="top",
                            rotation=90,
                            bbox=dict(
                                boxstyle="round,pad=0.2",
                                facecolor="white",
                                edgecolor="none",
                                alpha=0.7,
                            ),
                        )
                ax.set_xlabel(ylabel)
                ax.set_title(f"{ylabel} by Region — {base_title}", fontweight="bold")
                ax.legend(title="Model", fontsize=8)
                ax.tick_params(axis='y', which='minor', length=0)
                plt.tight_layout()
                fig.savefig(dir_comp / f"{metric.lower()}_by_region_{country}_{crop}.png",
                            dpi=250, bbox_inches="tight")
                plt.close(fig)

            # By year: grouped bar for each metric
            for metric, ylabel in [("MAPE", "Mean Absolute Percentage Error (%)"), ("RMSE", f"RMSE ({yield_units})"), ("RRMSE", "RRMSE (%)"), ("R2", "R²")]:
                if df_year.empty:
                    continue
                pivot = df_year.pivot_table(index="Harvest Year", columns="Model", values=metric)
                if pivot.empty:
                    continue
                bar_colors = [_MODEL_COLORS.get(m, "steelblue") for m in pivot.columns]
                pivot.columns = [_display_model_name(m) for m in pivot.columns]
                fig, ax = plt.subplots(figsize=(12, 5))

                # Conditional cap: only clip + break when an actual
                # MAPE/RRMSE value exceeds the cap by a LARGE amount.
                METRIC_CAP = 100.0
                metric_max = float(np.nanmax(pivot.values)) if not pivot.empty else 0.0
                do_cap = metric in ("MAPE", "RRMSE") and metric_max > METRIC_CAP * 1.5
                pivot_plot = pivot.clip(upper=METRIC_CAP) if do_cap else pivot
                pivot_plot.plot.bar(ax=ax, color=bar_colors)

                if do_cap:
                    for m_idx, container in enumerate(ax.containers):
                        for r_idx, patch in enumerate(container):
                            actual = pivot.iloc[r_idx, m_idx]
                            if pd.notna(actual) and actual > METRIC_CAP:
                                ax.annotate(
                                    f"{actual:.0f}",
                                    xy=(patch.get_x() + patch.get_width() / 2,
                                        METRIC_CAP + 1.5),
                                    rotation=90,
                                    fontsize=7, fontweight="bold",
                                    color="#b53b3b",
                                    ha="center", va="bottom",
                                )
                    ax.set_ylim(0, METRIC_CAP + 8)
                    diag._draw_axis_break(ax, axis="y", position=METRIC_CAP)

                # Per-model mean across years (dashed horizontal line, same
                # color as bars, numeric value annotated at the right edge).
                # Mirrors the per-model mean dashed VERTICAL line in the
                # "by Region" plot above — same statistic (arithmetic mean
                # of plotted values), different axis. Capping mirrors the
                # by-Region path: clamp the line to METRIC_CAP on-axis when
                # do_cap, but annotate the actual mean.
                x_right = ax.get_xlim()[1]
                for col, c in zip(pivot.columns, bar_colors):
                    m_mean = pivot[col].dropna().mean()
                    if pd.notna(m_mean):
                        line_y = min(m_mean, METRIC_CAP) if do_cap else m_mean
                        ax.axhline(line_y, color=c, linestyle="--",
                                   linewidth=1.2, alpha=0.8)
                        unit = "%" if metric in ("MAPE", "RRMSE") else ""
                        ax.annotate(
                            f"{m_mean:.1f}{unit}",
                            xy=(x_right, line_y),
                            xytext=(-3, 0),
                            textcoords="offset points",
                            color=c, fontsize=8, ha="right", va="center",
                            bbox=dict(
                                boxstyle="round,pad=0.2",
                                facecolor="white", edgecolor="none",
                                alpha=0.7,
                            ),
                        )
                ax.set_ylabel(ylabel)
                ax.set_title(f"{ylabel} by Year — {base_title}", fontweight="bold")
                ax.legend(title="Model", fontsize=8)
                ax.tick_params(axis='x', which='minor', length=0)
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                fig.savefig(dir_comp / f"{metric.lower()}_by_year_{country}_{crop}.png",
                            dpi=250, bbox_inches="tight")
                plt.close(fig)

            # rRMSEp summary bar chart (arxiv:2506.19046 Figure 3 style)
            # Fair comparison: restrict every model to the set of Harvest
            # Years covered by ALL models. BMA drops the first N years
            # (min_history_years warmup) so without this filter singles
            # would be averaged over more years than BMA — not apples-to-
            # apples. Intersection uses years that have >=1 valid obs+pred
            # pair per model.
            common_years = None
            for df_m in model_dfs.values():
                d = df_m.dropna(subset=[obs_col, pred_col])
                d = d[d[obs_col] != 0]
                if "Harvest Year" not in d.columns or d.empty:
                    continue
                years = set(d["Harvest Year"].dropna().unique())
                common_years = years if common_years is None else (common_years & years)
            rrmsep_rows = []
            for model, df_m in model_dfs.items():
                if common_years:
                    df_m = df_m[df_m["Harvest Year"].isin(common_years)]
                mean_r, std_r, n_y = _compute_rrmsep(df_m, obs_col, pred_col)
                if not np.isnan(mean_r):
                    rrmsep_rows.append({
                        "Model": model, "rrmsep_mean": mean_r,
                        "rrmsep_std": std_r, "n_years": n_y,
                    })
            if rrmsep_rows:
                df_rrmsep = pd.DataFrame(rrmsep_rows).sort_values("rrmsep_mean")
                fig, ax = plt.subplots(figsize=(max(6, len(df_rrmsep) * 1.0), 5))
                bar_colors = [
                    _MODEL_COLORS.get(m, "steelblue")
                    for m in df_rrmsep["Model"]
                ]
                ax.bar(
                    [_display_model_name(m) for m in df_rrmsep["Model"]],
                    df_rrmsep["rrmsep_mean"],
                    yerr=df_rrmsep["rrmsep_std"],
                    color=bar_colors, capsize=4,
                )
                ax.set_ylabel("rRMSEp (%, mean ± stdev over LOOCV years)")
                if common_years:
                    yr_sorted = sorted(int(y) for y in common_years if pd.notna(y))
                    yr_str = (
                        f"{yr_sorted[0]}-{yr_sorted[-1]} ({len(yr_sorted)} yrs)"
                        if len(yr_sorted) >= 2 else f"{yr_sorted[0]}"
                        if yr_sorted else "n/a"
                    )
                else:
                    yr_str = "n/a"
                ax.set_title(
                    f"rRMSEp — {base_title}\n"
                    f"(normalized by pooled mean obs yield; common years {yr_str})",
                    fontweight="bold",
                )
                plt.xticks(rotation=20, ha="right")
                plt.tight_layout()
                fig.savefig(
                    dir_comp / f"rrmsep_summary_{country}_{crop}.png",
                    dpi=250, bbox_inches="tight",
                )
                plt.close(fig)
                df_rrmsep.to_csv(
                    dir_csvs_comp / f"rrmsep_summary_{country}_{crop}.csv",
                    index=False,
                )

        # Best model per region map (qualitative choropleth)
        # For each region, pick the model with lowest MAPE
        best_model = (
            df_region.sort_values("MAPE")
            .drop_duplicates(subset=["Region"], keep="first")
            [["Region", "Model"]].copy()
        )
        best_model["Country Region"] = (
            country.lower().replace("_", " ") + " " + best_model["Region"].str.lower()
        )
        # Encode model as integer for qualitative map, using consistent colors
        model_to_id = {m: i + 1 for i, m in enumerate(all_models_sorted)}
        best_model["Best Model"] = best_model["Model"].map(model_to_id)
        # Legend: integer id → display name
        dict_lup = {
            mid: _display_model_name(m) for m, mid in model_to_id.items()
        }
        # Build color list matching model order (convert RGBA tuple to list for plot_map)
        model_cmap = [list(_MODEL_COLORS[m][:3]) for m in all_models_sorted]

        logger.info(
            f"Best model per region ({country} {crop}): "
            f"{best_model[['Region', 'Model', 'Best Model']].to_dict('records')}"
        )

        countries_display = [country.title().replace("_", " ")]
        dg_sub = dg[dg["ADM0_NAME"].isin(countries_display)].copy()

        plot.plot_map(
            dg_sub,
            best_model,
            dict_lup=dict_lup,
            merge_col="Country Region",
            name_country=countries_display,
            name_col="Best Model",
            dir_out=dir_comp,
            fname=f"best_model_map_{country}_{crop}.png",
            title=f"Best Model by Region (lowest MAPE) — {base_title}",
            label="Model",
            series="qualitative",
            cmap=model_cmap,
            annotate_regions=True,
            use_key=True,
        )

        # ------------------------------------------------------------------
        # Optional cross-model trigger-evaluation summary (gated).
        # 2×2 panel: Missed payout % / False payout % / Overall accuracy % /
        # RMSE (yield_units), one bar per model. Companion CSV saved next
        # to the PNG. Threshold from [ML] trigger_threshold (default 18.9).
        # ------------------------------------------------------------------
        if make_trigger_plot:
            trig_rows = []
            for m in all_models_sorted:
                mdf = model_dfs.get(m)
                if mdf is None:
                    continue
                mdf = mdf.dropna(subset=[obs_col, pred_col])
                if mdf.empty:
                    continue
                obs_low = mdf[obs_col] < trigger_threshold
                pred_low = mdf[pred_col] < trigger_threshold
                n = len(mdf)
                n_low = int(obs_low.sum())
                n_nolow = n - n_low
                missed = int((obs_low & ~pred_low).sum())
                false_pay = int((~obs_low & pred_low).sum())
                correct_pay = int((obs_low & pred_low).sum())
                correct_no = int((~obs_low & ~pred_low).sum())
                rmse = float(np.sqrt(((mdf[pred_col] - mdf[obs_col]) ** 2).mean()))
                trig_rows.append({
                    "Model": m,
                    "Missed payout %": round(100.0 * missed / n_low) if n_low else 0,
                    "False payout %": round(100.0 * false_pay / n_nolow) if n_nolow else 0,
                    "Overall accuracy %": round(100.0 * (correct_pay + correct_no) / n),
                    f"RMSE ({yield_units})": round(rmse, 2),
                })
            if trig_rows:
                df_trig = pd.DataFrame(trig_rows)
                df_trig.to_csv(
                    dir_csvs_comp / f"trigger_metrics_{country}_{crop}.csv",
                    index=False,
                )

                metric_cols = list(df_trig.columns[1:])  # skip "Model"
                fig, axes = plt.subplots(2, 2, figsize=(10, 7))
                bar_colors = [_MODEL_COLORS.get(m, "steelblue")
                              for m in df_trig["Model"]]
                display_names = [_display_model_name(m) for m in df_trig["Model"]]

                for ax, mcol in zip(axes.flatten(), metric_cols):
                    vals = df_trig[mcol].tolist()
                    ax.bar(display_names, vals, color=bar_colors)
                    ax.set_title(mcol, fontsize=10, fontweight="bold")
                    for i, v in enumerate(vals):
                        ax.text(
                            i, v, f"{v:g}",
                            ha="center", va="bottom", fontsize=8,
                        )
                    ax.tick_params(axis="x", rotation=20)
                    if "%" in mcol:
                        ax.set_ylim(0, max(105, max(vals) * 1.15 if vals else 100))
                    else:
                        ax.set_ylim(0, max(vals) * 1.20 if vals else 1)
                    ax.grid(True, axis="y", linestyle=":", alpha=0.4)

                fig.suptitle(
                    f"Trigger Metrics — {base_title} "
                    f"(threshold = {trigger_threshold:g} {yield_units})",
                    fontsize=11, fontweight="bold",
                )
                plt.tight_layout()
                fig.savefig(
                    dir_comp / f"trigger_metrics_{country}_{crop}.png",
                    dpi=200, bbox_inches="tight",
                )
                plt.close(fig)


def _generate_outlook_map(
    dg,
    df_outlook,
    countries,
    crop,
    model,
    current_year,
    n_years,
    aggregation,
    dir_out,
    stage_name="",
    annotate_regions=False,
    col="outlook_index",
    col_label=None,
    fname_extra="",
    label_extra="",
):
    """Generate a diverging choropleth map of the yield outlook index (or any anomaly column).

    ``fname_extra`` is appended before the ``.png`` extension so callers
    can distinguish variants of the same map (e.g. ``_filtered`` for the
    minimal-crop-area filtered anomaly map).

    ``label_extra`` is appended to the colorbar label (whether the label is the
    computed default or an explicit ``col_label``) so callers can tag a map
    (e.g. ``" — Season 1"``). Empty by default -> label is byte-for-byte
    unchanged.
    """
    # [ML] make_maps gate (default False): when figures are disabled this
    # renderer is a no-op, so ensemble/blend computation and the outlook CSV
    # still run but no PNG is drawn. Callers ignore the return value.
    if not _MAKE_MAPS:
        return

    # Fixed range: -40% to +40% departure (matching analysis.py anomaly maps)
    vmin = -40
    vmax = 40

    # Determine extend arrows based on actual data range (NaN values are
    # excluded regions; ignore them when picking arrows)
    data_min = df_outlook[col].min(skipna=True)
    data_max = df_outlook[col].max(skipna=True)
    if data_min < vmin and data_max > vmax:
        extend = "both"
    elif data_min < vmin:
        extend = "min"
    elif data_max > vmax:
        extend = "max"
    else:
        extend = "neither"

    countries_display = [c.title().replace("_", " ") for c in countries]
    stage_suffix = f"_{stage_name}" if stage_name else ""
    if len(countries) > 1:
        fname = f"yield_outlook_{len(countries)}_countries_{crop}_{model}{stage_suffix}_{current_year}{fname_extra}.png"
    else:
        fname = f"yield_outlook_{'_'.join(countries)}_{crop}_{model}{stage_suffix}_{current_year}{fname_extra}.png"

    friendly = friendly_stage_label(stage_name) if stage_name else ""
    stage_label = f", {friendly}" if friendly else ""
    label = col_label or f"% departure from {n_years}-year hindcast {aggregation}\n{crop.title()}, {current_year}{stage_label}"
    if label_extra:
        label = f"{label}{label_extra}"
    plot.plot_map(
        dg,
        df_outlook,
        merge_col="Country Region",
        name_country=countries_display,
        name_col=col,
        dir_out=dir_out,
        fname=fname,
        label=label,
        vmin=vmin,
        vmax=vmax,
        cmap=pal.colorbrewer.diverging.BrBG_11,
        series="diverging",
        annotate_regions=annotate_regions,
        loc_legend="lower left",
        extend=extend,
    )


def _summarize_fallbacks(dir_analysis):
    """Merge per-PID fallback CSVs (from Geocif._record_fallback) into a
    single summary + bar chart. Lands at:

      ``<dir_analysis>/fallbacks_summary.csv``  — full row-per-event log
      ``<dir_analysis>/fallbacks_summary_counts.csv`` — pivot by
          (model, country, crop, category)
      ``<dir_analysis>/fallbacks_summary.png`` — stacked bar chart

    A "fallback" is any execution where the configured CID-selection
    schema couldn't deliver and the model trained on something other
    than its intended feature set (placeholder use_cids, all CIDs,
    etc.). Categories include ``pearson_summary_missing``,
    ``auto_select_zero``, ``top_n_empty_survivors``,
    ``correlation_selection_empty``. Empty / missing fallback dir =
    no-op (no fallbacks happened — best case).
    """
    import glob
    from pathlib import Path as _Path

    fall_dir = _Path(dir_analysis) / "fallbacks"
    if not fall_dir.exists():
        logger.info("No fallbacks/ dir — no diagnostic to summarize")
        return

    files = sorted(glob.glob(str(fall_dir / "fallback_*.csv")))
    if not files:
        logger.info(f"No fallback CSVs under {fall_dir}")
        return

    frames = []
    for f in files:
        try:
            frames.append(pd.read_csv(f))
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"  fallback file unreadable: {f} ({exc})")
    if not frames:
        return
    df = pd.concat(frames, ignore_index=True, sort=False)
    if df.empty:
        return

    summary_path = _Path(dir_analysis) / "fallbacks_summary.csv"
    df.to_csv(summary_path, index=False)
    logger.info(
        f"Fallback summary: {len(df)} events across {len(files)} worker(s) "
        f"→ {summary_path}"
    )

    counts = (
        df.groupby(["model", "country", "crop", "category"])
        .size()
        .reset_index(name="n_events")
        .sort_values("n_events", ascending=False)
    )
    counts_path = _Path(dir_analysis) / "fallbacks_summary_counts.csv"
    counts.to_csv(counts_path, index=False)

    # Bar chart: x = (model, country, crop), stacked by category
    try:
        import matplotlib.pyplot as plt
        import scienceplots  # noqa: F401
        pivot = (
            df.assign(_key=lambda x: x["country"].astype(str) + "/" +
                                    x["crop"].astype(str) + " " +
                                    x["model"].astype(str))
              .groupby(["_key", "category"]).size()
              .unstack(fill_value=0)
        )
        pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]
        with plt.style.context(["science", "no-latex"]):
            fig, ax = plt.subplots(figsize=(max(8, len(pivot) * 0.7), 5))
            pivot.plot(kind="bar", stacked=True, ax=ax,
                       colormap="tab10", edgecolor="white", width=0.8)
            ax.set_ylabel("Fallback events")
            ax.set_xlabel("country/crop  model")
            ax.set_title(
                f"Fallback events by (country, crop, model) — "
                f"{int(pivot.values.sum())} total"
            )
            ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left",
                      fontsize=7, title="Category")
            plt.xticks(rotation=30, ha="right", fontsize=8)
            plt.tight_layout()
            fig.savefig(_Path(dir_analysis) / "fallbacks_summary.png",
                        dpi=200, bbox_inches="tight")
            plt.close(fig)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"Fallback chart render failed (non-fatal): {exc}")


def _plot_observed_yields(parser, dir_outlook):
    """Plot observed-yield time series per (country, crop) — one line per
    region — into ``${dir_outlook}/plots/observed_yields/*.png`` plus a
    companion CSV per combo.

    Runs at the start of yield_outlook before the ML phase so the user
    can sanity-check the training-data ground truth while training is
    still warming up.
    """
    import matplotlib.pyplot as plt
    from geocif.progress import pbar as _pbar

    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    dir_output_proj = Path(parser.get("PATHS", "dir_output")) / project_name

    out_png_dir = dir_outlook / "plots" / "observed_yields"
    out_csv_dir = dir_outlook / "csvs" / "observed_yields"
    out_png_dir.mkdir(parents=True, exist_ok=True)
    out_csv_dir.mkdir(parents=True, exist_ok=True)

    combos = []
    for country in countries:
        try:
            crops = ast.literal_eval(parser.get(country, "crops"))
        except Exception:
            continue
        method = parser.get(country, "method", fallback="monthly_r")
        for crop in crops:
            combos.append((country, crop, method))

    if not combos:
        logger.info("Observed yields: no (country, crop) combos found in config")
        return

    logger.info(
        f"Plotting observed yields for {len(combos)} (country, crop) combos "
        f"before ML phase — output under {out_png_dir}"
    )

    n_plotted = 0
    for country, crop, method in _pbar(combos, desc="Observed yields"):
        stats_file = ut.statistics_file_path(dir_output_proj, method, country, crop)
        if not stats_file.exists():
            logger.warning(
                f"Observed yields: stats file missing for {country} {crop} "
                f"at {stats_file}; skipping"
            )
            continue
        try:
            df = pd.read_csv(stats_file)
        except Exception as e:
            logger.warning(f"Observed yields: failed to read {stats_file}: {e}")
            continue

        needed = {"Region", "Harvest Year", "Yield (tn per ha)"}
        if not needed.issubset(df.columns):
            logger.warning(
                f"Observed yields: {country} {crop} stats CSV missing "
                f"columns {needed - set(df.columns)}; skipping"
            )
            continue

        df = df[["Region", "Harvest Year", "Yield (tn per ha)"]].dropna()
        if df.empty:
            continue
        df["Harvest Year"] = df["Harvest Year"].astype(int)

        # Collapse duplicates (region, year) -> mean, then pivot wide.
        df_plot = (
            df.groupby(["Region", "Harvest Year"], as_index=False)
              ["Yield (tn per ha)"].mean()
        )
        df_wide = df_plot.pivot(
            index="Harvest Year", columns="Region", values="Yield (tn per ha)"
        ).sort_index()

        logger.info(
            f"  {country} {crop}: {df_wide.shape[1]} regions, "
            f"{df_wide.index.min()}-{df_wide.index.max()}"
        )

        try:
            import scienceplots  # noqa: F401
            ctx = plt.style.context(["science", "no-latex"])
        except (ImportError, OSError):
            from contextlib import nullcontext
            ctx = nullcontext()

        with ctx:
            fig, ax = plt.subplots(figsize=(12, 6))
            df_wide.plot(
                ax=ax, marker="o", linewidth=1.2, markersize=3, alpha=0.85
            )
            ax.set_xlabel("Harvest Year")
            ax.set_ylabel("Yield (tn per ha)")
            ax.set_title(
                f"Observed yields — "
                f"{country.title().replace('_', ' ')} {crop.title()}",
                fontsize=11, fontweight="bold",
            )
            ax.legend(
                loc="center left", bbox_to_anchor=(1.0, 0.5),
                fontsize=8, frameon=False,
            )
            plt.tight_layout()
            fname_png = f"observed_yields_{country}_{crop}.png"
            fig.savefig(out_png_dir / fname_png, dpi=200, bbox_inches="tight")
            plt.close(fig)

        df_wide.to_csv(out_csv_dir / f"observed_yields_{country}_{crop}.csv")
        n_plotted += 1

    logger.info(
        f"Observed yields: plotted {n_plotted}/{len(combos)} combos to "
        f"{out_png_dir}"
    )


def run(path_config_files=None, current_year=None, n_years=None, aggregation=None,
        reuse_db=None, use_latest_stage=True, fdw_export=False, since_year=None,
        until_year=None, parser=None, logger_obj=None, outlook_db_name=None,
        analysis_dir=None):
    """Main entry point for yield outlook map generation.

    1. Override forecast_seasons to cover [since_year, ..., current_year]
    2. Run the ML pipeline via gc.execute_models()
    3. Query predictions from the database
    4. Compute outlook index per region (using n_years window)
    5. Generate diverging choropleth maps and CSV
    6. Optionally export FDW forecast CSV (fdw_export=True)

    Args:
        path_config_files: List of config file paths.
        current_year: Forecast year (default: this year).
        n_years: Number of historical years for the outlook index hindcast
            comparison window (default: config ``outlook_n_years`` or 10).
        aggregation: 'mean' or 'median' (default: config or 'mean').
        reuse_db: Path to existing outlook DB to skip ML and regenerate maps only.
        use_latest_stage: If True (default), use latest available stage per
            region+year. Handles mismatched stage names across years/countries.
        since_year: Start year for ML execution (default: config
            ``outlook_since_year`` or 2005).  Controls how far back the ML
            pipeline runs; ``n_years`` still controls the outlook index window.
        until_year: Upper bound (inclusive) of the forecast/eval loop
            (default: config ``outlook_until_year`` or ``current_year``).
            Set below ``current_year`` for a bounded hindcast assessment
            (e.g. ``since_year=2001, until_year=2020`` evaluates 2001..2020
            only).  The capped year also becomes the effective "live" year
            so outlook maps / CSV labels land on a year that has predictions.
        parser: Pre-configured ConfigParser (skips reading config files if provided).
        logger_obj: Pre-configured logger (skips setup if provided).
    """
    if parser is None or logger_obj is None:
        if path_config_files is None:
            path_config_files = [Path("../config/geocif.txt")]
        logger_obj, parser = log.setup_logger_parser(path_config_files)

    # Read config with defaults
    if n_years is None:
        n_years = parser.getint("ML", "outlook_n_years", fallback=10)
    if aggregation is None:
        aggregation = parser.get("ML", "outlook_aggregation", fallback="mean")
    if current_year is None:
        current_year = ar.utcnow().to("America/New_York").year
    if since_year is None:
        since_year = parser.getint("ML", "outlook_since_year", fallback=2005)
    # Upper bound (inclusive) of the forecast/eval loop. Default = current_year
    # (calendar year or the explicit current_year kwarg), so default behavior
    # is unchanged. Set [ML] outlook_until_year or pass until_year=YYYY to cap
    # a bounded hindcast (e.g. 2001-2020). The capped year also becomes the
    # effective "live" year (current_year) so the outlook maps / CSV labels /
    # outlook-index center land on a year that actually has predictions rather
    # than an empty calendar-current year.
    if until_year is None:
        until_year = parser.getint("ML", "outlook_until_year", fallback=current_year)
    current_year = until_year

    # [ML] make_maps (default False): gates ONLY the slow per-stage choropleth
    # maps — outlook / predicted-yield / obs-anomaly / ensemble / blend imagery
    # rendered via the shared _generate_outlook_map renderer (see _MAKE_MAPS).
    # Diagnostic PLOTS (forest, yield table, MAPE/RMSE boxes, scatter,
    # model-comparison, cross-country, breakpoint) and the pre-ML observed-yield
    # plots ALWAYS render regardless of this flag — they are cheap. When
    # make_maps is False the ML fit, the DB, and the outlook CSVs are still
    # written and only the slow choropleths are skipped, so plot-only reruns
    # (esp. reuse_db) are fast.
    global _MAKE_MAPS
    make_maps = parser.getboolean("ML", "make_maps", fallback=False)
    _MAKE_MAPS = make_maps

    # [ML] show_production_share (default True): process-wide toggle for whether
    # a region's production share is DISPLAYED on figures/tables/captions (the
    # "(X.Y%)" label suffix, "% of Production" column, etc.). Set False for
    # projects whose area stats don't match the model's region scheme (e.g.
    # poppy: "Southern" isn't split into the newer "South-Western" region).
    # Ordering-by-production is unaffected — only the shown value is hidden.
    from .viz import diagnostics as _diag_cfg
    _diag_cfg.set_show_production_share(
        _diag_cfg.show_production_share_from_parser(parser)
    )

    # [ML] outlook_maps_current_year_only (default False): when True, the
    # headline outlook-index + predicted-yield choropleths are rendered ONLY
    # for current_year (the live forecast), skipping every per-hindcast-year
    # map (2005..current_year-1). Obs-anomaly maps are already current-year
    # only. This turns a full maps pass (every year x combo, ~hours) into a
    # fast forecast-only pass (~minutes) — ideal for reuse_db map reruns.
    maps_current_year_only = parser.getboolean(
        "ML", "outlook_maps_current_year_only", fallback=False
    )

    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    experiment_name = parser.get("DEFAULT", "experiment_name", fallback="default")

    # Bind inputs/crops/models up front so they are always defined.  The
    # normal (else) path below overwrites all three from the gathered ML
    # inputs, but the reuse_db path skips gathering entirely — and the
    # optional report / report_lite blocks at the end of run() reference all
    # three.  Without these defaults, a reuse_db rerun raises
    # `UnboundLocalError: inputs` at the report step (crops/models are the
    # same-shaped fallbacks the report guards fall back to).  Values come
    # from the [DEFAULT] section, the same source gather_inputs resolves.
    inputs = []
    crops = ast.literal_eval(parser.get("DEFAULT", "crops", fallback="[]"))
    models = ast.literal_eval(parser.get("DEFAULT", "models", fallback="[]"))

    # Set up dir_outlook early so observed-yield plots can render BEFORE
    # the ML phase starts. (The same dir is reused later for the
    # post-training plots/maps; later setup at Step-3 is now skipped
    # because dir_outlook is already defined.)
    _project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    _dir_output_proj = Path(parser.get("PATHS", "dir_output")) / _project_name
    if analysis_dir:
        dir_outlook = Path(analysis_dir) / "outlook"
    else:
        _today_tag = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY_HH[h]mm")
        dir_outlook = _dir_output_proj / "ml" / "analysis" / _today_tag / "outlook"
    os.makedirs(dir_outlook, exist_ok=True)

    # Pre-ML observed-yield line plots (one PNG per country/crop, one
    # line per region) so the user can see the training-data ground
    # truth while the long-running ML pipeline starts.
    # Observed-yield line plots ALWAYS render (a plot, not a slow choropleth).
    try:
        _plot_observed_yields(parser, dir_outlook)
    except Exception as e:
        logger.warning(f"Observed-yields plotting failed (non-fatal): {e}")

    if reuse_db is not None:
        # ---- Skip ML, reuse existing DB ----
        reuse_path = Path(reuse_db)
        if not reuse_path.exists():
            logger.error(f"Reuse DB not found: {reuse_path}")
            return
        outlook_db = reuse_path.name
        logger.info(f"Reusing existing outlook DB: {reuse_path}")
    else:
        # ---- Step 1: Run ML pipeline for all years since since_year ----
        outlook_seasons = list(range(since_year, current_year + 1))
        originals = {}
        for country in countries:
            originals[country] = parser.get(country, "forecast_seasons")
            parser.set(country, "forecast_seasons", str(outlook_seasons))

        parser.set("DEFAULT", "experiment_name", "outlook")
        orig_db = parser.get("DEFAULT", "db")
        if outlook_db_name:
            outlook_db = outlook_db_name
        else:
            outlook_db = ar.utcnow().to("America/New_York").format("[outlook_]MM[_]DD[_]YYYY[_]HH[h]mm[.db]")
        parser.set("DEFAULT", "db", outlook_db)
        pool_countries_flag = parser.getboolean("ML", "pool_countries", fallback=False)
        if pool_countries_flag:
            inputs = gc.gather_pooled_inputs(parser)
        else:
            inputs = gc.gather_inputs(parser)

        # Crops and models are per-country in the config; read the union
        # that will actually run from the assembled input list (field
        # indices: [project_name, country(s), crop, season, model]).
        crops = sorted({row[2] for row in inputs})
        models = sorted({row[4] for row in inputs})

        # Resolve yield file per country
        default_yield = "hvstat_africa_data_v1.0.csv"
        if parser.has_option("DEFAULT", "production_statistics_file"):
            default_yield = parser.get("DEFAULT", "production_statistics_file")
        yield_files = {}
        for c in countries:
            ck = c.lower().replace(" ", "_")
            if parser.has_option(ck, "production_statistics_file"):
                yield_files[c] = parser.get(ck, "production_statistics_file")
            else:
                yield_files[c] = default_yield

        dir_output = Path(parser.get("PATHS", "dir_output"))
        dir_inputs = Path(parser.get("PATHS", "dir_inputs", fallback=parser.get("PATHS", "dir_input", fallback="")))
        params = [
            ("Config files", [str(p) for p in path_config_files] if path_config_files else ["(parser provided)"]),
            ("Input dir", str(dir_inputs)),
            ("Output dir", str(dir_output)),
            ("Countries", countries),
            ("Crops", crops),
            ("Models", models),
            ("Forecast year (live)", str(current_year)),
            ("Forecast loop",
                f"{since_year}..{current_year} "
                f"({current_year - since_year + 1} model runs)"),
            ("Anomaly comparison window", f"{n_years} years"),
            ("Aggregation", aggregation),
            ("Time steps", parser.get("ML", "run_time_steps", fallback="latest")),
            ("Pooled", str(pool_countries_flag)),
            ("FDW export", str(fdw_export)),
            ("DB", parser.get("DEFAULT", "db")),
            ("Total combinations", str(len(inputs))),
            ("Feature selection",
                parser.get("ML", "feature_selection", fallback="gOMP_high")),
            ("force_include FLDAS/S2S",
                str(parser.getboolean("ML", "force_include_forecast_cids", fallback=True))),
            ("save_model_blobs",
                str(parser.getboolean("ML", "save_model_blobs", fallback=False))),
            ("Training rows per fold",
                f"Harvest Year >= {parser.get('ML', 'training_start_year', fallback='').strip()}"
                if parser.get("ML", "training_start_year", fallback="").strip()
                else "Harvest Year > earliest year in data (drops boundary year only)"),
            ("Yield Trend feature",
                parser.get("ML", "use_yield_trend_as_feature", fallback="False").strip()
                or "False"),
            ("Trend All feature",
                str(parser.getboolean("ML", "use_trend_all_as_feature", fallback=True))),
            ("CI (estimate_ci)",
                str(parser.getboolean("ML", "estimate_ci", fallback=False))),
            ("XAI (do_xai)",
                str(parser.getboolean("ML", "do_xai", fallback=False))),
            ("Maps (make_maps)", str(make_maps)),
        ]

        # Claude narrative status — resolved at startup so the operator
        # sees whether the PDF report will include the AI-generated
        # narrative section before the run consumes time. Three gates:
        #   1. [ML] generate_report — master switch for the PDF
        #   2. ANTHROPIC_API_KEY env var — required for the API call
        #   3. anthropic SDK installed — required for the client
        # When all three pass, the model from [NARRATIVE] claude_model
        # is reported (default: claude-sonnet-4-6).
        _gen_report = parser.getboolean("ML", "generate_report", fallback=False)
        if not _gen_report:
            _narr_status = "No — [ML] generate_report = False"
        elif not os.environ.get("ANTHROPIC_API_KEY", ""):
            _narr_status = "No — ANTHROPIC_API_KEY not set"
        else:
            try:
                import anthropic  # noqa: F401
                _claude_model = "claude-sonnet-4-6"
                if parser.has_section("NARRATIVE"):
                    _claude_model = parser.get(
                        "NARRATIVE", "claude_model", fallback=_claude_model,
                    )
                _narr_status = f"Yes — model={_claude_model}"
            except ImportError:
                _narr_status = "No — anthropic SDK not installed"
        params.append(("Claude narrative", _narr_status))

        for c, yf in yield_files.items():
            params.append((f"  {c} yield file", yf))
        ut.display_run_summary("GeoCIF Yield Outlook", params, wait=10)

        run_time_steps = parser.get("ML", "run_time_steps", fallback="latest")
        loop_fn = gc.loop_execute_pooled if pool_countries_flag else None

        # Check use_cids for forecast type presence
        try:
            _use_cids = ast.literal_eval(parser.get("DEFAULT", "use_cids", fallback="['all']"))
        except (ValueError, SyntaxError):
            _use_cids = ["all"]
        from geocif.utils import is_forecast_only, has_forecast
        _has_forecast = has_forecast(_use_cids)
        _forecast_only = is_forecast_only(_use_cids)

        if run_time_steps == "auto":
            if _forecast_only:
                # Forecast-only: single pass covering pre-season + in-season
                parser.set("ML", "run_time_steps", "pre_season")
                logger.info("Auto mode (forecast-only): single pass pre-season + in-season")
                gc.execute_models(inputs, logger_obj, parser,
                                  loop_fn=loop_fn, desc="Forecast models (pre+in-season)")
            elif _has_forecast:
                # Has forecast types: pre-season pass + in-season pass
                parser.set("ML", "run_time_steps", "pre_season")
                logger.info("Auto mode — Pass 1: Pre-season (FLDAS/S2S leads only)")
                gc.execute_models(inputs, logger_obj, parser,
                                  loop_fn=loop_fn, desc="Pre-season models")

                parser.set("ML", "run_time_steps", "all")
                logger.info("Auto mode — Pass 2: In-season (all time steps)")
                gc.execute_models(inputs, logger_obj, parser,
                                  loop_fn=loop_fn, desc="In-season models")
            else:
                # No forecast types: skip pre-season, in-season only
                parser.set("ML", "run_time_steps", "all")
                logger.info("Auto mode — No forecast CIDs, in-season only")
                gc.execute_models(inputs, logger_obj, parser,
                                  loop_fn=loop_fn, desc="In-season models")

            # Restore
            parser.set("ML", "run_time_steps", "auto")
        elif run_time_steps == "lag_only":
            # Both passes like auto, with a worker-side flag forcing
            # feature selection to keep only lag-yield columns. Baseline
            # mode: no CID features at all.
            parser.set("ML", "lag_only_features", "True")
            parser.set("ML", "run_time_steps", "pre_season")
            logger.info("Lag-only mode — Pass 1: Pre-season")
            gc.execute_models(inputs, logger_obj, parser,
                              loop_fn=loop_fn, desc="Pre-season models (lag-only)")

            parser.set("ML", "run_time_steps", "all")
            logger.info("Lag-only mode — Pass 2: In-season")
            gc.execute_models(inputs, logger_obj, parser,
                              loop_fn=loop_fn, desc="In-season models (lag-only)")

            # Restore
            parser.set("ML", "run_time_steps", "lag_only")
            parser.set("ML", "lag_only_features", "False")
        else:
            gc.execute_models(inputs, logger_obj, parser, loop_fn=loop_fn)

        # Restore original config values
        for country, orig in originals.items():
            parser.set(country, "forecast_seasons", orig)
        parser.set("DEFAULT", "experiment_name", experiment_name)
        parser.set("DEFAULT", "db", orig_db)

    # ---- Step 2: Load shapefiles ----
    dg, dict_config = _load_shapefiles(parser)

    # ---- Step 3: Query DB, compute outlook, generate maps ----
    # `dir_outlook` was set up earlier (before the ML phase) so observed-
    # yield plots could render up-front; reusing the same path here so
    # all plots land in one timestamped run directory. `dir_output` and
    # `db_path` still need to be computed here.
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    dir_output = Path(parser.get("PATHS", "dir_output")) / project_name
    if reuse_db is not None:
        db_path = Path(reuse_db)
    else:
        db_path = dir_output / "ml" / "db" / outlook_db

    all_outlook_frames = []
    df_pred_store = {}  # keyed by (country, crop, model) for diagnostics

    # Build flat (country_crop, model) list so we can wrap the outer
    # post-training plotting loop in one progress bar. Without this, the
    # phase appears silent for many minutes after the ML bar hits 100%
    # while it does DB queries, shapefile renders, and dozens of plots
    # per combo.
    from geocif.progress import pbar as _pbar, pwrite as _pwrite
    plot_combos = [
        (cc, cfg["crops"], m, cfg)
        for cc, cfg in dict_config.items()
        for m in cfg["models"]
    ]
    logger.info(
        f"Post-training: generating plots + outputs for {len(plot_combos)} "
        f"(country_crop, model) combos (DB queries + shapefile renders + "
        f"per-stage maps + diagnostics) — first DB read may be slow as "
        f"SQLite catches up on the WAL"
    )

    _last_country_crop = None
    obs_baselines = {}
    for country_crop, crop, model, config in _pbar(plot_combos, desc="Plotting"):
        country = country_crop.replace(f"_{crop}", "")
        is_pooled = country == "pooled"
        models = config["models"]
        # Reload observed baselines only when country_crop changes
        if country_crop != _last_country_crop:
            obs_baselines = _load_observed_baselines(
                [country], crop, parser, current_year=current_year
            )
            _last_country_crop = country_crop

        if True:  # preserve original indentation of the per-model body
            _pwrite(f"[plot] {country} {crop} {model}: querying DB...")
            logger.info(f"Yield outlook: {country} {crop} {model}")

            df = _query_predictions(db_path, country_crop, model, experiment_name="outlook")
            if df.empty:
                logger.warning(f"No predictions found for {country} {crop} {model}")
                continue

            # Years to render maps for: every Harvest Year that has predictions.
            # Headline outlook + predicted-yield choropleths are produced per
            # year so hindcasts (e.g. 2024) get the same map treatment as the
            # live forecast year. Obs-anomaly maps stay current-year-only
            # since their reference periods (2013-2017 / 2018-2022 / 10yr) are
            # anchored to the live forecast, not arbitrary hindcasts.
            years_with_preds = sorted(
                int(y) for y in df["Harvest Year"].dropna().unique()
            )
            if not years_with_preds:
                logger.warning(f"No prediction years in DB for {country} {crop} {model}")
                continue

            # [ML] outlook_maps_current_year_only: restrict the per-year map
            # loop to the live forecast year, skipping hindcast-year maps.
            # Only applied when current_year actually has predictions, so a
            # hindcast-only combo still renders (rather than producing zero).
            if maps_current_year_only and current_year in years_with_preds:
                years_with_preds = [current_year]

            map_countries = countries if is_pooled else [country]

            # Store raw predictions for diagnostics (once per combo, not per year)
            df_pred_store[(country, crop, model)] = df

            for year_to_map in years_with_preds:
                df_current = df[df["Harvest Year"] == year_to_map]
                if df_current.empty:
                    continue

                # Determine which stages to produce maps for (outlook maps
                # are only meaningful for in-season stages, not pre-season)
                _stage_names = df_current["Stage Name"].dropna().unique()
                _planting = _infer_planting_month(_stage_names)
                available_stages = sorted(
                    _stage_names, key=lambda s: _stage_sort_key(s, _planting)
                )
                in_season_stages = [
                    s for s in available_stages
                    if not s.startswith("Pre-Season") and not s.startswith("In-Season")
                ]
                if use_latest_stage or len(in_season_stages) <= 1:
                    stages_to_map = [in_season_stages[-1]] if in_season_stages else []
                else:
                    stages_to_map = in_season_stages

                for stage_name in stages_to_map:
                    # Filter to this stage across all years
                    df_stage = df[df["Stage Name"] == stage_name] if len(available_stages) > 1 else df

                    df_outlook = _compute_outlook_index(
                        df_stage, year_to_map, n_years, aggregation,
                        use_latest_stage=(len(available_stages) <= 1),
                        stage_name=stage_name,
                    )
                    if df_outlook.empty:
                        logger.warning(
                            f"Could not compute outlook for {country} {crop} {model} "
                            f"stage {stage_name} year {year_to_map}"
                        )
                        continue

                    n_hist = len(
                        df_stage[
                            (df_stage["Harvest Year"] < year_to_map)
                            & (df_stage["Harvest Year"] >= year_to_map - n_years)
                        ]["Harvest Year"].unique()
                    )
                    if n_hist < 3:
                        logger.warning(
                            f"Only {n_hist} historical years for {country} {crop} {model} "
                            f"stage {stage_name} year {year_to_map} (requested {n_years})"
                        )

                    df_outlook["Crop"] = crop
                    df_outlook["Model"] = model
                    df_outlook["Stage Name"] = stage_name
                    # Analyst-facing calendar-order label (falls back to
                    # Stage Name for older DBs that don't emit it).
                    if "Stage Window Display" in df_stage.columns and len(df_stage):
                        _swd = df_stage["Stage Window Display"].dropna()
                        df_outlook["Stage Window Display"] = (
                            _swd.iloc[0] if not _swd.empty else stage_name
                        )
                    else:
                        df_outlook["Stage Window Display"] = stage_name
                    df_outlook["Forecast Year"] = year_to_map
                    all_outlook_frames.append(df_outlook)

                    # [ML] make_maps gate: skip per-year/stage rendering
                    # (outlook map + predicted-yield choropleth + obs-anomaly
                    # maps). all_outlook_frames already captured above, so the
                    # outlook CSV is unaffected.
                    if not make_maps:
                        continue

                    # Generate map — saved in maps/{model}[/{stage}] subfolder
                    stage_safe = friendly_stage_label(stage_name).replace(" - ", "-").replace(" ", "_")
                    dir_model = dir_outlook / "maps" / model / country / crop
                    if len(available_stages) > 1:
                        dir_model = dir_model / stage_safe
                    os.makedirs(dir_model, exist_ok=True)
                    _countries_str = "_".join(map_countries)

                    # Multi-season countries (e.g. Somalia 1=Gu, 2=Deyr) render
                    # ONE map set per season, each tagged with a "_s{n}" filename
                    # token + season label. Single-season / no-Season data yields
                    # a single ("", "") pass, so filenames + maps are unchanged.
                    for _season, dfo, season_token, season_label in _season_iter(df_outlook):
                        _generate_outlook_map(
                            dg,
                            dfo,
                            map_countries,
                            crop,
                            model,
                            year_to_map,
                            n_years,
                            aggregation,
                            dir_model,
                            stage_name=stage_name,
                            annotate_regions=False,
                            fname_extra=season_token,
                            label_extra=season_label,
                        )
                        logger.info(
                            f"Map saved: {dir_model / f'yield_outlook_{_countries_str}_{crop}_{model}_{stage_name}_{year_to_map}{season_token}.png'}"
                        )

                        # Absolute predicted-yield choropleth (sequential, tn/ha).
                        # Complements the diverging outlook-index map by showing the
                        # raw forecast value per region rather than a % departure.
                        df_pred_map = dfo[[
                            "Country", "Region", "Country Region", "current_predicted",
                        ]].rename(columns={"current_predicted": "Predicted Yield (tn per ha)"})
                        pred_fname = (
                            f"predicted_yield_{_countries_str}_{crop}_{model}"
                            f"_{stage_name}_{year_to_map}{season_token}.png"
                        )
                        plot.plot_map(
                            dg,
                            df_pred_map,
                            merge_col="Country Region",
                            name_country=[c.title().replace("_", " ") for c in map_countries],
                            name_col="Predicted Yield (tn per ha)",
                            dir_out=dir_model,
                            fname=pred_fname,
                            label=f"Predicted yield ({parser.get('ML', 'yield_units', fallback='Mg/ha')})\n{crop.title()}, {year_to_map}, {friendly_stage_label(stage_name)}{season_label}",
                            vmin=float(df_pred_map["Predicted Yield (tn per ha)"].min()),
                            vmax=float(df_pred_map["Predicted Yield (tn per ha)"].max()),
                            cmap=pal.scientific.sequential.Bamako_20_r,
                            series="sequential",
                            annotate_regions=False,
                            loc_legend="lower left",
                        )

                        # Observed-baseline anomaly maps — current year only.
                        # The reference periods (2013-2017 / 2018-2022 / 10yr from
                        # today) are anchored to the live forecast; rendering them
                        # against hindcast predictions would compare a 2010 forecast
                        # against an observed mean that includes the future.
                        if year_to_map == current_year:
                            # Minimal-crop-area filter (opt-in via geocif.txt):
                            # regions producing < min_share % of national are
                            # rendered gray on the *_filtered.png variant, so
                            # tiny-area regions with noisy predictions don't
                            # visually dominate the map. Computed here (not
                            # earlier) so it's country-scoped and reflects the
                            # same df used to build df_outlook.
                            area_filter_enabled = parser.getboolean(
                                "ML", "outlook_area_filter_enabled", fallback=True
                            )
                            min_share = parser.getfloat(
                                "ML", "outlook_min_production_share", fallback=0.5
                            )
                            prod_pct = {}
                            if area_filter_enabled:
                                from .viz import diagnostics as _diag
                                prod_pct = _diag.compute_production_pct(df, country)

                            for period_label, df_obs in obs_baselines.items():
                                df_anom = dfo[["Country", "Region", "Country Region", "current_predicted"]].merge(
                                    df_obs, on="Region", how="left"
                                )
                                df_anom["obs_anomaly"] = np.where(
                                    df_anom["obs_mean"] != 0,
                                    (df_anom["current_predicted"] - df_anom["obs_mean"]) / df_anom["obs_mean"] * 100,
                                    np.nan,
                                )
                                dir_obs = dir_model / "obs_anomaly" / period_label
                                os.makedirs(dir_obs, exist_ok=True)
                                _generate_outlook_map(
                                    dg, df_anom, map_countries, crop, model, current_year,
                                    n_years, aggregation, dir_obs,
                                    col="obs_anomaly",
                                    col_label=f"% departure from {period_label} observed mean\n{crop.title()}, {current_year}",
                                    fname_extra=season_token,
                                    label_extra=season_label,
                                )

                                if area_filter_enabled and prod_pct:
                                    df_anom_f = df_anom.copy()
                                    mask_excluded = df_anom_f["Region"].map(
                                        lambda r: prod_pct.get(r, 0.0) < min_share
                                    )
                                    df_anom_f.loc[mask_excluded, "obs_anomaly"] = np.nan
                                    _generate_outlook_map(
                                        dg, df_anom_f, map_countries, crop, model, current_year,
                                        n_years, aggregation, dir_obs,
                                        col="obs_anomaly",
                                        col_label=(
                                            f"% departure from {period_label} observed mean\n"
                                            f"{crop.title()}, {current_year}\n"
                                            f"(regions with <{min_share:g}% national share grayed)"
                                        ),
                                        fname_extra=f"{season_token}_filtered",
                                        label_extra=season_label,
                                    )

            # Diagnostic plots (forest, yield table, MAPE/RMSE boxes, scatter,
            # per-year scatters) ALWAYS run — no longer gated by make_maps.
            # make_maps now controls ONLY the choropleth maps (rendered above);
            # plots are cheap, the choropleth maps are the slow part.

            # Per-(country, crop, model) diagnostic plots
            from .viz import diagnostics as diag
            country_lower = country.lower().replace(" ", "_")
            plot_dir = dir_outlook / "plots" / model / country_lower / crop

            # Production share (last 5 years) — shared by forest plot and
            # MAPE bar to order regions consistently.
            prod_pct = diag.compute_production_pct(df, country)

            # Forest plot: current-year predicted + CI, with last 5 observed yields per region
            if "lower CI" in df_current.columns:
                df_plot = (
                    df_current.sort_values("Stage Name")
                    .groupby("Region", as_index=False).last()
                )
                df_obs_last5 = (
                    df.dropna(subset=["Observed Yield (tn per ha)"])
                    .drop_duplicates(subset=["Region", "Harvest Year"])
                    .sort_values(["Region", "Harvest Year"])
                    .groupby("Region", group_keys=False)
                    .tail(5)
                )[["Region", "Harvest Year", "Observed Yield (tn per ha)"]]

                if not df_obs_last5.empty:
                    yr_min = int(df_obs_last5["Harvest Year"].min())
                    yr_max = int(df_obs_last5["Harvest Year"].max())
                    obs_label = f"Observed ({yr_min}-{yr_max})"
                else:
                    obs_label = "Observed"

                diag.forest_yield_ci(
                    df_plot,
                    predicted_col="Predicted Yield (tn per ha)",
                    out_path=plot_dir / f"yield_ci_{country_lower}_{crop}_{model}.png",
                    title=f"Predicted Yield with CI \u2014 {country.title().replace('_', ' ')} {crop.title().replace('_', ' ')} ({model})",
                    reference_df=df_obs_last5,
                    reference_value_col="Observed Yield (tn per ha)",
                    reference_label=obs_label,
                    production_pct=prod_pct,
                )

                # Per-region tabular summary (same ordering as the forest
                # plot: largest producer at top, region labels with
                # production-share suffix).
                df_table = df_plot[[
                    "Region", "Predicted Yield (tn per ha)",
                    "lower CI", "upper CI",
                ]].rename(columns={"Predicted Yield (tn per ha)": "Predicted Yield"})

                # Last observed yield + year per region (different regions can
                # have different "last available" years).
                df_last_obs = (
                    df.dropna(subset=["Observed Yield (tn per ha)"])
                    .sort_values(["Region", "Harvest Year"])
                    .drop_duplicates(subset=["Region"], keep="last")[
                        ["Region", "Harvest Year", "Observed Yield (tn per ha)"]
                    ]
                    .rename(columns={
                        "Harvest Year": "Last Obs Year",
                        "Observed Yield (tn per ha)": "Last Obs Yield",
                    })
                )
                df_last_obs["Last Obs Year"] = df_last_obs["Last Obs Year"].apply(
                    lambda v: str(int(v)) if pd.notna(v) else ""
                )
                df_table = df_table.merge(df_last_obs, on="Region", how="left")

                # Mean of the last 5 observed years per region + the span of
                # years averaged. Reuses df_obs_last5 (the forest plot's
                # reference set) so the table and the "Observed (yr_min-yr_max)"
                # plot reference are computed from exactly the same rows.
                if not df_obs_last5.empty:
                    df_last5 = (
                        df_obs_last5.groupby("Region")
                        .agg(
                            _mean=("Observed Yield (tn per ha)", "mean"),
                            _ymin=("Harvest Year", "min"),
                            _ymax=("Harvest Year", "max"),
                            _n=("Harvest Year", "count"),
                        )
                        .reset_index()
                    )
                    df_last5["Mean 5yr Obs Yield"] = df_last5["_mean"].round(2)
                    # Contiguous spans print as "YYYY-YYYY"; gaps (or <5 years
                    # available) append "(n=k)" so the count isn't misread.
                    df_last5["5yr Obs Years"] = df_last5.apply(
                        lambda r: (
                            f"{int(r['_ymin'])}–{int(r['_ymax'])}"
                            if int(r["_ymax"]) - int(r["_ymin"]) == int(r["_n"]) - 1
                            else f"{int(r['_ymin'])}–{int(r['_ymax'])} (n={int(r['_n'])})"
                        ),
                        axis=1,
                    )
                    df_table = df_table.merge(
                        df_last5[["Region", "Mean 5yr Obs Yield", "5yr Obs Years"]],
                        on="Region", how="left",
                    )

                from .viz.diagnostics import is_production_share_shown
                _show_prod_share = is_production_share_shown()
                if prod_pct:
                    order = sorted(
                        df_table["Region"].tolist(),
                        key=lambda r: prod_pct.get(r, 0),
                        reverse=True,
                    )
                    df_table = df_table.set_index("Region").loc[order].reset_index()
                    # Production share goes in its own column so the Region
                    # name keeps its native width (no parenthetical suffix
                    # that pushed the column to truncate region names).
                    if _show_prod_share:
                        df_table["% of Production"] = [
                            f"{prod_pct.get(r, 0):.1f}%" for r in df_table["Region"]
                        ]
                ci_has_values = (
                    df_table["lower CI"].notna().any()
                    or df_table["upper CI"].notna().any()
                )
                cols_order = []
                if prod_pct and _show_prod_share:
                    cols_order.append("% of Production")
                cols_order += ["Predicted Yield"]
                if ci_has_values:
                    cols_order += ["lower CI", "upper CI"]
                cols_order += ["Last Obs Yield", "Last Obs Year"]
                for _c in ["Mean 5yr Obs Yield", "5yr Obs Years"]:
                    if _c in df_table.columns:
                        cols_order.append(_c)
                diag.yield_table(
                    df_table[["Region"] + cols_order],
                    out_path=plot_dir / f"yield_table_{country_lower}_{crop}_{model}.png",
                    title=(
                        f"Yield Forecast Summary \u2014 "
                        f"{country.title().replace('_', ' ')} "
                        f"{crop.title().replace('_', ' ')} ({current_year})"
                    ),
                    columns=cols_order,
                )

            # MAPE diagnostics: one row per (Region, Harvest Year) using latest stage.
            df_mape = df.dropna(
                subset=["Observed Yield (tn per ha)", "Predicted Yield (tn per ha)"]
            ).copy()
            df_mape = df_mape[df_mape["Observed Yield (tn per ha)"] != 0]
            if not df_mape.empty:
                df_mape["MAPE"] = (
                    (df_mape["Predicted Yield (tn per ha)"]
                     - df_mape["Observed Yield (tn per ha)"]).abs()
                    / df_mape["Observed Yield (tn per ha)"] * 100
                )
                # RMSE per (Region, Year) row is just the absolute error in Mg/ha;
                # aggregating box-style across regions/years reproduces the standard
                # RMSE distribution.
                df_mape["RMSE"] = (
                    df_mape["Predicted Yield (tn per ha)"]
                    - df_mape["Observed Yield (tn per ha)"]
                ).abs()
                df_mape = (
                    df_mape.sort_values("Stage Name")
                    .groupby(["Region", "Harvest Year"], as_index=False).last()
                )

                # Distribution-aware box plots with jittered individual
                # (Region, Year) points so year-to-year spread per region
                # (and region-to-region spread per year) is visible.
                diag.mape_box_by_region(
                    df_mape,
                    title=(
                        f"MAPE Distribution by Region \u2014 "
                        f"{country.title().replace('_', ' ')} "
                        f"{crop.title().replace('_', ' ')} ({model})"
                    ),
                    dir_out=plot_dir,
                    fname=f"mape_box_region_{country_lower}_{crop}_{model}.png",
                    production_pct=prod_pct,
                )
                diag.mape_box_by_year(
                    df_mape,
                    title=(
                        f"MAPE Distribution by Year \u2014 "
                        f"{country.title().replace('_', ' ')} "
                        f"{crop.title().replace('_', ' ')} ({model})"
                    ),
                    dir_out=plot_dir,
                    fname=f"mape_box_year_{country_lower}_{crop}_{model}.png",
                )
                diag.mape_by_year(
                    df_mape,
                    title=f"MAPE by Year \u2014 {country.title().replace('_', ' ')} {crop.title().replace('_', ' ')} ({model})",
                    dir_out=plot_dir,
                    fname=f"mape_year_{country_lower}_{crop}_{model}.png",
                    obs_col="Observed Yield (tn per ha)",
                    pred_col="Predicted Yield (tn per ha)",
                    area_col="Area (ha)",
                    threshold=20.0,
                )
                # RMSE twins of the three MAPE plots above. Same (Region, Year)
                # grid, natural Mg/ha units, no percentage cap.
                diag.rmse_box_by_region(
                    df_mape,
                    title=(
                        f"RMSE Distribution by Region \u2014 "
                        f"{country.title().replace('_', ' ')} "
                        f"{crop.title().replace('_', ' ')} ({model})"
                    ),
                    dir_out=plot_dir,
                    fname=f"rmse_box_region_{country_lower}_{crop}_{model}.png",
                    production_pct=prod_pct,
                )
                diag.rmse_box_by_year(
                    df_mape,
                    title=(
                        f"RMSE Distribution by Year \u2014 "
                        f"{country.title().replace('_', ' ')} "
                        f"{crop.title().replace('_', ' ')} ({model})"
                    ),
                    dir_out=plot_dir,
                    fname=f"rmse_box_year_{country_lower}_{crop}_{model}.png",
                )
                diag.rmse_by_year(
                    df_mape,
                    title=f"RMSE by Year \u2014 {country.title().replace('_', ' ')} {crop.title().replace('_', ' ')} ({model})",
                    dir_out=plot_dir,
                    fname=f"rmse_year_{country_lower}_{crop}_{model}.png",
                    obs_col="Observed Yield (tn per ha)",
                    pred_col="Predicted Yield (tn per ha)",
                    area_col="Area (ha)",
                )

            # % of national crop area — choropleth (mirrors analysis.py's perc_area map)
            area_pct = diag.compute_area_pct(df, country)
            if area_pct:
                df_area_pct = pd.DataFrame(
                    [{"Region": r, "% of National Area (ha)": v}
                     for r, v in area_pct.items()]
                )
                df_area_pct["Country"] = country
                df_area_pct["Country Region"] = (
                    df_area_pct["Country"].str.lower().str.replace("_", " ")
                    + " " + df_area_pct["Region"].str.lower()
                )
                area_map_dir = dir_outlook / "maps" / model / country_lower / crop
                plot.plot_map(
                    dg,
                    df_area_pct,
                    merge_col="Country Region",
                    name_country=[country.title().replace("_", " ")],
                    name_col="% of National Area (ha)",
                    dir_out=area_map_dir,
                    fname=f"perc_area_{country_lower}_{crop}_{model}.png",
                    label=f"% of National Area (ha) — last 5-yr avg\n{crop.title()}",
                    vmin=float(df_area_pct["% of National Area (ha)"].min()),
                    vmax=float(df_area_pct["% of National Area (ha)"].max()),
                    cmap=pal.scientific.sequential.Bamako_20_r,
                    series="sequential",
                    annotate_regions=False,
                    loc_legend="lower left",
                )

    # ---- Consolidated output: maps, ensemble, and CSVs ----
    if all_outlook_frames:
        df_all = pd.concat(all_outlook_frames, ignore_index=True)
        scope = "africa" if len(countries) > 1 else countries[0].lower().replace(" ", "_")
        crops_str = "_".join(sorted(df_all["Crop"].unique()))

        # Consolidated multi-country maps — one per (crop, model) subfolder
        for (crop, model), df_group in df_all.groupby(["Crop", "Model"]):
            countries_with_data = df_group["Country"].unique().tolist()
            if len(countries_with_data) <= 1:
                continue
            # Multi-country consolidated map — lives under maps/{model}/_combined/
            # to avoid clashing with per-country folders that now sit at
            # maps/{model}/{country}/ after the country-level insertion.
            dir_model = dir_outlook / "maps" / model / "_combined"
            os.makedirs(dir_model, exist_ok=True)
            # Split by season so a multi-season country in the pool doesn't
            # merge 2 rows/region onto the shapefile (no-Season -> single pass).
            for _season, dfg, season_token, season_label in _season_iter(df_group):
                _generate_outlook_map(
                    dg, dfg, countries_with_data, crop, model,
                    current_year, n_years, aggregation, dir_model,
                    stage_name="combined", annotate_regions=False,
                    fname_extra=season_token, label_extra=season_label,
                )

        # Consolidated multi-country obs_anomaly maps — one per (crop, model, period)
        for (crop_val, model_val), df_group in df_all.groupby(["Crop", "Model"]):
            countries_with_data = df_group["Country"].unique().tolist()
            if len(countries_with_data) <= 1:
                continue
            obs_baselines_combined = _load_observed_baselines(countries_with_data, crop_val, parser, current_year=current_year)
            for period_label, df_obs in obs_baselines_combined.items():
                for _season, dfg, season_token, season_label in _season_iter(df_group):
                    df_anom = dfg[
                        ["Country", "Region", "Country Region", "current_predicted"]
                    ].merge(df_obs, on="Region", how="left")
                    df_anom["obs_anomaly"] = np.where(
                        df_anom["obs_mean"] != 0,
                        (df_anom["current_predicted"] - df_anom["obs_mean"])
                        / df_anom["obs_mean"] * 100,
                        np.nan,
                    )
                    dir_obs_combined = dir_outlook / "maps" / model_val / "_combined" / "obs_anomaly" / period_label
                    os.makedirs(dir_obs_combined, exist_ok=True)
                    _generate_outlook_map(
                        dg, df_anom, countries_with_data, crop_val, model_val,
                        current_year, n_years, aggregation, dir_obs_combined,
                        col="obs_anomaly",
                        col_label=f"% departure from {period_label} observed mean\n{crop_val.title()}, {current_year}",
                        stage_name="combined", annotate_regions=False,
                        fname_extra=season_token, label_extra=season_label,
                    )

        # Ensemble: mean across models (skip when only one model)
        n_models = df_all["Model"].nunique()
        df_ensemble = None
        if n_models > 1:
            _agg_map = {
                "outlook_index": "mean",
                "current_predicted": "mean",
                "hist_predicted": "mean",
                "Stage Name": "last",
            }
            # Propagate the calendar-order display label when the DB
            # provided it (newer runs). Older DBs won't have this column;
            # the aggregation just skips it. See stages.get_stage_information_dict.
            if "Stage Window Display" in df_all.columns:
                _agg_map["Stage Window Display"] = "last"
            # Season-aware grouping: keep Gu/Deyr separate so the ensemble
            # doesn't average two seasons into one row per region. Falls back
            # to the original 5-key grouping when there's no Season column.
            _ens_keys = ["Country", "Region", "Country Region", "Crop", "Forecast Year"]
            if "Season" in df_all.columns:
                _ens_keys = [
                    "Country", "Region", "Country Region", "Season",
                    "Crop", "Forecast Year",
                ]
            df_ensemble = (
                df_all.groupby(_ens_keys, as_index=False).agg(_agg_map)
            )
            df_ensemble["Model"] = "ensemble"

            dir_ens = dir_outlook / "maps" / "ensemble"
            os.makedirs(dir_ens, exist_ok=True)

            # Per-country ensemble maps — under maps/ensemble/{country}/
            for (country_val, crop_val), df_group in df_ensemble.groupby(["Country", "Crop"]):
                map_countries_val = countries if country_val == "pooled" else [country_val]
                stage_val = df_group["Stage Name"].iloc[0]
                dir_ens_country = dir_ens / country_val
                os.makedirs(dir_ens_country, exist_ok=True)
                for _season, dfg, season_token, season_label in _season_iter(df_group):
                    _generate_outlook_map(
                        dg, dfg, map_countries_val, crop_val,
                        "ensemble", current_year, n_years, aggregation, dir_ens_country,
                        stage_name=stage_val, annotate_regions=False,
                        fname_extra=season_token, label_extra=season_label,
                    )

            # Multi-country ensemble maps — under maps/ensemble/_combined/
            dir_ens_combined = dir_ens / "_combined"
            for crop_val, df_group in df_ensemble.groupby("Crop"):
                if len(df_group["Country"].unique()) > 1:
                    os.makedirs(dir_ens_combined, exist_ok=True)
                    for _season, dfg, season_token, season_label in _season_iter(df_group):
                        _generate_outlook_map(
                            dg, dfg, dfg["Country"].unique().tolist(), crop_val,
                            "ensemble", current_year, n_years, aggregation, dir_ens_combined,
                            stage_name="combined", annotate_regions=False,
                            fname_extra=season_token, label_extra=season_label,
                        )

            # Ensemble observed-baseline anomaly maps — single country goes
            # under maps/ensemble/{country}/obs_anomaly/{period}/, multi-country
            # under maps/ensemble/_combined/obs_anomaly/{period}/.
            for crop_val, df_ens_crop in df_ensemble.groupby("Crop"):
                countries_ens = df_ens_crop["Country"].unique().tolist()
                obs_baselines_ens = _load_observed_baselines(countries_ens, crop_val, parser, current_year=current_year)
                for period_label, df_obs in obs_baselines_ens.items():
                    for _season, dfg, season_token, season_label in _season_iter(df_ens_crop):
                        df_ens_anom = dfg[
                            ["Country", "Region", "Country Region", "current_predicted"]
                        ].merge(df_obs, on="Region", how="left")
                        df_ens_anom["obs_anomaly"] = np.where(
                            df_ens_anom["obs_mean"] != 0,
                            (df_ens_anom["current_predicted"] - df_ens_anom["obs_mean"])
                            / df_ens_anom["obs_mean"] * 100,
                            np.nan,
                        )
                        if len(countries_ens) == 1:
                            dir_ens_obs = dir_ens / countries_ens[0] / "obs_anomaly" / period_label
                        else:
                            dir_ens_obs = dir_ens / "_combined" / "obs_anomaly" / period_label
                        os.makedirs(dir_ens_obs, exist_ok=True)
                        _generate_outlook_map(
                            dg, df_ens_anom, countries_ens, crop_val, "ensemble", current_year,
                            n_years, aggregation, dir_ens_obs,
                            col="obs_anomaly",
                            col_label=f"% departure from {period_label} observed mean\n{crop_val.title()}, {current_year}",
                            fname_extra=season_token, label_extra=season_label,
                        )

        # Config-gated ensemble blends. Two flavors, both leak-safe (per-
        # region history filtered to Harvest Year < Forecast Year):
        #   * ``use_inv_rmse_stack``  → weights ∝ 1/RMSE  (pseudo-model 'inv_rmse')
        #   * ``use_bma_bic``         → weights ∝ exp(-BIC/2), proper BMA
        #                                (pseudo-model 'bma')
        # Both can run in parallel — outputs appear as separate pseudo-
        # models in long/wide CSVs, maps, and diagnostics.
        blends = []  # list of (flag_name, blend_df, pseudo_model_name)

        use_inv_rmse_stack = parser.getboolean(
            "ML", "use_inv_rmse_stack", fallback=False,
        )
        if use_inv_rmse_stack and n_models > 1:
            df_inv_rmse = _inv_rmse_stack(df_all, df_pred_store)
            if df_inv_rmse is not None and not df_inv_rmse.empty:
                logger.info(
                    f"inv_rmse_stack: emitted {len(df_inv_rmse)} rows across "
                    f"{df_inv_rmse['Region'].nunique()} regions, "
                    f"{df_inv_rmse['Country'].nunique()} countries."
                )
                blends.append(("inv_rmse", df_inv_rmse))
            else:
                logger.warning(
                    "inv_rmse_stack produced no rows — insufficient historical "
                    "predictions across models. Ensure at least "
                    "min_history_years=3 forecast_seasons in the DB."
                )

        use_bma_bic = parser.getboolean("ML", "use_bma_bic", fallback=False)
        if use_bma_bic and n_models > 1:
            # Load per-project effective parameter overrides if present
            eff_params_override = None
            if parser.has_option("ML", "bma_effective_params"):
                try:
                    eff_params_override = ast.literal_eval(
                        parser.get("ML", "bma_effective_params")
                    )
                    if not isinstance(eff_params_override, dict):
                        eff_params_override = None
                except (ValueError, SyntaxError):
                    logger.warning(
                        "Could not parse [ML] bma_effective_params — must be a "
                        "Python literal dict. Using built-in defaults."
                    )
                    eff_params_override = None
            df_bma = _bma_bic_blend(
                df_all, df_pred_store, effective_params=eff_params_override
            )
            if df_bma is not None and not df_bma.empty:
                logger.info(
                    f"bma_bic: emitted {len(df_bma)} rows across "
                    f"{df_bma['Region'].nunique()} regions, "
                    f"{df_bma['Country'].nunique()} countries."
                )
                blends.append(("bma", df_bma))
            else:
                logger.warning(
                    "bma_bic produced no rows — either insufficient history "
                    "OR every model was skipped for missing effective_params. "
                    "Check [ML] bma_effective_params in geocif.txt."
                )

        # Emit per-country maps for each active blend under maps/{blend}/
        for blend_name, df_blend in blends:
            dir_blend = dir_outlook / "maps" / blend_name
            os.makedirs(dir_blend, exist_ok=True)
            for (country_val, crop_val), df_group in df_blend.groupby(["Country", "Crop"]):
                map_countries_val = countries if country_val == "pooled" else [country_val]
                stage_val = df_group["Stage Name"].iloc[0] if "Stage Name" in df_group.columns else ""
                dir_blend_country = dir_blend / country_val
                os.makedirs(dir_blend_country, exist_ok=True)
                _generate_outlook_map(
                    dg, df_group, map_countries_val, crop_val,
                    blend_name, current_year, n_years, aggregation, dir_blend_country,
                    stage_name=stage_val, annotate_regions=False,
                )

        # Planting/harvest months per (Country, Crop, Season) from each
        # country's configured crop calendar (EWCM etc.), falling back to the
        # multi-year stage-window span when the calendar lacks the crop/season.
        # Built from df_pred_store (all years/stages) so the live in-season
        # year's truncated windows don't understate the harvest.
        from pathlib import Path as _Path
        _dir_cal = parser.get("PATHS", "dir_crop_calendars", fallback="")
        season_bounds = {}
        for (_c_cfg, _crop_cfg, _m), _dfp in df_pred_store.items():
            if _dfp is None or _dfp.empty or "Stage Window Display" not in _dfp.columns:
                continue
            _country_val = _dfp["Country"].iloc[0] if "Country" in _dfp.columns else _c_cfg
            _seasons = ([int(s) for s in _dfp["Season"].dropna().unique()]
                        if "Season" in _dfp.columns else [None])
            _cal_file = (parser.get(_c_cfg, "calendar_file", fallback="")
                         if parser.has_section(_c_cfg) else "")
            for _s in _seasons:
                _key = (_country_val, _crop_cfg, _s)
                if _key in season_bounds:
                    continue
                _pb = (None, None)
                if _cal_file and _dir_cal:
                    _pb = _calendar_bounds(_Path(_dir_cal) / _cal_file, _c_cfg,
                                           _crop_cfg, _s if _s is not None else 1)
                if _pb == (None, None):
                    _sub = _dfp if _s is None else _dfp[_dfp["Season"] == _s]
                    _pb = _season_bounds_from_windows(_sub["Stage Window Display"])
                season_bounds[_key] = _pb
        logger.info(f"Calendar planting/harvest bounds (Country,Crop,Season): {season_bounds}")

        # Full hindcast+forecast series, one row per time step. Written from
        # df_pred_store (every year/stage the DB returned) rather than df_all,
        # which is already narrowed to the live forecast year.
        try:
            _write_monthly_history(df_pred_store, season_bounds, dir_outlook)
        except Exception as e:  # never let an export kill a completed run
            logger.warning(f"Monthly history CSV export failed: {e}")

        # Long-format CSV — one row per (region, year, model) including
        # ensemble + every active blend
        df_long_parts = [df_all]
        if df_ensemble is not None:
            df_long_parts.append(df_ensemble)
        for _blend_name, df_blend in blends:
            df_long_parts.append(df_blend)
        df_long = pd.concat(df_long_parts, ignore_index=True)
        # Analyst-facing calendar columns: planting / harvest (from crop
        # calendar) + prediction/as-of month (per time-step row).
        df_long = _add_calendar_columns(df_long, season_bounds)
        csv_path = dir_outlook / f"yield_outlook_{scope}_{crops_str}_{current_year}.csv"
        df_long.to_csv(csv_path, index=False)
        logger.info(f"Outlook CSV saved to {csv_path}")

        # Wide-format CSV: one outlook_index column per model + ensemble
        # + one column per active blend
        pivot_cols = ["Country", "Region", "Crop", "Forecast Year"]
        df_pivot_src = df_all
        if "Season" in df_all.columns:
            # Multi-season countries: keep seasons as distinct wide rows so
            # pivot_table doesn't silently average Gu+Deyr into one value.
            # Rows from single-season / no-Season DBs (in a mixed run) carry
            # NaN Season, which pivot_table would drop as a NaN index key —
            # fill with 0 ("unspecified season") for the pivot so they survive.
            pivot_cols = pivot_cols + ["Season"]
            df_pivot_src = df_all.copy()
            df_pivot_src["Season"] = df_pivot_src["Season"].fillna(0).astype(int)
        # Keep each time-step (prediction month) as its own wide row rather
        # than silently averaging across stages when run_time_steps != latest.
        if "Stage Window Display" in df_pivot_src.columns:
            pivot_cols = pivot_cols + ["Stage Window Display"]
        df_wide = df_pivot_src.pivot_table(
            index=pivot_cols, columns="Model", values="outlook_index"
        ).reset_index()
        df_wide.columns.name = None
        model_cols = [c for c in df_wide.columns if c not in pivot_cols]
        if len(model_cols) > 1:
            df_wide["ensemble"] = df_wide[model_cols].mean(axis=1)
        for blend_name, df_blend in blends:
            # Blends may lack a Season column (their internals group on region
            # only); merge on whatever pivot keys the blend actually has.
            merge_cols = [c for c in pivot_cols if c in df_blend.columns]
            df_wide = df_wide.merge(
                df_blend[merge_cols + ["outlook_index"]].rename(
                    columns={"outlook_index": blend_name}
                ),
                on=merge_cols, how="left",
            )
        df_wide = _add_calendar_columns(df_wide, season_bounds)
        csv_wide = dir_outlook / f"yield_outlook_{scope}_{crops_str}_{current_year}_wide.csv"
        df_wide.to_csv(csv_wide, index=False)
        logger.info(f"Wide-format CSV saved to {csv_wide}")
    else:
        logger.warning("No outlook data generated — check DB has predictions.")

    # Inject each ensemble blend as a synthetic ordinary "model" in
    # df_pred_store so every downstream diagnostic (rRMSEp bar, per-region
    # MAPE/RMSE bars, per-year scatter, model_comparison figures, best-
    # model-per-region map) treats the blend as first-class. The blend
    # lives ONLY in the outlook long CSV in the DB era — its raw hindcast
    # predictions per (region, harvest year) come from
    # df_blend.current_predicted (the weighted blend of the constituent
    # models' current_predicted values). Observed yield + stage name are
    # copied from any source model's df_pred_store entry for the same
    # (country, crop) — the observed values are model-independent.
    try:
        _blends_for_diag = blends  # noqa: F821 — defined inside the outlook block
    except NameError:
        _blends_for_diag = []
    for _blend_name, _df_blend in _blends_for_diag:
        if _df_blend is None or _df_blend.empty or not df_pred_store:
            continue
        for (country_val, crop_val), grp in _df_blend.groupby(["Country", "Crop"]):
            src_df = None
            for _key, _val in df_pred_store.items():
                if _key[0] == country_val and _key[1] == crop_val:
                    src_df = _val
                    break
            if src_df is None or src_df.empty:
                continue
            has_stage_src = "Stage Name" in src_df.columns
            has_stage_blend = "Stage Name" in grp.columns
            join_cols = ["Region", "Harvest Year"]
            obs_cols = join_cols + ["Observed Yield (tn per ha)"]
            obs_lookup = src_df[obs_cols].drop_duplicates(subset=join_cols)

            take = ["Region", "Forecast Year", "current_predicted"]
            if has_stage_blend:
                take.append("Stage Name")
            blend_hind = grp[take].rename(columns={
                "Forecast Year": "Harvest Year",
                "current_predicted": "Predicted Yield (tn per ha)",
            })
            try:
                blend_hind["Harvest Year"] = blend_hind["Harvest Year"].astype(
                    obs_lookup["Harvest Year"].dtype
                )
            except (TypeError, ValueError):
                pass
            blend_hind = blend_hind.merge(obs_lookup, on=join_cols, how="left")
            if not has_stage_blend and has_stage_src:
                stage_lookup = (
                    src_df[join_cols + ["Stage Name"]]
                    .drop_duplicates(subset=join_cols)
                )
                blend_hind = blend_hind.merge(stage_lookup, on=join_cols, how="left")
            df_pred_store[(country_val, crop_val, _blend_name)] = blend_hind
            logger.info(
                f"{_blend_name} in df_pred_store: added {len(blend_hind)} rows for "
                f"{country_val} {crop_val} ({_blend_name} will now appear in "
                f"rrmsep / MAPE / RMSE / scatter / model_comparison plots)"
            )

    # Diagnostic plots: scatter, MAPE bar, MAPE map, model-comparison,
    # cross-country, breakpoint — ALWAYS render (not gated by make_maps).
    # make_maps controls only the slow per-stage choropleth maps; these
    # diagnostics (incl. their per-combo MAPE map) are cheap by comparison.
    if df_pred_store:
        _generate_diagnostics(df_pred_store, dg, dir_outlook,
                              current_year=current_year, dict_config=dict_config,
                              db_path=db_path, parser=parser)

    # Optional PDF report
    generate_report_flag = parser.getboolean("ML", "generate_report", fallback=False)
    if generate_report_flag and all_outlook_frames:
        from .report import generate_report
        all_models = sorted({row[4] for row in inputs}) if inputs else models
        generate_report(
            dir_outlook, parser, current_year,
            countries, sorted({row[2] for row in inputs}) if inputs else crops,
            all_models,
        )

    # Optional lightweight per-country PDF report (independent of the full
    # report above). One PDF per country: cover + TOC + one section per crop
    # with the best-model predicted-yield map, outlook-index map, and rRMSEp
    # scorecard.
    report_lite = parser.getboolean("ML", "report_lite", fallback=False)
    if report_lite and all_outlook_frames:
        try:
            from geocif.report_lite import generate_report_lite
            all_models = sorted({row[4] for row in inputs}) if inputs else models
            generate_report_lite(
                dir_outlook, parser, current_year,
                countries, sorted({row[2] for row in inputs}) if inputs else crops,
                all_models,
                outlook_db=db_path,
            )
        except ImportError as exc:
            logger.warning(f"report_lite unavailable (skipping lite PDF): {exc}")

    # Post-run fallback diagnostic: merge per-PID fallbacks/*.csv files
    # into fallbacks_summary.csv + a bar chart per (model, category).
    # Best-effort; never blocks the rest of the post-run steps.
    try:
        _summarize_fallbacks(dir_outlook.parent)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"Fallback summary failed (non-fatal): {exc}")

    # Optional FDW CSV exports (Template 1 forecast + Template 2 historical + Template 3 accuracy)
    if fdw_export:
        from geocif.fdw_export import export_forecast, export_historical, export_accuracy

        export_forecast(
            parser,
            db_path=db_path,
            forecast_year=current_year,
            experiment_name="outlook",
            n_years=10,
        )
        export_historical(parser)
        export_accuracy(
            parser,
            db_path=db_path,
            forecast_year=current_year,
            experiment_name="outlook",
        )

    # End-of-run signal + forced exit.
    #
    # Two problems the naive `logger.info` alone couldn't solve:
    #   1. Log buffering — logzero output can sit in a buffer during
    #      interpreter shutdown and never reach the log file if the
    #      process is killed / hangs before flush.
    #   2. Interpreter-shutdown hang — after all work is written to
    #      disk (rrmsep CSVs, plots, DB), Python's atexit chain
    #      (multiprocessing.resource_tracker, matplotlib backend
    #      cleanup, lingering ML-library threads) can block indefinitely
    #      in full-ML mode (the 60+ min hangs we observed in 0.4.799).
    #
    # Fix: write a plain-file completion marker BEFORE the logger call
    # (guaranteed to hit disk immediately, no buffering); then log +
    # flush stdio; then os._exit(0) to skip the atexit chain. All work
    # is already persisted at this point, so bypassing the atexit
    # cleanup costs nothing but avoids the hang. Skipped when the
    # process was launched via a test harness that expects normal
    # returns (detected by GEOCIF_NO_FORCE_EXIT env var).
    import sys as _sys
    import os as _os
    _mode = "reuse_db" if reuse_db is not None else "full_ML"
    _msg = f"yield_outlook.run: complete ({_mode} mode) → {dir_outlook}"
    try:
        _marker = Path(dir_outlook) / ".yield_outlook_complete"
        _marker.write_text(f"{_msg}\n", encoding="utf-8")
    except OSError:
        pass  # marker is best-effort; not fatal
    logger.info(_msg)
    _sys.stdout.flush()
    _sys.stderr.flush()
    if not _os.environ.get("GEOCIF_NO_FORCE_EXIT"):
        _os._exit(0)


if __name__ == "__main__":
    run()
