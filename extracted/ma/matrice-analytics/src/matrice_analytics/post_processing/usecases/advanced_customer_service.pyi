"""Auto-generated stub for module: advanced_customer_service."""
from typing import Any, Dict, List, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import CustomerServiceConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, calculate_distance, filter_by_confidence, get_bbox_center, match_results_structure, point_in_polygon
from ..utils.business_metrics_manager_utils import BUSINESS_METRICS_MANAGER, BusinessMetricsManagerFactory

# Functions
def assign_person_by_area(detections: Any, _customer_areas: Any, staff_areas: Any) -> Any:
    """
    Assigns category 'person' detections to 'staff' or 'customer' based on their location in area polygons.
    Modifies the detection list in-place.
    Args:
        detections: List of detection dicts.
        customer_areas: Dict of area_name -> polygon (list of [x, y]).
        staff_areas: Dict of area_name -> polygon (list of [x, y]).
    """
    ...

# Classes
class AdvancedCustomerServiceUseCase:
    def __init__(self: Any) -> None:
        """
        Initialize advanced customer service use case.
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_camera_info_from_stream(self: Any, stream_info: Any) -> Any:
        """
        Extract camera_info from stream_info, matching people_counting pattern.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for advanced customer service.
        """
        ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return total unique track counts per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[dict] = None) -> Any:
        """
        Process advanced customer service analytics.
        """
        ...

