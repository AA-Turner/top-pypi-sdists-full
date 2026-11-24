"""A schedule-only Action runs from its schedule and from nowhere else (PF-SCHED, 2026-11-02).

System tasks (a nightly purge, a rent posting, a spend text) become Actions so the one
registry names them. Every runnable Action is open on the api, binding and directive doors
by construction, so without this a signed-in person could POST /actions/<purge>/run, an
agent could bind one as a variable, or emit it as a directive.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from matrx_graph.actions import ActionRegistry, declare_action, run_action
from matrx_graph.actions.doors import DOORS, directive_noun_of
from matrx_graph.actions.engines import DOOR_AUTHORITY, SELF_LEDGERED_DOORS
from matrx_graph.actions.spec import ActionFailed
from matrx_graph.nodes import NodeRegistry


class In(BaseModel):
    n: int = 1


class Out(BaseModel):
    n: int


@pytest.fixture
def registry() -> ActionRegistry:
    actions = ActionRegistry()

    @declare_action(
        name="system_task.nightly_purge", description="purge", input_schema=In, output_schema=Out,
        doors={"schedule"}, writes_or_spends=True, action_registry=actions, node_registry=NodeRegistry(),
    )
    async def purge(app, input: In) -> Out:  # noqa: ANN001
        return Out(n=input.n)

    return actions


def test_the_schedule_door_exists_and_carries_the_recorded_approval() -> None:
    assert "schedule" in DOORS
    assert DOOR_AUTHORITY["schedule"] == "approved"
    assert "schedule" in SELF_LEDGERED_DOORS


def test_no_door_opens_for_it_by_construction(registry: ActionRegistry) -> None:
    spec = registry.get("system_task.nightly_purge")
    assert spec.schedule_only
    assert spec.door_names() == {"schedule": "system_task.nightly_purge"}
    assert directive_noun_of(spec) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("door", ["api", "binding", "mcp", "tool", "directive", "step"])
async def test_every_other_door_is_refused(registry: ActionRegistry, door: str) -> None:
    with pytest.raises(ActionFailed) as err:
        await run_action("system_task.nightly_purge", {"n": 2}, app=None, door=door, registry=registry)
    assert err.value.code == "schedule_only"


@pytest.mark.asyncio
async def test_the_schedule_door_runs_it_without_asking_again(registry: ActionRegistry) -> None:
    out = await run_action("system_task.nightly_purge", {"n": 3}, app=None, door="schedule", registry=registry)
    assert out == Out(n=3)


def test_every_door_an_action_may_declare_has_a_name() -> None:
    """A declared door with no entry in ``door_names`` raised KeyError for the whole listing
    (``appointment.after_book`` declares ``service``; GET /actions died on it, 2026-11-03)."""
    actions = ActionRegistry()

    @declare_action(
        name="demo.every_door", description="d", input_schema=In, output_schema=Out,
        doors=set(DOORS) - {"schedule", "directive"}, action_registry=actions,
        node_registry=NodeRegistry(),
    )
    async def every(app, input: In) -> Out:  # noqa: ANN001
        return Out(n=input.n)

    names = actions.get("demo.every_door").door_names()
    assert names["service"] == "/actions/service/demo.every_door/run"
    assert set(DOORS) - {"schedule", "directive"} <= set(names)
