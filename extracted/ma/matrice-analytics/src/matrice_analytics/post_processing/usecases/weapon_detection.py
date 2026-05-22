"""
Weapon Detection use case (single-camera).

Transforms raw detections into severity-graded incidents, alerts, and tracking
stats. Structured after the fire_detection active pattern:
  - state machines lifted into IncidentIdTracker
  - deduplicated alert-dict / severity-level logic extracted to helpers
  - single-camera assumption collapses camera_id resolution to a constant
  - adds min_confirmation_frames: N consecutive frames of sustained detection
    required before an incident is emitted (default 5; set to 1 to disable)

Category set is reduced to two classes: {0: "weapon", 1: "person"}.
"""

import re
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..core.config import AlertConfig, BaseConfig
from ..utils import (
    BBoxSmoothingConfig,
    BBoxSmoothingTracker,
    apply_category_mapping,
    bbox_smoothing,
    filter_by_confidence,
    match_results_structure,
)
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# ============================================================================
# Constants
# ============================================================================

# Severity cutoffs on intensity (0-10 scale; ordered high→low; first match wins).
_SEVERITY_CUTOFFS: Tuple[Tuple[str, float], ...] = (
    ("critical", 9.0),
    ("significant", 7.0),
    ("medium", 5.0),
)
_LEVEL_SETTINGS = {"low": 1, "medium": 3, "significant": 4, "critical": 7}
_RESET_SETTINGS = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]

# Trend window used by both _check_alerts and _generate_incidents.
_TREND_LOOKBACK = 23
_TREND_PRIOR = 14

# IncidentIdTracker state-machine thresholds.
_HIT_CONFIRM_FRAMES = 7
_EMPTY_RESET_FRAMES = 130

# Rolling-buffer caps.
_ALERT_HISTORY_CAP = 5000

# Single-camera identifier published to the incident manager.
_DEFAULT_CAMERA_ID = "camera"

# Default alert channel used when alert_config is missing.
_DEFAULT_ALERT_CONFIG_KWARGS = dict(
    count_thresholds={"all": 1},
    alert_type=["email"],
    alert_value=["WEAPON_INFO@matrice.ai"],
    alert_incident_category=["WEAPON-ALERT"],
)


# ============================================================================
# Config
# ============================================================================


@dataclass
class WeaponDetectionConfig(BaseConfig):
    confidence_threshold: float = 0.28

    weapon_categories: List[str] = field(default_factory=lambda: ["weapon"])
    target_categories: List[str] = field(default_factory=lambda: ["weapon", "person"])

    alert_config: Optional[AlertConfig] = field(default_factory=lambda: AlertConfig(**_DEFAULT_ALERT_CONFIG_KWARGS))

    index_to_category: Optional[Dict[int, str]] = field(default_factory=lambda: {0: "weapon", 1: "person"})

    # BBox smoothing.
    enable_smoothing: bool = True
    smoothing_algorithm: str = "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # Count baseline mapped to 100 % (i.e. intensity 10).
    threshold_count: int = 15

    # Consecutive frames of sustained detection required before emitting an
    # incident. Set to 1 to disable confirmation gating.
    min_confirmation_frames: int = 5

    # Incident-manager wiring.
    session: Optional[Any] = None
    server_id: Optional[str] = None

    def __post_init__(self):
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")
        self.weapon_categories = [c.lower() for c in self.weapon_categories]
        if self.index_to_category:
            self.index_to_category = {k: v.lower() for k, v in self.index_to_category.items()}
        if self.target_categories:
            self.target_categories = [c.lower() for c in self.target_categories]


# ============================================================================
# Pure helpers
# ============================================================================


def _level_from_intensity(intensity: float) -> str:
    for level, cutoff in _SEVERITY_CUTOFFS:
        if intensity >= cutoff:
            return level
    return "low"


def _compute_intensity(total_detections: int, threshold_count: int) -> float:
    if threshold_count <= 0:
        return 10.0 if total_detections > 0 else 0.0
    return min(10.0, (total_detections / threshold_count) * 10.0)


def _trend_windows(history: List[str]) -> Optional[Tuple[str, str]]:
    """
    Return (older_dominant, newer_dominant) over the lookback window, or None
    if the history is too short.
    """
    if len(history) < _TREND_LOOKBACK:
        return None
    post = _TREND_LOOKBACK - _TREND_PRIOR - 1
    older = history[-_TREND_LOOKBACK:][:-_TREND_PRIOR]
    newer = history[-post:]
    older_dom = Counter(older).most_common(1)[0][0]
    newer_dom = Counter(newer).most_common(1)[0][0]
    return older_dom, newer_dom


