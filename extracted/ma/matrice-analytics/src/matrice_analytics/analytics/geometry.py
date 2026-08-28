"""Geometry helpers for the analytics framework.

Converts normalized zone_config dicts (from the Matrice post-processing API)
into pixel-space counters (ABLineCounter / PolygonCounter) that can be used
by VolumeProcessor for entry/exit counting.

Also provides zone-assignment utilities for partitioning detections into
named polygon zones (used by per-zone volume analytics).
"""
from __future__ import annotations

import copy
import logging
from typing import Any, List, Optional, Tuple, Union

import cv2
import numpy as np

from ..post_processing.utils.counting_utils import (
    ABLineCounter,
    PolygonCounter,
    parse_line_config,
    polygon_offset_inward,
)


logger = logging.getLogger(__name__)

_DEFAULT_INNER_POLYGON_OFFSET = 20


def _to_pixel(value: Any, dimension: int) -> int:
    """Convert a single normalized coordinate (0-1) to an integer pixel value.

    Args:
        value: Normalized coordinate as float or string.
        dimension: Frame width or height in pixels.

    Returns:
        Integer pixel coordinate.
    """
    return int(round(float(value) * dimension))


def denormalize_zone_config(
    zone_config: dict[str, Any],
    width: int,
    height: int,
) -> dict[str, Any]:
    """Convert a zone_config from normalized (0-1) coords to integer pixel coords.

    Args:
        zone_config: Dict with ``"lines"`` and/or ``"zones"`` in normalized coords.
        width: Frame width in pixels.
        height: Frame height in pixels.

    Returns:
        Deep copy of zone_config with all coordinates converted to pixels.
    """
    out: dict[str, Any] = copy.deepcopy(zone_config)
    lines = out.get("lines") or {}
    zones = out.get("zones") or {}

    if isinstance(lines, dict):
        out["lines"] = {
            name: _denormalize_points(pts, width, height)
            for name, pts in lines.items()
            if isinstance(pts, list)
        }
    if isinstance(zones, dict):
        out["zones"] = {
            name: _denormalize_points(pts, width, height)
            for name, pts in zones.items()
            if isinstance(pts, list)
        }
    return out


def _denormalize_points(
    points: Any,
    width: int,
    height: int,
) -> List[List[int]]:
    """Convert a list of ``[x_norm, y_norm]`` to ``[[x_px, y_px], ...]``."""
    result: List[List[int]] = []
    if not isinstance(points, list):
        return result
    for pt in points:
        if not isinstance(pt, (list, tuple)) or len(pt) < 2:
            continue
        result.append([_to_pixel(pt[0], width), _to_pixel(pt[1], height)])
    return result


def create_counter_from_zone_config(
    zone_config_px: dict[str, Any],
    method: str = "abline",
    in_direction: str = "A_to_B",
    use_foot_center: bool = False,
    inner_polygon_offset: int = _DEFAULT_INNER_POLYGON_OFFSET,
) -> Union[ABLineCounter, PolygonCounter]:
    """Create a counting counter from a pixel-space zone_config.

    The ``method`` parameter selects which counter to build:

    * ``"abline"``: requires >= 2 lines in ``zone_config_px["lines"]``.
      The first two lines become ``line_a`` and ``line_b`` for ``ABLineCounter``.
    * ``"polygon"``: requires >= 1 zone in ``zone_config_px["zones"]``.
      First zone is ``outer_polygon``; second (if present) is ``inner_polygon``.
      When only one zone is provided, ``inner_polygon`` is auto-computed via
      ``polygon_offset_inward``.

    Args:
        zone_config_px: Dict with ``"lines"`` and/or ``"zones"`` in pixel coords.
        method: ``"abline"`` or ``"polygon"``.
        in_direction: For abline -- ``"A_to_B"`` or ``"B_to_A"``.
        use_foot_center: Use bottom-center of bbox instead of center.
        inner_polygon_offset: Pixel inset for auto-computed inner polygon.

    Returns:
        An ``ABLineCounter`` or ``PolygonCounter`` instance.

    Raises:
        ValueError: If required geometry is missing for the chosen method.
    """
    lines_px = zone_config_px.get("lines") or {}
    zones_px = zone_config_px.get("zones") or {}

    if method == "abline":
        line_values = list(lines_px.values()) if isinstance(lines_px, dict) else []
        if len(line_values) < 2:
            raise ValueError(
                f"abline method requires at least 2 lines, got {len(line_values)}"
            )
        line_a = parse_line_config(line_values[0])
        line_b = parse_line_config(line_values[1])
        logger.info("Creating ABLineCounter (in_direction=%s)", in_direction)
        return ABLineCounter(
            line_a=line_a,
            line_b=line_b,
            in_direction=in_direction,
            use_foot_center=use_foot_center,
        )

    if method == "polygon":
        zone_values = list(zones_px.values()) if isinstance(zones_px, dict) else []
        if len(zone_values) < 1:
            raise ValueError("polygon method requires at least 1 zone")
        outer = np.array(zone_values[0], dtype=np.float64)
        if len(zone_values) >= 2:
            inner = np.array(zone_values[1], dtype=np.int32)
        else:
            inner = polygon_offset_inward(outer, inner_polygon_offset)
        logger.info("Creating PolygonCounter (outer=%d pts, inner=%d pts)", len(outer), len(inner))
        return PolygonCounter(
            inner_polygon=inner,
            outer_polygon=np.array(zone_values[0], dtype=np.int32),
            initial_warmup_frames=5,
            use_foot_center=use_foot_center,
        )

    raise ValueError(f"Unknown counting method: {method!r} (expected 'abline' or 'polygon')")


