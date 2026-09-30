"""Tests for testmu_selenium.condition runtime evaluation.

Covers numeric/type-mismatch coercion in Condition comparisons (the until/while
condition path) and strict operator validation. Ensures generated
`Condition(...).evaluate(...)` expressions resolve numeric operands instead of
comparing them as strings.
"""
from __future__ import annotations

import pytest

from testmu_selenium.condition import (
    Assertion,
    AssertionCondition,
    ConcatenationOperator,
    Condition,
    PossibleCondition,
    ResolvedCondition,
)


def _typed_store(store):
    """Return a get_variable_value callable resolving {{name}} to typed values."""
    def _gv(template, variables=None, *args, **kwargs):
        return store.get(template, template)
    return _gv


class TestConditionNumericCoercion:
    def test_greater_than_numeric_strings_compares_numerically_not_lexically(self):
        # "100" > "99" is True numerically but False as a string comparison.
        cond = Condition([ResolvedCondition("100", PossibleCondition(">"), "99")], [])
        result, _ = cond.evaluate({}, _typed_store({}))
        assert result is True

    def test_equals_int_variable_vs_string_literal(self):
        # left resolves to int 3, right is the literal "3" — must compare equal.
        gv = _typed_store({"{{count}}": 3})
        cond = Condition([ResolvedCondition("{{count}}", PossibleCondition("=="), "3")], [])
        result, _ = cond.evaluate({}, gv)
        assert result is True

    def test_greater_than_int_variable_vs_string_literal_no_typeerror(self):
        # 5 > "3" raises TypeError today; coercion must make it 5 > 3 -> True.
        gv = _typed_store({"{{count}}": 5})
        cond = Condition([ResolvedCondition("{{count}}", PossibleCondition(">="), "3")], [])
        result, _ = cond.evaluate({}, gv)
        assert result is True

    def test_genuinely_non_numeric_ordering_still_raises(self):
        # 5 > "abc" is a real type error and must surface, not silently pass.
        gv = _typed_store({"{{count}}": 5})
        cond = Condition([ResolvedCondition("{{count}}", PossibleCondition(">"), "abc")], [])
        with pytest.raises(TypeError):
            cond.evaluate({}, gv)


class TestCompoundConnectorFold:
    """A compound until/while condition (N conditions + N-1 connectors) must
    honour EVERY sub-condition. The fold seeds final_result with results[0]
    then folds results[idx + 1]; a regression reading results[idx] double-counts
    results[0] and silently drops the last condition, so only N-1 of N are
    evaluated (e.g. True AND True AND False -> True)."""

    @pytest.mark.parametrize(
        "name, conditions, connectors, expected",
        [
            # 3-condition AND, all true except the last -> overall must be False.
            # The dropped-last-condition bug evaluates this to True.
            (
                "and three conditions last is false",
                [("5", "==", "5"), ("3", "<", "10"), ("1", "==", "2")],
                [ConcatenationOperator.AND, ConcatenationOperator.AND],
                False,
            ),
            # 3-condition OR, all false except the last -> overall must be True.
            # The dropped-last-condition bug evaluates this to False.
            (
                "or three conditions only last is true",
                [("1", "==", "2"), ("3", "==", "4"), ("5", "==", "5")],
                [ConcatenationOperator.OR, ConcatenationOperator.OR],
                True,
            ),
        ],
    )
    def test_compound_fold_honors_every_condition(self, name, conditions, connectors, expected):
        cond = Condition(
            [ResolvedCondition(left, PossibleCondition(op), right) for left, op, right in conditions],
            connectors,
        )
        result, _ = cond.evaluate({}, _typed_store({}))
        assert result is expected, name


class TestStrictOperatorValidation:
    def test_unknown_possible_condition_operator_raises(self):
        with pytest.raises(ValueError):
            PossibleCondition("definitely_not_an_operator")

    def test_unknown_assertion_condition_operator_raises(self):
        with pytest.raises(ValueError):
            AssertionCondition("definitely_not_an_operator")


