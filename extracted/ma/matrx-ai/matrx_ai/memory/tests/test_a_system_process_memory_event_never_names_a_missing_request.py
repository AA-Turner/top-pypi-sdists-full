"""A memory event written under a request with no ``user_request`` row is written unlinked, never lost.

2026-11-17 write_failure b88a7d92: the nightly conversation reflection (``identity.person_scope``)
runs the Observer under an ambient request id that no ``chat.user_request`` row carries. The OM
event stamped that id as ``user_request_id``; every insert hit
``observational_memory_event_user_request_id_fkey`` and the paid call's cost row was lost after
5 retries. A chat turn's recorded request still links.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db import conversation_gate
from matrx_ai.memory import llm_adapter

RID = "82947370-5243-4f19-b87e-1e5f0ce3b969"


@pytest.fixture()
def queued(monkeypatch) -> list[dict[str, Any]]:
    import matrx_ai.persistence as persistence

    rows: list[dict[str, Any]] = []

    @asynccontextmanager
    async def _coordinator(**_kw: Any):
        yield None

    monkeypatch.setattr(persistence, "standalone_coordinator", _coordinator)
    monkeypatch.setattr(persistence, "queue_om_event_create", lambda **f: rows.append(f) or f["id"])
    return rows


def _recorded(monkeypatch, present: bool) -> None:
    async def _was_recorded(_rid: str) -> bool:
        return present

    monkeypatch.setattr(conversation_gate, "request_has_record", lambda _rid: False)
    monkeypatch.setattr(conversation_gate, "_user_request_was_recorded", _was_recorded)


async def _write(ctx: Any) -> None:
    now = datetime.now(UTC)
    await llm_adapter._write_event(
        ctx=ctx,
        conversation_id="78dcd0af-807b-4ed5-803d-6f6367f5789c",
        memory_record_id=None,
        event_type="observer",
        model="m",
        input_tokens=1,
        output_tokens=1,
        cost=0.01,
        duration_ms=5,
        triggered_at=now,
        completed_at=now,
        success=True,
        error=None,
        trigger_reason="observer",
    )


@pytest.mark.asyncio
async def test_a_request_with_no_row_is_written_unlinked(monkeypatch, queued) -> None:
    _recorded(monkeypatch, present=False)
    await _write(SimpleNamespace(request_id=RID, user_id="u1"))
    assert len(queued) == 1, "the cost row must still be queued"
    assert queued[0]["user_request_id"] is None
    assert queued[0]["metadata"] == {"context_request_id": RID}


@pytest.mark.asyncio
async def test_a_recorded_turn_request_keeps_its_link(monkeypatch, queued) -> None:
    _recorded(monkeypatch, present=True)
    await _write(SimpleNamespace(request_id=RID, user_id="u1"))
    assert queued[0]["user_request_id"] == RID
    assert queued[0]["metadata"] == {}


@pytest.mark.asyncio
async def test_a_durable_runtime_spine_request_is_not_a_user_request(monkeypatch, queued) -> None:
    """2026-11-18 write_failure cc7e170b: a coding-session observer ran under a runtime spine
    request (``runtime.global_request``, marked durable by ``runtime/entry``) that has no
    ``chat.user_request`` row. "Durable" is not "a user_request row"; the FK refuses it."""
    from matrx_ai.db import conversation_gate as gate

    monkeypatch.setattr(gate, "_durable_request_ids", type(gate._durable_request_ids)())
    gate.mark_request_durable(RID)

    async def _absent(_rid: str) -> bool:
        return False

    monkeypatch.setattr(gate, "_user_request_was_recorded", _absent)
    await _write(SimpleNamespace(request_id=RID, user_id="u1"))
    assert queued[0]["user_request_id"] is None, "a spine request id was stamped into the user_request FK"
    assert queued[0]["metadata"] == {"context_request_id": RID}
