"""V2-parity for numeric-vs-string operand comparison in the assertion evaluator.

V2 (UIActions.evaluate_assertion) only coerces operands numerically when EXACTLY
one side is a real int/float and the other a str (an exact TYPE test). When BOTH
operands are strings it compares them RAW and CASE-SENSITIVE -- so "007" != "7"
and "1.0" != "1". The V3 binding used to best-effort float-parse every numeric
looking string operand in _resolve, turning both-string compares into numeric
ones (a silent false-pass). These tests pin the V2 behavior.

string_to_float is currency-tolerant (filters to digits/'.'), not a plain float
parse, so several V2 quirks are intentional and pinned here as parity.
"""
import pytest

from testmu_selenium.condition import Assertion


def _passthrough(store=None):
    store = store or {}
    def _gv(template, variables=None, *args, **kwargs):
        return store.get(template, template)
    return _gv


def _leaf(op, left, right):
    return {"operator": [op], "assertion_operands": [],
            "left_operand": left, "right_operand": right, "operands": []}


def _ev(op, left, right, store=None):
    return Assertion.from_json(_leaf(op, left, right)).evaluate({}, _passthrough(store))[0]


class TestBothStringNoNumericCoercion:
    """Both operands strings -> raw, case-sensitive compare. No float-parse."""

    def test_leading_zeros_not_equal(self):
        assert _ev("equals", "007", "7") is False

    def test_trailing_zero_decimal_not_equal(self):
        assert _ev("equals", "1.0", "1") is False

    def test_versioned_string_not_equal(self):
        assert _ev("equals", "v1.0", "v1") is False

    def test_not_equals_leading_zeros_is_true(self):
        assert _ev("not_equals", "007", "7") is True

    def test_identical_strings_still_equal(self):
        assert _ev("equals", "7", "7") is True


class TestBothStringOrderingIsLexicographic:
    """gt/lt/gte/lte on two strings compare raw (lexicographic), like V2."""

    def test_greater_than_is_lexicographic(self):
        # "10" > "9" is False as strings ('1' < '9'); V2 never coerced ordering.
        assert _ev("greater_than", "10", "9") is False

    def test_less_than_is_lexicographic(self):
        assert _ev("less_than", "10", "9") is True

    def test_gte_equal_strings_true(self):
        assert _ev("greater_than_or_equal", "9", "9") is True


class TestMixedTypeNumericCoercion:
    """Exactly one operand a real int/float, the other a str -> string_to_float
    both, then compare numerically (V2 exact-type coercion)."""

    def test_int_variable_equals_numeric_string(self):
        assert _ev("equals", "{{count}}", "7", store={"{{count}}": 7}) is True

    def test_int_variable_not_equal_padded_string_after_coercion(self):
        # int 7 vs "007" -> string_to_float both -> 7.0 == 7.0 -> True.
        assert _ev("equals", "{{count}}", "007", store={"{{count}}": 7}) is True

    def test_float_variable_equals_decimal_string(self):
        assert _ev("equals", "{{amt}}", "1.0", store={"{{amt}}": 1.0}) is True

    def test_int_variable_gte_numeric_string(self):
        assert _ev("greater_than_or_equal", "{{count}}", "3", store={"{{count}}": 5}) is True

    def test_int_variable_greater_than_numeric_string(self):
        assert _ev("greater_than", "{{count}}", "9", store={"{{count}}": 10}) is True


class TestBothNumericRaw:
    """Both operands real numbers -> compared as-is."""

    def test_int_equals_int(self):
        assert _ev("equals", "{{a}}", "{{b}}", store={"{{a}}": 7, "{{b}}": 7}) is True

    def test_int_greater_than_int(self):
        assert _ev("greater_than", "{{a}}", "{{b}}", store={"{{a}}": 10, "{{b}}": 9}) is True


class TestDeliberateV2Quirks:
    """string_to_float is currency-tolerant; these results are intentional V2
    parity, NOT bugs. A future reader must not 'fix' them."""

    def test_number_equals_currency_string(self):
        # filter yields "7" -> 7.0 -> equal.
        assert _ev("equals", "{{n}}", "$7", store={"{{n}}": 7}) is True

    def test_number_equals_trailing_alpha_string(self):
        # filter yields "7" -> 7.0 -> equal.
        assert _ev("equals", "{{n}}", "7a", store={"{{n}}": 7}) is True

    def test_zero_equals_non_numeric_string(self):
        # filter yields "" -> 0 -> equal. Yes, really. This is V2.
        assert _ev("equals", "{{n}}", "abc", store={"{{n}}": 0}) is True

    def test_multi_dot_residue_raises_loudly(self):
        # string_to_float("v1.2.3") -> a="1.2.3" -> float() raises uncaught.
        # Loud failure is the V2-faithful behavior; do not swallow it.
        with pytest.raises(ValueError):
            _ev("equals", "{{n}}", "v1.2.3", store={"{{n}}": 5})


class TestBoolVsStringAllOperators:
    """V2 lowers bool<->str for EVERY operator (evaluate_assertion:221-223 runs
    before _compare_atomic, outside any operator branch), so ordering compares
    the lowered STRINGS lexicographically. Base a658faa passed True gt "0" via
    the eager float; item 14 must not regress it to a TypeError."""

    def test_true_greater_than_zero_string(self):
        # V2: str(True).lower()="true" vs "0" -> "true" > "0" -> True.
        assert _ev("greater_than", "{{flag}}", "0", store={"{{flag}}": True}) is True

    def test_false_less_than_true_string(self):
        # "false" < "true" lexicographically.
        assert _ev("less_than", "{{flag}}", "true", store={"{{flag}}": False}) is True

    def test_bool_equals_string_unchanged(self):
        assert _ev("equals", "{{flag}}", "true", store={"{{flag}}": True}) is True

    # gte/lte and the reversed (string-left / bool-right) direction: the fix
    # edits four separate ordering branches, so each needs its own pin.
    def test_bool_gte_bool_string(self):
        # "true" >= "true" -> True.
        assert _ev("greater_than_or_equal", "{{flag}}", "true", store={"{{flag}}": True}) is True

    def test_bool_lte_numeric_string(self):
        # "true" <= "0" -> False (lexicographic).
        assert _ev("less_than_or_equal", "{{flag}}", "0", store={"{{flag}}": True}) is False

    def test_string_left_bool_right_greater_than(self):
        # Reversed operands (string literal left, bool right): "true" > "false".
        assert _ev("greater_than", "true", "{{flag}}", store={"{{flag}}": False}) is True

    def test_string_left_bool_right_ordering_no_typeerror(self):
        # str on the left, bool on the right must also normalize, not raise.
        assert _ev("less_than_or_equal", "false", "{{flag}}", store={"{{flag}}": True}) is True

    def test_not_equals_bool_string_unchanged(self):
        assert _ev("not_equals", "{{flag}}", "false", store={"{{flag}}": True}) is True

    def test_both_strings_ordering_still_lexicographic(self):
        # Neither side bool: "007" < "7" stays a raw string compare, no coercion.
        assert _ev("less_than", "007", "7", store=None) is True
