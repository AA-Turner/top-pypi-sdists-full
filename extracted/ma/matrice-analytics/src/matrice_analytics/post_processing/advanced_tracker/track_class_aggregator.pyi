"""Auto-generated stub for module: track_class_aggregator."""
from typing import Any, Dict, List

# Constants
logger: Any

# Classes
class TrackClassAggregator:
    # Maintains per-track sliding windows of class labels and returns the most frequent.
    #
    # This aggregator reduces class label flickering in tracking results by applying
    # temporal voting based on historical observations within a sliding window.
    #
    # Attributes:
    #     window_size (int): Maximum number of frames to keep in the sliding window.
    #     track_windows (Dict[int, deque]): Per-track sliding windows of class labels.

    def __init__(self: Any, window_size: int = 30) -> None:
        """
        Initialize the TrackClassAggregator.
        
        Args:
            window_size (int): Number of recent frames to consider for aggregation.
                Must be positive. Larger windows provide more stability but slower
                adaptation to genuine class changes.
        """
        ...

    def get_active_track_count(self: Any) -> int:
        """
        Get the number of tracks currently being aggregated.
        """
        ...

    def get_aggregated_class(self: Any, track_id: int, fallback_class: Any) -> Any:
        """
        Get the aggregated class for a track without updating the window.
        
        Args:
            track_id (int): Unique identifier for the track.
            fallback_class (Any): Class to return if track has no history.
        
        Returns:
            Any: The aggregated class label, or fallback_class if no history exists.
        """
        ...

    def remove_track(self: Any, track_id: int) -> None:
        """
        Remove a track's window from memory.
        
        Args:
            track_id (int): Unique identifier for the track to remove.
        """
        ...

    def remove_tracks(self: Any, track_ids: list) -> None:
        """
        Remove multiple tracks' windows from memory (batch operation).
        
        Args:
            track_ids (list): List of track IDs to remove.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear all track windows.
        """
        ...

    def update_and_aggregate(self: Any, track_id: int, observed_class: Any) -> Any:
        """
        Update the sliding window for a track and return the aggregated class label.
        
        This method:
        1. Adds the new observation to the track's window
        2. Maintains window size by removing oldest entries if needed
        3. Returns the most frequent class in the window
        
        Args:
            track_id (int): Unique identifier for the track.
            observed_class (Any): The class label observed in the current frame.
        
        Returns:
            Any: The aggregated class label (most frequent in the window).
                If there's a tie, returns the most recent among tied classes.
        """
        ...

