"""Shared tracker protocol and helpers for Matrice post-processing."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

DetectionDict = Dict[str, Any]


class BaseObjectTracker(ABC):
    """Matrice-facing tracker API: List[Dict] in, same list + track_id out."""

    @abstractmethod
    def update(
        self,
        detections: List[DetectionDict],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[DetectionDict]:
        """Attach ``track_id`` to each detection dict."""

    def reset(self) -> None:
        """Reset internal tracker state."""

    def restore_state(self) -> None:
        """Restore persisted state if supported."""

    def save_state(self) -> None:
        """Persist tracker state if supported."""


def ensure_track_id(detections: List[DetectionDict]) -> List[DetectionDict]:
    """Set ``track_id`` to -1 when missing (SORT/ByteTrack convention)."""
    for det in detections:
        if isinstance(det, dict) and "track_id" not in det:
            det["track_id"] = -1
    return detections
