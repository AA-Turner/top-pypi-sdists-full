"""Stub file for post_processing.usecases directory."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..advanced_tracker.proxy_tracker import ProxyAdvancedTracker
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult, ResultFormat
from ..core.config import AlertConfig, BaseConfig
from ..core.config import AlertConfig, BaseConfig, LineConfig, ZoneConfig
from ..core.config import AlertConfig, BaseConfig, PeopleCountingConfig
from ..core.config import AlertConfig, BaseConfig, TrackingConfig
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..core.config import AlertConfig, PeopleCountingConfig, ZoneConfig
from ..core.config import BaseConfig
from ..core.config import CarServiceConfig
from ..core.config import CustomerServiceConfig
from ..core.config import IntrusionAdvancedTrackerConfig, IntrusionConfig, ZoneConfig
from ..core.config import LineConfig, PeopleTrackingConfig
from ..core.config import PeopleCountingConfig
from ..core.config import ProximityConfig
from ..ocr.fast_plate_ocr_py38 import LicensePlateRecognizer
from ..ocr.preprocessing import ImagePreprocessor
from ..usecases.color.clip import ClipProcessor
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, calculate_distance, filter_by_confidence, get_bbox_center, match_results_structure, point_in_polygon
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, calculate_iou, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, calculate_iou, count_objects_in_zones, match_results_structure
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, calculate_iou, match_results_structure
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_by_category, filter_by_categories, filter_by_confidence, match_results_structure
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, get_bbox_center, match_results_structure, point_in_polygon
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_categories, filter_by_confidence, match_results_structure
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_confidence, match_results_structure
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, bbox_smoothing, count_objects_by_category, filter_by_confidence, match_results_structure
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, bbox_smoothing, filter_by_confidence, match_results_structure
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, bbox_smoothing, match_results_structure
from ..utils import BBoxSmoothingTracker, ByteTrackWrapper, SORTTracker, apply_category_mapping, bbox_centroid, bbox_feet_point, bbox_iou, dist, filter_by_confidence, match_results_structure, smooth_point
from ..utils import apply_category_mapping
from ..utils import apply_category_mapping, calculate_counting_summary, count_objects_in_zones, count_unique_tracks, filter_by_confidence, match_results_structure
from ..utils import apply_category_mapping, calculate_distance, filter_by_confidence, get_bbox_center, match_results_structure, point_in_polygon
from ..utils import apply_category_mapping, filter_by_categories, filter_by_confidence, match_results_structure
from ..utils import apply_category_mapping, filter_by_confidence
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure, point_in_polygon
from ..utils import apply_category_mapping, filter_by_confidence, point_in_polygon
from ..utils import apply_category_mapping, match_results_structure
from ..utils import filter_by_confidence, get_bbox_bottom25_center, match_results_structure
from ..utils import get_bbox_center, point_in_polygon
from ..utils.agnostic_nms import AgnosticNMS
from ..utils.alert_instance_utils import ALERT_INSTANCE
from ..utils.business_metrics_manager_utils import BUSINESS_METRICS_MANAGER, BusinessMetricsManagerFactory
from ..utils.counting_utils import ABLineCounter, PolygonCounter, parse_line_config, polygon_offset_inward
from ..utils.geometry_utils import get_bbox_bottom25_center, get_bbox_center, point_in_polygon
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.geometry_utils import point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.incident_manager_utils import IncidentManagerFactory
from ..utils.parking_analytics_tracker import ParkingAnalyticsTracker
from ..utils.post_processing_config_client import GEOMETRY_RETRY_INTERVAL, PostProcessingConfigClient
from ..utils.tailgating_utils import AccessEventManager, CrossingRecord, DoorRuntime, analyze_passage, compute_entry_normal, detect_crossing, signed_distance
from ..utils.wrong_way_tracker import WrongWayDetectionTracker
from .color.color_classifier import ColorCache
from .color.color_classifier import ColorClassifier
from .fence_climbing_detection import FenceClimbingDetectionConfig, FenceClimbingDetectionUseCase
from .hazard_zone_entry import PostProcessingConfigClient
from .overcrowding_detection import PostProcessingConfigClient, lift_ai_camera_zones_into_post_processing

# Constants
AVG_AGE: int = ...  # From age_detection
MAX_AGE: int = ...  # From age_detection
MIN_AGE: int = ...  # From age_detection
ort: None = ...  # From age_gender_detection
DEFAULT_CAPACITY: int = ...  # From area_utilization
DEFAULT_WINDOW_SECONDS: int = ...  # From area_utilization
TARGET_CATEGORY: str = ...  # From area_utilization
WARN_MISSING_STREAM_RESOLUTION: str = ...  # From area_utilization
WARN_NO_ZONES: str = ...  # From area_utilization
WARN_ZONE_TOO_BIG: str = ...  # From area_utilization
ColorInfo: Any = ...  # From color_map_utils
PALETTE: Any = ...  # From color_map_utils
PALETTE_RGB: Dict[Any, Any] = ...  # From color_map_utils
LEFT_SHOULDER: int = ...  # From face_covering_detection_pose
RIGHT_SHOULDER: int = ...  # From face_covering_detection_pose
EMOTION_LABELS: List[Any] = ...  # From face_emotion
AVG_AGE: int = ...  # From gender_detection
MAX_AGE: int = ...  # From gender_detection
MIN_AGE: int = ...  # From gender_detection
HAS_MATRICE_SESSION: bool = ...  # From license_plate_monitoring
major_version: Any = ...  # From license_plate_monitoring
minor_version: Any = ...  # From license_plate_monitoring
logger: Any = ...  # From liquid_leak_detection
logger: Any = ...  # From pipe_corrosion_detection
logger: Any = ...  # From pipe_gas_leak_detection
logger: Any = ...  # From tailgating_detection
ColorCache: None = ...  # From vehicle_color_detection
ColorClassifier: None = ...  # From vehicle_color_detection

# Functions
# From advanced_customer_service
def assign_person_by_area(detections: Any, _customer_areas: Any, staff_areas: Any) -> Any:
    """
    Assigns category 'person' detections to 'staff' or 'customer' based on their location in area polygons.
    Modifies the detection list in-place.
    Args:
        detections: List of detection dicts.
        customer_areas: Dict of area_name -> polygon (list of [x, y]).
        staff_areas: Dict of area_name -> polygon (list of [x, y]).
    """
    ...

# From age_gender_detection
def apply_category_mapping(results: Any, index_to_category: Dict[str, str]) -> Any:
    """
    Apply category index to name mapping.
    
    Args:
        results: Detection or tracking results
        index_to_category: Mapping from category index to category name
    
    Returns:
        Results with mapped category names
    """
    ...

# From age_gender_detection
def load_model_from_checkpoint(checkpoint_path: Any, local_path: Any) -> Any:
    """
    Load a model from checkpoint URL
    """
    ...

# From car_service
def assign_person_by_area(detections: Any, _car_areas: Any, staff_areas: Any) -> Any:
    """
    Assigns category detections to 'staff' or 'car' based on their location in area polygons.
    Modifies the detection list in-place.
    Args:
        detections: List of detection dicts.
        car_areas: Dict of area_name -> polygon (list of [x, y]).
        staff_areas: Dict of area_name -> polygon (list of [x, y]).
    """
    ...

# From color_map_utils
def extract_major_colors(image: Any.Any, k: int = 3) -> Any: ...

# From color_map_utils
def find_nearest_color(lab_color: Any.Any) -> Any: ...

# From color_map_utils
def lab_distance(c1: Any.Any, c2: Any.Any) -> float: ...

# From color_map_utils
def rgb_to_lab(rgb: tuple) -> Any.Any: ...

# From customer_service
def assign_person_by_area(detections: Any, customer_areas: Any, staff_areas: Any) -> Any:
    """
    Assigns category 'person' detections to 'staff' or 'customer' based on their location in area polygons.
    Modifies the detection list in-place.
    Args:
        detections: List of detection dicts.
        customer_areas: Dict of area_name -> polygon (list of [x, y]).
        staff_areas: Dict of area_name -> polygon (list of [x, y]).
    """
    ...

# From face_covering_detection_pose
def head_crop_from_pose(frame_shape: Tuple[int, int], box_xyxy: Tuple[float, float, float, float], kps: List[Tuple[float, float, float]]) -> Optional[Tuple[int, int, int, int]]:
    """
    Head crop in pixel coords; logic aligned with extract_faces.py.
    """
    ...

# From fence_climbing_detection_pose
def hands_raised_above_head(detection: Dict[str, Any], kp_conf_thresh: float, margin_px: float, require_both_wrists: bool) -> Tuple[bool, Optional[float], Optional[float]]:
    """
    In image coords (y downward), wrists must sit above facial keypoints:
    
        wrist_y < head_ref_y - margin_px
    
    head_ref_y is the minimum y among visible nose / eyes / ears (highest visible
    facial landmark in frame).
    
    Returns (passed, head_ref_y, best_wrist_y) for telemetry; refs may be None if no pass.
    """
    ...

# From overcrowding_detection
def lift_ai_camera_zones_into_post_processing(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fold AI-style payloads into ``postProcessing`` so denormalization and zone extraction work.
    
        Supported shapes:
    
        1. Standard Matrice document: ``{"postProcessing": {camera_id: {..., "zone_config": {...}}}}``
        2. AI export (camera id as top-level key)::
    
               {"<camera_id>": {"zone_config": {"lines": {}, "zones": {"Polygon 1": [[nx,ny],...], ...}}}}
    
           Polygon / zone labels are kept as the user defined them (e.g. ``Polygon 1``); use the same
           strings in ``count_thresholds`` / ``zone_settings`` when overriding per zone.
    
        Top-level camera blocks are merged into ``postProcessing`` only for camera ids that are not
        already present under ``postProcessing`` (no overwrite).
    """
    ...

# From suspicious_activity_detection
def apply_category_mapping(results: Any, index_to_category: Dict[str, str]) -> Any:
    """
    Apply category index to name mapping.
    
    Args:
        results: Detection or tracking results
        index_to_category: Mapping from category index to category name
    
    Returns:
        Results with mapped category names
    """
    ...

# From suspicious_activity_detection
def load_model_from_checkpoint(checkpoint_path: Any, local_path: Any) -> Any:
    """
    Load a model from checkpoint URL
    """
    ...

# From tailgating_detection
def lift_ai_camera_zones_into_post_processing(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fold AI-style payloads into ``postProcessing`` (same contract as overcrowding).
    
        Matrice UI / exports may place ``zone_config`` under a top-level camera id key;
        this merges those into ``postProcessing`` without overwriting existing keys.
    """
    ...

# Classes
# From Histopathological_Cancer_Detection_img
class HistopathologicalCancerDetectionConfig:
    # Configuration for Histopathological Cancer Detection.

    ...

# From Histopathological_Cancer_Detection_img
class HistopathologicalCancerDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From abandoned_object_detection
class AbandonedObjectConfig:
    # Configuration for abandoned object detection use case.

    ...

# From abandoned_object_detection
class AbandonedObjectDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From advanced_customer_service
class AdvancedCustomerServiceUseCase:
    def __init__(self: Any) -> None:
        """
        Initialize advanced customer service use case.
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_camera_info_from_stream(self: Any, stream_info: Any) -> Any:
        """
        Extract camera_info from stream_info, matching people_counting pattern.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for advanced customer service.
        """
        ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return total unique track counts per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[dict] = None) -> Any:
        """
        Process advanced customer service analytics.
        """
        ...


# From age_detection
class AgeDetectionConfig:
    ...

# From age_detection
class AgeDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From age_detection
class AgeSmoother:
    def __init__(self: Any, window_size: int = 20) -> None: ...

    def prune(self: Any, active_track_ids: set) -> Any: ...

    def update(self: Any, track_id: int, age: int) -> int: ...


