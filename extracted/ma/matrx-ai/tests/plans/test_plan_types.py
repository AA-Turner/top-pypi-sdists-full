"""AgentPlan schema + reference grammar."""

from __future__ import annotations

import pytest
from matrx_ai.plans import AgentPlan, plan_json_schema
from matrx_ai.plans.types import ParsedRef, parse_ref
from matrx_ai.schema import lint_output_schema
from pydantic import ValidationError

_AGENT = "1fd0cb1f-5b95-49f0-a7f8-79308dc50f58"


def _minimal(**overrides) -> dict:
    plan = {
        "name": "test",
        "reasoning": "because",
        "steps": [
            {"step": 1, "agent_id": _AGENT, "purpose": "do it", "inputs": {"topic": "x"}}
        ],
    }
    plan.update(overrides)
    return plan


def test_minimal_plan_validates():
    plan = AgentPlan.model_validate(_minimal())
    assert plan.steps[0].step == 1
    assert str(plan.steps[0].agent_id) == _AGENT


def test_extra_keys_forbidden():
    with pytest.raises(ValidationError):
        AgentPlan.model_validate(_minimal(workflow_type="sequential"))


def test_steps_bounds():
    with pytest.raises(ValidationError):
        AgentPlan.model_validate(_minimal(steps=[]))
    too_many = [
        {"step": i, "agent_id": _AGENT, "purpose": "p", "inputs": {}}
        for i in range(1, 23)
    ]
    with pytest.raises(ValidationError):
        AgentPlan.model_validate(_minimal(steps=too_many))


@pytest.mark.parametrize(
    ("ref", "expected"),
    [
        ("$inputs.topic", ParsedRef("inputs", None, ("topic",))),
        ("$inputs.cards.0.question", ParsedRef("inputs", None, ("cards", "0", "question"))),
        ("$steps.1.output", ParsedRef("steps", 1, ())),
        (
            "$steps.12.output.structured_output.cards",
            ParsedRef("steps", 12, ("structured_output", "cards")),
        ),
        ("$item", ParsedRef("item", None, ())),
        ("$item.question", ParsedRef("item", None, ("question",))),
    ],
)
def test_ref_grammar_accepts(ref, expected):
    assert parse_ref(ref) == expected


@pytest.mark.parametrize(
    "ref",
    [
        "$step.1.output",          # typo: step vs steps
        "$steps.1",                # missing .output
        "$steps.one.output",       # non-numeric step
        "$inputs",                 # whole-inputs ref not allowed
        "$steps.1.output.cards[]", # wildcards banned
        "$steps.1.output.cards[0]",# bracket indexing banned (use .0.)
        "$items.0",                # not a namespace
        "$item.",                  # trailing dot
    ],
)
def test_ref_grammar_rejects(ref):
    assert parse_ref(ref) is None


def test_plan_json_schema_passes_the_schema_gate():
    result = lint_output_schema(plan_json_schema())
    assert result.ok, [f.message for f in result.errors]
