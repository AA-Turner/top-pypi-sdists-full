"""Auto-generated stub for module: weapon_human_filter."""
from typing import Any, Dict, List, Set, Tuple

from .weapon_person_fusion_v1 import _norm_cat, _xyxy_from_det, coerce_frame_detections, iou_positive_or_centroid_inside

# Functions
def apply_weapon_human_filter(data: Any) -> List[Dict[str, Any]]:
    """
    Normalize input to a flat frame list and apply the filter.
    """
    ...
def apply_weapon_human_frame_filter(detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Return ``kept_weapons + humans + other`` for one frame.
    """
    ...
def filter_weapons_by_nearest_human_area_ratio(weapon_detections: List[Dict[str, Any]], person_detections: List[Dict[str, Any]], max_weapon_to_human_area_ratio: float = 0.4) -> List[Dict[str, Any]]:
    """
    Filter for ``best (2).pt`` — weapons are kept when the frame has no humans.
    When humans are present, a weapon must contact a human and pass the area rule.
    """
    ...
def split_weapon_human_and_other(detections: Any[Dict[str, Any]], weapon_categories: Set[str], human_categories: Set[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]: ...
def weapon_contacts_human(weapon_xyxy: Tuple[int, int, int, int], human_xyxy: Tuple[int, int, int, int]) -> bool:
    """
    Overlap, edge contact, or weapon bbox center inside the human bbox.
    """
    ...
