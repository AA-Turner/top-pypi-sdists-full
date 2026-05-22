"""Stub file for post_processing.core directory."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from ..face_reg.face_recognition import FaceRecognitionEmbeddingConfig
from ..usecases.Histopathological_Cancer_Detection_img import HistopathologicalCancerDetectionConfig
from ..usecases.abandoned_object_detection import AbandonedObjectConfig
from ..usecases.age_detection import AgeDetectionConfig
from ..usecases.age_gender_detection import AgeGenderConfig
from ..usecases.animal_detection import AnimalDetectionConfig
from ..usecases.anti_spoofing_detection import AntiSpoofingDetectionConfig
from ..usecases.area_utilization import AreaUtilizationConfig
from ..usecases.assembly_line_detection import AssemblyLineConfig
from ..usecases.banana_defect_detection import BananaMonitoringConfig
from ..usecases.basic_counting_tracking import BasicCountingTrackingConfig
from ..usecases.blood_cancer_detection_img import BloodCancerDetectionConfig
from ..usecases.bottle_defect_detection import BottleDefectDetectionConfig
from ..usecases.burglary_detection import BurglaryDetectionConfig
from ..usecases.car_damage_detection import CarDamageConfig
from ..usecases.car_part_segmentation import CarPartSegmentationConfig
from ..usecases.cardiomegaly_classification import CardiomegalyConfig
from ..usecases.cell_microscopy_segmentation import CellMicroscopyConfig
from ..usecases.chicken_pose_detection import ChickenPoseDetectionConfig
from ..usecases.child_monitoring import ChildMonitoringConfig
from ..usecases.claude_people_counting_usecase import ClaudePeopleCountingUsecaseConfig
from ..usecases.color_detection import ColorDetectionConfig
from ..usecases.concrete_crack_detection import ConcreteCrackConfig
from ..usecases.crop_weed_detection import CropWeedDetectionConfig
from ..usecases.crowd_density_heatmaps import CrowdDensityHeatMapsConfig
from ..usecases.crowdflow import CrowdflowConfig
from ..usecases.defect_detection_products import BottleDefectConfig
from ..usecases.distracted_driver_detection import DistractedDriverConfig
from ..usecases.drone_traffic_monitoring import VehiclePeopleDroneMonitoringConfig
from ..usecases.drowsy_driver_detection import DrowsyDriverConfig
from ..usecases.dwell_detection import DwellConfig
from ..usecases.emergency_vehicle_detection import EmergencyVehicleConfig
from ..usecases.face_covering_detection_pose import FaceCoveringDetectionPoseConfig
from ..usecases.face_emotion import FaceEmotionConfig
from ..usecases.fall_detection import FallDetectionConfig
from ..usecases.fashion_detection import FashionDetectionConfig
from ..usecases.fence_climbing_detection_pose import FenceClimbingPoseGatedDetectionConfig
from ..usecases.fence_climbing_with_zone import FenceClimbingWithZoneConfig
from ..usecases.field_mapping import FieldMappingConfig
from ..usecases.fire_detection import FireSmokeConfig
from ..usecases.flare_analysis import FlareAnalysisConfig
from ..usecases.flower_segmentation import FlowerConfig
from ..usecases.footfall import FootFallConfig
from ..usecases.gas_leak_detection import GasLeakDetectionConfig
from ..usecases.gender_detection import GenderDetectionConfig
from ..usecases.gloves_boots_detection import GlovesBootsDetectionConfig
from ..usecases.hazard_zone_entry import HazardZoneEntryConfig
from ..usecases.heatmaps import HeatMapsConfig
from ..usecases.human_activity_recognition import HumanActivityConfig
from ..usecases.landslide_detection import LandslideDetectionConfig
from ..usecases.leaf_disease import LeafDiseaseDetectionConfig
from ..usecases.leak_detection import LeakDetectionConfig
from ..usecases.license_plate_detection import LicensePlateConfig
from ..usecases.license_plate_monitoring import LicensePlateMonitorConfig
from ..usecases.liquid_leak_detection import LiquidLeakDetectionConfig
from ..usecases.litter_monitoring import LitterDetectionConfig
from ..usecases.loitering_detection import LoiteringConfig
from ..usecases.mask_detection import MaskDetectionConfig
from ..usecases.mask_type_detection import MaskTypeDetectionConfig
from ..usecases.natural_disaster import NaturalDisasterConfig
from ..usecases.overcrowding_detection import OvercrowdingDetectionConfig
from ..usecases.package_detection import PackageDetectionConfig
from ..usecases.parking_lot_analytics import ParkingLotAnalyticsConfig
from ..usecases.parking_space_detection import ParkingSpaceConfig
from ..usecases.pcb_defect_detection import PCBDefectConfig
from ..usecases.pedestrian_detection import PedestrianDetectionConfig
from ..usecases.people_counting_in_zone import PeopleCountingInZoneConfig
from ..usecases.phone_screen_defect_detection import PhoneScreenDefectDetectionConfig
from ..usecases.pipe_corrosion_detection import PipeCorrosionDetectionConfig
from ..usecases.pipe_gas_leak_detection import PipeGasLeakDetectionConfig
from ..usecases.pipeline_detection import PipelineDetectionConfig
from ..usecases.plaque_segmentation_img import PlaqueSegmentationConfig
from ..usecases.pothole_detection import PotholeDetectionConfig
from ..usecases.pothole_segmentation import PotholeConfig
from ..usecases.ppe_compliance import PPEComplianceConfig
from ..usecases.price_tag_detection import PriceTagConfig
from ..usecases.road_lane_detection import LaneDetectionConfig
from ..usecases.road_traffic_density import RoadTrafficConfig
from ..usecases.road_view_segmentation import RoadViewSegmentationConfig
from ..usecases.running_detection import RunningDetectionConfig
from ..usecases.shelf_inventory_detection import ShelfInventoryConfig
from ..usecases.shelf_inventory_detection import ShelfInventoryUseCase
from ..usecases.shoplifting_detection import ShopliftingDetectionConfig
from ..usecases.shopping_cart_analysis import ShoppingCartAnalysisConfig
from ..usecases.shopping_cart_analysis import ShoppingCartConfig
from ..usecases.skin_cancer_classification_img import SkinCancerClassificationConfig
from ..usecases.smoker_detection import SmokerDetectionConfig
from ..usecases.solar_panel import SolarPanelConfig
from ..usecases.stopped_vehicle_monitoring import StoppedVehicleMonitoringConfig
from ..usecases.suspicious_activity_detection import SusActivityConfig
from ..usecases.tailgating_detection import TailgatingConfig
from ..usecases.theft_detection import TheftDetectionConfig
from ..usecases.traffic_sign_monitoring import TrafficSignMonitoringConfig
from ..usecases.underground_pipeline_defect_detection import UndergroundPipelineDefectConfig
from ..usecases.underwater_pollution_detection import UnderwaterPlasticConfig
from ..usecases.vegetable_detection import VegetableDetectionConfig
from ..usecases.vehicle_color_detection import VehicleColorDetectionConfig
from ..usecases.vehicle_monitoring import VehicleMonitoringConfig
from ..usecases.vehicle_monitoring_drone_view import VehicleMonitoringDroneViewConfig
from ..usecases.vehicle_monitoring_parking_lot import VehicleMonitoringParkingLotConfig
from ..usecases.vehicle_monitoring_wrong_way import VehicleMonitoringWrongWayConfig
from ..usecases.warehouse_object_segmentation import WarehouseObjectConfig
from ..usecases.waterbody_segmentation import WaterBodyConfig
from ..usecases.weapon_detection import WeaponDetectionConfig
from ..usecases.weld_defect_detection import WeldDefectConfig
from ..usecases.wildlife_monitoring import WildLifeMonitoringConfig
from ..usecases.windmill_maintenance import WindmillMaintenanceConfig
from ..usecases.wound_segmentation import WoundConfig
from .base import ConfigProtocol
from .config import AlertConfig, CustomerServiceConfig, IntrusionConfig, LineConfig, PeopleCountingConfig, PeopleTrackingConfig, ProximityConfig, TrackingConfig, ZoneConfig, config_manager

# Constants
logger: Any = ...  # From base
registry: Any = ...  # From base
config_manager: Any = ...  # From config
logger: Any = ...  # From config

# Functions
# From config
def filter_config_kwargs(config_class: Any, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filter kwargs to only include parameters that are valid for the config class.
    
    Args:
        config_class: The config class to create
        kwargs: Dictionary of parameters to filter
    
    Returns:
        Dict[str, Any]: Filtered kwargs containing only valid parameters
    """
    ...

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# From config_utils
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

