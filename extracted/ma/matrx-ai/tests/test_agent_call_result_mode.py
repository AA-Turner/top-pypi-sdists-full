from __future__ import annotations

from types import SimpleNamespace

import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["paused", "suspended_awaiting_client", "truncated"])
async def test_agent_call_reference_never_stores_incomplete_child(
    monkeypatch: pytest.MonkeyPatch,
    status: str,
) -> None:
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    import matrx_ai._ext as ext
    from matrx_ai.agents import executor as executor_mod
    from matrx_ai.agents.definition import Agent
    from matrx_ai.agents.executor import AgentRunResult
    from matrx_ai.db.agx_manager import AgxDefinition
    from matrx_ai.tools.implementations.agent_call import agent_call
    from matrx_ai.tools.models import ToolContext

    user_id = "11111111-1111-4111-8111-111111111111"
    agent_id = "22222222-2222-4222-8222-222222222222"
    monkeypatch.setattr(
        AgxDefinition,
        "load_by_id_or_none",
        classmethod(
            lambda _cls, _agent_id: _async_value(
                SimpleNamespace(
                    id=agent_id,
                    created_by=user_id,
                    is_active=True,
                    is_archived=False,
                )
            )
        ),
    )

    class FakeAgent:
        name = "child"
        output_schema = None

    monkeypatch.setattr(
        Agent,
        "from_agent",
        classmethod(lambda _cls, *_args, **_kwargs: _async_value(FakeAgent())),
    )
    captured: dict[str, object] = {}

    async def fake_run_agent(_agent, **kwargs):
        captured.update(kwargs)
        return AgentRunResult(
            success=True,
            output="partial child output",
            metadata={"status": status},
        )

    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    writes: list[dict] = []

    async def writer(**kwargs):
        writes.append(kwargs)
        return {"key": "must-not-exist"}

    before = ext._registry.get("conversation_value_writer")
    ext.configure_ext(conversation_value_writer=writer)
    token = set_app_context(AppContext(emitter=None, user_id=user_id))
    try:
        result = await agent_call(
            {"agent_id": agent_id, "result_mode": "reference"},
            ToolContext(call_id="call-1"),
        )
    finally:
        clear_app_context(token)
        if before is None:
            ext._registry.pop("conversation_value_writer", None)
        else:
            ext._registry["conversation_value_writer"] = before

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "agent_incomplete_output"
    assert writes == []
    assert captured["require_complete_output"] is True
    assert captured["allow_client_delegation"] is False


async def _async_value(value):
    return value
