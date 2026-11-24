"""Two replay groups that can never succeed are quarantined on sight, once.

SUT: :func:`matrx_ai.persistence.replay.replay_pending` in auto mode and its classifiers.

Live evidence (ops.system_error, route matrx_ai.persistence.replay.replay_pending):
* 45 ``persistence_replay_failed`` rows [SQLSTATE 23503] came from NINE
  ``chat.user_request`` inserts whose ``organization_id`` named an organization that
  never existed — ``user_request_organization_id_fkey``. An FK refusal was read as a
  parent-row race, so each row was attempted five times, one system_error per attempt.
* 20 ``persistence_replay_failed`` rows (ValueError) came from EIGHT rows of
  confidential conversations whose payload ``ops.seal_confidential_write_failure``
  had redacted to ``{id, conversation_id, role, position, redacted}`` — nothing to
  rebuild the write from — again attempted five times each.

Breaks these tests name: the organization FK is treated as a race again; a sibling
parent FK (a conversation, a parent user_request) stops being a race; a redacted
payload is attempted (``execute_tiers`` reached) or files more than one capture.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.persistence import replay

from .test_replay_permanent_quarantine import _Harness, _row

_ORG_FK = (
    "asyncpg.exceptions.ForeignKeyViolationError: insert or update on table "
    '"user_request" violates foreign key constraint "user_request_organization_id_fkey" '
    "[SQLSTATE 23503] constraint=user_request_organization_id_fkey table=user_request"
)
_ORG_FK_DETAIL_ONLY = (
    "ForeignKeyViolationError: violates foreign key constraint [SQLSTATE 23503] "
    'detail=Key (organization_id)=(x) is not present in table "organizations".'
)
_PARENT_REQUEST_FK = (
    "asyncpg.exceptions.ForeignKeyViolationError: insert or update on table "
    '"user_request" violates foreign key constraint "user_request_parent_request_id_fkey" '
    "[SQLSTATE 23503] constraint=user_request_parent_request_id_fkey table=user_request"
)


def test_a_missing_organization_is_permanent_and_a_missing_parent_request_is_a_race() -> None:
    assert replay.is_permanent_failure_text(_ORG_FK)
    assert replay.is_permanent_failure_text(_ORG_FK_DETAIL_ONLY)
    assert not replay.is_permanent_failure_text(_PARENT_REQUEST_FK)
    # The organization signatures never fire on a non-FK error.
    assert not replay.is_organization_fk_violation_text("user_request_organization_id_fkey mentioned")


def _redacted_row(row_id: str, table: str, op_type: str) -> dict[str, Any]:
    row = _row(row_id, "builtins.RuntimeError: coordinator drop: queue_in_phase_errored")
    row["table_target"] = table
    row["op_type"] = op_type
    row["payload"] = {
        "id": None,
        "conversation_id": "conv-1",
        "role": None,
        "position": None,
        "redacted": replay.SEALED_REDACTION_MARKER,
    }
    return row


def test_a_redacted_confidential_payload_is_recognised() -> None:
    assert replay.is_sealed_redacted_row(_redacted_row("a", "chat.user_request", "update"))
    assert not replay.is_sealed_redacted_row(_row("b", "coordinator drop: x"))


@pytest.mark.asyncio
async def test_a_redacted_group_is_quarantined_once_without_an_attempt(monkeypatch) -> None:
    rows = [
        _redacted_row("a", "chat.message", "insert"),
        _redacted_row("b", "chat.user_request", "update"),
    ]
    h = _Harness(monkeypatch, rows)

    report = await replay.replay_pending(
        dry_run=False,
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert h.executed == [], "a redacted payload must never be re-sent"
    assert h.attempts == [
        {"ids": ["a", "b"], "max_attempts": replay.AUTO_REPLAY_MAX_ATTEMPTS, "permanent": True}
    ]
    assert [c["kind"] for c in h.captured] == ["persistence_replay_quarantined"]
    assert report.by_request == {"request-1": "quarantined (confidential payload redacted)"}
    assert report.quarantined_count == 2


@pytest.mark.asyncio
async def test_an_org_fk_group_is_quarantined_once_without_an_attempt(monkeypatch) -> None:
    h = _Harness(monkeypatch, [_row("a", _ORG_FK)])

    await replay.replay_pending(
        dry_run=False,
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )

    assert h.executed == []
    assert [c["kind"] for c in h.captured] == ["persistence_replay_quarantined"]
