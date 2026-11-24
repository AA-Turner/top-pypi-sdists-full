"""The replay lands a row's terminal UPDATE with the row, and never calls a no-op UPDATE recovered.

SUT: :func:`matrx_ai.persistence.replay._fetch_pending` (eligibility) and
:func:`matrx_ai.persistence.replay.replay_pending` in auto mode.

Live evidence 2026-11-03, three refused ``rag.pdf_page_cleaner`` runs
(``chat.user_request`` 49d6dd7a, 1ce06045, 2267a9fa). The row's INSERT was captured
to ``ops.system_write_failure`` under one flush id and its ``status='failed'`` UPDATE
("1 UPDATE(s) matched no row") under another. The INSERT is a recoverable class, so the
sweep landed it, ``pending``. The UPDATE matched no class, so the same sweep quarantined
it unattempted. The request then stood ``pending`` until the watchdog abandoned it, its
refusal (``run_approval_required``) gone from the row and its ``completed_at`` empty.

Breaks these tests name: an UPDATE waiting on its own row's INSERT is quarantined again;
it replays in a different transaction from that INSERT; an INSERT + UPDATE of one row reach
``tier_ops`` uncoalesced (it keeps one op per row and the other vanishes); an UPDATE that
matched no row on replay is marked recovered; a sibling that DID land is held back with it.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_orm.session.flush import _unmatched_updates

from matrx_ai.persistence import replay

from .test_replay_permanent_quarantine import _Harness, _row

_ROW_TO_OP = replay._row_to_op
_TIER_OPS = replay.tier_ops
_COALESCE_OPS = replay.coalesce_ops

_REQUEST_FK = (
    "asyncpg.exceptions.ForeignKeyViolationError: insert or update on table "
    '"user_request" violates foreign key constraint "user_request_parent_request_id_fkey" '
    "[SQLSTATE 23503] constraint=user_request_parent_request_id_fkey table=user_request"
)
_NO_ROW = "builtins.LookupError: 1 UPDATE(s) matched no row: the row did not exist when the update ran"
_DROP = "builtins.RuntimeError: coordinator drop: queue_in_phase_errored"
_REQUEST = "49d6dd7a-75d8-4389-a3cd-fe464b285574"
_OTHER_REQUEST = "1ce06045-ee9a-4325-817d-d1855f574d57"


class _Meta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "user_request"
    db_schema = "chat"


class _UserRequest:
    _meta = _Meta()


def _swf(
    row_id: str,
    *,
    flush_id: str,
    op_type: str,
    error_text: str,
    payload: dict[str, Any],
    pk: str = _REQUEST,
) -> dict[str, Any]:
    return {
        **_row(row_id, error_text),
        "request_id": flush_id,
        "table_target": "chat.user_request",
        "op_type": op_type,
        "primary_key": {"id": pk},
        "payload": payload,
    }


def _insert(pk: str = _REQUEST, *, flush_id: str = "flush-insert", error_text: str = _REQUEST_FK) -> dict[str, Any]:
    return _swf(
        f"insert-{pk}",
        flush_id=flush_id,
        op_type="insert",
        error_text=error_text,
        payload={"id": pk, "status": "pending", "metadata": {"mandate_key": "rag.pdf_page_cleaner"}},
        pk=pk,
    )


def _update(pk: str = _REQUEST, *, flush_id: str = "flush-update", error_text: str = _NO_ROW) -> dict[str, Any]:
    return _swf(
        f"update-{pk}",
        flush_id=flush_id,
        op_type="update",
        error_text=error_text,
        payload={"status": "failed", "error": '{"error_type":"run_approval_required"}'},
        pk=pk,
    )


class _Query:
    def __init__(self, rows: list[dict[str, Any]], kw: dict[str, Any] | None = None) -> None:
        self._rows = rows
        self._kw = dict(kw or {})

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


class _SwfModel:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def filter(self, **kw: Any) -> _Query:
        return _Query(self._rows, kw)


async def _fetch(monkeypatch: pytest.MonkeyPatch, rows: list[dict[str, Any]], *, row_on_disk: bool = False):
    async def on_disk(_row: Any) -> bool:
        return row_on_disk

    monkeypatch.setattr(replay, "_swf_model", lambda: _SwfModel(rows))
    monkeypatch.setattr(replay, "_insert_already_landed", on_disk)
    refused: list[dict[str, Any]] = []
    eligible = await replay._fetch_pending(
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        limit=200,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
        unreplayable=refused,
    )
    return sorted(r["id"] for r in eligible), sorted(r["id"] for r in refused)


@pytest.mark.asyncio
async def test_an_update_waiting_on_its_rows_insert_is_not_quarantined(monkeypatch) -> None:
    eligible, refused = await _fetch(monkeypatch, [_insert(), _update()])

    assert refused == []
    assert eligible == [f"insert-{_REQUEST}", f"update-{_REQUEST}"]


@pytest.mark.asyncio
async def test_an_update_whose_row_landed_since_is_not_quarantined(monkeypatch) -> None:
    eligible, refused = await _fetch(monkeypatch, [_update()], row_on_disk=True)

    assert (eligible, refused) == ([f"update-{_REQUEST}"], [])


@pytest.mark.asyncio
async def test_an_update_of_a_row_nothing_will_write_is_still_quarantined(monkeypatch) -> None:
    eligible, refused = await _fetch(monkeypatch, [_update()], row_on_disk=False)

    assert (eligible, refused) == ([], [f"update-{_REQUEST}"])


@pytest.mark.asyncio
async def test_an_insert_refused_for_good_does_not_keep_its_update_waiting(monkeypatch) -> None:
    refused_insert = _insert(error_text="builtins.ValueError: something no class names")
    eligible, refused = await _fetch(monkeypatch, [refused_insert, _update()], row_on_disk=False)

    assert eligible == []
    assert refused == [f"insert-{_REQUEST}", f"update-{_REQUEST}"]


async def _sweep(rows: list[dict[str, Any]]) -> replay.ReplayReport:
    return await replay.replay_pending(
        dry_run=False,
        retry_errors=replay.RECOVERABLE_RETRY_ERRORS,
        max_attempts=replay.AUTO_REPLAY_MAX_ATTEMPTS,
    )


def _real_ops(monkeypatch: pytest.MonkeyPatch, h: _Harness) -> list[list[Any]]:
    """The harness with the real op build and DAG: the ops execute_tiers would really receive."""
    monkeypatch.setattr(replay, "_model_for_table", lambda _table: _UserRequest)
    monkeypatch.setattr(replay, "_row_to_op", _ROW_TO_OP)
    monkeypatch.setattr(replay, "tier_ops", _TIER_OPS)
    monkeypatch.setattr(replay, "coalesce_ops", _COALESCE_OPS)
    return h.executed


@pytest.mark.asyncio
async def test_the_update_lands_in_one_transaction_with_its_insert(monkeypatch) -> None:
    """Captured under two flush ids, they are one write of one row."""
    h = _Harness(monkeypatch, [_insert(), _update()])
    executed = _real_ops(monkeypatch, h)

    report = await _sweep(h.rows)

    assert len(executed) == 1, f"the row's writes replayed in {len(executed)} transactions"
    ops = [op for tier in executed[0] for op in tier]
    assert [(op.op_type, op.payload["status"]) for op in ops] == [("insert", "failed")]
    assert ops[0].payload["error"] == '{"error_type":"run_approval_required"}'
    assert ops[0].payload["metadata"] == {"mandate_key": "rag.pdf_page_cleaner"}
    assert sorted(i for ids in h.recovered for i in ids) == [f"insert-{_REQUEST}", f"update-{_REQUEST}"]
    assert report.recovered_count == 2


@pytest.mark.asyncio
async def test_one_flushs_insert_and_update_of_a_row_both_survive_the_dag(monkeypatch) -> None:
    h = _Harness(monkeypatch, [_insert(flush_id="one-flush"), _update(flush_id="one-flush", error_text=_DROP)])
    executed = _real_ops(monkeypatch, h)

    await _sweep(h.rows)

    ops = [op for tier in executed[0] for op in tier]
    assert [(op.op_type, op.payload["status"]) for op in ops] == [("insert", "failed")]


@pytest.mark.asyncio
async def test_an_update_that_matched_no_row_on_replay_is_never_recovered(monkeypatch) -> None:
    """The replay's own UPDATE commits "successfully" and changes nothing: not a recovery."""
    orphan = _update(pk=_REQUEST, flush_id="one-flush", error_text=_DROP)
    landed = _insert(pk=_OTHER_REQUEST, flush_id="one-flush")
    h = _Harness(monkeypatch, [orphan, landed])
    _real_ops(monkeypatch, h)

    async def execute(tiers: Any) -> None:
        sink = _unmatched_updates.get()
        assert sink is not None, "the replay does not collect the UPDATEs that matched no row"
        sink.extend(op for tier in tiers for op in tier if op.op_type == "update")

    monkeypatch.setattr(replay, "execute_tiers", execute)

    report = await _sweep(h.rows)

    assert [i for ids in h.recovered for i in ids] == [f"insert-{_OTHER_REQUEST}"]
    assert [a["ids"] for a in h.attempts] == [[f"update-{_REQUEST}"]]
    assert h.attempts[0]["permanent"] is False
    assert report.recovered_count == 1
    assert report.still_failed_count == 1
    assert isinstance(h.captured[0]["exc"], LookupError)
