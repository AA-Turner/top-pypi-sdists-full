"""
Configuration utilities for easy post-processing setup.

This module provides convenient functions for creating common post-processing configurations
without needing to understand the complex configuration structure.
"""

from typing import Dict, List, Any, Tuple, Optional, Union
from pathlib import Path
import json

from .config import (
    PeopleCountingConfig,
    CustomerServiceConfig,
    IntrusionConfig,
    ProximityConfig,
    ZoneConfig,
    TrackingConfig,
    AlertConfig,
    config_manager
)

# Note: BasicCountingTrackingConfig import moved to function level to avoid circular imports


def create_people_counting_config(
    confidence_threshold: float = 0.5,
    zones: Optional[Dict[str, List[List[float]]]] = None,
    person_categories: Optional[List[str]] = None,
    enable_tracking: bool = False,
    time_window_minutes: int = 60,
    alert_thresholds: Optional[Dict[str, int]] = None,
    category: str = "general",
    **kwargs
) -> PeopleCountingConfig:
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
    # Create zone configuration if zones provided
    zone_config = None
    if zones:
        zone_config = ZoneConfig(zones=zones)
    
    # Create alert configuration if thresholds provided  
    alert_config = None
    if alert_thresholds:
        alert_config = AlertConfig(count_thresholds=alert_thresholds)
    
    return PeopleCountingConfig(
        category=category,
        usecase="people_counting",
        confidence_threshold=confidence_threshold,
        zone_config=zone_config,
        person_categories=person_categories or ["person", "people"],
        enable_tracking=enable_tracking,
        time_window_minutes=time_window_minutes,
        alert_config=alert_config,
        **kwargs
    )


def create_intrusion_detection_config(
    confidence_threshold: float = 0.5,
    zones: Optional[Dict[str, List[List[float]]]] = None,
    person_categories: Optional[List[str]] = None,
    enable_tracking: bool = False,
    time_window_minutes: int = 60,
    alert_thresholds: Optional[Dict[str, int]] = None,
    category: str = "security",
    **kwargs
) -> IntrusionConfig:
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
        **kwargs: Additional configuration parameters
        
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
    # Create zone configuration if zones provided
    zone_config = None
    if zones:
        zone_config = ZoneConfig(zones=zones)
    
    # Create alert configuration if thresholds provided  
    alert_config = None
    if alert_thresholds:
        alert_config = AlertConfig(count_thresholds=alert_thresholds)
    
    return IntrusionConfig(
        category=category,
        usecase="intrusion_detection",
        confidence_threshold=confidence_threshold,
        zone_config=zone_config,
        person_categories=person_categories or ["person"],
        enable_tracking=enable_tracking,
        time_window_minutes=time_window_minutes,
        alert_config=alert_config,
        **kwargs
    )


def create_proximity_detection_config(
    confidence_threshold: float = 0.5,
    zones: Optional[Dict[str, List[List[float]]]] = None,
    person_categories: Optional[List[str]] = None,
    enable_tracking: bool = False,
    time_window_minutes: int = 60,
    alert_thresholds: Optional[Dict[str, int]] = None,
    category: str = "general",
    **kwargs
) -> ProximityConfig:
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
    # Create zone configuration if zones provided
    zone_config = None
    if zones:
        zone_config = ZoneConfig(zones=zones)
    
    # Create alert configuration if thresholds provided  
    alert_config = None
    if alert_thresholds:
        alert_config = AlertConfig(count_thresholds=alert_thresholds)
    
    return ProximityConfig(
        category=category,
        usecase="proximity_detection",
        confidence_threshold=confidence_threshold,
        zone_config=zone_config,
        person_categories=person_categories or ["person"],
        enable_tracking=enable_tracking,
        time_window_minutes=time_window_minutes,
        alert_config=alert_config,
        **kwargs
    )


