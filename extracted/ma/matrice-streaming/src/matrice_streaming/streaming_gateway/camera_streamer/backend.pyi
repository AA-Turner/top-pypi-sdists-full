"""Auto-generated stub for module: backend."""
from typing import Any, Dict

from __future__ import annotations

# Classes
class CameraBackend(Protocol):
    """
    Six-method interface used by DynamicCameraManager.
    
        Any object that implements all six methods is automatically considered
        a valid CameraBackend via structural subtyping (runtime_checkable Protocol).
    """

    def add_camera(self: Any, camera_config: Dict[str, Any]) -> bool: ...
        """
        Add a camera to the backend worker pool. Returns True on success.
        """

    def get_camera_assignments(self: Any) -> Dict[str, int]: ...
        """
        Return mapping of camera_id → worker/GPU index.
        """

    def get_worker_statistics(self: Any) -> Dict[str, Any]: ...
        """
        Return per-camera / per-worker statistics snapshot.
        """

    def is_running(self: Any) -> bool: ...
        """
        Return True if the backend is actively processing frames.
        """

    def remove_camera(self: Any, stream_key: str) -> bool: ...
        """
        Remove a camera by stream key. Returns True on success.
        """

    def update_camera(self: Any, camera_config: Dict[str, Any]) -> bool: ...
        """
        Update camera config in the backend. Returns True on success.
        """

