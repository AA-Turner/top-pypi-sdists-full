"""A model-started child run never arrives empty — it is refused, saying what to send.

Live 2026-10-16 07:56Z–08:00Z (PB-02; chat.tool_call rows in conversations
96bb302f…, 9f2ba6db…, a668ef2a…): Compass Mandate Desk called Lane Planner with
``agent_call({"agent_id": …, "variables": {"destination_city": "Mexico City"}})``.
Lane Planner has a system prompt only — no authored turn, no declared
variables — so the child reached the send boundary with nothing to answer
(``empty_conversation``) and the tool told the model to "check the agent's
variables and configuration". The retry passed ``user_input`` and succeeded.

SUTs: ``agent_call`` and ``execute_agent_tool`` (the two doors where a MODEL
composes the arguments of a child run). Doubles replace only what they CALL:
the agent loader, the access check, and ``run_agent`` (recording whether a
child ran at all). The child Agent itself is real.

Breaks named: a door that starts the child with no turn and no input; a
refusal that does not name the argument to send or the undeclared variables;
a late ``empty_conversation`` from the send boundary reported as "check the
configuration".
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"
_AGENT_ID = "d8f7402e-9cd3-43f9-8302-aa78ffa24c1f"
_LANE_PLANNER_PROMPT = (
    "You are the Lane Planner. You are given a destination city. Reply with the hub."
)


def _lane_planner(*, with_opening_turn: bool = False) -> Any:
    from matrx_ai.agents.definition import Agent
    from matrx_ai.config import MessageList, UnifiedConfig
    from matrx_ai.config.message_config import UnifiedMessage

    messages = MessageList()
    messages.append(UnifiedMessage.from_dict({"role": "system", "content": _LANE_PLANNER_PROMPT}))
    if with_opening_turn:
        messages.append(UnifiedMessage.from_dict({"role": "user", "content": "Plan the lane."}))
    agent = Agent(UnifiedConfig(model="claude-haiku-5-5", messages=messages), name="Lane Planner")
    agent.declares_variables = True  # a saved agent: its (empty) definitions ARE its declaration
    return agent


async def _value(v: Any) -> Any:
    return v


@pytest.fixture
def child_runs(monkeypatch) -> list[dict[str, Any]]:
    """Wire agent_call's loader + access check; record every child run."""
    import matrx_ai._ext as ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db.agx_manager import AgxDefinition

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        yield

    monkeypatch.setitem(ext._registry, "acting_as_caller", acting_as_caller)
    monkeypatch.setattr(
        AgxDefinition,
        "load_by_id_or_none",
        classmethod(
            lambda _cls, _id: _value(
                SimpleNamespace(
                    id=_AGENT_ID, created_by=_USER_ID, is_active=True, is_archived=False
                )
            )
        ),
    )
    runs: list[dict[str, Any]] = []

    async def fake_run_agent(_agent: Any, **kwargs: Any) -> AgentRunResult:
        runs.append(kwargs)
        return AgentRunResult(success=True, output="hub: Los Angeles", metadata={})

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    return runs


def _use_agent(monkeypatch, agent: Any) -> None:
    from matrx_ai.agents.definition import Agent

    monkeypatch.setattr(Agent, "from_agent", classmethod(lambda _cls, *a, **k: _value(agent)))


async def _call(args: dict[str, Any]) -> Any:
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    token = set_app_context(AppContext(emitter=None, user_id=_USER_ID))
    try:
        return await agent_call(args, ToolContext(call_id="call-1"))
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_variables_only_call_to_an_agent_with_no_turn_is_refused_before_it_runs(
    monkeypatch, child_runs
) -> None:
    _use_agent(monkeypatch, _lane_planner())
    result = await _call({"agent_id": _AGENT_ID, "variables": {"destination_city": "Mexico City"}})

    assert child_runs == [], "the child ran with nothing to answer"
    assert result.success is False
    error = result.error
    assert error.error_type == "missing_user_input"
    model_view = error.to_agent_message()
    assert "user_input" in model_view  # what to send
    assert "destination_city" in model_view  # what it sent that filled nothing
    assert "Lane Planner" in model_view


