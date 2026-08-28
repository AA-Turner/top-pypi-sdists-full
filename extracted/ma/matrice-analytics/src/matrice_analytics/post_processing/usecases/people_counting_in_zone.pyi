"""Auto-generated stub for module: people_counting_in_zone."""
from typing import Any, Dict, List, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure

# Classes
class PeopleCountingInZoneConfig:
    # Configuration for people counting use case.

    def validate(self: Any) -> List[str]:
        """
        Validate people counting configuration.
        """
        ...

class PeopleCountingInZoneUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared for the FIRST TIME EVER in this frame.
        
                This counts only track IDs that have never been seen before (not in total set).
                Re-entries (person leaves and comes back) are NOT counted as new.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

