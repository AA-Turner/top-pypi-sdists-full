"""Tests for CASExhaustionReporter."""

import json
from argparse import Namespace
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.reconciliation.cas_recovery import CASExhaustionReporter, _PreDispatchCASRetry
from agentic_devtools.cli.ci.reconciliation.contention import QueueTransitionRetryExhaustedError
from agentic_devtools.cli.ci.reconciliation.dispatch_identity import (
    DispatchRetryExhaustedError,
    derive_dispatch_operation_id,
)
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus
from agentic_devtools.cli.ci.reconciliation.queue_store import ConcurrentModificationError


def _make_state(now: datetime) -> QueueState:
    item = WorkItem(
        pr_number=42,
        repo="owner/repo",
        change_id="head-1",
        eligibility="eligible",
        due_at=now,
        status=WorkItemStatus.QUEUED,
        observation_watermark="watermark-1",
    )
    return QueueState("owner/repo", 3, {42: item}, [], [])


def test_reports_deferred_for_matching_persisted_due_work(capsys: pytest.CaptureFixture[str]) -> None:
    now = datetime.now(UTC)
    state = _make_state(now)
    store = MagicMock()
    store.load.return_value = state

    reported = CASExhaustionReporter._report_deferred_if_due_work_is_confirmed(
        store,
        pr_number=42,
        head_sha="head-1",
        expected_operation_id=derive_dispatch_operation_id(state.items[42]),
        json_output=True,
        now=now,
    )

    assert reported is True
    output = json.loads(capsys.readouterr().out)
    assert output["action"] == "deferred"
    assert output["operation_id"] == derive_dispatch_operation_id(state.items[42])
    assert output["pr_number"] == 42
    assert "incomplete" in output["message"]
    assert "no provider dispatch" in output["message"]
    store.load.assert_called_once()


def test_reports_deferred_when_due_at_is_absent(capsys: pytest.CaptureFixture[str]) -> None:
    now = datetime.now(UTC)
    state = _make_state(now)
    item = replace(state.items[42], due_at=None)
    state.items[42] = item
    store = MagicMock()
    store.load.return_value = state

    reported = CASExhaustionReporter._report_deferred_if_due_work_is_confirmed(
        store,
        pr_number=42,
        head_sha="head-1",
        expected_operation_id=derive_dispatch_operation_id(item),
        json_output=False,
        now=now,
    )

    assert reported is True
    assert "incomplete" in capsys.readouterr().out


