"""
Counting utilities for post-processing operations.
"""

import time
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from .geometry_utils import get_bbox_bottom_center, point_in_polygon, to_zone_test_point


def count_objects_by_category(results: Any) -> Dict[str, int]:
    """
    Count objects by category from detection results.

    Args:
        results: Detection results (list or dict format)

    Returns:
        Dict[str, int]: Category counts
    """
    counts = defaultdict(int)

    if isinstance(results, list):
        # Detection format
        for detection in results:
            category = detection.get("category", "unknown")
            counts[category] += 1

    elif isinstance(results, dict):
        # Frame-based format (tracking or activity recognition)
        seen_tracks = set()  # To avoid double counting same track across frames

        for frame_id, detections in results.items():
            if isinstance(detections, list):
                for detection in detections:
                    category = detection.get("category", "unknown")
                    track_id = detection.get("track_id")

                    # If tracking data is available, count unique tracks only
                    if track_id is not None:
                        track_key = f"{category}_{track_id}"
                        if track_key not in seen_tracks:
                            seen_tracks.add(track_key)
                            counts[category] += 1
                    else:
                        # No tracking, count all detections
                        counts[category] += 1

    return dict(counts)


def count_objects_in_zones(
    results: Any, zones: Dict[str, List[List[float]]], stream_info: Optional[Any] = None
) -> Dict[str, Dict[str, int]]:
    """
    Count objects in defined zones.

    Args:
        results: Detection results
        zones: Dictionary of zone_name -> polygon coordinates

    Returns:
        Dict[str, Dict[str, int]]: Zone counts by category
    """
    zone_counts = {}

    for zone_name, zone_polygon in zones.items():
        zone_counts[zone_name] = defaultdict(int)

        if isinstance(results, list):
            # Detection format
            for detection in results:
                if _is_detection_in_zone(detection, zone_polygon, stream_info):
                    category = detection.get("category", "unknown")
                    zone_counts[zone_name][category] += 1

        elif isinstance(results, dict):
            # Frame-based format
            seen_tracks = set()

            for frame_id, detections in results.items():
                if isinstance(detections, list):
                    for detection in detections:
                        if _is_detection_in_zone(detection, zone_polygon, stream_info):
                            category = detection.get("category", "unknown")
                            track_id = detection.get("track_id")

                            if track_id is not None:
                                track_key = f"{zone_name}_{category}_{track_id}"
                                if track_key not in seen_tracks:
                                    seen_tracks.add(track_key)
                                    zone_counts[zone_name][category] += 1
                            else:
                                zone_counts[zone_name][category] += 1

        # Convert to regular dict
        zone_counts[zone_name] = dict(zone_counts[zone_name])

    return zone_counts


def count_unique_tracks(results: Dict[str, List[Dict]]) -> Dict[str, int]:
    """
    Count unique tracks by category from tracking results.

    Args:
        results: Tracking results in frame format

    Returns:
        Dict[str, int]: Unique track counts by category
    """
    unique_tracks = defaultdict(set)

    for frame_id, detections in results.items():
        if isinstance(detections, list):
            for detection in detections:
                track_id = detection.get("track_id")
                category = detection.get("category", "unknown")

                if track_id is not None:
                    unique_tracks[category].add(track_id)

    return {category: len(tracks) for category, tracks in unique_tracks.items()}


def calculate_counting_summary(results: Any, zones: Optional[Dict[str, List[List[float]]]] = None) -> Dict[str, Any]:
    """
    Calculate comprehensive counting summary.

    Args:
        results: Detection/tracking results
        zones: Optional zone definitions

    Returns:
        Dict[str, Any]: Comprehensive counting summary
    """
    summary = {"total_objects": 0, "by_category": {}, "timestamp": time.time()}

    # Basic category counts
    category_counts = count_objects_by_category(results)
    summary["by_category"] = category_counts
    summary["total_objects"] = sum(category_counts.values())

    # Zone-based counts if zones provided
    if zones:
        zone_counts = count_objects_in_zones(results, zones)
        summary["zone_analysis"] = zone_counts

        # Calculate zone totals
        zone_totals = {}
        for zone_name, zone_data in zone_counts.items():
            zone_totals[zone_name] = sum(zone_data.values())
        summary["zone_totals"] = zone_totals

    # Tracking-specific counts
    if isinstance(results, dict):
        unique_counts = count_unique_tracks(results)
        if unique_counts:
            summary["unique_tracks"] = unique_counts
            summary["total_unique_tracks"] = sum(unique_counts.values())

    return summary


