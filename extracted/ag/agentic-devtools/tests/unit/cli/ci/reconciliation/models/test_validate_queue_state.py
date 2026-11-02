"""Tests for validate_queue_state()."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

from agentic_devtools.cli.ci.reconciliation.models import (
    CooldownProbe,
    ProbeStatus,
    QueueState,
    WorkItem,
    WorkItemStatus,
    validate_queue_state,
)


def _make_work_item(**kwargs: Any) -> WorkItem:
    defaults: dict[str, Any] = {
        "pr_number": 1,
        "repo": "owner/repo",
        "change_id": "abc",
        "eligibility": "eligible",
        "due_at": None,
        "status": WorkItemStatus.QUEUED,
    }
    defaults.update(kwargs)
    return WorkItem(**defaults)


def test_rejects_foreign_work_item_repo() -> None:
    state = QueueState(
        repo="owner/repo",
        revision=0,
        items={1: _make_work_item(repo="other/repo")},
        records=[],
        quarantines=[],
    )
    with pytest.raises(ValueError, match="does not match QueueState repo"):
        validate_queue_state(state)


def test_rejects_expected_repo_mismatch() -> None:
    with pytest.raises(ValueError, match="expected repo"):
        validate_queue_state(
            QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[]),
            expected_repo="other/repo",
        )


def test_rejects_negative_revision_and_blank_state_ref() -> None:
    state = QueueState(
        repo="owner/repo",
        revision=-1,
        items={},
        records=[],
        quarantines=[],
        state_ref="",
        lease_reclaim_cycles=-1,
    )
    with pytest.raises(ValueError, match="revision"):
        validate_queue_state(state)


def test_rejects_blank_repo() -> None:
    with pytest.raises(ValueError, match="repo"):
        validate_queue_state(QueueState(repo="", revision=0, items={}, records=[], quarantines=[]))


def test_rejects_negative_recovery_epoch() -> None:
    with pytest.raises(ValueError, match="recovery_epoch"):
        validate_queue_state(
            QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[], recovery_epoch=-1)
        )


def test_rejects_negative_lease_reclaim_cycles() -> None:
    with pytest.raises(ValueError, match="lease_reclaim_cycles"):
        validate_queue_state(
            QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[], lease_reclaim_cycles=-1)
        )


def test_rejects_blank_state_ref() -> None:
    with pytest.raises(ValueError, match="state_ref"):
        validate_queue_state(
            QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[], state_ref="")
        )


def test_rejects_state_ref_mismatch() -> None:
    with pytest.raises(ValueError, match="expected state_ref"):
        validate_queue_state(
            QueueState(repo="owner/repo", revision=0, items={}, records=[], quarantines=[], state_ref="ref-a"),
            expected_state_ref="ref-b",
        )


def test_rejects_item_key_mismatch() -> None:
    state = QueueState(
        repo="owner/repo",
        revision=0,
        items={2: _make_work_item(pr_number=1)},
        records=[],
        quarantines=[],
    )
    with pytest.raises(ValueError, match="item key"):
        validate_queue_state(state)


def test_validates_embedded_probes() -> None:
    state = QueueState(
        repo="owner/repo",
        revision=0,
        items={},
        records=[],
        quarantines=[],
        probes=[
            CooldownProbe(
                probe_id="probe-1",
                provider_identity="gh",
                credential_identity="cred",
                cooldown_generation_id="gen-1",
                status=ProbeStatus.PENDING,
                scheduled_at=datetime.now(UTC),
            )
        ],
    )
    validate_queue_state(state)


def test_validates_embedded_work_items() -> None:
    validate_queue_state(
        QueueState(repo="owner/repo", revision=0, items={1: _make_work_item()}, records=[], quarantines=[])
    )
