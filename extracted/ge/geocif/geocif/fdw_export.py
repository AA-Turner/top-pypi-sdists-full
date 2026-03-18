"""FDW (Yield Intercomparison Dashboard) forecast CSV export.

Generates Template 1 (Yield Forecast) CSVs from geocif's SQLite database,
conforming to the Yield Intercomparison Dashboard Submission Guidelines.
"""

import ast
import logging
import os
import sqlite3
from pathlib import Path

import arrow as ar
import numpy as np
import pandas as pd

from geocif import __version__

logger = logging.getLogger(__name__)


def _query_forecast(db_path, table, model, experiment_name, forecast_year):
    """Query forecast-year predictions from the database.

    Returns DataFrame with columns needed for FDW export.
    """
    if not db_path.exists():
        logger.error("Database not found: %s", db_path)
        return pd.DataFrame()

    con = sqlite3.connect(db_path)
    try:
        df = pd.read_sql(
            f'SELECT "Country", "Region", "Season", "Harvest Year", '
            f'"Stage Name", "Date", '
            f'"Predicted Yield (tn per ha)" '
            f'FROM "{table}" '
            f'WHERE "Experiment Name" = ? AND "Model" = ? '
            f'AND "Harvest Year" = ?',
            con,
            params=(experiment_name, model, forecast_year),
        )
    except (pd.errors.DatabaseError, sqlite3.OperationalError) as e:
        logger.warning("Failed to query table '%s': %s", table, e)
        df = pd.DataFrame()
    finally:
        con.close()

    if not df.empty:
        df["Harvest Year"] = df["Harvest Year"].astype(int)
        df["Season"] = pd.to_numeric(df["Season"], errors="coerce").astype("Int64")
        df["Predicted Yield (tn per ha)"] = pd.to_numeric(
            df["Predicted Yield (tn per ha)"], errors="coerce"
        )
    return df


