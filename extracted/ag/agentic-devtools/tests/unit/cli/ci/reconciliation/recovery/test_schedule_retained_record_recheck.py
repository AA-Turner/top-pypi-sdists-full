"""Tests for retained-record recovery helpers."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from agentic_devtools.cli.ci.reconciliation.models import (
    CandidateInventoryRecord,
    LifecycleState,
    ObservationOutcome,
    RecoveryDisposition,
    ScopeClassification,
    TriStateValue,
)
from agentic_devtools.cli.ci.reconciliation.recovery import restart_recovery_epoch, schedule_retained_record_recheck


def _record() -> CandidateInventoryRecord:
    return CandidateInventoryRecord(
        record_id="owner/repo#1",
        repo="owner/repo",
        pr_number=1,
        target_branch="main",
        lifecycle_state=LifecycleState.INACCESSIBLE,
        scope_classification=ScopeClassification.RETAINED_AUDIT_ONLY,
        eligibility_state=TriStateValue.UNKNOWN,
        observation_outcome=ObservationOutcome.TRUSTED_INACCESSIBLE,
        observed_at_utc_z="2026-09-15T12:00:00Z",
        observed_monotonic_seconds=10.0,
    )


def test_schedule_retained_record_recheck_requires_aware_datetime() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        schedule_retained_record_recheck(_record(), now_utc=datetime(2026, 9, 15, 12, 0))


def test_schedule_retained_record_recheck_tracks_exhaustion() -> None:
    scheduled = schedule_retained_record_recheck(
        _record(),
        now_utc=datetime(2026, 9, 15, 12, 0, tzinfo=UTC),
        interval_minutes=30,
        max_attempts=1,
    )
    assert scheduled.recovery_disposition == RecoveryDisposition.EXHAUSTED
    assert "limit=1" in scheduled.exhaustion_metadata
    with pytest.raises(ValueError, match="max_attempts"):
        schedule_retained_record_recheck(
            _record(),
            now_utc=datetime(2026, 9, 15, 12, 0, tzinfo=UTC),
            max_attempts=0,
        )


def test_restart_recovery_epoch_validates_inputs_and_resets_attempts() -> None:
    record = _record()
    restarted = restart_recovery_epoch(
        record,
        actor="operator",
        reason="manual verification",
        no_late_write_confirmed=True,
    )
    assert restarted.recovery_epoch == record.recovery_epoch + 1
    assert restarted.recovery_attempt_count == 0
    with pytest.raises(ValueError):
        restart_recovery_epoch(record, actor="", reason="x", no_late_write_confirmed=True)
    with pytest.raises(ValueError):
        restart_recovery_epoch(record, actor="a", reason="", no_late_write_confirmed=True)
    with pytest.raises(ValueError):
        restart_recovery_epoch(record, actor="a", reason="x", no_late_write_confirmed=False)
