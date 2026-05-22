"""Auto-generated stub for module: proxy_tracker."""
from typing import Any, Dict, List, Tuple

# Constants
logger: Any

# Classes
class KalmanFilterXYAH:
    # Kalman filter for bbox tracking (center_x, center_y, aspect_ratio, height).

    def __init__(self: Any) -> None: ...

    def initiate(self: Any, measurement: Any.Any) -> Tuple[Any.Any, Any.Any]: ...

    def predict(self: Any, mean: Any.Any, covariance: Any.Any) -> Tuple[Any.Any, Any.Any]: ...

    def project(self: Any, mean: Any.Any, covariance: Any.Any) -> Tuple[Any.Any, Any.Any]: ...

    def update(self: Any, mean: Any.Any, covariance: Any.Any, measurement: Any.Any) -> Tuple[Any.Any, Any.Any]: ...

class ProxyAdvancedTracker:
    # Production-ready tracker compatible with usecase pipeline.
    #
    # Input format (detection dict):
    #     {
    #         "bounding_box": {"xmin": float, "ymin": float, "xmax": float, "ymax": float},
    #         "category": str,
    #         "confidence": float,
    #         ...
    #     }
    #
    # Output format (same dict with track_id and frame_id added):
    #     {
    #         "bounding_box": {...},
    #         "category": str,
    #         "confidence": float,
    #         "track_id": int,
    #         "frame_id": int,
    #         ...
    #     }

    def __init__(self: Any, iou_threshold: float = 0.3, max_misses: int = 30) -> None: ...

    def get_tracker_stats(self: Any) -> Dict[str, Any]:
        """
        Get tracker statistics.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset tracker state.
        """
        ...

    def restore_state(self: Any) -> Any:
        """
        No-op for compatibility with AdvancedTracker API.
        """
        ...

    def update(self: Any, detections: List[Dict]) -> List[Dict]:
        """
        Update tracker with detections and return detections with track_id added.
        
        Args:
            detections: List of detection dicts with bounding_box, category, confidence
        
        Returns:
            Same detections list with track_id and frame_id fields added to each detection
        """
        ...

class TrackState:
    CONFIRMED: int
    LOST: int
    REMOVED: int
    TENTATIVE: int

