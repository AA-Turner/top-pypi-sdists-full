"""Auto-generated stub for module: adapter."""
from typing import Any, Dict, List, Optional

from ...utils.bytetrack_utils import SORTTracker
from ...utils.bytetrack_utils import SORTTracker
from ..base import BaseObjectTracker, DetectionDict, ensure_track_id
from ..config import MatriceTrackerConfig

# Classes
class SORTTrackerAdapter:
    # Wraps in-repo ``SORTTracker`` from ``bytetrack_utils``.

    def __init__(self: Any, config: Any) -> None: ...

    def reset(self: Any) -> None: ...

    def update(self: Any, detections: List[Any], stream_info: Optional[Dict[str, Any]] = None) -> List[Any]: ...

