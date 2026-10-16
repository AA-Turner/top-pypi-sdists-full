"""An agent run that ends early must still settle the money it really spent.

Live incident (news engine run 70601b15, 2026-10-05): a per-call time limit
(``asyncio.wait_for``) cancelled ``run_agent`` mid-loop, after the model had
already made billed calls. The cancel branch settled the run's spine execution
as ``cancelled`` with NO meters — $0 — so the run total, the cost tree and the
monthly spend ceiling all under-counted about $0.70. The crash branch had the
same hole: an exception escaping the loop settled ``failed`` at $0.

The usage lives on the in-flight request inside ``execute_until_complete``; it
never reached ``run_agent`` because ``Agent.execute`` raised instead of
returning. These tests drive the REAL ``run_agent`` -> REAL
``execute_until_complete`` chain; only the provider loop body (which bills one
call and then waits, or raises) and the persistence write are doubled. They
assert on what the host tracker's ``settle`` actually received.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

import matrx_ai.orchestrator.executor as executor_mod
from matrx_ai.config import MessageList, TextContent, TokenUsage, UnifiedConfig, UnifiedMessage
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.orchestrator.requests import AIMatrixRequest

PER_CALL_USD = 0.35


@pytest.fixture
def priced(monkeypatch: pytest.MonkeyPatch) -> None:
    # Pricing comes from the DB catalog; pin it so the test measures settlement,
    # not the catalog. (Never changes production pricing.)
    monkeypatch.setattr(
        TokenUsage, "calculate_cost", lambda self, pricing_lookup=None: PER_CALL_USD
    )


@pytest.fixture
def app_ctx():
    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    token = set_app_context(
        AppContext(
            emitter=ConsoleEmitter(),
            user_id="22222222-2222-2222-2222-222222222222",
            request_id="33333333-3333-3333-3333-333333333333",
        )
    )
    try:
        yield
    finally:
        clear_app_context(token)


@pytest.fixture
def tracker(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    settled: list[dict[str, Any]] = []

    async def settle(status: str, *, error: str | None = None, meters: dict | None = None) -> None:
        settled.append({"status": status, "error": error, "meters": meters})

    async def open_tracker(*, label: str, source_feature: str) -> Any:
        return settle

    import matrx_ai._ext as ext

    monkeypatch.setattr(ext, "get_internal_run_tracker", lambda: open_tracker)
    return settled


@pytest.fixture
def no_persist(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_finalize(*, state: ExecutionState | None = None, **_kw: Any) -> object:
        if state is not None:
            state.persisted = True
        return object()

    monkeypatch.setattr(executor_mod, "_finalize_and_persist", fake_finalize)


def _request() -> AIMatrixRequest:
    cfg = UnifiedConfig(
        model="m",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="judge it")])]
        ),
    )
    return AIMatrixRequest(conversation_id="conv-1", config=cfg)


def _billed_call() -> TokenUsage:
    return TokenUsage(input_tokens=1000, output_tokens=200, matrx_model_name="m", api="xai")


def _loop_that_bills_then(after_billing: str):
    """The provider loop body: one billed call lands, then the run either waits
    for its next call (and gets cancelled) or crashes out of the loop."""

    async def fake_inner(*, state: ExecutionState, **_kw: Any) -> Any:
        req = _request()
        state.current_request = req
        state.iteration = 1
        state.trigger_position = 0
        state.pre_execution_message_count = 1
        req.add_usage(_billed_call())
        if after_billing == "wait":
            await asyncio.sleep(30)  # the second model call, cut off by the limit
        raise RuntimeError("commit barrier failed after a billed call")

    return fake_inner


def _agent() -> Any:
    async def execute(user_input: Any = None, *, max_iterations: Any = None, **_: Any) -> Any:
        return await executor_mod.execute_until_complete(
            initial_request=object(), client=object()
        )

    return SimpleNamespace(
        name="news-judge",
        config=SimpleNamespace(model="m", metadata={}),
        source_id=None,
        source_is_version=False,
        execute=execute,
    )


@pytest.mark.asyncio
async def test_a_run_cancelled_by_a_time_limit_settles_what_it_spent(
    monkeypatch: pytest.MonkeyPatch, priced, app_ctx, tracker, no_persist
) -> None:
    from matrx_ai.agents.executor import run_agent

    monkeypatch.setattr(
        executor_mod, "_execute_until_complete_inner", _loop_that_bills_then("wait")
    )

    with pytest.raises(TimeoutError):
        await asyncio.wait_for(
            run_agent(_agent(), label="judge", source_app="test", source_feature="news",
                      emit_lifecycle=False),
            timeout=0.2,
        )

    assert len(tracker) == 1, tracker
    assert tracker[0]["status"] == "cancelled"
    meters = tracker[0]["meters"] or {}
    assert meters.get("usd") == pytest.approx(PER_CALL_USD), (
        f"a cancelled run that made a billed call settled {meters!r} — the spend "
        "vanished from the run total, the cost tree and the monthly ceiling"
    )
    assert meters.get("input_tokens") == 1000
    assert meters.get("output_tokens") == 200


@pytest.mark.asyncio
async def test_a_run_that_crashes_out_of_the_loop_settles_what_it_spent(
    monkeypatch: pytest.MonkeyPatch, priced, app_ctx, tracker, no_persist
) -> None:
    from matrx_ai.agents.executor import run_agent

    monkeypatch.setattr(
        executor_mod, "_execute_until_complete_inner", _loop_that_bills_then("raise")
    )

    result = await run_agent(
        _agent(), label="judge", source_app="test", source_feature="news", emit_lifecycle=False
    )

    assert result.success is False
    assert len(tracker) == 1, tracker
    assert tracker[0]["status"] == "failed"
    meters = tracker[0]["meters"] or {}
    assert meters.get("usd") == pytest.approx(PER_CALL_USD), meters
    # The caller sees the spend too (agent-as-tool settles its child from this).
    assert len(result.usage_history) == 1
    assert result.usage["total"]["total_cost"] == pytest.approx(PER_CALL_USD)


@pytest.mark.asyncio
async def test_a_nested_run_never_claims_its_parents_spend(
    monkeypatch: pytest.MonkeyPatch, priced, app_ctx, tracker, no_persist
) -> None:
    """A tool that calls the loop directly (no run_agent of its own) inside a
    run must not rebind the run's usage to the tool's own request."""
    from matrx_ai.orchestrator.execution_state import (
        bind_run_usage_sink,
        close_run_usage_sink,
        open_run_usage_sink,
    )

    sink, token = open_run_usage_sink()
    try:
        outer = ExecutionState()
        bind_run_usage_sink(outer)
        outer.current_request = _request()
        outer.current_request.add_usage(_billed_call())
        inner = ExecutionState()
        bind_run_usage_sink(inner)  # must be ignored — the sink is the outer run's
        inner.current_request = _request()
        assert len(sink.usage_history()) == 1
        assert sink.state is outer
    finally:
        close_run_usage_sink(token)


# ---------------------------------------------------------------------------
# Agent-as-tool: the spawner OWNS the child's spine record (run_agent's own
# tracker stands down for it), so the tool path must settle the real spend too.
# ---------------------------------------------------------------------------


@pytest.fixture
def child_spawner(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    settled: list[dict[str, Any]] = []

    async def settle(*, success: bool, usage_history: list[Any], cancelled: bool = False) -> None:
        settled.append({"success": success, "usage_history": list(usage_history),
                        "cancelled": cancelled})

    async def spawner(*, label: str, link_id: Any) -> Any:
        return "child-exec-1", settle

    import matrx_ai._ext as ext
    import matrx_ai.agents.definition as definition_mod

    monkeypatch.setattr(ext, "get_child_execution_spawner", lambda: spawner)

    async def from_agent(*_a: Any, **_kw: Any) -> Any:
        return _agent()

    monkeypatch.setattr(
        definition_mod.Agent, "from_agent", classmethod(lambda cls, *a, **kw: from_agent(*a, **kw))
    )
    return settled


def _agent_tool_def() -> Any:
    from matrx_ai.tools.agent_projection import _variable_definitions_to_parameters
    from matrx_ai.tools.models import ToolDefinition, ToolType

    return ToolDefinition(
        name="judge_tool",
        tool_type=ToolType.AGENT,
        prompt_id="abc-123",
        parameters=_variable_definitions_to_parameters(None),
    )


@pytest.mark.asyncio
async def test_a_cancelled_agent_tool_child_settles_what_it_spent(
    monkeypatch: pytest.MonkeyPatch, priced, app_ctx, child_spawner, no_persist
) -> None:
    from matrx_ai.tools.agent_tool import execute_agent_tool
    from matrx_ai.tools.models import ToolContext

    monkeypatch.setattr(
        executor_mod, "_execute_until_complete_inner", _loop_that_bills_then("wait")
    )

    with pytest.raises(TimeoutError):
        await asyncio.wait_for(
            execute_agent_tool(_agent_tool_def(), {"input": "judge"}, ToolContext(call_id="c")),
            timeout=0.2,
        )

    assert len(child_spawner) == 1, "a cancelled agent-tool child was never settled"
    assert child_spawner[0]["success"] is False
    assert child_spawner[0]["cancelled"] is True, "a cut-off child must settle CANCELLED"
    assert len(child_spawner[0]["usage_history"]) == 1, (
        "the child's billed call never reached its spine settle — recorded $0"
    )


@pytest.mark.asyncio
async def test_a_crashed_agent_tool_child_settles_what_it_spent(
    monkeypatch: pytest.MonkeyPatch, priced, app_ctx, child_spawner, no_persist
) -> None:
    from matrx_ai.tools.agent_tool import execute_agent_tool
    from matrx_ai.tools.models import ToolContext

    monkeypatch.setattr(
        executor_mod, "_execute_until_complete_inner", _loop_that_bills_then("raise")
    )

    result = await execute_agent_tool(
        _agent_tool_def(), {"input": "judge"}, ToolContext(call_id="c")
    )

    assert result.success is False
    assert len(child_spawner) == 1
    assert child_spawner[0]["success"] is False
    assert len(child_spawner[0]["usage_history"]) == 1
    assert child_spawner[0]["cancelled"] is False, "a crash is a failure, not a cancel"


def test_a_time_limit_error_still_carries_the_runs_spend() -> None:
    """``asyncio.wait_for`` raises TimeoutError FROM the run's cancellation; a
    caller tallying its own cost reads the spend through the chain."""
    from matrx_ai.agents.executor import _stamp_run_usage, run_usage_from_exception

    cancel = asyncio.CancelledError()
    _stamp_run_usage(cancel, [_billed_call()])
    try:
        raise TimeoutError() from cancel
    except TimeoutError as exc:
        assert len(run_usage_from_exception(exc)) == 1
    assert run_usage_from_exception(RuntimeError("nothing billed")) == []


@pytest.mark.asyncio
async def test_a_run_the_loop_stopped_settles_cancelled_not_completed(
    priced, app_ctx, tracker
) -> None:
    """A tree budget / deadline / subtree time budget stop returns normally with
    status "cancelled". The spine must record "cancelled", with its spend."""
    from matrx_ai.agents.executor import run_agent
    from matrx_ai.config.usage_config import TokenUsage as _TU

    history = [_billed_call()]

    async def execute(user_input: Any = None, *, max_iterations: Any = None, **_: Any) -> Any:
        return SimpleNamespace(
            output="partial answer",
            assistant_response=None,
            config=SimpleNamespace(model="m", metadata={}),
            usage=_TU.aggregate_by_model(history),
            usage_history=history,
            metadata={
                "status": "cancelled",
                "error": "Request stopped by execution control: tree dollar budget exhausted",
            },
        )

    agent = SimpleNamespace(name="judge", config=SimpleNamespace(model="m", metadata={}),
                            source_id=None, source_is_version=False, execute=execute)
    await run_agent(agent, label="judge", source_app="test", source_feature="news",
                    emit_lifecycle=False)

    assert len(tracker) == 1
    assert tracker[0]["status"] == "cancelled", tracker
    assert "budget" in (tracker[0]["error"] or "")
    assert (tracker[0]["meters"] or {}).get("usd") == pytest.approx(PER_CALL_USD)


@pytest.mark.asyncio
async def test_a_failed_agent_call_child_reports_its_usage_to_the_parent_log(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """agent_call's failure result carries the child's usage, so the parent's
    tool-call log records the child's spend like it does on success."""
    import contextlib

    import matrx_ai._ext as ext
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.agents import executor as agents_executor
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db.agx_manager import AgxDefinition
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    agent_id = "3b1f6c1e-7d0a-4f0e-9a51-2f4c8f0d9e21"
    user_id = "e4687a9c-acf7-469f-aa12-860eb4d948d0"

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        yield

    async def _value(v: Any) -> Any:
        return v

    monkeypatch.setitem(ext._registry, "acting_as_caller", acting_as_caller)
    monkeypatch.setattr(
        AgxDefinition, "load_by_id_or_none",
        classmethod(lambda _cls, _id: _value(SimpleNamespace(
            id=agent_id, created_by=user_id, is_active=True, is_archived=False))),
    )

    class _Child:
        name = "Judge"
        output_schema = None

    monkeypatch.setattr(Agent, "from_agent", classmethod(lambda _cls, *a, **k: _value(_Child())))
    spent = [_billed_call()]

    async def fake_run_agent(_agent: Any, **_kw: Any) -> AgentRunResult:
        return AgentRunResult(success=False, error="boom", error_kind="execution",
                              usage_history=spent)

    monkeypatch.setattr(agents_executor, "run_agent", fake_run_agent)
    token = set_app_context(AppContext(emitter=None, user_id=user_id))
    try:
        result = await agent_call({"agent_id": agent_id}, ToolContext(call_id="call-1"))
    finally:
        clear_app_context(token)

    assert result.success is False
    assert len(result.child_usages) == 1, "the failed child's spend never reached the parent log"


