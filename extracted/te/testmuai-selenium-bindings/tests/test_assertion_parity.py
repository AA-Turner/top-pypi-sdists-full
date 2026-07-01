"""V2-parity for V3 assertion operators beyond equals.

V3 authoring decides pass/fail with V2 semantics, so the V3 runtime evaluator
must match V2 (the V2 condition comparison + text normalization):
- contains / start_with / end_with: case-insensitive + ascii-fold + whitespace
  collapse (not raw case-sensitive substring).
- in / not_in / lower_case / upper_case: supported (were unsupported -> raised).
- type_equals: 'boolean' aliases bool.
- length_equals: a numeric-string operand is treated as the number, not len().

Each test FAILS against the pre-parity implementation.
"""
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


class TestContainsStartsEndsNormalization:
    def test_contains_is_case_insensitive(self):
        assert _ev("contains", "Hello World", "hello") is True

    def test_contains_folds_accents(self):
        assert _ev("contains", "Café Menu", "cafe") is True

    def test_contains_collapses_whitespace(self):
        assert _ev("contains", "a   b", "a b") is True

    def test_contains_negative_still_false(self):
        assert _ev("contains", "Hello", "xyz") is False

    def test_not_contains_case_insensitive(self):
        assert _ev("not_contains", "Hello", "ELL") is False
        assert _ev("not_contains", "Hello", "xyz") is True

    def test_start_with_case_insensitive(self):
        assert _ev("start_with", "Hello", "HE") is True

    def test_end_with_case_insensitive(self):
        assert _ev("end_with", "Hello", "LO") is True


class TestMissingOperators:
    def test_in_list(self):
        assert _ev("in", "b", ["a", "b"]) is True
        assert _ev("in", "z", ["a", "b"]) is False

    def test_in_string_case_insensitive(self):
        assert _ev("in", "ELL", "Hello") is True

    def test_not_in_list(self):
        assert _ev("not_in", "z", ["a", "b"]) is True
        assert _ev("not_in", "b", ["a", "b"]) is False

    def test_lower_case(self):
        assert _ev("lower_case", "abc", "") is True
        assert _ev("lower_case", "Abc", "") is False

    def test_upper_case(self):
        assert _ev("upper_case", "ABC", "") is True
        assert _ev("upper_case", "Abc", "") is False


class TestTypeEqualsBooleanAlias:
    def test_boolean_alias(self):
        assert _ev("type_equals", True, "boolean") is True

    def test_bool_still_works(self):
        assert _ev("type_equals", True, "bool") is True

    def test_str_type(self):
        assert _ev("type_equals", "hello", "str") is True


class TestLengthEqualsNumericOperand:
    def test_string_length(self):
        assert _ev("length_equals", "hello", 5) is True

    def test_string_length_with_string_operand(self):
        # right "5" is float-coerced to 5.0 by _resolve; must still mean length 5.
        assert _ev("length_equals", "hello", "5") is True

    def test_numeric_string_left_treated_as_number(self):
        # V2 are_lengths_equal: "12345".isdigit() -> the number 12345, not len 5.
        assert _ev("length_equals", "12345", "5") is False
        assert _ev("length_equals", "12345", "12345") is True
