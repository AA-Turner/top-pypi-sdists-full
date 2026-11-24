import pytest
from pydantic import BaseModel

from matrx_graph import ActionRegistry, NodeRegistry, MemoryCheckpointer
from matrx_graph.actions import declare_action, run_as_step, run_action
from matrx_graph.actions.decorator import ActionSignatureError
from matrx_graph.actions.spec import ActionFailed
from matrx_graph.types.context import ChannelView, NodeExecutionContext
from tests._fixtures import make_app_context


class Value(BaseModel):
    value: int = 1


def context():
    return NodeExecutionContext(app=make_app_context(), run_id="run", thread_id="run", node_id="n",
                                step=0, attempt=1, channels=ChannelView(_values={}, _pending_writes=[]),
                                checkpointer=MemoryCheckpointer())


async def test_context_is_the_actual_step_invocation_and_not_public_input():
    observed = []
    @declare_action(name="test.context_transport", description="test", input_schema=Value,
                    output_schema=Value, doors={"step"}, node_registry=NodeRegistry(), action_registry=ActionRegistry())
    async def work(app, inputs, *, node_context):
        observed.append(node_context)
        return inputs
    ctx = context()
    result = await run_as_step(work, ctx, Value())
    assert result.result.value == 1 and observed == [ctx] and observed[0] is ctx
    assert "node_context" not in Value.model_fields
    with pytest.raises(ActionFailed):
        await run_action(work._matrx_action_spec, Value(), app=ctx.app, door="api")
    assert len(observed) == 1


def test_context_rejects_non_step_or_positional_parameter():
    for doors, fn in [({"step", "tool"}, _keyword), ({"step"}, _positional)]:
        with pytest.raises(ActionSignatureError):
            declare_action(name="test.bad_context", description="test", input_schema=Value,
                           output_schema=Value, doors=doors, node_registry=NodeRegistry(),
                           action_registry=ActionRegistry())(fn)


async def _keyword(app, inputs, *, node_context):
    return inputs


async def _positional(app, inputs, node_context):
    return inputs
