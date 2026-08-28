"""Stub file for post_processing.utils directory."""
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from ...analytics.engine_session import resolve_camera_fields_from_stream_info
from ...analytics.engine_session import resolve_camera_fields_from_stream_info, resolve_location_for_publish
from ...analytics.schemas import IncidentEvent, IncidentMessage, StreamInfo
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.base import ResultFormat
from ..core.base import registry
from .filter_utils import filter_by_confidence
from .format_utils import match_results_structure
from .geometry_utils import calculate_iou
from .geometry_utils import get_bbox_area
from .geometry_utils import get_bbox_bottom_center, point_in_polygon, to_zone_test_point
from .geometry_utils import get_bbox_center, line_segments_intersect, point_in_polygon
from .geometry_utils import get_bbox_center, point_in_polygon
from .incident_res_format import _pick_str, build_incident_res_message
from .incident_res_format import build_incident_res_message
from .incident_res_format import is_valid_incident_end_time
from .incident_res_format import is_valid_incident_end_time, normalize_incident_timestamp, utc_now_iso_z
from .incident_res_format import utc_now_iso_z
from .legacy_analytics_bridge import get_legacy_profile
from .location_name_cache import LocationNameCache
from .post_processing_config_client import PostProcessingConfigClient
from .post_processing_config_client import is_null_object_id, is_resolvable_location_id
from .post_processing_config_client import is_null_object_id, is_resolvable_location_id, looks_like_object_id, normalize_location_id
from .post_processing_config_client import is_resolvable_location_id, normalize_location_id
from .public_ip import resolve_public_ip_once
from .stream_time_utils import force_wallclock_stream_time, wallclock_incident_stream_time
from .visualization_utils import bbox_dict_to_xyxy
from .weapon_person_fusion_v1 import _norm_cat, _xyxy_from_det, coerce_frame_detections, iou_positive_or_centroid_inside

# Constants
AGGREGATION_TYPES: List[Any] = ...  # From business_metrics_manager_utils
DEFAULT_AGGREGATION_INTERVAL: int = ...  # From business_metrics_manager_utils
DEFAULT_METRICS_CONFIG: Dict[Any, Any] = ...  # From business_metrics_manager_utils
CANONICAL_COLOR_LAB: Any = ...  # From color_utils
CANONICAL_COLOR_NAMES: List[Any] = ...  # From color_utils
CANONICAL_COLOR_RGB: Dict[Any, Any] = ...  # From color_utils
XKCD_COLORS: Any = ...  # From color_utils
logger: Any = ...  # From color_utils
logger: Any = ...  # From filter_utils
DEFAULT_THRESHOLDS: List[Any] = ...  # From incident_manager_utils
LOITERING_DEFAULT_THRESHOLDS: List[Any] = ...  # From incident_manager_utils
OVERCROWDING_DEFAULT_THRESHOLDS: List[Any] = ...  # From incident_manager_utils
SEVERITY_LEVELS: List[Any] = ...  # From incident_manager_utils
WEAPON_DEFAULT_THRESHOLDS: List[Any] = ...  # From incident_manager_utils
AGGREGATION_INTERVAL_SEC: float = ...  # From legacy_analytics_bridge
ANALYTICS_ZONE_GLOBAL: str = ...  # From legacy_analytics_bridge
LEGACY_PUBLISHER_ENV: str = ...  # From legacy_analytics_bridge
logger: Any = ...  # From legacy_analytics_bridge
GEOMETRY_RETRY_INTERVAL: int = ...  # From post_processing_config_client
ENV_SKIP_PUBLIC_IP: str = ...  # From public_ip
logger: Any = ...  # From smoothing_utils
ENV_FLAG: str = ...  # From stream_time_utils
FIRE_TIMESTAMP_FMT: str = ...  # From stream_time_utils
INCIDENT_STREAM_TIME_FMT: str = ...  # From stream_time_utils
logger: Any = ...  # From tailgating_utils
logger: Any = ...  # From wrong_way_tracker

# Functions
# From advanced_counting_utils
def calculate_bbox_fingerprint(bbox: Dict, category: str = '') -> str:
    """
    Calculate a fingerprint for bbox deduplication.
    """
    ...

# From advanced_counting_utils
def calculate_bbox_overlap(bbox1: Dict, bbox2: Dict) -> float:
    """
    Calculate overlap between two bounding boxes.
    """
    ...

# From advanced_counting_utils
def clean_expired_tracks(track_timestamps: Dict, track_last_seen: Dict, current_timestamp: float, expiry_seconds: int) -> Any:
    """
    Clean expired tracks from tracking dictionaries.
    """
    ...

# From advanced_helper_utils
def bytes_to_image(image_bytes: Any, return_format: str = 'pil') -> Optional[Any]:
    """
    Convert image bytes to PIL Image or numpy array.
    """
    ...

# From advanced_helper_utils
def bytes_to_video_frame(video_bytes: Any, frame_number: int = 0, return_format: str = 'cv2') -> Optional[Any]:
    """
    Extract a specific frame from video bytes.
    """
    ...

# From advanced_helper_utils
def calculate_bbox_fingerprint(bbox: Dict[str, float], category: str = 'unknown') -> str:
    """
    Generate a fingerprint for bbox deduplication.
    """
    ...

# From advanced_helper_utils
def clean_expired_tracks(track_timestamps: Dict, track_last_seen: Dict, current_timestamp: float, expiry_time: float) -> None:
    """
    Clean expired tracks from tracking dictionaries.
    """
    ...

# From advanced_helper_utils
def convert_detection_to_tracking_format(detections: List[Dict], frame_id: str = '0') -> Dict:
    """
    Convert detection format to tracking format.
    """
    ...

# From advanced_helper_utils
def convert_tracking_to_detection_format(tracking_results: Dict) -> List[Dict]:
    """
    Convert tracking format to detection format.
    """
    ...

# From advanced_helper_utils
def generate_summary_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate comprehensive summary statistics from tracking data.
    """
    ...

# From advanced_helper_utils
def get_image_dimensions(image_bytes: Any) -> Optional[Tuple[int, int]]:
    """
    Get image dimensions (width, height) from image bytes.
    """
    ...

# From advanced_helper_utils
def get_image_format(image_bytes: Any) -> Optional[str]:
    """
    Detect image format from bytes.
    """
    ...

# From advanced_helper_utils
def is_valid_image_bytes(image_bytes: Any) -> bool:
    """
    Check if bytes represent a valid image.
    """
    ...

# From advanced_helper_utils
def line_segments_intersect(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float], p4: Tuple[float, float]) -> bool:
    """
    Check if two line segments intersect.
    """
    ...

# From agnostic_nms
def apply_nms(detections: List[Dict[str, Any]], iou_threshold: float = 0.45, class_agnostic: bool = True, min_box_size: float = 2.0, use_vectorized: bool = True) -> List[Dict[str, Any]]:
    """
    Convenience function for one-time NMS application.
    
    Args:
        detections: List of detection dicts
        iou_threshold: IoU threshold for suppression
        class_agnostic: If True, suppress across all classes
        min_box_size: Minimum box dimension in pixels
        use_vectorized: Use PyTorch implementation if available
    
    Returns:
        Filtered list of detections
    
    Example:
        >>> detections = [
        ...     {"category": "car", "confidence": 0.9,
        ...      "bounding_box": {"x1": 100, "y1": 100, "x2": 200, "y2": 200}},
        ...     {"category": "car", "confidence": 0.85,
        ...      "bounding_box": {"x1": 105, "y1": 105, "x2": 205, "y2": 205}}
        ... ]
        >>> filtered = apply_nms(detections, iou_threshold=0.5, class_agnostic=True)
        >>> len(filtered)
        1
    """
    ...

# From alerting_utils
def check_dwell_time_alert(track_dwell_times: Dict[int, float], max_dwell_time: float) -> Dict:
    """
    Check dwell time alerts.
    """
    ...

# From alerting_utils
def check_threshold_alert(results: Any, threshold: int, category: str = 'all') -> Dict:
    """
    Check if count exceeds threshold.
    """
    ...

# From alerting_utils
def check_zone_occupancy_alert(zone_counts: Dict[str, int], zone_thresholds: Dict[str, int]) -> Dict:
    """
    Check zone occupancy alerts.
    """
    ...

# From alerting_utils
def trigger_alerts(results: Any, category_count_threshold: Dict[str, int] = None, category_triggers: List[str] = None) -> List[Dict]:
    """
    Convenience function to trigger alerts.
    
    Args:
        results: Detection/tracking results
        category_count_threshold: Count thresholds by category
        category_triggers: Categories that should trigger alerts
    
    Returns:
        List of triggered alert events
    """
    ...

# From business_metrics_manager_utils
def get_business_metrics_manager(config: Any, logger: Optional[Any.Any] = None, aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL, metrics_config: Optional[Dict[str, str]] = None) -> Optional[Any]:
    """
    Get or create BUSINESS_METRICS_MANAGER instance.
    
    This is a convenience function that uses a module-level factory.
    For more control, use BusinessMetricsManagerFactory directly.
    
    Args:
        config: Configuration object with session, server_id, etc.
        logger: Logger instance
        aggregation_interval: Interval in seconds for aggregation (default 300)
        metrics_config: Dict of metric_name -> aggregation_type
    
    Returns:
        BUSINESS_METRICS_MANAGER instance or None
    """
    ...

# From bytetrack_utils
def bbox_centroid(bbox: Dict[str, Any]) -> Tuple[float, float]: ...

# From bytetrack_utils
def bbox_feet_point(bbox: Dict[str, Any]) -> Tuple[float, float]: ...

# From bytetrack_utils
def bbox_iou(a: Dict[str, Any], b: Dict[str, Any]) -> float: ...

# From bytetrack_utils
def bbox_to_xyxy(bbox: Dict[str, Any]) -> Tuple[float, float, float, float]:
    """
    Supports both:
      - Matrice: xmin,ymin,xmax,ymax
      - Alternate: x1,y1,x2,y2
    """
    ...

# From bytetrack_utils
def dist(a: Tuple[float, float], b: Tuple[float, float]) -> float: ...

# From bytetrack_utils
def iou_xyxy(a: Any.Any, b: Any.Any) -> float: ...

# From bytetrack_utils
def make_runtime_bytetrack_config() -> str:
    """
    Create a temporary runtime ByteTrack YAML config for Ultralytics YOLO.track().
    Returns:
        str: YAML path that can be passed into YOLO.track(tracker=...)
    """
    ...

# From bytetrack_utils
def matrice_dets_to_xyxy_score(dets: List[Dict[str, Any]]) -> Any.Any: ...

# From bytetrack_utils
def smooth_point(prev: Tuple[float, float], new: Tuple[float, float], alpha: float) -> Tuple[float, float]: ...

# From bytetrack_utils
def ultralytics_track_to_matrice_dets(results: Any, person_class_id: int = 0) -> List[Dict[str, Any]]:
    """
    Convert ultralytics YOLO.track() output to Matrice detections list.
    
    Output schema:
    {
      "track_id": int,
      "confidence": float,
      "category": str (class id as string),
      "bounding_box": {"xmin","ymin","xmax","ymax"}
    }
    """
    ...

# From bytetrack_utils
def validate_bytetrack_cfg(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate + sanitize an Ultralytics ByteTrack YAML config dict.
    
    Returns:
        A cleaned cfg dict (safe types + clamped thresholds).
    Raises:
        ValueError if mandatory keys are missing or invalid beyond repair.
    """
    ...

