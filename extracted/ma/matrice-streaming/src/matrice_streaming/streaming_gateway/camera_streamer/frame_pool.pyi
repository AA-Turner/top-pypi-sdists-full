"""Auto-generated stub for module: frame_pool."""
from typing import Any, Optional, Tuple

from __future__ import annotations
from collections import deque
from contextlib import contextmanager
from threading import Lock
import numpy as np

# Classes
class GatewayFramePool:
    """
    Per-shape ring of reusable frame buffers.
    
        Eliminates per-frame ``np.empty`` / ``np.full`` allocation on the hot path.
    """

    def __init__(self: Any, resolution: Tuple[int, ...], pool_size: int = 4, dtype: Any = np.uint8) -> None: ...

    def free_count(self: Any) -> int: ...

    def lease(self: Any) -> Any: ...
        """
        Yield a buffer from the pool; return it on context exit.
        """

class PoolExhaustedError(RuntimeError):
    """
    Raised when no buffer is free in the pool.
    """

    pass
