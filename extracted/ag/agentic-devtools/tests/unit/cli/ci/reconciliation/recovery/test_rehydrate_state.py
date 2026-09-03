"""Tests for rehydrate_state()."""

from __future__ import annotations

from datetime import UTC, datetime

from agentic_devtools.cli.ci.reconciliation.models import QuarantineRecord, QueueState
from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore
from agentic_devtools.cli.ci.reconciliation.recovery import rehydrate_state


def test_successful_rehydration_advances_epoch_and_unblocks_quarantine() -> None:
    now = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    state = QueueState(
        repo="owner/repo",
        revision=0,
        items={},
        records=[],
        quarantines=[QuarantineRecord("q1", "owner/repo", "bad", "digest", "evidence", now)],
    )
    rebuilt = QueueState(repo=state.repo, revision=4, items={}, records=[], quarantines=[], state_ref=state.state_ref)

    recovered = rehydrate_state(state, lambda: rebuilt)

    assert recovered.recovery_epoch == 1
    assert recovered.quarantines[0].rehydration_attempted is True
    assert QueueStore(repo=state.repo, backing=InMemoryBackingStore()).is_quarantined(recovered) is False