def _is_trend_ascending(history: List[str]) -> bool:
    pair = _trend_windows(history)
    if pair is None:
        return True
    ring = ["low", "medium", "significant", "critical", "low"]
    older_dom, newer_dom = pair
    return ring.index(older_dom) <= ring.index(newer_dom)


def _alert_settings_dict(alert_config: Optional[AlertConfig]) -> Dict[str, str]:
    if not alert_config:
        return {}
    types = alert_config.alert_type or ["Default"]
    values = alert_config.alert_value or ["JSON"]
    return {t: v for t, v in zip(types, values)}


# ============================================================================
# Incident-id state machine
# ============================================================================


class IncidentIdTracker:
    """
    Tracks severity-level progression across frames to produce monotonically
    increasing incident/alert IDs (7 frames to advance a level; 130 empty
    frames to close an incident).
    """

    _HIT_CYCLE = ["low", "medium", "significant", "critical", "low"]

    def __init__(self):
        self.id_hit_list: List[str] = list(self._HIT_CYCLE)
        self.id_hit_counter: int = 0
        self.latest_stack: Optional[str] = None
        self.id_timing_list: List[str] = []
        self.return_id_counter: int = 1

    def advance(self, sev_level: str, current_ts: str) -> Tuple[int, int]:
        """
        Feed a severity level ("" if no detection). Returns (rank_id, alert_id).
        """
        if sev_level != "":
            if sev_level == self.id_hit_list[0] and len(self.id_hit_list) >= 2:
                self.id_hit_counter += 1
                if self.id_hit_counter > _HIT_CONFIRM_FRAMES:
                    self.latest_stack = self.id_hit_list[0]
                    self.id_hit_list.pop(0)
                    self.id_hit_counter = 0
                    self.id_timing_list.append(current_ts)
                    return (5 - len(self.id_hit_list), self.return_id_counter)
            elif self.id_hit_counter > 0:
                self.id_hit_counter -= 1
            elif self.id_hit_counter < 0:
                self.id_hit_counter = 0

            if len(self.id_hit_list) > 1:
                if sev_level == self.latest_stack:
                    return (5 - len(self.id_hit_list), self.return_id_counter)
                return (0, 0)
        else:
            if len(self.id_hit_list) == 1:
                self.id_hit_counter += 1
                if self.id_hit_counter > _EMPTY_RESET_FRAMES:
                    self.id_hit_list = list(self._HIT_CYCLE)
                    pre_return_id = self.return_id_counter
                    self.return_id_counter += 1
                    self.id_hit_counter = 0
                    self.latest_stack = None
                    self.id_timing_list.append(current_ts)
                    return (5, pre_return_id)
                if sev_level == self.latest_stack:
                    return (5 - len(self.id_hit_list), self.return_id_counter)
                return (0, 0)
            elif self.id_hit_counter > 0:
                self.id_hit_counter -= 1
            elif self.id_hit_counter < 0:
                self.id_hit_counter = 0

        return (1, 1)


# ============================================================================
# Use case
# ============================================================================


