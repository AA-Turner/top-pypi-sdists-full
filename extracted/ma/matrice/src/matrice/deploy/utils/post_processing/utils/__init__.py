"""
Utility functions for post-processing operations.

This module provides organized utility functions for common post-processing tasks
like geometry calculations, format conversions, counting, tracking, and filtering.
"""

from .geometry_utils import (
    point_in_polygon,
    get_bbox_center,
    calculate_distance,
    calculate_bbox_overlap,
    calculate_iou,
    get_bbox_area,
    normalize_bbox,
    denormalize_bbox,
    line_segments_intersect
)

from .format_utils import (
    convert_to_coco_format,
    convert_to_yolo_format,
    convert_to_tracking_format,
    convert_detection_to_tracking_format,
    convert_tracking_to_detection_format,
    match_results_structure
)

from .filter_utils import (
    filter_by_confidence,
    filter_by_categories,
    calculate_bbox_fingerprint,
    clean_expired_tracks,
    remove_duplicate_detections,
    apply_category_mapping,
    filter_by_area
)

from .counting_utils import (
    count_objects_by_category,
    count_objects_in_zones,
    count_unique_tracks,
    calculate_counting_summary
)

from .tracking_utils import (
    track_objects_in_zone,
    detect_line_crossings,
    analyze_track_movements,
    filter_tracks_by_duration
)

from .smoothing_utils import (
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    create_bbox_smoothing_tracker,
    create_default_smoothing_config
)

from .color_utils import (
    extract_major_colors
)

# Configuration utilities for easy setup
from ..core.config_utils import (
    create_people_counting_config,
    create_intrusion_detection_config,
    create_proximity_detection_config,
    create_customer_service_config,
    create_advanced_customer_service_config,
    create_basic_counting_tracking_config,
    create_zone_from_bbox,
    create_polygon_zone,
    create_config_from_template,
    validate_zone_polygon,
    get_use_case_examples,
    create_retail_store_zones,
    create_office_zones
)

__all__ = [
    # Geometry utilities
    'point_in_polygon',
    'get_bbox_center', 
    'calculate_distance',
    'calculate_bbox_overlap',
    'calculate_iou',
    'get_bbox_area',
    'normalize_bbox',
    'denormalize_bbox',
    'line_segments_intersect',
    
    # Format utilities
    'convert_to_coco_format',
    'convert_to_yolo_format', 
    'convert_to_tracking_format',
    'convert_detection_to_tracking_format',
    'convert_tracking_to_detection_format',
    'match_results_structure',
    
    # Filter utilities
    'filter_by_confidence',
    'filter_by_categories',
    'calculate_bbox_fingerprint',
    'clean_expired_tracks',
    'remove_duplicate_detections',
    'apply_category_mapping',
    'filter_by_area',
    
    # Counting utilities
    'count_objects_by_category',
    'count_objects_in_zones',
    'count_unique_tracks',
    'calculate_counting_summary',
    
    # Tracking utilities
    'track_objects_in_zone',
    'detect_line_crossings',
    'analyze_track_movements',
    'filter_tracks_by_duration',
    
    # Smoothing utilities
    'bbox_smoothing',
    'BBoxSmoothingConfig',
    'BBoxSmoothingTracker',
    'create_bbox_smoothing_tracker',
    'create_default_smoothing_config',
    
    # Color utilities
    'extract_major_colors',
    'rgb_to_lab',
    'lab_distance',
    'find_nearest_color',
    
    # Configuration utilities
    'create_people_counting_config',
    'create_customer_service_config',
    'create_intrusion_detection_config',
    'create_proximity_detection_config', 
    'create_advanced_customer_service_config',
    'create_basic_counting_tracking_config',
    'create_zone_from_bbox',
    'create_polygon_zone',
    'create_config_from_template',
    'validate_zone_polygon',
    'get_use_case_examples',
    'create_retail_store_zones',
    'create_office_zones'
] 