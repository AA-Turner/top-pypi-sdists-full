"""Alerts Verification -- raise a fire alert from a single detection.

The verification half is deliberately a SEAM, not a feature. Today every detection that
clears the confidence threshold becomes an alert on the frame it appears; the confirmation
API that will accept or reject that alert is not built yet, and :meth:`_verify_alert` is the
one method it lands in. Nothing else in this file needs to change when it does.

WHY ONE FRAME, when weapon detection waits five (`min_confirmation_frames: 5`) and the
engine's own `confirm_frames` floor is three. Fire is the case where the wait costs the
most: a fire that is real grows while a confirmation window counts frames, and the point of
the use case is to hand a candidate to a verifier quickly rather than to be certain alone.
The temporal gate is still here and still configurable -- `min_confirmation_frames` defaults
to 1 rather than being deleted -- so a camera that proves noisy can be slowed down without a
code change, and the remote verifier is what replaces the wait once it exists.

SMOKE IS NOT ALERTED ON. The model emits both, and `index_to_category` maps both, so smoke
detections are mapped and counted -- they are simply not in `target_categories`, so they
raise nothing. Adding smoke later is a config change, not a code change.

This use case does NOT need the frame: it reads detections only, so it is absent from
`use_cases_with_bytes` in `post_processor.py` and `process()` takes no `input_bytes`.
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..utils import apply_category_mapping, filter_by_confidence, match_results_structure
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory

# ============================================================================
# Constants
# ============================================================================

#: Severity by the strongest detection's confidence, ordered high->low; first match wins.
#: The cutoffs sit where weapon detection's do, for the same reason: they are the rungs the
#: backend's DEFAULT_THRESHOLDS already grade against, and inventing a second scale here
#: would make two fire alerts from two apps incomparable on one dashboard.
_SEVERITY_CUTOFFS: Tuple[Tuple[str, float], ...] = (
    ("critical", 70.0),
    ("medium", 40.0),
    ("low", 27.0),
)
_LEVEL_SETTINGS = {"low": 27, "medium": 40, "critical": 70}

#: Used when `alert_config` arrives unset, which it does whenever a deployment configures
#: nothing: an alert with no channel is an alert nobody receives.
_DEFAULT_ALERT_CONFIG_KWARGS = dict(
    alert_type=["Default"],
    alert_value=["JSON"],
    alert_incident_category=["Incident Alert"],
)

#: Single-camera fallback when `stream_info` names no camera.
_DEFAULT_CAMERA_ID = "camera"

_INCIDENT_LOG = "[INCIDENT_MANAGER]"

#: What a call into IncidentManager can fail with. It is optional wiring supplied by the
#: runtime rather than by this package -- absent in a bare import, half-configured in a
#: local run (`Session` is None and the factory raises `TypeError` on call) -- so the set is
#: named rather than caught blind: a fire alert must not be lost to an integration fault,
#: and a genuine bug in this file must not be swallowed as one.
_INTEGRATION_ERRORS = (
    AttributeError,
    ImportError,
    KeyError,
    OSError,
    RuntimeError,
    TypeError,
    ValueError,
)


def _level_from_confidence_pct(confidence_pct: float) -> str:
    """The severity rung `confidence_pct` reaches, or ``"low"`` below every rung.

    Never returns ``""``: this use case alerts on the first detection, so anything that
    reached here already cleared `confidence_threshold` and is by definition an alert. An
    empty level would be read downstream as "no incident".
    """
    for level, cutoff in _SEVERITY_CUTOFFS:
        if confidence_pct >= cutoff:
            return level
    return "low"


def _max_confidence_pct(detections: List[Dict]) -> float:
    """Strongest detection's confidence as a percentage, or ``0.0`` when there are none."""
    best = 0.0
    for det in detections:
        try:
            value = float(det.get("confidence") or 0.0)
        except (TypeError, ValueError):
            continue
        best = max(best, value)
    return round(best * 100.0, 2) if best <= 1.0 else round(best, 2)


def _resolve_camera_id(stream_info: Optional[Dict[str, Any]]) -> str:
    """The camera key IncidentManager tracks state under."""
    if not stream_info:
        return _DEFAULT_CAMERA_ID
    input_settings = stream_info.get("input_settings")
    if not isinstance(input_settings, dict):
        input_settings = {}
    camera_info = stream_info.get("camera_info")
    if not isinstance(camera_info, dict):
        camera_info = {}
    camera_id = (
        stream_info.get("camera_id")
        or input_settings.get("camera_id")
        or camera_info.get("camera_id")
        or stream_info.get("stream_key")
    )
    return str(camera_id) if camera_id else _DEFAULT_CAMERA_ID


def _stream_timestamp(stream_info: Optional[Dict[str, Any]]) -> str:
    """The frame's own time where the stream carries one, else now.

    Prefers the media anchor over the wall clock so a replayed stream reports the times the
    live run did. `stream_time` is the same field `rtp_number` anchors, which is what the
    backend resolves a thumbnail from.
    """
    input_settings = (stream_info or {}).get("input_settings")
    if isinstance(input_settings, dict):
        candidate = input_settings.get("stream_time")
        if candidate and candidate != "NA":
            return str(candidate)
        nested = input_settings.get("stream_info")
        if isinstance(nested, dict) and nested.get("stream_time"):
            return str(nested["stream_time"])
    return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")


# ============================================================================
# Config
# ============================================================================


@dataclass
class AlertsVerificationConfig(BaseConfig):
    """Configuration for Alerts Verification."""

    confidence_threshold: float = 0.3

    #: What raises an alert. Smoke is mapped by `index_to_category` but deliberately not
    #: listed here, so it is counted and never alerted on. Add "smoke" to alert on it.
    target_categories: List[str] = field(default_factory=lambda: ["fire"])

    #: The fire model's class indices. Both classes are mapped even though only fire
    #: alerts: an unmapped index reaches the pipeline as a bare integer and matches no
    #: target, which looks identical to "the model saw nothing".
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {0: "fire", 1: "smoke"}
    )

    #: Consecutive frames of detection before an alert is raised. 1 -- alert on the first
    #: frame -- is the default and the point of this use case. Raise it for a camera whose
    #: detector is noisy enough that the verifier would spend its budget on false ones.
    min_confirmation_frames: int = 1

    alert_config: Optional[AlertConfig] = field(
        default_factory=lambda: AlertConfig(**_DEFAULT_ALERT_CONFIG_KWARGS)
    )

    #: IncidentManager wiring, supplied by the runtime rather than by a person.
    session: Optional[Any] = None
    server_id: Optional[str] = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")
        if self.min_confirmation_frames < 1:
            raise ValueError("min_confirmation_frames must be at least 1")
        self.target_categories = [c.lower() for c in self.target_categories]
        if self.index_to_category:
            self.index_to_category = {k: str(v).lower() for k, v in self.index_to_category.items()}


# ============================================================================
# Use case
# ============================================================================


class AlertsVerificationUseCase(BaseProcessor):
    """Raise a fire alert from a single detection, ready for remote verification."""

    CASE_TYPE: Optional[str] = "alerts_verification"
    CASE_VERSION: Optional[str] = "1.0"

    def __init__(self) -> None:
        super().__init__("alerts_verification")
        self.category = "safety"

        self._consecutive_fire_frames: int = 0
        self._incident_counter: int = 0
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False

    # -- verification seam ---------------------------------------------------

    def _verify_alert(
        self,
        detections: List[Dict],
        severity: str,
        stream_info: Optional[Dict[str, Any]],
    ) -> Tuple[bool, str]:
        """Confirm or reject a candidate alert. **The API integration point.**

        Returns ``(confirmed, reason)``. Today it confirms everything locally and reports
        ``"unverified"``, which is the honest description of what happened: the detector
        alone decided. Every caller already handles a rejection, so wiring the API is a
        change to this method and nothing else.

        When it is wired, three things matter and are recorded here rather than rediscovered:

        * **A verifier that is down must not silence fire.** Fail OPEN -- on a timeout or a
          transport error, return ``(True, "verifier_unavailable")`` and let the alert
          through. A verification service outage that suppressed every fire alert would be
          a far worse failure than the false positives it exists to remove.
        * **It must not block the frame loop.** This runs per frame on the analytics path;
          a synchronous call to a remote service belongs behind a short timeout and a
          cache keyed by camera, not inline on every detection.
        * **The reason travels.** It is published on the incident as
          ``verification_reason``, so a rejected alert can be told apart from one that was
          never checked.
        """
        del detections, severity, stream_info  # the verifier's inputs, once it exists
        return True, "unverified"

    # -- incident manager ----------------------------------------------------

    def _initialize_incident_manager_once(self, config: AlertsVerificationConfig) -> None:
        if self._incident_manager_initialized:
            return
        try:
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager:
                self.logger.info("%s Incident manager ready", _INCIDENT_LOG)
            else:
                self.logger.warning(
                    "%s Incident manager unavailable; incidents will not be published",
                    _INCIDENT_LOG,
                )
        except _INTEGRATION_ERRORS as exc:
            self.logger.error("%s Incident manager init failed: %s", _INCIDENT_LOG, exc)
        finally:
            self._incident_manager_initialized = True

    def _send_incident_to_manager(
        self,
        incident: Dict,
        stream_info: Optional[Dict[str, Any]],
        context: Optional[ProcessingContext],
    ) -> bool:
        """Publish through IncidentManager; report whether it went out."""
        if not incident:
            if context is not None:
                context.metadata["incident_published_via_manager"] = False
            return False

        published = False
        camera_id = _resolve_camera_id(stream_info)
        if self._incident_manager:
            try:
                published = bool(
                    self._incident_manager.process_incident(
                        camera_id=camera_id,
                        incident_data=incident,
                        stream_info=stream_info,
                    )
                )
            except _INTEGRATION_ERRORS as exc:
                self.logger.error("%s Error publishing incident: %s", _INCIDENT_LOG, exc)

        if context is not None:
            # IncidentManager owns the open/close lifecycle when it is active, so
            # PostProcessor must not also publish a legacy incident_res for this frame.
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)
        return published

    # -- pipeline ------------------------------------------------------------

    def _filter_and_map(self, data: Any, config: AlertsVerificationConfig) -> List[Dict]:
        """Threshold, map indices to names, then keep only what alerts."""
        processed = data
        if config.confidence_threshold is not None:
            processed = filter_by_confidence(processed, config.confidence_threshold)
        if config.index_to_category:
            processed = apply_category_mapping(processed, config.index_to_category)
        targets = set(config.target_categories)
        return [d for d in processed if str(d.get("category", "")).lower() in targets]

    def _build_incident(
        self,
        detections: List[Dict],
        severity: str,
        reason: str,
        alerts: List[Dict],
        stream_info: Optional[Dict[str, Any]],
    ) -> Dict:
        """One incident for this frame's fire."""
        timestamp = _stream_timestamp(stream_info)
        self._incident_counter += 1
        confidence_pct = _max_confidence_pct(detections)

        human_text = (
            f"Fire detected -- {len(detections)} detection(s), "
            f"confidence {confidence_pct:.1f}%, severity {severity}"
        )
        event = self.create_incident(
            incident_id=f"incident_{self.CASE_TYPE}_{self._incident_counter}",
            incident_type=self.CASE_TYPE,
            severity_level=severity,
            human_text=human_text,
            camera_info=self.get_camera_info_from_stream(stream_info),
            alerts=alerts,
            alert_settings=[],
            start_time=timestamp,
            end_time="Incident still active",
            level_settings=_LEVEL_SETTINGS,
        )
        event["incident_quant"] = confidence_pct
        # Distinguishes "the verifier passed it" from "nothing checked it", which is the
        # whole reason this use case exists as its own thing.
        event["verification_reason"] = reason
        return event

    def _build_alerts(
        self,
        detections: List[Dict],
        severity: str,
        stream_info: Optional[Dict[str, Any]],
    ) -> List[Dict]:
        """The alert objects carried on the incident."""
        return [
            {
                "alert_id": f"alert_{self.CASE_TYPE}_{self._incident_counter + 1}",
                "alert_type": "fire_detected",
                "severity_level": severity,
                "detection_count": len(detections),
                "confidence_pct": _max_confidence_pct(detections),
                "timestamp": _stream_timestamp(stream_info),
                "camera_id": _resolve_camera_id(stream_info),
            }
        ]

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """Alert on this frame's fire, if any."""
        started = time.monotonic()
        try:
            if not isinstance(config, AlertsVerificationConfig):
                return self.create_error_result(
                    "Invalid configuration type for alerts verification",
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
            if config.alert_config is None:
                config.alert_config = AlertConfig(**_DEFAULT_ALERT_CONFIG_KWARGS)

            detections = self._filter_and_map(data, config)
            incident, alerts, severity, reason = self._decide(detections, config, stream_info)
            self._send_incident_to_manager(incident, stream_info, context)

            context.processing_time = time.monotonic() - started
            context.mark_completed()
            summary = self._agg_summary(detections, incident, alerts, severity, reason)
            return self.create_result(
                data={"agg_summary": summary},
                usecase=self.name,
                category=self.category,
                context=context,
            )

        except Exception as exc:
            self.logger.error("Error in alerts verification processing: %s", exc, exc_info=True)
            return self.create_error_result(
                f"Alerts verification processing failed: {exc}",
                error_type="AlertsVerificationProcessingError",
                usecase=self.name,
                category=self.category,
                context=context,
            )

    def _decide(
        self,
        detections: List[Dict],
        config: AlertsVerificationConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Tuple[Dict, List[Dict], str, str]:
        """Whether this frame raises an alert, and what it says.

        Split out of `process` so the alerting decision reads on one screen: the streak,
        the severity, the verifier's verdict, and nothing else.
        """
        if not detections:
            self._consecutive_fire_frames = 0
            return {}, [], "", "no_detection"

        self._consecutive_fire_frames += 1
        if self._consecutive_fire_frames < config.min_confirmation_frames:
            return {}, [], "", "awaiting_confirmation"

        severity = _level_from_confidence_pct(_max_confidence_pct(detections))
        confirmed, reason = self._verify_alert(detections, severity, stream_info)
        if not confirmed:
            self.logger.info("Alert rejected by verification: %s", reason)
            return {}, [], severity, reason

        alerts = self._build_alerts(detections, severity, stream_info)
        incident = self._build_incident(detections, severity, reason, alerts, stream_info)
        return incident, alerts, severity, reason

    def _agg_summary(
        self,
        detections: List[Dict],
        incident: Dict,
        alerts: List[Dict],
        severity: str,
        reason: str,
    ) -> Dict[str, Any]:
        """The standard agg_summary envelope, carrying incidents and alerts only.

        No metrics or widgets: this use case reports events, and a count series would be a
        second, quieter claim about the same detections.
        """
        return {
            "alerts_verification": {
                "incidents": incident,
                "alerts": alerts,
                "business_analytics": [],
                "human_text": incident.get("human_text", "") if incident else "",
                "alerts_verification_analytics": {
                    "fire_detections": len(detections),
                    "consecutive_frames": self._consecutive_fire_frames,
                    "severity_level": severity,
                    "verification_reason": reason,
                },
            }
        }
