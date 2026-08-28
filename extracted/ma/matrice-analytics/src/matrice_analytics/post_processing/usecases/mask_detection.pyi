"""Auto-generated stub for module: mask_detection."""
from typing import Any, Dict, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_confidence, match_results_structure

# Constants
MASK_CATEGORY_AGGREGATION: Dict[Any, Any]

# Classes
class MaskDetectionConfig:
    # Configuration for mask detection use case in mask monitoring.

    ...
class MaskDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Unique track IDs first seen this frame, per category.
        """
        ...

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

