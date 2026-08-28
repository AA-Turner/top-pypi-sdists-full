"""Auto-generated stub for module: weapon_person_fusion_v1."""
from typing import Any, Dict, List, Set, Tuple

from .geometry_utils import calculate_iou
from .visualization_utils import bbox_dict_to_xyxy

# Functions
def apply_weapon_person_fusion_v1(detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Full V1 path: split → knife-priority fusion → person association.
    
    Intended for tests and for calling from services without the full use case.
    """
    ...
def coerce_frame_detections(data: Any) -> List[Dict[str, Any]]:
    """
    Normalize pipeline input to a flat list of detection dicts for one frame.
    
    Supported shapes:
    - list[dict]: detections for the current frame
    - dict with keys ``person_detections`` / ``weapon_detections`` (lists merged)
    - dict with ``detections`` list
    - dict[str|int, list] tracking-style single frame (first value used if only one key)
    """
    ...
def filter_weapons_by_person_proximity(weapon_detections: List[Dict[str, Any]], person_detections: List[Dict[str, Any]], max_weapon_to_person_area_ratio: float = 0.5) -> List[Dict[str, Any]]:
    """
    Keep weapons that overlap / touch a person and are smaller than ``ratio`` × person area.
    """
    ...
def fuse_knife_preferred_weapon_detections(weapon_detections: List[Dict[str, Any]], knife_priority_categories: Set[str]) -> List[Dict[str, Any]]:
    """
    If any knife-priority class is present, keep only those; otherwise keep all weapons.
    
    Mirrors: ``if len(knife_boxes) > 0: final = knife_boxes else: final = general``.
    """
    ...
def iou_positive_or_centroid_inside(weapon_xyxy: Tuple[int, int, int, int], person_xyxy: Tuple[int, int, int, int]) -> bool:
    """
    IoU > 0 or weapon bbox center (integer midpoints) lies inside person xyxy.
    """
    ...
def split_person_and_weapons(detections: Any[Dict[str, Any]], person_categories: Set[str], weapon_categories: Set[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Split a flat detection list using lowercase category names.
    """
    ...
