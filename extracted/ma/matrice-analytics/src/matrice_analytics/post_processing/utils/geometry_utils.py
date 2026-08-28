"""
Geometry utility functions for post-processing operations.
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union


def point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """
    Check if point is inside polygon using ray casting algorithm.

    Args:
        point: (x, y) coordinate tuple
        polygon: List of (x, y) coordinate tuples defining the polygon

    Returns:
        bool: True if point is inside polygon
    """
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def get_bbox_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get center point of bounding box.

    Args:
        bbox: Bounding box dict with coordinates or list [x1, y1, x2, y2]

    Returns:
        Tuple[float, float]: (x, y) center coordinates
    """
    if isinstance(bbox, list):
        # Handle list format [x1, y1, x2, y2]
        if len(bbox) >= 4:
            return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
        return (0, 0)

    elif isinstance(bbox, dict):
        # Handle dict formats
        if "xmin" in bbox and "xmax" in bbox and "ymin" in bbox and "ymax" in bbox:
            return (
                (bbox["xmin"] + bbox["xmax"]) / 2,
                (bbox["ymin"] + bbox["ymax"]) / 2,
            )
        elif "x1" in bbox and "x2" in bbox and "y1" in bbox and "y2" in bbox:
            return ((bbox["x1"] + bbox["x2"]) / 2, (bbox["y1"] + bbox["y2"]) / 2)
        else:
            # Handle different bbox formats
            keys = list(bbox.keys())
            if len(keys) >= 4:
                values = list(bbox.values())
                return ((values[0] + values[2]) / 2, (values[1] + values[3]) / 2)

    return (0, 0)


def get_bbox_bottom_center(
    bbox: Union[Dict[str, float], List[float]],
) -> Tuple[float, float]:
    """
    Get bottom-center point of bounding box (horizontal center, bottom edge).

    Used for floor-level zone membership (foot-in-zone semantics).
    """
    if isinstance(bbox, list):
        if len(bbox) >= 4:
            return ((bbox[0] + bbox[2]) / 2, bbox[3])
        return (0, 0)

    if isinstance(bbox, dict):
        if "xmin" in bbox and "xmax" in bbox and "ymax" in bbox:
            return ((bbox["xmin"] + bbox["xmax"]) / 2, bbox["ymax"])
        if "x1" in bbox and "x2" in bbox and "y2" in bbox:
            return ((bbox["x1"] + bbox["x2"]) / 2, bbox["y2"])
        keys = list(bbox.keys())
        if len(keys) >= 4:
            values = list(bbox.values())
            return ((values[0] + values[2]) / 2, values[3])

    return (0, 0)


def get_bbox_bottom10_center(
    bbox: Union[Dict[str, float], List[float]],
) -> Tuple[float, float]:
    """
    Get bottom 10% center point of bounding box (x at horizontal center).
    """
    if isinstance(bbox, list):
        if len(bbox) >= 4:
            x_center = (bbox[0] + bbox[2]) / 2
            height = bbox[3] - bbox[1]
            y_target = bbox[3] - 0.10 * height
            return (x_center, y_target)
        return (0, 0)

    if isinstance(bbox, dict):
        if "xmin" in bbox and "xmax" in bbox and "ymin" in bbox and "ymax" in bbox:
            x_center = (bbox["xmin"] + bbox["xmax"]) / 2
            height = bbox["ymax"] - bbox["ymin"]
            y_target = bbox["ymax"] - 0.10 * height
            return (x_center, y_target)
        if "x1" in bbox and "x2" in bbox and "y1" in bbox and "y2" in bbox:
            x_center = (bbox["x1"] + bbox["x2"]) / 2
            height = bbox["y2"] - bbox["y1"]
            y_target = bbox["y2"] - 0.10 * height
            return (x_center, y_target)
        keys = list(bbox.keys())
        if len(keys) >= 4:
            values = list(bbox.values())
            x_center = (values[0] + values[2]) / 2
            height = values[3] - values[1]
            y_target = values[3] - 0.10 * height
            return (x_center, y_target)

    return (0, 0)


