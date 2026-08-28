"""Stub file for post_processing.Trackers.advanced_tracker directory."""
from typing import Any, Dict, List, Optional

from ...advanced_tracker import AdvancedTracker
from ...advanced_tracker.config import TrackerConfig
from ..base import BaseObjectTracker, DetectionDict
from ..config import MatriceTrackerConfig

# Constants
logger: Any = ...  # From adapter

# Classes
# From adapter
class AdvancedTrackerAdapter:
    # Thin wrapper around ``AdvancedTracker`` with Matrice dict I/O.

    def __init__(self: Any, config: Any, namespace: Optional[str] = None) -> None: ...

    def reset(self: Any) -> None: ...

    def restore_state(self: Any) -> None: ...

    def save_state(self: Any) -> None: ...

    def update(self: Any, detections: List[Any], stream_info: Optional[Dict[str, Any]] = None) -> List[Any]: ...


from . import adapter