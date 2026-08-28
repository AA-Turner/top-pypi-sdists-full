"""Auto-generated stub for module: running_detection."""
from typing import Any, Dict, List, Optional

from ...analytics.redis_publisher import AnalyticsRedisPublisher
from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.legacy_analytics_bridge import get_legacy_session

# Classes
class RunningConfirmationConfig:
    # Configuration for running detection confirmation layer.

    ...
class RunningConfirmationLayer:
    # Per-track temporal confirmation for running detection.
    # Suppresses flickering FPs by requiring persistent running classification.

    def __init__(self: Any, config: Optional[Any] = None) -> None: ...

    def get_stats(self: Any) -> Dict[str, Any]: ...

    def reset(self: Any) -> Any: ...

    def update(self: Any, detections: List[Dict]) -> List[Dict]:
        """
        Apply confirmation logic to running detections.
        Only detections meeting min_positives_for_run threshold are confirmed.
        """
        ...

class RunningDetectionConfig:
    # Configuration for running detection use case.

    ...
class RunningDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]: ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

class RunningDetector:
    # Velocity-based running detection from tracked person detections.
    # Uses height-normalized velocity for scale-invariant detection.

    def __init__(self: Any, config: Optional[Dict] = None) -> None: ...

    DEFAULT_CONFIG: Dict[Any, Any]

    def cleanup_lost_tracks(self: Any, active_track_ids: List[int]) -> Any: ...

    def reset(self: Any) -> Any: ...

    def update(self: Any, detections: List[Dict], frame_id: Optional[int] = None) -> List[Dict]:
        """
        Process detections and add velocity/running info.
        """
        ...

