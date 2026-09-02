"""The agent-plan validation gate — one test per rule, all issues collected."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from matrx_ai.plans import AgentPlan, AgentPlanValidationError, validate_plan
from matrx_ai.plans.errors import raise_if_issues
from matrx_ai.plans.validate import validate_plan_agents

_A1 = "1fd0cb1f-5b95-49f0-a7f8-79308dc50f58"
_A2 = "9f8eab67-96e4-4a08-9563-7a982f920527"


def _plan(steps: list[dict], inputs: dict | None = None) -> AgentPlan:
    return AgentPlan.model_validate(
        {"name": "t", "reasoning": "r", "inputs": inputs or {}, "steps": steps}
    )


def _step(n: int, **overrides) -> dict:
    step = {"step": n, "agent_id": _A1, "purpose": f"step {n}", "inputs": {}}
    step.update(overrides)
    return step


def _messages(plan: AgentPlan) -> str:
    return "\n".join(i.message for i in validate_plan(plan))


# --- structural rules ---


def test_valid_linear_plan_has_no_issues():
    plan = _plan(
        [
            _step(1, inputs={"user_input": "make cards"}),
            _step(2, inputs={"front": "$steps.1.output.final_text"}),
        ]
    )
    assert validate_plan(plan) == []


def test_duplicate_step_numbers():
    plan = _plan([_step(1), _step(1)])
    assert "duplicate step number" in _messages(plan)


def test_bad_ref_grammar_caught():
    plan = _plan([_step(1, inputs={"x": "$step.1.output"})])
    assert "does not match the grammar" in _messages(plan)


def test_undefined_step_reference():
    plan = _plan([_step(1, inputs={"x": "$steps.9.output"})])
    assert "undefined step 9" in _messages(plan)


def test_self_reference_and_self_dependency():
    plan = _plan([_step(1, inputs={"x": "$steps.1.output"}, depends_on=[1])])
    messages = _messages(plan)
    assert "cannot reference its own output" in messages
    assert "cannot depend on itself" in messages


def test_cycle_detected():
    plan = _plan(
        [
            _step(1, depends_on=[2]),
            _step(2, depends_on=[1]),
        ]
    )
    assert "cycle" in _messages(plan)


def test_item_outside_for_each():
    plan = _plan([_step(1, inputs={"x": "$item.question"})])
    assert "$item is only valid inside a for_each step" in _messages(plan)


def test_cross_step_ref_inside_for_each():
    plan = _plan(
        [
            _step(1),
            _step(2),
            _step(
                3,
                for_each="$steps.1.output.structured_output.cards",
                inputs={"x": "$steps.2.output.final_text"},
            ),
        ]
    )
    assert "may only use $item, $inputs and literals" in _messages(plan)


def test_for_each_inputs_ref_must_be_list():
    plan = _plan(
        [_step(1, for_each="$inputs.topic")],
        inputs={"topic": "chemistry"},
    )
    assert "requires a list" in _messages(plan)

    ok_plan = _plan(
        [_step(1, for_each="$inputs.cards", inputs={"q": "$item.question"})],
        inputs={"cards": [{"question": "Q1"}]},
    )
    assert validate_plan(ok_plan) == []


def test_unresolvable_inputs_ref():
    plan = _plan([_step(1, inputs={"x": "$inputs.missing"})])
    assert "does not resolve against plan.inputs" in _messages(plan)


def test_when_requires_single_dep_and_own_dep_refs():
    multi_dep = _plan(
        [
            _step(1),
            _step(2),
            _step(3, depends_on=[1, 2], when="$steps.1.output.iterations > 0"),
        ]
    )
    assert "exactly one dependency" in _messages(multi_dep)

    foreign_ref = _plan(
        [
            _step(1),
            _step(2),
            _step(3, depends_on=[2], when="$steps.1.output.iterations > 0"),
        ]
    )
    # Referencing step 1 makes it a dependency too → back to the multi-dep error.
    assert "exactly one dependency" in _messages(foreign_ref)


def test_when_predicate_sandbox_rejects_calls():
    plan = _plan(
        [
            _step(1),
            _step(2, depends_on=[1], when="len($steps.1.output.final_text) > 0"),
        ]
    )
    assert "disallowed expression element" in _messages(plan).lower()


def test_valid_when_predicate_passes():
    plan = _plan(
        [
            _step(1),
            _step(
                2,
                depends_on=[1],
                when="$steps.1.output.iterations < 5 and $steps.1.output.final_text != ''",
            ),
        ]
    )
    assert validate_plan(plan) == []


def test_issues_are_collected_not_fail_first():
    plan = _plan(
        [
            _step(1, inputs={"a": "$step.bad", "b": "$steps.9.output", "c": "$inputs.nope"}),
        ]
    )
    assert len(validate_plan(plan)) == 3


def test_raise_if_issues_carries_error_type():
    plan = _plan([_step(1, inputs={"x": "$steps.9.output"})])
    with pytest.raises(AgentPlanValidationError) as exc_info:
        raise_if_issues(validate_plan(plan))
    assert exc_info.value.error_type == "agent_plan_validation_gate"
    assert "undefined step 9" in str(exc_info.value)


# --- agent-aware rules (mocked agx manager) ---


def _agent_row(**overrides: Any) -> SimpleNamespace:
    row = SimpleNamespace(
        created_by="user-1",
        is_active=True,
        is_archived=False,
        name="Test Agent",
        variable_definitions=[
            {"name": "topic", "helpText": "", "required": True},
            {"name": "front", "helpText": "", "required": False},
        ],
        output_schema={"type": "object", "properties": {}},
    )
    for key, value in overrides.items():
        setattr(row, key, value)
    return row


_CTX = SimpleNamespace(user_id="user-1", is_admin=False)


def _mock_manager(rows: dict[str, Any]):
    async def _load(agent_id: str) -> Any:
        if agent_id in rows and rows[agent_id] is not None:
            return rows[agent_id]
        raise LookupError(f"agent {agent_id} not found")

    manager = SimpleNamespace(load_by_id=AsyncMock(side_effect=_load))
    return patch(
        "matrx_ai.db.agx_manager.agx_agent_manager_instance", manager, create=True
    )


async def test_missing_agent_reported():
    plan = _plan([_step(1, inputs={"topic": "x"})])
    with _mock_manager({}):
        issues = await validate_plan_agents(plan, _CTX)
    assert any("could not be loaded" in i.message for i in issues)


async def test_access_denied_for_foreign_private_agent():
    plan = _plan([_step(1, inputs={"topic": "x"})])
    with _mock_manager({_A1: _agent_row(created_by="someone-else")}), patch(
        "matrx_ai.db.agx_manager.agent_viewer_access",
        AsyncMock(return_value=False),
        create=True,
    ):
        issues = await validate_plan_agents(plan, _CTX)
    assert any("do not have access" in i.message for i in issues)


async def test_viewer_and_admin_access_allowed():
    plan = _plan([_step(1, inputs={"topic": "x"})])
    # Viewer-level access (the 2026-08-12 replacement for is_public) allows the run.
    with _mock_manager({_A1: _agent_row(created_by="someone-else")}), patch(
        "matrx_ai.db.agx_manager.agent_viewer_access",
        AsyncMock(return_value=True),
        create=True,
    ):
        assert await validate_plan_agents(plan, _CTX) == []
    admin_ctx = SimpleNamespace(user_id="admin-1", is_admin=True)
    with _mock_manager({_A1: _agent_row(created_by="someone-else")}):
        assert await validate_plan_agents(plan, admin_ctx) == []


async def test_archived_agent_rejected():
    plan = _plan([_step(1, inputs={"topic": "x"})])
    with _mock_manager({_A1: _agent_row(is_archived=True)}):
        issues = await validate_plan_agents(plan, _CTX)
    assert any("inactive or archived" in i.message for i in issues)


async def test_unknown_variable_and_missing_required():
    plan = _plan([_step(1, inputs={"nonexistent": "x"})])
    with _mock_manager({_A1: _agent_row()}):
        issues = await validate_plan_agents(plan, _CTX)
    messages = "\n".join(i.message for i in issues)
    assert "has no variable 'nonexistent'" in messages
    assert "requires variable 'topic'" in messages


async def test_user_input_always_allowed():
    plan = _plan([_step(1, inputs={"user_input": "go", "topic": "x"})])
    with _mock_manager({_A1: _agent_row()}):
        assert await validate_plan_agents(plan, _CTX) == []


async def test_structured_output_ref_requires_output_schema():
    plan = _plan(
        [
            _step(1, inputs={"topic": "x"}),
            _step(
                2,
                agent_id=_A2,
                inputs={"topic": "y", "front": "$steps.1.output.structured_output.cards"},
            ),
        ]
    )
    rows = {_A1: _agent_row(output_schema=None), _A2: _agent_row()}
    with _mock_manager(rows):
        issues = await validate_plan_agents(plan, _CTX)
    assert any("has no output_schema" in i.message for i in issues)


# --- 2026-07-07 live-test regressions ---


def test_null_depends_on_and_inputs_accepted():
    """LLMs emit explicit nulls for 'nothing here' — treat like omission."""
    plan = AgentPlan.model_validate(
        {
            "name": "t",
            "reasoning": "r",
            "steps": [
                {"step": 1, "agent_id": _A1, "purpose": "p", "inputs": None, "depends_on": None}
            ],
        }
    )
    assert plan.steps[0].inputs == {}
    assert plan.steps[0].depends_on == []


def test_list_and_dict_literal_inputs_accepted():
    plan = _plan(
        [
            _step(1, inputs={"kinds": ["example", "mnemonic"], "config": {"depth": 2}}),
        ]
    )
    assert validate_plan(plan) == []


def test_nested_refs_inside_literals_are_validated():
    plan = _plan([_step(1, inputs={"kinds": ["$steps.9.output.final_text", "$step.bad"]})])
    messages = _messages(plan)
    assert "undefined step 9" in messages
    assert "does not match the grammar" in messages


def test_payload_path_rule_catches_bare_cards():
    """The exact 2026-07-07 failure: $steps.1.output.cards passed the gate,
    then step 1's PAID LLM call ran and step 2 died on KeyError: 'cards'."""
    plan = _plan(
        [
            _step(1),
            _step(2, for_each="$steps.1.output.cards", inputs={"front": "$item.front"}),
        ]
    )
    messages = _messages(plan)
    assert "structured_output" in messages
    assert "$steps.1.output.structured_output.cards" in messages


