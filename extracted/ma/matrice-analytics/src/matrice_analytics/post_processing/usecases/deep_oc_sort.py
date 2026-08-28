"""
deep_oc_sort — people counting driven by the DeepOCSORT tracker.

This use case counts people per frame and maintains a unique running total by
attaching stable track IDs via DeepOCSORT (OC-SORT motion core). Tracking is
delegated to the shared ``Trackers`` framework through ``ConfigDrivenTracker``
with ``tracking_method="deep_oc_sort"``. The DeepOCSORT adapter's ``boxmot``
appearance/ReID backend has been removed (AGPL-3.0 licensing -- see
``Trackers/deep_oc_sort/adapter.py``'s module docstring); it now always uses
the in-repo pure-python ``advanced`` motion tracker.

Outputs follow the standard agg_summary contract (tracking_stats / alerts /
incidents / business_analytics / human_text).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..Trackers.integration import ConfigDrivenTracker
from ..utils import (
    apply_category_mapping,
    filter_by_confidence,
    match_results_structure,
)

_RESET_SETTINGS = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]
_ALERT_COOLDOWN_SECONDS = 30.0


@dataclass
class DeepOCSortConfig(BaseConfig):
    """Configuration for DeepOCSORT-based people counting."""

    confidence_threshold: float = 0.3

    person_categories: List[str] = field(default_factory=lambda: ["person", "people", "human"])
    target_categories: List[str] = field(default_factory=lambda: ["person", "people", "human"])
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "person"})

    enable_unique_counting: bool = True

    # Tracking: route the shared Trackers framework to DeepOCSORT.
    tracking_method: str = "deep_oc_sort"

    # DeepOCSORT tuning (passed through to MatriceTrackerConfig.from_config).
    deep_oc_sort_det_thresh: float = 0.3
    deep_oc_sort_max_age: int = 30
    deep_oc_sort_min_hits: int = 3
    deep_oc_sort_iou_threshold: float = 0.3
    deep_oc_sort_embedding_off: bool = False
    deep_oc_sort_cmc_off: bool = False
    deep_oc_sort_reid_weights: Optional[str] = None
    deep_oc_sort_device: str = "cpu"
    deep_oc_sort_half: bool = False
    deep_oc_sort_backend: Optional[str] = None  # 'auto' | 'boxmot' | 'fallback'

    alert_config: Optional[AlertConfig] = None

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")
        self.person_categories = [c.lower() for c in self.person_categories]
        if self.target_categories:
            self.target_categories = [c.lower() for c in self.target_categories]

    def validate(self) -> List[str]:
        errors = super().validate()
        if not self.person_categories:
            errors.append("person_categories cannot be empty")
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        return errors


class DeepOCSortUseCase(BaseProcessor):
    CASE_TYPE: Optional[str] = "deep_oc_sort"
    CASE_VERSION: Optional[str] = "1.0"

    def __init__(self) -> None:
        super().__init__("deep_oc_sort")
        self.category = "general"
        self.target_categories: List[str] = ["person", "people", "human"]

        # Tracking + counting state.
        self._tracker = ConfigDrivenTracker()
        self._unique_track_ids: Set[Any] = set()
        self._total_frame_counter = 0
        # Per-threshold-key alert cooldown anchors, stamped with time.monotonic() so a
        # wall-clock step backwards (NTP correction, VM restore) cannot suppress alerts
        # past the cooldown. A missing key means "never emitted" -- checked with an
        # explicit `is None` rather than a 0.0 default, because monotonic() may start
        # near zero and would otherwise gate the first alert.
        self._last_alert_monotonic: Dict[str, float] = {}
        self.start_timer: Optional[str] = None

    # ---- Config plumbing --------------------------------------------------

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.3,
                },
                "person_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["person"],
                },
                "tracking_method": {
                    "type": "string",
                    "default": "deep_oc_sort",
                    "description": "Tracker to run; defaults to DeepOCSORT",
                },
                "deep_oc_sort_backend": {
                    "type": "string",
                    "enum": ["auto", "boxmot", "fallback"],
                    "default": "auto",
                    "description": (
                        "'boxmot' is accepted for backward config compatibility but always "
                        "resolves to the in-repo motion-only fallback -- the boxmot ReID "
                        "backend was removed (AGPL-3.0 licensing)."
                    ),
                },
                "enable_unique_counting": {"type": "boolean", "default": True},
                "alert_config": {
                    "type": "object",
                    "properties": {
                        "count_thresholds": {
                            "type": "object",
                            "additionalProperties": {"type": "integer", "minimum": 1},
                        }
                    },
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": True,
        }

    def create_default_config(self, **overrides: Any) -> DeepOCSortConfig:
        defaults: Dict[str, Any] = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.3,
        }
        defaults.update(overrides)
        return DeepOCSortConfig(**defaults)

    # ---- Main pipeline ----------------------------------------------------

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        start_time = time.time()
        try:
            if not isinstance(config, DeepOCSortConfig):
                return self.create_error_result(
                    "Invalid configuration type for deep_oc_sort",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            if context is None:
                context = ProcessingContext()
            context.input_format = match_results_structure(data)
            context.confidence_threshold = config.confidence_threshold
            context.enable_tracking = True

            processed = self._filter_and_map(data, config)

            # Attach DeepOCSORT track IDs.
            processed = self._tracker.apply(processed, config, stream_info=stream_info, log=self.logger)

            self._total_frame_counter += 1
            current_count = len(processed)

            if config.enable_unique_counting:
                for det in processed:
                    tid = det.get("track_id")
                    if tid is not None and tid != -1:
                        self._unique_track_ids.add(tid)
            unique_total = len(self._unique_track_ids) if config.enable_unique_counting else current_count

            frame_number = self._extract_frame_number(stream_info)
            camera_info = self.get_camera_info_from_stream(stream_info)
            current_ts = self._get_current_timestamp_str(stream_info)

            per_category = self._count_by_category(processed)

            tracking_stats = self._generate_tracking_stats(
                processed,
                per_category,
                current_count,
                unique_total,
                config,
                camera_info,
                current_ts,
                stream_info,
            )
            alerts = self._build_alerts(current_count, per_category, config, frame_number)
            tracking_stats["alerts"] = alerts

            human_text = (
                f"Application Name: {self.CASE_TYPE}\n"
                f"Application Version: {self.CASE_VERSION}\n"
                f"CURRENT FRAME @ {current_ts}: {current_count} people\n"
                f"UNIQUE TOTAL: {unique_total} "
                f"(tracker: {self._active_backend()})"
            )

            frame_key = str(frame_number) if frame_number is not None else "current_frame"
            agg_summary = {
                frame_key: {
                    "incidents": {},
                    "tracking_stats": tracking_stats,
                    "business_analytics": [],
                    "alerts": alerts,
                    "human_text": human_text,
                }
            }

            context.processing_time = time.time() - start_time
            context.mark_completed()
            return self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context,
            )
        except Exception as e:  # noqa: BLE001
            self.logger.error(f"Error in deep_oc_sort processing: {e}", exc_info=True)
            return self.create_error_result(
                f"deep_oc_sort processing failed: {e}",
                error_type="DeepOCSortProcessingError",
                usecase=self.name,
                category=self.category,
                context=context,
            )

    # ---- Stages -----------------------------------------------------------

    def _filter_and_map(self, data: Any, config: DeepOCSortConfig) -> List[Dict]:
        processed = data
        if config.confidence_threshold is not None:
            processed = filter_by_confidence(processed, config.confidence_threshold)
        if config.index_to_category:
            processed = apply_category_mapping(processed, config.index_to_category)
        targets = config.target_categories or self.target_categories
        processed = [d for d in processed if str(d.get("category", "")).lower() in targets]
        return processed

    def _active_backend(self) -> str:
        tracker = getattr(self._tracker, "_tracker", None)
        return getattr(tracker, "backend", "n/a") if tracker is not None else "n/a"

    @staticmethod
    def _extract_frame_number(stream_info: Optional[Dict[str, Any]]) -> Optional[int]:
        if not stream_info:
            return None
        input_settings = stream_info.get("input_settings", {}) or {}
        start = input_settings.get("start_frame")
        end = input_settings.get("end_frame")
        if start is not None and end is not None and start == end:
            return start
        return start

    def _count_by_category(self, detections: List[Dict]) -> Dict[str, int]:
        per_category: Dict[str, int] = {}
        for det in detections:
            cat = str(det.get("category", "person")).lower()
            per_category[cat] = per_category.get(cat, 0) + 1
        return per_category

    def _generate_tracking_stats(
        self,
        detections: List[Dict],
        per_category: Dict[str, int],
        current_count: int,
        unique_total: int,
        config: DeepOCSortConfig,
        camera_info: Dict[str, Any],
        current_ts: str,
        stream_info: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        current_counts = [self.create_count_object(cat, cnt) for cat, cnt in per_category.items()]
        if not current_counts and current_count:
            current_counts = [self.create_count_object("person", current_count)]
        total_counts = [self.create_count_object("person", unique_total)]

        detection_objects = [
            self.create_detection_object(
                det.get("category", "person"),
                det.get("bounding_box", det.get("bbox", {})),
                track_id=det.get("track_id"),
            )
            for det in detections
        ]

        human_text = (
            f"CURRENT FRAME @ {current_ts}:\n"
            f"\t- People in frame: {current_count}\n"
            f"\t- Unique people (total): {unique_total}"
        )

        alert_settings = self._alert_settings_block(config)
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detection_objects,
            human_text=human_text,
            camera_info=camera_info,
            alert_settings=alert_settings,
            reset_settings=_RESET_SETTINGS,
            start_time=self._get_start_timestamp_str(stream_info),
        )
        tracking_stat["target_categories"] = self.target_categories
        tracking_stat["tracking_method"] = config.tracking_method
        return tracking_stat

    def _alert_settings_block(self, config: DeepOCSortConfig) -> List[Dict]:
        ac = config.alert_config
        if not ac:
            return []
        return [
            {
                "alert_type": ac.alert_type or ["Default"],
                "incident_category": self.CASE_TYPE,
                "threshold_level": ac.count_thresholds or {},
                "ascending": True,
                "settings": {t: v for t, v in zip(ac.alert_type or ["Default"], ac.alert_value or ["JSON"])},
            }
        ]

    def _build_alerts(
        self,
        current_count: int,
        per_category: Dict[str, int],
        config: DeepOCSortConfig,
        frame_number: Optional[int],
    ) -> List[Dict]:
        ac = config.alert_config
        if not ac:
            return []
        thresholds = getattr(ac, "count_thresholds", {}) or {}
        if not thresholds:
            return []

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts: List[Dict] = []
        now = time.monotonic()
        for key, threshold in thresholds.items():
            actual = current_count if key == "all" else per_category.get(key, 0)
            if actual >= threshold:
                last = self._last_alert_monotonic.get(key)
                if last is None or now - last >= _ALERT_COOLDOWN_SECONDS:
                    alerts.append(
                        {
                            "alert_type": ac.alert_type or ["Default"],
                            "alert_id": f"alert_{self.CASE_TYPE}_{key}_{frame_key}",
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "count": actual,
                            "ascending": True,
                            "settings": {
                                t: v for t, v in zip(ac.alert_type or ["Default"], ac.alert_value or ["JSON"])
                            },
                        }
                    )
                    self._last_alert_monotonic[key] = now
        return alerts

    # ---- Timestamp helpers ------------------------------------------------

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        if stream_info:
            stream_time = stream_info.get("input_settings", {}).get("stream_time")
            if stream_time and stream_time != "NA":
                cleaned = str(stream_time).replace(" UTC", "")
                try:
                    return datetime.strptime(cleaned, "%Y-%m-%d-%H:%M:%S.%f").strftime("%Y:%m:%d %H:%M:%S")
                except ValueError:
                    pass
        return datetime.now(timezone.utc).strftime("%Y:%m:%d %H:%M:%S")

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        if self.start_timer is None:
            candidate = None
            if stream_info:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
        return self.start_timer
