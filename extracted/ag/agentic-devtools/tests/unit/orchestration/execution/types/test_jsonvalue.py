"""Tests for JSONValue type alias usage."""

from agentic_devtools.orchestration.execution.types import JSONValue


class TestJSONValue:
    def test_str_is_valid(self) -> None:
        value: JSONValue = "hello"
        assert isinstance(value, str)

    def test_int_is_valid(self) -> None:
        value: JSONValue = 42
        assert isinstance(value, int)

    def test_float_is_valid(self) -> None:
        value: JSONValue = 3.14
        assert isinstance(value, float)

    def test_bool_is_valid(self) -> None:
        value: JSONValue = True
        assert isinstance(value, bool)

    def test_none_is_valid(self) -> None:
        value: JSONValue = None
        assert value is None

    def test_list_is_valid(self) -> None:
        value: JSONValue = [1, "two", None, True]
        assert isinstance(value, list)

    def test_dict_is_valid(self) -> None:
        value: JSONValue = {"key": "value", "num": 42}
        assert isinstance(value, dict)

    def test_nested_structure(self) -> None:
        value: JSONValue = {
            "users": [{"name": "Alice", "active": True}],
            "count": 1,
        }
        assert isinstance(value, dict)
        assert isinstance(value["users"], list)
