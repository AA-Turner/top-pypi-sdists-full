"""
Advanced counting utilities with time-based tracking and deduplication for post-processing.
"""

import time
from typing import List, Dict, Any, Tuple, Optional, Set
from collections import defaultdict
from .format_utils import match_results_structure
from .geometry_utils import point_in_polygon, get_bbox_center


def calculate_bbox_overlap(bbox1: Dict, bbox2: Dict) -> float:
    """Calculate overlap between two bounding boxes."""
    # Convert to consistent format
    if 'xmin' in bbox1:
        x1_min, y1_min, x1_max, y1_max = bbox1['xmin'], bbox1['ymin'], bbox1['xmax'], bbox1['ymax']
    else:
        x1_min, y1_min, x1_max, y1_max = bbox1.get('x1', 0), bbox1.get('y1', 0), bbox1.get('x2', 0), bbox1.get('y2', 0)
    
    if 'xmin' in bbox2:
        x2_min, y2_min, x2_max, y2_max = bbox2['xmin'], bbox2['ymin'], bbox2['xmax'], bbox2['ymax']
    else:
        x2_min, y2_min, x2_max, y2_max = bbox2.get('x1', 0), bbox2.get('y1', 0), bbox2.get('x2', 0), bbox2.get('y2', 0)
    
    # Calculate intersection
    x_left = max(x1_min, x2_min)
    y_top = max(y1_min, y2_min)
    x_right = min(x1_max, x2_max)
    y_bottom = min(y1_max, y2_max)
    
    if x_right < x_left or y_bottom < y_top:
        return 0.0
    
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    
    # Calculate union
    bbox1_area = (x1_max - x1_min) * (y1_max - y1_min)
    bbox2_area = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = bbox1_area + bbox2_area - intersection_area
    
    if union_area == 0:
        return 0.0
    
    return intersection_area / union_area


def calculate_bbox_fingerprint(bbox: Dict, category: str = "") -> str:
    """Calculate a fingerprint for bbox deduplication."""
    if not bbox:
        return f"{category}_empty"
    
    # Normalize bbox coordinates
    if 'xmin' in bbox:
        x1, y1, x2, y2 = bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']
    else:
        x1, y1, x2, y2 = bbox.get('x1', 0), bbox.get('y1', 0), bbox.get('x2', 0), bbox.get('y2', 0)
    
    # Round to reduce minor variations
    x1, y1, x2, y2 = round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1)
    
    return f"{category}_{x1}_{y1}_{x2}_{y2}"


def clean_expired_tracks(track_timestamps: Dict, track_last_seen: Dict, 
                        current_timestamp: float, expiry_seconds: int):
    """Clean expired tracks from tracking dictionaries."""
    expired_tracks = []
    
    for track_id, last_seen in track_last_seen.items():
        if current_timestamp - last_seen > expiry_seconds:
            expired_tracks.append(track_id)
    
    for track_id in expired_tracks:
        track_timestamps.pop(track_id, None)
        track_last_seen.pop(track_id, None)