@pytest.mark.parametrize(
    "mutate",
    [
        lambda state: replace(state, items={}),
        lambda state: replace(state, items={42: replace(state.items[42], change_id="head-2")}),
        lambda state: replace(state, items={42: replace(state.items[42], eligibility="ineligible")}),
        lambda state: replace(state, items={42: replace(state.items[42], status=WorkItemStatus.COMPLETED)}),
        lambda state: replace(
            state,
            items={42: replace(state.items[42], due_at=datetime.now(UTC) + timedelta(minutes=1))},
        ),
        lambda state: replace(state, items={42: replace(state.items[42], observation_watermark="other")}),
    ],
    ids=["missing", "changed-head", "ineligible", "not-queued", "future-due", "changed-operation"],
)
def test_does_not_report_deferred_for_unconfirmed_due_work(
    mutate,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = datetime.now(UTC)
    original = _make_state(now)
    store = MagicMock()
    store.load.return_value = mutate(original)

    reported = CASExhaustionReporter._report_deferred_if_due_work_is_confirmed(
        store,
        pr_number=42,
        head_sha="head-1",
        expected_operation_id=derive_dispatch_operation_id(original.items[42]),
        json_output=True,
        now=now,
    )

    assert reported is False
    assert capsys.readouterr().out == ""


def test_does_not_report_deferred_when_winner_cannot_be_loaded(capsys: pytest.CaptureFixture[str]) -> None:
    store = MagicMock()
    store.load.side_effect = RuntimeError("queue unavailable")

    reported = CASExhaustionReporter._report_deferred_if_due_work_is_confirmed(
        store,
        pr_number=42,
        head_sha="head-1",
        expected_operation_id="expected-operation",
        json_output=True,
    )

    assert reported is False
    assert capsys.readouterr().out == ""


def test_outer_retry_result_reports_deferred_from_reloaded_winner(capsys: pytest.CaptureFixture[str]) -> None:
    """The outer retry exhaustion verifies the persisted winner before returning non-failing."""
    now = datetime.now(UTC)
    state = _make_state(now)
    store = MagicMock()
    store.load.return_value = state
    retry = _PreDispatchCASRetry(
        "retry budget exhausted",
        queue_store=store,
        pr_number=42,
        head_sha="head-1",
        expected_operation_id=derive_dispatch_operation_id(state.items[42]),
        json_output=True,
    )

    assert CASExhaustionReporter.outer_retry_result(retry, 3) == 0
    assert json.loads(capsys.readouterr().out)["action"] == "deferred"
    store.load.assert_called_once()


def test_run_with_outer_retries_retries_and_returns_success() -> None:
    """A transient pre-dispatch conflict retries the operation and returns its result."""
    now = datetime.now(UTC)
    state = _make_state(now)
    store = MagicMock()
    store.load.return_value = state
    operation_id = derive_dispatch_operation_id(state.items[42])
    first_retry = _PreDispatchCASRetry(
        "first conflict",
        queue_store=store,
        pr_number=42,
        head_sha="head-1",
        expected_operation_id=operation_id,
    )
    attempts = 0
    waits: list[int] = []

    def operation(_triggering_retry: _PreDispatchCASRetry | None) -> int:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise first_retry
        return 0

    assert CASExhaustionReporter.run_with_outer_retries(operation, 2, waits.append) == 0
    assert attempts == 2
    assert waits == [1]


def test_run_with_outer_retries_suppresses_replacement_success_output(capsys: pytest.CaptureFixture[str]) -> None:
    now = datetime.now(UTC)
    state = _make_state(now)
    store = MagicMock()
    store.load.return_value = state
    triggering_retry = _PreDispatchCASRetry(
        "first conflict",
        queue_store=store,
        pr_number=42,
        head_sha="head-1",
        expected_operation_id=derive_dispatch_operation_id(state.items[42]),
    )
    attempts = 0

    def operation(_retry: _PreDispatchCASRetry | None) -> int:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise triggering_retry
        store.load.return_value = replace(
            state,
            items={42: replace(state.items[42], observation_watermark="replacement")},
        )
        print("replacement success")
        return 0

    assert CASExhaustionReporter.run_with_outer_retries(operation, 2, lambda _attempt: None) == 1
    assert capsys.readouterr().out == ""


def test_outer_retry_identity_is_not_required_without_trusted_pr_context() -> None:
    retry = _PreDispatchCASRetry("inventory conflict")

    assert CASExhaustionReporter._trigger_operation_is_persisted(retry) is True


@pytest.mark.parametrize(
    ("queue_store", "operation_id"),
    [(None, "operation-A"), (MagicMock(), None)],
)
def test_outer_retry_identity_fails_closed_without_readback_context(queue_store, operation_id) -> None:
    retry = _PreDispatchCASRetry(
        "trusted conflict",
        queue_store=queue_store,
        pr_number=42,
        head_sha="head-1",
        expected_operation_id=operation_id,
    )

    assert CASExhaustionReporter._trigger_operation_is_persisted(retry) is False


def test_outer_retry_identity_fails_closed_when_latest_store_cannot_be_loaded() -> None:
    retry = _PreDispatchCASRetry(
        "trusted conflict",
        queue_store=MagicMock(load=MagicMock(side_effect=RuntimeError("queue unavailable"))),
        pr_number=42,
        head_sha="head-1",
        expected_operation_id="operation-A",
    )

    assert CASExhaustionReporter._trigger_operation_is_persisted(retry) is False


def test_update_retry_store_preserves_trigger_when_context_exists() -> None:
    retry = _PreDispatchCASRetry("trusted conflict")
    store = MagicMock()

    CASExhaustionReporter.update_retry_store(None, store)
    CASExhaustionReporter.update_retry_store(retry, store)

    assert retry.queue_store is store


def test_run_with_outer_retries_preserves_nonzero_result() -> None:
    """A retry that returns an error remains an error without a success log path."""
    attempts = 0

    def operation(_triggering_retry: _PreDispatchCASRetry | None) -> int:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise _PreDispatchCASRetry("first conflict")
        return 1

    assert CASExhaustionReporter.run_with_outer_retries(operation, 2, lambda _attempt: None) == 1


def test_run_with_outer_retries_reports_terminal_exhaustion() -> None:
    """The bounded outer retry loop reports failure after repeated conflicts."""
    first_retry = _PreDispatchCASRetry("first conflict", expected_operation_id="operation-A")
    final_retry = _PreDispatchCASRetry("final conflict", expected_operation_id="operation-B")
    attempts = 0
    waits: list[int] = []

    def operation(_triggering_retry: _PreDispatchCASRetry | None) -> int:
        nonlocal attempts
        attempts += 1
        raise first_retry if attempts == 1 else final_retry

    assert CASExhaustionReporter.run_with_outer_retries(operation, 2, waits.append) == 1
    assert attempts == 2
    assert waits == [1]


def test_retry_handlers_report_only_verified_queue_winners(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = datetime.now(UTC)
    state = _make_state(now)
    store = MagicMock()
    store.load.return_value = state
    args = Namespace(trusted_pr_number=42, trusted_head_sha="head-1", json_output=True)
    operation_id = derive_dispatch_operation_id(state.items[42])
    triggering_retry = _PreDispatchCASRetry(
        "outer conflict",
        queue_store=store,
        pr_number=42,
        head_sha="head-1",
        expected_operation_id=operation_id,
    )
    dispatch_error = DispatchRetryExhaustedError(
        "dispatch exhausted",
        pr_number=42,
        change_id="head-1",
        operation_id=operation_id,
    )

    assert (
        CASExhaustionReporter.dispatch_retry_result(store, args, dispatch_error, triggering_retry=triggering_retry) == 0
    )
    assert json.loads(capsys.readouterr().out)["action"] == "deferred"

    assert CASExhaustionReporter.dispatch_retry_result(store, args, dispatch_error) == 0
    assert json.loads(capsys.readouterr().out)["action"] == "deferred"

    store.load.return_value = replace(state, items={})
    assert CASExhaustionReporter.dispatch_retry_result(store, args, dispatch_error) == 1
    assert capsys.readouterr().out == ""

    store.load.return_value = state
    assert (
        CASExhaustionReporter.transition_retry_result(
            store,
            args,
            QueueTransitionRetryExhaustedError("transition exhausted", operation_id=operation_id),
            triggering_retry=triggering_retry,
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["action"] == "deferred"

    store.load.return_value = replace(state, items={})
    assert (
        CASExhaustionReporter.transition_retry_result(
            store,
            args,
            QueueTransitionRetryExhaustedError("transition exhausted", operation_id=operation_id),
        )
        == 1
    )
    assert capsys.readouterr().out == ""

    assert CASExhaustionReporter.outer_retry_result(_PreDispatchCASRetry("no context"), 3) == 1
    assert capsys.readouterr().out == ""

    monkeypatch.setenv("AGDT_OPERATION_ID", "event-seed")
    retry = CASExhaustionReporter.retry_after_conflict(
        ConcurrentModificationError("stale revision"), store, args, state
    )
    assert retry.queue_store is store
    assert retry.pr_number == 42
    assert retry.head_sha == "head-1"
    assert retry.expected_operation_id == operation_id
    assert retry.json_output is True


@pytest.mark.parametrize(("pr_number", "head_sha"), [(None, "head-1"), (42, "")])
def test_requires_trusted_pr_and_head(pr_number, head_sha, capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        CASExhaustionReporter._report_deferred_if_due_work_is_confirmed(
            MagicMock(),
            pr_number=pr_number,
            head_sha=head_sha,
            expected_operation_id="expected-operation",
            json_output=True,
        )
        is False
    )
    assert capsys.readouterr().out == ""
