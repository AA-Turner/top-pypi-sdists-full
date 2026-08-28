"""Auto-generated stub for module: violence_detection."""
from typing import Any, Dict, Optional, Tuple

from ...analytics.redis_publisher import AnalyticsRedisPublisher
from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.legacy_analytics_bridge import get_legacy_session

# Classes
class ViolenceDetectionConfig:
    # Configuration for violence detection post-processing.

    ...
class ViolenceDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_duration_seconds(self: Any, start_time: Any, end_time: Any) -> Any: ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

class ViolenceIncidentIdTracker:
    def __init__(self: Any) -> None: ...

    def advance(self: Any, sev_level: str, current_ts: str) -> Tuple[int, int]: ...

