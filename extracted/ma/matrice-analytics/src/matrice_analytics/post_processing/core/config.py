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
import logging
from abc import ABC, abstractmethod

from .base import ConfigProtocol

logger = logging.getLogger(__name__)


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

    # --- Legacy/dict-like compatibility helpers ---
    def _as_legacy_dict(self) -> Dict[str, Any]:
        return {
            "zones": self.zones,
            "zone_confidence_thresholds": self.zone_confidence_thresholds,
            "zone_categories": self.zone_categories,
        }

    def __getitem__(self, key: str) -> Any:  # Support config.zone_config['zones']
        return self._as_legacy_dict()[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self._as_legacy_dict().get(key, default)

    def keys(self):
        return self._as_legacy_dict().keys()

    def items(self):
        return self._as_legacy_dict().items()

    def __contains__(self, key: object) -> bool:
        return key in self._as_legacy_dict()

    def __iter__(self):
        return iter(self._as_legacy_dict())

    def __len__(self) -> int:
        return len(self._as_legacy_dict())

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
    
    # enable_webhook_alerts: bool = False
    # webhook_url: Optional[str] = None
    # enable_email_alerts: bool = False
    # email_recipients: List[str] = field(default_factory=list)

    alert_type: List[str] = field(default_factory=lambda: ['Default']) #webhook, email, sms, slack, telegram, whatsapp, etc.
    alert_value: List[str] = field(default_factory=lambda: ['JSON']) #webhook_url, email_recipients, etc.
    alert_incident_category: List[str] = field(default_factory=lambda: ['Incident Alert'])
    #alert_settings: Optional[Dict[str, Any]] = {alert_type: None}
    
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

        if len(self.alert_incident_category)!=len(self.alert_type) or len(self.alert_incident_category)!=len(self.alert_value):
            errors.append("Details for all alerts is required")

        if self.alert_type[0]!='Default':
            for i in range(len(self.alert_type)):
                normalized = self.alert_type[i].lower()
                # Validate webhook settings
                if normalized=="webhook"  and not self.alert_value:
                    errors.append("webhook_url is required")
                
                elif normalized=="email" and not self.alert_value:
                    errors.append("email_recipients is required")

                elif normalized=="phone" and not self.alert_value:
                    errors.append("phone_number is required")
        if len(self.alert_type)==1 and self.alert_type[0]=='Default':
            self.alert_value=["JSON"]
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "count_thresholds": self.count_thresholds,
            "occupancy_thresholds": self.occupancy_thresholds,
            "dwell_time_threshold": self.dwell_time_threshold,
            "service_time_threshold": self.service_time_threshold,
            "alert_cooldown": self.alert_cooldown,
            "alert_type": self.alert_type,
            "alert_value": self.alert_value
        }

    # --- Legacy/dict-like compatibility helpers ---
    def _as_legacy_dict(self) -> Dict[str, Any]:
        return {
            "count_thresholds": self.count_thresholds,
            "occupancy_thresholds": self.occupancy_thresholds,
            "dwell_time_threshold": self.dwell_time_threshold,
            "service_time_threshold": self.service_time_threshold,
            "alert_cooldown": self.alert_cooldown,
            "alert_type": self.alert_type,
            "alert_value": self.alert_value,
            "alert_incident_category": self.alert_incident_category,
        }

    def __getitem__(self, key: str) -> Any:
        return self._as_legacy_dict()[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self._as_legacy_dict().get(key, default)

    def keys(self):
        return self._as_legacy_dict().keys()

    def items(self):
        return self._as_legacy_dict().items()

    def __contains__(self, key: object) -> bool:
        return key in self._as_legacy_dict()

    def __iter__(self):
        return iter(self._as_legacy_dict())

    def __len__(self) -> int:
        return len(self._as_legacy_dict())


@dataclass
class PeopleCountingConfig(BaseConfig):
    """Configuration for people counting use case."""

    # Smoothing configuration
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # ====== PERFORMANCE: Tracker selection ======
    enable_advanced_tracker: bool = True  # Heavy O(n³) tracker - enable only when tracking quality is critical
    enable_simple_tracker: bool = False     # Lightweight O(n) tracker - enabled by default for tracking ID assignment
    # ====== END PERFORMANCE CONFIG ======
    confidence_threshold: float = 0.245

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

    target_categories: List[str] = field(
        default_factory=lambda: [
            'person', 'people', 'human', 'man', 'woman', 'male', 'female']
    )

    # Minimum number of frames a track must be present before it is counted as
    # a "new" person.  This filters out spurious short-lived track IDs that the
    # tracker may generate from noise, flickering detections, or brief ID
    # switches.  At 30 fps the default of 5 frames equals ~0.1 s latency.
    min_hits_for_new_track: int = 5
    
    def validate(self) -> List[str]:
        """Validate people counting configuration."""
        errors = super().validate()
        
        if self.time_window_minutes <= 0:
            errors.append("time_window_minutes must be positive")
        
        if not self.person_categories:
            errors.append("person_categories cannot be empty")

        if self.min_hits_for_new_track < 1:
            errors.append("min_hits_for_new_track must be >= 1")
        
        # Validate nested configurations
        if self.zone_config:
            errors.extend(self.zone_config.validate())
        
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        
        return errors


@dataclass
class IntrusionConfig(BaseConfig):
    """Configuration for intrusion detection use case."""
    
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
    person_categories: List[str] = field(default_factory=lambda: ["person"])
    index_to_category: Optional[Dict[int, str]] = None
    
    # Alert configuration
    alert_config: Optional[AlertConfig] = None
    
    def validate(self) -> List[str]:
        """Validate intrusion detection configuration."""
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
class ProximityConfig(BaseConfig):
    """Configuration for intrusion detection use case."""
    
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
    
    proximity_threshold_meters: float = 1.0
    proximity_threshold_pixels: float = 250.0
    meters_per_pixel: float = 0.0028
    scene_width_meters: float = 0.0
    scene_height_meters: float = 0.0
    
    # Category mapping
    person_categories: List[str] = field(default_factory=lambda: ["person"])
    index_to_category: Optional[Dict[int, str]] = None
    
    # Alert configuration
    alert_config: Optional[AlertConfig] = None
    
    def validate(self) -> List[str]:
        """Validate proximity detection configuration."""
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

@dataclass  
class CarServiceConfig(BaseConfig):
    """Configuration for car service use case."""
    
    # Area definitions
    car_areas: Dict[str, List[List[float]]] = field(default_factory=dict)
    staff_areas: Dict[str, List[List[float]]] = field(default_factory=dict)
    service_areas: Dict[str, List[List[float]]] = field(default_factory=dict)
    
    # Category identification
    staff_categories: List[str] = field(default_factory=lambda: ["staff", "employee"])
    car_categories: List[str] = field(default_factory=lambda: ["car"])
    
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
        
        if not self.car_categories:
            errors.append("car_categories cannot be empty")
        
        # Validate area polygons
        all_areas = {**self.car_categories, **self.staff_areas, **self.service_areas}
        for area_name, polygon in all_areas.items():
            if len(polygon) < 0:
                errors.append(f"Area '{area_name}' must have at least 0 points")
            
            for i, point in enumerate(polygon):
                if len(point) != 2:
                    errors.append(f"Area '{area_name}' point {i} must have exactly 2 coordinates")
        
        # Validate nested configurations
        if self.tracking_config:
            errors.extend(self.tracking_config.validate())
        
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        
        return errors
    

@dataclass
class LineConfig:
    """Configuration for line crossing detection."""
    
    # Line definition
    points: List[List[float]] = field(default_factory=list)  # Two points defining the line [[x1, y1], [x2, y2]]
    
    # Line-specific settings
    side1_label: str = field(default_factory=lambda: "Side1")  # Label for one side of the line
    side2_label: str = field(default_factory=lambda: "Side2")  # Label for the other side of the line
    crossing_categories: List[str] = field(default_factory=list)  # Categories to track for crossing
    
    def validate(self) -> List[str]:
        """Validate line configuration."""
        errors = []
        
        # Validate line points
        if len(self.points) != 2:
            errors.append("points must contain exactly 2 points")
        
        for i, point in enumerate(self.points):
            if not isinstance(point, (list, tuple)) or len(point) != 2:
                errors.append(f"Point {i} must have exactly 2 coordinates [x, y]")
            for j, coord in enumerate(point):
                if not isinstance(coord, (int, float)):
                    errors.append(f"Point {i} coordinate {j} must be a number")
        
        # Validate side labels
        if not self.side1_label:
            errors.append("side1_label must be a non-empty string")
        if not self.side2_label:
            errors.append("side2_label must be a non-empty string")
        if self.side1_label == self.side2_label:
            errors.append("side1_label and side2_label must be different")
        
        # Validate crossing categories
        if not self.crossing_categories:
            errors.append("crossing_categories cannot be empty")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "points": self.points,
            "side1_label": self.side1_label,
            "side2_label": self.side2_label,
            "crossing_categories": self.crossing_categories
        }
    
    # --- Legacy/dict-like compatibility helpers ---
    def _as_legacy_dict(self) -> Dict[str, Any]:
        return {
            "points": self.points,
            "side1_label": self.side1_label,
            "side2_label": self.side2_label,
            "crossing_categories": self.crossing_categories
        }
    
    def __getitem__(self, key: str) -> Any:  # Support config.line_config['points']
        return self._as_legacy_dict()[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._as_legacy_dict().get(key, default)
    
    def keys(self):
        return self._as_legacy_dict().keys()
    
    def items(self):
        return self._as_legacy_dict().items()
    
    def __contains__(self, key: object) -> bool:
        return key in self._as_legacy_dict()
    
    def __iter__(self):
        return iter(self._as_legacy_dict())
    
    def __len__(self) -> int:
        return len(self._as_legacy_dict())
    

@dataclass
class PeopleTrackingConfig(BaseConfig):
    """Configuration for People Tracking use case with polygon/abline counting."""

    # Counting method: "polygon" (double-polygon hysteresis) or "abline" (trap zone two-line)
    method: str = "polygon"

    # Use bottom-center (foot) of bbox for counting logic; False = bbox center
    use_foot_center: bool = True

    # --- Polygon method settings ---
    outer_polygon: Optional[List[List[float]]] = None  # [[x,y], ...] vertices
    inner_polygon: Optional[List[List[float]]] = None  # [[x,y], ...] vertices (auto-computed if None)
    inner_polygon_offset: int = 20  # Pixels to inset outer_polygon when inner_polygon is None

    # --- ABLine (trap zone) method settings ---
    line_a: Optional[List[float]] = None  # [x1, y1, x2, y2] or [[x1,y1],[x2,y2]]
    line_b: Optional[List[float]] = None  # [x1, y1, x2, y2] or [[x1,y1],[x2,y2]]
    in_direction: str = "A_to_B"  # "A_to_B" or "B_to_A"

    # --- Tracker ---
    enable_advanced_tracker: bool = True

    # --- Smoothing ---
    enable_smoothing: bool = False
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # --- Category / mapping ---
    person_categories: List[str] = field(default_factory=lambda: ["person", "people"])
    index_to_category: Optional[Dict[int, str]] = None

    # --- Counting ---
    enable_unique_counting: bool = True
    time_window_minutes: int = 60

    # --- Optional nested configs (kept for compatibility / future use) ---
    zone_config: Optional[ZoneConfig] = None
    line_config: Optional[LineConfig] = None
    alert_config: Optional[AlertConfig] = None

    def validate(self) -> List[str]:
        """Validate people tracking configuration."""
        errors = super().validate()

        if self.method not in ("polygon", "abline"):
            errors.append(f"method must be 'polygon' or 'abline', got '{self.method}'")

        if self.method == "polygon":
            if self.outer_polygon is None:
                errors.append("outer_polygon is required for polygon method")
            elif len(self.outer_polygon) < 3:
                errors.append("outer_polygon must have at least 3 points")

        if self.method == "abline":
            if self.line_a is None:
                errors.append("line_a is required for abline method")
            if self.line_b is None:
                errors.append("line_b is required for abline method")
            if self.in_direction not in ("A_to_B", "B_to_A"):
                errors.append(f"in_direction must be 'A_to_B' or 'B_to_A', got '{self.in_direction}'")

        if not self.person_categories:
            errors.append("person_categories cannot be empty")

        if self.zone_config:
            errors.extend(self.zone_config.validate())
        if self.alert_config:
            errors.extend(self.alert_config.validate())

        return errors


def filter_config_kwargs(config_class: type, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filter kwargs to only include parameters that are valid for the config class.
    
    Args:
        config_class: The config class to create
        kwargs: Dictionary of parameters to filter
        
    Returns:
        Dict[str, Any]: Filtered kwargs containing only valid parameters
    """
    if not hasattr(config_class, '__dataclass_fields__'):
        # Not a dataclass, return kwargs as-is
        return kwargs
    
    # Get valid field names from the dataclass
    valid_fields = set(config_class.__dataclass_fields__.keys())
    
    # Filter kwargs to only include valid fields
    filtered_kwargs = {}
    ignored_params = []
    
    for key, value in kwargs.items():
        if key in valid_fields:
            filtered_kwargs[key] = value
        else:
            ignored_params.append(key)
    
    # Log ignored parameters for debugging
    if ignored_params:
        logger.debug(
            f"Ignoring non-config parameters for {config_class.__name__}: {ignored_params}"
        )
    
    return filtered_kwargs


class ConfigManager:
    """Centralized configuration management for post-processing operations."""
    
    def __init__(self):
        """Initialize configuration manager."""
        self._config_classes = {
            "people_counting": PeopleCountingConfig,
            "customer_service": CustomerServiceConfig,
            "advanced_customer_service": CustomerServiceConfig,
            "intrusion_detection": IntrusionConfig,
            "proximity_detection": ProximityConfig,
            "basic_counting_tracking": None,  # Will be set later to avoid circular import
            "license_plate_detection": None,  # Will be set later to avoid circular import
            "ppe_compliance_detection": None,
            "color_detection": None,  # Will be set later to avoid circular import
            "video_color_classification": None,  # Alias for color_detection
            "drone_traffic_monitoring": None,
            "vehicle_monitoring" : None,
            "fire_smoke_detection": None,
            "flare_analysis" : None,
            "mask_detection": None,
            "pipeline_detection": None,
            "parking_space_detection": None,
            "car_damage_detection":None,
            "weld_defect_detection" : None,
            "banana_defect_detection" : None,
            "chicken_pose_detection" : None,
            "traffic_sign_monitoring" : None,
            "theft_detection" : None,
            "gender_detection": None,
            "solar_panel": None,
            "crop_weed_detection": None,
            "emergency_vehicle_detection": None,
            "shoplifting_detection":None,
            "price_tag_detection": None,
            "child_monitoring": None,
            "weapon_detection" : None,
            "concrete_crack_detection": None,
            "fashion_detection": None,
            "pothole_segmentation": None,
            "warehouse_object_segmentation": None,
            "shopping_cart_analysis": None,
            "defect_detection_products": None,
            'assembly_line_detection': None,
            'anti_spoofing_detection' : None,
            'shelf_inventory' : None,
            'wound_segmentation': None,
            'leaf_disease_detection': None,
            'field_mapping': None,
            'car_part_segmentation': None,
            'lane_detection' : None,
            'windmill_maintenance': None,
            'face_emotion': None,
            'flower_segmentation': None,
            'smoker_detection': None,
            'road_traffic_density': None,
            'road_view_segmentation': None,
            'face_recognition': None,
            'drowsy_driver_detection': None,
            'waterbody_segmentation': None,
            'litter_detection' :None,
            'abandoned_object_detection' : None,
            'litter_detection':None,
            'leak_detection': None,
            'human_activity_recognition': None,
            'gas_leak_detection': None,
            'license_plate_monitor' : None,
            'dwell' : None,
            'age_gender_detection': None,
            'wildlife_monitoring': None,
            'people_tracking' : PeopleTrackingConfig,
            'pcb_defect_detection': None,
            'underground_pipeline_defect' : None,
            'suspicious_activity_detection': None,
            'natural_disaster_detection': None,
            'footfall': None,
            'vehicle_monitoring_parking_lot': None,
            'vehicle_monitoring_drone_view': None,
            'parking_lot_analytics': None,
            'vehicle_monitoring_wrong_way': None,
            'crowdflow': None,
            'stopped_vehicle_monitoring': None,
            'area_utilization' : None,
            'heatmaps': None,
            'crowd_density_heatmaps': None,
            'loitering_detection' : None,
            'hazard_zone_entry' : None,
            'tailgating_detection': None,
            'vehicle_color_detection': None,
            'fall_detection': None,
            'running_detection': None,
            'liquid_leak_detection': None,
            'pipe_gas_leak_detection': None,
            'pipe_corrosion_detection': None,
            'overcrowding_detection': None,
            'animal_detection': None,
            'burglary_detection': None,
            'landslide_detection': None,

            #Put all image based usecases here::
            'blood_cancer_detection_img': None,
            'skin_cancer_classification_img': None,
            'plaque_segmentation_img': None,
            'cardiomegaly_classification': None,
            'histopathological_cancer_detection' : None,
            'cell_microscopy_segmentation': None,
            'people_counting_in_zone': None
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
    def _get_wound_segmentation_config_class(self):
        """Get LicensePlateConfig class to avoid circular imports."""
        try:
            from ..usecases.wound_segmentation import WoundConfig
            return WoundConfig
        except ImportError:
            return None
    def _get_leaf_disease_config_class(self):
        """Get LicensePlateConfig class to avoid circular imports."""
        try:
            from ..usecases.leaf_disease import LeafDiseaseDetectionConfig
            return LeafDiseaseDetectionConfig
        except ImportError:
            return None
    def _get_field_mapping_config_class(self):
        """Get LicensePlateConfig class to avoid circular imports."""
        try:
            from ..usecases.field_mapping import FieldMappingConfig
            return FieldMappingConfig
        except ImportError:
            return None

    def vehicle_monitoring_config_class(self):
        """Get vehicle monitoring class to avoid circular imports."""
        try:
            from ..usecases.vehicle_monitoring import VehicleMonitoringConfig
            return VehicleMonitoringConfig
        except ImportError:
            return None
    
    def drone_traffic_monitoring_config_class(self):
        """Get drone traffic monitoring class to avoid circular imports."""
        try:
            from ..usecases.drone_traffic_monitoring import VehiclePeopleDroneMonitoringConfig
            return VehiclePeopleDroneMonitoringConfig
        except ImportError:
            return None
        
    def banana_defect_detection_config_class(self):
        """Get Banana monitoring class to avoid circular imports."""
        try:
            from ..usecases.banana_defect_detection import BananaMonitoringConfig
            return BananaMonitoringConfig
        except ImportError:
            return None
        
    def lane_detection_config_class(self):
        """Get road lane monitoring class to avoid circular imports."""
        try:
            from ..usecases.road_lane_detection import LaneDetectionConfig
            return LaneDetectionConfig
        except ImportError:
            return None
        
    def shelf_inventory_config_class(self):
        """Get inventory monitoring class to avoid circular imports."""
        try:
            from ..usecases.shelf_inventory_detection import ShelfInventoryUseCase
            return ShelfInventoryUseCase
        except ImportError:
            return None
        
    def anti_spoofing_detection_config_class(self):
        """Get Anti-Spoofing class to avoid circular imports."""
        try:
            from ..usecases.anti_spoofing_detection import AntiSpoofingDetectionConfig
            return AntiSpoofingDetectionConfig
        except ImportError:
            return None
        
    def theft_detection_config_class(self):
        """Get  theft detection class to avoid circular imports."""
        try:
            from ..usecases.theft_detection import TheftDetectionConfig
            return TheftDetectionConfig
        except ImportError:
            return None
        
    def weapon_tracking_config_class(self):
        """Get  weapon detection class to avoid circular imports."""
        try:
            from ..usecases.weapon_detection import WeaponDetectionConfig
            return WeaponDetectionConfig
        except ImportError:
            return None
        
    def traffic_sign_monitoring_config_class(self):
        """Get traffic sign monitoring class to avoid circular imports."""
        try:
            from ..usecases.traffic_sign_monitoring import TrafficSignMonitoringConfig
            return TrafficSignMonitoringConfig
        except ImportError:
            return None
        
    def chicken_pose_detection_config_class(self):
        """Get Chicken pose monitoring class to avoid circular imports."""
        try:
            from ..usecases.chicken_pose_detection import ChickenPoseDetectionConfig
            return ChickenPoseDetectionConfig
        except ImportError:
            return None

    def _get_fire_smoke_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.fire_detection import FireSmokeConfig
            return FireSmokeConfig
        except ImportError:
            return None

    def _get_shoplifting_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.shoplifting_detection import ShopliftingDetectionConfig
            return ShopliftingDetectionConfig
        except ImportError:
            return None
    

    def _get_car_damage_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.car_damage_detection import CarDamageConfig
            return CarDamageConfig
        except ImportError:
            return None


    def _get_parking_space_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.parking_space_detection import ParkingSpaceConfig
            return ParkingSpaceConfig
        except ImportError:
            return None

    def _get_mask_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.mask_detection import MaskDetectionConfig
            return MaskDetectionConfig
        except ImportError:
            return None

    def _get_pipeline_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.pipeline_detection import PipelineDetectionConfig
            return PipelineDetectionConfig
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
    
    def face_emotion_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.face_emotion import FaceEmotionConfig
            return FaceEmotionConfig
        except ImportError:
            return None
    
    def underwater_pollution_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.underwater_pollution_detection import UnderwaterPlasticConfig
            return UnderwaterPlasticConfig
        except ImportError:
            return None

    def pedestrian_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.pedestrian_detection import PedestrianDetectionConfig
            return PedestrianDetectionConfig
        except ImportError:
            return None
    
    def age_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.age_detection import AgeDetectionConfig
            return AgeDetectionConfig
        except ImportError:
            return None
        
    def weld_defect_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.weld_defect_detection import WeldDefectConfig
            return WeldDefectConfig
        except ImportError:
            return None
        
    def price_tag_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.price_tag_detection import PriceTagConfig
            return PriceTagConfig
        except ImportError:
            return None
    
    def distracted_driver_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.distracted_driver_detection import DistractedDriverConfig
            return DistractedDriverConfig
        except ImportError:
            return None
        
    def emergency_vehicle_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.emergency_vehicle_detection import EmergencyVehicleConfig
            return EmergencyVehicleConfig
        except ImportError:
            return None
    
    def solar_panel_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.solar_panel import SolarPanelConfig
            return SolarPanelConfig
        except ImportError:
            return None
        
    def crop_weed_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.crop_weed_detection import CropWeedDetectionConfig
            return CropWeedDetectionConfig
        except ImportError:
            return None
    
    def child_monitoring_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.child_monitoring import ChildMonitoringConfig
            return ChildMonitoringConfig
        except ImportError:
            return None
        
    def gender_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.gender_detection import GenderDetectionConfig
            return GenderDetectionConfig
        except ImportError:
            return None
    
    def concrete_crack_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.concrete_crack_detection import ConcreteCrackConfig
            return ConcreteCrackConfig
        except ImportError:
            return None
        
    def fashion_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.fashion_detection import FashionDetectionConfig
            return FashionDetectionConfig
        except ImportError:
            return None
    
    def warehouse_object_segmentation_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.warehouse_object_segmentation import WarehouseObjectConfig
            return WarehouseObjectConfig
        except ImportError:
            return None
    
    def shopping_cart_analysis_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.shopping_cart_analysis import ShoppingCartAnalysisConfig
            return ShoppingCartAnalysisConfig
        except ImportError:
            return None
    
    def defect_detection_products_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.defect_detection_products import BottleDefectConfig
            return BottleDefectConfig
        except ImportError:
            return None
        
    def assembly_line_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.assembly_line_detection import AssemblyLineConfig
            return AssemblyLineConfig
        except ImportError:
            return None
    
    def car_part_segmentation_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.car_part_segmentation import CarPartSegmentationConfig
            return CarPartSegmentationConfig
        except ImportError:
            return None
        
    def windmill_maintenance_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.windmill_maintenance import WindmillMaintenanceConfig
            return WindmillMaintenanceConfig
        except ImportError:
            return None
    
    def flower_segmentation_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.flower_segmentation import FlowerConfig
            return FlowerConfig
        except ImportError:
            return None
    
    def smoker_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.smoker_detection import SmokerDetectionConfig
            return SmokerDetectionConfig
        except ImportError:
            return None
    
    def road_traffic_density_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.road_traffic_density import RoadTrafficConfig
            return RoadTrafficConfig
        except ImportError:
            return None
    
    def road_view_segmentation_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.road_view_segmentation import RoadViewSegmentationConfig
            return RoadViewSegmentationConfig
        except ImportError:
            return None
    
    def face_recognition_config_class(self):
        """Register a configuration class for a use case."""
        try:
            # from ..usecases.face_recognition import FaceRecognitionConfig
            # return FaceRecognitionConfig
            from ..face_reg.face_recognition import FaceRecognitionEmbeddingConfig
            
            return FaceRecognitionEmbeddingConfig
        except ImportError:
            return None
    
    def drowsy_driver_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.drowsy_driver_detection import DrowsyDriverConfig
            return DrowsyDriverConfig
        except ImportError:
            return None
    
    def waterbody_segmentation_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.waterbody_segmentation import WaterBodyConfig
            return WaterBodyConfig
        except ImportError:
            return None
        
    def litter_detection_config_class(self):
        """Get Litter monitoring class to avoid circular imports."""
        try:
            from ..usecases.litter_monitoring import LitterDetectionConfig
            return LitterDetectionConfig
        except ImportError:
            return None
        

    def abandoned_object_detection_config_class(self):
        """Get monitoring class to avoid circular imports."""
        try:
            from ..usecases.abandoned_object_detection import AbandonedObjectConfig
            return AbandonedObjectConfig
        except ImportError:
            return None
        
    def leak_detection_config_class(self):
        """Get Leak detection class to avoid circular imports."""
        try:
            from ..usecases.leak_detection import LeakDetectionConfig
            return LeakDetectionConfig
        except ImportError:
            return None
    
    def human_activity_recognition_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.human_activity_recognition import HumanActivityConfig
            return HumanActivityConfig
        except ImportError:
            return None

    def license_plate_monitor_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.license_plate_monitoring import LicensePlateMonitorConfig
            return LicensePlateMonitorConfig
        except ImportError:
            return None
        
    def dwell_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.dwell_detection import DwellConfig
            return DwellConfig
        except ImportError:
            return None
    
    def gas_leak_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.gas_leak_detection import GasLeakDetectionConfig
            return GasLeakDetectionConfig
        except ImportError:
            return None
    
    def age_gender_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.age_gender_detection import AgeGenderConfig
            return AgeGenderConfig
        except ImportError:
            return None
    
    def wildlife_monitoring_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.wildlife_monitoring import WildLifeMonitoringConfig
            return WildLifeMonitoringConfig
        except ImportError:
            return None
    
    def pcb_defect_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.pcb_defect_detection import PCBDefectConfig
            return PCBDefectConfig
        except ImportError:
            return None
    
    def suspicious_activity_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.suspicious_activity_detection import SusActivityConfig
            return SusActivityConfig
        except ImportError:
            return None
    
    def natural_disaster_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.natural_disaster import NaturalDisasterConfig
            return NaturalDisasterConfig
        except ImportError:
            return None
        
    def footfall_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.footfall import FootFallConfig
            return FootFallConfig
        except ImportError:
            return None
        
    def vehicle_monitoring_parking_lot_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.vehicle_monitoring_parking_lot import VehicleMonitoringParkingLotConfig
            return VehicleMonitoringParkingLotConfig
        except ImportError:
            return None
        
    def vehicle_monitoring_drone_view_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.vehicle_monitoring_drone_view import VehicleMonitoringDroneViewConfig
            return VehicleMonitoringDroneViewConfig
        except ImportError:
            return None
        
    def parking_lot_analytics_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.parking_lot_analytics import ParkingLotAnalyticsConfig
            return ParkingLotAnalyticsConfig
        except ImportError:
            return None
        
    def crowdflow_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.crowdflow import CrowdflowConfig
            return CrowdflowConfig
        except ImportError:
            return None
        
    def heatmaps_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.heatmaps import HeatMapsConfig
            return HeatMapsConfig
        except ImportError:
            return None
        
    def crowd_density_heatmaps_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.crowd_density_heatmaps import CrowdDensityHeatMapsConfig
            return CrowdDensityHeatMapsConfig
        except ImportError:
            return None
        
    def hazard_zone_entry_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.hazard_zone_entry import HazardZoneEntryConfig
            return HazardZoneEntryConfig
        except ImportError:
            return None
    
        
    def vehicle_monitoring_wrong_way_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.vehicle_monitoring_wrong_way import VehicleMonitoringWrongWayConfig
            return VehicleMonitoringWrongWayConfig
        except ImportError:
            return None

    def area_utilization_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.area_utilization import AreaUtilizationConfig
            return AreaUtilizationConfig
        except ImportError:
            return None
        
    def stopped_vehicle_monitoring_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.stopped_vehicle_monitoring import StoppedVehicleMonitoringConfig
            return StoppedVehicleMonitoringConfig
        except ImportError:
            return None

    def loitering_detection_config_class(self):
        try:
            from ..usecases.loitering_detection import LoiteringConfig
            return LoiteringConfig
        except ImportError:
            return None
        
    def tailgating_detection_config_class(self):
        try:
            from ..usecases.tailgating_detection import TailgatingConfig
            return TailgatingConfig
        except ImportError:
            return None
        
    def vehicle_color_detection_config_class(self):
        try:
            from ..usecases.vehicle_color_detection import VehicleColorDetectionConfig
            return VehicleColorDetectionConfig
        except ImportError:
            return None
        
    def fall_detection_config_class(self):
        try:
            from ..usecases.fall_detection import FallDetectionConfig
            return FallDetectionConfig
        except ImportError:
            return None
    
    def running_detection_config_class(self):
        try:
            from ..usecases.running_detection import RunningDetectionConfig
            return RunningDetectionConfig
        except ImportError:
            return None
        
    def liquid_leak_detection_config_class(self):
        try:
            from ..usecases.liquid_leak_detection import LiquidLeakDetectionConfig
            return LiquidLeakDetectionConfig
        except ImportError:
            return None

    def people_counting_in_zone_config_class(self):
        try:
            from ..usecases.people_counting_in_zone import PeopleCountingInZoneConfig
            return PeopleCountingInZoneConfig
        except ImportError:
            return None
        
    def pipe_gas_leak_detection_config_class(self):
        try:
            from ..usecases.pipe_gas_leak_detection import PipeGasLeakDetectionConfig
            return PipeGasLeakDetectionConfig
        except ImportError:
            return None
    
    def pipe_corrosion_detection_config_class(self):
        try:
            from ..usecases.pipe_corrosion_detection import PipeCorrosionDetectionConfig
            return PipeCorrosionDetectionConfig
        except ImportError:
            return None

    def overcrowding_detection_config_class(self):
        try:
            from ..usecases.overcrowding_detection import OvercrowdingDetectionConfig
            return OvercrowdingDetectionConfig
        except ImportError:
            return None
    
    def animal_detection_config_class(self):
        try:
            from ..usecases.animal_detection import AnimalDetectionConfig
            return AnimalDetectionConfig
        except ImportError:
            return None

    def burglary_detection_config_class(self):
        try:
            from ..usecases.burglary_detection import BurglaryDetectionConfig
            return BurglaryDetectionConfig
        except ImportError:
            return None

    def landslide_detection_config_class(self):
        try:
            from ..usecases.landslide_detection import LandslideDetectionConfig
            return LandslideDetectionConfig
        except ImportError:
            return None
        
    #put all image based usecases here::
    def blood_cancer_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.blood_cancer_detection_img import BloodCancerDetectionConfig
            return BloodCancerDetectionConfig
        except ImportError:
            return None
    
    def plaque_segmentation_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.plaque_segmentation_img import PlaqueSegmentationConfig
            return PlaqueSegmentationConfig
        except ImportError:
            return None
        
    def skin_cancer_classification_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.skin_cancer_classification_img import SkinCancerClassificationConfig
            return SkinCancerClassificationConfig
        except ImportError:
            return None
    
    def cardiomegaly_classification_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.cardiomegaly_classification import CardiomegalyConfig
            return CardiomegalyConfig
        except ImportError:
            return None
        
    def histopathological_cancer_detection_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.Histopathological_Cancer_Detection_img import HistopathologicalCancerDetectionConfig
            return HistopathologicalCancerDetectionConfig
        except ImportError:
            return None
        
    def cell_microscopy_segmentation_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.cell_microscopy_segmentation import CellMicroscopyConfig
            return CellMicroscopyConfig
        except ImportError:
            return None
    
    def underground_pipeline_defect_config_class(self):
        """Register a configuration class for a use case."""
        try:
            from ..usecases.underground_pipeline_defect_detection import UndergroundPipelineDefectConfig
            return UndergroundPipelineDefectConfig
        except ImportError:
            return None

    def _filter_kwargs_for_config(self, config_class: type, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter kwargs to only include valid parameters for the config class.
        
        Args:
            config_class: The config class
            kwargs: Dictionary of parameters
            
        Returns:
            Filtered kwargs
        """
        return filter_config_kwargs(config_class, kwargs)
    
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
        # Filter out common non-config parameters that should never be passed to configs
        common_non_config_params = [
            'deployment_id', 'stream_key', 'stream_id', 'camera_id', 'server_id',
            'inference_id', 'timestamp', 'frame_id', 'frame_number', 'request_id',
            'user_id', 'tenant_id', 'organization_id', 'app_name', 'app_id'
        ]
        for param in common_non_config_params:
            if param in kwargs:
                logger.debug(f"Removing non-config parameter '{param}' from config creation")
                kwargs.pop(param, None)
        
        if usecase == "people_counting":
            # Handle nested configurations
            zone_config = kwargs.pop("zone_config", None)
            if zone_config and isinstance(zone_config, dict):
                zone_config = ZoneConfig(**zone_config)

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(PeopleCountingConfig, kwargs)
            
            config = PeopleCountingConfig(
                category=category or "general",
                usecase=usecase,
                zone_config=zone_config,
                alert_config=alert_config,
                **filtered_kwargs
            )
        elif usecase == "people_counting_in_zone":
           
            # Handle nested configurations
            zone_config = kwargs.pop("zone_config", None)
            if zone_config and isinstance(zone_config, dict):
                zone_config = ZoneConfig(**zone_config)

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(PeopleCountingConfig, kwargs)
            
            config = PeopleCountingConfig(
                category=category or "general",
                usecase=usecase,
                zone_config=zone_config,
                alert_config=alert_config,
                **filtered_kwargs
            )

        elif usecase == "people_tracking":
            # Handle nested configurations
            zone_config = kwargs.pop("zone_config", None)
            if zone_config and isinstance(zone_config, dict):
                zone_config = ZoneConfig(**zone_config)

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(PeopleTrackingConfig, kwargs)
            
            config = PeopleTrackingConfig(
                category=category or "general",
                usecase=usecase,
                zone_config=zone_config,
                alert_config=alert_config,
                **filtered_kwargs
            )
        
        elif usecase == "intrusion_detection":
            # Handle nested configurations
            zone_config = kwargs.pop("zone_config", None)
            if zone_config and isinstance(zone_config, dict):
                zone_config = ZoneConfig(**zone_config)

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(IntrusionConfig, kwargs)
            
            config = IntrusionConfig(
                category=category or "security",
                usecase=usecase,
                zone_config=zone_config,
                alert_config=alert_config,
                **filtered_kwargs
            )
        
        elif usecase == "proximity_detection":
            # Handle nested configurations
            zone_config = kwargs.pop("zone_config", None)
            if zone_config and isinstance(zone_config, dict):
                zone_config = ZoneConfig(**zone_config)

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(ProximityConfig, kwargs)
            
            config = ProximityConfig(
                category=category or "security",
                usecase=usecase,
                zone_config=zone_config,
                alert_config=alert_config,
                **filtered_kwargs
            )

        elif usecase in ["customer_service", "advanced_customer_service"]:
            # Handle nested configurations
            tracking_config = kwargs.pop("tracking_config", None)
            if tracking_config and isinstance(tracking_config, dict):
                tracking_config = TrackingConfig(**tracking_config)

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(CustomerServiceConfig, kwargs)
            
            config = CustomerServiceConfig(
                category=category or "sales",
                usecase=usecase,
                tracking_config=tracking_config,
                alert_config=alert_config,
                **filtered_kwargs
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

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(BasicCountingTrackingConfig, kwargs)
            
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
                **filtered_kwargs
            )
        elif usecase == "license_plate_detection":
            # Import here to avoid circular import
            from ..usecases.license_plate_detection import LicensePlateConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(LicensePlateConfig, kwargs)
            
            config = LicensePlateConfig(
                category=category or "vehicle",
                usecase=usecase,
                alert_config=alert_config,
                **filtered_kwargs
            )
        elif usecase == "parking_space_detection":
            # Import here to avoid circular import
            from ..usecases.parking_space_detection import ParkingSpaceConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(ParkingSpaceConfig, kwargs)
            
            config = ParkingSpaceConfig(
                category=category or "parking_space",
                usecase=usecase,
                alert_config=alert_config,
                **filtered_kwargs
            )
        elif usecase == "field_mapping":
            # Import here to avoid circular import
            from ..usecases.field_mapping import FieldMappingConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(FieldMappingConfig, kwargs)
            
            config = FieldMappingConfig(
                category=category or "infrastructure",
                usecase=usecase,
                alert_config=alert_config,
                **filtered_kwargs
            )

        elif usecase == "leaf_disease_detection":
            # Import here to avoid circular import
            from ..usecases.leaf_disease import LeafDiseaseDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(LeafDiseaseDetectionConfig, kwargs)

            config = LeafDiseaseDetectionConfig(
                category=category or "agriculture",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "mask_detection":
            # Import here to avoid circular import
            from ..usecases.mask_detection import MaskDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = MaskDetectionConfig(
                category=category or "mask_detection",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "pipeline_detection":
            from ..usecases.pipeline_detection import PipelineDetectionConfig

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = PipelineDetectionConfig(
                category=category or "pipeline_detection",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "shoplifting_detection":
            # Import here to avoid circular import
            from ..usecases.shoplifting_detection import ShopliftingDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = ShopliftingDetectionConfig(
                category=category or "mask_detection",
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
        
        elif usecase == "solar_panel":
            # Import here to avoid circular import
            from ..usecases.solar_panel import SolarPanelConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = SolarPanelConfig(
                category=category or "energy",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "wound_segmentation":
            # Import here to avoid circular import
            from ..usecases.wound_segmentation import WoundConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = WoundConfig(
                category=category or "energy",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "car_damage_detection":
            # Import here to avoid circular import
            from ..usecases.car_damage_detection import CarDamageConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = CarDamageConfig(
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

        elif usecase == "chicken_pose_detection":
            # Import here to avoid circular import
            from ..usecases.chicken_pose_detection import ChickenPoseDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = ChickenPoseDetectionConfig(
                category=category or "agriculture",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "fruit_monitoring":
            # Import here to avoid circular import
            from ..usecases.banana_defect_detection import BananaMonitoringConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = BananaMonitoringConfig(
                category=category or "agriculture",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "abandoned_object_detection":
            # Import here to avoid circular import
            from ..usecases.abandoned_object_detection import AbandonedObjectConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = AbandonedObjectConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "lane_detection":
            # Import here to avoid circular import
            from ..usecases.road_lane_detection import LaneDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = LaneDetectionConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "shelf_inventory":
            # Import here to avoid circular import
            from ..usecases.shelf_inventory_detection import ShelfInventoryConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = ShelfInventoryConfig(
                category=category or "retail",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "anti_spoofing_detection":
            # Import here to avoid circular import
            from ..usecases.anti_spoofing_detection import AntiSpoofingDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = AntiSpoofingDetectionConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "theft_detection":
            # Import here to avoid circular import
            from ..usecases.theft_detection import TheftDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = TheftDetectionConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "weapon_detection":
            # Import here to avoid circular import
            from ..usecases.weapon_detection import WeaponDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = WeaponDetectionConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "traffic_sign_monitoring":
            # Import here to avoid circular import
            from ..usecases.traffic_sign_monitoring import TrafficSignMonitoringConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = TrafficSignMonitoringConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "vehicle_monitoring":
            # Import here to avoid circular import
            from ..usecases.vehicle_monitoring import VehicleMonitoringConfig

            # Handle nested configurations
            zone_config = kwargs.pop("zone_config", None)
            # VehicleMonitoringConfig expects zone_config as Dict, not ZoneConfig object
            # If it's a ZoneConfig object, convert it to dict
            if zone_config and hasattr(zone_config, 'to_dict'):
                zone_config = zone_config.to_dict()
            elif zone_config and isinstance(zone_config, ZoneConfig):
                zone_config = {"zones": zone_config.zones} if zone_config.zones else None

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(VehicleMonitoringConfig, kwargs)

            config = VehicleMonitoringConfig(
                category=category or "traffic",
                usecase=usecase,
                zone_config=zone_config,
                alert_config=alert_config,
                **filtered_kwargs
            )
        
        elif usecase == "drone_traffic_monitoring":
            # Import here to avoid circular import
            from ..usecases.drone_traffic_monitoring import VehiclePeopleDroneMonitoringConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = VehiclePeopleDroneMonitoringConfig(
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

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(ColorDetectionConfig, kwargs)

            config = ColorDetectionConfig(
                category=category or "visual_appearance",
                usecase=usecase,
                alert_config=alert_config,
                **filtered_kwargs
            )
        elif usecase == "video_color_classification":
            # Alias for color_detection - Import here to avoid circular import
            from ..usecases.color_detection import ColorDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(ColorDetectionConfig, kwargs)

            config = ColorDetectionConfig(
                category=category or "visual_appearance",
                usecase="color_detection",  # Use canonical name internally
                alert_config=alert_config,
                **filtered_kwargs
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
        elif usecase == "face_emotion":
            # Import here to avoid circular import
            from ..usecases.face_emotion import FaceEmotionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = FaceEmotionConfig(
                category=category or "general",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "pedestrian_detection":
            # Import here to avoid circular import
            from ..usecases.pedestrian_detection import PedestrianDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)
            config = PedestrianDetectionConfig(
                category=category or "pedestrian",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )


        elif usecase == "underwater_pollution_detection":
            # Import here to avoid circular import
            from ..usecases.underwater_pollution_detection import UnderwaterPlasticConfig
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)
            config = UnderwaterPlasticConfig(
                category=category or "pollution",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "weld_defect_detection":
            # Import here to avoid circular import
            from ..usecases.weld_defect_detection import WeldDefectConfig
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)
            config = WeldDefectConfig(
                category=category or "weld",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "age_detection":
            # Import here to avoid circular import
            from ..usecases.age_detection import AgeDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = AgeDetectionConfig(
                category=category or "general",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "price_tag_detection":
            # Import here to avoid circular import
            from ..usecases.price_tag_detection import PriceTagConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = PriceTagConfig(
                category=category or "retail",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "distracted_driver_detection":
            # Import here to avoid circular import
            from ..usecases.distracted_driver_detection import DistractedDriverConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = DistractedDriverConfig(
                category=category or "automobile",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "emergency_vehicle_detection":
            # Import here to avoid circular import
            from ..usecases.emergency_vehicle_detection import EmergencyVehicleConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = EmergencyVehicleConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "crop_weed_detection":
            # Import here to avoid circular import
            from ..usecases.crop_weed_detection import CropWeedDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = CropWeedDetectionConfig(
                category=category or "agriculture",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "child_monitoring":
            # Import here to avoid circular import
            from ..usecases.child_monitoring import ChildMonitoringConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = ChildMonitoringConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "gender_detection":
            # Import here to avoid circular import 
            from ..usecases.gender_detection import GenderDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)
            
            config = GenderDetectionConfig(
                category=category or "general",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "concrete_crack_detection":
            # Import here to avoid circular import
            from ..usecases.concrete_crack_detection import ConcreteCrackConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = ConcreteCrackConfig(
                category=category or "general",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "fashion_detection":
            # Import here to avoid circular import
            from ..usecases.fashion_detection import FashionDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = FashionDetectionConfig(
                category=category or "retail",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "warehouse_object_segmentation":
            # Import here to avoid circular import
            from ..usecases.warehouse_object_segmentation import WarehouseObjectConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = WarehouseObjectConfig(
                category=category or "retail",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "shopping_cart_analysis":
            # Import here to avoid circular import
            from ..usecases.shopping_cart_analysis import ShoppingCartConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = ShoppingCartConfig(
                category=category or "retail",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "defect_detection_products":
            # Import here to avoid circular import
            from ..usecases.defect_detection_products import BottleDefectConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = BottleDefectConfig(
                category=category or "retail",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "assembly_line_detection":
            # Import here to avoid circular import
            from ..usecases.assembly_line_detection import AssemblyLineConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = AssemblyLineConfig(
                category=category or "manufacturing",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "car_part_segmentation":
            # Import here to avoid circular import
            from ..usecases.car_part_segmentation import CarPartSegmentationConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = CarPartSegmentationConfig(
                category=category or "automobile",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "windmill_maintenance":
            # Import here to avoid circular import
            from ..usecases.windmill_maintenance import WindmillMaintenanceConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = WindmillMaintenanceConfig(
                category=category or "manufacturing",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "flower_segmentation":
            # Import here to avoid circular import
            from ..usecases.flower_segmentation import FlowerConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = FlowerConfig(
                category=category or "agriculture",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "smoker_detection":
            # Import here to avoid circular import
            from ..usecases.smoker_detection import SmokerDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = SmokerDetectionConfig(
                category=category or "general",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "road_traffic_density":
            # Import here to avoid circular import
            from ..usecases.road_traffic_density import RoadTrafficConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = RoadTrafficConfig(
                category=category or "automobile",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "road_view_segmentation":
            # Import here to avoid circular import
            from ..usecases.road_view_segmentation import RoadViewSegmentationConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = RoadViewSegmentationConfig(
                category=category or "automobile",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "face_recognition":
            # Import here to avoid circular import
            from ..face_reg.face_recognition import FaceRecognitionEmbeddingConfig
            
            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = FaceRecognitionEmbeddingConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
            return config
        elif usecase == "drowsy_driver_detection":
            # Import here to avoid circular import
            from ..usecases.drowsy_driver_detection import DrowsyDriverConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = DrowsyDriverConfig(
                category=category or "automobile",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "waterbody_segmentation":
            # Import here to avoid circular import
            from ..usecases.waterbody_segmentation import WaterBodyConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = WaterBodyConfig(
                category=category or "agriculture",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "litter_detection":
            # Import here to avoid circular import
            from ..usecases.litter_monitoring import LitterDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = LitterDetectionConfig(
                category=category or "litter_detection",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "leak_detection":
            # Import here to avoid circular import
            from ..usecases.leak_detection import LeakDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = LeakDetectionConfig(
                category=category or "oil_gas",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "human_activity_recognition":
            # Import here to avoid circular import
            from ..usecases.human_activity_recognition import HumanActivityConfig

            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = HumanActivityConfig(
                category=category or "general",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
            
        elif usecase == "gas_leak_detection":
            # Import here to avoid circular import
            from ..usecases.gas_leak_detection import GasLeakDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = GasLeakDetectionConfig(
                category=category or "oil_gas",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "license_plate_monitor":
            # Import here to avoid circular import
            from ..usecases.license_plate_monitoring import LicensePlateMonitorConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            # Filter kwargs to only include valid parameters
            filtered_kwargs = self._filter_kwargs_for_config(LicensePlateMonitorConfig, kwargs)
            
            config = LicensePlateMonitorConfig(
                category=category or "license_plate_monitor",
                usecase=usecase,
                alert_config=alert_config,
                **filtered_kwargs
            )

        elif usecase == "dwell":
            # Import here to avoid circular import
            from ..usecases.dwell_detection import DwellConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = DwellConfig(
                category=category or "general",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "age_gender_detection":
            # Import here to avoid circular import
            from ..usecases.age_gender_detection import AgeGenderConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = AgeGenderConfig(
                category=category or "age_gender_detection",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "wildlife_monitoring":
            # Import here to avoid circular import
            from ..usecases.wildlife_monitoring import WildLifeMonitoringConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = WildLifeMonitoringConfig(
                category=category or "environmental",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "pcb_defect_detection":
            # Import here to avoid circular import
            from ..usecases.pcb_defect_detection import PCBDefectConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = PCBDefectConfig(
                category=category or "manufacturing",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "suspicious_activity_detection":
            # Import here to avoid circular import
            from ..usecases.suspicious_activity_detection import SusActivityConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = SusActivityConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "natural_disaster_detection":
            # Import here to avoid circular import
            from ..usecases.natural_disaster import NaturalDisasterConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = NaturalDisasterConfig(
                category=category or "environmental",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "footfall":
            # Import here to avoid circular import
            from ..usecases.footfall import FootFallConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = FootFallConfig(
                category=category or "retail",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "vehicle_monitoring_parking_lot":
            # Import here to avoid circular import
            from ..usecases.vehicle_monitoring_parking_lot import VehicleMonitoringParkingLotConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = VehicleMonitoringParkingLotConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "vehicle_monitoring_drone_view":
            # Import here to avoid circular import
            from ..usecases.vehicle_monitoring_drone_view import VehicleMonitoringDroneViewConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = VehicleMonitoringDroneViewConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "parking_lot_analytics":
            # Import here to avoid circular import
            from ..usecases.parking_lot_analytics import ParkingLotAnalyticsConfig

             # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = ParkingLotAnalyticsConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "area_utilization":
            # Import here to avoid circular import
            from ..usecases.area_utilization import AreaUtilizationConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = AreaUtilizationConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "crowdflow":
            # Import here to avoid circular import
            from ..usecases.crowdflow import CrowdflowConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)
            
            config = CrowdflowConfig(
                category=category or "retail",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "heatmaps":
            # Import here to avoid circular import
            from ..usecases.heatmaps import HeatMapsConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = HeatMapsConfig(
                category=category or "retail",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "crowd_density_heatmaps":
            # Import here to avoid circular import
            from ..usecases.crowd_density_heatmaps import CrowdDensityHeatMapsConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = CrowdDensityHeatMapsConfig(
                category=category or "retail",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "hazard_zone_entry":
            # Import here to avoid circular import
            from ..usecases.hazard_zone_entry import HazardZoneEntryConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = HazardZoneEntryConfig(
                category=category or "general",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
            

        elif usecase == "vehicle_monitoring_wrong_way":
            # Import here to avoid circular import
            from ..usecases.vehicle_monitoring_wrong_way import VehicleMonitoringWrongWayConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = VehicleMonitoringWrongWayConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "stopped_vehicle_monitoring":
            # Import here to avoid circular import
            from ..usecases.stopped_vehicle_monitoring import StoppedVehicleMonitoringConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = StoppedVehicleMonitoringConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "loitering_detection":
            # Import here to avoid circular import
            from ..usecases.loitering_detection import LoiteringConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = LoiteringConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "tailgating_detection":
            # Import here to avoid circular import
            from ..usecases.tailgating_detection import TailgatingConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = TailgatingConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "liquid_leak_detection":
            # Import here to avoid circular import
            from ..usecases.liquid_leak_detection import LiquidLeakDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = LiquidLeakDetectionConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "vehicle_color_detection":
            # Import here to avoid circular import
            from ..usecases.vehicle_color_detection import VehicleColorDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = VehicleColorDetectionConfig(
                category=category or "traffic",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "fall_detection":   
            # Import here to avoid circular import
            from ..usecases.fall_detection import FallDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = FallDetectionConfig(
                category=category or "general",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "running_detection":
            # Import here to avoid circular import
            from ..usecases.running_detection import RunningDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = RunningDetectionConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "pipe_gas_leak_detection":
            # Import here to avoid circular import
            from ..usecases.pipe_gas_leak_detection import PipeGasLeakDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = PipeGasLeakDetectionConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "pipe_corrosion_detection":
            # Import here to avoid circular import
            from ..usecases.pipe_corrosion_detection import PipeCorrosionDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = PipeCorrosionDetectionConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == 'overcrowding_detection':
            # Import here to avoid circular import
            from ..usecases.overcrowding_detection import OvercrowdingDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = OvercrowdingDetectionConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "animal_detection":
            # Import here to avoid circular import
            from ..usecases.animal_detection import AnimalDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = AnimalDetectionConfig(
                category=category or "environmental",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "burglary_detection":
            # Import here to avoid circular import
            from ..usecases.burglary_detection import BurglaryDetectionConfig
            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = BurglaryDetectionConfig(
                category=category or "security",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        
        elif usecase == "landslide_detection":
            # Import here to avoid circular import
            from ..usecases.landslide_detection import LandslideDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = LandslideDetectionConfig(
                category=category or "environmental",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        #Add IMAGE based usecases here::
        elif usecase == "blood_cancer_detection_img":
            # Import here to avoid circular import
            from ..usecases.blood_cancer_detection_img import BloodCancerDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = BloodCancerDetectionConfig(
                category=category or "healthcare",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "skin_cancer_classification_img":
            # Import here to avoid circular import
            from ..usecases.skin_cancer_classification_img import SkinCancerClassificationConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = SkinCancerClassificationConfig(
                category=category or "healthcare",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "plaque_segmentation_img":
            # Import here to avoid circular import
            from ..usecases.plaque_segmentation_img import PlaqueSegmentationConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = PlaqueSegmentationConfig(
                category=category or "healthcare",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "cardiomegaly_classification":
            # Import here to avoid circular import
            from ..usecases.cardiomegaly_classification import CardiomegalyConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = CardiomegalyConfig(
                category=category or "healthcare",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "histopathological_cancer_detection":
            # Import here to avoid circular import
            from ..usecases.Histopathological_Cancer_Detection_img import HistopathologicalCancerDetectionConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = HistopathologicalCancerDetectionConfig(
                category=category or "healthcare",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )
        elif usecase == "cell_microscopy_segmentation":
            # Import here to avoid circular import
            from ..usecases.cell_microscopy_segmentation import CellMicroscopyConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = CellMicroscopyConfig(
                category=category or "healthcare",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )


        elif usecase == "underground_pipeline_defect":
            # Import here to avoid circular import
            from ..usecases.underground_pipeline_defect_detection import UndergroundPipelineDefectConfig

            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)

            config = UndergroundPipelineDefectConfig(
                category=category or "underground_pipeline_defect",
                usecase=usecase,
                alert_config=alert_config,
                **kwargs
            )

        elif usecase == "area_utilization":
            # Import here to avoid circular import
            from ..usecases.area_utilization import AreaUtilizationConfig
            # Handle nested configurations
            alert_config = kwargs.pop("alert_config", None)
            if alert_config and isinstance(alert_config, dict):
                alert_config = AlertConfig(**alert_config)
            
            config = AreaUtilizationConfig(
                category=category or "area_utilization",
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
        elif usecase == "field_mapping":
            # Import here to avoid circular import
            from ..usecases.field_mapping import FieldMappingConfig
            default_config = FieldMappingConfig()
            return default_config.to_dict()
        elif usecase == "parking_space_detection":
            # Import here to avoid circular import
            from ..usecases.parking_space_detection import ParkingSpaceConfig
            default_config = ParkingSpaceConfig()
            return default_config.to_dict()
        elif usecase == "mask_detection":
            # Import here to avoid circular import
            from ..usecases.mask_detection import MaskDetectionConfig
            default_config = MaskDetectionConfig()
            return default_config.to_dict()
        
        elif usecase == "pipeline_detection":
            from ..usecases.pipeline_detection import PipelineDetectionConfig
            default_config = PipelineDetectionConfig()
            return default_config.to_dict()

        elif usecase == "fire_smoke_detection":
            # Import here to avoid circular import
            from ..usecases.fire_detection import FireSmokeConfig
            default_config = FireSmokeConfig()
            return default_config.to_dict()

        elif usecase == "wound_segmentation":
            # Import here to avoid circular import
            from ..usecases.wound_segmentation import WoundConfig
            default_config = WoundConfig()
            return default_config.to_dict()

        elif usecase == "shoplifting_detection":
            # Import here to avoid circular import
            from ..usecases.shoplifting_detection import ShopliftingDetectionConfig
            default_config = ShopliftingDetectionConfig()
            return default_config.to_dict()

        elif usecase == "solar_panel":
            # Import here to avoid circular import
            from ..usecases.solar_panel import SolarPanelConfig
            default_config = SolarPanelConfig()
            return default_config.to_dict()

        elif usecase == "car_damage_detection":
            # Import here to avoid circular import
            from ..usecases.car_damage_detection import CarDamageConfig
            default_config = CarDamageConfig()
            return default_config.to_dict()

        elif usecase == "pothole_segmentation":
            # Import here to avoid circular import
            from ..usecases.pothole_segmentation import PotholeConfig
            default_config = PotholeConfig()
            return default_config.to_dict()

        elif usecase == "leaf_disease_detection":
            # Import here to avoid circular import
            from ..usecases.leaf_disease import LeafDiseaseDetectionConfig
            default_config = LeafDiseaseDetectionConfig()
            return default_config.to_dict()

        elif usecase == "vehicle_monitoring":
            # Import here to avoid circular import
            from ..usecases.vehicle_monitoring import VehicleMonitoringConfig
            default_config = VehicleMonitoringConfig()
            return default_config.to_dict()
        
        elif usecase == "drone_traffic_monitoring":
            # Import here to avoid circular import
            from ..usecases.drone_traffic_monitoring import VehiclePeopleDroneMonitoringConfig
            default_config = VehiclePeopleDroneMonitoringConfig()
            return default_config.to_dict()
        
        elif usecase == "chicken_pose_detection":
            # Import here to avoid circular import
            from ..usecases.chicken_pose_detection import ChickenPoseDetectionConfig
            default_config = ChickenPoseDetectionConfig()
            return default_config.to_dict()
        
        elif usecase == "fruit_monitoring":
            # Import here to avoid circular import
            from ..usecases.banana_defect_detection import BananaMonitoringConfig
            default_config = BananaMonitoringConfig()
            return default_config.to_dict()
        
        elif usecase == "lane_detection":
            # Import here to avoid circular import
            from ..usecases.road_lane_detection import LaneDetectionConfig 
            default_config = LaneDetectionConfig()
            return default_config.to_dict()
        
        elif usecase == "shelf_inventory":
            # Import here to avoid circular import
            from ..usecases.shelf_inventory_detection import ShelfInventoryConfig
            default_config = ShelfInventoryConfig()
            return default_config.to_dict()

        elif usecase == "anti_spoofing_detection":
            # Import here to avoid circular import
            from ..usecases.anti_spoofing_detection import AntiSpoofingDetectionConfig
            default_config = AntiSpoofingDetectionConfig()
            return default_config.to_dict()
        
        elif usecase == "traffic_sign_monitoring":
            # Import here to avoid circular import
            from ..usecases.traffic_sign_monitoring import TrafficSignMonitoringConfig
            default_config = TrafficSignMonitoringConfig()
            return default_config.to_dict()

        elif usecase == "theft_detection":
            # Import here to avoid circular import
            from ..usecases.theft_detection import TheftDetectionConfig
            default_config = TheftDetectionConfig()
            return default_config.to_dict()
        
        elif usecase == "weapon_detection":
            # Import here to avoid circular import
            from ..usecases.weapon_detection import WeaponDetectionConfig
            default_config = WeaponDetectionConfig()
            return default_config.to_dict()
        
        elif usecase == "weld_defect_detection":
            # Import here to avoid circular import
            from ..usecases.weld_defect_detection import WeldDefectConfig
            default_config = WeldDefectConfig()
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
        elif usecase == "face_emotion":
            # Import here to avoid circular import
            from ..usecases.face_emotion import FaceEmotionConfig
            default_config = FaceEmotionConfig()
            return default_config.to_dict()
        elif usecase == "underwater_pollution_detection":
            # Import here to avoid circular import
            from ..usecases.underwater_pollution_detection import UnderwaterPlasticConfig
            default_config = UnderwaterPlasticConfig()
            return default_config.to_dict()
        elif usecase == "pedestrian_detection":
            # Import here to avoid circular import
            from ..usecases.pedestrian_detection import PedestrianDetectionConfig
            default_config = PedestrianDetectionConfig()
            return default_config.to_dict()
        elif usecase == "age_detection":
            # Import here to avoid circular import
            from ..usecases.age_detection import AgeDetectionConfig
            default_config = AgeDetectionConfig()
            return default_config.to_dict()
        elif usecase == "price_tag_detection":
            # Import here to avoid circular import
            from ..usecases.price_tag_detection import PriceTagConfig
            default_config = PriceTagConfig()
            return default_config.to_dict()
        elif usecase == "distracted_driver_detection":
            # Import here to avoid circular import
            from ..usecases.distracted_driver_detection import DistractedDriverConfig
            default_config = DistractedDriverConfig()
            return default_config.to_dict()
        elif usecase == "emergency_vehicle_detection":
            # Import here to avoid circular import
            from ..usecases.emergency_vehicle_detection import EmergencyVehicleConfig
            default_config = EmergencyVehicleConfig()
            return default_config.to_dict()
        elif usecase == "crop_weed_detection":
            # Import here to avoid circular import
            from ..usecases.crop_weed_detection import CropWeedDetectionConfig
            default_config = CropWeedDetectionConfig()
            return default_config.to_dict()
        elif usecase == "child_monitoring":
            # Import here to avoid circular import
            from ..usecases.child_monitoring import ChildMonitoringConfig
            default_config = ChildMonitoringConfig()
            return default_config.to_dict()
        elif usecase == "gender_detection":
            # Import here to avoid circular import
            from ..usecases.gender_detection import GenderDetectionConfig
            default_config = GenderDetectionConfig()
            return default_config.to_dict()
        elif usecase == "concrete_crack_detection":
            # Import here to avoid circular import
            from ..usecases.concrete_crack_detection import ConcreteCrackConfig
            default_config = ConcreteCrackConfig()
            return default_config.to_dict()
        elif usecase == "fashion_detection":
            # Import here to avoid circular import
            from ..usecases.fashion_detection import FashionDetectionConfig
            default_config = FashionDetectionConfig()
            return default_config.to_dict()
        elif usecase == "warehouse_object_segmentation":
            # Import here to avoid circular import
            from ..usecases.warehouse_object_segmentation import WarehouseObjectConfig
            default_config = WarehouseObjectConfig()
            return default_config.to_dict()
        elif usecase == "shopping_cart_analysis":
            # Import here to avoid circular import
            from ..usecases.shopping_cart_analysis import ShoppingCartConfig
            default_config = ShoppingCartConfig()
            return default_config.to_dict()
        elif usecase == "defect_detection_products":
            # Import here to avoid circular import
            from ..usecases.defect_detection_products import BottleDefectConfig
            default_config = BottleDefectConfig()
            return default_config.to_dict()
        elif usecase == "assembly_line_detection":
            # Import here to avoid circular import
            from ..usecases.assembly_line_detection import AssemblyLineConfig
            default_config = AssemblyLineConfig()
            return default_config.to_dict()
        elif usecase == "car_part_segmentation":
            # Import here to avoid circular import
            from ..usecases.car_part_segmentation import CarPartSegmentationConfig
            default_config = CarPartSegmentationConfig()
            return default_config.to_dict()
        elif usecase == "windmill_maintenance":
            # Import here to avoid circular import
            from ..usecases.windmill_maintenance import WindmillMaintenanceConfig
            default_config = WindmillMaintenanceConfig()
            return default_config.to_dict()
        elif usecase == "flower_segmentation":
            # Import here to avoid circular import
            from ..usecases.flower_segmentation import FlowerConfig
            default_config = FlowerConfig()
            return default_config.to_dict()
        elif usecase == "smoker_detection":
            # Import here to avoid circular import
            from ..usecases.smoker_detection import SmokerDetectionConfig
            default_config = SmokerDetectionConfig()
            return default_config.to_dict()
        elif usecase == "road_traffic_density":
            # Import here to avoid circular import
            from ..usecases.road_traffic_density import RoadTrafficConfig
            default_config = RoadTrafficConfig()
            return default_config.to_dict()
        elif usecase == "road_view_segmentation":
            # Import here to avoid circular import
            from ..usecases.road_view_segmentation import RoadViewSegmentationConfig
            default_config = RoadViewSegmentationConfig()
            return default_config.to_dict()
        elif usecase == "face_recognition":
            # Import here to avoid circular import
            from ..face_reg.face_recognition import FaceRecognitionEmbeddingConfig
            default_config = FaceRecognitionEmbeddingConfig()
            return default_config.to_dict()
        elif usecase == "drowsy_driver_detection":
            # Import here to avoid circular import
            from ..usecases.drowsy_driver_detection import DrowsyDriverConfig
            default_config = DrowsyDriverConfig()
            return default_config.to_dict()
        elif usecase == "waterbody_segmentation":
            # Import here to avoid circular import
            from ..usecases.waterbody_segmentation import WaterBodyConfig
            default_config = WaterBodyConfig()
            return default_config.to_dict()
        
        elif usecase == "litter_detection":
            # Import here to avoid circular import
            from ..usecases.litter_monitoring import LitterDetectionConfig
            default_config = LitterDetectionConfig()
            return default_config.to_dict()
        
        elif usecase == "abandoned_object_detection":
            # Import here to avoid circular import
            from ..usecases.abandoned_object_detection import AbandonedObjectConfig
            default_config = AbandonedObjectConfig()
            return default_config.to_dict()
        elif usecase == "leak_detection":
            # Import here to avoid circular import
            from ..usecases.leak_detection import LeakDetectionConfig
            default_config = LeakDetectionConfig()
            return default_config.to_dict()
        elif usecase == "human_activity_recognition":
            # Import here to avoid circular import
            from ..usecases.human_activity_recognition import HumanActivityConfig
            default_config = HumanActivityConfig()
            return default_config.to_dict()
        elif usecase == "gas_leak_detection":
            # Import here to avoid circular import
            from ..usecases.gas_leak_detection import GasLeakDetectionConfig
            default_config = GasLeakDetectionConfig()
            return default_config.to_dict()
        
        elif usecase == "license_plate_monitor":
            # Import here to avoid circular import
            from ..usecases.license_plate_monitoring import LicensePlateMonitorConfig
            default_config = LicensePlateMonitorConfig()
            return default_config.to_dict()

        elif usecase == "dwell":
            # Import here to avoid circular import
            from ..usecases.dwell_detection import DwellConfig
            default_config = DwellConfig()
            return default_config.to_dict()

        elif usecase == "age_gender_detection":
            # Import here to avoid circular import
            from ..usecases.age_gender_detection import AgeGenderConfig
            default_config = AgeGenderConfig()
            return default_config.to_dict()
        
        elif usecase == "wildlife_monitoring":
            # Import here to avoid circular import
            from ..usecases.wildlife_monitoring import WildLifeMonitoringConfig
            default_config = WildLifeMonitoringConfig()
            return default_config.to_dict()
    
        elif usecase == "pcb_defect_detection":
            # Import here to avoid circular import
            from ..usecases.pcb_defect_detection import PCBDefectConfig
            default_config = PCBDefectConfig()
            return default_config.to_dict()

        elif usecase == "suspicious_activity_detection":
            # Import here to avoid circular import
            from ..usecases.suspicious_activity_detection import SusActivityConfig
            default_config = SusActivityConfig()
            return default_config.to_dict()
        
        elif usecase == "natural_disaster_detection":
            # Import here to avoid circular import
            from ..usecases.natural_disaster import NaturalDisasterConfig
            default_config = NaturalDisasterConfig()
            return default_config.to_dict()

        elif usecase == "footfall":
            # Import here to avoid circular import
            from ..usecases.footfall import FootFallConfig
            default_config = FootFallConfig()
            return default_config.to_dict()
        
        elif usecase == "vehicle_monitoring_parking_lot":
            # Import here to avoid circular import
            from ..usecases.vehicle_monitoring_parking_lot import VehicleMonitoringParkingLotConfig
            default_config = VehicleMonitoringParkingLotConfig()
            return default_config.to_dict()
        
        elif usecase == "vehicle_monitoring_drone_view":
            # Import here to avoid circular import
            from ..usecases.vehicle_monitoring_drone_view import VehicleMonitoringDroneViewConfig
            default_config = VehicleMonitoringDroneViewConfig()
            return default_config.to_dict()
        
        elif usecase == "parking_lot_analytics":
            # Import here to avoid circular import
            from ..usecases.parking_lot_analytics import ParkingLotAnalyticsConfig
            default_config = ParkingLotAnalyticsConfig()
            
        elif usecase == "crowdflow":
            # Import here to avoid circular import
            from ..usecases.crowdflow import CrowdflowConfig
            default_config = CrowdflowConfig()
            return default_config.to_dict()
        
        elif usecase == "heatmaps":
            # Import here to avoid circular import
            from ..usecases.heatmaps import HeatMapsConfig
            default_config = HeatMapsConfig()
            return default_config.to_dict()
        
        elif usecase == "crowd_density_heatmaps":
            # Import here to avoid circular import
            from ..usecases.crowd_density_heatmaps import CrowdDensityHeatMapsConfig
            default_config = CrowdDensityHeatMapsConfig()
            return default_config.to_dict()
        
        elif usecase == "hazard_zone_entry":
            # Import here to avoid circular import
            from ..usecases.hazard_zone_entry import HazardZoneEntryConfig
            default_config = HazardZoneEntryConfig()
            return default_config.to_dict()
        
        elif usecase == "vehicle_monitoring_wrong_way":
            # Import here to avoid circular import
            from ..usecases.vehicle_monitoring_wrong_way import VehicleMonitoringWrongWayConfig
            default_config = VehicleMonitoringWrongWayConfig()
            return default_config.to_dict()
        
        elif usecase == "underground_pipeline_defect":
            # Import here to avoid circular import
            from ..usecases.underground_pipeline_defect_detection import UndergroundPipelineDefectConfig
            default_config = UndergroundPipelineDefectConfig()
            return default_config.to_dict()
        
        elif usecase == "stopped_vehicle_monitoring":
            # Import here to avoid circular import
            from ..usecases.stopped_vehicle_monitoring import StoppedVehicleMonitoringConfig
            default_config = StoppedVehicleMonitoringConfig()
            return default_config.to_dict()

        elif usecase == "loitering_detection":
            # Import here to avoid circular import
            from ..usecases.loitering_detection import LoiteringConfig
            default_config = LoiteringConfig()
            return default_config.to_dict()
        
        elif usecase == "tailgating_detection":
            # Import here to avoid circular import
            from ..usecases.tailgating_detection import TailgatingConfig
            default_config = TailgatingConfig()
            return default_config.to_dict()
        
        elif usecase == "vehicle_color_detection":
            # Import here to avoid circular import
            from ..usecases.vehicle_color_detection import VehicleColorDetectionConfig
            default_config = VehicleColorDetectionConfig()
            return default_config.to_dict()
        
        elif usecase == "fall_detection":
            # Import here to avoid circular import
            from ..usecases.fall_detection import FallDetectionConfig
            default_config = FallDetectionConfig()
            return default_config.to_dict()
        
        elif usecase == "running_detection":
            # Import here to avoid circular import
            from ..usecases.running_detection import RunningDetectionConfig
            default_config = RunningDetectionConfig()
        elif usecase == "liquid_leak_detection":
            # Import here to avoid circular import
            from ..usecases.liquid_leak_detection import LiquidLeakDetectionConfig
            default_config = LiquidLeakDetectionConfig()
            return default_config.to_dict()
        elif usecase == "pipe_gas_leak_detection":
            # Import here to avoid circular import
            from ..usecases.pipe_gas_leak_detection import PipeGasLeakDetectionConfig
            default_config = PipeGasLeakDetectionConfig()
            return default_config.to_dict()
        elif usecase == "pipe_corrosion_detection":
            # Import here to avoid circular import
            from ..usecases.pipe_corrosion_detection import PipeCorrosionDetectionConfig
            default_config = PipeCorrosionDetectionConfig()
            return default_config.to_dict()
        elif usecase == "people_counting_in_zone":
            # Import here to avoid circular import
            from ..usecases.people_counting_in_zone import PeopleCountingInZoneConfig
            default_config = PeopleCountingInZoneConfig()
            return default_config.to_dict()
        elif usecase == "overcrowding_detection":
            # Import here to avoid circular import
            from ..usecases.overcrowding_detection import OvercrowdingDetectionConfig
            default_config = OvercrowdingDetectionConfig()
            return default_config.to_dict()
        elif usecase == "animal_detection":
            # Import here to avoid circular import
            from ..usecases.animal_detection import AnimalDetectionConfig
            default_config = AnimalDetectionConfig()
            return default_config.to_dict()

        elif usecase == "burglary_detection":
            # Import here to avoid circular import
            from ..usecases.burglary_detection import BurglaryDetectionConfig
            default_config = BurglaryDetectionConfig()
            return default_config.to_dict()

        elif usecase == "landslide_detection":
            # Import here to avoid circular import
            from ..usecases.landslide_detection import LandslideDetectionConfig
            default_config = LandslideDetectionConfig()
            return default_config.to_dict()
            
        #Add all image based usecases here
        elif usecase == "blood_cancer_detection_img":
            # Import here to avoid circular import
            from ..usecases.blood_cancer_detection_img import BloodCancerDetectionConfig
            default_config = BloodCancerDetectionConfig()
            return default_config.to_dict()
        elif usecase == "skin_cancer_classification_img":   
            # Import here to avoid circular import
            from ..usecases.skin_cancer_classification_img import SkinCancerClassificationConfig
            default_config = SkinCancerClassificationConfig()
            return default_config.to_dict()
        elif usecase == "plaque_segmentation_img":
            # Import here to avoid circular import  
            from ..usecases.plaque_segmentation_img import PlaqueSegmentationConfig
            default_config = PlaqueSegmentationConfig()
            return default_config.to_dict()
        elif usecase == "cardiomegaly_classification":
            # Import here to avoid circular import
            from ..usecases.cardiomegaly_classification import CardiomegalyConfig
            default_config = CardiomegalyConfig()
            return default_config.to_dict()
        elif usecase == "histopathological_cancer_detection":
            # Import here to avoid circular import
            from ..usecases.Histopathological_Cancer_Detection_img import HistopathologicalCancerDetectionConfig
            default_config = HistopathologicalCancerDetectionConfig()
            return default_config.to_dict()
        elif usecase == "cell_microscopy_segmentation":
            # Import here to avoid circular import
            from ..usecases.cell_microscopy_segmentation import CellMicroscopyConfig
            default_config = CellMicroscopyConfig()
            return default_config.to_dict()
        elif usecase == "area_utilization":
            # Import here to avoid circular import
            from ..usecases.area_utilization import AreaUtilizationConfig
            default_config = AreaUtilizationConfig()
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