"""Auto-generated stub for module: bytetrack_utils."""
from typing import Any, Dict, List, Optional, Tuple

# Functions
def bbox_centroid(bbox: Dict[str, Any]) -> Tuple[float, float]: ...
def bbox_feet_point(bbox: Dict[str, Any]) -> Tuple[float, float]: ...
def bbox_iou(a: Dict[str, Any], b: Dict[str, Any]) -> float: ...
def bbox_to_xyxy(bbox: Dict[str, Any]) -> Tuple[float, float, float, float]:
    """
    Supports both:
      - Matrice: xmin,ymin,xmax,ymax
      - Alternate: x1,y1,x2,y2
    """
    ...
def dist(a: Tuple[float, float], b: Tuple[float, float]) -> float: ...
def iou_xyxy(a: Any.Any, b: Any.Any) -> float: ...
def make_runtime_bytetrack_config() -> str:
    """
    Create a temporary runtime ByteTrack YAML config for Ultralytics YOLO.track().
    Returns:
        str: YAML path that can be passed into YOLO.track(tracker=...)
    """
    ...
def matrice_dets_to_xyxy_score(dets: List[Dict[str, Any]]) -> Any.Any: ...
def smooth_point(prev: Tuple[float, float], new: Tuple[float, float], alpha: float) -> Tuple[float, float]: ...
def ultralytics_track_to_matrice_dets(results: Any, person_class_id: int = 0) -> List[Dict[str, Any]]:
    """
    Convert ultralytics YOLO.track() output to Matrice detections list.
    
    Output schema:
    {
      "track_id": int,
      "confidence": float,
      "category": str (class id as string),
      "bounding_box": {"xmin","ymin","xmax","ymax"}
    }
    """
    ...
def validate_bytetrack_cfg(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate + sanitize an Ultralytics ByteTrack YAML config dict.
    
    Returns:
        A cleaned cfg dict (safe types + clamped thresholds).
    Raises:
        ValueError if mandatory keys are missing or invalid beyond repair.
    """
    ...

# Classes
class ByteTrackArgs:
    ...
class ByteTrackWrapper:
    # Wrapper around YOLOX BYTETracker.
    #
    # NOTE:
    # - This is NOT the same as ultralytics ByteTrack
    # - It assigns track_id to detections by IoU matching

    def __init__(self: Any, fps: float = 30.0, track_thresh: float = 0.25, match_thresh: float = 0.8, track_buffer: int = 30) -> None: ...

    def update(self: Any, dets: List[Dict[str, Any]], stream_info: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]: ...

class SORTTracker:
    def __init__(self: Any, iou_threshold: float = 0.25, max_age: int = 30, min_hits: int = 2) -> None: ...

    def update(self: Any, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]: ...

