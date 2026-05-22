"""
Use case implementations for post-processing.

This module contains all available use case processors for different
post-processing scenarios.
"""

from ..face_reg.face_recognition import (
    FaceRecognitionEmbeddingConfig,
    FaceRecognitionEmbeddingUseCase,
)
from .abandoned_object_detection import (
    AbandonedObjectConfig,
    AbandonedObjectDetectionUseCase,
)
from .advanced_customer_service import AdvancedCustomerServiceUseCase
from .age_detection import AgeDetectionConfig, AgeDetectionUseCase
from .age_gender_detection import AgeGenderConfig, AgeGenderUseCase
from .animal_detection import AnimalDetectionConfig, AnimalDetectionUseCase
from .anti_spoofing_detection import (
    AntiSpoofingDetectionConfig,
    AntiSpoofingDetectionUseCase,
)
from .area_utilization import AreaUtilizationConfig, AreaUtilizationUseCase
from .assembly_line_detection import AssemblyLineConfig, AssemblyLineUseCase
from .banana_defect_detection import BananaMonitoringConfig, BananaMonitoringUseCase
from .basic_counting_tracking import BasicCountingTrackingUseCase

# Put all IMAGE based usecases here
from .blood_cancer_detection_img import (
    BloodCancerDetectionConfig,
    BloodCancerDetectionUseCase,
)
from .bottle_defect_detection import (
    BottleDefectDetectionConfig,
    BottleDefectDetectionUseCase,
)
from .burglary_detection import BurglaryDetectionConfig, BurglaryDetectionUseCase
from .car_damage_detection import CarDamageConfig, CarDamageDetectionUseCase
from .car_part_segmentation import CarPartSegmentationConfig, CarPartSegmentationUseCase
from .cardiomegaly_classification import CardiomegalyConfig, CardiomegalyUseCase
from .cell_microscopy_segmentation import CellMicroscopyConfig, CellMicroscopyUseCase
from .chicken_pose_detection import (
    ChickenPoseDetectionConfig,
    ChickenPoseDetectionUseCase,
)
from .child_monitoring import ChildMonitoringConfig, ChildMonitoringUseCase
from .claude_people_counting_usecase import (
    ClaudePeopleCountingUsecaseConfig,
    ClaudePeopleCountingUsecaseUseCase,
)
from .color_detection import ColorDetectionConfig, ColorDetectionUseCase
from .concrete_crack_detection import ConcreteCrackConfig, ConcreteCrackUseCase
from .crop_weed_detection import CropWeedDetectionConfig, CropWeedDetectionUseCase
from .crowd_density_heatmaps import (
    CrowdDensityHeatMapsConfig,
    CrowdDensityHeatMapsUseCase,
)
from .crowdflow import CrowdflowConfig, CrowdflowUseCase
from .customer_service import CustomerServiceConfig, CustomerServiceUseCase
from .defect_detection_products import BottleDefectConfig, BottleDefectUseCase
from .distracted_driver_detection import DistractedDriverConfig, DistractedDriverUseCase
from .drone_traffic_monitoring import (
    DroneTrafficMonitoringUsecase,
    VehiclePeopleDroneMonitoringConfig,
)

