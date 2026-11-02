"""Exercise trusted reconciliation with real queue CAS and provider attribution."""

import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import AgentTaskInventoryLoadResult
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.models import PRMetadata
from agentic_devtools.cli.ci.reconciliation import command, config
from agentic_devtools.cli.ci.reconciliation.models import QuarantineRecord, QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    InMemoryBackingStore,
    QueueStore,
)
from agentic_devtools.cli.ci.reconciliation.recovery import rehydrate_state
from agentic_devtools.cli.ci.scheduler_inventory_scan import SchedulerInventoryScan


@pytest.fixture
def reconciliation(monkeypatch, tmp_path):
    store = QueueStore("o/r", backing=InMemoryBackingStore())
    provider = GitHubActionsProvider(repo="o/r")
    metadata = PRMetadata(42, "title", "branch", "head", "main")

    def list_eligible_prs():
        """Supply the complete same-scan evidence that the real provider captures."""
        scan = SchedulerInventoryScan()
        scan.load(lambda: AgentTaskInventoryLoadResult(()))
        provider._scheduler_inventory_scan = scan
        return [metadata]

    for name, value in {
        "list_reviews": [],
        "list_issue_comments": [],
        "get_pr_metadata": metadata,
        "list_relevant_pull_requests": ([metadata], None),
        "dispatch_workflow": None,
    }.items():
        monkeypatch.setattr(provider, name, MagicMock(return_value=value))
    monkeypatch.setattr(provider, "list_eligible_prs", MagicMock(side_effect=list_eligible_prs))
    monkeypatch.setattr(command, "QueueStore", lambda **kwargs: store)
    monkeypatch.setattr(command, "_create_provider", lambda *args: provider)
    monkeypatch.setattr(command, "active_cooldown", lambda *args, **kwargs: False)
    monkeypatch.setattr("agentic_devtools.cli.ci.reconciliation.contention.time.sleep", lambda _: None)
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))
    return store, provider, metadata


def test_missing_watermark_is_bounded_conservative_and_dispatch_is_deduplicated(reconciliation, monkeypatch, caplog):
    store, provider, _ = reconciliation
    state = store.load()
    item = WorkItem(
        42,
        "o/r",
        "head",
        "eligible",
        datetime.now(UTC),
        WorkItemStatus.QUEUED,
        observation_watermark="missing",
    )
    store.save(replace(state, items={42: item}), expected_revision=state.revision)
    pages = MagicMock(
        return_value=json.dumps([{"sha": f"ordinary-{i}", "author": {"login": "ordinary-user"}} for i in range(100)])
    )
    monkeypatch.setattr("agentic_devtools.cli.ci.push_attribution._gh_api", pages)
    monkeypatch.setattr(config, "MAX_PAGINATION_PAGES_PER_RUN", 2)
    args = ["--workflow-id", "ai-pr-loop.yml", "--repo", "o/r", "--invalidate-inventory"]

    assert command.reconcile_command(args) == 0
    assert pages.call_count == 2
    assert "treating push attribution as unknown" in caplog.text
    assert store.load().items[42].status == WorkItemStatus.COMPLETED
    assert command.reconcile_command(args) == 0
    assert pages.call_count == 4
    provider.dispatch_workflow.assert_called_once()


@pytest.mark.parametrize("change", ["head", "operation"])
def test_new_head_or_operation_remains_dispatchable(reconciliation, monkeypatch, change):
    _, provider, metadata = reconciliation
    monkeypatch.setattr(
        provider,
        "get_pr_copilot_attribution",
        MagicMock(
            return_value={
                "push": True,
                "observation_watermark": "same-observation",
            }
        ),
    )
    args = ["--workflow-id", "ai-pr-loop.yml", "--repo", "o/r", "--invalidate-inventory"]
    assert command.reconcile_command(args) == 0
    first_operation = provider.dispatch_workflow.call_args.args[1]["operation_id"]
    assert command.reconcile_command(args) == 0
    provider.dispatch_workflow.assert_called_once()
    if change == "head":
        metadata = replace(metadata, head_sha="new-head")
        provider.get_pr_metadata.return_value = metadata
        provider.list_relevant_pull_requests.return_value = ([metadata], None)
    else:
        monkeypatch.setenv("AGDT_OPERATION_ID", "distinct-operation")
    assert command.reconcile_command(args) == 0
    assert provider.dispatch_workflow.call_count == 2
    assert provider.dispatch_workflow.call_args.args[1]["operation_id"] != first_operation


