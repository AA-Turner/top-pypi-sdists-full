"""
Use case implementations for post-processing.

This module contains all available use case processors for different
post-processing scenarios.
"""

from ..usecases.people_counting import PeopleCountingUseCase, PeopleCountingConfig
from ..usecases.customer_service import CustomerServiceUseCase, CustomerServiceConfig
from ..usecases.advanced_customer_service import AdvancedCustomerServiceUseCase
from ..usecases.basic_counting_tracking import BasicCountingTrackingUseCase
from ..usecases.license_plate_detection import LicensePlateUseCase, LicensePlateConfig
from ..usecases.color_detection import ColorDetectionUseCase, ColorDetectionConfig
from ..usecases.ppe_compliance import PPEComplianceUseCase, PPEComplianceConfig
from ..usecases.vehicle_monitoring import VehicleMonitoringConfig, VehicleMonitoringUseCase
from ..usecases.fire_detection import FireSmokeConfig, FireSmokeUseCase
from ..usecases.flare_analysis import FlareAnalysisConfig,FlareAnalysisUseCase
from ..usecases.pothole_segmentation import PotholeConfig, PotholeSegmentationUseCase
from ..usecases.face_emotion import FaceEmotionConfig, FaceEmotionUseCase
from ..usecases.parking_space_detection import ParkingSpaceConfig, ParkingSpaceUseCase
from ..usecases.underwater_pollution_detection import UnderwaterPlasticConfig, UnderwaterPlasticUseCase
from ..usecases.pedestrian_detection import PedestrianDetectionConfig, PedestrianDetectionUseCase
from ..usecases.car_damage_detection import CarDamageConfig, CarDamageDetectionUseCase
from ..usecases.age_detection import AgeDetectionUseCase, AgeDetectionConfig
from ..usecases.weld_defect_detection import WeldDefectUseCase,WeldDefectConfig
from ..usecases.price_tag_detection import PriceTagUseCase, PriceTagConfig
from ..usecases.mask_detection import MaskDetectionConfig, MaskDetectionUseCase
from ..usecases.banana_defect_detection import BananaMonitoringUseCase,BananaMonitoringConfig
from ..usecases.distracted_driver_detection import DistractedDriverUseCase, DistractedDriverConfig
from ..usecases.emergency_vehicle_detection import EmergencyVehicleUseCase, EmergencyVehicleConfig
from ..usecases.solar_panel import SolarPanelUseCase, SolarPanelConfig
from ..usecases.chicken_pose_detection import ChickenPoseDetectionUseCase,ChickenPoseDetectionConfig
from ..usecases.theft_detection import TheftDetectionUseCase,TheftDetectionConfig
from ..usecases.traffic_sign_monitoring import TrafficSignMonitoringConfig, TrafficSignMonitoringUseCase
from ..usecases.crop_weed_detection import CropWeedDetectionUseCase, CropWeedDetectionConfig
from ..usecases.child_monitoring import ChildMonitoringUseCase, ChildMonitoringConfig
from ..usecases.gender_detection import GenderDetectionConfig, GenderDetectionUseCase
from ..usecases.weapon_detection import WeaponDetectionUseCase,WeaponDetectionConfig
from ..usecases.concrete_crack_detection import ConcreteCrackUseCase, ConcreteCrackConfig
from ..usecases.fashion_detection import FashionDetectionUseCase, FashionDetectionConfig
from ..usecases.anti_spoofing_detection import AntiSpoofingDetectionUseCase, AntiSpoofingDetectionConfig

from ..usecases.warehouse_object_segmentation import WarehouseObjectUseCase, WarehouseObjectConfig
from ..usecases.shopping_cart_analysis import ShoppingCartUseCase, ShoppingCartConfig
from ..usecases.assembly_line_detection import AssemblyLineUseCase, AssemblyLineConfig

