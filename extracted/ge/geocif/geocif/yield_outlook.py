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

        optional_cols = [
            c for c in ("lower CI", "upper CI", "Area (ha)") if c in table_cols
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
    """
    if use_latest_stage:
        # For each region+year, keep only the latest (last) stage prediction
        df_work = (
            df.sort_values("Stage Name")
            .groupby(["Country", "Region", "Harvest Year"])
            .last()
            .reset_index()
        )
    else:
        df_work = df[df["Stage Name"] == stage_name].copy()

    # Current year predictions per region
    df_current = df_work[df_work["Harvest Year"] == current_year]
    current_pred = (
        df_current.groupby(["Country", "Region"])["Predicted Yield (tn per ha)"]
        .mean()
        .rename("current_predicted")
    )

    # Historical years per region
    min_year = current_year - n_years
    df_hist = df_work[
        (df_work["Harvest Year"] < current_year)
        & (df_work["Harvest Year"] >= min_year)
    ]
    agg_func = "median" if aggregation == "median" else "mean"
    hist_agg = (
        df_hist.groupby(["Country", "Region"])["Predicted Yield (tn per ha)"]
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

    # Create merge column (same pattern as analysis.py:1410-1414)
    df_outlook["Country Region"] = (
        df_outlook["Country"].str.lower().str.replace("_", " ")
        + " "
        + df_outlook["Region"].str.lower()
    )

    return df_outlook


def _load_observed_baselines(countries, crop, parser, current_year=None):
    """Load observed yield baselines from statistics CSVs.

    Returns dict: {period_label -> DataFrame(Region, obs_mean)}
    Periods: '2013-2017', '2018-2022', '10yr' (10 years prior to current_year).
    The current season is always excluded from the 10yr window.
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
    baselines = {}
    for label, y1, y2 in [
        ("2013-2017", 2013, 2017),
        ("2018-2022", 2018, 2022),
        ("10yr", max_year - 10, y2_10yr),
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
                                    admin_level="admin_1"):
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

    dir_plots = dir_outlook / "plots" / model / country
    dir_maps = dir_outlook / "maps" / model
    dir_csvs = dir_outlook / "csvs" / model / country
    if stage_safe:
        dir_plots = dir_plots / stage_safe
        dir_maps = dir_maps / stage_safe
        dir_csvs = dir_csvs / stage_safe
    os.makedirs(dir_plots, exist_ok=True)
    os.makedirs(dir_maps, exist_ok=True)
    os.makedirs(dir_csvs, exist_ok=True)

    title = f"{country.title()} {crop.title()} — {model}"
    if stage_name:
        title += f" ({diag.friendly_stage_label(stage_name)})"

    with plt.style.context(["science", "no-latex"]):
        diag.scatter_obs_pred(df, title, dir_plots,
                              f"scatter_{country}_{crop}_{model}{stage_suffix}.png")
        df.to_csv(dir_csvs / f"scatter_{country}_{crop}_{model}{stage_suffix}.csv", index=False)

        # National scatter (area-weighted)
        df_national = _aggregate_national_yields(df)
        if len(df_national) >= 2:
            title_nat = f"{title} — National"
            diag.scatter_obs_pred(df_national, title_nat, dir_plots,
                                  f"scatter_national_{country}_{crop}_{model}{stage_suffix}.png")
            df_national.to_csv(dir_csvs / f"scatter_national_{country}_{crop}_{model}{stage_suffix}.csv", index=False)

        df_mape = (
            df.assign(
                MAPE=lambda d: (
                    (d[pred_col] - d[obs_col]).abs() / d[obs_col].replace(0, np.nan) * 100
                )
            )
            .groupby("Region", as_index=False)["MAPE"].mean()
        )
        prod_pct = diag.compute_production_pct(df, country)
        diag.mape_bar_chart(df_mape, title, dir_plots,
                            f"mape_bar_{country}_{crop}_{model}{stage_suffix}.png",
                            production_pct=prod_pct)
        df_mape.to_csv(dir_csvs / f"mape_bar_{country}_{crop}_{model}{stage_suffix}.csv", index=False)

    df_mape["Country Region"] = (
        country.lower().replace("_", " ") + " " + df_mape["Region"].str.lower()
    )
    df_mape = df_mape.rename(columns={"MAPE": "Mean Absolute Percentage Error"})
    dg_sub = dg[dg["ADM0_NAME"].isin(countries_display)].copy()
    logger.info(f"Map GeoDataFrame: {len(dg_sub)} rows, geom types: {dg_sub.geometry.type.unique()}")
    diag.mape_choropleth(
        dg_sub, df_mape, countries_display, False,
        dir_maps, f"mape_map_{country}_{crop}_{model}{stage_suffix}.png",
    )

    # Combined: predicted yield map + MAPE bar chart
    _plot_combined_map_mape(
        df, df_mape, dg_sub, country, crop, model, dir_plots,
        f"combined_{country}_{crop}_{model}{stage_suffix}.png",
        title, prod_pct,
        forecast_year=forecast_year, admin_level=admin_level,
    )


def _plot_combined_map_mape(df, df_mape, dg_sub, country, crop, model,
                            dir_out, fname, title, prod_pct,
                            forecast_year=None, admin_level="admin_1"):
    """Side-by-side: predicted yield choropleth (left) + MAPE bar chart (right).

    Reuses ``viz.plot.plot_map`` with ``ax=`` for the map panel.
    """
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    import palettable as pal
    import scienceplots  # noqa: F401
    from .viz.diagnostics import _label_with_pct, _sort_by_production

    pred_col = "Predicted Yield (tn per ha)"

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

    # MAPE bar data — sort by production share descending (largest at top)
    mape_col = "Mean Absolute Percentage Error"
    if mape_col not in df_mape.columns:
        return
    df_bar = df_mape.groupby("Region")[mape_col].mean()
    if prod_pct:
        order = sorted(df_bar.index, key=lambda r: prod_pct.get(r, 0), reverse=True)
        df_bar = df_bar.reindex(order)
        df_bar.index = _label_with_pct(df_bar.index, prod_pct)
    else:
        df_bar = df_bar.sort_values(ascending=False)

    countries_display = [country.title().replace("_", " ")]
    # Annotation column based on admin level
    annot_col = "ADM2_NAME" if admin_level == "admin_2" else "ADM1_NAME"

    with plt.style.context(["science", "no-latex"]):
        fig = plt.figure(figsize=(14, max(5, len(df_bar) * 0.5)))
        ax_map = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
        ax_bar = fig.add_subplot(1, 2, 2)

        # Left: predicted yield map via plot_map
        plot.plot_map(
            dg_sub,
            df_pred_region,
            merge_col="Country Region",
            name_country=countries_display,
            name_col=pred_col,
            label="Predicted yield (tn/ha)",
            title=f"Predicted Yield — {display_year}",
            vmin=float(df_pred_region[pred_col].min()),
            vmax=float(df_pred_region[pred_col].max()),
            cmap=pal.scientific.sequential.Bamako_20_r,
            series="sequential",
            annotate_regions=True,
            annotate_region_column=annot_col,
            ax=ax_map,
        )

        # Right: MAPE bar chart
        bars = ax_bar.barh(df_bar.index, df_bar.values, color="steelblue")
        for bar, val in zip(bars, df_bar.values):
            ax_bar.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                        f"{val:.1f}%", va="center", fontsize=8)
        ax_bar.set_xlabel("MAPE (%)")
        ax_bar.set_title("MAPE by Region", fontsize=10, fontweight="bold")
        ax_bar.tick_params(axis='y', length=0)

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
        return (s - e) % 12 if s >= e else s - e + 12
    return 0


