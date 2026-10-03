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
