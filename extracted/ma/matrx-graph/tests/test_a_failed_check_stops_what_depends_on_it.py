"""A step after a FAILED check does not run on the other branch's inputs alone (Law 4).

THE USE CASE (AI-visibility "Release a panel version", run f308bcea, 2026-10-27): the Safety
Check ``release_ok`` (``data.assert``) failed and its ERROR connection led to a planned step.
``save`` was fed by the check's success path (``parts`` -> ``artifacts`` / ``hash_map``) AND by an
independent branch (``prompts``). The check's normal connections pruned exactly like a condition
that said no, the join counted a pruned connection as resolved, so ``save`` ran on ``prompts``
alone and only failed before writing because a template path happened to be missing. A check
exists to stop what depends on it.

THE RULE: when a step's upstream FAILED (its failure caught by an ERROR connection) the steps
on its normal path, and every step joined to them, do not run; each is reported skipped with
the reason. Unchanged: a ``data.optional`` step's failure prunes like a branch not taken; a
condition that said no prunes and the plain half still runs (the designed join); a recovery
path that rejoins (the check's ERROR connection leads on to the step) runs the step; a For
Each hole is still a hole.

THE BREAKS: the scheduler stops marking a caught failure's pruned connections, the join stops
reading the mark, the mark stops travelling through a pruned step, or the skip is not reported.
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


def _node(nid: str, type_: str, config: dict[str, Any], **data: Any) -> dict[str, Any]:
    return {"id": nid, "type": type_, "position": {"x": 0, "y": 0}, "data": {"config": config, **data}}


def _transform(nid: str, expression: str, **data: Any) -> dict[str, Any]:
    return _node(nid, "data.transform", {"expression": expression}, **data)


def _edge(eid: str, source: str, target: str, **data: Any) -> dict[str, Any]:
    return {"id": eid, "source": source, "target": target, "data": data}


def _definition(
    *, holds: bool, through_mid: bool = False, optional: bool = False, error_edge: bool = True,
    rejoins: bool = False,
) -> Definition:
    """start -> check -> [mid ->] save ; start -> other -> save ; check -error-> note [-> save]."""
    check_data: dict[str, Any] = {"optional": True} if optional else {}
    nodes = [
        _transform("start", f"{{'questions': {3 if holds else 0}}}"),
        _node("check", "data.assert", {"predicate": "inputs['questions'] > 0", "message": SAYS}, **check_data),
        _transform("other", "{'prompts': 2}"),
        _transform("save", "'SAVED'"),
        _transform("note", "'NOTED'"),
    ]
    edges = [
        _edge("a", "start", "check"),
        _edge("o1", "start", "other"),
        _edge("o2", "other", "save", mappings={"prompts": "prompts"}),
    ]
    if through_mid:
        nodes.append(_transform("mid", "{'parts': 1}"))
        edges += [_edge("c1", "check", "mid"), _edge("c2", "mid", "save", mappings={"parts": "parts"})]
    else:
        edges.append(_edge("c1", "check", "save", mappings={"passed": "passed"}))
    if error_edge:
        edges.append(_edge("err", "check", "note", kind="error", mappings={"why": "message"}))
    if rejoins:
        edges.append(_edge("n2", "note", "save", mappings={"noted": "result"}))
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


@pytest.mark.parametrize("through_mid", [False, True], ids=["direct", "through a step after the check"])
async def test_a_failed_check_stops_the_step_joined_to_another_branch(through_mid: bool):
    result, emitter = await _run(_definition(holds=False, through_mid=through_mid), f"blocked-{through_mid}")
    assert result.status is RunStatus.COMPLETED, result.error
    ran = _ran(emitter)
    assert "other" in ran and "note" in ran, ran
    assert "save" not in ran, "save ran on the other branch alone after the check failed"
    assert "mid" not in ran
    skipped = {e["node_id"]: e for e in _events(emitter, "node_skipped")}
    assert "save" in skipped, "the blocked step is not reported"
    reason = skipped["save"].get("reason") or ""
    assert "check" in reason and "failed" in reason, reason
    assert result.stopped == {"reason": "assertion_failed", "says": SAYS, "step": "check"}


async def test_a_check_that_holds_lets_the_join_run_with_both_inputs():
    result, emitter = await _run(_definition(holds=True), "held")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "save" in _ran(emitter)
    assert not _events(emitter, "node_skipped")


async def test_an_optional_step_failure_still_prunes_like_a_branch_not_taken():
    result, emitter = await _run(_definition(holds=False, optional=True, error_edge=False), "optional")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "save" in _ran(emitter), "an optional step's dependents run on their other inputs (designed)"


async def test_a_recovery_path_that_rejoins_runs_the_step():
    result, emitter = await _run(_definition(holds=False, rejoins=True), "rejoins")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "save" in _ran(emitter), "the check's error path leads on to save: the author wired it"


async def test_a_condition_that_said_no_still_runs_the_plain_half():
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
                _edge("c", "start", "save", kind="conditional", condition="inputs['go']",
                      mappings={"go": "go"}),
            ],
        }
    )
    result, emitter = await _run(definition, "conditional")
    assert result.status is RunStatus.COMPLETED, result.error
    assert "save" in _ran(emitter)
    assert not _events(emitter, "node_skipped")


def _warnings(definition: Definition) -> list[str]:
    from matrx_graph import validate_definition

    registry = NodeRegistry()
    register_builtin_nodes(registry)
    result = validate_definition(definition, registry)
    return [i.message for i in result.issues if i.severity == "warning" and "does not run when" in i.message]


@pytest.mark.parametrize(
    ("label", "kwargs", "warned"),
    [
        ("joined to another branch", {}, True),
        ("through a step after the check", {"through_mid": True}, True),
        ("check is optional", {"optional": True, "error_edge": False}, False),
        ("recovery path rejoins", {"rejoins": True}, False),
    ],
)
def test_a_step_joined_to_a_checked_path_is_warned_at_save(label: str, kwargs: dict, warned: bool):
    messages = _warnings(_definition(holds=False, **kwargs))
    if warned:
        assert messages == [
            "'save' does not run when 'check' fails, even though 'other' still arrives. "
            "To run it without 'check', mark 'check' optional."
        ], label
    else:
        assert messages == [], label
