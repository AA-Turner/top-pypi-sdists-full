"""
Core components for post-processing.

This module contains core base classes and configuration utilities.
Note: Use case imports have been moved to avoid circular imports.
"""

# Core components that don't create circular imports
from .base import (
    ProcessingResult, 
    ProcessingContext, 
    ProcessingStatus,
    ResultFormat,
    BaseProcessor,
    BaseUseCase,
    ProcessorRegistry,
    registry
)

from .config import (
    BaseConfig,
    PeopleCountingConfig,
    CustomerServiceConfig,
    IntrusionConfig,
    ZoneConfig,
    TrackingConfig,
    AlertConfig,
    ConfigManager,
    config_manager,
    ConfigValidationError
)

# Note: Use case imports have been removed from this file to avoid circular imports.
# Use cases should be imported directly from their respective modules in the usecases package.


# Export only core components to avoid circular imports
__all__ = [
    # Base classes
    'ProcessingResult',
    'ProcessingContext', 
    'ProcessingStatus',
    'ResultFormat',
    'BaseProcessor',
    'BaseUseCase',
    'ProcessorRegistry',
    'registry',
    
    # Configuration classes
    'BaseConfig',
    'PeopleCountingConfig',
    'IntrusionConfig',
    'ProximityConfig',
    'CustomerServiceConfig',
    'ZoneConfig',
    'TrackingConfig',
    'AlertConfig',
    'ConfigManager',
    'config_manager',
    'ConfigValidationError'
]
