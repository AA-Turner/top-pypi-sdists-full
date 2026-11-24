"""A step whose input does not fit its Action fails as the STEP's Failure, in plain words.

Live 2026-11-15: two "Run an Action" steps (table.row.create, no table picked) killed their runs
with a raw pydantic dump ("1 validation error for RowCreateInput / table / Field required").
The step door now answers ``invalid_input`` naming the missing input; a ValidationError raised
inside the work itself is not the step's input and still propagates.
"""

import pytest
from pydantic import BaseModel, ValidationError

from matrx_graph import ActionRegistry, MemoryCheckpointer, NodeRegistry
from matrx_graph.actions import declare_action, run_as_step
from matrx_graph.types.context import ChannelView, NodeExecutionContext
from matrx_graph.types.result import Failure
from tests._fixtures import make_app_context


class NeedsTable(BaseModel):
    table: str
    count: int = 1


class Out(BaseModel):
    ok: int = 1


def context() -> NodeExecutionContext:
    return NodeExecutionContext(app=make_app_context(), run_id="run", thread_id="run", node_id="n",
                                step=0, attempt=1, channels=ChannelView(_values={}, _pending_writes=[]),
                                checkpointer=MemoryCheckpointer())


def _declare(name: str, work):
    return declare_action(name=name, description="test", input_schema=NeedsTable, output_schema=Out,
                          doors={"step"}, node_registry=NodeRegistry(), action_registry=ActionRegistry())(work)


async def test_a_missing_input_is_the_steps_failure_naming_the_input():
    async def work(app, inputs):
        return Out()

    fn = _declare("test.needs_table", work)
    result = await run_as_step(fn, context(), {})  # type: ignore[arg-type]
    assert isinstance(result, Failure)
    assert result.error.code == "invalid_input"
    assert "needs table" in result.error.message
    assert "validation error" not in result.error.message
    assert result.error.details["errors"][0]["field"] == "table"


async def test_a_wrong_value_names_the_field():
    async def work(app, inputs):
        return Out()

    fn = _declare("test.needs_table_wrong", work)
    result = await run_as_step(fn, context(), {"table": "t", "count": "many"})  # type: ignore[arg-type]
    assert isinstance(result, Failure) and result.error.code == "invalid_input"
    assert "count" in result.error.message


async def test_a_validation_error_inside_the_work_still_raises():
    async def work(app, inputs):
        Out.model_validate({"ok": "not a number"})
        return Out()

    fn = _declare("test.inner_validation", work)
    with pytest.raises(ValidationError):
        await run_as_step(fn, context(), {"table": "t"})  # type: ignore[arg-type]
