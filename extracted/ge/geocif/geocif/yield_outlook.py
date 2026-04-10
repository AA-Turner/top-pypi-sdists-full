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


def _query_predictions(db_path, table, model, experiment_name="default"):
    """Query predictions from the SQLite database for a specific model.

    Returns DataFrame with columns: Country, Region, Harvest Year, Stage Name,
    Predicted Yield (tn per ha), Observed Yield (tn per ha).
    """
    if not db_path.exists():
        logger.error("Database not found: %s", db_path)
        return pd.DataFrame()

    con = sqlite3.connect(db_path)
    try:
        df = pd.read_sql(
            f'SELECT "Country", "Region", "Harvest Year", "Stage Name", '
            f'"Predicted Yield (tn per ha)", "Observed Yield (tn per ha)" '
            f'FROM "{table}" WHERE "Experiment Name" = ? AND "Model" = ?',
            con,
            params=(experiment_name, model),
        )
    except (pd.errors.DatabaseError, sqlite3.OperationalError) as e:
        logger.warning("Failed to query table '%s': %s", table, e)
        df = pd.DataFrame()
    finally:
        con.close()
    if not df.empty:
        if "Harvest Year" in df.columns:
            df["Harvest Year"] = df["Harvest Year"].astype(int)
        for col in ("Predicted Yield (tn per ha)", "Observed Yield (tn per ha)"):
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


