"""
Advanced tracking utilities with Kalman filter support for post-processing.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Any, Union
import time
import logging
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

# Try to import optional dependencies
try:
    from filterpy.kalman import KalmanFilter
    KALMAN_AVAILABLE = True
except ImportError:
    KALMAN_AVAILABLE = False
    logger.warning("filterpy not available. Advanced Kalman tracking disabled. Install with: pip install filterpy")

try:
    from scipy.optimize import linear_sum_assignment
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    logger.warning("scipy not available. Optimal assignment disabled. Install with: pip install scipy")

from .geometry_utils import get_bbox_center, calculate_iou


def convert_bbox_to_z(bbox):
    """Convert bounding box to Kalman filter state vector."""
    if isinstance(bbox, dict):
        # Handle dict format
        if "xmin" in bbox:
            x1, y1, x2, y2 = bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]
        elif "x1" in bbox:
            x1, y1, x2, y2 = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]
        else:
            values = list(bbox.values())
            x1, y1, x2, y2 = values[0], values[1], values[2], values[3]
        bbox = [x1, y1, x2, y2]
    
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = bbox[0] + w/2.
    y = bbox[1] + h/2.
    s = w * h
    r = w / float(h) if h > 0 else 1.0
    return np.array([x, y, s, r]).reshape((4, 1))


def convert_x_to_bbox(x, score=None):
    """Convert Kalman filter state vector to bounding box."""
    w = np.sqrt(x[2] * x[3])
    h = x[2] / w if w > 0 else x[2]
    if score is None:
        return np.array([x[0]-w/2., x[1]-h/2., x[0]+w/2., x[1]+h/2.]).reshape((1, 4))
    else:
        return np.array([x[0]-w/2., x[1]-h/2., x[0]+w/2., x[1]+h/2., score]).reshape((1, 5))


def convert_detection_to_tracking_format(detection: Dict) -> Dict:
    """Convert detection format to tracking format."""
    tracking_detection = detection.copy()
    
    # Ensure bbox format consistency
    if 'bounding_box' in detection and 'bbox' not in detection:
        tracking_detection['bbox'] = detection['bounding_box']
    elif 'bbox' in detection and 'bounding_box' not in detection:
        tracking_detection['bounding_box'] = detection['bbox']
    
    # Ensure category/class consistency
    if 'category' in detection and 'class' not in detection:
        tracking_detection['class'] = detection['category']
    elif 'class' in detection and 'category' not in detection:
        tracking_detection['category'] = detection['class']
    
    return tracking_detection


def convert_tracking_to_detection_format(tracking_result: Dict) -> Dict:
    """Convert tracking result back to detection format."""
    detection = tracking_result.copy()
    
    # Ensure standard detection format
    if 'bbox' in tracking_result and 'bounding_box' not in tracking_result:
        detection['bounding_box'] = tracking_result['bbox']
    
    if 'class' in tracking_result and 'category' not in tracking_result:
        detection['category'] = tracking_result['class']
    
    return detection


class KalmanBoxTracker:
    """Individual object tracker using Kalman filter."""
    
    count = 0
    
    def __init__(self, bbox, class_name, confidence=0.0, features=None):
        """Initialize Kalman filter tracker."""
        if not KALMAN_AVAILABLE:
            raise ImportError("filterpy is required for Kalman tracking. Install with: pip install filterpy")
            
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        self.kf.F = np.array([[1,0,0,0,1,0,0],
                              [0,1,0,0,0,1,0],
                              [0,0,1,0,0,0,1],
                              [0,0,0,1,0,0,0],
                              [0,0,0,0,1,0,0],
                              [0,0,0,0,0,1,0],
                              [0,0,0,0,0,0,1]])
        self.kf.H = np.array([[1,0,0,0,0,0,0],
                              [0,1,0,0,0,0,0],
                              [0,0,1,0,0,0,0],
                              [0,0,0,1,0,0,0]])

        self.kf.R[2:,2:] *= 10.
        self.kf.P[4:,4:] *= 1000.
        self.kf.P *= 10.
        self.kf.Q[-1,-1] *= 0.01
        self.kf.Q[4:,4:] *= 0.01

        self.kf.x[:4] = convert_bbox_to_z(bbox)
        self.time_since_update = 0
        self.id = KalmanBoxTracker.count
        KalmanBoxTracker.count += 1
        self.history = []
        self.hits = 0
        self.hit_streak = 0
        self.age = 0
        self.class_name = class_name
        self.confidence = confidence
        self.features = features or []
        
        # Enhanced tracking attributes
        self.disappeared_frames = 0
        self.max_disappeared = 15
        self.trajectory = []
        self.velocity = (0, 0)
        self.center_history = []
        
    def update(self, bbox, confidence=None, features=None):
        """Update tracker with new detection."""
        self.time_since_update = 0
        self.history = []
        self.hits += 1
        self.hit_streak += 1
        self.disappeared_frames = 0
        
        if confidence is not None:
            self.confidence = confidence
        if features is not None:
            self.features = features
            
        # Update center history
        if isinstance(bbox, dict):
            center = get_bbox_center(bbox)
        else:
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            center = (center_x, center_y)
        
        self.center_history.append((center[0], center[1], time.time()))
        
        # Keep only recent history
        if len(self.center_history) > 20:
            self.center_history = self.center_history[-20:]
            
        # Calculate velocity
        if len(self.center_history) >= 2:
            curr_pos = self.center_history[-1]
            prev_pos = self.center_history[-2]
            dt = curr_pos[2] - prev_pos[2]
            if dt > 0:
                self.velocity = ((curr_pos[0] - prev_pos[0]) / dt, 
                               (curr_pos[1] - prev_pos[1]) / dt)
        
        self.kf.update(convert_bbox_to_z(bbox))

    def predict(self):
        """Predict next state."""
        if (self.kf.x[6] + self.kf.x[2]) <= 0:
            self.kf.x[6] *= 0.0
        self.kf.predict()
        self.age += 1
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        self.disappeared_frames += 1
        self.history.append(convert_x_to_bbox(self.kf.x))
        return self.history[-1]

    def get_state(self):
        """Get current bounding box."""
        return convert_x_to_bbox(self.kf.x)
    
    def get_center(self):
        """Get current center point."""
        bbox = self.get_state()[0]
        return ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
    
    def is_active(self):
        """Check if tracker is still active."""
        return self.disappeared_frames < self.max_disappeared


class AdvancedTrackingLibrary:
    """Advanced tracking library with Kalman filter support."""
    
    def __init__(self, 
                 tracking_method: str = 'kalman',
                 max_age: int = 30,
                 min_hits: int = 3,
                 iou_threshold: float = 0.3,
                 target_classes: List[str] = None):
        """Initialize advanced tracking library."""
        self.tracking_method = tracking_method
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.target_classes = target_classes or []
        
        if tracking_method == 'kalman' and not KALMAN_AVAILABLE:
            logger.warning("Kalman tracking requested but filterpy not available. Falling back to basic tracking.")
            self.tracking_method = 'basic'
        
        self.trackers = []
        self.frame_count = 0
        self.total_counts = defaultdict(int)
        self.class_tracks = defaultdict(set)
        self.active_tracks = {}
        
    def process(self, detections: List[Dict], frame_id: str = None) -> Dict[str, Any]:
        """Process detections and return tracking results."""
        if frame_id is None:
            frame_id = str(self.frame_count)
        
        self.frame_count += 1
        
        # Format detections for tracking
        formatted_detections = self._format_detections(detections)
        
        # Update tracking
        tracked_detections = self._update_tracking(formatted_detections)
        
        # Convert to tracking format
        tracking_results = {
            frame_id: []
        }
        
        for detection in tracked_detections:
            tracking_detection = convert_detection_to_tracking_format(detection)
            tracking_results[frame_id].append(tracking_detection)
        
        return tracking_results
    
    def _format_detections(self, detections: List[Dict]) -> List[Dict]:
        """Format detections for tracking."""
        formatted = []
        
        for detection in detections:
            # Skip if not target class
            class_name = detection.get('category', detection.get('class', 'unknown'))
            if self.target_classes and class_name not in self.target_classes:
                continue
            
            # Ensure required fields
            formatted_detection = {
                'bbox': detection.get('bounding_box', detection.get('bbox')),
                'confidence': detection.get('confidence', 1.0),
                'class': class_name,
                'category': class_name
            }
            
            # Add optional fields
            if 'features' in detection:
                formatted_detection['features'] = detection['features']
            
            formatted.append(formatted_detection)
        
        return formatted
    
    def _update_tracking(self, detections: List[Dict]) -> List[Dict]:
        """Update tracking with new detections."""
        if self.tracking_method == 'kalman':
            return self._update_kalman_tracking(detections)
        else:
            return self._update_basic_tracking(detections)
    
    def _update_kalman_tracking(self, detections: List[Dict]) -> List[Dict]:
        """Update Kalman filter based tracking."""
        # Predict for all trackers
        for tracker in self.trackers:
            tracker.predict()
        
        # Associate detections to trackers
        matched, unmatched_dets, unmatched_trks = self._associate_detections_to_trackers(
            detections, self.trackers, self.iou_threshold
        )
        
        # Update matched trackers
        for m in matched:
            self.trackers[m[1]].update(detections[m[0]]['bbox'], 
                                     detections[m[0]]['confidence'],
                                     detections[m[0]].get('features'))
        
        # Create new trackers for unmatched detections
        for i in unmatched_dets:
            det = detections[i]
            tracker = KalmanBoxTracker(
                det['bbox'], 
                det['class'], 
                det['confidence'],
                det.get('features')
            )
            self.trackers.append(tracker)
        
        # Remove dead trackers
        active_trackers = []
        tracked_detections = []
        
        for tracker in self.trackers:
            if tracker.time_since_update < self.max_age and tracker.hit_streak >= self.min_hits:
                # Create tracked detection
                bbox = tracker.get_state()[0]
                tracked_det = {
                    'bbox': {
                        'xmin': int(bbox[0]),
                        'ymin': int(bbox[1]),
                        'xmax': int(bbox[2]),
                        'ymax': int(bbox[3])
                    },
                    'bounding_box': {
                        'xmin': int(bbox[0]),
                        'ymin': int(bbox[1]),
                        'xmax': int(bbox[2]),
                        'ymax': int(bbox[3])
                    },
                    'track_id': tracker.id,
                    'confidence': tracker.confidence,
                    'class': tracker.class_name,
                    'category': tracker.class_name,
                    'velocity': tracker.velocity
                }
                
                tracked_detections.append(tracked_det)
                self.active_tracks[tracker.id] = tracked_det
                self.class_tracks[tracker.class_name].add(tracker.id)
            
            if tracker.is_active():
                active_trackers.append(tracker)
        
        self.trackers = active_trackers
        return tracked_detections
    
    def _update_basic_tracking(self, detections: List[Dict]) -> List[Dict]:
        """Basic tracking fallback when Kalman is not available."""
        # Simple tracking based on IoU matching
        tracked_detections = []
        
        for i, detection in enumerate(detections):
            # Add basic track ID (frame-based)
            track_id = f"{self.frame_count}_{i}"
            
            tracked_det = detection.copy()
            tracked_det['track_id'] = track_id
            tracked_detections.append(tracked_det)
        
        return tracked_detections
    
    def _associate_detections_to_trackers(self, detections, trackers, iou_threshold=0.3):
        """Associate detections to trackers using IoU."""
        if len(trackers) == 0:
            return np.empty((0, 2), dtype=int), np.arange(len(detections)), np.empty((0, 5), dtype=int)
        
        # Create IoU matrix
        iou_matrix = np.zeros((len(detections), len(trackers)), dtype=np.float32)
        
        for d, det in enumerate(detections):
            det_bbox = det['bbox']
            if isinstance(det_bbox, dict):
                det_bbox = [det_bbox.get('xmin', 0), det_bbox.get('ymin', 0), 
                           det_bbox.get('xmax', 0), det_bbox.get('ymax', 0)]
            
            for t, trk in enumerate(trackers):
                trk_bbox = trk.get_state()[0]
                iou_matrix[d, t] = calculate_iou(det_bbox, trk_bbox)
        
        # Use Hungarian algorithm if available, otherwise greedy matching
        if SCIPY_AVAILABLE:
            matched_indices = linear_sum_assignment(-iou_matrix)
            matched_indices = np.array(list(zip(matched_indices[0], matched_indices[1])))
        else:
            matched_indices = self._greedy_assignment(iou_matrix)
        
        unmatched_detections = []
        for d, det in enumerate(detections):
            if len(matched_indices) == 0 or d not in matched_indices[:, 0]:
                unmatched_detections.append(d)
        
        unmatched_trackers = []
        for t, trk in enumerate(trackers):
            if len(matched_indices) == 0 or t not in matched_indices[:, 1]:
                unmatched_trackers.append(t)
        
        # Filter out matched with low IoU
        matches = []
        for m in matched_indices:
            if iou_matrix[m[0], m[1]] < iou_threshold:
                unmatched_detections.append(m[0])
                unmatched_trackers.append(m[1])
            else:
                matches.append(m.reshape(1, 2))
        
        if len(matches) == 0:
            matches = np.empty((0, 2), dtype=int)
        else:
            matches = np.concatenate(matches, axis=0)
        
        return matches, np.array(unmatched_detections), np.array(unmatched_trackers)
    
    def _greedy_assignment(self, cost_matrix):
        """Greedy assignment when scipy is not available."""
        matches = []
        used_rows = set()
        used_cols = set()
        
        # Sort by cost (descending for IoU)
        costs = []
        for i in range(cost_matrix.shape[0]):
            for j in range(cost_matrix.shape[1]):
                costs.append((cost_matrix[i, j], i, j))
        
        costs.sort(reverse=True)  # Highest IoU first
        
        for cost, i, j in costs:
            if i not in used_rows and j not in used_cols:
                matches.append([i, j])
                used_rows.add(i)
                used_cols.add(j)
        
        return np.array(matches)
    
    def get_track_counts(self) -> Dict[str, int]:
        """Get total track counts by class."""
        return dict(self.total_counts)
    
    def get_active_tracks(self) -> Dict[int, Dict]:
        """Get currently active tracks."""
        return self.active_tracks.copy()
    
    def reset(self):
        """Reset tracking state."""
        self.trackers = []
        self.frame_count = 0
        self.total_counts.clear()
        self.class_tracks.clear()
        self.active_tracks.clear()
        KalmanBoxTracker.count = 0 