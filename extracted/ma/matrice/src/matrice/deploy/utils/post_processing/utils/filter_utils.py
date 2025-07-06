"""
Filter utilities for post-processing operations.
"""

import time
from typing import List, Dict, Any, Set
from collections import defaultdict


def filter_by_confidence(results: Any, threshold: float = 0.5) -> Any:
    """
    Filter results by confidence threshold.
    
    Args:
        results: Detection or tracking results
        threshold: Minimum confidence threshold
        
    Returns:
        Filtered results in the same format
    """
    if isinstance(results, list):
        # Detection format
        return [r for r in results if r.get("confidence", 0) >= threshold]
    
    elif isinstance(results, dict):
        # Check if it's a simple classification result
        if "confidence" in results and "category" in results:
            return results if results.get("confidence", 0) >= threshold else {}
        
        # Frame-based format (tracking or activity recognition)
        filtered_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                filtered_detections = [
                    d for d in detections if d.get("confidence", 0) >= threshold
                ]
                if filtered_detections:
                    filtered_results[frame_id] = filtered_detections
        
        return filtered_results
    
    return results


def filter_by_categories(results: Any, allowed_categories: List[str]) -> Any:
    """
    Filter results to only include specified categories.
    
    Args:
        results: Detection or tracking results
        allowed_categories: List of allowed category names
        
    Returns:
        Filtered results in the same format
    """
    if isinstance(results, list):
        # Detection format
        return [r for r in results if r.get("category", "") in allowed_categories]
    
    elif isinstance(results, dict):
        # Check if it's a simple classification result
        if "category" in results:
            return results if results.get("category", "") in allowed_categories else {}
        
        # Frame-based format
        filtered_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                filtered_detections = [
                    d for d in detections if d.get("category", "") in allowed_categories
                ]
                if filtered_detections:
                    filtered_results[frame_id] = filtered_detections
        
        return filtered_results
    
    return results


def calculate_bbox_fingerprint(bbox: Dict[str, Any], category: str = "") -> str:
    """
    Calculate a fingerprint for a bounding box to detect duplicates.
    
    Args:
        bbox: Bounding box dictionary
        category: Object category
        
    Returns:
        str: Unique fingerprint for the bbox
    """
    # Extract coordinates
    if "xmin" in bbox:
        coords = (bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"])
    elif "x1" in bbox:
        coords = (bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"])
    else:
        values = list(bbox.values())
        coords = tuple(values[:4]) if len(values) >= 4 else (0, 0, 0, 0)
    
    # Round coordinates to reduce floating point precision issues
    rounded_coords = tuple(round(c, 2) for c in coords)
    
    return f"{category}_{rounded_coords}"


def clean_expired_tracks(track_timestamps: Dict[str, float], 
                        track_last_seen: Dict[str, float],
                        current_timestamp: float, 
                        expiry_time: float) -> None:
    """
    Clean expired tracks from tracking dictionaries.
    
    Args:
        track_timestamps: Dictionary of track_id -> first_seen_timestamp
        track_last_seen: Dictionary of track_id -> last_seen_timestamp
        current_timestamp: Current timestamp
        expiry_time: Time after which tracks expire
    """
    expired_tracks = []
    
    for track_id, last_seen in track_last_seen.items():
        if current_timestamp - last_seen > expiry_time:
            expired_tracks.append(track_id)
    
    for track_id in expired_tracks:
        track_timestamps.pop(track_id, None)
        track_last_seen.pop(track_id, None)


def remove_duplicate_detections(results: List[Dict[str, Any]], 
                               similarity_threshold: float = 0.8) -> List[Dict[str, Any]]:
    """
    Remove duplicate detections based on bbox similarity.
    
    Args:
        results: List of detection dictionaries
        similarity_threshold: IoU threshold for considering detections as duplicates
        
    Returns:
        List of unique detections
    """
    from .geometry_utils import calculate_iou

    if not results:
        return results

    unique_detections = []

    for detection in results:
        is_duplicate = False

        for existing in unique_detections:
            # Check if same category
            if detection.get("category") == existing.get("category"):
                # Calculate IoU between bounding boxes
                bbox1 = detection.get("bounding_box", detection.get("bbox", {}))
                bbox2 = existing.get("bounding_box", existing.get("bbox", {}))

                if bbox1 and bbox2:
                    iou = calculate_iou(bbox1, bbox2)
                    if iou >= similarity_threshold:
                        is_duplicate = True
                        # Keep the one with higher confidence
                        if detection.get("confidence", 0) > existing.get("confidence", 0):
                            unique_detections.remove(existing)
                            unique_detections.append(detection)
                        break

        if not is_duplicate:
            unique_detections.append(detection)

    return unique_detections


def apply_category_mapping(results: Any, index_to_category: Dict[str, str]) -> Any:
    """
    Apply category index to name mapping.

    Args:
        results: Detection or tracking results
        index_to_category: Mapping from category index to category name

    Returns:
        Results with mapped category names
    """

    def map_detection(
        detection: Dict[str, Any], index_to_category: Dict[str, str]
    ) -> Dict[str, Any]:
        """Map a single detection."""
        detection = detection.copy()
        category_id = str(detection.get("category", detection.get("category_id")))
        index_to_category = {str(k): str(v) for k, v in index_to_category.items()}
        if category_id in index_to_category:
            detection["category"] = index_to_category[category_id]
            detection["category_id"] = category_id
        return detection

    if isinstance(results, list):
        # Detection format
        return [map_detection(r, index_to_category) for r in results]

    elif isinstance(results, dict):
        # Check if it's a simple classification result
        if "category" in results or "category_id" in results:
            return map_detection(results, index_to_category)

        # Frame-based format
        mapped_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                mapped_results[frame_id] = [
                    map_detection(d, index_to_category) for d in detections
                ]
            else:
                mapped_results[frame_id] = detections

        return mapped_results

    return results


def filter_by_area(results: Any, min_area: float = 0, max_area: float = float('inf')) -> Any:
    """
    Filter detections by bounding box area.
    
    Args:
        results: Detection or tracking results
        min_area: Minimum bounding box area
        max_area: Maximum bounding box area
        
    Returns:
        Filtered results
    """
    from .geometry_utils import get_bbox_area
    
    def is_valid_area(detection: Dict[str, Any]) -> bool:
        """Check if detection has valid area."""
        bbox = detection.get("bounding_box", detection.get("bbox"))
        if not bbox:
            return True  # Keep detections without bbox
        
        area = get_bbox_area(bbox)
        return min_area <= area <= max_area
    
    if isinstance(results, list):
        # Detection format
        return [r for r in results if is_valid_area(r)]
    
    elif isinstance(results, dict):
        # Frame-based format
        filtered_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                filtered_detections = [d for d in detections if is_valid_area(d)]
                if filtered_detections:
                    filtered_results[frame_id] = filtered_detections
        
        return filtered_results
    
    return results 
