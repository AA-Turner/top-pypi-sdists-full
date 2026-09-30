"""Follow-up to strip IEEE-754 float noise from math results.

Binary floats cannot represent most decimal fractions exactly, so 1.1 + 1.8
evaluates to 2.9000000000000004. An assertion comparing that against the
authored "2.9" then fails on a value the user considers correct.

Port of V2 (Mathmatic._clean_float).
"""
import math

import pytest

from testmu_selenium._helpers.math import _clean_float, evaluate_math


class TestCleanFloat:
    def test_strips_addition_noise(self):
        assert _clean_float(1.1 + 1.8) == 2.9

    def test_strips_multiplication_noise(self):
        assert _clean_float(0.1 * 3) == 0.3

    def test_preserves_genuine_precision(self):
        # 12 decimals is well below float's ~15-16 significant digits.
        assert _clean_float(1.123456789012) == 1.123456789012
        assert _clean_float(0.5) == 0.5
        assert _clean_float(1234.5678) == 1234.5678

    def test_leaves_integers_alone(self):
        assert _clean_float(5) == 5
        assert isinstance(_clean_float(5), int)

    def test_non_float_passes_through(self):
        assert _clean_float("x") == "x"
        assert _clean_float(None) is None


class TestEvaluateStripsNoise:
    def test_add_result_is_clean(self):
        assert evaluate_math({"operator": "add", "operands": [1.1, 1.8]}) == 2.9

    def test_multiply_result_is_clean(self):
        assert evaluate_math({"operator": "multiply", "operands": [0.1, 3]}) == 0.3

    def test_subtract_result_is_clean(self):
        assert evaluate_math({"operator": "subtract", "operands": [0.3, 0.1]}) == 0.2

    def test_the_noise_was_real(self):
        # Guard the guard: prove the raw arithmetic really is noisy, so this
        # test fails loudly if someone removes _clean_float.
        assert 1.1 + 1.8 != 2.9

    def test_nested_tree_is_clean_at_every_level(self):
        tree = {"operator": "add",
                "operands": [{"operator": "add", "operands": [1.1, 1.8]}, 0.1]}
        assert evaluate_math(tree) == 3.0

    def test_large_values_keep_their_magnitude(self):
        assert evaluate_math({"operator": "multiply", "operands": [1e6, 3]}) == 3e6