# From category_mapping_utils
def apply_category_mapping(results: Any, index_to_category: Dict[int, str]) -> Any:
    """
    Convenience function to apply category mapping to results.
    
    Args:
        results: Raw results to map
        index_to_category: Mapping from indices to category names
    
    Returns:
        Results with mapped categories
    """
    ...

# From category_mapping_utils
def create_category_mapper(index_to_category: Dict[int, str]) -> Any:
    """
    Create a category mapper instance.
    
    Args:
        index_to_category: Mapping from indices to category names
    
    Returns:
        CategoryMappingLibrary instance
    """
    ...

# From color_utils
def extract_major_colors(image: Any.Any, k: int = 3) -> List[Tuple[str, str, float]]:
    """
    Extract the major colors from an image using K-means clustering.
    
    Args:
        image: Input image as numpy array (RGB format)
        k: Number of dominant colors to extract
    
    Returns:
        List of tuples containing (color_name, hex_color, percentage)
    """
    ...

# From color_utils
def process_video_with_color_detection(video_bytes: Any, predictions: Dict[str, List[Dict]], output_dir: str = './output', top_k_colors: int = 3, min_confidence: float = 0.5, fps: Optional[float] = None) -> Tuple[str, str]:
    """
    Convenience function to process video with color detection.
    
    Args:
        video_bytes: Raw video file bytes
        predictions: Dict with frame_id -> list of detection dicts
        output_dir: Directory to save output files
        top_k_colors: Number of top colors to extract per detection
        min_confidence: Minimum confidence threshold for detections
        fps: Video FPS (will be auto-detected if not provided)
    
    Returns:
        Tuple of (detailed_results_path, summary_results_path)
    """
    ...

# From counting_utils
def calculate_counting_summary(results: Any, zones: Optional[Dict[str, List[List[float]]]] = None) -> Dict[str, Any]:
    """
    Calculate comprehensive counting summary.
    
    Args:
        results: Detection/tracking results
        zones: Optional zone definitions
    
    Returns:
        Dict[str, Any]: Comprehensive counting summary
    """
    ...

# From counting_utils
def count_objects_by_category(results: Any) -> Dict[str, int]:
    """
    Count objects by category from detection results.
    
    Args:
        results: Detection results (list or dict format)
    
    Returns:
        Dict[str, int]: Category counts
    """
    ...

# From counting_utils
def count_objects_in_zones(results: Any, zones: Dict[str, List[List[float]]], stream_info: Optional[Any] = None) -> Dict[str, Dict[str, int]]:
    """
    Count objects in defined zones.
    
    Args:
        results: Detection results
        zones: Dictionary of zone_name -> polygon coordinates
    
    Returns:
        Dict[str, Dict[str, int]]: Zone counts by category
    """
    ...

# From counting_utils
def count_unique_tracks(results: Dict[str, List[Dict]]) -> Dict[str, int]:
    """
    Count unique tracks by category from tracking results.
    
    Args:
        results: Tracking results in frame format
    
    Returns:
        Dict[str, int]: Unique track counts by category
    """
    ...

# From counting_utils
def parse_line_config(line_config: Any) -> Any.Any:
    """
    Parse a line definition into a (2, 2) numpy array.
    
    Accepts either:
      - [x1, y1, x2, y2]        (flat list)
      - [[x1, y1], [x2, y2]]    (nested list)
    
    Returns:
        np.ndarray: shape (2, 2) with dtype float64
    """
    ...

# From counting_utils
def polygon_offset_inward(polygon: Any.Any, offset: float) -> Any.Any:
    """
    Inset polygon inward by a constant offset (in pixels).
    Each edge is shifted inward along its inward-pointing normal; new vertices
    are the intersections of consecutive shifted edges.
    
    Args:
        polygon: (N, 2) array of polygon vertices
        offset: Number of pixels to inset
    
    Returns:
        np.ndarray: Inset polygon vertices (N, 2), dtype int32
    """
    ...

# From filter_utils
def apply_category_mapping(results: Any, index_to_category: Dict[str, str]) -> Any:
    """
    Apply category index to name mapping.
    
    This is where a deployment's ``class_index_map`` becomes ``detection["category"]``,
    which makes it the boundary where a malformed entry turns into silent data loss.
    Two hardenings live here for that reason:
    
    * **Labels are stripped.** A real deployment carried
      ``{"0": "knife", "1": "gun "}`` -- one trailing space. The weapon manifest's
      ``entity_mapping`` is ``{knife: knife, gun: gun}``, ``"gun "`` matched nothing,
      and because an unmapped class is *ignored* rather than rejected, the app detected
      nothing, published nothing and raised no incident. Silently. Forever.
    * **An index the map does not cover is reported.** Previously there was no branch at
      all: the detection kept its numeric category and was dropped by a later category
      filter. That is the other half of the same outage -- the weapon manifest declared
      six classes against a two-entry map, so indices 2-5 resolved to nothing.
    
    Args:
        results: Detection or tracking results
        index_to_category: Mapping from category index to category name
    
    Returns:
        Results with mapped category names
    """
    ...

# From filter_utils
def calculate_bbox_fingerprint(bbox: Dict[str, Any], category: str = '') -> str:
    """
    Calculate a fingerprint for a bounding box to detect duplicates.
    
    Args:
        bbox: Bounding box dictionary
        category: Object category
    
    Returns:
        str: Unique fingerprint for the bbox
    """
    ...

# From filter_utils
def clean_expired_tracks(track_timestamps: Dict[str, float], track_last_seen: Dict[str, float], current_timestamp: float, expiry_time: float) -> None:
    """
    Clean expired tracks from tracking dictionaries.
    
    Args:
        track_timestamps: Dictionary of track_id -> first_seen_timestamp
        track_last_seen: Dictionary of track_id -> last_seen_timestamp
        current_timestamp: Current timestamp
        expiry_time: Time after which tracks expire
    """
    ...

# From filter_utils
def filter_by_area(results: Any, min_area: float = 0, max_area: float = float('inf')) -> Any:
    """
    Filter detections by bounding box area.
    
    Args:
        results: Detection or tracking results
        min_area: Minimum bounding box area
        max_area: Maximum bounding box area
    
    Returns:
        Filtered results
    """
    ...

# From filter_utils
def filter_by_categories(results: Any, allowed_categories: List[str]) -> Any:
    """
    Filter results to only include specified categories.
    
    Args:
        results: Detection or tracking results
        allowed_categories: List of allowed category names
    
    Returns:
        Filtered results in the same format
    """
    ...

