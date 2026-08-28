"""Auto-generated stub for module: det_utils."""
from typing import Any, Dict, List, Optional, Tuple

from ..utils.bytetrack_utils import bbox_to_xyxy, iou_xyxy

# Functions
def assign_track_ids_by_iou(detections: List[Dict[str, Any]], track_boxes: List[Tuple[Any.Any, int]], min_iou: float = 0.1) -> List[Dict[str, Any]]:
    """
    Map tracker output boxes onto input detections via IoU.
    
        F10b S12 (consolidation-plan.md Step 12): this package's own in-package copy of
        the IoU remap, kept for ``deep_oc_sort`` (its only caller, `Trackers/deep_oc_sort/
        adapter.py`) rather than unified away -- ``py_inference`` is the only place the
        plan designates a canonical shared implementation for. ``min_iou=0.10`` is
        **inclusive** (``>=``, not ``>``): a detection/track pair at exactly the boundary
        IoU counts as a match. This differs from two of the plan's other five IoU-remap
        sites, which gate on strict ``>`` -- picking ``>=`` here is a deliberate, called-out
        semantics choice (consolidation-plan.md §1.12), not an oversight.
    """
    ...
def frame_from_stream(stream_info: Optional[Dict[str, Any]]) -> Any:
    """
    Return a BGR frame array from ``stream_info`` when present.
    """
    ...
def stream_resolution(stream_info: Optional[Dict[str, Any]]) -> Tuple[int, int]:
    """
    Return ``(height, width)`` from stream_info; default ``(480, 640)``.
    """
    ...
