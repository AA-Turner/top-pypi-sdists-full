"""Auto-generated stub for module: config_utils."""
from typing import Any, Dict, List, Optional, Tuple, Union

from ..usecases.basic_counting_tracking import BasicCountingTrackingConfig
from .config import AlertConfig, CustomerServiceConfig, IntrusionConfig, LineConfig, PeopleCountingConfig, PeopleTrackingConfig, ProximityConfig, TrackingConfig, ZoneConfig, config_manager

# Functions
def create_advanced_customer_service_config(customer_areas: Dict[str, List[List[float]]], staff_areas: Dict[str, List[List[float]]], service_areas: Optional[Dict[str, List[List[float]]]] = None, staff_categories: List[str] = None, customer_categories: List[str] = None, service_proximity_threshold: float = 100.0, max_service_time: float = 1800.0, tracking_method: str = 'kalman', enable_analytics: bool = True, confidence_threshold: float = 0.6, alert_thresholds: Optional[Dict[str, int]] = None, category: str = 'sales', **kwargs: Any) -> Any:
    """
    Create advanced customer service configuration with journey analysis.
    
    Args:
        customer_areas: Dictionary of customer area polygons
        staff_areas: Dictionary of staff area polygons
        service_areas: Optional service area polygons
        staff_categories: List of staff category names
        customer_categories: List of customer category names
        service_proximity_threshold: Distance threshold for service interactions
        max_service_time: Maximum service time in seconds
        tracking_method: Tracking method to use
        enable_analytics: Enable advanced analytics
        confidence_threshold: Detection confidence threshold
        alert_thresholds: Alert threshold configuration
        category: Use case category
        **kwargs: Additional configuration parameters
    
    Returns:
        CustomerServiceConfig: Configured customer service config
    """
    ...
def create_basic_counting_tracking_config(confidence_threshold: float = 0.5, target_categories: Optional[List[str]] = None, zones: Optional[Dict[str, List[List[float]]]] = None, enable_tracking: bool = True, tracking_method: str = 'kalman', max_age: int = 30, min_hits: int = 3, count_thresholds: Optional[Dict[str, int]] = None, zone_thresholds: Optional[Dict[str, int]] = None, alert_cooldown: float = 60.0, enable_unique_counting: bool = True, **kwargs: Any) -> Any:
    """
    Create a basic counting with tracking configuration.
    
    This is a simplified configuration for scenarios where you need basic object counting
    with tracking capabilities and simple alerting. It's designed to be easy to use
    while providing essential tracking and counting features.
    
    Args:
        confidence_threshold: Minimum confidence for detections (0.0-1.0)
        target_categories: List of category names to count and track
        zones: Dictionary of zone_name -> polygon points for spatial analysis
        enable_tracking: Whether to enable object tracking
        tracking_method: Tracking algorithm ('kalman', 'sort', 'deepsort', 'bytetrack')
        max_age: Maximum age for tracks in frames
        min_hits: Minimum hits before confirming track
        count_thresholds: Dictionary of category -> max_count for count alerts
        zone_thresholds: Dictionary of zone_name -> max_occupancy for zone alerts
        alert_cooldown: Alert cooldown time in seconds
        enable_unique_counting: Enable unique object counting using tracking
        **kwargs: Additional configuration parameters
    
    Returns:
        BasicCountingTrackingConfig: Configured basic counting tracking configuration
    
    Example:
        # Basic setup with tracking
        config = create_basic_counting_tracking_config(
            confidence_threshold=0.6,
            target_categories=["person", "car", "bicycle"],
            enable_tracking=True,
            tracking_method="bytetrack"
        )
    
        # With zones and alerts
        config = create_basic_counting_tracking_config(
            confidence_threshold=0.5,
            zones={
                "entrance": [[0, 0], [200, 0], [200, 100], [0, 100]],
                "parking": [[200, 0], [800, 0], [800, 400], [200, 400]]
            },
            count_thresholds={"person": 20, "car": 50},
            zone_thresholds={"entrance": 10, "parking": 30},
            alert_cooldown=120.0
        )
    
        # Simple object counting
        config = create_basic_counting_tracking_config(
            target_categories=["object"],
            enable_tracking=False,  # Disable tracking for simple counting
            enable_unique_counting=False
        )
    """
    ...
