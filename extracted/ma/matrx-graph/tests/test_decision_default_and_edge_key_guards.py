"""Guards for two shared-engine fixes (Agent Studio rebuild, lane 2A, 2026-10-21).

A. Every ``decision`` gate can time out to its declared default. Before the fix
   the escalation sweeper resumed with ``{"answer": "<default>"}`` and the gate's
   derived schema (``{"answer": {"answers": {...}}}``) refused it forever.
B. An edge key that misspells a field the engine routes on (``source_handle``)
   is refused by validation. Before the fix it was accepted and ignored, so
   every branch handle delivered.
"""

from __future__ import annotations

import pytest

from matrx_graph.decision_spec import (
    DecisionDefaultError,
    decision_schema_hint,
    DecisionSpec,
    default_answer_resume_value,
    default_decision_answer,
)
from matrx_graph.executor.schema_validation import resume_value_validation_errors, validate_instance
from matrx_graph.validation import validate_definition

OFFER = {
    "items": [
        {
            "key": "fit",
            "label": "How to build it",
            "choices": ["pick_one"],
            "options": [
                {"value": "keep_going", "label": "Keep going as one agent"},
                {"value": "workflow", "label": "Build it as a workflow"},
            ],
            "required": True,
        }
    ]
}


def test_a_pick_one_gate_times_out_to_the_named_option() -> None:
    value = default_decision_answer(OFFER, "keep_going")
    assert value == {"answer": {"answers": {"fit": {"verdict": "pick_one", "value": "keep_going"}}}}
    assert validate_instance(decision_schema_hint(DecisionSpec.model_validate(OFFER)), value) == []


def test_a_confirm_items_are_confirmed_by_the_default() -> None:
    spec = {"items": [{"key": "name", "label": "Name", "value": "Acme"}], "min_answers": 1}
    assert default_decision_answer(spec, "yes") == {"answer": {"answers": {"name": {"verdict": "confirm"}}}}


def test_a_an_unsettlable_required_item_is_named_never_guessed() -> None:
    with pytest.raises(DecisionDefaultError, match="fit"):
        default_decision_answer(OFFER, "something_else")


def test_a_the_sweeper_shape_satisfies_the_decision_gate_admission() -> None:
    """The exact payload a parked decision gate freezes, run through the one
    helper the sweeper uses, then the engine's resume admission. Old code
    produced {'answer': 'keep_going'} here, which admission refuses."""
    payload = {
        "default_answer": "keep_going",
        "decision": DecisionSpec.model_validate(OFFER).model_dump(mode="json"),
        "schema_hint": decision_schema_hint(DecisionSpec.model_validate(OFFER)),
    }
    value = default_answer_resume_value(payload)
    assert resume_value_validation_errors(payload, value) == []
    assert resume_value_validation_errors(payload, {"answer": "keep_going"}) != []


def test_a_other_presets_keep_the_verbatim_shape() -> None:
    assert default_answer_resume_value({"default_answer": "ok"}) == {"answer": "ok"}
    assert default_answer_resume_value({"default_answer": {"answer": 1}}) == {"answer": 1}
    assert default_answer_resume_value({"default_answer": ""}) is None


def test_a_the_sweeper_uses_the_shared_helper() -> None:
    from aidream.services.human_decisions import sweeper

    payload = {
        "default_answer": "keep_going",
        "decision": DecisionSpec.model_validate(OFFER).model_dump(mode="json"),
    }
    from datetime import UTC, datetime

    answer, provenance, failure, _ = sweeper._decide_by_default(payload, datetime.now(UTC))
    assert failure is None and provenance is not None
    assert answer == {"answer": {"answers": {"fit": {"verdict": "pick_one", "value": "keep_going"}}}}


def _branch_def(edge_extra: dict) -> dict:
    return {
        "version": "1",
        "nodes": [
            {"id": "a", "type": "control.branch", "position": {"x": 0, "y": 0}, "data": {"config": {"expression": "True"}}},
            {"id": "b", "type": "data.transform", "position": {"x": 0, "y": 0}, "data": {"config": {"expression": "{}"}}},
        ],
        "edges": [{"id": "e_ab", "source": "a", "target": "b", **edge_extra}],
    }


def test_b_a_snake_case_handle_key_is_refused_by_name() -> None:
    result = validate_definition(_branch_def({"source_handle": "true"}))
    hits = [i for i in result.issues if i.edge_id == "e_ab" and "source_handle" in i.message]
    assert not result.valid and hits, result.issues
    assert "sourceHandle" in hits[0].message


def test_b_the_camel_case_key_and_canvas_extras_are_accepted() -> None:
    result = validate_definition(_branch_def({"sourceHandle": "true", "animated": True, "style": {}}))
    assert not [i for i in result.issues if "Unknown edge key" in i.message], result.issues
