import logging
import math
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from .geometry_utils import point_in_polygon

logger = logging.getLogger(__name__)


@dataclass
class CrossingRecord:
    track_id: Any
    timestamp: float


@dataclass
class AccessEvent:
    event_id: str
    door_id: str
    start_ts: float
    access_window_sec: float
    crossings: List[CrossingRecord] = field(default_factory=list)
    last_crossing_ts: float = 0.0
    closed: bool = False


class DoorRuntime:
    def __init__(self, door_id):
        self.door_id = door_id

        # --- geometry ---
        self.entry_normal = None

        # --- crossing memory ---
        self.last_crossing_ts = None
        self.crossings_in_window = []

        # --- active event ---
        self.active_event = None

        # --- cooldown handling ---
        self.cooldown_until_ts = 0

        # --- misc runtime ---
        self.last_activity_ts = None


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
    """
    Manages access-window lifecycle only.
    No geometry. No analytics.
    """

    def can_open(self, door: DoorRuntime, now_ts: float) -> bool:
        return door.active_event is None and now_ts >= door.cooldown_until_ts

    def open_event(
        self,
        door: DoorRuntime,
        access_window_sec: float,
        now_ts: float,
    ) -> AccessEvent:
        event = AccessEvent(
            event_id=str(uuid.uuid4()),
            door_id=door.door_id,
            start_ts=now_ts,
            access_window_sec=access_window_sec,
            last_crossing_ts=now_ts,
        )
        door.active_event = event
        return event

    def add_crossing(self, event: AccessEvent, crossing: CrossingRecord):
        # dedupe per track
        if any(c.track_id == crossing.track_id for c in event.crossings):
            return

        event.crossings.append(crossing)
        event.last_crossing_ts = crossing.timestamp

    def should_close(
        self,
        event: AccessEvent,
        _door: DoorRuntime,
        now_ts: float,
        silence_timeout_sec: float,
    ) -> bool:
        # hard window end
        _ = (_door,)
        if now_ts - event.start_ts >= event.access_window_sec:
            return True

        # silence after last crossing
        if event.crossings and now_ts - event.last_crossing_ts >= silence_timeout_sec:
            return True

        return False

    def close_event(
        self,
        door: DoorRuntime,
        cooldown_sec: float,
        now_ts: float,
    ) -> Optional[AccessEvent]:
        event = door.active_event
        if not event:
            return None

        event.closed = True
        door.active_event = None
        door.cooldown_until_ts = now_ts + cooldown_sec

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
    """
    Signed distance from infinite line.
    """
    x0, y0 = point
    x1, y1 = p1
    x2, y2 = p2

    dx, dy = x2 - x1, y2 - y1
    denom = math.hypot(dx, dy)
    if denom < 1e-6:
        return 0.0

    return ((x0 - x1) * dy - (y0 - y1) * dx) / denom


def compute_entry_normal(p1, p2, secured_side_point):
    """
    Normal pointing into secured zone.
    """
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]

    n1 = (-dy, dx)
    n2 = (dy, -dx)

    mid = ((p1[0] + p2[0]) * 0.5, (p1[1] + p2[1]) * 0.5)
    v = (
        secured_side_point[0] - mid[0],
        secured_side_point[1] - mid[1],
    )

    return normalize(n1 if n1[0] * v[0] + n1[1] * v[1] > 0 else n2)


# ============================================================
# CROSSING DETECTION
# ============================================================


def segment_intersects_line(p0, p1, l0, l1):
    """
    Segment intersection test.
    """

    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    o1 = orient(p0, p1, l0)
    o2 = orient(p0, p1, l1)
    o3 = orient(l0, l1, p0)
    o4 = orient(l0, l1, p1)

    return o1 * o2 < 0 and o3 * o4 < 0


def detect_crossing(
    prev_pt,
    curr_pt,
    line_p1,
    line_p2,
    secured_zone,
    min_motion_magnitude=0.002,
    line_intersection_tolerance=0.02,
    enable_direction_validation=True,
    entry_normal=None,
):
    if prev_pt is None:
        return False

    mv = motion_vector(prev_pt, curr_pt)
    mv_mag = math.hypot(mv[0], mv[1])
    if mv_mag < min_motion_magnitude:
        return False

    intersects = segment_intersects_line(
        prev_pt,
        curr_pt,
        line_p1,
        line_p2,
    )

    if not intersects:
        return False

    d_curr = signed_distance(curr_pt, line_p1, line_p2)

    prev_inside = point_in_polygon(prev_pt, secured_zone)
    curr_inside = point_in_polygon(curr_pt, secured_zone)

    entered_zone = (not prev_inside) and curr_inside
    exited_zone = prev_inside and not curr_inside
    _ = (entry_normal, enable_direction_validation)
    near_line = abs(d_curr) < line_intersection_tolerance

    logger.debug(
        "detect_crossing: prev_inside=%s curr_inside=%s near_line=%s",
        prev_inside,
        curr_inside,
        near_line,
    )

    return entered_zone or exited_zone or near_line


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
        {"severity": "alert", "reason": "close_follow"},
    )
