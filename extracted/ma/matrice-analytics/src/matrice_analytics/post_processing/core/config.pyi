"""Auto-generated stub for module: config."""
from typing import Any, Dict, List, Optional, Set, Union

from ..Trackers.config import SUPPORTED_TRACKING_METHODS
from ..Trackers.factory import normalize_tracking_method
from ..face_reg.face_recognition import FaceRecognitionEmbeddingConfig
from ..face_reg.face_recognition import FaceRecognitionEmbeddingConfig
from ..face_reg.face_recognition import FaceRecognitionEmbeddingConfig
from ..usecases.Histopathological_Cancer_Detection_img import HistopathologicalCancerDetectionConfig
from ..usecases.Histopathological_Cancer_Detection_img import HistopathologicalCancerDetectionConfig
from ..usecases.Histopathological_Cancer_Detection_img import HistopathologicalCancerDetectionConfig
from ..usecases.abandoned_object_detection import AbandonedObjectConfig
from ..usecases.abandoned_object_detection import AbandonedObjectConfig
from ..usecases.abandoned_object_detection import AbandonedObjectConfig
from ..usecases.accident_detection import AccidentDetectionConfig
from ..usecases.accident_detection import AccidentDetectionConfig
from ..usecases.accident_detection import AccidentDetectionConfig
from ..usecases.age_detection import AgeDetectionConfig
from ..usecases.age_detection import AgeDetectionConfig
from ..usecases.age_detection import AgeDetectionConfig
from ..usecases.age_gender_detection import AgeGenderConfig
from ..usecases.age_gender_detection import AgeGenderConfig
from ..usecases.age_gender_detection import AgeGenderConfig
from ..usecases.animal_detection import AnimalDetectionConfig
from ..usecases.animal_detection import AnimalDetectionConfig
from ..usecases.animal_detection import AnimalDetectionConfig
from ..usecases.anti_spoofing_detection import AntiSpoofingDetectionConfig
from ..usecases.anti_spoofing_detection import AntiSpoofingDetectionConfig
from ..usecases.anti_spoofing_detection import AntiSpoofingDetectionConfig
from ..usecases.area_utilization import AreaUtilizationConfig
from ..usecases.area_utilization import AreaUtilizationConfig
from ..usecases.area_utilization import AreaUtilizationConfig
from ..usecases.assembly_line_detection import AssemblyLineConfig
from ..usecases.assembly_line_detection import AssemblyLineConfig
from ..usecases.assembly_line_detection import AssemblyLineConfig
from ..usecases.banana_defect_detection import BananaMonitoringConfig
from ..usecases.banana_defect_detection import BananaMonitoringConfig
from ..usecases.banana_defect_detection import BananaMonitoringConfig
from ..usecases.basic_counting_tracking import BasicCountingTrackingConfig
from ..usecases.basic_counting_tracking import BasicCountingTrackingConfig
from ..usecases.blood_cancer_detection_img import BloodCancerDetectionConfig
from ..usecases.blood_cancer_detection_img import BloodCancerDetectionConfig
from ..usecases.blood_cancer_detection_img import BloodCancerDetectionConfig
from ..usecases.bottle_defect_detection import BottleDefectDetectionConfig
from ..usecases.bottle_defect_detection import BottleDefectDetectionConfig
from ..usecases.bottle_defect_detection import BottleDefectDetectionConfig
from ..usecases.burglary_detection import BurglaryDetectionConfig
from ..usecases.burglary_detection import BurglaryDetectionConfig
from ..usecases.burglary_detection import BurglaryDetectionConfig
from ..usecases.car_damage_detection import CarDamageConfig
from ..usecases.car_damage_detection import CarDamageConfig
from ..usecases.car_damage_detection import CarDamageConfig
from ..usecases.car_part_segmentation import CarPartSegmentationConfig
from ..usecases.car_part_segmentation import CarPartSegmentationConfig
from ..usecases.car_part_segmentation import CarPartSegmentationConfig
from ..usecases.cardiomegaly_classification import CardiomegalyConfig
from ..usecases.cardiomegaly_classification import CardiomegalyConfig
from ..usecases.cardiomegaly_classification import CardiomegalyConfig
from ..usecases.cell_microscopy_segmentation import CellMicroscopyConfig
from ..usecases.cell_microscopy_segmentation import CellMicroscopyConfig
from ..usecases.cell_microscopy_segmentation import CellMicroscopyConfig
from ..usecases.chicken_pose_detection import ChickenPoseDetectionConfig
from ..usecases.chicken_pose_detection import ChickenPoseDetectionConfig
from ..usecases.chicken_pose_detection import ChickenPoseDetectionConfig
from ..usecases.child_monitoring import ChildMonitoringConfig
from ..usecases.child_monitoring import ChildMonitoringConfig
from ..usecases.child_monitoring import ChildMonitoringConfig
from ..usecases.claude_people_counting_usecase import ClaudePeopleCountingUsecaseConfig
from ..usecases.claude_people_counting_usecase import ClaudePeopleCountingUsecaseConfig
from ..usecases.claude_people_counting_usecase import ClaudePeopleCountingUsecaseConfig
from ..usecases.color_detection import ColorDetectionConfig
from ..usecases.color_detection import ColorDetectionConfig
from ..usecases.color_detection import ColorDetectionConfig
from ..usecases.color_detection import ColorDetectionConfig
from ..usecases.concrete_crack_detection import ConcreteCrackConfig
from ..usecases.concrete_crack_detection import ConcreteCrackConfig
from ..usecases.concrete_crack_detection import ConcreteCrackConfig
from ..usecases.crop_weed_detection import CropWeedDetectionConfig
from ..usecases.crop_weed_detection import CropWeedDetectionConfig
from ..usecases.crop_weed_detection import CropWeedDetectionConfig
from ..usecases.crowd_density_heatmaps import CrowdDensityHeatMapsConfig
from ..usecases.crowd_density_heatmaps import CrowdDensityHeatMapsConfig
from ..usecases.crowd_density_heatmaps import CrowdDensityHeatMapsConfig
from ..usecases.crowdflow import CrowdflowConfig
from ..usecases.crowdflow import CrowdflowConfig
from ..usecases.crowdflow import CrowdflowConfig
from ..usecases.deep_oc_sort import DeepOCSortConfig
from ..usecases.deep_oc_sort import DeepOCSortConfig
from ..usecases.deep_oc_sort import DeepOCSortConfig
from ..usecases.defect_detection_products import BottleDefectConfig
from ..usecases.defect_detection_products import BottleDefectConfig
from ..usecases.defect_detection_products import BottleDefectConfig
from ..usecases.distracted_driver_detection import DistractedDriverConfig
from ..usecases.distracted_driver_detection import DistractedDriverConfig
from ..usecases.distracted_driver_detection import DistractedDriverConfig
from ..usecases.drone_detection import DroneDetectionConfig
from ..usecases.drone_detection import DroneDetectionConfig
from ..usecases.drone_detection import DroneDetectionConfig
from ..usecases.drone_traffic_monitoring import VehiclePeopleDroneMonitoringConfig
from ..usecases.drone_traffic_monitoring import VehiclePeopleDroneMonitoringConfig
from ..usecases.drone_traffic_monitoring import VehiclePeopleDroneMonitoringConfig
from ..usecases.drowsy_driver_detection import DrowsyDriverConfig
from ..usecases.drowsy_driver_detection import DrowsyDriverConfig
from ..usecases.drowsy_driver_detection import DrowsyDriverConfig
from ..usecases.dwell_detection import DwellConfig
from ..usecases.dwell_detection import DwellConfig
from ..usecases.dwell_detection import DwellConfig
from ..usecases.emergency_vehicle_detection import EmergencyVehicleConfig
from ..usecases.emergency_vehicle_detection import EmergencyVehicleConfig
from ..usecases.emergency_vehicle_detection import EmergencyVehicleConfig
from ..usecases.face_covering_detection_pose import FaceCoveringDetectionPoseConfig
from ..usecases.face_covering_detection_pose import FaceCoveringDetectionPoseConfig
from ..usecases.face_covering_detection_pose import FaceCoveringDetectionPoseConfig
from ..usecases.face_emotion import FaceEmotionConfig
from ..usecases.face_emotion import FaceEmotionConfig
from ..usecases.face_emotion import FaceEmotionConfig
from ..usecases.fall_detection import FallDetectionConfig
from ..usecases.fall_detection import FallDetectionConfig
from ..usecases.fall_detection import FallDetectionConfig
from ..usecases.fashion_detection import FashionDetectionConfig
from ..usecases.fashion_detection import FashionDetectionConfig
from ..usecases.fashion_detection import FashionDetectionConfig
from ..usecases.fence_climbing_detection_pose import FenceClimbingPoseGatedDetectionConfig
from ..usecases.fence_climbing_detection_pose import FenceClimbingPoseGatedDetectionConfig
from ..usecases.fence_climbing_detection_pose import FenceClimbingPoseGatedDetectionConfig
from ..usecases.fence_climbing_with_zone import FenceClimbingWithZoneConfig
from ..usecases.fence_climbing_with_zone import FenceClimbingWithZoneConfig
from ..usecases.fence_climbing_with_zone import FenceClimbingWithZoneConfig
from ..usecases.field_mapping import FieldMappingConfig
from ..usecases.field_mapping import FieldMappingConfig
from ..usecases.field_mapping import FieldMappingConfig
from ..usecases.fire_detection import FireSmokeConfig
from ..usecases.fire_detection import FireSmokeConfig
from ..usecases.fire_detection import FireSmokeConfig
from ..usecases.flare_analysis import FlareAnalysisConfig
from ..usecases.flare_analysis import FlareAnalysisConfig
from ..usecases.flare_analysis import FlareAnalysisConfig
from ..usecases.flood_detection import FloodDetectionConfig
from ..usecases.flood_detection import FloodDetectionConfig
from ..usecases.flood_detection import FloodDetectionConfig
from ..usecases.flower_segmentation import FlowerConfig
from ..usecases.flower_segmentation import FlowerConfig
from ..usecases.flower_segmentation import FlowerConfig
from ..usecases.footfall import FootFallConfig
from ..usecases.footfall import FootFallConfig
from ..usecases.footfall import FootFallConfig
from ..usecases.fr_access_control import FaceRecognitionAccessControlConfig
from ..usecases.fr_access_control import FaceRecognitionAccessControlConfig
from ..usecases.fr_surveillance import FaceRecognitionSurveillanceConfig
from ..usecases.fr_surveillance import FaceRecognitionSurveillanceConfig
from ..usecases.gas_leak_detection import GasLeakDetectionConfig
from ..usecases.gas_leak_detection import GasLeakDetectionConfig
from ..usecases.gas_leak_detection import GasLeakDetectionConfig
from ..usecases.gender_detection import GenderDetectionConfig
from ..usecases.gender_detection import GenderDetectionConfig
from ..usecases.gender_detection import GenderDetectionConfig
from ..usecases.gloves_boots_detection import GlovesBootsDetectionConfig
from ..usecases.gloves_boots_detection import GlovesBootsDetectionConfig
from ..usecases.gloves_boots_detection import GlovesBootsDetectionConfig
from ..usecases.hazard_zone_entry import HazardZoneEntryConfig
from ..usecases.hazard_zone_entry import HazardZoneEntryConfig
from ..usecases.hazard_zone_entry import HazardZoneEntryConfig
from ..usecases.heatmaps import HeatMapsConfig
from ..usecases.heatmaps import HeatMapsConfig
from ..usecases.heatmaps import HeatMapsConfig
from ..usecases.human_activity_recognition import HumanActivityConfig
from ..usecases.human_activity_recognition import HumanActivityConfig
from ..usecases.human_activity_recognition import HumanActivityConfig
from ..usecases.illegal_parking_detection import IllegalParkingConfig
from ..usecases.illegal_parking_detection import IllegalParkingConfig
from ..usecases.illegal_parking_detection import IllegalParkingConfig
from ..usecases.landslide_detection import LandslideDetectionConfig
from ..usecases.landslide_detection import LandslideDetectionConfig
from ..usecases.landslide_detection import LandslideDetectionConfig
from ..usecases.leaf_disease import LeafDiseaseDetectionConfig
from ..usecases.leaf_disease import LeafDiseaseDetectionConfig
from ..usecases.leaf_disease import LeafDiseaseDetectionConfig
from ..usecases.leak_detection import LeakDetectionConfig
from ..usecases.leak_detection import LeakDetectionConfig
from ..usecases.leak_detection import LeakDetectionConfig
from ..usecases.license_plate_detection import LicensePlateConfig
from ..usecases.license_plate_detection import LicensePlateConfig
from ..usecases.license_plate_detection import LicensePlateConfig
from ..usecases.license_plate_monitoring import LicensePlateMonitorConfig
from ..usecases.license_plate_monitoring import LicensePlateMonitorConfig
from ..usecases.license_plate_monitoring import LicensePlateMonitorConfig
from ..usecases.liquid_leak_detection import LiquidLeakDetectionConfig
from ..usecases.liquid_leak_detection import LiquidLeakDetectionConfig
from ..usecases.liquid_leak_detection import LiquidLeakDetectionConfig
from ..usecases.litter_monitoring import LitterDetectionConfig
from ..usecases.litter_monitoring import LitterDetectionConfig
from ..usecases.litter_monitoring import LitterDetectionConfig
from ..usecases.loitering_detection import LoiteringConfig
from ..usecases.loitering_detection import LoiteringConfig
from ..usecases.loitering_detection import LoiteringConfig
from ..usecases.lpr_access_control import LicensePlateAccessControlConfig
from ..usecases.lpr_access_control import LicensePlateAccessControlConfig
from ..usecases.lpr_surveillance import LicensePlateSurveillanceConfig
from ..usecases.lpr_surveillance import LicensePlateSurveillanceConfig
from ..usecases.mask_detection import MaskDetectionConfig
from ..usecases.mask_detection import MaskDetectionConfig
from ..usecases.mask_detection import MaskDetectionConfig
from ..usecases.mask_type_detection import MaskTypeDetectionConfig
from ..usecases.mask_type_detection import MaskTypeDetectionConfig
from ..usecases.mask_type_detection import MaskTypeDetectionConfig
from ..usecases.natural_disaster import NaturalDisasterConfig
from ..usecases.natural_disaster import NaturalDisasterConfig
from ..usecases.natural_disaster import NaturalDisasterConfig
from ..usecases.overcrowding_detection import OvercrowdingDetectionConfig
from ..usecases.overcrowding_detection import OvercrowdingDetectionConfig
from ..usecases.overcrowding_detection import OvercrowdingDetectionConfig
from ..usecases.package_detection import PackageDetectionConfig
from ..usecases.package_detection import PackageDetectionConfig
from ..usecases.package_detection import PackageDetectionConfig
from ..usecases.parking_lot_analytics import ParkingLotAnalyticsConfig
from ..usecases.parking_lot_analytics import ParkingLotAnalyticsConfig
from ..usecases.parking_lot_analytics import ParkingLotAnalyticsConfig
from ..usecases.parking_space_detection import ParkingSpaceConfig
from ..usecases.parking_space_detection import ParkingSpaceConfig
from ..usecases.parking_space_detection import ParkingSpaceConfig
from ..usecases.pcb_defect_detection import PCBDefectConfig
from ..usecases.pcb_defect_detection import PCBDefectConfig
from ..usecases.pcb_defect_detection import PCBDefectConfig
from ..usecases.pedestrian_detection import PedestrianDetectionConfig
from ..usecases.pedestrian_detection import PedestrianDetectionConfig
from ..usecases.pedestrian_detection import PedestrianDetectionConfig
from ..usecases.people_counting_in_zone import PeopleCountingInZoneConfig
from ..usecases.people_counting_in_zone import PeopleCountingInZoneConfig
from ..usecases.phone_screen_defect_detection import PhoneScreenDefectDetectionConfig
from ..usecases.phone_screen_defect_detection import PhoneScreenDefectDetectionConfig
from ..usecases.phone_screen_defect_detection import PhoneScreenDefectDetectionConfig
from ..usecases.pipe_corrosion_detection import PipeCorrosionDetectionConfig
from ..usecases.pipe_corrosion_detection import PipeCorrosionDetectionConfig
from ..usecases.pipe_corrosion_detection import PipeCorrosionDetectionConfig
from ..usecases.pipe_gas_leak_detection import PipeGasLeakDetectionConfig
from ..usecases.pipe_gas_leak_detection import PipeGasLeakDetectionConfig
from ..usecases.pipe_gas_leak_detection import PipeGasLeakDetectionConfig
from ..usecases.pipeline_detection import PipelineDetectionConfig
from ..usecases.pipeline_detection import PipelineDetectionConfig
from ..usecases.pipeline_detection import PipelineDetectionConfig
from ..usecases.plaque_segmentation_img import PlaqueSegmentationConfig
from ..usecases.plaque_segmentation_img import PlaqueSegmentationConfig
from ..usecases.plaque_segmentation_img import PlaqueSegmentationConfig
from ..usecases.pothole_detection import PotholeDetectionConfig
from ..usecases.pothole_detection import PotholeDetectionConfig
from ..usecases.pothole_detection import PotholeDetectionConfig
from ..usecases.pothole_segmentation import PotholeConfig
from ..usecases.pothole_segmentation import PotholeConfig
from ..usecases.pothole_segmentation import PotholeConfig
from ..usecases.ppe_compliance import PPEComplianceConfig
from ..usecases.ppe_compliance import PPEComplianceConfig
from ..usecases.price_tag_detection import PriceTagConfig
from ..usecases.price_tag_detection import PriceTagConfig
from ..usecases.price_tag_detection import PriceTagConfig
from ..usecases.road_lane_detection import LaneDetectionConfig
from ..usecases.road_lane_detection import LaneDetectionConfig
from ..usecases.road_lane_detection import LaneDetectionConfig
from ..usecases.road_traffic_density import RoadTrafficConfig
from ..usecases.road_traffic_density import RoadTrafficConfig
from ..usecases.road_traffic_density import RoadTrafficConfig
from ..usecases.road_view_segmentation import RoadViewSegmentationConfig
from ..usecases.road_view_segmentation import RoadViewSegmentationConfig
from ..usecases.road_view_segmentation import RoadViewSegmentationConfig
from ..usecases.running_detection import RunningDetectionConfig
from ..usecases.running_detection import RunningDetectionConfig
from ..usecases.running_detection import RunningDetectionConfig
from ..usecases.shelf_inventory_detection import ShelfInventoryConfig
from ..usecases.shelf_inventory_detection import ShelfInventoryConfig
from ..usecases.shelf_inventory_detection import ShelfInventoryUseCase
from ..usecases.shoplifting_detection import ShopliftingDetectionConfig
from ..usecases.shoplifting_detection import ShopliftingDetectionConfig
from ..usecases.shoplifting_detection import ShopliftingDetectionConfig
from ..usecases.shopping_cart_analysis import ShoppingCartAnalysisConfig
from ..usecases.shopping_cart_analysis import ShoppingCartConfig
from ..usecases.shopping_cart_analysis import ShoppingCartConfig
from ..usecases.skin_cancer_classification_img import SkinCancerClassificationConfig
from ..usecases.skin_cancer_classification_img import SkinCancerClassificationConfig
from ..usecases.skin_cancer_classification_img import SkinCancerClassificationConfig
from ..usecases.smoker_detection import SmokerDetectionConfig
from ..usecases.smoker_detection import SmokerDetectionConfig
from ..usecases.smoker_detection import SmokerDetectionConfig
from ..usecases.solar_panel import SolarPanelConfig
from ..usecases.solar_panel import SolarPanelConfig
from ..usecases.solar_panel import SolarPanelConfig
from ..usecases.stopped_vehicle_monitoring import StoppedVehicleMonitoringConfig
from ..usecases.stopped_vehicle_monitoring import StoppedVehicleMonitoringConfig
from ..usecases.stopped_vehicle_monitoring import StoppedVehicleMonitoringConfig
from ..usecases.street_vendor_detection import StreetVendorDetectionConfig
from ..usecases.street_vendor_detection import StreetVendorDetectionConfig
from ..usecases.street_vendor_detection import StreetVendorDetectionConfig
from ..usecases.suspicious_activity_detection import SusActivityConfig
from ..usecases.suspicious_activity_detection import SusActivityConfig
from ..usecases.suspicious_activity_detection import SusActivityConfig
from ..usecases.tailgating_detection import TailgatingConfig
from ..usecases.tailgating_detection import TailgatingConfig
from ..usecases.tailgating_detection import TailgatingConfig
from ..usecases.theft_detection import TheftDetectionConfig
from ..usecases.theft_detection import TheftDetectionConfig
from ..usecases.theft_detection import TheftDetectionConfig
from ..usecases.traffic_sign_monitoring import TrafficSignMonitoringConfig
from ..usecases.traffic_sign_monitoring import TrafficSignMonitoringConfig
from ..usecases.traffic_sign_monitoring import TrafficSignMonitoringConfig
from ..usecases.unauthorized_encampment_detection import UnauthorizedEncampmentDetectionConfig
from ..usecases.unauthorized_encampment_detection import UnauthorizedEncampmentDetectionConfig
from ..usecases.unauthorized_encampment_detection import UnauthorizedEncampmentDetectionConfig
from ..usecases.underground_pipeline_defect_detection import UndergroundPipelineDefectConfig
from ..usecases.underground_pipeline_defect_detection import UndergroundPipelineDefectConfig
from ..usecases.underground_pipeline_defect_detection import UndergroundPipelineDefectConfig
from ..usecases.underwater_pollution_detection import UnderwaterPlasticConfig
from ..usecases.underwater_pollution_detection import UnderwaterPlasticConfig
from ..usecases.underwater_pollution_detection import UnderwaterPlasticConfig
from ..usecases.unwanted_animal_detection import UnwantedAnimalDetectionConfig
from ..usecases.unwanted_animal_detection import UnwantedAnimalDetectionConfig
from ..usecases.unwanted_animal_detection import UnwantedAnimalDetectionConfig
from ..usecases.vegetable_detection import VegetableDetectionConfig
from ..usecases.vegetable_detection import VegetableDetectionConfig
from ..usecases.vegetable_detection import VegetableDetectionConfig
from ..usecases.vehicle_color_detection import VehicleColorDetectionConfig
from ..usecases.vehicle_color_detection import VehicleColorDetectionConfig
from ..usecases.vehicle_color_detection import VehicleColorDetectionConfig
from ..usecases.vehicle_monitoring import VehicleMonitoringConfig
from ..usecases.vehicle_monitoring import VehicleMonitoringConfig
from ..usecases.vehicle_monitoring import VehicleMonitoringConfig
from ..usecases.vehicle_monitoring_drone_view import VehicleMonitoringDroneViewConfig
from ..usecases.vehicle_monitoring_drone_view import VehicleMonitoringDroneViewConfig
from ..usecases.vehicle_monitoring_drone_view import VehicleMonitoringDroneViewConfig
from ..usecases.vehicle_monitoring_parking_lot import VehicleMonitoringParkingLotConfig
from ..usecases.vehicle_monitoring_parking_lot import VehicleMonitoringParkingLotConfig
from ..usecases.vehicle_monitoring_parking_lot import VehicleMonitoringParkingLotConfig
from ..usecases.vehicle_monitoring_wrong_way import VehicleMonitoringWrongWayConfig
from ..usecases.vehicle_monitoring_wrong_way import VehicleMonitoringWrongWayConfig
from ..usecases.vehicle_monitoring_wrong_way import VehicleMonitoringWrongWayConfig
from ..usecases.vehicle_segmentation import VehicleSegmentationConfig
from ..usecases.vehicle_segmentation import VehicleSegmentationConfig
from ..usecases.vehicle_segmentation import VehicleSegmentationConfig
from ..usecases.vehicle_type_classification import VehicleTypeClassificationConfig
from ..usecases.vehicle_type_classification import VehicleTypeClassificationConfig
from ..usecases.vehicle_type_classification import VehicleTypeClassificationConfig
from ..usecases.violence_detection import ViolenceDetectionConfig
from ..usecases.violence_detection import ViolenceDetectionConfig
from ..usecases.violence_detection import ViolenceDetectionConfig
from ..usecases.violence_detection_testing import ViolenceDetectionTestingConfig
from ..usecases.violence_detection_testing import ViolenceDetectionTestingConfig
from ..usecases.violence_detection_testing import ViolenceDetectionTestingConfig
from ..usecases.warehouse_object_segmentation import WarehouseObjectConfig
from ..usecases.warehouse_object_segmentation import WarehouseObjectConfig
from ..usecases.warehouse_object_segmentation import WarehouseObjectConfig
from ..usecases.waterbody_segmentation import WaterBodyConfig
from ..usecases.waterbody_segmentation import WaterBodyConfig
from ..usecases.waterbody_segmentation import WaterBodyConfig
from ..usecases.weapon_detection import WeaponDetectionConfig
from ..usecases.weapon_detection import WeaponDetectionConfig
from ..usecases.weapon_detection import WeaponDetectionConfig
from ..usecases.weapon_human_detection import WeaponHumanDetectionConfig
from ..usecases.weapon_human_detection import WeaponHumanDetectionConfig
from ..usecases.weapon_human_detection import WeaponHumanDetectionConfig
from ..usecases.weld_defect_detection import WeldDefectConfig
from ..usecases.weld_defect_detection import WeldDefectConfig
from ..usecases.weld_defect_detection import WeldDefectConfig
from ..usecases.wildlife_monitoring import WildLifeMonitoringConfig
from ..usecases.wildlife_monitoring import WildLifeMonitoringConfig
from ..usecases.wildlife_monitoring import WildLifeMonitoringConfig
from ..usecases.windmill_maintenance import WindmillMaintenanceConfig
from ..usecases.windmill_maintenance import WindmillMaintenanceConfig
from ..usecases.windmill_maintenance import WindmillMaintenanceConfig
from ..usecases.wound_segmentation import WoundConfig
from ..usecases.wound_segmentation import WoundConfig
from ..usecases.wound_segmentation import WoundConfig
from .base import ConfigProtocol