def create_config_from_template(usecase: str, template_file: Optional[Union[str, Any]] = None, **overrides: Any) -> Any:
    """
    Create configuration from a template file or default template.
    
    Args:
        usecase: Use case name ('people_counting', 'customer_service', 'advanced_customer_service', 'basic_counting_tracking')
        template_file: Optional path to template file (JSON/YAML)
        **overrides: Parameters to override in the template
    
    Returns:
        BaseConfig: Created configuration
    
    Example:
        # From default template
        config = create_config_from_template(
            "people_counting",
            confidence_threshold=0.7,
            zones={"area1": [[0, 0], [100, 0], [100, 100], [0, 100]]}
        )
    
        # From file template
        config = create_config_from_template(
            "customer_service",
            template_file="templates/retail_config.json",
            confidence_threshold=0.6
        )
    
        # Basic counting with tracking
        config = create_config_from_template(
            "basic_counting_tracking",
            target_categories=["person", "car"],
            enable_tracking=True
        )
    """
    ...
def create_customer_service_config(confidence_threshold: float = 0.5, customer_areas: Optional[Dict[str, List[List[float]]]] = None, staff_areas: Optional[Dict[str, List[List[float]]]] = None, service_areas: Optional[Dict[str, List[List[float]]]] = None, staff_categories: Optional[List[str]] = None, customer_categories: Optional[List[str]] = None, service_proximity_threshold: float = 100.0, enable_tracking: bool = True, enable_alerts: bool = False, category: str = 'sales', **kwargs: Any) -> Any:
    """
    Create a customer service configuration with sensible defaults.
    
    Args:
        confidence_threshold: Minimum confidence for detections (0.0-1.0)
        customer_areas: Dictionary of area_name -> polygon for customer areas
        staff_areas: Dictionary of area_name -> polygon for staff areas
        service_areas: Dictionary of area_name -> polygon for service areas
        staff_categories: List of category names that represent staff
        customer_categories: List of category names that represent customers
        service_proximity_threshold: Distance threshold for service interactions
        enable_tracking: Whether to enable object tracking
        enable_alerts: Whether to enable alerting system
        category: Use case category
        **kwargs: Additional configuration parameters
    
    Returns:
        CustomerServiceConfig: Configured customer service configuration
    
    Example:
        config = create_customer_service_config(
            confidence_threshold=0.6,
            customer_areas={
                "waiting_area": [[0, 0], [200, 0], [200, 100], [0, 100]]
            },
            staff_areas={
                "service_desk": [[200, 0], [400, 0], [400, 100], [200, 100]]
            },
            service_proximity_threshold=150.0
        )
    """
    ...
def create_intrusion_detection_config(confidence_threshold: float = 0.5, zones: Optional[Dict[str, List[List[float]]]] = None, person_categories: Optional[List[str]] = None, enable_tracking: bool = False, time_window_minutes: int = 60, alert_thresholds: Optional[Dict[str, int]] = None, category: str = 'security', **kwargs: Any) -> Any:
    """
    Create a intrusion detection configuration with sensible defaults.
    
    Args:
        confidence_threshold: Minimum confidence for detections (0.0-1.0)
        zones: Dictionary of zone_name -> polygon points [[x1,y1], [x2,y2], ...]
        person_categories: List of category names that represent people
        enable_tracking: Whether to enable object tracking
        time_window_minutes: Time window for counting statistics
        alert_thresholds: Dictionary of zone_name -> max_count for alerts
        category: Use case category
        **kwargs: Additional ``IntrusionConfig`` fields, including ``advanced_tracker_config``
            (dict or ``IntrusionAdvancedTrackerConfig``), ``track_merge_iou_threshold``,
            ``track_merge_time_window_seconds``, ``min_inside_frames``, etc.
    
    Returns:
        IntrusionConfig: Configured intrusion detection configuration
    
    Example:
        config = create_intrusion_detection_config(
            confidence_threshold=0.6,
            zones={
                "High": [[535, 558], [745, 453], [846, 861], [665, 996]],
                "Mid": [[663, 995], [925, 817], [1266, 885], [1012, 1116]]
            },
            alert_thresholds={"High": 0, "Mid": 0}
        )
    """
    ...
