"""
Use case implementations for post-processing.

This module contains all available use case processors for different
post-processing scenarios.
"""

from .people_counting import PeopleCountingUseCase, PeopleCountingConfig
from .intrusion_detection import IntrusionUseCase, IntrusionConfig
from .proximity_detection import ProximityUseCase, ProximityConfig
from .customer_service import CustomerServiceUseCase, CustomerServiceConfig
from .advanced_customer_service import AdvancedCustomerServiceUseCase
from .basic_counting_tracking import BasicCountingTrackingUseCase
from .license_plate_detection import LicensePlateUseCase, LicensePlateConfig
from .color_detection import ColorDetectionUseCase, ColorDetectionConfig
from .ppe_compliance import PPEComplianceUseCase, PPEComplianceConfig
from .vehicle_monitoring import VehicleMonitoringUseCase, VehicleMonitoringConfig
from .fire_detection import FireSmokeUseCase, FireSmokeConfig
from .flare_analysis import FlareAnalysisUseCase,FlareAnalysisConfig
from .pothole_segmentation import PotholeSegmentationUseCase, PotholeConfig
from .face_emotion import FaceEmotionUseCase, FaceEmotionConfig
from .parking_space_detection import ParkingSpaceConfig, ParkingSpaceUseCase
from .underwater_pollution_detection import UnderwaterPlasticUseCase, UnderwaterPlasticConfig
from .pedestrian_detection import PedestrianDetectionUseCase, PedestrianDetectionConfig
from .age_detection import AgeDetectionUseCase, AgeDetectionConfig

from .weld_defect_detection import WeldDefectConfig,WeldDefectUseCase
from .banana_defect_detection import BananaMonitoringUseCase,BananaMonitoringConfig

from .car_damage_detection import CarDamageConfig, CarDamageDetectionUseCase
from .price_tag_detection import PriceTagConfig, PriceTagUseCase
from .mask_detection import MaskDetectionConfig, MaskDetectionUseCase
from .pipeline_detection import PipelineDetectionConfig, PipelineDetectionUseCase
from .distracted_driver_detection import DistractedDriverUseCase, DistractedDriverConfig
from .emergency_vehicle_detection import EmergencyVehicleUseCase, EmergencyVehicleConfig
from .solar_panel import SolarPanelUseCase, SolarPanelConfig
from .chicken_pose_detection import ChickenPoseDetectionConfig,ChickenPoseDetectionUseCase
from .traffic_sign_monitoring import TrafficSignMonitoringConfig, TrafficSignMonitoringUseCase
from .theft_detection import TheftDetectionConfig , TheftDetectionUseCase
from .crop_weed_detection import CropWeedDetectionConfig, CropWeedDetectionUseCase
from .child_monitoring import ChildMonitoringUseCase, ChildMonitoringConfig
from .gender_detection import GenderDetectionUseCase, GenderDetectionConfig
from .weapon_detection import WeaponDetectionConfig,WeaponDetectionUseCase
from .concrete_crack_detection import ConcreteCrackUseCase, ConcreteCrackConfig
from .fashion_detection import FashionDetectionUseCase, FashionDetectionConfig

from .warehouse_object_segmentation import WarehouseObjectUseCase, WarehouseObjectConfig
from .shopping_cart_analysis import ShoppingCartUseCase, ShoppingCartConfig

from .shoplifting_detection import ShopliftingDetectionConfig, ShopliftingDetectionUseCase
from .defect_detection_products import BottleDefectUseCase, BottleDefectConfig
from .assembly_line_detection import AssemblyLineUseCase, AssemblyLineConfig
from .anti_spoofing_detection import AntiSpoofingDetectionConfig, AntiSpoofingDetectionUseCase
from .shelf_inventory_detection import ShelfInventoryUseCase,ShelfInventoryConfig
from .car_part_segmentation import CarPartSegmentationUseCase, CarPartSegmentationConfig
from .road_lane_detection import LaneDetectionConfig , LaneDetectionUseCase

from .windmill_maintenance import WindmillMaintenanceUseCase, WindmillMaintenanceConfig

from .field_mapping import FieldMappingConfig, FieldMappingUseCase
from .wound_segmentation import WoundConfig, WoundSegmentationUseCase
from .leaf_disease import LeafDiseaseDetectionConfig, LeafDiseaseDetectionUseCase
from .flower_segmentation import FlowerUseCase, FlowerConfig
from .parking import ParkingConfig, ParkingUseCase
from .leaf import LeafConfig, LeafUseCase
from .smoker_detection import SmokerDetectionConfig, SmokerDetectionUseCase
from .road_traffic_density import RoadTrafficConfig, RoadTrafficUseCase
from .road_view_segmentation import RoadViewSegmentationConfig, RoadViewSegmentationUseCase
from .face_recognition import FaceRecognitionConfig, FaceRecognitionUseCase
from .drowsy_driver_detection import DrowsyDriverUseCase, DrowsyDriverUseCase
from .waterbody_segmentation import WaterBodyConfig, WaterBodyUseCase
from .litter_monitoring import LitterDetectionConfig,LitterDetectionUseCase
from .abandoned_object_detection import AbandonedObjectConfig,AbandonedObjectDetectionUseCase