class CountingLibrary:
    """Library class for handling object counting operations with time-based tracking."""
    
    def __init__(self, 
                 time_window_seconds: int = 3600,
                 track_expiry_seconds: int = 300,
                 enable_time_based_counting: bool = True,
                 enable_bbox_deduplication: bool = True,
                 bbox_similarity_threshold: float = 0.8):
        """Initialize counting library with configuration."""
        self.zone_counters = defaultdict(int)
        self.dwell_times = defaultdict(dict)
        
        # Time-based tracking for incremental counting
        self.unique_tracks_seen = set()  # All unique track IDs ever seen
        self.track_timestamps = {}  # track_id -> first_seen_timestamp
        self.track_last_seen = {}  # track_id -> last_seen_timestamp
        self.zone_unique_tracks = defaultdict(set)  # zone_name -> set of unique track IDs
        self.zone_track_timestamps = defaultdict(dict)  # zone_name -> {track_id: first_seen}
        
        # Bounding box-based deduplication
        self.bbox_fingerprints = {}  # track_id -> bbox_fingerprint for deduplication
        self.seen_bbox_fingerprints = set()  # Set of all bbox fingerprints seen
        self.category_bbox_fingerprints = defaultdict(set)  # category -> set of bbox fingerprints
        
        # Configuration
        self.time_window = time_window_seconds
        self.track_expiry_time = track_expiry_seconds
        self.enable_time_based_counting = enable_time_based_counting
        self.bbox_similarity_threshold = bbox_similarity_threshold
        self.enable_bbox_deduplication = enable_bbox_deduplication
    
    def set_time_window(self, time_window_seconds: int):
        """Set the time window for statistics collection."""
        self.time_window = time_window_seconds
    
    def count_objects(self, results: Any, identification_keys: List[str] = None, 
                     current_timestamp: Optional[float] = None) -> Tuple[Any, Dict]:
        """Count objects with metadata, supporting incremental time-based counting."""
        # Use default identification keys if not provided
        if identification_keys is None:
            identification_keys = ["track_id"]
        
        if current_timestamp is None:
            current_timestamp = time.time()
        
        # Clean expired tracks if time-based counting is enabled
        if self.enable_time_based_counting:
            clean_expired_tracks(self.track_timestamps, self.track_last_seen, 
                               current_timestamp, self.track_expiry_time)
        
        metadata = {"total": 0, "by_category": defaultdict(int)}
        results_type = match_results_structure(results)
        
        if results_type == "detection":
            metadata["total"] = len(results)
            for result in results:
                category = result.get("category", "unknown")
                metadata["by_category"][category] += 1
        
        elif results_type == "classification":
            metadata["total"] = len(results)
        
        elif results_type == "object_tracking":
            current_unique_tracks = set()
            new_tracks_this_frame = set()
            unique_detections_per_category = defaultdict(set)  # For proper category counting
            
            # Keep track of processed detections to avoid duplicates
            processed_detections = []
            
            for frame_id, detections in results.items():
                if isinstance(detections, list):
                    for detection in detections:
                        # Skip if this detection is a duplicate of an already processed detection
                        if self.enable_bbox_deduplication and self._is_duplicate_detection(detection, processed_detections):
                            continue
                        
                        # Add to processed detections to check future duplicates
                        processed_detections.append(detection)
                            
                        for key in identification_keys:
                            if key in detection:
                                track_id = detection[key]
                                current_unique_tracks.add(track_id)
                                
                                # Track time-based information
                                if self.enable_time_based_counting:
                                    if track_id not in self.unique_tracks_seen:
                                        self.unique_tracks_seen.add(track_id)
                                        self.track_timestamps[track_id] = current_timestamp
                                        new_tracks_this_frame.add(track_id)
                                    
                                    # Update last seen time
                                    self.track_last_seen[track_id] = current_timestamp
                                
                                category = detection.get("category", "unknown")
                                
                                # Use bounding box fingerprint for unique category counting
                                if ("bounding_box" in detection or "bbox" in detection) and self.enable_bbox_deduplication:
                                    bbox = detection.get("bounding_box", detection.get("bbox", {}))
                                    bbox_fingerprint = calculate_bbox_fingerprint(bbox, category)
                                    unique_detections_per_category[category].add(bbox_fingerprint)
                                else:
                                    # Fallback to track_id based counting
                                    unique_detections_per_category[category].add(track_id)
                                
                                break  # Only use first matching identification key
            
            # Update category counts based on unique detections
            for category, unique_fingerprints in unique_detections_per_category.items():
                metadata["by_category"][category] = len(unique_fingerprints)
            
            # Set counts based on counting mode
            if self.enable_time_based_counting:
                metadata["total"] = len(self.unique_tracks_seen)
                metadata["current_frame_unique"] = len(current_unique_tracks)
                metadata["new_tracks_this_frame"] = len(new_tracks_this_frame)
                metadata["total_tracks_in_time_window"] = len(self._get_tracks_in_time_window(current_timestamp))
            else:
                metadata["total"] = len(current_unique_tracks)
        
        # Convert defaultdict to regular dict for JSON serialization
        metadata["by_category"] = dict(metadata["by_category"])
        
        # Add time-based metadata
        if self.enable_time_based_counting:
            metadata["time_based_counting"] = {
                "enabled": True,
                "time_window_seconds": self.time_window,
                "track_expiry_seconds": self.track_expiry_time,
                "current_timestamp": current_timestamp,
                "active_tracks": len([t for t in self.track_last_seen.values() 
                                    if current_timestamp - t <= self.track_expiry_time])
            }
        
        return results, metadata
    
    def count_in_zones(self, results: Dict, zones: Dict[str, List[Tuple[float, float]]] = None, 
                      current_timestamp: Optional[float] = None) -> Dict:
        """Count objects in defined zones with configurable rules and time-based tracking."""
        if zones is None:
            zones = {}
        
        if current_timestamp is None:
            current_timestamp = time.time()
        
        # Clean expired tracks for each zone
        if self.enable_time_based_counting:
            for zone_name in zones.keys():
                self._clean_expired_zone_tracks(zone_name, current_timestamp)
        
        zone_counts = {}
        
        for zone_name, zone_polygon in zones.items():
            if zone_name not in self.zone_counters:
                self.zone_counters[zone_name] = 0
            
            current_count = 0
            current_frame_tracks = set()
            new_zone_tracks = set()
            
            if isinstance(results, dict):
                for frame_id, detections in results.items():
                    if isinstance(detections, list):
                        for detection in detections:
                            if "bounding_box" in detection or "bbox" in detection:
                                bbox = detection.get("bounding_box", detection.get("bbox", {}))
                                center = get_bbox_center(bbox)
                                
                                if point_in_polygon(center, zone_polygon):
                                    # Get track ID for uniqueness
                                    track_id = None
                                    for key in ["track_id"]:  # Default identification key
                                        if key in detection:
                                            track_id = detection[key]
                                            break
                                    
                                    if track_id is not None:
                                        current_frame_tracks.add(track_id)
                                        
                                        # Time-based zone tracking
                                        if self.enable_time_based_counting:
                                            if track_id not in self.zone_unique_tracks[zone_name]:
                                                self.zone_unique_tracks[zone_name].add(track_id)
                                                self.zone_track_timestamps[zone_name][track_id] = current_timestamp
                                                new_zone_tracks.add(track_id)
                                        
                                        current_count += 1
            
            # Set zone counts based on counting mode
            if self.enable_time_based_counting:
                zone_tracks_in_window = self._get_zone_tracks_in_time_window(zone_name, current_timestamp)
                zone_counts[zone_name] = {
                    "current_frame": len(current_frame_tracks),
                    "new_this_frame": len(new_zone_tracks),
                    "total_unique": len(self.zone_unique_tracks[zone_name]),
                    "in_time_window": len(zone_tracks_in_window),
                    "time_window_seconds": self.time_window
                }
            else:
                zone_counts[zone_name] = {
                    "current_frame": len(current_frame_tracks),
                    "total": len(current_frame_tracks)
                }
        
        return zone_counts
    
    def get_unique_count_by_keys(self, results: Any, keys: List[str] = None) -> Dict[str, int]:
        """Get unique count based on specified keys."""
        if keys is None:
            keys = ["track_id"]
        
        unique_values = set()
        results_type = match_results_structure(results)
        
        if results_type == "object_tracking":
            for frame_id, detections in results.items():
                if isinstance(detections, list):
                    for detection in detections:
                        for key in keys:
                            if key in detection:
                                unique_values.add(detection[key])
                                break
        
        return {"unique_count": len(unique_values), "keys_used": keys}
    
    def get_counting_statistics(self, current_timestamp: Optional[float] = None) -> Dict[str, Any]:
        """Get comprehensive counting statistics."""
        if current_timestamp is None:
            current_timestamp = time.time()
        
        stats = {
            "total_unique_tracks": len(self.unique_tracks_seen),
            "active_tracks": len([t for t in self.track_last_seen.values() 
                                if current_timestamp - t <= self.track_expiry_time]),
            "tracks_in_time_window": len(self._get_tracks_in_time_window(current_timestamp)),
            "zone_statistics": {},
            "configuration": {
                "time_window_seconds": self.time_window,
                "track_expiry_seconds": self.track_expiry_time,
                "time_based_counting_enabled": self.enable_time_based_counting,
                "bbox_deduplication_enabled": self.enable_bbox_deduplication,
                "bbox_similarity_threshold": self.bbox_similarity_threshold
            }
        }
        
        # Add zone statistics
        for zone_name in self.zone_unique_tracks.keys():
            zone_tracks_in_window = self._get_zone_tracks_in_time_window(zone_name, current_timestamp)
            stats["zone_statistics"][zone_name] = {
                "total_unique_tracks": len(self.zone_unique_tracks[zone_name]),
                "tracks_in_time_window": len(zone_tracks_in_window)
            }
        
        return stats
    
    def reset_counters(self, reset_zones: bool = True, reset_time_tracking: bool = True):
        """Reset counting state."""
        if reset_zones:
            self.zone_counters.clear()
            self.dwell_times.clear()
            self.zone_unique_tracks.clear()
            self.zone_track_timestamps.clear()
        
        if reset_time_tracking:
            self.unique_tracks_seen.clear()
            self.track_timestamps.clear()
            self.track_last_seen.clear()
            self.bbox_fingerprints.clear()
            self.seen_bbox_fingerprints.clear()
            self.category_bbox_fingerprints.clear()
    
    def _get_tracks_in_time_window(self, current_timestamp: float) -> Set[str]:
        """Get tracks that were first seen within the time window."""
        cutoff_time = current_timestamp - self.time_window
        return {track_id for track_id, first_seen in self.track_timestamps.items() 
                if first_seen >= cutoff_time}
    
    def _get_zone_tracks_in_time_window(self, zone_name: str, current_timestamp: float) -> Set[str]:
        """Get zone tracks that were first seen within the time window."""
        cutoff_time = current_timestamp - self.time_window
        zone_timestamps = self.zone_track_timestamps.get(zone_name, {})
        return {track_id for track_id, first_seen in zone_timestamps.items() 
                if first_seen >= cutoff_time}
    
    def _clean_expired_zone_tracks(self, zone_name: str, current_timestamp: float):
        """Clean expired tracks from zone tracking."""
        if zone_name not in self.zone_track_timestamps:
            return
        
        expired_tracks = []
        zone_timestamps = self.zone_track_timestamps[zone_name]
        
        for track_id, first_seen in zone_timestamps.items():
            if current_timestamp - first_seen > self.track_expiry_time:
                expired_tracks.append(track_id)
        
        for track_id in expired_tracks:
            self.zone_unique_tracks[zone_name].discard(track_id)
            self.zone_track_timestamps[zone_name].pop(track_id, None)
    
    def _is_duplicate_detection(self, detection: Dict[str, Any], current_detections: List[Dict[str, Any]]) -> bool:
        """Check if detection is a duplicate based on bbox similarity."""
        if not self.enable_bbox_deduplication:
            return False
        
        detection_bbox = detection.get("bounding_box", detection.get("bbox"))
        if not detection_bbox:
            return False
        
        detection_category = detection.get("category", "unknown")
        
        for existing_detection in current_detections:
            existing_bbox = existing_detection.get("bounding_box", existing_detection.get("bbox"))
            existing_category = existing_detection.get("category", "unknown")
            
            if existing_bbox and detection_category == existing_category:
                overlap = calculate_bbox_overlap(detection_bbox, existing_bbox)
                if overlap >= self.bbox_similarity_threshold:
                    return True
        
        return False 