def _load_hvstat(parser):
    """Load the hvstat CSV and extract planting/harvest month info.

    Returns a DataFrame with columns:
    fnid, product, season_name, planting_month, harvest_month
    deduplicated to the most recent row per (fnid, product, season_name).
    """
    dir_stats = Path(parser.get("PATHS", "dir_production_statistics"))
    hvstat_fn = parser.get(
        "DEFAULT", "production_statistics_file",
        fallback="hvstat_africa_data_v1.0.csv",
    )
    hvstat_path = dir_stats / hvstat_fn
    if not hvstat_path.exists():
        logger.warning("hvstat file not found: %s", hvstat_path)
        return pd.DataFrame()

    df = pd.read_csv(hvstat_path, low_memory=False)

    needed = ["fnid", "product", "season_name", "planting_month", "harvest_month"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        logger.warning("hvstat missing columns %s — month data will be blank", missing)
        return pd.DataFrame()

    # Keep only needed columns, drop NaN months, take most recent per group
    df = df[needed + ["harvest_year"]].dropna(subset=["planting_month", "harvest_month"])
    df = (
        df.sort_values("harvest_year")
        .groupby(["fnid", "product", "season_name"])
        .last()
        .reset_index()
    )
    return df[needed]


def _build_shapefile_lookup(dg, country_admin_levels):
    """Build a lookup from (country, region) -> (ADM_ID, ADM1_NAME, ADM2_NAME).

    For admin_2 countries the join key (_region_lc) is set to the ADM2 name
    (district), matching how the DB stores Region for those countries.
    For admin_1 countries the join key is ADM1 (province).

    Returns a DataFrame with lowercase country/region for joining.
    """
    cols = ["ADM0_NAME", "ADM1_NAME"]
    if "ADM2_NAME" in dg.columns:
        cols.append("ADM2_NAME")
    if "ADM_ID" in dg.columns:
        cols.append("ADM_ID")

    lookup = dg[cols].drop_duplicates().copy()
    lookup["_country_lc"] = lookup["ADM0_NAME"].str.lower().str.replace("_", " ")

    def _pick_region(row):
        admin = country_admin_levels.get(row["_country_lc"], "admin_1")
        if admin == "admin_2" and pd.notna(row.get("ADM2_NAME")):
            return str(row["ADM2_NAME"]).lower()
        return str(row["ADM1_NAME"]).lower()

    lookup["_region_lc"] = lookup.apply(_pick_region, axis=1)
    lookup = lookup.drop_duplicates(subset=["_country_lc", "_region_lc"])
    return lookup


def _compute_planted_year(harvest_year, planting_month, harvest_month):
    """Infer planting year from harvest year and month relationship."""
    if pd.isna(planting_month) or pd.isna(harvest_month) or pd.isna(harvest_year):
        return ""
    if int(planting_month) > int(harvest_month):
        return int(harvest_year) - 1
    return int(harvest_year)


def _parse_model_run_date(date_str):
    """Convert geocif Date format (MMMM_DD_YYYY) to YYYY-MM-DD."""
    try:
        return ar.get(date_str, "MMMM_DD_YYYY").format("YYYY-MM-DD")
    except Exception:
        return ""


def export_forecast(
    parser,
    db_path=None,
    forecast_year=None,
    forecast_issue_date=None,
    source_name_version="FDW",
    group="NASA Harvest",
    dir_out=None,
):
    """Export forecast predictions as FDW Template 1 CSV.

    Args:
        parser: ConfigParser with geocif config loaded.
        db_path: Path to SQLite database. If None, uses default from config.
        forecast_year: Year to export. Defaults to current year.
        forecast_issue_date: YYYY-MM-DD string. Defaults to today.
        source_name_version: Value for source_name_version column.
        group: Research group name.
        dir_out: Output directory. Defaults to ml/analysis/{today}/fdw/.

    Returns:
        Path to the saved CSV, or None if no data.
    """
    from geocif.yield_outlook import _load_shapefiles

    # Defaults
    if forecast_year is None:
        forecast_year = ar.utcnow().to("America/New_York").year
    if forecast_issue_date is None:
        forecast_issue_date = ar.utcnow().to("America/New_York").format("YYYY-MM-DD")

    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    experiment_name = parser.get("DEFAULT", "experiment_name", fallback="default")
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")

    if db_path is None:
        dir_output = Path(parser.get("PATHS", "dir_output")) / project_name
        db_name = parser.get("DEFAULT", "db")
        db_path = dir_output / "ml" / "db" / db_name
    else:
        db_path = Path(db_path)
        dir_output = Path(parser.get("PATHS", "dir_output")) / project_name

    if dir_out is None:
        today = ar.utcnow().to("America/New_York").format("MMMM_DD_YYYY")
        dir_out = dir_output / "ml" / "analysis" / today / "fdw"
    else:
        dir_out = Path(dir_out)
    os.makedirs(dir_out, exist_ok=True)

    model_version = f"geocif v{__version__}"

    # Load shapefiles and config
    dg, dict_config = _load_shapefiles(parser)

    # Load hvstat for planting/harvest months
    df_hvstat = _load_hvstat(parser)

    # Build per-country admin level lookup from config
    country_admin_levels = {}
    for country in countries:
        admin = parser.get(country, "admin_level", fallback="admin_1")
        country_admin_levels[country.lower().replace("_", " ")] = admin

    # Build shapefile lookup once (handles mixed admin levels)
    shp_lookup = _build_shapefile_lookup(dg, country_admin_levels)

    all_rows = []

    for country_crop, config in dict_config.items():
        crop = config["crops"]
        country = country_crop.replace(f"_{crop}", "")

        for model in config["models"]:
            logger.info("FDW export: %s %s %s", country, crop, model)

            df_pred = _query_forecast(
                db_path, country_crop, model, experiment_name, forecast_year
            )
            if df_pred.empty:
                logger.warning(
                    "No forecast predictions for %s %s %s year=%d",
                    country, crop, model, forecast_year,
                )
                continue

            # Keep latest stage per (Country, Region)
            df_latest = (
                df_pred.sort_values("Stage Name")
                .groupby(["Country", "Region"])
                .last()
                .reset_index()
            )

            # Join with shapefile to get FNID
            df_latest["_country_lc"] = (
                df_latest["Country"].str.lower().str.replace("_", " ")
            )
            df_latest["_region_lc"] = df_latest["Region"].str.lower()

            df_merged = df_latest.merge(
                shp_lookup,
                on=["_country_lc", "_region_lc"],
                how="left",
            )

            # Join with hvstat for planting/harvest month and season_name
            if not df_hvstat.empty and "ADM_ID" in df_merged.columns:
                # Normalize crop name for matching hvstat product column
                crop_title = crop.title().replace("_", " ")
                df_hvstat_crop = df_hvstat[
                    df_hvstat["product"].str.lower() == crop_title.lower()
                ].copy()

                if not df_hvstat_crop.empty:
                    df_merged = df_merged.merge(
                        df_hvstat_crop.rename(columns={"fnid": "ADM_ID"}),
                        on="ADM_ID",
                        how="left",
                    )
                else:
                    df_merged["planting_month"] = np.nan
                    df_merged["harvest_month"] = np.nan
                    df_merged["season_name"] = np.nan
            else:
                df_merged["planting_month"] = np.nan
                df_merged["harvest_month"] = np.nan
                df_merged["season_name"] = np.nan

            # Parse model run date
            date_model_run = ""
            if "Date" in df_merged.columns:
                date_model_run = _parse_model_run_date(
                    df_merged["Date"].iloc[0]
                )

            # Build FDW rows
            for _, row in df_merged.iterrows():
                row_country_lc = row.get("_country_lc", "")
                admin_level = country_admin_levels.get(row_country_lc, "admin_1")
                is_admin2 = admin_level == "admin_2"

                # admin_1: Region is province; admin_2: Region is district
                if is_admin2:
                    adm0 = row["ADM0_NAME"] if pd.notna(row.get("ADM0_NAME")) else row.get("Country", "")
                    adm1 = row["ADM1_NAME"] if pd.notna(row.get("ADM1_NAME")) else ""
                    adm2 = row.get("Region", "")
                else:
                    adm0 = row["ADM0_NAME"] if pd.notna(row.get("ADM0_NAME")) else row.get("Country", "")
                    adm1 = row.get("Region", "")
                    adm2 = ""

                yield_val = row.get("Predicted Yield (tn per ha)", "")
                if pd.notna(yield_val) and yield_val != "" and float(yield_val) < 0:
                    yield_val = ""

                fdw_row = {
                    "source_id": row.get("ADM_ID", ""),
                    "source_name_version": source_name_version,
                    "admin_0": adm0,
                    "admin_1": adm1,
                    "admin_2": adm2,
                    "admin_3": "",
                    "planted_year": _compute_planted_year(
                        row.get("Harvest Year"),
                        row.get("planting_month"),
                        row.get("harvest_month"),
                    ),
                    "approx_planted_month": row.get("planting_month", ""),
                    "harvest_year": row.get("Harvest Year", ""),
                    "approx_harvest_month": row.get("harvest_month", ""),
                    "crop": crop.title().replace("_", " "),
                    "crop_season": row.get("season_name", ""),
                    "forecast_issue_date": forecast_issue_date,
                    "date_model_run": date_model_run,
                    "input_croptype_product": "",
                    "group": group,
                    "model_version": model_version,
                    "yield_fcst": yield_val,
                    "is_final": "yes",
                    "notes": "",
                }
                all_rows.append(fdw_row)

    if not all_rows:
        logger.warning("No FDW data to export.")
        return None

    df_fdw = pd.DataFrame(all_rows)

    # Replace NaN with empty string for clean CSV
    df_fdw = df_fdw.fillna("")

    # Determine filename scope
    if len(countries) > 1:
        scope = "africa"
    else:
        scope = countries[0].lower().replace(" ", "_")

    # Determine admin unit from config
    admin_levels = {config["admin_zone"] for config in dict_config.values()}
    admin_unit = "admin2" if "admin_2" in admin_levels else "admin1"

    fname = f"geocif_{scope}_{admin_unit}_forecast_{forecast_issue_date}.csv"
    csv_path = dir_out / fname
    df_fdw.to_csv(csv_path, index=False)
    logger.info("FDW forecast CSV saved to %s (%d rows)", csv_path, len(df_fdw))

    return csv_path


def run(path_config_files=None, db_path=None, forecast_year=None, **kwargs):
    """Convenience entry point — accepts config file paths.

    Usage:
        from geocif import fdw_export
        fdw_export.run(["/path/to/geocif.txt"], db_path="/path/to/db")
    """
    from geocif import logger as log

    if path_config_files is None:
        path_config_files = [Path("../config/geocif.txt")]

    _, parser = log.setup_logger_parser(path_config_files)
    return export_forecast(parser, db_path=db_path, forecast_year=forecast_year, **kwargs)
