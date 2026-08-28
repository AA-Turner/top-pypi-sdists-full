"""Auto-generated stub for module: tracking_utils."""
from typing import Any, Dict, List, Optional

from .geometry_utils import get_bbox_center, line_segments_intersect, point_in_polygon

# Functions
def analyze_track_movements(results: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Analyze movement patterns of tracked objects.
    
    Args:
        results: Tracking results in frame format
    
    Returns:
        Dict with movement analysis
    """
    ...
def detect_line_crossings(results: Dict[str, List[Dict]], line_points: List[List[float]], track_history: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Detect when tracked objects cross a virtual line.
    
    Args:
        results: Tracking results in frame format
        line_points: Line coordinates [[x1,y1], [x2,y2]]
        track_history: Optional track position history
    
    Returns:
        Dict with crossing information
    """
    ...
def filter_tracks_by_duration(results: Dict[str, List[Dict]], min_duration: int = 5) -> Dict[str, List[Dict]]:
    """
    Filter tracking results to only include tracks that appear for minimum duration.
    
    Args:
        results: Tracking results in frame format
        min_duration: Minimum number of frames a track must appear
    
    Returns:
        Filtered tracking results
    """
    ...
def track_objects_in_zone(results: Any, zone_polygon: List[List[float]]) -> Dict[str, Any]:
    """
    Track objects within a defined zone.
    
    Args:
        results: Detection or tracking results
        zone_polygon: Zone polygon coordinates [[x1,y1], [x2,y2], ...]
    
    Returns:
        Dict with zone tracking information
    """
    ...