# from .face_recognition import FaceRecognitionConfig, FaceRecognitionUseCase
from .drowsy_driver_detection import DrowsyDriverUseCase
from .dwell_detection import DwellConfig, DwellUseCase
from .emergency_vehicle_detection import EmergencyVehicleConfig, EmergencyVehicleUseCase
from .face_covering_detection_pose import (
    FaceCoveringDetectionPoseConfig,
    FaceCoveringDetectionPoseUseCase,
)
from .face_emotion import FaceEmotionConfig, FaceEmotionUseCase
from .fall_detection import FallDetectionConfig, FallDetectionUseCase
from .fashion_detection import FashionDetectionConfig, FashionDetectionUseCase
from .fence_climbing_detection import (
    FenceClimbingDetectionConfig,
    FenceClimbingDetectionUseCase,
)
from .fence_climbing_detection_pose import (
    FenceClimbingPoseGatedDetectionConfig,
    FenceClimbingPoseGatedDetectionUseCase,
)
from .fence_climbing_with_zone import (
    FenceClimbingWithZoneConfig,
    FenceClimbingWithZoneUseCase,
)
from .field_mapping import FieldMappingConfig, FieldMappingUseCase
from .fire_detection import FireSmokeConfig, FireSmokeUseCase
from .flare_analysis import FlareAnalysisConfig, FlareAnalysisUseCase
from .flower_segmentation import FlowerConfig, FlowerUseCase
from .footfall import FootFallConfig, FootFallUseCase
from .gas_leak_detection import GasLeakDetectionConfig, GasLeakDetectionUseCase
from .gender_detection import GenderDetectionConfig, GenderDetectionUseCase
from .gloves_boots_detection import (
    GlovesBootsDetectionConfig,
    GlovesBootsDetectionUseCase,
)
from .hazard_zone_entry import HazardZoneEntryConfig, HazardZoneEntryUseCase
from .heatmaps import HeatMapsConfig, HeatMapsUseCase
from .Histopathological_Cancer_Detection_img import (
    HistopathologicalCancerDetectionConfig,
    HistopathologicalCancerDetectionUseCase,
)
from .human_activity_recognition import HumanActivityConfig, HumanActivityUseCase
from .intrusion_detection import IntrusionConfig, IntrusionUseCase
from .landslide_detection import LandslideDetectionConfig, LandslideDetectionUseCase
from .leaf import LeafConfig, LeafUseCase
from .leaf_disease import LeafDiseaseDetectionConfig, LeafDiseaseDetectionUseCase
from .leak_detection import LeakDetectionConfig, LeakDetectionUseCase
from .license_plate_detection import LicensePlateConfig, LicensePlateUseCase
from .license_plate_monitoring import (
    LicensePlateMonitorConfig,
    LicensePlateMonitorUseCase,
)
from .liquid_leak_detection import LiquidLeakDetectionConfig, LiquidLeakDetectionUseCase
from .litter_monitoring import LitterDetectionConfig, LitterDetectionUseCase
from .loitering_detection import LoiteringConfig, LoiteringUseCase
from .mask_detection import MaskDetectionConfig, MaskDetectionUseCase
from .mask_type_detection import MaskTypeDetectionConfig, MaskTypeDetectionUseCase
from .natural_disaster import NaturalDisasterConfig, NaturalDisasterUseCase
from .overcrowding_detection import (
    OvercrowdingDetectionConfig,
    OvercrowdingDetectionUseCase,
)
from .package_detection import PackageDetectionConfig, PackageDetectionUseCase
from .parking import ParkingConfig, ParkingUseCase
from .parking_lot_analytics import ParkingLotAnalyticsConfig, ParkingLotAnalyticsUseCase
from .parking_space_detection import ParkingSpaceConfig, ParkingSpaceUseCase
from .pcb_defect_detection import PCBDefectConfig, PCBDefectUseCase
from .pedestrian_detection import PedestrianDetectionConfig, PedestrianDetectionUseCase
from .people_counting import PeopleCountingConfig, PeopleCountingUseCase
from .people_counting_in_zone import (
    PeopleCountingInZoneConfig,
    PeopleCountingInZoneUseCase,
)
from .people_tracking import PeopleTrackingConfig, PeopleTrackingUseCase
from .phone_screen_defect_detection import (
    PhoneScreenDefectDetectionConfig,
    PhoneScreenDefectDetectionUseCase,
)
from .pipe_corrosion_detection import (
    PipeCorrosionDetectionConfig,
    PipeCorrosionDetectionUseCase,
)
from .pipe_gas_leak_detection import (
    PipeGasLeakDetectionConfig,
    PipeGasLeakDetectionUseCase,
)
from .pipeline_detection import PipelineDetectionConfig, PipelineDetectionUseCase
from .plaque_segmentation_img import PlaqueSegmentationConfig, PlaqueSegmentationUseCase
from .pothole_detection import PotholeDetectionConfig, PotholeDetectionUseCase
from .pothole_segmentation import PotholeConfig, PotholeSegmentationUseCase
from .ppe_compliance import PPEComplianceConfig, PPEComplianceUseCase
from .price_tag_detection import PriceTagConfig, PriceTagUseCase
from .proximity_detection import ProximityConfig, ProximityUseCase
from .road_lane_detection import LaneDetectionConfig, LaneDetectionUseCase
from .road_traffic_density import RoadTrafficConfig, RoadTrafficUseCase
from .road_view_segmentation import (
    RoadViewSegmentationConfig,
    RoadViewSegmentationUseCase,
)
from .running_detection import RunningDetectionConfig, RunningDetectionUseCase
from .shelf_inventory_detection import ShelfInventoryConfig, ShelfInventoryUseCase
from .shoplifting_detection import (
    ShopliftingDetectionConfig,
    ShopliftingDetectionUseCase,
)
from .shopping_cart_analysis import ShoppingCartConfig, ShoppingCartUseCase
from .skin_cancer_classification_img import (
    SkinCancerClassificationConfig,
    SkinCancerClassificationUseCase,
)
from .smoker_detection import SmokerDetectionConfig, SmokerDetectionUseCase
from .solar_panel import SolarPanelConfig, SolarPanelUseCase
from .stopped_vehicle_monitoring import (
    StoppedVehicleMonitoringConfig,
    StoppedVehicleMonitoringUseCase,
)
from .suspicious_activity_detection import SusActivityConfig, SusActivityUseCase
from .tailgating_detection import TailgatingConfig, TailgatingDetectionUseCase
from .theft_detection import TheftDetectionConfig, TheftDetectionUseCase
from .traffic_sign_monitoring import (
    TrafficSignMonitoringConfig,
    TrafficSignMonitoringUseCase,
)
from .underground_pipeline_defect_detection import (
    UndergroundPipelineDefectConfig,
    UndergroundPipelineDefectUseCase,
)
from .underwater_pollution_detection import (
    UnderwaterPlasticConfig,
    UnderwaterPlasticUseCase,
)
from .vegetable_detection import VegetableDetectionConfig, VegetableDetectionUseCase
from .vehicle_color_detection import (
    VehicleColorDetectionConfig,
    VehicleColorDetectionUseCase,
)
from .vehicle_monitoring import VehicleMonitoringConfig, VehicleMonitoringUseCase
from .vehicle_monitoring_drone_view import (
    VehicleMonitoringDroneViewConfig,
    VehicleMonitoringDroneViewUseCase,
)
from .vehicle_monitoring_parking_lot import (
    VehicleMonitoringParkingLotConfig,
    VehicleMonitoringParkingLotUseCase,
)
from .vehicle_monitoring_wrong_way import (
    VehicleMonitoringWrongWayConfig,
    VehicleMonitoringWrongWayUseCase,
)
from .warehouse_object_segmentation import WarehouseObjectConfig, WarehouseObjectUseCase
from .waterbody_segmentation import WaterBodyConfig, WaterBodyUseCase
from .weapon_detection import WeaponDetectionConfig, WeaponDetectionUseCase
from .weld_defect_detection import WeldDefectConfig, WeldDefectUseCase
from .wildlife_monitoring import WildLifeMonitoringConfig, WildLifeMonitoringUseCase
from .windmill_maintenance import WindmillMaintenanceConfig, WindmillMaintenanceUseCase
from .wound_segmentation import WoundConfig, WoundSegmentationUseCase

