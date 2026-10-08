"""Auto-generated stub for module: vehicle_monitoring_drone_view."""
from typing import Any, Dict, Optional, Tuple

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.agnostic_nms import AgnosticNMS
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon

# Functions
def resolve_category(d: Dict[str, Any], index_to_category: Optional[Dict[int, str]] = None) -> Tuple[str, Optional[int]]: ...
def to_bbox_dict(d: Dict[str, Any]) -> Dict[str, Any]: ...

# Classes
class VehicleMonitoringDroneViewConfig:
    # Configuration for drone view vehicle monitoring use case.

    ...
class VehicleMonitoringDroneViewUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame/aggregation vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

