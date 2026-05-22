"""Auto-generated stub for module: car_service."""
from typing import Any, Dict, List, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import CarServiceConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, calculate_distance, filter_by_confidence, get_bbox_center, match_results_structure, point_in_polygon

# Functions
def assign_person_by_area(detections: Any, _car_areas: Any, staff_areas: Any) -> Any:
    """
    Assigns category detections to 'staff' or 'car' based on their location in area polygons.
    Modifies the detection list in-place.
    Args:
        detections: List of detection dicts.
        car_areas: Dict of area_name -> polygon (list of [x, y]).
        staff_areas: Dict of area_name -> polygon (list of [x, y]).
    """
    ...

# Classes
class CarServiceUseCase:
    def __init__(self: Any) -> None:
        """
        Initialize car service use case.
        """
        ...

    DEFAULT_ALERT_EMAIL: str

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
        Get configuration schema for car service.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[dict] = None) -> Any:
        """
        Process advanced car service analytics.
        """
        ...

