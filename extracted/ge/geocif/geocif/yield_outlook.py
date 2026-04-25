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

warnings.simplefilter(action="ignore", category=FutureWarning)

logger = logging.getLogger(__name__)

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
    from geoprepare.georegion import get_boundary_col_mapping

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

        # Load shapefile
        shp_file = parser.get(country, "boundary_file")
        dg_country = gpd.read_file(
            dir_boundary_files / shp_file,
            engine="pyogrio",
        )

        # Rename columns using config-driven mapping
        rename = get_boundary_col_mapping(parser, shp_file)
        targets = set(rename.values())
        sources = set(rename.keys())
        conflicting = [
            c for c in dg_country.columns if c in targets and c not in sources
        ]
        if conflicting:
            dg_country = dg_country.drop(columns=conflicting)
        dg_country = dg_country.rename(columns=rename)

        if "ADM0_NAME" not in dg_country.columns:
            dg_country.loc[:, "ADM0_NAME"] = country.title().replace("_", " ")

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

    # Create "Country Region" merge column (same pattern as analysis.py:1229-1242)
    dg["Country Region"] = dg["ADM0_NAME"]
    dg["Country Region"] = dg["Country Region"].str.cat(dg["ADM1_NAME"], sep=" ")
    if "ADM2_NAME" in dg.columns:
        dg.loc[dg["ADM2_NAME"].notna(), "Country Region"] = (
            dg["ADM0_NAME"] + " " + dg["ADM2_NAME"]
        )
    dg["Country Region"] = dg["Country Region"].str.lower().replace("_", " ")

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
                                    stage_name=""):
    """Generate scatter, MAPE bar chart, and MAPE map for one stage.

    Args:
        df: DataFrame with obs/pred columns for this stage.
        country, crop, model: Identifiers.
        dg: GeoDataFrame for choropleth maps.
        dir_outlook: Base output directory.
        stage_name: Stage name suffix for filenames/subdirectories.
    """
    from .viz import diagnostics as diag

    obs_col = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"
    df = df.dropna(subset=[obs_col, pred_col]) if obs_col in df.columns else pd.DataFrame()
    if df.empty:
        return

    countries_display = [country.title().replace("_", " ")]
    stage_safe = stage_name.replace(" ", "_") if stage_name else ""
    stage_suffix = f"_{stage_safe}" if stage_safe else ""

    dir_plots = dir_outlook / "plots" / model / country
    dir_maps = dir_outlook / "maps" / model
    if stage_safe:
        dir_plots = dir_plots / stage_safe
        dir_maps = dir_maps / stage_safe
    os.makedirs(dir_plots, exist_ok=True)
    os.makedirs(dir_maps, exist_ok=True)

    title = f"{country.title()} {crop.title()} — {model}"
    if stage_name:
        title += f" ({stage_name})"

    diag.scatter_obs_pred(df, title, dir_plots,
                          f"scatter_{country}_{crop}_{model}{stage_suffix}.png")

    df_mape = (
        df.assign(
            MAPE=lambda d: (
                (d[pred_col] - d[obs_col]).abs() / d[obs_col].replace(0, np.nan) * 100
            )
        )
        .groupby("Region", as_index=False)["MAPE"].mean()
    )
    diag.mape_bar_chart(df_mape, title, dir_plots,
                        f"mape_bar_{country}_{crop}_{model}{stage_suffix}.png")

    df_mape["Country Region"] = (
        country.lower().replace("_", " ") + " " + df_mape["Region"].str.lower()
    )
    df_mape = df_mape.rename(columns={"MAPE": "Mean Absolute Percentage Error"})
    dg_sub = dg[dg["ADM0_NAME"].isin(countries_display)].copy()
    diag.mape_choropleth(
        dg_sub, df_mape, countries_display, False,
        dir_maps, f"mape_map_{country}_{crop}_{model}{stage_suffix}.png",
    )