# From filter_utils
def filter_by_confidence(results: Any, threshold: float = 0.5) -> Any:
    """
    Filter results by confidence threshold.
    
    Args:
        results: Detection or tracking results
        threshold: Minimum confidence threshold
    
    Returns:
        Filtered results in the same format
    """
    ...

# From filter_utils
def remove_duplicate_detections(results: List[Dict[str, Any]], similarity_threshold: float = 0.8) -> List[Dict[str, Any]]:
    """
    Remove duplicate detections based on bbox similarity.
    
    Args:
        results: List of detection dictionaries
        similarity_threshold: IoU threshold for considering detections as duplicates
    
    Returns:
        List of unique detections
    """
    ...

# From format_utils
def convert_detection_to_tracking_format(detections: List[Dict], frame_id: str = '0') -> Dict:
    """
    Convert detection format to tracking format.
    
    Args:
        detections: List of detection dictionaries
        frame_id: Frame identifier
    
    Returns:
        Dict: Results in tracking format
    """
    ...

# From format_utils
def convert_to_coco_format(results: Any) -> List[Dict]:
    """
    Convert results to COCO format.
    
    Args:
        results: Input results in any supported format
    
    Returns:
        List[Dict]: Results in COCO format
    """
    ...

# From format_utils
def convert_to_tracking_format(detections: List[Dict], frame_id: str = '0') -> Dict:
    """
    Convert detection format to tracking format.
    
    Args:
        detections: List of detection dictionaries
        frame_id: Frame identifier
    
    Returns:
        Dict: Results in tracking format
    """
    ...

# From format_utils
def convert_to_yolo_format(results: Any) -> List[List[float]]:
    """
    Convert results to YOLO format (normalized coordinates).
    
    Args:
        results: Input results in any supported format
    
    Returns:
        List[List[float]]: Results in YOLO format [class_id, x_center, y_center, width, height, confidence]
    """
    ...

# From format_utils
def convert_tracking_to_detection_format(tracking_results: Dict) -> List[Dict]:
    """
    Convert tracking format to detection format.
    
    Args:
        tracking_results: Tracking results dictionary
    
    Returns:
        List[Dict]: Results in detection format
    """
    ...

# From format_utils
def match_results_structure(results: Any) -> Any:
    """
    Match the results structure to the expected structure based on actual output formats.
    
    Based on eg_output.json:
    - Classification: {"category": str, "confidence": float}
    - Detection: [{"bounding_box": {...}, "category": str, "confidence": float}, ...]
    - Instance Segmentation: Same as detection but with "masks" field
    - Object Tracking: {"frame_id": [{"track_id": int, "category": str, "confidence": float, "bounding_box": {...}}, ...]}
    - Activity Recognition: {"frame_id": [{"category": str, "confidence": float, "bounding_box": {...}}, ...]} (no track_id)
    
    Args:
        results: Raw model output to analyze
    
    Returns:
        ResultFormat: Detected format type
    """
    ...

# From geometry_utils
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

# From geometry_utils
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

# From geometry_utils
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

# From geometry_utils
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

# From geometry_utils
def get_bbox_area(bbox: Dict[str, float]) -> float:
    """
    Calculate area of bounding box.
    
    Args:
        bbox: Bounding box dict
    
    Returns:
        float: Area of the bounding box
    """
    ...

# From geometry_utils
def get_bbox_bottom10_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get bottom 10% center point of bounding box (x at horizontal center).
    """
    ...

# From geometry_utils
def get_bbox_bottom25_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get bottom 25% center point of bounding box.
    
    Args:
        bbox: Bounding box dict with coordinates or list [x1, y1, x2, y2]
    
    Returns:
        Tuple[float, float]: (x, y) coordinates at bottom 25% height from center X
    """
    ...

# From geometry_utils
def get_bbox_bottom_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get bottom-center point of bounding box (horizontal center, bottom edge).
    
    Used for floor-level zone membership (foot-in-zone semantics).
    """
    ...

# From geometry_utils
def get_bbox_center(bbox: Union[Dict[str, float], List[float]]) -> Tuple[float, float]:
    """
    Get center point of bounding box.
    
    Args:
        bbox: Bounding box dict with coordinates or list [x1, y1, x2, y2]
    
    Returns:
        Tuple[float, float]: (x, y) center coordinates
    """
    ...

# From geometry_utils
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

# From geometry_utils
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

# From geometry_utils
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

# From geometry_utils
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

# From geometry_utils
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

# From geometry_utils
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

# From incident_manager_utils
def get_incident_manager(config: Any, logger: Optional[Any.Any] = None) -> Optional[Any]:
    """
    Get or create INCIDENT_MANAGER instance.
    
    This is a convenience function that uses a module-level factory.
    For more control, use IncidentManagerFactory directly.
    
    Args:
        config: Configuration object with session, server_id, etc.
        logger: Logger instance
    
    Returns:
        INCIDENT_MANAGER instance or None
    """
    ...

# From incident_res_format
def build_incident_res_message(incident_data: Dict[str, Any], stream_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Serialize a legacy incident dict to the canonical ``incident_res`` envelope.
    """
    ...

# From incident_res_format
def format_incident_human_text(incident_type: str, severity_level: str) -> str: ...

# From incident_res_format
def is_valid_incident_end_time(value: Any) -> bool:
    """
    True when ``value`` is a real closing timestamp (not a lifecycle placeholder).
    """
    ...

# From incident_res_format
def map_severity_for_wire(level: str) -> str:
    """
    Map internal ``significant`` to backend ``high``.
    """
    ...

# From incident_res_format
def normalize_incident_timestamp(value: Any) -> str:
    """
    Coerce a legacy use case's start_time/end_time into RFC3339 (``%Y-%m-%dT%H:%M:%SZ``).
    
        Unparseable or empty input is returned unchanged (as ``_pick_str`` would leave it) --
        passing through rather than dropping data on a shape not seen before.
    """
    ...

# From incident_res_format
def stream_info_dict_to_stream_info(stream_info: Optional[Dict[str, Any]]) -> Any:
    """
    Map legacy pipeline ``stream_info`` dict → :class:`StreamInfo`.
    """
    ...

# From incident_res_format
def utc_now_iso_z() -> str: ...

