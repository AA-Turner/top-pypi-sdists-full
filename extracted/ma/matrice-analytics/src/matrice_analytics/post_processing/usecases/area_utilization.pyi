"""Auto-generated stub for module: area_utilization."""
from typing import Any, Dict, List, Optional, Set

from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import ByteTrackWrapper, SORTTracker, apply_category_mapping, filter_by_confidence, match_results_structure, point_in_polygon
from .overcrowding_detection import PostProcessingConfigClient, lift_ai_camera_zones_into_post_processing

# Constants
DEFAULT_CAPACITY: int
DEFAULT_WINDOW_SECONDS: int
OCCUPANCY_CRITICAL_PERCENT: float
OCCUPANCY_ENTER_PERCENT: float
OCCUPANCY_EXIT_FRAMES: int
OCCUPANCY_EXIT_PERCENT: float
SEVERITY_CRITICAL: str
SEVERITY_HIGH: str
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
    # Per-zone capacity is the single source of truth and lives inside the zone
    # geometry payload::
    #
    #   zone_config.zone_params = {"meeting_room": {"capacity": 6}, ...}
    #
    # That capacity drives BOTH the utilization math (``occupancy_percent``) AND the
    # alerting: a zone alerts when its in-zone people count exceeds its capacity.
    # ``extra_params.zone_capacities`` is still read as a legacy fallback, and
    # ``window_seconds`` (rolling-window length) still lives in ``extra_params``.

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
    # - alerts (per-zone over-capacity, threshold = zone_params capacity)
    # - human_text summary
    #
    # Adds:
    # - business_analytics (list per frame) with zone-wise utilization metrics

    def __init__(self: Any) -> None: ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Count of track ids reported for the FIRST time this frame, per category.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Any) -> None:
        """
        Set client used to resolve zones from deployment/camera post-processing config.
        """
        ...