def _is_detection_in_zone(
    detection: Dict[str, Any],
    zone_polygon: List[List[float]],
    stream_info: Optional[Any] = None,
) -> bool:
    """Check if a detection is within a zone polygon."""
    bbox = detection.get("bounding_box", detection.get("bbox"))
    if not bbox:
        return False
    if stream_info:  # This code ensures that if zone is bigger than the stream resolution, then whole frame is considered as in the zone.
        for p in zone_polygon:
            if (
                p[0] > stream_info.get("stream_resolution", {}).get("width", 0)
                and stream_info.get("stream_resolution", {}).get("width", 0) != 0
            ):
                return True
            if (
                p[1] > stream_info.get("stream_resolution", {}).get("height", 0)
                and stream_info.get("stream_resolution", {}).get("height", 0) != 0
            ):
                return True
    foot_center = get_bbox_bottom_center(bbox)
    # `zone_polygon` is pixel-space (denormalized from the API against the camera's
    # real resolution -- see intrusion_detection.py::_resolve_geometry_from_api);
    # `bbox` may be normalized 0-1 (the newer coordinate-frame convention). Scale
    # the point to match, or this test silently never matches on a normalized feed.
    foot_center = to_zone_test_point(foot_center, bbox, stream_info)
    return point_in_polygon(foot_center, [(p[0], p[1]) for p in zone_polygon])


# ============================================================================
# Geometry helpers for counting
# ============================================================================


def _line_intersection(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray, p4: np.ndarray) -> Optional[Tuple[float, float]]:
    """Intersection of line p1->p2 with line p3->p4. Returns (x,y) or None if parallel."""
    da = p2 - p1
    db = p4 - p3
    denom = da[0] * db[1] - da[1] * db[0]
    if abs(denom) < 1e-10:
        return None
    t = ((p3[0] - p1[0]) * db[1] - (p3[1] - p1[1]) * db[0]) / denom
    return (float(p1[0] + t * da[0]), float(p1[1] + t * da[1]))


def polygon_offset_inward(polygon: np.ndarray, offset: float) -> np.ndarray:
    """
    Inset polygon inward by a constant offset (in pixels).
    Each edge is shifted inward along its inward-pointing normal; new vertices
    are the intersections of consecutive shifted edges.

    Args:
        polygon: (N, 2) array of polygon vertices
        offset: Number of pixels to inset

    Returns:
        np.ndarray: Inset polygon vertices (N, 2), dtype int32
    """
    if offset <= 0:
        return polygon.astype(np.float64)
    n = len(polygon)
    poly = np.array(polygon, dtype=np.float64)
    centroid = poly.mean(axis=0)
    new_verts = []
    for i in range(n):
        a = poly[i]
        b = poly[(i + 1) % n]
        prev_a = poly[(i - 1) % n]
        e = b - a
        L = np.sqrt(np.dot(e, e)) + 1e-10
        perp1 = np.array([-e[1], e[0]]) / L
        perp2 = np.array([e[1], -e[0]]) / L
        mid = 0.5 * (a + b)
        to_center = centroid - mid
        inward = perp1 if np.dot(perp1, to_center) > 0 else perp2
        a_off = a + inward * offset
        b_off = b + inward * offset
        e_prev = a - prev_a
        L_prev = np.sqrt(np.dot(e_prev, e_prev)) + 1e-10
        in_prev = np.array([-e_prev[1], e_prev[0]]) / L_prev
        if np.dot(in_prev, centroid - (0.5 * (prev_a + a))) < 0:
            in_prev = -in_prev
        prev_a_off = prev_a + in_prev * offset
        a_off_prev = a + in_prev * offset
        pt = _line_intersection(np.array(prev_a_off), np.array(a_off_prev), np.array(a_off), np.array(b_off))
        if pt is not None:
            new_verts.append(pt)
        else:
            new_verts.append((float(a_off[0]), float(a_off[1])))
    return np.array(new_verts, dtype=np.int32)


