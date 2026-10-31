"""THE MID-LOOP CHECKPOINT'S ROWS CARRY THE TIME THEY STORE, AND THE WIRE SAYS IT.

Live walk 4 (2026-10-29, conversation 70f79d6e): "Worked for 11s" live, "Worked for 7.9s" after a
reload of the same turn. The turn's "Worked for" is the row-to-row wall clock of its assistant rows
(AssistantTurnGroup). Every row ``persist_completed_request`` writes is stamped in Python and the
same instant rides ``record_update.created_at``; the rows ``_flush_assistant_message_mid_loop``
writes were stamped by the database's own ``now()`` and announced nothing — the stored stream shows
no ``record_update`` for them at all — so the live client kept its receipt clock (28.07) for a row
the database stored at 31.25.

Forcing function: the assertions read what the REAL checkpoint queued and emitted. Drop the
``created_at`` from either queue call or either wire event and these fail.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator.requests import AIMatrixRequest

CONVERSATION_ID = "70f79d6e-419b-4e9f-b0ec-49aff31a17c5"
USER_ID = "87a6e699-3622-4869-8843-d0867456c0dd"
REQUEST_ID = "2334aaa5-359e-49d2-9998-a0339092b4d4"


class _RecordingTracker:
    def __init__(self) -> None:
        self.reserved: list[dict[str, Any]] = []
        self.active: list[dict[str, Any]] = []

    async def reserve(self, *, emitter: Any, record_id: str, created_at: str | None = None, **_: Any) -> str:
        self.reserved.append({"record_id": record_id, "created_at": created_at})
        return record_id

    async def mark_active(self, emitter: Any, table: str, record_id: str, created_at: str | None = None, **_: Any) -> None:
        self.active.append({"table": table, "record_id": record_id, "created_at": created_at})


class _ExecCtx:
    conversation_id = CONVERSATION_ID
    user_id = USER_ID
    store = True
    system_run = False
    emitter = object()


def _request() -> AIMatrixRequest:
    return AIMatrixRequest(
        conversation_id=CONVERSATION_ID,
        config=UnifiedConfig(
            model="claude-test",
            messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="go")])]),
        ),
        request_id=REQUEST_ID,
    )


def _response() -> UnifiedResponse:
    return UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=[TextContent(text="Madrid's weather is in hand.")])]
    )


@pytest.fixture
def recorded(monkeypatch):
    import matrx_ai.persistence.queue_helpers as qh

    writes: list[tuple[str, dict[str, Any]]] = []
    monkeypatch.setattr(qh, "queue_message_update", lambda mid, **kw: writes.append((mid, kw)) or "")
    monkeypatch.setattr(qh, "queue_message_create", lambda **kw: writes.append((kw["id"], kw)) or "")
    tracker = _RecordingTracker()
    monkeypatch.setattr(executor_mod, "get_tracker", lambda: tracker)
    return writes, tracker


@pytest.mark.asyncio
async def test_a_reserved_row_stores_its_time_and_announces_it(recorded):
    writes, tracker = recorded
    request = _request()
    reserved_id = str(uuid4())
    position = len(request.config.messages.to_list())

    await executor_mod._flush_assistant_message_mid_loop(
        response=_response(),
        current_request=request,
        exec_ctx=_ExecCtx(),
        reserved_messages={position: reserved_id},
        parent_refs={},
    )

    assert len(writes) == 1
    stored = writes[0][1].get("created_at")
    assert stored, "the checkpoint wrote the row with the database's now(), which the wire never names"
    assert tracker.active == [{"table": "message", "record_id": reserved_id, "created_at": stored}]


@pytest.mark.asyncio
async def test_a_fresh_row_stores_its_time_and_announces_it(recorded):
    writes, tracker = recorded

    message_id = await executor_mod._flush_assistant_message_mid_loop(
        response=_response(),
        current_request=_request(),
        exec_ctx=_ExecCtx(),
        reserved_messages={},
        parent_refs={},
    )

    assert len(writes) == 1
    stored = writes[0][1].get("created_at")
    assert stored
    assert tracker.reserved == [{"record_id": message_id, "created_at": stored}]
    assert tracker.active == [{"table": "message", "record_id": message_id, "created_at": stored}]
