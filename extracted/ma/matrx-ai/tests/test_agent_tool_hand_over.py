"""Context passthrough on the agent-tool path (host-agnostic half).

* A host-attached projection carries ``host_data`` and the optional ``hand_over`` argument.
* ``hand_over`` never becomes a child variable; the host resolver fills fields; message text
  never rides ``user_input``; a hand-over with no typed input starts a HOST turn.
* What could not be passed comes back in the tool result.
* THE NO-LEAK GUARD: a child run never inherits its caller's context manifest on its context —
  the caller's values reach it only as ``Agent.host_parent_context``.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.tools.agent_projection import (
    HAND_OVER_ARG,
    HAND_OVER_PARAMETER,
    _variable_definitions_to_parameters,
)
from matrx_ai.tools.agent_tool import _merge_projected_variables, execute_agent_tool
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType

HOST = {"orchestra": {"conductor_id": "c1", "context": {"mode": "handed_over"}}}
CONDUCTOR_MANIFEST = [{"key": "angle", "content": "The angle"}]


def _projected(variable_names: list[str], *, host: bool = True) -> ToolDefinition:
    defs = [{"name": n, "helpText": f"var {n}", "required": False} for n in variable_names]
    params = _variable_definitions_to_parameters(defs)
    if host:
        params.setdefault(HAND_OVER_ARG, dict(HAND_OVER_PARAMETER))
    return ToolDefinition(
        name="custom_tool_1",
        tool_type=ToolType.AGENT,
        function_path="agent:abc-123",
        prompt_id="abc-123",
        parameters=params,
        host_data=HOST if host else None,
    )


class _Agent:
    def __init__(self) -> None:
        self.host_data = None
        self.host_parent_context = None
        self.host_notes: list[dict[str, Any]] = []


@pytest.fixture
def harness(monkeypatch):
    captured: dict[str, Any] = {"resolver_calls": []}

    async def fake_from_agent(cls, agent_id, is_version=False, variables=None, **kw):
        captured["variables"] = dict(variables or {})
        agent = _Agent()
        captured["agent"] = agent
        return agent

    async def fake_run_agent(agent, *, label, source_feature, user_input, **kw):
        from matrx_connect.context.app_context import get_app_context

        captured["user_input"] = user_input
        captured["host_turn"] = kw.get("host_turn")
        captured["child_metadata"] = dict(get_app_context().metadata)
        # The host prepare hook may add notes while the child runs.
        agent.host_notes.append({"value": "voice", "reason": "refused"})
        from matrx_ai.agents.executor import AgentRunResult

        return AgentRunResult(success=True, output="child answer")

    async def resolver(**kwargs):
        captured["resolver_calls"].append(kwargs)
        return {
            "variables": {"facts": "The angle"},
            "host_state": {"context": [], "message_text": "Voice:\nWarm"},
            "notes": [{"value": "ghost", "reason": "not one of your values"}],
        }

    import matrx_ai._ext as ext
    import matrx_ai.agents.definition as definition_mod
    import matrx_ai.agents.executor as executor_mod

    monkeypatch.setattr(definition_mod.Agent, "from_agent", classmethod(fake_from_agent))
    monkeypatch.setattr(executor_mod, "run_agent", fake_run_agent)
    monkeypatch.setattr(ext, "get_agent_tool_handover_resolver", lambda: resolver)
    token = set_app_context(AppContext(emitter=None, user_id="u1", metadata={"context_objects": CONDUCTOR_MANIFEST}))
    yield captured
    clear_app_context(token)


def test_hand_over_is_never_a_variable():
    tool_def = _projected(["facts"])
    variables, user_input = _merge_projected_variables(
        {"facts": "x", HAND_OVER_ARG: "angle", "input": "go"}, tool_def
    )
    assert variables == {"facts": "x"} and user_input == "go"


def test_an_author_variable_named_hand_over_wins():
    tool_def = _projected([HAND_OVER_ARG])  # the author's own variable — its own description
    variables, _ = _merge_projected_variables({HAND_OVER_ARG: "mine"}, tool_def)
    assert variables == {HAND_OVER_ARG: "mine"}


@pytest.mark.asyncio
async def test_the_host_resolves_fields_and_carries_the_callers_values_on_the_agent(harness):
    result = await execute_agent_tool(_projected(["facts"]), {HAND_OVER_ARG: "angle", "input": "write"}, ToolContext(call_id="c"))
    assert result.success is True
    (call,) = harness["resolver_calls"]
    assert call["hand_over"] == "angle" and call["declared_fields"] == ["facts"]
    assert call["parent_context_objects"] == CONDUCTOR_MANIFEST
    assert harness["variables"] == {"facts": "The angle"}
    agent = harness["agent"]
    assert agent.host_data == {"spec": HOST, "hand_over": "angle", "state": {"context": [], "message_text": "Voice:\nWarm"}}
    assert agent.host_parent_context == CONDUCTOR_MANIFEST
    # THE USER-INPUT LAW: the handed message text is never appended to the input.
    assert harness["user_input"] == "write"


@pytest.mark.asyncio
async def test_what_could_not_be_passed_comes_back_in_the_result(harness):
    result = await execute_agent_tool(_projected(["facts"]), {HAND_OVER_ARG: "angle", "input": "write"}, ToolContext(call_id="c"))
    assert result.output["result"] == "child answer"
    assert result.output["hand_over"] == [
        {"value": "ghost", "reason": "not one of your values"},
        {"value": "voice", "reason": "refused"},
    ]


@pytest.mark.asyncio
async def test_a_hand_over_with_no_input_starts_a_host_turn(harness):
    await execute_agent_tool(_projected([]), {HAND_OVER_ARG: "angle"}, ToolContext(call_id="c"))
    assert not harness["user_input"]
    assert harness["host_turn"] is not None and harness["host_turn"].reason == "orchestra_hand_over"


@pytest.mark.asyncio
async def test_a_plain_agent_tool_gets_no_resolver_and_no_parent_values(harness):
    await execute_agent_tool(_projected(["facts"], host=False), {"facts": "x", "input": "go"}, ToolContext(call_id="c"))
    assert harness["resolver_calls"] == []
    assert harness["agent"].host_parent_context is None


# ── the no-leak guard, at the ONE child funnel (run_agent) ────────────────────


@pytest.mark.asyncio
async def test_a_child_run_never_inherits_the_callers_manifest(monkeypatch):
    from matrx_ai.agents import executor as executor_mod

    seen: dict[str, Any] = {}

    class _Child:
        name = "child"
        source_id = None
        source_is_version = False
        request_metadata: dict[str, Any] = {}

        class config:  # noqa: N801 — attribute bag
            model = None

        async def execute(self, user_input=None, **_kw):
            from matrx_connect.context.app_context import get_app_context

            seen["metadata"] = dict(get_app_context().metadata)
            raise RuntimeError("stop here")  # run_agent never raises; the result says failed

    token = set_app_context(AppContext(
        emitter=None, user_id="u1",
        metadata={"context_objects": CONDUCTOR_MANIFEST, "context_receipt": {"rows": []},
                  "context_excluded_keys": ["x"], "keep_me": 1},
    ))
    try:
        result = await executor_mod.run_agent(
            _Child(), label="child", source_feature="test", user_input="hi", emit_lifecycle=False
        )
    finally:
        clear_app_context(token)
    assert result.success is False
    metadata = seen["metadata"]
    for key in ("context_objects", "context_receipt", "context_excluded_keys"):
        assert key not in metadata, f"a child inherited its caller's {key}"
    assert metadata.get("keep_me") == 1
