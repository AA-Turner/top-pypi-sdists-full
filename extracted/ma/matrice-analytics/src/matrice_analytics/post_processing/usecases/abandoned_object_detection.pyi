"""Auto-generated stub for module: abandoned_object_detection."""
from typing import Any, Dict, List

from ..Trackers import ConfigDrivenTracker, TrackerProfile, legacy_sort_tracker_overrides
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, ByteTrackWrapper, SORTTracker, apply_category_mapping, bbox_centroid, bbox_iou, bbox_smoothing, dist, filter_by_confidence, match_results_structure, smooth_point
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# Constants
ABANDONED_CLASS_ID: int

# Classes
class AbandonedObjectConfig:
    # Configuration for abandoned object detection.

    def validate(self: Any) -> List[str]: ...

class AbandonedObjectDetectionUseCase:
    # Detects abandoned objects using a velocity-based stationary state machine.
    #
    # Flow per frame:
    #     1. Filter by confidence
    #     2. Apply category mapping (index -> name)
    #     3. Smooth bboxes (optional)
    #     4. Track objects (SORT / ByteTrack)
    #     5. Update per-track abandonment state machine
    #     6. Enrich detections with is_abandoned flag
    #     7. Generate alerts (cooldown-enforced per track)
    #     8. Return agg_summary

    def __init__(self: Any) -> None: ...

    GLOBAL_ZONE_NAME: str

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Return count of NEW track_ids per category (first appearance under that category).
        """
        ...

    def get_total_counts(self: Any) -> Dict[str, int]:
        """
        Return total unique track_id counts per category.
        """
        ...

    def process(self: Any, data: Any, config: Any, context: Any | None = None, stream_info: Dict[str, Any] | None = None) -> Any: ...