# Constants
config_manager: Any
logger: Any

# Functions
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

# Classes
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

class CarServiceConfig:
    # Configuration for car service use case.

    def validate(self: Any) -> List[str]:
        """
        Validate customer service configuration.
        """
        ...

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

    def accident_detection_config_class(self: Any) -> Any: ...

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

    def create_config(self: Any, usecase: str, category: str | None = None, **kwargs: Any) -> Any:
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

    def deep_oc_sort_config_class(self: Any) -> Any: ...

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

    def drone_detection_config_class(self: Any) -> Any: ...

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

    def flood_detection_config_class(self: Any) -> Any: ...

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

    def illegal_parking_detection_config_class(self: Any) -> Any: ...

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

    def street_vendor_detection_config_class(self: Any) -> Any: ...

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

    def unauthorized_encampment_detection_config_class(self: Any) -> Any: ...

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

    def unwanted_animal_detection_config_class(self: Any) -> Any: ...

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

    def vehicle_segmentation_config_class(self: Any) -> Any: ...

    def vehicle_type_classification_config_class(self: Any) -> Any: ...

    def violence_detection_config_class(self: Any) -> Any: ...

    def violence_detection_testing_config_class(self: Any) -> Any: ...

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

    def weapon_human_detection_config_class(self: Any) -> Any:
        """
        Get weapon human detection config class to avoid circular imports.
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

class ConfigValidationError(Exception):
    # Raised when configuration validation fails.

    ...
class CustomerServiceConfig:
    # Configuration for customer service use case.
    #
    #     Shared by the ``customer_service`` and ``advanced_customer_service`` use
    #     cases. Fields are therefore ADDITIVE ONLY: changing an existing default or
    #     its semantics changes behaviour for both.

    def validate(self: Any) -> List[str]:
        """
        Validate customer service configuration.
        """
        ...

class IntrusionAdvancedTrackerConfig:
    # AdvancedTracker (BYTE-style) tuning for ``intrusion_detection``.
    #
    #     Set on ``IntrusionConfig.advanced_tracker_config`` or pass key ``advanced_tracker_config``
    #     as a nested dict when using the config factory / YAML. Values override the corresponding
    #     fields on ``TrackerConfig``; all other tracker fields keep ``TrackerConfig`` defaults.

    def to_dict(self: Any) -> Dict[str, Any]: ...

    def validate(self: Any) -> List[str]: ...

class IntrusionConfig:
    # Configuration for intrusion detection use case.

    def validate(self: Any) -> List[str]:
        """
        Validate intrusion detection configuration.
        """
        ...

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

class PeopleCountingConfig:
    # Configuration for people counting use case.

    def validate(self: Any) -> List[str]:
        """
        Validate people counting configuration.
        """
        ...

class PeopleTrackingConfig:
    # Configuration for People Tracking use case with polygon/abline counting.

    def validate(self: Any) -> List[str]:
        """
        Validate people tracking configuration.
        """
        ...

class ProximityConfig:
    # Configuration for intrusion detection use case.

    def validate(self: Any) -> List[str]:
        """
        Validate proximity detection configuration.
        """
        ...

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