def _compute_region_metric(df, stages_sorted, metric_col):
    """Compute per-region metric at each stage."""
    return (
        df.groupby(["Stage Name", "Region"])[metric_col]
        .mean()
        .reset_index()
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

        markers = ["o", "s", "D", "^", "v", "<", ">", "p", "h", "X", "*", "P"]
        for i, region in enumerate(regions):
            rdf = region_vals[region_vals["Region"] == region]
            rdf = rdf.set_index("Stage Name").reindex(stages_sorted)
            rlabel = f"{region} ({prod_pct[region]:.1f}%)" if region in prod_pct else region
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


def _plot_all_progressions(df, country, crop, model, dir_outlook):
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

    dir_progression = dir_outlook / "plots" / model / country / "progression"
    dir_csvs_prog = dir_outlook / "csvs" / model / country / "progression"
    os.makedirs(dir_csvs_prog, exist_ok=True)
    base_title = f"{country.title()} {crop.title()} ({model})"

    # MAPE
    _plot_metric_progression(
        df, stages_sorted, "MAPE", "MAPE (%)",
        f"MAPE Progression — {base_title}",
        country, crop, model, dir_progression,
        f"mape_progression_{country}_{crop}_{model}.png",
        prod_pct, has_area,
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
            df_rmse, stages_sorted, "RMSE", "RMSE (tn/ha)",
            f"RMSE Progression — {base_title}",
            country, crop, model, dir_progression,
            f"rmse_progression_{country}_{crop}_{model}.png",
            prod_pct, has_area,
            df_for_national=df,
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
        df_r2.to_csv(dir_csvs_prog / f"r2_progression_{country}_{crop}_{model}.csv", index=False)


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

    dir_plots = dir_outlook / "plots" / model / country / "feature_selection"
    dir_csvs = dir_outlook / "csvs" / model / country / "feature_selection"
    os.makedirs(dir_plots, exist_ok=True)
    os.makedirs(dir_csvs, exist_ok=True)

    base_title = f"{country.title()} {crop.title()} ({model})"

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
                          dict_config=None, db_path=None):
    """Generate scatter, MAPE bar chart, and MAPE map per (country, crop, model, stage).

    When multi-step results are present (multiple Stage Names), produces
    separate plots per stage, an aggregate, and a MAPE progression plot.
    """
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
                )
            _plot_all_progressions(df, country, crop, model, dir_outlook)
        else:
            # Single stage or no stages — generate once
            _generate_diagnostics_for_stage(
                df, country, crop, model, dg, dir_outlook,
                forecast_year=current_year, admin_level=admin_level,
            )

        # Feature selection by CID Type across stages
        if db_path is not None:
            table = f"{country}_{crop}"
            df_feat = _query_selected_features(db_path, table, model)
            if not df_feat.empty:
                _plot_feature_selection_by_stage(
                    df_feat, country, crop, model, dir_outlook
                )

    # Model comparison plots (only when multiple models)
    _generate_model_comparison(df_pred_store, dg, dir_outlook)


