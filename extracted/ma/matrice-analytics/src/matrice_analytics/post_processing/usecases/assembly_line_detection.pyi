"""Auto-generated stub for module: assembly_line_detection."""
from typing import Any, Dict, Optional, Tuple

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_confidence, match_results_structure

# Classes
class AssemblyLineConfig:
    # Configuration for assembly line detection use case.

    ...
class AssemblyLineUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]
    EMPTY_PLATE_CATEGORIES: Tuple[Any, ...]
    LOADED_PLATE_CATEGORIES: Tuple[Any, ...]
    ROBOT_ARM_CATEGORIES: Tuple[Any, ...]

    def get_new_counts_this_frame(self: Any) -> Any:
        """
        Return the count of track_ids seen for the FIRST time this frame, per category.
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

