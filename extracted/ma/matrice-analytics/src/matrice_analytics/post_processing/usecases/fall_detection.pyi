"""Auto-generated stub for module: fall_detection."""
from typing import Any, Dict, List, Optional

from ..Trackers import ConfigDrivenTracker, TrackerProfile
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, count_objects_in_zones, filter_by_confidence, match_results_structure
from ..utils.geometry_utils import get_bbox_bottom25_center, point_in_polygon
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# Classes
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

class PoseFallConfig:
    # Configuration for the pose-based (3-step) fall detector.

    ...
class PoseFallDetector:
    # Per-track 3-step fall detection (drop -> flat -> stayed down).
    #
    # For each tracked person, runs a state machine that requires a sudden fast
    # drop, followed by a horizontal posture, followed by staying down for a few
    # seconds without getting up. Only then is the detection relabeled to
    # ``fall_class``; everything else passes through unchanged.

    def __init__(self: Any, config: Optional[Any] = None) -> None: ...

    def get_stats(self: Any) -> Dict[str, Any]:
        """
        Return detector statistics.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset all state. Call when switching streams or restarting.
        """
        ...

    def update(self: Any, detections: List[Dict], frame_h: Optional[int] = None) -> List[Dict]:
        """
        Process tracked detections and apply the 3-step fall detection.
        
        Args:
            detections: detection dicts from the tracker. Each should have
                'track_id', 'bounding_box', and ideally 'keypoints'.
            frame_h: stream frame height in pixels, used to normalize the
                vertical-drop signal (Step 1). Required for the drop step; when
                absent, the drop can't be measured so no fall is confirmed.
        
        Returns:
            The detections list with confirmed falls relabeled to ``fall_class``.
            Untracked detections pass through unchanged.
        """
        ...

