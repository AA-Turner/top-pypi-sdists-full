"""Auto-generated stub for module: vegetable_detection."""
from typing import Any, Dict, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult, ResultFormat
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_by_category, filter_by_categories, filter_by_confidence, match_results_structure

# Classes
class VegetableDetectionConfig:
    # Configuration for vegetable detection use case.

    ...
class VegetableDetectionUseCase:
    # Vegetable detection processor for post-processing model outputs.

    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process vegetable detections and generate agg_summary output.
        """
        ...

