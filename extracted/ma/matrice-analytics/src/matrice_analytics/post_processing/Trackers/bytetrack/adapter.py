"""ByteTrack adapter (YOLOX backend via existing wrapper)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..base import BaseObjectTracker, DetectionDict, ensure_track_id
from ..config import MatriceTrackerConfig


class ByteTrackAdapter(BaseObjectTracker):
    """Wraps ``ByteTrackWrapper`` from ``bytetrack_utils`` (YOLOX BYTETracker)."""

    def __init__(self, config: MatriceTrackerConfig):
        from ...utils.bytetrack_utils import ByteTrackWrapper

        self._tracker = ByteTrackWrapper(
            fps=config.bytetrack_fps,
            track_thresh=config.bytetrack_track_thresh,
            match_thresh=config.bytetrack_match_thresh,
            track_buffer=config.bytetrack_track_buffer,
        )

    def update(
        self,
        detections: List[DetectionDict],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[DetectionDict]:
        return ensure_track_id(self._tracker.update(list(detections or []), stream_info=stream_info))
