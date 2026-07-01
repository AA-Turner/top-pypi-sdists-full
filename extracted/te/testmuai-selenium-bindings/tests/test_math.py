"""Tests for testmu_selenium._helpers.math — math expression tree evaluation."""
import pytest

from testmu_selenium._helpers.math import evaluate_math
from testmu_selenium._vars import set_var, _variable_store


@pytest.fixture(autouse=True)
def _reset_vars():
    _variable_store.clear()
    yield
    _variable_store.clear()


def test_evaluate_math_simple_addition():
    result = evaluate_math({"operator": "add", "operands": ["1", "2", "3"]})
    assert result == 6.0


def test_evaluate_math_subtract_two_operands():
    result = evaluate_math({"operator": "subtract", "operands": ["10", "3"]})
    assert result == 7.0


def test_evaluate_math_subtract_rejects_three_operands():
    with pytest.raises(ValueError, match="exactly 2 operands"):
        evaluate_math({"operator": "subtract", "operands": ["10", "3", "1"]})


def test_evaluate_math_resolves_variable_placeholder():
    set_var("price", 100)
    set_var("tax", 8)
    result = evaluate_math({"operator": "add", "operands": ["{{price}}", "{{tax}}"]})
    assert result == 108.0


def test_evaluate_math_nested_tree():
    tree = {
        "operator": "multiply",
        "operands": [
            {"operator": "add", "operands": ["1", "2"]},
            "3",
        ],
    }
    assert evaluate_math(tree) == 9.0


def test_evaluate_math_division_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        evaluate_math({"operator": "divide", "operands": ["10", "0"]})
