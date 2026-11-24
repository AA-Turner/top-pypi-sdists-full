"""A step after a step its 'Only when' said no to does not run on its other inputs (§3.3b).

THE USE CASE (research search as a workflow, L7a, 2026-11-07): the YouTube steps carry
'Only when' (video search on, units granted). When the switch was off they were skipped, yet
the step that joins the web pages and the videos still ran, with the video input simply
missing, so every consumer had to guard each read with ``get()``. 'Only when' says the step
does not run; what reads from it must not run on half its inputs either.

THE RULE: a step SKIPPED by its 'Only when' marks its pruned connections; a join that still
has those fields missing (no connection that delivered brings them) does not run, is reported
skipped with the reason, and the mark travels through every step it prunes. Unchanged: a join
whose other side brings the same input (an if / else, 'If skipped' standing in) runs; a step
that declares ``when_input_skipped: "run"`` runs on what arrived; a plain condition that says
no is a branch not taken and the plain half still runs; a skipped step that would have been
the join's only input prunes the join exactly as before.

THE BREAKS: the conditional edge stops marking an 'Only when' no, the join stops reading the
mark, the mark stops travelling, the rejoin or the declaration stops being honoured, or the
stop is not reported.
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
    validate_definition,
)

from tests._fixtures import FakeEmitter, make_app_context


def _transform(nid: str, expression: str, **data: Any) -> dict[str, Any]:
    return {
        "id": nid,
        "type": "data.transform",
        "position": {"x": 0, "y": 0},
        "data": {"config": {"expression": expression}, **data},
    }


def _edge(eid: str, source: str, target: str, **data: Any) -> dict[str, Any]:
    return {"id": eid, "source": source, "target": target, "data": data}


def _definition(
    *,
    go: bool,
    through_mid: bool = False,
    declared: bool = False,
    if_skipped: bool = False,
    rejoin: bool = False,
) -> Definition:
    """start -> videos (Only when go) -> [mid ->] merge ; start -> web -> merge."""
    videos: dict[str, Any] = {"when": "inputs['go']"}
    if if_skipped:
        videos["if_skipped"] = "{'videos': []}"
    merge: dict[str, Any] = {"when_input_skipped": "run"} if declared else {}
    nodes = [
        _transform("start", f"{{'go': {go}}}"),
        _transform("videos", "{'videos': ['v1']}", **videos),
        _transform("web", "{'pages': ['p1']}"),
        _transform(
            "merge",
            "{'pages': inputs['pages'], 'videos': get(inputs, 'videos', 'MISSING')}",
            **merge,
        ),
    ]
    edges = [
        _edge("s1", "start", "videos", mappings={"go": "go"}),
        _edge("s2", "start", "web"),
        _edge("w", "web", "merge", mappings={"pages": "pages"}),
    ]
    if through_mid:
        nodes.append(_transform("mid", "{'videos': inputs['videos']}"))
        edges += [
            _edge("v1", "videos", "mid", mappings={"videos": "videos"}),
            _edge("v2", "mid", "merge", mappings={"videos": "videos"}),
        ]
    else:
        edges.append(_edge("v", "videos", "merge", mappings={"videos": "videos"}))
    if rejoin:
        nodes.append(_transform("no_videos", "{'videos': []}", when="not inputs['go']"))
        edges += [
            _edge("s3", "start", "no_videos", mappings={"go": "go"}),
            _edge("n", "no_videos", "merge", mappings={"videos": "videos"}),
        ]
    return Definition.model_validate({"nodes": nodes, "edges": edges})


async def _run(definition: Definition, run_id: str):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(definition, registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    return await scheduler.run(run_id=run_id), emitter


def _events(emitter: FakeEmitter, name: str) -> list[dict[str, Any]]:
    return [e for k, e in emitter.events if k == "data" and isinstance(e, dict) and e.get("event") == name]


def _ran(emitter: FakeEmitter) -> set[str]:
    return {e["node_id"] for e in _events(emitter, "node_completed")}


def _output(result: Any, node_id: str) -> Any:
    out = result.last_outputs.get(node_id)
    return out.get("result", out) if isinstance(out, dict) else out


@pytest.mark.parametrize("through_mid", [False, True], ids=["direct", "through a step after it"])
async def test_a_skipped_step_stops_the_step_joined_to_another_branch(through_mid: bool):
    result, emitter = await _run(_definition(go=False, through_mid=through_mid), f"skip-{through_mid}")
    assert result.status is RunStatus.COMPLETED, result.error
    ran = _ran(emitter)
    assert "web" in ran
    assert "videos" not in ran and "mid" not in ran
    assert "merge" not in ran, "merge ran with the skipped step's input missing"
    skipped = {e["node_id"]: e for e in _events(emitter, "node_skipped")}
    assert "merge" in skipped, "the stopped step is not reported"
    assert skipped["merge"].get("reason") == "'videos' was skipped, so this step did not run"


async def test_a_step_that_ran_feeds_the_join():
    result, emitter = await _run(_definition(go=True), "ran")
    assert result.status is RunStatus.COMPLETED, result.error
    assert _output(result, "merge") == {"pages": ["p1"], "videos": ["v1"]}
    assert not _events(emitter, "node_skipped")


async def test_a_step_that_declares_it_handles_the_missing_input_runs():
    result, emitter = await _run(_definition(go=False, declared=True), "declared")
    assert result.status is RunStatus.COMPLETED, result.error
    assert _output(result, "merge") == {"pages": ["p1"], "videos": "MISSING"}


async def test_if_skipped_stands_in_for_the_step():
    result, _ = await _run(_definition(go=False, if_skipped=True), "if-skipped")
    assert result.status is RunStatus.COMPLETED, result.error
    assert _output(result, "merge") == {"pages": ["p1"], "videos": []}


@pytest.mark.parametrize("go", [True, False])
async def test_an_if_else_whose_sides_bring_the_same_input_runs(go: bool):
    result, emitter = await _run(_definition(go=go, rejoin=True), f"rejoin-{go}")
    assert result.status is RunStatus.COMPLETED, result.error
    assert _output(result, "merge") == {"pages": ["p1"], "videos": ["v1"] if go else []}
    assert "merge" not in {e["node_id"] for e in _events(emitter, "node_skipped")}


async def test_a_plain_condition_that_said_no_still_runs_the_plain_half():
    definition = Definition.model_validate(
        {
            "nodes": [
                _transform("start", "{'go': False}"),
                _transform("other", "{'prompts': 2}"),
                _transform("save", "'SAVED'"),
            ],
            "edges": [
                _edge("o1", "start", "other"),
                _edge("o2", "other", "save", mappings={"prompts": "prompts"}),
                _edge("c", "start", "save", kind="conditional", condition="inputs['go']", mappings={"go": "go"}),
            ],
        }
    )
    result, emitter = await _run(definition, "conditional")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "save" in _ran(emitter)


def _warnings(definition: Definition) -> list[str]:
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    result = validate_definition(definition, registry)
    return [i.message for i in result.issues if i.severity == "warning" and "is skipped" in i.message]


@pytest.mark.parametrize(
    ("label", "kwargs", "warned"),
    [
        ("joined to another branch", {}, True),
        ("through a step after it", {"through_mid": True}, True),
        ("declares it handles the missing input", {"declared": True}, False),
        ("If skipped stands in", {"if_skipped": True}, False),
        ("an if / else rejoins", {"rejoin": True}, False),
    ],
)
def test_a_step_joined_to_a_skippable_step_is_warned_at_save(label: str, kwargs: dict, warned: bool):
    messages = _warnings(_definition(go=False, **kwargs))
    if warned:
        assert messages == [
            "'merge' does not run when 'videos' is skipped, even though 'web' still arrives. "
            "To run it anyway, set its 'when_input_skipped' to 'run'."
        ], label
    else:
        assert messages == [], label


def test_an_unknown_setting_is_refused():
    definition = _definition(go=False)
    for node in definition.nodes:
        if node.id == "merge":
            node.data["when_input_skipped"] = "maybe"
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    result = validate_definition(definition, registry)
    assert any(i.path == "nodes[merge].data.when_input_skipped" for i in result.issues)
