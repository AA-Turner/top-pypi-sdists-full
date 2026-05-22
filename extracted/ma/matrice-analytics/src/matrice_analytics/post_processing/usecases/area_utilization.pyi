"""Auto-generated stub for module: area_utilization."""
from typing import Any, Dict, List, Optional, Set

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure, point_in_polygon
from .overcrowding_detection import PostProcessingConfigClient, lift_ai_camera_zones_into_post_processing

# Constants
DEFAULT_CAPACITY: int
DEFAULT_WINDOW_SECONDS: int
TARGET_CATEGORY: str
WARN_MISSING_STREAM_RESOLUTION: str
WARN_NO_ZONES: str
WARN_ZONE_TOO_BIG: str

# Classes
class AreaUtilizationConfig:
    # Configuration for area utilization use case.
    #
    # This config intentionally mirrors PeopleCountingConfig so that:
    # - client payloads stay consistent
    # - PostProcessor/config_manager behavior remains predictable
    # - we can safely clone people_counting.py behavior
    #
    # Utilization-specific parameters live in:
    #   extra_params = {
    #     "zone_capacities": {"global": 10, "meeting_room": 6},
    #     "window_seconds": 300,
    #   }
    #
    # Per-zone alert headcounts: ``alert_config.occupancy_thresholds`` maps zone name
    # to a *people count*; an alert is raised when that zone's count is **greater than**
    # the value (same sense as ``count_thresholds`` for globals). Occupancy % is only
    # for analytics / display.

    def validate(self: Any) -> List[str]:
        """
        Validate area utilization configuration (PeopleCountingConfig-compatible).
        """
        ...

class AreaUtilizationUseCase:
    # Area Utilization = People Counting + Capacity Analytics.
    #
    # Keeps PeopleCounting behavior:
    # - incidents
    # - tracking_stats
    # - alerts (global count + optional per-zone people-count via occupancy_thresholds)
    # - human_text summary
    #
    # Adds:
    # - business_analytics (list per frame) with zone-wise utilization metrics

    def __init__(self: Any) -> None: ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Any) -> None:
        """
        Set client used to resolve zones from deployment/camera post-processing config.
        """
        ...

