"""Create a Matrice-compatible object tracker by method name."""

from __future__ import annotations

import logging
from typing import Optional

from .base import BaseObjectTracker
from .config import SUPPORTED_TRACKING_METHODS, MatriceTrackerConfig

logger = logging.getLogger(__name__)


_METHOD_ALIASES = {
    "kalman": "advanced",
    "advanced": "advanced",
    "byte_track": "bytetrack",
    "byte-track": "bytetrack",
    # oc_sort/deepsort/botsort adapters + their vendor clones were deleted
    # (F10b consolidation step S3 -- oc_sort/OC_SORT, deepsort/deep_sort,
    # botsort/BoT-SORT were 0-file empty clones; nothing ever actually ran).
    # Remapped to the motion-only advanced tracker rather than raising, so an
    # existing deployment JSON that still names one of these keeps working
    # (SUPPORTED_TRACKING_METHODS is intentionally left unchanged -- see
    # config.py -- so validation of those values does not start failing).
    "oc-sort": "advanced",
    "ocsort": "advanced",
    "oc_sort": "advanced",
    "deep_oc_sort": "deep_oc_sort",
    "deep-oc-sort": "deep_oc_sort",
    "deepocsort": "deep_oc_sort",
    "deep_ocsort": "deep_oc_sort",
    "deep_oc-sort": "deep_oc_sort",
    "deep_sort": "advanced",
    "deep-sort": "advanced",
    "deepsort": "advanced",
    "bot_sort": "advanced",
    "bot-sort": "advanced",
    "bc_sort": "advanced",
    "botsort": "advanced",
}

# Requested names that now resolve to "advanced" instead of themselves, used
# to decide when normalize_tracking_method should log the deprecation
# warning. Underscore form only: normalize_tracking_method always replaces
# "-" -> "_" in `requested` before this set is checked.
_REMOVED_METHODS = frozenset({"oc_sort", "ocsort", "deepsort", "deep_sort", "botsort", "bot_sort", "bc_sort"})


def normalize_tracking_method(method: str) -> str:
    requested = str(method or "advanced").lower().strip().replace("-", "_")
    normalized = _METHOD_ALIASES.get(requested, requested)
    if requested in _REMOVED_METHODS:
        logger.warning(
            "tracking_method '%s' was removed (F10b consolidation) -- falling back to 'advanced'",
            method,
        )
    if normalized in SUPPORTED_TRACKING_METHODS:
        return normalized
    return normalized


def create_tracker(
    method: str,
    config: Optional[MatriceTrackerConfig] = None,
    namespace: Optional[str] = None,
) -> BaseObjectTracker:
    """
    Factory for post-processing trackers.

    Args:
        method: ``advanced`` | ``sort`` | ``bytetrack`` | ``deep_oc_sort``. ``oc_sort`` /
            ``deepsort`` / ``botsort`` are accepted (see ``SUPPORTED_TRACKING_METHODS``)
            but normalize to ``advanced`` -- their adapters were deleted (F10b step S3).
        config: Unified tracker configuration
        namespace: Optional stream namespace for ID isolation (advanced tracker)

    Returns:
        BaseObjectTracker instance
    """
    cfg = config or MatriceTrackerConfig()
    name = normalize_tracking_method(method)

    if name == "none":
        raise ValueError("tracking_method 'none' disables tracking — do not call create_tracker")

    if name not in SUPPORTED_TRACKING_METHODS:
        raise ValueError(f"Unknown tracking_method '{method}'. Supported: {sorted(SUPPORTED_TRACKING_METHODS)}")

    if name == "advanced":
        from .advanced_tracker import AdvancedTrackerAdapter

        return AdvancedTrackerAdapter(cfg, namespace=namespace)

    if name == "sort":
        from .sort import SORTTrackerAdapter

        return SORTTrackerAdapter(cfg)

    if name == "bytetrack":
        from .bytetrack import ByteTrackAdapter

        return ByteTrackAdapter(cfg)

    if name == "deep_oc_sort":
        from .deep_oc_sort import DeepOCSortAdapter

        return DeepOCSortAdapter(cfg, namespace=namespace)

    raise ValueError(f"Unsupported tracking_method: {method}")