@pytest.mark.asyncio
async def test_the_same_call_with_user_input_runs(monkeypatch, child_runs) -> None:
    _use_agent(monkeypatch, _lane_planner())
    result = await _call({"agent_id": _AGENT_ID, "user_input": "Mexico City"})

    assert result.success is True
    assert [r["user_input"] for r in child_runs] == ["Mexico City"]


@pytest.mark.asyncio
async def test_an_agent_with_its_own_opening_turn_runs_without_user_input(
    monkeypatch, child_runs
) -> None:
    _use_agent(monkeypatch, _lane_planner(with_opening_turn=True))
    result = await _call({"agent_id": _AGENT_ID})

    assert result.success is True
    assert len(child_runs) == 1


@pytest.mark.asyncio
async def test_a_late_empty_conversation_refusal_names_what_to_send(monkeypatch) -> None:
    """An authored turn the variables filled with nothing: the send boundary refuses
    it (no spend) — the tool error must still tell the model to send user_input."""
    import matrx_ai._ext as ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.config.send_boundary import EMPTY_CONVERSATION_USER_MESSAGE
    from matrx_ai.db.agx_manager import AgxDefinition

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        yield

    monkeypatch.setitem(ext._registry, "acting_as_caller", acting_as_caller)
    monkeypatch.setattr(
        AgxDefinition,
        "load_by_id_or_none",
        classmethod(
            lambda _cls, _id: _value(
                SimpleNamespace(
                    id=_AGENT_ID, created_by=_USER_ID, is_active=True, is_archived=False
                )
            )
        ),
    )

    async def refused_run_agent(_agent: Any, **kwargs: Any) -> AgentRunResult:
        return AgentRunResult(
            success=False,
            error=EMPTY_CONVERSATION_USER_MESSAGE,
            error_kind="execution",
            metadata={"status": "failed", "error_type": "empty_conversation"},
        )

    monkeypatch.setattr(executor_mod, "run_agent", refused_run_agent)
    _use_agent(monkeypatch, _lane_planner(with_opening_turn=True))
    result = await _call({"agent_id": _AGENT_ID, "variables": {"destination_city": ""}})

    assert result.success is False
    model_view = result.error.to_agent_message()
    assert "user_input" in model_view
    assert "Check the agent's variables and configuration" not in model_view


@pytest.mark.asyncio
async def test_an_agent_tool_with_no_turn_and_no_input_is_refused_before_it_runs(
    monkeypatch,
) -> None:
    """Sibling door: a saved agent projected as a tool (``execute_agent_tool``)."""
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.tools.agent_projection import AUTO_INPUT_DESCRIPTION
    from matrx_ai.tools.agent_tool import execute_agent_tool
    from matrx_ai.tools.models import ToolContext

    runs: list[Any] = []

    async def fake_run_agent(_agent: Any, **kwargs: Any) -> AgentRunResult:
        runs.append(kwargs)
        return AgentRunResult(success=True, output="hub: Los Angeles", metadata={})

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    agent = _lane_planner()
    monkeypatch.setattr(Agent, "from_agent", classmethod(lambda _cls, *a, **k: _value(agent)))
    tool_def = SimpleNamespace(
        name="custom_tool_1",
        prompt_id=_AGENT_ID,
        prompt_is_version=False,
        result_mode="inline",
        handoff_terminal=False,
        parameters={"input": {"type": "string", "description": AUTO_INPUT_DESCRIPTION}},
    )

    token = set_app_context(AppContext(emitter=None, user_id=_USER_ID))
    try:
        result = await execute_agent_tool(
            tool_def,  # type: ignore[arg-type]
            {"destination_city": "Mexico City"},
            ToolContext(call_id="call-2"),
        )
    finally:
        clear_app_context(token)

    assert runs == [], "the child ran with nothing to answer"
    assert result.success is False
    model_view = result.error.to_agent_message()
    assert "input" in model_view
    assert "destination_city" in model_view
