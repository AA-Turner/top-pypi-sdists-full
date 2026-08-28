"""
Accident Detection Use Case for Post-Processing.

Model: X3D whole-clip/frame video classifier (no bounding boxes, no
per-object track IDs). Each ``process()`` call corresponds to one source
video frame and carries a single classification result, e.g.:

    {
        "classification0": {
            "type": "classification",
            "data": {
                ...,
                "predictions": [
                    {"class_id": 0, "category": "class_0", "confidence": 0.68},
                    {"class_id": 1, "category": "class_1", "confidence": 0.32},
                ],
                "top_prediction": {"class_id": 0, "category": "class_0", "confidence": 0.68, "stabilized": True},
            },
        },
    }

Only ``data.top_prediction.class_id`` is used to decide the category for
that frame -- ``class_id`` is mapped to a real label via
``config.index_to_category`` (``top_prediction.category`` is a generic
placeholder like ``"class_0"``, not a usable label on its own). Entries may
also be an object exposing a ``.data`` attribute instead of a ``"data"``
dict key. A flattened ``{"label": ..., "confidence": ...}`` shape is
supported as a fallback for compatibility with simpler callers.

Classes:
- accident (target category — drives incidents/alerts/analytics)
- normal (background class; frames labelled "normal" are treated as a miss)

Without bounding boxes there is no object identity to track, so "how many
accidents" is derived from a debounced presence signal instead of unique
track IDs: a category must be detected for ``confirm_frames`` worth of
*continuous* frames (measured via ``stream_time``/``original_fps``, not raw
call count, so it stays correct even if inference cadence changes) before
it is considered a confirmed accident. A confirmed episode tolerates brief
flicker and only ends after ``break_frames`` worth of continuous misses;
reappearing after such a break starts a new episode.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
    ResultFormat,
)
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_confidence

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class AccidentDetectionConfig(BaseConfig):
    """Configuration for accident detection post-processing (X3D classifier)."""

    confidence_threshold: float = 0.15

    zone_config: Optional[Dict[str, List[List[float]]]] = None

    usecase_categories: List[str] = field(default_factory=lambda: ["accident", "normal"])
    target_categories: List[str] = field(default_factory=lambda: ["accident"])

    # Fire an alert as soon as an accident episode is confirmed.
    alert_config: Optional[AlertConfig] = field(default_factory=lambda: AlertConfig(count_thresholds={"accident": 1}))

    # MUST mirror the model's EngineConfig.index_to_category EXACTLY — the X3D
    # accident model emits class_id 0 = "accident", 1 = "normal", so the app's
    # filtering map has to match or class_ids get relabelled to the wrong
    # category (accident<->normal flip) whenever the model emits bare class_N
    # placeholders instead of real label strings.
    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "accident", 1: "normal"})

    # Debounce thresholds for the bbox-free presence signal (see module
    # docstring). Expressed as frame-equivalents and converted to a
    # stream-time duration via ``original_fps`` (falls back to ``default_fps``
    # when the stream doesn't report one).
    confirm_frames: int = 15
    break_frames: int = 15
    default_fps: float = 30.0


# ---------------------------------------------------------------------------
# Processor
# ---------------------------------------------------------------------------


class AccidentDetectionUseCase(BaseProcessor):
    """Post-processor for X3D accident-classification model outputs."""

    CATEGORY_DISPLAY: Dict[str, str] = {"accident": "Accident", "normal": "Normal"}

    def __init__(self) -> None:
        super().__init__("accident_detection")
        self.category: str = "traffic"
        self.CASE_TYPE: Optional[str] = "accident_detection"
        self.CASE_VERSION: Optional[str] = "2.0"

        self.target_categories: List[str] = ["accident"]

        # Debounced presence state, keyed by category (only "accident" is
        # populated in practice). See ``_update_presence_state``.
        self._presence_state: Dict[str, Dict[str, Any]] = {}

        self._total_frame_counter: int = 0
        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"
        self._episode_start_ts_str: Optional[str] = None
        self.start_timer: Optional[str] = None
        self._tracking_start_time: Optional[float] = None

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def process(
        self,
        data: Any = None,
        config: ConfigProtocol = None,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """Run the accident-classification post-processing pipeline for one frame.

        Args:
            data: Raw X3D classification output for this frame (see module
                docstring for shape).
            config: Must be an :class:`AccidentDetectionConfig` instance.
            context: Optional processing context carrying metadata.
            stream_info: Stream/video metadata used for timestamps and the
                debounce clock (``stream_time`` / ``original_fps``).

        Returns:
            :class:`ProcessingResult` containing the ``agg_summary`` payload.
        """
        processing_start = time.time()

        is_valid_config = isinstance(config, AccidentDetectionConfig) or (
            hasattr(config, "usecase")
            and config.usecase == "accident_detection"
            and hasattr(config, "category")
            and config.category == "traffic"
        )
        if not is_valid_config:
            self.logger.error(
                f"Config validation failed in accident_detection. "
                f"Got type={type(config).__name__}, module={type(config).__module__}, "
                f"usecase={getattr(config, 'usecase', 'N/A')}, "
                f"category={getattr(config, 'category', 'N/A')}"
            )
            return self.create_error_result(
                f"Invalid config type: expected AccidentDetectionConfig or config with "
                f"usecase='accident_detection', got {type(config).__name__} with "
                f"usecase={getattr(config, 'usecase', 'N/A')}",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        if context is None:
            context = ProcessingContext()

        # Normalise the X3D classification payload -- no bboxes, no track IDs.
        classifications = self._normalize_x3d_results(data)
        self.logger.debug(f"[accident_detection] normalized_input={classifications}")

        context.input_format = ResultFormat.CLASSIFICATION
        context.confidence_threshold = config.confidence_threshold

        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(classifications, config.confidence_threshold)
        else:
            processed_data = classifications

        if config.index_to_category:
            processed_data = apply_category_mapping(processed_data, config.index_to_category)

        if config.target_categories:
            processed_data = [d for d in processed_data if d.get("category") in config.target_categories]

        self._total_frame_counter += 1

        # Resolve frame number from stream_info when available.
        frame_number: Optional[int] = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        current_time, fps = self._resolve_stream_clock(stream_info, config.default_fps)
        is_hit = len(processed_data) > 0
        state = self._update_presence_state(is_hit, current_time, fps, config.confirm_frames, config.break_frames)

        counting_summary = self._count_categories(processed_data, state)
        zone_analysis = self._compute_global_zone_analysis(state)

        # Downstream outputs
        alerts = self._check_alerts(counting_summary, frame_number, config)
        incidents_list = self._generate_incidents(
            counting_summary, state, alerts, config, frame_number, stream_info
        )
        tracking_stats_list = self._generate_tracking_stats(
            counting_summary, zone_analysis, alerts, config, frame_number, stream_info, state
        )
        business_analytics_list = self._generate_business_analytics(
            counting_summary, alerts, config, stream_info, is_empty=True
        )
        summary_list = self._generate_summary(
            counting_summary,
            incidents_list,
            tracking_stats_list,
            business_analytics_list,
            alerts,
        )

        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = business_analytics_list[0] if business_analytics_list else {}
        summary = summary_list[0] if summary_list else {}

        agg_summary = {
            str(frame_number): {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "zone_analysis": zone_analysis,
                "human_text": summary,
            }
        }

        context.mark_completed()
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )

        proc_time = time.time() - processing_start
        self.logger.debug(
            f"[accident_detection] latency_ms={proc_time * 1000.0:.2f} "
            f"frame_number={self._total_frame_counter}"
        )
        return result

    # ------------------------------------------------------------------
    # X3D classification normalisation
    # ------------------------------------------------------------------

    def _normalize_x3d_results(self, data: Any) -> List[Dict[str, Any]]:
        """Normalise X3D classification output to ``[{category, confidence}, ...]``.

        Accepts a dict of ``TypedOutput``-like entries (e.g. keyed
        ``"classification0"``, ``"classification1"``, ...), a single such
        entry, or a plain list of them. Each entry's payload is read off
        ``.data`` (attribute or dict key) and only ``label``/``confidence``
        are used -- ``top_k``/``classifications`` are ignored by design.
        No bounding box or track ID is ever synthesised.

        Args:
            data: Raw model output for the current frame.

        Returns:
            List of ``{"category": str, "confidence": float}`` dicts.
        """

        def extract(entry: Any) -> Optional[Dict[str, Any]]:
            payload = entry
            if hasattr(entry, "data"):
                payload = entry.data
            elif isinstance(entry, dict) and isinstance(entry.get("data"), dict):
                payload = entry["data"]
            if not isinstance(payload, dict):
                return None

            category: Any = None
            confidence: Any = 0.0

            # Real model-codebase shape: data.top_prediction = {class_id,
            # category, confidence, stabilized}. "category" there is a
            # generic placeholder (e.g. "class_0") -- class_id is what
            # actually maps to a real label via config.index_to_category.
            top_prediction = payload.get("top_prediction")
            if isinstance(top_prediction, dict):
                if top_prediction.get("class_id") is not None:
                    category = top_prediction.get("class_id")
                elif top_prediction.get("category") is not None:
                    category = top_prediction.get("category")
                confidence = top_prediction.get("confidence", 0.0)

            # Fallback: flattened {label, confidence} shape.
            if category is None:
                label = payload.get("label", payload.get("category"))
                if label is not None:
                    category = label
                    confidence = payload.get("confidence", payload.get("score", 0.0))

            if category is None:
                return None

            try:
                confidence = float(confidence)
            except (TypeError, ValueError):
                confidence = 0.0
            return {"category": str(category), "confidence": confidence}

        if data is None:
            return []

        if isinstance(data, dict):
            if "label" in data or isinstance(data.get("data"), dict):
                entries: List[Any] = [data]
            else:
                entries = list(data.values())
        elif isinstance(data, list):
            entries = data
        else:
            entries = [data]

        normalized: List[Dict[str, Any]] = []
        for entry in entries:
            extracted = extract(entry)
            if extracted is not None:
                normalized.append(extracted)
        return normalized

    # ------------------------------------------------------------------
    # Stream clock / debounced presence tracking
    # ------------------------------------------------------------------

    def _parse_stream_time(self, value: Any) -> Optional[float]:
        """Parse a ``stream_time`` value (``YYYY-MM-DD-HH:MM:SS.ffffff UTC`` or
        numeric) into a Unix epoch float, or ``None`` if unparseable."""
        if value is None or value == "NA":
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            cleaned = value.replace(" UTC", "").strip()
            try:
                dt = datetime.strptime(cleaned, "%Y-%m-%d-%H:%M:%S.%f")
                return dt.replace(tzinfo=timezone.utc).timestamp()
            except Exception:
                return None
        return None

    def _resolve_stream_clock(
        self,
        stream_info: Optional[Dict[str, Any]],
        default_fps: float,
    ) -> Tuple[float, float]:
        """Resolve ``(current_time_seconds, fps)`` for the debounce math.

        Uses the video-source ``stream_time`` rather than a local call
        counter, so confirm/break windows stay correct in real video-time
        even if the inference pipeline's call cadence changes (skipped
        frames, variable inference speed, duplicated per-frame calls, etc).
        Falls back to wall-clock time only when no usable ``stream_time`` is
        present (e.g. first-ever call or malformed stream_info).
        """
        fps = default_fps
        stream_time_val = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {}) or {}
            fps = input_settings.get("original_fps") or stream_info.get("original_fps") or fps
            stream_time_val = input_settings.get("stream_time") or stream_info.get("stream_time")
        parsed = self._parse_stream_time(stream_time_val)
        if parsed is None:
            parsed = time.time()
        return parsed, float(fps) if fps else default_fps

    def _update_presence_state(
        self,
        is_hit: bool,
        current_time: float,
        fps: float,
        confirm_frames: int,
        break_frames: int,
    ) -> Dict[str, Any]:
        """Debounced presence tracking for the bbox-free "accident" category.

        An episode is confirmed only after ``confirm_frames`` worth of
        *continuous* hits (any miss during build-up restarts the count from
        zero -- "continuous" is taken literally). Once confirmed, brief
        misses (flicker) are tolerated; the episode only ends after
        ``break_frames`` worth of *continuous* misses. Reappearing after
        such a break starts a brand-new episode: a fresh "new" pulse and
        +1 on the cumulative total. All durations are measured in real
        stream-time (via ``fps``), not raw call count.
        """
        cat = "accident"
        state = self._presence_state.setdefault(
            cat,
            {
                "streak_start": None,
                "miss_start": None,
                "confirmed": False,
                "total_count": 0,
                "episode_start": None,
                "new_this_frame": False,
                "ended_this_frame": False,
                "last_time": None,
            },
        )
        state["new_this_frame"] = False
        state["ended_this_frame"] = False

        effective_fps = fps if fps and fps > 0 else 30.0
        confirm_duration = confirm_frames / effective_fps
        break_duration = break_frames / effective_fps

        if is_hit:
            state["miss_start"] = None
            if state["streak_start"] is None:
                state["streak_start"] = current_time
            streak_duration = max(0.0, current_time - state["streak_start"])
            if not state["confirmed"] and streak_duration >= confirm_duration:
                state["confirmed"] = True
                state["total_count"] += 1
                state["new_this_frame"] = True
                state["episode_start"] = state["streak_start"]
        else:
            state["streak_start"] = None
            if state["confirmed"]:
                if state["miss_start"] is None:
                    state["miss_start"] = current_time
                miss_duration = max(0.0, current_time - state["miss_start"])
                if miss_duration >= break_duration:
                    state["confirmed"] = False
                    state["ended_this_frame"] = True
                    state["episode_start"] = None
                    state["miss_start"] = None

        state["last_time"] = current_time
        return state

    # ------------------------------------------------------------------
    # Zone analysis (structural placeholder -- no bbox to geometrically
    # assign a zone; reports a single global bucket, mirroring the
    # no-zones-configured fallback used by people_counting.py)
    # ------------------------------------------------------------------

    def _compute_global_zone_analysis(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "__global__": {
                "current_count": 1 if state.get("confirmed") else 0,
                "total_count": state.get("total_count", 0),
            }
        }

    # ------------------------------------------------------------------
    # Alerts
    # ------------------------------------------------------------------

    def _check_alerts(
        self,
        summary: Dict[str, Any],
        frame_number: Any,
        config: AccidentDetectionConfig,
    ) -> List[Dict[str, Any]]:
        """Evaluate alert thresholds for the current frame.

        An alert is generated once an accident episode is confirmed (default
        threshold: 1) and stays active every frame while it remains confirmed.

        Args:
            summary: Counting summary produced by ``_count_categories``.
            frame_number: Current frame index or ``None``.
            config: Use-case configuration with ``alert_config``.

        Returns:
            List of alert dicts (may be empty).
        """

        def get_trend(data: List[int], lookback: int = 900, threshold: float = 0.6) -> bool:
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True
            increasing = sum(1 for i in range(1, len(window)) if window[i] >= window[i - 1])
            return (increasing / (len(window) - 1)) >= threshold

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts: List[Dict[str, Any]] = []

        if not config.alert_config:
            return alerts

        total_detections = summary.get("total_count", 0)
        per_category_count = summary.get("per_category_count", {})

        if not (hasattr(config.alert_config, "count_thresholds") and config.alert_config.count_thresholds):
            return alerts

        for category, threshold in config.alert_config.count_thresholds.items():
            triggered = False
            if category == "all" and total_detections >= threshold:
                triggered = True
            elif category in per_category_count and per_category_count[category] >= threshold:
                triggered = True

            if triggered:
                alerts.append(
                    {
                        "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                        "alert_id": f"alert_{category}_{frame_key}",
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list, lookback=900, threshold=0.8),
                        "settings": {
                            t: v
                            for t, v in zip(
                                getattr(config.alert_config, "alert_type", ["Default"]),
                                getattr(config.alert_config, "alert_value", ["JSON"]),
                            )
                        },
                    }
                )
        return alerts

    # ------------------------------------------------------------------
    # Incidents
    # ------------------------------------------------------------------

    def _generate_incidents(
        self,
        _counting_summary: Dict[str, Any],
        state: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: AccidentDetectionConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Generate the incident record for the current frame, if confirmed.

        Severity is always ``"critical"`` -- an accident is inherently a
        critical event, so there is no lower-severity tier to escalate from
        (unlike count-based use cases where severity scales with how many
        objects are involved).

        Args:
            counting_summary: Frame-level counting summary (unused directly;
                kept for signature parity).
            state: Debounced presence state from ``_update_presence_state``.
            alerts: Alerts generated for this frame.
            config: Use-case configuration.
            frame_number: Current frame index.
            stream_info: Stream metadata.

        Returns:
            List containing a single incident dict (empty dict if no
            confirmed accident episode is active this frame).
        """
        _ = (_counting_summary,)
        incidents: List[Dict[str, Any]] = []
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)
        display_cat = self._display_category("accident")

        if state.get("new_this_frame"):
            self._episode_start_ts_str = current_timestamp
            self.current_incident_end_timestamp = "Incident still active"
        if state.get("ended_this_frame"):
            self.current_incident_end_timestamp = current_timestamp

        if state.get("confirmed"):
            episode_start = state.get("episode_start")
            last_time = state.get("last_time")
            elapsed_seconds = (
                max(0.0, last_time - episode_start) if episode_start is not None and last_time is not None else 0.0
            )
            level = "critical"
            self._ascending_alert_list.append(3)

            human_text_lines = [f"ACCIDENT INCIDENT DETECTED @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE, level)}")
            human_text_lines.append(f"\t{display_cat} ongoing for ~{elapsed_seconds:.1f}s")
            human_text = "\n".join(human_text_lines)

            alert_settings: List[Dict[str, Any]] = []
            if config.alert_config and hasattr(config.alert_config, "alert_type"):
                alert_settings.append(
                    {
                        "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": (
                            config.alert_config.count_thresholds
                            if hasattr(config.alert_config, "count_thresholds")
                            else {}
                        ),
                        "ascending": True,
                        "settings": {
                            t: v
                            for t, v in zip(
                                getattr(config.alert_config, "alert_type", ["Default"]),
                                getattr(config.alert_config, "alert_value", ["JSON"]),
                            )
                        },
                    }
                )

            event = self.create_incident(
                incident_id=f"{self.CASE_TYPE}_{frame_number}",
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=self._episode_start_ts_str or current_timestamp,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 5, "critical": 8},
            )
            incidents.append(event)
        else:
            self._ascending_alert_list.append(0)
            incidents.append({})

        self._ascending_alert_list = self._ascending_alert_list[-900:]
        return incidents

    # ------------------------------------------------------------------
    # Tracking statistics
    # ------------------------------------------------------------------

    def _generate_tracking_stats(
        self,
        counting_summary: Dict[str, Any],
        zone_analysis: Dict[str, Any],
        alerts: List[Dict[str, Any]],
        config: AccidentDetectionConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        state: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Build tracking statistics for the current frame.

        Without bounding boxes/track IDs, ``total_counts``/``current_counts``/
        ``current_new_counts`` are derived from the debounced presence
        ``state`` (confirmed episode count) instead of unique-track sets.

        Args:
            counting_summary: Frame-level counting summary.
            zone_analysis: Global zone-analysis bucket (see
                ``_compute_global_zone_analysis``).
            alerts: Active alerts for this frame.
            config: Use-case configuration.
            frame_number: Current frame index.
            stream_info: Stream metadata.
            state: Debounced presence state.

        Returns:
            Single-element list with a tracking stats dict.
        """
        camera_info = self.get_camera_info_from_stream(stream_info)
        tracking_stats: List[Dict[str, Any]] = []
        state = state or {}
        display_cat = self._display_category("accident")

        confirmed = bool(state.get("confirmed"))
        new_flag = bool(state.get("new_this_frame"))
        total_count = state.get("total_count", 0)

        current_timestamp = self._get_current_timestamp_str(stream_info, precision=False)
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

        # Always report the target category explicitly, even at count 0 --
        # downstream consumers should see "Accident: 0", not an empty list.
        total_counts = [{"category": display_cat, "count": total_count}]
        current_counts = [{"category": display_cat, "count": 1 if confirmed else 0}]
        current_new_counts = [{"category": display_cat, "count": 1 if new_flag else 0}]

        detections_output: List[Dict[str, Any]] = [
            {"classification": {"category": display_cat}} for _ in counting_summary.get("detections", [])
        ]

        alert_settings: List[Dict[str, Any]] = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": getattr(config.alert_config, "alert_type", ["Default"]),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": (
                        config.alert_config.count_thresholds if hasattr(config.alert_config, "count_thresholds") else {}
                    ),
                    "ascending": True,
                    "settings": {
                        t: v
                        for t, v in zip(
                            getattr(config.alert_config, "alert_type", ["Default"]),
                            getattr(config.alert_config, "alert_value", ["JSON"]),
                        )
                    },
                }
            )

        human_text_lines: List[str] = [f"CURRENT FRAME @ {current_timestamp}:"]
        human_text_lines.append(f"\t- {display_cat} Status: {'CONFIRMED (ongoing)' if confirmed else 'not detected'}")
        human_text_lines.append(f"\t- New {display_cat} this frame: {'yes' if new_flag else 'no'}")
        human_text_lines.append(f"\t- Total {display_cat} episodes since start: {total_count}")
        human_text_lines.append("")
        human_text = "\n".join(human_text_lines)

        reset_settings = [{"interval_type": "daily", "reset_time": {"value": 0, "time_unit": "hour"}}]
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections_output,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings,
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp,
        )
        tracking_stat["target_categories"] = self.target_categories
        tracking_stat["current_new_counts"] = current_new_counts
        # Legacy-bridge alias (mirrors people_counting.py / car_damage_detection.py).
        tracking_stat["total_current_counts"] = list(current_counts)
        tracking_stat["zone_analysis"] = zone_analysis or {}
        tracking_stats.append(tracking_stat)
        return tracking_stats

    # ------------------------------------------------------------------
    # Business analytics
    # ------------------------------------------------------------------

    def _generate_business_analytics(
        self,
        _counting_summary: Dict[str, Any],
        _alerts: Any,
        _config: AccidentDetectionConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty: bool = False,
    ) -> List[Dict[str, Any]]:
        """Return business analytics payload.

        Currently returns an empty list -- accident detection does not
        require business KPIs. Override to add custom analytics.
        """
        _ = (_alerts, _config, _counting_summary, _stream_info, is_empty)
        return []

    # ------------------------------------------------------------------
    # Human-readable summary
    # ------------------------------------------------------------------

    def _generate_summary(
        self,
        _summary: Dict[str, Any],
        incidents: List[Dict[str, Any]],
        tracking_stats: List[Dict[str, Any]],
        business_analytics: List[Dict[str, Any]],
        _alerts: List[Dict[str, Any]],
    ) -> List[str]:
        """Assemble a human-readable summary string for the frame."""
        _ = (_alerts, _summary)
        lines: List[str] = [
            f"Application Name: {self.CASE_TYPE}",
            f"Application Version: {self.CASE_VERSION}",
        ]
        if incidents and incidents[0]:
            lines.append("Incidents: \n\t" + incidents[0].get("human_text", "No incidents detected"))
        if tracking_stats:
            lines.append(
                "Tracking Statistics: \t" + tracking_stats[0].get("human_text", "No tracking statistics detected")
            )
        if business_analytics:
            lines.append(
                "Business Analytics: \t" + business_analytics[0].get("human_text", "No business analytics detected")
            )
        if (not incidents or not incidents[0]) and not tracking_stats and not business_analytics:
            lines.append("Summary: No Summary Data")

        return ["\n".join(lines)]

    # ------------------------------------------------------------------
    # Presence-state accessors (kept for API parity with other usecases)
    # ------------------------------------------------------------------

    def get_total_counts(self) -> Dict[str, int]:
        """Return cumulative confirmed-episode counts per category."""
        return {cat: state.get("total_count", 0) for cat, state in self._presence_state.items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Return 1 for categories whose episode was newly confirmed this frame."""
        return {cat: (1 if state.get("new_this_frame") else 0) for cat, state in self._presence_state.items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        """Return 1 for categories with a currently-confirmed episode."""
        return {cat: (1 if state.get("confirmed") else 0) for cat, state in self._presence_state.items()}

    # ------------------------------------------------------------------
    # Counting helpers
    # ------------------------------------------------------------------

    def _display_category(self, category: str) -> str:
        return self.CATEGORY_DISPLAY.get(category, category.capitalize())

    def _count_categories(self, detections: List[Dict[str, Any]], state: Dict[str, Any]) -> Dict[str, Any]:
        """Build the frame-level counting summary from the confirmed state.

        ``total_count``/``per_category_count`` reflect whether an accident
        episode is currently *confirmed* (debounced), not the raw per-frame
        classification hit -- this is what alert thresholds key off.

        Args:
            detections: Filtered, normalised classification list for this
                frame (raw hits, pre-debounce).
            state: Debounced presence state from ``_update_presence_state``.

        Returns:
            Dict with ``total_count``, ``per_category_count``, and
            ``detections`` keys.
        """
        confirmed = bool(state.get("confirmed"))
        return {
            "total_count": 1 if confirmed else 0,
            "per_category_count": {"accident": 1} if confirmed else {},
            "detections": [{"category": det.get("category", "accident")} for det in detections],
        }

    # ------------------------------------------------------------------
    # Timestamp utilities
    # ------------------------------------------------------------------

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to ``YYYY:MM:DD HH:MM:SS``.

        Accepts a numeric Unix timestamp or a string in the form
        ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.

        Args:
            timestamp: Source timestamp value.

        Returns:
            Formatted string ``YYYY:MM:DD HH:MM:SS``.
        """
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime("%Y:%m:%d %H:%M:%S")

        if not isinstance(timestamp, str):
            return str(timestamp)

        timestamp_clean = timestamp.replace(" UTC", "").strip()
        if "." in timestamp_clean:
            timestamp_clean = timestamp_clean.split(".")[0]

        try:
            if timestamp_clean.count("-") >= 2:
                parts = timestamp_clean.split("-")
                if len(parts) >= 4:
                    return f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
        except Exception:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision: bool = False,
        frame_id: Optional[str] = None,
    ) -> str:
        """Return a formatted current-frame timestamp string.

        Args:
            stream_info: Stream metadata dict.
            precision: If ``True``, return microsecond-precision ISO timestamp.
            frame_id: Optional explicit frame ID override.

        Returns:
            Formatted timestamp string.
        """
        if not stream_info:
            return "00:00:00.00"

        input_settings = stream_info.get("input_settings", {})

        if precision:
            if input_settings.get("start_frame", "na") != "na":
                return self._format_timestamp(input_settings.get("stream_time", "NA"))
            return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if input_settings.get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id) / input_settings.get("original_fps", 30)
            else:
                start_time = input_settings.get("start_frame", 30) / input_settings.get("original_fps", 30)
            _ = self._format_timestamp_for_video(start_time)
            return self._format_timestamp(input_settings.get("stream_time", "NA"))

        stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
        if stream_time_str:
            try:
                ts_clean = stream_time_str.replace(" UTC", "")
                dt = datetime.strptime(ts_clean, "%Y-%m-%d-%H:%M:%S.%f")
                timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                return self._format_timestamp_for_stream(timestamp)
            except Exception:
                return self._format_timestamp_for_stream(time.time())
        return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision: bool = False,
    ) -> str:
        """Return a formatted start-of-session timestamp string.

        Args:
            stream_info: Stream metadata dict.
            precision: If ``True``, return microsecond-precision ISO timestamp.

        Returns:
            Formatted timestamp string.
        """
        if not stream_info:
            return "00:00:00"

        input_settings = stream_info.get("input_settings", {})

        if precision:
            if self.start_timer is None:
                candidate = input_settings.get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
            elif input_settings.get("start_frame", "na") == 1:
                candidate = input_settings.get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
            return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            candidate = input_settings.get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = input_settings.get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        ts_clean = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(ts_clean, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime(
                            "%Y-%m-%d-%H:%M:%S.%f UTC"
                        )
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)

        if input_settings.get("start_frame", "na") == 1:
            candidate = input_settings.get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = input_settings.get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        ts_clean = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(ts_clean, "%Y-%m-%d-%H:%M:%S.%f")
                        ts = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except Exception:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)

        if self.start_timer is not None and self.start_timer != "NA":
            return self._format_timestamp(self.start_timer)

        if self._tracking_start_time is None:
            stream_time_str = input_settings.get("stream_info", {}).get("stream_time", "")
            if stream_time_str:
                try:
                    ts_clean = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(ts_clean, "%Y-%m-%d-%H:%M:%S.%f")
                    self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                except Exception:
                    self._tracking_start_time = time.time()
            else:
                self._tracking_start_time = time.time()

        dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
        dt = dt.replace(minute=0, second=0, microsecond=0)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _get_tracking_start_time(self) -> str:
        """Return the session start time as a formatted string."""
        if self._tracking_start_time is None:
            return "N/A"
        return self._format_timestamp(self._tracking_start_time)

    def _set_tracking_start_time(self) -> None:
        """Capture the current wall-clock time as the tracking session start."""
        self._tracking_start_time = time.time()
