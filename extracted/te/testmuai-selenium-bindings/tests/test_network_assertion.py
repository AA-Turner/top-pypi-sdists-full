"""Tests for testmu_selenium._helpers.network — assertion tree evaluation."""
import pytest

from testmu_selenium._helpers.network import evaluate_network_assertion
from testmu_selenium._vars import set_var, _variable_store


@pytest.fixture(autouse=True)
def _reset_vars():
    _variable_store.clear()
    yield
    _variable_store.clear()


def test_evaluate_passes_when_equals_matches():
    set_var("response", {"status": 200})
    tree = {
        "operator": "equals",
        "left_operand": "{{response.status}}",
        "right_operand": "200",
    }
    assert evaluate_network_assertion(tree) is True


def test_evaluate_raises_when_assertion_fails():
    set_var("response", {"status": 500})
    tree = {
        "operator": "equals",
        "left_operand": "{{response.status}}",
        "right_operand": "200",
    }
    with pytest.raises(AssertionError):
        evaluate_network_assertion(tree)


def test_evaluate_and_logic():
    set_var("response", {"status": 200, "method": "GET"})
    tree = {
        "operator": "and",
        "operands": [
            {
                "operator": "equals",
                "left_operand": "{{response.status}}",
                "right_operand": "200",
            },
            {
                "operator": "equals",
                "left_operand": "{{response.method}}",
                "right_operand": "GET",
            },
        ],
    }
    assert evaluate_network_assertion(tree) is True


def test_bool_true_equals_string_true_normalized():
    # A resolved boolean True must equal the authored string 'true' (V2 parity),
    # not fail because str(True) == 'True' != 'true'.
    set_var("response", {"ok": True})
    tree = {
        "operator": "equals",
        "left_operand": "{{response.ok}}",
        "right_operand": "true",
    }
    assert evaluate_network_assertion(tree) is True


def test_bool_false_equals_string_false_normalized():
    set_var("response", {"ok": False})
    tree = {
        "operator": "equals",
        "left_operand": "{{response.ok}}",
        "right_operand": "false",
    }
    assert evaluate_network_assertion(tree) is True


def test_bool_true_not_equals_string_true_is_false():
    # not_equals of a boolean True against 'true' must be False -> assertion fails.
    set_var("response", {"ok": True})
    tree = {
        "operator": "not_equals",
        "left_operand": "{{response.ok}}",
        "right_operand": "true",
    }
    with pytest.raises(AssertionError):
        evaluate_network_assertion(tree)


def test_int_equals_numeric_string_still_passes():
    # Regression guard: bool normalization must not break the int-vs-string
    # equality that already works (str coercion path).
    set_var("response", {"status": 200})
    tree = {
        "operator": "equals",
        "left_operand": "{{response.status}}",
        "right_operand": "200",
    }
    assert evaluate_network_assertion(tree) is True
