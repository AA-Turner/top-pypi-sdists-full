"""Auto-generated stub for module: geometry_utils."""
from typing import Any, Dict, List, Optional, Tuple, Union

# Functions
def calculate_bbox_overlap(bbox1: Dict[str, float], bbox2: Dict[str, float]) -> float:
    """
    Calculate IoU (Intersection over Union) between two bounding boxes.
    
    Args:
        bbox1: First bounding box
        bbox2: Second bounding box
    
    Returns:
        float: IoU value between 0 and 1
    """
    ...
def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1: First point (x, y)
        point2: Second point (x, y)
    
    Returns:
        float: Euclidean distance
    """
    ...
def calculate_iou(bbox1: Dict[str, float], bbox2: Dict[str, float]) -> float:
    """
    Calculate IoU (Intersection over Union) between two bounding boxes.
    
    Args:
        bbox1: First bounding box
        bbox2: Second bounding box
    
    Returns:
        float: IoU value between 0 and 1
    """
    ...
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
    ...
def get_bbox_area(bbox: Dict[str, float]) -> float:
    """
    Calculate area of bounding box.
    
    Args:
        bbox: Bounding box dict
    
    Returns:
        float: Area of the bounding box
    """
    ...
def get_bbox_bottom10_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get bottom 10% center point of bounding box (x at horizontal center).
    """
    ...
def get_bbox_bottom25_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get bottom 25% center point of bounding box.
    
    Args:
        bbox: Bounding box dict with coordinates or list [x1, y1, x2, y2]
    
    Returns:
        Tuple[float, float]: (x, y) coordinates at bottom 25% height from center X
    """
    ...
def get_bbox_bottom_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get bottom-center point of bounding box (horizontal center, bottom edge).
    
    Used for floor-level zone membership (foot-in-zone semantics).
    """
    ...
def get_bbox_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get center point of bounding box.
    
    Args:
        bbox: Bounding box dict with coordinates or list [x1, y1, x2, y2]
    
    Returns:
        Tuple[float, float]: (x, y) center coordinates
    """
    ...
def line_segments_intersect(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
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
    ...
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
    ...
def point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """
    Check if point is inside polygon using ray casting algorithm.
    
    Args:
        point: (x, y) coordinate tuple
        polygon: List of (x, y) coordinate tuples defining the polygon
    
    Returns:
        bool: True if point is inside polygon
    """
    ...
def reference_size_from_payload(data: Any) -> Tuple[int, int]:
    """
    ``(width, height)`` from a detections payload's ``coordinate_frame``, or ``(0, 0)``.
    
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
    ...
def resolve_frame_dims(stream_info: Optional[Dict[str, Any]]) -> Tuple[int, int]:
    """
    Best-effort ``(width, height)`` from ``stream_info``, or ``(0, 0)`` if unknown.
    
        Two shapes have both shipped for ``stream_resolution`` across this codebase: a
        top-level ``{"width": .., "height": ..}`` dict (``intrusion_detection.py``'s own
        ``_frame_dims``), and ``input_settings.stream_resolution`` as either the same
        dict shape or a bare ``[width, height]`` pair (``Trackers/det_utils.py``). This
        tries all of them, in that order, and returns ``(0, 0)`` -- not a guessed
        fallback -- when none resolve, so a caller can tell "no dimensions" apart from
        a real ``0x0`` stream and skip whatever scaling it wanted these for.
    """
    ...
def to_zone_test_point(point: Tuple[float, float], bbox: Union[Dict[str, float], List[float]], stream_info: Optional[Dict[str, Any]] = None) -> Tuple[float, float]:
    """
    Scale a bbox-derived point (e.g. from :func:`get_bbox_bottom_center`) to
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
    ...
