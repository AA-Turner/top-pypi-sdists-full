"""Auto-generated stub for module: fence_climbing_detection_pose."""
from typing import Any, Dict, List, Optional, Tuple

from ..utils.geometry_utils import get_bbox_bottom25_center, get_bbox_center, point_in_polygon
from .fence_climbing_detection import FenceClimbingDetectionConfig, FenceClimbingDetectionUseCase

# Functions
def hands_raised_above_head(detection: Dict[str, Any], kp_conf_thresh: float, margin_px: float, require_both_wrists: bool) -> Tuple[bool, Optional[float], Optional[float]]:
    """
    In image coords (y downward), wrists must sit above facial keypoints:
    
        wrist_y < head_ref_y - margin_px
    
    head_ref_y is the minimum y among visible nose / eyes / ears (highest visible
    facial landmark in frame).
    
    Returns (passed, head_ref_y, best_wrist_y) for telemetry; refs may be None if no pass.
    """
    ...

# Classes
class FenceClimbingPoseGatedDetectionConfig:
    # Adds pose gating thresholds on top of `FenceClimbingDetectionConfig`.

    def validate(self: Any) -> List[str]: ...

class FenceClimbingPoseGatedDetectionUseCase:
    # Fence climbing use case requiring raised hands above head from pose keypoints.

    def __init__(self: Any) -> None: ...

    def create_default_config(self: Any, **overrides: Any) -> Any: ...

    def get_config_schema(self: Any) -> Dict[str, Any]: ...