def get_bbox_bottom25_center(
    bbox: Union[Dict[str, float], List[float]],
) -> Tuple[float, float]:
    """
    Get bottom 25% center point of bounding box.

    Args:
        bbox: Bounding box dict with coordinates or list [x1, y1, x2, y2]

    Returns:
        Tuple[float, float]: (x, y) coordinates at bottom 25% height from center X
    """
    if isinstance(bbox, list):
        # Handle list format [x1, y1, x2, y2]
        if len(bbox) >= 4:
            x_center = (bbox[0] + bbox[2]) / 2
            height = bbox[3] - bbox[1]
            y_target = bbox[3] - 0.25 * height
            return (x_center, y_target)
        return (0, 0)

    elif isinstance(bbox, dict):
        # Handle dict formats
        if "xmin" in bbox and "xmax" in bbox and "ymin" in bbox and "ymax" in bbox:
            x_center = (bbox["xmin"] + bbox["xmax"]) / 2
            height = bbox["ymax"] - bbox["ymin"]
            y_target = bbox["ymax"] - 0.25 * height
            return (x_center, y_target)
        elif "x1" in bbox and "x2" in bbox and "y1" in bbox and "y2" in bbox:
            x_center = (bbox["x1"] + bbox["x2"]) / 2
            height = bbox["y2"] - bbox["y1"]
            y_target = bbox["y2"] - 0.25 * height
            return (x_center, y_target)
        else:
            # Handle different bbox formats
            keys = list(bbox.keys())
            if len(keys) >= 4:
                values = list(bbox.values())
                x_center = (values[0] + values[2]) / 2
                height = values[3] - values[1]
                y_target = values[3] - 0.25 * height
                return (x_center, y_target)

    return (0, 0)


def _bbox_extent(bbox: Union[Dict[str, float], List[float]]) -> float:
    """The largest raw coordinate in ``bbox``, in whatever units it arrives.

    Used only to guess normalized-vs-pixel space (:func:`resolve_frame_dims` /
    the zone-membership point scaling below) -- a real person's box always has
    ``xmax``/``ymax`` (or the bare 3rd/4th value) as its largest corner, so this
    is the same value :func:`get_bbox_bottom_center` would read for the bottom
    edge, without re-deriving the whole point.
    """
    if isinstance(bbox, list):
        return max(bbox) if len(bbox) >= 4 else 0.0
    if isinstance(bbox, dict):
        if "xmax" in bbox and "ymax" in bbox:
            return max(float(bbox["xmax"]), float(bbox["ymax"]))
        if "x2" in bbox and "y2" in bbox:
            return max(float(bbox["x2"]), float(bbox["y2"]))
        values = list(bbox.values())
        return max(float(v) for v in values) if len(values) >= 4 else 0.0
    return 0.0


def reference_size_from_payload(data: Any) -> Tuple[int, int]:
    """``(width, height)`` from a detections payload's ``coordinate_frame``, or ``(0, 0)``.

    The resolution these helpers need has been in the wire payload all along -- it just is not
    in ``stream_info``, which is the only place :func:`resolve_frame_dims` was looking.
    py_inference stamps a ``CoordinateFrame`` onto the *data* dict
    (``engine_core/node/batch_engine_runner.py``: ``data["coordinate_frame"] = asdict(cf)``), and
    its ``reference_size`` is exactly the native ``(source_w, source_h)`` the normalized boxes
    are relative to -- "stamped once, by the normalization owner, from the effective
    preprocessing; never re-derived downstream".

    That matters because the CUDA-SHM worker path reaches ``PostProcessor.process`` without ever
    calling ``build_stream_info(source_dims=...)``, so ``stream_resolution`` is absent and
    :func:`to_zone_test_point` fails open -- every zone reports 0 and nobody is relabelled. The
    fix is to read the value that is already here rather than to thread a new one down from
    ml-codebases.

    Tolerant of shape by design: the payload is a dict for a single-port output and a list of
    per-detection dicts elsewhere, and ``reference_size`` survives ``asdict`` as a list.
    Anything unrecognised returns ``(0, 0)`` so the caller keeps its existing fail-open path.
    """

    def _from_frame(frame: Any) -> Tuple[int, int]:
        if not isinstance(frame, dict):
            return 0, 0
        size = frame.get("reference_size")
        if isinstance(size, (list, tuple)) and len(size) == 2:
            try:
                width, height = int(size[0]), int(size[1])
            except (TypeError, ValueError):
                return 0, 0
            if width > 0 and height > 0:
                return width, height
        return 0, 0

    if isinstance(data, dict):
        dims = _from_frame(data.get("coordinate_frame"))
        if dims != (0, 0):
            return dims
        # `{"detections": [...], "coordinate_frame": {...}}` is the common shape, but a nested
        # per-port payload puts it one level down.
        for value in data.values():
            if isinstance(value, dict):
                dims = _from_frame(value.get("coordinate_frame"))
                if dims != (0, 0):
                    return dims
    elif isinstance(data, (list, tuple)):
        for entry in data:
            if isinstance(entry, dict):
                dims = _from_frame(entry.get("coordinate_frame"))
                if dims != (0, 0):
                    return dims
    return 0, 0


