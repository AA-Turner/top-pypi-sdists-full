"""Mandate-candidate containment — a candidate run can read, never write.

PLAN.md (common-docs/projects/mandate-candidates) P3/P11/P12 and §2.7. Under the
``mandate_candidate`` marker every tool call is decided BEFORE it can do
anything: ``real`` (read_only / paid_read), ``borrowed`` (the live run made the
same call; its model-facing result is handed back), or ``stopped`` (everything
else). A stop is terminal and is never fed to the model as a result.

Every test here drives the REAL ``ToolExecutor.execute`` pipeline; the only
doubles are the tool bodies (which record whether they ran) and the durable
row writes (which record what was stamped).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.logger import ToolExecutionLogger
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType
from matrx_ai.tools.registry import ToolRegistry

MARKER = {
    "candidate_id": "11111111-1111-1111-1111-111111111111",
    "candidate_run_id": "22222222-2222-2222-2222-222222222222",
    "live_request_id": "33333333-3333-3333-3333-333333333333",
}


class _NullEmitter:
    def __init__(self) -> None:
        self.tool_events: list[Any] = []

    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_info(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_init(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_completion(self, *_a: Any, **_kw: Any) -> None: ...

    async def send_tool_event(self, event: Any, *_a: Any, **_kw: Any) -> None:
        self.tool_events.append(event)

    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


def _candidate_metadata() -> dict[str, Any]:
    try:
        from matrx_ai.tools.candidate_containment import candidate_context_metadata
    except ImportError:  # the unfixed tree: only the bare marker exists
        return {"mandate_candidate": dict(MARKER)}
    return candidate_context_metadata(MARKER)


@pytest.fixture
def harness(monkeypatch):
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    import matrx_ai.persistence.queue_helpers as qh

    # Not inside a request lane: no coordinator (see CLAUDE.md "An executor test
    # that is not inside a request lane doubles get_coordinator").
    monkeypatch.setattr(qh, "get_coordinator", lambda: None)

    emitter = _NullEmitter()
    metadata = _candidate_metadata()
    token = set_app_context(AppContext(emitter=emitter, metadata=metadata, is_authenticated=True))
    registry = ToolRegistry.get_instance()
    saved = dict(registry._tools)
    invoked: list[str] = []
    started: list[dict[str, Any]] = []
    abandoned: list[dict[str, Any]] = []
    delegated: list[str] = []

    async def fake_log_started(self, ctx, tool_def, arguments, **kw):
        started.append({"tool": tool_def.name, **kw})
        return f"row-{tool_def.name}"

    async def fake_log_abandoned(self, row_id, **kw):
        abandoned.append({"row_id": row_id, **kw})

    async def fake_log_completed(self, row_id, result, *_a, **_kw):
        return None

    async def fake_delegate_durably(self, row_id, **_kw):
        delegated.append(row_id)

    monkeypatch.setattr(ToolExecutionLogger, "log_started", fake_log_started)
    monkeypatch.setattr(ToolExecutionLogger, "log_abandoned", fake_log_abandoned)
    monkeypatch.setattr(ToolExecutionLogger, "log_completed", fake_log_completed)
    monkeypatch.setattr(ToolExecutionLogger, "log_error", fake_log_completed)
    monkeypatch.setattr(ToolExecutionLogger, "delegate_durably", fake_delegate_durably)

    def add_tool(name: str, side_effect_class: str | None, output: Any = "done") -> None:
        async def body(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
            invoked.append(name)
            return ToolResult(success=True, output=output, tool_name=name, call_id=ctx.call_id)

        definition = ToolDefinition(
            name=name,
            description=f"{name} test tool",
            parameters={},
            tool_type=ToolType.LOCAL,
            function_path=f"tests.fake.{name}",
            side_effect_class=side_effect_class,
        )
        definition._callable = body
        registry._tools[name] = definition

    yield {
        "executor": ToolExecutor(registry=registry),
        "add_tool": add_tool,
        "invoked": invoked,
        "started": started,
        "abandoned": abandoned,
        "delegated": delegated,
        "emitter": emitter,
        "metadata": metadata,
        "registry": registry,
    }
    registry._tools = saved
    clear_app_context(token)
    try:
        from matrx_ai.tools.candidate_containment import set_candidate_borrow_lookup

        set_candidate_borrow_lookup(None)
    except ImportError:
        pass


def _ctx(name: str, call_id: str = "call-1") -> ToolContext:
    return ToolContext(call_id=call_id, tool_name=name)


def _ledger(metadata: dict[str, Any]) -> dict[str, Any]:
    return metadata["mandate_candidate_containment"]


async def test_sends_to_human_tool_halts_with_zero_effect(harness) -> None:
    harness["add_tool"]("send_email_test", "sends_to_human")
    content, result = await harness["executor"].execute(
        "send_email_test", {"to": "a@b.c", "body": "hi"}, _ctx("send_email_test")
    )
    assert harness["invoked"] == [], "the tool body ran under the candidate marker"
    assert getattr(result, "candidate_stopped", False) is True
    assert result.success is False
    ledger = _ledger(harness["metadata"])
    assert ledger["stopped_at"]["tool"] == "send_email_test"
    assert ledger["stopped_at"]["class"] == "sends_to_human"
    assert ledger["stopped_at"]["args"] == {"to": "a@b.c", "body": "hi"}
    assert ledger["tool_dispositions"][0]["disposition"] == "stopped"
    # The disposition is stamped on the tool-call row at insert, and the row is
    # closed as a candidate stop — not a tool failure the model caused.
    assert harness["started"][0]["candidate_disposition"]["disposition"] == "stopped"
    assert harness["abandoned"][0]["reason"] == "candidate_stopped"


async def test_unclassified_tool_halts_with_zero_effect(harness) -> None:
    harness["add_tool"]("mystery_tool", None)
    _content, result = await harness["executor"].execute(
        "mystery_tool", {"x": 1}, _ctx("mystery_tool")
    )
    assert harness["invoked"] == [], "an UNCLASSIFIED tool ran under the candidate marker"
    assert getattr(result, "candidate_stopped", False) is True
    stop = _ledger(harness["metadata"])["stopped_at"]
    assert stop["class"] == "platform_meta"  # NULL is read as the most dangerous class
    assert "unclassified" in _ledger(harness["metadata"])["tool_dispositions"][0]["stopped_reason"]


async def test_read_only_tool_runs_for_real(harness) -> None:
    harness["add_tool"]("lookup_test", "read_only", output="3 rows")
    content, result = await harness["executor"].execute(
        "lookup_test", {"q": "x"}, _ctx("lookup_test")
    )
    assert harness["invoked"] == ["lookup_test"]
    assert result.success is True and content["content"] == "3 rows"
    ledger = _ledger(harness["metadata"])
    assert ledger["stopped_at"] is None
    entry = ledger["tool_dispositions"][0]
    assert entry["disposition"] == "real" and entry["side_effect_class"] == "read_only"
    assert harness["started"][0]["candidate_disposition"]["disposition"] == "real"


async def test_delegated_tool_halts_at_the_call_and_never_delegates(harness) -> None:
    # A client tool classified read_only is STILL stopped: the effect happens
    # on a client that does not exist in the background.
    harness["add_tool"]("browser_read_page", "read_only")
    _content, result = await harness["executor"].execute(
        "browser_read_page",
        {"tab": 1},
        _ctx("browser_read_page"),
        client_tools=frozenset({"browser_read_page"}),
    )
    assert harness["invoked"] == []
    assert harness["delegated"] == [], "the delegation suspend path ran"
    assert not any(
        getattr(e, "event", None) == "tool_delegated" for e in harness["emitter"].tool_events
    )
    assert result.delegated_pending is False
    assert getattr(result, "candidate_stopped", False) is True
    assert (
        "client-delegated" in _ledger(harness["metadata"])["tool_dispositions"][0]["stopped_reason"]
    )


async def test_live_call_with_equal_args_is_borrowed_not_run(harness) -> None:
    from matrx_ai.tools.candidate_containment import (
        BorrowedToolResult,
        args_digest,
        set_candidate_borrow_lookup,
    )

    harness["add_tool"]("write_row_test", "db_write")
    asked: list[Any] = []

    async def lookup(req):
        asked.append(req)
        if req.tool_name == "write_row_test" and req.args_digest == args_digest({"b": 2, "a": 1}):
            return BorrowedToolResult(content='{"id": "row-9"}', live_call_id="live-call-7")
        return None

    set_candidate_borrow_lookup(lookup)
    content, result = await harness["executor"].execute(
        "write_row_test", {"a": 1, "b": 2}, _ctx("write_row_test")
    )
    assert harness["invoked"] == [], "a borrowed write ran for real"
    assert content["content"] == '{"id": "row-9"}' and content["is_error"] is False
    assert asked[0].occurrence == 1
    entry = _ledger(harness["metadata"])["tool_dispositions"][0]
    assert entry["disposition"] == "borrowed" and entry["borrowed_from_call_id"] == "live-call-7"
    assert _ledger(harness["metadata"])["stopped_at"] is None


async def test_no_marker_means_no_containment(harness) -> None:
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    harness["add_tool"]("send_email_test", "sends_to_human")
    token = set_app_context(AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True))
    try:
        _content, result = await harness["executor"].execute(
            "send_email_test", {"to": "a@b.c"}, _ctx("send_email_test")
        )
    finally:
        clear_app_context(token)
    assert harness["invoked"] == ["send_email_test"]
    assert result.success is True
    assert (
        "candidate_disposition" not in harness["started"][0]
        or harness["started"][0]["candidate_disposition"] is None
    )


async def test_child_agent_inherits_containment(harness, monkeypatch) -> None:
    """An agent-as-tool runs (its child is contained); the child's write stops
    the child AND the parent call — the parent never receives the child's
    result."""
    from matrx_connect.context.app_context import child_agent_context

    import matrx_ai.tools.agent_tool as agent_tool_mod

    harness["add_tool"]("send_sms_test", "sends_to_human")
    executor = harness["executor"]
    child_saw_marker: list[bool] = []

    async def fake_execute_agent_tool(tool_def, args, ctx):
        async with child_agent_context("child", emit_lifecycle=False) as child_ctx:
            child_saw_marker.append("mandate_candidate" in child_ctx.metadata)
            await executor.execute("send_sms_test", {"to": "+1"}, _ctx("send_sms_test", "c-2"))
        return ToolResult(
            success=True, output="child answered", tool_name=tool_def.name, call_id=ctx.call_id
        )

    monkeypatch.setattr(agent_tool_mod, "execute_agent_tool", fake_execute_agent_tool)
    agent_def = ToolDefinition(
        name="custom_tool_1",
        description="a saved agent",
        parameters={},
        tool_type=ToolType.AGENT,
    )
    harness["registry"]._tools["custom_tool_1"] = agent_def

    content, result = await executor.execute("custom_tool_1", {"q": "go"}, _ctx("custom_tool_1"))
    assert child_saw_marker == [True], "the child agent did not inherit the marker"
    assert harness["invoked"] == [], "the child's write ran"
    assert getattr(result, "candidate_stopped", False) is True, (
        "the parent was handed the child's answer after the child stopped"
    )
    assert content.get("content") != "child answered"
    ledger = _ledger(harness["metadata"])
    assert [d["disposition"] for d in ledger["tool_dispositions"]] == ["real", "stopped"]
    assert ledger["stopped_at"]["tool"] == "send_sms_test"


async def test_stopped_call_is_never_fed_to_the_model(harness, monkeypatch) -> None:
    """handle_tool_calls_v2 drops a stopped call from the results the model gets
    and never reports it as a pending (delegated) call."""
    import matrx_ai.tools.handle_tool_calls as htc

    harness["add_tool"]("send_email_test", "sends_to_human")
    harness["add_tool"]("lookup_test", "read_only", output="ok")
    monkeypatch.setattr(htc, "get_executor", lambda: harness["executor"])
    completed, _usages, pending, _stubs, _handoff = await htc.handle_tool_calls_v2(
        [
            {"name": "lookup_test", "arguments": {}, "call_id": "c-read"},
            {"name": "send_email_test", "arguments": {"to": "x"}, "call_id": "c-send"},
        ],
        iteration=1,
    )
    assert [c["call_id"] for c in completed] == ["c-read"]
    assert pending == []
    assert _ledger(harness["metadata"])["stopped_at"]["tool"] == "send_email_test"


# ── The run ends TERMINALLY at a stop (orchestrator) ─────────────────────────


def _orchestrator_source() -> str:
    import inspect

    import matrx_ai.orchestrator.executor as orch

    return inspect.getsource(orch)


def candidate_stop_wiring_problems(source: str) -> list[str]:
    """Structural half: the loop ends the run at a candidate stop, and every
    finalize exposes the dispositions. Returns what is missing."""
    import ast

    tree = ast.parse(source)
    funcs = {
        n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef)
    }
    problems: list[str] = []
    if "_stop_for_candidate" not in funcs:
        problems.append("no _stop_for_candidate terminal exit")
    callers = [
        name
        for name, fn in funcs.items()
        if name != "_stop_for_candidate"
        and any(
            isinstance(c, ast.Call) and getattr(c.func, "id", None) == "_stop_for_candidate"
            for c in ast.walk(fn)
        )
    ]
    if not any(
        any(
            isinstance(c, ast.Call) and getattr(c.func, "id", None) == "handle_tool_calls"
            for c in ast.walk(funcs[name])
        )
        for name in callers
    ):
        problems.append("the tool-dispatch loop never calls _stop_for_candidate")
    finalize = funcs.get("_finalize_and_persist")
    if finalize is None or not any(
        isinstance(c, ast.Call) and getattr(c.func, "id", None) == "candidate_outcome"
        for c in ast.walk(finalize)
    ):
        problems.append("_finalize_and_persist does not expose candidate_outcome()")
    return problems


def test_the_loop_ends_the_run_at_a_candidate_stop() -> None:
    assert candidate_stop_wiring_problems(_orchestrator_source()) == []


async def test_stop_for_candidate_is_terminal_and_carries_the_stop(monkeypatch) -> None:
    import matrx_ai.orchestrator.executor as orch

    captured: dict[str, Any] = {}

    async def fake_finalize(**kwargs):
        captured.update(kwargs)
        return "completed-request"

    monkeypatch.setattr(orch, "_finalize_and_persist", fake_finalize)

    class _Ctx:
        emitter = _NullEmitter()

    stop = {"step": 2, "tool": "send_email_test", "args": {"to": "x"}, "class": "sends_to_human"}
    out = await orch._stop_for_candidate(
        exec_ctx=_Ctx(),
        state=None,
        current_request=None,
        response=None,
        iteration=1,
        stopped_at=stop,
        trigger_position=0,
        pre_execution_message_count=0,
        debug=False,
    )
    assert out == "completed-request"
    assert captured["metadata"]["status"] == "candidate_stopped"
    assert captured["metadata"]["candidate_stopped"] == stop


# ── P11: the tools OFFERED are exactly the live run's ─────────────────────────


def test_candidate_marker_never_changes_the_offered_tools() -> None:
    """A client-executed tool stays offered (and routed to the client) under the
    marker — containment stops at the CALL, it never trims the offer. The offer
    with and without the marker is identical."""
    import copy

    from matrx_connect.context.app_context import AppContext

    from matrx_ai.config.unified_config import UnifiedConfig
    from matrx_ai.tools.candidate_containment import candidate_context_metadata
    from matrx_ai.tools.merge import merge_request_tools
    from matrx_ai.tools.specs import RegisteredToolSpec

    reg = ToolRegistry.get_instance()
    saved_state = {
        k: (copy.copy(v) if isinstance(v, dict | set | list) else v)
        for k, v in reg.__dict__.items()
    }
    try:
        reg.load_from_definitions(
            [
                ToolDefinition(
                    name="browser_read_page_p11",
                    description="x",
                    parameters={},
                    tool_type=ToolType.EXTERNAL_HANDLER,
                    tool_id="44444444-4444-4444-4444-444444444444",
                    side_effect_class="read_only",
                )
            ]
        )
        reg._bindings_by_tool = {"browser_read_page_p11": {"matrx-user"}}

        def offer(metadata: dict[str, Any]) -> tuple[list[Any], list[str]]:
            config = UnifiedConfig(model="gpt-4.1-mini", messages=[], tools=[], custom_tools=[])
            ctx = merge_request_tools(
                config,
                AppContext(emitter=None, client_tools=[], metadata=metadata),
                [RegisteredToolSpec(name="browser_read_page_p11")],
                active_executors=frozenset({"matrx-user"}),
            )
            return list(config.tools), sorted(ctx.client_tools or [])

        live = offer({})
        candidate = offer(candidate_context_metadata(MARKER))
        assert candidate == live
        assert "browser_read_page_p11" in candidate[1], "the client tool was not offered"
    finally:
        reg.__dict__.clear()
        reg.__dict__.update(saved_state)


async def test_sub_agent_tools_run_contained_and_stop_only_a_write_back(harness) -> None:
    """Mandate Candidates C2/C3 (supersedes the C1 v1 stop): agent_call / mandate_call /
    staff_escalate run CONTAINED — the child inherits the marker and ledger — and only
    agent_call's ``remember`` write-back into another conversation stops."""
    from matrx_ai.tools.candidate_containment import AGENT_TOOL_CLASS, classify_call

    for name in ("agent_call", "mandate_call", "staff_escalate"):
        tool = SimpleNamespace(name=name, tool_type=None, side_effect_class="platform_meta")
        assert classify_call(tool, {"agent_id": "x", "user_input": "go"}, is_delegated=False) == (
            AGENT_TOOL_CLASS,
            None,
        )
    harness["add_tool"]("agent_call", "platform_meta")
    _content, result = await harness["executor"].execute(
        "agent_call",
        {"agent_id": "x", "user_input": "go", "history_mode": "snapshot", "remember": True},
        _ctx("agent_call"),
    )
    assert harness["invoked"] == []
    assert result.candidate_stopped is True
    stop = _ledger(harness["metadata"])["stopped_at"]
    assert stop["reason"].startswith("sub-agent call with remember=true")


async def test_the_ledger_reaches_the_metadata_write_without_a_nul_byte(harness) -> None:
    """FX2-S N5: the containment ledger rides the candidate's request metadata into
    ``chat.user_request``. Its occurrence keys used ``\\x00`` as a separator, so every
    contained call made the write gate (``_queue_or_drop`` → ``sanitize_postgres_text``)
    replace a NUL byte, log an ERROR and file ``persistence_payload_sanitized``. A real call
    and a stopped call must both leave a ledger the gate passes untouched."""
    from matrx_ai.persistence.postgres_text import sanitize_postgres_text

    harness["add_tool"]("lookup_test", "read_only", output="3 rows")
    harness["add_tool"]("send_email_test", "sends_to_human")
    await harness["executor"].execute("lookup_test", {"q": "x"}, _ctx("lookup_test"))
    await harness["executor"].execute(
        "send_email_test", {"to": "a@b.c"}, _ctx("send_email_test", "call-2")
    )
    ledger = _ledger(harness["metadata"])
    assert len(ledger["occurrences"]) == 2 and ledger["stopped_at"]["tool"] == "send_email_test"
    gate = sanitize_postgres_text({"metadata": harness["metadata"]})
    assert gate.replacements == 0, list(gate.paths)
