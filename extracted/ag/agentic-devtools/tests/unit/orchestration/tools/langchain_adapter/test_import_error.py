"""Tests for LangChain adapter - import error handling."""

import sys
from unittest.mock import patch

import pytest

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestImportError:
    """Test lazy ImportError when langchain-core is missing."""

    def test_import_error_when_langchain_missing(self):
        """to_langchain_tool raises ImportError with install instructions."""
        from agentic_devtools.orchestration.tools.langchain_adapter import to_langchain_tool

        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="test",
                description="Test",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda: None,
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        definition = registry.get("test")

        # Temporarily hide langchain_core
        with patch.dict(sys.modules, {"langchain_core": None, "langchain_core.tools": None}):
            with pytest.raises(ImportError, match=r"pip install agentic-devtools$"):
                to_langchain_tool(definition, executor)
