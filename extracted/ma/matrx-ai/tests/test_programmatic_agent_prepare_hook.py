from __future__ import annotations

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai import _ext
from matrx_ai.agents.definition import Agent
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage


class _Prepared(RuntimeError):
    pass


@pytest.mark.asyncio
async def test_direct_agent_execute_crosses_host_resource_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: dict[str, object] = {}

    async def prepare_hook(*, agent, app_ctx):
        seen["agent"] = agent
        seen["ctx"] = app_ctx
        seen["variables_applied"] = agent._variables_applied
        raise _Prepared

    monkeypatch.setitem(_ext._registry, "programmatic_agent_prepare_hook", prepare_hook)

    agent = Agent(
        config=UnifiedConfig(
            model="test-model",
            messages=MessageList(
                _messages=[
                    UnifiedMessage(
                        role="user",
                        content=[TextContent(text="Use {{pdf_file}}")],
                    )
                ]
            ),
        ),
        variable_defaults={
            "pdf_file": AgentVariable(
                name="pdf_file",
                default_value="550e8400-e29b-41d4-a716-446655440000",
                custom_component={"type": "document"},
            )
        },
        auto_tools_disabled=True,
    )
    agent.source_id = "4185e955-0f4e-4faa-b63c-704bb876c85f"
    ctx = AppContext(
        emitter=SilentEmitter(),
        user_id="user-1",
        is_authenticated=True,
        auth_type="token",
    )
    token = set_app_context(ctx)
    try:
        with pytest.raises(_Prepared):
            await agent.execute(user_input="Inspect the document")
    finally:
        clear_app_context(token)

    assert seen["agent"] is agent
    assert seen["agent"].auto_tools_disabled is True
    assert seen["ctx"] is ctx
    assert seen["variables_applied"] is True
