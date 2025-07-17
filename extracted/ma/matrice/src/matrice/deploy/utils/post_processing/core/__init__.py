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

__all__ = [
    'PeopleCountingUseCase',
    'CustomerServiceUseCase',
    'AdvancedCustomerServiceUseCase',
    'BasicCountingTrackingUseCase',
    'LicensePlateUseCase',
    'ColorDetectionUseCase',
    'PPEComplianceUseCase',
    'VehicleMonitoringUseCase',
    'FireSmokeUseCase',
    'PotholeSegmentationUseCase',
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
    'PeopleCountingConfig',
    'PotholeConfig',
    'CustomerServiceConfig',
    'AdvancedCustomerServiceConfig',
    'PPEComplianceConfig',
    'LicensePlateConfig',
    'ColorDetectionConfig',
    'VehicleMonitoringConfig',
    'ParkingSpaceConfig',
    'MaskDetectionConfig',
    'FireSmokeConfig',
    'CarDamageConfig',
    'FlareAnalysisConfig',
    'FaceEmotionConfig',
    'UnderwaterPlasticConfig',
    'PedestrianDetectionConfig',
    'AgeDetectionConfig',
    'WeldDefectConfig',
    'PriceTagConfig'
]
