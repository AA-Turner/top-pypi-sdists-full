"""Auto-generated stub for module: advanced_counting_utils."""
from typing import Any, Dict, List, Optional, Set, Tuple

from ..core.base import ResultFormat
from .format_utils import match_results_structure
from .geometry_utils import get_bbox_center, point_in_polygon

# Functions
def calculate_bbox_fingerprint(bbox: Dict, category: str = '') -> str:
    """
    Calculate a fingerprint for bbox deduplication.
    """
    ...
def calculate_bbox_overlap(bbox1: Dict, bbox2: Dict) -> float:
    """
    Calculate overlap between two bounding boxes.
    """
    ...
def clean_expired_tracks(track_timestamps: Dict, track_last_seen: Dict, current_timestamp: float, expiry_seconds: int) -> Any:
    """
    Clean expired tracks from tracking dictionaries.
    """
    ...

# Classes
class CountingLibrary:
    # Library class for handling object counting operations with time-based tracking.

    def __init__(self: Any, time_window_seconds: int = 3600, track_expiry_seconds: int = 300, enable_time_based_counting: bool = True, enable_bbox_deduplication: bool = True, bbox_similarity_threshold: float = 0.8) -> None:
        """
        Initialize counting library with configuration.
        """
        ...

    def count_in_zones(self: Any, results: Dict, zones: Dict[str, List[Tuple[float, float]]] = None, current_timestamp: Optional[float] = None) -> Dict:
        """
        Count objects in defined zones with configurable rules and time-based tracking.
        """
        ...

    def count_objects(self: Any, results: Any, identification_keys: List[str] = None, current_timestamp: Optional[float] = None) -> Tuple[Any, Dict]:
        """
        Count objects with metadata, supporting incremental time-based counting.
        """
        ...

    def get_counting_statistics(self: Any, current_timestamp: Optional[float] = None) -> Dict[str, Any]:
        """
        Get comprehensive counting statistics.
        """
        ...

    def get_unique_count_by_keys(self: Any, results: Any, keys: List[str] = None) -> Dict[str, int]:
        """
        Get unique count based on specified keys.
        """
        ...

    def reset_counters(self: Any, reset_zones: bool = True, reset_time_tracking: bool = True) -> Any:
        """
        Reset counting state.
        """
        ...

    def set_time_window(self: Any, time_window_seconds: int) -> Any:
        """
        Set the time window for statistics collection.
        """
        ...