class TestAssertionConditionAliases:
    """V2 ``_compare_atomic`` parity: the AssertionCondition lookup accepts both
    spellings for every operator V2 aliases (equals/equal, not_equals/not_equal,
    start_with/starts_with, end_with/ends_with, contains/contain) without changing
    the enum string values or the raise-on-unknown contract."""

    @pytest.mark.parametrize(
        "spelling,expected",
        [
            ("starts_with", AssertionCondition.STARTS_WITH),
            ("ends_with", AssertionCondition.ENDS_WITH),
            ("equal", AssertionCondition.EQUALS),
            ("not_equal", AssertionCondition.NOT_EQUALS),
            ("contain", AssertionCondition.CONTAINS),
        ],
    )
    def test_v2_alias_spellings_resolve(self, spelling, expected):
        assert AssertionCondition(spelling) is expected

    @pytest.mark.parametrize(
        "spelling,expected",
        [
            ("start_with", AssertionCondition.STARTS_WITH),
            ("end_with", AssertionCondition.ENDS_WITH),
            ("equals", AssertionCondition.EQUALS),
            ("not_equals", AssertionCondition.NOT_EQUALS),
            ("contains", AssertionCondition.CONTAINS),
        ],
    )
    def test_canonical_values_still_resolve(self, spelling, expected):
        assert AssertionCondition(spelling) is expected

    def test_alias_is_case_insensitive(self):
        assert AssertionCondition("STARTS_WITH") is AssertionCondition.STARTS_WITH

    def test_unknown_operator_still_raises(self):
        with pytest.raises(ValueError):
            AssertionCondition("nope_op")


class TestConditionBooleanCoercionPreserved:
    """Regression guard: the common `{{flag}} == true` shape must keep working
    after numeric coercion is added."""

    def test_bool_variable_equals_true_literal(self):
        gv = _typed_store({"{{flag}}": True})
        cond = Condition([ResolvedCondition("{{flag}}", PossibleCondition("=="), "true")], [])
        result, _ = cond.evaluate({}, gv)
        assert result is True

    def test_bool_variable_false_unmet(self):
        gv = _typed_store({"{{flag}}": False})
        cond = Condition([ResolvedCondition("{{flag}}", PossibleCondition("=="), "true")], [])
        result, _ = cond.evaluate({}, gv)
        assert result is False


def _passthrough(store):
    """get_variable_value mirroring var(): resolve {{name}} from store, leave
    plain literals (e.g. '#f5f5f5') unchanged."""
    def _gv(template, variables=None, *args, **kwargs):
        return store.get(template, template)
    return _gv


