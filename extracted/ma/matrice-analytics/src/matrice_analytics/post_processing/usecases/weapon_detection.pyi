"""Auto-generated stub for module: weapon_detection."""
from typing import Any, Dict, List, Optional, Set, Tuple

from ...analytics.redis_publisher import AnalyticsRedisPublisher
from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.legacy_analytics_bridge import get_legacy_session
from ..utils.post_processing_config_client import PostProcessingConfigClient

# Classes
class IncidentIdTracker:
    # Tracks severity-level progression across frames to produce monotonically
    # increasing incident/alert IDs (7 frames to advance a level; 130 empty
    # frames to close an incident).

    def __init__(self: Any) -> None: ...

    def advance(self: Any, sev_level: str, current_ts: str) -> Tuple[int, int]:
        """
        Feed a severity level ("" if no detection). Returns (rank_id, alert_id).
        """
        ...

class WeaponDetectionConfig:
    def validate(self: Any) -> List[str]:
        """
        Validate weapon detection configuration.
        
                zone_config may be empty at load time when geometry will be resolved from
                API via stream_info + config_client in process().
        """
        ...

class WeaponDetectionUseCase:
    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]: ...

    def get_duration_seconds(self: Any, start_time: Any, end_time: Any) -> Any: ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]: ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set PostProcessingConfigClient for API zone polygons (by_app_deployment + camera_id).
        """
        ...

