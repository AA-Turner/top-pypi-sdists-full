"""A sub-agent's tool calls are stored naming the agent_call that ran them.

Defect (2026-10-01, PB-01 S14): Compass Dispatch Assistant asked Lane Planner
(via ``agent_call``) for a hub and weather code; Lane Planner called Weather
Desk (its own ``agent_call``) and reasoned about the answer. The live transcript
showed that nested work; after a reload it was gone, because every
``chat.tool_call`` row the child wrote had ``parent_call_id`` NULL — nothing
linked Lane Planner's call to Weather Desk back to the card that ran Lane
Planner. Arman's ruling the same morning: nested work is SHOWN after a reload,
the same as live.

The behaviour proven here, on the INSERT payloads the logger queues for
``chat.tool_call`` (the rows that get stored):
  1. a child's tool call names the parent's agent_call ROW as ``parent_call_id``;
  2. depth is kept — the grandchild's call names the CHILD's agent_call row;
  3. the parent's own later calls carry no parent (the binding never leaks);
  4. every agent_call answer names the conversation the child ran in.
Plus a structural guard: every logger INSERT path stamps the parent.
"""

from __future__ import annotations

import ast
import textwrap
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_utils.source_guard import stable_source

import matrx_ai.tools.logger as logger_mod
from matrx_ai.tools.logger import ToolExecutionLogger

USER = "5e1c0a11-0000-4000-8000-000000000001"
PARENT_CONV = "5e1c0a11-0000-4000-8000-0000000000c0"
LANE_PLANNER = "d8f7402e-9cd3-43f9-8302-aa78ffa24c1f"
WEATHER_DESK = "5e1c0a11-0000-4000-8000-0000000000a2"


@pytest.fixture
def stored(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    """Capture every chat.tool_call INSERT the logger would store."""
    rows: list[dict[str, Any]] = []

    async def _no_parents(**_kw: Any) -> None:
        return None

    monkeypatch.setattr(logger_mod, "_should_persist_tool_call", lambda: True)
    monkeypatch.setattr(logger_mod, "_ensure_tool_call_parents", _no_parents)
    monkeypatch.setattr(logger_mod, "_get_coordinator", lambda: object())
    monkeypatch.setattr(logger_mod, "_queue_tool_call_create", lambda **kw: rows.append(kw))
    monkeypatch.setattr(logger_mod, "stamp_row_owner", lambda data, user_id: None)
    monkeypatch.setattr(logger_mod, "try_get_tracker", lambda: None, raising=False)
    return rows


async def _log_call(tool_name: str, call_id: str) -> str:
    """What the executor does when a model calls a tool: log_started."""
    from matrx_ai.tools.models import ToolContext

    tool_def = SimpleNamespace(name=tool_name, tool_type=SimpleNamespace(value="local"))
    return await ToolExecutionLogger().log_started(
        ToolContext(call_id=call_id, tool_name=tool_name), tool_def, {"q": "Mexico City"}
    )


@pytest.fixture
def agents(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Lane Planner calls Weather Desk; Weather Desk calls one plain tool."""
    import importlib

    from matrx_connect.context.app_context import get_app_context, set_app_context

    agent_call_mod = importlib.import_module("matrx_ai.tools.implementations.agent_call")
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    bag: dict[str, Any] = {"row_ids": {}}

    async def load_agent(agent_id: str, _ctx: Any) -> Any:
        return SimpleNamespace(id=agent_id, is_active=True, is_archived=False)

    monkeypatch.setattr(agent_call_mod, "load_agent_as_the_person", load_agent)

    class _Agent:
        output_schema = None

        def __init__(self, agent_id: str) -> None:
            self.id = agent_id
            self.name = "Lane Planner" if agent_id == LANE_PLANNER else "Weather Desk"
            self.config = SimpleNamespace(messages=[])

    async def from_agent(_cls: Any, agent_id: str, **_kw: Any) -> _Agent:
        return _Agent(agent_id)

    monkeypatch.setattr(Agent, "from_agent", classmethod(from_agent))

    async def run_agent(agent: _Agent, **_kw: Any) -> AgentRunResult:
        # The child runs in its own conversation, as run_agent's fork does.
        parent_ctx = get_app_context()
        child_conv = f"{agent.id[:-2]}cc"
        set_app_context(parent_ctx.with_overrides(conversation_id=child_conv))
        try:
            if agent.id == LANE_PLANNER:
                # Lane Planner's own agent_call to Weather Desk.
                bag["row_ids"]["lane_planner_agent_call"] = await _log_call(
                    "agent_call", "call-lane-to-weather"
                )
                await agent_call(
                    {"agent_id": WEATHER_DESK, "user_input": "Weather code for MEX?"},
                    ToolContext(call_id="call-lane-to-weather", tool_name="agent_call"),
                )
            else:
                bag["row_ids"]["weather_lookup"] = await _log_call(
                    "weather_lookup", "call-weather-lookup"
                )
        finally:
            set_app_context(parent_ctx)
        return AgentRunResult(
            success=True,
            output=f"{agent.name} answered.",
            metadata={"conversation_id": child_conv},
        )

    monkeypatch.setattr(executor_mod, "run_agent", run_agent)
    return bag


@pytest.mark.asyncio
async def test_nested_child_rows_name_the_agent_call_that_ran_them(stored, agents):
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    token = set_app_context(AppContext(emitter=None, user_id=USER, conversation_id=PARENT_CONV))
    try:
        dispatch_row = await _log_call("agent_call", "call-dispatch-to-lane")
        result = await agent_call(
            {"agent_id": LANE_PLANNER, "user_input": "Hub and weather code for Mexico City"},
            ToolContext(call_id="call-dispatch-to-lane", tool_name="agent_call"),
        )
        after_row = await _log_call("send_reply", "call-parent-after")
    finally:
        clear_app_context(token)

    assert result.success, result
    by_id = {row["id"]: row for row in stored}
    lane_row = by_id[agents["row_ids"]["lane_planner_agent_call"]]
    weather_row = by_id[agents["row_ids"]["weather_lookup"]]

    assert by_id[dispatch_row].get("parent_call_id") is None
    assert lane_row.get("parent_call_id") == dispatch_row, (
        "Lane Planner's own agent_call must be stored naming the Dispatch card's row"
    )
    assert weather_row.get("parent_call_id") == lane_row["id"], (
        "depth: Weather Desk's call names Lane Planner's agent_call, not the top call"
    )
    assert by_id[after_row].get("parent_call_id") is None, (
        "the parent's own later call must not inherit the child's binding"
    )
    assert result.output["child_conversation_id"].endswith("cc")


def test_every_tool_call_insert_path_stamps_its_parent():
    tree = ast.parse(textwrap.dedent(stable_source(ToolExecutionLogger)))
    inserting: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            continue
        called = {
            n.func.id if isinstance(n.func, ast.Name) else getattr(n.func, "attr", "")
            for n in ast.walk(node)
            if isinstance(n, ast.Call)
        }
        if called & {"_queue_tool_call_create", "log_tool_call_start"}:
            inserting.append(node.name)
            assert "_stamp_parent_call" in called, (
                f"ToolExecutionLogger.{node.name} INSERTs a chat.tool_call row without "
                "_stamp_parent_call — a sub-agent's call written there loses its "
                "parent and disappears from the reloaded nesting."
            )
    assert {"log_started", "log_rejected"} <= set(inserting), inserting
