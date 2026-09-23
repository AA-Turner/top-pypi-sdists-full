"""The per-subtree execution budget, measured on the REAL loop.

Every test here drives ``execute_until_complete`` / ``execute_ai_request`` with
the mock provider and a real registered tool through the client-host seams —
the same funnel a live request takes. Nothing about the stop decision is
stubbed: the loop really polls, really finishes the tool it is holding, and
really persists what it produced.

What each test is FOR (delete the production line it pins and it goes red):

* the child's clock stops the child AT a boundary — never mid-tool, and never
  by throwing the paid-for work away;
* the child's iteration ceiling really reaches ``execute_ai_request``;
* the TREE-ROOT layer still ends everything, because the subtree check now runs
  in front of it;
* a child's budget never bounds its parent — the failure that would make this
  whole mechanism worse than useless.
"""

from __future__ import annotations

import asyncio
import uuid
from typing import Any

import pytest

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_execute_with_store import (  # noqa: E402
    _MOCK_MODEL,
    FakeEmitter,
    InMemoryStore,
    StaticCatalog,
)

#: How long the slow tool blocks. Must comfortably exceed the budget below so
#: the second boundary is always past it — a flaky budget test is worthless.
SLOW_TOOL_SECONDS = 2.0
#: The child's window. Fresh at the first boundary, gone by the second.
CHILD_BUDGET_SECONDS = 1


@pytest.fixture
def slow_tool_registered():
    """A real local tool that takes longer than the budget it runs under."""
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    saved_tools = dict(registry._tools)
    saved_by_id = dict(registry._tools_by_id)
    saved_loaded = registry._loaded

    calls: list[str] = []

    async def _slow(args: dict[str, Any], ctx: Any) -> dict[str, Any]:
        calls.append("started")
        await asyncio.sleep(SLOW_TOOL_SECONDS)
        calls.append("finished")
        return {"slow": "ran to completion", "args": dict(args or {})}

    registry.register_local(
        "subtree_budget_slow_tool",
        _slow,
        description="a tool that outlives the budget it runs under",
        parameters={"anything": {"type": "string", "description": "free"}},
    )
    registry._loaded = True
    try:
        yield calls
    finally:
        registry._tools.clear()
        registry._tools.update(saved_tools)
        registry._tools_by_id.clear()
        registry._tools_by_id.update(saved_by_id)
        registry._loaded = saved_loaded


@pytest.fixture
def fast_tool_registered():
    """A real local tool that returns instantly — for counting ROUNDS, where
    the clock must not be what ends the run."""
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    saved_tools = dict(registry._tools)
    saved_by_id = dict(registry._tools_by_id)
    saved_loaded = registry._loaded

    calls: list[str] = []

    async def _fast(args: dict[str, Any], ctx: Any) -> dict[str, Any]:
        calls.append("finished")
        return {"fast": "ran", "args": dict(args or {})}

    registry.register_local(
        "subtree_budget_fast_tool",
        _fast,
        description="an instant tool for counting rounds",
        parameters={"anything": {"type": "string", "description": "free"}},
    )
    registry._loaded = True
    try:
        yield calls
    finally:
        registry._tools.clear()
        registry._tools.update(saved_tools)
        registry._tools_by_id.clear()
        registry._tools_by_id.update(saved_by_id)
        registry._loaded = saved_loaded


def _configure(store: InMemoryStore) -> None:
    configure_ext(
        conversation_store=store,
        model_catalog=StaticCatalog([_MOCK_MODEL]),
        api_key_resolver=lambda name: "not-a-real-key",
    )


def _set_context(emitter: FakeEmitter, metadata: dict[str, Any] | None = None) -> str:
    from matrx_connect.context.app_context import AppContext, set_app_context

    request_id = str(uuid.uuid4())
    set_app_context(
        AppContext(
            emitter=emitter,
            user_id=str(uuid.uuid4()),
            request_id=request_id,
            conversation_id=str(uuid.uuid4()),
            is_internal_agent=True,
            store=True,
            source_app="client_host_tests",
            source_feature="test",
            metadata=dict(metadata or {}),
        )
    )
    return request_id


def _config(tool_name: str, *, text: str = "done") -> Any:
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage

    return UnifiedConfig(
        model="mock-model",
        tools=[tool_name],
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="go")])]
        ),
        metadata={
            "mock": {
                "latency_ms": 1,
                "ttft_ms": 0,
                "chunks": 1,
                "mode": "text",
                "text": text,
                "tool_calls": [{"name": tool_name, "arguments": {"anything": "x"}}],
            }
        },
    )


