"""
Unified object trackers for Matrice post-processing.

Each adapter accepts ``List[Dict]`` detections (bbox, category, confidence)
and returns the same list with ``track_id`` attached.
"""

from .base import BaseObjectTracker, DetectionDict, ensure_track_id
from .config import SUPPORTED_TRACKING_METHODS, MatriceTrackerConfig
from .factory import create_tracker, normalize_tracking_method
from .frame_timestamp import FrameTimestampReader
from .integration import (
    ConfigDrivenTracker,
    TrackerHealth,
    TrackerInitializationError,
    TrackerProfile,
    build_tracker_config,
    get_effective_tracking_method,
    legacy_sort_enabled,
    legacy_sort_tracker_overrides,
    record_untracked_frame,
    record_update_failure,
    tracker_health,
    tracker_namespace,
)

__all__ = [
    "FrameTimestampReader",
    "BaseObjectTracker",
    "ConfigDrivenTracker",
    "DetectionDict",
    "MatriceTrackerConfig",
    "SUPPORTED_TRACKING_METHODS",
    "TrackerHealth",
    "TrackerInitializationError",
    "TrackerProfile",
    "build_tracker_config",
    "create_tracker",
    "ensure_track_id",
    "get_effective_tracking_method",
    "legacy_sort_enabled",
    "legacy_sort_tracker_overrides",
    "normalize_tracking_method",
    "record_untracked_frame",
    "record_update_failure",
    "tracker_health",
    "tracker_namespace",
]
