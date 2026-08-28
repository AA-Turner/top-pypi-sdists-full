"""Auto-generated stub for module: parking_lot_analytics."""
from typing import Any, Dict, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.parking_analytics_tracker import ParkingAnalyticsTracker
from ..utils.post_processing_config_client import GEOMETRY_RETRY_INTERVAL
from ..utils.post_processing_config_client import PostProcessingConfigClient

# Classes
class ParkingLotAnalyticsConfig:
    # Configuration for vehicle detection use case in parking lot analytics (parking time).

    ...
class ParkingLotAnalyticsUseCase:
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

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Inject a ``PostProcessingConfigClient`` for API-based zone resolution.
        
                Must be called before the first ``process()`` invocation.  When a
                client is provided the use case resolves zone polygons drawn in the
                Matrice UI, falling back to ``zone_config`` in ``ParkingLotAnalyticsConfig``
                if the API is unavailable.
        """
        ...

