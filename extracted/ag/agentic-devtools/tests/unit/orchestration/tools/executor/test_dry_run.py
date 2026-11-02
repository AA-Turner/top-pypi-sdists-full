"""Tests for dry-run enforcement."""

from unittest.mock import MagicMock

import pytest

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestDryRun:
    """Tests for dry-run enforcement in ToolExecutor."""

    def test_mutating_tool_skipped_in_dry_run(self):
        """Mutating tool is NOT called in dry-run mode."""
        fn = MagicMock(return_value={"ok": True})
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="mutator",
                description="Mutates",
                category="git",
                input_schema={"type": "object", "properties": {}},
                mutating=True,
            ),
            fn=fn,
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: True)
        result = executor.execute("mutator")
        assert result.success is True
        assert result.dry_run is True
        assert "would_execute" in result.output
        fn.assert_not_called()

    def test_non_mutating_tool_executes_in_dry_run(self):
        """Non-mutating tool executes normally in dry-run mode."""
        fn = MagicMock(return_value={"data": "value"})
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="reader",
                description="Reads",
                category="git",
                input_schema={"type": "object", "properties": {}},
                mutating=False,
            ),
            fn=fn,
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: True)
        result = executor.execute("reader")
        assert result.success is True
        assert result.dry_run is False
        fn.assert_called_once()

    def test_mutating_tool_executes_when_dry_run_off(self):
        """Mutating tool executes normally when dry-run is disabled."""
        fn = MagicMock(return_value={"ok": True})
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="mutator",
                description="Mutates",
                category="git",
                input_schema={"type": "object", "properties": {}},
                mutating=True,
            ),
            fn=fn,
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.execute("mutator")
        assert result.success is True
        assert result.dry_run is False
        fn.assert_called_once()

    def test_non_callable_dry_run_fn_raises_type_error(self):
        """Passing a non-callable dry_run_fn raises TypeError at construction time."""
        registry = ConcreteToolRegistry()
        with pytest.raises(TypeError, match="dry_run_fn must be callable"):
            ToolExecutor(registry, dry_run_fn=True)  # type: ignore[arg-type]