def _generate_model_comparison(df_pred_store, dg, dir_outlook):
    """Compare model performance when multiple models are available.

    Produces grouped bar charts of MAPE, RMSE, and R² by region and by year,
    plus a choropleth map showing which model has the lowest MAPE per region.
    Saved to ``outlook/plots/model_comparison/{country}/``.
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
                rows_region.append({
                    "Model": model, "Region": region,
                    "MAPE": rdf["MAPE"].mean(),
                    "RMSE": np.sqrt(rdf["SE"].mean()),
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
                rows_year.append({
                    "Model": model, "Harvest Year": year,
                    "MAPE": ydf["MAPE"].mean(),
                    "RMSE": np.sqrt(ydf["SE"].mean()),
                    "R2": r2,
                })

        if not rows_region:
            continue

        df_region = pd.DataFrame(rows_region)
        df_year = pd.DataFrame(rows_year)
        df_region.to_csv(dir_csvs_comp / f"metrics_by_region_{country}_{crop}.csv", index=False)
        df_year.to_csv(dir_csvs_comp / f"metrics_by_year_{country}_{crop}.csv", index=False)
        base_title = f"{country.title()} {crop.title()}"

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

        # Production share per region (reuse existing utility)
        first_df = next(iter(model_dfs.values()))
        prod_pct = diag.compute_production_pct(first_df, country)

        # National-scale metric per model (for legend labels). Computed on
        # production-aggregated national yields per year — i.e. the metric a
        # stakeholder would observe by summing predicted production into a
        # national total.  Distinct from the area-weighted average of per-
        # region scores, which cannot capture cross-region error cancellation.
        national_metrics = {}
        for model, df in model_dfs.items():
            df = df.dropna(subset=[obs_col, pred_col])
            if df.empty:
                continue
            df = df[df[obs_col] != 0].copy()
            has_area = "Area (ha)" in df.columns and df["Area (ha)"].notna().any()
            if has_area:
                nat = _aggregate_national_yields(df)
            else:
                nat = (
                    df.groupby("Harvest Year")
                    .agg({obs_col: "mean", pred_col: "mean"})
                    .reset_index()
                )
            nat = nat[nat[obs_col] != 0]
            if nat.empty:
                continue
            err = nat[pred_col] - nat[obs_col]
            w_mape = (err.abs() / nat[obs_col] * 100).mean()
            w_rmse = float(np.sqrt((err ** 2).mean()))
            national_metrics[model] = {"MAPE": w_mape, "RMSE": w_rmse}

        def _model_legend(model, metric):
            """Model display name with national metric in parentheses."""
            display = _display_model_name(model)
            nm = national_metrics.get(model, {})
            val = nm.get(metric)
            if val is not None:
                unit = "%" if metric == "MAPE" else "tn/ha" if metric == "RMSE" else ""
                return f"{display} (nat: {val:.1f}{unit})"
            return display

        with plt.style.context(["science", "no-latex"]):
            # By region: grouped bar for each metric
            for metric, ylabel in [("MAPE", "MAPE (%)"), ("RMSE", "RMSE (tn/ha)"), ("R2", "R²")]:
                pivot = df_region.pivot_table(index="Region", columns="Model", values=metric)
                if pivot.empty:
                    continue
                # Sort by production share descending (largest producer at top)
                if prod_pct:
                    order = sorted(pivot.index, key=lambda r: prod_pct.get(r, 0), reverse=True)
                    pivot = pivot.reindex(order)
                    pivot.index = [
                        f"{r} ({prod_pct[r]:.1f}%)" if r in prod_pct else r
                        for r in pivot.index
                    ]
                # Rename columns to include national metric
                # Use consistent model colors
                bar_colors = [_MODEL_COLORS.get(m, "steelblue") for m in pivot.columns]
                pivot.columns = [_model_legend(m, metric) for m in pivot.columns]
                fig, ax = plt.subplots(figsize=(10, max(4, len(pivot) * 0.5)))
                pivot.plot.barh(ax=ax, color=bar_colors)
                ax.set_xlabel(ylabel)
                ax.set_title(f"{ylabel} by Region — {base_title}", fontweight="bold")
                ax.legend(title="Model", fontsize=8)
                ax.tick_params(axis='y', length=0)
                plt.tight_layout()
                fig.savefig(dir_comp / f"{metric.lower()}_by_region_{country}_{crop}.png",
                            dpi=250, bbox_inches="tight")
                plt.close(fig)

            # By year: grouped bar for each metric
            for metric, ylabel in [("MAPE", "MAPE (%)"), ("RMSE", "RMSE (tn/ha)"), ("R2", "R²")]:
                if df_year.empty:
                    continue
                pivot = df_year.pivot_table(index="Harvest Year", columns="Model", values=metric)
                if pivot.empty:
                    continue
                bar_colors = [_MODEL_COLORS.get(m, "steelblue") for m in pivot.columns]
                pivot.columns = [_model_legend(m, metric) for m in pivot.columns]
                fig, ax = plt.subplots(figsize=(12, 5))
                pivot.plot.bar(ax=ax, color=bar_colors)
                ax.set_ylabel(ylabel)
                ax.set_title(f"{ylabel} by Year — {base_title}", fontweight="bold")
                ax.legend(title="Model", fontsize=8)
                ax.tick_params(axis='x', length=0)
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                fig.savefig(dir_comp / f"{metric.lower()}_by_year_{country}_{crop}.png",
                            dpi=250, bbox_inches="tight")
                plt.close(fig)

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
):
    """Generate a diverging choropleth map of the yield outlook index (or any anomaly column)."""
    # Fixed range: -40% to +40% departure (matching analysis.py anomaly maps)
    vmin = -40
    vmax = 40

    # Determine extend arrows based on actual data range
    data_min = df_outlook[col].min()
    data_max = df_outlook[col].max()
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
        fname = f"yield_outlook_{len(countries)}_countries_{crop}_{model}{stage_suffix}_{current_year}.png"
    else:
        fname = f"yield_outlook_{'_'.join(countries)}_{crop}_{model}{stage_suffix}_{current_year}.png"

    friendly = friendly_stage_label(stage_name) if stage_name else ""
    stage_label = f", {friendly}" if friendly else ""
    label = col_label or f"% departure from {n_years}-year hindcast {aggregation}\n{crop.title()}, {current_year}{stage_label}"
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
        parser=None, logger_obj=None, outlook_db_name=None, analysis_dir=None):
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

    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    experiment_name = parser.get("DEFAULT", "experiment_name", fallback="default")

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
            ("Forecast year", str(current_year)),
            ("Outlook index window", f"{n_years} years"),
            ("Seasons", f"{outlook_seasons[0]}-{outlook_seasons[-1]}"),
            ("Aggregation", aggregation),
            ("Time steps", parser.get("ML", "run_time_steps", fallback="latest")),
            ("Pooled", str(pool_countries_flag)),
            ("FDW export", str(fdw_export)),
            ("DB", parser.get("DEFAULT", "db")),
            ("Total combinations", str(len(inputs))),
        ]
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

            # Get all stages available for current year
            df_current = df[df["Harvest Year"] == current_year]
            if df_current.empty:
                logger.warning(
                    f"No predictions for year {current_year} in {country} {crop} {model}"
                )
                continue

            map_countries = countries if is_pooled else [country]

            # Store raw predictions for diagnostics
            df_pred_store[(country, crop, model)] = df

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
                    df_stage, current_year, n_years, aggregation,
                    use_latest_stage=(len(available_stages) <= 1),
                )
                if df_outlook.empty:
                    logger.warning(
                        f"Could not compute outlook for {country} {crop} {model} stage {stage_name}"
                    )
                    continue

                n_hist = len(
                    df_stage[
                        (df_stage["Harvest Year"] < current_year)
                        & (df_stage["Harvest Year"] >= current_year - n_years)
                    ]["Harvest Year"].unique()
                )
                if n_hist < 3:
                    logger.warning(
                        f"Only {n_hist} historical years for {country} {crop} {model} "
                        f"stage {stage_name} (requested {n_years})"
                    )

                df_outlook["Crop"] = crop
                df_outlook["Model"] = model
                df_outlook["Stage Name"] = stage_name
                df_outlook["Forecast Year"] = current_year
                all_outlook_frames.append(df_outlook)

                # Generate map — saved in maps/{model}[/{stage}] subfolder
                stage_safe = friendly_stage_label(stage_name).replace(" - ", "-").replace(" ", "_")
                dir_model = dir_outlook / "maps" / model
                if len(available_stages) > 1:
                    dir_model = dir_model / stage_safe
                os.makedirs(dir_model, exist_ok=True)
                _countries_str = "_".join(map_countries)
                _generate_outlook_map(
                    dg,
                    df_outlook,
                    map_countries,
                    crop,
                    model,
                    current_year,
                    n_years,
                    aggregation,
                    dir_model,
                    stage_name=stage_name,
                    annotate_regions=False,
                )
                logger.info(
                    f"Map saved: {dir_model / f'yield_outlook_{_countries_str}_{crop}_{model}_{stage_name}_{current_year}.png'}"
                )

                # Absolute predicted-yield choropleth (sequential, tn/ha).
                # Complements the diverging outlook-index map by showing the
                # raw forecast value per region rather than a % departure.
                df_pred_map = df_outlook[[
                    "Country", "Region", "Country Region", "current_predicted",
                ]].rename(columns={"current_predicted": "Predicted Yield (tn per ha)"})
                pred_fname = (
                    f"predicted_yield_{_countries_str}_{crop}_{model}"
                    f"_{stage_name}_{current_year}.png"
                )
                plot.plot_map(
                    dg,
                    df_pred_map,
                    merge_col="Country Region",
                    name_country=[c.title().replace("_", " ") for c in map_countries],
                    name_col="Predicted Yield (tn per ha)",
                    dir_out=dir_model,
                    fname=pred_fname,
                    label=f"Predicted yield (tn/ha)\n{crop.title()}, {current_year}, {friendly_stage_label(stage_name)}",
                    vmin=float(df_pred_map["Predicted Yield (tn per ha)"].min()),
                    vmax=float(df_pred_map["Predicted Yield (tn per ha)"].max()),
                    cmap=pal.scientific.sequential.Bamako_20_r,
                    series="sequential",
                    annotate_regions=False,
                    loc_legend="lower left",
                )

                # Observed-baseline anomaly maps (matching analysis.py: 2013-2017, 2018-2022, 10yr)
                for period_label, df_obs in obs_baselines.items():
                    df_anom = df_outlook[["Country", "Region", "Country Region", "current_predicted"]].merge(
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
                    )

            # Per-(country, crop, model) diagnostic plots
            from .viz import diagnostics as diag
            country_lower = country.lower().replace(" ", "_")
            plot_dir = dir_outlook / "plots" / model / country_lower

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
                    title=f"Predicted Yield with CI \u2014 {country} {crop} ({model})",
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

                if prod_pct:
                    order = sorted(
                        df_table["Region"].tolist(),
                        key=lambda r: prod_pct.get(r, 0),
                        reverse=True,
                    )
                    df_table = df_table.set_index("Region").loc[order].reset_index()
                    df_table["Region"] = [
                        f"{r} ({prod_pct.get(r, 0):.1f}%)" for r in df_table["Region"]
                    ]
                ci_has_values = (
                    df_table["lower CI"].notna().any()
                    or df_table["upper CI"].notna().any()
                )
                cols_order = ["Predicted Yield"]
                if ci_has_values:
                    cols_order += ["lower CI", "upper CI"]
                cols_order += ["Last Obs Yield", "Last Obs Year"]
                diag.yield_table(
                    df_table[["Region"] + cols_order],
                    out_path=plot_dir / f"yield_table_{country_lower}_{crop}_{model}.png",
                    title=f"Yield Forecast Summary \u2014 {country} {crop} ({model}, {current_year})",
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
                df_mape = (
                    df_mape.sort_values("Stage Name")
                    .groupby(["Region", "Harvest Year"], as_index=False).last()
                )

                diag.mape_bar_chart(
                    df_mape,
                    title=f"Mean MAPE by Region \u2014 {country} {crop} ({model})",
                    dir_out=plot_dir,
                    fname=f"mape_bar_{country_lower}_{crop}_{model}.png",
                    production_pct=prod_pct,
                )
                diag.mape_by_year(
                    df_mape,
                    title=f"MAPE by Year \u2014 {country} {crop} ({model})",
                    dir_out=plot_dir,
                    fname=f"mape_year_{country_lower}_{crop}_{model}.png",
                    threshold=20.0,
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
                area_map_dir = dir_outlook / "maps" / model
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
            dir_model = dir_outlook / "maps" / model
            os.makedirs(dir_model, exist_ok=True)
            _generate_outlook_map(
                dg, df_group, countries_with_data, crop, model,
                current_year, n_years, aggregation, dir_model,
                stage_name="combined", annotate_regions=False,
            )

        # Consolidated multi-country obs_anomaly maps — one per (crop, model, period)
        for (crop_val, model_val), df_group in df_all.groupby(["Crop", "Model"]):
            countries_with_data = df_group["Country"].unique().tolist()
            if len(countries_with_data) <= 1:
                continue
            obs_baselines_combined = _load_observed_baselines(countries_with_data, crop_val, parser, current_year=current_year)
            for period_label, df_obs in obs_baselines_combined.items():
                df_anom = df_group[
                    ["Country", "Region", "Country Region", "current_predicted"]
                ].merge(df_obs, on="Region", how="left")
                df_anom["obs_anomaly"] = np.where(
                    df_anom["obs_mean"] != 0,
                    (df_anom["current_predicted"] - df_anom["obs_mean"])
                    / df_anom["obs_mean"] * 100,
                    np.nan,
                )
                dir_obs_combined = dir_outlook / "maps" / model_val / "obs_anomaly" / period_label
                os.makedirs(dir_obs_combined, exist_ok=True)
                _generate_outlook_map(
                    dg, df_anom, countries_with_data, crop_val, model_val,
                    current_year, n_years, aggregation, dir_obs_combined,
                    col="obs_anomaly",
                    col_label=f"% departure from {period_label} observed mean\n{crop_val.title()}, {current_year}",
                    stage_name="combined", annotate_regions=False,
                )

        # Ensemble: mean across models (skip when only one model)
        n_models = df_all["Model"].nunique()
        df_ensemble = None
        if n_models > 1:
            df_ensemble = (
                df_all.groupby(
                    ["Country", "Region", "Country Region", "Crop", "Forecast Year"],
                    as_index=False,
                ).agg({
                    "outlook_index": "mean",
                    "current_predicted": "mean",
                    "hist_predicted": "mean",
                    "Stage Name": "last",
                })
            )
            df_ensemble["Model"] = "ensemble"

            dir_ens = dir_outlook / "maps" / "ensemble"
            os.makedirs(dir_ens, exist_ok=True)

            # Per-country ensemble maps
            for (country_val, crop_val), df_group in df_ensemble.groupby(["Country", "Crop"]):
                map_countries_val = countries if country_val == "pooled" else [country_val]
                stage_val = df_group["Stage Name"].iloc[0]
                _generate_outlook_map(
                    dg, df_group, map_countries_val, crop_val,
                    "ensemble", current_year, n_years, aggregation, dir_ens,
                    stage_name=stage_val, annotate_regions=False,
                )

            # Multi-country ensemble maps
            for crop_val, df_group in df_ensemble.groupby("Crop"):
                if len(df_group["Country"].unique()) > 1:
                    _generate_outlook_map(
                        dg, df_group, df_group["Country"].unique().tolist(), crop_val,
                        "ensemble", current_year, n_years, aggregation, dir_ens,
                        stage_name="combined", annotate_regions=False,
                    )

            # Ensemble observed-baseline anomaly maps
            for crop_val, df_ens_crop in df_ensemble.groupby("Crop"):
                countries_ens = df_ens_crop["Country"].unique().tolist()
                obs_baselines_ens = _load_observed_baselines(countries_ens, crop_val, parser, current_year=current_year)
                for period_label, df_obs in obs_baselines_ens.items():
                    df_ens_anom = df_ens_crop[
                        ["Country", "Region", "Country Region", "current_predicted"]
                    ].merge(df_obs, on="Region", how="left")
                    df_ens_anom["obs_anomaly"] = np.where(
                        df_ens_anom["obs_mean"] != 0,
                        (df_ens_anom["current_predicted"] - df_ens_anom["obs_mean"])
                        / df_ens_anom["obs_mean"] * 100,
                        np.nan,
                    )
                    dir_ens_obs = dir_ens / "obs_anomaly" / period_label
                    os.makedirs(dir_ens_obs, exist_ok=True)
                    _generate_outlook_map(
                        dg, df_ens_anom, countries_ens, crop_val, "ensemble", current_year,
                        n_years, aggregation, dir_ens_obs,
                        col="obs_anomaly",
                        col_label=f"% departure from {period_label} observed mean\n{crop_val.title()}, {current_year}",
                    )

        # Long-format CSV
        df_long = pd.concat([df_all] + ([df_ensemble] if df_ensemble is not None else []), ignore_index=True)
        csv_path = dir_outlook / f"yield_outlook_{scope}_{crops_str}_{current_year}.csv"
        df_long.to_csv(csv_path, index=False)
        logger.info(f"Outlook CSV saved to {csv_path}")

        # Wide-format CSV: one outlook_index column per model + ensemble column
        pivot_cols = ["Country", "Region", "Crop", "Forecast Year"]
        df_wide = df_all.pivot_table(
            index=pivot_cols, columns="Model", values="outlook_index"
        ).reset_index()
        df_wide.columns.name = None
        model_cols = [c for c in df_wide.columns if c not in pivot_cols]
        if len(model_cols) > 1:
            df_wide["ensemble"] = df_wide[model_cols].mean(axis=1)
        csv_wide = dir_outlook / f"yield_outlook_{scope}_{crops_str}_{current_year}_wide.csv"
        df_wide.to_csv(csv_wide, index=False)
        logger.info(f"Wide-format CSV saved to {csv_wide}")
    else:
        logger.warning("No outlook data generated — check DB has predictions.")

    # Diagnostic plots: scatter, MAPE bar, progression — always run if we
    # have predictions, even when outlook index computation fails.
    if df_pred_store:
        _generate_diagnostics(df_pred_store, dg, dir_outlook,
                              current_year=current_year, dict_config=dict_config,
                              db_path=db_path)

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


if __name__ == "__main__":
    run()
