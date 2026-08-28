"""Auto-generated stub for module: adapter."""
from typing import Any, Dict, List, Optional

from ...advanced_tracker import AdvancedTracker
from ...advanced_tracker.config import TrackerConfig
from ..base import BaseObjectTracker, DetectionDict
from ..config import MatriceTrackerConfig

# Constants
logger: Any

# Classes
class AdvancedTrackerAdapter:
    # Thin wrapper around ``AdvancedTracker`` with Matrice dict I/O.

    def __init__(self: Any, config: Any, namespace: Optional[str] = None) -> None: ...

    def reset(self: Any) -> None: ...

    def restore_state(self: Any) -> None: ...

    def save_state(self: Any) -> None: ...

    def update(self: Any, detections: List[Any], stream_info: Optional[Dict[str, Any]] = None) -> List[Any]: ...