def create_office_zones(office_width: float = 800, office_height: float = 600, reception_height: float = 150) -> Dict[str, List[List[float]]]:
    """
    Create typical office zone layout.
    
    Args:
        office_width: Total office width
        office_height: Total office height
        reception_height: Height of reception area
    
    Returns:
        Dict[str, List[List[float]]]: Dictionary of zone_name -> polygon
    """
    ...
def create_people_counting_config(confidence_threshold: float = 0.5, zones: Optional[Dict[str, List[List[float]]]] = None, person_categories: Optional[List[str]] = None, enable_tracking: bool = False, time_window_minutes: int = 60, alert_thresholds: Optional[Dict[str, int]] = None, category: str = 'general', **kwargs: Any) -> Any:
    """
    Create a people counting configuration with sensible defaults.
    
    Args:
        confidence_threshold: Minimum confidence for detections (0.0-1.0)
        zones: Dictionary of zone_name -> polygon points [[x1,y1], [x2,y2], ...]
        person_categories: List of category names that represent people
        enable_tracking: Whether to enable object tracking
        time_window_minutes: Time window for counting statistics
        alert_thresholds: Dictionary of zone_name -> max_count for alerts
        category: Use case category
        **kwargs: Additional configuration parameters
    
    Returns:
        PeopleCountingConfig: Configured people counting configuration
    
    Example:
        config = create_people_counting_config(
            confidence_threshold=0.6,
            zones={
                "entrance": [[0, 0], [100, 0], [100, 100], [0, 100]],
                "exit": [[200, 0], [300, 0], [300, 100], [200, 100]]
            },
            alert_thresholds={"entrance": 10, "exit": 5}
        )
    """
    ...
def create_people_tracking_config(confidence_threshold: float = 0.5, zones: Optional[Dict[str, List[List[float]]]] = None, line_config: Optional[Dict[str, Any]] = None, person_categories: Optional[List[str]] = None, enable_tracking: bool = True, enable_unique_counting: bool = True, time_window_minutes: int = 60, count_thresholds: Optional[Dict[str, int]] = None, occupancy_thresholds: Optional[Dict[str, int]] = None, crossing_thresholds: Optional[Dict[str, int]] = None, enable_smoothing: bool = False, smoothing_algorithm: str = 'kalman', smoothing_window_size: int = 5, smoothing_cooldown_frames: int = 10, smoothing_confidence_range_factor: float = 0.2, category: str = 'general', alert_type: Optional[List[str]] = None, alert_value: Optional[List[str]] = None, alert_incident_category: Optional[List[str]] = None, **kwargs: Any) -> Any:
    """
    Create a people tracking configuration with sensible defaults.
    
    Args:
        confidence_threshold: Minimum confidence for detections (0.0-1.0)
        zones: Dictionary of zone_name -> polygon points [[x1,y1], [x2,y2], ...]
        line_config: Dictionary defining line crossing configuration (e.g., {"points": [[x1,y1], [x2,y2]], "side1_label": "Outside", "side2_label": "Inside"})
        person_categories: List of category names that represent people
        enable_tracking: Whether to enable object tracking
        enable_unique_counting: Whether to enable unique people counting
        time_window_minutes: Time window for tracking statistics
        count_thresholds: Dictionary of category -> max_count for alerts
        occupancy_thresholds: Dictionary of zone_name -> max_count for zone occupancy alerts
        crossing_thresholds: Dictionary of direction (e.g., 'side1_to_side2') -> max_count for line crossing alerts
        enable_smoothing: Whether to enable bounding box smoothing
        smoothing_algorithm: Algorithm for smoothing (e.g., 'kalman')
        smoothing_window_size: Number of frames for smoothing window
        smoothing_cooldown_frames: Frames to wait before re-smoothing
        smoothing_confidence_range_factor: Factor for confidence range in smoothing
        category: Use case category
        alert_type: List of alert types (e.g., ['email', 'sms'])
        alert_value: List of alert values corresponding to alert types (e.g., ['user@example.com'])
        alert_incident_category: List of alert incident categories (e.g., ['Tracking Alert'])
        **kwargs: Additional configuration parameters
    
    Returns:
        PeopleTrackingConfig: Configured people tracking configuration
    
    Example:
        config = create_people_tracking_config(
            confidence_threshold=0.6,
            zones={
                "entrance": [[0, 0], [100, 0], [100, 100], [0, 100]],
                "exit": [[200, 0], [300, 0], [300, 100], [200, 100]]
            },
            line_config={
                "points": [[100, 200], [300, 200]],
                "side1_label": "Outside",
                "side2_label": "Inside"
            },
            count_thresholds={"all": 10},
            occupancy_thresholds={"entrance": 5, "exit": 3},
            crossing_thresholds={"side1_to_side2": 2, "side2_to_side1": 2},
            enable_tracking=True,
            enable_smoothing=True
        )
    """
    ...
