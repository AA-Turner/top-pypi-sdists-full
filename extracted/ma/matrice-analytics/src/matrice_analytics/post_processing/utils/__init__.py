"""
Utility functions for post-processing operations.

This module provides organized utility functions for common post-processing tasks
like geometry calculations, format conversions, counting, tracking, and filtering.
"""

from .agnostic_nms import AgnosticNMS
from .bytetrack_utils import (
    ByteTrackArgs,
    ByteTrackWrapper,
    SORTTracker,
    bbox_centroid,
    bbox_feet_point,
    bbox_iou,
    bbox_to_xyxy,
    dist,
    iou_xyxy,
    make_runtime_bytetrack_config,
    matrice_dets_to_xyxy_score,
    smooth_point,
    ultralytics_track_to_matrice_dets,
    validate_bytetrack_cfg,
)
from .counting_utils import (
    calculate_counting_summary,
    count_objects_by_category,
    count_objects_in_zones,
    count_unique_tracks,
)
from .filter_utils import (
    apply_category_mapping,
    calculate_bbox_fingerprint,
    clean_expired_tracks,
    filter_by_area,
    filter_by_categories,
    filter_by_confidence,
    remove_duplicate_detections,
)
from .format_utils import (
    convert_detection_to_tracking_format,
    convert_to_coco_format,
    convert_to_tracking_format,
    convert_to_yolo_format,
    convert_tracking_to_detection_format,
    match_results_structure,
)
from .geometry_utils import (
    calculate_bbox_overlap,
    calculate_distance,
    calculate_iou,
    denormalize_bbox,
    get_bbox_area,
    get_bbox_bottom25_center,
    get_bbox_bottom_center,
    get_bbox_center,
    line_segments_intersect,
    normalize_bbox,
    point_in_polygon,
)
from .smoothing_utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    bbox_smoothing,
    create_bbox_smoothing_tracker,
    create_default_smoothing_config,
)
from .tracking_utils import (
    analyze_track_movements,
    detect_line_crossings,
    filter_tracks_by_duration,
    track_objects_in_zone,
)

try:
    from .visualization_utils import bbox_dict_to_xyxy, clamp_xyxy, draw_box, draw_text
except ImportError:
    draw_text = draw_box = clamp_xyxy = bbox_dict_to_xyxy = None

# from .color_utils import (
#     extract_major_colors
# )
# Configuration utilities for easy setup
from ..core.config_utils import (
    create_advanced_customer_service_config,
    create_basic_counting_tracking_config,
    create_config_from_template,
    create_customer_service_config,
    create_intrusion_detection_config,
    create_office_zones,
    create_people_counting_config,
    create_polygon_zone,
    create_proximity_detection_config,
    create_retail_store_zones,
    create_zone_from_bbox,
    get_use_case_examples,
    validate_zone_polygon,
)
from .parking_analytics_tracker import ParkingAnalyticsTracker
from .tailgating_utils import (
    AccessEvent,
    AccessEventManager,
    AccessPointState,
    # Tailgating utilities
    CrossingRecord,
    PassageAnalysisResult,
    analyze_passage,
    build_side_zone_map,
    detect_crossing,
    motion_vector,
    normalize,
    polygon_centroid,
    segment_intersects_line,
    signed_distance,
)
from .wrong_way_tracker import WrongWayDetectionTracker

__all__ = [
    # Geometry utilities
    "point_in_polygon",
    "get_bbox_center",
    "calculate_distance",
    "calculate_bbox_overlap",
    "calculate_iou",
    "get_bbox_area",
    "normalize_bbox",
    "denormalize_bbox",
    "line_segments_intersect",
    "get_bbox_bottom25_center",
    "get_bbox_bottom_center",
    # Format utilities
    "convert_to_coco_format",
    "convert_to_yolo_format",
    "convert_to_tracking_format",
    "convert_detection_to_tracking_format",
    "convert_tracking_to_detection_format",
    "match_results_structure",
    # Filter utilities
    "filter_by_confidence",
    "filter_by_categories",
    "calculate_bbox_fingerprint",
    "clean_expired_tracks",
    "remove_duplicate_detections",
    "apply_category_mapping",
    "filter_by_area",
    "AgnosticNMS",
    # Counting utilities
    "count_objects_by_category",
    "count_objects_in_zones",
    "count_unique_tracks",
    "calculate_counting_summary",
    # Tracking utilities
    "track_objects_in_zone",
    "detect_line_crossings",
    "analyze_track_movements",
    "filter_tracks_by_duration",
    # Smoothing utilities
    "bbox_smoothing",
    "BBoxSmoothingConfig",
    "BBoxSmoothingTracker",
    "create_bbox_smoothing_tracker",
    "create_default_smoothing_config",
    # # Color utilities
    # 'extract_major_colors',
    # 'rgb_to_lab',
    # 'lab_distance',
    # 'find_nearest_color',
    # ByteTrack + SORT config/tools
    "validate_bytetrack_cfg",
    "make_runtime_bytetrack_config",
    # ByteTrack bbox helpers
    "bbox_to_xyxy",
    "bbox_centroid",
    "bbox_feet_point",
    "dist",
    "smooth_point",
    "iou_xyxy",
    "bbox_iou",
    # Trackers
    "SORTTracker",
    "matrice_dets_to_xyxy_score",
    "ultralytics_track_to_matrice_dets",
    "ByteTrackArgs",
    "ByteTrackWrapper",
    "ParkingAnalyticsTracker",
    "WrongWayDetectionTracker",
    # Visualization utilities
    "draw_text",
    "draw_box",
    "clamp_xyxy",
    "bbox_dict_to_xyxy",
    # Tailgating utilities
    "CrossingRecord",
    "AccessEvent",
    "AccessPointState",
    "PassageAnalysisResult",
    "AccessEventManager",
    "normalize",
    "motion_vector",
    "signed_distance",
    "polygon_centroid",
    "build_side_zone_map",
    "segment_intersects_line",
    "detect_crossing",
    "analyze_passage",
    # Configuration utilities
    "create_people_counting_config",
    "create_customer_service_config",
    "create_intrusion_detection_config",
    "create_proximity_detection_config",
    "create_advanced_customer_service_config",
    "create_basic_counting_tracking_config",
    "create_zone_from_bbox",
    "create_polygon_zone",
    "create_config_from_template",
    "validate_zone_polygon",
    "get_use_case_examples",
    "create_retail_store_zones",
    "create_office_zones",
]
