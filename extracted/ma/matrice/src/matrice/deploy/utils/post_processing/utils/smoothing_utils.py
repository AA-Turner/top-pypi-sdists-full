"""
BBox smoothing utilities for post-processing operations.

This module provides generalized smoothing algorithms for bounding box detections
to reduce noise and false positives in detection results.
"""

from typing import List, Dict, Any, Optional, Union
from collections import deque
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class BBoxSmoothingConfig:
    """Configuration for bbox smoothing algorithms."""
    
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    window_size: int = 20
    cooldown_frames: int = 5
    confidence_threshold: float = 0.5
    confidence_range_factor: float = 0.5  # For observability algorithm
    track_by_centroid: bool = True
    centroid_quantization: int = 10
    enable_smoothing: bool = True  # Master flag to enable/disable smoothing
    
    def __post_init__(self):
        """Validate configuration parameters."""
        if self.smoothing_algorithm not in ["window", "observability"]:
            raise ValueError(f"Invalid smoothing_algorithm: {self.smoothing_algorithm}. Must be 'window' or 'observability'")
        
        if self.window_size <= 0:
            raise ValueError(f"window_size must be positive, got {self.window_size}")
        
        if self.cooldown_frames < 0:
            raise ValueError(f"cooldown_frames must be non-negative, got {self.cooldown_frames}")
        
        if not 0.0 <= self.confidence_threshold <= 1.0:
            raise ValueError(f"confidence_threshold must be between 0.0 and 1.0, got {self.confidence_threshold}")
        
        if not 0.0 <= self.confidence_range_factor <= 1.0:
            raise ValueError(f"confidence_range_factor must be between 0.0 and 1.0, got {self.confidence_range_factor}")


