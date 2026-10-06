"""Law — a stored system run keeps its FULL history, exactly like a chat.

Owner ruling (Arman, 2026-10-05): "It is NEVER acceptable for an agent run to
have no history." ``run_agent(system_run=True)`` used to persist only the cost
spine (no messages, no conversation backfill); an opt-in kept the transcript
for mandate runs only. Both are gone: every stored run writes

  sections 1 + 2 — the conversation config backfill and the chat.message rows,
  sections 3 + 4 — the chat.request cost rows and the user-request completion,

and no parameter, metadata key or knob can turn history off.

A system run skips ONLY non-history ceremony: the title LLM call, the
cache_state refresh and the context-state event. Those (plus per-run DB work
outside the coordinator) were the 2026-07-07 RAG-derive starvation (~40
concurrent derive calls); the history writes are queued ops that ride the ONE
coordinator flush. ``test_forty_concurrent_system_runs_stay_cheap`` pins that.
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

    async def _capture_execute(user_input: Any = None, *, max_iterations: Any = None) -> Any:
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

    async def _capture_execute(user_input: Any = None, *, max_iterations: Any = None) -> Any:
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

    async def _capture_execute(user_input: Any = None, *, max_iterations: Any = None) -> Any:
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


def _assert_full_history(calls: dict[str, list[Any]], result: dict[str, Any]) -> None:
    # HISTORY — section 1 (conversation backfill) + section 2 (messages).
    assert calls["conversation_update"], "a stored system run must backfill its conversation"
    conv_id, conv_fields = calls["conversation_update"][0]
    assert conv_id == CONVERSATION_ID
    assert "config" in conv_fields, "the backfill carries the run's config"
    roles = [kw.get("role") for kw in calls["message_create"]] + [
        kw.get("role") for _, kw in calls["message_update"]
    ]
    assert "user" in roles, "the request (user message) must be written"
    assert "assistant" in roles, "the answer (assistant message) must be written"
    assert len(result["message_ids"]) == 2
    # COST — section 3 + 4. A paid call never loses its cost record.
    assert len(calls["request_create"]) == 1, "chat.request cost row must land"
    req_row = calls["request_create"][0]
    assert req_row["input_tokens"] == 100
    assert req_row["output_tokens"] == 50
    assert req_row["conversation_id"] == CONVERSATION_ID
    assert calls["user_request_update"], "the user-request completion must land"


@pytest.mark.asyncio
async def test_system_run_persists_full_history(system_run_harness):
    persistence_mod, calls = system_run_harness

    result = await persistence_mod.persist_completed_request(
        _build_completed(), conversation_id=CONVERSATION_ID
    )

    _assert_full_history(calls, result)
    req_row = calls["request_create"][0]
    assert req_row["execution_kind"] == "workflow_run"
    assert req_row["execution_id"] == REQUEST_ID
    ur_updates = {k: v for _, kw in calls["user_request_update"] for k, v in kw.items()}
    assert ur_updates.get("status") == "completed"
    # The parent's totals are DERIVED by the chat.request _propagate_totals
    # trigger from the cost row above; assigning them here is last-write-wins
    # and erases every sibling call's money
    # (scripts/check_user_request_totals_derived.py).
    assert "total_input_tokens" not in ur_updates
    assert "total_cost" not in ur_updates
    assert result["conversation_id"] == CONVERSATION_ID
    assert result["request_ids"], "cost row id must be reported"
    # Non-history ceremony is the ONLY thing a system run skips.
    assert calls["cache_state"] == []
    assert calls["context_state"] == []


@pytest.mark.asyncio
async def test_no_metadata_key_turns_history_off(system_run_harness, monkeypatch):
    """The old opt-in/opt-out channel is gone: whatever a context carries in
    its metadata, a stored system run still writes its history."""
    persistence_mod, calls = system_run_harness
    import matrx_ai.context.app_context as app_ctx_mod

    assert not hasattr(persistence_mod, "SYSTEM_RUN_KEEP_TRANSCRIPT_KEY")

    class NoisyCtx(_SystemRunCtx):
        metadata = {"system_run_keep_transcript": False, "keep_transcript": False}

    ctx = NoisyCtx()
    monkeypatch.setattr(app_ctx_mod, "get_app_context", lambda: ctx)
    monkeypatch.setattr(app_ctx_mod, "try_get_app_context", lambda: ctx)
    result = await persistence_mod.persist_completed_request(
        _build_completed(), conversation_id=CONVERSATION_ID
    )
    _assert_full_history(calls, result)


@pytest.mark.asyncio
async def test_forty_concurrent_system_runs_stay_cheap(system_run_harness, monkeypatch):
    """The 2026-07-07 starvation must not return. 40 concurrent system-run
    persists, each against a fake DB with 20 ms latency per awaited read:
    every history write is a QUEUED op (no awaited round trip — they commit in
    the one coordinator flush), the only awaited DB reads are the
    system-prompt freeze lookup and the superseded-failure check (2/run), no
    cache_state / context-state work runs, and the batch finishes in about
    one read latency (concurrent), never 40 x N sequential round trips."""
    import asyncio
    import time

    persistence_mod, calls = system_run_harness
    reads: list[str] = []
    latency = 0.02

    class _CountingCxm:
        class conversation:  # noqa: N801 - mirrors cxm.conversation
            @staticmethod
            async def load_conversation_by_id(conv_id):
                reads.append(conv_id)
                await asyncio.sleep(latency)
                return SimpleNamespace(system_instruction=None, config={})

    monkeypatch.setattr(persistence_mod, "cxm", _CountingCxm())

    async def _counting_hide(conv_id, up_to):
        reads.append(f"hide:{conv_id}")
        await asyncio.sleep(latency)
        return 0

    monkeypatch.setattr(persistence_mod, "_hide_superseded_failed_turns", _counting_hide)

    runs = 40
    t0 = time.perf_counter()
    results = await asyncio.gather(
        *[
            persistence_mod.persist_completed_request(
                _build_completed(), conversation_id=CONVERSATION_ID
            )
            for _ in range(runs)
        ]
    )
    elapsed = time.perf_counter() - t0

    queued = (
        len(calls["message_create"])
        + len(calls["message_update"])
        + len(calls["conversation_update"])
        + len(calls["request_create"])
        + len(calls["user_request_update"])
    )
    print(
        f"\n[starvation-proof] runs={runs} awaited_db_reads={len(reads)} "
        f"queued_ops={queued} ({queued / runs:.1f}/run) "
        f"cache_state={len(calls['cache_state'])} context_state={len(calls['context_state'])} "
        f"elapsed={elapsed * 1000:.0f}ms (one read = {latency * 1000:.0f}ms)"
    )
    assert all(len(r["message_ids"]) == 2 for r in results)
    assert len(reads) <= 2 * runs, "at most TWO awaited DB reads per system run"
    assert calls["cache_state"] == [] and calls["context_state"] == []
    assert elapsed < latency * 2 * 5, "concurrent persists must not serialize round trips"


@pytest.mark.asyncio
async def test_lost_history_write_is_captured_once(system_run_harness, monkeypatch):
    """No silent loss: a stored run whose message write fails lands ONE
    ``run_history_write_failure`` system_error, and the failure still
    propagates (data-first persistence contract)."""
    persistence_mod, calls = system_run_harness
    import matrx_ai._ext as ext_mod

    captured: list[dict[str, Any]] = []

    async def _record_error(exc, **kw):
        captured.append(kw)

    monkeypatch.setitem(ext_mod._registry, "record_error", _record_error)

    def _boom(**kw):
        raise RuntimeError("message queue down")

    monkeypatch.setattr(persistence_mod, "_queue_message_create", _boom)
    with pytest.raises(RuntimeError) as raised:
        await persistence_mod.persist_completed_request(
            _build_completed(), conversation_id=CONVERSATION_ID
        )
    # A second (commit-level) report of the same exception is a no-op.
    await persistence_mod.record_run_history_write_failure(raised.value, stage="commit")
    assert [c["kind"] for c in captured] == [persistence_mod.RUN_HISTORY_WRITE_FAILURE_KIND]
    assert captured[0]["payload"]["stage"] == "queue"
    assert captured[0]["payload"]["system_run"] is True
    assert captured[0]["payload"]["conversation_id"] == CONVERSATION_ID


@pytest.mark.asyncio
async def test_normal_run_still_persists_messages(system_run_harness, monkeypatch):
    """Control: a normal run writes the same history a system run does, and
    additionally runs the ceremony a system run skips."""
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


@pytest.mark.asyncio
@pytest.mark.parametrize("actor", [None, "", "   "])
async def test_organization_system_run_keeps_cost_without_user(
    system_run_harness, monkeypatch, actor
):
    persistence_mod, calls = system_run_harness
    import matrx_ai.context.app_context as app_ctx_mod

    class GuestCtx(_SystemRunCtx):
        user_id = actor
        organization_id = "66666666-6666-4666-8666-666666666666"

    ctx = GuestCtx()
    monkeypatch.setattr(app_ctx_mod, "get_app_context", lambda: ctx)
    monkeypatch.setattr(app_ctx_mod, "try_get_app_context", lambda: ctx)
    result = await persistence_mod.persist_completed_request(
        _build_completed(), conversation_id=CONVERSATION_ID
    )
    assert len(calls["request_create"]) == 1
    assert calls["request_create"][0]["created_by"] is None
    assert calls["request_create"][0]["organization_id"] == ctx.organization_id
    assert calls["user_request_update"]
    assert calls["conversation_update"], "an org system run keeps its history too"
    assert result["request_ids"]


# ---------------------------------------------------------------------------
# run_agent surface — history cannot be switched off at the call site either
# ---------------------------------------------------------------------------


def test_run_agent_has_no_history_switch():
    import inspect

    from matrx_ai.agents.executor import run_agent

    params = inspect.signature(run_agent).parameters
    assert "keep_transcript" not in params, "no parameter may turn a run's history off"


def _capturing_agent(seen: dict[str, Any], *, name: str = "mandate-holder") -> Any:
    async def _capture_execute(user_input: Any = None, *, max_iterations: Any = None) -> Any:
        from matrx_connect.context.app_context import get_app_context

        ctx = get_app_context()
        seen["store"] = ctx.store
        seen["system_run"] = ctx.system_run
        seen["request_id"] = ctx.request_id
        seen["metadata"] = dict(ctx.metadata)
        return SimpleNamespace(
            output="ok",
            assistant_response=None,
            config=SimpleNamespace(model="test-model", metadata={}),
            usage=None,
            usage_history=[],
            metadata={},
        )

    return SimpleNamespace(
        name=name,
        config=SimpleNamespace(model="test-model", metadata={}),
        source_id=None,
        source_is_version=False,
        request_metadata={},
        execute=_capture_execute,
    )


@pytest.mark.asyncio
async def test_run_agent_system_run_reports_ids():
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id=USER_ID, request_id=REQUEST_ID))
    seen: dict[str, Any] = {}
    result = await run_agent(
        _capturing_agent(seen),  # type: ignore[arg-type]
        label="mandate:x.y",
        source_app="test",
        source_feature="mandate:x.y",
        emit_lifecycle=False,
        system_run=True,
    )
    assert result.success
    assert seen["system_run"] is True
    assert result.metadata.get("request_id") == REQUEST_ID, "the run's request id is reported"
    assert result.metadata.get("conversation_id"), "the run's conversation id is reported"


@pytest.mark.asyncio
async def test_run_agent_store_true_persists_inside_non_persisting_parent():
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(
        AppContext(emitter=ConsoleEmitter(), user_id=USER_ID, request_id="not-a-uuid", store=False)
    )
    seen: dict[str, Any] = {}
    result = await run_agent(
        _capturing_agent(seen),  # type: ignore[arg-type]
        label="mandate:x.y",
        source_app="test",
        source_feature="mandate:x.y",
        emit_lifecycle=False,
        system_run=True,
        store=True,
    )
    assert seen["store"] is True, "store=True must persist the run inside a store=False parent"
    import uuid as _uuid

    _uuid.UUID(seen["request_id"])  # a stored run gets a UUID request id
    assert result.metadata.get("request_id") == seen["request_id"]


@pytest.mark.asyncio
async def test_run_agent_store_default_inherits_parent():
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent

    set_app_context(
        AppContext(emitter=ConsoleEmitter(), user_id=USER_ID, request_id=REQUEST_ID, store=False)
    )
    seen: dict[str, Any] = {}
    await run_agent(
        _capturing_agent(seen),  # type: ignore[arg-type]
        label="ephemeral",
        source_app="test",
        source_feature="ephemeral",
        emit_lifecycle=False,
        system_run=True,
    )
    assert seen["store"] is False
