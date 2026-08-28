"""
V1 person–weapon fusion and association (offline script parity).

Implements knife-priority fusion and person association used in the standalone
weapon pipeline, operating on Matrice detection dicts (bounding_box, category, confidence).

This module is intentionally independent of Ultralytics so it can run in post-processing only.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from .geometry_utils import calculate_iou
from .visualization_utils import bbox_dict_to_xyxy


def coerce_frame_detections(data: Any) -> List[Dict[str, Any]]:
    """
    Normalize pipeline input to a flat list of detection dicts for one frame.

    Supported shapes:
    - list[dict]: detections for the current frame
    - dict with keys ``person_detections`` / ``weapon_detections`` (lists merged)
    - dict with ``detections`` list
    - dict[str|int, list] tracking-style single frame (first value used if only one key)
    """
    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]

    if isinstance(data, dict):
        if "person_detections" in data or "weapon_detections" in data:
            wd = data.get("weapon_detections") or []
            pd = data.get("person_detections") or []
            out: List[Dict[str, Any]] = []
            if isinstance(pd, list):
                out.extend(d for d in pd if isinstance(d, dict))
            if isinstance(wd, list):
                out.extend(d for d in wd if isinstance(d, dict))
            return out

        dets = data.get("detections")
        if isinstance(dets, list):
            return [d for d in dets if isinstance(d, dict)]

        frame_keys = [k for k in data.keys() if isinstance(k, (str, int))]
        if frame_keys:
            first = data.get(frame_keys[0])
            if isinstance(first, list):
                return [d for d in first if isinstance(d, dict)]

    return []


def _norm_cat(det: Dict[str, Any]) -> str:
    c = det.get("category", "") or ""
    return str(c).strip().lower()


def split_person_and_weapons(
    detections: Iterable[Dict[str, Any]],
    person_categories: Set[str],
    weapon_categories: Set[str],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Split a flat detection list using lowercase category names."""
    persons: List[Dict[str, Any]] = []
    weapons: List[Dict[str, Any]] = []
    person_categories_l = {c.lower() for c in person_categories}
    weapon_categories_l = {c.lower() for c in weapon_categories}
    for det in detections:
        cat = _norm_cat(det)
        if cat in person_categories_l:
            persons.append(det)
        elif cat in weapon_categories_l:
            weapons.append(det)
    return persons, weapons


def fuse_knife_preferred_weapon_detections(
    weapon_detections: List[Dict[str, Any]],
    knife_priority_categories: Set[str],
) -> List[Dict[str, Any]]:
    """
    If any knife-priority class is present, keep only those; otherwise keep all weapons.

    Mirrors: ``if len(knife_boxes) > 0: final = knife_boxes else: final = general``.
    """
    knife_priority_categories_l = {c.lower() for c in knife_priority_categories}
    knife_only = [d for d in weapon_detections if _norm_cat(d) in knife_priority_categories_l]
    if knife_only:
        return knife_only
    return list(weapon_detections)


def _xyxy_from_det(det: Dict[str, Any]) -> Optional[Tuple[int, int, int, int]]:
    bb = det.get("bounding_box") or det.get("bbox")
    if isinstance(bb, dict):
        t = bbox_dict_to_xyxy(bb)
        return t
    if isinstance(bb, (list, tuple)) and len(bb) >= 4:
        return int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])
    return None


def _bbox_dict_from_xyxy(box: Tuple[int, int, int, int]) -> Dict[str, float]:
    x1, y1, x2, y2 = box
    return {"x1": float(x1), "y1": float(y1), "x2": float(x2), "y2": float(y2)}


def iou_positive_or_centroid_inside(
    weapon_xyxy: Tuple[int, int, int, int],
    person_xyxy: Tuple[int, int, int, int],
) -> bool:
    """IoU > 0 or weapon bbox center (integer midpoints) lies inside person xyxy."""
    w_box = _bbox_dict_from_xyxy(weapon_xyxy)
    p_box = _bbox_dict_from_xyxy(person_xyxy)
    if calculate_iou(w_box, p_box) > 0:
        return True
    wx1, wy1, wx2, wy2 = weapon_xyxy
    px1, py1, px2, py2 = person_xyxy
    cx = (wx1 + wx2) // 2
    cy = (wy1 + wy2) // 2
    return px1 <= cx <= px2 and py1 <= cy <= py2


def filter_weapons_by_person_proximity(
    weapon_detections: List[Dict[str, Any]],
    person_detections: List[Dict[str, Any]],
    max_weapon_to_person_area_ratio: float = 0.5,
) -> List[Dict[str, Any]]:
    """
    Keep weapons that overlap / touch a person and are smaller than ``ratio`` × person area.
    """
    if not person_detections:
        return []

    person_boxes: List[Tuple[int, int, int, int]] = []
    for p in person_detections:
        t = _xyxy_from_det(p)
        if t is not None:
            person_boxes.append(t)

    if not person_boxes:
        return []

    valid: List[Dict[str, Any]] = []
    for wdet in weapon_detections:
        w_xy = _xyxy_from_det(wdet)
        if w_xy is None:
            continue
        wx1, wy1, wx2, wy2 = w_xy
        w_area = max(0, wx2 - wx1) * max(0, wy2 - wy1)
        if w_area <= 0:
            continue
        for p_xy in person_boxes:
            px1, py1, px2, py2 = p_xy
            p_area = max(0, px2 - px1) * max(0, py2 - py1)
            if p_area <= 0:
                continue
            if w_area < p_area * max_weapon_to_person_area_ratio and iou_positive_or_centroid_inside(
                w_xy, p_xy
            ):
                valid.append(wdet)
                break
    return valid


def apply_weapon_person_fusion_v1(
    detections: List[Dict[str, Any]],
    *,
    person_category_names: Set[str],
    fusion_weapon_categories: Set[str],
    knife_priority_categories: Set[str],
    association_max_weapon_to_person_area_ratio: float = 0.5,
) -> List[Dict[str, Any]]:
    """
    Full V1 path: split → knife-priority fusion → person association.

    Intended for tests and for calling from services without the full use case.
    """
    persons, weapons = split_person_and_weapons(
        detections, person_category_names, fusion_weapon_categories
    )
    fused = fuse_knife_preferred_weapon_detections(weapons, knife_priority_categories)
    return filter_weapons_by_person_proximity(
        fused, persons, association_max_weapon_to_person_area_ratio
    )