def create_customer_service_config(
    confidence_threshold: float = 0.5,
    customer_areas: Optional[Dict[str, List[List[float]]]] = None,
    staff_areas: Optional[Dict[str, List[List[float]]]] = None,
    service_areas: Optional[Dict[str, List[List[float]]]] = None,
    staff_categories: Optional[List[str]] = None,
    customer_categories: Optional[List[str]] = None,
    service_proximity_threshold: float = 100.0,
    enable_tracking: bool = True,
    enable_alerts: bool = False,
    category: str = "sales",
    **kwargs
) -> CustomerServiceConfig:
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
    # Create tracking configuration if enabled
    tracking_config = None
    if enable_tracking:
        tracking_config = TrackingConfig(
            tracking_method="kalman",
            max_age=30,
            min_hits=3
        )
    
    # Create alert configuration if enabled
    alert_config = None
    if enable_alerts:
        alert_config = AlertConfig()
    
    return CustomerServiceConfig(
        category=category,
        usecase="customer_service",
        confidence_threshold=confidence_threshold,
        customer_areas=customer_areas or {},
        staff_areas=staff_areas or {},
        service_areas=service_areas or {},
        staff_categories=staff_categories or ["staff", "employee"],
        customer_categories=customer_categories or ["customer", "person"],
        service_proximity_threshold=service_proximity_threshold,
        enable_tracking=enable_tracking,
        tracking_config=tracking_config,
        alert_config=alert_config,
        **kwargs
    )


def create_advanced_customer_service_config(
    customer_areas: Dict[str, List[List[float]]],
    staff_areas: Dict[str, List[List[float]]],
    service_areas: Optional[Dict[str, List[List[float]]]] = None,
    staff_categories: List[str] = None,
    customer_categories: List[str] = None,
    service_proximity_threshold: float = 100.0,
    max_service_time: float = 1800.0,
    tracking_method: str = "kalman",
    enable_analytics: bool = True,
    confidence_threshold: float = 0.6,
    alert_thresholds: Optional[Dict[str, int]] = None,
    category: str = "sales",
    **kwargs
) -> CustomerServiceConfig:
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
    # Set defaults
    if staff_categories is None:
        staff_categories = ["staff", "employee", "worker"]
    if customer_categories is None:
        customer_categories = ["customer", "person", "visitor"]
    if service_areas is None:
        service_areas = {}
    
    # Create tracking configuration for journey analysis
    tracking_config = TrackingConfig(
        tracking_method=tracking_method,
        max_age=30,
        min_hits=3,
        iou_threshold=0.3,
        target_classes=staff_categories + customer_categories,
        use_appearance_features=True,
        appearance_threshold=0.7
    )
    
    # Create alert configuration
    alert_config = None
    if alert_thresholds:
        alert_config = AlertConfig(
            count_thresholds=alert_thresholds,
            occupancy_thresholds={},
            service_time_threshold=max_service_time,
            alert_cooldown=30.0
        )
    
    return CustomerServiceConfig(
        category=category,
        usecase="advanced_customer_service",
        customer_areas=customer_areas,
        staff_areas=staff_areas,
        service_areas=service_areas,
        staff_categories=staff_categories,
        customer_categories=customer_categories,
        service_proximity_threshold=service_proximity_threshold,
        max_service_time=max_service_time,
        confidence_threshold=confidence_threshold,
        enable_analytics=enable_analytics,
        enable_tracking=True,
        tracking_config=tracking_config,
        alert_config=alert_config,
        **kwargs
    )


