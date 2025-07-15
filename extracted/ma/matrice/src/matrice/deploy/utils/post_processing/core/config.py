"""
Configuration system for post-processing operations.

This module provides a clean, type-safe configuration system using dataclasses
with built-in validation, serialization support, and pythonic configuration management.
"""

from dataclasses import dataclass, field, fields
from typing import Any, Dict, List, Optional, Union, get_type_hints
from pathlib import Path
import json
import yaml
from abc import ABC, abstractmethod

from .base import ConfigProtocol


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


@dataclass
class BaseConfig(ConfigProtocol):
    """Base configuration class with common functionality and validation."""
    
    # Core identification
    category: str = ""
    usecase: str = ""
    
    # Common processing parameters
    confidence_threshold: Optional[float] = 0.5
    enable_tracking: bool = False
    enable_analytics: bool = True
    
    # Performance settings
    batch_size: Optional[int] = None
    max_objects: Optional[int] = 1000
    
    # Additional parameters
    extra_params: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of error messages."""
        errors = []
        
        # Validate confidence threshold
        if self.confidence_threshold is not None:
            if not 0.0 <= self.confidence_threshold <= 1.0:
                errors.append("confidence_threshold must be between 0.0 and 1.0")
        
        # Validate max_objects
        if self.max_objects is not None and self.max_objects <= 0:
            errors.append("max_objects must be positive")
        
        # Validate batch_size
        if self.batch_size is not None and self.batch_size <= 0:
            errors.append("batch_size must be positive")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {}
        
        # Get all fields
        for field_info in fields(self):
            value = getattr(self, field_info.name)
            if value is not None:
                # Handle nested configs
                if hasattr(value, 'to_dict'):
                    result[field_info.name] = value.to_dict()
                elif isinstance(value, dict):
                    # Handle dictionaries with potential nested configs
                    nested_dict = {}
                    for k, v in value.items():
                        if hasattr(v, 'to_dict'):
                            nested_dict[k] = v.to_dict()
                        else:
                            nested_dict[k] = v
                    result[field_info.name] = nested_dict
                else:
                    result[field_info.name] = value
        
        # Merge extra_params at top level
        if self.extra_params:
            result.update(self.extra_params)
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseConfig':
        """Create config from dictionary with type conversion."""
        # Get field names and types for this class
        field_names = {f.name: f.type for f in fields(cls)}
        
        # Separate known fields from extra parameters
        known_params = {}
        extra_params = {}
        
        for k, v in data.items():
            if k in field_names:
                known_params[k] = v
            else:
                extra_params[k] = v
        
        if extra_params:
            known_params['extra_params'] = extra_params
        
        return cls(**known_params)


@dataclass
class ZoneConfig:
    """Configuration for zone-based processing."""
    
    # Zone definitions (name -> polygon points)
    zones: Dict[str, List[List[float]]] = field(default_factory=dict)
    
    # Zone-specific settings
    zone_confidence_thresholds: Dict[str, float] = field(default_factory=dict)
    zone_categories: Dict[str, List[str]] = field(default_factory=dict)
    
    def validate(self) -> List[str]:
        """Validate zone configuration."""
        errors = []
        
        for zone_name, polygon in self.zones.items():
            if len(polygon) < 3:
                errors.append(f"Zone '{zone_name}' must have at least 3 points")
            
            for i, point in enumerate(polygon):
                if len(point) != 2:
                    errors.append(f"Zone '{zone_name}' point {i} must have exactly 2 coordinates")
        
        # Validate zone confidence thresholds
        for zone_name, threshold in self.zone_confidence_thresholds.items():
            if zone_name not in self.zones:
                errors.append(f"Zone confidence threshold defined for unknown zone '{zone_name}'")
            if not 0.0 <= threshold <= 1.0:
                errors.append(f"Zone '{zone_name}' confidence threshold must be between 0.0 and 1.0")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "zones": self.zones,
            "zone_confidence_thresholds": self.zone_confidence_thresholds,
            "zone_categories": self.zone_categories
        }

@dataclass
class TrackingConfig:
    """Configuration for tracking operations."""
    
    # Tracking method and parameters
    tracking_method: str = "kalman"
    max_age: int = 30
    min_hits: int = 3
    iou_threshold: float = 0.3
    
    # Target classes for tracking
    target_classes: List[str] = field(default_factory=list)
    
    # Advanced tracking settings
    use_appearance_features: bool = False
    appearance_threshold: float = 0.7
    
    def validate(self) -> List[str]:
        """Validate tracking configuration."""
        errors = []
        
        valid_methods = ["kalman", "sort", "deepsort", "bytetrack"]
        if self.tracking_method not in valid_methods:
            errors.append(f"tracking_method must be one of {valid_methods}")
        
        if self.max_age <= 0:
            errors.append("max_age must be positive")
        
        if self.min_hits <= 0:
            errors.append("min_hits must be positive")
        
        if not 0.0 <= self.iou_threshold <= 1.0:
            errors.append("iou_threshold must be between 0.0 and 1.0")
        
        if not 0.0 <= self.appearance_threshold <= 1.0:
            errors.append("appearance_threshold must be between 0.0 and 1.0")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "tracking_method": self.tracking_method,
            "max_age": self.max_age,
            "min_hits": self.min_hits,
            "iou_threshold": self.iou_threshold,
            "target_classes": self.target_classes,
            "use_appearance_features": self.use_appearance_features,
            "appearance_threshold": self.appearance_threshold
        }


@dataclass
class AlertConfig:
    """Configuration for alerting system."""
    
    # Threshold-based alerts
    count_thresholds: Dict[str, int] = field(default_factory=dict)
    occupancy_thresholds: Dict[str, int] = field(default_factory=dict)
    
    # Time-based alerts
    dwell_time_threshold: Optional[float] = None
    service_time_threshold: Optional[float] = None
    
    # Alert settings
    alert_cooldown: float = 60.0  # seconds
    enable_email_alerts: bool = False
    enable_webhook_alerts: bool = False
    webhook_url: Optional[str] = None
    email_recipients: List[str] = field(default_factory=list)
    
    def validate(self) -> List[str]:
        """Validate alert configuration."""
        errors = []
        
        # Validate thresholds are positive
        for category, threshold in self.count_thresholds.items():
            if threshold <= 0:
                errors.append(f"Count threshold for '{category}' must be positive")
        
        for zone, threshold in self.occupancy_thresholds.items():
            if threshold <= 0:
                errors.append(f"Occupancy threshold for zone '{zone}' must be positive")
        
        # Validate time thresholds
        if self.dwell_time_threshold is not None and self.dwell_time_threshold <= 0:
            errors.append("dwell_time_threshold must be positive")
        
        if self.service_time_threshold is not None and self.service_time_threshold <= 0:
            errors.append("service_time_threshold must be positive")
        
        if self.alert_cooldown <= 0:
            errors.append("alert_cooldown must be positive")
        
        # Validate webhook settings
        if self.enable_webhook_alerts and not self.webhook_url:
            errors.append("webhook_url is required when enable_webhook_alerts is True")
        
        if self.enable_email_alerts and not self.email_recipients:
            errors.append("email_recipients is required when enable_email_alerts is True")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "count_thresholds": self.count_thresholds,
            "occupancy_thresholds": self.occupancy_thresholds,
            "dwell_time_threshold": self.dwell_time_threshold,
            "service_time_threshold": self.service_time_threshold,
            "alert_cooldown": self.alert_cooldown,
            "enable_email_alerts": self.enable_email_alerts,
            "enable_webhook_alerts": self.enable_webhook_alerts,
            "webhook_url": self.webhook_url,
            "email_recipients": self.email_recipients
        }


@dataclass
class PeopleCountingConfig(BaseConfig):
    """Configuration for people counting use case."""
    
    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5
    
    # Zone configuration
    zone_config: Optional[ZoneConfig] = None
    
    # Counting parameters
    enable_unique_counting: bool = True
    time_window_minutes: int = 60
    
    # Category mapping
    person_categories: List[str] = field(default_factory=lambda: ["person", "people"])
    index_to_category: Optional[Dict[int, str]] = None
    
    # Alert configuration
    alert_config: Optional[AlertConfig] = None
    
    def validate(self) -> List[str]:
        """Validate people counting configuration."""
        errors = super().validate()
        
        if self.time_window_minutes <= 0:
            errors.append("time_window_minutes must be positive")
        
        if not self.person_categories:
            errors.append("person_categories cannot be empty")
        
        # Validate nested configurations
        if self.zone_config:
            errors.extend(self.zone_config.validate())
        
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        
        return errors
    


@dataclass  
class CustomerServiceConfig(BaseConfig):
    """Configuration for customer service use case."""
    
    # Area definitions
    customer_areas: Dict[str, List[List[float]]] = field(default_factory=dict)
    staff_areas: Dict[str, List[List[float]]] = field(default_factory=dict)
    service_areas: Dict[str, List[List[float]]] = field(default_factory=dict)
    
    # Category identification
    staff_categories: List[str] = field(default_factory=lambda: ["staff", "employee"])
    customer_categories: List[str] = field(default_factory=lambda: ["customer", "person"])
    
    # Service parameters
    service_proximity_threshold: float = 100.0
    max_service_time: float = 1800.0  # 30 minutes
    buffer_time: float = 2.0
    
    # Tracking configuration
    tracking_config: Optional[TrackingConfig] = None
    
    # Alert configuration
    alert_config: Optional[AlertConfig] = None
    
    # Additional analytics options
    enable_journey_analysis: bool = False
    enable_queue_analytics: bool = False
    
    def validate(self) -> List[str]:
        """Validate customer service configuration."""
        errors = super().validate()
        
        if self.service_proximity_threshold <= 0:
            errors.append("service_proximity_threshold must be positive")
        
        if self.max_service_time <= 0:
            errors.append("max_service_time must be positive")
        
        if self.buffer_time < 0:
            errors.append("buffer_time must be non-negative")
        
        # Validate category lists
        if not self.staff_categories:
            errors.append("staff_categories cannot be empty")
        
        if not self.customer_categories:
            errors.append("customer_categories cannot be empty")
        
        # Validate area polygons
        all_areas = {**self.customer_areas, **self.staff_areas, **self.service_areas}
        for area_name, polygon in all_areas.items():
            if len(polygon) < 3:
                errors.append(f"Area '{area_name}' must have at least 3 points")
            
            for i, point in enumerate(polygon):
                if len(point) != 2:
                    errors.append(f"Area '{area_name}' point {i} must have exactly 2 coordinates")
        
        # Validate nested configurations
        if self.tracking_config:
            errors.extend(self.tracking_config.validate())
        
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        
        return errors


class ConfigManager:
    """Centralized configuration management for post-processing operations."""
    
    def __init__(self):
        """Initialize configuration manager."""
        self._config_classes = {
            "people_counting": PeopleCountingConfig,
            "customer_service": CustomerServiceConfig,
            "advanced_customer_service": CustomerServiceConfig,
            "basic_counting_tracking": None,  # Will be set later to avoid circular import
            "license_plate_detection": None,  # Will be set later to avoid circular import
            "ppe_compliance_detection": None,
            "color_detection": None,  # Will be set later to avoid circular import
            "video_color_classification": None,  # Alias for color_detection
            "vehicle_monitoring" : None,
            "fire_smoke_detection": None,
            "flare_analysis" : None
        }

    def register_config_class(self, usecase: str, config_class: type) -> None:
        """Register a configuration class for a use case."""
        self._config_classes[usecase] = config_class

    def _get_license_plate_config_class(self):
        """Get LicensePlateConfig class to avoid circular imports."""
        try:
            from ..usecases.license_plate_detection import LicensePlateConfig
            return LicensePlateConfig
        except ImportError:
            return None

    def vehicle_monitoring_config_class(self):
        """Get vehicle monitoring class to avoid circular imports."""
        try:
            from ..usecases.vehicle_monitoring import VehicleMonitoringConfig
            return VehicleMonitoringConfig
        except ImportError:
            return None

    def _get_fire_smoke_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.fire_detection import FireSmokeConfig
            return FireSmokeConfig
        except ImportError:
            return None

    def _get_pothole_segmentation_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.pothole_segmentation import PotholeConfig
            return PotholeConfig
        except ImportError:
            return None
        
    def flare_analysis_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.flare_analysis import FlareAnalysisConfig
            return FlareAnalysisConfig
        except ImportError:
            return None

    def create_config(self, usecase: str, category: Optional[str] = None, **kwargs) -> BaseConfig:
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
        if usecase == "people_counting":
            # Handle nested configurations
            zone_config = kwargs.pop("zone_config", None)
            if zone_config and isinstance(zone_config, dict):
                zone_config = ZoneConfig(**zone_config)

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = PeopleCountingConfig(
                category=category or "general",
                usecase=usecase,
                zone_config=zone_config,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase in ["customer_service", "advanced_customer_service"]:
            # Handle nested configurations
            tracking_config = kwargs.pop("tracking_config", None)
            if tracking_config and isinstance(tracking_config, dict):
                tracking_config = TrackingConfig(**tracking_config)

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = CustomerServiceConfig(
                category=category or "sales",
                usecase=usecase,
                tracking_config=tracking_config,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "basic_counting_tracking":
            # Import here to avoid circular import
            from ..usecases.basic_counting_tracking import BasicCountingTrackingConfig

            # Handle nested configurations
            tracking_config = kwargs.pop("tracking_config", None)
            if tracking_config and isinstance(tracking_config, dict):
                tracking_config = TrackingConfig(**tracking_config)

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Extract basic counting tracking specific parameters
            target_categories = kwargs.pop("target_categories", None)
            zones = kwargs.pop("zones", None)
            tracking_method = kwargs.pop("tracking_method", "kalman")
            max_age = kwargs.pop("max_age", 30)
            min_hits = kwargs.pop("min_hits", 3)
            count_thresholds = kwargs.pop("count_thresholds", None)
            zone_thresholds = kwargs.pop("zone_thresholds", None)
            alert_cooldown = kwargs.pop("alert_cooldown", 60.0)
            enable_unique_counting = kwargs.pop("enable_unique_counting", True)

            config = BasicCountingTrackingConfig(
                category=category or "general",
                usecase=usecase,
                target_categories=target_categories,
                zones=zones,
                tracking_method=tracking_method,
                max_age=max_age,
                min_hits=min_hits,
                count_thresholds=count_thresholds,
                zone_thresholds=zone_thresholds,
                alert_cooldown=alert_cooldown,
                enable_unique_counting=enable_unique_counting,
                **kwargs
            )
        elif usecase == "license_plate_detection":
            # Import here to avoid circular import
            from ..usecases.license_plate_detection import LicensePlateConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = LicensePlateConfig(
                category=category or "vehicle",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "fire_smoke_detection":
            # Import here to avoid circular import
            from ..usecases.fire_detection import FireSmokeConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = FireSmokeConfig(
                category=category or "normal",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "pothole_segmentation":
            # Import here to avoid circular import
            from ..usecases.pothole_segmentation import PotholeConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = PotholeConfig(
                category=category or "normal",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )


        elif usecase == "flare_analysis":
            # Import here to avoid circular import
            from ..usecases.flare_analysis import FlareAnalysisConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = FlareAnalysisConfig(
                category=category or "normal",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "vehicle_monitoring":
            # Import here to avoid circular import
            from ..usecases.vehicle_monitoring import VehicleMonitoringConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = VehicleMonitoringConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "ppe_compliance_detection":
            # Import here to avoid circular import
            from ..usecases.ppe_compliance import PPEComplianceConfig
            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)
            config = PPEComplianceConfig(
                category=category or "ppe",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "color_detection":
            # Import here to avoid circular import
            from ..usecases.color_detection import ColorDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = ColorDetectionConfig(
                category=category or "visual_appearance",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "video_color_classification":
            # Alias for color_detection - Import here to avoid circular import
            from ..usecases.color_detection import ColorDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = ColorDetectionConfig(
                category=category or "visual_appearance",
                usecase="color_detection",  # Use canonical name internally
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "ppe_compliance_detection":
            # Import here to avoid circular import
            from ..usecases.ppe_compliance import PPEComplianceConfig
            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)
            config = PPEComplianceConfig(
                category=category or "ppe",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        else:
            raise ConfigValidationError(f"Unknown use case: {usecase}")

        # Validate configuration
        errors = config.validate()
        if errors:
            raise ConfigValidationError(f"Configuration validation failed: {errors}")

        return config

    def load_from_file(self, file_path: Union[str, Path]) -> BaseConfig:
        """
        Load configuration from file.

        Args:
            file_path: Path to configuration file (JSON or YAML)

        Returns:
            BaseConfig: Configuration object

        Raises:
            ConfigValidationError: If file cannot be loaded or validation fails
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise ConfigValidationError(f"Configuration file not found: {file_path}")

        try:
            # Load data based on file extension
            if file_path.suffix.lower() == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
            elif file_path.suffix.lower() in ['.yml', '.yaml']:
                with open(file_path, 'r') as f:
                    data = yaml.safe_load(f)
            else:
                raise ConfigValidationError(f"Unsupported file format: {file_path.suffix}")

            # Extract usecase and category
            usecase = data.get('usecase')
            if not usecase:
                raise ConfigValidationError("Configuration file must specify 'usecase'")

            category = data.get('category', 'general')

            # Remove category and usecase from data to avoid duplication
            data_copy = data.copy()
            data_copy.pop('category', None)
            data_copy.pop('usecase', None)

            # Create config
            return self.create_config(usecase, category, **data_copy)

        except (json.JSONDecodeError, yaml.YAMLError) as e:
            raise ConfigValidationError(f"Failed to parse configuration file: {str(e)}")
        except Exception as e:
            raise ConfigValidationError(f"Failed to load configuration: {str(e)}")

    def save_to_file(self, config: BaseConfig, file_path: Union[str, Path], format: str = "json") -> None:
        """
        Save configuration to file.

        Args:
            config: Configuration object
            file_path: Output file path
            format: Output format ('json' or 'yaml')

        Raises:
            ConfigValidationError: If format is unsupported or saving fails
        """
        file_path = Path(file_path)

        try:
            data = config.to_dict()

            if format.lower() == 'json':
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
            elif format.lower() in ['yml', 'yaml']:
                with open(file_path, 'w') as f:
                    yaml.dump(data, f, default_flow_style=False, indent=2)
            else:
                raise ConfigValidationError(f"Unsupported format: {format}")

        except Exception as e:
            raise ConfigValidationError(f"Failed to save configuration: {str(e)}")

    def get_config_template(self, usecase: str) -> Dict[str, Any]:
        """Get configuration template for a use case."""
        if usecase == "basic_counting_tracking":
            # Import here to avoid circular import
            from ..usecases.basic_counting_tracking import BasicCountingTrackingConfig
            default_config = BasicCountingTrackingConfig()
            return default_config.to_dict()
        elif usecase == "license_plate_detection":
            # Import here to avoid circular import
            from ..usecases.license_plate_detection import LicensePlateConfig
            default_config = LicensePlateConfig()
            return default_config.to_dict()
        elif usecase == "fire_smoke_detection":
            # Import here to avoid circular import
            from ..usecases.fire_detection import FireSmokeConfig
            default_config = FireSmokeConfig()
            return default_config.to_dict()

        elif usecase == "pothole_segmentation":
            # Import here to avoid circular import
            from ..usecases.pothole_segmentation import PotholeConfig
            default_config = PotholeConfig()
            return default_config.to_dict()

        elif usecase == "vehicle_monitoring":
            # Import here to avoid circular import
            from ..usecases.vehicle_monitoring import VehicleMonitoringConfig
            default_config = VehicleMonitoringConfig()
            return default_config.to_dict()
        elif usecase == "video_color_classification":
            from ..usecases.color_detection import ColorDetectionConfig
            default_config = ColorDetectionConfig()
            return default_config.to_dict()
        elif usecase == "color_detection":
            # Import here to avoid circular import
            from ..usecases.color_detection import ColorDetectionConfig
            default_config = ColorDetectionConfig()
            return default_config.to_dict()
        elif usecase == "flare_analysis":
            # Import here to avoid circular import
            from ..usecases.flare_analysis import FlareAnalysisConfig
            default_config = FlareAnalysisConfig()
            return default_config.to_dict()
        elif usecase == "ppe_compliance_detection":
            # Import here to avoid circular import
            from ..usecases.ppe_compliance import PPEComplianceConfig
            default_config = PPEComplianceConfig()
            return default_config.to_dict()
        elif usecase not in self._config_classes:
            raise ConfigValidationError(f"Unsupported use case: {usecase}")


        
        config_class = self._config_classes[usecase]
        default_config = config_class()
        return default_config.to_dict()
    
    def list_supported_usecases(self) -> List[str]:
        """List all supported use cases."""
        return list(self._config_classes.keys())


# Global configuration manager instance
config_manager = ConfigManager()
