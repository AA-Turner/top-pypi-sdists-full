"""
crop_mask.py — resolve the per-country, per-crop fractional mask raster.

The user already maintains pre-staged 5 km fractional crop masks under
``${PATHS.dir_crop_masks}``:

    Percent_Maize.tif         (BACS-derived, 0-100% maize per cell)
    Percent_Winter_Wheat.tif
    Percent_Spring_Wheat.tif
    Percent_Rice.tif
    Percent_Soybean.tif
    cropland_v9.tif           (fallback for non-BACS crops)

The crops.txt config maps each crop to its mask filename:

    [maize]   mask = Percent_Maize.tif
    [sorghum] mask = cropland_v9.tif

But the per-country ``use_cropland_mask`` flag (countries.txt) OVERRIDES
this — when True, the cropland mask is used even for BACS crops. This is
the existing geomerge convention (``crop_folder_name = "cr" if
self.use_cropland_mask else self.crop``); we honour it here.

Returned masks are float32 arrays of fraction 0.0-1.0 (converted from
0-100% if needed) — suitable for use as the AFI weight in
``geom_extract`` and as the per-cell area weight when aggregating raster
yields to admin polygons.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import rasterio

logger = logging.getLogger(__name__)


def resolve_mask_path(parser, country: str, crop: str) -> Path:
    """Resolve the mask raster path for a (country, crop) combination.

    Per-country ``use_cropland_mask = True`` forces cropland fallback.
    Otherwise reads ``[<crop>] mask`` from crops.txt.

    Args:
        parser: ConfigParser with geobase.txt + crops.txt + countries.txt.
        country: Lowercase country name.
        crop: Canonical crop name.

    Returns:
        Absolute Path to the mask GeoTIFF.

    Raises:
        FileNotFoundError: if the resolved file doesn't exist.
        configparser.NoOptionError: if the crop section is missing in crops.txt.
    """
    dir_crop_masks = Path(parser.get("PATHS", "dir_crop_masks"))

    use_cropland = parser.getboolean(country, "use_cropland_mask", fallback=False)

    if use_cropland:
        # Cropland mask filename: per-country override > crops.txt default
        # for any crop with cropland fallback (they all share cropland_v9.tif
        # in the default crops.txt).
        if parser.has_option(country, "mask"):
            fname = parser.get(country, "mask")
        else:
            # Use the cropland mask configured for one of the cropland crops.
            # 'sorghum' is the conventional fallback in crops.txt.
            fname = parser.get("sorghum", "mask")
        logger.debug(
            "%s/%s: use_cropland_mask=True → %s", country, crop, fname,
        )
    else:
        fname = parser.get(crop, "mask")
        logger.debug("%s/%s: crop-specific mask → %s", country, crop, fname)

    path = dir_crop_masks / fname
    if not path.is_file():
        raise FileNotFoundError(
            f"Crop mask not found for {country}/{crop}: {path}"
        )
    return path


def read_mask_array(
    path: Path,
    bounds: tuple[float, float, float, float] | None = None,
    nodata_fill: float = 0.0,
) -> tuple[np.ndarray, dict]:
    """Read a crop fraction mask and normalize to 0.0-1.0.

    Auto-detects whether the source is 0-100% (typical for Percent_*.tif)
    or already 0-1 fractional, and rescales accordingly.

    Args:
        path: Mask raster path.
        bounds: Optional (minx, miny, maxx, maxy) to clip — uses
            rasterio window read for efficiency.
        nodata_fill: Value to use for nodata cells (default 0.0 — these
            cells will be skipped by ``min_crop_fraction`` filtering).

    Returns:
        Tuple of (array float32 in [0, 1], profile dict with transform/crs).
    """
    with rasterio.open(path) as src:
        profile = src.profile.copy()
        if bounds is not None:
            window = rasterio.windows.from_bounds(*bounds, src.transform)
            arr = src.read(1, window=window).astype(np.float32)
            profile["transform"] = src.window_transform(window)
            profile["width"] = arr.shape[1]
            profile["height"] = arr.shape[0]
        else:
            arr = src.read(1).astype(np.float32)

        nodata = src.nodata

    # Replace nodata with fill
    if nodata is not None:
        arr = np.where(arr == nodata, nodata_fill, arr)
    # Also catch common nodata sentinels
    arr = np.where(arr < 0, nodata_fill, arr)

    # Auto-rescale: if max > 1.5, assume 0-100% → divide by 100
    finite_max = np.nanmax(arr) if np.any(np.isfinite(arr)) else 0.0
    if finite_max > 1.5:
        arr = arr / 100.0
        logger.debug("Mask %s rescaled from 0-100%% to 0-1", path.name)

    arr = np.clip(arr, 0.0, 1.0)
    return arr, profile


def aggregate_to_5km(
    src_array: np.ndarray, src_profile: dict, target_transform, target_shape,
) -> np.ndarray:
    """Aggregate a finer-resolution mask to the 5 km AgERA5/CHIRPS grid.

    Uses block-mean — the convention locked in Q4 (mean aggregation
    before any non-linear processing).

    No-op if the source resolution already matches the target (within
    1e-6 degree tolerance).
    """
    from rasterio.warp import reproject, Resampling

    src_transform = src_profile["transform"]
    src_res_x = abs(src_transform.a)
    target_res_x = abs(target_transform.a)

    if abs(src_res_x - target_res_x) < 1e-6:
        return src_array

    dst = np.zeros(target_shape, dtype=np.float32)
    reproject(
        source=src_array,
        destination=dst,
        src_transform=src_transform,
        src_crs=src_profile.get("crs"),
        dst_transform=target_transform,
        dst_crs=src_profile.get("crs"),
        resampling=Resampling.average,  # block-mean = our locked-in choice
    )
    return dst
