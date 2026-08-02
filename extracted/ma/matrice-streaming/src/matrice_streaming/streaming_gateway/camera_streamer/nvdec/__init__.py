"""NVDEC GPU decode path — hardware decode with CUDA IPC ring buffers.

NVDEC imports are optional and handled in camera_streamer/__init__.py
with graceful fallbacks when GPU dependencies are not available.

Re-export nvdec_pool_process at the package level so that
multiprocessing (spawn context) can find it when unpickling the
target function reference.
"""

try:
    from .nvdec import nvdec_pool_process  # noqa: F401

    __all__ = ["nvdec_pool_process"]
except (ImportError, AttributeError, RuntimeError, TypeError, ValueError):
    # GPU dependencies not available (CuPy, PyNvVideoCodec, etc.)
    __all__ = []
