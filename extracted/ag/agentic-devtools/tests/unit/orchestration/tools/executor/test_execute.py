"""Tests for ToolExecutor.execute()."""

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.executor import ToolExecutor
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestExecute:
    """Tests for ToolExecutor.execute()."""

    def _make_registry_with_tool(self, name="test_tool", mutating=False, fn=None):
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name=name,
                description="Test",
                category="testing",
                input_schema={"type": "object", "properties": {"x": {"type": "string"}}},
                mutating=mutating,
            ),
            fn=fn or (lambda x="": {"result": x}),
        )
        return registry

    def test_successful_invocation(self):
        """Execute returns success ToolResult."""
        registry = self._make_registry_with_tool()
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.execute("test_tool", {"x": "hello"})
        assert result.success is True
        assert result.output == {"result": "hello"}
        assert result.duration_ms > 0

    def test_tool_not_found(self):
        """Execute returns not_found error for missing tool."""
        registry = ConcreteToolRegistry()
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.execute("nonexistent")
        assert result.success is False
        assert result.error_type == "not_found"

    def test_validation_error(self):
        """Execute returns validation_error for bad inputs."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="strict",
                description="Strict",
                category="testing",
                input_schema={
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                },
            ),
            fn=lambda name: name,
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.execute("strict", {})
        assert result.success is False
        assert result.error_type == "validation_error"

    def test_execution_error(self):
        """Execute catches exceptions and returns execution_error."""

        def _raise(**kwargs):
            raise RuntimeError("boom")

        registry = self._make_registry_with_tool(fn=_raise)
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.execute("test_tool", {"x": "a"})
        assert result.success is False
        assert result.error_type == "execution_error"
        assert "boom" in result.error_message

    def test_domain_failure_dict_mapped_to_failure_result(self):
        """Tool returning {"success": False, ...} produces ToolResult(success=False)."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="domain_fail",
                description="Domain failure",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda **kw: {"success": False, "error": "detached HEAD"},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.execute("domain_fail")
        assert result.success is False
        assert result.error_type == "execution_error"
        assert "detached HEAD" in result.error_message
        assert result.output == {"success": False, "error": "detached HEAD"}

    def test_domain_failure_message_key_extracted(self):
        """Git-style tools using 'message' key produce a readable error_message."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="git_fail",
                description="Git failure",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda **kw: {"success": False, "branch": None, "message": "Detached HEAD or not a git repo"},
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.execute("git_fail")
        assert result.success is False
        assert "Detached HEAD" in result.error_message

    def test_domain_failure_stderr_key_extracted(self):
        """Testing-style tools using 'stderr' key produce a readable error_message."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="test_fail",
                description="Testing failure",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda **kw: {
                "success": False,
                "returncode": 1,
                "stderr": "Invalid test pattern: contains disallowed characters",
            },
        )
        executor = ToolExecutor(registry, dry_run_fn=lambda: False)
        result = executor.execute("test_fail")
        assert result.success is False
        assert "Invalid test pattern" in result.error_message
