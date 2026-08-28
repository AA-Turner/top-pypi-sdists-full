"""Stub file for post_processing.Trackers.bytetrack directory."""
from typing import Any, Dict, List, Optional

from ...utils.bytetrack_utils import ByteTrackWrapper
from ..base import BaseObjectTracker, DetectionDict, ensure_track_id
from ..config import MatriceTrackerConfig

# Classes
# From adapter
class ByteTrackAdapter:
    # Wraps ``ByteTrackWrapper`` from ``bytetrack_utils`` (YOLOX BYTETracker).

    def __init__(self: Any, config: Any) -> None: ...

    def update(self: Any, detections: List[Any], stream_info: Optional[Dict[str, Any]] = None) -> List[Any]: ...


from . import adapter