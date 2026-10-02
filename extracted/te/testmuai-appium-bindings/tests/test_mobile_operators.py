"""The mobile json_* operator family (legacy perform_assertion parity).

The canonical testmu_helper.evaluation operator set has no json_* rows. The
canonical copies must stay byte-identical to their source, so the package extends
them from its own module instead.

The cases here are deliberately written as NATURAL RECORDED INPUT — real JSON
documents with booleans, nulls, numbers and nested objects — because a comparer that
only handles the string-shaped subset answers those with the wrong boolean.
"""
import pytest

from testmu_appium._evaluation._mobile_operators import compare, evaluate_sub_checks

_OBJ = '{"name": "sid", "roles": ["admin", "dev"], "count": 3}'
_ARR = '["a", "b", "c"]'
#: A real boolean, a real null and a nested object — none of which Python spells the
#: way JSON does.
_TYPED = '{"active": true, "disabled": false, "note": null, "score": 4, "meta": {"a": 1}}'


@pytest.mark.parametrize(
    "actual,expected,operator,result",
    [
        # json_key_exists
        (_OBJ, "name", "json_key_exists", True),
        (_OBJ, "missing", "json_key_exists", False),
        ("not json", "name", "json_key_exists", False),
        (_ARR, "name", "json_key_exists", False),
        (_TYPED, "note", "json_key_exists", True),
        # json_keys_count
        (_OBJ, "3", "json_keys_count", True),
        (_OBJ, "2", "json_keys_count", False),
        ("not json", "1", "json_keys_count", False),
        (_OBJ, "three", "json_keys_count", False),
        # json_array_length
        (_ARR, "3", "json_array_length", True),
        (_ARR, "2", "json_array_length", False),
        (_OBJ, "3", "json_array_length", False),
        ("[]", "0", "json_array_length", True),
        # json_array_contains
        (_ARR, "b", "json_array_contains", True),
        (_ARR, "z", "json_array_contains", False),
        ("[1, 2, 3]", "2", "json_array_contains", True),
        (_OBJ, "sid", "json_array_contains", False),
        # json_value_equals — dotted path into the document
        (_OBJ, "name=sid", "json_value_equals", True),
        (_OBJ, "name=other", "json_value_equals", False),
        (_OBJ, "roles.0=admin", "json_value_equals", True),
        (_OBJ, "count=3", "json_value_equals", True),
        (_OBJ, "missing=x", "json_value_equals", False),
    ],
)
def test_json_operators(actual, expected, operator, result):
    assert compare(actual, expected, operator) is result


class TestParsedValueSemantics:
    """Values are compared parsed, never as their Python repr ('True', 'None',
    "{'a': 1}")."""

    @pytest.mark.parametrize(
        "expected,result",
        [
            ("active=true", True),
            ("active=false", False),
            ("disabled=false", True),
            ("disabled=true", False),
            ("note=null", True),
            ("note=nope", False),
            ("score=4", True),
            ("score=5", False),
        ],
    )
    def test_booleans_and_nulls_compare_as_json_literals(self, expected, result):
        assert compare(_TYPED, expected, "json_value_equals") is result

    def test_a_nested_object_compares_structurally(self):
        assert compare(_TYPED, 'meta={"a": 1}', "json_value_equals") is True

    def test_a_nested_object_does_not_match_its_python_repr(self):
        assert compare(_TYPED, "meta={'a': 1}", "json_value_equals") is False

    def test_a_bare_expected_value_compares_against_the_whole_document(self):
        assert compare('{"a": 1}', '{"a": 1}', "json_value_equals") is True
        assert compare('{"a": 1}', '{"a": 2}', "json_value_equals") is False

    def test_a_whole_document_null_matches_null(self):
        assert compare("null", "null", "json_value_equals") is True

    def test_an_array_of_booleans_contains_a_boolean(self):
        assert compare("[true, false]", "true", "json_array_contains") is True

    def test_an_array_of_strings_still_contains_the_string_spelling(self):
        """The expected value is plain recorded text; both readings are honoured."""
        assert compare('["true", "other"]', "true", "json_array_contains") is True


class TestBooleansAreNotNumbers:
    """Python's True == 1 would make every one of these the wrong answer."""

    def test_an_array_of_numbers_does_not_contain_true(self):
        assert compare("[1]", "true", "json_array_contains") is False

    def test_an_array_of_numbers_does_not_contain_false(self):
        assert compare("[0]", "false", "json_array_contains") is False

    def test_an_array_of_booleans_does_not_contain_one(self):
        assert compare("[true]", "1", "json_array_contains") is False

    def test_a_boolean_value_does_not_equal_a_number(self):
        assert compare('{"a": true}', "a=1", "json_value_equals") is False

    def test_a_number_value_does_not_equal_a_boolean(self):
        assert compare('{"a": 1}', "a=true", "json_value_equals") is False


