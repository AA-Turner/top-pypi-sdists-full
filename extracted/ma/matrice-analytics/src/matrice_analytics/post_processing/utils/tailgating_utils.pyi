"""Auto-generated stub for module: tailgating_utils."""
from typing import Any, Dict, List, Optional, Tuple

# Constants
logger: Any

# Functions
def analyze_passage(crossings: List[Any], allowed_persons: int, max_follow_dt: float) -> Any: ...
def build_side_zone_map(line_p1: Any, line_p2: Any, zones: Dict[str, List[List[float]]]) -> Optional[Dict[int, str]]:
    """
    Map the two sides of an access line to the two shared zone names.
    
        Uses each zone's centroid signed distance to the line. Returns
        ``{1: zone_on_positive_side, -1: zone_on_negative_side}`` or ``None`` when the
        configuration is degenerate (not exactly two zones, or both centroids fall on
        the same side / on the line). A ``None`` result means direction can still be
        detected but cannot be labelled with zone names.
    """
    ...
def detect_crossing(track_side_state: Dict[str, Any], foot: Any, line_p1: Any, line_p2: Any) -> Tuple[bool, Optional[int]]:
    """
    Anchored, bidirectional crossing detector for one ``(line, track)`` pair.
    
        ``track_side_state`` is a mutable dict holding ``last_side`` (``+1``/``-1`` of the
        most recent *clear* side) and ``last_side_pt`` (the foot point recorded there).
    
        The detector is robust to the gap between the zone polygons and the access
        line: while the foot is within ``side_margin`` of the line (i.e. in the gap or
        on the line, typically inside neither polygon) the anchor is **held** and
        nothing fires. A crossing is reported only when the foot reaches the opposite
        *clear* side and the straight path from the anchor to the current foot
        intersects the finite access-line segment. Because attribution uses the finite
        segment, walking around a line end does not count, and an arbitrarily wide gap
        in the middle of the traversal does not suppress detection.
    
        Returns ``(crossed, direction)`` where ``direction`` is ``+1`` when the foot
        crossed onto the positive side of the line and ``-1`` onto the negative side.
        Mutates ``track_side_state`` in place.
    """
    ...
def motion_vector(p0: Any, p1: Any) -> Tuple[float, float]: ...
def normalize(v: Tuple[float, float]) -> Tuple[float, float]: ...
def polygon_centroid(poly: List[List[float]]) -> Tuple[float, float]:
    """
    Arithmetic centroid of polygon vertices (sufficient for side assignment).
    """
    ...
def segment_intersects_line(p0: Any, p1: Any, l0: Any, l1: Any, padding: float = 0.0) -> bool:
    """
    True when segment ``p0->p1`` crosses the finite segment ``l0->l1``.
    
        ``padding`` optionally extends the access-line segment beyond its endpoints so
        a doorway drawn slightly shorter than the walkable opening still registers.
    """
    ...
def signed_distance(point: Any, p1: Any, p2: Any) -> float:
    """
    Signed distance from the infinite line through ``p1``/``p2``.
    """
    ...

# Classes
class AccessEvent:
    # One authorization window for a single (access_line, direction) pair.

    ...
class AccessEventManager:
    # Manages access-window lifecycle only. No geometry. No analytics.

    def add_crossing(self: Any, event: Any, crossing: Any) -> None: ...

    def can_open(self: Any, state: Any, now_ts: float) -> bool: ...

    def close_event(self: Any, state: Any, cooldown_sec: float, now_ts: float) -> Optional[Any]: ...

    def open_event(self: Any, state: Any, access_window_sec: float, now_ts: float) -> Any: ...

    def should_close(self: Any, event: Any, _state: Any, now_ts: float, silence_timeout_sec: float) -> bool: ...

class AccessPointState:
    # Per (access_line, direction) lifecycle state. No geometry, no analytics.
    #
    #     Replaces the old per-door ``DoorRuntime``: geometry is now shared (two zones)
    #     and the access-event state machine is keyed by access line *and* crossing
    #     direction, so opposite-direction passages never interfere.

    def __init__(self: Any, access_line_id: str, direction: str) -> None: ...

class CrossingRecord:
    ...
class PassageAnalysisResult:
    ...
