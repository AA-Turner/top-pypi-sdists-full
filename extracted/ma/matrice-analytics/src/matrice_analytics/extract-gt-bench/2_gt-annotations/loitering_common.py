"""Shared constants and JSON helpers for loitering-detection ground truth."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

# YOLO (people-counting model) only ever detects class 0 -> "person".
# class 1 -> "loitering_person" is assigned by LoiteringUseCase bootstrap or manual GT edit.
PERSON_CLASS_ID = 0
LOITERING_PERSON_CLASS_ID = 1

# Back-compat alias used in scripts
LOITERING_CLASS_ID = LOITERING_PERSON_CLASS_ID

LOITERING_CLASS_NAMES: Dict[str, str] = {
    str(PERSON_CLASS_ID): "person",
    str(LOITERING_PERSON_CLASS_ID): "loitering_person",
}

# Repo root: .../PY Analytics  (resources -> loitering-detection -> annotation-apps -> repo)
REPO_ROOT = Path(__file__).resolve().parents[3]

DEFAULT_MODEL = REPO_ROOT / "assets" / "models" / "people_counting_coco_kaggle_0.91_Y11m.pt"

# Match tests/loitering_detection_test.py defaults
DEFAULT_YOLO_CONF = 0.18
DEFAULT_YOLO_IOU = 0.60
DEFAULT_YOLO_IMGSZ = 960
DEFAULT_YOLO_DEVICE = "cpu"
YOLO_PERSON_CLASS_ID = 0


def ensure_loitering_class_names(class_names: Dict[str, str] | None) -> Dict[str, str]:
    """Return a copy of class_names restricted to person + loitering_person."""
    out = dict(LOITERING_CLASS_NAMES)
    if class_names:
        for k, v in class_names.items():
            if str(k) in out:
                out[str(k)] = str(v)
    return out


def clamp_class_id(class_id: int) -> int:
    cid = int(class_id)
    if cid <= PERSON_CLASS_ID:
        return PERSON_CLASS_ID
    return LOITERING_PERSON_CLASS_ID


def color_for_class(class_id: int) -> tuple[int, int, int]:
    """BGR colors aligned with loitering_detection_test.py drawing."""
    if int(class_id) == LOITERING_PERSON_CLASS_ID:
        return (0, 0, 255)  # red — loitering_person
    return (255, 0, 0)  # blue


def json_det_to_matrice(det: Dict[str, Any], width: int, height: int) -> Dict[str, Any]:
    x1, y1, x2, y2 = det["bbox"]
    return {
        "track_id": int(det.get("track_id", -1)),
        "confidence": float(det.get("confidence", 1.0)),
        "category": "person",
        "bounding_box": {
            "xmin": float(x1) * width,
            "ymin": float(y1) * height,
            "xmax": float(x2) * width,
            "ymax": float(y2) * height,
        },
    }


def matrice_det_to_json(
    det: Dict[str, Any],
    width: int,
    height: int,
    *,
    loitering_class_id: int = LOITERING_PERSON_CLASS_ID,
    person_class_id: int = PERSON_CLASS_ID,
) -> Dict[str, Any]:
    bb = det.get("bounding_box") or {}
    x1 = float(bb.get("xmin", bb.get("x1", 0.0)))
    y1 = float(bb.get("ymin", bb.get("y1", 0.0)))
    x2 = float(bb.get("xmax", bb.get("x2", 0.0)))
    y2 = float(bb.get("ymax", bb.get("y2", 0.0)))

    is_loiter = bool(det.get("is_loitering", False))
    category = str(det.get("category", "person"))
    if category == "loitering_person":
        is_loiter = True

    class_id = loitering_class_id if is_loiter else person_class_id

    out: Dict[str, Any] = {
        "class_id": int(class_id),
        "confidence": float(det.get("confidence", 1.0)),
        "bbox": [
            max(0.0, min(1.0, x1 / width)),
            max(0.0, min(1.0, y1 / height)),
            max(0.0, min(1.0, x2 / width)),
            max(0.0, min(1.0, y2 / height)),
        ],
    }
    tid = det.get("track_id")
    if tid is not None:
        out["track_id"] = int(tid)
    return out


def add_analytics_src_to_path() -> Path:
    src = REPO_ROOT / "PY_ANALYTICS_NEW" / "py_analytics" / "src"
    if not src.is_dir():
        raise RuntimeError(f"matrice_analytics source not found: {src}")
    import sys

    path_str = str(src)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
    return src
