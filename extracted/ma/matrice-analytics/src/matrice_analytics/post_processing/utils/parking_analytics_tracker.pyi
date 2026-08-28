"""Auto-generated stub for module: parking_analytics_tracker."""
from typing import Any, Dict, List

# Classes
class ParkingAnalyticsTracker:
    # Tracks parking duration and status for vehicles.
    #
    # Determines if vehicles are parked based on movement patterns:
    # - Tracks bbox position over a sliding window (default 60 frames)
    # - Calculates movement as percentage of bbox size
    # - Marks vehicle as parked after threshold duration of stationary behavior

    def __init__(self: Any, parked_threshold_frames: int = 150, movement_threshold_percent: float = 5.0, movement_window_frames: int = 60, fps: float = 30.0) -> None:
        """
        Initialize parking analytics tracker.
        
        Args:
            parked_threshold_frames: Frames vehicle must be stationary to be marked as parked
            movement_threshold_percent: Max movement % of bbox size to be considered stationary
            movement_window_frames: Number of frames to analyze for movement
            fps: Frames per second for time calculations
        """
        ...

    def update(self: Any, detections: List[Dict], current_frame: int, current_timestamp: str) -> Dict[str, Any]:
        """
        Update parking analytics with current frame detections.
        
        Args:
            detections: List of detection dicts with track_id, category, bounding_box
            current_frame: Current frame number
            current_timestamp: Current timestamp string
        
        Returns:
            Analytics summary dict with active_vehicles, parked_vehicles, and summary stats
        """
        ...

class VehicleParkingState:
    # Per-vehicle parking state tracking

    def dwell_time_frames(self: Any) -> int:
        """
        Total frames vehicle has been tracked
        """
        ...

    def parked_time_frames(self: Any) -> int:
        """
        Total frames vehicle has been parked
        """
        ...

