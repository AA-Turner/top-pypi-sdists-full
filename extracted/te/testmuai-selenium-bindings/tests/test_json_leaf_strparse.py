"""V2-parity: json_* assertion operators accept stringified JSON operands.

V2 first attempted json.loads (then ast.literal_eval) on the left operand
before evaluating json_* conditions.  V3 narrowed these checks to require an
actual dict/list, breaking callers whose variable holds a serialised JSON
string — e.g. get_cookies returning '{"name": "session", "value": "abc"}' or
an API response body stored as a string.

FIX: _try_parse_json coerces str → parsed object (json.loads, then
ast.literal_eval fallback) before each json_* branch in _eval_leaf_condition.
A wrong-type-but-valid-JSON operand fails the branch's isinstance guard and
returns False. An UNPARSEABLE operand raises (V2 parity — the ast.literal_eval
failure propagates, matching the playwright-python/java/csharp siblings, rather
than being swallowed to a silent False).
"""
from __future__ import annotations

import pytest

from testmu_selenium.condition import Assertion


def _passthrough(store=None):
    store = store or {}

    def _gv(template, variables=None, *args, **kwargs):
        return store.get(template, template)

    return _gv


def _leaf(op, left, right):
    return {
        "operator": [op],
        "assertion_operands": [],
        "left_operand": left,
        "right_operand": right,
        "operands": [],
    }


def _ev(op, left, right, store=None):
    return Assertion.from_json(_leaf(op, left, right)).evaluate({}, _passthrough(store))[0]


class TestJsonKeyExistsStringParse:
    """json_key_exists must accept a stringified dict as left operand."""

    def test_string_left_key_present(self):
        # A stringified dict must be parsed and matched like a real dict.
        assert _ev("json_key_exists", '{"user_preferences": 1}', "user_preferences") is True

    def test_string_left_key_absent(self):
        assert _ev("json_key_exists", '{"a": 1}', "b") is False

    def test_real_dict_still_works(self):
        # Existing real-dict path must not regress.
        assert _ev("json_key_exists", {"x": 1}, "x") is True

    def test_non_json_string_raises(self):
        # An unparseable operand must raise (V2 parity — not swallowed to False).
        with pytest.raises((ValueError, SyntaxError)):
            _ev("json_key_exists", "not-json", "key")

    def test_wrong_type_valid_json_is_false(self):
        # A valid-JSON array fed to json_key_exists fails the dict guard → False.
        assert _ev("json_key_exists", "[1, 2, 3]", "1") is False


class TestJsonKeysCountStringParse:
    """json_keys_count must accept a stringified dict as left operand."""

    def test_string_left_count_matches(self):
        assert _ev("json_keys_count", '{"a": 1, "b": 2}', 2) is True

    def test_string_left_count_mismatch(self):
        assert _ev("json_keys_count", '{"a": 1}', 2) is False

    def test_real_dict_still_works(self):
        assert _ev("json_keys_count", {"x": 1, "y": 2, "z": 3}, 3) is True


class TestJsonArrayLengthEqualsStringParse:
    """json_array_length_equals must accept a stringified list as left operand."""

    def test_string_left_length_matches(self):
        assert _ev("json_array_length_equals", '["x", "y", "z"]', 3) is True

    def test_string_left_length_mismatch(self):
        assert _ev("json_array_length_equals", '["x"]', 3) is False

    def test_real_list_still_works(self):
        assert _ev("json_array_length_equals", ["a", "b"], 2) is True

    def test_non_json_string_raises(self):
        with pytest.raises((ValueError, SyntaxError)):
            _ev("json_array_length_equals", "not-json", 1)

    def test_wrong_type_valid_json_no_false_pass(self):
        # A size-2 dict must NOT satisfy json_array_length_equals==2.
        assert _ev("json_array_length_equals", '{"a": 1, "b": 2}', 2) is False


class TestJsonArrayContainsStringParse:
    """json_array_contains must accept a stringified list as left operand."""

    def test_string_left_element_present(self):
        assert _ev("json_array_contains", '["apple", "banana"]', "banana") is True

    def test_string_left_element_absent(self):
        assert _ev("json_array_contains", '["apple"]', "banana") is False

    def test_real_list_still_works(self):
        assert _ev("json_array_contains", ["a", "b"], "a") is True


class TestJsonValueEqualsStringParse:
    """json_value_equals must accept a stringified dict as left operand."""

    def test_string_left_value_matches(self):
        assert _ev("json_value_equals", '{"color": "blue"}', ["color", "blue"]) is True

    def test_string_left_value_mismatch(self):
        assert _ev("json_value_equals", '{"color": "red"}', ["color", "blue"]) is False

    def test_real_dict_still_works(self):
        assert _ev("json_value_equals", {"k": "v"}, ["k", "v"]) is True


class TestJsonValueEqualsRightOperandNotParsed:
    """Only the LEFT operand is coerced — the [key, value] pair is used as-is.

    playwright-python (``_json_coerce(left)``), java (``parseJsonOperand(left)``)
    and csharp all parse the container operand only; the right operand is
    type-checked with an isinstance guard and never re-parsed. Parsing it here
    too made the verdict language-dependent and turned a malformed right operand
    into an uncaught raise instead of a plain False.
    """

    def test_stringified_pair_does_not_satisfy_the_guard(self):
        # Siblings: isinstance('["color", "blue"]', (list, tuple)) is False -> False.
        # Parsing it would have made selenium-python alone return True.
        assert _ev("json_value_equals", '{"color": "blue"}', '["color", "blue"]') is False

    def test_non_json_right_operand_returns_false_not_raises(self):
        # ast.literal_eval("blue") raises ValueError; siblings just fail the
        # isinstance guard. A malformed right operand must not crash the run.
        assert _ev("json_value_equals", '{"color": "blue"}', "blue") is False

    def test_tuple_pair_still_accepted(self):
        assert _ev("json_value_equals", {"k": "v"}, ("k", "v")) is True

    def test_wrong_length_pair_is_false(self):
        assert _ev("json_value_equals", {"k": "v"}, ["k"]) is False

    def test_unparseable_left_operand_still_raises(self):
        # The left-operand loud-failure contract is unchanged.
        with pytest.raises((ValueError, SyntaxError)):
            _ev("json_value_equals", "not json at all", ["k", "v"])
