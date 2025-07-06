"""
Counting utilities for post-processing operations.
"""

import time
from typing import List, Dict, Any, Tuple, Optional, Set
from collections import defaultdict

from .geometry_utils import point_in_polygon, get_bbox_center, get_bbox_bottom25_center
from .filter_utils import calculate_bbox_fingerprint


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


def count_objects_in_zones(results: Any, zones: Dict[str, List[List[float]]]) -> Dict[str, Dict[str, int]]:
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
                if _is_detection_in_zone(detection, zone_polygon):
                    category = detection.get("category", "unknown")
                    zone_counts[zone_name][category] += 1
        
        elif isinstance(results, dict):
            # Frame-based format
            seen_tracks = set()
            
            for frame_id, detections in results.items():
                if isinstance(detections, list):
                    for detection in detections:
                        if _is_detection_in_zone(detection, zone_polygon):
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
    summary = {
        "total_objects": 0,
        "by_category": {},
        "timestamp": time.time()
    }
    
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


def _is_detection_in_zone(detection: Dict[str, Any], zone_polygon: List[List[float]]) -> bool:
    """Check if a detection is within a zone polygon."""
    bbox = detection.get("bounding_box", detection.get("bbox"))
    if not bbox:
        return False
    
    #center = get_bbox_center(bbox)
    bottom25_center = get_bbox_bottom25_center(bbox)
    return point_in_polygon(bottom25_center, [(p[0], p[1]) for p in zone_polygon]) 