class TestAssertionColorEquality:
    """A background-color/color textual_query returns the computed style
    (`rgb(...)`); the authored expected is hex (`#f5f5f5`) or a name. Same
    colour, different notation — `equals` must compare by colour value, not by
    raw string. RCA: [[v3_color_assertion_format_mismatch]]."""

    def _leaf(self, op, left, right):
        return {
            "operator": [op], "assertion_operands": [],
            "left_operand": left, "right_operand": right, "operands": [],
        }

    def test_equals_rgb_value_matches_hex_literal(self):
        # The exact production failure: rgb(245, 245, 245) vs #f5f5f5.
        gv = _passthrough({"{{base_rate_bg}}": "rgb(245, 245, 245)"})
        leaf = self._leaf("equals", "{{base_rate_bg}}", "#f5f5f5")
        result, _ = Assertion.from_json(leaf).evaluate({}, gv)
        assert result is True

    def test_equals_rgba_opaque_matches_hex_literal(self):
        gv = _passthrough({"{{bg}}": "rgba(245, 245, 245, 1)"})
        leaf = self._leaf("equals", "{{bg}}", "#f5f5f5")
        result, _ = Assertion.from_json(leaf).evaluate({}, gv)
        assert result is True

    def test_equals_three_digit_hex_matches_rgb(self):
        gv = _passthrough({"{{bg}}": "rgb(255, 0, 0)"})
        leaf = self._leaf("equals", "{{bg}}", "#f00")
        result, _ = Assertion.from_json(leaf).evaluate({}, gv)
        assert result is True

    def test_equals_distinct_colors_still_unequal(self):
        # Guard against over-eager normalization: different colours must not match.
        gv = _passthrough({"{{bg}}": "rgb(0, 0, 0)"})
        leaf = self._leaf("equals", "{{bg}}", "#f5f5f5")
        result, _ = Assertion.from_json(leaf).evaluate({}, gv)
        assert result is False

    def test_not_equals_same_color_different_notation_is_false(self):
        gv = _passthrough({"{{bg}}": "rgb(245, 245, 245)"})
        leaf = self._leaf("not_equals", "{{bg}}", "#f5f5f5")
        result, _ = Assertion.from_json(leaf).evaluate({}, gv)
        assert result is False

    def test_equals_non_color_strings_unaffected(self):
        # Regression guard: plain string equality must be untouched.
        gv = _passthrough({"{{name}}": "Active"})
        assert Assertion.from_json(self._leaf("equals", "{{name}}", "Active")).evaluate({}, gv)[0] is True
        assert Assertion.from_json(self._leaf("equals", "{{name}}", "Inactive")).evaluate({}, gv)[0] is False


class TestConditionContainsDirection:
    """CONTAINS / NOT_CONTAINS read "left contains right" (right in left), matching
    Assertion.contains and STARTS_WITH/ENDS_WITH. Regression guard for the inverted
    `str(left) in str(right)` that made `url contains ip` evaluate False (so the
    branch never ran)."""

    def _leaf(self, op, left, right):
        return {
            "operator": [op], "assertion_operands": [],
            "left_operand": left, "right_operand": right, "operands": [],
        }

    def test_contains_substring_present_is_true(self):
        # "url contains ip": the URL contains the substring "ip".
        cond = Condition([ResolvedCondition("https://ipinfo.io", PossibleCondition("contains"), "ip")], [])
        assert cond.evaluate({}, _typed_store({}))[0] is True

    def test_contains_substring_absent_is_false(self):
        cond = Condition([ResolvedCondition("https://ipinfo.io", PossibleCondition("contains"), "zzz")], [])
        assert cond.evaluate({}, _typed_store({}))[0] is False

    def test_not_contains_substring_present_is_false(self):
        # The URL DOES contain "ip", so not_contains must be False.
        cond = Condition([ResolvedCondition("https://ipinfo.io", PossibleCondition("not_contains"), "ip")], [])
        assert cond.evaluate({}, _typed_store({}))[0] is False

    def test_not_contains_substring_absent_is_true(self):
        cond = Condition([ResolvedCondition("https://ipinfo.io", PossibleCondition("not_contains"), "zzz")], [])
        assert cond.evaluate({}, _typed_store({}))[0] is True

    def test_contains_resolves_variable_and_strips_quoted_literal(self):
        # Real codegen shape: left is a {{var}} resolving to the URL, right is a
        # quote-wrapped literal 'ip'. _clean_string strips the quotes, then the
        # direction must read "ip" in URL -> True.
        gv = _passthrough({"{{page_url}}": "https://ipinfo.io"})
        cond = Condition([ResolvedCondition("{{page_url}}", PossibleCondition("contains"), "'ip'")], [])
        assert cond.evaluate({}, gv)[0] is True

    def test_condition_contains_agrees_with_assertion_contains(self):
        # Same operands must yield the same result through both evaluators; the
        # Assertion path was already correct, Condition must match it.
        left, right = "https://ipinfo.io", "ip"
        cond_result = Condition([ResolvedCondition(left, PossibleCondition("contains"), right)], []).evaluate({}, _typed_store({}))[0]
        assert_result = Assertion.from_json(self._leaf("contains", left, right)).evaluate({}, _passthrough({}))[0]
        assert cond_result is True
        assert cond_result == assert_result


