"""IncidentLifecycle -- pure state machine for incident lifecycle management.

Receives a ``SeverityLevel`` per frame per camera, maintains per-camera
``IncidentLifecycleState`` (Pydantic), and returns ``IncidentEvent`` models
on state transitions.

No I/O, no Redis, no Kafka.  The caller drains the returned events and
decides how to publish them.

State machine behaviour (unchanged from the original INCIDENT_MANAGER):

* A detection is only *confirmed* after a configurable number of
  consecutive frames at the same severity level (5 for medium / significant
  / critical, 10 for low).
* An incident remains *active* during the cooldown period (frames with no
  detection).
* After a configurable number of consecutive empty frames (default 101) the
  incident ends and an ``"info"`` end-signal event is emitted.
* After the end signal a new *cycle* begins (``cycle_id`` increments).
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone

from .schemas import (
    SEVERITY_ORDER,
    IncidentEvent,
    IncidentLifecycleState,
    LifecycleConfig,
    SeverityLevel,
)


logger = logging.getLogger(__name__)


def _map_level_to_backend(level: str) -> str:
    """Map internal ``"significant"`` to backend ``"high"``."""
    return "high" if level == "significant" else level


def _generate_incident_id(camera_id: str, cycle_id: int) -> str:
    """Generate a globally-unique, fully-random incident ID.

    The ID is a random ``uuid4`` (with a constant ``incident_`` prefix so the
    string stays identifiable). Being fully random, it never collides across
    concurrent applications running on the same camera, nor across an
    application restart (which resets ``cycle_id`` back to 1). ``camera_id``
    and ``cycle_id`` are accepted for signature compatibility but no longer
    embedded in the ID. It is regenerated only when a new cycle begins, so it
    stays stable across frames within a single incident.
    """
    return f"incident_{uuid.uuid4().hex}"


class IncidentLifecycle:
    """Per-camera incident lifecycle state machine.

    Pure computation: no I/O.  Given a severity level for each frame it
    maintains per-camera state and emits :class:`IncidentEvent` instances
    when the confirmed severity level changes or an incident ends.

    Args:
        config: Tunable consecutive-frame thresholds.
    """

    def __init__(self, config: LifecycleConfig | None = None) -> None:
        """Initialize with optional lifecycle configuration (defaults applied)."""
        self._config = config or LifecycleConfig()
        self._states: dict[str, IncidentLifecycleState] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process_frame(
        self,
        camera_id: str,
        severity_level: SeverityLevel,
        incident_quant: float,
        event_confidence: float,
        frame_ts: float,
        frame_id: str,
        incident_type: str,
    ) -> list[IncidentEvent]:
        """Run one frame through the lifecycle for *camera_id*.

        Args:
            camera_id: Unique camera identifier.
            severity_level: Computed severity for this frame.
            incident_quant: Quantitative incident measurement (0-100).
            event_confidence: Maximum detection confidence (0-1).
            frame_ts: Frame timestamp in seconds.
            frame_id: Frame identifier string.
            incident_type: Incident type key from the manifest.

        Returns:
            List of ``IncidentEvent`` models emitted this frame (usually 0 or 1).
        """
        state = self._get_or_create_state(camera_id)
        events: list[IncidentEvent] = []

        if severity_level == SeverityLevel.none:
            self._handle_empty_frame(
                camera_id,
                state,
                frame_ts,
                frame_id,
                incident_type,
                events,
            )
        else:
            self._handle_detection(
                camera_id,
                state,
                severity_level,
                incident_quant,
                event_confidence,
                frame_ts,
                frame_id,
                incident_type,
                events,
            )

        return events

    def get_state(self, camera_id: str) -> IncidentLifecycleState | None:
        """Return a copy of the lifecycle state for a camera, or ``None``."""
        state = self._states.get(camera_id)
        if state is None:
            return None
        return state.model_copy()

    def get_all_states(self) -> dict[str, IncidentLifecycleState]:
        """Return copies of all per-camera lifecycle states."""
        return {cid: s.model_copy() for cid, s in self._states.items()}

    def reset(self) -> None:
        """Clear all per-camera state."""
        self._states.clear()

    def reset_camera(self, camera_id: str) -> None:
        """Clear state for a single camera."""
        self._states.pop(camera_id, None)

    # ------------------------------------------------------------------
    # Internals — detection handling
    # ------------------------------------------------------------------

    def _handle_detection(
        self,
        camera_id: str,
        state: IncidentLifecycleState,
        severity_level: SeverityLevel,
        incident_quant: float,
        event_confidence: float,
        frame_ts: float,
        frame_id: str,
        incident_type: str,
        events: list[IncidentEvent],
    ) -> None:
        """Process a frame with a real detection (severity != none)."""
        state.empty_frames_count = 0

        if severity_level == state.pending_level:
            state.consecutive_count += 1
        else:
            state.pending_level = severity_level
            state.consecutive_count = 1

        frames_required = self._get_frames_required(severity_level)

        if state.consecutive_count < frames_required:
            return

        old_level = state.current_level
        new_level = state.pending_level

        if new_level == state.current_level:
            return

        state.current_level = new_level

        should_publish = new_level != SeverityLevel.none and new_level != state.last_published_level
        if not should_publish:
            return

        if not state.incident_active:
            state.event_detected_count += 1
        state.incident_active = True

        if not state.start_time:
            state.start_time = datetime.now(tz=timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ",
            )

        is_escalation = (
            old_level.value in SEVERITY_ORDER
            and new_level.value in SEVERITY_ORDER
            and SEVERITY_ORDER.index(new_level.value) > SEVERITY_ORDER.index(old_level.value)
            and old_level != SeverityLevel.none
        )

        events.append(
            self._build_event(
                camera_id=camera_id,
                state=state,
                severity_level=new_level,
                incident_type=incident_type,
                incident_quant=incident_quant,
                event_confidence=event_confidence,
                frame_id=frame_id,
                is_escalation=is_escalation,
            ),
        )
        state.last_published_level = new_level

    # ------------------------------------------------------------------
    # Internals — empty-frame handling
    # ------------------------------------------------------------------

    def _handle_empty_frame(
        self,
        camera_id: str,
        state: IncidentLifecycleState,
        frame_ts: float,
        frame_id: str,
        incident_type: str,
        events: list[IncidentEvent],
    ) -> None:
        """Process a frame with no detection (severity == none).

        After ``consecutive_frames_empty`` empty frames with an active
        incident, emits an ``"info"`` end-signal and starts a new cycle.
        """
        state.empty_frames_count += 1

        if state.pending_level not in (SeverityLevel.none, SeverityLevel.info):
            state.pending_level = SeverityLevel.none
            state.consecutive_count = 0

        if state.empty_frames_count < self._config.consecutive_frames_empty:
            return

        should_send_info = state.incident_active and state.last_published_level not in (
            SeverityLevel.info,
            SeverityLevel.none,
        )

        if should_send_info:
            events.append(
                self._build_event(
                    camera_id=camera_id,
                    state=state,
                    severity_level=SeverityLevel.info,
                    incident_type=incident_type,
                    incident_quant=0.0,
                    event_confidence=0.0,
                    frame_id=frame_id,
                    is_end_signal=True,
                ),
            )

            state.last_published_level = SeverityLevel.info
            state.incident_cycle_id += 1
            state.current_incident_id = _generate_incident_id(
                camera_id,
                state.incident_cycle_id,
            )
            state.incident_active = False
            state.current_level = SeverityLevel.none
            state.pending_level = SeverityLevel.none
            state.consecutive_count = 0
            state.empty_frames_count = 0
            state.start_time = ""
        else:
            state.empty_frames_count = 0

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_or_create_state(self, camera_id: str) -> IncidentLifecycleState:
        if camera_id not in self._states:
            state = IncidentLifecycleState()
            state.current_incident_id = _generate_incident_id(
                camera_id,
                state.incident_cycle_id,
            )
            self._states[camera_id] = state
        return self._states[camera_id]

    def _get_frames_required(self, level: SeverityLevel) -> int:
        if level == SeverityLevel.low:
            return self._config.consecutive_frames_low
        return self._config.consecutive_frames_default

    @staticmethod
    def _build_event(
        camera_id: str,
        state: IncidentLifecycleState,
        severity_level: SeverityLevel,
        incident_type: str,
        incident_quant: float,
        event_confidence: float,
        frame_id: str,
        is_escalation: bool = False,
        is_end_signal: bool = False,
    ) -> IncidentEvent:
        mapped_level = _map_level_to_backend(severity_level.value)
        return IncidentEvent(
            incident_id=state.current_incident_id,
            incident_type=incident_type,
            severity_level=mapped_level,
            human_text=(
                "Incident ended" if is_end_signal else f"INCIDENT DETECTED: {incident_type} severity={mapped_level}"
            ),
            start_time=state.start_time,
            end_time=("" if not is_end_signal else datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
            camera_id=camera_id,
            cycle_id=state.incident_cycle_id,
            is_escalation=is_escalation,
            is_end_signal=is_end_signal,
            incident_quant=incident_quant,
            event_confidence=event_confidence,
            frame_id=frame_id,
        )
