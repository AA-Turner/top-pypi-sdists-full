"""
Unwanted Animal Detection use case (single-camera).

Detects unwanted animals (cats / dogs) from the ``yolov8n_cat_dog.pt`` model
output and raises an incident whenever an animal is present in the scene.

Behavior contract (as requested):
  - An *incident* begins the first frame an unwanted animal is detected and stays
    "active" for as long as at least one animal keeps being detected.
  - Exactly **one alert** is raised on the frame the incident *starts*. While the
    incident remains active no further alerts are emitted.
  - When no animal is detected the incident closes. A later re-appearance opens a
    new incident (new incident id) and raises a new single alert.

Model classes (``yolov8n_cat_dog.pt`` exposes a 2-class head, ``nc=2``):
    index 0 -> cat
    index 1 -> dog
These two indices are mapped to names and both are kept as target categories.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

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
    match_results_structure,
)
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# ============================================================================
# Constants
# ============================================================================

# Single-camera identifier (mirrors other single-camera use cases).
_DEFAULT_CAMERA_ID = "camera"

# Severity thresholds on the number of animals detected in the frame.
_SEVERITY_LOW = 1
_SEVERITY_MEDIUM = 3
_SEVERITY_CRITICAL = 6

_LEVEL_SETTINGS = {"low": 1, "medium": 3, "significant": 4, "critical": 7}
_RESET_SETTINGS = [{"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}]

# yolov8n_cat_dog.pt 2-class head (nc=2): model.names == {0: "cat", 1: "dog"}.
_MODEL_INDEX_TO_CATEGORY: Dict[int, str] = {0: "cat", 1: "dog"}

# Alerting here is incident-driven (one alert when an incident opens), not
# count-threshold driven, so count_thresholds is intentionally left empty to
# avoid AlertConfig's "threshold must be positive" validation error.
_DEFAULT_ALERT_CONFIG_KWARGS = dict(
    count_thresholds={},
    alert_type=["Default"],
    alert_value=["JSON"],
    alert_incident_category=["UNWANTED-ANIMAL-ALERT"],
)


def _resolve_manager_camera_id(stream_info: Optional[Dict[str, Any]]) -> str:
    """Resolve the camera key used by IncidentManager state tracking."""
    if not stream_info:
        return _DEFAULT_CAMERA_ID
    inp = stream_info.get("input_settings")
    if not isinstance(inp, dict):
        inp = {}
    camera_info = stream_info.get("camera_info")
    if not isinstance(camera_info, dict):
        camera_info = {}
    camera_id = (
        stream_info.get("camera_id")
        or inp.get("camera_id")
        or camera_info.get("camera_id")
        or stream_info.get("stream_key")
    )
    return str(camera_id) if camera_id else _DEFAULT_CAMERA_ID


# ============================================================================
# Config
# ============================================================================


@dataclass
class UnwantedAnimalDetectionConfig(BaseConfig):
    """Configuration for the unwanted animal detection use case."""

    confidence_threshold: float = 0.4

    # Categories that are considered "unwanted" and drive incidents/alerts.
    unwanted_animal_categories: List[str] = field(default_factory=lambda: ["cat", "dog"])
    target_categories: List[str] = field(default_factory=lambda: ["cat", "dog"])

    alert_config: Optional[AlertConfig] = field(
        default_factory=lambda: AlertConfig(**_DEFAULT_ALERT_CONFIG_KWARGS)
    )

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: dict(_MODEL_INDEX_TO_CATEGORY)
    )

    enable_unique_counting: bool = True

    # Incident-manager wiring (third flow).
    session: Optional[Any] = None
    server_id: Optional[str] = None

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")
        self.unwanted_animal_categories = [c.lower() for c in self.unwanted_animal_categories]
        if self.target_categories:
            self.target_categories = [c.lower() for c in self.target_categories]

    def validate(self) -> List[str]:
        errors = super().validate()
        if not self.unwanted_animal_categories:
            errors.append("unwanted_animal_categories cannot be empty")
        if self.alert_config:
            errors.extend(self.alert_config.validate())
        return errors


# ============================================================================
# Use case
# ============================================================================


class UnwantedAnimalDetectionUseCase(BaseProcessor):
    CASE_TYPE: Optional[str] = "unwanted_animal_detection"
    CASE_VERSION: Optional[str] = "1.0"

    CATEGORY_DISPLAY = {"cat": "Cat", "dog": "Dog"}

    def __init__(self) -> None:
        super().__init__("unwanted_animal_detection")
        self.category = "general"
        self.target_categories: List[str] = ["cat", "dog"]

        # Rolling counters.
        self._total_frame_counter = 0
        self._total_detections = 0
        self._per_category_total: Dict[str, int] = {}

        # Incident state machine (drives the single-alert-per-incident behavior).
        self._incident_active: bool = False
        self._incident_counter: int = 0
        self._incident_start_ts: Optional[str] = None

        # Timestamp plumbing.
        self.start_timer: Optional[str] = None

        # Incident manager (third flow): owns the incident open/close lifecycle
        # and incident_res publishing.
        self._INCIDENT_LOG = "[INCIDENT_MANAGER]"
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False

    # ---- Incident manager lifecycle ---------------------------------------

    def _initialize_incident_manager_once(self, config: "UnwantedAnimalDetectionConfig") -> None:
        if self._incident_manager_initialized:
            return
        try:
            self.logger.info(f"{self._INCIDENT_LOG} Initializing incident manager for unwanted animal detection...")
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

    def _send_incident_to_manager(
        self,
        incident: Dict,
        stream_info: Optional[Dict[str, Any]] = None,
        context: Optional[ProcessingContext] = None,
    ) -> bool:
        """Feed the incident to the manager and report whether its state changed.

        Fire-style: the manager is called every frame with ``incident or {}`` (no
        early return on an empty dict) so it can count idle frames and publish the
        closing ``info`` transition once the animal leaves. Returns True only when
        the manager published a state change (open / severity change / close).
        """
        published = False
        camera_id = _resolve_manager_camera_id(stream_info)
        if self._incident_manager:
            try:
                published = bool(
                    self._incident_manager.process_incident(
                        camera_id=camera_id,
                        incident_data=incident or {},
                        stream_info=stream_info,
                    )
                )
                if published:
                    self.logger.info(f"{self._INCIDENT_LOG} Incident published for camera: {camera_id}")
            except Exception as e:
                self.logger.error(
                    f"{self._INCIDENT_LOG} Error publishing incident: {e}",
                    exc_info=True,
                )

        if context is not None:
            # When IncidentManager is active it owns the full open/close lifecycle.
            # Skip duplicate legacy incident_res publishes from PostProcessor.
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        return published

    # ---- Config plumbing --------------------------------------------------

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.4,
                    "description": "Minimum confidence threshold for detections",
                },
                "unwanted_animal_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["cat", "dog"],
                    "description": "Category names treated as unwanted animals",
                },
                "index_to_category": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Mapping from model class indices to names",
                },
                "alert_config": {
                    "type": "object",
                    "properties": {
                        "count_thresholds": {
                            "type": "object",
                            "additionalProperties": {"type": "integer", "minimum": 0},
                        }
                    },
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": True,
        }

    def create_default_config(self, **overrides: Any) -> UnwantedAnimalDetectionConfig:
        defaults: Dict[str, Any] = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.4,
        }
        defaults.update(overrides)
        return UnwantedAnimalDetectionConfig(**defaults)

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
            if not isinstance(config, UnwantedAnimalDetectionConfig):
                return self.create_error_result(
                    "Invalid configuration type for unwanted animal detection",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            if context is None:
                context = ProcessingContext()
            context.input_format = match_results_structure(data)
            context.confidence_threshold = config.confidence_threshold

            # Ensure a concrete AlertConfig so the incident-start alert can fire
            # even when the config factory passed alert_config=None.
            if config.alert_config is None:
                config.alert_config = AlertConfig(**_DEFAULT_ALERT_CONFIG_KWARGS)

            if not self._incident_manager_initialized:
                self._initialize_incident_manager_once(config)

            processed = self._filter_and_map(data, config)

            counting_summary = self._count_categories(processed)
            self._total_frame_counter += 1
            self._total_detections += counting_summary["total_count"]
            for cat, cnt in counting_summary["per_category_count"].items():
                self._per_category_total[cat] = self._per_category_total.get(cat, 0) + cnt

            frame_number = self._extract_frame_number(stream_info)
            camera_info = self.get_camera_info_from_stream(stream_info)
            current_ts = self._get_current_timestamp_str(stream_info)

            # Drive the incident state machine and decide whether THIS frame is an
            # incident-start (the only frame that emits an alert).
            incident_started = self._update_incident_state(counting_summary["total_count"], current_ts)

            alerts = self._build_alerts(counting_summary, config, incident_started, frame_number)
            incidents = self._generate_incident(
                counting_summary, config, alerts, camera_info, current_ts
            )

            # Third flow: hand the incident to the IncidentManager, which owns the
            # open/close lifecycle and publishes to incident_res. Sets the
            # incident_published_via_manager flag so the PostProcessor legacy bridge
            # does not double-publish. Fed every frame ({} when idle) for idle close.
            self._send_incident_to_manager(incidents, stream_info, context=context)

            tracking_stats = self._generate_tracking_stats(
                counting_summary, config, alerts, camera_info, current_ts, stream_info
            )

            human_text = self._generate_summary(counting_summary, incidents, current_ts)

            frame_key = str(frame_number) if frame_number is not None else "current_frame"
            agg_summary = {
                frame_key: {
                    "incidents": incidents,
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
        except Exception as e:  # noqa: BLE001 - surface failures as error results
            self.logger.error(f"Error in unwanted animal detection: {e}", exc_info=True)
            return self.create_error_result(
                f"Unwanted animal detection failed: {e}",
                error_type="UnwantedAnimalDetectionError",
                usecase=self.name,
                category=self.category,
                context=context,
            )

    # ---- Pipeline stages --------------------------------------------------

    def _filter_and_map(self, data: Any, config: UnwantedAnimalDetectionConfig) -> List[Dict]:
        processed = data
        if config.confidence_threshold is not None:
            processed = filter_by_confidence(processed, config.confidence_threshold)
        if config.index_to_category:
            processed = apply_category_mapping(processed, config.index_to_category)
        targets = config.target_categories or self.target_categories
        processed = [d for d in processed if str(d.get("category", "")).lower() in targets]
        return processed

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

    def _count_categories(self, detections: List[Dict]) -> Dict[str, Any]:
        per_category: Dict[str, int] = {}
        for det in detections:
            cat = str(det.get("category", "unknown")).lower()
            per_category[cat] = per_category.get(cat, 0) + 1
        return {
            "total_count": len(detections),
            "per_category_count": per_category,
            "detections": detections,
        }

    def _update_incident_state(self, total_count: int, current_ts: str) -> bool:
        """Advance the incident state machine; return True only on the start frame.

        - total > 0 and no active incident  -> open a new incident (start frame)
        - total > 0 and active incident      -> incident continues (no alert)
        - total == 0                         -> close any active incident
        """
        if total_count > 0:
            if not self._incident_active:
                self._incident_active = True
                self._incident_counter += 1
                self._incident_start_ts = current_ts
                return True
            return False
        # No animals: close the incident so a re-appearance starts a fresh one.
        self._incident_active = False
        self._incident_start_ts = None
        return False

    def _severity_for(self, count: int) -> str:
        if count >= _SEVERITY_CRITICAL:
            return "critical"
        if count >= _SEVERITY_MEDIUM:
            return "significant"
        if count >= _SEVERITY_LOW:
            return "medium"
        return "low"

    def _alert_settings_dict(self, alert_config: Optional[AlertConfig]) -> Dict[str, str]:
        if not alert_config:
            return {}
        types = alert_config.alert_type or ["Default"]
        values = alert_config.alert_value or ["JSON"]
        return {t: v for t, v in zip(types, values)}

    def _build_alerts(
        self,
        counting_summary: Dict[str, Any],
        config: UnwantedAnimalDetectionConfig,
        incident_started: bool,
        frame_number: Optional[int],
    ) -> List[Dict]:
        # Single alert: only on the frame the incident starts.
        if not incident_started or not config.alert_config:
            return []
        total = counting_summary.get("total_count", 0)
        ac = config.alert_config
        alert_type = ac.alert_type or ["Default"]
        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        return [
            {
                "alert_type": alert_type,
                "alert_id": f"alert_{self.CASE_TYPE}_{alert_type[0]}_{self._incident_counter}",
                "incident_category": self.CASE_TYPE,
                "threshold_level": 0,
                "ascending": True,
                "count": total,
                "settings": self._alert_settings_dict(ac),
                "frame": frame_key,
            }
        ]

    def _alert_settings_block(self, config: UnwantedAnimalDetectionConfig) -> List[Dict]:
        ac = config.alert_config
        if not ac:
            return []
        return [
            {
                "alert_type": ac.alert_type or ["Default"],
                "incident_category": self.CASE_TYPE,
                "threshold_level": ac.count_thresholds or {},
                "ascending": True,
                "settings": self._alert_settings_dict(ac),
            }
        ]

    def _generate_incident(
        self,
        counting_summary: Dict[str, Any],
        config: UnwantedAnimalDetectionConfig,
        alerts: List[Dict],
        camera_info: Dict[str, Any],
        current_ts: str,
    ) -> Dict[str, Any]:
        # No active incident -> empty payload for this frame.
        if not self._incident_active:
            return {}

        total = counting_summary.get("total_count", 0)
        per_cat = counting_summary.get("per_category_count", {})
        level = self._severity_for(total)

        breakdown = ", ".join(
            f"{self.CATEGORY_DISPLAY.get(cat, cat)}: {cnt}" for cat, cnt in per_cat.items()
        )
        human_text = (
            f"UNWANTED ANIMAL INCIDENT @ {current_ts}:\n"
            f"\tSeverity Level: {level}\n"
            f"\tUnwanted animals detected: {total} ({breakdown})"
        )

        start_ts = self._incident_start_ts or current_ts
        end_time = "Incident still active"

        event = self.create_incident(
            incident_id=f"incident_{self.CASE_TYPE}_{self._incident_counter}",
            incident_type=self.CASE_TYPE,
            severity_level=level,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=self._alert_settings_block(config),
            start_time=start_ts,
            end_time=end_time,
            level_settings=_LEVEL_SETTINGS,
        )
        # incident_quant drives severity in the IncidentManager (third flow). Any
        # present unwanted animal is treated as a maximum-severity event, so the
        # count saturates the 0-100 quant (a single animal -> 100 -> critical). A
        # stable quant keeps the manager's consecutive-frame confirmation from
        # resetting frame-to-frame (same approach as fall/violence).
        event["incident_quant"] = min(100.0, total * 100.0)
        return event

    def _generate_tracking_stats(
        self,
        counting_summary: Dict[str, Any],
        config: UnwantedAnimalDetectionConfig,
        alerts: List[Dict],
        camera_info: Dict[str, Any],
        current_ts: str,
        stream_info: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        total = counting_summary.get("total_count", 0)
        per_cat = counting_summary.get("per_category_count", {})

        current_counts = [self.create_count_object(cat, cnt) for cat, cnt in per_cat.items()]
        total_counts = [
            self.create_count_object(cat, cnt) for cat, cnt in self._per_category_total.items() if cnt > 0
        ]

        detections = [
            self.create_detection_object(
                det.get("category", "unknown"),
                det.get("bounding_box", det.get("bbox", {})),
            )
            for det in counting_summary.get("detections", [])
        ]

        if total > 0:
            lines = [f"CURRENT FRAME @ {current_ts}:"]
            for cat, cnt in per_cat.items():
                lines.append(f"\t- {self.CATEGORY_DISPLAY.get(cat, cat)}: {cnt}")
        else:
            lines = [f"CURRENT FRAME @ {current_ts}:", "\t- No unwanted animals detected"]
        human_text = "\n".join(lines)

        high_precision_start = self._get_start_timestamp_str(stream_info)

        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=self._alert_settings_block(config),
            reset_settings=_RESET_SETTINGS,
            start_time=high_precision_start,
        )
        tracking_stat["target_categories"] = self.target_categories
        return tracking_stat

    def _generate_summary(
        self,
        counting_summary: Dict[str, Any],
        incidents: Dict[str, Any],
        current_ts: str,
    ) -> str:
        total = counting_summary.get("total_count", 0)
        lines = [
            f"Application Name: {self.CASE_TYPE}",
            f"Application Version: {self.CASE_VERSION}",
        ]
        if incidents:
            lines.append("Incidents:")
            lines.append(f"\t{incidents.get('human_text', 'Unwanted animal incident active')}")
        else:
            lines.append(f"No unwanted animals detected @ {current_ts}")
        lines.append(f"Unwanted animals this frame: {total}")
        return "\n".join(lines)

    # ---- Timestamp plumbing ----------------------------------------------

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        if dt.year < 2000:
            dt = datetime.now(timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        if not stream_info:
            return self._format_timestamp_for_stream(time.time())
        input_settings = stream_info.get("input_settings", {}) or {}
        stream_time = input_settings.get("stream_time")
        if stream_time and stream_time != "NA":
            cleaned = str(stream_time).replace(" UTC", "")
            try:
                dt = datetime.strptime(cleaned, "%Y-%m-%d-%H:%M:%S.%f")
                return dt.strftime("%Y:%m:%d %H:%M:%S")
            except ValueError:
                pass
        return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]]) -> str:
        if self.start_timer is None:
            candidate = None
            if stream_info:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
        return self.start_timer