@pytest.mark.asyncio
async def test_a_stopped_agent_tool_child_settles_cancelled(
    monkeypatch: pytest.MonkeyPatch, priced, app_ctx, child_spawner
) -> None:
    """A child the loop stopped (budget / deadline) returns normally with status
    "cancelled" — its spine record must say cancelled, not completed."""
    import matrx_ai.agents.executor as agents_executor
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.tools.agent_tool import execute_agent_tool
    from matrx_ai.tools.models import ToolContext

    async def fake_run_agent(_agent: Any, **_kw: Any) -> AgentRunResult:
        return AgentRunResult(success=True, output="partial", usage_history=[_billed_call()],
                              metadata={"status": "cancelled", "error": "tree budget exhausted"})

    monkeypatch.setattr(agents_executor, "run_agent", fake_run_agent)
    await execute_agent_tool(_agent_tool_def(), {"input": "judge"}, ToolContext(call_id="c"))

    assert len(child_spawner) == 1
    assert child_spawner[0]["cancelled"] is True
    assert len(child_spawner[0]["usage_history"]) == 1


@pytest.mark.asyncio
async def test_a_dict_shaped_stop_error_settles_its_sentence(priced, app_ctx, tracker) -> None:
    from matrx_ai.agents.executor import run_agent

    async def execute(user_input: Any = None, *, max_iterations: Any = None, **_: Any) -> Any:
        return SimpleNamespace(
            output="partial", assistant_response=None,
            config=SimpleNamespace(model="m", metadata={}),
            usage=None, usage_history=[],
            metadata={"status": "cancelled",
                      "error": {"type": "run_stalled", "message": "internal detail",
                                "user_message": "The run stopped making progress."}},
        )

    agent = SimpleNamespace(name="judge", config=SimpleNamespace(model="m", metadata={}),
                            source_id=None, source_is_version=False, execute=execute)
    await run_agent(agent, label="judge", source_app="test", source_feature="news",
                    emit_lifecycle=False)

    assert tracker[0]["status"] == "cancelled"
    assert tracker[0]["error"] == "The run stopped making progress."