class TestAssertionBoolStringEquality:
    """A JS step that returns a boolean is stored as Python ``True``/``False``;
    the authored expected operand is the string ``'true'``/``'false'``. Same
    truth value, different type — ``equals`` must normalize bool<->string the
    way V2 does, not fail on ``True == 'true'``."""

    def _leaf(self, op, left, right):
        return {
            "operator": [op], "assertion_operands": [],
            "left_operand": left, "right_operand": right, "operands": [],
        }

    def test_equals_bool_true_matches_string_true(self):
        # The exact production failure: js_isValid is True, expected 'true'.
        gv = _passthrough({"{{js_isValid}}": True})
        result, _ = Assertion.from_json(self._leaf("equals", "{{js_isValid}}", "true")).evaluate({}, gv)
        assert result is True

    def test_equals_bool_false_matches_string_false(self):
        gv = _passthrough({"{{flag}}": False})
        result, _ = Assertion.from_json(self._leaf("equals", "{{flag}}", "false")).evaluate({}, gv)
        assert result is True

    def test_equals_bool_true_does_not_match_string_false(self):
        gv = _passthrough({"{{flag}}": True})
        result, _ = Assertion.from_json(self._leaf("equals", "{{flag}}", "false")).evaluate({}, gv)
        assert result is False

    def test_equals_bool_true_matches_capitalized_string(self):
        # V2 lowercases both sides, so 'True' (authored) also matches.
        gv = _passthrough({"{{flag}}": True})
        result, _ = Assertion.from_json(self._leaf("equals", "{{flag}}", "True")).evaluate({}, gv)
        assert result is True

    def test_not_equals_bool_true_vs_string_true_is_false(self):
        gv = _passthrough({"{{js_isValid}}": True})
        result, _ = Assertion.from_json(self._leaf("not_equals", "{{js_isValid}}", "true")).evaluate({}, gv)
        assert result is False

    def test_equals_string_true_literal_still_passes(self):
        # Regression: a string 'true' vs 'true' was already passing; keep it.
        gv = _passthrough({"{{s}}": "true"})
        result, _ = Assertion.from_json(self._leaf("equals", "{{s}}", "true")).evaluate({}, gv)
        assert result is True


# ---------------------------------------------------------------------------
# List CONTAINS number is membership, not a substring test
#
# Both operands used to be stringified, so the test became a substring match on
# the list's repr: [12, 3] "contains" 2 and [10, 20] "contains" 0 — false
# positives that make a FAILING assertion pass silently (Pepsico sub-division
# columns). Integer-shaped values compare as ints so adjacent integers above
# 2**53 stay distinct.
# ---------------------------------------------------------------------------