class TestFailClosedOnMalformedJson:
    """A document that does not parse is not evidence about its contents."""

    GARBAGE = ["not json", "", "   ", "{oops", "<html>gateway timeout</html>", "undefined"]

    @pytest.mark.parametrize("actual", GARBAGE)
    @pytest.mark.parametrize("operator", sorted({
        "json_key_exists", "json_keys_count", "json_array_length",
        "json_array_contains", "json_value_equals",
    }))
    def test_every_json_operator_is_false_on_garbage(self, actual, operator):
        assert compare(actual, "anything", operator) is False

    @pytest.mark.parametrize("actual", GARBAGE)
    def test_json_value_equals_does_not_fail_open_against_a_none_shaped_expectation(
        self, actual
    ):
        """Unparseable text fails closed, so a failed extraction cannot pass against
        a null-shaped expectation."""
        assert compare(actual, "None", "json_value_equals") is False
        assert compare(actual, "null", "json_value_equals") is False
        assert compare(actual, "a=None", "json_value_equals") is False
        assert compare(actual, "a=null", "json_value_equals") is False

    def test_a_document_that_is_literally_null_is_not_garbage(self):
        """Parsing to None is a real answer; failing to parse is not."""
        assert compare("null", "null", "json_value_equals") is True


def test_web_operators_delegate_to_the_canonical_comparer():
    assert compare("hello world", "world", "contains") is True
    assert compare("10", "3", "gt") is True
    assert compare("a", "b", "equals") is False


def test_unknown_operator_raises_unlike_the_canonical_comparer():
    """Deliberate divergence from canonical _compare's silent-False fall-through:
    "operator not understood" must not read as "assertion failed"."""
    with pytest.raises(ValueError, match="unknown assertion operator"):
        compare("a", "a", "no_such_operator")


def test_evaluate_sub_checks_routes_json_operators():
    result = evaluate_sub_checks(
        "", "and",
        [
            {"extracted_value": _OBJ, "expected_value": "name", "operator": "json_key_exists"},
            {"extracted_value": _ARR, "expected_value": "3", "operator": "json_array_length"},
        ],
    )
    assert result["status"] == "passed"
    assert len(result["sub_results"]) == 2


def test_evaluate_sub_checks_composite_or():
    result = evaluate_sub_checks(
        "", "or",
        [
            {"extracted_value": _OBJ, "expected_value": "missing", "operator": "json_key_exists"},
            {"extracted_value": _ARR, "expected_value": "3", "operator": "json_array_length"},
        ],
    )
    assert result["status"] == "passed"


def test_evaluate_sub_checks_applies_transforms_before_json_compare():
    result = evaluate_sub_checks(
        "", "and",
        [{"extracted_value": f"  {_ARR}  ", "expected_value": "3",
          "operator": "json_array_length", "transforms": ["strip"]}],
    )
    assert result["status"] == "passed"


def test_evaluate_sub_checks_fails_a_malformed_json_document():
    result = evaluate_sub_checks(
        "", "and",
        [{"extracted_value": "<html>error</html>", "expected_value": "a=null",
          "operator": "json_value_equals"}],
    )
    assert result["status"] == "failed"


class TestOperatorVocabularyIsLoud:
    """The canonical comparer's fall-through returns False for an unknown
    operator — a silent wrong-answer. The mobile layer maps the legacy symbol
    vocabulary onto canonical names and raises on anything it cannot map."""

    def test_legacy_symbol_operators_map_to_their_canonical_twins(self):
        assert compare("5", "5", "==") is True
        assert compare("5", "6", "!=") is True
        assert compare("7", "5", ">") is True
        assert compare("5", "5", ">=") is True
        assert compare("3", "5", "<") is True
        assert compare("5", "5", "<=") is True

    def test_an_unknown_operator_raises_instead_of_reading_as_failed(self):
        with pytest.raises(ValueError, match="unknown assertion operator"):
            compare("5", "5", "eq")
        with pytest.raises(ValueError, match="unknown assertion operator"):
            compare("5", "5", "equalz")

    def test_is_null_stays_unmapped_until_a_producer_defines_it(self):
        with pytest.raises(ValueError):
            compare("", "", "is_null")