def parse_line_config(line_config) -> np.ndarray:
    """
    Parse a line definition into a (2, 2) numpy array.

    Accepts either:
      - [x1, y1, x2, y2]        (flat list)
      - [[x1, y1], [x2, y2]]    (nested list)

    Returns:
        np.ndarray: shape (2, 2) with dtype float64
    """
    if hasattr(line_config[0], "__len__") and not isinstance(line_config[0], (int, float)):
        return np.array(line_config, dtype=np.float64)
    return np.array(
        [[line_config[0], line_config[1]], [line_config[2], line_config[3]]],
        dtype=np.float64,
    )


# ============================================================================
# Counter Classes
# ============================================================================


class ABLineCounter:
    """Manages trap zone [two AB lines] counting: count only on full crossing A -> zone -> B or B -> zone -> A."""

    # Sentinel value for points outside segment extent
    OUTSIDE_SEGMENT_EXTENT = -2

    def __init__(
        self,
        line_a: np.ndarray,
        line_b: np.ndarray,
        in_direction: str = "A_to_B",
        use_foot_center: bool = False,
    ):
        """
        Initialize trap zone counter.

        Args:
            line_a: (2, 2) array — rows are segment start and end for Line A
            line_b: (2, 2) array — rows are segment start and end for Line B
            in_direction: "A_to_B" (crossing A then B = In) or "B_to_A" (crossing B then A = In)
            use_foot_center: if True use bottom-center (foot) of bbox for logic; else use bbox center
        """
        self.line_a = np.asarray(line_a, dtype=np.float64)
        self.line_b = np.asarray(line_b, dtype=np.float64)
        self.in_direction = in_direction
        self.use_foot_center = use_foot_center

        # Pre-extract scalar coordinates to avoid per-call numpy allocations
        self._a1x, self._a1y = float(self.line_a[0][0]), float(self.line_a[0][1])
        self._a2x, self._a2y = float(self.line_a[1][0]), float(self.line_a[1][1])
        self._b1x, self._b1y = float(self.line_b[0][0]), float(self.line_b[0][1])
        self._b2x, self._b2y = float(self.line_b[1][0]), float(self.line_b[1][1])

        # Pre-compute direction vectors and squared lengths for projection
        self._a_dx = self._a2x - self._a1x
        self._a_dy = self._a2y - self._a1y
        self._a_len_sq = self._a_dx * self._a_dx + self._a_dy * self._a_dy

        self._b_dx = self._b2x - self._b1x
        self._b_dy = self._b2y - self._b1y
        self._b_len_sq = self._b_dx * self._b_dx + self._b_dy * self._b_dy

        # Pre-compute zone-side invariants (which side of each line the zone is on)
        mid_bx = (self._b1x + self._b2x) / 2
        mid_by = (self._b1y + self._b2y) / 2
        mid_ax = (self._a1x + self._a2x) / 2
        mid_ay = (self._a1y + self._a2y) / 2
        self._side_a_toward_zone = self._scalar_side(mid_bx, mid_by, self._a1x, self._a1y, self._a2x, self._a2y)
        self._side_b_toward_zone = self._scalar_side(mid_ax, mid_ay, self._b1x, self._b1y, self._b2x, self._b2y)

        self.track_region: Dict[int, int] = {}  # track_id -> -1 | 0 | 1
        self.track_entered_from: Dict[int, int] = {}  # when in zone, which region we came from
        self.track_last_center: Dict[int, Tuple[float, float]] = {}

        self.total_in = 0
        self.total_out = 0
        self.present_count = 0
        self.new_in = 0
        self.new_out = 0
        self.frame_index = 0

    @staticmethod
    def _scalar_side(px, py, ax, ay, bx, by):
        """Which side of directed line (ax,ay)->(bx,by) does point (px,py) lie on? Returns 1 or -1."""
        cross = (bx - ax) * (py - ay) - (by - ay) * (px - ax)
        return 1 if cross >= 0 else -1

    def _point_side_of_line(self, point: Tuple[float, float], line_a: np.ndarray, line_b: np.ndarray) -> int:
        """Returns which side of the directed line A->B the point lies on. Returns -1 or 1."""
        return self._scalar_side(
            point[0],
            point[1],
            float(line_a[0]),
            float(line_a[1]),
            float(line_b[0]),
            float(line_b[1]),
        )

    def _point_projection_param(
        self,
        point: np.ndarray,
        seg_start: np.ndarray,
        seg_end: np.ndarray,
        clip: bool = False,
    ) -> float:
        """Parameter t for closest point on segment. Kept for external callers."""
        p = np.asarray(point, dtype=np.float64)
        a = np.asarray(seg_start, dtype=np.float64)
        b = np.asarray(seg_end, dtype=np.float64)
        ab = b - a
        ap = p - a
        denom = np.dot(ab, ab)
        if denom < 1e-12:
            return 0.0
        t = np.dot(ap, ab) / denom
        if clip:
            t = np.clip(t, 0.0, 1.0)
        return float(t)

    def _point_within_segment_extent(self, point: Tuple[float, float]) -> bool:
        """True if point projects within [0,1] on both line segments. Kept for external callers."""
        return self._fast_within_extent(point[0], point[1])

    def _fast_within_extent(self, px: float, py: float) -> bool:
        """Pure-scalar extent check using pre-computed values. No numpy allocations."""
        if self._a_len_sq > 1e-12:
            t_a = ((px - self._a1x) * self._a_dx + (py - self._a1y) * self._a_dy) / self._a_len_sq
        else:
            t_a = 0.0
        if not (0 <= t_a <= 1):
            return False
        if self._b_len_sq > 1e-12:
            t_b = ((px - self._b1x) * self._b_dx + (py - self._b1y) * self._b_dy) / self._b_len_sq
        else:
            t_b = 0.0
        return 0 <= t_b <= 1

    def _get_region(self, point: Tuple[float, float]) -> int:
        """
        Return which of the three trap-zone regions the point lies in.
        Returns: -1 (outside Line A), 0 (trap zone), +1 (outside Line B),
        or OUTSIDE_SEGMENT_EXTENT (-2) when outside segment longitudinal extent.
        Uses pre-computed scalars — no numpy allocations per call.
        """
        px, py = point[0], point[1]
        if not self._fast_within_extent(px, py):
            return self.OUTSIDE_SEGMENT_EXTENT
        side_p_a = self._scalar_side(px, py, self._a1x, self._a1y, self._a2x, self._a2y)
        side_p_b = self._scalar_side(px, py, self._b1x, self._b1y, self._b2x, self._b2y)
        if side_p_a == self._side_a_toward_zone and side_p_b == self._side_b_toward_zone:
            return 0
        if side_p_a != self._side_a_toward_zone:
            return -1
        return 1

    def get_center(self, box: np.ndarray) -> Tuple[float, float]:
        """Get center point of bounding box."""
        x1, y1, x2, y2 = box[:4]
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def get_foot_center(self, box: np.ndarray) -> Tuple[float, float]:
        """Get foot (bottom-center) point of bounding box."""
        x1, _y1, x2, y2 = box[:4]
        return ((x1 + x2) / 2, float(y2))

    def get_counting_point(self, box: np.ndarray) -> Tuple[float, float]:
        """Point used for crossing/region logic: foot_center if use_foot_center else bbox center."""
        return self.get_foot_center(box) if self.use_foot_center else self.get_center(box)

    def update(self, boxes: np.ndarray, track_ids: np.ndarray) -> int:
        """
        Update counting: only count when a track completes A -> zone -> B or B -> zone -> A.
        Uses get_counting_point (foot or center per config) for region/crossing logic.
        """
        self.new_in = 0
        self.new_out = 0

        if boxes is None or len(boxes) == 0:
            self.present_count = max(0, self.total_in - self.total_out)
            return self.present_count

        boxes = np.asarray(boxes)
        track_ids = np.asarray(track_ids)
        if boxes.shape[0] == 0:
            self.present_count = max(0, self.total_in - self.total_out)
            return self.present_count

        current_tracks = set()

        for i, (box, track_id) in enumerate(zip(boxes, track_ids)):
            track_id = int(track_id)
            current_tracks.add(track_id)
            point = self.get_counting_point(box)
            region = self._get_region(point)

            prev_region = self.track_region.get(track_id)
            entered_from = self.track_entered_from.get(track_id)

            # Only apply crossing logic when point is within the exact segment extent
            if region == self.OUTSIDE_SEGMENT_EXTENT:
                self.track_region[track_id] = self.OUTSIDE_SEGMENT_EXTENT
                self.track_last_center[track_id] = point
                continue

            if prev_region is not None and prev_region != self.OUTSIDE_SEGMENT_EXTENT:
                if prev_region != 0 and region == 0:
                    self.track_entered_from[track_id] = prev_region
                elif prev_region == 0 and region != 0 and region != self.OUTSIDE_SEGMENT_EXTENT:
                    # Exited zone: (entered_from, region) -> (-1,+1) is A->B, (+1,-1) is B->A
                    if entered_from == -1 and region == 1:
                        if self.in_direction == "A_to_B":
                            self.total_in += 1
                            self.new_in += 1
                        else:
                            self.total_out += 1
                            self.new_out += 1
                    elif entered_from == 1 and region == -1:
                        if self.in_direction == "B_to_A":
                            self.total_in += 1
                            self.new_in += 1
                        else:
                            self.total_out += 1
                            self.new_out += 1
                    if track_id in self.track_entered_from:
                        del self.track_entered_from[track_id]
            # When prev_region was OUTSIDE_SEGMENT_EXTENT and we now have 0, don't set entered_from

            self.track_region[track_id] = region
            self.track_last_center[track_id] = point

        for track_id in list(self.track_region.keys()):
            if track_id not in current_tracks:
                del self.track_region[track_id]
                self.track_entered_from.pop(track_id, None)
                del self.track_last_center[track_id]

        self.present_count = max(0, self.total_in - self.total_out)
        self.frame_index += 1
        return self.present_count

    def is_track_counted(self, track_id: int) -> bool:
        """True if track has crossed the entry line (green side)."""
        region = self.track_region.get(track_id, -2)
        if self.in_direction == "A_to_B":
            return region == 1  # past entry line B
        return region == -1  # past entry line A (B_to_A)

    def is_track_inside(self, track_id: int) -> bool:
        """True if track has entered and not yet exited: green until they cross the exit line."""
        region = self.track_region.get(track_id, -2)
        entered_from = self.track_entered_from.get(track_id)
        if self.in_direction == "A_to_B":
            # Inside = past B (region 1) or in zone after having been past B (exiting toward A)
            return region == 1 or (region == 0 and entered_from == 1)
        # B_to_A: inside = past A (region -1) or in zone after having been past A
        return region == -1 or (region == 0 and entered_from == -1)

    def get_track_bbox_color(self, track_id: int) -> Tuple[int, int, int]:
        """Green = inside (entered, not yet exited). Red = outside or already exited."""
        return (0, 255, 0) if self.is_track_inside(track_id) else (0, 0, 255)


