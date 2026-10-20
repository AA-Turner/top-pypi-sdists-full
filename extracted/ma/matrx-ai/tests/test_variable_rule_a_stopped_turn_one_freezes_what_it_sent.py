"""THE VARIABLE RULE on a STOPPED saved turn 1 (2026-10-16).

A saved run (store=True) is stopped by the person partway through turn 1's reply, then the
person sends turn 2. A stopped turn still SENT its filled prompt, so:

1. Every stop path ends in ``_finalize_and_persist`` -> ``persist_completed_request``, whose
   structural write freezes turn 1's FILLED system prompt onto ``chat.conversation`` (column
   ``system_instruction`` + ``config.system_prompt_frozen``) exactly as a completed turn does.
2. Turn 2 reads that row back as frozen: the filled prompt, never a refill, plus the stored
   history INCLUDING the stopped partial reply.

Seam: the real ``_stopped_call_response`` and the real ``persist_completed_request`` (queue
writers doubled, the same harness as test_stop_is_a_terminal_state.py), then the real
``CxManagers.get_conversation_unified_config`` over the row that write produced.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import MessageList, TextContent, TokenUsage, UnifiedConfig, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator import executor
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

CONVERSATION_ID = "7d0f3a52-2b8e-4f43-9a51-0c6b1f4e2a90"
USER_ID = "22222222-2222-2222-2222-222222222222"
REQUEST_ID = "5b1e2c3d-4f50-4a61-8b72-9c83d4e5f601"
FILLED = "You are a guide for Oaxaca. Answer in Spanish."
SHOWN = "Primero, visita el mercado de Benito Ju"


class _StubModelManager:
    async def load_model_get_string_uuid(self, name):
        return "44444444-4444-4444-4444-444444444444"


class _StubCoordinator:
    def queue(self, *a, **k):
        return ""


class _AsyncAnything:
    def __getattr__(self, name):
        return _AsyncAnything()

    async def __call__(self, *a, **k):
        return []


class _ChatCtx:
    user_id = USER_ID
    conversation_id = CONVERSATION_ID
    store = True
    system_run = False
    execution_kind = "conversation"
    execution_id = REQUEST_ID
    parent_conversation_id = None
    emitter = None
    metadata: dict[str, Any] = {}


@pytest.fixture()
def harness(monkeypatch):
    import matrx_ai.context.app_context as app_ctx_mod
    import matrx_ai.db.persistence as persistence_mod

    ctx = _ChatCtx()
    monkeypatch.setattr(app_ctx_mod, "get_app_context", lambda: ctx)
    monkeypatch.setattr(app_ctx_mod, "try_get_app_context", lambda: ctx)
    writes: dict[str, list[Any]] = {"conversation": [], "message": []}
    monkeypatch.setattr(persistence_mod, "ai_model_manager_instance", _StubModelManager())
    monkeypatch.setattr(persistence_mod, "_get_coordinator", lambda: _StubCoordinator())
    monkeypatch.setattr(
        persistence_mod, "_queue_message_create", lambda **kw: writes["message"].append(kw)
    )
    monkeypatch.setattr(
        persistence_mod, "_queue_message_update", lambda mid, **kw: writes["message"].append(kw)
    )
    monkeypatch.setattr(
        persistence_mod,
        "_queue_conversation_update",
        lambda cid, **kw: writes["conversation"].append(kw),
    )
    monkeypatch.setattr(persistence_mod, "_queue_request_create", lambda **kw: None)
    monkeypatch.setattr(persistence_mod, "_queue_user_request_update", lambda rid, **kw: None)

    async def _nothing(*a, **k):
        return 0

    async def _no_backfill(*a, **k):
        return []

    monkeypatch.setattr(persistence_mod, "_hide_superseded_failed_turns", _nothing)
    monkeypatch.setattr(persistence_mod, "_refresh_cache_state", _nothing)
    monkeypatch.setattr(persistence_mod, "_emit_context_state", _nothing)
    monkeypatch.setattr(persistence_mod, "_backfill_tool_message", _no_backfill)
    # The row the gate created at turn 1's start: no prompt yet.
    monkeypatch.setattr(persistence_mod, "cxm", _AsyncAnything())
    monkeypatch.setattr(persistence_mod, "try_get_tracker", lambda: None)
    return persistence_mod, writes


def _stopped_turn_one() -> CompletedRequest:
    exec_ctx = SimpleNamespace(emitter=SimpleNamespace(get_turn_text=lambda: SHOWN))
    partial = executor._stopped_call_response(exec_ctx, "stopped-turn-one").messages[0]
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="Plan my first morning.")]),
        partial,
    ]
    cfg = UnifiedConfig(
        model="test-model", system_instruction=FILLED, messages=MessageList(_messages=messages)
    )
    req = AIMatrixRequest(conversation_id=CONVERSATION_ID, config=cfg, request_id=REQUEST_ID)
    req.add_usage(
        TokenUsage(input_tokens=300, output_tokens=12, matrx_model_name="test-model", api="test")
    )
    return CompletedRequest(
        request=req,
        iterations=1,
        final_response=UnifiedResponse(messages=[partial]),
        metadata={"status": "cancelled", "error": "Request canceled while the model was generating."},
        trigger_message_position=0,
        result_start_position=1,
        result_end_position=1,
    )


@pytest.mark.asyncio
async def test_a_stopped_turn_one_freezes_its_filled_prompt_on_the_row(harness):
    persistence_mod, writes = harness
    completed = _stopped_turn_one()

    await persistence_mod.persist_completed_request(completed, conversation_id=CONVERSATION_ID)

    row = {k: v for kw in writes["conversation"] for k, v in kw.items()}
    # The stored text is the rendered instruction turn 1 sent (date line included).
    assert FILLED in (row.get("system_instruction") or ""), row.keys()
    assert (row.get("config") or {}).get("system_prompt_frozen") is True
    assert completed.request.config.system_prompt_frozen is True
    stopped = [m for m in writes["message"] if (m.get("role") or "") == "assistant"]
    assert stopped and (stopped[0].get("metadata") or {}).get("stopped") is True


@pytest.mark.asyncio
async def test_turn_two_reads_the_frozen_prompt_and_the_stopped_reply(harness, monkeypatch):
    persistence_mod, writes = harness
    await persistence_mod.persist_completed_request(
        _stopped_turn_one(), conversation_id=CONVERSATION_ID
    )
    row = {k: v for kw in writes["conversation"] for k, v in kw.items()}

    import matrx_ai.db.conversation_rebuild as rebuild
    from matrx_ai.db._cx_managers_impl import CxManagers

    history = [
        UnifiedMessage(role="user", content=[TextContent(text="Plan my first morning.")]),
        UnifiedMessage(role="assistant", content=[TextContent(text=SHOWN)]),
    ]

    async def _rebuilt(*_a, **_k):
        return list(history)

    monkeypatch.setattr(rebuild, "rebuild_conversation_messages", _rebuilt)

    class _Store:
        async def get_conversation_data(self, _cid):
            return {
                "conversation": SimpleNamespace(
                    config=row["config"],
                    last_model_id=None,
                    system_instruction=row["system_instruction"],
                ),
                "messages": [],
                "tool_calls": [],
                "media": [],
            }

    loaded = await CxManagers.get_conversation_unified_config(_Store(), CONVERSATION_ID)

    assert loaded.system_prompt_frozen is True
    assert FILLED in str(loaded.system_instruction)
    assert str(loaded.system_instruction).count(FILLED) == 1
    texts = [m.content[0].text for m in loaded.messages]
    assert texts == ["Plan my first morning.", SHOWN]
