"""Auto-generated stub for module: flood_detection."""
from typing import Any, Dict, Optional, Tuple

from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, ByteTrackWrapper, SORTTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon

# Classes
class FloodDetectionConfig:
    # Configuration for flood detection post-processing.

    ...
class FloodDetectionUseCase:
    # Post-processor for flood detection model outputs.

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

    def get_resolution(self: Any, camera_id: str) -> Tuple[Optional[int], Optional[int]]:
        """
        Fetch frame width/height for *camera_id* via CameraManagement API.
        
                Mirrors the same method in :class:`FootfallProcessor` so that flood
                detection can normalise segmentation-mask areas to a percentage of the
                real frame.
        
                Returns
                -------
                tuple of (width, height) in pixels, or (None, None) on failure.
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return cumulative unique detection counts per category.
        """
        ...

    def process(self: Any, data: Any = None, config: Any = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Run full flood detection post-processing pipeline.
        
                Args:
                    data: Raw model detections (list or YOLO-style dict).
                    config: Must be a :class:`FloodDetectionConfig` instance.
                    context: Optional processing context carrying metadata.
                    stream_info: Stream/video metadata used for timestamps.
        
                Returns:
                    :class:`ProcessingResult` containing ``agg_summary`` payload.
        """
        ...

