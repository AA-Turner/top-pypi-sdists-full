"""Auto-generated stub for module: frame_optimizer."""
from typing import Any, Dict, Optional, Set

from __future__ import annotations
from abc import ABC, abstractmethod
import cupy as cp
import logging

# Constants
logger: Any

# Functions
def build_frame_optimizer(config: Optional[Dict[str, Any]] = None) -> Any: ...
    """
    Construct a :class:`FrameOptimizer` from a config dict.
    
        Returns :class:`NoOpFrameOptimizer` by default. Set ``config["optimizer"]`` to
        select a skip policy; unknown names log a warning and fall back to no-op.
    """

# Classes
class FrameOptimizer(ABC):
    """
    Decide, per camera, whether a decoded frame should be published.
    
        Implementations are stateful per ``camera_id`` (the same instance is shared
        across all cameras a worker owns). Subclass this to add a skip policy.
    """

    def optimize(self: Any, camera_id: str, frame: Any) -> Optional[Any]: ...
        """
        Return the frame to publish, or ``None`` to drop it.
        """

    def reset(self: Any, camera_id: str) -> None: ...
        """
        Drop per-camera state (called on stream reconnect/remove). Default no-op.
        """

class MotionFrameOptimizer(FrameOptimizer):
    """
    GPU motion gate for NVDEC NV12 frames using downsampled Y-plane SSIM.
    
        Compares each frame to the last *published* reference for ``camera_id``. Frames
        whose motion score ``1 - SSIM`` falls below ``threshold`` are dropped. The metric
        runs entirely on-GPU (downsampled luma thumbnails only); non-CuPy frames (OpenCV
        BGR) pass through unchanged.
    """

    def __init__(self: Any, threshold: float = 0.02, thumb_height: int = 64, thumb_width: int = 64) -> None: ...

    def optimize(self: Any, camera_id: str, frame: Any) -> Optional[Any]: ...

    def reset(self: Any, camera_id: str) -> None: ...

class NoOpFrameOptimizer(FrameOptimizer):
    """
    Default optimizer: never drops a frame — every frame passes through.
    """

    def optimize(self: Any, camera_id: str, frame: Any) -> Optional[Any]: ...

