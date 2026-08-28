"""JSON → processor-detection-shape adapter for the BV evaluators.

Kept separate from the evaluators so it can be edited when the on-disk JSON
schema changes without touching the metric logic.

Expected on-disk JSON shape (per ``retail_tracked_person_c25.json``)::

    {
      "video": "...",
      "width": 1270,
      "height": 720,
      "fps": 13.093,
      "class_names": {"0": "person", "1": "bicycle", ...},
      "frames": {
        "0": [
          {
            "class_id": 0,
            "confidence": 0.83,
            "bbox": [x1, y1, x2, y2],   # normalized 0..1
            "track_id": 17               # optional; required for unique counts
          },
          ...
        ],
        ...
      }
    }

Processor-detection shape (per ``base_processor._pre_process``)::

    {
      "category": "person",                  # entity name from entity_mapping
      "bounding_box": {"xmin", "ymin", "xmax", "ymax"},  # pixel coords
      "confidence": float,
      "track_id": int | None,
    }
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_detection_json(path: str | Path) -> dict[str, Any]:
    """Load a detection JSON file and return the parsed dict unchanged."""
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def to_processor_detections(
    raw_frame_dets: list[dict[str, Any]],
    class_names: dict[str, str],
    width: int,
    height: int,
    *,
    target_classes: set[str] | None = None,
    confidence_threshold: float | None = None,
) -> list[dict[str, Any]]:
    """Convert one frame's raw detections to the processor input shape.

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
    out: list[dict[str, Any]] = []
    for det in raw_frame_dets:
        cls_id = det.get("class_id")
        cls_name = class_names.get(str(cls_id), str(cls_id))

        if target_classes is not None and cls_name not in target_classes:
            continue

        conf = float(det.get("confidence", 1.0))
        if confidence_threshold is not None and conf < confidence_threshold:
            continue

        bbox = det.get("bbox") or det.get("bounding_box")
        xyxy_px = _bbox_to_pixel_xyxy(bbox, width, height)
        if xyxy_px is None:
            continue
        x1, y1, x2, y2 = xyxy_px

        out.append(
            {
                "category": cls_name,
                "bounding_box": {"xmin": x1, "ymin": y1, "xmax": x2, "ymax": y2},
                "confidence": conf,
                "track_id": det.get("track_id"),
            }
        )
    return out


def iter_frames(
    detection_json: dict[str, Any],
    *,
    target_classes: set[str] | None = None,
    confidence_threshold: float | None = None,
):
    """Yield ``(frame_idx, processor_detections)`` in numeric frame order."""
    class_names = detection_json.get("class_names", {})
    width = int(detection_json.get("width", 0))
    height = int(detection_json.get("height", 0))
    frames = detection_json.get("frames", {})

    for key in sorted(frames.keys(), key=lambda k: int(k)):
        dets = to_processor_detections(
            frames[key],
            class_names=class_names,
            width=width,
            height=height,
            target_classes=target_classes,
            confidence_threshold=confidence_threshold,
        )
        yield int(key), dets


# ---------------------------------------------------------------------------
# Bbox / matching helpers (also used by the evaluators for FP/FN)
# ---------------------------------------------------------------------------


def _bbox_to_pixel_xyxy(
    bbox: Any, width: int, height: int
) -> tuple[float, float, float, float] | None:
    """Normalize a bbox in any of the supported on-disk shapes to pixel xyxy."""
    if bbox is None:
        return None
    if isinstance(bbox, list) and len(bbox) >= 4:
        x1, y1, x2, y2 = bbox[:4]
    elif isinstance(bbox, dict):
        if "x1" in bbox:
            x1, y1, x2, y2 = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]
        elif "xmin" in bbox:
            x1, y1, x2, y2 = bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]
        else:
            vals = list(bbox.values())
            if len(vals) < 4:
                return None
            x1, y1, x2, y2 = vals[:4]
    else:
        return None

    # If max coord is <= 1.0001, treat as normalized → denormalize.
    if max(x1, y1, x2, y2) <= 1.0001:
        x1 *= width
        x2 *= width
        y1 *= height
        y2 *= height
    return float(x1), float(y1), float(x2), float(y2)


def iou_xyxy(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    """Standard IoU of two ``[x1, y1, x2, y2]`` boxes."""
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)
    iw = max(0.0, ix2 - ix1)
    ih = max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0.0:
        return 0.0
    area_a = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    area_b = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = area_a + area_b - inter
    return inter / union if union > 0 else 0.0


def match_frame_fp_fn(
    gt_dets: list[dict[str, Any]],
    pred_dets: list[dict[str, Any]],
    iou_threshold: float = 0.5,
) -> tuple[int, int, int]:
    """Greedy IoU matching for one frame.

    Returns:
        ``(true_positives, false_positives, false_negatives)``.
    """
    gt_boxes = [_extract_xyxy(d) for d in gt_dets]
    pred_boxes = [_extract_xyxy(d) for d in pred_dets]

    pred_order = sorted(
        range(len(pred_dets)),
        key=lambda i: float(pred_dets[i].get("confidence", 1.0)),
        reverse=True,
    )
    gt_matched = [False] * len(gt_dets)
    tp = 0

    for pi in pred_order:
        pb = pred_boxes[pi]
        if pb is None:
            continue
        best_iou = 0.0
        best_gi = -1
        for gi, gb in enumerate(gt_boxes):
            if gt_matched[gi] or gb is None:
                continue
            v = iou_xyxy(pb, gb)
            if v > best_iou:
                best_iou = v
                best_gi = gi
        if best_gi >= 0 and best_iou >= iou_threshold:
            gt_matched[best_gi] = True
            tp += 1

    fp = len(pred_dets) - tp
    fn = sum(1 for m in gt_matched if not m)
    return tp, fp, fn


def _extract_xyxy(det: dict[str, Any]) -> tuple[float, float, float, float] | None:
    """Pull pixel xyxy out of a processor-shaped detection."""
    bb = det.get("bounding_box") or det.get("bbox")
    if isinstance(bb, dict):
        return (
            float(bb.get("xmin", bb.get("x1", 0.0))),
            float(bb.get("ymin", bb.get("y1", 0.0))),
            float(bb.get("xmax", bb.get("x2", 0.0))),
            float(bb.get("ymax", bb.get("y2", 0.0))),
        )
    if isinstance(bb, list) and len(bb) >= 4:
        return float(bb[0]), float(bb[1]), float(bb[2]), float(bb[3])
    return None
