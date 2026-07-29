"""Standardized CUDA / TensorRT teardown sequence.

The motivating bug: on Jetson Thor (and other iGPU/unified-memory NVIDIA
platforms), GPU-driver allocations come from system RAM but stay tied to
inode references after process exit until ``drop_caches=2`` runs. Calling
this sequence *before* the process exits causes the driver to release its
dmabufs proactively, so the kernel sees the pages as free immediately.

Canonical order (each step wrapped so a single failure doesn't skip the rest):

1. Synchronize provided streams + the default stream.
2. Drop TensorRT execution contexts (``del`` references).
3. Drop the engine and runtime references.
4. Free CuPy default + pinned memory pools' blocks back to the driver.
5. Optional ``cudaDeviceReset`` (only safe when the caller owns the entire
   primary context; off by default).

All arguments are optional — call sites pass whatever they hold.
"""

from __future__ import annotations

import logging
from typing import Iterable, Optional

logger = logging.getLogger(__name__)


def finalize_cuda(
    *,
    streams: Optional[Iterable] = None,
    contexts: Optional[Iterable] = None,
    engines: Optional[Iterable] = None,
    runtime: Optional[object] = None,
    device_id: Optional[int] = None,
    reset: bool = False,
) -> None:
    """Run the canonical CUDA teardown sequence; never raises."""
    _step("synchronize_streams", _synchronize_streams, streams, device_id)
    _step("drop_contexts", _drop_iterable, contexts)
    _step("drop_engines", _drop_iterable, engines)
    _step("drop_runtime", _drop_one, runtime)
    _step("free_default_pool", _free_default_pool)
    _step("free_pinned_pool", _free_pinned_pool)
    if reset:
        _step("device_reset", _device_reset, device_id)


# --- internals ---------------------------------------------------------------


def _step(name: str, fn, *args) -> None:
    try:
        fn(*args)
    except Exception:  # noqa: BLE001
        logger.debug("finalize_cuda step %s failed", name, exc_info=True)


def _import_cupy():
    try:
        import cupy  # type: ignore

        return cupy
    except Exception:  # noqa: BLE001
        return None


def _synchronize_streams(streams, device_id) -> None:
    cp = _import_cupy()
    if cp is None:
        return
    if device_id is not None:
        try:
            cp.cuda.Device(device_id).synchronize()
        except Exception:  # noqa: BLE001
            logger.debug("device synchronize failed", exc_info=True)
    if not streams:
        return
    for stream in list(streams):
        try:
            sync = getattr(stream, "synchronize", None)
            if callable(sync):
                sync()
        except Exception:  # noqa: BLE001
            logger.debug("stream synchronize failed", exc_info=True)


def _drop_iterable(items) -> None:
    if not items:
        return
    # Iterate over a snapshot so callers can safely pass attributes that we'll
    # clear later. Each ``del`` is best-effort — Python's GC will reclaim the
    # underlying CUDA objects when the last reference goes away.
    for item in list(items):
        try:
            del item
        except Exception:  # noqa: BLE001
            pass


def _drop_one(obj) -> None:
    if obj is None:
        return
    try:
        del obj
    except Exception:  # noqa: BLE001
        pass


def _free_default_pool() -> None:
    cp = _import_cupy()
    if cp is None:
        return
    try:
        cp.get_default_memory_pool().free_all_blocks()
    except Exception:  # noqa: BLE001
        logger.debug("default mempool free_all_blocks failed", exc_info=True)


def _free_pinned_pool() -> None:
    cp = _import_cupy()
    if cp is None:
        return
    try:
        cp.get_default_pinned_memory_pool().free_all_blocks()
    except Exception:  # noqa: BLE001
        logger.debug("pinned mempool free_all_blocks failed", exc_info=True)


def _device_reset(device_id) -> None:
    cp = _import_cupy()
    if cp is None:
        return
    try:
        if device_id is not None:
            cp.cuda.Device(device_id).use()
        cp.cuda.runtime.deviceReset()
    except Exception:  # noqa: BLE001
        logger.debug("cudaDeviceReset failed", exc_info=True)
