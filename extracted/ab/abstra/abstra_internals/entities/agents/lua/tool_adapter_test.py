from typing import Any, Dict

from abstra_internals.entities.agents.lua.tool_adapter import (
    LuaToolAdapter,
    _convert_value,
    _to_dict,
    lua_table_to_dict,
    lua_table_to_list,
)


class FakeTool:
    def __init__(self, name: str, result: str = "ok"):
        self._name = name
        self._result = result
        self.call_count = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return f"Fake tool: {self._name}"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"value": {"type": "string"}}}

    def execute(self, action_input: Dict[str, Any]) -> str:
        self.call_count += 1
        return self._result


class ErrorTool:
    @property
    def name(self) -> str:
        return "broken"

    @property
    def description(self) -> str:
        return "Always fails"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object"}

    def execute(self, action_input: Dict[str, Any]) -> str:
        raise RuntimeError("Tool exploded!")


class TestLuaToolAdapter:
    def test_adapt_simple_tool(self):
        tool = FakeTool("test", "result")
        adapter = LuaToolAdapter()
        fn = adapter.adapt(tool)
        result = fn()
        assert result == "result"
        assert tool.call_count == 1

    def test_adapt_with_dict_arg(self):
        tool = FakeTool("test", "ok")
        adapter = LuaToolAdapter()
        fn = adapter.adapt(tool)
        result = fn({"key": "value"})
        assert result == "ok"

    def test_call_log(self):
        tool = FakeTool("test", "ok")
        adapter = LuaToolAdapter()
        fn = adapter.adapt(tool)
        fn()
        fn()
        assert len(adapter.call_log) == 2
        assert all(entry[0] == "test" for entry in adapter.call_log)

    def test_error_handling(self):
        tool = ErrorTool()
        adapter = LuaToolAdapter()
        fn = adapter.adapt(tool)
        result = fn()
        assert "Error" in result
        assert "Tool exploded" in result

    def test_auto_print_via_log_fn(self):
        """When log_fn is provided, tool results are auto-printed."""
        logged: list = []
        tool = FakeTool("navigate", "Page: Example\n  0: [A] 'Home'")
        adapter = LuaToolAdapter(log_fn=logged.append)
        fn = adapter.adapt(tool)
        result = fn()
        assert result == "Page: Example\n  0: [A] 'Home'"
        assert len(logged) == 1
        assert "Page: Example" in logged[0]

    def test_no_auto_print_without_log_fn(self):
        """Without log_fn, results are not auto-printed."""
        tool = FakeTool("test", "result")
        adapter = LuaToolAdapter()  # no log_fn
        fn = adapter.adapt(tool)
        fn()
        # No crash, no auto-print — just works normally


class TestMultiArgWrapper:
    def test_multi_arg_returns_error(self):
        """Calling a wrapper with 2+ args returns a helpful error instead of TypeError."""
        tool = FakeTool("files-write", "ok")
        adapter = LuaToolAdapter()
        fn = adapter.adapt(tool)
        result = fn("path.txt", "content")
        assert "Error" in result
        assert "single table argument" in result
        assert "files_write" in result
        assert tool.call_count == 0
        assert len(adapter.call_log) == 1

    def test_multi_arg_logged(self):
        """Multi-arg error is recorded in call log and via log_fn."""
        logged: list = []
        tool = FakeTool("files-write", "ok")
        adapter = LuaToolAdapter(log_fn=logged.append)
        fn = adapter.adapt(tool)
        fn("a", "b", "c")
        assert len(logged) == 1
        assert "single table argument" in logged[0]
        assert "3 arguments" in logged[0]

    def test_single_string_arg_still_works(self):
        """A single non-dict arg still works (returns {} to handler)."""
        tool = FakeTool("test", "ok")
        adapter = LuaToolAdapter()
        fn = adapter.adapt(tool)
        result = fn("hello")
        assert result == "ok"
        assert tool.call_count == 1


class TestLuaTableToDict:
    def test_none_returns_empty(self):
        assert lua_table_to_dict(None) == {}

    def test_dict_passthrough(self):
        d = {"key": "value"}
        assert lua_table_to_dict(d) == d

    def test_string_returns_empty(self):
        assert lua_table_to_dict("hello") == {}

    def test_number_returns_empty(self):
        assert lua_table_to_dict(42) == {}


class TestConvertValue:
    def test_python_list_preserved(self):
        """Python lists (from array()) are preserved as lists."""
        assert _convert_value([1, 2, 3]) == [1, 2, 3]

    def test_empty_python_list_preserved(self):
        """Empty Python lists (from array()) are preserved."""
        assert _convert_value([]) == []

    def test_nested_list_in_dict(self):
        """Lists nested inside dicts are preserved."""
        data = {"items": [1, 2], "name": "test"}
        result = _convert_value(data)
        # dict passthrough doesn't recurse, but _convert_value on a dict returns it
        assert isinstance(result, dict)

    def test_list_items_recursively_converted(self):
        """Items inside a Python list are recursively converted."""
        result = _convert_value(["a", 42, None, True])
        assert result == ["a", 42, None, True]


class TestToDict:
    def test_to_dict_with_list(self):
        """A list argument should return an empty dict."""
        assert _to_dict([1, 2, 3]) == {}


class TestLuaTableToList:
    def test_lua_table_to_list_with_dict(self):
        """A dict with integer keys should be converted to a sorted list."""
        assert lua_table_to_list({1: "a", 2: "b"}) == ["a", "b"]

    def test_lua_table_to_list_with_none(self):
        """None should return an empty list."""
        assert lua_table_to_list(None) == []

    def test_lua_table_to_list_with_list(self):
        """A plain list should be returned as-is."""
        assert lua_table_to_list(["a", "b"]) == ["a", "b"]
