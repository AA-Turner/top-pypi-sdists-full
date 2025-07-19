"""
Use case implementations for post-processing.

This module contains all available use case processors for different
post-processing scenarios.
"""

from .people_counting import PeopleCountingUseCase, PeopleCountingConfig
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

__all__ = [
    'PeopleCountingUseCase',
    'CustomerServiceUseCase',
    'AdvancedCustomerServiceUseCase',
    'BasicCountingTrackingUseCase',
    'LicensePlateUseCase',
    'ColorDetectionUseCase',
    'PPEComplianceUseCase',
    'BananaMonitoringUseCase',
    'VehicleMonitoringUseCase',
    'ParkingSpaceUseCase',
    'FireSmokeUseCase',
    'MaskDetectionUseCase',
    'FlareAnalysisUseCase',
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
    'PeopleCountingConfig',
    'ParkingSpaceConfig',
    'CustomerServiceConfig',
    'AdvancedCustomerServiceConfig',
    'PPEComplianceConfig',
    'LicensePlateConfig',
    'PotholeConfig',
    'ColorDetectionConfig',
    'CarDamageConfig',
    'CarDamageConfig',
    'VehicleMonitoringConfig',
    'FireSmokeConfig',
    'FlareAnalysisConfig',
    'FaceEmotionConfig',
    'UnderwaterPlasticConfig',
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
    'FashionDetectionConfig'
]