class BBoxSmoothingTracker:
    """Tracks individual objects for smoothing across frames."""
    
    def __init__(self, config: BBoxSmoothingConfig):
        self.config = config
        self.object_windows = {}  # {object_id: deque}
        self.object_cooldowns = {}  # {object_id: cooldown_counter}
        self.logger = logging.getLogger(f"{__name__}.BBoxSmoothingTracker")
    
    def reset(self):
        """Reset tracker state."""
        self.object_windows.clear()
        self.object_cooldowns.clear()
        self.logger.debug("BBox smoothing tracker reset")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get tracker statistics."""
        return {
            "active_objects": len(self.object_windows),
            "total_cooldowns": len(self.object_cooldowns),
            "window_size": self.config.window_size,
            "cooldown_frames": self.config.cooldown_frames
        }


def _get_object_id(detection: Dict, config: BBoxSmoothingConfig) -> str:
    """
    Generate unique object ID from detection using robust hashing.
    
    Args:
        detection: Detection dictionary
        config: Smoothing configuration
        
    Returns:
        str: Unique object identifier
    """
    # Extract bbox coordinates (handle different formats)
    bbox = detection.get('bounding_box', detection.get('bbox', {}))
    
    # Normalize bbox to consistent format
    if isinstance(bbox, dict):
        if 'x' in bbox and 'y' in bbox and 'width' in bbox and 'height' in bbox:
            x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
        elif 'xmin' in bbox and 'ymin' in bbox and 'xmax' in bbox and 'ymax' in bbox:
            x, y, w, h = bbox['xmin'], bbox['ymin'], bbox['xmax'] - bbox['xmin'], bbox['ymax'] - bbox['ymin']
        elif 'x1' in bbox and 'y1' in bbox and 'x2' in bbox and 'y2' in bbox:
            x, y, w, h = bbox['x1'], bbox['y1'], bbox['x2'] - bbox['x1'], bbox['y2'] - bbox['y1']
        else:
            # Fallback: try to extract any numeric values
            values = [v for v in bbox.values() if isinstance(v, (int, float))]
            if len(values) >= 4:
                x, y, w, h = values[0], values[1], values[2], values[3]
            else:
                x, y, w, h = 0, 0, 0, 0
    else:
        # Handle list/tuple format
        if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
        else:
            x, y, w, h = 0, 0, 0, 0
    
    # Quantize coordinates to reduce jitter (similar to centroid approach but more robust)
    quantized_x = int(x // config.centroid_quantization) if hasattr(config, 'centroid_quantization') else int(x)
    quantized_y = int(y // config.centroid_quantization) if hasattr(config, 'centroid_quantization') else int(y)
    quantized_w = int(w // config.centroid_quantization) if hasattr(config, 'centroid_quantization') else int(w)
    quantized_h = int(h // config.centroid_quantization) if hasattr(config, 'centroid_quantization') else int(h)
    
    # Get other attributes (handle missing values)
    confidence = detection.get('confidence', 0.0)
    category = detection.get('category', 'unknown')
    
    # Create hash string from quantized bbox and attributes (no track_id dependency)
    hash_string = f"{quantized_x}_{quantized_y}_{quantized_w}_{quantized_h}_{confidence}_{category}"
    
    # Generate hash and ensure it's positive
    detection_hash = abs(hash(hash_string))
    return f"detection_{detection_hash}"


def _apply_window_smoothing(detections: List[Dict], 
                          config: BBoxSmoothingConfig,
                          tracker: BBoxSmoothingTracker) -> List[Dict]:
    """
    Apply window smoothing without cooldown (frame-accurate).
    
    Args:
        detections: List of detection dictionaries
        config: Smoothing configuration
        tracker: Tracker instance for state management
        
    Returns:
        List[Dict]: Smoothed detections (only from current frame)
    """
    output = []
    current_object_ids = set()
    
    # Process current detections
    for det in detections:
        object_id = _get_object_id(det, config)
        current_object_ids.add(object_id)
        
        # Initialize window if new object
        if object_id not in tracker.object_windows:
            tracker.object_windows[object_id] = deque(maxlen=config.window_size)
        
        # Add to window
        tracker.object_windows[object_id].append(det)
    
    # Only output detections from current frame
    for object_id in current_object_ids:
        if object_id in tracker.object_windows:
            window = tracker.object_windows[object_id]
            if window:
                # Calculate average confidence for smoothing
                confidences = [d.get('confidence', 0.0) for d in window]
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
                
                # Output if above threshold
                if avg_confidence >= config.confidence_threshold:
                    output.append(window[-1])  # Most recent detection
    
    # Clean up unused windows (optional memory management)
    for object_id in list(tracker.object_windows.keys()):
        if object_id not in current_object_ids:
            del tracker.object_windows[object_id]
    
    return output


def _apply_observability_smoothing(detections: List[Dict],
                                 config: BBoxSmoothingConfig,
                                 tracker: BBoxSmoothingTracker) -> List[Dict]:
    """
    Apply observability/confidence tradeoff smoothing without cooldown (frame-accurate).
    
    Args:
        detections: List of detection dictionaries
        config: Smoothing configuration
        tracker: Tracker instance for state management
        
    Returns:
        List[Dict]: Smoothed detections (only from current frame)
    """
    output = []
    current_object_ids = set()
    
    # Process current detections
    for det in detections:
        object_id = _get_object_id(det, config)
        current_object_ids.add(object_id)
        
        # Initialize window if new object
        if object_id not in tracker.object_windows:
            tracker.object_windows[object_id] = deque(maxlen=config.window_size)
        
        tracker.object_windows[object_id].append(det)
    
    # Only process detections from current frame
    for object_id in current_object_ids:
        if object_id in tracker.object_windows:
            window = tracker.object_windows[object_id]
            if window:
                # Calculate observability score
                observability_score = len(window) / config.window_size
                
                # Get current confidence
                current_confidence = window[-1].get('confidence', 0.0)
                
                # Define confidence range
                conf_range = config.confidence_threshold * config.confidence_range_factor
                
                # Decision logic
                if current_confidence >= config.confidence_threshold:
                    # High confidence: always keep
                    output.append(window[-1])
                elif current_confidence >= (config.confidence_threshold - conf_range):
                    # Borderline: apply tradeoff
                    confidence_factor = (config.confidence_threshold - current_confidence) / conf_range
                    if confidence_factor <= observability_score:
                        output.append(window[-1])
                # else: too low confidence, discard
    
    # Clean up unused windows (optional memory management)
    for object_id in list(tracker.object_windows.keys()):
        if object_id not in current_object_ids:
            del tracker.object_windows[object_id]
    
    return output


def bbox_smoothing(detections: Union[List[Dict], Dict[str, List[Dict]]], 
                  config: BBoxSmoothingConfig,
                  tracker: Optional[BBoxSmoothingTracker] = None) -> Union[List[Dict], Dict[str, List[Dict]]]:
    """
    Apply smoothing algorithm to bbox detections.
    
    Args:
        detections: Either:
                   - List of detection dictionaries (detection format)
                   - Dict with frame keys containing lists of detections (tracking format)
        config: Smoothing configuration
        tracker: Optional tracker instance for persistent state across frames
        
    Returns:
        Same format as input: List[Dict] or Dict[str, List[Dict]]
    """
    # Early return if smoothing is disabled
    if not config.enable_smoothing:
        return detections
    
    # Early return if no detections
    if not detections:
        return detections
    
    # Create tracker if not provided
    if tracker is None:
        tracker = BBoxSmoothingTracker(config)
    
    # Handle tracking format (dict with frame keys)
    if isinstance(detections, dict):
        smoothed_tracking_results = {}
        
        for frame_id, frame_detections in detections.items():
            if isinstance(frame_detections, list):
                # Apply smoothing to this frame's detections
                if config.smoothing_algorithm == "observability":
                    smoothed_frame = _apply_observability_smoothing(frame_detections, config, tracker)
                else:  # "window"
                    smoothed_frame = _apply_window_smoothing(frame_detections, config, tracker)
                
                smoothed_tracking_results[frame_id] = smoothed_frame
        
        return smoothed_tracking_results
    
    # Handle detection format (list of detections)
    elif isinstance(detections, list):
        # Apply selected smoothing algorithm
        if config.smoothing_algorithm == "observability":
            return _apply_observability_smoothing(detections, config, tracker)
        else:  # "window"
            return _apply_window_smoothing(detections, config, tracker)
    
    # Fallback for unknown format
    return detections


def create_bbox_smoothing_tracker(config: BBoxSmoothingConfig) -> BBoxSmoothingTracker:
    """
    Create a new bbox smoothing tracker instance.
    
    Args:
        config: Smoothing configuration
        
    Returns:
        BBoxSmoothingTracker: New tracker instance
    """
    return BBoxSmoothingTracker(config)


def create_default_smoothing_config(**overrides) -> BBoxSmoothingConfig:
    """
    Create default smoothing configuration with optional overrides.
    
    Args:
        **overrides: Configuration overrides
        
    Returns:
        BBoxSmoothingConfig: Configuration instance
    """
    return BBoxSmoothingConfig(**overrides) 