def test_post_dispatch_conflict_fences_without_repeating_dispatch(reconciliation, monkeypatch):
    store, provider, _ = reconciliation
    monkeypatch.setattr(
        provider,
        "get_pr_copilot_attribution",
        MagicMock(
            return_value={
                "push": True,
                "observation_watermark": "same-observation",
            }
        ),
    )
    winner = WorkItem(99, "o/r", "unrelated-head", "ineligible", None, WorkItemStatus.COMPLETED)

    def accept_dispatch_and_advance_queue(*args):
        current = store.load()
        store.save(replace(current, items={**current.items, 99: winner}), expected_revision=current.revision)

    provider.dispatch_workflow.side_effect = accept_dispatch_and_advance_queue
    args = ["--workflow-id", "ai-pr-loop.yml", "--repo", "o/r", "--invalidate-inventory"]
    assert command.reconcile_command(args) == 1
    assert store.load().items[42].status == WorkItemStatus.UNKNOWN
    assert store.load().items[99] == winner
    assert command.reconcile_command(args) == 0
    assert store.load().items[42].status == WorkItemStatus.UNKNOWN
    provider.dispatch_workflow.assert_called_once()


def test_multiple_writers_preserved_without_repeating_provider_observation(reconciliation, monkeypatch):
    store, provider, _ = reconciliation
    attribution = MagicMock(return_value={"push": True, "observation_watermark": "same-observation"})
    monkeypatch.setattr(provider, "get_pr_copilot_attribution", attribution)
    save = store.save
    winners = {}
    attempts = 0

    def racing_save(state, expected_revision):
        nonlocal attempts
        attempts += 1
        if attempts <= 2:
            current = store.load()
            pr = 90 + attempts
            winners[pr] = WorkItem(pr, "o/r", f"winner-{pr}", "ineligible", None, WorkItemStatus.COMPLETED)
            save(replace(current, items={**current.items, pr: winners[pr]}), current.revision)
        return save(state, expected_revision)

    monkeypatch.setattr(store, "save", racing_save)
    assert command.reconcile_command(["--workflow-id", "ai-pr-loop.yml", "--repo", "o/r"]) == 0
    for pr, item in winners.items():
        assert store.load().items[pr] == item
    attribution.assert_called_once()
    provider.dispatch_workflow.assert_called_once()


def test_inventory_retry_exhaustion_fails_once_before_dispatch(reconciliation, monkeypatch, caplog):
    store, provider, _ = reconciliation
    attribution = MagicMock(return_value={"push": True, "observation_watermark": "same-observation"})
    monkeypatch.setattr(provider, "get_pr_copilot_attribution", attribution)
    save = MagicMock(side_effect=ConcurrentModificationError("last winning revision conflict"))
    monkeypatch.setattr(store, "save", save)
    monkeypatch.setattr(config, "MAX_RETRY_ATTEMPTS", 3)

    assert command.reconcile_command(["--workflow-id", "ai-pr-loop.yml", "--repo", "o/r"]) == 1
    assert save.call_count == 3
    assert "budget of 3 exhausted: last winning revision conflict" in caplog.text
    attribution.assert_called_once()
    provider.dispatch_workflow.assert_not_called()


