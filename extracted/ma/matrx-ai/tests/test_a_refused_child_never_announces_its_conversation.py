"""A child refused by its first-turn pass never announces a conversation that will never exist.

Live 2026-11-12 (system_error dbda7ad6, chat 382586b2…): ``agent`` → 'DB Cartographer' without
its required ``task``. The child context opened first and sent the sub_agent INIT naming child
conversation b5d123e3…; the first-turn pass then refused, nothing was written, and the client's
card waited a minute for that conversation and failed with CONVERSATION_NOT_MATERIALIZED.

SUT: the real ``agent_call``. Doubles replace only what it CALLS: the agent loader, the access
check, and ``run_agent`` (the door that opens the child context and sends the INIT) — which must
never be reached when the child's own pre-run checks refuse.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

_USER_ID = "e4687a9c-acf7-469f-aa12-860eb4d948d0"
_ORG_ID = "0a900000-0000-4000-8000-00000000a7a7"
_AGENT_ID = "3b1f6c1e-7d0a-4f0e-9a51-2f4c8f0d9e21"


@pytest.mark.asyncio
async def test_missing_required_inputs_refuse_before_the_child_context_opens(monkeypatch) -> None:
    import matrx_ai._ext as ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.required_variables import RequiredVariablesMissing
    from matrx_ai.db.agx_manager import AgxDefinition
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        yield

    async def _value(v: Any) -> Any:
        return v

    monkeypatch.setitem(ext._registry, "acting_as_caller", acting_as_caller)
    monkeypatch.setattr(
        AgxDefinition,
        "load_by_id_or_none",
        classmethod(
            lambda _cls, _id: _value(
                SimpleNamespace(id=_AGENT_ID, created_by=_USER_ID, is_active=True, is_archived=False)
            )
        ),
    )

    class _ChildAgent:
        name = "DB Cartographer"
        output_schema = None

        async def run_first_turn_pass(self) -> Any:
            raise RequiredVariablesMissing(["task"], agent_name=self.name)

    monkeypatch.setattr(Agent, "from_agent", classmethod(lambda _cls, *a, **k: _value(_ChildAgent())))
    child_runs: list[Any] = []

    async def fake_run_agent(agent: Any, **kwargs: Any) -> Any:
        child_runs.append(kwargs)
        await agent.run_first_turn_pass()  # what execute does inside the opened child context

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    token = set_app_context(AppContext(emitter=None, user_id=_USER_ID, organization_id=_ORG_ID))
    try:
        result = await agent_call(
            {"agent_id": _AGENT_ID, "user_input": "Where do we store company records?"},
            ToolContext(call_id="call-1"),
        )
    finally:
        clear_app_context(token)

    assert child_runs == [], "the child context opened (and announced its conversation) before the refusal"
    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "required_variables_missing"
    assert "task" in result.error.message