# ============================================================================
# VectorABLineCounter – vector-intersection based two-line counter
# ============================================================================


class VectorABLineCounter:
    def __init__(self, line_a, line_b, in_direction="A_to_B", use_foot_center=True, padding=150):
        self.in_direction = in_direction
        self.use_foot_center = use_foot_center
        self.padding = padding

        # 1. Calculate Corridor Geometry
        a1, a2 = np.array(line_a[0]), np.array(line_a[1])
        b1, b2 = np.array(line_b[0]), np.array(line_b[1])

        self.center_a = (a1 + a2) / 2.0
        self.center_b = (b1 + b2) / 2.0

        # Corridor vector pointing from A to B
        self.corridor_vec = self.center_b - self.center_a
        self.corridor_len = np.linalg.norm(self.corridor_vec)

        if self.corridor_len == 0:
            self.u = np.array([0, 1])
        else:
            self.u = self.corridor_vec / self.corridor_len

        # Lateral vector for boundary checking (perpendicular to corridor)
        self.w = np.array([-self.u[1], self.u[0]])

        # Calculate max lateral width (half of the longest drawn line + padding)
        len_a = np.linalg.norm(a2 - a1)
        len_b = np.linalg.norm(b2 - b1)
        self.max_lateral = (max(len_a, len_b) / 2.0) + self.padding

        # 2. State Memory
        self.track_origins = {}  # Stores the first zone a track was seen in (1, 2, or 3)
        self.last_update = {}  # Timestamp for cleanup

        # Counters
        self.total_in = 0
        self.total_out = 0
        self.present_count = 0
        self.new_in = 0
        self.new_out = 0
        self.current_in_corridor = 0

    def _get_zone(self, point):
        """Projects a 2D point onto the 1D corridor to find its Zone."""
        p_vec = np.array(point) - self.center_a

        # Distance along the corridor (Forward/Backward)
        proj = np.dot(p_vec, self.u)
        # Distance away from the center of the door (Left/Right)
        lat = np.dot(p_vec, self.w)

        # Ignore people walking far outside the padded line edges
        if abs(lat) > self.max_lateral:
            return None

        # Determine Zone based on 1D progression
        if proj < 0:
            return 1  # Zone 1: Before Line A
        elif proj > self.corridor_len:
            return 3  # Zone 3: After Line B
        else:
            return 2  # Zone 2: Between the lines

    def update(self, boxes, track_ids):
        self.new_in = 0
        self.new_out = 0
        current_time = time.time()

        # Cleanup stale tracks (> 10 seconds unseen)
        stale_ids = [tid for tid, ts in self.last_update.items() if current_time - ts > 10.0]
        for tid in stale_ids:
            self.track_origins.pop(tid, None)
            self.last_update.pop(tid, None)

        current_ids = set(track_ids.tolist() if hasattr(track_ids, "tolist") else track_ids)
        self.present_count = len(current_ids)

        in_corridor = 0
        for box, tid in zip(boxes, track_ids):
            tid = int(tid)
            self.last_update[tid] = current_time

            x1, y1, x2, y2 = box
            if self.use_foot_center:
                curr_center = [(x1 + x2) / 2.0, y1 + 0.75 * (y2 - y1)]
            else:
                curr_center = [(x1 + x2) / 2.0, (y1 + y2) / 2.0]

            zone = self._get_zone(curr_center)
            if zone is None:
                continue  # Outside lateral boundaries

            if zone == 2:
                in_corridor += 1

            # If this is a brand new track, record where it spawned
            if tid not in self.track_origins:
                self.track_origins[tid] = zone
                continue

            origin = self.track_origins[tid]

            # 3. The Sequence Logic (Resolves Set 2 Late Spawning)
            if origin == 1 and zone == 3:
                # Perfect full crossing: A -> B
                self._register_count("A_to_B")
                self.track_origins[tid] = 3  # Reset origin to prevent double count

            elif origin == 3 and zone == 1:
                # Perfect full crossing: B -> A
                self._register_count("B_to_A")
                self.track_origins[tid] = 1

            elif origin == 2:
                # Late Spawn: They appeared between the lines!
                if zone == 3:
                    # They finished crossing B -> Count IN
                    self._register_count("A_to_B")
                    self.track_origins[tid] = 3
                elif zone == 1:
                    # They finished crossing A -> Count OUT
                    self._register_count("B_to_A")
                    self.track_origins[tid] = 1

        self.current_in_corridor = in_corridor

    def _register_count(self, direction):
        if direction == "A_to_B":
            if self.in_direction == "A_to_B":
                self.new_in += 1
                self.total_in += 1
            else:
                self.new_out += 1
                self.total_out += 1
        else:  # B_to_A
            if self.in_direction == "A_to_B":
                self.new_out += 1
                self.total_out += 1
            else:
                self.new_in += 1
                self.total_in += 1


