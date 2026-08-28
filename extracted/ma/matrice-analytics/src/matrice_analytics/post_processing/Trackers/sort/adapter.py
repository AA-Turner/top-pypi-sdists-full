"""SORT tracker adapter."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..base import BaseObjectTracker, DetectionDict, ensure_track_id
from ..config import MatriceTrackerConfig


class SORTTrackerAdapter(BaseObjectTracker):
    """Wraps in-repo ``SORTTracker`` from ``bytetrack_utils``."""

    def __init__(self, config: MatriceTrackerConfig):
        from ...utils.bytetrack_utils import SORTTracker

        self._config = config
        self._tracker = SORTTracker(
            iou_threshold=config.sort_iou_threshold,
            max_age=config.sort_max_age,
            min_hits=config.sort_min_hits,
        )

    def update(
        self,
        detections: List[DetectionDict],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[DetectionDict]:
        _ = stream_info
        return ensure_track_id(self._tracker.update(list(detections or [])))

    def reset(self) -> None:
        from ...utils.bytetrack_utils import SORTTracker

        self._tracker = SORTTracker(
            iou_threshold=self._config.sort_iou_threshold,
            max_age=self._config.sort_max_age,
            min_hits=self._config.sort_min_hits,
        )
