"""Tests for reclaim_leases()."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.recovery import reclaim_leases


def _empty_state() -> QueueState:
    return QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[])


def test_returns_state() -> None:
    state = _empty_state()
    assert reclaim_leases(state).revision == state.revision


def test_importable_from_package() -> None:
    from agentic_devtools.cli.ci.reconciliation import reclaim_leases as exported

    assert callable(exported)


def test_honors_per_cycle_limit() -> None:
    state = _empty_state()
    expiry = datetime.now(UTC) - timedelta(minutes=1)
    for pr_number in (1, 2):
        state.items[pr_number] = WorkItem(
            pr_number=pr_number,
            repo=state.repo,
            change_id=f"change-{pr_number}",
            eligibility="eligible",
            due_at=None,
            status=WorkItemStatus.LEASED,
            claim_id=f"claim-{pr_number}",
            lease_id=f"lease-{pr_number}",
            operation_id=f"operation-{pr_number}",
            lease_expires_at=expiry,
        )
    reclaimed = reclaim_leases(state, max_reclaims=1, now_utc=datetime.now(UTC))
    assert sum(item.status == WorkItemStatus.QUEUED for item in reclaimed.items.values()) == 1
    assert sum(item.status == WorkItemStatus.LEASED for item in reclaimed.items.values()) == 1


def test_stops_after_configured_cycle_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config, "MAX_LEASE_RECLAIMS_PER_CYCLE", 1)
    monkeypatch.setattr(config, "MAX_LEASE_RECLAIM_CYCLES", 2)
    expiry = datetime.now(UTC) - timedelta(minutes=1)
    state = _empty_state()
    for pr_number in (1, 2, 3):
        state.items[pr_number] = WorkItem(
            pr_number=pr_number,
            repo=state.repo,
            change_id=f"change-{pr_number}",
            eligibility="eligible",
            due_at=None,
            status=WorkItemStatus.LEASED,
            claim_id=f"claim-{pr_number}",
            lease_id=f"lease-{pr_number}",
            operation_id=f"operation-{pr_number}",
            lease_expires_at=expiry,
        )
    state = reclaim_leases(state, now_utc=datetime.now(UTC))
    state = reclaim_leases(state, now_utc=datetime.now(UTC))
    stopped = reclaim_leases(state, now_utc=datetime.now(UTC))
    assert stopped.lease_reclaim_cycles == 0
    assert stopped.reclamation_limit_reached is False
    assert stopped.items[3].status == WorkItemStatus.QUARANTINED
    assert stopped.items[3].lease_id == ""
    assert stopped.records[-1].provider_status == "alertable"
    assert "pr_numbers=[3]" in stopped.records[-1].message


def test_retry_and_pagination_limits_are_recorded() -> None:
    from agentic_devtools.cli.ci.reconciliation.recovery import (
        enforce_retry_limit,
        handle_pagination_exhaustion,
    )

    state = _empty_state()
    state.items[1] = WorkItem(1, state.repo, "change", "eligible", None, WorkItemStatus.QUEUED)
    state = enforce_retry_limit(state, 1, max_attempts=1)
    assert state.items[1].status == WorkItemStatus.QUARANTINED
    assert state.quarantines
    state = handle_pagination_exhaustion(state, cursor="cursor")
    assert state.records[-1].provider_status == "alertable"
    assert state.records[-1].message == "pagination exhausted at cursor='cursor'"


def test_retry_below_limit_and_invalid_inputs() -> None:
    from agentic_devtools.cli.ci.reconciliation.recovery import enforce_retry_limit

    state = _empty_state()
    state.items[1] = WorkItem(1, state.repo, "change", "eligible", None, WorkItemStatus.QUEUED)
    assert enforce_retry_limit(state, 1, max_attempts=2).items[1].retry_count == 1
    with pytest.raises(ValueError):
        enforce_retry_limit(state, 1, max_attempts=0)
    with pytest.raises(KeyError):
        enforce_retry_limit(state, 2)


def test_provider_failure_duration_and_timestamp_validation() -> None:
    from agentic_devtools.cli.ci.reconciliation.recovery import record_provider_failure

    started = datetime.now(UTC) - timedelta(seconds=1)
    state = record_provider_failure(_empty_state(), failure_started_at=started, now_utc=datetime.now(UTC))
    assert state.records[-1].provider_status == "provider_failure"
    assert state.records[-1].message.startswith("provider failure duration=")
    with pytest.raises(ValueError):
        record_provider_failure(_empty_state(), failure_started_at=datetime.now(), now_utc=datetime.now(UTC))


def test_provider_failure_becomes_alertable_after_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    from agentic_devtools.cli.ci.reconciliation import config
    from agentic_devtools.cli.ci.reconciliation.recovery import record_provider_failure

    monkeypatch.setattr(config, "MAX_PROVIDER_FAILURE_DURATION", 1)
    now = datetime.now(UTC)
    state = record_provider_failure(
        _empty_state(),
        failure_started_at=now - timedelta(seconds=1),
        now_utc=now,
    )
    assert state.records[-1].provider_status == "alertable"


def test_provider_failure_rejects_naive_now() -> None:
    from agentic_devtools.cli.ci.reconciliation.recovery import record_provider_failure

    with pytest.raises(ValueError):
        record_provider_failure(
            _empty_state(),
            failure_started_at=datetime.now(UTC),
            now_utc=datetime.now(),
        )
