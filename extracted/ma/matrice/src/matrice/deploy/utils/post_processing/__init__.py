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
    ProximityConfig,
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
from .usecases.pothole_segmentation import PotholeConfig
from .usecases.wound_segmentation import WoundConfig, WoundSegmentationUseCase
from .usecases.face_emotion import FaceEmotionConfig
from .usecases.pipeline_detection import PipelineDetectionUseCase
from .usecases.parking_space_detection import ParkingSpaceConfig
from .usecases.underwater_pollution_detection import UnderwaterPlasticConfig
from .usecases.pedestrian_detection import PedestrianDetectionConfig
from .usecases.age_detection import AgeDetectionConfig
from .usecases.mask_detection import MaskDetectionConfig
from .usecases.pipeline_detection import PipelineDetectionConfig
from .usecases.chicken_pose_detection import ChickenPoseDetectionConfig
from .usecases.field_mapping import FieldMappingConfig, FieldMappingUseCase
from .usecases.leaf_disease import LeafDiseaseDetectionConfig, LeafDiseaseDetectionUseCase
from .usecases.parking import ParkingConfig
from .usecases.abandoned_object_detection import AbandonedObjectConfig


from .usecases.weld_defect_detection import WeldDefectConfig
from .usecases.weapon_detection import WeaponDetectionConfig

from .usecases.car_damage_detection import CarDamageConfig
from .usecases.price_tag_detection import PriceTagConfig
from .usecases.banana_defect_detection import BananaMonitoringConfig
from .usecases.distracted_driver_detection import DistractedDriverConfig
from .usecases.emergency_vehicle_detection import EmergencyVehicleConfig
from .usecases.solar_panel import SolarPanelConfig
from .usecases.theft_detection import TheftDetectionConfig
from .usecases.traffic_sign_monitoring import TrafficSignMonitoringConfig
from .usecases.crop_weed_detection import CropWeedDetectionConfig
from .usecases.child_monitoring import ChildMonitoringConfig
from .usecases.gender_detection import GenderDetectionConfig
from .usecases.concrete_crack_detection import ConcreteCrackConfig
from .usecases.fashion_detection import FashionDetectionConfig, FashionDetectionUseCase
from .usecases.shelf_inventory_detection import ShelfInventoryConfig
from .usecases.road_lane_detection import LaneDetectionConfig

from .usecases.warehouse_object_segmentation import WarehouseObjectConfig
from .usecases.shopping_cart_analysis import ShoppingCartConfig
from .usecases.anti_spoofing_detection import AntiSpoofingDetectionConfig

from .usecases.shoplifting_detection import ShopliftingDetectionConfig, ShopliftingDetectionUseCase
from .usecases.defect_detection_products import BottleDefectUseCase, BottleDefectConfig
from .usecases.assembly_line_detection import AssemblyLineUseCase, AssemblyLineConfig
from .usecases.car_part_segmentation import CarPartSegmentationUseCase, CarPartSegmentationConfig
from .usecases.windmill_maintenance import WindmillMaintenanceUseCase, WindmillMaintenanceConfig
from .usecases.flower_segmentation import FlowerUseCase, FlowerConfig
from .usecases.leaf import LeafConfig, LeafUseCase
from .usecases.litter_monitoring import LitterDetectionUseCase,LitterDetectionConfig
from .usecases.human_activity_recognition import HumanActivityUseCase, HumanActivityConfig
from .usecases.gas_leak_detection import GasLeakDetectionConfig, GasLeakDetectionUseCase

#Put all IMAGE based usecases here
from .usecases.blood_cancer_detection_img import BloodCancerDetectionConfig, BloodCancerDetectionUseCase
from .usecases.skin_cancer_classification_img import SkinCancerClassificationConfig, SkinCancerClassificationUseCase
from .usecases.plaque_segmentation_img import PlaqueSegmentationConfig, PlaqueSegmentationUseCase
from .usecases.smoker_detection import SmokerDetectionUseCase, SmokerDetectionConfig
from .usecases.Histopathological_Cancer_Detection_img import HistopathologicalCancerDetectionConfig, HistopathologicalCancerDetectionUseCase