@pytest.mark.asyncio
async def test_a_nested_run_agent_keeps_its_own_spend(
    monkeypatch: pytest.MonkeyPatch, priced, app_ctx, no_persist
) -> None:
    """A parent run whose loop launches a child run_agent: each settles ONLY its
    own calls. If the child reused the parent's sink, the child would settle the
    parent's one call instead of its own two."""
    import matrx_ai._ext as ext
    from matrx_ai.agents.executor import run_agent

    settled: dict[str, Any] = {}

    async def open_tracker(*, label: str, source_feature: str) -> Any:
        async def settle(status: str, *, error: Any = None, meters: Any = None) -> None:
            settled[label] = meters or {}

        return settle

    monkeypatch.setattr(ext, "get_internal_run_tracker", lambda: open_tracker)

    def _agent_named(name: str) -> Any:
        a = _agent()
        a.name = name
        return a

    depth = {"n": 0}

    async def fake_inner(*, state: ExecutionState, **_kw: Any) -> Any:
        depth["n"] += 1
        me = depth["n"]
        req = _request()
        state.current_request = req
        state.trigger_position = 0
        state.pre_execution_message_count = 1
        if me == 1:  # the parent: one billed call, then a child run, then it crashes
            req.add_usage(_billed_call())
            await run_agent(_agent_named("child"), label="child", source_app="test",
                            source_feature="news", emit_lifecycle=False)
            raise RuntimeError("parent crashed after its child ran")
        req.add_usage(_billed_call())  # the child: two billed calls, then it crashes
        req.add_usage(_billed_call())
        raise RuntimeError("child crashed")

    monkeypatch.setattr(executor_mod, "_execute_until_complete_inner", fake_inner)

    await run_agent(_agent_named("parent"), label="parent", source_app="test",
                    source_feature="news", emit_lifecycle=False)

    assert settled["child"].get("usd") == pytest.approx(2 * PER_CALL_USD), settled
    assert settled["parent"].get("usd") == pytest.approx(PER_CALL_USD), settled


