"""Tests for ReconciliationRunTracker."""

from __future__ import annotations

from agentic_devtools.cli.ci.reconciliation.runs import ReconciliationRunTracker


def test_start_generates_stable_run_metadata() -> None:
    tracker = ReconciliationRunTracker()
    run = tracker.start(mode="scheduled", source_revision="abc", started_at_utc_z="2026-09-15T12:00:00Z")
    assert run.run_id
    assert run.outcome == "running"


def test_checkpoint_and_complete_behaviors() -> None:
    tracker = ReconciliationRunTracker()
    run = tracker.start(mode="scheduled", source_revision="abc", started_at_utc_z="2026-09-15T12:00:00Z")
    checkpointed = tracker.checkpoint(run, checkpoint="cursor:1")
    completed = tracker.complete(
        checkpointed,
        completed_at_utc_z="2026-09-15T12:10:00Z",
        outcome="success",
        processed_records=10,
        failed_records=1,
        traversal_baseline_advanced=True,
    )
    failed = tracker.complete(
        checkpointed,
        completed_at_utc_z="2026-09-15T12:10:00Z",
        outcome="aborted",
        processed_records=10,
        failed_records=1,
        traversal_baseline_advanced=True,
    )
    assert completed.persisted_checkpoint == "cursor:1"
    assert completed.traversal_baseline_advanced
    assert not failed.traversal_baseline_advanced
