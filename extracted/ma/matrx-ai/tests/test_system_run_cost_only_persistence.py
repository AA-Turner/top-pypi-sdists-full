"""Regression — system_run agent calls persist the COST SPINE only.

FOUND_DEFECTS 2026-07-07 (RAG-derive starvation ROOT CAUSE): internal
``run_one_agent`` fan-out calls (one per document section, concurrent) each
spun up the FULL user-chat persistence machinery — ConversationGate backfill,
2× cx_message, reservations, labeling, context-state — creating ~40 throwaway
persisted conversations per document derive and saturating the event loop
until a trivial PK read blew a 10s command_timeout.

The platform primitive pinned here: ``run_agent(system_run=True)`` forks the
child AppContext with ``system_run=True``, and persistence then keeps ONLY the
cost spine:

  KEPT    — cx_request cost rows (section 3) + the cx_user_request rollup
            (section 4) + the gate's minimal cx_conversation FK anchor.
            A paid call NEVER loses its cost record (CLAUDE.md billing rule) —
            this is the whole difference from ``store=False``.
  SKIPPED — cx_message rows (section 2), the conversation config backfill
            UPDATE (section 1), cache-state refresh, the context-state event,
            labeling, message reservations, and mid-loop flushes.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import MessageList, TextContent, TokenUsage, UnifiedConfig, UnifiedMessage
from matrx_ai.config.unified_config import UnifiedResponse
from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest

CONVERSATION_ID = "11111111-1111-1111-1111-111111111111"
USER_ID = "22222222-2222-2222-2222-222222222222"
REQUEST_ID = "33333333-3333-3333-3333-333333333333"


# ---------------------------------------------------------------------------
# Layer 1 — run_agent forks the context with system_run=True + muted stream
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_run_agent_system_run_forks_context_flag():
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context
    from matrx_connect.emitters import SilentEmitter

    from matrx_ai.agents.executor import run_agent

    set_app_context(
        AppContext(
            emitter=ConsoleEmitter(),
            user_id=USER_ID,
            request_id=REQUEST_ID,
            client_tools=["desktop_only"],
            metadata={"active_tool_executors": ["matrx-local"]},
        )
    )

    seen: dict[str, Any] = {}

    async def _capture_execute(user_input: Any = None) -> Any:
        from matrx_connect.context.app_context import get_app_context

        ctx = get_app_context()
        seen["system_run"] = getattr(ctx, "system_run", None)
        seen["emitter"] = ctx.emitter
        seen["client_tools"] = list(ctx.client_tools or [])
        seen["metadata"] = dict(ctx.metadata)
        return SimpleNamespace(
            output="ok",
            assistant_response=None,
            config=SimpleNamespace(model="test-model", metadata={}),
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = SimpleNamespace(
        name="qa-generator",
        config=SimpleNamespace(model="test-model", metadata={}),
        source_id=None,
        source_is_version=False,
        execute=_capture_execute,
    )

    result = await run_agent(
        agent,  # type: ignore[arg-type]
        label="derive-test",
        source_app="test",
        source_feature="derive-test",
        emit_lifecycle=False,
        system_run=True,
    )

    assert result.success
    assert seen["system_run"] is True, "child context must carry system_run=True"
    assert isinstance(seen["emitter"], SilentEmitter), (
        "system_run must mute the child's stream (suppress_stream implied)"
    )
    assert seen["client_tools"] == []
    assert seen["metadata"]["client_delegation_disabled"] is True
    assert seen["metadata"]["active_tool_executors"] == []


@pytest.mark.asyncio
async def test_run_agent_default_is_not_system_run():
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id=USER_ID, request_id=REQUEST_ID))
    seen: dict[str, Any] = {}

    async def _capture_execute(user_input: Any = None) -> Any:
        from matrx_connect.context.app_context import get_app_context

        seen["system_run"] = getattr(get_app_context(), "system_run", None)
        return SimpleNamespace(
            output="ok",
            assistant_response=None,
            config=SimpleNamespace(model="test-model", metadata={}),
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = SimpleNamespace(
        name="normal-agent",
        config=SimpleNamespace(model="test-model", metadata={}),
        source_id=None,
        source_is_version=False,
        execute=_capture_execute,
    )
    await run_agent(
        agent,  # type: ignore[arg-type]
        label="normal",
        source_app="test",
        source_feature="normal",
        emit_lifecycle=False,
    )
    assert seen["system_run"] is False


@pytest.mark.asyncio
async def test_system_run_can_stream_without_enabling_chat_persistence():
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    emitter = ConsoleEmitter()
    set_app_context(
        AppContext(
            emitter=emitter,
            user_id=USER_ID,
            request_id=REQUEST_ID,
            client_tools=["desktop_only"],
        )
    )
    seen: dict[str, Any] = {}

    async def _capture_execute(user_input: Any = None) -> Any:
        from matrx_connect.context.app_context import get_app_context

        ctx = get_app_context()
        seen["system_run"] = ctx.system_run
        seen["emitter"] = ctx.emitter
        seen["client_tools"] = list(ctx.client_tools or [])
        return SimpleNamespace(
            output="ok",
            assistant_response=None,
            config=SimpleNamespace(model="test-model", metadata={}),
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = SimpleNamespace(
        name="streamed-system-agent",
        config=SimpleNamespace(model="test-model", metadata={}),
        source_id=None,
        source_is_version=False,
        execute=_capture_execute,
    )
    result = await run_agent(
        agent,  # type: ignore[arg-type]
        label="streamed-system-test",
        source_app="test",
        source_feature="streamed-system-test",
        emit_lifecycle=False,
        system_run=True,
        stream_system_run=True,
    )

    assert result.success
    assert seen["system_run"] is True
    assert seen["emitter"] is emitter
    assert seen["client_tools"] == []


# ---------------------------------------------------------------------------
# Layer 2 — persistence: messages/backfill skipped, cost rows kept
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


class _SystemRunCtx:
    """The forked child context of a run_agent(system_run=True) call."""

    user_id = USER_ID
    conversation_id = CONVERSATION_ID
    store = True
    system_run = True
    execution_kind = "workflow_run"
    execution_id = REQUEST_ID
    parent_conversation_id = "55555555-5555-5555-5555-555555555555"
    emitter = None
    metadata: dict[str, Any] = {}


def _build_completed() -> CompletedRequest:
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="summarize this section")]),
        UnifiedMessage(role="assistant", content=[TextContent(text='{"summary": "..."}')]),
    ]
    cfg = UnifiedConfig(model="test-model", messages=MessageList(_messages=messages))
    req = AIMatrixRequest(
        conversation_id=CONVERSATION_ID,
        config=cfg,
        request_id=REQUEST_ID,
    )
    req.add_usage(
        TokenUsage(
            input_tokens=100,
            output_tokens=50,
            matrx_model_name="test-model",
            api="test",
        )
    )
    return CompletedRequest(
        request=req,
        iterations=1,
        final_response=UnifiedResponse(messages=[messages[-1]]),
        trigger_message_position=0,
        result_start_position=1,
        result_end_position=1,
    )


@pytest.fixture()
def system_run_harness(monkeypatch):
    import matrx_ai.context.app_context as app_ctx_mod
    import matrx_ai.db.persistence as persistence_mod

    stub_ctx = _SystemRunCtx()
    monkeypatch.setattr(app_ctx_mod, "get_app_context", lambda: stub_ctx)
    monkeypatch.setattr(app_ctx_mod, "try_get_app_context", lambda: stub_ctx)

    calls: dict[str, list[Any]] = {
        "message_create": [],
        "message_update": [],
        "conversation_update": [],
        "request_create": [],
        "user_request_update": [],
        "cache_state": [],
        "context_state": [],
    }

    monkeypatch.setattr(persistence_mod, "ai_model_manager_instance", _StubModelManager())
    monkeypatch.setattr(persistence_mod, "_get_coordinator", lambda: _StubCoordinator())
    monkeypatch.setattr(
        persistence_mod, "_queue_message_create", lambda **kw: calls["message_create"].append(kw)
    )
    monkeypatch.setattr(
        persistence_mod,
        "_queue_message_update",
        lambda mid, **kw: calls["message_update"].append((mid, kw)),
    )
    monkeypatch.setattr(
        persistence_mod,
        "_queue_conversation_update",
        lambda cid, **kw: calls["conversation_update"].append((cid, kw)),
    )
    monkeypatch.setattr(
        persistence_mod, "_queue_request_create", lambda **kw: calls["request_create"].append(kw)
    )
    monkeypatch.setattr(
        persistence_mod,
        "_queue_user_request_update",
        lambda rid, **kw: calls["user_request_update"].append((rid, kw)),
    )

    async def _no_hide(*a, **k):
        return 0

    async def _cache(*a, **k):
        calls["cache_state"].append(k)

    async def _ctx_state(*a, **k):
        calls["context_state"].append(k)

    monkeypatch.setattr(persistence_mod, "_hide_superseded_failed_turns", _no_hide)
    monkeypatch.setattr(persistence_mod, "_refresh_cache_state", _cache)
    monkeypatch.setattr(persistence_mod, "_emit_context_state", _ctx_state)
    monkeypatch.setattr(persistence_mod, "cxm", _AsyncAnything())
    monkeypatch.setattr(persistence_mod, "try_get_tracker", lambda: None)

    return persistence_mod, calls


@pytest.mark.asyncio
async def test_system_run_persists_cost_spine_only(system_run_harness):
    persistence_mod, calls = system_run_harness

    result = await persistence_mod.persist_completed_request(
        _build_completed(), conversation_id=CONVERSATION_ID
    )

    # SKIPPED — the throwaway transcript machinery.
    assert calls["message_create"] == [], "system_run must not write cx_message rows"
    assert calls["message_update"] == [], "system_run must not update cx_message rows"
    assert calls["conversation_update"] == [], (
        "system_run must skip the conversation config backfill UPDATE"
    )
    assert calls["cache_state"] == []
    assert calls["context_state"] == []
    assert result["message_ids"] == []

    # KEPT — the cost spine. A paid call NEVER loses its cost record.
    assert len(calls["request_create"]) == 1, "cx_request cost row must still land"
    req_row = calls["request_create"][0]
    assert req_row["input_tokens"] == 100
    assert req_row["output_tokens"] == 50
    assert req_row["conversation_id"] == CONVERSATION_ID
    assert req_row["execution_kind"] == "workflow_run"
    assert req_row["execution_id"] == REQUEST_ID
    assert calls["user_request_update"], "cx_user_request rollup must still land"
    ur_updates = {k: v for _, kw in calls["user_request_update"] for k, v in kw.items()}
    assert ur_updates.get("total_input_tokens") == 100
    assert result["conversation_id"] == CONVERSATION_ID
    assert result["request_ids"], "cost row id must be reported"


@pytest.mark.asyncio
async def test_normal_run_still_persists_messages(system_run_harness, monkeypatch):
    """Control: the SAME harness with system_run=False keeps writing messages —
    the skip is scoped to system runs, not a global regression."""
    persistence_mod, calls = system_run_harness

    import matrx_ai.context.app_context as app_ctx_mod

    class _NormalCtx(_SystemRunCtx):
        system_run = False

    normal_ctx = _NormalCtx()
    monkeypatch.setattr(app_ctx_mod, "get_app_context", lambda: normal_ctx)
    monkeypatch.setattr(app_ctx_mod, "try_get_app_context", lambda: normal_ctx)

    async def _no_backfill(*a, **k):
        return []

    monkeypatch.setattr(persistence_mod, "_backfill_tool_message", _no_backfill)

    await persistence_mod.persist_completed_request(
        _build_completed(), conversation_id=CONVERSATION_ID
    )

    assert calls["message_create"] or calls["message_update"], (
        "normal runs must still persist cx_message rows"
    )
    assert calls["conversation_update"], "normal runs must still backfill the conversation"
    assert calls["request_create"], "cost rows always land"