@pytest.mark.asyncio
async def test_an_incomplete_agent_call_child_reports_its_usage_to_the_parent_log(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A reference-mode child that came back truncated is refused as incomplete —
    and its spend still reaches the parent's tool-call log."""
    import contextlib

    import matrx_ai._ext as ext
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.agents import executor as agents_executor
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db.agx_manager import AgxDefinition
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    agent_id = "3b1f6c1e-7d0a-4f0e-9a51-2f4c8f0d9e21"
    user_id = "e4687a9c-acf7-469f-aa12-860eb4d948d0"

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        yield

    async def _value(v: Any) -> Any:
        return v

    monkeypatch.setitem(ext._registry, "acting_as_caller", acting_as_caller)
    monkeypatch.setattr(
        AgxDefinition, "load_by_id_or_none",
        classmethod(lambda _cls, _id: _value(SimpleNamespace(
            id=agent_id, created_by=user_id, is_active=True, is_archived=False))),
    )

    class _Child:
        name = "Judge"
        output_schema = None

    monkeypatch.setattr(Agent, "from_agent", classmethod(lambda _cls, *a, **k: _value(_Child())))

    async def fake_run_agent(_agent: Any, **_kw: Any) -> AgentRunResult:
        return AgentRunResult(success=True, output="cut off mid", usage_history=[_billed_call()],
                              metadata={"status": "truncated"})

    monkeypatch.setattr(agents_executor, "run_agent", fake_run_agent)
    token = set_app_context(AppContext(emitter=None, user_id=user_id))
    try:
        result = await agent_call({"agent_id": agent_id, "result_mode": "reference"},
                                  ToolContext(call_id="call-1"))
    finally:
        clear_app_context(token)

    assert result.success is False
    assert result.error is not None and result.error.error_type == "agent_incomplete_output"
    assert len(result.child_usages) == 1, "the incomplete child's spend never reached the parent log"