def _generate_diagnostics(df_pred_store, dg, dir_outlook):
    """Generate scatter, MAPE bar chart, and MAPE map for each (country, crop, model).

    Called after the main outlook loop.  Uses the raw per-year obs/pred DataFrame
    collected during _query_predictions() to produce model-accuracy diagnostics.
    Output goes to outlook/plots/{model}/{country}/ and outlook/maps/{model}/.
    """
    from .viz import diagnostics as diag

    for (country, crop, model), df in df_pred_store.items():
        obs_col  = "Observed Yield (tn per ha)"
        pred_col = "Predicted Yield (tn per ha)"
        df = df.dropna(subset=[obs_col, pred_col]) if obs_col in df.columns else pd.DataFrame()
        if df.empty:
            continue

        countries_display = [country.title().replace("_", " ")]
        dir_plots = dir_outlook / "plots" / model / country
        dir_maps  = dir_outlook / "maps"  / model
        os.makedirs(dir_plots, exist_ok=True)
        os.makedirs(dir_maps, exist_ok=True)

        title = f"{country.title()} {crop.title()} — {model}"

        # Scatter: observed vs predicted, all years
        diag.scatter_obs_pred(df, title, dir_plots,
                              f"scatter_{country}_{crop}_{model}.png")

        # MAPE bar chart: mean MAPE per region
        df_mape = (
            df.assign(
                MAPE=lambda d: (
                    (d[pred_col] - d[obs_col]).abs() / d[obs_col].replace(0, np.nan) * 100
                )
            )
            .groupby("Region", as_index=False)["MAPE"].mean()
        )
        diag.mape_bar_chart(df_mape, title, dir_plots,
                            f"mape_{country}_{crop}_{model}.png")

        # MAPE choropleth map
        df_mape["Country Region"] = (
            country.lower().replace("_", " ") + " " + df_mape["Region"].str.lower()
        )
        df_mape = df_mape.rename(columns={"MAPE": "Mean Absolute Percentage Error"})
        dg_sub = dg[dg["ADM0_NAME"].isin(countries_display)].copy()
        diag.mape_choropleth(
            dg_sub, df_mape, countries_display, False,
            dir_maps, f"mape_map_{country}_{crop}_{model}.png",
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
        reuse_db=None, use_latest_stage=True, fdw_export=False):
    """Main entry point for yield outlook map generation.

    1. Override forecast_seasons to cover [current_year - n_years, ..., current_year]
    2. Run the ML pipeline via gc.execute_models()
    3. Query predictions from the database
    4. Compute outlook index per region
    5. Generate diverging choropleth maps and CSV
    6. Optionally export FDW forecast CSV (fdw_export=True)

    Args:
        path_config_files: List of config file paths.
        current_year: Forecast year (default: this year).
        n_years: Number of historical years for comparison (default: config or 10).
        aggregation: 'mean' or 'median' (default: config or 'mean').
        reuse_db: Path to existing outlook DB to skip ML and regenerate maps only.
        use_latest_stage: If True (default), use latest available stage per
            region+year. Handles mismatched stage names across years/countries.
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

    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    experiment_name = parser.get("DEFAULT", "experiment_name", fallback="default")

    if reuse_db is not None:
        # ---- Skip ML, reuse existing DB ----
        reuse_path = Path(reuse_db)
        if not reuse_path.exists():
            logger.error("Reuse DB not found: %s", reuse_path)
            return
        outlook_db = reuse_path.name
        logger.info("Reusing existing outlook DB: %s", reuse_path)
    else:
        # ---- Step 1: Run ML pipeline for all needed years ----
        outlook_seasons = list(range(current_year - n_years, current_year + 1))
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

        params = [
            ("Countries", countries),
            ("Forecast year", str(current_year)),
            ("Lookback years", str(n_years)),
            ("Seasons", f"{outlook_seasons[0]}-{outlook_seasons[-1]}"),
            ("Aggregation", aggregation),
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
            logger.info("Yield outlook: %s %s %s", country, crop, model)

            df = _query_predictions(db_path, country_crop, model, experiment_name="outlook")
            if df.empty:
                logger.warning("No predictions found for %s %s %s", country, crop, model)
                continue

            # Get all stages available for current year
            df_current = df[df["Harvest Year"] == current_year]
            if df_current.empty:
                logger.warning(
                    "No predictions for year %d in %s %s %s",
                    current_year, country, crop, model,
                )
                continue

            if is_pooled:
                annotate = False
                map_countries = countries
            else:
                annotate = parser.getboolean(
                    country, "annotate_regions", fallback=False
                )
                map_countries = [country]

            # Store raw predictions for diagnostics
            df_pred_store[(country, crop, model)] = df

            # Compute outlook index
            df_outlook = _compute_outlook_index(
                df, current_year, n_years, aggregation,
                use_latest_stage=use_latest_stage,
            )
            if df_outlook.empty:
                logger.warning(
                    "Could not compute outlook for %s %s %s",
                    country, crop, model,
                )
                continue

            # Use current year's stage name for labeling
            stage_name = df_current["Stage Name"].iloc[-1]

            n_hist = len(
                df[
                    (df["Harvest Year"] < current_year)
                    & (df["Harvest Year"] >= current_year - n_years)
                ]["Harvest Year"].unique()
            )
            if n_hist < 3:
                logger.warning(
                    "Only %d historical years for %s %s %s (requested %d)",
                    n_hist, country, crop, model, n_years,
                )

            df_outlook["Crop"] = crop
            df_outlook["Model"] = model
            df_outlook["Stage Name"] = stage_name
            df_outlook["Forecast Year"] = current_year
            all_outlook_frames.append(df_outlook)

            # Generate map — saved in maps/{model} subfolder
            dir_model = dir_outlook / "maps" / model
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
                annotate_regions=annotate,
            )
            logger.info(
                "Map saved: %s",
                dir_model
                / f"yield_outlook_{'_'.join(map_countries)}_{crop}_{model}_{stage_name}_{current_year}.png",
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
            annotate_val = (
                parser.getboolean(country_val, "annotate_regions", fallback=False)
                if country_val != "pooled" else False
            )
            stage_val = df_group["Stage Name"].iloc[0]
            _generate_outlook_map(
                dg, df_group, map_countries_val, crop_val,
                "ensemble", current_year, n_years, aggregation, dir_ens,
                stage_name=stage_val, annotate_regions=annotate_val,
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
        logger.info("Outlook CSV saved to %s", csv_path)

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
        logger.info("Wide-format CSV saved to %s", csv_wide)
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