# Use case implementations
from .usecases import (
    PeopleCountingUseCase,
    CustomerServiceUseCase,
    ProximityUseCase,
    AdvancedCustomerServiceUseCase,
    BasicCountingTrackingUseCase,
    LicensePlateUseCase,
    ColorDetectionUseCase,
    PPEComplianceUseCase,
    CarDamageDetectionUseCase,
    VehicleMonitoringUseCase,
    FireSmokeUseCase,
    MaskDetectionUseCase,
    ParkingSpaceUseCase,
    FlareAnalysisUseCase,
    PotholeSegmentationUseCase,
    ParkingUseCase,
    FaceEmotionUseCase,
    UnderwaterPlasticUseCase,
    PedestrianDetectionUseCase,
    LeafUseCase,
    WoundSegmentationUseCase,
    AgeDetectionUseCase,
    BananaMonitoringUseCase,
    WeldDefectUseCase,
    PriceTagUseCase,
    DistractedDriverUseCase,
    EmergencyVehicleUseCase,
    SolarPanelUseCase,
    ChickenPoseDetectionUseCase,
    LeafDiseaseDetectionUseCase,
    TheftDetectionUseCase,
    TrafficSignMonitoringUseCase,
    CropWeedDetectionUseCase,
    ChildMonitoringUseCase,
    GenderDetectionUseCase,
    WeaponDetectionUseCase,
    FashionDetectionUseCase,
    ConcreteCrackUseCase,
    WarehouseObjectUseCase,
    ShoppingCartUseCase,
    BottleDefectUseCase,
    AssemblyLineUseCase,
    FieldMappingUseCase,
    AntiSpoofingDetectionUseCase,
    ShelfInventoryUseCase,
    LaneDetectionUseCase,
    WindmillMaintenanceUseCase,
    CarPartSegmentationUseCase,
    FlowerUseCase,
    SmokerDetectionUseCase,
    LitterDetectionUseCase,
    AbandonedObjectDetectionUseCase,

    HumanActivityUseCase,

    #Put all IMAGE based usecases here
    BloodCancerDetectionUseCase,
    SkinCancerClassificationUseCase,
    PlaqueSegmentationUseCase,
    HistopathologicalCancerDetectionUseCase,

)

# Register use cases automatically
_people_counting = PeopleCountingUseCase()
_customer_service = CustomerServiceUseCase()
_proximity_detection = ProximityUseCase()
_advanced_customer_service = AdvancedCustomerServiceUseCase()
_basic_counting_tracking = BasicCountingTrackingUseCase()
_license_plate = LicensePlateUseCase()
_color_detection = ColorDetectionUseCase()
_ppe_compliance = PPEComplianceUseCase()
_vehicle_monitoring = VehicleMonitoringUseCase()
_fire_detection = FireSmokeUseCase()
_flare_analysis = FlareAnalysisUseCase()
_pothole_segmentation = PotholeSegmentationUseCase()
_face_emotion = FaceEmotionUseCase()
_parking_space_detection = ParkingSpaceUseCase()
_underwater_pollution_detection = UnderwaterPlasticUseCase()
_pedestrian_detection = PedestrianDetectionUseCase()
_age_detection = AgeDetectionUseCase()
_mask_detection = MaskDetectionUseCase()
_pipeline_detection = PipelineDetectionUseCase()
_banana_defect_detection = BananaMonitoringUseCase()
_chicken_pose_detection = ChickenPoseDetectionUseCase()
_theft_detection = TheftDetectionUseCase()
_traffic_sign_monitoring = TrafficSignMonitoringUseCase()
_shelf_inventory = ShelfInventoryUseCase()
_lane_detection = LaneDetectionUseCase()

_weld_defect_detection = WeldDefectUseCase()
_pricetag_detection = PriceTagUseCase()
_car_damage = CarDamageDetectionUseCase()
_distracted_driver = DistractedDriverUseCase()
_emergency_vehicle_detection = EmergencyVehicleUseCase()
_solar_panel = SolarPanelUseCase()
_crop_weed_detection = CropWeedDetectionUseCase()
_child_monitoring = ChildMonitoringUseCase()
_gender_detection = GenderDetectionUseCase()
_weapon_tracking = WeaponDetectionUseCase()
_concrete_crack_detection = ConcreteCrackUseCase()
_fashion_detection = FashionDetectionUseCase()

_warehouse_object_segmentation = WarehouseObjectUseCase()
_shopping_cart_analysis = ShoppingCartUseCase()
_anti_spoofing_detection = AntiSpoofingDetectionUseCase()
_parking_det = ParkingUseCase()

