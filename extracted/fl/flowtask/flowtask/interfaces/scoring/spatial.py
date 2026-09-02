"""Spatial Helpers (FEAT-190).

H3 hex-grid tessellation and coordinate utilities (spec Module 6).

``h3`` is imported lazily, inside function bodies only, so that
``flowtask.interfaces.scoring.models`` (and therefore this whole package's
lightweight contract types) remains importable without h3 installed
(spec AC11). Only ``numpy`` is imported eagerly here.
"""
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from .models import CandidateGrid

# WGS-84 mean Earth radius, in meters.
_EARTH_RADIUS_M = 6371008.8


def deg_to_rad(arr: np.ndarray) -> np.ndarray:
    """Convert an array of degrees to radians."""
    return np.radians(arr)


def haversine_distance(lat1, lon1, lat2, lon2) -> np.ndarray:
    """Vectorized haversine great-circle distance, in meters.

    Args:
        lat1: Latitude(s) of the first point(s), in degrees. Scalar or array.
        lon1: Longitude(s) of the first point(s), in degrees. Scalar or array.
        lat2: Latitude(s) of the second point(s), in degrees. Scalar or array.
        lon2: Longitude(s) of the second point(s), in degrees. Scalar or array.

    Returns:
        Distance(s) in meters. Same broadcast shape as the inputs; a plain
        float when all inputs are scalars.
    """
    lat1_r = deg_to_rad(np.asarray(lat1, dtype=float))
    lon1_r = deg_to_rad(np.asarray(lon1, dtype=float))
    lat2_r = deg_to_rad(np.asarray(lat2, dtype=float))
    lon2_r = deg_to_rad(np.asarray(lon2, dtype=float))

    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r

    a = (
        np.sin(dlat / 2.0) ** 2
        + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(dlon / 2.0) ** 2
    )
    c = 2.0 * np.arcsin(np.sqrt(np.clip(a, 0.0, 1.0)))
    distance = _EARTH_RADIUS_M * c

    if distance.ndim == 0:
        return float(distance)
    return distance


def h3_tessellate(
    bbox: tuple[float, float, float, float],
    resolution: int = 8,
) -> "CandidateGrid":
    """Fill a bounding box with H3 hex cells and return their centroids.

    Args:
        bbox: ``(min_lat, min_lng, max_lat, max_lng)``.
        resolution: H3 resolution (0-15). Higher = smaller hexes.

    Returns:
        A ``CandidateGrid`` with one candidate per H3 cell centroid.

    Raises:
        ImportError: if the ``h3`` package is not installed.
    """
    try:
        import h3
    except ImportError as exc:
        raise ImportError(
            "h3 is required for H3 tessellation. "
            "Install with: uv pip install h3"
        ) from exc

    from .models import CandidateGrid

    min_lat, min_lng, max_lat, max_lng = bbox
    outer = [
        (min_lat, min_lng), (max_lat, min_lng),
        (max_lat, max_lng), (min_lat, max_lng),
    ]
    polygon = h3.LatLngPoly(outer)
    cells = h3.polygon_to_cells(polygon, resolution)
    centroids = [h3.cell_to_latlng(c) for c in cells]
    lats = np.array([c[0] for c in centroids])
    lngs = np.array([c[1] for c in centroids])
    ids = list(cells)
    return CandidateGrid(
        latitudes=lats, longitudes=lngs, ids=ids, h3_resolution=resolution
    )
