"""RFC 9535 strict: the same parser behaviour as the TypeScript, Java and C# runtimes.
A bare name, a blank path or a missing `$` is a parse error, never a silent "No match"."""
import pytest

from testmu_selenium.condition import _apply_rfc_json_path

DOC = {"a": 1, "banana": 2, "items": [{"a": 2}, {"a": 0}]}


def test_valid_paths_query_the_document():
    assert _apply_rfc_json_path(DOC, "$.a") == [1]
    assert _apply_rfc_json_path(DOC, "$..a") == [1, 2, 0]
    assert _apply_rfc_json_path(DOC, "$.items[?@.a > 1]") == [{"a": 2}]
    assert _apply_rfc_json_path('{"a": 5}', "$.a") == [5]
    assert _apply_rfc_json_path({"status": 200, "headers": {}, "body": '{"a": 7}'}, "$.a") == [7]


@pytest.mark.parametrize("path", ["banana", "   ", "", ".a", "$banana", "  $.a  ", "$..["])
def test_lenient_forms_are_parse_errors(path):
    with pytest.raises(Exception):
        _apply_rfc_json_path(DOC, path)


# -- JSONPath match_mode ("all" default / "any") -------------------

from testmu_selenium.condition import Assertion

ARGS = '{"args": {"foo1": "bar1", "foo2": "bar2"}}'


def _gv(template, variables=None, *args, **kwargs):
    return template


def _tree_leaf(op, path="$.args.*", match_mode=None):
    leaf = {"operator": [op], "assertion_operands": [], "left_operand": ARGS,
            "right_operand": "bar1", "operands": [], "json_path": path}
    if match_mode is not None:
        leaf["match_mode"] = match_mode
    return leaf


@pytest.mark.parametrize("op,mode,expected", [
    ("contains", "all", False), ("contains", "any", True),
    ("equals", "all", False), ("equals", "any", True), ("equals", " ANY ", True),
    ("equals", None, False), ("equals", "", False), ("equals", "some", False),
])
def test_tree_leaf_match_mode(op, mode, expected):
    result, _ = Assertion.from_json(_tree_leaf(op, match_mode=mode)).evaluate({}, _gv)
    assert result is expected


@pytest.mark.parametrize("mode", ["all", "any"])
def test_tree_leaf_zero_matches_fail_in_both_modes(mode):
    result, _ = Assertion.from_json(
        _tree_leaf("contains", path="$.nothing[*]", match_mode=mode)).evaluate({}, _gv)
    assert result is False


def test_tree_leaf_round_trip_keeps_match_mode():
    assert Assertion.from_json(_tree_leaf("equals", match_mode="any")).to_dict()["match_mode"] == "any"
    assert "match_mode" not in Assertion.from_json(_tree_leaf("equals")).to_dict()
