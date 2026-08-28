"""Auto-generated stub for module: loitering_common."""
from typing import Any, Dict

# Constants
DEFAULT_MODEL: Any
DEFAULT_YOLO_CONF: float
DEFAULT_YOLO_DEVICE: str
DEFAULT_YOLO_IMGSZ: int
DEFAULT_YOLO_IOU: float
LOITERING_CLASS_ID: Any
LOITERING_PERSON_CLASS_ID: int
PERSON_CLASS_ID: int
REPO_ROOT: Any
YOLO_PERSON_CLASS_ID: int

# Functions
def add_analytics_src_to_path() -> Any: ...
def clamp_class_id(class_id: int) -> int: ...
def color_for_class(class_id: int) -> tuple[int, int, int]:
    """
    BGR colors aligned with loitering_detection_test.py drawing.
    """
    ...
def ensure_loitering_class_names(class_names: Dict[str, str] | None) -> Dict[str, str]:
    """
    Return a copy of class_names restricted to person + loitering_person.
    """
    ...
def json_det_to_matrice(det: Dict[str, Any], width: int, height: int) -> Dict[str, Any]: ...
def matrice_det_to_json(det: Dict[str, Any], width: int, height: int) -> Dict[str, Any]: ...
