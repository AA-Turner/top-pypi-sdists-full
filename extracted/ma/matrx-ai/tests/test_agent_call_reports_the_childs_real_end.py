"""agent_call hands the caller the child's REAL end state, and an unfinished child is never success.

Before (research-tool-repair E1/D4): an inline agent_call returned ``success=True`` with
``result=""`` when the child produced nothing, reported a paused/truncated/suspended child as
success unless ``require_complete_output`` was set, and dressed an empty answer from a run cut
off mid-tool-call as a sentence inside a successful result.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any

import pytest


async def _async_value(value: Any) -> Any:
    return value


async def _run_inline(monkeypatch: pytest.MonkeyPatch, child: Any) -> Any:
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    import matrx_ai._ext as ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.db.agx_manager import AgxDefinition
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx=None):
        yield

    monkeypatch.setitem(ext._registry, "acting_as_caller", acting_as_caller)
    user_id = "11111111-1111-4111-8111-111111111111"
    agent_id = "22222222-2222-4222-8222-222222222222"
    monkeypatch.setattr(
        AgxDefinition,
        "load_by_id_or_none",
        classmethod(
            lambda _cls, _agent_id: _async_value(
                SimpleNamespace(id=agent_id, created_by=user_id, is_active=True, is_archived=False)
            )
        ),
    )

    class FakeAgent:
        name = "child"
        output_schema = None
        async def run_first_turn_pass(self):  # the real pass: present on every Agent
            return self

    monkeypatch.setattr(
        Agent, "from_agent", classmethod(lambda _cls, *_a, **_k: _async_value(FakeAgent()))
    )

    async def fake_run_agent(_agent, **_kwargs):
        return child

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    token = set_app_context(
        AppContext(emitter=None, user_id=user_id, organization_id="0a900000-0000-4000-8000-00000000a7a7")
    )
    try:
        return await agent_call({"agent_id": agent_id}, ToolContext(call_id="call-1"))
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_an_empty_child_is_not_success(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.agents.executor import AgentRunResult

    result = await _run_inline(
        monkeypatch, AgentRunResult(success=True, output="", metadata={"status": "completed"})
    )
    assert result.success is False
    assert result.error.error_type == "agent_incomplete_output"
    assert result.output["child_end"]["empty"] is True
    assert result.output["child_end"]["status"] == "completed"
    assert "no answer" in result.output["child_end"]["reason"]


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["paused", "truncated", "suspended_awaiting_client"])
async def test_an_unfinished_child_is_not_success_even_inline(
    monkeypatch: pytest.MonkeyPatch, status: str
) -> None:
    from matrx_ai.agents.executor import AgentRunResult

    result = await _run_inline(
        monkeypatch, AgentRunResult(success=True, output="half an answer", metadata={"status": status})
    )
    assert result.success is False
    assert result.error.error_type == "agent_incomplete_output"
    assert result.output["child_end"]["status"] == status
    assert result.output["child_end"]["reason"]
    # What the child did get to still reaches the caller, beside the end state.
    assert result.output["result"] == "half an answer"


@pytest.mark.asyncio
async def test_a_run_cut_off_mid_tool_call_fails_naming_its_last_action(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.agents.executor import AgentRunResult

    child = AgentRunResult(
        success=True,
        output="",
        metadata={"status": "completed"},
        stopped_on_tool_calls=[{"name": "shell_execute", "arguments": {"command": "git log -1"}}],
    )
    result = await _run_inline(monkeypatch, child)
    assert result.success is False
    assert result.output["result"] == ""
    assert result.output["child_end"]["last_actions"] == ["shell_execute(command='git log -1')"]
    assert "last action: shell_execute" in result.error.message


@pytest.mark.asyncio
async def test_a_finished_child_carries_its_end_state(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.agents.executor import AgentRunResult

    result = await _run_inline(
        monkeypatch, AgentRunResult(success=True, output="The answer.", metadata={"status": "completed"})
    )
    assert result.success is True
    assert result.output["result"] == "The answer."
    assert result.output["child_end"] == {"status": "completed", "empty": False}


@pytest.mark.asyncio
async def test_a_media_only_child_is_a_finished_answer(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.agents.executor import AgentRunResult

    child = AgentRunResult(
        success=True,
        output="",
        metadata={"status": "completed"},
        media=[{"file_id": "33333333-3333-4333-8333-333333333333", "mime_type": "image/png", "kind": "image"}],
    )
    result = await _run_inline(monkeypatch, child)
    assert result.success is True
    assert result.output["child_end"]["empty"] is False


@pytest.mark.asyncio
async def test_an_unreadable_agent_list_carries_its_cause(monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib

    mod = importlib.import_module("matrx_ai.tools.implementations.agent_call")
    from matrx_ai.utils.carried_failure import carried_exception

    boom = RuntimeError("pool exhausted")

    async def broken(_app_ctx):
        raise boom

    monkeypatch.setattr(mod, "reachable_agents", broken)
    message = await mod.unknown_agent_refusal("nobody", SimpleNamespace(organization_id=None))
    assert "RuntimeError: pool exhausted" in message
    assert carried_exception(message) is boom
