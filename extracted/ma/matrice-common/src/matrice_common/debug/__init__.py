"""matrice_common.debug — host-side per-camera streaming debugger.

Read-only host-side helper that auto-discovers running matrice containers,
calls the backend with their credentials, inspects ``/dev/shm`` (and
optionally Redis), and emits a per-camera correlated health report.

Designed to be used either as a CLI::

    python -m matrice_common.debug status
    python -m matrice_common.debug camera <camera_id>

or programmatically::

    from matrice_common.debug import main, collect_state, correlate, CameraReport
    main(["status", "--json"])
"""

from .cli import (
    CameraReport,
    cmd_camera,
    cmd_cameras,
    cmd_containers,
    cmd_gpu_map,
    cmd_shm,
    cmd_status,
    collect_state,
    correlate,
    main,
)

__all__ = [
    "CameraReport",
    "cmd_camera",
    "cmd_cameras",
    "cmd_containers",
    "cmd_gpu_map",
    "cmd_shm",
    "cmd_status",
    "collect_state",
    "correlate",
    "main",
]