# From age_gender_detection
class AgeGenderConfig:
    # Configuration for age and gender detection use case in age and gender detection.

    def validate(self: Any) -> List[str]:
        """
        Validate configuration parameters.
        """
        ...


# From age_gender_detection
class AgeGenderUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique age-gender encountered so far.
        """
        ...

    def helper(self: Any, detections: Any, input_bytes: Any, config: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reset_all_tracking(self: Any) -> None:
        """
        Reset both advanced tracker and plate tracking state.
        """
        ...

    def reset_plate_tracking(self: Any) -> None:
        """
        Reset plate tracking state.
        """
        ...

    def reset_tracker(self: Any) -> None:
        """
        Reset the advanced tracker instance.
        """
        ...


# From animal_detection
class AnimalDetectionConfig:
    # Configuration for animal detection use case.

    ...

# From animal_detection
class AnimalDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From anti_spoofing_detection
class AntiSpoofingDetectionConfig:
    # Configuration for anti-spoofing detection use case.

    ...

# From anti_spoofing_detection
class AntiSpoofingDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Any

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From area_utilization
class AreaUtilizationConfig:
    # Configuration for area utilization use case.
    #
    # This config intentionally mirrors PeopleCountingConfig so that:
    # - client payloads stay consistent
    # - PostProcessor/config_manager behavior remains predictable
    # - we can safely clone people_counting.py behavior
    #
    # Utilization-specific parameters live in:
    #   extra_params = {
    #     "zone_capacities": {"global": 10, "meeting_room": 6},
    #     "window_seconds": 300,
    #   }
    #
    # Per-zone alert headcounts: ``alert_config.occupancy_thresholds`` maps zone name
    # to a *people count*; an alert is raised when that zone's count is **greater than**
    # the value (same sense as ``count_thresholds`` for globals). Occupancy % is only
    # for analytics / display.

    def validate(self: Any) -> List[str]:
        """
        Validate area utilization configuration (PeopleCountingConfig-compatible).
        """
        ...


# From area_utilization
class AreaUtilizationUseCase:
    # Area Utilization = People Counting + Capacity Analytics.
    #
    # Keeps PeopleCounting behavior:
    # - incidents
    # - tracking_stats
    # - alerts (global count + optional per-zone people-count via occupancy_thresholds)
    # - human_text summary
    #
    # Adds:
    # - business_analytics (list per frame) with zone-wise utilization metrics

    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Any) -> None:
        """
        Set client used to resolve zones from deployment/camera post-processing config.
        """
        ...


# From assembly_line_detection
class AssemblyLineConfig:
    # Configuration for assembly line detection use case.

    ...

# From assembly_line_detection
class AssemblyLineUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From banana_defect_detection
class BananaMonitoringConfig:
    # Configuration for banana defect detection use case.

    ...

# From banana_defect_detection
class BananaMonitoringUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From basic_counting_tracking
class BasicCountingTrackingConfig:
    # Configuration for basic counting with tracking.

    def __init__(self: Any, category: str = 'general', usecase: str = 'basic_counting_tracking', confidence_threshold: float = 0.5, target_categories: List[str] = None, zones: Optional[Dict[str, List[List[float]]]] = None, enable_tracking: bool = True, tracking_method: str = 'kalman', max_age: int = 30, min_hits: int = 3, count_thresholds: Optional[Dict[str, int]] = None, zone_thresholds: Optional[Dict[str, int]] = None, alert_cooldown: float = 60.0, enable_unique_counting: bool = True, index_to_category: Optional[Dict[int, str]] = None, **kwargs: Any) -> None:
        """
        Initialize basic counting tracking configuration.
        
        Args:
            category: Use case category
            usecase: Use case name
            confidence_threshold: Minimum confidence for detections
            target_categories: List of categories to count
            zones: Zone definitions for spatial analysis
            enable_tracking: Whether to enable tracking
            tracking_method: Tracking algorithm to use
            max_age: Maximum age for tracks in frames
            min_hits: Minimum hits before confirming track
            count_thresholds: Count thresholds for alerts
            zone_thresholds: Zone occupancy thresholds for alerts
            alert_cooldown: Alert cooldown time in seconds
            enable_unique_counting: Enable unique object counting
            index_to_category: Optional mapping from class indices to category names
            **kwargs: Additional parameters
        """
        ...

    def validate(self: Any) -> List[str]:
        """
        Validate configuration.
        """
        ...


# From basic_counting_tracking
class BasicCountingTrackingUseCase:
    # Basic counting with tracking use case.

    def __init__(self: Any) -> None:
        """
        Initialize basic counting tracking use case.
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for basic counting tracking.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None) -> Any:
        """
        Process basic counting with tracking.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: Basic counting tracking configuration
            context: Processing context
        
        Returns:
            ProcessingResult: Processing result with counting and tracking analytics
        """
        ...

    def validate_config(self: Any, config: Any) -> bool:
        """
        Validate configuration for this use case.
        """
        ...


# From blood_cancer_detection_img
class BloodCancerDetectionConfig:
    # Configuration for BloodCancer detection use case in BloodCancer monitoring.

    ...

