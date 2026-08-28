"""Stub file for post_processing.Trackers.deep_oc_sort directory."""
from typing import Any, Dict, List, Optional

from ..advanced_tracker import AdvancedTrackerAdapter
from ..base import BaseObjectTracker, DetectionDict
from ..config import MatriceTrackerConfig

# Constants
logger: Any = ...  # From adapter

# Classes
# From adapter
class DeepOCSortAdapter:
    # Matrice wrapper for DeepOCSORT. Motion-only: always the in-repo
    #     ``AdvancedTracker`` (the historical ``boxmot`` ReID backend was removed
    #     for AGPL-3.0 licensing reasons -- see module docstring).

    def __init__(self: Any, config: Any, namespace: Optional[str] = None) -> None: ...

    def reset(self: Any) -> None: ...

    def restore_state(self: Any) -> None: ...

    def save_state(self: Any) -> None: ...

    def update(self: Any, detections: List[Any], stream_info: Optional[Dict[str, Any]] = None) -> List[Any]: ...


from . import adapter