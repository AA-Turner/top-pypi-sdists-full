from typing import Any, Dict, Optional, Tuple

try:
    import cv2
except ImportError:
    cv2 = None
import numpy as np


def draw_text(frame: np.ndarray, text: str, x: int, y: int, scale: float = 0.6) -> None:
    cv2.putText(
        frame,
        text,
        (int(x), int(y)),
        cv2.FONT_HERSHEY_SIMPLEX,
        float(scale),
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )


def draw_box(frame: np.ndarray, xyxy: Tuple[int, int, int, int], color: Tuple[int, int, int]) -> None:
    x1, y1, x2, y2 = xyxy
    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)


def clamp_xyxy(x1: int, y1: int, x2: int, y2: int, w: int, h: int) -> Tuple[int, int, int, int]:
    """
    Clamp + sanitize bbox coords into frame bounds.

    Ensures:
      - 0 <= x < w
      - 0 <= y < h
      - x1 <= x2
      - y1 <= y2
    """
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    # swap if inverted
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1

    # clamp after swap
    x1 = max(0, min(w - 1, x1))
    x2 = max(0, min(w - 1, x2))
    y1 = max(0, min(h - 1, y1))
    y2 = max(0, min(h - 1, y2))

    return x1, y1, x2, y2


def bbox_dict_to_xyxy(bb: Dict[str, Any]) -> Optional[Tuple[int, int, int, int]]:
    """
    Supports:
      - {"xmin","ymin","xmax","ymax"}
      - {"x1","y1","x2","y2"}
    Returns:
      (x1, y1, x2, y2) ints, or None if invalid.
    """
    if not isinstance(bb, dict):
        return None

    def _as_int(v: Any) -> int:
        try:
            return int(float(v))
        except Exception:
            return 0

    if "xmin" in bb:
        return (
            _as_int(bb.get("xmin", 0)),
            _as_int(bb.get("ymin", 0)),
            _as_int(bb.get("xmax", 0)),
            _as_int(bb.get("ymax", 0)),
        )

    if "x1" in bb:
        return (
            _as_int(bb.get("x1", 0)),
            _as_int(bb.get("y1", 0)),
            _as_int(bb.get("x2", 0)),
            _as_int(bb.get("y2", 0)),
        )

    return None
