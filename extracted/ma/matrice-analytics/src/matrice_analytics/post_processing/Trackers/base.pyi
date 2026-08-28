"""Auto-generated stub for module: base."""
from typing import Any, Dict, List, Optional, Set

# Constants
DetectionDict: Any

# Functions
def ensure_track_id(detections: List[Any]) -> List[Any]:
    """
    Set ``track_id`` to -1 when missing (SORT/ByteTrack convention).
    """
    ...

# Classes
class BaseObjectTracker:
    # Matrice-facing tracker API: List[Dict] in, same list + track_id out.

    def reset(self: Any) -> None:
        """
        Reset internal tracker state.
        """
        ...

    def restore_state(self: Any) -> None:
        """
        Restore persisted state if supported.
        """
        ...

    def save_state(self: Any) -> None:
        """
        Persist tracker state if supported.
        """
        ...

    def update(self: Any, detections: List[Any], stream_info: Optional[Dict[str, Any]] = None) -> List[Any]:
        """
        Attach ``track_id`` to each detection dict.
        """
        ...

