"""A run that ended at a failed Safety Check says so at run level — never a bare ``completed``.

THE USE CASE (AI-visibility "Release a panel version", 2026-10-27): a ``data.assert`` checks the
panel before release; when it fails, its ERROR connection leads to a planned step (or a note), and
the release steps after the check never run. The run read ``completed`` and only a review flag on
the step said it had stopped — Law 4, a failure reading as success. Now the run's stop record
(``RunResult.stopped`` → ``workflow.run.metadata.stopped``, and the ``run_completed`` event) names
the failed step and its sentence.

THE BREAKS:
* the scheduler stops recording caught failures, or ``declared_run_stop`` stops reading them
  (first case: ``stopped`` is None instead of the check's record);
* a caught failure whose recovery path rejoined the normal path claims a stop (third case);
* the ``run_completed`` event loses it (the live page would still read "Done").
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from tests._fixtures import FakeEmitter, make_app_context

SAYS = "The panel has no questions yet"


def _node(nid: str, x: int, type_: str, config: dict[str, Any]) -> dict[str, Any]:
    return {"id": nid, "type": type_, "position": {"x": x, "y": 0}, "data": {"config": config}}


def _definition(holds: bool, *, recovery_rejoins: bool) -> Definition:
    edges: list[dict[str, Any]] = [
        {"id": "a", "source": "start", "target": "check", "data": {}},
        {"id": "b", "source": "check", "target": "release", "data": {}},
        {"id": "err", "source": "check", "target": "note_it",
         "data": {"kind": "error", "mappings": {"why": "message"}}},
    ]
    if recovery_rejoins:
        edges.append({"id": "c", "source": "note_it", "target": "release", "data": {}})
    return Definition.model_validate(
        {
            "nodes": [
                _node("start", 0, "data.transform", {"expression": f"{{'questions': {3 if holds else 0}}}"}),
                _node("check", 200, "data.assert",
                      {"predicate": "inputs['questions'] > 0", "message": SAYS}),
                _node("release", 400, "data.transform", {"expression": "'RELEASED'"}),
                _node("note_it", 400, "data.transform", {"expression": "'NOTED'"}),
            ],
            "edges": edges,
        }
    )


@pytest.mark.parametrize(
    ("label", "holds", "rejoins", "expected"),
    [
        ("check failed, release never ran", False, False,
         {"reason": "assertion_failed", "says": SAYS, "step": "check"}),
        ("check held, release ran", True, False, None),
        ("check failed but the recovery path went on to release", False, True, None),
    ],
)
async def test_a_failed_check_stops_the_run_with_its_sentence(label, holds, rejoins, expected):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(_definition(holds, recovery_rejoins=rejoins), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    result = await scheduler.run(run_id=f"check-stop-{label}")
    assert result.status is RunStatus.COMPLETED, (label, result.error)
    assert result.stopped == expected, label
    completed = [e for e in _events(emitter) if e.get("event") == "run_completed"]
    assert completed and completed[-1].get("stopped") == expected, label


def _events(emitter: FakeEmitter) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in getattr(emitter, "events", []):
        payload = item[1] if isinstance(item, tuple) and len(item) > 1 else item
        if hasattr(payload, "model_dump"):
            payload = payload.model_dump(mode="json")
        if isinstance(payload, dict):
            out.append(payload.get("data", payload) if "event" not in payload else payload)
    return out
