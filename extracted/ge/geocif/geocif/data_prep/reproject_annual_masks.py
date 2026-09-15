"""Reproject annual per-crop masks onto the standard geoprepare crop-mask grid.

Sources are MODIS-sinusoidal GeoTIFFs holding percent-crop values (float32,
0-100, NaN nodata), one file per year, e.g.
    kenya_maize/2015.tif
    zimbabwe_maize/Zimbabwe_maize_2015_1km.tiff

geoprepare's annual-mask resolver (utils._resolve_annual_mask) expects
    ${dir_crop_masks}/<mask_dir>/{YYYY}.tif
on the global 0.05-degree EPSG:4326 grid (3600x7200) with uint16 values scaled
percent x 100 (0-10000), matching cropland_v9.tif and brazil_soybean/. This
script parses the year out of each source filename (so it also performs any
renaming), zero-fills NaN (no-data == no crop), reprojects with average
resampling, rescales, and writes {YYYY}.tif to the destination.

Run locally; the default --dst-root is the Z: mount of /gpfs, so writing the
outputs IS the copy to the HPC.

Usage:
    python reproject_annual_masks.py --src-dir "D:\\...\\crop_masks\\kenya_maize" --out-name kenya_maize
"""

import argparse
import csv
import re
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import Resampling, reproject

DST_CRS = "EPSG:4326"
DST_RES = 0.05
DST_WIDTH = 7200
DST_HEIGHT = 3600
DST_TRANSFORM = from_origin(-180.0, 90.0, DST_RES, DST_RES)
SCALE = 100  # percent -> percent x 100, matching cropland_v9 / brazil_soybean

YEAR_RE = re.compile(r"(?<!\d)((?:19|20)\d{2})(?!\d)")


def year_from_name(path):
    """Extract the 4-digit year embedded in a mask filename."""
    matches = YEAR_RE.findall(path.stem)
    if len(matches) != 1:
        raise ValueError(f"cannot parse a unique year from {path.name!r}: {matches}")
    return int(matches[0])


def reproject_mask(src_path, dst_path):
    """Reproject one sinusoidal percent mask onto the global 0.05-degree grid."""
    with rasterio.open(src_path) as src:
        arr = src.read(1)
        arr = np.nan_to_num(arr, nan=0.0).astype(np.float32)
        dst = np.zeros((DST_HEIGHT, DST_WIDTH), dtype=np.float32)
        reproject(
            source=arr,
            destination=dst,
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=DST_TRANSFORM,
            dst_crs=DST_CRS,
            resampling=Resampling.average,
        )

    out = np.clip(np.round(dst * SCALE), 0, 100 * SCALE).astype(np.uint16)
    profile = {
        "driver": "GTiff",
        "dtype": "uint16",
        "count": 1,
        "width": DST_WIDTH,
        "height": DST_HEIGHT,
        "crs": DST_CRS,
        "transform": DST_TRANSFORM,
        "compress": "deflate",
    }
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(dst_path, "w", **profile) as dstf:
        dstf.write(out, 1)
    return out


def qa_row(year, out):
    rows, cols = np.nonzero(out)
    if rows.size == 0:
        return {"year": year, "nonzero_cells": 0}
    lons = -180.0 + (cols + 0.5) * DST_RES
    lats = 90.0 - (rows + 0.5) * DST_RES
    vals = out[rows, cols] / SCALE  # back to percent
    return {
        "year": year,
        "nonzero_cells": int(rows.size),
        "mean_pct": round(float(vals.mean()), 2),
        "max_pct": round(float(vals.max()), 2),
        "lon_min": round(float(lons.min()), 2),
        "lon_max": round(float(lons.max()), 2),
        "lat_min": round(float(lats.min()), 2),
        "lat_max": round(float(lats.max()), 2),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--src-dir", required=True, type=Path)
    ap.add_argument("--out-name", required=True, help="mask_dir name, e.g. kenya_maize")
    ap.add_argument(
        "--dst-root",
        type=Path,
        default=Path(r"Z:\cmongp1\GEO\inputs\metadata\crop_masks"),
    )
    args = ap.parse_args()

    src_files = sorted(
        list(args.src_dir.glob("*.tif")) + list(args.src_dir.glob("*.tiff"))
    )
    if not src_files:
        raise SystemExit(f"no .tif/.tiff files in {args.src_dir}")

    dst_dir = args.dst_root / args.out_name
    report = []
    for src_path in src_files:
        year = year_from_name(src_path)
        dst_path = dst_dir / f"{year}.tif"
        out = reproject_mask(src_path, dst_path)
        row = qa_row(year, out)
        report.append(row)
        print(f"{src_path.name} -> {dst_path}  {row}")

    qa_csv = args.src_dir / f"reprojection_qa_{args.out_name}.csv"
    fields = ["year", "nonzero_cells", "mean_pct", "max_pct", "lon_min", "lon_max", "lat_min", "lat_max"]
    with open(qa_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report)
    print(f"\nwrote {len(report)} masks to {dst_dir}")
    print(f"QA CSV: {qa_csv}")

    empty = [r["year"] for r in report if r["nonzero_cells"] == 0]
    if empty:
        raise SystemExit(f"ERROR: all-zero masks for years {empty}")


if __name__ == "__main__":
    main()
