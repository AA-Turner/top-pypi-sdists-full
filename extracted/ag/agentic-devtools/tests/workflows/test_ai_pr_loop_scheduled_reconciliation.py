"""Static contract for the scheduled durable reconciliation consumer."""

from argparse import Namespace
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.reconciliation import config
from agentic_devtools.cli.ci.reconciliation.cas_recovery import CASExhaustionReporter
from agentic_devtools.cli.ci.reconciliation.command import _reconcile_command_once
from agentic_devtools.cli.ci.reconciliation.contention import QueueTransitionRetryExhaustedError, retry_queue_transition
from agentic_devtools.cli.ci.reconciliation.dispatch import DispatchRetryExhaustedError, derive_dispatch_operation_id
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    InMemoryBackingStore,
    QueueStore,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_PR_LOOP = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop.yml"
AI_PR_LOOP_WATCHDOG = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop-watchdog.yml"


def test_scheduled_reconciliation_consumes_persisted_due_work() -> None:
    """The checked-in 20-minute schedule invokes the queue reconciler."""
    content = AI_PR_LOOP.read_text(encoding="utf-8")
    parsed = yaml.safe_load(content)
    job = parsed["jobs"]["scheduled-reconciliation"]
    command = next(step["run"] for step in job["steps"] if "agdt-ci-reconcile" in step.get("run", ""))

    assert 'cron: "*/20 * * * *"' in content
    assert "agdt-ci-reconcile --workflow-id ai-pr-loop.yml" in command
    assert "--provider github" in command


def test_watchdog_due_probe_is_not_the_queue_work_item_consumer() -> None:
    """The cooldown-probe watchdog remains distinct from scheduled queue reconciliation."""
    watchdog = AI_PR_LOOP_WATCHDOG.read_text(encoding="utf-8")

    assert "due-probe-only" in watchdog
    assert "agdt-ci-reconcile" not in watchdog


def _make_due_store(now: datetime, *, backing: InMemoryBackingStore | None = None) -> QueueStore:
    item = WorkItem(
        42,
        "owner/repo",
        "head-1",
        "eligible",
        now - timedelta(minutes=1),
        WorkItemStatus.QUEUED,
        last_observed_at=now - timedelta(minutes=2),
        observation_watermark="observation-1",
    )
    state = QueueState(
        repo="owner/repo",
        revision=0,
        items={42: item},
        records=[],
        quarantines=[],
        full_scan_complete=True,
        next_inventory_at=now + timedelta(hours=1),
        inventory_invalidated=False,
    )
    store = QueueStore(repo="owner/repo", backing=backing if backing is not None else InMemoryBackingStore())
    store.save(state, expected_revision=0)
    return store


