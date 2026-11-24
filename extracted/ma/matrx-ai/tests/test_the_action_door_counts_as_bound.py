"""The drift gate calls an Action tool bound ONLY while its Action still owns the model.

Every Action tool shares one function, so its source never names a model and the source-text
check called all of them "unverified": 178 tools on every boot, one matrx_tool_drift_gate row per
deploy with 0 errors, and a gate that was never green. Real: the tool is the generated door
(``open_tool_door`` → ``run_action_tool``), the Action is declared, and the second test proves the
exemption is not a blanket one by swapping the model out from under the door.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace

import pytest
from matrx_graph.actions import declare_action, default_action_registry, tool_name_for
from pydantic import BaseModel, ConfigDict


class _In(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: str


class _Other(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: str


class _Out(BaseModel):
    echoed: str


@pytest.fixture
def door_tool():
    from matrx_ai.tools import action_door
    from matrx_ai.tools import declared as tools

    name = f"bound_test.echo_{uuid.uuid4().hex[:8]}"

    @declare_action(name=name, description="Echo (test).", input_schema=_In, output_schema=_Out,
                    doors={"tool"})
    async def echo(app, payload: _In) -> _Out:
        return _Out(echoed=payload.value)

    tool_name = tool_name_for(name)
    action_door.open_tool_door()
    yield tool_name
    default_action_registry().unregister(name)
    tools._REGISTRY.pop(tool_name, None)
    action_door._BY_TOOL_NAME.pop(tool_name, None)


def _gate(tool_name: str) -> list[dict[str, str]]:
    from matrx_ai.tools.declared import get_declared_tool
    from matrx_ai.tools.validation.runner import find_unverified_tools

    return find_unverified_tools({tool_name: get_declared_tool(tool_name)}, {"aidream"})


def test_an_action_tool_is_bound_by_its_door(door_tool: str) -> None:
    assert _gate(door_tool) == []


def test_a_door_whose_action_lost_the_model_is_reported(door_tool: str) -> None:
    from matrx_ai.tools import action_door

    action_door._BY_TOOL_NAME[door_tool] = SimpleNamespace(input_schema=_Other)
    assert [row["tool_name"] for row in _gate(door_tool)] == [door_tool]


def test_an_action_tool_offered_a_narrower_model_is_bound_by_its_door() -> None:
    """calendar_event_create (2026-11-15): the tool omits import-only fields, so its model is the host's
    narrower one, not the Action's input_schema; still bound, because the door validates that model's fields."""
    from matrx_ai.tools import action_door
    from matrx_ai.tools import declared as tools

    class _Narrow(BaseModel):
        model_config = ConfigDict(extra="forbid")

    name = f"bound_test.narrow_{uuid.uuid4().hex[:8]}"

    @declare_action(name=name, description="Echo (test).", input_schema=_In, output_schema=_Out,
                    doors={"tool"})
    async def echo(app, payload: _In) -> _Out:
        return _Out(echoed=payload.value)

    tool_name = tool_name_for(name)
    try:
        action_door.open_tool_door(tool_args={tool_name: _Narrow})
        assert tools.get_declared_tool(tool_name).args_model is _Narrow
        assert _gate(tool_name) == []
    finally:
        default_action_registry().unregister(name)
        tools._REGISTRY.pop(tool_name, None)
        action_door._BY_TOOL_NAME.pop(tool_name, None)
        action_door._TOOL_ARGS.pop(tool_name, None)
