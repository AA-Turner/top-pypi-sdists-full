"""Auto-generated stub for module: people_counting."""
from typing import Any, Dict, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import PeopleCountingConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure

# Classes
class PeopleCountingUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of CONFIRMED new track IDs reported for the first time this frame.
        
                A track is only counted as "new" when it has been present in the tracker
                output for at least ``min_hits_for_new_track`` consecutive output frames
                (default 3). Short dropouts are tolerated via a soft-decay counter (a
                one-frame miss reduces the counter by 1 instead of resetting to 0).
                This filters out:
                  - Spurious short-lived detections (noise, reflections, shadows)
                  - Brief ID switches caused by tracker matching failures
                  - Flickering detections near the confidence threshold
        
                Each track ID is reported as new **exactly once** across all frames.
                Subsequent frames will return 0 for that track even though it is still
                visible.  This makes downstream aggregation (summing over N seconds)
                produce the correct total of genuinely new people.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

