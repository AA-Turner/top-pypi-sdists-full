"""Tests for ToolInvocationError exception."""

from agentic_devtools.orchestration.execution.exceptions import ToolInvocationError


class TestToolInvocationError:
    def test_message(self) -> None:
        err = ToolInvocationError("tool failed")
        assert str(err) == "tool failed"

    def test_tool_name_attribute(self) -> None:
        err = ToolInvocationError("fail", tool_name="get_diff")
        assert err.tool_name == "get_diff"

    def test_tool_name_defaults_empty(self) -> None:
        err = ToolInvocationError("fail")
        assert err.tool_name == ""

    def test_cause_attribute(self) -> None:
        cause = ValueError("inner")
        err = ToolInvocationError("fail", cause=cause)
        assert err.cause is cause

    def test_cause_defaults_none(self) -> None:
        err = ToolInvocationError("fail")
        assert err.cause is None

    def test_is_runtime_error(self) -> None:
        err = ToolInvocationError("fail")
        assert isinstance(err, RuntimeError)
