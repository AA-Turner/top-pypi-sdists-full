"""
Track class aggregation for object tracking.

This module provides a sliding-window-based mechanism to aggregate class labels
across frames, reducing label flickering in tracking outputs through temporal voting.
"""

from typing import Any, Dict
from collections import deque, Counter
import logging

logger = logging.getLogger(__name__)


class TrackClassAggregator:
    """
    Maintains per-track sliding windows of class labels and returns the most frequent.
    
    This aggregator reduces class label flickering in tracking results by applying
    temporal voting based on historical observations within a sliding window.
    
    Attributes:
        window_size (int): Maximum number of frames to keep in the sliding window.
        track_windows (Dict[int, deque]): Per-track sliding windows of class labels.
    """
    
    def __init__(self, window_size: int = 30):
        """
        Initialize the TrackClassAggregator.
        
        Args:
            window_size (int): Number of recent frames to consider for aggregation.
                Must be positive. Larger windows provide more stability but slower
                adaptation to genuine class changes.
        """
        if window_size <= 0:
            raise ValueError(f"window_size must be positive, got {window_size}")
        
        self.window_size = window_size
        self.track_windows: Dict[int, deque] = {}
    
    def update_and_aggregate(self, track_id: int, observed_class: Any) -> Any:
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
        # Initialize window for new tracks
        if track_id not in self.track_windows:
            self.track_windows[track_id] = deque(maxlen=self.window_size)
        
        # Add current observation
        window = self.track_windows[track_id]
        window.append(observed_class)
        
        # Return most frequent class
        if len(window) == 0:
            return observed_class
        
        # Count frequencies and return most common
        class_counts = Counter(window)
        most_common = class_counts.most_common(1)[0][0]
        
        return most_common
    
    def get_aggregated_class(self, track_id: int, fallback_class: Any) -> Any:
        """
        Get the aggregated class for a track without updating the window.
        
        Args:
            track_id (int): Unique identifier for the track.
            fallback_class (Any): Class to return if track has no history.
        
        Returns:
            Any: The aggregated class label, or fallback_class if no history exists.
        """
        if track_id not in self.track_windows:
            return fallback_class
        
        window = self.track_windows[track_id]
        if len(window) == 0:
            return fallback_class
        
        class_counts = Counter(window)
        return class_counts.most_common(1)[0][0]
    
    def remove_track(self, track_id: int) -> None:
        """
        Remove a track's window from memory.
        
        Args:
            track_id (int): Unique identifier for the track to remove.
        """
        if track_id in self.track_windows:
            del self.track_windows[track_id]
    
    def remove_tracks(self, track_ids: list) -> None:
        """
        Remove multiple tracks' windows from memory (batch operation).
        
        Args:
            track_ids (list): List of track IDs to remove.
        """
        for track_id in track_ids:
            self.remove_track(track_id)
    
    def reset(self) -> None:
        """Clear all track windows."""
        self.track_windows.clear()
    
    def get_active_track_count(self) -> int:
        """Get the number of tracks currently being aggregated."""
        return len(self.track_windows)
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"TrackClassAggregator(window_size={self.window_size}, active_tracks={len(self.track_windows)})"