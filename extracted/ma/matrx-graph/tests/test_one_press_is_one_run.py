"""One press is one run: the outermost ``run_action`` mints the run id and every Action it runs
inside itself inherits it.

The host says the run id to the database so every row version a run writes carries it; that is what
lets a whole run be listed and undone as one change. If a nested call minted its own id, one press
would look like several unrelated changes.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from matrx_graph.actions import ActionRegistry, current_action_call, current_action_run_id, declare_action, run_action
from matrx_graph.nodes import NodeRegistry


class In(BaseModel):
    n: int = 0


class Out(BaseModel):
    run_id: str
    inner_run_id: str | None = None
    run_action: str | None = None
    run_door: str | None = None
    inner_action: str | None = None


@pytest.fixture
def registry() -> ActionRegistry:
    actions = ActionRegistry()
    nodes = NodeRegistry()

    @declare_action(
        name="probe.inner", description="Reports the run it is in.", input_schema=In, output_schema=Out,
        doors={"api", "step"}, action_registry=actions, node_registry=nodes,
    )
    async def inner(app, input: In) -> Out:  # noqa: ANN001
        call = current_action_call()
        assert call is not None
        return Out(run_id=call.run_id or "", run_action=call.run_action, run_door=call.run_door, inner_action=call.action)

    @declare_action(
        name="probe.outer", description="Runs another Action inside itself.", input_schema=In, output_schema=Out,
        doors={"api", "step"}, action_registry=actions, node_registry=nodes,
    )
    async def outer(app, input: In) -> Out:  # noqa: ANN001
        mine = current_action_run_id()
        nested = await run_action("probe.inner", {"n": 1}, app=app, door="step", registry=actions)
        assert isinstance(nested, Out)
        # The outer call is the current call again once the nested one returns.
        assert current_action_run_id() == mine
        return Out(
            run_id=mine or "", inner_run_id=nested.run_id, run_action=nested.run_action,
            run_door=nested.run_door, inner_action=nested.inner_action,
        )

    return actions


def test_no_run_outside_an_action() -> None:
    assert current_action_run_id() is None


@pytest.mark.asyncio
async def test_a_call_gets_a_run_id(registry: ActionRegistry) -> None:
    out = await run_action("probe.inner", {}, app=None, door="api", registry=registry)
    assert isinstance(out, Out)
    assert len(out.run_id) == 32
    assert (out.run_action, out.run_door) == ("probe.inner", "api")
    assert current_action_run_id() is None


@pytest.mark.asyncio
async def test_a_nested_action_is_in_the_same_run(registry: ActionRegistry) -> None:
    out = await run_action("probe.outer", {}, app=None, door="api", registry=registry)
    assert isinstance(out, Out)
    assert out.run_id and out.inner_run_id == out.run_id
    # The run is named for what was actually asked: the outermost Action and its door.
    assert (out.run_action, out.run_door) == ("probe.outer", "api")
    assert out.inner_action == "probe.inner"


@pytest.mark.asyncio
async def test_two_presses_are_two_runs(registry: ActionRegistry) -> None:
    first = await run_action("probe.inner", {}, app=None, door="api", registry=registry)
    second = await run_action("probe.inner", {}, app=None, door="api", registry=registry)
    assert isinstance(first, Out) and isinstance(second, Out)
    assert first.run_id != second.run_id
