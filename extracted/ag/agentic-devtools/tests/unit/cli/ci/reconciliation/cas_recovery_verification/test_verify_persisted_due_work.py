"""Tests for verify_persisted_due_work()."""

from dataclasses import replace
from datetime import UTC, datetime, timedelta, tzinfo
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.reconciliation.cas_recovery_verification import verify_persisted_due_work
from agentic_devtools.cli.ci.reconciliation.dispatch_identity import derive_dispatch_operation_id
from agentic_devtools.cli.ci.reconciliation.models import QueueState, WorkItem, WorkItemStatus


class _InvalidOffset(tzinfo):
    def utcoffset(self, dt: datetime | None) -> timedelta:
        return timedelta(hours=24)

    def dst(self, dt: datetime | None) -> timedelta | None:
        return None

    def tzname(self, dt: datetime | None) -> str:
        return "invalid"


def _make_state(now: datetime) -> QueueState:
    item = WorkItem(
        42,
        "owner/repo",
        "head-1",
        "eligible",
        now,
        WorkItemStatus.QUEUED,
        observation_watermark="watermark-1",
    )
    return QueueState("owner/repo", 3, {42: item}, [], [])


def _verify(state: QueueState, *, expected_operation_id: str | None = None, now: datetime | None = None) -> str | None:
    item = _make_state(now or datetime.now(UTC)).items[42]
    store = MagicMock()
    store.load.return_value = state
    return verify_persisted_due_work(
        store,
        pr_number=42,
        head_sha="head-1",
        expected_operation_id=expected_operation_id or derive_dispatch_operation_id(item),
        now=now,
    )


@pytest.mark.parametrize(
    ("mutate", "valid"),
    [
        (lambda state: state, True),
        (lambda state: replace(state, items={42: replace(state.items[42], due_at=None)}), True),
        (lambda state: replace(state, items={}), False),
        (lambda state: replace(state, items={42: replace(state.items[42], pr_number=43)}), False),
        (lambda state: replace(state, items={42: replace(state.items[42], repo="other/repo")}), False),
        (lambda state: replace(state, items={42: replace(state.items[42], change_id="head-2")}), False),
        (lambda state: replace(state, items={42: replace(state.items[42], status=WorkItemStatus.COMPLETED)}), False),
        (lambda state: replace(state, items={42: replace(state.items[42], eligibility="ineligible")}), False),
        (
            lambda state: replace(
                state, items={42: replace(state.items[42], due_at=datetime.now(UTC) + timedelta(minutes=1))}
            ),
            False,
        ),
        (lambda state: replace(state, items={42: replace(state.items[42], due_at=datetime.now())}), False),
        (
            lambda state: replace(
                state,
                items={42: replace(state.items[42], last_observed_at=datetime.now(UTC) + timedelta(minutes=1))},
            ),
            False,
        ),
        (
            lambda state: replace(
                state,
                items={42: replace(state.items[42], completed_at=datetime.now(UTC) + timedelta(minutes=1))},
            ),
            False,
        ),
        (
            lambda state: replace(
                state,
                items={42: replace(state.items[42], last_observed_at="not-a-timestamp")},
            ),
            False,
        ),
        (
            lambda state: replace(
                state,
                items={42: replace(state.items[42], last_observed_at=datetime(2026, 1, 1, tzinfo=_InvalidOffset()))},
            ),
            False,
        ),
    ],
)
def test_verifies_only_matching_due_work(mutate, valid: bool) -> None:
    state = _make_state(datetime.now(UTC))
    item = state.items[42]
    expected_operation_id = derive_dispatch_operation_id(item)
    mutated = mutate(state)
    if mutated is state and not valid:
        pytest.fail("invalid fixture did not change state")

    result = _verify(mutated, expected_operation_id=expected_operation_id, now=datetime.now(UTC))

    assert (result == expected_operation_id) is valid


@pytest.mark.parametrize(
    ("pr_number", "head_sha", "expected_operation_id"),
    [(None, "head-1", "operation-1"), (42, "", "operation-1"), (42, "head-1", None)],
)
def test_requires_trigger_identity(pr_number, head_sha, expected_operation_id) -> None:
    store = MagicMock()

    result = verify_persisted_due_work(
        store,
        pr_number=pr_number,
        head_sha=head_sha,
        expected_operation_id=expected_operation_id,
    )

    assert result is None
    store.load.assert_not_called()


def test_rejects_nonmatching_operation_id() -> None:
    assert _verify(_make_state(datetime.now(UTC)), expected_operation_id="other-operation") is None


def test_rejects_naive_decision_clock() -> None:
    assert _verify(_make_state(datetime.now(UTC)), now=datetime.now()) is None


def test_rejects_invalid_decision_clock() -> None:
    assert _verify(_make_state(datetime.now(UTC)), now=datetime(2026, 1, 1, tzinfo=_InvalidOffset())) is None


def test_rejects_unavailable_winning_state() -> None:
    store = MagicMock()
    store.load.side_effect = RuntimeError("queue unavailable")

    assert (
        verify_persisted_due_work(
            store,
            pr_number=42,
            head_sha="head-1",
            expected_operation_id="operation-1",
        )
        is None
    )