class TestNumericListContains:
    def _leaf(self, cond, left, right):
        from testmu_selenium.condition import Assertion, AssertionCondition
        inst = Assertion(assertion_operator=AssertionCondition.CONTAINS,
                         left_operand=left, right_operand=right)
        return inst._eval_leaf_condition(cond, left, right)

    @pytest.mark.parametrize("left,right,expected", [
        ([1, 2, 3], 2, True),
        ([1, 2, 3], 4, False),
        # The regression: substring matches that were silently passing.
        ([12, 3], 2, False),
        ([10, 20], 0, False),
        # String items coerce (a JSON payload whose numbers arrived as strings).
        (["2"], 2, True),
        ([" 7 "], 7, True),
        (["abc"], 2, False),
        ([""], 2, False),
        # Numeric shapes.
        ([1.0], 1, True),
        ([1], 1.0, True),
        ([1.5], 1.5, True),
        ([1.5], 1, False),
        # bool is not a number here: True == 1 is a Python accident.
        ([True], 1, False),
        # Adjacent integers above 2**53 must not collapse onto one float.
        ([9007199254740993], 9007199254740992, False),
        ([9007199254740993], 9007199254740993, True),
        # Empty list contains nothing.
        ([], 1, False),
    ])
    def test_contains(self, left, right, expected):
        from testmu_selenium.condition import AssertionCondition
        assert self._leaf(AssertionCondition.CONTAINS, left, right) is expected

    @pytest.mark.parametrize("left,right,expected", [
        ([1, 2, 3], 2, False),
        ([12, 3], 2, True),
        ([10, 20], 0, True),
    ])
    def test_not_contains_is_the_exact_negation(self, left, right, expected):
        from testmu_selenium.condition import AssertionCondition
        assert self._leaf(AssertionCondition.NOT_CONTAINS, left, right) is expected

    def test_non_list_left_still_uses_substring_semantics(self):
        from testmu_selenium.condition import AssertionCondition
        # A string haystack is unchanged — the numeric path must not hijack it.
        assert self._leaf(AssertionCondition.CONTAINS, "a123b", 123) is True

    def test_non_numeric_right_still_uses_substring_semantics(self):
        from testmu_selenium.condition import AssertionCondition
        assert self._leaf(AssertionCondition.CONTAINS, ["alpha", "beta"], "alpha") is True

    def test_bool_right_is_not_treated_as_numeric(self):
        from testmu_selenium.condition import AssertionCondition
        # Falls through to substring semantics rather than matching 1.
        assert self._leaf(AssertionCondition.CONTAINS, [1], True) is False


class TestNumericListContainsQuotedNumber:
    """ follow-up: a quoted number on the right must behave like a number.

    Authoring emits `contains '1'`, and V3 keeps operand types verbatim, so the
    right operand reaches the comparison as a string. Without coercion the
    element-wise path is skipped and CONTAINS substring-matches the list's repr
    — `['SUB-DIVISION', '1X']` "contains" '1'. These pin the V2 answers, taken
    from running its evaluator in V2 mode.
    """

    def _leaf(self, cond, left, right):
        from testmu_selenium.condition import Assertion
        inst = Assertion(assertion_operator=cond, left_operand=left, right_operand=right)
        return inst._eval_leaf_condition(cond, left, right)

    @pytest.mark.parametrize("left,right,expected", [
        # The reported case: no element is the number 1.
        (["SUB-DIVISION", "1X", "1O", "1B"], "1", False),
        (["SUB-DIVISION", "1X", "1O", "1B"], 1, False),
        # The original false positive, now also reachable with a quoted number.
        ([12, 3], "2", False),
        ([10, 20], "0", False),
        # Genuine members still match, whichever form the needle arrives in.
        (["1", "1X", "10"], "1", True),
        (["1", "1X", "10"], "10", True),
        ([1, 2, 3], "2", True),
        ([1.5, 2.5], "2.5", True),
        ([1.5, 2.5], "2", False),
        # Whitespace and float-equivalent forms, as V2 coerced them.
        ([" 1 ", "2"], "1", True),
        (["1.0"], "1", True),
        # Non-numeric strings are NOT coerced — substring semantics stay.
        (["SUB-DIVISION", "1X"], "1X", True),
        (["alpha", "beta"], "alpha", True),
        (["1", "1X"], "1Z", False),
        # Empty string is not a number: falls through to substring ("" in anything).
        (["1"], "", True),
    ])
    def test_quoted_number_matches_v2(self, left, right, expected):
        from testmu_selenium.condition import AssertionCondition
        assert self._leaf(AssertionCondition.CONTAINS, left, right) is expected
        assert self._leaf(AssertionCondition.NOT_CONTAINS, left, right) is (not expected)

    def test_scalar_numeric_strings_still_compare_as_strings(self):
        """The coercion is scoped to a list left operand: "007" != "7" elsewhere."""
        from testmu_selenium.condition import AssertionCondition
        assert self._leaf(AssertionCondition.EQUALS, "007", "7") is False
