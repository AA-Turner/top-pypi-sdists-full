"""
Core components for post-processing.

This module contains core base classes and configuration utilities.
Note: Use case imports have been moved to avoid circular imports.
"""

# Core components that don't create circular imports
from .base import (
    BaseProcessor,
    BaseUseCase,
    ProcessingContext,
    ProcessingResult,
    ProcessingStatus,
    ProcessorRegistry,
    ResultFormat,
    registry,
)
from .config import (
    AlertConfig,
    BaseConfig,
    ConfigManager,
    ConfigValidationError,
    CustomerServiceConfig,
    IntrusionAdvancedTrackerConfig,
    IntrusionConfig,
    PeopleCountingConfig,
    PeopleTrackingConfig,
    ProximityConfig,
    TrackingConfig,
    ZoneConfig,
    config_manager,
)

# Note: Use case imports have been removed from this file to avoid circular imports.
# Use cases should be imported directly from their respective modules in the usecases package.


# Export only core components to avoid circular imports
__all__ = [
    # Base classes
    "ProcessingResult",
    "ProcessingContext",
    "ProcessingStatus",
    "ResultFormat",
    "BaseProcessor",
    "BaseUseCase",
    "ProcessorRegistry",
    "registry",
    # Configuration classes
    "BaseConfig",
    "PeopleCountingConfig",
    "IntrusionAdvancedTrackerConfig",
    "IntrusionConfig",
    "ProximityConfig",
    "CustomerServiceConfig",
    "ZoneConfig",
    "TrackingConfig",
    "AlertConfig",
    "ConfigManager",
    "config_manager",
    "ConfigValidationError",
    "PeopleTrackingConfig",
]
