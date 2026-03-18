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
    Predicted Yield (tn per ha).
    """
    if not db_path.exists():
        logger.error("Database not found: %s", db_path)
        return pd.DataFrame()

    con = sqlite3.connect(db_path)
    try:
        df = pd.read_sql(
            f'SELECT "Country", "Region", "Harvest Year", "Stage Name", '
            f'"Predicted Yield (tn per ha)" '
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
        if "Predicted Yield (tn per ha)" in df.columns:
            df["Predicted Yield (tn per ha)"] = pd.to_numeric(
                df["Predicted Yield (tn per ha)"], errors="coerce"
            )
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
):
    """Generate a diverging choropleth map of the yield outlook index."""
    col = "outlook_index"

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
    plot.plot_map(
        dg,
        df_outlook,
        merge_col="Country Region",
        name_country=countries_display,
        name_col=col,
        dir_out=dir_out,
        fname=fname,
        label=f"% departure from {n_years}-yr {aggregation}\n{crop.title()}, {current_year}{stage_label}",
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
        orig_parallel = parser.get("DEFAULT", "do_parallel_ml", fallback=None)
        parser.set("DEFAULT", "do_parallel_ml", "False")

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
        if orig_parallel is not None:
            parser.set("DEFAULT", "do_parallel_ml", orig_parallel)
        elif parser.has_option("DEFAULT", "do_parallel_ml"):
            parser.remove_option("DEFAULT", "do_parallel_ml")

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

    for country_crop, config in dict_config.items():
        crop = config["crops"]
        country = country_crop.replace(f"_{crop}", "")
        is_pooled = country == "pooled"
        models = config["models"]

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

            # Generate map
            _generate_outlook_map(
                dg,
                df_outlook,
                map_countries,
                crop,
                model,
                current_year,
                n_years,
                aggregation,
                dir_outlook,
                stage_name=stage_name,
                annotate_regions=annotate,
            )
            logger.info(
                "Map saved: %s",
                dir_outlook
                / f"yield_outlook_{country}_{crop}_{model}_{stage_name}_{current_year}.png",
            )

    # ---- Consolidated maps (all countries on one map) ----
    if all_outlook_frames:
        df_all = pd.concat(all_outlook_frames, ignore_index=True)
        for (crop, model), df_group in df_all.groupby(
            ["Crop", "Model"]
        ):
            countries_with_data = df_group["Country"].unique().tolist()
            if len(countries_with_data) <= 1:
                continue
            _generate_outlook_map(
                dg,
                df_group,
                countries_with_data,
                crop,
                model,
                current_year,
                n_years,
                aggregation,
                dir_outlook,
                stage_name="combined",
                annotate_regions=False,
            )

    # Save combined CSV
    if all_outlook_frames:
        df_all = pd.concat(all_outlook_frames, ignore_index=True)
        csv_path = dir_outlook / f"yield_outlook_{current_year}.csv"
        df_all.to_csv(csv_path, index=False)
        logger.info("Outlook CSV saved to %s", csv_path)
    else:
        logger.warning("No outlook data generated — check DB has predictions.")

    # Optional FDW forecast CSV export
    if fdw_export:
        from geocif.fdw_export import export_forecast

        export_forecast(
            parser,
            db_path=db_path,
            forecast_year=current_year,
        )


if __name__ == "__main__":
    run()