def resolve_frame_dims(stream_info: Optional[Dict[str, Any]]) -> Tuple[int, int]:
    """Best-effort ``(width, height)`` from ``stream_info``, or ``(0, 0)`` if unknown.

    Two shapes have both shipped for ``stream_resolution`` across this codebase: a
    top-level ``{"width": .., "height": ..}`` dict (``intrusion_detection.py``'s own
    ``_frame_dims``), and ``input_settings.stream_resolution`` as either the same
    dict shape or a bare ``[width, height]`` pair (``Trackers/det_utils.py``). This
    tries all of them, in that order, and returns ``(0, 0)`` -- not a guessed
    fallback -- when none resolve, so a caller can tell "no dimensions" apart from
    a real ``0x0`` stream and skip whatever scaling it wanted these for.
    """
    if not isinstance(stream_info, dict):
        return 0, 0
    candidates = [
        stream_info.get("stream_resolution"),
        (stream_info.get("input_settings") or {}).get("stream_resolution"),
    ]
    for candidate in candidates:
        if isinstance(candidate, dict):
            width = int(candidate.get("width") or 0)
            height = int(candidate.get("height") or 0)
            if width > 0 and height > 0:
                return width, height
        elif isinstance(candidate, (list, tuple)) and len(candidate) == 2:
            try:
                width, height = int(candidate[0]), int(candidate[1])
            except (TypeError, ValueError):
                continue
            if width > 0 and height > 0:
                return width, height
    return 0, 0


def to_zone_test_point(
    point: Tuple[float, float],
    bbox: Union[Dict[str, float], List[float]],
    stream_info: Optional[Dict[str, Any]] = None,
) -> Tuple[float, float]:
    """Scale a bbox-derived point (e.g. from :func:`get_bbox_bottom_center`) to
    match a pixel-space zone polygon, when the bbox itself is normalized.

    Zone polygons resolved via ``PostProcessingConfigClient.denormalize_config``
    (``_resolve_geometry_from_api`` in ``intrusion_detection.py`` /
    ``hazard_zone_entry.py``) are always pixel coordinates matching the camera's
    real resolution -- that is what "denormalize" means there. Detections carrying
    the newer coordinate-frame convention (``metadata.coordinate_frame.space:
    "normalized"``) arrive normalized 0-1 instead. Testing an unscaled normalized
    point against a pixel-space polygon can never match: every zone coordinate is
    then larger than the point by 2-3 orders of magnitude, so the point reads as
    permanently outside every zone regardless of where the person actually stands.

    This scales up only when the bbox looks normalized (its largest raw coordinate
    is at most ~1) and a real frame size is available; an already-pixel-space bbox,
    or a frame whose dimensions could not be resolved, is returned unchanged --
    exactly today's behaviour, so a deployment that was already working correctly
    is not affected.
    """
    if _bbox_extent(bbox) > 1.02:
        return point
    width, height = resolve_frame_dims(stream_info)
    if width <= 0 or height <= 0:
        return point
    return (point[0] * width, point[1] * height)


def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.

    Args:
        point1: First point (x, y)
        point2: Second point (x, y)

    Returns:
        float: Euclidean distance
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def calculate_bbox_overlap(bbox1: Dict[str, float], bbox2: Dict[str, float]) -> float:
    """
    Calculate IoU (Intersection over Union) between two bounding boxes.

    Args:
        bbox1: First bounding box
        bbox2: Second bounding box

    Returns:
        float: IoU value between 0 and 1
    """
    return calculate_iou(bbox1, bbox2)


