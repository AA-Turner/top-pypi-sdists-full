"""AdvancedTracker adapter — wraps in-repo ``advanced_tracker`` module.

Besides the standard thresholds, this adapter maps the CCTVTracker-style opt-in
features (carried in ``MatriceTrackerConfig.extra``) onto ``TrackerConfig`` so a
caller migrating off CCTVTracker gets temporal confirmation / FPS adaptation /
predict-glide with the same config vocabulary. All of these default OFF, so an
empty ``extra`` reproduces the previous adapter behavior exactly.
"""

from __future__ import annotations

import logging
from dataclasses import fields as _dc_fields
from typing import Any, Dict, List, Optional

from ..base import BaseObjectTracker, DetectionDict
from ..config import MatriceTrackerConfig

logger = logging.getLogger(__name__)


class AdvancedTrackerAdapter(BaseObjectTracker):
    """Thin wrapper around ``AdvancedTracker`` with Matrice dict I/O."""

    def __init__(self, config: MatriceTrackerConfig, namespace: Optional[str] = None):
        from ...advanced_tracker import AdvancedTracker
        from ...advanced_tracker.config import TrackerConfig

        extra: Dict[str, Any] = getattr(config, "extra", None) or {}

        # fps handling (CCTVTracker semantics): fps == 0 means auto-detect ->
        # enable FPS adaptation; fps > 0 pins the frame_rate. TrackerConfig has no
        # fps=0 state (frame_rate must be > 0), so 0 maps to the adaptation flag.
        frame_rate = config.frame_rate
        enable_fps_adaptation = bool(extra.get("enable_fps_adaptation", False))
        fps = extra.get("fps", None)
        if fps is not None:
            try:
                fps_val = float(fps)
            except (TypeError, ValueError):
                fps_val = None  # non-numeric fps in extra -> ignore, keep frame_rate
            if fps_val is not None:
                if fps_val <= 0:
                    enable_fps_adaptation = True  # 0/negative == auto-detect
                else:
                    # max(1, ...): a sub-0.5 fps would round to 0, which
                    # TrackerConfig rejects ("frame_rate must be positive").
                    frame_rate = max(1, int(round(fps_val)))

        tc_kwargs: Dict[str, Any] = dict(
            track_high_thresh=config.track_high_thresh,
            track_low_thresh=config.track_low_thresh,
            new_track_thresh=config.new_track_thresh,
            match_thresh=config.match_thresh,
            track_buffer=config.track_buffer,
            max_time_lost=config.max_time_lost,
            frame_rate=frame_rate,
            enable_fps_adaptation=enable_fps_adaptation,
            enable_temporal_confirmation=bool(extra.get("enable_temporal_confirmation", False)),
            enable_predict_on_empty=bool(extra.get("enable_predict_on_empty", False)),
        )
        # Any other valid TrackerConfig field may be tuned via extra (e.g.
        # grace_period_sec, confirm_window_sec, enable_state_persistence,
        # enable_gmc). Only real fields pass through; TrackerConfig.__post_init__
        # then validates them. ``fps`` is handled above, not a TrackerConfig field.
        tc_field_names = {f.name for f in _dc_fields(TrackerConfig)}
        passthrough = {k: v for k, v in extra.items() if k in tc_field_names and k not in tc_kwargs}
        tc_kwargs.update(passthrough)

        try:
            tracker_config = TrackerConfig(**tc_kwargs)
        except (TypeError, ValueError) as exc:
            # ``extra`` was ignored entirely before this adapter learned to read it,
            # so a caller carrying an out-of-range or wrongly typed value there must
            # not start crashing tracker construction. Drop the passthrough and warn.
            if not passthrough:
                raise
            logger.warning(
                "AdvancedTrackerAdapter: ignoring invalid TrackerConfig overrides from `extra` (%s): %s",
                ", ".join(sorted(passthrough)),
                exc,
            )
            for key in passthrough:
                tc_kwargs.pop(key, None)
            tracker_config = TrackerConfig(**tc_kwargs)
        if config.confidence_threshold is not None:
            tracker_config.track_high_thresh = float(config.confidence_threshold)
            tracker_config.track_low_thresh = max(0.05, float(config.confidence_threshold) / 2)
            tracker_config.new_track_thresh = float(config.confidence_threshold)

        self._tracker = AdvancedTracker(tracker_config, namespace=namespace)

    def update(
        self,
        detections: List[DetectionDict],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[DetectionDict]:
        _ = stream_info
        return self._tracker.update(detections)

    def reset(self) -> None:
        if hasattr(self._tracker, "reset"):
            self._tracker.reset()

    def restore_state(self) -> None:
        if hasattr(self._tracker, "restore_state"):
            self._tracker.restore_state()

    def save_state(self) -> None:
        if hasattr(self._tracker, "save_state"):
            self._tracker.save_state()
