"""
Filter utilities for post-processing operations.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def filter_by_confidence(results: Any, threshold: float = 0.5) -> Any:
    """
    Filter results by confidence threshold.

    Args:
        results: Detection or tracking results
        threshold: Minimum confidence threshold

    Returns:
        Filtered results in the same format
    """
    if isinstance(results, list):
        # Detection format
        return [r for r in results if r.get("confidence", 0) >= threshold]

    elif isinstance(results, dict):
        # Check if it's a simple classification result
        if "confidence" in results and "category" in results:
            return results if results.get("confidence", 0) >= threshold else {}

        # Frame-based format (tracking or activity recognition)
        filtered_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                filtered_detections = [d for d in detections if d.get("confidence", 0) >= threshold]
                if filtered_detections:
                    filtered_results[frame_id] = filtered_detections

        return filtered_results

    return results


def filter_by_categories(results: Any, allowed_categories: List[str]) -> Any:
    """
    Filter results to only include specified categories.

    Args:
        results: Detection or tracking results
        allowed_categories: List of allowed category names

    Returns:
        Filtered results in the same format
    """
    if isinstance(results, list):
        # Detection format
        return [r for r in results if r.get("category", "") in allowed_categories]

    elif isinstance(results, dict):
        # Check if it's a simple classification result
        if "category" in results:
            return results if results.get("category", "") in allowed_categories else {}

        # Frame-based format
        filtered_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                filtered_detections = [d for d in detections if d.get("category", "") in allowed_categories]
                if filtered_detections:
                    filtered_results[frame_id] = filtered_detections

        return filtered_results

    return results


def calculate_bbox_fingerprint(bbox: Dict[str, Any], category: str = "") -> str:
    """
    Calculate a fingerprint for a bounding box to detect duplicates.

    Args:
        bbox: Bounding box dictionary
        category: Object category

    Returns:
        str: Unique fingerprint for the bbox
    """
    # Extract coordinates
    if "xmin" in bbox:
        coords = (bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"])
    elif "x1" in bbox:
        coords = (bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"])
    else:
        values = list(bbox.values())
        coords = tuple(values[:4]) if len(values) >= 4 else (0, 0, 0, 0)

    # Round coordinates to reduce floating point precision issues
    rounded_coords = tuple(round(c, 2) for c in coords)

    return f"{category}_{rounded_coords}"


def clean_expired_tracks(
    track_timestamps: Dict[str, float],
    track_last_seen: Dict[str, float],
    current_timestamp: float,
    expiry_time: float,
) -> None:
    """
    Clean expired tracks from tracking dictionaries.

    Args:
        track_timestamps: Dictionary of track_id -> first_seen_timestamp
        track_last_seen: Dictionary of track_id -> last_seen_timestamp
        current_timestamp: Current timestamp
        expiry_time: Time after which tracks expire
    """
    expired_tracks = []

    for track_id, last_seen in track_last_seen.items():
        if current_timestamp - last_seen > expiry_time:
            expired_tracks.append(track_id)

    for track_id in expired_tracks:
        track_timestamps.pop(track_id, None)
        track_last_seen.pop(track_id, None)


def remove_duplicate_detections(
    results: List[Dict[str, Any]], similarity_threshold: float = 0.8
) -> List[Dict[str, Any]]:
    """
    Remove duplicate detections based on bbox similarity.

    Args:
        results: List of detection dictionaries
        similarity_threshold: IoU threshold for considering detections as duplicates

    Returns:
        List of unique detections
    """
    from .geometry_utils import calculate_iou

    if not results:
        return results

    unique_detections = []

    for detection in results:
        is_duplicate = False

        for existing in unique_detections:
            # Check if same category
            if detection.get("category") == existing.get("category"):
                # Calculate IoU between bounding boxes
                bbox1 = detection.get("bounding_box", detection.get("bbox", {}))
                bbox2 = existing.get("bounding_box", existing.get("bbox", {}))

                if bbox1 and bbox2:
                    iou = calculate_iou(bbox1, bbox2)
                    if iou >= similarity_threshold:
                        is_duplicate = True
                        # Keep the one with higher confidence
                        if detection.get("confidence", 0) > existing.get("confidence", 0):
                            unique_detections.remove(existing)
                            unique_detections.append(detection)
                        break

        if not is_duplicate:
            unique_detections.append(detection)

    return unique_detections


#: Index maps whose unmatched indices have already been reported, keyed by
#: ``(sorted keys, unmatched index)``. Once per config shape, not once per frame -- an
#: unmapped class recurs on every detection of every frame, and this warning exists to
#: be noticed, not to bury the log.
_UNMATCHED_INDEX_WARNED: set = set()


def apply_category_mapping(results: Any, index_to_category: Dict[str, str]) -> Any:
    """
    Apply category index to name mapping.

    This is where a deployment's ``class_index_map`` becomes ``detection["category"]``,
    which makes it the boundary where a malformed entry turns into silent data loss.
    Two hardenings live here for that reason:

    * **Labels are stripped.** A real deployment carried
      ``{"0": "knife", "1": "gun "}`` -- one trailing space. The weapon manifest's
      ``entity_mapping`` is ``{knife: knife, gun: gun}``, ``"gun "`` matched nothing,
      and because an unmapped class is *ignored* rather than rejected, the app detected
      nothing, published nothing and raised no incident. Silently. Forever.
    * **An index the map does not cover is reported.** Previously there was no branch at
      all: the detection kept its numeric category and was dropped by a later category
      filter. That is the other half of the same outage -- the weapon manifest declared
      six classes against a two-entry map, so indices 2-5 resolved to nothing.

    Args:
        results: Detection or tracking results
        index_to_category: Mapping from category index to category name

    Returns:
        Results with mapped category names
    """
    # Built once per call. This used to be rebuilt inside map_detection, i.e. once per
    # detection per frame.
    normalized = {str(k).strip(): str(v).strip() for k, v in (index_to_category or {}).items()}
    warn_key_base = tuple(sorted(normalized))

    def map_detection(detection: Dict[str, Any], _unused: Any = None) -> Dict[str, Any]:
        """Map a single detection."""
        detection = detection.copy()
        category_id = str(detection.get("category", detection.get("category_id"))).strip()
        if category_id in normalized:
            detection["category"] = normalized[category_id]
            detection["category_id"] = category_id
        elif normalized and category_id.isdigit():
            # Numeric and unmapped: the model emitted a class the deployment config does
            # not name, so nothing downstream can match it.
            warn_key = (warn_key_base, category_id)
            if warn_key not in _UNMATCHED_INDEX_WARNED:
                _UNMATCHED_INDEX_WARNED.add(warn_key)
                logger.warning(
                    "apply_category_mapping: class index %r is not in the deployment's "
                    "class_index_map (it covers %s); detections of this class keep a numeric "
                    "category and will be dropped by any category filter downstream.",
                    category_id,
                    ", ".join(f"{k}={normalized[k]!r}" for k in sorted(normalized)),
                )
        return detection

    if isinstance(results, list):
        # Detection format
        return [map_detection(r) for r in results]

    elif isinstance(results, dict):
        # Check if it's a simple classification result
        if "category" in results or "category_id" in results:
            return map_detection(results)

        # Frame-based format
        mapped_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                mapped_results[frame_id] = [map_detection(d) for d in detections]
            else:
                mapped_results[frame_id] = detections

        return mapped_results

    return results


def filter_by_area(results: Any, min_area: float = 0, max_area: float = float("inf")) -> Any:
    """
    Filter detections by bounding box area.

    Args:
        results: Detection or tracking results
        min_area: Minimum bounding box area
        max_area: Maximum bounding box area

    Returns:
        Filtered results
    """
    from .geometry_utils import get_bbox_area

    def is_valid_area(detection: Dict[str, Any]) -> bool:
        """Check if detection has valid area."""
        bbox = detection.get("bounding_box", detection.get("bbox"))
        if not bbox:
            return True  # Keep detections without bbox

        area = get_bbox_area(bbox)
        return min_area <= area <= max_area

    if isinstance(results, list):
        # Detection format
        return [r for r in results if is_valid_area(r)]

    elif isinstance(results, dict):
        # Frame-based format
        filtered_results = {}
        for frame_id, detections in results.items():
            if isinstance(detections, list):
                filtered_detections = [d for d in detections if is_valid_area(d)]
                if filtered_detections:
                    filtered_results[frame_id] = filtered_detections

        return filtered_results

    return results