def test_payload_path_rule_on_plain_input_refs():
    plan = _plan([_step(1), _step(2, inputs={"x": "$steps.1.output.answer"})])
    assert "did you mean" in _messages(plan)
    ok = _plan([_step(1), _step(2, inputs={"x": "$steps.1.output.final_text"})])
    assert validate_plan(ok) == []


def test_payload_path_rule_for_fan_out_sources():
    plan = _plan(
        [
            _step(1),
            _step(2, for_each="$steps.1.output.structured_output.cards", inputs={"q": "$item.q"}),
            _step(3, inputs={"n": "$steps.2.output.cards"}),
        ]
    )
    messages = _messages(plan)
    assert "{values, count}" in messages
    ok = _plan(
        [
            _step(1),
            _step(2, for_each="$steps.1.output.structured_output.cards", inputs={"q": "$item.q"}),
            _step(3, inputs={"n": "$steps.2.output.count"}),
        ]
    )
    assert validate_plan(ok) == []


def test_when_refs_get_payload_path_check():
    plan = _plan(
        [
            _step(1),
            _step(2, depends_on=[1], when="$steps.1.output.cards != ''"),
        ]
    )
    assert "structured_output" in _messages(plan)


# --- schema-aware path validation (agent-aware phase) ---

_CARDS_SCHEMA = {
    "name": "flashcard_set_generator",
    "schema": {
        "type": "object",
        "properties": {
            "set_title": {"type": "string"},
            "cards": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "front": {"type": "string"},
                        "back": {"type": "string"},
                    },
                },
            },
        },
    },
}


