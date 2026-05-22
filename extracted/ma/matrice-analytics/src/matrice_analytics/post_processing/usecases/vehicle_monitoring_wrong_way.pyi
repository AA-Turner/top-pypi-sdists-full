"""Auto-generated stub for module: vehicle_monitoring_wrong_way."""
from typing import Any, Dict, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.wrong_way_tracker import WrongWayDetectionTracker

# Classes
class VehicleMonitoringWrongWayConfig:
    # Configuration for wrong-way vehicle detection use case.

    ...
class VehicleMonitoringWrongWayUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any:
        """
        Get total counts per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

