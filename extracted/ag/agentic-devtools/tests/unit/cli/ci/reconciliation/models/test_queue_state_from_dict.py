"""Tests for queue_state_from_dict()."""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.reconciliation.models import (
    CooldownProbe,
    ProbeStatus,
    QuarantineRecord,
    QueueState,
    ReconciliationRecord,
    WorkItem,
    WorkItemStatus,
    queue_state_from_dict,
)


def test_round_trip_from_asdict_returns_equivalent_state() -> None:
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    state = QueueState(
        repo="owner/repo",
        revision=7,
        items={
            1: WorkItem(
                pr_number=1,
                repo="owner/repo",
                change_id="change-1",
                eligibility="eligible",
                due_at=now,
                status=WorkItemStatus.LEASED,
                claim_id="claim-1",
                lease_id="lease-1",
                lease_expires_at=now + timedelta(minutes=5),
                operation_id="operation-1",
                retry_count=2,
                last_observed_at=now,
            )
        },
        records=[
            ReconciliationRecord(
                record_id="record-1",
                repo="owner/repo",
                run_id="run-1",
                started_at=now,
                completed_at=now + timedelta(minutes=1),
                observation_watermark="sha-1",
                cursor_progress="cursor-1",
                provider_status="ok",
                message="recorded diagnostic",
                run_duration_seconds=12.5,
                invalidations=(1,),
                unknown_outcomes=(2,),
            )
        ],
        quarantines=[
            QuarantineRecord(
                quarantine_id="quarantine-1",
                repo="owner/repo",
                reason="bad-data",
                evidence_digest="deadbeef",
                evidence="{}",
                quarantined_at=now,
                recovery_epoch=1,
                rehydration_attempted=True,
            )
        ],
        recovery_epoch=2,
        last_updated_at=now,
        state_ref="custom-state-ref",
        probes=[
            CooldownProbe(
                probe_id="probe-1",
                provider_identity="gh",
                credential_identity="cred-1",
                cooldown_generation_id="generation-1",
                status=ProbeStatus.FAILED,
                scheduled_at=now,
                attempted_at=now,
                resume_at=now,
                next_probe_at=now + timedelta(minutes=5),
                retry_count=1,
                alert_reason="provider-down",
            )
        ],
        lease_reclaim_cycles=1,
        reclamation_limit_reached=True,
        pagination_cursor="cursor-1",
        full_scan_complete=True,
        next_inventory_at=now + timedelta(minutes=20),
        inventory_invalidated=False,
    )

    assert queue_state_from_dict(asdict(state)) == state


def test_missing_fields_use_defaults() -> None:
    state = queue_state_from_dict({"repo": "owner/repo"})

    assert state.repo == "owner/repo"
    assert state.revision == 0
    assert state.items == {}
    assert state.records == []
    assert state.quarantines == []
    assert state.recovery_epoch == 0
    assert state.last_updated_at is None
    assert state.state_ref == "ai-pr-loop-state"
    assert state.probes == []
    assert state.lease_reclaim_cycles == 0
    assert state.reclamation_limit_reached is False
    assert state.pagination_cursor is None
    assert state.full_scan_complete is False
    assert state.next_inventory_at is None
    assert state.inventory_invalidated is True


def test_accepts_numeric_string_key_and_datetime_string() -> None:
    state = queue_state_from_dict(
        {
            "repo": "owner/repo",
            "last_updated_at": "2026-01-02T03:04:05+00:00",
            "items": {
                "1": {
                    "pr_number": 1,
                    "repo": "owner/repo",
                    "change_id": "change-1",
                    "eligibility": "eligible",
                }
            },
        }
    )
    assert state.items[1].pr_number == 1


def test_defaults_record_invalidations() -> None:
    state = queue_state_from_dict(
        {
            "repo": "owner/repo",
            "records": [
                {
                    "record_id": "record-1",
                    "repo": "owner/repo",
                    "run_id": "run-1",
                    "started_at": "2026-01-02T03:04:05+00:00",
                }
            ],
        }
    )
    assert state.records[0].invalidations == ()
    assert state.records[0].message == ""


