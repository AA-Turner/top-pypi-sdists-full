"""Auto-generated stub for module: age_detection."""
from typing import Any, Dict, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, bbox_smoothing, count_objects_by_category, filter_by_confidence, match_results_structure

# Constants
AVG_AGE: int
MAX_AGE: int
MIN_AGE: int

# Classes
class AgeDetectionConfig:
    ...
class AgeDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

class AgeSmoother:
    def __init__(self: Any, window_size: int = 20) -> None: ...

    def prune(self: Any, active_track_ids: set) -> Any: ...

    def update(self: Any, track_id: int, age: int) -> int: ...

