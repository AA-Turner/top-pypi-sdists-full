"""Auto-generated stub for module: frame_processor."""
from typing import Any, Dict, Optional, Tuple

from __future__ import annotations
from frame_pool import GatewayFramePool
import cv2
import numpy as np

# Functions
def actual_dimensions(video_width: int, video_height: int, target_width: Optional[int], target_height: Optional[int]) -> Tuple[int, int]: ...
    """
    Return the output (width, height): the target if set, else the source size.
    """
def pool_exhausted_total() -> int: ...
def resize_frame(frame: Any, target_width: Optional[int], target_height: Optional[int]) -> Any: ...
    """
    Resize a frame with letterbox padding, preserving aspect ratio.
    
        Matches ultralytics LetterBox preprocessing: scale to fit within the target
        dimensions, then pad with gray (114) to reach the exact target size. Returns
        the original frame unchanged if no resize is needed.
    """
def set_use_frame_pool(enabled: bool) -> None: ...
    """
    Toggle pooled letterbox canvases (used by WorkerManager optimization modes).
    """