# Classes
# From base
class BaseProcessor:
    # Base class for all processors with standardized agg_summary generation.

    def __init__(self: Any, name: str) -> None:
        """
        Initialize processor with name.
        """
        ...

    def create_agg_summary(self: Any, frame_id: Union[str, int], incidents: Optional[List[Dict]] = None, tracking_stats: Optional[List[Dict]] = None, business_analytics: Optional[List[Dict]] = None, alerts: Optional[List[Dict]] = None, human_text: str = '') -> Dict[str, Any]:
        """
        Create standardized agg_summary structure following the expected format.
        """
        ...

    def create_agg_summary_for_frame(self: Any, frame_number: Union[int, str], incidents: List[Dict] = None, tracking_stats: List[Dict] = None, business_analytics: List[Dict] = None, alerts: List[Dict] = None, human_text: str = '') -> Dict[str, Any]:
        """
        Create agg_summary structure for a specific frame matching the expected format.
        """
        ...

    def create_alert_object(self: Any, alert_type: str, alert_id: str, incident_category: str, threshold_value: float, ascending: bool = True, settings: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a standardized alert object.
        """
        ...

    def create_business_analytics(self: Any, analysis_name: str, statistics: Dict[str, Any], human_text: str, camera_info: Optional[Dict[str, Any]] = None, alerts: Optional[List[Dict]] = None, alert_settings: Optional[List[Dict]] = None, reset_settings: Optional[List[Dict]] = None, start_time: Optional[str] = None, reset_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Create standardized business analytics object following the agg_summary format.
        """
        ...

    def create_count_object(self: Any, category: str, count: int) -> Dict[str, Any]:
        """
        Create a standardized count object for total_counts and current_counts.
        """
        ...

    def create_detection_object(self: Any, category: str, bounding_box: Dict[str, Any], _confidence: Optional[float] = None, segmentation: Optional[List] = None, track_id: Optional[Any] = None, plate_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a standardized detection object for tracking stats.
        """
        ...

    def create_error_result(self: Any, message: str, error_type: str = 'ProcessingError', usecase: str = '', category: str = '', context: Optional[Any] = None) -> Any:
        """
        Create an error result.
        """
        ...

    def create_frame_wise_agg_summary(self: Any, frame_incidents: Dict[str, List[Dict]], frame_tracking_stats: Dict[str, List[Dict]], frame_business_analytics: Dict[str, List[Dict]], frame_alerts: Dict[str, List[Dict]] = None, frame_human_text: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Create frame-wise agg_summary structure for multiple frames.
        """
        ...

    def create_incident(self: Any, incident_id: str, incident_type: str, severity_level: str, human_text: str = '', camera_info: Optional[Dict[str, Any]] = None, alerts: Optional[List[Dict]] = None, alert_settings: Optional[List[Dict]] = None, start_time: Optional[str] = None, end_time: Optional[str] = None, level_settings: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """
        Create a standardized incident object following the agg_summary format.
        """
        ...

    def create_result(self: Any, data: Any, usecase: str = '', category: str = '', context: Optional[Any] = None) -> Any:
        """
        Create a successful result.
        """
        ...

    def create_structured_business_analytics(self: Any, analysis_name: str, statistics: Dict, camera_info: Dict = None, alerts: List[Dict] = None, alert_settings: List[Dict] = None) -> Dict:
        """
        Create structured business analytics in the required format.
        """
        ...

    def create_structured_event(self: Any, event_type: str, level: str, intensity: float, application_name: str, location_info: str = None, additional_info: str = '', application_version: str = '1.0') -> Dict:
        """
        Create a structured event in the required format.
        """
        ...

    def create_structured_incident(self: Any, incident_id: str, incident_type: str, severity_level: str, start_time: str = None, end_time: str = None, camera_info: Dict = None, alerts: List[Dict] = None, alert_settings: List[Dict] = None) -> Dict:
        """
        Create a structured incident in the required format.
        """
        ...

    def create_structured_tracking_stats(self: Any, _results_data: Dict, human_text: str) -> Dict:
        """
        Create structured tracking stats in the required format.
        """
        ...

    def create_tracking_stats(self: Any, total_counts: List[Dict[str, Any]], current_counts: List[Dict[str, Any]], detections: List[Dict[str, Any]], human_text: str, camera_info: Optional[Dict[str, Any]] = None, alerts: Optional[List[Dict]] = None, alert_settings: Optional[List[Dict]] = None, reset_settings: Optional[List[Dict]] = None, start_time: Optional[str] = None, reset_time: Optional[str] = None) -> Dict[str, Any]:
        """
        Create standardized tracking stats object following the agg_summary format.
        """
        ...

    def detect_frame_structure(self: Any, data: Any) -> bool:
        """
        Detect if data has frame-based structure (multi-frame) or single frame.
        """
        ...

    def determine_event_level_and_intensity(self: Any, count: int, threshold: int = 10) -> tuple:
        """
        Determine event level and intensity based on count and threshold.
        """
        ...

    def determine_severity_level(self: Any, count: int, threshold_low: int = 3, threshold_medium: int = 7, threshold_critical: int = 15) -> str:
        """
        Determine severity level based on count and thresholds.
        """
        ...

    def extract_deployment_ids(self: Any, stream_info: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Extract app_deployment_id and application_id from stream_info.
        
                Uses a priority-based fallback chain identical to the one in
                incident_manager_utils / business_metrics_manager_utils:
        
                    stream_info root  >  input_settings  >  camera_info
        
                Each level checks snake_case and camelCase key variants.
                Returns a dict with ``app_deployment_id`` and ``application_id``
                (empty strings when not found).
        """
        ...

    def extract_frame_ids(self: Any, data: Any) -> List[str]:
        """
        Extract frame IDs from frame-based data structure.
        """
        ...

    def generate_analytics_human_text(self: Any, _analysis_name: str, statistics: Dict[str, Any], current_timestamp: str, reset_timestamp: str, alerts_summary: str = 'None') -> str:
        """
        Generate standardized human text for business analytics.
        """
        ...

    def generate_tracking_human_text(self: Any, current_counts: Dict[str, int], total_counts: Dict[str, int], current_timestamp: str, reset_timestamp: str, alerts_summary: str = 'None') -> str:
        """
        Generate standardized human text for tracking stats.
        """
        ...

    def get_camera_info_from_stream(self: Any, stream_info: Optional[Dict[str, Any]] = None, camera_info: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Extract camera info from stream_info or use provided camera_info.
        
                The returned dict always includes ``app_deployment_id`` and
                ``application_id`` extracted from *stream_info* using a
                priority-based fallback chain (root -> input_settings -> camera_info).
        """
        ...

    def get_default_camera_info(self: Any) -> Dict[str, str]:
        """
        Get default camera info structure.
        """
        ...

    def get_default_level_settings(self: Any) -> Dict[str, int]:
        """
        Get default severity level settings.
        """
        ...

    def get_default_reset_settings(self: Any) -> List[Dict[str, Any]]:
        """
        Get default reset settings.
        """
        ...

    def get_high_precision_timestamp(self: Any) -> str:
        """
        Get high precision timestamp with microsecond granularity.
        """
        ...

    def get_standard_timestamp(self: Any) -> str:
        """
        Get standard timestamp without microseconds.
        """
        ...

    def process(self: Any, _data: Any, _config: Any, _context: Optional[Any] = None) -> Any:
        """
        Process data with given configuration.
        """
        ...


# From base
class BaseUseCase:
    # Base class for all use cases.

    def __init__(self: Any, name: str, category: str) -> None:
        """
        Initialize use case with name and category.
        """
        ...

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

    def validate_config(self: Any, config: Any) -> List[str]:
        """
        Validate configuration for this use case.
        """
        ...


# From base
class ConfigProtocol:
    # Protocol for configuration objects.

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Convert to dictionary.
        """
        ...

    def validate(self: Any) -> List[str]:
        """
        Validate configuration and return list of errors.
        """
        ...


# From base
class ProcessingContext:
    # Context information for processing operations.

    def mark_completed(self: Any) -> None:
        """
        Mark processing as completed and calculate processing time, latency in ms, and fps.
        """
        ...


# From base
class ProcessingResult:
    # Standardized result container for all post-processing operations.

    def add_insight(self: Any, message: str) -> None:
        """
        Add insight message.
        """
        ...

    def add_warning(self: Any, message: str) -> None:
        """
        Add warning message.
        """
        ...

    def is_success(self: Any) -> bool:
        """
        Check if processing was successful.
        """
        ...

    def set_error(self: Any, message: str, error_type: str = 'ProcessingError', details: Optional[Dict[str, Any]] = None) -> None:
        """
        Set error information.
        """
        ...

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.
        """
        ...


# From base
class ProcessingStatus:
    # Processing status indicators.

    ERROR: str
    PARTIAL: str
    SUCCESS: str
    WARNING: str


# From base
class ProcessorProtocol:
    # Protocol for processors.

    def process(self: Any, _data: Any, _config: Any, _context: Optional[Any] = None) -> Any:
        """
        Process data with given configuration.
        """
        ...


# From base
class ProcessorRegistry:
    # Registry for processors and use cases.

    def __init__(self: Any) -> None:
        """
        Initialize registry.
        """
        ...

    def get_processor(self: Any, name: str) -> Optional[Any[Any]]:
        """
        Get processor class by name.
        """
        ...

    def get_use_case(self: Any, category: str, name: str) -> Optional[Any[Any]]:
        """
        Get use case class by category and name.
        
                Falls back to searching all categories if the exact category/name
                pair is not found (handles category mismatches like general/footfall
                when footfall is registered under retail).
        """
        ...

    def list_processors(self: Any) -> List[str]:
        """
        List all registered processors.
        """
        ...

    def list_use_cases(self: Any) -> Dict[str, List[str]]:
        """
        List all registered use cases by category.
        """
        ...

    def register_processor(self: Any, name: str, processor_class: Any[Any]) -> None:
        """
        Register a processor class.
        """
        ...

    def register_use_case(self: Any, category: str, name: str, use_case_class: Any[Any]) -> None:
        """
        Register a use case class.
        """
        ...


# From base
class ResultFormat:
    # Supported result formats.

    ACTIVITY_RECOGNITION: str
    CLASSIFICATION: str
    DETECTION: str
    FACE_RECOGNITION: str
    INSTANCE_SEGMENTATION: str
    OBJECT_TRACKING: str
    TRACKING: str
    UNKNOWN: str


# From config
class AlertConfig:
    # Configuration for alerting system.

    def get(self: Any, key: str, default: Any = None) -> Any: ...

    def items(self: Any) -> Any: ...

    def keys(self: Any) -> Any: ...

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Convert to dictionary.
        """
        ...

    def validate(self: Any) -> List[str]:
        """
        Validate alert configuration.
        """
        ...


# From config
class BaseConfig:
    # Base configuration class with common functionality and validation.

    def from_dict(cls: Any, data: Dict[str, Any]) -> 'Any':
        """
        Create config from dictionary with type conversion.
        """
        ...

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.
        """
        ...

    def validate(self: Any) -> List[str]:
        """
        Validate configuration and return list of error messages.
        """
        ...


# From config
class CarServiceConfig:
    # Configuration for car service use case.

    def validate(self: Any) -> List[str]:
        """
        Validate customer service configuration.
        """
        ...


# From config
class ConfigManager:
    # Centralized configuration management for post-processing operations.

    def __init__(self: Any) -> None:
        """
        Initialize configuration manager.
        """
        ...

    def abandoned_object_detection_config_class(self: Any) -> Any:
        """
        Get monitoring class to avoid circular imports.
        """
        ...

    def age_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def age_gender_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def animal_detection_config_class(self: Any) -> Any: ...

    def anti_spoofing_detection_config_class(self: Any) -> Any:
        """
        Get Anti-Spoofing class to avoid circular imports.
        """
        ...

    def area_utilization_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def assembly_line_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def banana_defect_detection_config_class(self: Any) -> Any:
        """
        Get Banana monitoring class to avoid circular imports.
        """
        ...

    def blood_cancer_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def bottle_defect_detection_config_class(self: Any) -> Any: ...

    def burglary_detection_config_class(self: Any) -> Any: ...

    def car_part_segmentation_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def cardiomegaly_classification_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def cell_microscopy_segmentation_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def chicken_pose_detection_config_class(self: Any) -> Any:
        """
        Get Chicken pose monitoring class to avoid circular imports.
        """
        ...

    def child_monitoring_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def claude_people_counting_usecase_config_class(self: Any) -> Any: ...

    def concrete_crack_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def create_config(self: Any, usecase: str, category: Optional[str] = None, **kwargs: Any) -> Any:
        """
        Create configuration for a specific use case.
        
        Args:
            usecase: Use case name
            category: Optional category override
            **kwargs: Configuration parameters
        
        Returns:
            BaseConfig: Created configuration
        
        Raises:
            ConfigValidationError: If configuration is invalid
        """
        ...

    def crop_weed_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def crowd_density_heatmaps_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def crowdflow_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def defect_detection_products_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def distracted_driver_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def drone_traffic_monitoring_config_class(self: Any) -> Any:
        """
        Get drone traffic monitoring class to avoid circular imports.
        """
        ...

    def drowsy_driver_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def dwell_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def emergency_vehicle_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def face_covering_detection_pose_config_class(self: Any) -> Any: ...

    def face_emotion_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def face_recognition_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def fall_detection_config_class(self: Any) -> Any: ...

    def fashion_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def fence_climbing_detection_pose_config_class(self: Any) -> Any: ...

    def fence_climbing_with_zone_config_class(self: Any) -> Any: ...

    def flare_analysis_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def flower_segmentation_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def footfall_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def gas_leak_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def gender_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def get_config_template(self: Any, usecase: str) -> Dict[str, Any]:
        """
        Get configuration template for a use case.
        """
        ...

    def gloves_boots_detection_config_class(self: Any) -> Any: ...

    def hazard_zone_entry_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def heatmaps_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def histopathological_cancer_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def human_activity_recognition_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def landslide_detection_config_class(self: Any) -> Any: ...

    def lane_detection_config_class(self: Any) -> Any:
        """
        Get road lane monitoring class to avoid circular imports.
        """
        ...

    def leak_detection_config_class(self: Any) -> Any:
        """
        Get Leak detection class to avoid circular imports.
        """
        ...

    def license_plate_monitor_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def liquid_leak_detection_config_class(self: Any) -> Any: ...

    def list_supported_usecases(self: Any) -> List[str]:
        """
        List all supported use cases.
        """
        ...

    def litter_detection_config_class(self: Any) -> Any:
        """
        Get Litter monitoring class to avoid circular imports.
        """
        ...

    def load_from_file(self: Any, file_path: Union[str, Any]) -> Any:
        """
        Load configuration from file.
        
        Args:
            file_path: Path to configuration file (JSON or YAML)
        
        Returns:
            BaseConfig: Configuration object
        
        Raises:
            ConfigValidationError: If file cannot be loaded or validation fails
        """
        ...

    def loitering_detection_config_class(self: Any) -> Any: ...

    def natural_disaster_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def overcrowding_detection_config_class(self: Any) -> Any: ...

    def package_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def parking_lot_analytics_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def pcb_defect_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def pedestrian_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def people_counting_in_zone_config_class(self: Any) -> Any: ...

    def phone_screen_defect_detection_config_class(self: Any) -> Any: ...

    def pipe_corrosion_detection_config_class(self: Any) -> Any: ...

    def pipe_gas_leak_detection_config_class(self: Any) -> Any: ...

    def plaque_segmentation_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def pothole_detection_config_class(self: Any) -> Any: ...

    def price_tag_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def register_config_class(self: Any, usecase: str, config_class: Any) -> None:
        """
        Register a configuration class for a use case.
        """
        ...

    def road_traffic_density_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def road_view_segmentation_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def running_detection_config_class(self: Any) -> Any: ...

    def save_to_file(self: Any, config: Any, file_path: Union[str, Any], fmt: str = 'json') -> None:
        """
        Save configuration to file.
        
        Args:
            config: Configuration object
            file_path: Output file path
            fmt: Output format ('json' or 'yaml')
        
        Raises:
            ConfigValidationError: If format is unsupported or saving fails
        """
        ...

    def shelf_inventory_config_class(self: Any) -> Any:
        """
        Get inventory monitoring class to avoid circular imports.
        """
        ...

    def shopping_cart_analysis_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def skin_cancer_classification_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def smoker_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def solar_panel_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def stopped_vehicle_monitoring_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def suspicious_activity_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def tailgating_detection_config_class(self: Any) -> Any: ...

    def theft_detection_config_class(self: Any) -> Any:
        """
        Get  theft detection class to avoid circular imports.
        """
        ...

    def traffic_sign_monitoring_config_class(self: Any) -> Any:
        """
        Get traffic sign monitoring class to avoid circular imports.
        """
        ...

    def underground_pipeline_defect_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def underwater_pollution_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def vegetable_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for vegetable detection use case.
        """
        ...

    def vehicle_color_detection_config_class(self: Any) -> Any: ...

    def vehicle_monitoring_config_class(self: Any) -> Any:
        """
        Get vehicle monitoring class to avoid circular imports.
        """
        ...

    def vehicle_monitoring_drone_view_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def vehicle_monitoring_parking_lot_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def vehicle_monitoring_wrong_way_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def warehouse_object_segmentation_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def waterbody_segmentation_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def weapon_tracking_config_class(self: Any) -> Any:
        """
        Get  weapon detection class to avoid circular imports.
        """
        ...

    def weld_defect_detection_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def wildlife_monitoring_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...

    def windmill_maintenance_config_class(self: Any) -> Any:
        """
        Register a configuration class for a use case.
        """
        ...


# From config
class ConfigValidationError(Exception):
    # Raised when configuration validation fails.

    ...

# From config
class CustomerServiceConfig:
    # Configuration for customer service use case.

    def validate(self: Any) -> List[str]:
        """
        Validate customer service configuration.
        """
        ...


# From config
class IntrusionAdvancedTrackerConfig:
    # AdvancedTracker (BYTE-style) tuning for ``intrusion_detection``.
    #
    #     Set on ``IntrusionConfig.advanced_tracker_config`` or pass key ``advanced_tracker_config``
    #     as a nested dict when using the config factory / YAML. Values override the corresponding
    #     fields on ``TrackerConfig``; all other tracker fields keep ``TrackerConfig`` defaults.

    def to_dict(self: Any) -> Dict[str, Any]: ...

    def validate(self: Any) -> List[str]: ...


# From config
class IntrusionConfig:
    # Configuration for intrusion detection use case.

    def validate(self: Any) -> List[str]:
        """
        Validate intrusion detection configuration.
        """
        ...


# From config
class LineConfig:
    # Configuration for line crossing detection.

    def get(self: Any, key: str, default: Any = None) -> Any: ...

    def items(self: Any) -> Any: ...

    def keys(self: Any) -> Any: ...

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Convert to dictionary.
        """
        ...

    def validate(self: Any) -> List[str]:
        """
        Validate line configuration.
        """
        ...


# From config
class PeopleCountingConfig:
    # Configuration for people counting use case.

    def validate(self: Any) -> List[str]:
        """
        Validate people counting configuration.
        """
        ...


# From config
class PeopleTrackingConfig:
    # Configuration for People Tracking use case with polygon/abline counting.

    def validate(self: Any) -> List[str]:
        """
        Validate people tracking configuration.
        """
        ...


# From config
class ProximityConfig:
    # Configuration for intrusion detection use case.

    def validate(self: Any) -> List[str]:
        """
        Validate proximity detection configuration.
        """
        ...


# From config
class TrackingConfig:
    # Configuration for tracking operations.

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Convert to dictionary.
        """
        ...

    def validate(self: Any) -> List[str]:
        """
        Validate tracking configuration.
        """
        ...


# From config
class ZoneConfig:
    # Configuration for zone-based processing.

    def get(self: Any, key: str, default: Any = None) -> Any: ...

    def items(self: Any) -> Any: ...

    def keys(self: Any) -> Any: ...

    def to_dict(self: Any) -> Dict[str, Any]:
        """
        Convert to dictionary.
        """
        ...

    def validate(self: Any) -> List[str]:
        """
        Validate zone configuration.
        """
        ...


from . import base, config, config_utils