class WeaponDetectionUseCase(BaseProcessor):
    CASE_TYPE: Optional[str] = "weapon_detection"
    CASE_VERSION: Optional[str] = "1.2"
    _INCIDENT_LOG = "[INCIDENT_MANAGER]"

    def __init__(self):
        super().__init__("weapon_detection")
        self.category = "security"

        self.target_categories: List[str] = ["weapon", "person"]

        # Rolling state.
        self.smoothing_tracker: Optional[BBoxSmoothingTracker] = None
        self._ascending_alert_list: List[str] = []
        self._consecutive_weapon_frames: int = 0
        self.current_incident_end_timestamp: str = "N/A"
        self.start_timer = None
        self._tracking_start_time = None

        # Incident-id state machine.
        self._id_tracker = IncidentIdTracker()

        # Incident manager.
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False

    # ---- Incident manager lifecycle ---------------------------------------

    def _initialize_incident_manager_once(self, config: WeaponDetectionConfig) -> None:
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info(f"{self._INCIDENT_LOG} Initializing incident manager for weapon detection...")
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info(f"{self._INCIDENT_LOG} Incident manager ready")
            else:
                self.logger.warning(
                    f"{self._INCIDENT_LOG} Incident manager unavailable; incidents will not be published"
                )
        except Exception as e:
            self.logger.error(
                f"{self._INCIDENT_LOG} Incident manager init failed: {e}",
                exc_info=True,
            )
        finally:
            self._incident_manager_initialized = True

    def _send_incident_to_manager(self, incident: Dict, stream_info: Optional[Dict[str, Any]] = None) -> None:
        if not self._incident_manager:
            return
        try:
            published = self._incident_manager.process_incident(
                camera_id=_DEFAULT_CAMERA_ID,
                incident_data=incident,
                stream_info=stream_info,
            )
            if published:
                self.logger.info(f"{self._INCIDENT_LOG} Incident published for camera: {_DEFAULT_CAMERA_ID}")
        except Exception as e:
            self.logger.error(
                f"{self._INCIDENT_LOG} Error publishing incident: {e}",
                exc_info=True,
            )

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
            if not isinstance(config, WeaponDetectionConfig):
                self._debug_elapsed_since(start_time)
                return self.create_error_result(
                    "Invalid configuration type for weapon detection",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            if not self._incident_manager_initialized:
                self._initialize_incident_manager_once(config)

            if context is None:
                context = ProcessingContext()
            context.input_format = match_results_structure(data)
            context.confidence_threshold = config.confidence_threshold
            self.logger.info(
                f"Processing weapon detection with format: "
                f"{context.input_format.value} "
                f"with threshold: {config.confidence_threshold}"
            )

            if config.alert_config is None:
                config.alert_config = AlertConfig(**_DEFAULT_ALERT_CONFIG_KWARGS)

            self.target_categories = [c.lower() for c in config.target_categories]

            processed = self._filter_and_map(data, config)
            processed = self._smooth_bboxes(processed, config)
            summary = self._calculate_weapon_summary(processed, config)
            frame_number = self._extract_frame_number(stream_info)

            alerts = self._check_alerts(summary, config, stream_info)
            incidents_list = self._generate_incidents(summary, alerts, config, stream_info)
            tracking_stats_list = self._generate_tracking_stats(
                summary,
                alerts,
                config,
                frame_number=frame_number,
                stream_info=stream_info,
            )
            business_analytics_list = (
                self._generate_business_analytics(summary, alerts, config, stream_info, is_empty=True) or []
            )

            incident = incidents_list[0] if incidents_list else {}
            self._send_incident_to_manager(incident, stream_info)

            summary_list = self._generate_summary(incidents_list, tracking_stats_list, business_analytics_list)

            context.processing_time = time.time() - start_time
            tracking_stat = tracking_stats_list[0] if tracking_stats_list else {}

            if len(tracking_stats_list) > 1:
                alerts = tracking_stats_list[1]
                incident = tracking_stats_list[2]

            agg_summary = {
                str(frame_number): {
                    "incidents": incident,
                    "tracking_stats": tracking_stat,
                    "business_analytics": business_analytics_list,
                    "alerts": alerts,
                    "human_text": summary_list[0] if summary_list else {},
                }
            }
            context.mark_completed()
            result = self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context,
            )
            self._debug_elapsed_since(start_time)
            return result

        except Exception as e:
            self.logger.error(f"Error in weapon detection processing: {e}", exc_info=True)
            self._debug_elapsed_since(start_time)
            return self.create_error_result(
                f"Weapon detection processing failed: {e}",
                error_type="WeaponDetectionProcessingError",
                usecase=self.name,
                category=self.category,
                context=context,
            )

    # ---- Pipeline stages --------------------------------------------------

    def _filter_and_map(self, data: Any, config: WeaponDetectionConfig) -> List[Dict]:
        processed = data
        if config.confidence_threshold is not None:
            processed = filter_by_confidence(processed, config.confidence_threshold)
        if config.index_to_category:
            processed = apply_category_mapping(processed, config.index_to_category)
        if self.target_categories:
            processed = [d for d in processed if d.get("category", "").lower() in self.target_categories]
        return processed

    def _smooth_bboxes(self, processed: List[Dict], config: WeaponDetectionConfig) -> List[Dict]:
        if not config.enable_smoothing:
            return processed
        if self.smoothing_tracker is None:
            smoothing_config = BBoxSmoothingConfig(
                smoothing_algorithm=config.smoothing_algorithm,
                window_size=config.smoothing_window_size,
                cooldown_frames=config.smoothing_cooldown_frames,
                confidence_threshold=config.confidence_threshold,
                confidence_range_factor=config.smoothing_confidence_range_factor,
                enable_smoothing=True,
            )
            self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)

        smoothable = set(self.target_categories)
        to_smooth = [d for d in processed if d.get("category", "").lower() in smoothable]
        others = [d for d in processed if d.get("category", "").lower() not in smoothable]
        smoothed = bbox_smoothing(to_smooth, self.smoothing_tracker.config, self.smoothing_tracker)
        return others + smoothed

    @staticmethod
    def _extract_frame_number(
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[int]:
        if not stream_info:
            return None
        input_settings = stream_info.get("input_settings", {})
        start = input_settings.get("start_frame")
        end = input_settings.get("end_frame")
        if start is not None and end is not None and start == end:
            return start
        return start

    def _calculate_weapon_summary(self, data: Any, config: WeaponDetectionConfig) -> Dict[str, Any]:
        if not isinstance(data, list):
            return {
                "total_objects": 0,
                "by_category": {},
                "detections": [],
                "by_category_tracking": {},
            }

        tracking_cats = [c.lower() for c in config.target_categories]
        by_category_tracking: Dict[str, int] = {c: 0 for c in tracking_cats}
        for d in data:
            if not isinstance(d, dict):
                continue
            c = d.get("category", "").lower()
            if c in by_category_tracking:
                by_category_tracking[c] = by_category_tracking.get(c, 0) + 1

        valid = [c.lower() for c in config.weapon_categories]
        detections = [d for d in data if isinstance(d, dict) and d.get("category", "").lower() in valid]
        per_cat: Dict[str, int] = {}
        for d in detections:
            c = d.get("category", "unknown").lower()
            per_cat[c] = per_cat.get(c, 0) + 1

        by_cat = {
            cat: sum(1 for d in detections if d.get("category", "").lower() == cat.lower())
            for cat in config.weapon_categories
        }
        return {
            "total_objects": len(detections),
            "by_category": by_cat,
            "detections": detections,
            "per_category_count": per_cat,
            "by_category_tracking": by_category_tracking,
        }

    # ---- Alerts -----------------------------------------------------------

    def _check_alerts(
        self,
        summary: Dict,
        config: WeaponDetectionConfig,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        total = summary.get("total_objects", 0)
        if total == 0 or not config.alert_config:
            return []
        thresholds = getattr(config.alert_config, "count_thresholds", None) or {}
        if not thresholds:
            return []

        last_level = self._ascending_alert_list[-1] if self._ascending_alert_list else "low"
        current_ts = self._get_current_timestamp_str(stream_info)
        rank_ids, alert_id = self._id_tracker.advance(last_level, current_ts)
        if rank_ids not in (1, 2, 3, 4, 5):
            alert_id = 1

        trend = _is_trend_ascending(self._ascending_alert_list)
        per_cat = summary.get("per_category_count", {})
        alerts: List[Dict] = []
        for category, threshold in thresholds.items():
            if isinstance(threshold, str):
                threshold = int(threshold)
            if category == "all":
                if total > threshold:
                    alerts.append(self._build_alert(category, alert_id, threshold, trend, config))
            elif category in per_cat and per_cat[category] > threshold:
                alerts.append(self._build_alert(category, alert_id, threshold, trend, config))
        return alerts

    def _build_alert(
        self,
        category: str,
        alert_id: int,
        threshold: int,
        ascending: bool,
        config: WeaponDetectionConfig,
    ) -> Dict:
        ac = config.alert_config
        alert_type = (ac.alert_type if ac else ["Default"]) or ["Default"]
        return {
            "alert_type": alert_type,
            "alert_id": f"alert_{category}_{alert_type[0]}_{alert_id}",
            "incident_category": self.CASE_TYPE,
            "threshold_level": threshold,
            "ascending": ascending,
            "settings": _alert_settings_dict(ac),
        }

    # ---- Incidents --------------------------------------------------------

    def _generate_incidents(
        self,
        summary: Dict,
        alerts: List[Dict],
        config: WeaponDetectionConfig,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        total = summary.get("total_objects", 0)
        current_ts = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        if len(self._ascending_alert_list) > _ALERT_HISTORY_CAP:
            self._ascending_alert_list = self._ascending_alert_list[-_ALERT_HISTORY_CAP:]

        if total == 0:
            self._consecutive_weapon_frames = 0
            return [{}]

        self._consecutive_weapon_frames += 1
        if self._consecutive_weapon_frames < config.min_confirmation_frames:
            self.logger.debug(
                f"Weapon detected but awaiting confirmation: "
                f"{self._consecutive_weapon_frames}/{config.min_confirmation_frames} frames"
            )
            return [{}]

        thresholds = getattr(config.alert_config, "count_thresholds", None) or {}
        per_cat = summary.get("per_category_count", {})
        if not thresholds and per_cat:
            thresholds = {cat: 0 for cat in per_cat.keys()}
            self.logger.debug(f"[INCIDENT] count_thresholds was empty, using detected categories: {thresholds}")

        threshold_count = config.threshold_count or 15
        incidents: List[Dict] = []
        for category in thresholds:
            if category == "all" or category in per_cat:
                incidents.append(
                    self._build_incident(
                        total,
                        threshold_count,
                        config,
                        alerts,
                        camera_info,
                        current_ts,
                        stream_info,
                        is_fallback=False,
                    )
                )
                break

        if not incidents:
            self.logger.warning(
                f"[INCIDENT] No incident generated despite {total} detections. Generating fallback incident."
            )
            incidents.append(
                self._build_incident(
                    total,
                    threshold_count,
                    config,
                    alerts,
                    camera_info,
                    current_ts,
                    stream_info,
                    is_fallback=True,
                )
            )
        return incidents

    def _build_incident(
        self,
        total_detections: int,
        threshold_count: int,
        config: WeaponDetectionConfig,
        alerts: List[Dict],
        camera_info: Dict,
        current_ts: str,
        stream_info: Optional[Dict[str, Any]],
        is_fallback: bool,
    ) -> Dict:
        start_ts = self._get_start_timestamp_str(stream_info)
        self._debug_stream_timing("start_timestamp", start_ts)

        if not is_fallback:
            self._update_incident_end_timestamp(start_ts)
        else:
            self.current_incident_end_timestamp = "Incident still active"

        intensity = _compute_intensity(total_detections, threshold_count)
        level = _level_from_intensity(intensity)
        self._ascending_alert_list.append(level)

        rank_ids, incident_id = self._id_tracker.advance(level, current_ts)
        if rank_ids not in (1, 2, 3, 4, 5):
            incident_id = 1
        timing = self._id_tracker.id_timing_list
        if timing:
            if len(timing) == rank_ids:
                start_ts = timing[-1]
            if len(timing) > 4 and level == "critical":
                start_ts = timing[-1]

        print_level = "high" if level == "significant" else level
        human_text = f"INCIDENTS DETECTED @ {current_ts}:\n\tSeverity Level: {(self.CASE_TYPE, print_level)}"

        alert_settings = self._alert_settings_block(config) if not is_fallback else []
        end_time = self.current_incident_end_timestamp if not is_fallback else "Incident still active"
        incident_suffix = "fallback" if is_fallback else str(incident_id)

        event = self.create_incident(
            incident_id=f"incident_{self.CASE_TYPE}_{incident_suffix}",
            incident_type=self.CASE_TYPE,
            severity_level=level,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            start_time=start_ts,
            end_time=end_time,
            level_settings=_LEVEL_SETTINGS,
        )
        if not is_fallback:
            event["duration"] = self.get_duration_seconds(start_ts, self.current_incident_end_timestamp)
        event["incident_quant"] = intensity
        return event

    def _update_incident_end_timestamp(self, start_ts: str) -> None:
        """
        State machine:
          "N/A"                   -> "Incident still active"  (on start)
          "Incident still active" -> "Incident active"        (on dominant-level flip)
          anything else           -> "N/A"                    (reset)
        """
        if start_ts and self.current_incident_end_timestamp == "N/A":
            self.current_incident_end_timestamp = "Incident still active"
        elif start_ts and self.current_incident_end_timestamp == "Incident still active":
            pair = _trend_windows(self._ascending_alert_list)
            if pair is not None and pair[0] != pair[1]:
                self.current_incident_end_timestamp = "Incident active"
        elif self.current_incident_end_timestamp not in (
            "Incident still active",
            "N/A",
        ):
            self.current_incident_end_timestamp = "N/A"

    def _alert_settings_block(self, config: WeaponDetectionConfig) -> List[Dict]:
        ac = config.alert_config
        if not ac:
            return []
        return [
            {
                "alert_type": ac.alert_type or ["Default"],
                "incident_category": self.CASE_TYPE,
                "threshold_level": ac.count_thresholds or {},
                "ascending": True,
                "settings": _alert_settings_dict(ac),
            }
        ]

    # ---- Tracking stats ---------------------------------------------------

    def _generate_tracking_stats(
        self,
        summary: Dict,
        alerts: List,
        config: WeaponDetectionConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List:
        camera_info = self.get_camera_info_from_stream(stream_info)
        by_cat = summary.get("by_category", {})
        by_cat_track = summary.get("by_category_tracking") or {}
        total_weapon = int(by_cat_track.get("weapon", by_cat.get("weapon", 0)))
        total_person = int(by_cat_track.get("person", by_cat.get("person", 0)))
        any_target = total_weapon > 0 or total_person > 0

        current_ts = self._get_current_timestamp_str(stream_info)
        start_ts = self._get_start_timestamp_str(stream_info)
        self._debug_stream_timing("start_timestamp", start_ts)
        high_precision_start = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset = self._get_start_timestamp_str(stream_info, precision=True)

        total_counts = (
            [{"category": "Weapon/Person", "count": 1}]
            if any_target
            else [
                {"category": "Person", "count": 0},
                {"category": "Weapon", "count": 0},
            ]
        )
        current_counts = [
            {"category": "Person", "count": 1 if total_person > 0 else 0},
            {"category": "Weapon", "count": 1 if total_weapon > 0 else 0},
        ]
        new_counts_dict = self.get_new_counts_this_frame()
        current_new_counts = [{"category": cat, "count": count} for cat, count in new_counts_dict.items()]

        lines = [f"CURRENT FRAME @ {current_ts}:"]
        if total_person > 0:
            lines.append(f"\t- Persons detected: {total_person}")
        if total_weapon > 0:
            lines.append(f"\t- Weapons detected: {total_weapon}")
        if total_person == 0 and total_weapon == 0:
            lines.append("\t- No persons or weapons detected")
        lines.append("")
        human_text = "\n".join(lines)

        detections: List[Dict] = []
        for det in summary.get("detections", []):
            bbox = det.get("bounding_box", {})
            category = det.get("category", "Weapon")
            seg = det.get("masks") or det.get("segmentation") or det.get("mask")
            if seg is not None:
                detections.append(self.create_detection_object(category, bbox, segmentation=seg))
            else:
                detections.append(self.create_detection_object(category, bbox))

        alert_settings = self._alert_settings_block(config)
        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=_RESET_SETTINGS,
            start_time=high_precision_start,
            reset_time=high_precision_reset,
        )
        tracking_stat["target_categories"] = self.target_categories
        tracking_stat["current_new_counts"] = current_new_counts
        tracking_stats: List = [tracking_stat]

        event_ended = self._maybe_emit_event_ended(config, alert_settings, camera_info, start_ts, stream_info)
        if event_ended is not None:
            ended_alerts, ended_incident = event_ended
            tracking_stats.append(ended_alerts)
            tracking_stats[0]["alerts"] = ended_alerts
            tracking_stats.append(ended_incident)
        return tracking_stats

    def _maybe_emit_event_ended(
        self,
        config: WeaponDetectionConfig,
        alert_settings: List[Dict],
        camera_info: Dict,
        start_ts: str,
        stream_info: Optional[Dict[str, Any]],
    ) -> Optional[Tuple[List[Dict], Dict]]:
        if len(self._id_tracker.id_hit_list) != 1:
            return None

        current_ts = self._get_current_timestamp_str(stream_info)
        last_ending_id, incident_id = self._id_tracker.advance("", current_ts)
        if last_ending_id != 5:
            return None

        timing = self._id_tracker.id_timing_list
        if len(timing) > 0 and len(timing) >= 5:
            start_ts = timing[-1]
        if incident_id == self._id_tracker.return_id_counter:
            incident_id = incident_id - 1
        if self._id_tracker.return_id_counter > incident_id:
            incident_id = self._id_tracker.return_id_counter - incident_id

        ac = config.alert_config
        alert_type = (ac.alert_type if ac else ["Default"]) or ["Default"]
        alert = {
            "alert_type": alert_type,
            "alert_id": f"alert_Event_Ended_{alert_type[0]}_{incident_id}",
            "incident_category": self.CASE_TYPE,
            "threshold_level": 0,
            "ascending": False,
            "settings": _alert_settings_dict(ac),
        }
        incident = self.create_incident(
            incident_id=f"incident_{self.CASE_TYPE}_{incident_id}",
            incident_type=self.CASE_TYPE,
            severity_level="info",
            human_text="Event Over",
            camera_info=camera_info,
            alerts=[alert],
            alert_settings=alert_settings,
            start_time=start_ts,
            end_time="Incident still active",
            level_settings=_LEVEL_SETTINGS,
        )
        return [alert], incident

    # ---- Business analytics / summary / schema ---------------------------

    def _generate_business_analytics(
        self,
        _summary: Dict,
        _alerts: Any,
        _config: WeaponDetectionConfig,
        _stream_info: Optional[Dict[str, Any]] = None,
        is_empty: bool = False,
    ) -> Optional[List[Dict]]:
        if is_empty:
            return []
        return None

    def _generate_summary(
        self,
        incidents: List[Dict],
        tracking_stats: List,
        business_analytics: List,
    ) -> List[str]:
        lines = [
            f"Application Name: {self.CASE_TYPE}",
            f"Application Version: {self.CASE_VERSION}",
        ]
        if incidents:
            first = incidents[0] if isinstance(incidents[0], dict) else {}
            lines.append("Incidents: " + f"\n\t{first.get('human_text', 'No incidents detected')}")
        if tracking_stats:
            first = tracking_stats[0] if isinstance(tracking_stats[0], dict) else {}
            lines.append("Tracking Statistics: " + f"\t{first.get('human_text', 'No tracking statistics detected')}")
        if business_analytics:
            first = business_analytics[0] if isinstance(business_analytics[0], dict) else {}
            lines.append("Business Analytics: " + f"\t{first.get('human_text', 'No business analytics detected')}")
        if not incidents and not tracking_stats and not business_analytics:
            lines.append("Summary: No Summary Data")
        return ["\n".join(lines)]

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.28,
                    "description": "Minimum confidence threshold for detections",
                },
                "weapon_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["weapon"],
                    "description": "Category names counted as weapons for incidents and alert totals",
                },
                "min_confirmation_frames": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 5,
                    "description": "Consecutive frames of sustained detection required before an incident is emitted",
                },
                "index_to_category": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Mapping from category indices to names",
                },
                "alert_config": {
                    "type": "object",
                    "properties": {
                        "count_thresholds": {
                            "type": "object",
                            "additionalProperties": {
                                "type": "integer",
                                "minimum": 1,
                            },
                            "description": "Count thresholds for alerts",
                        }
                    },
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False,
        }

    def create_default_config(self, **overrides) -> WeaponDetectionConfig:
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.28,
            "weapon_categories": ["weapon"],
        }
        defaults.update(overrides)
        return WeaponDetectionConfig(**defaults)

    # ---- Tracking stubs (API compatibility) ------------------------------

    def _update_tracking_state(self, detections: list) -> None:
        """
        Update per-category track-id sets from detections. Kept for API
        compatibility with consumers that invoke get_new_counts_this_frame /
        get_total_counts / get_current_frame_counts; not called by the
        weapon-detection pipeline.
        """
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}
        for det in detections:
            cat = det.get("category")
            track_id = det.get("track_id")
            if cat not in self.target_categories or track_id is None:
                continue
            self._per_category_total_track_ids.setdefault(cat, set()).add(track_id)
            self._current_frame_track_ids[cat].add(track_id)
        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._previous_frame_track_ids.get(cat, set()))
            for cat in self.target_categories
        }
        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def get_total_counts(self) -> Dict[str, int]:
        return {cat: len(ids) for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        return {cat: len(ids) for cat, ids in getattr(self, "_new_track_ids_this_frame", {}).items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        return {cat: len(ids) for cat, ids in getattr(self, "_current_frame_track_ids", {}).items()}

    # ---- Timestamp plumbing (preserved from prior version) ---------------

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        if dt.year < 2000:
            dt = datetime.now(timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to YYYY:MM:DD HH:MM:SS."""
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            if dt.year < 2000:
                dt = datetime.now(timezone.utc)
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
                    try:
                        if int(parts[0]) < 2000:
                            return datetime.now(timezone.utc).strftime("%Y:%m:%d %H:%M:%S")
                    except ValueError:
                        pass
                    return f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
        except Exception:
            pass

        return timestamp_clean

    def _get_current_timestamp_str(
        self,
        stream_info: Optional[Dict[str, Any]],
        precision: bool = False,
        frame_id: Optional[str] = None,
    ) -> str:
        if not stream_info:
            return "00:00:00.00"
        input_settings = stream_info.get("input_settings", {}) or {}
        start_frame = input_settings.get("start_frame", "na")

        if precision:
            if start_frame != "na":
                if frame_id:
                    start_time = int(frame_id) / input_settings.get("original_fps", 30)
                else:
                    start_time = input_settings.get("start_frame", 30) / input_settings.get("original_fps", 30)
                self._debug_stream_timing("stream_time_str", self._format_timestamp_for_video(start_time))
                return self._format_timestamp(input_settings.get("stream_time", "NA"))
            return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if start_frame != "na":
            if frame_id:
                start_time = int(frame_id) / input_settings.get("original_fps", 30)
            else:
                start_time = input_settings.get("start_frame", 30) / input_settings.get("original_fps", 30)
            self._debug_stream_timing("stream_time_str", self._format_timestamp_for_video(start_time))
            return self._format_timestamp(input_settings.get("stream_time", "NA"))

        stream_time_str = input_settings.get("stream_info", {}).get("stream_time", "")
        if stream_time_str:
            try:
                dt = datetime.strptime(stream_time_str.replace(" UTC", ""), "%Y-%m-%d-%H:%M:%S.%f")
                ts = dt.replace(tzinfo=timezone.utc).timestamp()
                return self._format_timestamp_for_stream(ts)
            except Exception:
                return self._format_timestamp_for_stream(time.time())
        return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision: bool = False) -> str:
        if not stream_info:
            return "00:00:00"
        input_settings = stream_info.get("input_settings", {}) or {}

        def _candidate_from_stream_time(now_fallback: bool = True) -> str:
            candidate = input_settings.get("stream_time")
            if not candidate or candidate == "NA":
                nested = input_settings.get("stream_info", {}).get("stream_time", "")
                if nested:
                    try:
                        dt = datetime.strptime(nested.replace(" UTC", ""), "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime(
                            "%Y-%m-%d-%H:%M:%S.%f UTC"
                        )
                    except Exception:
                        candidate = (
                            datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC") if now_fallback else None
                        )
                else:
                    candidate = (
                        datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC") if now_fallback else None
                    )
            return candidate

        if precision:
            if self.start_timer is None:
                candidate = input_settings.get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            if input_settings.get("start_frame", "na") == 1:
                candidate = input_settings.get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            self.start_timer = _candidate_from_stream_time()
            return self._format_timestamp(self.start_timer)

        if input_settings.get("start_frame", "na") == 1:
            candidate = input_settings.get("stream_time")
            if not candidate or candidate == "NA":
                nested = input_settings.get("stream_info", {}).get("stream_time", "")
                if nested:
                    try:
                        dt = datetime.strptime(nested.replace(" UTC", ""), "%Y-%m-%d-%H:%M:%S.%f")
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
            nested = input_settings.get("stream_info", {}).get("stream_time", "")
            if nested:
                try:
                    dt = datetime.strptime(nested.replace(" UTC", ""), "%Y-%m-%d-%H:%M:%S.%f")
                    self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                except Exception:
                    self._tracking_start_time = time.time()
            else:
                self._tracking_start_time = time.time()

        dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
        if dt.year < 2000:
            dt = datetime.now(timezone.utc)
        dt = dt.replace(minute=0, second=0, microsecond=0)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def get_duration_seconds(self, start_time, end_time):
        def parse_relative_time(t):
            try:
                parts = t.strip().split(":")
                if len(parts) != 3:
                    return None
                return timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=float(parts[2]))
            except Exception:
                return None

        def parse_time(t):
            if re.match(r"^\d{1,2}:\d{2}:\d{1,2}(\.\d+)?$", t):
                return parse_relative_time(t)
            if "UTC" in t:
                try:
                    return datetime.strptime(t, "%Y-%m-%d-%H:%M:%S.%f UTC")
                except ValueError:
                    return None
            return None

        start_dt = parse_time(start_time)
        end_dt = parse_time(end_time)

        if start_dt is None or end_dt is None:
            return "N/A"
        if isinstance(start_dt, timedelta) and isinstance(end_dt, timedelta):
            return (end_dt - start_dt).total_seconds()
        if isinstance(start_dt, datetime) and isinstance(end_dt, datetime):
            return (end_dt - start_dt).total_seconds()
        return None
