"""Auto-generated stub for module: landslide_detection."""
from typing import Any, Dict, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon

# Classes
class LandslideDetectionConfig:
    # Configuration for landslide detection post-processing.

    ...
class LandslideDetectionUseCase:
    # Post-processor for landslide detection model outputs.

    def __init__(self: Any) -> None: ...

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Return count of all track IDs currently visible in this frame.
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Return count of track IDs that appeared for the first time this frame.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return cumulative unique detection counts per category.
        """
        ...

    def process(self: Any, data: Any = None, config: Any = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run full landslide detection post-processing pipeline.
        
                Args:
                    data: Raw model detections (list or YOLO-style dict).
                    config: Must be a :class:`LandslideDetectionConfig` instance.
                    context: Optional processing context carrying metadata.
                    stream_info: Stream/video metadata used for timestamps.
        
                Returns:
                    :class:`ProcessingResult` containing ``agg_summary`` payload.
        """
        ...