_shoplifting_detection = ShopliftingDetectionUseCase()
_defect_detection_products = BottleDefectUseCase()
_assembly_line_detection = AssemblyLineUseCase()
_car_part_segmentation = CarPartSegmentationUseCase()

_windmill_maintenance = WindmillMaintenanceUseCase()

_field_mapping = FieldMappingUseCase()
_wound_segmentation = WoundSegmentationUseCase()
_leaf_disease = LeafDiseaseDetectionUseCase()
_flower_segmentation = FlowerUseCase()
_leaf_det = LeafUseCase()
_smoker_detection = SmokerDetectionUseCase()
_litter_detection = LitterDetectionUseCase()
_abandoned_object_detection = AbandonedObjectDetectionUseCase()
_human_activity_recognition = HumanActivityUseCase()
_gas_leak_detection = GasLeakDetectionUseCase()


#Put all IMAGE based usecases here
_blood_cancer_detection = BloodCancerDetectionUseCase()
_skin_cancer_classification = SkinCancerClassificationUseCase()
_plaque_segmentation = PlaqueSegmentationUseCase()
_histopathological_cancer_detection = HistopathologicalCancerDetectionUseCase()

registry.register_use_case(_abandoned_object_detection.category, _abandoned_object_detection.name, AbandonedObjectDetectionUseCase)
registry.register_use_case(_litter_detection.category, _litter_detection.name, LitterDetectionUseCase)
registry.register_use_case(_people_counting.category, _people_counting.name, PeopleCountingUseCase)
registry.register_use_case(_proximity_detection.category, _proximity_detection.name, ProximityUseCase)
registry.register_use_case(_customer_service.category, _customer_service.name, CustomerServiceUseCase)
registry.register_use_case(_advanced_customer_service.category, _advanced_customer_service.name, AdvancedCustomerServiceUseCase)
registry.register_use_case(_basic_counting_tracking.category, _basic_counting_tracking.name, BasicCountingTrackingUseCase)
registry.register_use_case(_license_plate.category, _license_plate.name, LicensePlateUseCase)
registry.register_use_case(_color_detection.category, _color_detection.name, ColorDetectionUseCase)
registry.register_use_case(_ppe_compliance.category, _ppe_compliance.name, PPEComplianceUseCase)
registry.register_use_case(_vehicle_monitoring.category,_vehicle_monitoring.name,VehicleMonitoringUseCase)
registry.register_use_case(_fire_detection.category,_fire_detection.name,FireSmokeUseCase)
registry.register_use_case(_flare_analysis.category,_flare_analysis.name,FlareAnalysisUseCase)
registry.register_use_case(_pothole_segmentation.category, _pothole_segmentation.name, PotholeSegmentationUseCase)
registry.register_use_case(_face_emotion.category, _face_emotion.name, FaceEmotionUseCase)
registry.register_use_case(_parking_space_detection.category, _parking_space_detection.name, ParkingSpaceUseCase )
registry.register_use_case(_underwater_pollution_detection.category, _underwater_pollution_detection.name, UnderwaterPlasticUseCase)
registry.register_use_case(_pedestrian_detection.category, _pedestrian_detection.name, PedestrianDetectionUseCase)
registry.register_use_case(_age_detection.category, _age_detection.name, AgeDetectionUseCase)
registry.register_use_case(_pricetag_detection.category, _pricetag_detection.name, PriceTagUseCase)
registry.register_use_case(_weld_defect_detection.category, _weld_defect_detection.name, WeldDefectUseCase  )
registry.register_use_case(_mask_detection.category, _mask_detection.name, MaskDetectionUseCase)
registry.register_use_case(_pipeline_detection.category, _pipeline_detection.name, PipelineDetectionUseCase)
registry.register_use_case(_banana_defect_detection.category, _banana_defect_detection.name, BananaMonitoringUseCase)
registry.register_use_case(_chicken_pose_detection.category, _chicken_pose_detection.name, ChickenPoseDetectionUseCase)
registry.register_use_case(_theft_detection.category, _theft_detection.name, TheftDetectionUseCase)
registry.register_use_case(_traffic_sign_monitoring.category, _traffic_sign_monitoring.name, TrafficSignMonitoringUseCase)
registry.register_use_case(_gender_detection.category, _gender_detection.name, GenderDetectionUseCase)
registry.register_use_case(_anti_spoofing_detection.category, _anti_spoofing_detection.name, AntiSpoofingDetectionUseCase)
registry.register_use_case(_shelf_inventory.category, _shelf_inventory.name, ShelfInventoryUseCase)
registry.register_use_case(_lane_detection.category, _lane_detection.name, LaneDetectionUseCase)

