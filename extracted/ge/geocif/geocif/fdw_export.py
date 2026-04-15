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


_CANON_PRED = "Predicted Yield (tn per ha)"


def _resolve_pred_col(table_cols):
    """Find the DB's Predicted-yield column (prefix ``Predicted `` + ``Yield``).

    Handles configs with ``rename_target = True`` + ``new_name_target = Yield``
    where the DB stores ``"Predicted Yield"`` instead of the canonical
    ``"Predicted Yield (tn per ha)"``.
    """
    return next(
        (c for c in table_cols if c.startswith("Predicted ") and "Yield" in c),
        None,
    )


def _query_forecast(db_path, table, model, experiment_name, forecast_year, min_year=None):
    """Query forecast-year predictions from the database.

    Returns DataFrame with columns needed for FDW export, with the
    Predicted-yield column renamed to the canonical form regardless of
    the user's ``rename_target`` config.  If min_year is set, returns all
    years in [min_year, forecast_year].
    """
    if not db_path.exists():
        logger.error(f"Database not found: {db_path}")
        return pd.DataFrame()

    con = sqlite3.connect(db_path)
    try:
        table_cols = pd.read_sql(f'PRAGMA table_info("{table}")', con)["name"].tolist()
        pred_col = _resolve_pred_col(table_cols)
        if pred_col is None:
            logger.warning(f"Table '{table}' missing Predicted yield column")
            return pd.DataFrame()

        if min_year is not None and min_year < forecast_year:
            df = pd.read_sql(
                f'SELECT "Country", "Region", "Season", "Harvest Year", '
                f'"Stage Name", "Date", "{pred_col}" '
                f'FROM "{table}" '
                f'WHERE "Experiment Name" = ? AND "Model" = ? '
                f'AND "Harvest Year" >= ? AND "Harvest Year" <= ?',
                con,
                params=(experiment_name, model, min_year, forecast_year),
            )
        else:
            df = pd.read_sql(
                f'SELECT "Country", "Region", "Season", "Harvest Year", '
                f'"Stage Name", "Date", "{pred_col}" '
                f'FROM "{table}" '
                f'WHERE "Experiment Name" = ? AND "Model" = ? '
                f'AND "Harvest Year" = ?',
                con,
                params=(experiment_name, model, forecast_year),
            )
    except (pd.errors.DatabaseError, sqlite3.OperationalError) as e:
        logger.warning(f"Failed to query table '{table}': {e}")
        df = pd.DataFrame()
    finally:
        con.close()

    if not df.empty:
        # Rename to canonical form so downstream code keeps using the
        # canonical column name regardless of rename_target config.
        if pred_col and pred_col != _CANON_PRED:
            df = df.rename(columns={pred_col: _CANON_PRED})
        df["Harvest Year"] = df["Harvest Year"].astype(int)
        df["Season"] = pd.to_numeric(df["Season"], errors="coerce").astype("Int64")
        df[_CANON_PRED] = pd.to_numeric(df[_CANON_PRED], errors="coerce")
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
        logger.warning(f"hvstat file not found: {hvstat_path}")
        return pd.DataFrame()

    df = pd.read_csv(hvstat_path, low_memory=False)

    needed = ["fnid", "product", "season_name", "planting_month", "harvest_month"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        logger.warning(f"hvstat missing columns {missing} — month data will be blank")
        return pd.DataFrame()

    # Keep needed columns + area-related columns for national yield computation
    keep = needed + ["harvest_year", "country", "admin_1", "area"]
    keep = [c for c in keep if c in df.columns]
    df = df[keep].dropna(subset=["planting_month", "harvest_month"])
    df = (
        df.sort_values("harvest_year")
        .groupby(["fnid", "product", "season_name"])
        .last()
        .reset_index()
    )
    return df


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


def _query_area_weights(parser, crop, n_years=5):
    """Compute average area per (Country, Region) from CID indices CSVs.

    Reads {dir_output}/{project_name}/cid/indices/{method}/global/{Country}_{Crop}_statistics_{method}.csv
    for each country, extracts Area (ha), and computes the mean over the last
    n_years per region.

    Returns DataFrame with columns: Country, Region, avg_area.
    Country uses DB convention (lowercase with underscores).
    """
    empty = pd.DataFrame(columns=["Country", "Region", "avg_area"])

    dir_output = Path(parser.get("PATHS", "dir_output"))
    project_name = parser.get("DEFAULT", "project_name", fallback="geocif")
    method = parser.get("DEFAULT", "method", fallback="monthly_r")
    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))

    csv_dir = dir_output / project_name / "cid" / "indices" / method / "global"
    crop_title = crop.title().replace("_", " ")

    frames = []
    for country in countries:
        # CSV filenames use title case: "South Africa", "Madagascar"
        country_title = country.title().replace("_", " ")
        fname = f"{country_title}_{crop_title}_statistics_{method}.csv"
        csv_path = csv_dir / fname

        if not csv_path.exists():
            logger.warning(f"CID indices CSV not found: {csv_path}")
            continue

        logger.info(f"Reading CID area data: {csv_path}")
        df = pd.read_csv(csv_path, low_memory=False)
        if "Area (ha)" not in df.columns or "Region" not in df.columns:
            logger.warning(f"CID CSV missing required columns: {csv_path}")
            continue

        df["Area (ha)"] = pd.to_numeric(df["Area (ha)"], errors="coerce")
        df = df[df["Area (ha)"].notna() & (df["Area (ha)"] > 0)]
        if df.empty:
            continue

        if "Harvest Year" not in df.columns:
            logger.warning(f"CID CSV missing 'Harvest Year': {csv_path}")
            continue
        df["Harvest Year"] = pd.to_numeric(df["Harvest Year"], errors="coerce")
        # Normalize country to DB convention (lowercase with underscores)
        df["Country"] = country.lower().replace(" ", "_")

        frames.append(df[["Country", "Region", "Harvest Year", "Area (ha)"]])

    if not frames:
        return empty

    all_df = pd.concat(frames, ignore_index=True)

    # Per (Country, Region): take last n_years with data, compute mean area
    def _last_n_mean(g):
        return g.nlargest(n_years, "Harvest Year")["Area (ha)"].mean()

    avg = (
        all_df.groupby(["Country", "Region"])
        .apply(_last_n_mean)
        .reset_index(name="avg_area")
    )
    return avg


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
    experiment_name=None,
    n_years=1,
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
        experiment_name: Experiment name to query (e.g. "outlook"). If None,
            reads from parser DEFAULT section.
        n_years: Number of years to include, counting back from forecast_year.
            Default 1 (current year only). Set to e.g. 10 to include last 10 years.

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
    if experiment_name is None:
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
            logger.info(f"FDW export: {country} {crop} {model}")

            min_year = forecast_year - n_years if n_years > 1 else None
            df_pred = _query_forecast(
                db_path, country_crop, model, experiment_name, forecast_year,
                min_year=min_year,
            )
            if df_pred.empty:
                logger.warning(
                    f"No forecast predictions for {country} {crop} {model} year={forecast_year}"
                )
                continue

            # Keep latest stage per (Country, Region, Harvest Year)
            df_latest = (
                df_pred.sort_values("Stage Name")
                .groupby(["Country", "Region", "Harvest Year"])
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
                    # Deduplicate to one row per fnid: prefer primary seasons
                    # (Main, Long, etc.) over Annual, mirroring stats.py logic.
                    _PRIMARY = [
                        "Long", "Gu", "Season A", "First", "1st Season",
                        "Main", "Meher", "Main harvest", "Summer", "Wet",
                    ]
                    df_hvstat_crop["_rank"] = df_hvstat_crop["season_name"].map(
                        lambda s: _PRIMARY.index(s) if s in _PRIMARY else len(_PRIMARY)
                    )
                    df_hvstat_crop = (
                        df_hvstat_crop.sort_values("_rank")
                        .drop_duplicates(subset=["fnid"], keep="first")
                        .drop(columns=["_rank"])
                    )
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
    logger.info(f"FDW forecast CSV saved to {csv_path} ({len(df_fdw)} rows)")

    return csv_path


def export_national_forecast(
    parser,
    db_path=None,
    forecast_year=None,
    forecast_issue_date=None,
    source_name_version="FDW",
    group="NASA Harvest",
    dir_out=None,
    experiment_name=None,
):
    """Export area-weighted national yield forecasts as FDW Template 1 CSV.

    Computes national yield per country as the weighted average of regional
    yields, using the 5-year average area per region as weights.

    Returns:
        Path to the saved CSV, or None if no data.
    """
    from geocif.yield_outlook import _load_shapefiles

    if forecast_year is None:
        forecast_year = ar.utcnow().to("America/New_York").year
    if forecast_issue_date is None:
        forecast_issue_date = ar.utcnow().to("America/New_York").format("YYYY-MM-DD")

    countries = ast.literal_eval(parser.get("DEFAULT", "countries"))
    if experiment_name is None:
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

    _, dict_config = _load_shapefiles(parser)
    df_hvstat = _load_hvstat(parser)

    all_rows = []

    for country_crop, config in dict_config.items():
        crop = config["crops"]

        # Query area weights from CID indices CSVs
        df_area = _query_area_weights(parser, crop)

        for model in config["models"]:
            df_pred = _query_forecast(
                db_path, country_crop, model, experiment_name, forecast_year
            )
            if df_pred.empty:
                continue

            # Keep latest stage per (Country, Region)
            df_latest = (
                df_pred.sort_values("Stage Name")
                .groupby(["Country", "Region"])
                .last()
                .reset_index()
            )

            # Parse model run date
            date_model_run = ""
            if "Date" in df_latest.columns:
                date_model_run = _parse_model_run_date(df_latest["Date"].iloc[0])

            # Blank out negative yields
            pred_col = "Predicted Yield (tn per ha)"
            df_latest.loc[df_latest[pred_col] < 0, pred_col] = np.nan

            # Join with area weights
            df_weighted = df_latest.merge(df_area, on=["Country", "Region"], how="left")
            df_weighted = df_weighted.dropna(subset=[pred_col, "avg_area"])

            if df_weighted.empty:
                logger.warning(f"No area weights for {country_crop} {model} — skipping national yield")
                continue

            # Compute national yield per country
            df_weighted["_production"] = df_weighted[pred_col] * df_weighted["avg_area"]
            national = (
                df_weighted.groupby("Country")
                .agg({"_production": "sum", "avg_area": "sum", "Harvest Year": "first"})
                .reset_index()
            )
            national["national_yield"] = national["_production"] / national["avg_area"]

            # Build one row per country
            for _, nat_row in national.iterrows():
                country_name = nat_row["Country"]
                harvest_year = nat_row["Harvest Year"]

                # Get planting/harvest months from hvstat for planted_year computation
                planting_month = np.nan
                harvest_month = np.nan
                season_name = ""
                if not df_hvstat.empty:
                    crop_title = crop.title().replace("_", " ")
                    hvstat_country = df_hvstat[
                        df_hvstat["product"].str.lower() == crop_title.lower()
                    ]
                    if not hvstat_country.empty:
                        _PRIMARY = [
                            "Long", "Gu", "Season A", "First", "1st Season",
                            "Main", "Meher", "Main harvest", "Summer", "Wet",
                        ]
                        hvstat_country = hvstat_country.copy()
                        hvstat_country["_rank"] = hvstat_country["season_name"].map(
                            lambda s: _PRIMARY.index(s) if s in _PRIMARY else len(_PRIMARY)
                        )
                        hvstat_country = hvstat_country.sort_values("_rank")
                        planting_month = hvstat_country["planting_month"].iloc[0]
                        harvest_month = hvstat_country["harvest_month"].iloc[0]
                        season_name = hvstat_country["season_name"].iloc[0]

                fdw_row = {
                    "source_name_version": source_name_version,
                    "admin_0": country_name.title().replace("_", " "),
                    "planted_year": _compute_planted_year(harvest_year, planting_month, harvest_month),
                    "harvest_year": harvest_year,
                    "crop": crop.title().replace("_", " "),
                    "crop_season": season_name if pd.notna(season_name) else "",
                    "forecast_issue_date": forecast_issue_date,
                    "date_model_run": date_model_run,
                    "input_croptype_product": "",
                    "group": group,
                    "model_version": model_version,
                    "yield_fcst": round(nat_row["national_yield"], 3),
                    "is_final": "yes",
                    "notes": "",
                }
                all_rows.append(fdw_row)

    if not all_rows:
        logger.warning("No national FDW data to export.")
        return None

    df_fdw = pd.DataFrame(all_rows).fillna("")

    scope = "africa" if len(countries) > 1 else countries[0].lower().replace(" ", "_")
    fname = f"geocif_{scope}_national_forecast_{forecast_issue_date}.csv"
    csv_path = dir_out / fname
    df_fdw.to_csv(csv_path, index=False)
    logger.info(f"FDW national forecast CSV saved to {csv_path} ({len(df_fdw)} rows)")

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
    regional_csv = export_forecast(parser, db_path=db_path, forecast_year=forecast_year, **kwargs)
    national_csv = export_national_forecast(parser, db_path=db_path, forecast_year=forecast_year, **kwargs)
    return regional_csv, national_csv
