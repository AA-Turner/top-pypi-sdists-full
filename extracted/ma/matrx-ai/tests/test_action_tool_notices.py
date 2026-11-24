"""An Action's work hands the model a notice through the tool door (``add_tool_notices``), and only
there: the same work run through the step door carries no notice and never fails for asking.

Green only when real: the tool is the generated door (``open_tool_door`` → ``run_action_tool``), the
step is the generated step executor, and the work is a declared Action.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_graph.actions import declare_action, default_action_registry, tool_name_for
from matrx_graph.executor.registry import default_registry
from pydantic import BaseModel, ConfigDict


class _In(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: str


class _Out(BaseModel):
    echoed: str


class _Emitter:
    pass


@pytest.fixture
def declared():
    from matrx_ai.tools import action_door
    from matrx_ai.tools import declared as tools
    from matrx_ai.tools.action_door import add_tool_notices

    name = f"notice_test.echo_{uuid.uuid4().hex[:8]}"

    @declare_action(name=name, description="Echo (test).", input_schema=_In, output_schema=_Out,
                    doors={"step", "tool"})
    async def echo(app, payload: _In) -> _Out:
        add_tool_notices(f"read {payload.value} the quick way", "")
        return _Out(echoed=payload.value)

    yield name
    default_action_registry().unregister(name)
    default_registry()._executors.pop(name, None)
    tools._REGISTRY.pop(tool_name_for(name), None)
    action_door._BY_TOOL_NAME.pop(tool_name_for(name), None)


async def test_the_tool_door_hands_the_works_notices_to_the_model(declared):
    from matrx_ai.tools.action_door import open_tool_door
    from matrx_ai.tools.declared import get_declared_tool
    from matrx_ai.tools.models import ToolContext

    tool_name = tool_name_for(declared)
    assert tool_name in open_tool_door()
    token = set_app_context(AppContext(emitter=_Emitter(), user_id="u", organization_id="o"))  # type: ignore[arg-type]
    try:
        res = await get_declared_tool(tool_name).func({"value": "a"}, ToolContext(call_id="", tool_name=tool_name))
        again = await get_declared_tool(tool_name).func({"value": "b"}, ToolContext(call_id="", tool_name=tool_name))
    finally:
        clear_app_context(token)
    assert res.success and res.output["echoed"] == "a"
    assert res.model_notices == ["read a the quick way"]
    assert again.model_notices == ["read b the quick way"]  # one call's notices never leak into the next


async def test_the_step_door_carries_no_notice(declared):
    app = AppContext(emitter=_Emitter(), user_id="u", organization_id="o")  # type: ignore[arg-type]
    ctx = SimpleNamespace(app=app, run_id="r", node_id="n", dispatch_id="d", item_index=0, firing=0)
    result = await default_registry().get(declared).execute(ctx, _In(value="s"), None)
    assert result.result == _Out(echoed="s")
