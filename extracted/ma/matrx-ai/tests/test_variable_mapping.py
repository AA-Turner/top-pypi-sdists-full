from typing import Any

import pytest

from matrx_ai.agents.named import VariableVerdictKind, resolve_variable_mapping
from matrx_ai.agents.variables import AgentVariable


def _var(
    name: str, *, required: bool = False, default: Any = None, data_type: str | None = None
) -> AgentVariable:
    payload: dict[str, Any] = {"name": name, "required": required, "default_value": default}
    if data_type:
        payload["dataType"] = data_type
    return AgentVariable.model_validate(payload)


def _kinds(result: Any) -> list[VariableVerdictKind]:
    return [item.verdict for item in result.verdicts]


def test_same_name_is_ok() -> None:
    result = resolve_variable_mapping({"topic": "x"}, {"topic": _var("topic")})
    assert _kinds(result) == [VariableVerdictKind.OK]
    assert result.variables == {"topic": "x"}


def test_rename_is_keyed_by_agent_variable() -> None:
    result = resolve_variable_mapping(
        {"time_of_day": "morning"},
        {"time_in_day": _var("time_in_day")},
        {"time_in_day": {"mapType": "code_value", "target": "time_of_day"}},
    )
    assert _kinds(result) == [VariableVerdictKind.RENAMED]


def test_agent_default_is_preserved() -> None:
    result = resolve_variable_mapping({}, {"tone": _var("tone", default="warm")})
    assert _kinds(result) == [VariableVerdictKind.DEFAULT_USED]
    assert result.variables == {}


def test_optional_unmapped_is_intentionally_blank() -> None:
    result = resolve_variable_mapping({}, {"tone": _var("tone")}, {"tone": {"mapType": "unmapped"}})
    assert _kinds(result) == [VariableVerdictKind.INTENTIONALLY_BLANK]
    assert not result.blocking


def test_spill_is_context_never_turn_text_and_is_caution() -> None:
    """Injection census #28 (2026-10-17): the caller's text is returned exactly as sent."""
    result = resolve_variable_mapping({"topic": "Owls"}, {}, spill={"topic"}, user_input="Research")
    assert result.user_input == "Research"
    assert result.spilled == {"topic": "Owls"}
    assert result.verdicts[0].verdict is VariableVerdictKind.SPILLED_TO_CONTEXT
    assert result.verdicts[0].caution and not result.blocking


def test_drop_is_explicit_developer_illusion() -> None:
    result = resolve_variable_mapping({"user_request": "Owls"}, {})
    assert result.verdicts[0].verdict is VariableVerdictKind.DROPPED
    assert "DEVELOPER ILLUSION" in result.verdicts[0].message
    assert result.verdicts[0].caution and not result.blocking


def test_missing_required_code_value_blocks() -> None:
    result = resolve_variable_mapping({}, {"topic": _var("topic", required=True)})
    assert _kinds(result) == [VariableVerdictKind.MISSING_FROM_CODE]
    assert result.blocking


def test_direct_literal_beats_default() -> None:
    result = resolve_variable_mapping(
        {},
        {"language": _var("language", default="en")},
        {"language": {"mapType": "direct_value", "target": "fr"}},
    )
    assert result.variables == {"language": "fr"}
    assert _kinds(result) == [VariableVerdictKind.OK]


def test_required_unmapped_blocks() -> None:
    result = resolve_variable_mapping(
        {}, {"topic": _var("topic", required=True)}, {"topic": {"mapType": "unmapped"}}
    )
    assert _kinds(result) == [VariableVerdictKind.REQUIRED_UNMAPPED]
    assert result.blocking


def test_lossless_type_mismatch_is_caution_not_blocking() -> None:
    result = resolve_variable_mapping(
        {"count": "12"}, {"count": _var("count", data_type="integer")}
    )
    assert result.variables == {"count": 12}
    assert _kinds(result) == [VariableVerdictKind.TYPE_MISMATCH]
    assert result.verdicts[0].caution and not result.blocking


def test_lossy_type_mismatch_blocks() -> None:
    result = resolve_variable_mapping(
        {"count": "many"}, {"count": _var("count", data_type="integer")}
    )
    assert result.verdicts[0].lossy and result.blocking


def test_prompt_user_is_rejected_server_side() -> None:
    with pytest.raises(ValueError, match="no human present"):
        resolve_variable_mapping(
            {}, {"topic": _var("topic")}, {"topic": {"mapType": "prompt_user"}}
        )


def test_a_multimodal_caller_gets_the_spill_by_name() -> None:
    """A caller passing content blocks gets the spilled values by NAME, to deliver as
    context — nothing is folded into any turn (injection census #28)."""
    result = resolve_variable_mapping(
        {"user_request": "History of sourdough"},
        {},
        spill={"user_request"},
        user_input="Keep it under 10 minutes.",
    )
    assert result.spilled == {"user_request": "History of sourdough"}
    assert result.user_input == "Keep it under 10 minutes."
    assert _kinds(result) == [VariableVerdictKind.SPILLED_TO_CONTEXT]


def test_nothing_spills_when_no_spill_is_declared() -> None:
    result = resolve_variable_mapping({"user_request": "x"}, {})
    assert result.spilled == {}
    assert _kinds(result) == [VariableVerdictKind.DROPPED]
