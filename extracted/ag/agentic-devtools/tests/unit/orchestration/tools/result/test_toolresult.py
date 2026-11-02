"""Tests for ToolResult dataclass."""

import json

from agentic_devtools.orchestration.tools.result import ToolResult


class TestToolResult:
    """Tests for ToolResult construction and serialization."""

    def test_success_result(self):
        """Create a success result."""
        r = ToolResult(success=True, output={"key": "value"}, duration_ms=42.0)
        assert r.success is True
        assert r.output == {"key": "value"}
        assert r.error_type is None
        assert r.dry_run is False
        assert r.duration_ms == 42.0

    def test_error_result(self):
        """Create an error result."""
        r = ToolResult(
            success=False,
            error_type="execution_error",
            error_message="Something went wrong",
            duration_ms=100.0,
        )
        assert r.success is False
        assert r.error_type == "execution_error"
        assert r.error_message == "Something went wrong"

    def test_dry_run_result(self):
        """Create a dry-run result."""
        r = ToolResult(success=True, output={"would_execute": "tool"}, dry_run=True)
        assert r.dry_run is True

    def test_frozen_immutable(self):
        """ToolResult is immutable."""
        r = ToolResult(success=True)
        try:
            r.success = False  # type: ignore[misc]
            assert False, "Should have raised"
        except AttributeError:
            pass

    def test_to_dict(self):
        """to_dict serializes all fields."""
        r = ToolResult(success=True, output="hello", duration_ms=5.0)
        d = r.to_dict()
        assert d["success"] is True
        assert d["output"] == "hello"
        assert d["duration_ms"] == 5.0

    def test_to_json(self):
        """to_json produces valid JSON string."""
        r = ToolResult(success=True, output={"x": 1})
        j = r.to_json()
        parsed = json.loads(j)
        assert parsed["success"] is True
        assert parsed["output"] == {"x": 1}