@pytest.mark.parametrize(
    ("data", "match"),
    [
        ([], "must be a dict"),
        ({"repo": "owner/repo", "revision": True}, "revision must be an int"),
        ({"repo": "owner/repo", "items": []}, "items must be a dict"),
        ({"repo": "owner/repo", "records": {}}, "records must be a list"),
        ({"repo": "owner/repo", "reclamation_limit_reached": "yes"}, "must be a bool"),
        (
            {
                "repo": "owner/repo",
                "items": {
                    "abc": {
                        "pr_number": 1,
                        "repo": "owner/repo",
                        "change_id": "change-1",
                        "eligibility": "eligible",
                        "due_at": None,
                        "status": "queued",
                    }
                },
            },
            "item key must be an integer",
        ),
        ({"repo": "owner/repo", "items": {True: {}}}, "item key must be an integer"),
        ({"repo": 1}, "repo must be a str"),
        ({"repo": "owner/repo", "pagination_cursor": 1}, "pagination_cursor must be a str"),
        ({"repo": "owner/repo", "records": [1]}, "record must be a dict"),
        ({"repo": "owner/repo", "records": [{}]}, "started_at must not be empty"),
        (
            {
                "repo": "owner/repo",
                "records": [{"started_at": 1}],
            },
            "started_at must be an ISO 8601 datetime string",
        ),
        (
            {
                "repo": "owner/repo",
                "records": [{"started_at": "2026-01-02T03:04:05"}],
            },
            "started_at must be timezone-aware",
        ),
        (
            {
                "repo": "owner/repo",
                "records": [
                    {
                        "record_id": "record-1",
                        "repo": "owner/repo",
                        "run_id": "run-1",
                        "started_at": "not-a-datetime",
                    }
                ],
            },
            "started_at must be an ISO 8601 datetime string",
        ),
        (
            {
                "repo": "owner/repo",
                "records": [
                    {
                        "record_id": "record-1",
                        "repo": "owner/repo",
                        "run_id": "run-1",
                        "started_at": datetime(2026, 1, 2, 3, 4, 5),
                    }
                ],
            },
            "started_at must be timezone-aware",
        ),
        (
            {
                "repo": "owner/repo",
                "records": [
                    {
                        "record_id": "record-1",
                        "repo": "owner/repo",
                        "run_id": "run-1",
                        "started_at": datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
                        "run_duration_seconds": "fast",
                    }
                ],
            },
            "run_duration_seconds must be a float",
        ),
        (
            {
                "repo": "owner/repo",
                "records": [
                    {
                        "record_id": "record-1",
                        "repo": "owner/repo",
                        "run_id": "run-1",
                        "started_at": datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
                        "invalidations": [True],
                    }
                ],
            },
            r"invalidations\[0\] must be an int",
        ),
        (
            {
                "repo": "owner/repo",
                "records": [
                    {
                        "record_id": "record-1",
                        "repo": "owner/repo",
                        "run_id": "run-1",
                        "started_at": datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
                        "invalidations": "bad",
                    }
                ],
            },
            "invalidations must be a list or tuple",
        ),
        (
            {
                "repo": "owner/repo",
                "probes": [
                    {
                        "probe_id": "probe-1",
                        "provider_identity": "gh",
                        "credential_identity": "cred-1",
                        "cooldown_generation_id": "generation-1",
                        "status": "not-a-status",
                        "scheduled_at": datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
                    }
                ],
            },
            "status must be one of",
        ),
        (
            {
                "repo": "owner/repo",
                "probes": [
                    {
                        "probe_id": "probe-1",
                        "provider_identity": "gh",
                        "credential_identity": "cred-1",
                        "cooldown_generation_id": "generation-1",
                        "status": 1,
                        "scheduled_at": datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
                    }
                ],
            },
            "status must be a ProbeStatus string",
        ),
    ],
)
def test_invalid_field_types_raise_value_error(data: object, match: str) -> None:
    with pytest.raises(ValueError, match=match):
        queue_state_from_dict(data)  # type: ignore[arg-type]