# ── 1. The clock stops the child at a boundary, keeping the finished tool ────


@pytest.mark.asyncio
async def test_a_child_time_budget_stops_at_a_boundary_and_keeps_the_paid_work(
    slow_tool_registered,
):
    """A 1s budget with a 2s tool: the tool RUNS TO COMPLETION, and the loop
    stops at the next boundary carrying everything it produced.

    Red without the subtree poll: the loop reaches the second boundary with no
    budget to check, calls the provider again and completes normally.
    """
    from matrx_ai.orchestrator.executor import execute_until_complete
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.orchestrator.subtree_budget import (
        SUBTREE_BUDGET_STOP_MARKER,
        with_subtree_budget,
    )
    from matrx_ai.providers.unified_client import UnifiedAIClient

    store = InMemoryStore()
    _configure(store)
    emitter = FakeEmitter()
    request_id = _set_context(
        emitter,
        with_subtree_budget({}, seconds=CHILD_BUDGET_SECONDS, label="'Senior Staff' run"),
    )

    completed = await execute_until_complete(
        AIMatrixRequest(
            conversation_id=str(uuid.uuid4()),
            config=_config("subtree_budget_slow_tool"),
            request_id=request_id,
        ),
        UnifiedAIClient(),
        6,  # a ceiling far above where the budget should bite
    )

    metadata = completed.metadata or {}
    assert metadata.get("status") == "cancelled", (
        "the subtree budget did not stop the loop at a boundary; the run ended as "
        f"{metadata.get('status')!r}"
    )
    assert SUBTREE_BUDGET_STOP_MARKER in str(metadata.get("error") or ""), (
        "the stop was not attributed to the subtree budget, so a caller cannot tell "
        f"a bounded answer from a cancel: {metadata.get('error')!r}"
    )

    # 🚨 The whole point: the tool that was in flight FINISHED. A budget that
    # cancels mid-tool destroys work already paid for.
    assert slow_tool_registered == ["started", "finished"], (
        f"the slow tool did not run to completion: {slow_tool_registered}"
    )
    rows = [
        row
        for row in store.tool_rows.values()
        if row.get("tool_name") == "subtree_budget_slow_tool"
    ]
    assert rows and all(row.get("status") == "completed" for row in rows), (
        f"the in-flight tool was not recorded as completed: {rows}"
    )
    assert store.completed, "a bounded run must still persist what it produced"


# ── 2. The iteration ceiling reaches the one execution funnel ────────────────


@pytest.mark.asyncio
async def test_a_child_iteration_ceiling_of_three_stops_at_three(
    fast_tool_registered, monkeypatch
):
    """``execute_ai_request(max_iterations=3)`` really bounds the loop at 3.

    The mock normally stops asking for tools once a tool result is in history;
    here that brake is released so the loop would run to the library default,
    and only the ceiling can end it.
    """
    from matrx_ai.orchestrator.executor import execute_ai_request
    from matrx_ai.providers.mock.mock_api import MockChat

    # Release the mock's own brake so it asks for the tool EVERY turn: without
    # this the run ends on its own after two rounds and the ceiling is never
    # what stopped it.
    monkeypatch.setattr(
        MockChat, "_history_has_tool_result", staticmethod(lambda unified_config: False)
    )

    # ...and vary the arguments each round, or the platform's own triplicate
    # loop guard ends the run at three identical calls and we would be pinning
    # THAT, not the ceiling.
    round_counter = {"n": 0}
    original_raw_spec = MockChat._raw_spec

    def _varying_raw_spec(unified_config):
        raw = dict(original_raw_spec(unified_config) or {})
        round_counter["n"] += 1
        raw["tool_calls"] = [
            {
                "name": "subtree_budget_fast_tool",
                "arguments": {"anything": f"round-{round_counter['n']}"},
            }
        ]
        return raw

    monkeypatch.setattr(MockChat, "_raw_spec", staticmethod(_varying_raw_spec))

    store = InMemoryStore()
    _configure(store)
    _set_context(FakeEmitter())

    completed = await execute_ai_request(
        _config("subtree_budget_fast_tool"),
        max_iterations=3,
    )

    metadata = completed.metadata or {}
    assert metadata.get("status") == "max_iterations_exceeded", (
        f"the ceiling did not end the loop; status was {metadata.get('status')!r}"
    )
    assert metadata.get("max_iterations") == 3
    assert fast_tool_registered.count("finished") == 3, (
        "the loop did not stop at exactly three rounds: "
        f"{fast_tool_registered.count('finished')} tool completions"
    )


