from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp.github_actions import (
    DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV,
    WorkflowDispatchResult,
    resolve_default_workflow_branch,
)
from airbyte_ops_mcp.github_api import PRHeadInfo
from airbyte_ops_mcp.human_in_the_loop import dispatch_escalation
from airbyte_ops_mcp.mcp.github_actions import trigger_ci_workflow


@pytest.mark.unit
def test_resolve_default_workflow_branch_uses_default_when_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default workflow branch resolution ignores empty override values."""
    monkeypatch.delenv(DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV, raising=False)
    assert resolve_default_workflow_branch("main") == "main"

    monkeypatch.setenv(DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV, "   ")
    assert resolve_default_workflow_branch("main") == "main"


@pytest.mark.unit
def test_resolve_default_workflow_branch_uses_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default workflow branch resolution honors the local testing override."""
    monkeypatch.setenv(DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV, " feature/workflows ")
    assert resolve_default_workflow_branch("main") == "feature/workflows"


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.github_actions.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_actions.resolve_ci_trigger_github_token")
def test_trigger_ci_workflow_uses_branch_override_when_ref_omitted(
    mock_token: MagicMock,
    mock_dispatch: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`trigger_ci_workflow` uses the override only when no explicit ref is provided."""
    monkeypatch.setenv(DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV, "feature/workflows")
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/example.yml",
    )

    result = trigger_ci_workflow(
        owner="airbytehq",
        repo="airbyte-ops-mcp",
        workflow_file="example.yml",
        inputs={"foo": "bar"},
    )

    assert result.success is True
    assert "(ref: feature/workflows)" in result.message
    assert mock_dispatch.call_args.kwargs["ref"] == "feature/workflows"


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.github_actions.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_actions.resolve_ci_trigger_github_token")
def test_trigger_ci_workflow_explicit_ref_beats_branch_override(
    mock_token: MagicMock,
    mock_dispatch: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Explicit workflow refs take precedence over the local testing override."""
    monkeypatch.setenv(DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV, "feature/workflows")
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/example.yml",
    )

    trigger_ci_workflow(
        owner="airbytehq",
        repo="airbyte-ops-mcp",
        workflow_file="example.yml",
        workflow_definition_ref="explicit-branch",
        inputs={"foo": "bar"},
    )

    assert mock_dispatch.call_args.kwargs["ref"] == "explicit-branch"


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.github_actions.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_actions.get_pr_head_ref")
@patch("airbyte_ops_mcp.mcp.github_actions.resolve_ci_trigger_github_token")
def test_trigger_ci_workflow_pr_ref_beats_branch_override(
    mock_token: MagicMock,
    mock_get_pr_head_ref: MagicMock,
    mock_dispatch: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """PR-number workflow refs take precedence over the local testing override."""
    monkeypatch.setenv(DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV, "feature/workflows")
    mock_token.return_value = "fake-token"
    mock_get_pr_head_ref.return_value = PRHeadInfo(
        ref="pr-head-branch",
        sha="abcdef1234567890",
        short_sha="abcdef1",
    )
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/example.yml",
    )

    trigger_ci_workflow(
        owner="airbytehq",
        repo="airbyte-ops-mcp",
        workflow_file="example.yml",
        workflow_definition_ref="794",
        inputs={"foo": "bar"},
    )

    mock_get_pr_head_ref.assert_called_once_with(
        "airbytehq",
        "airbyte-ops-mcp",
        794,
        "fake-token",
    )
    assert mock_dispatch.call_args.kwargs["ref"] == "pr-head-branch"


@pytest.mark.unit
@patch("airbyte_ops_mcp.human_in_the_loop.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.human_in_the_loop.resolve_ci_trigger_github_token")
def test_dispatch_escalation_uses_branch_override(
    mock_token: MagicMock,
    mock_dispatch: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Shared workflow dispatch callers use the local testing override."""
    monkeypatch.setenv(DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV, "feature/hitl")
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/human-in-the-loop.yml",
    )

    dispatch_escalation(
        target_person="aj@airbyte.io",
        message="Test message.",
        agent_session_url="https://app.devin.ai/sessions/abc",
    )

    assert mock_dispatch.call_args.kwargs["ref"] == "feature/hitl"
