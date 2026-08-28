"""Auto-generated stub for module: counting_utils."""
from typing import Any, Dict, List, Optional, Tuple

from .geometry_utils import get_bbox_bottom_center, point_in_polygon, to_zone_test_point

# Functions
def calculate_counting_summary(results: Any, zones: Optional[Dict[str, List[List[float]]]] = None) -> Dict[str, Any]:
    """
    Calculate comprehensive counting summary.
    
    Args:
        results: Detection/tracking results
        zones: Optional zone definitions
    
    Returns:
        Dict[str, Any]: Comprehensive counting summary
    """
    ...
def count_objects_by_category(results: Any) -> Dict[str, int]:
    """
    Count objects by category from detection results.
    
    Args:
        results: Detection results (list or dict format)
    
    Returns:
        Dict[str, int]: Category counts
    """
    ...
def count_objects_in_zones(results: Any, zones: Dict[str, List[List[float]]], stream_info: Optional[Any] = None) -> Dict[str, Dict[str, int]]:
    """
    Count objects in defined zones.
    
    Args:
        results: Detection results
        zones: Dictionary of zone_name -> polygon coordinates
    
    Returns:
        Dict[str, Dict[str, int]]: Zone counts by category
    """
    ...
def count_unique_tracks(results: Dict[str, List[Dict]]) -> Dict[str, int]:
    """
    Count unique tracks by category from tracking results.
    
    Args:
        results: Tracking results in frame format
    
    Returns:
        Dict[str, int]: Unique track counts by category
    """
    ...
def parse_line_config(line_config: Any) -> Any.Any:
    """
    Parse a line definition into a (2, 2) numpy array.
    
    Accepts either:
      - [x1, y1, x2, y2]        (flat list)
      - [[x1, y1], [x2, y2]]    (nested list)
    
    Returns:
        np.ndarray: shape (2, 2) with dtype float64
    """
    ...
def polygon_offset_inward(polygon: Any.Any, offset: float) -> Any.Any:
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
    ...

# Classes
class ABLineCounter:
    # Manages trap zone [two AB lines] counting: count only on full crossing A -> zone -> B or B -> zone -> A.

    def __init__(self: Any, line_a: Any.Any, line_b: Any.Any, in_direction: str = 'A_to_B', use_foot_center: bool = False) -> None:
        """
        Initialize trap zone counter.
        
        Args:
            line_a: (2, 2) array — rows are segment start and end for Line A
            line_b: (2, 2) array — rows are segment start and end for Line B
            in_direction: "A_to_B" (crossing A then B = In) or "B_to_A" (crossing B then A = In)
            use_foot_center: if True use bottom-center (foot) of bbox for logic; else use bbox center
        """
        ...

    OUTSIDE_SEGMENT_EXTENT: Any

    def get_center(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Get center point of bounding box.
        """
        ...

    def get_counting_point(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Point used for crossing/region logic: foot_center if use_foot_center else bbox center.
        """
        ...

    def get_foot_center(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Get foot (bottom-center) point of bounding box.
        """
        ...

    def get_track_bbox_color(self: Any, track_id: int) -> Tuple[int, int, int]:
        """
        Green = inside (entered, not yet exited). Red = outside or already exited.
        """
        ...

    def is_track_counted(self: Any, track_id: int) -> bool:
        """
        True if track has crossed the entry line (green side).
        """
        ...

    def is_track_inside(self: Any, track_id: int) -> bool:
        """
        True if track has entered and not yet exited: green until they cross the exit line.
        """
        ...

    def update(self: Any, boxes: Any.Any, track_ids: Any.Any) -> int:
        """
        Update counting: only count when a track completes A -> zone -> B or B -> zone -> A.
        Uses get_counting_point (foot or center per config) for region/crossing logic.
        """
        ...

class PolygonCounter:
    # Manages double polygon counting logic.

    def __init__(self: Any, inner_polygon: List[Tuple[int, int]], outer_polygon: List[Tuple[int, int]], initial_warmup_frames: int = 5, use_foot_center: bool = True) -> None:
        """
        Initialize polygon counter.
        
        Args:
            inner_polygon: List of (x, y) points defining inner polygon
            outer_polygon: List of (x, y) points defining outer polygon
            initial_warmup_frames: Number of initial frames to count all inside detections (default: 5)
            use_foot_center: if True use bottom-center (foot) of bbox for logic; else use bbox center
        """
        ...

    def get_center(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Get center point of bounding box.
        """
        ...

    def get_counting_point(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Point used for polygon/zone logic: foot_center if use_foot_center else bbox center.
        """
        ...

    def get_foot_center(self: Any, box: Any.Any) -> Tuple[float, float]:
        """
        Get foot (bottom-center) point of bounding box.
        """
        ...

    def is_point_in_polygon(self: Any, point: Tuple[float, float], polygon: Any.Any) -> bool:
        """
        Check if a point is inside a polygon using ray casting algorithm.
        """
        ...

    def is_track_counted(self: Any, track_id: int) -> bool:
        """
        Check if a track ID is currently counted (has "inside" state).
        
        Args:
            track_id: Track ID to check
        
        Returns:
            True if track is counted, False otherwise
        """
        ...

    def update(self: Any, boxes: Any.Any, track_ids: Any.Any) -> int:
        """
        Update counting based on current detections.
        present_count = actual_inside_count (detections inside inner polygon).
        total_in counts unique entrants only; same track_id out then back in does not increment.
        """
        ...

class VectorABLineCounter:
    def __init__(self: Any, line_a: Any, line_b: Any, in_direction: Any = 'A_to_B', use_foot_center: Any = True, padding: Any = 150) -> None: ...

    def update(self: Any, boxes: Any, track_ids: Any) -> Any: ...