# From legacy_analytics_bridge
def build_incident_message(incident_data: Dict[str, Any], stream_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build ``incident_res`` payload matching NEW-flow ``IncidentMessage``.
    """
    ...

# From legacy_analytics_bridge
def extract_stream_context(stream_info: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """
    Resolve camera / deployment identity fields for Redis envelopes.
    """
    ...

# From legacy_analytics_bridge
def get_legacy_profile(usecase: str) -> Optional[Any]:
    """
    Explicit profile if registered, else a synthesized default profile.
    
        Returns ``None`` only for the documented still-image exclusions, so that a
        caller can distinguish "no analytics wiring" from "default wiring".
    """
    ...

# From legacy_analytics_bridge
def get_legacy_session(stream_key: str) -> 'Any': ...

# From legacy_analytics_bridge
def legacy_redis_analytics_usecases() -> Any[str]:
    """
    Every legacy app the SDK self-publishes (incident_res + results-agg).
    
        Full coverage: the explicit profiles PLUS every use-case in the processor
        registry, minus the documented still-image exclusions. Returns an EMPTY set
        when :data:`LEGACY_PUBLISHER_ENV` is truthy, ceding ownership to the caller's
        old ``AnalyticsPublisher`` so there is no double-publish.
    """
    ...

# From legacy_analytics_bridge
def publish_legacy_frame_analytics() -> None:
    """
    Ingest one legacy frame and publish Redis analytics when due.
    
    ``incident_via_manager`` is True when ``IncidentManager`` already handled
    the incident for this frame (skip duplicate ``incident_res`` publish).
    """
    ...

# From legacy_analytics_bridge
def reset_legacy_sessions() -> None: ...

# From post_processing_config_client
def is_null_object_id(value: Any) -> bool:
    """
    Return True for the all-zero placeholder ObjectId (unset location).
    """
    ...

# From post_processing_config_client
def is_resolvable_location_id(value: Any) -> bool:
    """
    Return True when ``value`` is a real location ObjectId worth API lookup.
    """
    ...

# From post_processing_config_client
def looks_like_object_id(value: Any) -> bool:
    """
    Return True when ``value`` looks like a MongoDB ObjectId (24 hex chars).
    """
    ...

# From post_processing_config_client
def normalize_location_id(value: Any) -> str:
    """
    Return a stripped location id, or empty for unset / null ObjectId placeholders.
    """
    ...

# From public_ip
def reset_cache() -> None:
    """
    Forget the resolved value so the next call looks it up again.
    
        Test support. Production never calls this: the whole point of the module is
        that the answer is decided once, and re-deciding it re-introduces the
        per-frame stall this replaced.
    """
    ...

# From public_ip
def resolve_public_ip_once(logger: Optional[Any.Any] = None) -> str:
    """
    This host's public IP, resolved at most once per process.
    
        Returns ``"localhost"`` when the lookup is disabled or fails. The lock is
        held across the request so N first-frame initialisers racing on startup make
        one lookup between them rather than N.
    """
    ...

# From smoothing_utils
def bbox_smoothing(detections: Union[List[Dict], Dict[str, List[Dict]]], config: Any, tracker: Optional[Any] = None) -> Union[List[Dict], Dict[str, List[Dict]]]:
    """
    Apply smoothing algorithm to bbox detections.
    
    Args:
        detections: Either:
                   - List of detection dictionaries (detection format)
                   - Dict with frame keys containing lists of detections (tracking format)
        config: Smoothing configuration
        tracker: Optional tracker instance for persistent state across frames
    
    Returns:
        Same format as input: List[Dict] or Dict[str, List[Dict]]
    """
    ...

# From smoothing_utils
def create_bbox_smoothing_tracker(config: Any) -> Any:
    """
    Create a new bbox smoothing tracker instance.
    
    Args:
        config: Smoothing configuration
    
    Returns:
        BBoxSmoothingTracker: New tracker instance
    """
    ...

# From smoothing_utils
def create_default_smoothing_config(**overrides: Any) -> Any:
    """
    Create default smoothing configuration with optional overrides.
    
    Args:
        **overrides: Configuration overrides
    
    Returns:
        BBoxSmoothingConfig: Configuration instance
    """
    ...

# From stream_time_utils
def force_wallclock_stream_time() -> bool:
    """
    True when ``MATRICE_FORCE_WALLCLOCK_STREAM_TIME`` is set to a truthy value.
    """
    ...

# From stream_time_utils
def set_wallclock_now_provider(provider: Optional[Callable[[], Any]]) -> None:
    """
    Override the wall-clock source. Pass ``None`` to restore the real clock.
    
        Intended for tests that need a deterministic "now"; production leaves it at
        the default (:func:`datetime.now`).
    """
    ...

# From stream_time_utils
def wallclock_fire_timestamp() -> str:
    """
    Wall-clock timestamp in the fire-detection human-text format.
    """
    ...

# From stream_time_utils
def wallclock_incident_stream_time() -> str:
    """
    Wall-clock stream_time in the incident-message format.
    """
    ...

# From stream_time_utils
def wallclock_now() -> Any:
    """
    Return the current wall-clock time from the (possibly injected) source.
    """
    ...

# From tailgating_utils
def analyze_passage(crossings: List[Any], allowed_persons: int, max_follow_dt: float) -> Any: ...

# From tailgating_utils
def build_side_zone_map(line_p1: Any, line_p2: Any, zones: Dict[str, List[List[float]]]) -> Optional[Dict[int, str]]:
    """
    Map the two sides of an access line to the two shared zone names.
    
        Uses each zone's centroid signed distance to the line. Returns
        ``{1: zone_on_positive_side, -1: zone_on_negative_side}`` or ``None`` when the
        configuration is degenerate (not exactly two zones, or both centroids fall on
        the same side / on the line). A ``None`` result means direction can still be
        detected but cannot be labelled with zone names.
    """
    ...

# From tailgating_utils
def detect_crossing(track_side_state: Dict[str, Any], foot: Any, line_p1: Any, line_p2: Any) -> Tuple[bool, Optional[int]]:
    """
    Anchored, bidirectional crossing detector for one ``(line, track)`` pair.
    
        ``track_side_state`` is a mutable dict holding ``last_side`` (``+1``/``-1`` of the
        most recent *clear* side) and ``last_side_pt`` (the foot point recorded there).
    
        The detector is robust to the gap between the zone polygons and the access
        line: while the foot is within ``side_margin`` of the line (i.e. in the gap or
        on the line, typically inside neither polygon) the anchor is **held** and
        nothing fires. A crossing is reported only when the foot reaches the opposite
        *clear* side and the straight path from the anchor to the current foot
        intersects the finite access-line segment. Because attribution uses the finite
        segment, walking around a line end does not count, and an arbitrarily wide gap
        in the middle of the traversal does not suppress detection.
    
        Returns ``(crossed, direction)`` where ``direction`` is ``+1`` when the foot
        crossed onto the positive side of the line and ``-1`` onto the negative side.
        Mutates ``track_side_state`` in place.
    """
    ...

# From tailgating_utils
def motion_vector(p0: Any, p1: Any) -> Tuple[float, float]: ...

# From tailgating_utils
def normalize(v: Tuple[float, float]) -> Tuple[float, float]: ...

# From tailgating_utils
def polygon_centroid(poly: List[List[float]]) -> Tuple[float, float]:
    """
    Arithmetic centroid of polygon vertices (sufficient for side assignment).
    """
    ...

# From tailgating_utils
def segment_intersects_line(p0: Any, p1: Any, l0: Any, l1: Any, padding: float = 0.0) -> bool:
    """
    True when segment ``p0->p1`` crosses the finite segment ``l0->l1``.
    
        ``padding`` optionally extends the access-line segment beyond its endpoints so
        a doorway drawn slightly shorter than the walkable opening still registers.
    """
    ...

# From tailgating_utils
def signed_distance(point: Any, p1: Any, p2: Any) -> float:
    """
    Signed distance from the infinite line through ``p1``/``p2``.
    """
    ...

# From tracking_utils
def analyze_track_movements(results: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Analyze movement patterns of tracked objects.
    
    Args:
        results: Tracking results in frame format
    
    Returns:
        Dict with movement analysis
    """
    ...

# From tracking_utils
def detect_line_crossings(results: Dict[str, List[Dict]], line_points: List[List[float]], track_history: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Detect when tracked objects cross a virtual line.
    
    Args:
        results: Tracking results in frame format
        line_points: Line coordinates [[x1,y1], [x2,y2]]
        track_history: Optional track position history
    
    Returns:
        Dict with crossing information
    """
    ...

# From tracking_utils
def filter_tracks_by_duration(results: Dict[str, List[Dict]], min_duration: int = 5) -> Dict[str, List[Dict]]:
    """
    Filter tracking results to only include tracks that appear for minimum duration.
    
    Args:
        results: Tracking results in frame format
        min_duration: Minimum number of frames a track must appear
    
    Returns:
        Filtered tracking results
    """
    ...

# From tracking_utils
def track_objects_in_zone(results: Any, zone_polygon: List[List[float]]) -> Dict[str, Any]:
    """
    Track objects within a defined zone.
    
    Args:
        results: Detection or tracking results
        zone_polygon: Zone polygon coordinates [[x1,y1], [x2,y2], ...]
    
    Returns:
        Dict with zone tracking information
    """
    ...

# From visualization_utils
def bbox_dict_to_xyxy(bb: Dict[str, Any]) -> Optional[Tuple[int, int, int, int]]:
    """
    Supports:
      - {"xmin","ymin","xmax","ymax"}
      - {"x1","y1","x2","y2"}
    Returns:
      (x1, y1, x2, y2) ints, or None if invalid.
    """
    ...

# From visualization_utils
def clamp_xyxy(x1: int, y1: int, x2: int, y2: int, w: int, h: int) -> Tuple[int, int, int, int]:
    """
    Clamp + sanitize bbox coords into frame bounds.
    
    Ensures:
      - 0 <= x < w
      - 0 <= y < h
      - x1 <= x2
      - y1 <= y2
    """
    ...

# From visualization_utils
def draw_box(frame: Any.Any, xyxy: Tuple[int, int, int, int], color: Tuple[int, int, int]) -> None: ...

# From visualization_utils
def draw_text(frame: Any.Any, text: str, x: int, y: int, scale: float = 0.6) -> None: ...

# From weapon_human_filter
def apply_weapon_human_filter(data: Any) -> List[Dict[str, Any]]:
    """
    Normalize input to a flat frame list and apply the filter.
    """
    ...

# From weapon_human_filter
def apply_weapon_human_frame_filter(detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Return ``kept_weapons + humans + other`` for one frame.
    """
    ...

# From weapon_human_filter
def filter_weapons_by_nearest_human_area_ratio(weapon_detections: List[Dict[str, Any]], person_detections: List[Dict[str, Any]], max_weapon_to_human_area_ratio: float = 0.4) -> List[Dict[str, Any]]:
    """
    Filter for ``best (2).pt`` — weapons are kept when the frame has no humans.
    When humans are present, a weapon must contact a human and pass the area rule.
    """
    ...

# From weapon_human_filter
def split_weapon_human_and_other(detections: Any[Dict[str, Any]], weapon_categories: Set[str], human_categories: Set[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]: ...

# From weapon_human_filter
def weapon_contacts_human(weapon_xyxy: Tuple[int, int, int, int], human_xyxy: Tuple[int, int, int, int]) -> bool:
    """
    Overlap, edge contact, or weapon bbox center inside the human bbox.
    """
    ...

# From weapon_person_fusion_v1
def apply_weapon_person_fusion_v1(detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Full V1 path: split → knife-priority fusion → person association.
    
    Intended for tests and for calling from services without the full use case.
    """
    ...

# From weapon_person_fusion_v1
def coerce_frame_detections(data: Any) -> List[Dict[str, Any]]:
    """
    Normalize pipeline input to a flat list of detection dicts for one frame.
    
    Supported shapes:
    - list[dict]: detections for the current frame
    - dict with keys ``person_detections`` / ``weapon_detections`` (lists merged)
    - dict with ``detections`` list
    - dict[str|int, list] tracking-style single frame (first value used if only one key)
    """
    ...

# From weapon_person_fusion_v1
def filter_weapons_by_person_proximity(weapon_detections: List[Dict[str, Any]], person_detections: List[Dict[str, Any]], max_weapon_to_person_area_ratio: float = 0.5) -> List[Dict[str, Any]]:
    """
    Keep weapons that overlap / touch a person and are smaller than ``ratio`` × person area.
    """
    ...

# From weapon_person_fusion_v1
def fuse_knife_preferred_weapon_detections(weapon_detections: List[Dict[str, Any]], knife_priority_categories: Set[str]) -> List[Dict[str, Any]]:
    """
    If any knife-priority class is present, keep only those; otherwise keep all weapons.
    
    Mirrors: ``if len(knife_boxes) > 0: final = knife_boxes else: final = general``.
    """
    ...

# From weapon_person_fusion_v1
def iou_positive_or_centroid_inside(weapon_xyxy: Tuple[int, int, int, int], person_xyxy: Tuple[int, int, int, int]) -> bool:
    """
    IoU > 0 or weapon bbox center (integer midpoints) lies inside person xyxy.
    """
    ...

# From weapon_person_fusion_v1
def split_person_and_weapons(detections: Any[Dict[str, Any]], person_categories: Set[str], weapon_categories: Set[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Split a flat detection list using lowercase category names.
    """
    ...

# Classes
# From advanced_counting_utils
class CountingLibrary:
    # Library class for handling object counting operations with time-based tracking.

    def __init__(self: Any, time_window_seconds: int = 3600, track_expiry_seconds: int = 300, enable_time_based_counting: bool = True, enable_bbox_deduplication: bool = True, bbox_similarity_threshold: float = 0.8) -> None:
        """
        Initialize counting library with configuration.
        """
        ...

    def count_in_zones(self: Any, results: Dict, zones: Dict[str, List[Tuple[float, float]]] = None, current_timestamp: Optional[float] = None) -> Dict:
        """
        Count objects in defined zones with configurable rules and time-based tracking.
        """
        ...

    def count_objects(self: Any, results: Any, identification_keys: List[str] = None, current_timestamp: Optional[float] = None) -> Tuple[Any, Dict]:
        """
        Count objects with metadata, supporting incremental time-based counting.
        """
        ...

    def get_counting_statistics(self: Any, current_timestamp: Optional[float] = None) -> Dict[str, Any]:
        """
        Get comprehensive counting statistics.
        """
        ...

    def get_unique_count_by_keys(self: Any, results: Any, keys: List[str] = None) -> Dict[str, int]:
        """
        Get unique count based on specified keys.
        """
        ...

    def reset_counters(self: Any, reset_zones: bool = True, reset_time_tracking: bool = True) -> Any:
        """
        Reset counting state.
        """
        ...

    def set_time_window(self: Any, time_window_seconds: int) -> Any:
        """
        Set the time window for statistics collection.
        """
        ...


# From agnostic_nms
class AgnosticNMS:
    # Production-grade NMS implementation with YOLO-matching behavior.
    #
    # Features:
    # - Class-specific and class-agnostic modes
    # - Vectorized (PyTorch) and iterative fallback
    # - Numerical stability enhancements
    # - Box validation and filtering
    # - Schema preservation
    # - Zero side effects
    # - Supports both x1/y1/x2/y2 and xmin/ymin/xmax/ymax bbox formats
    #
    # Attributes:
    #     iou_threshold: IoU threshold for suppression (default: 0.45)
    #     min_box_size: Minimum box width/height in pixels (default: 2.0)
    #     use_vectorized: Use torchvision.ops.nms if available (default: True)
    #     eps: Epsilon for numerical stability (default: 1e-7)

    def __init__(self: Any, iou_threshold: float = 0.45, min_box_size: float = 2.0, use_vectorized: bool = True, eps: float = 1e-07) -> None:
        """
        Initialize NMS module.
        
        Args:
            iou_threshold: IoU threshold for suppression (0.0 to 1.0)
            min_box_size: Minimum box dimension in pixels
            use_vectorized: Use PyTorch implementation if available
            eps: Epsilon for numerical stability in IoU computation
        """
        ...

    def apply(self: Any, detections: List[Dict[str, Any]], class_agnostic: bool = True, target_categories: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Apply NMS to detections.
        
        Args:
            detections: List of detection dicts with schema:
                {
                    "category": str,
                    "confidence": float,
                    "bounding_box": {"x1": float, "y1": float, "x2": float, "y2": float}
                                 or {"xmin": float, "ymin": float, "xmax": float, "ymax": float},
                    ... (other fields preserved)
                }
            class_agnostic: If True, suppress across all classes
            target_categories: Optional list of categories to process (others ignored)
        
        Returns:
            Filtered list of detections with identical schema
        """
        ...

    def get_stats(self: Any) -> Dict[str, Any]:
        """
        Get NMS usage statistics.
        
        Returns:
            Dictionary with statistics:
            - total_calls: Number of times apply() was called
            - vectorized_calls: Number of vectorized NMS calls
            - iterative_calls: Number of iterative NMS calls
            - total_input: Total input detections
            - total_output: Total output detections
            - total_suppressed: Total suppressed detections
            - suppression_rate: Percentage of detections suppressed
        """
        ...

    def is_vectorized_available() -> bool:
        """
        Check if vectorized implementation is available.
        """
        ...

    def reset_stats(self: Any) -> Any:
        """
        Reset usage statistics.
        """
        ...


# From alert_instance_utils
class ALERT_INSTANCE:
    # Manages instant alert configurations and evaluates detection events.
    #
    # This class handles:
    # - Polling alert configs from Redis/Kafka every polling_interval seconds
    # - Maintaining in-memory alert state
    # - Evaluating detection events against alert criteria
    # - Publishing trigger messages when matches occur
    #
    # Transport Priority:
    # - Redis is primary for both config reading and trigger publishing
    # - Kafka is fallback when Redis operations fail

    def __init__(self: Any, redis_client: Optional[Any] = None, kafka_client: Optional[Any] = None, config_topic: str = 'alert_instant_config_request', trigger_topic: str = 'alert_instant_triggered', polling_interval: int = 10, logger: Optional[Any.Any] = None, app_deployment_id: Optional[str] = None) -> None:
        """
        Initialize ALERT_INSTANCE.
        
        Args:
            redis_client: MatriceStream instance configured for Redis (primary transport)
            kafka_client: MatriceStream instance configured for Kafka (fallback transport)
            config_topic: Topic/stream name for receiving alert configs
            trigger_topic: Topic/stream name for publishing triggers
            polling_interval: Seconds between config polling
            logger: Python logger instance
            app_deployment_id: App deployment ID to filter incoming alerts (only process alerts matching this ID)
        """
        ...

    def get_active_alerts_count(self: Any) -> int:
        """
        Get count of active alerts.
        """
        ...

    def get_alerts_for_camera(self: Any, camera_id: str) -> List[Dict[str, Any]]:
        """
        Get all active alerts for a camera (for debugging/monitoring).
        """
        ...

    def process_detection_event(self: Any, detection_payload: Dict[str, Any], stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process a detection event and evaluate against active alerts.
        
        Args:
            detection_payload: Detection event data
            stream_info: Stream metadata containing stream_time and other info
        """
        ...

    def start(self: Any) -> Any:
        """
        Start the background polling thread for config updates.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the background polling thread gracefully.
        """
        ...


# From alert_instance_utils
class AlertConfig:
    # Represents an instant alert configuration.

    def from_dict(cls: Any, data: Dict[str, Any]) -> 'Any':
        """
        Create AlertConfig from dictionary.
        """
        ...


# From alerting_utils
class AlertingLibrary:
    # Library class for handling alerting and event triggering.

    def __init__(self: Any) -> None: ...

    def clear_alert_history(self: Any) -> Any:
        """
        Clear alert history.
        """
        ...

    def filter_by_confidence(self: Any, results: Any, threshold: float) -> Any:
        """
        Filter results by confidence threshold.
        """
        ...

    def get_alert_history(self: Any) -> List[Dict]:
        """
        Get history of triggered alerts.
        """
        ...

    def trigger_events(self: Any, results: Any, category_count_threshold: Dict[str, int] = None, category_triggers: List[str] = None) -> List[Dict]:
        """
        Trigger events based on detection conditions.
        """
        ...


# From alerting_utils
class SimpleAlerter:
    # Simple alerter for common use cases.

    def __init__(self: Any) -> None: ...

    def check_dwell_time_alert(self: Any, track_dwell_times: Dict[int, float], max_dwell_time: float) -> Dict:
        """
        Check dwell time alerts.
        """
        ...

    def check_threshold_alert(self: Any, results: Any, threshold: int, category: str = 'all') -> Dict:
        """
        Check if count exceeds threshold.
        """
        ...

    def check_zone_occupancy_alert(self: Any, zone_counts: Dict[str, int], zone_thresholds: Dict[str, int]) -> Dict:
        """
        Check zone occupancy alerts.
        """
        ...


# From business_metrics_manager_utils
class BUSINESS_METRICS_MANAGER:
    # Manages business metrics aggregation and publishing.
    #
    # Key behaviors:
    # - Aggregates business metrics for configurable interval (default 5 minutes)
    # - Publishes aggregated metrics to Redis/Kafka topic
    # - Supports multiple aggregation types (mean, min, max, sum)
    # - Resets all values after publishing
    # - Thread-safe operations
    #
    # Usage:
    #     manager = BUSINESS_METRICS_MANAGER(redis_client=..., kafka_client=...)
    #     manager.start()  # Start aggregation timer
    #     manager.process_metrics(camera_id, metrics_data, stream_info)
    #     manager.stop()   # Stop on shutdown

    def __init__(self: Any, redis_client: Optional[Any] = None, kafka_client: Optional[Any] = None, output_topic: str = 'business_metrics', aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL, metrics_config: Optional[Dict[str, str]] = None, logger: Optional[Any.Any] = None) -> None:
        """
        Initialize BUSINESS_METRICS_MANAGER.
        
        Args:
            redis_client: MatriceStream instance configured for Redis
            kafka_client: MatriceStream instance configured for Kafka
            output_topic: Topic/stream name for publishing metrics
            aggregation_interval: Interval in seconds for aggregation (default 300 = 5 minutes)
            metrics_config: Dict of metric_name -> aggregation_type
            logger: Python logger instance
        """
        ...

    OUTPUT_TOPIC: str

    def force_publish_all(self: Any) -> int:
        """
        Force publish all cameras with pending metrics. Returns count published.
        """
        ...

    def get_all_camera_states(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get all camera states for debugging/monitoring.
        """
        ...

    def get_camera_state(self: Any, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current metrics state for a camera (for debugging).
        """
        ...

    def process_metrics(self: Any, camera_id: str, metrics_data: Dict[str, Any], stream_info: Optional[Dict[str, Any]] = None) -> bool:
        """
        Process business metrics and add to aggregation.
        
        This method:
        1. Extracts camera info from stream_info
        2. Adds each metric value to the appropriate aggregator
        3. Checks if aggregation interval has passed and publishes if so
        
        Args:
            camera_id: Unique camera identifier
            metrics_data: Business metrics dictionary from usecase
            stream_info: Stream metadata
        
        Returns:
            True if metrics were published, False otherwise
        """
        ...

    def reset_camera_state(self: Any, camera_id: str) -> Any:
        """
        Reset metrics state for a specific camera.
        """
        ...

    def set_aggregation_interval(self: Any, interval_seconds: int) -> Any:
        """
        Set the aggregation interval.
        
        Args:
            interval_seconds: New interval in seconds
        """
        ...

    def set_factory_ref(self: Any, factory: 'Any') -> Any:
        """
        Set reference to factory for accessing deployment info.
        """
        ...

    def set_metrics_config(self: Any, metrics_config: Dict[str, str]) -> Any:
        """
        Set aggregation type configuration for metrics.
        
        Args:
            metrics_config: Dict of metric_name -> aggregation_type
        """
        ...

    def start(self: Any) -> Any:
        """
        Start the background timer thread for periodic publishing.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the background timer thread gracefully.
        """
        ...


# From business_metrics_manager_utils
class BusinessMetricsManagerFactory:
    # Factory class for creating BUSINESS_METRICS_MANAGER instances.
    #
    # Handles session initialization and Redis/Kafka client creation
    # following the same pattern as IncidentManagerFactory.

    def __init__(self: Any, logger: Optional[Any.Any] = None) -> None: ...

    ACTION_ID_PATTERN: Any

    def business_metrics_manager(self: Any) -> Optional[Any]: ...

    def initialize(self: Any, config: Any, aggregation_interval: int = DEFAULT_AGGREGATION_INTERVAL, metrics_config: Optional[Dict[str, str]] = None) -> Optional[Any]:
        """
        Initialize and return BUSINESS_METRICS_MANAGER with Redis/Kafka clients.
        
        This follows the same pattern as IncidentManagerFactory for
        session initialization and Redis/Kafka client creation.
        
        Args:
            config: Configuration object with session, server_id, etc.
            aggregation_interval: Interval in seconds for aggregation (default 300)
            metrics_config: Dict of metric_name -> aggregation_type
        
        Returns:
            BUSINESS_METRICS_MANAGER instance or None if initialization failed
        """
        ...

    def is_initialized(self: Any) -> bool: ...


# From business_metrics_manager_utils
class CameraMetricsState:
    # Stores metrics state for a camera.

    def add_metric_value(self: Any, metric_name: str, value: float, agg_type: str = 'mean') -> Any:
        """
        Add a value for a specific metric.
        """
        ...

    def get_aggregated_metrics(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get all aggregated metrics in output format.
        """
        ...

    def has_metrics(self: Any) -> bool:
        """
        Check if any metrics have values.
        """
        ...

    def reset_metrics(self: Any) -> Any:
        """
        Reset all metric aggregators.
        """
        ...


# From business_metrics_manager_utils
class MetricAggregator:
    # Stores aggregated values for a single metric.

    def add_value(self: Any, value: float) -> Any:
        """
        Add a value to the aggregator.
        """
        ...

    def get_aggregated_value(self: Any) -> Optional[float]:
        """
        Get the aggregated value based on aggregation type.
        """
        ...

    def has_values(self: Any) -> bool:
        """
        Check if aggregator has any values.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset the aggregator values.
        """
        ...


# From bytetrack_utils
class ByteTrackArgs:
    ...

# From bytetrack_utils
class ByteTrackWrapper:
    # Wrapper around YOLOX BYTETracker.
    #
    # NOTE:
    # - This is NOT the same as ultralytics ByteTrack
    # - It assigns track_id to detections by IoU matching

    def __init__(self: Any, fps: float = 30.0, track_thresh: float = 0.25, match_thresh: float = 0.8, track_buffer: int = 30) -> None: ...

    def update(self: Any, dets: List[Dict[str, Any]], stream_info: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]: ...


# From bytetrack_utils
class SORTTracker:
    def __init__(self: Any, iou_threshold: float = 0.25, max_age: int = 30, min_hits: int = 2) -> None: ...

    def update(self: Any, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]: ...


# From category_mapping_utils
class CategoryMappingLibrary:
    # Library class for handling category mapping operations.

    def __init__(self: Any, index_to_category: Dict[int, str] = None) -> None: ...

    def map_results(self: Any, results: Any) -> Any:
        """
        Map category indices to category names in results.
        """
        ...


# From color_utils
class VideoColorClassifier:
    # A comprehensive system for processing video frames with model predictions
    # and extracting color information from detected objects.

    def __init__(self: Any, top_k_colors: int = 3, min_confidence: float = 0.5) -> None:
        """
        Initialize the video color classifier.
        
        Args:
            top_k_colors: Number of top colors to extract per detection
            min_confidence: Minimum confidence threshold for detections
        """
        ...

    def process_video_with_predictions(self: Any, video_bytes: Any, predictions: Dict[str, List[Dict]], output_dir: str = './output', fps: Optional[float] = None) -> Tuple[str, str]:
        """
        Main function to process video with model predictions and extract colors.
        
        Args:
            video_bytes: Raw video file bytes
            predictions: Dict with frame_id -> list of detection dicts
            output_dir: Directory to save output files
            fps: Video FPS (will be auto-detected if not provided)
        
        Returns:
            Tuple of (detailed_results_path, summary_results_path)
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset the classifier state.
        """
        ...


# From counting_utils
class ABLineCounter:
    # Manages trap zone [two AB lines] counting: count only on full crossing A -> zone -> B or B -> zone -> A.

    def __init__(self: Any, line_a: Any.Any, line_b: Any.Any, in_direction: str = 'A_to_B', use_foot_center: bool = False) -> None:
        """
        Initialize trap zone counter.
        
        Args:
            line_a: (2, 2) array — rows are segment start and end for Line A
            line_b: (2, 2) array — rows are segment start and end for Line B
            in_direction: "A_to_B" (crossing A then B = In) or "B_to_A" (crossing B then A = In)
            use_foot_center: if True use bottom-center (foot) of bbox for logic; else use bbox center
        """
        ...

    OUTSIDE_SEGMENT_EXTENT: Any

    def get_center(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Get center point of bounding box.
        """
        ...

    def get_counting_point(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Point used for crossing/region logic: foot_center if use_foot_center else bbox center.
        """
        ...

    def get_foot_center(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Get foot (bottom-center) point of bounding box.
        """
        ...

    def get_track_bbox_color(self: Any, track_id: int) -> Tuple[int, int, int]:
        """
        Green = inside (entered, not yet exited). Red = outside or already exited.
        """
        ...

    def is_track_counted(self: Any, track_id: int) -> bool:
        """
        True if track has crossed the entry line (green side).
        """
        ...

    def is_track_inside(self: Any, track_id: int) -> bool:
        """
        True if track has entered and not yet exited: green until they cross the exit line.
        """
        ...

    def update(self: Any, boxes: Any.Any, track_ids: Any.Any) -> int:
        """
        Update counting: only count when a track completes A -> zone -> B or B -> zone -> A.
        Uses get_counting_point (foot or center per config) for region/crossing logic.
        """
        ...


# From counting_utils
class PolygonCounter:
    # Manages double polygon counting logic.

    def __init__(self: Any, inner_polygon: List[Tuple[int, int]], outer_polygon: List[Tuple[int, int]], initial_warmup_frames: int = 5, use_foot_center: bool = True) -> None:
        """
        Initialize polygon counter.
        
        Args:
            inner_polygon: List of (x, y) points defining inner polygon
            outer_polygon: List of (x, y) points defining outer polygon
            initial_warmup_frames: Number of initial frames to count all inside detections (default: 5)
            use_foot_center: if True use bottom-center (foot) of bbox for logic; else use bbox center
        """
        ...

    def get_center(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Get center point of bounding box.
        """
        ...

    def get_counting_point(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Point used for polygon/zone logic: foot_center if use_foot_center else bbox center.
        """
        ...

    def get_foot_center(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Get foot (bottom-center) point of bounding box.
        """
        ...

    def is_point_in_polygon(self: Any, point: Tuple[float, float], polygon: Any.Any) -> bool:
        """
        Check if a point is inside a polygon using ray casting algorithm.
        """
        ...

    def is_track_counted(self: Any, track_id: int) -> bool:
        """
        Check if a track ID is currently counted (has "inside" state).
        
        Args:
            track_id: Track ID to check
        
        Returns:
            True if track is counted, False otherwise
        """
        ...

    def update(self: Any, boxes: Any.Any, track_ids: Any.Any) -> int:
        """
        Update counting based on current detections.
        present_count = actual_inside_count (detections inside inner polygon).
        total_in counts unique entrants only; same track_id out then back in does not increment.
        """
        ...


# From counting_utils
class VectorABLineCounter:
    def __init__(self: Any, line_a: Any, line_b: Any, in_direction: Any = 'A_to_B', use_foot_center: Any = True, padding: Any = 150) -> None: ...

    def update(self: Any, boxes: Any, track_ids: Any) -> Any: ...


# From incident_manager_utils
class INCIDENT_MANAGER:
    # Manages incident severity level tracking and publishing.
    #
    # Key behaviors:
    # - Polls 'incident_modification_config' topic for dynamic threshold settings
    # - Calculates severity_level from incident_quant using thresholds
    # - Publishes incidents ONLY when severity level changes
    # - Requires different consecutive frames based on level:
    #   - 5 frames for medium/significant/critical
    #   - 10 frames for low (stricter to avoid false positives)
    #   - 50 empty frames to send "info" (incident ended)
    # - Supports both Redis and Kafka transports
    # - Thread-safe operations
    #
    # Usage:
    #     manager = INCIDENT_MANAGER(redis_client=..., kafka_client=...)
    #     manager.start()  # Start config polling
    #     manager.process_incident(camera_id, incident_data, stream_info)
    #     manager.stop()   # Stop polling on shutdown

    def __init__(self: Any, redis_client: Optional[Any] = None, kafka_client: Optional[Any] = None, incident_topic: str = 'incident_res', config_topic: str = 'incident_modification_config', logger: Optional[Any.Any] = None) -> None:
        """
        Initialize INCIDENT_MANAGER.
        
        Args:
            redis_client: MatriceStream instance configured for Redis
            kafka_client: MatriceStream instance configured for Kafka
            incident_topic: Topic/stream name for publishing incidents
            config_topic: Topic/stream name for receiving threshold configs
            logger: Python logger instance
        """
        ...

    CONFIG_POLLING_INTERVAL: int
    CONFIG_TOPIC: str
    CONSECUTIVE_FRAMES_DEFAULT: int
    CONSECUTIVE_FRAMES_EMPTY: int
    CONSECUTIVE_FRAMES_LOW: int
    IDLE_CLOSE_SEC: float
    INCIDENT_TOPIC: str

    def get_all_camera_states(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get all camera states for debugging/monitoring.
        """
        ...

    def get_camera_state(self: Any, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current incident state for a camera (for debugging).
        """
        ...

    def get_threshold_config(self: Any, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Get threshold configuration for a camera (for debugging).
        """
        ...

    def process_incident(self: Any, camera_id: str, incident_data: Dict[str, Any], stream_info: Optional[Dict[str, Any]] = None) -> bool:
        """
        Process an incident and publish if severity level changed.
        
        This method:
        1. Gets incident_quant from incident_data
        2. Calculates severity_level using dynamic thresholds for this camera
        3. Updates incident_data with new severity_level
        4. Tracks level changes with consecutive-frame validation:
           - 5 frames for medium/significant/critical
           - 10 frames for low (stricter)
        5. Tracks empty incidents and publishes "info" after 50 consecutive empty frames
        6. Publishes on level change
        7. Manages incident_id per camera per cycle (increments after info is sent)
        
        Args:
            camera_id: Unique camera identifier
            incident_data: Incident dictionary from usecase (must include incident_quant)
            stream_info: Stream metadata
        
        Returns:
            True if incident was published, False otherwise
        """
        ...

    def reset_camera_state(self: Any, camera_id: str) -> Any:
        """
        Reset incident state for a specific camera.
        """
        ...

    def set_factory_ref(self: Any, factory: 'Any') -> Any:
        """
        Set reference to factory for accessing deployment info.
        """
        ...

    def set_thresholds_for_camera(self: Any, camera_id: str, thresholds: List[Dict[str, Any]], application_id: str = '', app_deployment_id: str = '', incident_type: str = '', camera_name: str = '') -> Any:
        """
        Manually set thresholds for a camera (useful for testing or direct config).
        
        Args:
            camera_id: Camera identifier
            thresholds: List of threshold configs
            application_id: Application ID
            app_deployment_id: App deployment ID
            incident_type: Incident type (e.g., "fire")
            camera_name: Camera name
        """
        ...

    def start(self: Any) -> Any:
        """
        Start the background config polling thread.
        """
        ...

    def stop(self: Any) -> Any:
        """
        Stop the background polling thread gracefully.
        """
        ...


# From incident_manager_utils
class IncidentManagerFactory:
    # Factory class for creating INCIDENT_MANAGER instances.
    #
    # Handles session initialization and Redis/Kafka client creation
    # following the same pattern as license_plate_monitoring.py.

    def __init__(self: Any, logger: Optional[Any.Any] = None) -> None: ...

    ACTION_ID_PATTERN: Any

    def incident_manager(self: Any) -> Optional[Any]: ...

    def initialize(self: Any, config: Any) -> Optional[Any]:
        """
        Initialize and return INCIDENT_MANAGER with Redis/Kafka clients.
        
        Args:
            config: Configuration object with session, server_id, etc.
        
        Returns:
            INCIDENT_MANAGER instance or None if initialization failed
        """
        ...

    def is_initialized(self: Any) -> bool: ...


# From incident_manager_utils
class IncidentState:
    # Tracks the current incident state for a camera/usecase.

    ...

# From incident_manager_utils
class ThresholdConfig:
    # Stores threshold configuration for a camera.

    ...

# From legacy_analytics_bridge
class LegacyAnalyticsProfile:
    # Per-usecase Redis analytics wiring (incidents + VOLUME results-agg).

    ...

# From legacy_analytics_bridge
class LegacyAnalyticsSession:
    # Per-stream accumulator for 60s ``results-agg`` publishing.

    def ingest_agg_summary(self: Any, agg_summary: Any) -> None: ...

    def maybe_publish_incident(self: Any, incident_data: Dict[str, Any], stream_info: Optional[Dict[str, Any]]) -> bool:
        """
        Publish to ``incident_res`` on severity transition (deduped).
        """
        ...

    def maybe_publish_results_agg(self: Any, stream_info: Optional[Dict[str, Any]]) -> bool:
        """
        Publish ``results-agg`` every ~60s with zone-keyed tracking_stats + metrics.
        """
        ...


# From legacy_analytics_bridge
class VolumeMetricSpec:
    ...

# From location_name_cache
class LocationNameCache:
    # Remember resolved names; let failures expire.
    #
    #     Thread-safe: ``face_recognition`` and the plate sync sender both resolve names off
    #     their own threads while the frame thread is in ``process()``.

    def __init__(self: Any, retry_after: float = RETRY_AFTER_SECONDS) -> None: ...

    def clear(self: Any) -> None:
        """
        Drop everything. For tests and for a session change.
        """
        ...

    def note_failure(self: Any, location_id: str) -> None:
        """
        Start (or restart) the cool-off after a lookup failed.
        """
        ...

    def resolved(self: Any, location_id: str) -> Optional[str]:
        """
        The cached name, or ``None`` when this id has never resolved.
        """
        ...

    def should_fetch(self: Any, location_id: str) -> bool:
        """
        Whether a caller should spend a request on this id now.
        
                ``False`` only while a recent failure is still inside its cool-off. An id that
                has never been tried, or whose last failure has aged out, is always fetchable.
        """
        ...

    def store(self: Any, location_id: str, name: str) -> None:
        """
        Record a resolved name and clear any earlier failure for it.
        """
        ...


# From parking_analytics_tracker
class ParkingAnalyticsTracker:
    # Tracks parking duration and status for vehicles.
    #
    # Determines if vehicles are parked based on movement patterns:
    # - Tracks bbox position over a sliding window (default 60 frames)
    # - Calculates movement as percentage of bbox size
    # - Marks vehicle as parked after threshold duration of stationary behavior

    def __init__(self: Any, parked_threshold_frames: int = 150, movement_threshold_percent: float = 5.0, movement_window_frames: int = 60, fps: float = 30.0) -> None:
        """
        Initialize parking analytics tracker.
        
        Args:
            parked_threshold_frames: Frames vehicle must be stationary to be marked as parked
            movement_threshold_percent: Max movement % of bbox size to be considered stationary
            movement_window_frames: Number of frames to analyze for movement
            fps: Frames per second for time calculations
        """
        ...

    def update(self: Any, detections: List[Dict], current_frame: int, current_timestamp: str) -> Dict[str, Any]:
        """
        Update parking analytics with current frame detections.
        
        Args:
            detections: List of detection dicts with track_id, category, bounding_box
            current_frame: Current frame number
            current_timestamp: Current timestamp string
        
        Returns:
            Analytics summary dict with active_vehicles, parked_vehicles, and summary stats
        """
        ...


# From parking_analytics_tracker
class VehicleParkingState:
    # Per-vehicle parking state tracking

    def dwell_time_frames(self: Any) -> int:
        """
        Total frames vehicle has been tracked
        """
        ...

    def parked_time_frames(self: Any) -> int:
        """
        Total frames vehicle has been parked
        """
        ...


# From post_processing_config_client
class PostProcessingConfigClient:
    # Wrapper for Matrice post-processing config: session, stream identifiers,
    # REST fetch by app deployment, and config filtering by camera_id.

    def __init__(self: Any, session: Optional[Any] = None, access_key: Optional[str] = None, secret_key: Optional[str] = None, account_number: Optional[str] = None, logger: Optional[Any.Any] = None) -> None: ...

    def denormalize_config(self: Any, config: Union[Dict[str, Any], List[Dict[str, Any]]], width: int, height: int) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Convert normalized (0–1) line/zone coordinates to integer pixel coordinates.
        """
        ...

    def fetch_location_name(self: Any, location_id: str) -> str:
        """
        Resolve a human-readable location name from a location ObjectId.
        """
        ...

    def filter_configs_by_camera_id(self: Any, configs: List[Dict[str, Any]], camera_id: str) -> List[Dict[str, Any]]:
        """
        Filter config documents to those containing config for the given camera_id.
        """
        ...

    def get_camera_metadata(self: Any, camera_id: str) -> Dict[str, str]:
        """
        Look up human-readable camera fields by id via CameraManagement API.
        """
        ...

    def get_config_for_camera(self: Any, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Return cached post-processing config for a camera.
        """
        ...

    def get_post_processing_configs_by_app_deployment(self: Any, app_deployment_id: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """
        Fetch all post-processing configs for an app deployment via Matrice API.
        """
        ...

    def get_resolution(self: Any, camera_id: str) -> Tuple[Optional[int], Optional[int]]:
        """
        Get frame width and height for a camera by its ID.
        """
        ...

    def get_stream_identifiers(self: Any, stream_info: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Return camera_id, application_id, and app_deployment_id from stream_info.
        """
        ...

    def session(self: Any) -> Any:
        """
        Return the matrice_common Session (read-only).
        """
        ...

    def set_config_cache_from_api(self: Any, configs: List[Dict[str, Any]]) -> None:
        """
        Populate the config cache from a list of configs (e.g. from REST API).
        """
        ...


# From smoothing_utils
class BBoxSmoothingConfig:
    # Configuration for bbox smoothing algorithms.

    ...

# From smoothing_utils
class BBoxSmoothingTracker:
    # Tracks individual objects for smoothing across frames.

    def __init__(self: Any, config: Any) -> None: ...

    def get_stats(self: Any) -> Dict[str, Any]:
        """
        Get tracker statistics.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset tracker state.
        """
        ...


# From tailgating_utils
class AccessEvent:
    # One authorization window for a single (access_line, direction) pair.

    ...

# From tailgating_utils
class AccessEventManager:
    # Manages access-window lifecycle only. No geometry. No analytics.

    def add_crossing(self: Any, event: Any, crossing: Any) -> None: ...

    def can_open(self: Any, state: Any, now_ts: float) -> bool: ...

    def close_event(self: Any, state: Any, cooldown_sec: float, now_ts: float) -> Optional[Any]: ...

    def open_event(self: Any, state: Any, access_window_sec: float, now_ts: float) -> Any: ...

    def should_close(self: Any, event: Any, _state: Any, now_ts: float, silence_timeout_sec: float) -> bool: ...


# From tailgating_utils
class AccessPointState:
    # Per (access_line, direction) lifecycle state. No geometry, no analytics.
    #
    #     Replaces the old per-door ``DoorRuntime``: geometry is now shared (two zones)
    #     and the access-event state machine is keyed by access line *and* crossing
    #     direction, so opposite-direction passages never interfere.

    def __init__(self: Any, access_line_id: str, direction: str) -> None: ...


# From tailgating_utils
class CrossingRecord:
    ...

# From tailgating_utils
class PassageAnalysisResult:
    ...

# From wrong_way_tracker
class AutoReferenceState:
    # State for auto-reference direction estimation.

    ...

# From wrong_way_tracker
class ReferenceSource:
    # Source of reference direction.

    AUTO: str
    NONE: str
    USER_ZONE: str


# From wrong_way_tracker
class ReferenceStatus:
    # Status of reference direction estimation.

    CONFIRMED: str
    LEARNING: str
    NONE: str


# From wrong_way_tracker
class TrackMotionState:
    # Per-track motion state for trajectory-based detection.

    ...

# From wrong_way_tracker
class WrongWayDetectionTracker:
    # Trajectory-based wrong-way vehicle detection tracker.
    #
    # Uses EWMA velocity smoothing and continuous confidence accumulation
    # to detect vehicles moving against the expected traffic direction.
    #
    # Reference Direction Sources (in priority order):
    # 1. User-defined zone_config (first point → last point)
    # 2. Auto-estimation from observed traffic flow
    #
    # Auto-Reference Re-Learning:
    # - For AUTO sources, reference is periodically re-learned to adapt to
    #   changing traffic patterns (e.g., time-of-day flow changes)
    # - Re-learning interval configurable via auto_ref_relearn_interval_frames
    # - User-defined zones (USER_ZONE) are never re-learned

    def __init__(self: Any, alpha: float = 0.2, v_min: float = 1.2, beta: float = 0.1, gamma: float = 0.018, c_suspect: float = 0.25, c_confirm: float = 0.65, c_decay_from_wrong: float = 0.3, correct_direction_frames_to_decay: int = 20, min_confirm_frames: int = 12, stale_track_frames: int = 40, auto_ref_relearn_interval_frames: int = 108000, auto_ref_min_tracks: int = 5, auto_ref_warmup_frames: int = 90, auto_ref_alpha: float = 0.05, auto_ref_confirm_threshold: float = 0.7, auto_ref_stability_frames: int = 60) -> None: ...

    def get_reference_info(self: Any) -> Dict[str, Any]:
        """
        Get current reference direction information including re-learn status.
        """
        ...

    def get_stats(self: Any) -> Dict[str, Any]: ...

    def reset(self: Any) -> None: ...

    def set_reference_from_zone(self: Any, zone_polygon: List[List[float]]) -> bool: ...

    def update(self: Any, detections: List[Dict[str, Any]], current_frame: int) -> Dict[str, Any]: ...


# From wrong_way_tracker
class WrongWayState:
    # State machine states for wrong-way detection.

    NORMAL: str
    SUSPECT: str
    WRONG_WAY: str


from . import advanced_counting_utils, advanced_helper_utils, agnostic_nms, alert_instance_utils, alerting_utils, business_metrics_manager_utils, bytetrack_utils, category_mapping_utils, color_utils, counting_utils, filter_utils, format_utils, geometry_utils, incident_manager_utils, incident_res_format, legacy_analytics_bridge, location_name_cache, parking_analytics_tracker, post_processing_config_client, public_ip, smoothing_utils, stream_time_utils, tailgating_utils, tracking_utils, visualization_utils, weapon_human_filter, weapon_person_fusion_v1, wrong_way_tracker