registry.register_use_case(_car_damage.category, _car_damage.name, CarDamageDetectionUseCase)
registry.register_use_case(_distracted_driver.category, _distracted_driver.name, DistractedDriverUseCase)

registry.register_use_case(_emergency_vehicle_detection.category, _emergency_vehicle_detection.name, EmergencyVehicleUseCase)
registry.register_use_case(_solar_panel.category, _solar_panel.name, SolarPanelUseCase)
registry.register_use_case(_crop_weed_detection.category, _crop_weed_detection.name, CropWeedDetectionUseCase)
registry.register_use_case(_child_monitoring.category, _child_monitoring.name, ChildMonitoringUseCase)
registry.register_use_case(_weapon_tracking.category, _weapon_tracking.name, WeaponDetectionUseCase)
registry.register_use_case(_concrete_crack_detection.category, _concrete_crack_detection.name, ConcreteCrackUseCase)
registry.register_use_case(_fashion_detection.category, _fashion_detection.name, FashionDetectionUseCase)

registry.register_use_case(_warehouse_object_segmentation.category, _warehouse_object_segmentation.name, WarehouseObjectUseCase)
registry.register_use_case(_shopping_cart_analysis.category, _shopping_cart_analysis.name, ShoppingCartUseCase)


registry.register_use_case(_shoplifting_detection.category, _shoplifting_detection.name, ShopliftingDetectionUseCase)
registry.register_use_case(_defect_detection_products.category, _defect_detection_products.name, BottleDefectUseCase)
registry.register_use_case(_assembly_line_detection.category, _assembly_line_detection.name, AssemblyLineUseCase)
registry.register_use_case(_car_part_segmentation.category, _car_part_segmentation.name, CarPartSegmentationUseCase)

registry.register_use_case(_windmill_maintenance.category, _windmill_maintenance.name, WindmillMaintenanceUseCase)

registry.register_use_case(_field_mapping.category, _field_mapping.name, FieldMappingUseCase)
registry.register_use_case(_wound_segmentation.category, _wound_segmentation.name,WoundSegmentationUseCase)
registry.register_use_case(_leaf_disease.category, _leaf_disease.name, LeafDiseaseDetectionUseCase)
registry.register_use_case(_flower_segmentation.category, _flower_segmentation.name, FlowerUseCase)
registry.register_use_case(_parking_det.category, _parking_det.name, ParkingUseCase)
registry.register_use_case(_leaf_det.category, _leaf_det.name, LeafUseCase)
registry.register_use_case(_smoker_detection.category, _smoker_detection.name, SmokerDetectionUseCase)
registry.register_use_case(_human_activity_recognition.category, _human_activity_recognition.name, HumanActivityUseCase)
registry.register_use_case(_gas_leak_detection.category, _gas_leak_detection.name, GasLeakDetectionUseCase)