def _plot_mape_progression(df, country, crop, model, dir_outlook):
    """Plot MAPE progression across time steps for multi-stage runs.

    Produces a line chart with:
    - One thin line per region (MAPE at each stage)
    - A bold line for the area-weighted national MAPE

    Args:
        df: DataFrame with obs/pred/stage columns for all stages.
        country, crop, model: Identifiers.
        dir_outlook: Base output directory.
    """
    import matplotlib.pyplot as plt

    obs_col = "Observed Yield (tn per ha)"
    pred_col = "Predicted Yield (tn per ha)"
    df = df.dropna(subset=[obs_col, pred_col])
    if df.empty or "Stage Name" not in df.columns:
        return

    df = df[df[obs_col] != 0].copy()
    df["MAPE"] = (df[pred_col] - df[obs_col]).abs() / df[obs_col] * 100

    stages_sorted = sorted(df["Stage Name"].dropna().unique())
    if len(stages_sorted) < 2:
        return

    # Per-region MAPE at each stage
    region_mape = (
        df.groupby(["Stage Name", "Region"])["MAPE"]
        .mean()
        .reset_index()
    )

    # Area-weighted national MAPE at each stage
    has_area = "Area (ha)" in df.columns and df["Area (ha)"].notna().any()
    national_rows = []
    for stage in stages_sorted:
        ds = df[df["Stage Name"] == stage]
        if has_area:
            region_stats = ds.groupby("Region").agg(
                mape=("MAPE", "mean"),
                area=("Area (ha)", "first"),
            ).dropna()
            if region_stats.empty or region_stats["area"].sum() == 0:
                national_rows.append({"Stage Name": stage, "National MAPE": ds["MAPE"].mean()})
            else:
                weighted = (region_stats["mape"] * region_stats["area"]).sum() / region_stats["area"].sum()
                national_rows.append({"Stage Name": stage, "National MAPE": weighted})
        else:
            national_rows.append({"Stage Name": stage, "National MAPE": ds["MAPE"].mean()})
    df_national = pd.DataFrame(national_rows)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))

    regions = sorted(region_mape["Region"].unique())
    cmap = plt.cm.get_cmap("tab20", max(len(regions), 1))
    for i, region in enumerate(regions):
        rdf = region_mape[region_mape["Region"] == region]
        rdf = rdf.set_index("Stage Name").reindex(stages_sorted)
        ax.plot(stages_sorted, rdf["MAPE"].values, color=cmap(i),
                alpha=0.4, linewidth=1, label=region)

    # National line
    df_national = df_national.set_index("Stage Name").reindex(stages_sorted)
    label = "National (area-weighted)" if has_area else "National (mean)"
    ax.plot(stages_sorted, df_national["National MAPE"].values,
            color="black", linewidth=2.5, marker="o", markersize=5, label=label)

    ax.set_xlabel("Stage")
    ax.set_ylabel("MAPE (%)")
    ax.set_title(f"MAPE Progression — {country.title()} {crop.title()} ({model})")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=7, ncol=1)
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.tight_layout()

    dir_plots = dir_outlook / "plots" / model / country
    os.makedirs(dir_plots, exist_ok=True)
    fig.savefig(dir_plots / f"mape_progression_{country}_{crop}_{model}.png",
                dpi=250, bbox_inches="tight")
    plt.close(fig)


def _generate_diagnostics(df_pred_store, dg, dir_outlook):
    """Generate scatter, MAPE bar chart, and MAPE map per (country, crop, model, stage).

    When multi-step results are present (multiple Stage Names), produces
    separate plots per stage, an aggregate, and a MAPE progression plot.
    """
    for (country, crop, model), df in df_pred_store.items():
        if df.empty:
            continue

        # Check for multiple stages
        stages = df["Stage Name"].dropna().unique() if "Stage Name" in df.columns else []

        if len(stages) > 1:
            for stage_name in sorted(stages):
                df_stage = df[df["Stage Name"] == stage_name]
                _generate_diagnostics_for_stage(
                    df_stage, country, crop, model, dg, dir_outlook, stage_name
                )
            # MAPE progression across time steps
            _plot_mape_progression(df, country, crop, model, dir_outlook)

        # Always produce an aggregate (latest stage or all data)
        _generate_diagnostics_for_stage(df, country, crop, model, dg, dir_outlook)


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

    stage_label = f", stage {stage_name}" if stage_name else ""
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