def calculate_iou(bbox1: Dict[str, float], bbox2: Dict[str, float]) -> float:
    """
    Calculate IoU (Intersection over Union) between two bounding boxes.

    Args:
        bbox1: First bounding box
        bbox2: Second bounding box

    Returns:
        float: IoU value between 0 and 1
    """

    # Normalize bbox format
    def normalize_bbox_coords(bbox):
        if "xmin" in bbox:
            return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
        elif "x1" in bbox:
            return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
        else:
            values = list(bbox.values())
            return values[:4]

    box1 = normalize_bbox_coords(bbox1)
    box2 = normalize_bbox_coords(bbox2)

    # Calculate intersection
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    if x2 < x1 or y2 < y1:
        return 0.0

    intersection = (x2 - x1) * (y2 - y1)

    # Calculate union
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0.0


def get_bbox_area(bbox: Dict[str, float]) -> float:
    """
    Calculate area of bounding box.

    Args:
        bbox: Bounding box dict

    Returns:
        float: Area of the bounding box
    """
    if "xmin" in bbox and "xmax" in bbox and "ymin" in bbox and "ymax" in bbox:
        return (bbox["xmax"] - bbox["xmin"]) * (bbox["ymax"] - bbox["ymin"])
    elif "x1" in bbox and "x2" in bbox and "y1" in bbox and "y2" in bbox:
        return (bbox["x2"] - bbox["x1"]) * (bbox["y2"] - bbox["y1"])
    else:
        values = list(bbox.values())
        if len(values) >= 4:
            return (values[2] - values[0]) * (values[3] - values[1])
    return 0.0


def normalize_bbox(bbox: Dict[str, float], image_width: float, image_height: float) -> Dict[str, float]:
    """
    Normalize bounding box coordinates to [0, 1] range.

    Args:
        bbox: Bounding box dict
        image_width: Image width
        image_height: Image height

    Returns:
        Dict[str, float]: Normalized bounding box
    """
    if "xmin" in bbox:
        return {
            "xmin": bbox["xmin"] / image_width,
            "ymin": bbox["ymin"] / image_height,
            "xmax": bbox["xmax"] / image_width,
            "ymax": bbox["ymax"] / image_height,
        }
    elif "x1" in bbox:
        return {
            "x1": bbox["x1"] / image_width,
            "y1": bbox["y1"] / image_height,
            "x2": bbox["x2"] / image_width,
            "y2": bbox["y2"] / image_height,
        }
    else:
        # Handle generic format
        keys = list(bbox.keys())
        values = list(bbox.values())
        normalized_values = [
            values[0] / image_width,
            values[1] / image_height,
            values[2] / image_width,
            values[3] / image_height,
        ]
        return dict(zip(keys, normalized_values))


def denormalize_bbox(bbox: Dict[str, float], image_width: float, image_height: float) -> Dict[str, float]:
    """
    Denormalize bounding box coordinates from [0, 1] range to pixel coordinates.

    Args:
        bbox: Normalized bounding box dict
        image_width: Image width
        image_height: Image height

    Returns:
        Dict[str, float]: Denormalized bounding box
    """
    if "xmin" in bbox:
        return {
            "xmin": bbox["xmin"] * image_width,
            "ymin": bbox["ymin"] * image_height,
            "xmax": bbox["xmax"] * image_width,
            "ymax": bbox["ymax"] * image_height,
        }
    elif "x1" in bbox:
        return {
            "x1": bbox["x1"] * image_width,
            "y1": bbox["y1"] * image_height,
            "x2": bbox["x2"] * image_width,
            "y2": bbox["y2"] * image_height,
        }
    else:
        # Handle generic format
        keys = list(bbox.keys())
        values = list(bbox.values())
        denormalized_values = [
            values[0] * image_width,
            values[1] * image_height,
            values[2] * image_width,
            values[3] * image_height,
        ]
        return dict(zip(keys, denormalized_values))


def line_segments_intersect(
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    p3: Tuple[float, float],
    p4: Tuple[float, float],
) -> bool:
    """
    Check if two line segments intersect.

    Args:
        p1: First point of first line segment
        p2: Second point of first line segment
        p3: First point of second line segment
        p4: Second point of second line segment

    Returns:
        bool: True if line segments intersect
    """

    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)
