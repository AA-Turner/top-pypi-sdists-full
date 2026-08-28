"""Auto-generated stub for module: loitering_detection."""
from typing import Any, Dict, List, Optional, Set

from ...analytics.redis_publisher import AnalyticsRedisPublisher
from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import BBoxSmoothingTracker, ByteTrackWrapper, SORTTracker, apply_category_mapping, bbox_centroid, bbox_feet_point, bbox_iou, dist, filter_by_confidence, match_results_structure, point_in_polygon, smooth_point
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.legacy_analytics_bridge import get_legacy_session
from ..utils.post_processing_config_client import GEOMETRY_RETRY_INTERVAL, PostProcessingConfigClient

# Classes
class LoiteringConfig:
    def resolve_loiter_person_threshold(self: Any, zone_name: str) -> int:
        """
        Resolve a zone's loiterer-count incident threshold.
        
                Lookup order: ``zone_params[<zone>]["count"]`` -> ``["loiter_person_threshold"]``
                -> global ``loiter_person_threshold``.
        """
        ...

    def validate(self: Any) -> List[str]: ...

class LoiteringUseCase:
    def __init__(self: Any) -> None: ...

    GLOBAL_ZONE_NAME: str

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Count of track ids reported for the FIRST time this frame, per category.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return total unique track_id counts per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set the client used to resolve zones from deployment/camera post-processing config.
        """
        ...

