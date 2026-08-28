"""Auto-generated stub for module: gender_detection."""
from typing import Any, Dict, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, bbox_smoothing, filter_by_confidence, match_results_structure

# Constants
AVG_AGE: int
MAX_AGE: int
MIN_AGE: int

# Classes
class GenderDetectionConfig:
    # Configuration for gender detection use case in gender detection.

    ...
class GenderDetectionUseCase:
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

class GenderStabilizer:
    def __init__(self: Any, window_size: int = 10, min_votes: int = 3) -> None: ...

    def prune(self: Any, active_track_ids: set) -> Any:
        """
        Remove stale tracks to prevent memory growth
        """
        ...

    def update(self: Any, track_id: int, gender: str) -> str:
        """
        Returns stabilized gender for this track_id
        Majority vote over PREVIOUS frames (no current-frame bias)
        """
        ...

