"""Auto-generated stub for module: vehicle_type_classification_stats_utils."""
from typing import Any, Callable, Dict, List, Tuple

# Functions
def build_count_lists(total_counts_dict: Dict[str, int], detection_count_by_category: Dict[str, int], per_category_count: Dict[str, int], total_detections: int, new_counts_dict: Dict[str, int]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    ``(total_counts, current_counts, current_new_counts)`` -- the three ``[{category, count}]``
        lists ``_generate_tracking_stats`` builds before assembling the tracking-stat record.
    """
    ...
def build_detection_objects(raw_detections: List[Dict[str, Any]], create_detection_object: Callable[..., Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    The ``vehicle_type``-tagged detection objects for ``tracking_stats["detections"]``.
    
        ``create_detection_object`` is the use-case's own bound method -- passed in rather than
        imported, so this stays a plain data transform with no dependency on the use-case class.
    """
    ...
