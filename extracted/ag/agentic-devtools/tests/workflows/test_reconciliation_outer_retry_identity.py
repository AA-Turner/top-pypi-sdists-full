"""Exercise outer reconciliation retries against persisted queue winners."""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

import agentic_devtools.cli.ci.reconciliation.command as command
import agentic_devtools.cli.ci.reconciliation.config as config
from agentic_devtools.cli.ci.reconciliation.contention import QueueTransitionRetryExhaustedError
from agentic_devtools.cli.ci.reconciliation.dispatch import DispatchResult
from agentic_devtools.cli.ci.reconciliation.dispatch_identity import (
    DispatchRetryExhaustedError,
    derive_dispatch_operation_id,
)
from agentic_devtools.cli.ci.reconciliation.models import DispatchEligibility, QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import InMemoryBackingStore, QueueStore


@pytest.mark.parametrize(
    ("change_watermark", "expected_result"),
    [(False, 0), (True, 1)],
    ids=["matching-operation", "changed-operation"],
)
def test_outer_retry_exhaustion_uses_first_operation_identity(
    change_watermark: bool,
    expected_result: int,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Only the original due operation may be reported deferred after outer retries."""
    now = datetime.now(UTC)
    item = WorkItem(
        pr_number=42,
        repo="owner/repo",
        change_id="head-1",
        eligibility="eligible",
        due_at=now,
        status=WorkItemStatus.QUEUED,
        observation_watermark="watermark-A",
    )
    backing = InMemoryBackingStore()
    real_store = QueueStore(repo="owner/repo", backing=backing)
    real_store.save(
        QueueState(repo="owner/repo", revision=0, items={42: item}, records=[], quarantines=[]),
        expected_revision=0,
    )
    store_factory = QueueStore
    attempts = 0

    def create_store(*, repo: str) -> QueueStore:
        return store_factory(repo=repo, backing=backing)

    def dispatch_with_raw_conflict(state: QueueState, *, store: QueueStore, **_kwargs) -> DispatchResult:
        nonlocal attempts
        attempts += 1
        winner = store_factory(repo="owner/repo", backing=backing)
        persisted = winner.load()
        winner_item = persisted.items[42]
        if attempts == 1 and change_watermark:
            winner_item = replace(winner_item, observation_watermark="watermark-B")
        winner.save(
            replace(persisted, items={42: winner_item}),
            expected_revision=persisted.revision,
        )
        store.save(state, expected_revision=state.revision)
        raise AssertionError("stale QueueStore save should raise a CAS conflict")

    monkeypatch.setattr(config, "MAX_RETRY_ATTEMPTS", 2)
    monkeypatch.setattr(command, "QueueStore", create_store)
    monkeypatch.setattr(command, "_create_provider", lambda *_args, **_kwargs: MagicMock())
    monkeypatch.setattr(
        command,
        "_refresh_inventory",
        lambda _provider, _store, state, _repo, **_kwargs: state,
    )
    monkeypatch.setattr(command, "dispatch_due_work", dispatch_with_raw_conflict)
    monkeypatch.setattr(command, "wait_for_contention", lambda _attempt: None)
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))

    result = command.reconcile_command(
        [
            "--workflow-id",
            "ai-pr-loop.yml",
            "--repo",
            "owner/repo",
            "--trusted-pr-number",
            "42",
            "--trusted-head-sha",
            "head-1",
            "--json-output",
        ]
    )

    assert result == expected_result
    assert attempts == 2
    if change_watermark:
        assert capsys.readouterr().out == ""
    else:
        assert json.loads(capsys.readouterr().out)["action"] == "deferred"
    assert real_store.load().items[42].observation_watermark == ("watermark-B" if change_watermark else "watermark-A")


@pytest.mark.parametrize(
    ("exit_path", "expected_counts"),
    [
        ("dispatch-exhaustion", (2, 2, 2)),
        ("transition-exhaustion", (1, 2, 2)),
        ("ordinary-success", (2, 2, 2)),
        ("disabled-early-return", (1, 1, 1)),
        ("cooldown-early-return", (1, 1, 2)),
        ("inspect-mode-early-return", (1, 1, 1)),
    ],
)
def test_outer_retry_rejects_replacement_for_every_success_exit(
    exit_path: str,
    expected_counts: tuple[int, int, int],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """No retry exit may claim success for replacement work after the original trigger changes."""
    now = datetime.now(UTC)
    original = WorkItem(
        pr_number=42,
        repo="owner/repo",
        change_id="head-1",
        eligibility="eligible",
        due_at=now,
        status=WorkItemStatus.QUEUED,
        observation_watermark="watermark-A",
    )
    backing = InMemoryBackingStore()
    store_factory = QueueStore
    real_store = store_factory(repo="owner/repo", backing=backing)
    real_store.save(
        QueueState(repo="owner/repo", revision=0, items={42: original}, records=[], quarantines=[]),
        expected_revision=0,
    )
    calls = 0
    refreshes = 0
    argv = [
        "--workflow-id",
        "ai-pr-loop.yml",
        "--repo",
        "owner/repo",
        "--trusted-pr-number",
        "42",
        "--trusted-head-sha",
        "head-1",
        "--json-output",
    ]

    def create_store(*, repo: str) -> QueueStore:
        return store_factory(repo=repo, backing=backing)

    def refresh_inventory(_provider, _store, state, _repo, **_kwargs):
        nonlocal refreshes
        refreshes += 1
        if exit_path == "transition-exhaustion" and refreshes == 2:
            raise QueueTransitionRetryExhaustedError(
                "transition retries exhausted",
                operation_id=derive_dispatch_operation_id(replacement),
            )
        return state

    replacement = replace(original, observation_watermark="watermark-B")

    def dispatch_after_raw_conflict(state: QueueState, *, store: QueueStore, **_kwargs) -> DispatchResult:
        nonlocal calls
        calls += 1
        if calls == 1:
            winner = store_factory(repo="owner/repo", backing=backing)
            persisted = winner.load()
            winner.save(
                replace(persisted, items={42: replacement}),
                expected_revision=persisted.revision,
            )
            if exit_path == "disabled-early-return":
                config.ENABLE_RECONCILIATION = False
            if exit_path == "inspect-mode-early-return":
                argv[0:0] = ["--mode", "inspect-inventory"]
            store.save(state, expected_revision=state.revision)
            raise AssertionError("stale QueueStore save should raise a CAS conflict")
        if exit_path == "dispatch-exhaustion":
            raise DispatchRetryExhaustedError(
                "dispatch retries exhausted",
                pr_number=42,
                change_id="head-1",
                operation_id=derive_dispatch_operation_id(replacement),
            )
        return DispatchResult(
            eligibility=DispatchEligibility(0, state.repo, False, "no_due_work", now, False, ""),
            state=state,
        )

    monkeypatch.setattr(config, "MAX_RETRY_ATTEMPTS", 2)
    monkeypatch.setattr(config, "ENABLE_RECONCILIATION", True)
    monkeypatch.setattr(command, "QueueStore", create_store)
    monkeypatch.setattr(command, "_create_provider", lambda *_args, **_kwargs: MagicMock())
    monkeypatch.setattr(command, "_refresh_inventory", refresh_inventory)
    monkeypatch.setattr(command, "dispatch_due_work", dispatch_after_raw_conflict)
    monkeypatch.setattr(command, "wait_for_contention", lambda _attempt: None)
    cooldown_checks = 0

    def active_cooldown(*_args, **_kwargs) -> bool:
        nonlocal cooldown_checks
        cooldown_checks += 1
        return exit_path == "cooldown-early-return" and cooldown_checks == 2

    monkeypatch.setattr(command, "active_cooldown", active_cooldown)
    monkeypatch.setenv("AGDT_STATE_DIR", str(tmp_path))

    result = command.reconcile_command(argv)

    assert result == 1
    assert (calls, refreshes, cooldown_checks) == expected_counts
    assert real_store.load().items[42].observation_watermark == "watermark-B"
    assert capsys.readouterr().out == ""
