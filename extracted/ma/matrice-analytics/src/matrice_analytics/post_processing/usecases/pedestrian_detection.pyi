"""Auto-generated stub for module: pedestrian_detection."""
from typing import Any, Dict, Optional, Set

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.post_processing_config_client import PostProcessingConfigClient

# Classes
class PedestrianDetectionConfig:
    # Configuration for pedestrian detection use case in pedestrian monitoring.

    ...
class PedestrianDetectionUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Return count of track IDs confirmed as new for the first time this frame.
        
                A track is counted as new only after appearing for at least
                ``_min_confirm_frames`` consecutive frames, matching people_counting behaviour.
                Each ID is reported exactly once across all frames.
        """
        ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique confirmed track_id count for each category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Main entry point for  post-processing.
        Applies category mapping, smoothing, counting, alerting, and summary generation.
        Returns a ProcessingResult with all relevant outputs.
        """
        ...

    def set_config_client(self: Any, client: Optional[Any]) -> None:
        """
        Set the PostProcessingConfigClient used to resolve zones from API (by_app_deployment, camera_id).
        """
        ...