async def test_schema_path_validated_against_agent_output_schema():
    plan = _plan(
        [
            _step(1, inputs={"topic": "x"}),
            _step(
                2,
                agent_id=_A2,
                inputs={"topic": "y", "front": "$steps.1.output.structured_output.flashcards"},
            ),
        ]
    )
    rows = {_A1: _agent_row(output_schema=_CARDS_SCHEMA), _A2: _agent_row()}
    with _mock_manager(rows):
        issues = await validate_plan_agents(plan, _CTX)
    messages = "\n".join(i.message for i in issues)
    assert "no field 'flashcards'" in messages
    assert "cards" in messages  # available fields listed


async def test_schema_path_valid_deep_path_passes():
    plan = _plan(
        [
            _step(1, inputs={"topic": "x"}),
            _step(
                2,
                agent_id=_A2,
                inputs={
                    "topic": "y",
                    "front": "$steps.1.output.structured_output.cards.0.front",
                },
            ),
        ]
    )
    rows = {_A1: _agent_row(output_schema=_CARDS_SCHEMA), _A2: _agent_row()}
    with _mock_manager(rows):
        assert await validate_plan_agents(plan, _CTX) == []


async def test_for_each_over_non_array_schema_field_rejected():
    plan = _plan(
        [
            _step(1, inputs={"topic": "x"}),
            _step(
                2,
                agent_id=_A2,
                for_each="$steps.1.output.structured_output.set_title",
                inputs={"topic": "y", "front": "$item.front"},
            ),
        ]
    )
    rows = {_A1: _agent_row(output_schema=_CARDS_SCHEMA), _A2: _agent_row()}
    with _mock_manager(rows):
        issues = await validate_plan_agents(plan, _CTX)
    assert any("requires a list" in i.message for i in issues)


