"""Auto-generated stub for module: color_detection."""
from typing import Any, Dict, List, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..usecases.color.clip import ClipProcessor
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon

# Classes
class ColorDetectionConfig:
    # Configuration for color detection use case.

    def validate(self: Any) -> List[str]: ...

class ColorDetectionUseCase:
    # Color detection processor for analyzing object colors in video streams with tracking.

    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def color_helper(self: Any, curr_data: Any) -> Any: ...

    def create_default_config(self: Any, **overrides: Any) -> Any:
        """
        Create default configuration with optional overrides.
        """
        ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get JSON schema for configuration validation.
        """
        ...

    def get_total_category_counts(self: Any, data: Any) -> Any:
        """
        Return total unique track_id count per category (across all colors).
        """
        ...

    def get_total_color_counts(self: Any) -> Any:
        """
        Return total unique track_id count per color (across all categories).
        """
        ...

    def get_vehicle_stats(self: Any) -> Any:
        """
        Return the current global vehicle statistics as a normal dictionary.
        """
        ...

    def merge_color_summary(self: Any, detections_data: List[Dict[str, Any]], curr_frame_color: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine base detections with current frame color information and produce a color summary.
        Returns structure similar to _calculate_color_summary().
        """
        ...

    def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reset_all_tracking(self: Any) -> None:
        """
        Reset both advanced tracker and color tracking state.
        """
        ...

    def reset_color_tracking(self: Any) -> None:
        """
        Reset color tracking state.
        """
        ...

    def reset_tracker(self: Any) -> None:
        """
        Reset the advanced tracker instance.
        """
        ...

    def update_vehicle_stats(self: Any, frame_detections: dict) -> Any:
        """
        Update global vehicle statistics ensuring uniqueness per track_id and per zone.
        If the same vehicle (track_id) is seen again:
            - Ignore if confidence is lower.
            - Update its color if confidence is higher.
        """
        ...

