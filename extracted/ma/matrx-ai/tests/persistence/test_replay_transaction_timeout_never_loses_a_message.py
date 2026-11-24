"""A chat.message INSERT lost to a TRANSACTION timeout is replayed, never quarantined on sight.

Live 2026-11-06 (feedback d231594e): write failure c9cae605 — a chat.message INSERT that
died with ``asyncpg.exceptions.TransactionTimeoutError`` (SQLSTATE 25P04) — matched no
self-healing class, so the auto-replay quarantined it six seconds after capture as
"unreplayable". The row then landed 39 seconds later (the coding-session bridge re-sent the
line), yet the ledger still reported the message lost. Any other writer's message would
have stayed lost.

Breaks these tests name: TransactionTimeoutError leaves the recoverable classes; a
transaction-timed-out INSERT is replayed without first reading its key; a quarantine
settles an INSERT whose row is already in its table; or a failure row drops the
conversation its payload names.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import pytest

from matrx_ai.persistence import replay

_TX_TIMEOUT = (
    "asyncpg.exceptions.TransactionTimeoutError: terminating connection due to "
    "transaction timeout [SQLSTATE 25P04]"
)
_CONV = "38b05b27-5e5b-52e3-8e26-d6a696a3f179"


def _row(row_id: str, error_text: str) -> dict[str, Any]:
    return {
        "id": row_id,
        "op_type": "insert",
        "error_text": error_text,
        "request_id": f"req-{row_id}",
        "table_target": "chat.message",
        "retry_count": 0,
        "failed_at": datetime.now(UTC),
        "user_id": None,
        "conversation_id": None,
        "primary_key": {"id": f"msg-{row_id}"},
    }


class _Query:
    def __init__(self, rows: list[dict[str, Any]], kw: dict[str, Any]):
        self._rows, self._kw = rows, kw

    def filter(self, **kw: Any) -> _Query:
        return _Query(self._rows, {**self._kw, **kw})

    def order_by(self, *_a: Any) -> _Query:
        return self

    def limit(self, *_a: Any) -> _Query:
        return self

    async def values(self, *_cols: str) -> list[dict[str, Any]]:
        if "id" in self._kw:
            return [r for r in self._rows if r["id"] == self._kw["id"]]
        return list(self._rows)


class _Swf:
    def __init__(self, rows: list[dict[str, Any]]):
        self._rows = rows

    def filter(self, **kw: Any) -> _Query:
        return _Query(self._rows, kw)


def test_transaction_timeout_is_a_recoverable_class() -> None:
    assert any(sig in _TX_TIMEOUT for sig in replay.RECOVERABLE_RETRY_ERRORS)
    assert replay._is_query_timeout_capture_text(_TX_TIMEOUT)


@pytest.mark.asyncio
async def test_a_transaction_timed_out_insert_is_eligible_and_key_checked(monkeypatch) -> None:
    rows = [_row("missing", _TX_TIMEOUT), _row("landed", _TX_TIMEOUT)]
    monkeypatch.setattr(replay, "_swf_model", lambda: _Swf(rows))
    recovered: list[str] = []

    async def landed(row: Any) -> bool:
        return row["id"] == "landed"

    async def mark(ids: Any, op: str) -> None:
        recovered.extend(ids)

    monkeypatch.setattr(replay, "_insert_already_landed", landed)
    monkeypatch.setattr(replay, "_mark_recovered", mark)
    refused: list[dict[str, Any]] = []

    eligible = await replay._fetch_pending(
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        limit=50,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
        unreplayable=refused,
    )

    assert [r["id"] for r in eligible] == ["missing"]
    assert recovered == ["landed"]
    assert refused == []


@pytest.mark.asyncio
async def test_quarantine_settles_an_insert_that_already_landed(monkeypatch) -> None:
    rows = [_row("landed", "builtins.ValueError: no class"), _row("lost", "builtins.ValueError: no class")]
    recovered: list[str] = []
    quarantined: list[str] = []

    async def landed(row: Any) -> bool:
        return row["id"] == "landed"

    async def mark(ids: Any, op: str) -> None:
        recovered.extend(ids)

    async def capture(exc: Exception, **kw: Any) -> None:
        return None

    async def record(group: Any, *, max_attempts: int | None, permanent: bool = False) -> int:
        quarantined.extend(r["id"] for r in group)
        return len(group)

    monkeypatch.setattr(replay, "_insert_already_landed", landed)
    monkeypatch.setattr(replay, "_mark_recovered", mark)
    monkeypatch.setattr(replay, "_capture_replay_failure", capture)
    monkeypatch.setattr(replay, "_record_failed_attempt", record)

    await replay._quarantine_unreplayable(
        rows, replay.ReplayReport(), max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS
    )

    assert recovered == ["landed"]
    assert quarantined == ["lost"]


def test_a_failure_row_names_the_conversation_its_payload_carries() -> None:
    from matrx_orm.session.fallback import _op_failure_row
    from matrx_orm.session.op import SessionOp

    class _Meta:
        table_name = "message"
        db_schema = "chat"

    class _M:
        _meta = _Meta

    op = SessionOp(
        model_cls=_M,
        op_type="insert",
        pk_field="id",
        pk_value="6d787991-4a4e-5c1a-9b03-f3dfcfe9616e",
        payload={"id": "6d787991-4a4e-5c1a-9b03-f3dfcfe9616e", "conversation_id": _CONV},
    )
    row = _op_failure_row(
        op,
        request_id="r",
        session_id=None,
        safe_user_id=None,
        safe_conversation_id=None,
        organization_id=None,
        error_text=_TX_TIMEOUT,
        tb_text="",
        failed_at=datetime.now(UTC),
    )
    assert row["conversation_id"] == _CONV
