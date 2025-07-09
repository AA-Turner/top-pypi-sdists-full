"""
Post-processing utilities for Matrice SDK.

This module provides a unified, clean interface for post-processing model outputs
with support for various use cases like people counting, customer service analysis,
and more.

Key Features:
- Unified PostProcessor class for all processing needs
- Built-in use case processors for common scenarios
- Flexible configuration management with JSON/YAML support
- Comprehensive validation and error handling
- Processing statistics and insights
- Zone-based analysis and tracking

Quick Start:
    from matrice.deploy.utils.post_processing import PostProcessor
    
    # Simple processing
    processor = PostProcessor()
    result = processor.process_simple(
        raw_results, "people_counting",
        confidence_threshold=0.5
    )
    
    # With configuration file
    result = processor.process_from_file(raw_results, "config.json")
    
    # Get available use cases
    usecases = processor.list_available_usecases()
"""

# Core components - main processing interface
from .processor import (
    PostProcessor,
    process_simple,
    create_config_template,
    list_available_usecases,
    validate_config
)

# Core data structures and base classes
from .core.base import (
    ProcessingResult,
    ProcessingContext,
    ProcessingStatus,
    ResultFormat,
    BaseProcessor,
    BaseUseCase,
    ProcessorRegistry,
    registry
)

# Configuration system
from .core.config import (
    BaseConfig,
    PeopleCountingConfig,
    CustomerServiceConfig,
    ZoneConfig,
    TrackingConfig,
    AlertConfig,
    ConfigManager,
    config_manager,
    ConfigValidationError
)

# Additional config imports
from .usecases.color_detection import ColorDetectionConfig
from .usecases.fire_detection import FireSmokeUseCase, FireSmokeConfig
from .usecases.license_plate_detection import LicensePlateConfig

# Use case implementations
from .usecases import (
    PeopleCountingUseCase,
    CustomerServiceUseCase,
    AdvancedCustomerServiceUseCase,
    BasicCountingTrackingUseCase,
    LicensePlateUseCase,
    ColorDetectionUseCase,
    PPEComplianceUseCase,
    VehicleMonitoringUseCase,
    FireSmokeUseCase,
    FlareAnalysisUseCase
)

