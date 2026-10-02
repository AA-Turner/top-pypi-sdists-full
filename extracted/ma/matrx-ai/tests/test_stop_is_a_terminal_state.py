"""Stop is a first-class terminal state, end to end (PB-05 run 2, 2026-10-01).

Blind run (production conversation ac170b56…, Compass Itinerary Clerk): the
person pressed Stop at Stop 10 of a 40-stop answer. The run's chat.user_request
ended ``cancelled``, but the stopped provider call's chat.request row said
``completed`` and the saved answer carried nothing that said it was stopped —
so after a reload the answer simply ended mid-sentence ("= 267") with no sign
on it, and no reader of the row could tell a Stop from a finished answer.

Breaks guarded: the stopped partial is persisted without ``metadata.stopped``;
the stopped call's cost row is written ``completed`` instead of ``cancelled``;
a run that finished normally is marked stopped. Seam: the real
``_stopped_call_response`` and the real ``persist_completed_request``; only the
queue writers, the model lookup and the app context are doubles (the same
harness as test_system_run_cost_only_persistence.py).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import MessageList, TextContent, TokenUsage, UnifiedConfig, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator import executor
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

CONVERSATION_ID = "ac170b56-c9b1-4694-aaad-87f3870e7e2e"
USER_ID = "22222222-2222-2222-2222-222222222222"
REQUEST_ID = "3c96571c-e07e-4c09-8544-c4530362c128"
SHOWN = (
    "Stop 10 — La Grande, Oregon Rest Area & Route Confirmation, I-84 Mile 228: "
    "Cargo straps are visually inspected. **Mileage check: Tacoma to La Grande = 267"
)


def _ctx(streamed: str) -> SimpleNamespace:
    return SimpleNamespace(emitter=SimpleNamespace(get_turn_text=lambda: streamed))


def test_the_stopped_partial_says_it_was_stopped():
    response = executor._stopped_call_response(_ctx(SHOWN), "pb05-run2-plain-stop")
    assert [c.text for c in response.messages[0].content] == [SHOWN]
    assert (response.messages[0].metadata or {}).get("stopped") is True


# ---------------------------------------------------------------------------
# Persistence — the real persist_completed_request with queue doubles
# ---------------------------------------------------------------------------


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


def _completed(status: str, answer: UnifiedMessage) -> CompletedRequest:
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="Draft the 40-stop itinerary.")]),
        answer,
    ]
    cfg = UnifiedConfig(model="test-model", messages=MessageList(_messages=messages))
    req = AIMatrixRequest(conversation_id=CONVERSATION_ID, config=cfg, request_id=REQUEST_ID)
    req.add_usage(
        TokenUsage(input_tokens=900, output_tokens=1200, matrx_model_name="test-model", api="test")
    )
    return CompletedRequest(
        request=req,
        iterations=1,
        final_response=UnifiedResponse(messages=[answer]),
        metadata={"status": status},
        trigger_message_position=0,
        result_start_position=1,
        result_end_position=1,
    )


@pytest.fixture()
def harness(monkeypatch):
    import matrx_ai.context.app_context as app_ctx_mod
    import matrx_ai.db.persistence as persistence_mod

    ctx = _ChatCtx()
    monkeypatch.setattr(app_ctx_mod, "get_app_context", lambda: ctx)
    monkeypatch.setattr(app_ctx_mod, "try_get_app_context", lambda: ctx)
    calls: dict[str, list[Any]] = {"message": [], "request_create": [], "user_request": []}
    monkeypatch.setattr(persistence_mod, "ai_model_manager_instance", _StubModelManager())
    monkeypatch.setattr(persistence_mod, "_get_coordinator", lambda: _StubCoordinator())
    monkeypatch.setattr(
        persistence_mod, "_queue_message_create", lambda **kw: calls["message"].append(kw)
    )
    monkeypatch.setattr(
        persistence_mod,
        "_queue_message_update",
        lambda mid, **kw: calls["message"].append(kw),
    )
    monkeypatch.setattr(persistence_mod, "_queue_conversation_update", lambda cid, **kw: None)
    monkeypatch.setattr(
        persistence_mod, "_queue_request_create", lambda **kw: calls["request_create"].append(kw)
    )
    monkeypatch.setattr(
        persistence_mod,
        "_queue_user_request_update",
        lambda rid, **kw: calls["user_request"].append(kw),
    )

    async def _nothing(*a, **k):
        return 0

    async def _no_backfill(*a, **k):
        return []

    monkeypatch.setattr(persistence_mod, "_hide_superseded_failed_turns", _nothing)
    monkeypatch.setattr(persistence_mod, "_refresh_cache_state", _nothing)
    monkeypatch.setattr(persistence_mod, "_emit_context_state", _nothing)
    monkeypatch.setattr(persistence_mod, "_backfill_tool_message", _no_backfill)
    monkeypatch.setattr(persistence_mod, "cxm", _AsyncAnything())
    monkeypatch.setattr(persistence_mod, "try_get_tracker", lambda: None)
    return persistence_mod, calls


@pytest.mark.asyncio
async def test_a_stopped_run_persists_cancelled_and_the_stopped_marker(harness):
    persistence_mod, calls = harness
    stopped = executor._stopped_call_response(_ctx(SHOWN), "pb05-run2-persist").messages[0]

    await persistence_mod.persist_completed_request(
        _completed("cancelled", stopped), conversation_id=CONVERSATION_ID
    )

    ur = {k: v for kw in calls["user_request"] for k, v in kw.items()}
    assert ur.get("status") == "cancelled"
    assert [row.get("status") for row in calls["request_create"]] == ["cancelled"], (
        "the stopped provider call's chat.request row must end cancelled, not completed"
    )
    saved = [m for m in calls["message"] if (m.get("role") or "") == "assistant"]
    assert saved, "the stopped answer must persist"
    assert all((m.get("metadata") or {}).get("stopped") is True for m in saved)


@pytest.mark.asyncio
async def test_a_finished_run_is_never_marked_stopped(harness):
    persistence_mod, calls = harness
    answer = UnifiedMessage(role="assistant", content=[TextContent(text="Itinerary complete.")])

    await persistence_mod.persist_completed_request(
        _completed("completed", answer), conversation_id=CONVERSATION_ID
    )

    assert [row.get("status", "completed") for row in calls["request_create"]] == ["completed"]
    saved = [m for m in calls["message"] if (m.get("role") or "") == "assistant"]
    assert saved and not any((m.get("metadata") or {}).get("stopped") for m in saved)
