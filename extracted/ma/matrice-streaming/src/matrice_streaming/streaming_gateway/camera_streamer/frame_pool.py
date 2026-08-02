"""Per-camera reusable frame buffer pool for the OpenCV path."""

from __future__ import annotations

from collections import deque
from contextlib import contextmanager
from threading import Lock
from typing import Deque, Iterator, Optional, Tuple

import numpy as np


class PoolExhaustedError(RuntimeError):
    """Raised when no buffer is free in the pool."""


class GatewayFramePool:
    """Per-shape ring of reusable frame buffers.

    Eliminates per-frame ``np.empty`` / ``np.full`` allocation on the hot path.
    """

    def __init__(
        self,
        resolution: Tuple[int, ...],
        pool_size: int = 4,
        dtype: np.dtype = np.uint8,
    ):
        self.resolution = resolution
        self.pool_size = pool_size
        self.dtype = dtype
        self._free: Deque[np.ndarray] = deque(np.empty(resolution, dtype=dtype) for _ in range(pool_size))
        self._lock = Lock()
        self.pool_exhausted_total = 0

    @contextmanager
    def lease(self) -> Iterator[np.ndarray]:
        """Yield a buffer from the pool; return it on context exit."""
        buf: Optional[np.ndarray] = None
        with self._lock:
            if self._free:
                buf = self._free.popleft()
        if buf is None:
            self.pool_exhausted_total += 1
            buf = np.empty(self.resolution, dtype=self.dtype)
        try:
            yield buf
        finally:
            with self._lock:
                if len(self._free) < self.pool_size:
                    self._free.append(buf)

    @property
    def free_count(self) -> int:
        with self._lock:
            return len(self._free)
