"""Auto-generated stub for module: visualization_utils."""
from typing import Any, Dict, Optional, Tuple

# Functions
def bbox_dict_to_xyxy(bb: Dict[str, Any]) -> Optional[Tuple[int, int, int, int]]:
    """
    Supports:
      - {"xmin","ymin","xmax","ymax"}
      - {"x1","y1","x2","y2"}
    Returns:
      (x1, y1, x2, y2) ints, or None if invalid.
    """
    ...
def clamp_xyxy(x1: int, y1: int, x2: int, y2: int, w: int, h: int) -> Tuple[int, int, int, int]:
    """
    Clamp + sanitize bbox coords into frame bounds.
    
    Ensures:
      - 0 <= x < w
      - 0 <= y < h
      - x1 <= x2
      - y1 <= y2
    """
    ...
def draw_box(frame: Any.Any, xyxy: Tuple[int, int, int, int], color: Tuple[int, int, int]) -> None: ...
def draw_text(frame: Any.Any, text: str, x: int, y: int, scale: float = 0.6) -> None: ...
