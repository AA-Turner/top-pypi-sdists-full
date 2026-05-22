"""Auto-generated stub for module: wrong_way_tracker."""
from typing import Any, Dict, List

# Constants
logger: Any

# Classes
class AutoReferenceState:
    # State for auto-reference direction estimation.

    ...
class ReferenceSource:
    # Source of reference direction.

    AUTO: str
    NONE: str
    USER_ZONE: str

class ReferenceStatus:
    # Status of reference direction estimation.

    CONFIRMED: str
    LEARNING: str
    NONE: str

class TrackMotionState:
    # Per-track motion state for trajectory-based detection.

    ...
class WrongWayDetectionTracker:
    # Trajectory-based wrong-way vehicle detection tracker.
    #
    # Uses EWMA velocity smoothing and continuous confidence accumulation
    # to detect vehicles moving against the expected traffic direction.
    #
    # Reference Direction Sources (in priority order):
    # 1. User-defined zone_config (first point → last point)
    # 2. Auto-estimation from observed traffic flow
    #
    # Auto-Reference Re-Learning:
    # - For AUTO sources, reference is periodically re-learned to adapt to
    #   changing traffic patterns (e.g., time-of-day flow changes)
    # - Re-learning interval configurable via auto_ref_relearn_interval_frames
    # - User-defined zones (USER_ZONE) are never re-learned

    def __init__(self: Any, alpha: float = 0.2, v_min: float = 1.2, beta: float = 0.1, gamma: float = 0.018, c_suspect: float = 0.25, c_confirm: float = 0.65, c_decay_from_wrong: float = 0.3, correct_direction_frames_to_decay: int = 20, min_confirm_frames: int = 12, stale_track_frames: int = 40, auto_ref_relearn_interval_frames: int = 108000, auto_ref_min_tracks: int = 5, auto_ref_warmup_frames: int = 90, auto_ref_alpha: float = 0.05, auto_ref_confirm_threshold: float = 0.7, auto_ref_stability_frames: int = 60) -> None: ...

    def get_reference_info(self: Any) -> Dict[str, Any]:
        """
        Get current reference direction information including re-learn status.
        """
        ...

    def get_stats(self: Any) -> Dict[str, Any]: ...

    def reset(self: Any) -> None: ...

    def set_reference_from_zone(self: Any, zone_polygon: List[List[float]]) -> bool: ...

    def update(self: Any, detections: List[Dict[str, Any]], current_frame: int) -> Dict[str, Any]: ...

class WrongWayState:
    # State machine states for wrong-way detection.

    NORMAL: str
    SUSPECT: str
    WRONG_WAY: str