def test_pydantic_errors_render_clean():
    from matrx_ai.plans.errors import issues_from_validation_error
    from pydantic import ValidationError

    try:
        AgentPlan.model_validate(
            {"name": "t", "reasoning": "r", "steps": [{"step": "one", "agent_id": _A1}]}
        )
        raise AssertionError("expected ValidationError")
    except ValidationError as exc:
        issues = issues_from_validation_error(exc)
    rendered = "\n".join(i.message for i in issues)
    assert "pydantic.dev" not in rendered
    assert issues


# --- 2026-07-07 adversarial-review regressions ---


def test_deep_path_past_scalar_rejected():
    """$steps.1.output.final_text.foo passed the depth-1 gate and died at
    runtime after step 1's paid call (review finding #3)."""
    plan = _plan([_step(1), _step(2, inputs={"x": "$steps.1.output.final_text.foo"})])
    assert "is a scalar" in _messages(plan)


def test_values_without_item_index_rejected():
    """$steps.2.output.values.final_text (forgot the item index) — the
    near-certain LLM slip next to the taught values.<i>.<field> form."""
    plan = _plan(
        [
            _step(1),
            _step(2, for_each="$steps.1.output.structured_output.cards", inputs={"q": "$item.q"}),
            _step(3, inputs={"x": "$steps.2.output.values.final_text"}),
        ]
    )
    assert "did you forget the item index" in _messages(plan)

    ok = _plan(
        [
            _step(1),
            _step(2, for_each="$steps.1.output.structured_output.cards", inputs={"q": "$item.q"}),
            _step(3, inputs={"x": "$steps.2.output.values.0.final_text"}),
        ]
    )
    assert validate_plan(ok) == []


def test_values_item_paths_are_agent_records():
    plan = _plan(
        [
            _step(1),
            _step(2, for_each="$steps.1.output.structured_output.cards", inputs={"q": "$item.q"}),
            _step(3, inputs={"x": "$steps.2.output.values.0.cards"}),
        ]
    )
    assert "structured_output" in _messages(plan)  # did-you-mean hint fires per item too


def test_count_is_scalar():
    plan = _plan(
        [
            _step(1),
            _step(2, for_each="$steps.1.output.structured_output.cards", inputs={"q": "$item.q"}),
            _step(3, inputs={"x": "$steps.2.output.count.total"}),
        ]
    )
    assert "'count' is a scalar" in _messages(plan)


def test_nonfinite_floats_rejected():
    plan = _plan(
        [_step(1, inputs={"x": float("nan"), "nested": [1.0, float("inf")]})],
        inputs={"seed": float("-inf")},
    )
    messages = _messages(plan)
    assert messages.count("non-finite number") == 3


def test_null_plan_inputs_accepted():
    plan = AgentPlan.model_validate(
        {"name": "t", "reasoning": "r", "inputs": None, "steps": [_step(1)]}
    )
    assert plan.inputs == {}


async def test_nested_input_key_named_for_each_is_not_special():
    """A nested input key literally named 'for_each' misfired the
    for_each-must-be-array rule (review finding #4)."""
    plan = _plan(
        [
            _step(1, inputs={"topic": "x"}),
            _step(
                2,
                agent_id=_A2,
                inputs={
                    "topic": "y",
                    "config": {"for_each": "$steps.1.output.structured_output.set_title"},
                },
            ),
        ]
    )
    rows = {_A1: _agent_row(output_schema=_CARDS_SCHEMA), _A2: _agent_row()}
    with _mock_manager(rows):
        issues = await validate_plan_agents(plan, _CTX)
    assert not any("requires a list" in i.message for i in issues)
