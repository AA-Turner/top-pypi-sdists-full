"""Auto-generated stub for module: illegal_parking_detection."""
from typing import Any, Dict, List, Optional, Set

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_iou, bbox_smoothing, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom10_center, get_bbox_bottom25_center, point_in_polygon
from ..utils.post_processing_config_client import PostProcessingConfigClient

# Constants
DEFAULT_INDEX_TO_CATEGORY: Dict[Any, Any]
DEFAULT_VEHICLE_CATEGORIES: List[Any]

# Classes
class IllegalParkingConfig:
    # Configuration for illegal parking detection.

    def validate(self: Any) -> List[str]: ...

class IllegalParkingDetectionUseCase:
    # Emit vehicle detections only after illegal-parking dwell threshold is met.

    def __init__(self: Any) -> None: ...

    OUTPUT_CATEGORY: str

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def set_config_client(self: Any, client: Any) -> None:
        """
        Set PostProcessingConfigClient for API zone polygons (by_app_deployment + camera_id).
        """
        ...

