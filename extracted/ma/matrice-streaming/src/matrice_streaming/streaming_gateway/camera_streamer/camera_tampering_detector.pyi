"""Auto-generated stub for module: camera_tampering_detector."""
from typing import Any, Dict, Optional

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
import cupy as cp
import logging
import numpy as np
import time

# Constants
TAMPERING_TYPES: Any
TAMPERING_TYPE_BLOCKED_LENS: str
TAMPERING_TYPE_CAMERA_MOVED: str
TAMPERING_TYPE_FOCUS_LOST: str
logger: Any

# Functions
def build_tampering_detector(config: Optional[Dict[str, Any]] = None) -> Any: ...
def emit_tampering_to_queue(queue: Any, event: Optional[TamperingEvent]) -> None: ...
    """
    Best-effort forward of a tampering event to a multiprocessing queue.
    """
def utc_now_rfc3339() -> str: ...

# Classes
class BlankScreenTamperingDetector(CameraTamperingDetector):
    """
    Detect cloth-covered lens, disconnect, or other uniform/blank frames.
    """

    def __init__(self: Any) -> None: ...

    def inspect(self: Any, camera_id: str, frame: Any) -> Optional[TamperingEvent]: ...

    def reset(self: Any, camera_id: str) -> None: ...

class CameraTamperingDetector(ABC):
    """
    Inspect decoded frames for tampering; stateful per ``camera_id``.
    """

    def inspect(self: Any, camera_id: str, frame: Any) -> Optional[TamperingEvent]: ...
        """
        Return a tampering event, or ``None`` if the frame looks normal.
        """

    def reset(self: Any, camera_id: str) -> None: ...
        """
        Drop per-camera state (stream reconnect/remove). Default no-op.
        """

class NoOpTamperingDetector(CameraTamperingDetector):
    def inspect(self: Any, camera_id: str, frame: Any) -> Optional[TamperingEvent]: ...

class TamperingEvent:
    def to_status_message(self: Any) -> Dict[str, str]: ...