@pytest.mark.asyncio
async def test_agent_execute_forwards_its_ceiling_to_the_one_funnel(monkeypatch):
    """``Agent.execute(max_iterations=...)`` is the only seam between
    ``agent_call`` and the funnel. If it drops the value, the child desk runs
    to the library default and the budget is a lie."""
    import matrx_ai.agents.definition as definition_mod
    from matrx_ai.config import MessageList, UnifiedConfig

    seen: dict[str, Any] = {}

    async def _fake_execute_ai_request(config, **kwargs):
        seen.update(kwargs)
        raise RuntimeError("stop here — the plumb is what is under test")

    monkeypatch.setattr(definition_mod, "execute_ai_request", _fake_execute_ai_request)

    agent = definition_mod.Agent(
        UnifiedConfig(model="mock-model", messages=MessageList()), name="probe"
    )
    with pytest.raises(RuntimeError):
        await agent.execute(user_input="go", max_iterations=3)
    assert seen.get("max_iterations") == 3, (
        f"the ceiling never reached execute_ai_request: {seen}"
    )


# ── 3. The tree-root layer still ends everything ─────────────────────────────


@pytest.mark.asyncio
async def test_the_root_control_still_ends_everything(slow_tool_registered):
    """The subtree poll runs IN FRONT of the spine control check. If it ever
    short-circuits that check, a POST /cancel and the tree budget go dead."""
    from matrx_ai.orchestrator.executor import execute_until_complete
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.orchestrator.subtree_budget import SUBTREE_BUDGET_STOP_MARKER
    from matrx_ai.providers.unified_client import UnifiedAIClient

    store = InMemoryStore()
    _configure(store)
    emitter = FakeEmitter()
    # No subtree budget at all — only the root layer may speak.
    request_id = _set_context(emitter, {})

    async def _root_says_stop() -> str:
        return "deadline passed — tree deadline reached"

    configure_ext(spine_control_check=_root_says_stop)

    completed = await execute_until_complete(
        AIMatrixRequest(
            conversation_id=str(uuid.uuid4()),
            config=_config("subtree_budget_slow_tool"),
            request_id=request_id,
        ),
        UnifiedAIClient(),
        6,
    )

    metadata = completed.metadata or {}
    assert metadata.get("status") == "cancelled"
    assert "deadline passed" in str(metadata.get("error") or "")
    assert SUBTREE_BUDGET_STOP_MARKER not in str(metadata.get("error") or "")
    assert slow_tool_registered == [], (
        "the root deadline should stop the very first boundary, before any tool ran"
    )


# ── 4. A child's budget never bounds its parent ──────────────────────────────


def test_a_child_budget_never_bounds_its_parent_or_its_siblings():
    """``with_subtree_budget`` must never mutate the metadata it is handed.

    Sibling tool calls in one batch share the parent's metadata dict
    (``asyncio.gather``). An in-place append would bind every sibling — and the
    parent loop itself — to a clock that was only ever the one child's.
    """
    import time

    from matrx_ai.orchestrator.subtree_budget import (
        active_budgets,
        subtree_stop_reason,
        with_subtree_budget,
    )

    parent = {"existing": "value"}
    child = with_subtree_budget(parent, seconds=1, label="'Senior Staff' run")

    assert parent == {"existing": "value"}, "the parent's metadata was mutated"
    assert active_budgets(parent) == ()
    assert len(active_budgets(child)) == 1

    later = time.time() + 5
    assert subtree_stop_reason(child, now=later) is not None
    assert subtree_stop_reason(parent, now=later) is None, (
        "an expired child budget stopped the parent — the exact failure this "
        "mechanism must never cause"
    )


def test_nested_budgets_let_the_earliest_expiry_win():
    """A grandchild carries its parent's clock as well as its own, so an outer
    budget can stop an inner run whose own window still has time on it."""
    import time

    from matrx_ai.orchestrator.subtree_budget import subtree_stop_reason, with_subtree_budget

    outer = with_subtree_budget({}, seconds=1, label="outer desk")
    inner = with_subtree_budget(outer, seconds=600, label="inner desk")

    reason = subtree_stop_reason(inner, now=time.time() + 5)
    assert reason is not None and "outer desk" in reason, (
        f"the outer budget did not reach the nested run: {reason!r}"
    )


def test_a_budget_too_small_to_run_is_refused_not_silently_honored():
    """A zero/negative window would stop a run before its first call. Refuse it
    where it is written, not as a mystery empty answer later."""
    from matrx_ai.orchestrator.subtree_budget import with_subtree_budget

    with pytest.raises(ValueError):
        with_subtree_budget({}, seconds=0, label="impossible desk")
