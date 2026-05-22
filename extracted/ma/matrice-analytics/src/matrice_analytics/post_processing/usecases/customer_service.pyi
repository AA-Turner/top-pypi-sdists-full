"""Auto-generated stub for module: customer_service."""
from typing import Any, Dict, List, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import CustomerServiceConfig
from ..utils import apply_category_mapping, calculate_distance, filter_by_confidence, get_bbox_center, match_results_structure, point_in_polygon
from ..utils import get_bbox_center, point_in_polygon
from ..utils.business_metrics_manager_utils import BUSINESS_METRICS_MANAGER, BusinessMetricsManagerFactory

# Functions
def assign_person_by_area(detections: Any, customer_areas: Any, staff_areas: Any) -> Any:
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
class CustomerServiceUseCase:
    # Customer service analytics with comprehensive business intelligence.

    def __init__(self: Any) -> None:
        """
        Initialize customer service use case.
        """
        ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for customer service.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Get total unique counts per category across all processed frames.
        
        Returns:
            Dictionary mapping category to unique count
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Any] = None) -> Any:
        """
        Process customer service analytics.
        """
        ...

    def reset_tracking_state(self: Any) -> None:
        """
        Reset all tracking state. Useful for starting a new session.
        """
        ...