@pytest.mark.parametrize("quarantined", [False, True])
def test_conflicting_rehydration_persists_returned_epoch_and_preserves_winner(quarantined, monkeypatch):
    """Reloading after CAS must retain the authoritative epoch/quarantine transition."""
    now = datetime.now(UTC)
    store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
    state = QueueState(
        "owner/repo",
        0,
        {},
        [],
        [QuarantineRecord("q1", "owner/repo", "bad", "digest", "evidence", now)] if quarantined else [],
    )
    store._backing.save_entry(store._key(), state.revision, state)
    winner = WorkItem(99, "owner/repo", "winner-head", "ineligible", None, WorkItemStatus.UNKNOWN)
    save = store.save_rehydration
    calls = 0

    def racing_save(updated, expected_revision):
        nonlocal calls
        calls += 1
        if calls == 1:
            store._backing.save_entry(store._key(), 0, replace(state, revision=1, items={99: winner}))
        return save(updated, expected_revision)

    monkeypatch.setattr(store, "save_rehydration", racing_save)
    monkeypatch.setattr("agentic_devtools.cli.ci.reconciliation.contention.time.sleep", lambda _: None)
    provider = MagicMock()
    provider.list_relevant_pull_requests.return_value = ([], None)

    result = rehydrate_state(
        state, lambda: command._authoritative_rehydrate_loader(provider, store, state, "owner/repo")
    )

    assert store.load() == result
    assert result.recovery_epoch == 1
    assert result.items[99] == winner
    assert all(record.rehydration_attempted for record in result.quarantines)
    assert calls == 2


def test_recovery_retry_preserves_unresolved_dispatch_fence_when_inventory_omits_pr(monkeypatch):
    """A losing recovery save must retain the dispatch fence and unrelated winner item."""
    now = datetime.now(UTC)
    store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
    initial = store.load()
    leased = WorkItem(
        42,
        "owner/repo",
        "dispatched-head",
        "eligible",
        now,
        WorkItemStatus.LEASED,
        lease_expires_at=now + timedelta(minutes=5),
        claim_id="claim",
        lease_id="lease",
        operation_id="operation",
    )
    store._backing.save_entry(store._key(), initial.revision, replace(initial, items={42: leased}))
    state = store.load()
    concurrent_item = WorkItem(99, "owner/repo", "concurrent-head", "ineligible", None, WorkItemStatus.COMPLETED)
    save = store.save_rehydration
    calls = 0

    def racing_save(updated, expected_revision):
        nonlocal calls
        calls += 1
        if calls == 1:
            winner = store.load()
            store._backing.save_entry(
                store._key(),
                winner.revision,
                replace(winner, revision=winner.revision + 1, items={**winner.items, 99: concurrent_item}),
            )
        return save(updated, expected_revision)

    monkeypatch.setattr(store, "save_rehydration", racing_save)
    monkeypatch.setattr("agentic_devtools.cli.ci.reconciliation.contention.time.sleep", lambda _: None)
    provider = MagicMock()
    provider.list_relevant_pull_requests.return_value = ([], None)

    result = rehydrate_state(
        state,
        lambda: command._authoritative_rehydrate_loader(
            provider, store, state, "owner/repo", unresolved_dispatch_pr=42
        ),
    )

    assert calls == 2
    assert provider.list_relevant_pull_requests.call_count == 1
    assert result.items[42].status is WorkItemStatus.UNKNOWN
    assert result.items[42].eligibility == "ineligible"
    assert (result.items[42].claim_id, result.items[42].lease_id, result.items[42].operation_id) == (
        "claim",
        "lease",
        "operation",
    )
    assert result.items[99] == concurrent_item


@pytest.mark.parametrize("changed_authority", ["epoch", "quarantine"])
def test_rehydration_never_overwrites_newer_recovery_authority(changed_authority, monkeypatch):
    now = datetime.now(UTC)
    store = QueueStore(repo="owner/repo", backing=InMemoryBackingStore())
    state = store.load()
    winner = replace(
        state,
        revision=1,
        recovery_epoch=2 if changed_authority == "epoch" else 0,
        quarantines=[QuarantineRecord("new-q", "owner/repo", "bad", "digest", "evidence", now)]
        if changed_authority == "quarantine"
        else [],
    )
    save = store.save_rehydration
    calls = 0

    def racing_save(updated, expected_revision):
        nonlocal calls
        calls += 1
        store._backing.save_entry(store._key(), 0, winner)
        return save(updated, expected_revision)

    monkeypatch.setattr(store, "save_rehydration", racing_save)
    monkeypatch.setattr("agentic_devtools.cli.ci.reconciliation.contention.time.sleep", lambda _: None)
    provider = MagicMock()
    provider.list_relevant_pull_requests.return_value = ([], None)

    with pytest.raises(RuntimeError, match="Recovery authority changed"):
        command._authoritative_rehydrate_loader(provider, store, state, "owner/repo")
    assert calls == 1
    assert store.load() == winner
