""""Run an Action" (``tool.call``): ONE workflow step that runs any registered Action by name through the one
router (``run_action``, step door), driven by the Scheduler.

THE BREAKS this catches:
* the step stops going through ``run_action`` (no ledger, no apply gate, no lazy names) — the replay case runs the
  Action twice;
* the dedupe key carries the attempt, or is rebuilt per leg — a re-run of the same run from its checkpoint acts twice;
* the run's app is rebuilt — the Action sees another person, organization or runtime execution id (cost would not
  nest under the workflow root);
* a stopping run still starts the side effect (``run_stopping``);
* an Action that does not open the step door runs anyway (``door_closed``).
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest
from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph, register_builtin_nodes
from matrx_graph.actions import configure_action_ledger, declare_action, default_action_registry
from matrx_graph.actions import engines as engines_mod
from matrx_graph.executor.execution import Execution, current_execution, executing
from matrx_graph.executor.registry import default_registry
from pydantic import BaseModel

from tests._fixtures import FakeEmitter, make_app_context

RUN_EXECUTION = str(uuid.uuid4())


class _In(BaseModel):
    title: str


class _Out(BaseModel):
    made: str


@pytest.fixture
def actions():
    made = f"step_test.make_{uuid.uuid4().hex[:8]}"
    closed = f"step_test.closed_{uuid.uuid4().hex[:8]}"
    seen: list[dict[str, Any]] = []

    @declare_action(name=made, description="makes a thing (test)", input_schema=_In, output_schema=_Out,
                    doors={"step", "api"}, writes_or_spends=True)
    async def work(app: Any, inputs: _In, *, idempotency_key: str | None = None) -> _Out:
        execution = current_execution()
        seen.append({"user": app.user_id, "execution_id": getattr(app, "execution_id", None), "key": idempotency_key,
                     "title": inputs.title, "stop_check_wired": execution is not None and execution.stopping is not None})
        return _Out(made=inputs.title)

    @declare_action(name=closed, description="no step door (test)", input_schema=_In, output_schema=_Out, doors={"api"})
    async def work_closed(app: Any, inputs: _In) -> _Out:
        seen.append({"closed": True})
        return _Out(made=inputs.title)

    saved = list(engines_mod._LEDGER), list(engines_mod._DURABLE_LEDGER)
    ledger: dict[str, BaseModel] = {}

    async def memory_ledger(spec, app, data, *, door, idempotency_key, run):
        key = f"{spec.name}:{door}:{idempotency_key}"
        if key not in ledger:
            ledger[key] = await run()
        return ledger[key]

    configure_action_ledger(memory_ledger)
    yield made, closed, seen, ledger
    configure_action_ledger(saved[0][0] if saved[0] else None, durable_ledger=saved[1][0] if saved[1] else None)
    for name in (made, closed):
        default_action_registry().unregister(name)
        default_registry()._executors.pop(name, None)


def _graph(action: str):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    definition = Definition.model_validate({
        "nodes": [{"id": "make", "type": "tool.call", "position": {"x": 0, "y": 0},
                   "data": {"config": {"action_name": action, "merge_inputs": False},
                            "inputs": {"payload": {"title": "Q3 plan"}}}}],
        "edges": [],
    })
    return compile_graph(definition, registry=registry), registry


def _app():
    app = make_app_context(FakeEmitter(), user_id="member-1")
    object.__setattr__(app, "execution_kind", "workflow_run")
    object.__setattr__(app, "execution_id", RUN_EXECUTION)
    return app


async def test_the_step_runs_the_action_once_as_the_run_and_a_rerun_replays(actions):
    made, _, seen, ledger = actions
    graph, registry = _graph(made)
    first = await Scheduler(graph, MemoryCheckpointer(), _app(), registry=registry).run(run_id="run-a")
    assert first.status is RunStatus.COMPLETED, first.error
    assert first.last_outputs["make"]["action"] == made and first.last_outputs["make"]["output"]["made"] == "Q3 plan"
    assert len(seen) == 1
    assert seen[0]["user"] == "member-1" and seen[0]["execution_id"] == RUN_EXECUTION, "the run's app is carried"
    assert seen[0]["stop_check_wired"], "the scheduler hands the step its stop check"
    key = seen[0]["key"]
    assert key == "step:run-a:make::0:0", f"the key is (run, node, dispatch, item, firing), never the attempt: {key}"

    # The same run driven again (a re-run from its checkpoint, a retried leg): the same attempt-independent key,
    # so the ledger replays the first answer and the Action does not act twice.
    again = await Scheduler(graph, MemoryCheckpointer(), _app(), registry=registry).run(run_id="run-a")
    assert again.status is RunStatus.COMPLETED, again.error
    assert len(seen) == 1 and again.last_outputs["make"]["output"]["made"] == "Q3 plan"
    assert len(ledger) == 1

    other = await Scheduler(graph, MemoryCheckpointer(), _app(), registry=registry).run(run_id="run-b")
    assert other.status is RunStatus.COMPLETED and len(seen) == 2, "another run is another call"


async def test_a_stopping_run_never_starts_the_action(actions):
    made, _, seen, _ = actions
    graph, registry = _graph(made)
    from types import SimpleNamespace

    from matrx_graph.nodes.tool.call import ToolCallConfig, ToolCallExecutor, ToolCallInput

    async def stopping() -> bool:
        return True

    ctx = SimpleNamespace(app=_app(), run_id="run-s", node_id="make", dispatch_id="", item_index=0, firing=0)
    with executing(Execution(run_id="run-s", definition_hash="h", graph=graph, fresh=True, stopping=stopping)):
        result = await ToolCallExecutor().execute(ctx, ToolCallInput(payload={"title": "x"}),
                                                  ToolCallConfig(action_name=made, merge_inputs=False))
    assert result.status == "error" and result.error.code == "run_stopping" and made in result.error.message
    assert seen == []


async def test_an_action_without_a_step_door_is_refused_by_name(actions):
    _, closed, seen, _ = actions
    graph, registry = _graph(closed)
    result = await Scheduler(graph, MemoryCheckpointer(), _app(), registry=registry).run(run_id="run-c")
    assert result.status is not RunStatus.COMPLETED
    assert "door_closed" in str(result.error) or closed in str(result.error)
    assert seen == []
