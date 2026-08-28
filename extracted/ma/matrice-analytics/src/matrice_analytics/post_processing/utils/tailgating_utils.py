import logging
import math
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class CrossingRecord:
    track_id: Any
    timestamp: float


@dataclass
class AccessEvent:
    """One authorization window for a single (access_line, direction) pair."""

    event_id: str
    access_line_id: str
    direction: str
    start_ts: float
    access_window_sec: float
    crossings: List[CrossingRecord] = field(default_factory=list)
    last_crossing_ts: float = 0.0
    closed: bool = False


class AccessPointState:
    """Per (access_line, direction) lifecycle state. No geometry, no analytics.

    Replaces the old per-door ``DoorRuntime``: geometry is now shared (two zones)
    and the access-event state machine is keyed by access line *and* crossing
    direction, so opposite-direction passages never interfere.
    """

    def __init__(self, access_line_id: str, direction: str):
        self.access_line_id = access_line_id
        self.direction = direction

        # --- active event ---
        self.active_event: Optional[AccessEvent] = None

        # --- cooldown handling ---
        self.cooldown_until_ts: float = 0.0

        # --- misc runtime ---
        self.last_activity_ts: Optional[float] = None


@dataclass
class PassageAnalysisResult:
    total_crossings: int
    ordered_crossings: List[Any]
    suspected_tailgaters: List[Any]
    confidence: float
    debug: Dict[str, Any]


# ============================================================
# ACCESS EVENT STATE MACHINE
# ============================================================


class AccessEventManager:
    """Manages access-window lifecycle only. No geometry. No analytics."""

    def can_open(self, state: AccessPointState, now_ts: float) -> bool:
        return state.active_event is None and now_ts >= state.cooldown_until_ts

    def open_event(
        self,
        state: AccessPointState,
        access_window_sec: float,
        now_ts: float,
    ) -> AccessEvent:
        event = AccessEvent(
            event_id=str(uuid.uuid4()),
            access_line_id=state.access_line_id,
            direction=state.direction,
            start_ts=now_ts,
            access_window_sec=access_window_sec,
            last_crossing_ts=now_ts,
        )
        state.active_event = event
        return event

    def add_crossing(self, event: AccessEvent, crossing: CrossingRecord) -> None:
        # dedupe per track
        if any(c.track_id == crossing.track_id for c in event.crossings):
            return

        event.crossings.append(crossing)
        event.last_crossing_ts = crossing.timestamp

    def should_close(
        self,
        event: AccessEvent,
        _state: AccessPointState,
        now_ts: float,
        silence_timeout_sec: float,
    ) -> bool:
        _ = (_state,)
        # hard window end
        if now_ts - event.start_ts >= event.access_window_sec:
            return True

        # silence after last crossing
        if event.crossings and now_ts - event.last_crossing_ts >= silence_timeout_sec:
            return True

        return False

    def close_event(
        self,
        state: AccessPointState,
        cooldown_sec: float,
        now_ts: float,
    ) -> Optional[AccessEvent]:
        event = state.active_event
        if not event:
            return None

        event.closed = True
        state.active_event = None
        state.cooldown_until_ts = now_ts + cooldown_sec

        return event


# ============================================================
# GEOMETRY UTILITIES
# ============================================================


def normalize(v: Tuple[float, float]) -> Tuple[float, float]:
    mag = math.hypot(v[0], v[1])
    if mag < 1e-6:
        return (0.0, 0.0)
    return (v[0] / mag, v[1] / mag)


def motion_vector(p0, p1) -> Tuple[float, float]:
    return (p1[0] - p0[0], p1[1] - p0[1])


def signed_distance(point, p1, p2) -> float:
    """Signed distance from the infinite line through ``p1``/``p2``."""
    x0, y0 = point
    x1, y1 = p1
    x2, y2 = p2

    dx, dy = x2 - x1, y2 - y1
    denom = math.hypot(dx, dy)
    if denom < 1e-6:
        return 0.0

    return ((x0 - x1) * dy - (y0 - y1) * dx) / denom


def polygon_centroid(poly: List[List[float]]) -> Tuple[float, float]:
    """Arithmetic centroid of polygon vertices (sufficient for side assignment)."""
    if not poly:
        return (0.0, 0.0)
    n = len(poly)
    sx = sum(float(p[0]) for p in poly)
    sy = sum(float(p[1]) for p in poly)
    return (sx / n, sy / n)


