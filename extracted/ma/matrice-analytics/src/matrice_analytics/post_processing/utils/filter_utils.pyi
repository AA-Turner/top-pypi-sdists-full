"""Auto-generated stub for module: filter_utils."""
from typing import Any, Dict, List

from .geometry_utils import calculate_iou
from .geometry_utils import get_bbox_area

# Functions
def apply_category_mapping(results: Any, index_to_category: Dict[str, str]) -> Any:
    """
    Apply category index to name mapping.
    
    Args:
        results: Detection or tracking results
        index_to_category: Mapping from category index to category name
    
    Returns:
        Results with mapped category names
    """
    ...
def calculate_bbox_fingerprint(bbox: Dict[str, Any], category: str = '') -> str:
    """
    Calculate a fingerprint for a bounding box to detect duplicates.
    
    Args:
        bbox: Bounding box dictionary
        category: Object category
    
    Returns:
        str: Unique fingerprint for the bbox
    """
    ...
def clean_expired_tracks(track_timestamps: Dict[str, float], track_last_seen: Dict[str, float], current_timestamp: float, expiry_time: float) -> None:
    """
    Clean expired tracks from tracking dictionaries.
    
    Args:
        track_timestamps: Dictionary of track_id -> first_seen_timestamp
        track_last_seen: Dictionary of track_id -> last_seen_timestamp
        current_timestamp: Current timestamp
        expiry_time: Time after which tracks expire
    """
    ...
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
    ...
def filter_by_categories(results: Any, allowed_categories: List[str]) -> Any:
    """
    Filter results to only include specified categories.
    
    Args:
        results: Detection or tracking results
        allowed_categories: List of allowed category names
    
    Returns:
        Filtered results in the same format
    """
    ...
def filter_by_confidence(results: Any, threshold: float = 0.5) -> Any:
    """
    Filter results by confidence threshold.
    
    Args:
        results: Detection or tracking results
        threshold: Minimum confidence threshold
    
    Returns:
        Filtered results in the same format
    """
    ...
def remove_duplicate_detections(results: List[Dict[str, Any]], similarity_threshold: float = 0.8) -> List[Dict[str, Any]]:
    """
    Remove duplicate detections based on bbox similarity.
    
    Args:
        results: List of detection dictionaries
        similarity_threshold: IoU threshold for considering detections as duplicates
    
    Returns:
        List of unique detections
    """
    ...
