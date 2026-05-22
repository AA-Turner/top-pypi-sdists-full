"""Auto-generated stub for module: advanced_tracking_utils."""
from typing import Any, Dict, List

from .geometry_utils import calculate_iou, get_bbox_center

# Constants
logger: Any

# Functions
def convert_bbox_to_z(bbox: Any) -> Any:
    """
    Convert bounding box to Kalman filter state vector.
    """
    ...
def convert_detection_to_tracking_format(detection: Dict) -> Dict:
    """
    Convert detection format to tracking format.
    """
    ...
def convert_tracking_to_detection_format(tracking_result: Dict) -> Dict:
    """
    Convert tracking result back to detection format.
    """
    ...
def convert_x_to_bbox(x: Any, score: Any = None) -> Any:
    """
    Convert Kalman filter state vector to bounding box.
    """
    ...

# Classes
class AdvancedTrackingLibrary:
    # Advanced tracking library with Kalman filter support.

    def __init__(self: Any, tracking_method: str = 'kalman', max_age: int = 30, min_hits: int = 3, iou_threshold: float = 0.3, target_classes: List[str] = None) -> None:
        """
        Initialize advanced tracking library.
        """
        ...

    def get_active_tracks(self: Any) -> Dict[int, Dict]:
        """
        Get currently active tracks.
        """
        ...

    def get_track_counts(self: Any) -> Dict[str, int]:
        """
        Get total track counts by class.
        """
        ...

    def process(self: Any, detections: List[Dict], frame_id: str = None) -> Dict[str, Any]:
        """
        Process detections and return tracking results.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset tracking state.
        """
        ...

class KalmanBoxTracker:
    # Individual object tracker using Kalman filter.

    def __init__(self: Any, bbox: Any, class_name: Any, confidence: Any = 0.0, features: Any = None) -> None:
        """
        Initialize Kalman filter tracker.
        """
        ...

    count: int

    def get_center(self: Any) -> Any:
        """
        Get current center point.
        """
        ...

    def get_state(self: Any) -> Any:
        """
        Get current bounding box.
        """
        ...

    def is_active(self: Any) -> Any:
        """
        Check if tracker is still active.
        """
        ...

    def predict(self: Any) -> Any:
        """
        Predict next state.
        """
        ...

    def update(self: Any, bbox: Any, confidence: Any = None, features: Any = None) -> Any:
        """
        Update tracker with new detection.
        """
        ...

