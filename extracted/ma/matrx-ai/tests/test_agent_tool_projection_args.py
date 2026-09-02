"""Regression tests for the projected-agent args + is_version defects (2026-07-01).

Pins two bug classes:
  1. agent_projection advertises the agent's variable names as TOP-LEVEL tool
     parameters, but execute_agent_tool used to read only args['variables'] and
     input/user_input/query/task — so a model calling a projected agent tool had
     EVERY input silently dropped (the child received literally nothing).
  2. The projection dropped ``is_version`` (dump rebuild assumed non-version and
     dispatch always loaded the master row), so a version-pinned AgentToolSpec
     executed the wrong record.

Post-review hardening (2026-07-02): the merge is SCHEMA-AWARE — a name the agent
author DECLARED as a variable is always routed as a variable, even when it
collides with the reserved free-text names (input/user_input/query/task); the
auto-added ``input`` param is recognized by its description constant.
"""
from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools.agent_projection import (
    AUTO_INPUT_DESCRIPTION,
    _variable_definitions_to_parameters,
)
from matrx_ai.tools.agent_tool import (
    _merge_projected_variables,
    execute_agent_tool,
)
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType


def _projected(variable_names: list[str] | None = None) -> ToolDefinition:
    defs = [{"name": n, "helpText": f"var {n}", "required": False} for n in variable_names or []]
    return ToolDefinition(
        name="custom_tool_1",
        tool_type=ToolType.AGENT,
        function_path="agent:abc-123",
        prompt_id="abc-123",
        parameters=_variable_definitions_to_parameters(defs),
    )


# ---------------------------------------------------------------------------
# projection reaches the provider declarations (not just dispatch)
# ---------------------------------------------------------------------------


def test_projected_agent_tool_reaches_the_provider_declarations():
    """Regression for the 2026-07-07 live-smoke finding: a projected agent tool
    (``custom_tool_N``) is a ``RegisteredToolSpec(name=custom_tool_N)`` in
    ``config.tools`` whose ``ToolDefinition`` lives ONLY on the request's
    ``AppContext.metadata`` (never in the registry). ``get_provider_tools`` used
    to resolve names against the registry alone → the projection was DROPPED, so
    the model never saw the tool and could not call it (handoff / reference /
    agent-as-tool via ``request.tools`` silently no-op'd). The provider-declaration
    path must consult the projection map, exactly as the executor's dispatch does."""
    from matrx_connect.context.app_context import (
        AppContext,
        clear_app_context,
        set_app_context,
    )

    from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY
    from matrx_ai.tools.registry import ToolRegistry

    tool_def = _projected(["topic"])
    ctx = AppContext(
        emitter=None,
        user_id="u1",
        metadata={
            PROJECTED_AGENT_TOOLS_KEY: {"custom_tool_1": tool_def.model_dump(exclude={"_callable"})}
        },
    )
    token = set_app_context(ctx)
    try:
        registry = ToolRegistry.get_instance()
        # custom_tool_1 is NOT in the registry (projections never are) …
        assert registry.get("custom_tool_1") is None
        for provider in ("anthropic", "openai", "google"):
            decls = registry.get_provider_tools(["custom_tool_1"], provider)
            # … yet it MUST reach the provider declarations via the projection map.
            names = {d.get("name") or (d.get("function") or {}).get("name") for d in decls}
            assert "custom_tool_1" in names, (provider, decls)
        # A genuinely-unknown name is still dropped (not masked by the new path).
        assert registry.get_provider_tools(["definitely_not_a_tool_xyz"], "anthropic") == []
    finally:
        clear_app_context(token)


# ---------------------------------------------------------------------------
# _merge_projected_variables
# ---------------------------------------------------------------------------


def test_top_level_args_become_variables_and_input_is_task():
    variables, user_input = _merge_projected_variables(
        {"topic": "AI Safety", "audience": "developers", "input": "write it"},
        _projected(["topic", "audience"]),
    )
    assert variables == {"topic": "AI Safety", "audience": "developers"}
    assert user_input == "write it"


def test_declared_reserved_names_win_as_variables():
    # The author declared a variable literally named 'query' — the projection
    # contract says the author's intent wins, so it must reach variables (the
    # old reserved-set skip silently emptied its {{query}} placeholder).
    variables, user_input = _merge_projected_variables(
        {"query": "solar tariffs"}, _projected(["query"])
    )
    assert variables == {"query": "solar tariffs"}
    assert user_input == ""