AdvancedCustomerServiceConfig = CustomerServiceConfig

__all__ = [
    "FaceRecognitionEmbeddingUseCase",
    "FaceRecognitionEmbeddingConfig",
    "VehiclePeopleDroneMonitoringConfig",
    "DroneTrafficMonitoringUsecase",
    "PeopleCountingUseCase",
    "ClaudePeopleCountingUsecaseUseCase",
    "IntrusionUseCase",
    "ProximityUseCase",
    "CustomerServiceUseCase",
    "AdvancedCustomerServiceUseCase",
    "BasicCountingTrackingUseCase",
    "LicensePlateUseCase",
    "ColorDetectionUseCase",
    "PPEComplianceUseCase",
    "BananaMonitoringUseCase",
    "WoundSegmentationUseCase",
    "FieldMappingUseCase",
    "LeafDiseaseDetectionUseCase",
    "VehicleMonitoringUseCase",
    "ShopliftingDetectionUseCase",
    "ParkingUseCase",
    "ParkingSpaceUseCase",
    "FireSmokeUseCase",
    "MaskDetectionUseCase",
    "MaskTypeDetectionUseCase",
    "FlareAnalysisUseCase",
    "LeafUseCase",
    "PotholeDetectionUseCase",
    "PotholeSegmentationUseCase",
    "CarDamageDetectionUseCase",
    "FaceEmotionUseCase",
    "FaceCoveringDetectionPoseUseCase",
    "UnderwaterPlasticUseCase",
    "PedestrianDetectionUseCase",
    "PipelineDetectionUseCase",
    "AgeDetectionUseCase",
    "WeldDefectUseCase",
    "PriceTagUseCase",
    "WeaponDetectionUseCase",
    "TheftDetectionUseCase",
    "TrafficSignMonitoringUseCase",
    "DistractedDriverUseCase",
    "EmergencyVehicleUseCase",
    "SolarPanelUseCase",
    "ChickenPoseDetectionUseCase",
    "CropWeedDetectionUseCase",
    "ChildMonitoringUseCase",
    "GenderDetectionUseCase",
    "ConcreteCrackUseCase",
    "FashionDetectionUseCase",
    "WarehouseObjectUseCase",
    "ShoppingCartUseCase",
    "BottleDefectUseCase",
    "AssemblyLineUseCase",
    "AntiSpoofingDetectionUseCase",
    "ShelfInventoryUseCase",
    "CarPartSegmentationUseCase",
    "LaneDetectionUseCase",
    "WindmillMaintenanceUseCase",
    "FlowerUseCase",
    "SmokerDetectionUseCase",
    "RoadTrafficUseCase",
    "RoadViewSegmentationUseCase",
    # 'FaceRecognitionUseCase',
    "DrowsyDriverUseCase",
    "WaterBodyUseCase",
    "LitterDetectionUseCase",
    "AbandonedObjectDetectionUseCase",
    "LeakDetectionUseCase",
    "HumanActivityUseCase",
    "GasLeakDetectionUseCase",
    "LicensePlateMonitorUseCase",
    "DwellUseCase",
    "AgeGenderUseCase",
    "PeopleTrackingUseCase",
    "WildLifeMonitoringUseCase",
    "PCBDefectUseCase",
    "UndergroundPipelineDefectUseCase",
    "SusActivityUseCase",
    "NaturalDisasterUseCase",
    "FootFallUseCase",
    "VehicleMonitoringParkingLotUseCase",
    "VehicleMonitoringDroneViewUseCase",
    "ParkingLotAnalyticsUseCase",
    "VehicleMonitoringWrongWayUseCase",
    "CrowdflowUseCase",
    "StoppedVehicleMonitoringUseCase",
    "AreaUtilizationUseCase",
    "HeatMapsUseCase",
    "CrowdDensityHeatMapsUseCase",
    "LoiteringUseCase",
    "HazardZoneEntryUseCase",
    "FenceClimbingDetectionUseCase",
    "FenceClimbingPoseGatedDetectionUseCase",
    "FenceClimbingWithZoneUseCase",
    "TailgatingDetectionUseCase",
    "VehicleColorDetectionUseCase",
    "VegetableDetectionUseCase",
    "FallDetectionUseCase",
    "RunningDetectionUseCase",
    "LiquidLeakDetectionUseCase",
    "PipeGasLeakDetectionUseCase",
    "PeopleCountingInZoneUseCase",
    "PipeCorrosionDetectionUseCase",
    "OvercrowdingDetectionUseCase",
    "AnimalDetectionUseCase",
    "GlovesBootsDetectionUseCase",
    "BurglaryDetectionUseCase",
    "LandslideDetectionUseCase",
    "BottleDefectDetectionUseCase",
    "PhoneScreenDefectDetectionUseCase",
    "PackageDetectionUseCase",
    # Put all IMAGE based usecases here
    "BloodCancerDetectionUseCase",
    "SkinCancerClassificationUseCase",
    "PlaqueSegmentationUseCase",
    "CardiomegalyUseCase",
    "HistopathologicalCancerDetectionUseCase",
    "CellMicroscopyUseCase",
    "PeopleCountingConfig",
    "ClaudePeopleCountingUsecaseConfig",
    "IntrusionConfig",
    "ProximityConfig",
    "ParkingSpaceConfig",
    "CustomerServiceConfig",
    "AdvancedCustomerServiceConfig",
    "PPEComplianceConfig",
    "LicensePlateConfig",
    "PotholeDetectionConfig",
    "PotholeConfig",
    "ColorDetectionConfig",
    "LeafDiseaseDetectionConfig",
    "CarDamageConfig",
    "CarDamageConfig",
    "VehicleMonitoringConfig",
    "ShopliftingDetectionConfig",
    "MaskDetectionConfig",
    "MaskTypeDetectionConfig",
    "PipelineDetectionConfig",
    "ParkingConfig",
    "FireSmokeConfig",
    "LeafConfig",
    "FlareAnalysisConfig",
    "FaceEmotionConfig",
    "FaceCoveringDetectionPoseConfig",
    "UnderwaterPlasticConfig",
    "FieldMappingConfig",
    "WoundConfig",
    "PedestrianDetectionConfig",
    "ChickenPoseDetectionConfig",
    "AgeDetectionConfig",
    "BananaMonitoringConfig",
    "WeldDefectConfig",
    "PriceTagConfig",
    "DistractedDriverConfig",
    "EmergencyVehicleConfig",
    "TheftDetectionConfig",
    "TrafficSignMonitoringConfig",
    "SolarPanelConfig",
    "CropWeedDetectionConfig",
    "ChildMonitoringConfig",
    "GenderDetectionConfig",
    "WeaponDetectionConfig",
    "ConcreteCrackConfig",
    "FashionDetectionConfig",
    "WarehouseObjectConfig",
    "ShoppingCartConfig",
    "BottleDefectConfig",
    "AssemblyLineConfig",
    "AntiSpoofingDetectionConfig",
    "ShelfInventoryConfig",
    "CarPartSegmentationConfig",
    "LaneDetectionConfig",
    "WindmillMaintenanceConfig",
    "FlowerConfig",
    "SmokerDetectionConfig",
    "RoadTrafficConfig",
    "RoadViewSegmentationConfig",
    # 'FaceRecognitionConfig',
    "DrowsyDriverUseCase",
    "WaterBodyConfig",
    "LitterDetectionConfig",
    "AbandonedObjectConfig",
    "DwellConfig",
    "AgeGenderConfig",
    "PeopleTrackingConfig",
    "UndergroundPipelineDefectConfig",
    "AreaUtilizationConfig",
    "LoiteringConfig",
    "TailgatingConfig",
    "LiquidLeakDetectionConfig",
    "LeakDetectionConfig",
    "HumanActivityConfig",
    "GasLeakDetectionConfig",
    "LicensePlateMonitorConfig",
    "WildLifeMonitoringConfig",
    "PCBDefectConfig",
    "SusActivityConfig",
    "NaturalDisasterConfig",
    "FootFallConfig",
    "VehicleMonitoringParkingLotConfig",
    "VehicleMonitoringDroneViewConfig",
    "ParkingLotAnalyticsConfig",
    "VehicleMonitoringWrongWayConfig",
    "CrowdflowConfig",
    "StoppedVehicleMonitoringConfig",
    "HeatMapsConfig",
    "CrowdDensityHeatMapsConfig",
    "HazardZoneEntryConfig",
    "FenceClimbingDetectionConfig",
    "FenceClimbingPoseGatedDetectionConfig",
    "FenceClimbingWithZoneConfig",
    "VehicleColorDetectionConfig",
    "VegetableDetectionConfig",
    "FallDetectionConfig",
    "RunningDetectionConfig",
    "PipeGasLeakDetectionConfig",
    "PeopleCountingInZoneConfig",
    "PipeCorrosionDetectionConfig",
    "OvercrowdingDetectionConfig",
    "AnimalDetectionConfig",
    "GlovesBootsDetectionConfig",
    "BurglaryDetectionConfig",
    "LandslideDetectionConfig",
    "BottleDefectDetectionConfig",
    "PhoneScreenDefectDetectionConfig",
    "PackageDetectionConfig",
    # Put all IMAGE based usecase CONFIGS here
    "BloodCancerDetectionConfig",
    "SkinCancerClassificationConfig",
    "PlaqueSegmentationConfig",
    "CardiomegalyConfig",
    "HistopathologicalCancerDetectionConfig",
    "CellMicroscopyConfig",
]
