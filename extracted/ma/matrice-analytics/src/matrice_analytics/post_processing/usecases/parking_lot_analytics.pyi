"""Auto-generated stub for module: parking_lot_analytics."""
from typing import Any, Dict, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.parking_analytics_tracker import ParkingAnalyticsTracker

# Classes
class ParkingLotAnalyticsConfig:
    # Configuration for vehicle detection use case in parking lot analytics (parking time).

    ...
class ParkingLotAnalyticsUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

