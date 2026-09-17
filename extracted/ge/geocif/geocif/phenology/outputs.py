"""Raster and table writers for the season monitor (DESIGN.md section 6).

Three things live here:

* :func:`write_geotiff` -- one compressed, tiled, tagged GeoTIFF, profile
  copied from ``geocif/aquacrop/output.py`` (LZW, tiled 256x256).
* :func:`zonal_table` -- weighted mean / weighted median / valid-weight share
  of a per-pixel value, per admin unit.
* :func:`status_area_table` -- the cropland-weight share of each
  :class:`~geocif.phenology.core.SeasonState` per admin unit.

Weights
-------
The weight grid is **crop fraction (0..1) x pixel area (km^2)**, i.e. crop area
in km^2 per pixel. ``zonal_table`` and ``status_area_table`` therefore report
*area shares of the crop*, not pixel counts. Any non-finite or negative weight
is treated as 0.

Every table carries the lookup's slug columns AND a Title-Case ``display_name``
built with :func:`geocif.viz.aggregation._display_name`, so a figure can label
itself without re-deriving names.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
import rasterio
from affine import Affine

from geocif.phenology.core import SeasonState

logger = logging.getLogger(__name__)

#: Column added to every table: Title-Case name of the finest admin level.
DISPLAY_COL: str = "display_name"

#: Column prefix for per-state weight shares.
SHARE_PREFIX: str = "share_"

#: Column holding the weight share of pixels whose state is nodata.
NODATA_SHARE_COL: str = f"{SHARE_PREFIX}nodata"


# ---------------------------------------------------------------------------
# 6.1 Raster writer
# ---------------------------------------------------------------------------
def write_geotiff(
    path: Any,
    arr: np.ndarray,
    transform: Affine,
    nodata: float,
    dtype: str,
    tags: Optional[dict] = None,
    crs: str = "EPSG:4326",
) -> Path:
    """Write one band to a compressed, tiled, tagged GeoTIFF.

    Profile mirrors ``geocif/aquacrop/output.py``: LZW compression, tiled with
    256x256 blocks, an explicit nodata value, EPSG:4326.

    Non-finite values in ``arr`` are replaced with ``nodata`` *before* the cast,
    so an int raster never inherits a garbage value from ``NaN.astype(int)``.

    Args:
        path: output path; parent directories are created.
        arr: 2-D array ``(rows, cols)`` in the layer's own units.
        transform: affine transform of the window.
        nodata: sentinel written for non-finite cells (e.g. -32768 for int16
            day counts, -1 for int8 status codes, NaN for float32).
        dtype: rasterio dtype string, e.g. ``"int16"``, ``"int8"``, ``"float32"``.
        tags: GeoTIFF metadata tags; values are stringified. Units belong here.
        crs: coordinate reference system; the whole package is EPSG:4326.

    Returns:
        The resolved output path.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data = np.asarray(arr)
    if data.ndim != 2:
        raise ValueError(f"write_geotiff expects a 2-D array, got shape {data.shape}")

    if np.issubdtype(data.dtype, np.floating):
        data = np.where(np.isfinite(data), data, nodata)
    data = data.astype(dtype, copy=False)

    height, width = data.shape
    profile = {
        "driver": "GTiff",
        "dtype": dtype,
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
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(data, 1)
        if tags:
            dst.update_tags(**{str(k): str(v) for k, v in tags.items()})

    logger.info(f"wrote {path} ({height}x{width} {dtype}, nodata {nodata})")
    return path


# ---------------------------------------------------------------------------
# 6.2 Zonal helpers
# ---------------------------------------------------------------------------
def _clean_weight(weight: np.ndarray) -> np.ndarray:
    """Non-finite or negative weights -> 0.0, as float64."""
    w = np.asarray(weight, dtype=np.float64)
    return np.where(np.isfinite(w) & (w > 0.0), w, 0.0)


def _weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    """Lower weighted median: the first sorted value whose cumulative weight
    reaches half the total.

    Args:
        values: 1-D finite values.
        weights: 1-D non-negative weights, same length.

    Returns:
        The weighted median, or ``nan`` when the total weight is 0.
    """
    if values.size == 0:
        return float("nan")
    total = float(weights.sum())
    if not np.isfinite(total) or total <= 0.0:
        return float("nan")
    order = np.argsort(values, kind="stable")
    v = values[order]
    cumulative = np.cumsum(weights[order])
    idx = int(np.searchsorted(cumulative, 0.5 * total, side="left"))
    idx = min(idx, v.size - 1)
    return float(v[idx])


def _with_display_name(lookup: pd.DataFrame) -> pd.DataFrame:
    """Copy of ``lookup`` with a Title-Case :data:`DISPLAY_COL` column.

    The display name comes from the finest name column present
    (``ADM2_NAME`` if any, else ``ADM1_NAME``), via
    :func:`geocif.viz.aggregation._display_name`.
    """
    from geocif.viz.aggregation import _display_name

    out = lookup.copy()
    name_col = next(
        (c for c in ("ADM2_NAME", "ADM1_NAME") if c in out.columns and out[c].notna().any()),
        None,
    )
    if name_col is None:
        out[DISPLAY_COL] = [f"Unit {i}" for i in out.get("id", range(len(out)))]
    else:
        out[DISPLAY_COL] = out[name_col].map(_display_name)
    return out


def _state_share_frame(
    state: np.ndarray, weight: np.ndarray, id_grid: np.ndarray, ids: np.ndarray
) -> pd.DataFrame:
    """Per-id weight share of every :class:`SeasonState`, plus a nodata share.

    Shares over the six states are normalised by the **valid** weight (pixels
    whose state is a real code) and therefore sum to 1 for any id that has some
    valid weight. :data:`NODATA_SHARE_COL` is normalised by the **total** weight
    of the id, so it answers "how much of this unit's crop area has no state".

    Args:
        state: int8 ``(rows, cols)``; anything outside the SeasonState range
            (e.g. the -1 nodata sentinel) counts as nodata.
        weight: ``(rows, cols)`` non-negative weights.
        id_grid: int ``(rows, cols)``; 0 = outside every unit.
        ids: the unit ids to report, in output order.

    Returns:
        DataFrame indexed 0..len(ids)-1 with an ``id`` column, one
        ``share_<state>`` column per state and :data:`NODATA_SHARE_COL`.
    """
    w = _clean_weight(weight)
    ids_grid = np.asarray(id_grid)
    codes = np.asarray(state)
    valid_codes = {int(s) for s in SeasonState}
    is_valid = np.isin(codes, list(valid_codes))

    rows = []
    for unit in ids:
        sel = ids_grid == unit
        total = float(w[sel].sum())
        valid_w = float(w[sel & is_valid].sum())
        row: dict[str, Any] = {"id": int(unit)}
        for member in SeasonState:
            share = (
                float(w[sel & is_valid & (codes == int(member))].sum()) / valid_w
                if valid_w > 0.0
                else float("nan")
            )
            row[f"{SHARE_PREFIX}{member.name.lower()}"] = share
        row[NODATA_SHARE_COL] = (
            (total - valid_w) / total if total > 0.0 else float("nan")
        )
        row["valid_weight_km2"] = valid_w
        row["total_weight_km2"] = total
        rows.append(row)

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 6.3 Tables
# ---------------------------------------------------------------------------
def zonal_table(
    value: np.ndarray,
    weight: np.ndarray,
    id_grid: np.ndarray,
    lookup: pd.DataFrame,
    statuses: Optional[np.ndarray] = None,
) -> pd.DataFrame:
    """Weighted summary of a per-pixel layer, one row per admin unit.

    Args:
        value: ``(rows, cols)`` float layer in its own units (days, mm,
            probability, ...). NaN means "no value at this pixel".
        weight: ``(rows, cols)`` crop fraction x pixel area (km^2). Non-finite
            or negative entries count as 0.
        id_grid: int ``(rows, cols)`` of 1-based unit ids; 0 = outside.
        lookup: the ``rasterize_admin`` lookup (``id``, ``ADM_ID``,
            ``ADM1_NAME``, optionally ``ADM2_NAME``).
        statuses: optional int8 ``(rows, cols)`` of
            :class:`~geocif.phenology.core.SeasonState` codes; when given, the
            per-state weight shares from :func:`status_area_table` are joined on.

    Returns:
        DataFrame with the lookup columns, :data:`DISPLAY_COL`, and:

        * ``weighted_mean`` -- sum(w*v) / sum(w) over pixels with finite ``v``,
          in ``value``'s units;
        * ``weighted_median`` -- lower weighted median over the same pixels;
        * ``valid_weight_share`` -- weight with a finite value divided by the
          unit's total weight (0..1; NaN when the unit has no weight);
        * ``valid_weight_km2`` / ``total_weight_km2`` -- the two numerators;
        * ``n_pixels`` -- pixels inside the unit (unweighted).
    """
    v = np.asarray(value, dtype=np.float64)
    w = _clean_weight(weight)
    ids_grid = np.asarray(id_grid)
    if v.shape != w.shape or v.shape != ids_grid.shape:
        raise ValueError(
            f"zonal_table shape mismatch: value {v.shape}, weight {w.shape}, "
            f"id_grid {ids_grid.shape}"
        )

    table = _with_display_name(lookup)
    finite = np.isfinite(v)

    records = []
    for unit in table["id"].to_numpy():
        sel = ids_grid == unit
        total = float(w[sel].sum())
        good = sel & finite & (w > 0.0)
        good_w = w[good]
        good_v = v[good]
        valid = float(good_w.sum())
        records.append(
            {
                "id": int(unit),
                "weighted_mean": (
                    float((good_w * good_v).sum() / valid) if valid > 0.0 else float("nan")
                ),
                "weighted_median": _weighted_median(good_v, good_w),
                "valid_weight_share": valid / total if total > 0.0 else float("nan"),
                "valid_weight_km2": valid,
                "total_weight_km2": total,
                "n_pixels": int(sel.sum()),
            }
        )

    out = table.merge(pd.DataFrame(records), on="id", how="left")

    if statuses is not None:
        shares = _state_share_frame(statuses, w, ids_grid, table["id"].to_numpy())
        shares = shares.drop(columns=["valid_weight_km2", "total_weight_km2"])
        out = out.merge(shares, on="id", how="left")

    logger.info(f"zonal_table: {len(out)} unit(s), {int(finite.sum())} valid pixel(s)")
    return out


def status_area_table(
    state: np.ndarray,
    weight: np.ndarray,
    id_grid: np.ndarray,
    lookup: pd.DataFrame,
) -> pd.DataFrame:
    """Crop-area share of every season state, one row per admin unit.

    Args:
        state: int8 ``(rows, cols)`` of
            :class:`~geocif.phenology.core.SeasonState` codes; anything outside
            the enum (the -1 nodata sentinel included) is nodata.
        weight: ``(rows, cols)`` crop fraction x pixel area (km^2).
        id_grid: int ``(rows, cols)`` of 1-based unit ids; 0 = outside.
        lookup: the ``rasterize_admin`` lookup.

    Returns:
        DataFrame with the lookup columns, :data:`DISPLAY_COL`, one
        ``share_<state>`` column per state (**summing to 1 per unit over the
        valid weight**), :data:`NODATA_SHARE_COL` (nodata weight over the
        unit's TOTAL weight), and ``valid_weight_km2`` / ``total_weight_km2``.
    """
    w = _clean_weight(weight)
    ids_grid = np.asarray(id_grid)
    codes = np.asarray(state)
    if codes.shape != w.shape or codes.shape != ids_grid.shape:
        raise ValueError(
            f"status_area_table shape mismatch: state {codes.shape}, "
            f"weight {w.shape}, id_grid {ids_grid.shape}"
        )

    table = _with_display_name(lookup)
    shares = _state_share_frame(codes, w, ids_grid, table["id"].to_numpy())
    out = table.merge(shares, on="id", how="left")
    logger.info(f"status_area_table: {len(out)} unit(s)")
    return out
