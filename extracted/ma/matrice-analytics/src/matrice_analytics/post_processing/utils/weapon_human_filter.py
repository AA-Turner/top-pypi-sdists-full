"""
Weapon–human association filter (``best (2).pt`` notebook parity).

Model classes: ``0: weapon``, ``1: human``.

Per frame:
- No human present → keep all weapon detections.
- Human(s) present → keep a weapon only if it **contacts** at least one human
  (overlap, shared edge/corner, or weapon center inside human box) **and**
  ``area(weapon) < ratio × area(nearest contacting human)``.

Humans and non-weapon/non-human detections are always retained.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from .weapon_person_fusion_v1 import (
    _norm_cat,
    _xyxy_from_det,
    coerce_frame_detections,
    iou_positive_or_centroid_inside,
)


def _bbox_area_xyxy(box: Tuple[int, int, int, int]) -> float:
    x1, y1, x2, y2 = box
    return max(0.0, float(x2 - x1)) * max(0.0, float(y2 - y1))


def _boxes_touch_or_overlap(
    a: Tuple[int, int, int, int],
    b: Tuple[int, int, int, int],
) -> bool:
    """True when boxes overlap or share an edge/corner (zero gap on both axes)."""
    x_sep = min(a[2], b[2]) - max(a[0], b[0])
    y_sep = min(a[3], b[3]) - max(a[1], b[1])
    return x_sep >= 0 and y_sep >= 0


def weapon_contacts_human(
    weapon_xyxy: Tuple[int, int, int, int],
    human_xyxy: Tuple[int, int, int, int],
) -> bool:
    """Overlap, edge contact, or weapon bbox center inside the human bbox."""
    if iou_positive_or_centroid_inside(weapon_xyxy, human_xyxy):
        return True
    return _boxes_touch_or_overlap(weapon_xyxy, human_xyxy)


def _contacting_human_boxes(
    weapon_xyxy: Tuple[int, int, int, int],
    person_xyxys: List[Tuple[int, int, int, int]],
) -> List[Tuple[int, int, int, int]]:
    return [p for p in person_xyxys if weapon_contacts_human(weapon_xyxy, p)]


def _nearest_person_bbox(
    weapon_xyxy: Tuple[int, int, int, int],
    person_xyxys: List[Tuple[int, int, int, int]],
) -> Optional[Tuple[int, int, int, int]]:
    if not person_xyxys:
        return None
    wc = ((weapon_xyxy[0] + weapon_xyxy[2]) / 2.0, (weapon_xyxy[1] + weapon_xyxy[3]) / 2.0)
    best, best_d = None, 1e18
    for p_xy in person_xyxys:
        pc = ((p_xy[0] + p_xy[2]) / 2.0, (p_xy[1] + p_xy[3]) / 2.0)
        d = (wc[0] - pc[0]) ** 2 + (wc[1] - pc[1]) ** 2
        if d < best_d:
            best_d, best = d, p_xy
    return best


def filter_weapons_by_nearest_human_area_ratio(
    weapon_detections: List[Dict[str, Any]],
    person_detections: List[Dict[str, Any]],
    max_weapon_to_human_area_ratio: float = 0.40,
) -> List[Dict[str, Any]]:
    """
    Filter for ``best (2).pt`` — weapons are kept when the frame has no humans.
    When humans are present, a weapon must contact a human and pass the area rule.
    """
    if not person_detections:
        return list(weapon_detections)

    person_boxes: List[Tuple[int, int, int, int]] = []
    for p in person_detections:
        t = _xyxy_from_det(p)
        if t is not None:
            person_boxes.append(t)
    if not person_boxes:
        return list(weapon_detections)

    kept: List[Dict[str, Any]] = []
    for wdet in weapon_detections:
        w_xy = _xyxy_from_det(wdet)
        if w_xy is None:
            continue
        w_area = _bbox_area_xyxy(w_xy)
        if w_area <= 0:
            continue
        contacting = _contacting_human_boxes(w_xy, person_boxes)
        if not contacting:
            continue
        nearest = _nearest_person_bbox(w_xy, contacting)
        if nearest is None:
            continue
        p_area = _bbox_area_xyxy(nearest)
        if p_area <= 0:
            continue
        if w_area < p_area * max_weapon_to_human_area_ratio:
            kept.append(wdet)
    return kept


def split_weapon_human_and_other(
    detections: Iterable[Dict[str, Any]],
    weapon_categories: Set[str],
    human_categories: Set[str],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    weapons: List[Dict[str, Any]] = []
    humans: List[Dict[str, Any]] = []
    other: List[Dict[str, Any]] = []
    weapon_l = {c.lower() for c in weapon_categories}
    human_l = {c.lower() for c in human_categories}
    for det in detections:
        cat = _norm_cat(det)
        if cat in weapon_l:
            weapons.append(det)
        elif cat in human_l:
            humans.append(det)
        else:
            other.append(det)
    return weapons, humans, other


def apply_weapon_human_frame_filter(
    detections: List[Dict[str, Any]],
    *,
    weapon_categories: Set[str],
    human_categories: Set[str],
    max_weapon_to_human_area_ratio: float = 0.40,
) -> List[Dict[str, Any]]:
    """Return ``kept_weapons + humans + other`` for one frame."""
    weapons, humans, other = split_weapon_human_and_other(
        detections, weapon_categories, human_categories
    )
    kept_weapons = filter_weapons_by_nearest_human_area_ratio(
        weapons,
        humans,
        max_weapon_to_human_area_ratio=max_weapon_to_human_area_ratio,
    )
    return kept_weapons + humans + other


def apply_weapon_human_filter(
    data: Any,
    *,
    weapon_categories: Set[str],
    human_categories: Set[str],
    max_weapon_to_human_area_ratio: float = 0.40,
) -> List[Dict[str, Any]]:
    """Normalize input to a flat frame list and apply the filter."""
    flat = coerce_frame_detections(data)
    return apply_weapon_human_frame_filter(
        flat,
        weapon_categories=weapon_categories,
        human_categories=human_categories,
        max_weapon_to_human_area_ratio=max_weapon_to_human_area_ratio,
    )
