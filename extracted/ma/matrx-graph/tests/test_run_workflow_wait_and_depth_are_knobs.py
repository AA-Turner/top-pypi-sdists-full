"""The Run Workflow step's two limits are knobs an admin turns (lane 6i, review of 6g).

- Its wait limit is ``workflow.step_clock.run_workflow_wait_seconds`` (spec ``timeout_knob``); the 24 h on the
  spec is only that row's mirror, and the step's own ``data.step_clock`` still wins. Before: a constant the
  admin setting could never change, and a timeout said the AUTHOR had set it.
- Its nesting limit is ``workflow.run_workflow.max_depth`` (the host refuses past it); an inline child
  counts one level deeper than its caller (``inline_depth``).
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_graph import knobs as graph_knobs
from matrx_graph.errors import NodeTimeoutError
from matrx_graph.nodes.subgraph.call import SubgraphCallExecutor, set_subgraph_resolver
from matrx_graph.nodes.subgraph.inline import InlineChildEmitter, inline_depth
from matrx_graph.types.compiled import StepClock


@pytest.fixture(autouse=True)
def _clean():
    graph_knobs.clear_knob_cache()
    set_subgraph_resolver(None)
    yield
    graph_knobs.clear_knob_cache()
    set_subgraph_resolver(None)


def _rows(monkeypatch, feature_rows: dict[str, dict] | None):
    async def _values(feature: str):
        return None if feature_rows is None else feature_rows.get(feature, {})

    monkeypatch.setattr(graph_knobs, "_feature_values", _values)
    monkeypatch.setattr(graph_knobs, "MIN_STEP_SECONDS", 1)
    filed: list = []
    monkeypatch.setattr(graph_knobs, "_file_missing_rows", lambda f, k: filed.append((f, list(k))))
    return filed


def test_the_run_workflow_step_reads_its_wait_from_a_knob():
    spec = SubgraphCallExecutor.spec
    assert spec.timeout_knob == graph_knobs.RUN_WORKFLOW_WAIT_SECONDS_KEY
    assert spec.timeout_ms == graph_knobs.MAX_STEP_SECONDS * 1000  # the mirror only


async def test_the_admins_row_decides_the_wait(monkeypatch):
    _rows(monkeypatch, {graph_knobs.STEP_CLOCK_FEATURE: {"run_workflow_wait_seconds": 7200, "default_step_seconds": 600}})
    spec = SubgraphCallExecutor.spec
    assert await graph_knobs.step_timeout_seconds(spec.timeout_ms, timeout_knob=spec.timeout_knob) == (7200.0, "engine")


async def test_a_missing_row_keeps_the_mirror_and_is_filed(monkeypatch):
    filed = _rows(monkeypatch, {graph_knobs.STEP_CLOCK_FEATURE: {"default_step_seconds": 600}})
    spec = SubgraphCallExecutor.spec
    seconds, source = await graph_knobs.step_timeout_seconds(spec.timeout_ms, timeout_knob=spec.timeout_knob)
    assert (seconds, source) == (float(graph_knobs.MAX_STEP_SECONDS), "engine")
    assert filed == [(graph_knobs.STEP_CLOCK_FEATURE, ["run_workflow_wait_seconds"])]


async def test_the_steps_own_clock_still_wins_over_the_knob(monkeypatch):
    _rows(monkeypatch, {graph_knobs.STEP_CLOCK_FEATURE: {"run_workflow_wait_seconds": 7200}})
    spec = SubgraphCallExecutor.spec
    clock = StepClock(seconds=30)
    assert await graph_knobs.step_timeout_seconds(
        spec.timeout_ms, node_clock=clock, timeout_knob=spec.timeout_knob
    ) == (30.0, "declared")


def test_an_engine_limit_is_never_called_the_authors():
    err = NodeTimeoutError("read", 7_200_000, 1, source="engine", knob="run_workflow_wait_seconds")
    assert "author" not in err.person_message and "set on this step" not in str(err)
    assert "this kind of step" in err.person_message
    assert "'workflow.step_clock.run_workflow_wait_seconds'" in err.person_message


async def test_a_stopped_wait_names_the_knob_end_to_end(monkeypatch):
    from matrx_graph import (
        Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph, register_builtin_nodes,
    )
    from tests._fixtures import FakeEmitter, make_app_context

    _rows(monkeypatch, {graph_knobs.STEP_CLOCK_FEATURE: {"run_workflow_wait_seconds": 1, "default_step_seconds": 600}})

    async def _child(_ctx, _config, _inputs):
        await asyncio.Event().wait()

    set_subgraph_resolver(_child)
    definition = Definition.model_validate({"nodes": [{
        "id": "read", "type": "subgraph.call", "position": {"x": 0, "y": 0},
        "data": {"config": {"workflow_key": "research.journey.read"}},
    }], "edges": []})
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(compile_graph(definition, registry=registry), MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await asyncio.wait_for(scheduler.run(run_id="pass"), timeout=30)
    assert result.status is RunStatus.ERRORED
    failed = [e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == "node_failed"]
    assert len(failed) == 1 and "run_workflow_wait_seconds" in failed[0]["error_message"]


async def test_the_depth_limit_is_a_knob_with_a_loud_mirror(monkeypatch):
    filed = _rows(monkeypatch, {graph_knobs.RUN_WORKFLOW_FEATURE: {"max_depth": 3}})
    assert await graph_knobs.run_workflow_max_depth() == 3
    _rows(monkeypatch, {})
    graph_knobs.clear_knob_cache()
    assert await graph_knobs.run_workflow_max_depth() == graph_knobs.STARTING_RUN_WORKFLOW_MAX_DEPTH
    _rows(monkeypatch, None)
    assert await graph_knobs.run_workflow_max_depth() == graph_knobs.STARTING_RUN_WORKFLOW_MAX_DEPTH
    assert filed == []  # the first call had its row


def test_an_inline_child_runs_one_level_deeper_than_its_caller():
    base = SimpleNamespace()
    top = SimpleNamespace(app=SimpleNamespace(emitter=base))
    assert inline_depth(top) == 0
    first = InlineChildEmitter(base, node_prefix="a/", namespace="n/", depth=inline_depth(top) + 1)
    inner = SimpleNamespace(app=SimpleNamespace(emitter=first))
    assert inline_depth(inner) == 1
    second = InlineChildEmitter(first, node_prefix="a/b/", namespace="n/m/", depth=inline_depth(inner) + 1)
    assert inline_depth(SimpleNamespace(app=SimpleNamespace(emitter=second))) == 2
    # A step's scoped emitter keeps its depth.
    scoping = SimpleNamespace(for_invocation=lambda *a, **k: SimpleNamespace())
    scoped = InlineChildEmitter(scoping, node_prefix="a/", namespace="n/", depth=2).for_invocation("x")
    assert inline_depth(SimpleNamespace(app=SimpleNamespace(emitter=scoped))) == 2