# From blood_cancer_detection_img
class BloodCancerDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From bottle_defect_detection
class BottleDefectDetectionConfig:
    def __init__(self: Any, usecase: str = 'bottle_defect_detection', category: str = 'industrial', confidence_threshold: float = 0.4, target_categories: Optional[List[str]] = None, enable_bbox_merge: bool = True, merge_iou_threshold: float = 0.4, containment_threshold: float = 0.7, enable_tracking: bool = True, alert_config: Optional[Any] = None, index_to_category: Optional[Dict[int, str]] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> Any: ...


# From bottle_defect_detection
class BottleDefectDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...


# From burglary_detection
class BurglaryDetectionConfig:
    # Configuration for burglary detection post-processing.

    ...

# From burglary_detection
class BurglaryDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From car_damage_detection
class CarDamageConfig:
    # Configuration for car damage detection use case in car damage monitoring.

    ...

# From car_damage_detection
class CarDamageDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From car_part_segmentation
class CarPartSegmentationConfig:
    # Configuration for car part detection use case in car part monitoring.

    ...

# From car_part_segmentation
class CarPartSegmentationUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From car_service
class CarServiceUseCase:
    def __init__(self: Any) -> None:
        """
        Initialize car service use case.
        """
        ...

    DEFAULT_ALERT_EMAIL: str

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_camera_info_from_stream(self: Any, stream_info: Any) -> Any:
        """
        Extract camera_info from stream_info, matching people_counting pattern.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for car service.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[dict] = None) -> Any:
        """
        Process advanced car service analytics.
        """
        ...


# From cardiomegaly_classification
class CardiomegalyConfig:
    # Configuration for Cardiomegaly Classification detection use case in Cardiomegaly Classification monitoring.

    ...

# From cardiomegaly_classification
class CardiomegalyUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From cell_microscopy_segmentation
class CellMicroscopyConfig:
    # Configuration for Cell segmentation in microscopy images use case for post-processing.

    ...

# From cell_microscopy_segmentation
class CellMicroscopyUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From chicken_pose_detection
class ChickenPoseDetectionConfig:
    # Configuration for Chicken Pose Detection use case.

    ...

# From chicken_pose_detection
class ChickenPoseDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_pose_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reset_all_tracking(self: Any) -> None: ...

    def reset_pose_tracking(self: Any) -> None: ...

    def reset_tracker(self: Any) -> None: ...


# From child_monitoring
class ChildMonitoringConfig:
    # Configuration for child detection use case in child monitoring.

    ...

# From child_monitoring
class ChildMonitoringUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From claude_people_counting_usecase
class ClaudePeopleCountingUsecaseConfig:
    def __init__(self: Any, usecase: str = 'claude_people_counting_usecase', category: str = 'general', confidence_threshold: float = 0.4, target_categories: Optional[List[str]] = None, enable_analytics: bool = True, enable_tracking: bool = True, enable_unique_counting: bool = True, index_to_category: Optional[Dict[int, str]] = None, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> List[str]: ...


# From claude_people_counting_usecase
class ClaudePeopleCountingUsecaseUseCase:
    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> 'Any': ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From color_detection
class ColorDetectionConfig:
    # Configuration for color detection use case.

    def validate(self: Any) -> List[str]: ...


# From color_detection
class ColorDetectionUseCase:
    # Color detection processor for analyzing object colors in video streams with tracking.

    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def color_helper(self: Any, curr_data: Any) -> Any: ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get JSON schema for configuration validation.
        """
        ...

    def get_total_category_counts(self: Any, data: Any) -> Any:
        """
        Return total unique track_id count per category (across all colors).
        """
        ...

    def get_total_color_counts(self: Any) -> Any:
        """
        Return total unique track_id count per color (across all categories).
        """
        ...

    def get_vehicle_stats(self: Any) -> Any:
        """
        Return the current global vehicle statistics as a normal dictionary.
        """
        ...

    def merge_color_summary(self: Any, detections_data: List[Dict[str, Any]], curr_frame_color: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine base detections with current frame color information and produce a color summary.
        Returns structure similar to _calculate_color_summary().
        """
        ...

    def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reset_all_tracking(self: Any) -> None:
        """
        Reset both advanced tracker and color tracking state.
        """
        ...

    def reset_color_tracking(self: Any) -> None:
        """
        Reset color tracking state.
        """
        ...

    def reset_tracker(self: Any) -> None:
        """
        Reset the advanced tracker instance.
        """
        ...

    def update_vehicle_stats(self: Any, frame_detections: dict) -> Any:
        """
        Update global vehicle statistics ensuring uniqueness per track_id and per zone.
        If the same vehicle (track_id) is seen again:
            - Ignore if confidence is lower.
            - Update its color if confidence is higher.
        """
        ...


# From concrete_crack_detection
class ConcreteCrackConfig:
    # Configuration for Concrete Crack detection use case.

    ...

# From concrete_crack_detection
class ConcreteCrackUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From crop_weed_detection
class CropWeedDetectionConfig:
    # Configuration for crop weed detection use case.

    ...

# From crop_weed_detection
class CropWeedDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From crowd_density_heatmaps
class CrowdDensityHeatMapsConfig:
    # Configuration for heatmaps use case.

    ...

# From crowd_density_heatmaps
class CrowdDensityHeatMapsUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From crowdflow
class CrowdflowConfig:
    # Configuration for footfall use case.

    def validate(self: Any) -> List[str]:
        """
        Validate people counting configuration.
        """
        ...


# From crowdflow
class CrowdflowUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From crowdflow
class TrajectoryCorrector:
    # Handles Velocity-Fusion logic to correct model orientation errors.
    # Stores history of track centers and applies EMA smoothing.

    def __init__(self: Any) -> None: ...

    def get_direction_label(self: Any, angle: Any) -> Any:
        """
        Your custom logic for Front/Back/Left/Right
        """
        ...

    def update_and_get_label(self: Any, track_id: Any, center: Any, raw_angle_deg: Any) -> Any:
        """
        1. Fixes Angle (+90)
        2. Calculates Velocity
        3. Applies EMA Smoothing
        4. Returns (Smooth_Angle, Label_String)
        """
        ...


# From customer_service
class CustomerServiceUseCase:
    # Customer service analytics with comprehensive business intelligence.

    def __init__(self: Any) -> None:
        """
        Initialize customer service use case.
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for customer service.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Get total unique counts per category across all processed frames.
        
        Returns:
            Dictionary mapping category to unique count
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Process customer service analytics.
        """
        ...

    def reset_tracking_state(self: Any) -> None:
        """
        Reset all tracking state. Useful for starting a new session.
        """
        ...


# From defect_detection_products
class BottleDefectConfig:
    # Configuration for bottle defect detection use case in bottle defect monitoring.

    ...

# From defect_detection_products
class BottleDefectUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From distracted_driver_detection
class DistractedDriverConfig:
    # Configuration for distracted driver detection use case in distracted driver monitoring.

    ...

# From distracted_driver_detection
class DistractedDriverUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From drone_traffic_monitoring
class DroneTrafficMonitoringUsecase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From drone_traffic_monitoring
class VehiclePeopleDroneMonitoringConfig:
    # Configuration for vehicle detection use case in vehicle monitoring.

    ...

# From drowsy_driver_detection
class DrowsyDriverConfig:
    # Configuration for drowsy driver detection use case.

    ...

# From drowsy_driver_detection
class DrowsyDriverUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From dwell_detection
class DwellConfig:
    # Configuration for dwell detection use case.

    ...

# From dwell_detection
class DwellUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From emergency_vehicle_detection
class EmergencyVehicleConfig:
    ...

# From emergency_vehicle_detection
class EmergencyVehicleUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From face_covering_detection_pose
class FaceCoveringDetectionPoseConfig:
    # Configuration for face covering detection (pose head crop + RetinaFace).

    def validate(self: Any) -> List[str]: ...


# From face_covering_detection_pose
class FaceCoveringDetectionPoseUseCase:
    # Pose-guided head crops + RetinaFace for face covering / occlusion alerts.

    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_count(self: Any) -> int: ...

    def get_total_count(self: Any) -> int: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Any) -> None: ...


# From face_emotion
class FaceEmotionConfig:
    # Configuration for Face Emotion detection use case in Face Emotion monitoring.

    ...

# From face_emotion
class FaceEmotionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From face_recognition
class FaceRecognitionConfig:
    # Configuration for face detection use case.

    ...

# From face_recognition
class FaceRecognitionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From fall_detection
class FallConfirmationConfig:
    # Configuration for fall detection confirmation layer.

    ...

# From fall_detection
class FallConfirmationLayer:
    # Per-track temporal + confidence-weighted fall confirmation.
    #
    # For each tracked person, maintains a rolling window of recent
    # (classification, confidence) observations. A fall detection is
    # confirmed only when:
    #   1. The confidence-weighted fall score >= confirm_threshold
    #   2. At least min_fall_frames in the window are classified as fall
    #
    # This suppresses:
    #   - Flickering FPs (1-3 frame bursts) → score too low
    #   - Low-confidence sustained misclassification → confidence drags score down
    #   - Single high-confidence glitches → blocked by min_fall_frames

    def __init__(self: Any, config: Optional[Any] = None) -> None: ...

    def get_stats(self: Any) -> Dict[str, Any]:
        """
        Return confirmation layer statistics.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset all state. Call when switching streams or restarting.
        """
        ...

    def update(self: Any, detections: List[Dict]) -> List[Dict]:
        """
        Process tracked detections and apply fall confirmation logic.
        
        Args:
            detections: List of detection dicts from the tracker.
                Each must have: 'track_id', 'category', 'confidence', 'bounding_box'
        
        Returns:
            Filtered/modified detections list. Non-fall detections pass through unchanged.
            Fall detections are either confirmed (passed through) or suppressed
            (dropped or reclassified based on config.suppression_mode).
        """
        ...


# From fall_detection
class FallDetectionConfig:
    # Configuration for fall detection in people analytics usecase.

    ...

# From fall_detection
class FallDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From fashion_detection
class FashionDetectionConfig:
    # Configuration for Fashion detection use case in fashion monitoring.

    ...

# From fashion_detection
class FashionDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From fence_climbing_detection
class FenceClimbingDetectionConfig:
    # Configuration for Fence Climbing Detection use case.

    def validate(self: Any) -> List[str]: ...


# From fence_climbing_detection
class FenceClimbingDetectionUseCase:
    # Fence Climbing Detection with zone analysis, per-track state, and incident manager.

    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_count(self: Any) -> int: ...

    def get_total_count(self: Any) -> int: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Any) -> None: ...


# From fence_climbing_detection_pose
class FenceClimbingPoseGatedDetectionConfig:
    # Adds pose gating thresholds on top of `FenceClimbingDetectionConfig`.

    def validate(self: Any) -> List[str]: ...


# From fence_climbing_detection_pose
class FenceClimbingPoseGatedDetectionUseCase:
    # Fence climbing use case requiring raised hands above head from pose keypoints.

    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...


# From fence_climbing_with_zone
class FenceClimbingWithZoneConfig:
    # Configuration for `fence_climbing_with_zone`.
    #
    #     Attributes:
    #         zone_polygon: Polygon vertices in image pixel coordinates as a list
    #             of [x, y] pairs. Format matches `point_in_polygon`. Must have
    #             at least 3 vertices.
    #         confidence_threshold: Minimum YOLO detection score to consider.
    #         target_categories: Keep only detections whose `category` is in this
    #             list (lower-cased). Defaults to ``["person"]``.
    #         index_to_category: Optional class-index -> name map (YOLO classes).
    #         alert_config: Optional alert channel/threshold configuration.

    def validate(self: Any) -> List[str]: ...


# From fence_climbing_with_zone
class FenceClimbingWithZoneUseCase:
    # Per-detection in-zone check.
    #
    #     For each YOLO detection that survives the confidence + category filters,
    #     test whether the bbox's bottom-center sits inside ``config.zone_polygon``.
    #     Every match emits one alert and one incident.

    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From field_mapping
class FieldMappingConfig:
    # Configuration for field mapping detection use case in field mapping monitoring.

    ...

# From field_mapping
class FieldMappingUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From fire_detection
class FireSmokeConfig:
    ...

# From fire_detection
class FireSmokeUseCase:
    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]: ...

    def get_duration_seconds(self: Any, start_time: Any, end_time: Any) -> Any: ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]: ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From fire_detection
class IncidentIdTracker:
    # Tracks severity-level progression across frames to produce monotonically
    # increasing incident/alert IDs. Preserves the original numeric thresholds
    # (7 frames to advance a level; 130 empty frames to close an incident).

    def __init__(self: Any) -> None: ...

    def advance(self: Any, sev_level: str, current_ts: str) -> Tuple[int, int]:
        """
        Feed a severity level ("" if no detection). Returns (rank_id, alert_id).
        """
        ...


# From flare_analysis
class FlareAnalysisConfig:
    # Configuration for flare analysis use case.

    def validate(self: Any) -> List[str]: ...


# From flare_analysis
class FlareAnalysisUseCase:
    # Flare analysis processor for detecting and analyzing flare colors in video streams.

    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reset_all_tracking(self: Any) -> None: ...

    def reset_flare_tracking(self: Any) -> None: ...

    def reset_tracker(self: Any) -> None: ...


# From flower_segmentation
class FlowerConfig:
    # Configuration for Flower detection use case in Flower monitoring.

    ...

# From flower_segmentation
class FlowerUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From footfall
class ByteTrackWrapper:
    # Wraps ultralytics ``BYTETracker`` so it accepts / returns pipeline
    #     detection dicts (``List[Dict]``) instead of raw numpy / Boxes objects.
    #
    #     Follows the same tracking flow as the reference ``people_counter.py``:
    #
    #     1. Convert detection dicts → ``_MockResults`` (mimics ultralytics Boxes).
    #     2. Call ``BYTETracker.update(det, img, feats)`` exactly like the reference.
    #     3. Build **new** detection dicts from the tracker output – tracked
    #        (Kalman-filtered) bounding boxes replace the raw detections, and every
    #        dict carries a ``track_id`` assigned by ByteTrack.
    #
    #     Only *confirmed* tracks are returned; untracked / low-confidence detections
    #     that ByteTrack has not yet promoted to active tracks are dropped (standard
    #     ByteTrack behaviour).

    def __init__(self: Any, track_high_thresh: float = 0.4, track_low_thresh: float = 0.1, new_track_thresh: float = 0.4, track_buffer: int = 60, match_thresh: float = 0.8, fuse_score: bool = True, frame_rate: int = 30) -> None: ...

    def update(self: Any, detections: List[Dict]) -> List[Dict]:
        """
        Run one tracking step.
        
                Parameters
                ----------
                detections : list[dict]
                    Pipeline detection dicts.  Each must contain ``bounding_box``
                    (``{xmin, ymin, xmax, ymax}`` **or** ``{x1, y1, x2, y2}``)
                    and ``confidence``.
        
                Returns
                -------
                list[dict]
                    One dict per **confirmed track** with Kalman-filtered bounding
                    boxes, ``track_id``, ``confidence``, ``category`` and
                    ``category_id``.
        """
        ...


# From footfall
class FootFallConfig:
    # Configuration for Footfall use case (same schema as people tracking).

    def validate(self: Any) -> List[str]:
        """
        Validate people tracking configuration.
        
                Geometry (line_a, line_b, outer_polygon, inner_polygon) may be empty at load time
                when it will be resolved from API via stream_info + config_client in process().
                At use time (_get_or_create_counter), missing geometry raises if not resolved.
        """
        ...


# From footfall
class FootFallUseCase:
    # Footfall use case with polygon/abline counting, zone analysis and alerting (same logic as people tracking).

    def __init__(self: Any) -> None:
        """
        Initialize footfall use case.
        """
        ...

    def clear_current_frame_tracking(self: Any) -> int:
        """
        MANUAL USE ONLY: Clear only current frame tracking data while preserving cumulative totals.
        
         This method is NOT called automatically anywhere in the code.
        
        This is the SAFE method to use for manual clearing of stale/expired current frame data.
        The cumulative total (self._total_count) is always preserved.
        
        In streaming scenarios, you typically don't need to call this at all.
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def clear_expired_tracks(self: Any, max_age_seconds: float = 300.0) -> int: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_all_zone_counts(self: Any) -> Dict[str, Dict[str, int]]: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_count(self: Any) -> int:
        """
        Get the count of people in the current frame.
        """
        ...

    def get_frame_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about frame processing and global frame offset.
        """
        ...

    def get_global_frame_id(self: Any, local_frame_id: str) -> str:
        """
        Convert local frame ID to global frame ID.
        """
        ...

    def get_global_frame_offset(self: Any) -> int:
        """
        Get the current global frame offset.
        """
        ...

    def get_total_count(self: Any) -> int:
        """
        Get the total count of unique people tracked across all calls.
        """
        ...

    def get_total_frames_processed(self: Any) -> int:
        """
        Get the total number of frames processed across all calls.
        """
        ...

    def get_track_ids_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about track IDs.
        """
        ...

    def get_tracking_debug_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed debugging information about tracking state.
        """
        ...

    def get_zone_current_count(self: Any, zone_name: str) -> int: ...

    def get_zone_total_count(self: Any, zone_name: str) -> int: ...

    def get_zone_tracking_info(self: Any) -> Dict[str, Dict[str, Any]]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process a single frame of detections and return agg_summary with in/out counts.
                Args:
                    data: Raw model output (detection or tracking format)
                    config: People counting configuration
                    context: Processing context
                    stream_info: Stream information containing frame details (optional)
        
                Returns:
                    ProcessingResult: Processing result with standardized agg_summary structure
        """
        ...

    def reset_frame_counter(self: Any) -> None: ...

    def reset_tracking_state(self: Any) -> None:
        """
        WARNING: This completely resets ALL tracking data including cumulative totals!
        
        This should ONLY be used when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        
        For clearing expired/stale tracks, use clear_current_frame_tracking() instead.
        """
        ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set the PostProcessingConfigClient used to resolve lines/zones from API (by_app_deployment, camera_id).
        """
        ...

    def set_global_frame_offset(self: Any, offset: int) -> None:
        """
        Set the global frame offset for video chunk processing.
        """
        ...

    def update_global_frame_offset(self: Any, frames_in_chunk: int) -> None:
        """
        Update global frame offset after processing a chunk.
        """
        ...


# From footfall
class PostProcessingConfigClient:
    # Wrapper for Matrice post-processing config: session, stream identifiers,
    # REST fetch by app deployment, and config filtering by camera_id.

    def __init__(self: Any, session: Optional[Any] = None, access_key: Optional[str] = None, secret_key: Optional[str] = None, account_number: Optional[str] = None, logger: Optional[Any.Any] = None) -> None:
        """
        Create client with optional session or credentials (from args or env).
        
                Credentials are loaded in order: constructor args, then env vars
                (MATRICE_ACCESS_KEY_ID, MATRICE_SECRET_ACCESS_KEY, MATRICE_ACCOUNT_NUMBER).
                If session is provided, it is used and credentials are taken from it when needed for RPC.
        
                Parameters
                ----------
                session : object, optional
                    Matrice session (e.g. from matrice_common.session.Session). If None, one is
                    created from access_key/secret_key/account_number (args or env).
                access_key : str, optional
                    Matrice API access key. Default from MATRICE_ACCESS_KEY_ID.
                secret_key : str, optional
                    Matrice API secret key. Default from MATRICE_SECRET_ACCESS_KEY.
                account_number : str, optional
                    Account number. Default from MATRICE_ACCOUNT_NUMBER (default "").
                logger : logging.Logger, optional
                    Logger to use. Defaults to module logger.
        """
        ...

    def denormalize_config(self: Any, config: Union[Dict[str, Any], List[Dict[str, Any]]], width: int, height: int) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Convert normalized (0–1) line/zone coordinates to integer pixel coordinates.
        
                Takes the same structure returned by get_post_processing_configs_by_app_deployment
                (single doc or list of docs) and converts every coordinate in postProcessing
                .<camera_id>.zone_config.lines and .zones to pixels using:
                  pixel_x = round(norm_x * width),  pixel_y = round(norm_y * height).
        
                Parameters
                ----------
                config : dict or list of dict
                    One config document or list of configs (with postProcessing, _id, etc.).
                width : int
                    Frame width in pixels (e.g. from get_resolution).
                height : int
                    Frame height in pixels (e.g. from get_resolution).
        
                Returns
                -------
                dict or list of dict
                    New config(s) with the same structure and integer coordinates.
        """
        ...

    def filter_configs_by_camera_id(self: Any, configs: List[Dict[str, Any]], camera_id: str) -> List[Dict[str, Any]]:
        """
        Filter a list of config documents to those that contain config for the given camera_id.
        
                Each config item has ``postProcessing`` keyed by camera ID; this returns
                only items whose ``postProcessing`` has an entry for `camera_id`.
        
                Parameters
                ----------
                configs : list of dict
                    List of config objects (e.g. from get_post_processing_configs_by_app_deployment).
                camera_id : str
                    Camera ID to filter by.
        
                Returns
                -------
                list of dict
                    Configs that have postProcessing[camera_id].
        """
        ...

    def get_config_for_camera(self: Any, camera_id: str) -> Optional[Dict[str, Any]]:
        """
        Return the current post-processing config for a camera from the cache.
        
                The cache is populated by set_config_cache_from_api (REST load).
        
                Parameters
                ----------
                camera_id : str
                    Camera ID.
        
                Returns
                -------
                dict or None
                    Cached config for this camera, or None if not present.
        """
        ...

    def get_post_processing_configs_by_app_deployment(self: Any, app_deployment_id: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str], Optional[str]]:
        """
        Fetch all post-processing configs for an app deployment via Matrice API.
        
                Uses: GET /v1/inference/post_processing_configs/by_app_deployment/:appDeploymentId
        
                Parameters
                ----------
                app_deployment_id : str
                    Application deployment ID.
        
                Returns
                -------
                tuple of (data, error, message)
                    - data: List of config objects, or None on failure.
                    - error: Error string or None on success.
                    - message: API message string.
        """
        ...

    def get_resolution(self: Any, camera_id: str) -> Tuple[Optional[int], Optional[int]]:
        """
        Get frame width and height for a camera by its ID.
        
                Fetches camera streams via CameraManagement and reads customStreamSettings.
                Return order is (width, height) as requested for use with denormalize_config.
        
                Parameters
                ----------
                camera_id : str
                    Camera ID (as returned by get_stream_identifiers or API).
        
                Returns
                -------
                tuple of (width, height)
                    Pixel dimensions, or (None, None) if not found or on error.
        """
        ...

    def get_stream_identifiers(self: Any, stream_info: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Return camera_id, application_id, and app_deployment_id from stream_info.
        
                application_id and app_deployment_id come from base via self._deployment_id_helper
                (ids = self._deployment_id_helper.extract_deployment_ids(stream_info)).
                camera_id follows face_recognition-style extraction (topic, camera_info, frame_id).
        
                Returns
                -------
                dict
                    Keys: ``camera_id``, ``application_id``, ``app_deployment_id``.
                    Values are strings (empty if not found).
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
        
                For each config doc, each key in postProcessing is treated as a camera_id
                and stored in the cache.
        
                Parameters
                ----------
                configs : list of dict
                    List of config objects from get_post_processing_configs_by_app_deployment.
        """
        ...


# From footfall_bkcp
class FootFallConfig:
    # Configuration for footfall use case.

    def validate(self: Any) -> List[str]:
        """
        Validate people counting configuration.
        """
        ...


# From footfall_bkcp
class FootFallUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From footfall_bkcp
class TrajectoryCorrector:
    # Handles Velocity-Fusion logic to correct model orientation errors.
    # Stores history of track centers and applies EMA smoothing.

    def __init__(self: Any) -> None: ...

    def get_direction_label(self: Any, angle: Any) -> Any:
        """
        Your custom logic for Front/Back/Left/Right
        """
        ...

    def update_and_get_label(self: Any, track_id: Any, center: Any, raw_angle_deg: Any) -> Any:
        """
        1. Fixes Angle (+90)
        2. Calculates Velocity
        3. Applies EMA Smoothing
        4. Returns (Smooth_Angle, Label_String)
        """
        ...


# From gas_leak_detection
class GasLeakDetectionConfig:
    # Configuration for gas leakage detection use case.

    ...

# From gas_leak_detection
class GasLeakDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From gender_detection
class GenderDetectionConfig:
    # Configuration for gender detection use case in gender detection.

    ...

# From gender_detection
class GenderDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From gender_detection
class GenderStabilizer:
    def __init__(self: Any, window_size: int = 10, min_votes: int = 3) -> None: ...

    def prune(self: Any, active_track_ids: set) -> Any:
        """
        Remove stale tracks to prevent memory growth
        """
        ...

    def update(self: Any, track_id: int, gender: str) -> str:
        """
        Returns stabilized gender for this track_id
        Majority vote over PREVIOUS frames (no current-frame bias)
        """
        ...


# From gloves_boots_detection
class GlovesBootsDetectionConfig:
    # Configuration for gloves and boots (safety shoes) detection use case.

    ...

# From gloves_boots_detection
class GlovesBootsDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From hazard_zone_entry
class HazardZoneEntryConfig:
    # Configuration for Hazard Zone Entry use case.

    def validate(self: Any) -> List[str]: ...


# From hazard_zone_entry
class HazardZoneEntryUseCase:
    # hazard zone entry alert use case with zone analysis and alerting.

    def __init__(self: Any) -> None:
        """
        Initialize people counting use case.
        """
        ...

    def clear_current_frame_tracking(self: Any) -> int:
        """
        MANUAL USE ONLY: Clear only current frame tracking data while preserving cumulative totals.
        
         This method is NOT called automatically anywhere in the code.
        
        This is the SAFE method to use for manual clearing of stale/expired current frame data.
        The cumulative total (self._total_count) is always preserved.
        
        In streaming scenarios, you typically don't need to call this at all.
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def clear_expired_tracks(self: Any, max_age_seconds: float = 300.0) -> int:
        """
        MANUAL USE ONLY: Clear current frame tracking data if no updates for a while.
        
          This method is NOT called automatically anywhere in the code.
        It's provided as a utility function for manual cleanup if needed.
        
        In streaming scenarios, you typically don't need to call this at all.
        The cumulative total should keep growing as new unique people are detected.
        
        This method only clears current frame tracking data while preserving
        the cumulative total count. The cumulative total should never decrease.
        
        Args:
            max_age_seconds: Maximum age in seconds before clearing current frame tracks
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_all_zone_counts(self: Any) -> Dict[str, Dict[str, int]]:
        """
        Get current and total counts for all zones.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for people counting.
        """
        ...

    def get_current_frame_count(self: Any) -> int:
        """
        Get the count of people in the current frame.
        """
        ...

    def get_frame_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about frame processing and global frame offset.
        """
        ...

    def get_global_frame_id(self: Any, local_frame_id: str) -> str:
        """
        Convert local frame ID to global frame ID.
        """
        ...

    def get_global_frame_offset(self: Any) -> int:
        """
        Get the current global frame offset.
        """
        ...

    def get_total_count(self: Any) -> int:
        """
        Get the total count of unique people tracked across all calls.
        """
        ...

    def get_total_frames_processed(self: Any) -> int:
        """
        Get the total number of frames processed across all calls.
        """
        ...

    def get_track_ids_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about track IDs.
        """
        ...

    def get_tracking_debug_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed debugging information about tracking state.
        """
        ...

    def get_zone_current_count(self: Any, zone_name: str) -> int:
        """
        Get current count of people in a specific zone.
        """
        ...

    def get_zone_total_count(self: Any, zone_name: str) -> int:
        """
        Get total count of people who have been in a specific zone.
        """
        ...

    def get_zone_tracking_info(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get detailed zone tracking information.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process a single frame of detections and return agg_summary with hazard zone alerts.
        
                Args:
                    data: Raw model output for one frame — either a flat list of detections
                          or a frame-keyed dict (``{"0": [...]}``) from which the first
                          frame's detections are extracted.
                    config: HazardZoneEntryConfig instance.
                    context: Optional processing context.
                    stream_info: Optional stream metadata (used for frame number and API zone resolution).
        
                Returns:
                    ProcessingResult with ``agg_summary`` keyed by the current frame number.
        """
        ...

    def reset_frame_counter(self: Any) -> None:
        """
        Reset only the frame counter.
        """
        ...

    def reset_tracking_state(self: Any) -> None:
        """
        WARNING: This completely resets ALL tracking data including cumulative totals!
        
        This should ONLY be used when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        
        For clearing expired/stale tracks, use clear_current_frame_tracking() instead.
        """
        ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set the PostProcessingConfigClient used to resolve zones from API (by_app_deployment, camera_id).
        """
        ...

    def set_global_frame_offset(self: Any, offset: int) -> None:
        """
        Set the global frame offset for video chunk processing.
        """
        ...

    def update_global_frame_offset(self: Any, frames_in_chunk: int) -> None:
        """
        Update global frame offset after processing a chunk.
        """
        ...


# From heatmaps
class HeatMapsConfig:
    # Configuration for heatmaps use case.

    def validate(self: Any) -> List[str]: ...


# From heatmaps
class HeatMapsUseCase:
    def __init__(self: Any) -> None: ...

    INCIDENT_STILL_ACTIVE: str

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From human_activity_recognition
class HumanActivityConfig:
    # Configuration for human activity detection use case.

    ...

# From human_activity_recognition
class HumanActivityUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From intrusion_detection
class IntrusionUseCase:
    # Intrusion Detection use case with zone analysis, alerting, and incident manager.

    def __init__(self: Any) -> None: ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame.
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of CONFIRMED new track IDs reported for the first time this frame.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set the PostProcessingConfigClient used to resolve zones from API (by_app_deployment, camera_id).
        """
        ...


# From landslide_detection
class LandslideDetectionConfig:
    # Configuration for landslide detection post-processing.

    ...

# From landslide_detection
class LandslideDetectionUseCase:
    # Post-processor for landslide detection model outputs.

    def __init__(self: Any) -> None: ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Return count of all track IDs currently visible in this frame.
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Return count of track IDs that appeared for the first time this frame.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return cumulative unique detection counts per category.
        """
        ...

    def process(self: Any, data: Any = None, config: Any = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run full landslide detection post-processing pipeline.
        
                Args:
                    data: Raw model detections (list or YOLO-style dict).
                    config: Must be a :class:`LandslideDetectionConfig` instance.
                    context: Optional processing context carrying metadata.
                    stream_info: Stream/video metadata used for timestamps.
        
                Returns:
                    :class:`ProcessingResult` containing ``agg_summary`` payload.
        """
        ...


# From leaf
class LeafConfig:
    # Configuration for leaf disease detection use case in leaf disease monitoring.

    ...

# From leaf
class LeafUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From leaf_disease
class LeafDiseaseDetectionConfig:
    # Configuration for leaf disease detection use case in

    ...

# From leaf_disease
class LeafDiseaseDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From leak_detection
class LeakDetectionConfig:
    # Configuration for leakage detection use case.

    ...

# From leak_detection
class LeakDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From license_plate_detection
class LicensePlateConfig:
    # Configuration for License plate detection use case in License plate monitoring.

    ...

# From license_plate_detection
class LicensePlateUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From license_plate_monitoring
class LicensePlateMonitorConfig:
    # Configuration for License plate detection use case in License plate monitoring.
    #
    #     Available OCR models (``ocr_model_name``):
    #
    #     +-----------------------------------------+--------------+---------------------+-----------------------------------+
    #     | Model                                   | Architecture | Training Data       | Best For                          |
    #     +-----------------------------------------+--------------+---------------------+-----------------------------------+
    #     | cct-s-v1-global-model          (default)| CCT (S)      | Global plates       | General use                       |
    #     | cct-xs-v1-global-model                  | CCT (XS)     | Global plates       | Faster / smaller                  |
    #     | cct-s-relu-v1-global-model              | CCT-ReLU (S) | Global plates       | Same as S but with ReLU           |
    #     | cct-xs-relu-v1-global-model             | CCT-ReLU(XS) | Global plates       | Fastest CCT variant               |
    #     | european-plates-mobile-vit-v2-model     | MobileViT-v2 | European plates     | European plates specifically      |
    #     | global-plates-mobile-vit-v2-model       | MobileViT-v2 | Global (65+ countries)| Most comprehensive coverage      |
    #     | argentinian-plates-cnn-model            | CNN          | Argentinian plates  | Argentina only                    |
    #     | argentinian-plates-cnn-synth-model      | CNN          | Argentinian (synth) | Argentina only                    |
    #     +-----------------------------------------+--------------+---------------------+-----------------------------------+

    def validate(self: Any) -> List[str]:
        """
        Validate configuration parameters.
        """
        ...


# From license_plate_monitoring
class LicensePlateMonitorLogger:
    def __init__(self: Any) -> None: ...

    def get_server_connection_info(self: Any) -> Optional[Dict[str, Any]]:
        """
        Fetch server connection info from RPC.
        """
        ...

    def initialize_session(self: Any, config: Any) -> None:
        """
        Initialize session and fetch server connection info if lpr_server_id is provided.
        """
        ...

    async def log_plate(self: Any, plate_text: str, timestamp: str, stream_info: Dict[str, Any], image_data: Optional[str] = None, cooldown: float = 30.0) -> bool:
        """
        Log plate to RPC server with cooldown period.
        
                Args:
                    plate_text: The license plate text
                    timestamp: Capture timestamp
                    stream_info: Stream information dict
                    image_data: Base64-encoded JPEG image of the license plate crop
                    cooldown: Cooldown period in seconds
        """
        ...

    def should_log_plate(self: Any, plate_text: str, cooldown: float) -> bool:
        """
        Check if enough time has passed since last log for this plate.
        """
        ...

    def update_log_timestamp(self: Any, plate_text: str) -> None:
        """
        Update the last log timestamp for a plate.
        """
        ...


# From license_plate_monitoring
class LicensePlateMonitorUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique license plate texts encountered so far.
        """
        ...

    async def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reset_all_tracking(self: Any) -> None:
        """
        Reset both advanced tracker and plate tracking state.
        """
        ...

    def reset_plate_tracking(self: Any) -> None:
        """
        Reset plate tracking state.
        """
        ...

    def reset_tracker(self: Any) -> None:
        """
        Reset the advanced tracker instance.
        """
        ...

    def set_alert_manager(self: Any, alert_manager: Any) -> None:
        """
        Set the alert manager instance for instant alerts.
        
        Args:
            alert_manager: ALERT_INSTANCE instance configured with Redis/Kafka clients
        """
        ...

    def set_bgr_frame(self: Any, bgr_frame: Any) -> Any:
        """
        Set raw BGR frame for OCR analysis (avoids JPEG encode/decode loss).
        """
        ...


# From liquid_leak_detection
class LiquidLeakDetectionConfig:
    # Configuration class for Liquid Leak Detection.
    #
    # Extends BaseConfig and adds:
    # - Spatial merging parameters
    # - Temporal validation parameters
    # - Cooldown control
    # - Analytics toggles

    def __init__(self: Any, usecase: str = 'liquid_leak_detection', category: str = 'industrial', confidence_threshold: float = 0.25, target_categories: Optional[List[str]] = None, enable_analytics: bool = True, enable_spatial_merge: bool = True, iou_merge_threshold: float = 0.5, containment_threshold: float = 0.6, activation_frames: int = 3, deactivation_frames: int = 40, alert_cooldown_seconds: int = 30, index_to_category: Optional[Dict[int, str]] = None, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> List[str]:
        """
        Validates configuration parameters before processing.
        Ensures no invalid thresholds or misconfiguration.
        """
        ...


# From liquid_leak_detection
class LiquidLeakDetectionUseCase:
    # Industrial liquid leak detection usecase.
    #
    # Responsibilities:
    # - Process frame detections
    # - Apply filtering and merging
    # - Maintain temporal state
    # - Generate alerts and incidents
    # - Produce standardized agg_summary output

    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Creates a default configuration instance.
        
        Allows override of any field via kwargs.
        Used for testing and quick experimentation.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Main entry point for processing detection results.
        
        This function:
        - Validates configuration
        - Detects input format
        - Processes each frame independently
        - Builds standardized frame-wise agg_summary
        - Returns ProcessingResult
        """
        ...


# From litter_monitoring
class LitterDetectionConfig:
    # Configuration for litter detection use case in litter monitoring.

    ...

# From litter_monitoring
class LitterDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for litter post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        """
        ...


# From loitering_detection
class LoiteringConfig:
    def validate(self: Any) -> List[str]: ...


# From loitering_detection
class LoiteringUseCase:
    def __init__(self: Any) -> None: ...

    GLOBAL_ZONE_NAME: str

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return total unique track_id counts per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From mask_detection
class MaskDetectionConfig:
    # Configuration for mask detection use case in mask monitoring.

    ...

# From mask_detection
class MaskDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From mask_type_detection
class MaskTypeDetectionConfig:
    # Configuration for mask type detection use case.

    ...

# From mask_type_detection
class MaskTypeDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for mask type detection post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From natural_disaster
class NaturalDisasterConfig:
    # Configuration for PCB Defect Detection use case.

    ...

# From natural_disaster
class NaturalDisasterUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From overcrowding_detection
class OvercrowdingDetectionConfig:
    def validate(self: Any) -> List[str]: ...


# From overcrowding_detection
class OvercrowdingDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set client used to resolve zones from deployment/camera post-processing config.
        """
        ...


# From overcrowding_detection
class PostProcessingConfigClient:
    # Wrapper for Matrice post-processing config: session, stream identifiers,
    # REST fetch by app deployment, and config filtering by camera_id.

    def __init__(self: Any, session: Optional[Any] = None, access_key: Optional[str] = None, secret_key: Optional[str] = None, account_number: Optional[str] = None, logger: Optional[Any.Any] = None) -> None: ...

    def denormalize_config(self: Any, config: Union[Dict[str, Any], List[Dict[str, Any]]], width: int, height: int) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Convert normalized (0–1) line/zone coordinates to integer pixel coordinates.
        """
        ...

    def filter_configs_by_camera_id(self: Any, configs: List[Dict[str, Any]], camera_id: str) -> List[Dict[str, Any]]:
        """
        Filter config documents to those containing config for the given camera_id.
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


# From package_detection
class PackageDetectionConfig:
    # Configuration for package detection use case.

    ...

# From package_detection
class PackageDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of CONFIRMED new track IDs reported for the first time this frame.
        
                A track is only counted as "new" when it has been present in the tracker
                output for at least ``min_hits_for_new_track`` consecutive output frames
                (default 3). Short dropouts are tolerated via a soft-decay counter (a
                one-frame miss reduces the counter by 1 instead of resetting to 0).
                This filters out:
                  - Spurious short-lived detections (noise, reflections, shadows)
                  - Brief ID switches caused by tracker matching failures
                  - Flickering detections near the confidence threshold
        
                Each track ID is reported as new **exactly once** across all frames.
                Subsequent frames will return 0 for that track even though it is still
                visible.  This makes downstream aggregation (summing over N seconds)
                produce the correct total of genuinely new people.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From parking
class ParkingConfig:
    # Configuration for parking space detection use case in parking monitoring.

    ...

# From parking
class ParkingUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From parking_lot_analytics
class ParkingLotAnalyticsConfig:
    # Configuration for vehicle detection use case in parking lot analytics (parking time).

    ...

# From parking_lot_analytics
class ParkingLotAnalyticsUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From parking_space_detection
class ParkingSpaceConfig:
    # Configuration for Parking Space detection use case in Parking Space monitoring.

    ...

# From parking_space_detection
class ParkingSpaceUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any = None, config: Any = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From pcb_defect_detection
class PCBDefectConfig:
    # Configuration for PCB Defect Detection use case.

    ...

# From pcb_defect_detection
class PCBDefectUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From pedestrian_detection
class PedestrianDetectionConfig:
    # Configuration for pedestrian detection use case in pedestrian monitoring.

    ...

# From pedestrian_detection
class PedestrianDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From people_counting
class PeopleCountingUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of CONFIRMED new track IDs reported for the first time this frame.
        
                A track is only counted as "new" when it has been present in the tracker
                output for at least ``min_hits_for_new_track`` consecutive output frames
                (default 3). Short dropouts are tolerated via a soft-decay counter (a
                one-frame miss reduces the counter by 1 instead of resetting to 0).
                This filters out:
                  - Spurious short-lived detections (noise, reflections, shadows)
                  - Brief ID switches caused by tracker matching failures
                  - Flickering detections near the confidence threshold
        
                Each track ID is reported as new **exactly once** across all frames.
                Subsequent frames will return 0 for that track even though it is still
                visible.  This makes downstream aggregation (summing over N seconds)
                produce the correct total of genuinely new people.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From people_counting_bckp
class PeopleCountingUseCase:
    # People counting use case with zone analysis and alerting.

    def __init__(self: Any) -> None:
        """
        Initialize people counting use case.
        """
        ...

    def clear_current_frame_tracking(self: Any) -> int:
        """
        MANUAL USE ONLY: Clear only current frame tracking data while preserving cumulative totals.
        
         This method is NOT called automatically anywhere in the code.
        
        This is the SAFE method to use for manual clearing of stale/expired current frame data.
        The cumulative total (self._total_count) is always preserved.
        
        In streaming scenarios, you typically don't need to call this at all.
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def clear_expired_tracks(self: Any, max_age_seconds: float = 300.0) -> int:
        """
        MANUAL USE ONLY: Clear current frame tracking data if no updates for a while.
        
          This method is NOT called automatically anywhere in the code.
        It's provided as a utility function for manual cleanup if needed.
        
        In streaming scenarios, you typically don't need to call this at all.
        The cumulative total should keep growing as new unique people are detected.
        
        This method only clears current frame tracking data while preserving
        the cumulative total count. The cumulative total should never decrease.
        
        Args:
            max_age_seconds: Maximum age in seconds before clearing current frame tracks
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_all_zone_counts(self: Any) -> Dict[str, Dict[str, int]]:
        """
        Get current and total counts for all zones.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for people counting.
        """
        ...

    def get_current_frame_count(self: Any) -> int:
        """
        Get the count of people in the current frame.
        """
        ...

    def get_frame_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about frame processing and global frame offset.
        """
        ...

    def get_global_frame_id(self: Any, local_frame_id: str) -> str:
        """
        Convert local frame ID to global frame ID.
        """
        ...

    def get_global_frame_offset(self: Any) -> int:
        """
        Get the current global frame offset.
        """
        ...

    def get_total_count(self: Any) -> int:
        """
        Get the total count of unique people tracked across all calls.
        """
        ...

    def get_total_frames_processed(self: Any) -> int:
        """
        Get the total number of frames processed across all calls.
        """
        ...

    def get_track_ids_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about track IDs.
        """
        ...

    def get_tracking_debug_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed debugging information about tracking state.
        """
        ...

    def get_zone_current_count(self: Any, zone_name: str) -> int:
        """
        Get current count of people in a specific zone.
        """
        ...

    def get_zone_total_count(self: Any, zone_name: str) -> int:
        """
        Get total count of people who have been in a specific zone.
        """
        ...

    def get_zone_tracking_info(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get detailed zone tracking information.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Process people counting use case - automatically detects single or multi-frame structure.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: People counting configuration
            context: Processing context
            stream_info: Stream information containing frame details (optional)
        
        Returns:
            ProcessingResult: Processing result with standardized agg_summary structure
        """
        ...

    def reset_frame_counter(self: Any) -> None:
        """
        Reset only the frame counter.
        """
        ...

    def reset_tracking_state(self: Any) -> None:
        """
        WARNING: This completely resets ALL tracking data including cumulative totals!
        
        This should ONLY be used when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        
        For clearing expired/stale tracks, use clear_current_frame_tracking() instead.
        """
        ...

    def set_global_frame_offset(self: Any, offset: int) -> None:
        """
        Set the global frame offset for video chunk processing.
        """
        ...

    def update_global_frame_offset(self: Any, frames_in_chunk: int) -> None:
        """
        Update global frame offset after processing a chunk.
        """
        ...


# From people_counting_in_zone
class ByteTrackWrapper:
    # Wraps ultralytics ``BYTETracker`` so it accepts / returns pipeline
    #     detection dicts (``List[Dict]``) instead of raw numpy / Boxes objects.
    #
    #     Follows the same tracking flow as the reference ``people_counter.py``:
    #
    #     1. Convert detection dicts → ``_MockResults`` (mimics ultralytics Boxes).
    #     2. Call ``BYTETracker.update(det, img, feats)`` exactly like the reference.
    #     3. Build **new** detection dicts from the tracker output – tracked
    #        (Kalman-filtered) bounding boxes replace the raw detections, and every
    #        dict carries a ``track_id`` assigned by ByteTrack.
    #
    #     Only *confirmed* tracks are returned; untracked / low-confidence detections
    #     that ByteTrack has not yet promoted to active tracks are dropped (standard
    #     ByteTrack behaviour).

    def __init__(self: Any, track_high_thresh: float = 0.3, track_low_thresh: float = 0.1, new_track_thresh: float = 0.4, track_buffer: int = 60, match_thresh: float = 0.8, fuse_score: bool = True, frame_rate: int = 30) -> None: ...

    def update(self: Any, detections: List[Dict]) -> List[Dict]:
        """
        Run one tracking step.
        
                Parameters
                ----------
                detections : list[dict]
                    Pipeline detection dicts.  Each must contain ``bounding_box``
                    (``{xmin, ymin, xmax, ymax}`` **or** ``{x1, y1, x2, y2}``)
                    and ``confidence``.
        
                Returns
                -------
                list[dict]
                    One dict per **confirmed track** with Kalman-filtered bounding
                    boxes, ``track_id``, ``confidence``, ``category`` and
                    ``category_id``.
        """
        ...


# From people_counting_in_zone
class PeopleCountingInZoneConfig:
    # Configuration for people counting use case.

    def validate(self: Any) -> List[str]:
        """
        Validate people counting configuration.
        """
        ...


# From people_counting_in_zone
class PeopleCountingInZoneUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared for the FIRST TIME EVER in this frame.
        
                This counts only track IDs that have never been seen before (not in total set).
                Re-entries (person leaves and comes back) are NOT counted as new.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From people_tracking
class PeopleTrackingUseCase:
    # People counting use case with zone analysis and alerting.

    def __init__(self: Any) -> None:
        """
        Initialize people counting use case.
        """
        ...

    def clear_current_frame_tracking(self: Any) -> int:
        """
        MANUAL USE ONLY: Clear only current frame tracking data while preserving cumulative totals.
        
         This method is NOT called automatically anywhere in the code.
        
        This is the SAFE method to use for manual clearing of stale/expired current frame data.
        The cumulative total (self._total_count) is always preserved.
        
        In streaming scenarios, you typically don't need to call this at all.
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def clear_expired_tracks(self: Any, max_age_seconds: float = 300.0) -> int:
        """
        MANUAL USE ONLY: Clear current frame tracking data if no updates for a while.
        
          This method is NOT called automatically anywhere in the code.
        It's provided as a utility function for manual cleanup if needed.
        
        In streaming scenarios, you typically don't need to call this at all.
        The cumulative total should keep growing as new unique people are detected.
        
        This method only clears current frame tracking data while preserving
        the cumulative total count. The cumulative total should never decrease.
        
        Args:
            max_age_seconds: Maximum age in seconds before clearing current frame tracks
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_all_zone_counts(self: Any) -> Dict[str, Dict[str, int]]:
        """
        Get current and total counts for all zones.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for people counting.
        """
        ...

    def get_current_frame_count(self: Any) -> int:
        """
        Get the count of people in the current frame.
        """
        ...

    def get_frame_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about frame processing and global frame offset.
        """
        ...

    def get_global_frame_id(self: Any, local_frame_id: str) -> str:
        """
        Convert local frame ID to global frame ID.
        """
        ...

    def get_global_frame_offset(self: Any) -> int:
        """
        Get the current global frame offset.
        """
        ...

    def get_total_count(self: Any) -> int:
        """
        Get the total count of unique people tracked across all calls.
        """
        ...

    def get_total_frames_processed(self: Any) -> int:
        """
        Get the total number of frames processed across all calls.
        """
        ...

    def get_track_ids_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about track IDs.
        """
        ...

    def get_tracking_debug_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed debugging information about tracking state.
        """
        ...

    def get_zone_current_count(self: Any, zone_name: str) -> int:
        """
        Get current count of people in a specific zone.
        """
        ...

    def get_zone_total_count(self: Any, zone_name: str) -> int:
        """
        Get total count of people who have been in a specific zone.
        """
        ...

    def get_zone_tracking_info(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get detailed zone tracking information.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Process people counting use case - automatically detects single or multi-frame structure.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: People counting configuration
            context: Processing context
            stream_info: Stream information containing frame details (optional)
        
        Returns:
            ProcessingResult: Processing result with standardized agg_summary structure
        """
        ...

    def reset_frame_counter(self: Any) -> None:
        """
        Reset only the frame counter.
        """
        ...

    def reset_tracking_state(self: Any) -> None:
        """
        WARNING: This completely resets ALL tracking data including cumulative totals!
        
        This should ONLY be used when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        
        For clearing expired/stale tracks, use clear_current_frame_tracking() instead.
        """
        ...

    def set_global_frame_offset(self: Any, offset: int) -> None:
        """
        Set the global frame offset for video chunk processing.
        """
        ...

    def update_global_frame_offset(self: Any, frames_in_chunk: int) -> None:
        """
        Update global frame offset after processing a chunk.
        """
        ...


# From people_tracking_bkcp
class PeopleTrackingUseCase:
    # People counting use case with zone analysis and alerting.

    def __init__(self: Any) -> None:
        """
        Initialize people counting use case.
        """
        ...

    def clear_current_frame_tracking(self: Any) -> int:
        """
        MANUAL USE ONLY: Clear only current frame tracking data while preserving cumulative totals.
        
         This method is NOT called automatically anywhere in the code.
        
        This is the SAFE method to use for manual clearing of stale/expired current frame data.
        The cumulative total (self._total_count) is always preserved.
        
        In streaming scenarios, you typically don't need to call this at all.
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def clear_expired_tracks(self: Any, max_age_seconds: float = 300.0) -> int:
        """
        MANUAL USE ONLY: Clear current frame tracking data if no updates for a while.
        
          This method is NOT called automatically anywhere in the code.
        It's provided as a utility function for manual cleanup if needed.
        
        In streaming scenarios, you typically don't need to call this at all.
        The cumulative total should keep growing as new unique people are detected.
        
        This method only clears current frame tracking data while preserving
        the cumulative total count. The cumulative total should never decrease.
        
        Args:
            max_age_seconds: Maximum age in seconds before clearing current frame tracks
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_all_zone_counts(self: Any) -> Dict[str, Dict[str, int]]:
        """
        Get current and total counts for all zones.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for people counting.
        """
        ...

    def get_current_frame_count(self: Any) -> int:
        """
        Get the count of people in the current frame.
        """
        ...

    def get_frame_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about frame processing and global frame offset.
        """
        ...

    def get_global_frame_id(self: Any, local_frame_id: str) -> str:
        """
        Convert local frame ID to global frame ID.
        """
        ...

    def get_global_frame_offset(self: Any) -> int:
        """
        Get the current global frame offset.
        """
        ...

    def get_total_count(self: Any) -> int:
        """
        Get the total count of unique people tracked across all calls.
        """
        ...

    def get_total_frames_processed(self: Any) -> int:
        """
        Get the total number of frames processed across all calls.
        """
        ...

    def get_track_ids_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about track IDs.
        """
        ...

    def get_tracking_debug_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed debugging information about tracking state.
        """
        ...

    def get_zone_current_count(self: Any, zone_name: str) -> int:
        """
        Get current count of people in a specific zone.
        """
        ...

    def get_zone_total_count(self: Any, zone_name: str) -> int:
        """
        Get total count of people who have been in a specific zone.
        """
        ...

    def get_zone_tracking_info(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get detailed zone tracking information.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Process people counting use case - automatically detects single or multi-frame structure.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: People counting configuration
            context: Processing context
            stream_info: Stream information containing frame details (optional)
        
        Returns:
            ProcessingResult: Processing result with standardized agg_summary structure
        """
        ...

    def reset_frame_counter(self: Any) -> None:
        """
        Reset only the frame counter.
        """
        ...

    def reset_tracking_state(self: Any) -> None:
        """
        WARNING: This completely resets ALL tracking data including cumulative totals!
        
        This should ONLY be used when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        
        For clearing expired/stale tracks, use clear_current_frame_tracking() instead.
        """
        ...

    def set_global_frame_offset(self: Any, offset: int) -> None:
        """
        Set the global frame offset for video chunk processing.
        """
        ...

    def update_global_frame_offset(self: Any, frames_in_chunk: int) -> None:
        """
        Update global frame offset after processing a chunk.
        """
        ...


# From phone_screen_defect_detection
class PhoneScreenDefectDetectionConfig:
    def __init__(self: Any, usecase: str = 'phone_screen_defect_detection', category: str = 'industrial', confidence_threshold: float = 0.4, target_categories: Optional[List[str]] = None, enable_bbox_merge: bool = True, merge_iou_threshold: float = 0.4, containment_threshold: float = 0.7, enable_tracking: bool = True, alert_config: Optional[Any] = None, index_to_category: Optional[Dict[int, str]] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> Any: ...


# From phone_screen_defect_detection
class PhoneScreenDefectDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...


# From pipe_corrosion_detection
class PipeCorrosionDetectionConfig:
    # Configuration for Pipe Corrosion Detection Use Case.
    #
    # Includes:
    # - Confidence filtering
    # - Spatial merge thresholds
    # - Temporal validation parameters
    # - Alert cooldown settings

    def __init__(self: Any, usecase: str = 'pipe_corrosion_detection', category: str = 'industrial', confidence_threshold: float = 0.25, target_categories: Optional[List[str]] = None, enable_spatial_merge: bool = True, iou_merge_threshold: float = 0.3, containment_threshold: float = 0.5, activation_frames: int = 10, deactivation_frames: int = 10, alert_cooldown_seconds: int = 30, enable_analytics: bool = True, index_to_category: Optional[Dict[int, str]] = None, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> List[str]: ...


# From pipe_corrosion_detection
class PipeCorrosionDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...

    def reset_state(self: Any) -> Any: ...


# From pipe_gas_leak_detection
class PipeGasLeakDetectionConfig:
    def __init__(self: Any, usecase: str = 'gas_leak_detection', category: str = 'industrial', confidence_threshold: float = 0.25, target_categories: Optional[List[str]] = None, enable_analytics: bool = True, enable_spatial_merge: bool = True, iou_merge_threshold: float = 0.3, containment_threshold: float = 0.5, activation_frames: int = 4, deactivation_frames: int = 30, alert_cooldown_seconds: int = 30, index_to_category: Optional[Dict[int, str]] = None, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> List[str]: ...


# From pipe_gas_leak_detection
class PipeGasLeakDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...


# From pipeline_detection
class PipelineDetectionConfig:
    # Configuration for pipeline detection use case in pipeline monitoring.

    ...

# From pipeline_detection
class PipelineDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From plaque_segmentation_img
class PlaqueSegmentationConfig:
    # Configuration for PlaqueSegmentation detection use case in PlaqueSegmentation monitoring.

    ...

# From plaque_segmentation_img
class PlaqueSegmentationUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From pothole_detection
class PotholeDetectionConfig:
    # Configuration for pothole detection use case in pothole monitoring.

    ...

# From pothole_detection
class PotholeDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From pothole_segmentation
class PotholeConfig:
    # Configuration for pothole detection use case in pothole monitoring.

    ...

# From pothole_segmentation
class PotholeSegmentationUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From ppe_compliance
class PPEComplianceConfig:
    ...

# From ppe_compliance
class PPEComplianceUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_camera_info_from_stream(self: Any, stream_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract camera information from stream_info dict, matching mask_detection's approach.
        """
        ...

    def get_total_violation_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each violation category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for PPE compliance detection post-processing.
        Applies category mapping, violation smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs in the new agg_summary format
        """
        ...

    def reset_all_tracking(self: Any) -> None:
        """
        Reset both advanced tracker and violation tracking state.
        """
        ...

    def reset_tracker(self: Any) -> None:
        """
        Reset the advanced tracker instance.
        
        This should be called when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        """
        ...

    def reset_violation_tracking(self: Any) -> None:
        """
        Reset violation tracking state (total counts, track IDs, etc.).
        
        This should be called when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        """
        ...


# From price_tag_detection
class PriceTagConfig:
    # Configuration for price tag detection use case in price tag monitoring.

    ...

# From price_tag_detection
class PriceTagUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From proximity_detection
class ProximityUseCase:
    # Proximity Detection use case with zone analysis and alerting.

    def __init__(self: Any) -> None:
        """
        Initialize Proximity Detection use case.
        """
        ...

    def clear_current_frame_tracking(self: Any) -> int:
        """
        MANUAL USE ONLY: Clear only current frame tracking data while preserving cumulative totals.
        
        This method is NOT called automatically anywhere in the code.
        
        This is the SAFE method to use for manual clearing of stale/expired current frame data.
        The cumulative total (self._total_count) is always preserved.
        
        In streaming scenarios, you typically don't need to call this at all.
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def clear_expired_tracks(self: Any, max_age_seconds: float = 300.0) -> int:
        """
        MANUAL USE ONLY: Clear current frame tracking data if no updates for a while.
        
        This method is NOT called automatically anywhere in the code.
        It's provided as a utility function for manual cleanup if needed.
        
        In streaming scenarios, you typically don't need to call this at all.
        The cumulative total should keep growing as new unique people are detected.
        
        This method only clears current frame tracking data while preserving
        the cumulative total count. The cumulative total should never decrease.
        
        Args:
            max_age_seconds: Maximum age in seconds before clearing current frame tracks
        
        Returns:
            Number of current frame tracks cleared
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_all_zone_counts(self: Any) -> Dict[str, Dict[str, int]]:
        """
        Get current and total counts for all zones.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for proximity detection.
        """
        ...

    def get_current_frame_count(self: Any) -> int:
        """
        Get the count of people in the current frame.
        """
        ...

    def get_frame_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about frame processing and global frame offset.
        """
        ...

    def get_global_frame_id(self: Any, local_frame_id: str) -> str:
        """
        Convert local frame ID to global frame ID.
        """
        ...

    def get_global_frame_offset(self: Any) -> int:
        """
        Get the current global frame offset.
        """
        ...

    def get_total_count(self: Any) -> int:
        """
        Get the total count of unique people tracked across all calls.
        """
        ...

    def get_total_frames_processed(self: Any) -> int:
        """
        Get the total number of frames processed across all calls.
        """
        ...

    def get_track_ids_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed information about track IDs.
        """
        ...

    def get_tracking_debug_info(self: Any) -> Dict[str, Any]:
        """
        Get detailed debugging information about tracking state.
        """
        ...

    def get_zone_current_count(self: Any, zone_name: str) -> int:
        """
        Get current count of people in a specific zone.
        """
        ...

    def get_zone_total_count(self: Any, zone_name: str) -> int:
        """
        Get total count of people who have been in a specific zone.
        """
        ...

    def get_zone_tracking_info(self: Any) -> Dict[str, Dict[str, Any]]:
        """
        Get detailed zone tracking information.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Process proximity detection use case - automatically detects single or multi-frame structure.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: proximity detection configuration
            context: Processing context
            stream_info: Stream information containing frame details (optional)
        
        Returns:
            ProcessingResult: Processing result with standardized agg_summary structure
        """
        ...

    def reset_frame_counter(self: Any) -> None:
        """
        Reset only the frame counter.
        """
        ...

    def reset_tracking_state(self: Any) -> None:
        """
        WARNING: This completely resets ALL tracking data including cumulative totals!
        
        This should ONLY be used when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        
        For clearing expired/stale tracks, use clear_current_frame_tracking() instead.
        """
        ...

    def set_global_frame_offset(self: Any, offset: int) -> None:
        """
        Set the global frame offset for video chunk processing.
        """
        ...

    def update_global_frame_offset(self: Any, frames_in_chunk: int) -> None:
        """
        Update global frame offset after processing a chunk.
        """
        ...


# From road_lane_detection
class LaneDetectionConfig:
    # Configuration for lane detection use case in road monitoring.

    ...

# From road_lane_detection
class LaneDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From road_traffic_density
class RoadTrafficConfig:
    # Configuration for Road Traffic Density detection use case.

    ...

# From road_traffic_density
class RoadTrafficUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From road_view_segmentation
class RoadViewSegmentationConfig:
    # Configuration for road lane segmentation use case in road lane monitoring.

    ...

# From road_view_segmentation
class RoadViewSegmentationUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From running_detection
class RunningConfirmationConfig:
    # Configuration for running detection confirmation layer.

    ...

# From running_detection
class RunningConfirmationLayer:
    # Per-track temporal confirmation for running detection.
    # Suppresses flickering FPs by requiring persistent running classification.

    def __init__(self: Any, config: Optional[Any] = None) -> None: ...

    def get_stats(self: Any) -> Dict[str, Any]: ...

    def reset(self: Any) -> Any: ...

    def update(self: Any, detections: List[Dict]) -> List[Dict]:
        """
        Apply confirmation logic to running detections.
        Only detections meeting min_positives_for_run threshold are confirmed.
        """
        ...


# From running_detection
class RunningDetectionConfig:
    # Configuration for running detection use case.

    ...

# From running_detection
class RunningDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]: ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From running_detection
class RunningDetector:
    # Velocity-based running detection from tracked person detections.
    # Uses height-normalized velocity for scale-invariant detection.

    def __init__(self: Any, config: Optional[Dict] = None) -> None: ...

    DEFAULT_CONFIG: Dict[Any, Any]

    def cleanup_lost_tracks(self: Any, active_track_ids: List[int]) -> Any: ...

    def reset(self: Any) -> Any: ...

    def update(self: Any, detections: List[Dict], frame_id: Optional[int] = None) -> List[Dict]:
        """
        Process detections and add velocity/running info.
        """
        ...


# From shelf_inventory_detection
class ShelfInventoryConfig:
    # Configuration for shelf inventory detection use case.

    ...

# From shelf_inventory_detection
class ShelfInventoryUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From shoplifting_detection
class ShopliftingDetectionConfig:
    # Configuration for Shoplifting detection use case in shoplifting monitoring.

    ...

# From shoplifting_detection
class ShopliftingDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From shopping_cart_analysis
class ShoppingCartConfig:
    # Configuration for Shopping cart detection use case in shopping cart monitoring.

    ...

# From shopping_cart_analysis
class ShoppingCartUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From skin_cancer_classification_img
class SkinCancerClassificationConfig:
    # Configuration for Skin Cancer Classification detection use case in Skin Cancer Classification monitoring.

    ...

# From skin_cancer_classification_img
class SkinCancerClassificationUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From smoker_detection
class SmokerDetectionConfig:
    # Configuration for Smoker detection use case.

    ...

# From smoker_detection
class SmokerDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From solar_panel
class SolarPanelConfig:
    # Configuration for solar panel detection use case in solar panel monitoring.

    ...

# From solar_panel
class SolarPanelUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From stopped_vehicle_monitoring
class StoppedVehicleMonitoringConfig:
    # Minimal configuration - only essential tunable parameters

    ...

# From stopped_vehicle_monitoring
class StoppedVehicleMonitoringUseCase:
    # Stopped vehicle detection use case.
    # Detects vehicles that have stopped for configurable duration.

    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Get total unique counts per category
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From stopped_vehicle_monitoring
class StoppedVehicleTracker:
    # Per-track state for stopped vehicle detection.
    # Uses hybrid approach: displacement buffer for jitter + EWMA for drift.

    def __init__(self: Any, track_id: int, initial_bbox: Dict, timestamp: float, zone_name: Optional[str] = None) -> None: ...

    def get_stationary_duration(self: Any, current_time: float) -> float:
        """
        Get time since vehicle became stationary (seconds)
        """
        ...

    def update(self: Any, bbox: Dict, timestamp: float, zone_name: Optional[str] = None) -> bool:
        """
        Update track state and return True if vehicle is confirmed stopped.
        
        Algorithm:
        1. Update position buffer
        2. Update EWMA centroid
        3. Check short-term jitter (buffer analysis)
        4. Check long-term drift (EWMA analysis)
        5. Confirm stopped state if both conditions met
        """
        ...


# From suspicious_activity_detection
class SusActivityConfig:
    # Configuration for PCB Defect Detection use case.

    ...

# From suspicious_activity_detection
class SusActivityUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def helper(self: Any, data: Any, config: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From tailgating_detection
class TailgatingConfig:
    # Tailgating post-processing configuration.
    #
    #     **Zones** are **required**: supply ``zones`` at the top level and/or under
    #     ``extra_params["zones"]`` (same shape). Top-level ``zones`` overrides
    #     ``extra_params`` on duplicate door ids.
    #
    #     **Matrice UI / API geometry**: When ``stream_info`` is present and
    #     ``PostProcessingConfigClient`` can reach the deployment post-processing
    #     config (env credentials or ``stream_info["config_client"]`` or
    #     ``TailgatingDetectionUseCase.set_config_client``), door geometry for one
    #     door is merged on the first frame. Expected keys in the camera
    #     ``zone_config`` (after denormalization) are ``lines["access_line"]`` or
    #     ``zones["access_line"]`` (two points), ``zones["secured_zone"]`` (polygon),
    #     and optionally ``zones["access_buffer_zone"]``. Use
    #     ``stream_info["tailgating_door_id"]`` to choose which door id to update when
    #     several doors exist; if exactly one door is configured, that id is used.
    #     For local file / bench runs without deployment context, set
    #     ``stream_info["skip_tailgating_api_zones"]`` to true to skip Matrice API
    #     resolution entirely (avoids opening a session when credentials exist).
    #
    #     **Output labeling**: In each frame, ``tracking_stats.detections`` may use
    #     ``category: "tailgating_person"`` for any detection whose ``track_id`` is
    #     listed in that frame’s tailgating analysis ``suspected_tailgaters``; others
    #     remain ``"person"``. Counts in ``total_counts`` / ``current_counts`` match
    #     those categories.
    #
    #     **Timing and geometry tuning** in ``extra_params`` (``access_window_sec``,
    #     ``silence_timeout_sec``, ``cooldown_sec``, ``allowed_persons_per_event``,
    #     ``max_follow_time_delta_sec``, ``min_motion_magnitude``,
    #     ``line_intersection_tolerance``, ``enable_direction_validation``,
    #     ``cross_memory_frames``) are merged onto this config and removed from
    #     ``extra_params`` so they take effect in production payloads that nest them.

    def __init__(self: Any, usecase: str = 'tailgating_detection', category: str = 'security', confidence_threshold: float = 0.5, target_categories: Optional[List[str]] = None, zones: Optional[Dict[str, Any]] = None, access_window_sec: float = 5.0, silence_timeout_sec: float = 2.0, cooldown_sec: float = 4.0, allowed_persons_per_event: int = 1, max_follow_time_delta_sec: float = 3.0, min_motion_magnitude: float = 0.002, line_intersection_tolerance: float = 0.02, enable_direction_validation: bool = False, cross_memory_frames: int = 0, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    EXTRA_PARAM_KEYS: Any

    def merge_zones_sources(top_level: Optional[Dict[str, Any]], from_extra: Any) -> Dict[str, Any]:
        """
        Merge zone maps; top-level ``zones`` wins on duplicate door ids.
        """
        ...

    def normalize_zones_mapping(raw: Any) -> Dict[str, Any]:
        """
        Coerce door_id -> ZoneConfig from ZoneConfig instances or nested dicts.
        """
        ...

    def validate(self: Any) -> Any: ...

    def validate_door_geometry(door_id: str, zone_cfg: Any) -> None: ...

    def validate_zone_point(label: str, pt: Any, door_id: str) -> None: ...


# From tailgating_detection
class TailgatingDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def draw_config_zones_on_frame(self: Any, frame: Any, config: Any) -> None:
        """
        Draw all doors in *config* onto *frame*.
        """
        ...

    def draw_zones_on_frame(self: Any, frame: Any, zone_cfg: Any) -> None:
        """
        Draw secured zone, optional access buffer zone, and access (intersection) line on
        *frame* in place. *frame* is BGR; zone points are normalized [0, 1].
        
        Requires ``opencv-python`` and ``numpy``.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any: ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set client used to resolve door geometry from deployment post-processing config.
        """
        ...


# From template_usecase
class TemplateUseCase:
    # Template use case showing how to implement standardized agg_summary structure.

    def __init__(self: Any) -> None:
        """
        Initialize template use case.
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for template use case.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Process data using template use case - automatically detects single or multi-frame structure.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: Template use case configuration
            context: Processing context
            stream_info: Stream information (optional)
        
        Returns:
            ProcessingResult: Processing result with standardized agg_summary structure
        """
        ...


# From template_usecase
class TemplateUseCaseConfig:
    # Configuration for Template Use Case.

    def __init__(self: Any, usecase: str = 'template_usecase', category: str = 'general', confidence_threshold: float = 0.5, target_categories: List[str] = None, enable_analytics: bool = True, alert_threshold: int = 5, **kwargs: Any) -> None: ...

    def validate(self: Any) -> List[str]:
        """
        Validate configuration.
        """
        ...


# From theft_detection
class TheftDetectionConfig:
    # Configuration for theft detection use case in theft monitoring.

    ...

# From theft_detection
class TheftDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for theft post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        """
        ...


# From traffic_sign_monitoring
class TrafficSignMonitoringConfig:
    # Configuration for traffic sign monitoring use case.

    ...

# From traffic_sign_monitoring
class TrafficSignMonitoringUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for traffic sign post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        """
        ...


# From underground_pipeline_defect_detection
class UndergroundPipelineDefectConfig:
    # Configuration for Underground Pipeline Defect Detection use case.

    ...

# From underground_pipeline_defect_detection
class UndergroundPipelineDefectUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From underwater_pollution_detection
class UnderwaterPlasticConfig:
    # Configuration for underwater pollution detection use case in underwater pollution monitoring.

    ...

# From underwater_pollution_detection
class UnderwaterPlasticUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From vegetable_detection
class VegetableDetectionConfig:
    # Configuration for vegetable detection use case.

    ...

# From vegetable_detection
class VegetableDetectionUseCase:
    # Vegetable detection processor for post-processing model outputs.

    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process vegetable detections and generate agg_summary output.
        """
        ...


# From vehicle_color_detection
class VehicleColorDetectionConfig:
    # Configuration for vehicle color detection use case in vehicle monitoring.

    ...

# From vehicle_color_detection
class VehicleColorDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From vehicle_monitoring
class VehicleMonitoringConfig:
    # Configuration for vehicle detection use case in vehicle monitoring.

    ...

# From vehicle_monitoring
class VehicleMonitoringUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From vehicle_monitoring_drone_view
class VehicleMonitoringDroneViewConfig:
    # Configuration for drone view vehicle monitoring use case.

    ...

# From vehicle_monitoring_drone_view
class VehicleMonitoringDroneViewUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From vehicle_monitoring_parking_lot
class VehicleMonitoringParkingLotConfig:
    # Configuration for vehicle detection use case in parking lot vehicle monitoring.

    ...

# From vehicle_monitoring_parking_lot
class VehicleMonitoringParkingLotUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From vehicle_monitoring_wrong_way
class VehicleMonitoringWrongWayConfig:
    # Configuration for wrong-way vehicle detection use case.

    ...

# From vehicle_monitoring_wrong_way
class VehicleMonitoringWrongWayUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Get total counts per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From warehouse_object_segmentation
class WarehouseObjectConfig:
    # Configuration for Warehouse pallet detection use case in warehouse pallet monitoring.

    ...

# From warehouse_object_segmentation
class WarehouseObjectUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From waterbody_segmentation
class WaterBodyConfig:
    # Configuration for WaterBody detection use case in WaterBody monitoring.

    ...

# From waterbody_segmentation
class WaterBodyUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From weapon_detection
class IncidentIdTracker:
    # Tracks severity-level progression across frames to produce monotonically
    # increasing incident/alert IDs (7 frames to advance a level; 130 empty
    # frames to close an incident).

    def __init__(self: Any) -> None: ...

    def advance(self: Any, sev_level: str, current_ts: str) -> Tuple[int, int]:
        """
        Feed a severity level ("" if no detection). Returns (rank_id, alert_id).
        """
        ...


# From weapon_detection
class WeaponDetectionConfig:
    ...

# From weapon_detection
class WeaponDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]: ...

    def get_duration_seconds(self: Any, start_time: Any, end_time: Any) -> Any: ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]: ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From weld_defect_detection
class WeldDefectConfig:
    # Configuration for weld defect detection use case.

    ...

# From weld_defect_detection
class WeldDefectUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...


# From wildlife_monitoring
class WildLifeMonitoringConfig:
    # Configuration for WildLife Monitoring use case.

    ...

# From wildlife_monitoring
class WildLifeMonitoringUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From windmill_maintenance
class WindmillMaintenanceConfig:
    # Configuration for windmill maintenance detection use case.

    ...

# From windmill_maintenance
class WindmillMaintenanceUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any = None, config: Any = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


# From wound_segmentation
class WoundConfig:
    # Configuration for wound detection use case in wound monitoring.

    ...

# From wound_segmentation
class WoundSegmentationUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...


from . import Histopathological_Cancer_Detection_img, abandoned_object_detection, advanced_customer_service, age_detection, age_gender_detection, animal_detection, anti_spoofing_detection, area_utilization, assembly_line_detection, banana_defect_detection, basic_counting_tracking, blood_cancer_detection_img, bottle_defect_detection, burglary_detection, car_damage_detection, car_part_segmentation, car_service, cardiomegaly_classification, cell_microscopy_segmentation, chicken_pose_detection, child_monitoring, claude_people_counting_usecase, color_detection, color_map_utils, concrete_crack_detection, crop_weed_detection, crowd_density_heatmaps, crowdflow, customer_service, defect_detection_products, distracted_driver_detection, drone_traffic_monitoring, drowsy_driver_detection, dwell_detection, emergency_vehicle_detection, face_covering_detection_pose, face_emotion, face_recognition, fall_detection, fashion_detection, fence_climbing_detection, fence_climbing_detection_pose, fence_climbing_with_zone, field_mapping, fire_detection, flare_analysis, flower_segmentation, footfall, footfall_bkcp, gas_leak_detection, gender_detection, gloves_boots_detection, hazard_zone_entry, heatmaps, human_activity_recognition, intrusion_detection, landslide_detection, leaf, leaf_disease, leak_detection, license_plate_detection, license_plate_monitoring, liquid_leak_detection, litter_monitoring, loitering_detection, mask_detection, mask_type_detection, natural_disaster, overcrowding_detection, package_detection, parking, parking_lot_analytics, parking_space_detection, pcb_defect_detection, pedestrian_detection, people_counting, people_counting_bckp, people_counting_in_zone, people_tracking, people_tracking_bkcp, phone_screen_defect_detection, pipe_corrosion_detection, pipe_gas_leak_detection, pipeline_detection, plaque_segmentation_img, pothole_detection, pothole_segmentation, ppe_compliance, price_tag_detection, proximity_detection, road_lane_detection, road_traffic_density, road_view_segmentation, running_detection, shelf_inventory_detection, shoplifting_detection, shopping_cart_analysis, skin_cancer_classification_img, smoker_detection, solar_panel, stopped_vehicle_monitoring, suspicious_activity_detection, tailgating_detection, template_usecase, theft_detection, traffic_sign_monitoring, underground_pipeline_defect_detection, underwater_pollution_detection, vegetable_detection, vehicle_color_detection, vehicle_monitoring, vehicle_monitoring_drone_view, vehicle_monitoring_parking_lot, vehicle_monitoring_wrong_way, warehouse_object_segmentation, waterbody_segmentation, weapon_detection, weld_defect_detection, wildlife_monitoring, windmill_maintenance, wound_segmentation