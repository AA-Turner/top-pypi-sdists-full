"""claude_people_counting_usecase — count people per frame with unique-ID tracking."""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Set

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..utils import (
    apply_category_mapping,
    filter_by_confidence,
)


class ClaudePeopleCountingUsecaseConfig(BaseConfig):
    def __init__(
        self,
        usecase: str = "claude_people_counting_usecase",
        category: str = "general",
        confidence_threshold: float = 0.4,
        target_categories: Optional[List[str]] = None,
        enable_analytics: bool = True,
        enable_tracking: bool = True,
        enable_unique_counting: bool = True,
        index_to_category: Optional[Dict[int, str]] = None,
        alert_config: Optional[AlertConfig] = None,
        **kwargs,
    ):
        super().__init__(usecase=usecase, category=category, **kwargs)
        self.confidence_threshold = confidence_threshold
        self.target_categories = target_categories or ["person"]
        self.enable_analytics = enable_analytics
        self.enable_tracking = enable_tracking
        self.enable_unique_counting = enable_unique_counting
        self.index_to_category = index_to_category
        self.alert_config = alert_config

    def validate(self) -> List[str]:
        errors = super().validate()
        if not 0.0 <= self.confidence_threshold <= 1.0:
            errors.append("confidence_threshold must be between 0.0 and 1.0")
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        return errors


class ClaudePeopleCountingUsecaseUseCase(BaseProcessor):
    def __init__(self) -> None:
        super().__init__("claude_people_counting_usecase")
        self.CASE_TYPE = "claude_people_counting_usecase"
        self.CASE_VERSION = "1.0"
        self.category = "general"
        self.target_categories = ["person"]

        self._total_frames = 0
        self._total_detections = 0
        self._unique_track_ids: Set[int] = set()
        # Per-threshold-key alert cooldown anchors, stamped with time.monotonic() so a
        # wall-clock step backwards (NTP correction, VM restore) cannot suppress alerts
        # past the cooldown. A missing key means "never emitted" -- checked with an
        # explicit `is None` rather than a 0.0 default, because monotonic() may start
        # near zero and would otherwise gate the first alert.
        self._last_alert_monotonic: Dict[str, float] = {}

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "target_categories": {"type": "array", "items": {"type": "string"}},
                "enable_tracking": {"type": "boolean"},
                "enable_unique_counting": {"type": "boolean"},
            },
        }

    def create_default_config(self, **overrides: Any) -> "ClaudePeopleCountingUsecaseConfig":
        defaults: Dict[str, Any] = {"category": self.category, "usecase": self.name}
        defaults.update(overrides)
        return ClaudePeopleCountingUsecaseConfig(**defaults)

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        if not isinstance(config, ClaudePeopleCountingUsecaseConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        processed = filter_by_confidence(data, config.confidence_threshold)

        if config.index_to_category:
            processed = apply_category_mapping(processed, config.index_to_category)

        processed = [d for d in processed if d.get("category") in config.target_categories]

        if config.enable_unique_counting:
            for det in processed:
                tid = det.get("track_id")
                if tid is not None:
                    self._unique_track_ids.add(tid)

        self._total_frames += 1
        current_count = len(processed)
        self._total_detections += current_count

        frame_number = None
        if stream_info:
            frame_number = stream_info.get("frame_id") or stream_info.get("input_settings", {}).get("start_frame")

        camera_info = self.get_camera_info_from_stream(stream_info)
        timestamp = self.get_high_precision_timestamp()

        incidents: Dict[str, Any] = {}
        if current_count > 0:
            severity = self.determine_severity_level(current_count)
            incidents = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_number}",
                incident_type=self.CASE_TYPE,
                severity_level=severity,
                human_text=f"{self.CASE_TYPE}: {current_count} people [{severity}]",
                camera_info=camera_info,
            )

        current_counts = [
            self.create_count_object(cat, sum(1 for d in processed if d.get("category") == cat))
            for cat in config.target_categories
            if any(d.get("category") == cat for d in processed)
        ]
        unique_total = len(self._unique_track_ids) if config.enable_unique_counting else self._total_detections
        total_counts = [self.create_count_object(cat, unique_total) for cat in config.target_categories]
        detections = [
            self.create_detection_object(
                d.get("category", "unknown"),
                d.get("bounding_box", {}),
            )
            for d in processed
        ]
        tracking_stats = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections,
            human_text=f"Current: {current_count}, Unique total: {unique_total}",
            camera_info=camera_info,
            start_time=timestamp,
        )

        alerts: List[Dict[str, Any]] = []
        if config.alert_config and current_count > 0:
            thresholds = getattr(config.alert_config, "count_thresholds", {}) or {}
            cooldown_s = 10.0
            for key, threshold in thresholds.items():
                actual = current_count if key == "all" else sum(1 for d in processed if d.get("category") == key)
                if actual >= threshold:
                    now = time.monotonic()
                    last = self._last_alert_monotonic.get(key)
                    if last is None or now - last >= cooldown_s:
                        alerts.append(
                            {
                                "alert_type": getattr(config.alert_config, "alert_type", "count"),
                                "key": key,
                                "count": actual,
                                "threshold": threshold,
                            }
                        )
                        self._last_alert_monotonic[key] = now

        frame_key = str(frame_number) if frame_number else "current_frame"
        agg_summary = {
            frame_key: {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": {},
                "alerts": alerts,
                "human_text": (
                    f"{self.CASE_TYPE} v{self.CASE_VERSION}: "
                    f"{current_count} people this frame, {unique_total} unique total"
                ),
            }
        }

        context.mark_completed()
        return self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )
