"""IncidentProcessor -- standalone INCIDENT category processor.

Thin orchestrator that delegates quantification to :mod:`quant_strategies`
and lifecycle state management to :class:`IncidentLifecycle`.  Configured
entirely from the YAML manifest via :class:`IncidentProcessorConfig`.

**Does NOT inherit ``BaseMetricProcessor``.**  Incidents are event-driven,
not aggregated: there are no metrics, no 1-minute windows, no track-ID
counting.  The only output is a per-frame :class:`IncidentFrameResult` and
a queue of :class:`IncidentEvent` models drained by the engine for
publishing to Redis/Kafka.
"""
from __future__ import annotations

import logging
from typing import Any

from ..incident_lifecycle import IncidentLifecycle
from ..quant_strategies import compute_quant
from ..schemas import (
    SEVERITY_ORDER,
    IncidentEvent,
    IncidentFrameResult,
    IncidentLifecycleState,
    IncidentProcessorConfig,
    IncidentThreshold,
    IncidentTypeConfig,
    LifecycleConfig,
    QuantStrategyConfig,
    SeverityLevel,
)


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Default thresholds (match original IncidentProcessor)
# ---------------------------------------------------------------------------

DEFAULT_THRESHOLDS: list[dict[str, Any]] = [
    {"level": "low", "percentage": 1},
    {"level": "medium", "percentage": 3},
    {"level": "significant", "percentage": 13},
    {"level": "critical", "percentage": 30},
]


# ---------------------------------------------------------------------------
# Severity calculation (standalone, reusable)
# ---------------------------------------------------------------------------


def calculate_severity(
    incident_quant: float,
    thresholds: list[dict[str, Any]],
    order: str = "ascending",
) -> SeverityLevel:
    """Determine severity from *incident_quant* using *thresholds*.

    For ascending order (higher quant = more severe): returns the highest
    level whose ``percentage`` is <= *incident_quant*.

    Args:
        incident_quant: Quantitative incident measurement (0-100).
        thresholds: List of ``{"level": str, "percentage": float}`` dicts.
        order: ``"ascending"`` or ``"descending"``.

    Returns:
        Resolved :class:`SeverityLevel`.
    """
    if incident_quant is None or incident_quant < 0:
        return SeverityLevel.none

    sorted_t = sorted(thresholds, key=lambda x: float(x.get("percentage", 0)))

    if not sorted_t:
        return SeverityLevel.none

    if order == "descending":
        first_pct = float(sorted_t[0].get("percentage", 0))
        if incident_quant < first_pct:
            raw = sorted_t[0].get("level", "none")
        else:
            raw = sorted_t[-1].get("level", "none")
            for i in range(len(sorted_t) - 1):
                curr_pct = float(sorted_t[i].get("percentage", 0))
                next_pct = float(sorted_t[i + 1].get("percentage", 0))
                if curr_pct <= incident_quant < next_pct:
                    raw = sorted_t[i + 1].get("level", "none")
                    break
    else:
        raw = "none"
        for t in sorted_t:
            pct = float(t.get("percentage", 0))
            if incident_quant >= pct:
                raw = t.get("level", "none")
            else:
                break

    severity = str(raw).lower()
    if severity not in SEVERITY_ORDER:
        return SeverityLevel.none

    return SeverityLevel(severity)


# ---------------------------------------------------------------------------
# Helpers — config parsing
# ---------------------------------------------------------------------------


def _build_entity_mapping(raw: dict[str, Any]) -> dict[str, str]:
    """Build ``{detection_class: entity}`` reverse lookup from manifest."""
    mapping: dict[str, str] = {}
    for entity, classes in raw.items():
        for cls in [classes] if isinstance(classes, str) else classes:
            mapping[cls] = entity
    return mapping


def _parse_incident_types(raw: list[Any]) -> list[IncidentTypeConfig]:
    """Parse raw incident type dicts into validated Pydantic models."""
    result: list[IncidentTypeConfig] = []
    for item in raw or []:
        if isinstance(item, IncidentTypeConfig):
            result.append(item)
        elif isinstance(item, dict):
            raw_thresholds = item.get("thresholds", [])
            thresholds: list[IncidentThreshold] = []
            if isinstance(raw_thresholds, list):
                thresholds.extend(
                    IncidentThreshold(
                        level=t.get("level", ""),
                        percentage=float(t.get("percentage", 0)),
                    )
                    for t in raw_thresholds
                    if isinstance(t, dict)
                )
            elif isinstance(raw_thresholds, dict):
                thresholds.extend(
                    IncidentThreshold(level=str(lvl), percentage=float(pct)) for lvl, pct in raw_thresholds.items()
                )
            result.append(
                IncidentTypeConfig(
                    key=item.get("key", ""),
                    name=item.get("name", ""),
                    thresholds=thresholds,
                    order=item.get("order", "ascending"),
                )
            )
    return result


def _parse_incident_config(manifest: dict[str, Any]) -> IncidentProcessorConfig:
    """Build :class:`IncidentProcessorConfig` from the full manifest dict."""
    incident_section = manifest.get("incident", {}) or {}

    raw_types = incident_section.get(
        "incidentTypes",
        manifest.get("incidentTypes", []),
    )
    incident_types = _parse_incident_types(raw_types)

    quant = QuantStrategyConfig(
        strategy=incident_section.get("quant_strategy", "max_confidence"),
        threshold_area=float(incident_section.get("threshold_area", 250200.0)),
        count_threshold=int(incident_section.get("count_threshold", 10)),
    )

    lifecycle_raw = incident_section.get("lifecycle", {}) or {}
    lifecycle = LifecycleConfig(**lifecycle_raw)

    return IncidentProcessorConfig(
        incident_types=incident_types,
        quant=quant,
        lifecycle=lifecycle,
    )


def _extract_camera_id(detections: list[dict[str, Any]]) -> str:
    """Extract ``_camera_id`` from the first detection that carries it."""
    for det in detections:
        cid = det.get("_camera_id")
        if cid:
            return str(cid)
    return ""


def _map_level_from_backend(level: str) -> str:
    """Map backend ``"high"`` to internal ``"significant"``."""
    return "significant" if level.lower().strip() == "high" else level


# ---------------------------------------------------------------------------
# IncidentProcessor
# ---------------------------------------------------------------------------


class IncidentProcessor:
    """Standalone INCIDENT category processor.

    No metrics, no aggregation, no inheritance from ``BaseMetricProcessor``.
    Delegates quant computation to :func:`compute_quant` and lifecycle
    management to :class:`IncidentLifecycle`.  Configured from a YAML
    manifest via :class:`IncidentProcessorConfig`.

    Args:
        manifest_config: Full parsed manifest dict (same structure loaded
            from ``fire_detection.yaml``, ``weapon_detection.yaml``, etc.).
    """

    def __init__(self, manifest_config: dict[str, Any]) -> None:
        """Initialize from a parsed YAML manifest dict."""
        self._manifest = manifest_config
        self._config = _parse_incident_config(manifest_config)

        self._class_to_entity = _build_entity_mapping(
            manifest_config.get("entity_mapping", {}),
        )

        self._lifecycle = IncidentLifecycle(self._config.lifecycle)
        self._pending_events: list[IncidentEvent] = []
        self._threshold_overrides: dict[str, list[dict[str, Any]]] = {}
        self._current_camera_id: str = "default_camera"

        self.category: str = "INCIDENT"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process_frame(
        self,
        detections: list[dict[str, Any]],
        frame_ts: float,
        frame_id: str = "",
    ) -> IncidentFrameResult:
        """Process one frame of detections through the incident pipeline.

        1. Filter detections by entity mapping.
        2. Compute ``incident_quant`` via the configured quant strategy.
        3. Resolve severity from thresholds.
        4. Run the lifecycle state machine (consecutive-frame validation).
        5. Return an :class:`IncidentFrameResult` snapshot.

        Emitted :class:`IncidentEvent` objects are buffered internally and
        retrieved via :meth:`drain_events`.
        """
        filtered = self._filter_detections(detections)

        if filtered:
            camera_id = _extract_camera_id(filtered) or self._current_camera_id
            self._current_camera_id = camera_id
        else:
            camera_id = self._current_camera_id

        incident_type = self._get_primary_incident_type()

        if filtered:
            quant, confidence = compute_quant(filtered, self._config.quant)
            thresholds = self._resolve_thresholds(camera_id)
            order = self._config.incident_types[0].order if self._config.incident_types else "ascending"
            severity = calculate_severity(quant, thresholds, order)
        else:
            quant, confidence, severity = 0.0, 0.0, SeverityLevel.none

        events = self._lifecycle.process_frame(
            camera_id=camera_id,
            severity_level=severity,
            incident_quant=quant,
            event_confidence=confidence,
            frame_ts=frame_ts,
            frame_id=frame_id,
            incident_type=incident_type,
        )
        self._pending_events.extend(events)

        state = self._lifecycle.get_state(camera_id)
        return IncidentFrameResult(
            camera_id=camera_id,
            incident_type=incident_type,
            severity_level=severity,
            incident_quant=quant,
            event_confidence=confidence,
            incident_active=state.incident_active if state else False,
            event_detected_count=state.event_detected_count if state else 0,
            events_emitted=len(events),
        )

    def drain_events(self) -> list[IncidentEvent]:
        """Return and clear all pending incident events (Pydantic models)."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    def update_thresholds(
        self,
        camera_id: str,
        thresholds: list[dict[str, Any]],
        incident_type: str = "",
    ) -> None:
        """Set runtime threshold overrides for a camera.

        Maps backend ``"high"`` to internal ``"significant"`` on input.
        """
        normalised = []
        for t in thresholds:
            level = _map_level_from_backend(t.get("level", ""))
            normalised.append(
                {"level": level, "percentage": float(t.get("percentage", 0))},
            )
        self._threshold_overrides[camera_id] = normalised
        logger.info("Updated thresholds for camera %s: %s", camera_id, normalised)

    def get_lifecycle_state(self, camera_id: str) -> IncidentLifecycleState | None:
        """Return a copy of the lifecycle state for *camera_id*."""
        return self._lifecycle.get_state(camera_id)

    def reset(self) -> None:
        """Full reset — clears lifecycle state, pending events, and overrides."""
        self._lifecycle.reset()
        self._pending_events.clear()
        self._threshold_overrides.clear()
        self._current_camera_id = "default_camera"

    # ------------------------------------------------------------------
    # Detection filtering
    # ------------------------------------------------------------------

    def _filter_detections(
        self,
        detections: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Filter detections to mapped entity classes.

        If no entity mapping is configured, all detections pass through.
        """
        if not self._class_to_entity:
            return detections

        result = []
        for det in detections:
            raw_class = det.get("category", "")
            entity = self._class_to_entity.get(raw_class)
            if entity is not None:
                result.append({**det, "category": entity})
        return result

    # ------------------------------------------------------------------
    # Threshold resolution
    # ------------------------------------------------------------------

    def _resolve_thresholds(self, camera_id: str) -> list[dict[str, Any]]:
        """Return thresholds for a camera: runtime override > manifest > defaults."""
        if camera_id in self._threshold_overrides:
            return self._threshold_overrides[camera_id]

        if self._config.incident_types:
            it = self._config.incident_types[0]
            return [{"level": t.level, "percentage": t.percentage} for t in it.thresholds]

        return list(DEFAULT_THRESHOLDS)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_primary_incident_type(self) -> str:
        """Return the primary incident type key from the manifest."""
        if self._config.incident_types:
            return self._config.incident_types[0].key
        return "incident"
