"""Frame processing helpers (resize + dimension math)."""

from __future__ import annotations

from typing import Dict, Optional, Tuple

import cv2
import numpy as np

from ..frame_pool import GatewayFramePool

_pools: Dict[Tuple[int, int, int, int], GatewayFramePool] = {}
_use_frame_pool = True


def set_use_frame_pool(enabled: bool) -> None:
    """Toggle pooled letterbox canvases (used by WorkerManager optimization modes)."""
    global _use_frame_pool
    _use_frame_pool = enabled


def pool_exhausted_total() -> int:
    return sum(p.pool_exhausted_total for p in _pools.values())


def _pool_for_shape(final_h: int, final_w: int, channels: int) -> GatewayFramePool:
    key = (final_h, final_w, channels, np.uint8.itemsize)
    if key not in _pools:
        _pools[key] = GatewayFramePool((final_h, final_w, channels), pool_size=4)
    return _pools[key]


def resize_frame(frame: np.ndarray, target_width: Optional[int], target_height: Optional[int]) -> np.ndarray:
    """Resize a frame with letterbox padding, preserving aspect ratio.

    Matches ultralytics LetterBox preprocessing: scale to fit within the target
    dimensions, then pad with gray (114) to reach the exact target size. Returns
    the original frame unchanged if no resize is needed.
    """
    if not target_width and not target_height:
        return frame

    src = np.asarray(frame)
    current_h, current_w = src.shape[:2]
    final_w = target_width if target_width else current_w
    final_h = target_height if target_height else current_h

    if final_w == current_w and final_h == current_h:
        return src

    r = min(final_w / current_w, final_h / current_h)
    new_w = int(round(current_w * r))
    new_h = int(round(current_h * r))

    resized = cv2.resize(src, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    pad_top = int(round((final_h - new_h) / 2 - 0.1))
    pad_left = int(round((final_w - new_w) / 2 - 0.1))
    pad_color = (114, 114, 114) if src.ndim == 3 else 114

    if not _use_frame_pool:
        canvas = np.full((final_h, final_w) + src.shape[2:], pad_color, dtype=src.dtype)
        canvas[pad_top : pad_top + new_h, pad_left : pad_left + new_w] = resized
        return canvas

    channels = src.shape[2] if src.ndim == 3 else 1
    pool = _pool_for_shape(final_h, final_w, channels)
    with pool.lease() as canvas:
        if src.ndim == 3:
            canvas[:] = pad_color
        else:
            canvas.fill(pad_color)
        canvas[pad_top : pad_top + new_h, pad_left : pad_left + new_w] = resized
        return canvas.copy()


def actual_dimensions(
    video_width: int,
    video_height: int,
    target_width: Optional[int],
    target_height: Optional[int],
) -> Tuple[int, int]:
    """Return the output (width, height): the target if set, else the source size."""
    return (
        target_width if target_width else video_width,
        target_height if target_height else video_height,
    )
