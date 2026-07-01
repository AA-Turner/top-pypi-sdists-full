"""Tests for validate_click_modifier — V2 source parity (bounds,
frequency==1 collapse, missing-scalar rejection). Template resolution is the
public resolve_click_modifier_variables' job (see test_gesture_variable_resolution),
NOT validate's — validate operates on the already-resolved scalar."""
import pytest

from testmu_selenium._helpers.gesture import validate_click_modifier
from testmu_selenium import set_var
from testmu_selenium._vars import clear_state


@pytest.fixture(autouse=True)
def _clean_vars():
    clear_state()
    yield
    clear_state()


def test_none_returns_none():
    assert validate_click_modifier(None) is None
    assert validate_click_modifier({}) is None


def test_long_press_in_bounds_passes_through():
    out = validate_click_modifier({"kind": "long_press", "duration": 2.0})
    assert out["kind"] == "long_press"
    assert out["duration"] == 2.0


def test_long_press_below_min_raises():
    with pytest.raises(ValueError):
        validate_click_modifier({"kind": "long_press", "duration": 0.05})


def test_long_press_above_max_raises():
    with pytest.raises(ValueError):
        validate_click_modifier({"kind": "long_press", "duration": 30.5})


def test_multi_click_two_passes():
    out = validate_click_modifier({"kind": "multi_click", "frequency": 2})
    assert out["frequency"] == 2


def test_multi_click_frequency_one_collapses_to_plain():
    # frequency==1 -> clear dict -> plain click (engine treats None as plain)
    assert validate_click_modifier({"kind": "multi_click", "frequency": 1}) is None


def test_multi_click_bool_frequency_rejected():
    with pytest.raises(ValueError):
        validate_click_modifier({"kind": "multi_click", "frequency": True})


def test_multi_click_non_integer_float_rejected():
    with pytest.raises(ValueError):
        validate_click_modifier({"kind": "multi_click", "frequency": 2.5})


def test_multi_click_above_max_raises():
    with pytest.raises(ValueError):
        validate_click_modifier({"kind": "multi_click", "frequency": 21})


def test_right_click_passes_through():
    out = validate_click_modifier({"kind": "right_click"})
    assert out == {"kind": "right_click"}


def test_right_click_with_duration_raises():
    with pytest.raises(ValueError):
        validate_click_modifier({"kind": "right_click", "duration": 2.0})


def test_unknown_kind_raises():
    with pytest.raises(ValueError):
        validate_click_modifier({"kind": "triple_click"})


def test_validate_ignores_variables_carrier_uses_scalar_as_is():
    # Template resolution belongs to resolve_click_modifier_variables (run by every
    # caller BEFORE validate). validate must NOT resolve a leftover `variables`
    # carrier — it operates purely on the already-resolved scalar.
    set_var("HoldSecs", 9.0)
    out = validate_click_modifier(
        {"kind": "long_press", "duration": 2.0, "variables": {"duration": "${HoldSecs}"}}
    )
    assert out["duration"] == 2.0  # scalar used as-is; carrier ignored (not 9.0)


def test_long_press_missing_duration_raises():
    # the code generator never legitimately emits a scalar-less gesture; surface it loudly (not a
    # silent skip / TypeError). 3-surface parity with pw + sel-java.
    with pytest.raises(ValueError):
        validate_click_modifier({"kind": "long_press"})


def test_multi_click_missing_frequency_raises():
    with pytest.raises(ValueError):
        validate_click_modifier({"kind": "multi_click"})


def test_input_dict_not_mutated():
    src = {"kind": "long_press", "duration": 2.0}
    validate_click_modifier(src)
    assert src == {"kind": "long_press", "duration": 2.0}
