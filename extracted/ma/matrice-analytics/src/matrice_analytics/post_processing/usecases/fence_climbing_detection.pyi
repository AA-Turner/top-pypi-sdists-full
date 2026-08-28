"""Auto-generated stub for module: fence_climbing_detection."""
from typing import Any, Dict, List, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, PeopleCountingConfig, ZoneConfig
from ..utils import apply_category_mapping, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, get_bbox_center, point_in_polygon
from ..utils.incident_manager_utils import IncidentManagerFactory
from .hazard_zone_entry import PostProcessingConfigClient

# Classes
class FenceClimbingDetectionConfig:
    # Configuration for Fence Climbing Detection use case.

    def validate(self: Any) -> List[str]: ...

class FenceClimbingDetectionUseCase:
    # Fence Climbing Detection with zone analysis, per-track state, and incident manager.

    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

    def get_current_frame_count(self: Any) -> int: ...

    def get_total_count(self: Any) -> int: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Any) -> None: ...