def create_polygon_zone(points: List[Tuple[float, float]]) -> List[List[float]]:
    """
    Create a polygon zone from a list of coordinate tuples.
    
    Args:
        points: List of (x, y) coordinate tuples
    
    Returns:
        List[List[float]]: Polygon points in the required format
    
    Example:
        zone = create_polygon_zone([(0, 0), (100, 0), (100, 100), (50, 150), (0, 100)])
    """
    ...
def create_proximity_detection_config(confidence_threshold: float = 0.5, zones: Optional[Dict[str, List[List[float]]]] = None, person_categories: Optional[List[str]] = None, enable_tracking: bool = False, time_window_minutes: int = 60, alert_thresholds: Optional[Dict[str, int]] = None, category: str = 'general', **kwargs: Any) -> Any:
    """
    Create a proximity detection configuration with sensible defaults.
    
    Args:
        confidence_threshold: Minimum confidence for detections (0.0-1.0)
        zones: Dictionary of zone_name -> polygon points [[x1,y1], [x2,y2], ...]
        person_categories: List of category names that represent people
        enable_tracking: Whether to enable object tracking
        time_window_minutes: Time window for counting statistics
        alert_thresholds: Dictionary of zone_name -> max_count for alerts
        category: Use case category
        **kwargs: Additional configuration parameters
    
    Returns:
        ProximityConfig: Configured proximity detection configuration
    
    Example:
        config = create_proximity_detection_config(
            confidence_threshold=0.6,
            zones={
                "entrance": [[0, 0], [100, 0], [100, 100], [0, 100]],
                "exit": [[200, 0], [300, 0], [300, 100], [200, 100]]
            },
            alert_thresholds={"entrance": 10, "exit": 5}
        )
    """
    ...
def create_retail_store_zones(store_width: float = 1000, store_height: float = 600, entrance_width: float = 200, checkout_width: float = 300) -> Dict[str, List[List[float]]]:
    """
    Create typical retail store zone layout.
    
    Args:
        store_width: Total store width
        store_height: Total store height
        entrance_width: Width of entrance area
        checkout_width: Width of checkout area
    
    Returns:
        Dict[str, List[List[float]]]: Dictionary of zone_name -> polygon
    """
    ...
def create_zone_from_bbox(x: float, y: float, width: float, height: float) -> List[List[float]]:
    """
    Create a rectangular zone from bounding box coordinates.
    
    Args:
        x: Left coordinate
        y: Top coordinate
        width: Zone width
        height: Zone height
    
    Returns:
        List[List[float]]: Polygon points for the rectangular zone
    
    Example:
        zone = create_zone_from_bbox(100, 50, 200, 150)
        # Returns [[100, 50], [300, 50], [300, 200], [100, 200]]
    """
    ...
def get_use_case_examples() -> Dict[str, Dict[str, Any]]:
    """
    Get example configurations for all supported use cases.
    
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary of use_case -> example_config
    
    Example:
        examples = get_use_case_examples()
        people_counting_example = examples["people_counting"]
        print(json.dumps(people_counting_example, indent=2))
    """
    ...
def validate_zone_polygon(polygon: List[List[float]]) -> Tuple[bool, str]:
    """
    Validate a zone polygon for correctness.
    
    Args:
        polygon: Polygon points [[x1, y1], [x2, y2], ...]
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    
    Example:
        is_valid, error = validate_zone_polygon([[0, 0], [100, 0], [100, 100]])
        if not is_valid:
            print(f"Invalid polygon: {error}")
    """
    ...
