"""Tests for @tool_definition decorator and auto_discover."""

from agentic_devtools.orchestration.tools.decorators import (
    _TOOL_DEFINITION_ATTR,
    auto_discover,
    tool_definition,
)
from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestToolDefinitionDecorator:
    """Tests for the @tool_definition decorator."""

    def test_decorator_attaches_metadata(self):
        """Decorator attaches ToolDefinition to function."""

        @tool_definition(
            name="my_tool",
            description="My tool",
            category="testing",
            input_schema={"type": "object", "properties": {}},
            mutating=True,
        )
        def my_func():
            return {"ok": True}

        assert hasattr(my_func, _TOOL_DEFINITION_ATTR)
        defn = getattr(my_func, _TOOL_DEFINITION_ATTR)
        assert isinstance(defn, ToolDefinition)
        assert defn.name == "my_tool"
        assert defn.mutating is True

    def test_decorated_function_still_callable(self):
        """Decorated function remains callable."""

        @tool_definition(
            name="callable_tool",
            description="Callable",
            category="testing",
            input_schema={"type": "object", "properties": {}},
        )
        def my_func():
            return 42

        assert my_func() == 42

    def test_decorator_preserves_explicit_empty_output_schema(self):
        """An explicit empty output schema is preserved as-is."""

        @tool_definition(
            name="empty_output_schema_tool",
            description="Allows any output",
            category="testing",
            input_schema={"type": "object", "properties": {}},
            output_schema={},
        )
        def my_func():
            return 42

        defn = getattr(my_func, _TOOL_DEFINITION_ATTR)
        assert defn.output_schema == {}

    def test_auto_discover_registers_tools(self, tmp_path, monkeypatch):
        """auto_discover finds decorated functions in a module."""
        # Create a temporary module
        module_code = """
from agentic_devtools.orchestration.tools.decorators import tool_definition

@tool_definition(
    name="discovered_tool",
    description="Auto-discovered",
    category="testing",
    input_schema={"type": "object", "properties": {}},
)
def my_discovered_tool():
    return {"found": True}
"""
        module_file = tmp_path / "test_module.py"
        module_file.write_text(module_code)

        import sys

        monkeypatch.syspath_prepend(str(tmp_path))
        # Clean up if already imported
        if "test_module" in sys.modules:
            del sys.modules["test_module"]

        registry = ConcreteToolRegistry()
        count = auto_discover("test_module", registry)
        assert count == 1
        assert registry.get("discovered_tool") is not None

    def test_auto_discover_skips_already_registered(self, tmp_path, monkeypatch):
        """auto_discover skips tools that are already registered."""
        module_code = """
from agentic_devtools.orchestration.tools.decorators import tool_definition

@tool_definition(
    name="preregistered_tool",
    description="Already registered",
    category="testing",
    input_schema={"type": "object", "properties": {}},
)
def my_tool():
    return {"ok": True}
"""
        module_file = tmp_path / "test_module_dup.py"
        module_file.write_text(module_code)

        import sys

        monkeypatch.syspath_prepend(str(tmp_path))
        if "test_module_dup" in sys.modules:
            del sys.modules["test_module_dup"]

        registry = ConcreteToolRegistry()
        # Pre-register the tool so auto_discover finds it already present
        existing_defn = ToolDefinition(
            name="preregistered_tool",
            description="Existing",
            category="testing",
            input_schema={"type": "object", "properties": {}},
        )
        registry.register(existing_defn, fn=lambda: None)

        count = auto_discover("test_module_dup", registry)
        assert count == 0
        # Original registration should be preserved
        assert registry.get("preregistered_tool").description == "Existing"
