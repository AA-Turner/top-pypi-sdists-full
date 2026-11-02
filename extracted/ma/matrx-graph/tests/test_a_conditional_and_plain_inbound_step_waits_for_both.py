"""A step fed by one CONDITIONAL edge and one plain edge runs ONCE, after both resolve (ENGINE_SPEC §3.1-3.3).

Live 2026-10-27 (aidream ``kit.save_output`` run 81a05e96): "Report what was not saved" was fed by the
plan step (plain, mapping ``kind``) and by the save step (conditional, ``held_back_count > 0 or ...``).
It ran twice ("1 of 2 invocations") and the plain-only firing failed with ``KeyError: 'saved'``. The
join rule (§3.3 ``all``): fire when every required edge is delivered or pruned — so the step waits for
the conditional edge; a TRUE condition delivers both inputs into ONE firing, a FALSE one prunes it and the
step runs with the plain input only (its author reads that half with ``.get``).
"""

from __future__ import annotations

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)

from matrx_graph.validation import validate_definition

from tests._fixtures import FakeEmitter, make_app_context


def _node(nid: str, expression: str, **extra) -> dict:
    return {"id": nid, "type": "data.transform", "position": {"x": 0, "y": 0},
            "data": {"config": {"expression": expression}, **extra}}


_UNGUARDED = "{'kind': inputs['kind'], 'n': inputs['saved']['record'][0]}"
_GUARDED = "{'kind': inputs['kind'], 'n': inputs['saved']['record'][0] if 'saved' in inputs else 0}"


def _definition(held_back: int, report: str = _UNGUARDED) -> dict:
    return {
        "nodes": [
            _node("plan", "{'kind': 'quiz', 'output': 'q'}"),
            _node("check", "{'passed': True}"),
            _node("save", f"{{'saved': {{'record': [1]}}, 'held_back_count': {held_back}}}"),
            # Reads the conditional half directly: a plain-only firing would raise KeyError('saved').
            _node("not_saved", report, label="Report what was not saved"),
            _node("result", "{'kind': inputs['kind'], 'saved': inputs['saved']}"),
        ],
        "edges": [
            {"id": "e_plan_check", "source": "plan", "target": "check", "data": {"kind": "data", "mappings": {"output": "output"}}},
            {"id": "e_check_save", "source": "check", "target": "save", "data": {"kind": "data", "mappings": {"checked": "passed"}}},
            {"id": "e_plan_save", "source": "plan", "target": "save", "data": {"kind": "data", "mappings": {"output": "output"}}},
            {"id": "e_save_result", "source": "save", "target": "result", "data": {"kind": "data", "mappings": {"saved": "saved"}}},
            {"id": "e_plan_result", "source": "plan", "target": "result", "data": {"kind": "data", "mappings": {"kind": "kind"}}},
            {"id": "e_save_not_saved", "source": "save", "target": "not_saved",
             "data": {"kind": "conditional", "condition": "inputs['held_back_count'] > 0", "mappings": {"saved": "saved"}}},
            {"id": "e_plan_not_saved", "source": "plan", "target": "not_saved", "data": {"kind": "data", "mappings": {"kind": "kind"}}},
        ],
        "entry_nodes": ["plan"],
    }


async def _run(held_back: int, run_id: str, report: str = _UNGUARDED):
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    graph = compile_graph(Definition.model_validate(_definition(held_back, report)), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(emitter), registry=registry)
    return await scheduler.run(run_id=run_id)


async def test_a_true_condition_delivers_both_inputs_into_one_firing():
    result = await _run(held_back=2, run_id="mixed-join-true")
    assert result.status == RunStatus.COMPLETED, getattr(result, "error", None)
    assert result.last_outputs["not_saved"] == {"kind": "quiz", "n": 1}


async def test_a_false_condition_prunes_its_edge_and_the_step_runs_once_on_the_plain_half():
    result = await _run(held_back=0, run_id="mixed-join-false", report=_GUARDED)
    assert result.status == RunStatus.COMPLETED, getattr(result, "error", None)
    assert result.last_outputs["not_saved"] == {"kind": "quiz", "n": 0}


async def test_an_unguarded_read_of_the_conditional_half_fails_on_a_false_condition():
    """The live failure, reproduced: why the save-time warning below exists."""
    result = await _run(held_back=0, run_id="mixed-join-unguarded")
    assert result.status == RunStatus.ERRORED
    assert "KeyError: 'saved'" in str(result.error)


def test_saving_a_step_that_reads_the_conditional_half_unguarded_is_warned_in_plain_words():
    issues = [i for i in validate_definition(_definition(0)).issues if i.node_id == "not_saved"]
    warned = [i for i in issues if i.edge_id == "e_save_not_saved"]
    assert len(warned) == 1, [i.message for i in issues]
    assert warned[0].severity == "warning"
    assert warned[0].message.startswith("'Report what was not saved' also runs when the condition")
    assert "inputs['saved'] fails" in warned[0].message


def test_a_guarded_read_is_not_warned():
    issues = validate_definition(_definition(0, _GUARDED)).issues
    assert not [i for i in issues if i.edge_id == "e_save_not_saved"], [i.message for i in issues]


def test_a_broadcast_conditional_edge_is_warned_too():
    """Live 2026-10-27 (email unit ``searchset``): the conditional edge carried no mappings (the whole payload), the
    plain one carried ``free_mail``; the step read ``inputs['address']`` and failed on every false condition. The
    first version of this warning only looked at mapped keys, so it said nothing."""
    defn = {
        "nodes": [
            _node("parts", "{'valid': False, 'address': 'a@b.com', 'domain': 'b.com'}"),
            _node("free", "{'free_mail': False}"),
            _node("searchset", "{'q': inputs['address'], 'free': inputs['free_mail']}", label="Search set"),
        ],
        "edges": [
            {"id": "e_parts", "source": "parts", "target": "searchset",
             "data": {"kind": "conditional", "condition": "inputs['valid']"}},
            {"id": "e_free", "source": "free", "target": "searchset", "data": {"kind": "data", "mappings": {"free_mail": "free_mail"}}},
        ],
        "entry_nodes": ["parts", "free"],
    }
    warned = [i for i in validate_definition(defn).issues if i.edge_id == "e_parts"]
    assert len(warned) == 1, [i.message for i in validate_definition(defn).issues]
    assert "inputs['address'] fails" in warned[0].message
    assert warned[0].severity == "warning"
