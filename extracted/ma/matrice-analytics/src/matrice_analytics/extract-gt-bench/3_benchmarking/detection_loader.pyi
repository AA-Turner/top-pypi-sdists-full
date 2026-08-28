"""Auto-generated stub for module: detection_loader."""
from typing import Any, List, Optional

# Functions
def iou_xyxy(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    """
    Standard IoU of two ``[x1, y1, x2, y2]`` boxes.
    """
    ...
def iter_frames(detection_json: dict[str, Any]) -> Any:
    """
    Yield ``(frame_idx, processor_detections)`` in numeric frame order.
    """
    ...
def load_detection_json(path: str | Any) -> dict[str, Any]:
    """
    Load a detection JSON file and return the parsed dict unchanged.
    """
    ...
def match_frame_fp_fn(gt_dets: list[dict[str, Any]], pred_dets: list[dict[str, Any]], iou_threshold: float = 0.5) -> tuple[int, int, int]:
    """
    Greedy IoU matching for one frame.
    
        Returns:
            ``(true_positives, false_positives, false_negatives)``.
    """
    ...
def to_processor_detections(raw_frame_dets: list[dict[str, Any]], class_names: dict[str, str], width: int, height: int) -> list[dict[str, Any]]:
    """
    Convert one frame's raw detections to the processor input shape.
    
        Args:
            raw_frame_dets: List of detections from ``frames[<idx>]``.
            class_names: Mapping ``{"0": "person", ...}`` from the JSON header.
            width: Frame width in pixels (for denormalizing bbox).
            height: Frame height in pixels.
            target_classes: Optional whitelist of class names to keep (e.g. {"person"}).
                ``None`` keeps everything.
            confidence_threshold: Optional minimum confidence. ``None`` keeps everything.
    
        Returns:
            List of processor-shaped detection dicts.
    """
    ...
