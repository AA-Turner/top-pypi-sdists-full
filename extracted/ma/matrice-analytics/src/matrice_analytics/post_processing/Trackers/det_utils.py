"""Shared detection conversion helpers for tracker adapters."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..utils.bytetrack_utils import bbox_to_xyxy, iou_xyxy


def frame_from_stream(stream_info: Optional[Dict[str, Any]]):
    """Return a BGR frame array from ``stream_info`` when present."""
    if not stream_info:
        return None
    frame = stream_info.get("frame")
    if frame is not None:
        return frame
    nested = stream_info.get("input_settings", {})
    if isinstance(nested, dict):
        return nested.get("frame")
    return None


def stream_resolution(stream_info: Optional[Dict[str, Any]]) -> Tuple[int, int]:
    """Return ``(height, width)`` from stream_info; default ``(480, 640)``."""
    try:
        if stream_info:
            res = stream_info.get("input_settings", {}).get("stream_resolution")
            if isinstance(res, (list, tuple)) and len(res) == 2:
                w, h = int(res[0]), int(res[1])
                if w > 0 and h > 0:
                    return h, w
    except Exception:
        pass
    return 480, 640


def assign_track_ids_by_iou(
    detections: List[Dict[str, Any]],
    track_boxes: List[Tuple[np.ndarray, int]],
    min_iou: float = 0.10,
) -> List[Dict[str, Any]]:
    """Map tracker output boxes onto input detections via IoU.

    F10b S12 (consolidation-plan.md Step 12): this package's own in-package copy of
    the IoU remap, kept for ``deep_oc_sort`` (its only caller, `Trackers/deep_oc_sort/
    adapter.py`) rather than unified away -- ``py_inference`` is the only place the
    plan designates a canonical shared implementation for. ``min_iou=0.10`` is
    **inclusive** (``>=``, not ``>``): a detection/track pair at exactly the boundary
    IoU counts as a match. This differs from two of the plan's other five IoU-remap
    sites, which gate on strict ``>`` -- picking ``>=`` here is a deliberate, called-out
    semantics choice (consolidation-plan.md §1.12), not an oversight.
    """
    for det in detections:
        bb = det.get("bounding_box") or det.get("bbox") or {}
        x1, y1, x2, y2 = bbox_to_xyxy(bb)
        det_box = np.array([x1, y1, x2, y2], dtype=np.float32)

        best_iou, best_tid = 0.0, -1
        for trk_box, tid in track_boxes:
            iou = iou_xyxy(det_box, trk_box)
            if iou > best_iou:
                best_iou = iou
                best_tid = tid

        det["track_id"] = int(best_tid) if best_iou >= min_iou else -1

    return detections
