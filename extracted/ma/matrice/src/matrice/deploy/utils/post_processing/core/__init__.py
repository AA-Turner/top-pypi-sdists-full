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
    'FlareAnalysisUseCase',
    'PeopleCountingConfig',
    'PotholeConfig',
    'CustomerServiceConfig',
    'AdvancedCustomerServiceConfig',
    'PPEComplianceConfig',
    'LicensePlateConfig',
    'ColorDetectionConfig',
    'VehicleMonitoringConfig',
    'FireSmokeConfig',
    'FlareAnalysisConfig'
]