def create_basic_counting_tracking_config(
    confidence_threshold: float = 0.5,
    target_categories: Optional[List[str]] = None,
    zones: Optional[Dict[str, List[List[float]]]] = None,
    enable_tracking: bool = True,
    tracking_method: str = "kalman",
    max_age: int = 30,
    min_hits: int = 3,
    count_thresholds: Optional[Dict[str, int]] = None,
    zone_thresholds: Optional[Dict[str, int]] = None,
    alert_cooldown: float = 60.0,
    enable_unique_counting: bool = True,
    **kwargs
):
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
    # Import here to avoid circular imports
    from ..usecases.basic_counting_tracking import BasicCountingTrackingConfig
    
    return BasicCountingTrackingConfig(
        category="general",
        usecase="basic_counting_tracking",
        confidence_threshold=confidence_threshold,
        target_categories=target_categories or ["person", "people", "object"],
        zones=zones,
        enable_tracking=enable_tracking,
        tracking_method=tracking_method,
        max_age=max_age,
        min_hits=min_hits,
        count_thresholds=count_thresholds,
        zone_thresholds=zone_thresholds,
        alert_cooldown=alert_cooldown,
        enable_unique_counting=enable_unique_counting,
        **kwargs
    )


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
    return [
        [x, y],                    # Top-left
        [x + width, y],            # Top-right
        [x + width, y + height],   # Bottom-right
        [x, y + height]            # Bottom-left
    ]


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
    return [[float(x), float(y)] for x, y in points]


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
    if not isinstance(polygon, list):
        return False, "Polygon must be a list"
    
    if len(polygon) < 3:
        return False, "Polygon must have at least 3 points"
    
    for i, point in enumerate(polygon):
        if not isinstance(point, list) or len(point) != 2:
            return False, f"Point {i} must be a list of 2 coordinates"
        
        try:
            float(point[0])
            float(point[1])
        except (ValueError, TypeError):
            return False, f"Point {i} coordinates must be numeric"
    
    return True, ""


def create_config_from_template(
    usecase: str,
    template_file: Optional[Union[str, Path]] = None,
    **overrides
):
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
    if template_file:
        # Load from file and apply overrides
        config = config_manager.load_from_file(template_file)
        if overrides:
            # Convert to dict, apply overrides, and recreate
            config_dict = config.to_dict()
            config_dict.update(overrides)
            config = config_manager.create_config(usecase, **config_dict)
        return config
    else:
        # Create from default template with overrides
        if usecase == "people_counting":
            return create_people_counting_config(**overrides)
        elif usecase == "intrusion_detection":
            return create_intrusion_detection_config(**overrides)
        elif usecase == "proximity_detection":
            return create_proximity_detection_config(**overrides)
        elif usecase == "customer_service":
            return create_customer_service_config(**overrides)
        elif usecase == "advanced_customer_service":
            return create_advanced_customer_service_config(**overrides)
        elif usecase == "basic_counting_tracking":
            return create_basic_counting_tracking_config(**overrides)
        else:
            raise ValueError(f"Unsupported use case: {usecase}")


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
    return {
        "people_counting": {
            "usecase": "people_counting",
            "category": "general",
            "confidence_threshold": 0.6,
            "enable_tracking": True,
            "time_window_minutes": 60,
            "person_categories": ["person", "people"],
            "zone_config": {
                "zones": {
                    "entrance": [[0, 0], [200, 0], [200, 100], [0, 100]],
                    "main_area": [[200, 0], [800, 0], [800, 600], [200, 600]],
                    "exit": [[800, 0], [1000, 0], [1000, 100], [800, 100]]
                }
            },
            "alert_config": {
                "count_thresholds": {
                    "entrance": 10,
                    "main_area": 50,
                    "exit": 10
                },
                "alert_cooldown": 60.0
            }
        },
        
        "intrusion_detection": {
            "usecase": "intrusion_detection",
            "category": "security",
            "confidence_threshold": 0.6,
            "enable_tracking": True,
            "time_window_minutes": 60,
            "person_categories": ["person"],
            "zone_config": {
                "zones": {
                    "Boarding Gate": [[314, 652], [1034, 317], [1854, 845], [987, 1491]]
                }
            },
            "alert_config": {
                "count_thresholds": {
                    "Boarding Gate": 0
                },
                "alert_cooldown": 10.0
            }
        },
        
        "proximity_detection": {
            "usecase": "proximity_detection",
            "category": "security",
            "confidence_threshold": 0.6,
            "enable_tracking": True,
            "time_window_minutes": 60,
            "person_categories": ["person"],
            "zone_config": {
                "zones": {}
            },
            "alert_config": {
                "count_thresholds": {
                    "Boarding Gate": 0
                },
                "alert_cooldown": 10.0
            }
        },
        
        "customer_service": {
            "usecase": "customer_service", 
            "category": "sales",
            "confidence_threshold": 0.5,
            "enable_tracking": True,
            "staff_categories": ["staff", "employee"],
            "customer_categories": ["customer", "person"],
            "service_proximity_threshold": 120.0,
            "customer_areas": {
                "waiting_area": [[0, 0], [300, 0], [300, 200], [0, 200]],
                "service_area": [[300, 0], [600, 0], [600, 200], [300, 200]]
            },
            "staff_areas": {
                "service_desk": [[350, 50], [550, 50], [550, 150], [350, 150]]
            },
            "tracking_config": {
                "tracking_method": "kalman",
                "max_age": 30,
                "min_hits": 3,
                "iou_threshold": 0.3
            }
        },
        
        "advanced_customer_service": {
            "usecase": "advanced_customer_service",
            "category": "sales", 
            "confidence_threshold": 0.6,
            "enable_tracking": True,
            "enable_analytics": True,
            "staff_categories": ["staff", "employee"],
            "customer_categories": ["customer", "person"],
            "service_proximity_threshold": 100.0,
            "max_service_time": 1800.0,
            "enable_journey_analysis": True,
            "enable_queue_analytics": True,
            "customer_areas": {
                "entrance": [[0, 0], [100, 0], [100, 100], [0, 100]],
                "queue_area": [[100, 0], [400, 0], [400, 150], [100, 150]],
                "service_area": [[400, 0], [700, 0], [700, 150], [400, 150]]
            },
            "staff_areas": {
                "reception": [[450, 50], [650, 50], [650, 100], [450, 100]]
            },
            "service_areas": {
                "service_counter": [[400, 0], [700, 0], [700, 50], [400, 50]]
            },
            "tracking_config": {
                "tracking_method": "bytetrack",
                "max_age": 50,
                "min_hits": 3,
                "iou_threshold": 0.3
            },
            "alert_config": {
                "service_time_threshold": 1800.0,
                "dwell_time_threshold": 300.0,
                "alert_cooldown": 120.0
            }
        },
        
        "basic_counting_tracking": {
            "usecase": "basic_counting_tracking",
            "category": "general",
            "confidence_threshold": 0.5,
            "target_categories": ["person", "car", "bicycle"],
            "enable_tracking": True,
            "tracking_method": "kalman",
            "max_age": 30,
            "min_hits": 3,
            "enable_unique_counting": True,
            "zones": {
                "entrance": [[0, 0], [200, 0], [200, 100], [0, 100]],
                "main_area": [[200, 0], [800, 0], [800, 400], [200, 400]],
                "exit": [[800, 0], [1000, 0], [1000, 100], [800, 100]]
            },
            "count_thresholds": {
                "person": 20,
                "car": 10,
                "all": 30
            },
            "zone_thresholds": {
                "entrance": 5,
                "main_area": 25,
                "exit": 5
            },
            "alert_cooldown": 60.0
        }
    }


