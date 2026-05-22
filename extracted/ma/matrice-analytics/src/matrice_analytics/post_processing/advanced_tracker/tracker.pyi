"""Auto-generated stub for module: tracker."""
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from .base import BaseTrack, TrackState
from .config import TrackerConfig
from .kalman_filter import KalmanFilterXYAH
from .matching import fuse_score, iou_distance, linear_assignment
from .strack import STrack
from .track_class_aggregator import TrackClassAggregator

# Constants
logger: Any

# Classes
class AdvancedTracker:
    # AdvancedTracker: A tracking algorithm similar to BYTETracker for object detection and tracking.
    #
    # This class encapsulates the functionality for initializing, updating, and managing the tracks for detected objects in a
    # video sequence. It maintains the state of tracked, lost, and removed tracks over frames, utilizes Kalman filtering for
    # predicting the new object locations, and performs data association.
    #
    # Attributes:
    #     tracked_stracks (List[STrack]): List of successfully activated tracks.
    #     lost_stracks (List[STrack]): List of lost tracks.
    #     removed_stracks (List[STrack]): List of removed tracks.
    #     frame_id (int): The current frame ID.
    #     config (TrackerConfig): Tracker configuration.
    #     max_time_lost (int): The maximum frames for a track to be considered as 'lost'.
    #     kalman_filter (KalmanFilterXYAH): Kalman Filter object.
    #     class_smoother (Optional[ClassSmoother]): Optional class smoother for class label smoothing over flicker.

    def __init__(self: Any, config: Any, namespace: Optional[str] = None) -> None:
        """
        Initialize an AdvancedTracker instance for object tracking.
        
        Args:
            config (TrackerConfig): Tracker configuration object.
            namespace (Optional[str]): Namespace for track ID generation (e.g., camera_id).
                If provided, track IDs are isolated to this namespace to prevent
                cross-camera collisions. Recommended to use hash of camera_id.
        """
        ...

    def clear_saved_state(self: Any) -> bool:
        """
        Clear saved tracker state (use when intentionally resetting counts).
        
        Returns:
            bool: True if state was cleared successfully
        """
        ...

    def get_category_counts(self: Any) -> Dict[str, int]:
        """
        Get unique track counts by category since tracker start.
        """
        ...

    def get_dists(self: Any, tracks: List[Any], detections: List[Any]) -> Any.Any:
        """
        Calculate the distance between tracks and detections using IoU and optionally fuse scores.
        """
        ...

    def get_kalmanfilter(self: Any) -> Any:
        """
        Return a Kalman filter object for tracking bounding boxes using KalmanFilterXYAH.
        """
        ...

    def get_new_tracks_this_frame(self: Any, previous_ids: Set[int]) -> Set[int]:
        """
        Get track IDs that are new compared to a previous set.
        """
        ...

    def get_state_file_path(self: Any) -> str:
        """
        Get the file path for state persistence.
        """
        ...

    def get_total_count(self: Any) -> int:
        """
        Get total unique track count since tracker start.
        """
        ...

    def joint_stracks(tlista: List[Any], tlistb: List[Any]) -> List[Any]:
        """
        Combine two lists of STrack objects into a single list, ensuring no duplicates based on track IDs.
        """
        ...

    def multi_predict(self: Any, tracks: List[Any]) -> Any:
        """
        Predict the next states for multiple tracks using Kalman filter.
        """
        ...

    def remove_duplicate_stracks(self: Any, stracksa: List[Any], stracksb: List[Any]) -> Tuple[List[Any], List[Any]]:
        """
        Remove duplicate stracks from two lists based on Intersection over Union (IoU) distance.
        
                Uses the configurable duplicate_removal_iou_thresh from config.
                Higher thresholds are more permissive (reduce false duplicates).
                Lower thresholds are more aggressive (remove more duplicates).
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset the tracker by clearing all tracked, lost, and removed tracks and reinitializing the Kalman filter.
        """
        ...

    def reset_id() -> Any:
        """
        Reset the ID counter for STrack instances to ensure unique track IDs across tracking sessions.
        """
        ...

    def restore_state(self: Any) -> bool:
        """
        Restore tracker state from persistent storage.
        
        Call this after creating a new tracker instance to recover accumulated counts.
        
        Returns:
            bool: True if state was restored successfully
        """
        ...

    def save_state(self: Any) -> bool:
        """
        Save tracker state to persistent storage.
        
        This preserves count accuracy across restarts or tracker recreation.
        
        Returns:
            bool: True if state was saved successfully
        """
        ...

    def sub_stracks(tlista: List[Any], tlistb: List[Any]) -> List[Any]:
        """
        Filter out the stracks present in the second list from the first list.
        """
        ...

    def update(self: Any, detections: Union[List[Dict], Dict[str, List[Dict]]], img: Optional[Any.Any] = None) -> Union[List[Dict], Dict[str, List[Dict]]]:
        """
        Update the tracker with new detections and return the current list of tracked objects.
        
        Args:
            detections: Detection results in various formats:
                - List[Dict]: Single frame detections
                - Dict[str, List[Dict]]: Multi-frame detections with frame keys
            img: Optional image for motion compensation
        
        Returns:
            Tracking results in the same format as input
        """
        ...

