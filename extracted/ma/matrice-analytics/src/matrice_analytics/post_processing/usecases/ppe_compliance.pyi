"""Auto-generated stub for module: ppe_compliance."""
from typing import Any, Dict, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, bbox_smoothing, match_results_structure

# Classes
class PPEComplianceConfig:
    ...
class PPEComplianceUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_camera_info_from_stream(self: Any, stream_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract camera information from stream_info dict, matching mask_detection's approach.
        """
        ...

    def get_total_violation_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each violation category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for PPE compliance detection post-processing.
        Applies category mapping, violation smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs in the new agg_summary format
        """
        ...

    def reset_all_tracking(self: Any) -> None:
        """
        Reset both advanced tracker and violation tracking state.
        """
        ...

    def reset_tracker(self: Any) -> None:
        """
        Reset the advanced tracker instance.
        
        This should be called when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        """
        ...

    def reset_violation_tracking(self: Any) -> None:
        """
        Reset violation tracking state (total counts, track IDs, etc.).
        
        This should be called when:
        - Starting a completely new tracking session
        - Switching to a different video/stream
        - Manual reset requested by user
        """
        ...

