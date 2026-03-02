"""
Base tracking classes for advanced tracker implementation.

This module provides the foundational classes for object tracking,
including track states and base track functionality.
"""

from collections import OrderedDict
from typing import Any
import numpy as np


class TrackState:
    """
    Enumeration class representing the possible states of an object being tracked.

    Attributes:
        New (int): State when the object is newly detected.
        Tracked (int): State when the object is successfully tracked in subsequent frames.
        Lost (int): State when the object is no longer tracked.
        Removed (int): State when the object is removed from tracking.
    """

    New = 0
    Tracked = 1
    Lost = 2
    Removed = 3


class BaseTrack:
    """
    Base class for object tracking, providing foundational attributes and methods.

    Attributes:
        _count (int): Class-level counter for unique track IDs (fallback for global mode).
        _id_counter (dict): Per-namespace ID counters for camera isolation.
        track_id (int): Unique identifier for the track (numeric part).
        track_id_namespaced (str): Fully namespaced track ID ({namespace}_{id}).
        is_activated (bool): Flag indicating whether the track is currently active.
        state (TrackState): Current state of the track.
        history (OrderedDict): Ordered history of the track's states.
        features (list): List of features extracted from the object for tracking.
        curr_feature (Any): The current feature of the object being tracked.
        score (float): The confidence score of the tracking.
        start_frame (int): The frame number where tracking started.
        frame_id (int): The most recent frame ID processed by the track.
        time_since_update (int): Frames passed since the last update.
        location (tuple): The location of the object in the context of multi-camera tracking.
    """

    _count = 0  # Global counter (fallback for backward compatibility)
    _id_counters: dict = {}  # Per-namespace counters: {namespace: count}
    _current_namespace: str = None  # Currently active namespace for ID generation

    def __init__(self):
        """Initialize a new track with a unique ID and foundational tracking attributes."""
        self.track_id = 0
        self.track_id_namespaced = None  # Will be set when activated with namespace
        self._namespace = None  # Track's namespace (e.g., camera_id hash)
        self.is_activated = False
        self.state = TrackState.New
        self.history = OrderedDict()
        self.features = []
        self.curr_feature = None
        self.score = 0
        self.start_frame = 0
        self.frame_id = 0
        self.time_since_update = 0
        self.location = (np.inf, np.inf)

    @property
    def end_frame(self) -> int:
        """Return the ID of the most recent frame where the object was tracked."""
        return self.frame_id

    @staticmethod
    def set_namespace(namespace: str) -> None:
        """Set the current namespace for track ID generation.

        Call this before creating/activating tracks to assign them to a namespace.
        Typically called with camera_id or a hash of camera_id.
        """
        BaseTrack._current_namespace = namespace
        if namespace not in BaseTrack._id_counters:
            BaseTrack._id_counters[namespace] = 0

    @staticmethod
    def next_id() -> int:
        """Increment and return the next unique track ID.

        If a namespace is set, uses per-namespace counter for isolation.
        Otherwise falls back to global counter for backward compatibility.
        """
        namespace = BaseTrack._current_namespace
        if namespace is not None:
            BaseTrack._id_counters[namespace] += 1
            return BaseTrack._id_counters[namespace]
        else:
            # Fallback to global counter
            BaseTrack._count += 1
            return BaseTrack._count

    @staticmethod
    def get_namespaced_id(track_id: int) -> str:
        """Get the fully namespaced track ID string.

        Returns format: '{namespace}_{track_id}' or just '{track_id}' if no namespace.
        """
        namespace = BaseTrack._current_namespace
        if namespace:
            return f"{namespace}_{track_id}"
        return str(track_id)

    def activate(self, *args: Any) -> None:
        """Activate the track with provided arguments, initializing necessary attributes for tracking."""
        raise NotImplementedError

    def predict(self) -> None:
        """Predict the next state of the track based on the current state and tracking model."""
        raise NotImplementedError

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Update the track with new observations and data, modifying its state and attributes accordingly."""
        raise NotImplementedError

    def mark_lost(self) -> None:
        """Mark the track as lost by updating its state to TrackState.Lost."""
        self.state = TrackState.Lost

    def mark_removed(self) -> None:
        """Mark the track as removed by setting its state to TrackState.Removed."""
        self.state = TrackState.Removed

    @staticmethod
    def reset_id(namespace: str = None) -> None:
        """Reset track ID counter.

        Args:
            namespace: If provided, only reset that namespace's counter.
                      If None and a current namespace is set, reset current namespace.
                      If None and no namespace set, reset global counter.
        """
        if namespace:
            # Reset specific namespace
            BaseTrack._id_counters[namespace] = 0
        elif BaseTrack._current_namespace:
            # Reset current namespace
            BaseTrack._id_counters[BaseTrack._current_namespace] = 0
        else:
            # Reset global counter (backward compatibility)
            BaseTrack._count = 0

    @staticmethod
    def reset_all_ids() -> None:
        """Reset all ID counters (global and all namespaces)."""
        BaseTrack._count = 0
        BaseTrack._id_counters.clear()
        BaseTrack._current_namespace = None