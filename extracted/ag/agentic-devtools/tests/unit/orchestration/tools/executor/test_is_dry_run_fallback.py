"""Tests for ToolExecutor._is_dry_run fallback to state."""

from unittest.mock import patch

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestIsDryRunFallback:
    """Tests for _is_dry_run when no dry_run_fn is provided."""

    def test_fallback_to_state_dry_run_true(self):
        """When no dry_run_fn, falls back to state.is_dry_run()."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="mutator",
                description="Mutating tool",
                category="testing",
                input_schema={"type": "object", "properties": {}},
                mutating=True,
            ),
            fn=lambda: {"done": True},
        )
        # No dry_run_fn provided
        executor = ToolExecutor(registry)

        with patch("agentic_devtools.state.is_dry_run", return_value=True) as mock_dr:
            result = executor.execute("mutator")
            mock_dr.assert_called_once()

        assert result.success is True
        assert result.dry_run is True
        assert result.output["would_execute"] == "mutator"

    def test_fallback_to_state_dry_run_false(self):
        """When state.is_dry_run() returns False, tool executes normally."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="mutator",
                description="Mutating tool",
                category="testing",
                input_schema={"type": "object", "properties": {}},
                mutating=True,
            ),
            fn=lambda: {"done": True},
        )
        executor = ToolExecutor(registry)

        with patch("agentic_devtools.state.is_dry_run", return_value=False):
            result = executor.execute("mutator")

        assert result.success is True
        assert result.dry_run is False
        assert result.output == {"done": True}
