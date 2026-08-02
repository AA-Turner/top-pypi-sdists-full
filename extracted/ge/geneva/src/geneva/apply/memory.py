# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import ctypes
import gc
import logging
import os
import sys

import pyarrow as pa

_LOG = logging.getLogger(__name__)

APPLIER_MEMORY_TRIM_INTERVAL_ENV = "GENEVA_APPLIER_MEMORY_TRIM_INTERVAL"
DEFAULT_APPLIER_MEMORY_TRIM_INTERVAL = 8


def get_applier_memory_trim_interval() -> int:
    raw = os.environ.get(APPLIER_MEMORY_TRIM_INTERVAL_ENV)
    if raw is None:
        return DEFAULT_APPLIER_MEMORY_TRIM_INTERVAL
    try:
        return max(0, int(raw))
    except ValueError:
        _LOG.warning(
            "Invalid %s=%r; using default interval %d",
            APPLIER_MEMORY_TRIM_INTERVAL_ENV,
            raw,
            DEFAULT_APPLIER_MEMORY_TRIM_INTERVAL,
        )
        return DEFAULT_APPLIER_MEMORY_TRIM_INTERVAL


def release_unused_process_memory() -> None:
    """Best-effort allocator cleanup after large batch buffers are released."""
    # Variable-sized UDF buffers can leave free pages stranded in allocator
    # arenas even after the live Python/Arrow objects are gone. Arrow buffers
    # may sit in PyArrow's memory pool, while PIL/numpy/OpenCV-style decode
    # buffers usually go through libc malloc. Periodically releasing both pools
    # can lower RSS and avoid slow cgroup OOMs, but malloc_trim may walk large
    # fragmented arenas, so callers should run this every N batches rather than
    # after every batch.
    try:
        gc.collect()
    except Exception:
        _LOG.debug("Failed to collect Python garbage", exc_info=True)

    try:
        pa.default_memory_pool().release_unused()
    except Exception:
        _LOG.debug("Failed to release unused PyArrow memory", exc_info=True)

    if not sys.platform.startswith("linux"):
        return

    try:
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)
    except Exception:
        _LOG.debug("Failed to trim libc malloc arenas", exc_info=True)
