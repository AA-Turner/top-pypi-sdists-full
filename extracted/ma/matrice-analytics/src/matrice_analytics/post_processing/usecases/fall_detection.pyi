"""Auto-generated stub for module: fall_detection."""
from typing import Any, Dict, List, Optional

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon

# Classes
class FallConfirmationConfig:
    # Configuration for fall detection confirmation layer.

    ...
class FallConfirmationLayer:
    # Per-track temporal + confidence-weighted fall confirmation.
    #
    # For each tracked person, maintains a rolling window of recent
    # (classification, confidence) observations. A fall detection is
    # confirmed only when:
    #   1. The confidence-weighted fall score >= confirm_threshold
    #   2. At least min_fall_frames in the window are classified as fall
    #
    # This suppresses:
    #   - Flickering FPs (1-3 frame bursts) → score too low
    #   - Low-confidence sustained misclassification → confidence drags score down
    #   - Single high-confidence glitches → blocked by min_fall_frames

    def __init__(self: Any, config: Optional[Any] = None) -> None: ...

    def get_stats(self: Any) -> Dict[str, Any]:
        """
        Return confirmation layer statistics.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset all state. Call when switching streams or restarting.
        """
        ...

    def update(self: Any, detections: List[Dict]) -> List[Dict]:
        """
        Process tracked detections and apply fall confirmation logic.
        
        Args:
            detections: List of detection dicts from the tracker.
                Each must have: 'track_id', 'category', 'confidence', 'bounding_box'
        
        Returns:
            Filtered/modified detections list. Non-fall detections pass through unchanged.
            Fall detections are either confirmed (passed through) or suppressed
            (dropped or reclassified based on config.suppression_mode).
        """
        ...

class FallDetectionConfig:
    # Configuration for fall detection in people analytics usecase.

    ...
class FallDetectionUseCase:
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

