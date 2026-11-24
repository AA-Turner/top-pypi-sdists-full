"""``open_tool_door(tool_args=...)``: a host offers an Action tool with a narrower argument model.

Break: the narrower model is ignored (the tool keeps offering every input field), or a re-open drops it.
"""

from __future__ import annotations

from matrx_graph.actions import declare_action
from matrx_graph.actions.registry import ActionRegistry
from matrx_graph.executor.registry import NodeRegistry
from matrx_graph.types.primitives import ActionTier, NodeCategory
from pydantic import BaseModel


class _In(BaseModel):
    title: str
    import_uid: str | None = None


class _Narrow(BaseModel):
    title: str


class _Out(BaseModel):
    ok: bool


def test_a_host_narrows_an_action_tool() -> None:
    from matrx_ai.tools.action_door import action_for_tool, open_tool_door, tool_args_for
    from matrx_ai.tools.declared import get_declared_tool

    registry = ActionRegistry()

    async def work(_app: object, _inp: _In) -> _Out:
        return _Out(ok=True)

    declare_action(
        name="narrowtest.make", display_name="Make", description="Make one.", input_schema=_In, output_schema=_Out,
        doors=frozenset({"tool"}), category=NodeCategory.DATA, determinism=ActionTier.NON_DETERMINISTIC,
        tags=("narrowtest",), writes_or_spends=False, admin_only=False, node_registry=NodeRegistry(), action_registry=registry,
    )(work)
    open_tool_door(registry)
    assert get_declared_tool("narrowtest_make").args_model is _In
    open_tool_door(registry, tool_args={"narrowtest_make": _Narrow})
    spec = action_for_tool("narrowtest_make")
    assert spec is not None and tool_args_for("narrowtest_make", spec) is _Narrow
    assert get_declared_tool("narrowtest_make").args_model is _Narrow
    open_tool_door(registry)  # a later re-open keeps what the host said
    assert get_declared_tool("narrowtest_make").args_model is _Narrow
