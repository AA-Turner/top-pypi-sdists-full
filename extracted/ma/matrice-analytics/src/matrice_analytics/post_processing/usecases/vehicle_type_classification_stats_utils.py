"""Pure data-transform helpers split out of ``vehicle_type_classification._generate_tracking_stats``
(INC-2026-146/147 -- that method and its sibling ``process`` grew past both the file-size and
complexity caps the moment mandatory ``ruff format`` first touched this file; these two pieces
were the stateless ones, so they moved here unchanged rather than being rewritten).
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Tuple


def build_count_lists(
    total_counts_dict: Dict[str, int],
    detection_count_by_category: Dict[str, int],
    per_category_count: Dict[str, int],
    total_detections: int,
    new_counts_dict: Dict[str, int],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """``(total_counts, current_counts, current_new_counts)`` -- the three ``[{category, count}]``
    lists ``_generate_tracking_stats`` builds before assembling the tracking-stat record."""
    total_counts = [
        {"category": cat, "count": count} for cat, count in total_counts_dict.items() if count > 0
    ]
    current_counts = [
        {"category": cat, "count": count} for cat, count in detection_count_by_category.items()
    ]
    if not current_counts and total_detections > 0:
        current_counts = [
            {"category": cat, "count": count} for cat, count in per_category_count.items()
        ]
    current_new_counts = [
        {"category": cat, "count": count} for cat, count in new_counts_dict.items()
    ]
    return total_counts, current_counts, current_new_counts


def build_detection_objects(
    raw_detections: List[Dict[str, Any]],
    create_detection_object: Callable[..., Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """The ``vehicle_type``-tagged detection objects for ``tracking_stats["detections"]``.

    ``create_detection_object`` is the use-case's own bound method -- passed in rather than
    imported, so this stays a plain data transform with no dependency on the use-case class.
    """
    detections = []
    for detection in raw_detections:
        bbox = detection.get("bounding_box", {})
        category = detection.get("category", "vehicle")
        if detection.get("masks"):
            detection_obj = create_detection_object(
                category, bbox, segmentation=detection.get("masks", [])
            )
        elif detection.get("segmentation"):
            detection_obj = create_detection_object(
                category, bbox, segmentation=detection.get("segmentation")
            )
        elif detection.get("mask"):
            detection_obj = create_detection_object(
                category, bbox, segmentation=detection.get("mask")
            )
        else:
            detection_obj = create_detection_object(category, bbox)
        detection_obj["vehicle_type"] = detection.get("vehicle_type", "unknown")
        detection_obj["vehicle_type_confidence"] = detection.get("vehicle_type_confidence", 0.0)
        detections.append(detection_obj)
    return detections
