"""
Unified object trackers for Matrice post-processing.

Each adapter accepts ``List[Dict]`` detections (bbox, category, confidence)
and returns the same list with ``track_id`` attached.
"""

from .base import BaseObjectTracker, DetectionDict, ensure_track_id
from .config import SUPPORTED_TRACKING_METHODS, MatriceTrackerConfig
from .factory import create_tracker, normalize_tracking_method
from .integration import (
    ConfigDrivenTracker,
    TrackerProfile,
    build_tracker_config,
    get_effective_tracking_method,
    legacy_sort_enabled,
    legacy_sort_tracker_overrides,
    tracker_namespace,
)

__all__ = [
    "BaseObjectTracker",
    "ConfigDrivenTracker",
    "DetectionDict",
    "MatriceTrackerConfig",
    "SUPPORTED_TRACKING_METHODS",
    "TrackerProfile",
    "build_tracker_config",
    "create_tracker",
    "ensure_track_id",
    "get_effective_tracking_method",
    "legacy_sort_enabled",
    "legacy_sort_tracker_overrides",
    "normalize_tracking_method",
    "tracker_namespace",
]
