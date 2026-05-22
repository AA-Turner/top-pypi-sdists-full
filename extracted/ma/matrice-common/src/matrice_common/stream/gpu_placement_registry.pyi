"""Auto-generated stub for module: gpu_placement_registry."""
from typing import Any, Dict, List, Optional

# Constants
MAP_SHARED: Any
PROT_READ: Any
PROT_WRITE: Any
SHM_BASE_PATH: Any
logger: Any

# Classes
class GpuPlacementRegistry:
    # SHM-backed registry of per-GPU cameras + apps + load.
    #
    #     Distinct from ``GpuCameraMap`` — that one persists the per-camera
    #     mapping. This one persists what's currently *resident* on each GPU.
    #
    #     Same atomicity discipline as ``GpuCameraMap``: every read-modify-write
    #     is wrapped in an exclusive ``fcntl.flock`` on the fd.

    def __init__(self: Any) -> None: ...

    MAX_SIZE: Any
    SHM_PATH: Any

    def close(self: Any) -> None: ...

    def connect(self: Any) -> bool:
        """
        Open an existing SHM file read/write. Returns False if missing.
        """
        ...

    def initialize(self: Any, num_gpus: int) -> bool:
        """
        Open or create the SHM file, ensuring an entry exists for each GPU.
        
                Idempotent: existing file is preserved (cameras/apps survive
                producer restarts); only missing GPU ids get populated with empty
                state. Safe to call on every SG startup.
        """
        ...

    def remove_app_from_all(self: Any, deployment_id: str) -> None:
        """
        Remove a deployment_id from every GPU's ``apps[]``.
        
                Used by IE startup to clean stale entries from a prior crash before
                re-registering, and by the SG stale-sweep loop to evict dead IEs.
        """
        ...

    def replace_cameras_for_gpus(self: Any, by_gpu: Dict[int, List[str]], load_by_gpu: Optional[Dict[int, float]] = None) -> None:
        """
        Replace the ``cameras[]`` list (and optionally ``load``) for the
                given GPUs, leaving other GPUs and the ``apps[]`` lists untouched.
        
                Used by the SG on startup to seed the registry from the authoritative
                ``GpuCameraMap`` (single source of truth for camera->GPU placement).
        """
        ...

    def snapshot(self: Any) -> Dict[int, Any]:
        """
        Read the whole registry under a shared lock.
        """
        ...

    def update_apps(self: Any, gpu_id: int, add: Optional[Any[str]] = None, remove: Optional[Any[str]] = None) -> None:
        """
        Atomically add/remove app (deployment) entries on one GPU.
        """
        ...

    def update_cameras(self: Any, gpu_id: int, add: Optional[Any[str]] = None, remove: Optional[Any[str]] = None, load_delta: float = 0.0) -> None:
        """
        Atomically add/remove cameras and apply a load delta on one GPU.
        """
        ...

class GpuState:
    # Per-GPU state snapshot.

    def empty(cls: Any) -> 'Any': ...

    def from_dict(cls: Any, d: dict) -> 'Any': ...

    def to_dict(self: Any) -> dict: ...

