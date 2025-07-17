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

from .car_damage_detection import CarDamageConfig, CarDamageDetectionUseCase
from .price_tag_detection import PriceTagConfig, PriceTagUseCase
from .mask_detection import MaskDetectionConfig, MaskDetectionUseCase


__all__ = [
    'PeopleCountingUseCase',
    'CustomerServiceUseCase',
    'AdvancedCustomerServiceUseCase',
    'BasicCountingTrackingUseCase',
    'LicensePlateUseCase',
    'ColorDetectionUseCase',
    'PPEComplianceUseCase',
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
    'AgeDetectionConfig',
    'WeldDefectConfig',
    'PriceTagConfig'
]