"""Tests for the provider-neutral pull-request thread tool registration."""

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.tools.builtins import register_all_builtins
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestRegisterPullRequestThreadTool:
    """Validate delegation and error normalization for the registered tool."""

    def test_provider_neutral_reply_tool_delegates(self):
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("reply_to_pull_request_thread")
        assert fn is not None
        result = MagicMock()
        result.mutation_status = "replied"
        result.to_dict.return_value = {"mutationStatus": "replied"}
        with patch("agentic_devtools.cli.pull_request_thread.reply_to_pull_request_thread", return_value=result):
            output = fn(
                provider="github",
                repository="owner/repo",
                pull_request_number=12,
                discussion_id=34,
                body="reply",
            )
        assert output == {"mutationStatus": "replied"}
        assert "success" not in output

    def test_provider_neutral_reply_tool_propagates_failure_marker(self):
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("reply_to_pull_request_thread")
        assert fn is not None
        result = MagicMock()
        result.mutation_status = "failed"
        result.to_dict.return_value = {"mutationStatus": "failed", "diagnostics": ["auth error"]}
        with patch("agentic_devtools.cli.pull_request_thread.reply_to_pull_request_thread", return_value=result):
            output = fn(
                provider="github",
                repository="owner/repo",
                pull_request_number=12,
                discussion_id=34,
                body="reply",
            )
        assert output["success"] is False
        assert output["mutationStatus"] == "failed"

    def test_provider_neutral_reply_tool_returns_failure(self):
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("reply_to_pull_request_thread")
        assert fn is not None
        with patch(
            "agentic_devtools.cli.pull_request_thread.reply_to_pull_request_thread",
            side_effect=ValueError("invalid target"),
        ):
            output = fn(
                provider="github",
                repository="owner/repo",
                pull_request_number=12,
                discussion_id=34,
                body="reply",
            )
        assert output == {"success": False, "error": "invalid target"}