# Helper functions for common zone patterns
def create_retail_store_zones(
    store_width: float = 1000,
    store_height: float = 600,
    entrance_width: float = 200,
    checkout_width: float = 300
) -> Dict[str, List[List[float]]]:
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
    return {
        "entrance": create_zone_from_bbox(0, 0, entrance_width, store_height),
        "shopping_area": create_zone_from_bbox(
            entrance_width, 0, 
            store_width - entrance_width - checkout_width, 
            store_height
        ),
        "checkout": create_zone_from_bbox(
            store_width - checkout_width, 0, 
            checkout_width, store_height
        )
    }


def create_office_zones(
    office_width: float = 800,
    office_height: float = 600,
    reception_height: float = 150
) -> Dict[str, List[List[float]]]:
    """
    Create typical office zone layout.
    
    Args:
        office_width: Total office width
        office_height: Total office height
        reception_height: Height of reception area
        
    Returns:
        Dict[str, List[List[float]]]: Dictionary of zone_name -> polygon
    """
    return {
        "reception": create_zone_from_bbox(0, 0, office_width, reception_height),
        "waiting_area": create_zone_from_bbox(0, reception_height, office_width // 3, office_height - reception_height),
        "work_area": create_zone_from_bbox(office_width // 3, reception_height, 2 * office_width // 3, office_height - reception_height)
    } 