class PolygonCounter:
    """Manages double polygon counting logic."""

    def __init__(
        self,
        inner_polygon: List[Tuple[int, int]],
        outer_polygon: List[Tuple[int, int]],
        initial_warmup_frames: int = 5,
        use_foot_center: bool = True,
    ):
        """
        Initialize polygon counter.

        Args:
            inner_polygon: List of (x, y) points defining inner polygon
            outer_polygon: List of (x, y) points defining outer polygon
            initial_warmup_frames: Number of initial frames to count all inside detections (default: 5)
            use_foot_center: if True use bottom-center (foot) of bbox for logic; else use bbox center
        """
        self.inner_polygon = np.array(inner_polygon, dtype=np.int32)
        self.outer_polygon = np.array(outer_polygon, dtype=np.int32)
        self.initial_warmup_frames = initial_warmup_frames
        self.use_foot_center = use_foot_center

        # Track state for each person ID
        self.track_states: Dict[int, str] = {}  # track_id -> "inside", "outside", "buffer"
        self.total_in = 0
        self.total_out = 0
        self.present_count = 0  # actual_inside_count: detections currently inside inner polygon
        self.new_in = 0
        self.new_out = 0
        self.counted_track_ids = set()  # Re-entries (same track_id) do not increment total_in
        self.frame_index = 0  # Number of times update() has been called (for warmup)

    def is_point_in_polygon(self, point: Tuple[float, float], polygon: np.ndarray) -> bool:
        """Check if a point is inside a polygon using ray casting algorithm."""
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def get_center(self, box: np.ndarray) -> Tuple[float, float]:
        """Get center point of bounding box."""
        x1, y1, x2, y2 = box[:4]
        return ((x1 + x2) / 2, (y1 + y2) / 2)

    def get_foot_center(self, box: np.ndarray) -> Tuple[float, float]:
        """Get foot (bottom-center) point of bounding box."""
        x1, _y1, x2, y2 = box[:4]
        return ((x1 + x2) / 2, float(y2))

    def get_counting_point(self, box: np.ndarray) -> Tuple[float, float]:
        """Point used for polygon/zone logic: foot_center if use_foot_center else bbox center."""
        return self.get_foot_center(box) if self.use_foot_center else self.get_center(box)

    def update(self, boxes: np.ndarray, track_ids: np.ndarray) -> int:
        """
        Update counting based on current detections.
        present_count = actual_inside_count (detections inside inner polygon).
        total_in counts unique entrants only; same track_id out then back in does not increment.
        """
        self.new_in = 0
        self.new_out = 0

        if boxes is None or len(boxes) == 0:
            tracks_to_remove = set(self.track_states.keys())
            for track_id in tracks_to_remove:
                del self.track_states[track_id]
            self.present_count = 0
            return self.present_count

        boxes = np.asarray(boxes)
        track_ids = np.asarray(track_ids)
        if boxes.shape[0] == 0:
            tracks_to_remove = set(self.track_states.keys())
            for track_id in tracks_to_remove:
                del self.track_states[track_id]
            self.present_count = 0
            return self.present_count

        current_tracks = set()

        for i, (box, track_id) in enumerate(zip(boxes, track_ids)):
            track_id = int(track_id)
            current_tracks.add(track_id)

            point = self.get_counting_point(box)

            in_inner = self.is_point_in_polygon(point, self.inner_polygon)
            in_outer = self.is_point_in_polygon(point, self.outer_polygon)

            prev_state = self.track_states.get(track_id, None)
            is_first_seen = prev_state is None
            if prev_state is None:
                prev_state = "outside"

            is_warmup = self.frame_index < self.initial_warmup_frames

            if in_inner:
                if prev_state != "inside":
                    if is_warmup:
                        if track_id not in self.counted_track_ids:
                            self.total_in += 1
                            self.new_in += 1
                            self.counted_track_ids.add(track_id)
                    else:
                        if not is_first_seen and prev_state in ("outside", "buffer"):
                            if track_id not in self.counted_track_ids:
                                self.total_in += 1
                                self.new_in += 1
                                self.counted_track_ids.add(track_id)
                new_state = "inside"
            elif not in_outer:
                if prev_state == "inside":
                    self.total_out += 1
                    self.new_out += 1
                new_state = "outside"
            else:
                new_state = prev_state

            self.track_states[track_id] = new_state

        tracks_to_remove = set(self.track_states.keys()) - current_tracks
        for track_id in tracks_to_remove:
            del self.track_states[track_id]

        self.present_count = sum(1 for state in self.track_states.values() if state == "inside")
        self.frame_index += 1
        return self.present_count

    def is_track_counted(self, track_id: int) -> bool:
        """
        Check if a track ID is currently counted (has "inside" state).

        Args:
            track_id: Track ID to check

        Returns:
            True if track is counted, False otherwise
        """
        return self.track_states.get(track_id, "outside") == "inside"
