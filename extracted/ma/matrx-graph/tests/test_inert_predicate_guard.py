"""W58 — a sandbox predicate may never be INERT.

The production incident (2026-09-12 16:37Z, run
5f461187-32ba-4e6a-9ef8-5b5640677dd7, "Watson Parenting Adviser" v43): a
hand-built citation gate — ``data.transform`` lifts the cited rule ids, a
``data.filter`` is supposed to KEEP the ids that are NOT in the rulebook, and a
``data.assert`` stops the run when anything was kept. The filter reported
``kept: 14, dropped: 0`` over 14 ids that were ALL in its own 200-id list, and a
perfectly correct run was refused with "cited a rule that does not exist".

The predicate, recovered verbatim from the authoring tool_trace, was::

    ('|' + str(inputs) + '|') not in '|psychological-care-first|…|'

Nothing about it is illegal: ``str`` is a safe helper, ``in`` over two strings
is legal, the AST gate passes it. It was INERT. ``data.filter`` binds a non-dict
item as ``{"value": item}``, so ``str(inputs)`` is ``"{'value': 'only-restraint-
calls-out-rage'}"`` — never a substring of the pipe-fenced list — and ``not in``
answered True for every id that could ever exist.

The author's follow-up "fix", ``inputs in [...]``, is the same defect with the
sign flipped: a dict is never in a list of strings, so it answers False for
every item and the gate stops gating without anyone noticing.

These tests use the REAL recovered predicate and the REAL 14 cited ids from that
run (``tests/fixtures/watson_rulebook_ids.json``), not manufactured data.
"""

from __future__ import annotations

import json
import pathlib

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
from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import bind_item, safe_eval, uses_bare_inputs

from tests._fixtures import make_app_context

_FIXTURE = json.loads(
    (pathlib.Path(__file__).parent / "fixtures" / "watson_rulebook_ids.json").read_text()
)
RULEBOOK_IDS: list[str] = _FIXTURE["rulebook_ids"]
CITED_IDS: list[str] = _FIXTURE["cited_ids"]

# The v43 predicate, rebuilt exactly as the tool_trace recorded it.
V43_PREDICATE = "('|' + str(inputs) + '|') not in '|" + "|".join(RULEBOOK_IDS) + "|'"
# The v44 "fix" that is live on the definition to this day.
V44_PREDICATE = "inputs in [" + ",".join(repr(i) for i in RULEBOOK_IDS) + "]"
# What the author actually meant.
CORRECT_PREDICATE = "('|' + inputs['value'] + '|') not in '|" + "|".join(RULEBOOK_IDS) + "|'"


def test_the_incident_data_is_the_real_thing() -> None:
    """Every cited id IS in the rulebook — so an honest gate keeps NOTHING."""
    assert len(RULEBOOK_IDS) == 200
    assert len(CITED_IDS) == 14
    assert [c for c in CITED_IDS if c not in RULEBOOK_IDS] == []


# --------------------------------------------------------------------------
# 1. The defect, demonstrated: the raw sandbox still evaluates both predicates
#    to a constant. This is what the guard below exists to stop from reaching a
#    run — it is the "proven failing" half, kept permanently so the guard can
#    never be quietly deleted without this failure reappearing in the suite.
# --------------------------------------------------------------------------


def test_v43_predicate_is_inert_against_the_raw_wrapper() -> None:
    verdicts = {safe_eval(V43_PREDICATE, {"value": i}) for i in CITED_IDS}
    assert verdicts == {True}, "the v43 predicate kept all 14 — exactly the incident"


def test_v44_predicate_is_inert_in_the_other_direction() -> None:
    verdicts = {safe_eval(V44_PREDICATE, {"value": i}) for i in CITED_IDS}
    assert verdicts == {False}, "the live 'fix' drops all 14 — it never gates"
    # And it drops a HALLUCINATED id just as happily, which is the whole point:
    # the gate cannot catch the thing it was built to catch.
    assert safe_eval(V44_PREDICATE, {"value": "a-rule-watson-invented"}) is False


# --------------------------------------------------------------------------
# 2. The guard: the same predicates now FAIL the step, naming the construct.
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("label", "predicate"),
    [("v43", V43_PREDICATE), ("v44-live", V44_PREDICATE)],
)
def test_bind_item_refuses_bare_inputs_over_a_scalar(label: str, predicate: str) -> None:
    with pytest.raises(ExecutionError) as exc:
        bind_item(predicate, CITED_IDS[0], where="data.filter: item 0 of 14")
    message = str(exc.value)
    assert "reads `inputs` as a whole value" in message
    assert "inputs['value']" in message
    assert "SAME answer for every payload" in message
    assert "data.filter: item 0 of 14" in message


def test_bind_item_allows_bare_inputs_over_a_dict_item() -> None:
    """A dict item binds as itself — bare `inputs` is honest there."""
    item = {"rule_id": "only-two-inborn-fears"}
    assert bind_item("len(inputs) > 0", item, where="data.filter") is item


