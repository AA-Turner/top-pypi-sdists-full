"""Pluggable per-camera frame-skip optimization.

A camera_streamer worker calls ``optimizer.optimize(camera_id, frame)`` for every
decoded frame; the optimizer returns the frame to publish or ``None`` to drop it.
This is the single seam where frame-filtering policy lives — the same call is used
by both the OpenCV and NVDEC decode loops — so the loops stay free of skip logic and
future content-based algorithms can be added without touching the workers.

The shipped default, :class:`NoOpFrameOptimizer`, never drops a frame (every frame
passes). To add a real skip policy, subclass :class:`FrameOptimizer`, implement
``optimize`` (and optionally ``reset``), and select it from :func:`build_frame_optimizer`::

    optimizer_config={"optimizer": "motion", "threshold": 0.02}

The optimizer is frame-type-agnostic: OpenCV passes a BGR numpy array and NVDEC passes
a GPU CuPy NV12 tensor — the base/no-op never inspects pixels, and content-aware
subclasses do their own dtype handling.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

try:
    import cupy as cp

    _CUPY_AVAILABLE = True
except ImportError:
    cp = None  # type: ignore[assignment,misc]
    _CUPY_AVAILABLE = False


class FrameOptimizer(ABC):
    """Decide, per camera, whether a decoded frame should be published.

    Implementations are stateful per ``camera_id`` (the same instance is shared
    across all cameras a worker owns). Subclass this to add a skip policy.
    """

    @abstractmethod
    def optimize(self, camera_id: str, frame: Any) -> Optional[Any]:
        """Return the frame to publish, or ``None`` to drop it."""

    def reset(self, camera_id: str) -> None:
        """Drop per-camera state (called on stream reconnect/remove). Default no-op."""


class NoOpFrameOptimizer(FrameOptimizer):
    """Default optimizer: never drops a frame — every frame passes through."""

    def optimize(self, camera_id: str, frame: Any) -> Optional[Any]:
        return frame


def _is_cupy_array(frame: Any) -> bool:
    return _CUPY_AVAILABLE and hasattr(frame, "__cuda_array_interface__")


def _nv12_luma_height(total_h: int) -> int:
    return (total_h * 2) // 3


def _extract_nv12_y(frame: Any) -> Any:
    """Return the Y (luma) plane view from an NV12 CuPy tensor ``(H*1.5, W, 1)``."""
    total_h = int(frame.shape[0])
    width = int(frame.shape[1])
    luma_h = _nv12_luma_height(total_h)
    if frame.ndim == 3:
        return frame[:luma_h, :width, 0]
    return frame[:luma_h, :width]


def _downsample_y(y: Any, out_h: int, out_w: int) -> Any:
    """Stride-downsample a Y plane on GPU to ``(out_h, out_w)`` float32 in [0, 1]."""
    h, w = int(y.shape[0]), int(y.shape[1])
    sy = max(1, h // out_h)
    sx = max(1, w // out_w)
    small = y[::sy, ::sx][:out_h, :out_w]
    return small.astype(cp.float32) / 255.0  # type: ignore[union-attr]


def _ssim_mean(a: Any, b: Any) -> float:
    """Mean SSIM between two same-shape float32 GPU arrays in [0, 1]."""
    c1 = 0.01**2
    c2 = 0.03**2
    mu_a = cp.mean(a)  # type: ignore[union-attr]
    mu_b = cp.mean(b)  # type: ignore[union-attr]
    var_a = cp.var(a)  # type: ignore[union-attr]
    var_b = cp.var(b)  # type: ignore[union-attr]
    cov = cp.mean((a - mu_a) * (b - mu_b))  # type: ignore[union-attr]
    num = (2 * mu_a * mu_b + c1) * (2 * cov + c2)
    den = (mu_a * mu_a + mu_b * mu_b + c1) * (var_a + var_b + c2)
    return float(num / den)


class MotionFrameOptimizer(FrameOptimizer):
    """GPU motion gate for NVDEC NV12 frames using downsampled Y-plane SSIM.

    Compares each frame to the last *published* reference for ``camera_id``. Frames
    whose motion score ``1 - SSIM`` falls below ``threshold`` are dropped. The metric
    runs entirely on-GPU (downsampled luma thumbnails only); non-CuPy frames (OpenCV
    BGR) pass through unchanged.
    """

    def __init__(
        self,
        threshold: float = 0.02,
        thumb_height: int = 64,
        thumb_width: int = 64,
    ):
        self.threshold = threshold
        self.thumb_height = thumb_height
        self.thumb_width = thumb_width
        self._prev: Dict[str, Any] = {}
        if not _CUPY_AVAILABLE:
            logger.warning("MotionFrameOptimizer: cupy unavailable; NV12 motion skipping disabled")

    def optimize(self, camera_id: str, frame: Any) -> Optional[Any]:
        if not _is_cupy_array(frame):
            return frame

        thumb = _downsample_y(_extract_nv12_y(frame), self.thumb_height, self.thumb_width)
        prev = self._prev.get(camera_id)
        if prev is not None:
            ssim = _ssim_mean(prev, thumb)
            motion_score = 1.0 - ssim
            if motion_score < self.threshold:
                return None

        self._prev[camera_id] = thumb
        return frame

    def reset(self, camera_id: str) -> None:
        self._prev.pop(camera_id, None)


def build_frame_optimizer(config: Optional[Dict[str, Any]] = None) -> FrameOptimizer:
    """Construct a :class:`FrameOptimizer` from a config dict.

    Returns :class:`NoOpFrameOptimizer` by default. Set ``config["optimizer"]`` to
    select a skip policy; unknown names log a warning and fall back to no-op.
    """
    config = config or {}
    name = str(config.get("optimizer", "")).strip().lower()
    if name == "motion":
        return MotionFrameOptimizer(
            threshold=float(config.get("threshold", 0.02)),
            thumb_height=int(config.get("thumb_height", 64)),
            thumb_width=int(config.get("thumb_width", 64)),
        )
    if name not in ("", "none", "noop", "no-op"):
        logger.warning("Unknown frame optimizer %r; falling back to no-op", name)
    return NoOpFrameOptimizer()
