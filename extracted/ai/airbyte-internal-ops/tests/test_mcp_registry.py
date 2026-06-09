# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for registry MCP tools."""

from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp.approval_resolution import ApprovalResolutionError
from airbyte_ops_mcp.github_actions import WorkflowDispatchResult
from airbyte_ops_mcp.human_in_the_loop import validate_approval_request_summary
from airbyte_ops_mcp.mcp.registry import (
    YANK_WORKFLOW_DEFAULT_BRANCH,
    YANK_WORKFLOW_FILE,
    YANK_WORKFLOW_REPO_NAME,
    YANK_WORKFLOW_REPO_OWNER,
    yank_connector_version,
)


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.registry.resolve_admin_email_from_approval")
@patch("airbyte_ops_mcp.mcp.registry.resolve_ci_trigger_github_token")
@patch("airbyte_ops_mcp.mcp.registry.trigger_workflow_dispatch")
def test_yank_connector_version_requires_approval_before_dispatch(
    mock_dispatch: MagicMock,
    mock_resolve_token: MagicMock,
    mock_resolve_approval: MagicMock,
) -> None:
    result = yank_connector_version(
        connector_name="source-faker",
        version="1.2.3",
        store="coral:prod",
        reason="bad release",
    )

    assert result.approval_required is True
    assert result.github_run_id is None
    assert result.github_run_url is None
    assert result.workflow_url is None
    assert "`escalate_to_human`" in result.message
    assert result.approval_request_summary is not None
    assert "source-faker@1.2.3" in result.approval_request_summary
    assert "coral:prod" in result.approval_request_summary
    assert "bad release" in result.approval_request_summary
    assert result.approval_request_message is not None
    assert "- Action: `yank`" in result.approval_request_message
    assert "- Connector: `source-faker`" in result.approval_request_message
    assert "- Version: `1.2.3`" in result.approval_request_message
    assert "- Store: `coral:prod`" in result.approval_request_message
    assert "- Reason: bad release" in result.approval_request_message
    assert "registry store compile" in result.approval_request_message
    mock_resolve_approval.assert_not_called()
    mock_resolve_token.assert_not_called()
    mock_dispatch.assert_not_called()


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.registry.resolve_admin_email_from_approval")
@patch("airbyte_ops_mcp.mcp.registry.resolve_ci_trigger_github_token")
@patch("airbyte_ops_mcp.mcp.registry.trigger_workflow_dispatch")
def test_yank_connector_version_sanitizes_reason_in_approval_summary(
    mock_dispatch: MagicMock,
    mock_resolve_token: MagicMock,
    mock_resolve_approval: MagicMock,
) -> None:
    result = yank_connector_version(
        connector_name="source-faker",
        version="1.2.3",
        store="coral:prod",
        reason="bad `release",
    )

    assert result.approval_request_summary is not None
    validate_approval_request_summary(result.approval_request_summary)
    assert "bad 'release" in result.approval_request_summary
    assert "`" not in result.approval_request_summary
    assert result.approval_request_message is not None
    assert "- Reason: bad 'release" in result.approval_request_message
    assert "bad `release" not in result.approval_request_message
    mock_resolve_approval.assert_not_called()
    mock_resolve_token.assert_not_called()
    mock_dispatch.assert_not_called()


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.registry.resolve_admin_email_from_approval")
@patch("airbyte_ops_mcp.mcp.registry.resolve_ci_trigger_github_token")
@patch("airbyte_ops_mcp.mcp.registry.trigger_workflow_dispatch")
def test_yank_connector_version_rejects_invalid_approval_before_dispatch(
    mock_dispatch: MagicMock,
    mock_resolve_token: MagicMock,
    mock_resolve_approval: MagicMock,
) -> None:
    mock_resolve_approval.side_effect = ApprovalResolutionError("approval failed")

    result = yank_connector_version(
        connector_name="source-faker",
        version="1.2.3",
        store="coral:prod",
        approval_comment_url="https://airbytehq-team.slack.com/archives/C123/p123",
    )

    assert result.approval_required is True
    assert result.message == "approval failed"
    assert result.github_run_id is None
    mock_resolve_approval.assert_called_once_with(
        approval_comment_url="https://airbytehq-team.slack.com/archives/C123/p123"
    )
    mock_resolve_token.assert_not_called()
    mock_dispatch.assert_not_called()


@pytest.mark.unit
@pytest.mark.parametrize(
    "unyank,reason,expected_action,expected_inputs",
    [
        pytest.param(
            False,
            "bad release",
            "Yank",
            {
                "connector-name": "source-faker",
                "version": "1.2.3",
                "store": "coral:prod",
                "unyank": "false",
                "reason": "bad release",
                "approval-url": "https://airbytehq-team.slack.com/archives/C123/p123",
            },
            id="yank_with_reason",
        ),
        pytest.param(
            True,
            "",
            "Unyank",
            {
                "connector-name": "source-faker",
                "version": "1.2.3",
                "store": "coral:prod",
                "unyank": "true",
                "approval-url": "https://airbytehq-team.slack.com/archives/C123/p123",
            },
            id="unyank_without_reason",
        ),
    ],
)
@patch("airbyte_ops_mcp.mcp.registry.resolve_admin_email_from_approval")
@patch("airbyte_ops_mcp.mcp.registry.resolve_ci_trigger_github_token")
@patch("airbyte_ops_mcp.mcp.registry.trigger_workflow_dispatch")
def test_yank_connector_version_dispatches_after_approval(
    mock_dispatch: MagicMock,
    mock_resolve_token: MagicMock,
    mock_resolve_approval: MagicMock,
    unyank: bool,
    reason: str,
    expected_action: str,
    expected_inputs: dict[str, str],
) -> None:
    mock_resolve_approval.return_value = "approver@airbyte.io"
    mock_resolve_token.return_value = "github-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte/actions/workflows/version-yank-command.yml",
        run_id=123,
        run_url="https://github.com/airbytehq/airbyte/actions/runs/123",
    )

    result = yank_connector_version(
        connector_name="source-faker",
        version="1.2.3",
        store="coral:prod",
        reason=reason,
        unyank=unyank,
        approval_comment_url="https://airbytehq-team.slack.com/archives/C123/p123",
    )

    assert result.approval_required is False
    assert result.approved_by == "approver@airbyte.io"
    assert result.github_run_id == 123
    assert result.github_run_url == (
        "https://github.com/airbytehq/airbyte/actions/runs/123"
    )
    assert f"{expected_action} workflow triggered" in result.message
    assert "after approval by approver@airbyte.io" in result.message
    mock_resolve_approval.assert_called_once_with(
        approval_comment_url="https://airbytehq-team.slack.com/archives/C123/p123"
    )
    mock_resolve_token.assert_called_once_with()
    mock_dispatch.assert_called_once_with(
        owner=YANK_WORKFLOW_REPO_OWNER,
        repo=YANK_WORKFLOW_REPO_NAME,
        workflow_file=YANK_WORKFLOW_FILE,
        ref=YANK_WORKFLOW_DEFAULT_BRANCH,
        inputs=expected_inputs,
        token="github-token",
    )
