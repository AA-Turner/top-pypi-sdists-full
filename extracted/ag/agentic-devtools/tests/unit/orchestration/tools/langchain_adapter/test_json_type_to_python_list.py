"""Tests for _json_type_to_python with list-type JSON Schema values."""

import pytest

from agentic_devtools.orchestration.tools.langchain_adapter import _json_type_to_python

langchain_core = pytest.importorskip("langchain_core")


class TestJsonTypeToPythonListType:
    """Tests for _json_type_to_python handling list-form Draft 2020-12 types."""

    def test_string_type_string(self):
        """Single string type returns correct Python type."""
        assert _json_type_to_python("string") is str

    def test_list_type_string_null(self):
        """['string', 'null'] returns str (first non-null entry)."""
        assert _json_type_to_python(["string", "null"]) is str

    def test_list_type_null_string(self):
        """['null', 'string'] returns str (first non-null entry)."""
        assert _json_type_to_python(["null", "string"]) is str

    def test_list_type_integer_null(self):
        """['integer', 'null'] returns int."""
        assert _json_type_to_python(["integer", "null"]) is int

    def test_list_type_only_null(self):
        """['null'] returns str as safe default."""
        assert _json_type_to_python(["null"]) is str

    def test_list_type_empty(self):
        """Empty list returns str as safe default."""
        assert _json_type_to_python([]) is str

    def test_list_type_unknown(self):
        """Unknown type in list returns str as safe default."""
        assert _json_type_to_python(["unknown_type"]) is str

    def test_single_unknown_type_returns_str(self):
        """Unknown single-string type falls back to str."""
        assert _json_type_to_python("unknown_type") is str

    def test_list_with_nested_list_skipped_safely(self):
        """Nested lists in type array are skipped without recursion errors."""
        # [["string"], "null"] — the inner list is skipped, leaving only null → str
        assert _json_type_to_python([["string"], "null"]) is str  # type: ignore[arg-type]

    def test_list_with_nested_list_falls_through_to_valid(self):
        """Nested list entry is skipped; valid string entry is used."""
        assert _json_type_to_python([["string"], "integer"]) is int  # type: ignore[arg-type]

    def test_adapter_does_not_crash_with_list_type_schema(self):
        """to_langchain_tool does not crash when a property uses a list type."""
        from langchain_core.tools import BaseTool

        from agentic_devtools.orchestration.tools.definition import ToolDefinition
        from agentic_devtools.orchestration.tools.executor import ToolExecutor
        from agentic_devtools.orchestration.tools.langchain_adapter import to_langchain_tool
        from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="nullable_tool",
                description="Tool with nullable field",
                category="testing",
                input_schema={
                    "type": "object",
                    "properties": {
                        "name": {"type": ["string", "null"], "description": "Nullable name"},
                        "count": {"type": ["integer", "null"]},
                    },
                    "required": ["name"],
                },
            ),
            fn=lambda name, count=None: {"name": name, "count": count},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        definition = registry.get("nullable_tool")

        # Must not raise TypeError: unhashable type: 'list'
        tool = to_langchain_tool(definition, executor)
        assert isinstance(tool, BaseTool)
        assert tool.name == "nullable_tool"
