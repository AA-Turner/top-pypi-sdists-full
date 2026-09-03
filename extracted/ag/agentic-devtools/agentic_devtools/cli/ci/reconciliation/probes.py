"""Cooldown probe adapter implementing the probe state machine."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.models import (
    CooldownProbe,
    CooldownState,
    ProbeStatus,
)


class CooldownProbeAdapter:
    """Implements the cooldown probe state machine."""

    INITIAL_PROBE_WINDOW_MINUTES: int = 5

    def __init__(self, config: dict[str, object] | None = None) -> None:
        self._config = config or {}

    def is_due(self, probe: CooldownProbe, now: datetime) -> bool:
        """Return True when the probe is due."""
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        if probe.status == ProbeStatus.FAILED:
            return probe.next_probe_at is not None and probe.next_probe_at <= now
        if probe.status == ProbeStatus.IN_PROGRESS:
            return probe.claim_expires_at is not None and probe.claim_expires_at <= now
        if probe.status in {ProbeStatus.SUCCEEDED, ProbeStatus.ALERTABLE}:
            return False
        return probe.scheduled_at <= now

    def should_suppress(self, state: CooldownState, now: datetime) -> bool:
        """Return True when the cooldown window has not opened yet."""
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        return state.resume_at > now

    def generate_probe_id(self) -> str:
        """Generate a new probe ID."""
        return str(uuid4())

    def generate_generation_id(self) -> str:
        """Generate a new cooldown generation ID."""
        return str(uuid4())

    def execute_probe(
        self,
        state: CooldownState,
        probe: CooldownProbe,
        availability_result: bool,
        renewed_resume_at: datetime | None,
        now: datetime | None = None,
    ) -> tuple[CooldownState, CooldownProbe]:
        """Execute a probe transition."""
        if now is None:
            now = datetime.now(UTC)
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        if renewed_resume_at is not None and renewed_resume_at.tzinfo is None:
            raise ValueError("renewed_resume_at must be timezone-aware")
        if probe.provider_identity != state.provider_identity:
            raise ValueError("probe provider_identity does not match cooldown state")
        if probe.credential_identity != state.credential_identity:
            raise ValueError("probe credential_identity does not match cooldown state")
        if probe.cooldown_generation_id != state.cooldown_generation_id:
            raise ValueError("probe cooldown_generation_id does not match cooldown state")

        working_state = state
        if not availability_result and renewed_resume_at is not None and renewed_resume_at != state.resume_at:
            working_state = replace(
                state,
                cooldown_generation_id=self.generate_generation_id(),
                resume_at=renewed_resume_at,
                retry_count=0,
                probe_status=ProbeStatus.PENDING,
                next_probe_at=None,
            )
            return working_state, CooldownProbe(
                probe_id=self.generate_probe_id(),
                provider_identity=probe.provider_identity,
                credential_identity=probe.credential_identity,
                cooldown_generation_id=working_state.cooldown_generation_id,
                status=ProbeStatus.PENDING,
                scheduled_at=renewed_resume_at,
                resume_at=renewed_resume_at,
            )

        if availability_result:
            new_probe = replace(
                probe,
                status=ProbeStatus.SUCCEEDED,
                attempted_at=now,
                resume_at=working_state.resume_at,
                cooldown_generation_id=working_state.cooldown_generation_id,
            )
            new_state = replace(working_state, probe_status=ProbeStatus.SUCCEEDED)
            return new_state, new_probe

        new_retry_count = working_state.retry_count + 1
        initial_window_end = working_state.resume_at + timedelta(minutes=self.INITIAL_PROBE_WINDOW_MINUTES)
        retry_anchor = now if now > initial_window_end else initial_window_end
        scheduled_next_probe_at = retry_anchor + timedelta(minutes=new_retry_count * 5)
        max_failure_deadline = working_state.resume_at + timedelta(seconds=config.MAX_PROVIDER_FAILURE_DURATION)
        max_failure_exceeded = scheduled_next_probe_at > max_failure_deadline
        new_probe_status = (
            ProbeStatus.ALERTABLE
            if new_retry_count >= working_state.max_retries or max_failure_exceeded
            else ProbeStatus.FAILED
        )
        next_probe_at: datetime | None = None if max_failure_exceeded else scheduled_next_probe_at
        new_probe = replace(
            probe,
            status=new_probe_status,
            attempted_at=now,
            resume_at=working_state.resume_at,
            next_probe_at=next_probe_at,
            retry_count=new_retry_count,
            cooldown_generation_id=working_state.cooldown_generation_id,
        )
        new_state = replace(
            working_state,
            probe_status=new_probe_status,
            retry_count=new_retry_count,
            next_probe_at=next_probe_at,
        )
        return new_state, new_probe
