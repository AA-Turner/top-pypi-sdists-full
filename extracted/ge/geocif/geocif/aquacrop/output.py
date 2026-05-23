"""
output.py — write AquaCrop outputs:

    1.  Yield raster at 5 km:
        ${dir_output}/{project}/aquacrop/raster/{country}_{crop}_{year}_s{season}.tif
    2.  Admin-aggregated DB rows in the geocif yield_outlook schema:
        ${dir_output}/{project}/ml/db/aquacrop_outlook_{timestamp}.db
        Table per (country, crop) — same convention as geocif_runner.

Aggregation: ``geom_extract`` from geoprepare with the crop fraction mask
as the AFI weight. This guarantees per-admin yields are area-weighted
exactly the way geocif's CID extraction does it.

Columns written into the DB (matching geocif's _query_predictions schema
so existing diagnostics consume them directly):

    Country, Region, Region_ID, Harvest Year, Stage Name, Stage,
    Model, Experiment Name, Predicted Yield (tn per ha),
    Observed Yield (tn per ha), lower CI, upper CI, Area (ha),
    Production (tn), Selected Features, Season, Best Hyperparameters
"""

from __future__ import annotations

import datetime as _dt
import logging
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_bounds

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Raster output
# ---------------------------------------------------------------------------

def write_yield_raster(
    yield_array: np.ndarray,
    bounds: tuple[float, float, float, float],
    out_path: Path,
    crs: str = "EPSG:4326",
    nodata: float = -9999.0,
    crop: str = "",
    country: str = "",
    year: Optional[int] = None,
    season: Optional[int] = None,
    model: str = "aquacrop",
) -> Path:
    """Write a 5 km yield raster (tn/ha) to disk as GeoTIFF.

    Args:
        yield_array: 2D float32 array, NaN for unsimulated/masked cells.
        bounds: (minx, miny, maxx, maxy) in CRS units.
        out_path: Output .tif path. Parent created if needed.
        crs: Coordinate reference system.
        nodata: Sentinel for missing/masked.

    Returns:
        Resolved output path.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    height, width = yield_array.shape
    transform = from_bounds(*bounds, width, height)

    data = np.where(np.isfinite(yield_array), yield_array, nodata).astype(np.float32)

    profile = {
        "driver": "GTiff",
        "dtype": "float32",
        "width": width,
        "height": height,
        "count": 1,
        "crs": crs,
        "transform": transform,
        "nodata": nodata,
        "compress": "lzw",
        "tiled": True,
        "blockxsize": 256,
        "blockysize": 256,
    }

    with rasterio.open(out_path, "w", **profile) as dst:
        dst.write(data, 1)
        # Metadata: pin the run identity to the file so it's
        # self-describing without parsing the filename.
        tags = {"variable": "yield_tn_per_ha", "model": model}
        if crop:
            tags["crop"] = crop
        if country:
            tags["country"] = country
        if year is not None:
            tags["year"] = str(year)
        if season is not None:
            tags["season"] = str(season)
        dst.update_tags(**tags)

    return out_path


# ---------------------------------------------------------------------------
# Admin aggregation (raster → polygon)
# ---------------------------------------------------------------------------

def aggregate_raster_to_admin(
    yield_raster_path: Path,
    mask_raster_path: Path,
    admin_gdf,
    *,
    region_col: str,
    region_id_col: str,
    context_prefix: str = "",
) -> pd.DataFrame:
    """Aggregate yield raster to admin polygons using the crop mask as AFI.

    Uses ``geoprepare.extract.stats.geom_extract`` so weighting is
    identical to how geocif extracts EO CIDs to admin units.

    Args:
        yield_raster_path: GeoTIFF written by ``write_yield_raster``.
        mask_raster_path: Crop fraction raster (used as AFI weight).
        admin_gdf: GeoDataFrame of admin polygons.
        region_col: Column with admin region name (e.g. 'ADM1_NAME').
        region_id_col: Column with admin region ID (e.g. 'ADM_ID' or 'FNID').
        context_prefix: Optional prefix for the per-region context string
            in error logs (e.g. "malawi/maize/2024").

    Returns:
        DataFrame with columns:
            Region, Region_ID, Predicted Yield (tn per ha),
            n_pixels (count after masking), weight_sum (crop area weight)
    """
    # Lazy import — keeps geoprepare an optional dep when only reading
    # outputs.
    try:
        from geoprepare.extract.stats import geom_extract  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "geoprepare is required for admin aggregation. "
            "Install with `pip install -e ./geoprepare`."
        ) from exc

    rows = []
    for _, region in admin_gdf.iterrows():
        geom = region.geometry.__geo_interface__
        context = f"{context_prefix} {region[region_col]}"

        # 'default' var → masked_less(0.0), which suits a yield raster
        # where NoData is negative and all valid yields are >= 0.
        out = geom_extract(
            geometry=geom,
            variable="default",
            indicator=str(yield_raster_path),
            stats_out=("mean", "counts"),
            afi=str(mask_raster_path),
            context=context,
        )
        stats = out.get("stats", {})
        counts = out.get("counts", {})

        rows.append({
            "Region": region[region_col],
            "Region_ID": region[region_id_col],
            "Predicted Yield (tn per ha)": stats.get("mean"),
            "n_pixels": counts.get("valid_data_after_masking"),
            "weight_sum": counts.get("weight_sum_used"),
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# DB row writer (yield_outlook schema)
# ---------------------------------------------------------------------------

def build_db_dataframe(
    agg_df: pd.DataFrame,
    country: str,
    crop: str,
    harvest_year: int,
    season: int,
    stage_name: str,
    stage_id: str,
    *,
    model_name: str = "aquacrop",
    experiment_name: str = "aquacrop_v1",
    selected_features: Optional[list[str]] = None,
    observed_yield: Optional[pd.Series] = None,
    area_ha: Optional[pd.Series] = None,
    production_tn: Optional[pd.Series] = None,
    lower_ci: Optional[pd.Series] = None,
    upper_ci: Optional[pd.Series] = None,
) -> pd.DataFrame:
    """Build a DataFrame matching geocif's yield_outlook DB schema.

    Args:
        agg_df: Output of ``aggregate_raster_to_admin``.
        country: Lowercase canonical country name.
        crop: Canonical crop name.
        harvest_year: Year of harvest.
        season: 1 (primary) or 2 (secondary).
        stage_name: Human-readable stage (e.g. "Mar 11-Nov 6").
        stage_id: Underscore-joined stage IDs (e.g. "8_32").
        observed_yield, area_ha, production_tn, lower_ci, upper_ci:
            Optional aligned-by-index series.

    Returns:
        DataFrame ready for ``geocif.ml.output.store()``.
    """
    n = len(agg_df)
    # AquaCrop is a mechanistic crop model, not an ML feature-selector — it
    # consumes the full set of soil/weather/calendar drivers every cell. Use
    # an empty list rather than fake "feature names" that don't correspond
    # to anything queryable in the geocif statistics CSV / residuals_vs_cid.
    if selected_features is None:
        selected_features = []

    df = pd.DataFrame({
        "Country": [country] * n,
        # Crop column is *not* in the geocif yield_outlook DB schema (the
        # canonical schema encodes the crop in the table name), but we
        # carry it here so post-LOOCV ``concat`` of per-combo frames can
        # be ``groupby(["Country", "Crop"])``-ed back into the right
        # tables in ``aquacrop_runner.run``. The runner drops this column
        # before calling ``write_db_rows``.
        "Crop": [crop] * n,
        "Region": agg_df["Region"].values,
        "Region_ID": agg_df["Region_ID"].values,
        "Harvest Year": [harvest_year] * n,
        "Stage Name": [stage_name] * n,
        "Stage": [stage_id] * n,
        "Model": [model_name] * n,
        "Experiment Name": [experiment_name] * n,
        "Predicted Yield (tn per ha)": agg_df["Predicted Yield (tn per ha)"].values,
        "Observed Yield (tn per ha)": (
            observed_yield.values if observed_yield is not None
            else [np.nan] * n
        ),
        "lower CI": (
            lower_ci.values if lower_ci is not None else [np.nan] * n
        ),
        "upper CI": (
            upper_ci.values if upper_ci is not None else [np.nan] * n
        ),
        "Area (ha)": (
            area_ha.values if area_ha is not None else [np.nan] * n
        ),
        "Production (tn)": (
            production_tn.values if production_tn is not None else [np.nan] * n
        ),
        "Selected Features": [str(selected_features)] * n,
        "Season": [season] * n,
        # 'Best Hyperparameters' is required by geocif.ml.output.store()
        # (it runs make_serializable on it). Keep NaN for non-ML models.
        "Best Hyperparameters": [np.nan] * n,
    })
    df.index.set_names(["Index"], inplace=True)
    return df


def write_db_rows(
    df_outlook: pd.DataFrame,
    db_path: Path,
    country: str,
    crop: str,
    *,
    save_model_blobs: bool = False,
) -> None:
    """Write outlook rows to the geocif SQLite DB.

    Uses geocif.ml.output.store with experiment_id = '<country>_<crop>'
    (the standard yield_outlook table-per-country-crop convention).

    Args:
        df_outlook: Output of ``build_db_dataframe``.
        db_path: SQLite path. Parent created if needed.
        country: Used to build the table name.
        crop: Used to build the table name.
        save_model_blobs: Forwarded to ``store`` (default False — matches
            geocif's hot-lock-avoidance default).
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # The 'Crop' helper column carried through the pipeline isn't part of
    # the geocif yield_outlook schema (crop lives in the table name).
    # Drop it before persisting.
    df_to_write = df_outlook.drop(columns=["Crop"], errors="ignore")

    try:
        from geocif.ml.output import store  # type: ignore
    except ImportError:
        # Fallback: simple to_sql if geocif is not on the path. Useful
        # for standalone testing.
        import sqlite3
        with sqlite3.connect(db_path) as con:
            df_to_write.to_sql(
                f"{country}_{crop}", con, if_exists="append", index=True,
            )
        return

    experiment_id = f"{country}_{crop}"
    store(
        db_path=str(db_path),
        experiment_id=experiment_id,
        df=df_to_write,
        model=None,
        model_name="aquacrop",
        save_model_blobs=save_model_blobs,
    )


def make_db_path(
    parser, project_name: str, model_name: str = "aquacrop",
) -> Path:
    """Construct the AquaCrop DB path matching geocif's directory layout.

    ${dir_output}/{project_name}/ml/db/aquacrop_outlook_{MM_DD_YYYY_HHhMM}.db
    """
    dir_output = Path(parser.get("PATHS", "dir_output"))
    template = parser.get(
        "AQUACROP", "db_filename_template",
        fallback="aquacrop_outlook_{timestamp}.db",
    )
    ts = _dt.datetime.now().strftime("%m_%d_%Y_%Hh%M")
    fname = template.format(timestamp=ts)
    return dir_output / project_name / "ml" / "db" / fname
