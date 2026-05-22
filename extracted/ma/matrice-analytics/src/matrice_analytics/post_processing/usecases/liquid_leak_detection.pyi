"""Auto-generated stub for module: liquid_leak_detection."""
from typing import Any, Dict, List, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_categories, filter_by_confidence, match_results_structure

# Constants
logger: Any

# Classes
class LiquidLeakDetectionConfig:
    # Configuration class for Liquid Leak Detection.
    #
    # Extends BaseConfig and adds:
    # - Spatial merging parameters
    # - Temporal validation parameters
    # - Cooldown control
    # - Analytics toggles

    def __init__(self: Any, usecase: str = 'liquid_leak_detection', category: str = 'industrial', confidence_threshold: float = 0.25, target_categories: Optional[List[str]] = None, enable_analytics: bool = True, enable_spatial_merge: bool = True, iou_merge_threshold: float = 0.5, containment_threshold: float = 0.6, activation_frames: int = 3, deactivation_frames: int = 40, alert_cooldown_seconds: int = 30, index_to_category: Optional[Dict[int, str]] = None, alert_config: Optional[Any] = None, **kwargs: Any) -> None: ...

    def validate(self: Any) -> List[str]:
        """
        Validates configuration parameters before processing.
        Ensures no invalid thresholds or misconfiguration.
        """
        ...

class LiquidLeakDetectionUseCase:
    # Industrial liquid leak detection usecase.
    #
    # Responsibilities:
    # - Process frame detections
    # - Apply filtering and merging
    # - Maintain temporal state
    # - Generate alerts and incidents
    # - Produce standardized agg_summary output

    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Creates a default configuration instance.
        
        Allows override of any field via kwargs.
        Used for testing and quick experimentation.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Main entry point for processing detection results.
        
        This function:
        - Validates configuration
        - Detects input format
        - Processes each frame independently
        - Builds standardized frame-wise agg_summary
        - Returns ProcessingResult
        """
        ...

