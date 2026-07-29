"""Process lifecycle, CUDA teardown, SHM cleanup, and gated drop_caches helpers.

These primitives let services run a *standardized* shutdown sequence on atexit
and on SIGTERM/SIGINT, so GPU-driver pages tied to inode references (TensorRT
engines, CUDA IPC ring buffers, NVDEC dmabufs) are released proactively at
process exit. The motivating bug class: on Jetson Thor unified memory, those
pages otherwise sit reclaimable-but-unfreed until ``drop_caches`` is run.
"""

from .cuda_finalize import finalize_cuda
from .drop_caches import drop_caches
from .process_lifecycle import register_shutdown, run_shutdown_now
from .shm_cleanup import cleanup_owned_shm, safe_unlink_if_owner

__all__ = [
    "register_shutdown",
    "run_shutdown_now",
    "finalize_cuda",
    "cleanup_owned_shm",
    "safe_unlink_if_owner",
    "drop_caches",
]