from ..usecases.shoplifting_detection import ShopliftingDetectionConfig, ShopliftingDetectionUseCase
from ..usecases.defect_detection_products import BottleDefectUseCase, BottleDefectConfig
from ..usecases.shelf_inventory_detection import ShelfInventoryConfig,ShelfInventoryUseCase
from ..usecases.car_part_segmentation import CarPartSegmentationUseCase, CarPartSegmentationConfig
from ..usecases.road_lane_detection import LaneDetectionUseCase , LaneDetectionConfig

from ..usecases.windmill_maintenance import WindmillMaintenanceUseCase, WindmillMaintenanceConfig

from ..usecases.field_mapping import FieldMappingConfig, FieldMappingUseCase
from ..usecases.wound_segmentation import WoundConfig,WoundSegmentationUseCase
from ..usecases.leaf_disease import LeafDiseaseDetectionConfig, LeafDiseaseDetectionUseCase
from ..usecases.flower_segmentation import FlowerUseCase, FlowerConfig


__all__ = [
    'PeopleCountingUseCase',
    'CustomerServiceUseCase',
    'BananaMonitoringUseCase',
    'AdvancedCustomerServiceUseCase',
    'BasicCountingTrackingUseCase',
    'FieldMappingUseCase',
    'LicensePlateUseCase',
    'ColorDetectionUseCase',
    'LeafDiseaseDetectionUseCase',
    'PPEComplianceUseCase',
    'VehicleMonitoringUseCase',
    'FireSmokeUseCase',
    'PotholeSegmentationUseCase',
    'AntiSpoofingDetectionUseCase',
    'WoundSegmentationUseCase',
    'ShelfInventoryUseCase',
    'LaneDetectionUseCase',

    'ShopliftingDetectionUseCase',
    'ParkingSpaceUseCase',
    'FlareAnalysisUseCase',
    'MaskDetectionUseCase',
    'CarDamageDetectionUseCase',
    'FaceEmotionUseCase',
    'UnderwaterPlasticUseCase',
    'PedestrianDetectionUseCase',
    'AgeDetectionUseCase',
    'WeldDefectUseCase',
    'PriceTagUseCase',
    'DistractedDriverUseCase',
    'EmergencyVehicleUseCase',
    'ChickenPoseDetectionUseCase',
    'SolarPanelUseCase',
    'TheftDetectionUseCase',
    'TrafficSignMonitoringUseCase',
    'CropWeedDetectionUseCase',
    'ChildMonitoringUseCase',
    'GenderDetectionUseCase',
    'WeaponDetectionUseCase',
    'ConcreteCrackUseCase',
    'FashionDetectionUseCase',
    'WarehouseObjectUseCase',
    'ShoppingCartUseCase',
    'BottleDefectUseCase',
    'AssemblyLineUseCase',
    'CarPartSegmentationUseCase',
    'WindmillMaintenanceUseCase',
    'FlowerUseCase',




    'PeopleCountingConfig',
    'PotholeConfig',
    'BananaMonitoringConfig',
    'CustomerServiceConfig',
    'AdvancedCustomerServiceConfig',
    'PPEComplianceConfig',
    'LicensePlateConfig',
    'ColorDetectionConfig',
    'VehicleMonitoringConfig',
    'WoundConfig',
    'ParkingSpaceConfig',
    'MaskDetectionConfig',
    'FireSmokeConfig',
    'ShopliftingDetectionConfig',
    'CarDamageConfig',
    'FlareAnalysisConfig',
    'FieldMappingConfig',
    'FaceEmotionConfig',
    'UnderwaterPlasticConfig',
    'PedestrianDetectionConfig',
    'AgeDetectionConfig',
    'WeldDefectConfig',
    'PriceTagConfig',
    'DistractedDriverConfig',
    'EmergencyVehicleConfig',
    'ChickenPoseDetectionConfig',
    'SolarPanelConfig',
    'TheftDetectionConfig',
    'TrafficSignMonitoringConfig',
    'CropWeedDetectionConfig',
    'ChildMonitoringConfig',
    'GenderDetectionConfig',
    'WeaponDetectionConfig',
    'LeafDiseaseDetectionConfig',
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
]
