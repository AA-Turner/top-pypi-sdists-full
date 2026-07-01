"""Export-path V3 templated-gesture resolution (selenium-python binding).

In exported test.py the binding variable store IS populated (generated set_var
calls), so click_modifier['variables'] resolves binding-side via var(), writing
the scalar back onto frequency/duration before validate_click_modifier. Mirrors
the V2 source _handle_click_modifier.
"""
import pytest

from testmu_selenium._vars import set_var, clear_state
from testmu_selenium._helpers.gesture import resolve_click_modifier_variables


@pytest.fixture(autouse=True)
def _clean_store():
    clear_state()
    yield
    clear_state()


def test_multi_click_frequency_template_resolves_native_and_drops_carrier():
    set_var("MultiCount", 5)
    cm = {"kind": "multi_click", "frequency": 2,
          "variables": {"frequency": "{{MultiCount}}"}}
    out = resolve_click_modifier_variables(cm)
    assert out == {"kind": "multi_click", "frequency": 5}
    assert "variables" not in out


def test_long_press_duration_template_resolves():
    set_var("HoldSecs", 2.0)
    cm = {"kind": "long_press", "duration": 0.1,
          "variables": {"duration": "{{HoldSecs}}"}}
    out = resolve_click_modifier_variables(cm)
    assert out == {"kind": "long_press", "duration": 2.0}


def test_no_variables_carrier_is_passthrough():
    cm = {"kind": "right_click"}
    out = resolve_click_modifier_variables(cm)
    assert out == {"kind": "right_click"}


def test_non_dict_is_passthrough():
    assert resolve_click_modifier_variables(None) is None
