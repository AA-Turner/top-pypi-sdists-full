"""Auto-generated stub for module: distracted_driver_detection."""
from typing import Any, Dict, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_confidence, match_results_structure

# Classes
class DistractedDriverConfig:
    # Configuration for distracted driver detection use case in distracted driver monitoring.

    ...
class DistractedDriverUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...

