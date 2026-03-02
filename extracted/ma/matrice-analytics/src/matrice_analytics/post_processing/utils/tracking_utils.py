"""
Tracking utilities for post-processing operations.
"""

from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict

from .geometry_utils import point_in_polygon, get_bbox_center, line_segments_intersect


def track_objects_in_zone(results: Any, zone_polygon: List[List[float]]) -> Dict[str, Any]:
    """
    Track objects within a defined zone.
    
    Args:
        results: Detection or tracking results
        zone_polygon: Zone polygon coordinates [[x1,y1], [x2,y2], ...]
        
    Returns:
        Dict with zone tracking information
    """
    zone_tracks = []
    zone_polygon_tuples = [(p[0], p[1]) for p in zone_polygon]
    
    if isinstance(results, list):
        # Detection format
        for detection in results:
            if _is_detection_in_zone(detection, zone_polygon_tuples):
                bbox = detection.get("bounding_box", detection.get("bbox", {}))
                center = get_bbox_center(bbox)
                
                zone_tracks.append({
                    **detection,
                    "in_zone": True,
                    "zone_center": center
                })
    
    elif isinstance(results, dict):
        # Frame-based format
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                for detection in detections:
                    if _is_detection_in_zone(detection, zone_polygon_tuples):
                        bbox = detection.get("bounding_box", detection.get("bbox", {}))
                        center = get_bbox_center(bbox)
                        
                        zone_tracks.append({
                            **detection,
                            "frame_id": frame_id,
                            "in_zone": True,
                            "zone_center": center
                        })
    
    return {
        "zone_tracks": zone_tracks,
        "count_in_zone": len(zone_tracks)
    }


def detect_line_crossings(results: Dict[str, List[Dict]], line_points: List[List[float]], 
                         track_history: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Detect when tracked objects cross a virtual line.
    
    Args:
        results: Tracking results in frame format
        line_points: Line coordinates [[x1,y1], [x2,y2]]
        track_history: Optional track position history
        
    Returns:
        Dict with crossing information
    """
    if len(line_points) != 2:
        return {"crossings": [], "total_crossings": 0}
    
    line_start = tuple(line_points[0])
    line_end = tuple(line_points[1])
    crossings = []
    
    if track_history is None:
        track_history = {}
    
    for frame_id, detections in results.items():
        if isinstance(detections, list):
            for detection in detections:
                track_id = detection.get("track_id")
                if track_id is None:
                    continue
                
                bbox = detection.get("bounding_box", detection.get("bbox"))
                if not bbox:
                    continue
                
                center = get_bbox_center(bbox)
                
                # Check for line crossing
                if track_id in track_history:
                    prev_pos = track_history[track_id][-1] if track_history[track_id] else None
                    
                    if prev_pos and line_segments_intersect(prev_pos, center, line_start, line_end):
                        crossings.append({
                            "track_id": track_id,
                            "frame_id": frame_id,
                            "position": center,
                            "category": detection.get("category", "unknown"),
                            "previous_position": prev_pos
                        })
                
                # Update track history
                if track_id not in track_history:
                    track_history[track_id] = []
                
                track_history[track_id].append(center)
                
                # Keep only recent positions (last 10)
                if len(track_history[track_id]) > 10:
                    track_history[track_id] = track_history[track_id][-10:]
    
    return {
        "crossings": crossings,
        "total_crossings": len(crossings),
        "track_history": track_history
    }


def analyze_track_movements(results: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Analyze movement patterns of tracked objects.
    
    Args:
        results: Tracking results in frame format
        
    Returns:
        Dict with movement analysis
    """
    track_paths = defaultdict(list)
    track_stats = {}
    
    # Collect track positions
    for frame_id, detections in results.items():
        if isinstance(detections, list):
            for detection in detections:
                track_id = detection.get("track_id")
                if track_id is None:
                    continue
                
                bbox = detection.get("bounding_box", detection.get("bbox"))
                if bbox:
                    center = get_bbox_center(bbox)
                    track_paths[track_id].append({
                        "frame_id": frame_id,
                        "position": center,
                        "category": detection.get("category", "unknown")
                    })
    
    # Analyze each track
    for track_id, positions in track_paths.items():
        if len(positions) < 2:
            continue
        
        # Calculate total distance traveled
        total_distance = 0
        for i in range(1, len(positions)):
            prev_pos = positions[i-1]["position"]
            curr_pos = positions[i]["position"]
            distance = ((curr_pos[0] - prev_pos[0])**2 + (curr_pos[1] - prev_pos[1])**2)**0.5
            total_distance += distance
        
        # Calculate average speed (distance per frame)
        avg_speed = total_distance / (len(positions) - 1) if len(positions) > 1 else 0
        
        track_stats[track_id] = {
            "total_frames": len(positions),
            "total_distance": total_distance,
            "average_speed": avg_speed,
            "start_position": positions[0]["position"],
            "end_position": positions[-1]["position"],
            "category": positions[0]["category"]
        }
    
    return {
        "track_paths": dict(track_paths),
        "track_statistics": track_stats,
        "total_tracks": len(track_paths)
    }


def filter_tracks_by_duration(results: Dict[str, List[Dict]], min_duration: int = 5) -> Dict[str, List[Dict]]:
    """
    Filter tracking results to only include tracks that appear for minimum duration.
    
    Args:
        results: Tracking results in frame format
        min_duration: Minimum number of frames a track must appear
        
    Returns:
        Filtered tracking results
    """
    track_counts = defaultdict(int)
    
    # Count appearances per track
    for frame_id, detections in results.items():
        if isinstance(detections, list):
            for detection in detections:
                track_id = detection.get("track_id")
                if track_id is not None:
                    track_counts[track_id] += 1
    
    # Filter tracks that meet minimum duration
    valid_tracks = {track_id for track_id, count in track_counts.items() if count >= min_duration}
    
    # Filter results
    filtered_results = {}
    for frame_id, detections in results.items():
        filtered_detections = []
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None or track_id in valid_tracks:
                filtered_detections.append(detection)
        
        if filtered_detections:
            filtered_results[frame_id] = filtered_detections
    
    return filtered_results


def _is_detection_in_zone(detection: Dict[str, Any], zone_polygon: List[Tuple[float, float]]) -> bool:
    """Check if a detection is within a zone polygon."""
    bbox = detection.get("bounding_box", detection.get("bbox"))
    if not bbox:
        return False
    
    center = get_bbox_center(bbox)
    return point_in_polygon(center, zone_polygon) 