# Register use cases automatically
_people_counting = PeopleCountingUseCase()
_customer_service = CustomerServiceUseCase()
_advanced_customer_service = AdvancedCustomerServiceUseCase()
_basic_counting_tracking = BasicCountingTrackingUseCase()
_license_plate = LicensePlateUseCase()
_color_detection = ColorDetectionUseCase()
_ppe_compliance = PPEComplianceUseCase()
_vehicle_monitoring = VehicleMonitoringUseCase()
_fire_detection = FireSmokeUseCase()
_flare_analysis = FlareAnalysisUseCase()
registry.register_use_case(_people_counting.category, _people_counting.name, PeopleCountingUseCase)
registry.register_use_case(_customer_service.category, _customer_service.name, CustomerServiceUseCase)
registry.register_use_case(_advanced_customer_service.category, _advanced_customer_service.name, AdvancedCustomerServiceUseCase)
registry.register_use_case(_basic_counting_tracking.category, _basic_counting_tracking.name, BasicCountingTrackingUseCase)
registry.register_use_case(_license_plate.category, _license_plate.name, LicensePlateUseCase)
registry.register_use_case(_color_detection.category, _color_detection.name, ColorDetectionUseCase)
registry.register_use_case(_ppe_compliance.category, _ppe_compliance.name, PPEComplianceUseCase)
registry.register_use_case(_vehicle_monitoring.category,_vehicle_monitoring.name,VehicleMonitoringUseCase)
registry.register_use_case(_fire_detection.category,_fire_detection.name,FireSmokeUseCase)
registry.register_use_case(_flare_analysis.category,_flare_analysis.name,FlareAnalysisUseCase)
# Utility functions - organized by category
from .utils import (  # noqa: E402
    # Geometry utilities
    point_in_polygon,
    get_bbox_center,
    calculate_distance,
    calculate_bbox_overlap,
    calculate_iou,
    get_bbox_area,
    normalize_bbox,
    denormalize_bbox,
    line_segments_intersect,
    
    # Format utilities
    convert_to_coco_format,
    convert_to_yolo_format,
    convert_to_tracking_format,
    convert_detection_to_tracking_format,
    convert_tracking_to_detection_format,
    match_results_structure,
    
    # Filter utilities
    filter_by_confidence,
    filter_by_categories,
    calculate_bbox_fingerprint,
    clean_expired_tracks,
    remove_duplicate_detections,
    apply_category_mapping,
    filter_by_area,
    
    # Counting utilities
    count_objects_by_category,
    count_objects_in_zones,
    count_unique_tracks,
    calculate_counting_summary,
    
    # Tracking utilities
    track_objects_in_zone,
    detect_line_crossings,
    analyze_track_movements,
    filter_tracks_by_duration,
    
    # New utilities
    create_people_counting_config,
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

# Convenience functions for backward compatibility and simple usage
def process_usecase(raw_results, usecase: str, category: str = "general", **config):
    """
    Process raw results with a specific use case.
    
    Args:
        raw_results: Raw model output
        usecase: Use case name ('people_counting', 'customer_service', etc.)
        category: Use case category (default: 'general')
        **config: Configuration parameters
        
    Returns:
        ProcessingResult: Processing result with insights
        
    Example:
        result = process_usecase(
            raw_results, "people_counting",
            confidence_threshold=0.5,
            zones={"entrance": [[0, 0], [100, 0], [100, 100], [0, 100]]}
        )
    """
    return process_simple(raw_results, usecase, category, **config)


def get_config_template(usecase: str) -> dict:
    """
    Get configuration template for a use case.
    
    Args:
        usecase: Use case name
        
    Returns:
        dict: Configuration template
    """
    return create_config_template(usecase)


def get_available_usecases() -> dict:
    """
    Get all available use cases organized by category.
    
    Returns:
        dict: Available use cases by category
    """
    return list_available_usecases()


def create_processor() -> PostProcessor:
    """
    Create a new PostProcessor instance.
    
    Returns:
        PostProcessor: New processor instance
    """
    return PostProcessor()



# Main exports for external use
__all__ = [
    # Main processor class
    'PostProcessor',
    
    # Core data structures
    'ProcessingResult',
    'ProcessingContext',
    'ProcessingStatus',
    'ResultFormat',
    
    # Configuration classes
    'BaseConfig',
    'PeopleCountingConfig', 
    'CustomerServiceConfig',
    'ColorDetectionConfig',
    'LicensePlateConfig',
    'VehicleMonitoringConfig'
    'ZoneConfig',
    'TrackingConfig',
    'AlertConfig',
    'ConfigManager',
    'config_manager',
    'ConfigValidationError',
    'FireSmokeConfig',
    'FlareAnalysisConfig'
    
    # Use case classes
    'PeopleCountingUseCase',
    'CustomerServiceUseCase',
    'AdvancedCustomerServiceUseCase',
    'BasicCountingTrackingUseCase',
    'LicensePlateUseCase',
    'ColorDetectionUseCase',
    'PPEComplianceUseCase',
    'VehicleMonitoringUseCase',
    'FireSmokeUseCase',
    'FlareAnalysisUseCase'
    
    # Base classes for extension
    'BaseProcessor',
    'BaseUseCase',
    'ProcessorRegistry',
    'registry',
    
    # Convenience functions
    'process_simple',
    'process_usecase',
    'create_config_template',
    'get_config_template',
    'list_available_usecases',
    'get_available_usecases',
    'validate_config',
    'create_processor',
    
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
    
    # New utilities
    'create_people_counting_config',
    'create_customer_service_config',
    'create_advanced_customer_service_config',
    'create_basic_counting_tracking_config',
    'create_zone_from_bbox',
    'create_polygon_zone',
    'create_config_from_template',
    'validate_zone_polygon',
    'get_use_case_examples',
    'create_retail_store_zones',
    'create_office_zones',
    
    # Functions
    'list_available_usecases',
    'create_config_from_template'
]
