"""Auto-generated stub for module: people_counting_in_zone."""
from typing import Any, Dict, List, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig, ZoneConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure

# Classes
class ByteTrackWrapper:
    # Wraps ultralytics ``BYTETracker`` so it accepts / returns pipeline
    #     detection dicts (``List[Dict]``) instead of raw numpy / Boxes objects.
    #
    #     Follows the same tracking flow as the reference ``people_counter.py``:
    #
    #     1. Convert detection dicts → ``_MockResults`` (mimics ultralytics Boxes).
    #     2. Call ``BYTETracker.update(det, img, feats)`` exactly like the reference.
    #     3. Build **new** detection dicts from the tracker output – tracked
    #        (Kalman-filtered) bounding boxes replace the raw detections, and every
    #        dict carries a ``track_id`` assigned by ByteTrack.
    #
    #     Only *confirmed* tracks are returned; untracked / low-confidence detections
    #     that ByteTrack has not yet promoted to active tracks are dropped (standard
    #     ByteTrack behaviour).

    def __init__(self: Any, track_high_thresh: float = 0.3, track_low_thresh: float = 0.1, new_track_thresh: float = 0.4, track_buffer: int = 60, match_thresh: float = 0.8, fuse_score: bool = True, frame_rate: int = 30) -> None: ...

    def update(self: Any, detections: List[Dict]) -> List[Dict]:
        """
        Run one tracking step.
        
                Parameters
                ----------
                detections : list[dict]
                    Pipeline detection dicts.  Each must contain ``bounding_box``
                    (``{xmin, ymin, xmax, ymax}`` **or** ``{x1, y1, x2, y2}``)
                    and ``confidence``.
        
                Returns
                -------
                list[dict]
                    One dict per **confirmed track** with Kalman-filtered bounding
                    boxes, ``track_id``, ``confidence``, ``category`` and
                    ``category_id``.
        """
        ...

class PeopleCountingInZoneConfig:
    # Configuration for people counting use case.

    def validate(self: Any) -> List[str]:
        """
        Validate people counting configuration.
        """
        ...

class PeopleCountingInZoneUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared for the FIRST TIME EVER in this frame.
        
                This counts only track IDs that have never been seen before (not in total set).
                Re-entries (person leaves and comes back) are NOT counted as new.
        """
        ...

    def get_total_counts(self: Any) -> Any: ...

    def process(self: Any, data: Any, config: Any, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

