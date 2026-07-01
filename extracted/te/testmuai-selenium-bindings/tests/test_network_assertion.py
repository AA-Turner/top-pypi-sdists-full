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