def test_scheduled_command_consumes_due_row_with_live_provider_checks(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The scheduled consumer dispatches a persisted due row after fresh live checks."""
    store = _make_due_store(datetime.now(UTC))
    metadata = PRMetadata(42, "title", "feature", "head-1", "main")
    provider = MagicMock()
    provider.list_eligible_prs.return_value = [metadata]
    provider.get_pr_metadata.return_value = metadata
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))

    with (
        patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore", return_value=store),
        patch("agentic_devtools.cli.ci.reconciliation.command._create_provider", return_value=provider),
        patch("agentic_devtools.cli.ci.reconciliation.command.active_cooldown", return_value=False),
    ):
        result = _reconcile_command_once(
            ["--workflow-id", "ai-pr-loop.yml", "--provider", "github", "--repo", "owner/repo"]
        )

    assert result == 0
    provider.list_eligible_prs.assert_called_once()
    assert provider.get_pr_metadata.call_count == 2
    provider.dispatch_workflow.assert_called_once()
    assert store.load().items[42].status is WorkItemStatus.COMPLETED
    assert capsys.readouterr().out == "Dispatched reconciliation for PR #42.\n"


@pytest.mark.parametrize("conflict_site", ["eligibility", "preflight", "lease"])
def test_dispatch_retry_exhaustion_rejects_changed_operation_after_conflicts(
    conflict_site: str,
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Repeated CAS conflicts cannot defer a newer persisted dispatch operation."""
    now = datetime.now(UTC)
    backing = InMemoryBackingStore()
    store = _make_due_store(now, backing=backing)
    competing_store = QueueStore(repo="owner/repo", backing=backing)
    metadata = PRMetadata(42, "title", "feature", "head-1", "main")
    provider = MagicMock()
    provider.list_eligible_prs.return_value = [] if conflict_site == "eligibility" else [metadata]
    provider.get_pr_metadata.return_value = (
        replace(metadata, head_sha="different-head") if conflict_site == "preflight" else metadata
    )
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))
    monkeypatch.setattr(config, "MAX_RETRY_ATTEMPTS", 3)
    save = store.save
    conflicts = 0

    def racing_save(updated: QueueState, expected_revision: int) -> QueueState:
        nonlocal conflicts
        item = updated.items[42]
        if item.status is not WorkItemStatus.LEASED and item.due_at is not None and item.due_at <= now:
            return save(updated, expected_revision)
        conflicts += 1
        winner = competing_store.load()
        if conflicts == 1:
            winner.items[42] = replace(winner.items[42], observation_watermark="winner-operation")
        competing_store.save(winner, expected_revision=winner.revision)
        return save(updated, expected_revision)

    monkeypatch.setattr(store, "save", racing_save)

    with (
        patch("agentic_devtools.cli.ci.reconciliation.command.QueueStore", return_value=store),
        patch("agentic_devtools.cli.ci.reconciliation.command._create_provider", return_value=provider),
        patch("agentic_devtools.cli.ci.reconciliation.command._refresh_inventory", return_value=store.load()),
        patch("agentic_devtools.cli.ci.reconciliation.command.active_cooldown", return_value=False),
    ):
        result = _reconcile_command_once(
            [
                "--workflow-id",
                "ai-pr-loop.yml",
                "--provider",
                "github",
                "--repo",
                "owner/repo",
                "--trusted-pr-number",
                "42",
                "--trusted-head-sha",
                "head-1",
            ]
        )

    assert result == 1
    assert conflicts == config.MAX_RETRY_ATTEMPTS
    assert store.load().items[42].observation_watermark == "winner-operation"
    provider.dispatch_workflow.assert_not_called()
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(("change_operation", "expected_status"), [(False, 0), (True, 1)])
def test_transition_exhaustion_checks_actual_winning_queue_state(
    change_operation: bool,
    expected_status: int,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = datetime.now(UTC)
    store = _make_due_store(now)
    triggering_state = store.load()
    winner = store.load()
    if change_operation:
        winner.items[42] = replace(winner.items[42], observation_watermark="winner-watermark")
    winner.inventory_invalidated = True
    store.save(winner, expected_revision=winner.revision)
    args = Namespace(trusted_pr_number=42, trusted_head_sha="head-1", json_output=True)
    monkeypatch.setattr(config, "MAX_RETRY_ATTEMPTS", 1)

    with pytest.raises(QueueTransitionRetryExhaustedError) as exhausted:
        retry_queue_transition(
            store,
            triggering_state,
            lambda state: replace(state, inventory_invalidated=True),
            triggering_pr=(42, "head-1"),
        )

    assert CASExhaustionReporter.transition_retry_result(store, args, exhausted.value) == expected_status
    output = capsys.readouterr().out
    assert ("action" in output) is (expected_status == 0)


@pytest.mark.parametrize(("change_operation", "expected_status"), [(False, 0), (True, 1)])
def test_outer_exhaustion_checks_actual_winning_queue_state(
    change_operation: bool,
    expected_status: int,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = datetime.now(UTC)
    store = _make_due_store(now)
    triggering_state = store.load()
    winner = store.load()
    if change_operation:
        winner.items[42] = replace(winner.items[42], observation_watermark="winner-watermark")
    winner.inventory_invalidated = True
    store.save(winner, expected_revision=winner.revision)
    with pytest.raises(ConcurrentModificationError) as conflict:
        store.save(
            replace(triggering_state, inventory_invalidated=False),
            expected_revision=triggering_state.revision,
        )
    args = Namespace(trusted_pr_number=42, trusted_head_sha="head-1", json_output=True)
    retry = CASExhaustionReporter.retry_after_conflict(conflict.value, store, args, triggering_state)

    assert CASExhaustionReporter.outer_retry_result(retry, 3) == expected_status
    output = capsys.readouterr().out
    assert ("action" in output) is (expected_status == 0)


def test_dispatch_exhaustion_rejects_caller_identity_not_persisted_in_winner(
    capsys: pytest.CaptureFixture[str],
) -> None:
    store = _make_due_store(datetime.now(UTC))
    state = store.load()
    args = Namespace(trusted_pr_number=42, trusted_head_sha="head-1", json_output=True)
    error = DispatchRetryExhaustedError(
        "dispatch exhausted",
        pr_number=42,
        change_id="head-1",
        operation_id=derive_dispatch_operation_id(state.items[42], operation_identity="event-seed"),
    )

    assert CASExhaustionReporter.dispatch_retry_result(store, args, error) == 1
    assert capsys.readouterr().out == ""
