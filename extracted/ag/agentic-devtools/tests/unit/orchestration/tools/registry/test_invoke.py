"""Tests for ConcreteToolRegistry.invoke()."""

from agentic_devtools.orchestration.tools.definition import ToolDefinition
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestInvoke:
    """Tests for the invoke facade."""

    def test_invoke_success(self):
        """invoke returns ToolResult envelope on success."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="echo",
                description="Echo",
                category="testing",
                input_schema={"type": "object", "properties": {"msg": {"type": "string"}}},
            ),
            fn=lambda msg="": {"echoed": msg},
        )
        result = registry.invoke("echo", msg="hello")
        assert result["success"] is True
        assert result["output"]["echoed"] == "hello"

    def test_invoke_not_found(self):
        """invoke returns not_found ToolResult envelope for non-registered tool."""
        registry = ConcreteToolRegistry()
        result = registry.invoke("nonexistent")
        assert result["success"] is False
        assert result["error_type"] == "not_found"
        assert "nonexistent" in result["error_message"]

    def test_invoke_exception(self):
        """invoke wraps exceptions in error ToolResult."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="fail",
                description="Fails",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda: (_ for _ in ()).throw(RuntimeError("boom")),
        )

        def _failing_fn():
            raise RuntimeError("boom")

        registry._functions["fail"] = _failing_fn
        result = registry.invoke("fail")
        assert result["success"] is False
        assert result["error_type"] == "execution_error"
        assert "boom" in result["error_message"]

    def test_invoke_domain_failure_dict(self):
        """invoke maps {'success': False, ...} output to a failure ToolResult."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="domain_fail",
                description="Returns domain failure",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda: {"success": False, "error": "something went wrong"},
        )
        result = registry.invoke("domain_fail")
        assert result["success"] is False
        assert result["error_type"] == "execution_error"
        assert result["error_message"] == "something went wrong"
        # Raw output is preserved for callers that need detail
        assert result["output"]["error"] == "something went wrong"

    def test_invoke_domain_failure_message_key(self):
        """invoke extracts error from 'message' key when 'error' is absent."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="git_fail",
                description="Returns git-style failure",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda: {"success": False, "message": "not a git repo"},
        )
        result = registry.invoke("git_fail")
        assert result["success"] is False
        assert result["error_message"] == "not a git repo"

    def test_invoke_domain_failure_no_message_key(self):
        """invoke uses fallback error message when no message key is present."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="silent_fail",
                description="Returns failure with no message",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda: {"success": False},
        )
        result = registry.invoke("silent_fail")
        assert result["success"] is False
        assert result["error_message"] == "tool reported failure"

    def test_invoke_falsy_output_not_treated_as_failure(self):
        """invoke does not treat None or 0 as domain failures."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="none_tool",
                description="Returns None",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda: None,
        )
        result = registry.invoke("none_tool")
        assert result["success"] is True

    def test_invoke_success_dict_not_treated_as_failure(self):
        """invoke does not misread {'success': True, ...} as a failure."""
        registry = ConcreteToolRegistry()
        registry.register(
            ToolDefinition(
                name="ok_tool",
                description="Returns success dict",
                category="testing",
                input_schema={"type": "object", "properties": {}},
            ),
            fn=lambda: {"success": True, "data": 42},
        )
        result = registry.invoke("ok_tool")
        assert result["success"] is True
        assert result["output"]["data"] == 42
