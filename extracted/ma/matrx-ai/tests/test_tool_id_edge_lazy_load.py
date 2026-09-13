"""Agent.execute owns the readiness of the registry it resolves tool ids with.

A DB-loaded agent carries ``agx_agent.tools`` as UUIDs. ``canonical_tool_names``
passes an id through untouched when the registry does not recognize it, so a
process that never called ``initialize_tool_system`` (a worker lane, a script,
an MCP host) sent raw UUIDs to the provider boundary, where the guard refused
them — reported as "An unexpected Anthropic error occurred" (commerce-intake
research mandate, live 2026-08-30). The direct-execution edge now loads the
registry before resolving, and only when a UUID is actually present.
"""

from __future__ import annotations

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai import _ext
from matrx_ai.agents import definition as definition_module
from matrx_ai.agents.definition import Agent
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.tools.registry import ToolRegistry

WEB_TOOL_ID = "55bc14b4-a166-4a33-a0bc-a2b0dcf66de0"


class _Stop(RuntimeError):
    pass


def _agent(tools: list[str]) -> Agent:
    return Agent(
        config=UnifiedConfig(
            model="test-model",
            tools=list(tools),
            messages=MessageList(
                _messages=[UnifiedMessage(role="user", content=[TextContent(text="go")])]
            ),
        ),
    )


async def _run_until_prepare_hook(agent: Agent, monkeypatch: pytest.MonkeyPatch) -> None:
    async def prepare_hook(*, agent, app_ctx):  # noqa: ARG001 — the hook is the stop line
        raise _Stop

    monkeypatch.setitem(_ext._registry, "programmatic_agent_prepare_hook", prepare_hook)
    ctx = AppContext(
        emitter=SilentEmitter(), user_id="user-1", is_authenticated=True, auth_type="token"
    )
    token = set_app_context(ctx)
    try:
        with pytest.raises(_Stop):
            await agent.execute(user_input="run")
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_uuid_tools_load_the_registry_before_resolution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fresh = ToolRegistry()
    monkeypatch.setattr(ToolRegistry, "get_instance", classmethod(lambda cls: fresh))
    assert fresh.loaded is False

    calls: list[str] = []

    async def fake_initialize_tool_system() -> int:
        calls.append("init")
        fresh.ensure_registered("web", description="unified web tool", tool_id=WEB_TOOL_ID)
        fresh._loaded = True
        return fresh.count

    import matrx_ai.tools.handle_tool_calls as handle_tool_calls

    monkeypatch.setattr(handle_tool_calls, "initialize_tool_system", fake_initialize_tool_system)

    agent = _agent([WEB_TOOL_ID])
    await _run_until_prepare_hook(agent, monkeypatch)

    assert calls == ["init"], "the registry must be loaded exactly once, before resolution"
    assert agent.config.tools == ["web"], "the UUID must leave the edge as a canonical name"


@pytest.mark.asyncio
async def test_names_only_tools_never_trigger_a_registry_load(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fresh = ToolRegistry()
    monkeypatch.setattr(ToolRegistry, "get_instance", classmethod(lambda cls: fresh))

    async def must_not_run() -> int:
        raise AssertionError("a names-only tool list must not load the registry")

    import matrx_ai.tools.handle_tool_calls as handle_tool_calls

    monkeypatch.setattr(handle_tool_calls, "initialize_tool_system", must_not_run)

    agent = _agent(["web"])
    await _run_until_prepare_hook(agent, monkeypatch)
    assert agent.config.tools == ["web"]


def test_uuid_shape_detector_is_exact() -> None:
    assert definition_module._looks_like_tool_id(WEB_TOOL_ID)
    assert not definition_module._looks_like_tool_id("web")
    assert not definition_module._looks_like_tool_id("bundle:list_webflow")
    assert not definition_module._looks_like_tool_id(None)