# ---------------------------------------------------------------------------
# Zone assignment utilities (per-zone volume analytics)
# ---------------------------------------------------------------------------


def point_in_polygon(point: tuple[float, float], polygon: np.ndarray) -> bool:
    """Test whether *point* lies inside *polygon* using OpenCV.

    Args:
        point: ``(x, y)`` in pixel coordinates.
        polygon: Numpy array of shape ``(N, 2)`` with integer pixel vertices.

    Returns:
        ``True`` if the point is inside or on the edge of the polygon.
    """
    result = cv2.pointPolygonTest(polygon, point, False)
    return result >= 0  # >= 0 means inside or on edge


def get_detection_reference_point(
    detection: dict[str, Any],
    use_foot_center: bool = False,
) -> tuple[float, float] | None:
    """Extract the reference point (center or foot-center) from a detection.

    Args:
        detection: Dict with ``bounding_box`` or ``bbox`` key.
        use_foot_center: If ``True``, return the bottom-center of the bbox
            instead of the geometric center.

    Returns:
        ``(x, y)`` in the same coordinate space as the bounding box, or
        ``None`` if the bbox is missing / invalid.
    """
    raw = detection.get("bounding_box", detection.get("bbox"))
    if raw is None:
        return None

    if isinstance(raw, dict):
        xmin = raw.get("xmin", raw.get("x1"))
        ymin = raw.get("ymin", raw.get("y1"))
        xmax = raw.get("xmax", raw.get("x2"))
        ymax = raw.get("ymax", raw.get("y2"))
    elif isinstance(raw, (list, tuple)) and len(raw) >= 4:
        xmin, ymin, xmax, ymax = raw[0], raw[1], raw[2], raw[3]
    else:
        return None

    if None in (xmin, ymin, xmax, ymax):
        return None

    xmin, ymin, xmax, ymax = float(xmin), float(ymin), float(xmax), float(ymax)
    cx = (xmin + xmax) / 2.0
    if use_foot_center:
        cy = ymax
    else:
        cy = (ymin + ymax) / 2.0
    return (cx, cy)


def assign_detections_to_zones(
    detections: list[dict[str, Any]],
    zones_px: dict[str, np.ndarray],
    use_foot_center: bool = False,
) -> dict[str, list[dict[str, Any]]]:
    """Partition detections into named zones by point-in-polygon containment.

    Each detection is assigned to the **first** zone whose polygon contains
    the detection's reference point.  Detections that fall in no zone are
    discarded.

    Args:
        detections: Raw detection dicts (with ``bounding_box`` / ``bbox``).
        zones_px: Mapping of zone name to polygon vertices as a numpy array
            of shape ``(N, 2)`` in **pixel** coordinates (``int32``).
        use_foot_center: Use bottom-center of bbox instead of center.

    Returns:
        Dict mapping ``zone_name`` to the list of detections whose reference
        point falls inside that zone.
    """
    result: dict[str, list[dict[str, Any]]] = {name: [] for name in zones_px}
    zone_items = list(zones_px.items())

    for det in detections:
        pt = get_detection_reference_point(det, use_foot_center=use_foot_center)
        if pt is None:
            continue
        for zone_name, polygon in zone_items:
            if point_in_polygon(pt, polygon):
                result[zone_name].append(det)
                break  # first match wins

    return result


def build_zone_polygons_px(
    zones_normalized: dict[str, list[list[float]]],
    width: int,
    height: int,
) -> dict[str, np.ndarray]:
    """Denormalize zone polygons and convert to numpy arrays for OpenCV.

    Args:
        zones_normalized: Zone name to list of ``[x_norm, y_norm]`` vertices.
        width: Frame width in pixels.
        height: Frame height in pixels.

    Returns:
        Dict mapping zone name to ``np.ndarray`` of shape ``(N, 1, 2)``
        with ``int32`` dtype (format expected by ``cv2.pointPolygonTest``).
    """
    out: dict[str, np.ndarray] = {}
    for name, pts in zones_normalized.items():
        px_pts = _denormalize_points(pts, width, height)
        if len(px_pts) < 3:
            logger.warning("Zone '%s' has fewer than 3 vertices — skipping", name)
            continue
        out[name] = np.array(px_pts, dtype=np.int32).reshape((-1, 1, 2))
    return out
