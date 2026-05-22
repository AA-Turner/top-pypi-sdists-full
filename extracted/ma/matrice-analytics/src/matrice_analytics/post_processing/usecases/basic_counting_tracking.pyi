"""Auto-generated stub for module: basic_counting_tracking."""
from typing import Any, Dict, List, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, TrackingConfig
from ..utils import apply_category_mapping, calculate_counting_summary, count_objects_in_zones, count_unique_tracks, filter_by_confidence, match_results_structure

# Classes
class BasicCountingTrackingConfig:
    # Configuration for basic counting with tracking.

    def __init__(self: Any, category: str = 'general', usecase: str = 'basic_counting_tracking', confidence_threshold: float = 0.5, target_categories: List[str] = None, zones: Optional[Dict[str, List[List[float]]]] = None, enable_tracking: bool = True, tracking_method: str = 'kalman', max_age: int = 30, min_hits: int = 3, count_thresholds: Optional[Dict[str, int]] = None, zone_thresholds: Optional[Dict[str, int]] = None, alert_cooldown: float = 60.0, enable_unique_counting: bool = True, index_to_category: Optional[Dict[int, str]] = None, **kwargs: Any) -> None:
        """
        Initialize basic counting tracking configuration.
        
        Args:
            category: Use case category
            usecase: Use case name
            confidence_threshold: Minimum confidence for detections
            target_categories: List of categories to count
            zones: Zone definitions for spatial analysis
            enable_tracking: Whether to enable tracking
            tracking_method: Tracking algorithm to use
            max_age: Maximum age for tracks in frames
            min_hits: Minimum hits before confirming track
            count_thresholds: Count thresholds for alerts
            zone_thresholds: Zone occupancy thresholds for alerts
            alert_cooldown: Alert cooldown time in seconds
            enable_unique_counting: Enable unique object counting
            index_to_category: Optional mapping from class indices to category names
            **kwargs: Additional parameters
        """
        ...

    def validate(self: Any) -> List[str]:
        """
        Validate configuration.
        """
        ...

class BasicCountingTrackingUseCase:
    # Basic counting with tracking use case.

    def __init__(self: Any) -> None:
        """
        Initialize basic counting tracking use case.
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for basic counting tracking.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None) -> Any:
        """
        Process basic counting with tracking.
        
        Args:
            data: Raw model output (detection or tracking format)
            config: Basic counting tracking configuration
            context: Processing context
        
        Returns:
            ProcessingResult: Processing result with counting and tracking analytics
        """
        ...

    def validate_config(self: Any, config: Any) -> bool:
        """
        Validate configuration for this use case.
        """
        ...

