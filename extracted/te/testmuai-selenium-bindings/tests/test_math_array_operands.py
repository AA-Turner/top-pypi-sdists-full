"""math operations over captured arrays.

A captured variable can hold a list (a table column scraped into {{prices}}),
and the arithmetic is meant to run over its members. `_as_number` rejected a
list outright with "Unsupported operand type: list", so the whole math step
failed.

Port of V2 (Mathmatic._expand_operand_to_numbers).
"""
import pytest

from testmu_selenium._helpers.math import _expand_operand_to_numbers, evaluate_math


class TestExpandOperandToNumbers:
    def test_flattens_a_flat_list(self):
        assert _expand_operand_to_numbers([1, 2, 3]) == [1.0, 2.0, 3.0]

    def test_flattens_nested_lists_recursively(self):
        assert _expand_operand_to_numbers([1, [2, [3, 4]], 5]) == [1.0, 2.0, 3.0, 4.0, 5.0]

    def test_flattens_tuples_too(self):
        assert _expand_operand_to_numbers((1, 2)) == [1.0, 2.0]

    def test_scalar_becomes_a_one_element_list(self):
        assert _expand_operand_to_numbers(5) == [5.0]
        assert _expand_operand_to_numbers("7") == [7.0]

    def test_empty_list_contributes_nothing(self):
        assert _expand_operand_to_numbers([]) == []

    def test_numeric_strings_inside_a_list_are_parsed(self):
        assert _expand_operand_to_numbers(["1", "2"]) == [1.0, 2.0]

    def test_non_numeric_member_still_raises(self):
        with pytest.raises(ValueError, match="Non-numeric operand encountered"):
            _expand_operand_to_numbers([1, "abc"])


class TestEvaluateWithArrayOperands:
    def test_sum_of_a_captured_list(self):
        # The scenario the ticket exists for: "sum the captured list".
        assert evaluate_math({"operator": "add", "operands": [[10, 20, 30]]}) == 60.0

    def test_list_mixed_with_scalars(self):
        assert evaluate_math({"operator": "add", "operands": [[1, 2], 3]}) == 6.0

    def test_multiply_over_a_list(self):
        assert evaluate_math({"operator": "multiply", "operands": [[2, 3, 4]]}) == 24.0

    def test_expansion_feeds_the_arity_check(self):
        # A 3-element list in a 2-operand tree must report a real operand-count
        # error, not the old "Unsupported operand type: list".
        with pytest.raises(ValueError, match="exactly 2 operands"):
            evaluate_math({"operator": "subtract", "operands": [[1, 2, 3]]})

    def test_two_element_list_satisfies_subtract(self):
        assert evaluate_math({"operator": "subtract", "operands": [[10, 4]]}) == 6.0