from .litter_monitoring import LitterDetectionConfig, LitterDetectionUseCase
from .leak_detection import LeakDetectionConfig, LeakDetectionUseCase
from .human_activity_recognition import HumanActivityConfig, HumanActivityUseCase
from .gas_leak_detection import GasLeakDetectionConfig, GasLeakDetectionUseCase

#Put all IMAGE based usecases here
from .blood_cancer_detection_img import BloodCancerDetectionConfig, BloodCancerDetectionUseCase
from .skin_cancer_classification_img import SkinCancerClassificationConfig, SkinCancerClassificationUseCase
from .plaque_segmentation_img import PlaqueSegmentationConfig, PlaqueSegmentationUseCase
from .cardiomegaly_classification import CardiomegalyConfig, CardiomegalyUseCase
from .Histopathological_Cancer_Detection_img import HistopathologicalCancerDetectionConfig,HistopathologicalCancerDetectionUseCase

__all__ = [
    'PeopleCountingUseCase',
    'IntrusionUseCase',
    'ProximityUseCase',
    'CustomerServiceUseCase',
    'AdvancedCustomerServiceUseCase',
    'BasicCountingTrackingUseCase',
    'LicensePlateUseCase',
    'ColorDetectionUseCase',
    'PPEComplianceUseCase',
    'BananaMonitoringUseCase',
    'WoundSegmentationUseCase',
    'FieldMappingUseCase',
    'LeafDiseaseDetectionUseCase',
    'VehicleMonitoringUseCase',
    'ShopliftingDetectionUseCase',
    'ParkingUseCase',
    'ParkingSpaceUseCase',
    'FireSmokeUseCase',
    'MaskDetectionUseCase',
    'FlareAnalysisUseCase',
    'LeafUseCase',
    'PotholeSegmentationUseCase',
    'CarDamageDetectionUseCase',
    'FaceEmotionUseCase',
    'UnderwaterPlasticUseCase',
    'PedestrianDetectionUseCase',
    'AgeDetectionUseCase',
    'WeldDefectUseCase',
    'PriceTagUseCase',
    'WeaponDetectionUseCase',
    'TheftDetectionUseCase',
    'TrafficSignMonitoringUseCase',
    'DistractedDriverUseCase',
    'EmergencyVehicleUseCase',
    'SolarPanelUseCase',
    'ChickenPoseDetectionUseCase',
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
    'ShelfInventoryUseCase',
    'CarPartSegmentationUseCase',
    'LaneDetectionUseCase',
    'WindmillMaintenanceUseCase',
    'FlowerUseCase',
    'SmokerDetectionUseCase',
    'RoadTrafficUseCase',
    'RoadViewSegmentationUseCase',
    'FaceRecognitionUseCase',
    'DrowsyDriverUseCase',
    'WaterBodyUseCase',
    'LitterDetectionUseCase',
    'AbandonedObjectDetectionUseCase',
    'LeakDetectionUseCase',
    'HumanActivityUseCase',
    'GasLeakDetectionUseCase',

    #Put all IMAGE based usecases here
    'BloodCancerDetectionUseCase',
    'SkinCancerClassificationUseCase',
    'PlaqueSegmentationUseCase',
    'CardiomegalyUseCase',
    'HistopathologicalCancerDetectionUseCase',



    'PeopleCountingConfig',
    'IntrusionConfig',
    'ProximityConfig',
    'ParkingSpaceConfig',
    'CustomerServiceConfig',
    'AdvancedCustomerServiceConfig',
    'PPEComplianceConfig',
    'LicensePlateConfig',
    'PotholeConfig',
    'ColorDetectionConfig',
    'LeafDiseaseDetectionConfig',
    'CarDamageConfig',
    'CarDamageConfig',
    'VehicleMonitoringConfig',
    'ShopliftingDetectionConfig',
    'ParkingConfig',
    'FireSmokeConfig',
    'LeafConfig',
    'FlareAnalysisConfig',
    'FaceEmotionConfig',
    'UnderwaterPlasticConfig',
    'FieldMappingConfig',
    'WoundConfig',
    'PedestrianDetectionConfig',
    'ChickenPoseDetectionConfig',
    'AgeDetectionConfig',
    'BananaMonitoringConfig',
    'WeldDefectConfig',
    'PriceTagConfig',
    'DistractedDriverConfig',
    'EmergencyVehicleConfig',
    'TheftDetectionConfig',
    'TrafficSignMonitoringConfig',
    'SolarPanelConfig',
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
    'RoadTrafficConfig',
    'RoadViewSegmentationConfig',
    'FaceRecognitionConfig',
    'DrowsyDriverUseCase',
    'WaterBodyConfig',
    'LitterDetectionConfig',
    'AbandonedObjectConfig',

    'LeakDetectionConfig',
    'HumanActivityConfig',
    'GasLeakDetectionConfig',


    #Put all IMAGE based usecase CONFIGS here
    'BloodCancerDetectionConfig',
    'SkinCancerClassificationConfig',
    'PlaqueSegmentationConfig',
    'CardiomegalyConfig',
    'HistopathologicalCancerDetectionConfig',


]