#Put all IMAGE based usecases here
registry.register_use_case(_blood_cancer_detection.category, _blood_cancer_detection.name, BloodCancerDetectionUseCase)
registry.register_use_case(_skin_cancer_classification.category, _skin_cancer_classification.name, SkinCancerClassificationUseCase)
registry.register_use_case(_plaque_segmentation.category, _plaque_segmentation.name, PlaqueSegmentationUseCase)
registry.register_use_case(_histopathological_cancer_detection.category, _histopathological_cancer_detection.name, HistopathologicalCancerDetectionUseCase)

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
    create_office_zones,

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
    'ProximityConfig', 
    'CustomerServiceConfig',
    'ColorDetectionConfig',
    'LicensePlateConfig',
    'MaskDetectionConfig',
    'ShopliftingDetectionConfig',
    'LeafConfig',
    'CarDamageConfig',
    'LeafDiseaseDetectionConfig',
    'WoundConfig',
    'FieldMappingConfig',
    'ParkingConfig',
    'ParkingSpaceConfig',
    'PotholeConfig',
    'VehicleMonitoringConfig',
    'ZoneConfig',
    'TrackingConfig',
    'AlertConfig',
    'ConfigManager',
    'config_manager',
    'ConfigValidationError',
    'FireSmokeConfig',
    'FlareAnalysisConfig',
    'FaceEmotionConfig',
    'UnderwaterPlasticConfig',
    'PedestrianDetectionConfig',
    'AgeDetectionConfig',
    'WeldDefectConfig',
    'PriceTagConfig',
    'BananaMonitoringConfig',
    'DistractedDriverConfig',
    'EmergencyVehicleConfig',
    'SolarPanelConfig',
    'ChickenPoseDetectionConfig',
    'TheftDetectionConfig',
    'TrafficSignMonitoringConfig',
    'CropWeedDetectionConfig',
    'ChildMonitoringConfig',
    'GenderDetectionConfig',
    'WeaponDetectionConfig',
    'ConcreteCrackConfig',
    'FashionDetectionConfig',
    'WarehouseObjectConfig',
    'ShoppingCartConfig',
    'BottleDefectConfig',
    'AssemblyLineConfig',
    'AntiSpoofingDetectionConfig',
    'ShelfInventoryConfig',
    'CarPartSegmentationConfig',
    'LaneDetectionConfig',
    'WindmillMaintenanceConfig',
    'FlowerConfig',
    'SmokerDetectionConfig',
    'LitterDetectionConfig',
    'AbandonedObjectConfig',
    'GasLeakDetectionConfig',
    'HumanActivityConfig',

    #Put all IMAGE based usecase CONFIGS here
    'BloodCancerDetectionConfig',
    'SkinCancerClassificationConfig',
    'PlaqueSegmentationConfig',
    'HistopathologicalCancerDetectionConfig',

    # Use case classes
    'PeopleCountingUseCase',
    'CustomerServiceUseCase',
    'ProximityUseCase',
    'AdvancedCustomerServiceUseCase',
    'BasicCountingTrackingUseCase',
    'LicensePlateUseCase',
    'ColorDetectionUseCase',
    'PPEComplianceUseCase',
    'PotholeSegmentationUseCase',
    'WoundSegmentationUseCase',
    'MaskDetectionUseCase',
    'VehicleMonitoringUseCase',
    'FireSmokeUseCase',
    'CarDamageDetectionUseCase',
    'LeafUseCase',
    'ParkingUseCase',
    'ParkingSpaceUseCase',
    'FlareAnalysisUseCase',
    'FieldMappingUseCase',
    'FaceEmotionUseCase',
    'UnderwaterPlasticUseCase',
    'PedestrianDetectionUseCase',
    'AgeDetectionUseCase',
    'ShopliftingDetectionUseCase',
    'WeldDefectUseCase',
    'BananaMonitoringUseCase',
    'LeafDiseaseDetectionUseCase',
    'PriceTagUseCase',
    'DistractedDriverUseCase',
    'EmergencyVehicleUseCase',
    'SolarPanelUseCase',
    'ChickenPoseDetectionUseCase',
    'TheftDetectionUseCase',
    'TrafficSignMonitoringUseCase',
    'WeaponDetectionUseCase',
    'ShelfInventoryUseCase',

    'CropWeedDetectionUseCase',
    'ChildMonitoringUseCase',
    'GenderDetectionUseCase',
    'ConcreteCrackUseCase',
    'FashionDetectionUseCase',
    'WarehouseObjectUseCase',
    'ShoppingCartUseCase',
    'BottleDefectUseCase',
    'AssemblyLineUseCase',
    'AntiSpoofingDetectionUseCase',
    'CarPartSegmentationUseCase',
    'LaneDetectionUseCase',
    'WindmillMaintenanceUseCase',
    'FlowerUseCase',
    'SmokerDetectionUseCase',
    'LitterDetectionUseCase',
    'AbandonedObjectDetectionUseCase',
    'HumanActivityUseCase',
    'GasLeakDetectionUseCase',

    #Put all IMAGE based usecases here
    'BloodCancerDetectionUseCase',
    'SkinCancerClassificationUseCase',
    'PlaqueSegmentationUseCase',
    'HistopathologicalCancerDetectionUseCase',
    
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
    'create_intrusion_detection_config',
    'create_proximity_detection_config',
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
