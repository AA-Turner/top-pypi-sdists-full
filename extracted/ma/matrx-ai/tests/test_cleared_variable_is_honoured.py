"""A value the person clears is sent as "" and honored; an untouched value falls back (2026-10-16).

Proof case: a saved default "Gold", the person cleared the field, the server still used "Gold"."""

from matrx_ai.agents.variables import AgentVariable, compose_variable_values

DEFS = {"service_tier": AgentVariable(name="service_tier", default_value="Gold")}


def test_cleared_is_empty_not_default() -> None:
    assert compose_variable_values(DEFS, {"service_tier": ""})["service_tier"] == ""


def test_cleared_beats_a_bound_value() -> None:
    out = compose_variable_values(DEFS, {"service_tier": ""}, {"service_tier": "Silver"})
    assert out["service_tier"] == ""


def test_untouched_falls_back_to_default() -> None:
    assert compose_variable_values(DEFS, {})["service_tier"] == "Gold"


def test_null_falls_back_to_default() -> None:
    assert compose_variable_values(DEFS, {"service_tier": None})["service_tier"] == "Gold"


def test_null_falls_back_to_bound_then_default() -> None:
    out = compose_variable_values(DEFS, {"service_tier": None}, {"service_tier": "Silver"})
    assert out["service_tier"] == "Silver"


def test_a_locked_name_ignores_even_a_cleared_client_value() -> None:
    out = compose_variable_values(
        DEFS, {"service_tier": ""}, {"service_tier": "Silver"}, ignore_client={"service_tier"}
    )
    assert out["service_tier"] == "Silver"


def test_a_cleared_multi_select_is_honoured_as_empty() -> None:
    from matrx_ai.agents.variables import compose_variable_values

    class _Decl:
        value = None
        default_value = ["Tubeless sealant"]

    out = compose_variable_values({"parts_on_van": _Decl()}, client={"parts_on_van": []})
    assert out["parts_on_van"] == ""
