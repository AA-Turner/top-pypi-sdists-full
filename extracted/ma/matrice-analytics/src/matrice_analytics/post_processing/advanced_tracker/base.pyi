"""Auto-generated stub for module: base."""
from typing import Any, List, Set

# Classes
class BaseTrack:
    # Base class for object tracking, providing foundational attributes and methods.
    #
    # Attributes:
    #     _count (int): Class-level counter for unique track IDs (fallback for global mode).
    #     _id_counter (dict): Per-namespace ID counters for camera isolation.
    #     track_id (int): Unique identifier for the track (numeric part).
    #     track_id_namespaced (str): Fully namespaced track ID ({namespace}_{id}).
    #     is_activated (bool): Flag indicating whether the track is currently active.
    #     state (TrackState): Current state of the track.
    #     history (OrderedDict): Ordered history of the track's states.
    #     features (list): List of features extracted from the object for tracking.
    #     curr_feature (Any): The current feature of the object being tracked.
    #     score (float): The confidence score of the tracking.
    #     start_frame (int): The frame number where tracking started.
    #     frame_id (int): The most recent frame ID processed by the track.
    #     time_since_update (int): Frames passed since the last update.
    #     location (tuple): The location of the object in the context of multi-camera tracking.

    def __init__(self: Any) -> None:
        """
        Initialize a new track with a unique ID and foundational tracking attributes.
        """
        ...

    def activate(self: Any, *args: Any) -> None:
        """
        Activate the track with provided arguments, initializing necessary attributes for tracking.
        """
        ...

    def end_frame(self: Any) -> int:
        """
        Return the ID of the most recent frame where the object was tracked.
        """
        ...

    def get_namespaced_id(track_id: int) -> str:
        """
        Get the fully namespaced track ID string.
        
                Returns format: '{namespace}_{track_id}' or just '{track_id}' if no namespace.
        """
        ...

    def mark_lost(self: Any) -> None:
        """
        Mark the track as lost by updating its state to TrackState.Lost.
        """
        ...

    def mark_removed(self: Any) -> None:
        """
        Mark the track as removed by setting its state to TrackState.Removed.
        """
        ...

    def next_id() -> int:
        """
        Increment and return the next unique track ID.
        
                If a namespace is set, uses per-namespace counter for isolation.
                Otherwise falls back to global counter for backward compatibility.
        """
        ...

    def predict(self: Any) -> None:
        """
        Predict the next state of the track based on the current state and tracking model.
        """
        ...

    def reset_all_ids() -> None:
        """
        Reset all ID counters (global and all namespaces).
        """
        ...

    def reset_id(namespace: str = None) -> None:
        """
        Reset track ID counter.
        
                Args:
                    namespace: If provided, only reset that namespace's counter.
                              If None and a current namespace is set, reset current namespace.
                              If None and no namespace set, reset global counter.
        """
        ...

    def set_namespace(namespace: str) -> None:
        """
        Set the current namespace for track ID generation.
        
                Call this before creating/activating tracks to assign them to a namespace.
                Typically called with camera_id or a hash of camera_id.
        """
        ...

    def update(self: Any, *args: Any, **kwargs: Any) -> None:
        """
        Update the track with new observations and data, modifying its state and attributes accordingly.
        """
        ...

class TrackState:
    # Enumeration class representing the possible states of an object being tracked.
    #
    # Attributes:
    #     New (int): State when the object is newly detected.
    #     Tracked (int): State when the object is successfully tracked in subsequent frames.
    #     Lost (int): State when the object is no longer tracked.
    #     Removed (int): State when the object is removed from tracking.

    Lost: int
    New: int
    Removed: int
    Tracked: int

