"""Tests for the provider-neutral pull-request approval tool registration."""

from unittest.mock import patch

from agentic_devtools.adapters.pull_request_approval import PullRequestApprovalResult
from agentic_devtools.orchestration.tools.builtins import register_all_builtins
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry
from agentic_devtools.orchestration.tools.validation import validate_inputs


class TestRegisterPullRequestApprovalTool:
    """Validate delegation and error normalization for the registered tool."""

    def test_provider_neutral_approval_tool_delegates(self):
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("approve_pull_request")
        assert fn is not None
        result = PullRequestApprovalResult.for_request(
            _fake_request(),
            True,
            "approved",
            verified=True,
        )
        with patch(
            "agentic_devtools.cli.pull_request_approval.dispatch_pull_request_approval",
            return_value=result,
        ):
            output = fn(
                provider="github",
                repository="owner/repo",
                pull_request_id=12,
                content="LGTM",
                expected_head="a" * 40,
            )
        assert output["success"] is True
        assert output["status"] == "approved"
        assert output["repository"] == "owner/repo"
        assert output["pull_request_id"] == 12

    def test_provider_neutral_approval_tool_returns_failure_on_invalid_request(self):
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("approve_pull_request")
        assert fn is not None
        output = fn(
            provider="github",
            repository="owner/repo",
            pull_request_id=12,
            content="LGTM",
            expected_head=None,
        )
        assert output["success"] is False
        assert "expected_head" in output["error"]

    def test_approval_schema_requires_provider_specific_fields(self):
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        definition = registry.get("approve_pull_request")
        assert definition is not None

        azure_request = {
            "provider": "azure_devops",
            "repository": "my-repo",
            "pull_request_id": 42,
            "content": "LGTM",
        }
        result = validate_inputs(definition.input_schema, azure_request)
        assert result is not None
        assert "organization" in result.error_message

        azure_request.update({"organization": "https://dev.azure.com/org", "project": "project"})
        assert validate_inputs(definition.input_schema, azure_request) is None

        github_request = {
            "provider": "github",
            "repository": "owner/repo",
            "pull_request_id": 42,
            "content": "LGTM",
        }
        result = validate_inputs(definition.input_schema, github_request)
        assert result is not None
        assert "expected_head" in result.error_message

        github_request["expected_head"] = "a" * 40
        assert validate_inputs(definition.input_schema, github_request) is None

    def test_approval_tool_is_serialized_with_bounded_timeout(self):
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        definition = registry.get("approve_pull_request")
        assert definition is not None
        assert definition.thread_safe is False
        assert definition.timeout_seconds == 300.0

    def test_provider_neutral_approval_tool_normalizes_dispatch_exception(self):
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("approve_pull_request")
        assert fn is not None
        with patch(
            "agentic_devtools.cli.pull_request_approval.dispatch_pull_request_approval",
            side_effect=RuntimeError("boom"),
        ):
            output = fn(
                provider="azure_devops",
                repository="my-repo",
                pull_request_id=42,
                content="LGTM",
            )
        assert output == {"success": False, "error": "boom"}


def _fake_request():
    from agentic_devtools.adapters.pull_request_approval import PullRequestApprovalRequest

    return PullRequestApprovalRequest(
        provider="github",
        repository="owner/repo",
        pull_request_id=12,
        content="LGTM",
        expected_head="a" * 40,
    )