def test_bind_item_allows_subscripted_inputs_over_a_scalar() -> None:
    assert bind_item("inputs['value'] > 2", 5, where="data.filter") == {"value": 5}


@pytest.mark.parametrize(
    ("expr", "bare"),
    [
        ("inputs['value'] > 2", False),
        ("inputs['a']['b'] == inputs['c']", False),
        ("str(inputs)", True),
        ("inputs in ['a']", True),
        ("inputs == 'x'", True),
        ("len(inputs) > 0", True),
        ("inputs['a'] if inputs else 1", True),
    ],
)
def test_uses_bare_inputs(expr: str, bare: bool) -> None:
    assert uses_bare_inputs(expr) is bare


# --------------------------------------------------------------------------
# 3. The guard through the real node, and the gate that actually works.
# --------------------------------------------------------------------------


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def _run_filter(predicate: str, items: list) -> tuple[RunStatus, dict, str]:
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "check_case_ids",
                    "type": "data.filter",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {"predicate": predicate},
                        # Declared inputs (W68); the run delivers the same items.
                        "inputs": {"items": items},
                    },
                }
            ],
            "edges": [],
        }
    )
    registry = _registry()
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    state = await scheduler.run(run_id="t-inert-predicate", inputs={"items": items})
    output = (state.last_outputs or {}).get("check_case_ids") or {}
    blob = json.dumps(state, default=str).replace("\\", "")
    return state.status, output, blob


async def test_incident_predicate_now_fails_the_step_instead_of_keeping_14() -> None:
    status, output, blob = await _run_filter(V43_PREDICATE, list(CITED_IDS))
    assert status is not RunStatus.COMPLETED, "an inert predicate must never complete"
    assert output.get("kept") != 14
    assert "reads `inputs` as a whole value" in blob
    assert "inputs['value']" in blob


async def test_live_v44_predicate_also_fails_the_step() -> None:
    status, output, blob = await _run_filter(V44_PREDICATE, list(CITED_IDS))
    assert status is not RunStatus.COMPLETED
    assert output.get("dropped") != 14
    assert "inputs['value']" in blob


async def test_the_correct_gate_passes_clean_citations_and_catches_an_invented_one() -> None:
    status, output, _ = await _run_filter(CORRECT_PREDICATE, list(CITED_IDS))
    assert status is RunStatus.COMPLETED
    assert (output["kept"], output["dropped"]) == (0, 14)

    hallucinated = [*CITED_IDS, "a-rule-watson-invented"]
    status, output, _ = await _run_filter(CORRECT_PREDICATE, hallucinated)
    assert status is RunStatus.COMPLETED
    assert output["items"] == ["a-rule-watson-invented"]
    assert (output["kept"], output["dropped"]) == (1, 14)


# --------------------------------------------------------------------------
# 4. The CHECK-TIME warning: a predicate that answers the same for every
#    sample item is reported before a run is ever spent on it.
# --------------------------------------------------------------------------


def _filter_node(predicate: str):
    from matrx_graph.types.definition import NodeDef

    return NodeDef.model_validate(
        {
            "id": "check_case_ids",
            "type": "data.filter",
            "position": {"x": 0, "y": 0},
            "data": {"config": {"predicate": predicate}},
        }
    )


def test_dry_run_reports_the_inert_predicate_against_the_sample() -> None:
    from matrx_graph.dry_run import _check_predicate_against_sample

    msgs = _check_predicate_against_sample(
        _filter_node(V43_PREDICATE), {"items": list(CITED_IDS)}, "predicate"
    )
    assert len(msgs) == 1
    assert "not evaluable against sample item 0 of 14" in msgs[0]
    assert "inputs['value']" in msgs[0]


def test_dry_run_reports_a_predicate_that_is_constant_over_a_varied_sample() -> None:
    """Legal, evaluable, and still testing nothing — the warning leg."""
    from matrx_graph.dry_run import _check_predicate_against_sample

    msgs = _check_predicate_against_sample(
        _filter_node("inputs['value'] != 'a-rule-nobody-ever-writes'"),
        {"items": list(CITED_IDS)},
        "predicate",
    )
    assert len(msgs) == 1
    assert "returned the same value for every one of the 14 sample items" in msgs[0]
    assert "kept all of them" in msgs[0]


def test_dry_run_is_silent_on_a_predicate_that_actually_discriminates() -> None:
    from matrx_graph.dry_run import _check_predicate_against_sample

    sample = {"items": [*CITED_IDS, "a-rule-watson-invented"]}
    assert (
        _check_predicate_against_sample(_filter_node(CORRECT_PREDICATE), sample, "predicate") == []
    )


def test_dry_run_does_not_cry_constant_over_a_uniform_sample() -> None:
    """One distinct value cannot prove anything — no false alarm."""
    from matrx_graph.dry_run import _check_predicate_against_sample

    msgs = _check_predicate_against_sample(
        _filter_node("inputs['value'] == 'x'"), {"items": ["x", "x", "x"]}, "predicate"
    )
    assert msgs == []