def build_side_zone_map(
    line_p1,
    line_p2,
    zones: Dict[str, List[List[float]]],
) -> Optional[Dict[int, str]]:
    """Map the two sides of an access line to the two shared zone names.

    Uses each zone's centroid signed distance to the line. Returns
    ``{1: zone_on_positive_side, -1: zone_on_negative_side}`` or ``None`` when the
    configuration is degenerate (not exactly two zones, or both centroids fall on
    the same side / on the line). A ``None`` result means direction can still be
    detected but cannot be labelled with zone names.
    """
    items = list(zones.items())
    if len(items) != 2:
        return None
    (k_a, poly_a), (k_b, poly_b) = items
    d_a = signed_distance(polygon_centroid(poly_a), line_p1, line_p2)
    d_b = signed_distance(polygon_centroid(poly_b), line_p1, line_p2)
    if d_a == 0.0 or d_b == 0.0 or (d_a > 0) == (d_b > 0):
        logger.warning(
            "tailgating: access line does not separate the two zones "
            "(centroid signed distances %.3f / %.3f); zone labels unavailable",
            d_a,
            d_b,
        )
        return None
    if d_a > 0:
        return {1: k_a, -1: k_b}
    return {1: k_b, -1: k_a}


# ============================================================
# CROSSING DETECTION
# ============================================================


def _extend_segment(l0, l1, padding: float):
    """Extend a segment by ``padding`` pixels beyond each endpoint along its axis."""
    if padding <= 0:
        return l0, l1
    dx, dy = l1[0] - l0[0], l1[1] - l0[1]
    mag = math.hypot(dx, dy)
    if mag < 1e-6:
        return l0, l1
    ux, uy = dx / mag, dy / mag
    return (
        (l0[0] - ux * padding, l0[1] - uy * padding),
        (l1[0] + ux * padding, l1[1] + uy * padding),
    )


def segment_intersects_line(p0, p1, l0, l1, padding: float = 0.0) -> bool:
    """True when segment ``p0->p1`` crosses the finite segment ``l0->l1``.

    ``padding`` optionally extends the access-line segment beyond its endpoints so
    a doorway drawn slightly shorter than the walkable opening still registers.
    """
    if padding:
        l0, l1 = _extend_segment(l0, l1, padding)

    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    o1 = orient(p0, p1, l0)
    o2 = orient(p0, p1, l1)
    o3 = orient(l0, l1, p0)
    o4 = orient(l0, l1, p1)

    return o1 * o2 < 0 and o3 * o4 < 0


def detect_crossing(
    track_side_state: Dict[str, Any],
    foot,
    line_p1,
    line_p2,
    *,
    side_margin: float,
    min_motion_magnitude: float,
    endpoint_padding: float = 0.0,
) -> Tuple[bool, Optional[int]]:
    """Anchored, bidirectional crossing detector for one ``(line, track)`` pair.

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
    d = signed_distance(foot, line_p1, line_p2)

    # In the gap / on the line: hold the anchor, never fire.
    if abs(d) < side_margin:
        return False, None

    cur_side = 1 if d > 0 else -1
    last_side = track_side_state.get("last_side")
    last_pt = track_side_state.get("last_side_pt")

    crossed = False
    direction: Optional[int] = None
    if last_side is not None and last_pt is not None and cur_side != last_side:
        mv = motion_vector(last_pt, foot)
        if math.hypot(mv[0], mv[1]) >= min_motion_magnitude and segment_intersects_line(
            last_pt, foot, line_p1, line_p2, padding=endpoint_padding
        ):
            crossed = True
            direction = cur_side
            logger.debug(
                "detect_crossing: crossed line direction=%s d=%.3f", cur_side, d
            )

    # Re-anchor to the current clear side (enables back-and-forth re-detection).
    track_side_state["last_side"] = cur_side
    track_side_state["last_side_pt"] = foot
    return crossed, direction


# ============================================================
# SIMPLE PASSAGE ANALYSIS
# ============================================================


def analyze_passage(
    crossings: List[CrossingRecord],
    allowed_persons: int,
    max_follow_dt: float,
) -> PassageAnalysisResult:
    if not crossings:
        return PassageAnalysisResult(0, [], [], 0.0, {})

    ordered = sorted(crossings, key=lambda c: c.timestamp)
    ids = [c.track_id for c in ordered]
    total = len(ordered)

    if total <= allowed_persons:
        return PassageAnalysisResult(total, ids, [], 0.0, {})

    suspects = []
    last_authorized_ts = ordered[0].timestamp

    for c in ordered[1:]:
        dt = c.timestamp - last_authorized_ts
        if dt <= max_follow_dt:
            suspects.append(c.track_id)
        else:
            last_authorized_ts = c.timestamp

    confidence = 0.9 if suspects else 0.0

    return PassageAnalysisResult(
        total,
        ids,
        suspects,
        confidence,
        {"severity": "critical", "reason": "close_follow"},
    )