def test_declared_input_variable_wins_over_auto_input():
    variables, user_input = _merge_projected_variables(
        {"input": "the variable value"}, _projected(["input"])
    )
    assert variables == {"input": "the variable value"}
    assert user_input == ""


def test_undeclared_reserved_names_feed_user_input():
    variables, user_input = _merge_projected_variables(
        {"query": "find things", "kept": "v"}, _projected(["kept"])
    )
    assert variables == {"kept": "v"}
    assert user_input == "find things"


def test_nested_variables_win_over_top_level():
    variables, _ = _merge_projected_variables(
        {"topic": "from-top-level", "variables": {"topic": "from-nested"}},
        _projected(["topic"]),
    )
    assert variables == {"topic": "from-nested"}


def test_non_string_values_coerced_to_json():
    variables, _ = _merge_projected_variables(
        {"items": ["a", "b"], "count": 3}, _projected(["items", "count"])
    )
    assert variables["items"] == '["a", "b"]'
    assert variables["count"] == "3"


# ---------------------------------------------------------------------------
# _variable_definitions_to_parameters
# ---------------------------------------------------------------------------


def test_projected_schema_always_offers_input():
    params = _variable_definitions_to_parameters(None)
    assert params["input"]["description"] == AUTO_INPUT_DESCRIPTION
    assert params["input"]["required"] is False


def test_projected_schema_declares_variables_and_input():
    params = _variable_definitions_to_parameters(
        [{"name": "topic", "helpText": "the subject", "required": True}]
    )
    assert set(params) == {"input", "topic"}
    assert params["topic"] == {
        "type": "string",
        "description": "the subject",
        "required": True,
    }


def test_variable_named_input_wins_over_builtin():
    params = _variable_definitions_to_parameters(
        [{"name": "input", "helpText": "custom input var", "required": True}]
    )
    assert params["input"]["description"] == "custom input var"
    assert params["input"]["description"] != AUTO_INPUT_DESCRIPTION


# ---------------------------------------------------------------------------
# execute_agent_tool dispatch: variables + is_version reach Agent.from_agent
# ---------------------------------------------------------------------------


class _FakeAgent:
    """Stands in for the loaded Agent; run_agent is patched so it is inert."""


@pytest.mark.asyncio
@pytest.mark.parametrize("is_version", [False, True])
async def test_dispatch_forwards_projected_args_and_version(monkeypatch, is_version):
    captured: dict[str, Any] = {}

    async def fake_from_agent(agent_id, is_version=False, variables=None, **kwargs):
        captured["agent_id"] = agent_id
        captured["is_version"] = is_version
        captured["variables"] = variables
        return _FakeAgent()

    async def fake_run_agent(agent, *, label, source_feature, user_input, suppress_stream=False, **_kw):
        captured["user_input"] = user_input
        from matrx_ai.agents.executor import AgentRunResult

        return AgentRunResult(success=True, output="child answer")

    import matrx_ai.agents.definition as definition_mod
    import matrx_ai.agents.executor as executor_mod

    monkeypatch.setattr(
        definition_mod.Agent, "from_agent", classmethod(
            lambda cls, agent_id, is_version=False, variables=None, **kw: fake_from_agent(
                agent_id, is_version=is_version, variables=variables, **kw
            )
        ),
    )
    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)

    tool_def = _projected(["topic"])
    tool_def.prompt_is_version = is_version
    ctx = ToolContext(call_id="call-1")

    result = await execute_agent_tool(
        tool_def,
        {"topic": "AI Safety", "input": "write the brief"},
        ctx,
    )

    assert result.success is True
    assert captured["agent_id"] == "abc-123"
    assert captured["is_version"] is is_version
    assert captured["variables"] == {"topic": "AI Safety"}
    assert captured["user_input"] == "write the brief"


# ---------------------------------------------------------------------------
# Projection carries prompt_is_version + dedup map honors it
# ---------------------------------------------------------------------------


def test_tool_definition_carries_prompt_is_version_through_dump():
    tool_def = ToolDefinition(
        name="custom_tool_1",
        tool_type=ToolType.AGENT,
        prompt_id="abc-123",
        prompt_is_version=True,
    )
    dumped = tool_def.model_dump()
    assert dumped["prompt_is_version"] is True
    rehydrated = ToolDefinition.model_validate(dumped)
    assert rehydrated.prompt_is_version is True
