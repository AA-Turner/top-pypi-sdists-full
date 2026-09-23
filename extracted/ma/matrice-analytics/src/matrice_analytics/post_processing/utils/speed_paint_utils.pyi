"""Auto-generated stub for module: speed_paint_utils."""
from typing import Any, List, Optional, Tuple

# Functions
def paint_mask(background: Any.Any, tophat: int = 35, tophat_thresh: int = 22, roi_top: float = 0.3, road: Optional[Any.Any] = None) -> Any.Any:
    """
    Thin, bright, white-or-yellow structure below the horizon.
    
        ``tophat`` must be wider than the widest marking and narrower than a lane: a kernel
        wider than a lane stops treating the lane as background, and the whole carriageway
        starts to respond.
    """
    ...
def road_mask_from_points(points: List[Tuple[float, float]], width: int, height: int, dilate: int = 25, box_px: int = 24) -> Any.Any:
    """
    Where vehicles have been seen is road. Cheap, and better than any colour rule.
    
        A sunlit tree is thin, bright and unsaturated in places, so it survives every colour
        test ever written. What it is not is a place cars drive. ``points`` are the ground
        contact points of tracked vehicles, in pixels.
    """
    ...
def segments_from_paint(mask: Any.Any, min_len: int = 30, max_gap: int = 4) -> Any.Any:
    """
    Straight segments along the edges of the painted regions.
    """
    ...
def split_by_vp1(segs: Any.Any, vp1: Any.Any, vp1_reject_deg: float = 12.0, vertical_reject_deg: float = 25.0) -> Tuple[Any.Any, Any.Any, int]:
    """
    Split paint segments into ``(transverse, along_road, n_vertical)``.
    
        The along-road family is RETURNED rather than discarded, because it is free and
        independent evidence about VP1: those markings converge where VP1 says they do, or
        one of the two is wrong.
    
        Near-vertical segments are dropped outright. They are the sides of kerbs, poles and
        sign posts; they belong to the vertical vanishing direction rather than to either
        road direction, and they are numerous enough to dominate a fit if left in.
    """
    ...
