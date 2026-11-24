"""A run is reported ONCE, at its outermost call, with the way back its Actions DECLARED.

Amendment 5 of full-control undo: a change made through an Action is undone through that Action's
declared inverse, never by restoring rows underneath it, and no inverse means not undoable. The
router hands the host one RunRecord per outermost run; nested Actions contribute their parts.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from matrx_graph.actions import (
    INVERSE_OF_PARTS,
    ActionRegistry,
    InverseStep,
    RunRecord,
    configure_run_recorder,
    declare_action,
    inverse_of,
    last_run_id,
    run_action,
)
from matrx_graph.nodes import NodeRegistry


class In(BaseModel):
    n: int = 0


class Out(BaseModel):
    n: int = 0


class Recorder:
    def __init__(self) -> None:
        self.begun: list[str] = []
        self.records: list[RunRecord] = []

    async def begin(self, spec, app, run_id: str):  # noqa: ANN001
        self.begun.append(spec.name)
        return f"mark:{spec.name}"

    async def finish(self, record: RunRecord) -> None:
        self.records.append(record)


@pytest.fixture
def recorder():
    rec = Recorder()
    configure_run_recorder(rec)
    yield rec
    configure_run_recorder(None)


@pytest.fixture
def registry() -> ActionRegistry:
    actions = ActionRegistry()
    nodes = NodeRegistry()

    def back(data: In, out: Out) -> list[InverseStep]:
        return [InverseStep(action="probe.set", input={"n": -data.n})]

    @declare_action(name="probe.set", description="Sets n.", input_schema=In, output_schema=Out,
                    doors={"api", "step"}, action_registry=actions, node_registry=nodes, inverse=back)
    async def set_n(app, input: In) -> Out:  # noqa: ANN001
        return Out(n=input.n)

    @declare_action(name="probe.oneway", description="Cannot be taken back.", input_schema=In, output_schema=Out,
                    doors={"api", "step"}, action_registry=actions, node_registry=nodes)
    async def oneway(app, input: In) -> Out:  # noqa: ANN001
        return Out(n=input.n)

    @declare_action(name="probe.both", description="Two sets, undone by its parts.", input_schema=In, output_schema=Out,
                    doors={"api", "step"}, action_registry=actions, node_registry=nodes, inverse=INVERSE_OF_PARTS)
    async def both(app, input: In) -> Out:  # noqa: ANN001
        await run_action("probe.set", {"n": 1}, app=app, door="step", registry=actions)
        await run_action("probe.set", {"n": 2}, app=app, door="step", registry=actions)
        return Out(n=3)

    @declare_action(name="probe.mixed", description="A set and a one-way step.", input_schema=In, output_schema=Out,
                    doors={"api", "step"}, action_registry=actions, node_registry=nodes, inverse=INVERSE_OF_PARTS)
    async def mixed(app, input: In) -> Out:  # noqa: ANN001
        await run_action("probe.set", {"n": 1}, app=app, door="step", registry=actions)
        await run_action("probe.oneway", {"n": 2}, app=app, door="step", registry=actions)
        return Out(n=3)

    @declare_action(name="probe.boom", description="Writes then fails.", input_schema=In, output_schema=Out,
                    doors={"api", "step"}, action_registry=actions, node_registry=nodes, inverse=INVERSE_OF_PARTS)
    async def boom(app, input: In) -> Out:  # noqa: ANN001
        await run_action("probe.set", {"n": 1}, app=app, door="step", registry=actions)
        raise RuntimeError("partway")

    def bad(data: In, out: Out) -> list[dict]:
        return [{"not_an_action": True}]

    @declare_action(name="probe.badinverse", description="Its inverse is malformed.", input_schema=In, output_schema=Out,
                    doors={"api", "step"}, action_registry=actions, node_registry=nodes, inverse=bad)
    async def badinverse(app, input: In) -> Out:  # noqa: ANN001
        return Out(n=input.n)

    return actions


@pytest.mark.asyncio
async def test_a_malformed_inverse_never_fails_a_write_that_succeeded(registry, recorder) -> None:
    from matrx_graph.actions import current_action_call

    out = await run_action("probe.badinverse", {"n": 4}, app=None, door="api", registry=registry)
    assert isinstance(out, Out) and out.n == 4, "the write stands"
    assert current_action_call() is None, "the router still put the caller's call back"
    [rec] = recorder.records
    assert rec.inverse is None and "could not be worked out" in rec.not_undoable[0]


@pytest.mark.asyncio
async def test_one_record_per_outermost_run_with_the_declared_inverse(registry, recorder) -> None:
    await run_action("probe.set", {"n": 5}, app=None, door="api", registry=registry)
    assert recorder.begun == ["probe.set"]
    [rec] = recorder.records
    assert (rec.action, rec.door, rec.mark) == ("probe.set", "api", "mark:probe.set")
    assert rec.inverse == [InverseStep(action="probe.set", input={"n": -5})]
    assert rec.not_undoable == [] and len(rec.run_id) == 32


@pytest.mark.asyncio
async def test_last_run_id_is_the_outermost_runs_id_for_the_door_to_return(registry, recorder) -> None:
    await run_action("probe.both", {}, app=None, door="api", registry=registry)
    [rec] = recorder.records
    assert last_run_id() == rec.run_id, "the door must hand back the run the recorder wrote"


@pytest.mark.asyncio
async def test_nested_calls_are_parts_of_one_run_undone_newest_first(registry, recorder) -> None:
    await run_action("probe.both", {}, app=None, door="api", registry=registry)
    assert recorder.begun == ["probe.both"], "a nested call is never its own run"
    [rec] = recorder.records
    assert [s.input["n"] for s in rec.inverse or []] == [-2, -1]


@pytest.mark.asyncio
async def test_no_declared_inverse_is_not_undoable_and_says_why(registry, recorder) -> None:
    await run_action("probe.oneway", {}, app=None, door="api", registry=registry)
    await run_action("probe.mixed", {}, app=None, door="api", registry=registry)
    oneway, mixed = recorder.records
    assert oneway.inverse is None and "declares no way to undo" in oneway.not_undoable[0]
    assert mixed.inverse is None and "probe.oneway" in mixed.not_undoable[0]


@pytest.mark.asyncio
async def test_a_failed_run_is_still_recorded_and_not_undoable(registry, recorder) -> None:
    with pytest.raises(RuntimeError):
        await run_action("probe.boom", {}, app=None, door="api", registry=registry)
    [rec] = recorder.records
    assert rec.inverse is None and isinstance(rec.error, RuntimeError)
    assert "failed partway" in rec.not_undoable[0]


@pytest.mark.asyncio
async def test_a_recorder_that_fails_never_fails_the_run(registry) -> None:
    class Broken(Recorder):
        async def finish(self, record: RunRecord) -> None:
            raise ConnectionError("db down")

    configure_run_recorder(Broken())
    try:
        out = await run_action("probe.set", {"n": 1}, app=None, door="api", registry=registry)
    finally:
        configure_run_recorder(None)
    assert isinstance(out, Out) and out.n == 1


def test_inverse_is_declared_with_the_action(registry) -> None:
    assert inverse_of("probe.both") == INVERSE_OF_PARTS
    assert inverse_of("probe.oneway") is None
