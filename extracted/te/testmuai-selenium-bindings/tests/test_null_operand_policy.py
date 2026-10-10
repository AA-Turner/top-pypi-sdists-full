"""TE-24465 / TE-25086 (auteur-utils #927 + #944): null-operand policy.

A resolved-but-null variable must not be str()'d to "None" (making
`contains "one"` pass), collapsed onto falsy values, or crash ordering with a
TypeError. Policy: null equals only null (a typed `null`/`None` literal counts);
other positive operators are False, negated ones True; membership defers to the
real collection.
"""
from __future__ import annotations

import pytest

from testmu_selenium.condition import (
    Assertion,
    AssertionCondition,
    Condition,
    PossibleCondition,
    ResolvedCondition,
    null_operand_verdict,
)

NULL_TOKENS = ("null", "NULL", "Null", " null ", "none", "NONE", "None", "\tNone\n")


def _leaf(cond, left, right):
    inst = Assertion(assertion_operator=cond, left_operand=left, right_operand=right)
    return inst._eval_leaf_condition(cond, left, right)


def _typed_store(store):
    def _gv(template, variables=None, *args, **kwargs):
        return store.get(template, template)
    return _gv


def _cond(op, left, right, store):
    cond = Condition([ResolvedCondition(left, PossibleCondition(op), right)], [])
    result, _ = cond.evaluate({}, _typed_store(store))
    return result


class TestVerdictFunction:
    def test_real_null_equals_typed_null_tokens(self):
        for token in NULL_TOKENS:
            assert null_operand_verdict("equals", None, token) is True
            assert null_operand_verdict("not_equals", None, token) is False

    def test_v2_operator_spellings(self):
        assert null_operand_verdict("==", None, "null") is True
        assert null_operand_verdict("!=", None, "null") is False

    def test_other_strings_are_not_null(self):
        for other in ("nil", "", "0", "abc", "null null"):
            assert null_operand_verdict("equals", None, other) is False
            assert null_operand_verdict("not_equals", None, other) is True

    def test_non_string_operands_do_not_raise(self):
        for other in ([1, 2], (1,), 0, 1, False, True, 3.5, {"a": 1}):
            assert null_operand_verdict("equals", None, other) is False

    def test_membership_defers_to_the_collection(self):
        assert null_operand_verdict("in", None, [None, 1]) is True
        assert null_operand_verdict("in", None, [1, 2]) is False
        assert null_operand_verdict("not_in", None, [1, 2]) is True
        assert null_operand_verdict("contains", [None, "a"], None) is True

    def test_positive_ops_false_negated_true(self):
        assert null_operand_verdict("greater_than", None, "4") is False
        assert null_operand_verdict("contains", None, "on") is False
        assert null_operand_verdict("not_contains", None, "on") is True


class TestAssertionEngine:
    def test_null_contains_one_no_longer_passes(self):
        # str(None) = "None" made contains "one" PASS and not_contains FAIL.
        assert _leaf(AssertionCondition.CONTAINS, None, "one") is False
        assert _leaf(AssertionCondition.NOT_CONTAINS, None, "one") is True

    def test_ordering_against_null_is_false_not_a_crash(self):
        for cond in (AssertionCondition.GREATER_THAN, AssertionCondition.LESS_THAN,
                     AssertionCondition.GREATER_THAN_OR_EQUALS,
                     AssertionCondition.LESS_THAN_OR_EQUALS):
            assert _leaf(cond, None, 4) is False

    def test_null_equals_typed_null(self):
        assert _leaf(AssertionCondition.EQUALS, None, "null") is True
        assert _leaf(AssertionCondition.EQUALS, None, "None") is True
        assert _leaf(AssertionCondition.NOT_EQUALS, None, "null") is False

    def test_null_is_not_a_falsy_value(self):
        for other in ("0", "false", "", 0, False):
            assert _leaf(AssertionCondition.EQUALS, None, other) is False

    def test_length_no_longer_sees_len_of_the_word_none(self):
        assert _leaf(AssertionCondition.LENGTH_EQUALS, None, 4) is False

    def test_plain_string_null_vs_string_null_untouched(self):
        # No real None on either side: the guard never fires.
        assert _leaf(AssertionCondition.EQUALS, "null", "null") is True


class TestConditionEngine:
    def test_null_variable_equals_typed_null(self):
        for token in ("null", "None", "NULL"):
            assert _cond("==", "{{x}}", token, {"{{x}}": None}) is True
            assert _cond("!=", "{{x}}", token, {"{{x}}": None}) is False

    def test_null_is_not_falsy(self):
        for other in ("0", "false", ""):
            assert _cond("==", "{{x}}", other, {"{{x}}": None}) is False

    def test_substring_ops_do_not_match_the_word_none(self):
        assert _cond("contains", "{{x}}", "on", {"{{x}}": None}) is False
        assert _cond("not_contains", "{{x}}", "on", {"{{x}}": None}) is True
        assert _cond("starts_with", "{{x}}", "No", {"{{x}}": None}) is False

    def test_ordering_is_false_rather_than_a_crash(self):
        for op in (">", "<", ">=", "<="):
            assert _cond(op, "{{x}}", "4", {"{{x}}": None}) is False

    def test_non_null_conditions_untouched(self):
        assert _cond("==", "{{x}}", "4", {"{{x}}": 4}) is True
        assert _cond(">", "{{x}}", "4", {"{{x}}": 10}) is True
        assert _cond("contains", "{{x}}", "ell", {"{{x}}": "hello"}) is True