def run(path_config_files=None, current_year=None, n_years=None, aggregation=None,
        reuse_db=None, use_latest_stage=True, fdw_export=False, since_year=None):
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
    """
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
        outlook_db = ar.utcnow().to("America/New_York").format("[outlook_]MM[_]DD[_]YYYY[.db]")
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

        params = [
            ("Countries", countries),
            ("Crops", crops),
            ("Models", models),
            ("Forecast year", str(current_year)),
            ("Outlook index window", f"{n_years} years"),
            ("Seasons", f"{outlook_seasons[0]}-{outlook_seasons[-1]}"),
            ("Aggregation", aggregation),
            ("Stage alignment", str(parser.getboolean("ML", "align_hindcast_stage", fallback=False))),
            ("Pooled", str(pool_countries_flag)),
            ("DB", parser.get("DEFAULT", "db")),
            ("Total combinations", str(len(inputs))),
        ]
        ut.display_run_summary("GeoCIF Yield Outlook", params, wait=10)

        if pool_countries_flag:
            gc.execute_models(inputs, logger_obj, parser, loop_fn=gc.loop_execute_pooled)
        else:
            gc.execute_models(inputs, logger_obj, parser)

        # Restore original config values
        for country, orig in originals.items():
            parser.set(country, "forecast_seasons", orig)
        parser.set("DEFAULT", "experiment_name", experiment_name)
        parser.set("DEFAULT", "db", orig_db)

    # ---- Step 2: Load shapefiles ----
    dg, dict_config = _load_shapefiles(parser)

    # ---- Step 3: Query DB, compute outlook, generate maps ----
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    dir_output = Path(parser.get("PATHS", "dir_output")) / project_name
    if reuse_db is not None:
        db_path = Path(reuse_db)
    else:
        db_path = dir_output / "ml" / "db" / outlook_db

    today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY")
    dir_outlook = dir_output / "ml" / "analysis" / today / "outlook"
    os.makedirs(dir_outlook, exist_ok=True)

    all_outlook_frames = []
    df_pred_store = {}  # keyed by (country, crop, model) for diagnostics

    for country_crop, config in dict_config.items():
        crop = config["crops"]
        country = country_crop.replace(f"_{crop}", "")
        is_pooled = country == "pooled"
        models = config["models"]
        obs_baselines = _load_observed_baselines([country], crop, parser, current_year=current_year)

        for model in models:
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

            # Determine which stages to produce maps for
            available_stages = sorted(df_current["Stage Name"].dropna().unique())
            if use_latest_stage or len(available_stages) <= 1:
                stages_to_map = [available_stages[-1]] if available_stages else []
            else:
                stages_to_map = available_stages

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
                stage_safe = stage_name.replace(" ", "_")
                dir_model = dir_outlook / "maps" / model
                if len(available_stages) > 1:
                    dir_model = dir_model / stage_safe
                os.makedirs(dir_model, exist_ok=True)
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
                _countries_str = "_".join(map_countries)
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
                label=f"Predicted yield (tn/ha)\n{crop.title()}, {current_year}, stage {stage_name}",
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
                cols_order = ["Predicted Yield", "lower CI", "upper CI"]
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

        # Ensemble: mean of outlook_index / current_predicted / hist_predicted across models
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

        # Diagnostic plots: scatter, MAPE bar, MAPE map per (country, crop, model)
        _generate_diagnostics(df_pred_store, dg, dir_outlook)

        # Long-format CSV: all individual-model rows + ensemble rows
        df_long = pd.concat([df_all, df_ensemble], ignore_index=True)
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

    # Optional FDW forecast CSV export
    if fdw_export:
        from geocif.fdw_export import export_forecast

        export_forecast(
            parser,
            db_path=db_path,
            forecast_year=current_year,
            experiment_name="outlook",
            n_years=10,
        )


if __name__ == "__main__":
    run()
