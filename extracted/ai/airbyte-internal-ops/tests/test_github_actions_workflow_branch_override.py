from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp.github_actions import (
    DEFAULT_WORKFLOW_BRANCH_OVERRIDE_ENV,
    WorkflowDispatchResult,
    WorkflowJobInfo,
    WorkflowRunStatus,
    resolve_default_workflow_branch,
)
from airbyte_ops_mcp.github_api import PRHeadInfo
from airbyte_ops_mcp.human_in_the_loop import dispatch_escalation
from airbyte_ops_mcp.mcp.github_ops import trigger_ci_workflow


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
@patch("airbyte_ops_mcp.mcp.github_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_ops.resolve_ci_trigger_github_token")
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
@patch("airbyte_ops_mcp.mcp.github_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_ops.resolve_ci_trigger_github_token")
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
@patch("airbyte_ops_mcp.mcp.github_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_ops.get_pr_head_ref")
@patch("airbyte_ops_mcp.mcp.github_ops.resolve_ci_trigger_github_token")
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
@patch("airbyte_ops_mcp.mcp.github_ops.wait_for_workflow_completion")
@patch("airbyte_ops_mcp.mcp.github_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_ops.resolve_ci_trigger_github_token")
def test_trigger_ci_workflow_waits_for_successful_completion(
    mock_token: MagicMock,
    mock_dispatch: MagicMock,
    mock_wait: MagicMock,
) -> None:
    """The default behavior waits for and reports successful completion."""
    run_url = "https://github.com/airbytehq/airbyte-ops-mcp/actions/runs/42"
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/example.yml",
        run_id=42,
        run_url=run_url,
    )
    mock_wait.return_value = WorkflowRunStatus(
        run_id=42,
        status="completed",
        conclusion="success",
        run_url=run_url,
    )

    result = trigger_ci_workflow(
        owner="airbytehq",
        repo="airbyte-ops-mcp",
        workflow_file="example.yml",
        inputs={"foo": "bar"},
    )

    assert result.success is True
    assert result.completed is True
    assert result.status == "completed"
    assert result.conclusion == "success"
    assert result.run_url == run_url
    mock_wait.assert_called_once_with(
        owner="airbytehq",
        repo="airbyte-ops-mcp",
        run_id=42,
        token="fake-token",
        poll_interval_seconds=10.0,
        max_wait_seconds=600,
    )


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.github_ops.wait_for_workflow_completion")
@patch("airbyte_ops_mcp.mcp.github_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_ops.resolve_ci_trigger_github_token")
def test_trigger_ci_workflow_reports_failed_jobs(
    mock_token: MagicMock,
    mock_dispatch: MagicMock,
    mock_wait: MagicMock,
) -> None:
    """A failed workflow reports its failed jobs."""
    run_url = "https://github.com/airbytehq/airbyte-ops-mcp/actions/runs/43"
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/example.yml",
        run_id=43,
        run_url=run_url,
    )
    mock_wait.return_value = WorkflowRunStatus(
        run_id=43,
        status="completed",
        conclusion="failure",
        run_url=run_url,
        jobs=[
            WorkflowJobInfo(
                job_id=101,
                name="Build",
                status="completed",
                conclusion="failure",
            ),
            WorkflowJobInfo(
                job_id=102,
                name="Lint",
                status="completed",
                conclusion="success",
            ),
            WorkflowJobInfo(
                job_id=103,
                name="Deploy",
                status="completed",
                conclusion="cancelled",
            ),
        ],
    )

    result = trigger_ci_workflow(
        owner="airbytehq",
        repo="airbyte-ops-mcp",
        workflow_file="example.yml",
        inputs={"foo": "bar"},
    )

    assert result.success is False
    assert result.completed is True
    assert result.conclusion == "failure"
    assert result.failed_jobs == [
        "Build (job_id=101)",
        "Deploy (job_id=103)",
    ]
    assert "Build (job_id=101)" in result.message
    assert "Non-successful jobs:" in result.message


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.github_ops.wait_for_workflow_completion")
@patch("airbyte_ops_mcp.mcp.github_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_ops.resolve_ci_trigger_github_token")
def test_trigger_ci_workflow_reports_timeout(
    mock_token: MagicMock,
    mock_dispatch: MagicMock,
    mock_wait: MagicMock,
) -> None:
    """An incomplete workflow reports its status and polling instructions."""
    run_url = "https://github.com/airbytehq/airbyte-ops-mcp/actions/runs/44"
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/example.yml",
        run_id=44,
        run_url=run_url,
    )
    mock_wait.return_value = WorkflowRunStatus(
        run_id=44,
        status="in_progress",
        run_url=run_url,
    )

    result = trigger_ci_workflow(
        owner="airbytehq",
        repo="airbyte-ops-mcp",
        workflow_file="example.yml",
        inputs={"foo": "bar"},
        max_wait_seconds=5,
    )

    assert result.success is True
    assert result.completed is False
    assert result.status == "in_progress"
    assert "check_ci_workflow_status" in result.message
    assert mock_wait.call_args.kwargs["max_wait_seconds"] == 10


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.github_ops.wait_for_workflow_completion")
@patch("airbyte_ops_mcp.mcp.github_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_ops.resolve_ci_trigger_github_token")
def test_trigger_ci_workflow_can_return_without_waiting(
    mock_token: MagicMock,
    mock_dispatch: MagicMock,
    mock_wait: MagicMock,
) -> None:
    """Disabling waiting returns immediately after dispatch."""
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/example.yml",
        run_id=45,
        run_url="https://github.com/airbytehq/airbyte-ops-mcp/actions/runs/45",
    )

    result = trigger_ci_workflow(
        owner="airbytehq",
        repo="airbyte-ops-mcp",
        workflow_file="example.yml",
        inputs={"foo": "bar"},
        wait_for_completion=False,
    )

    assert result.success is True
    assert result.completed is False
    mock_wait.assert_not_called()


@pytest.mark.unit
@patch("airbyte_ops_mcp.mcp.github_ops.wait_for_workflow_completion")
@patch("airbyte_ops_mcp.mcp.github_ops.trigger_workflow_dispatch")
@patch("airbyte_ops_mcp.mcp.github_ops.resolve_ci_trigger_github_token")
def test_trigger_ci_workflow_reports_missing_run_id(
    mock_token: MagicMock,
    mock_dispatch: MagicMock,
    mock_wait: MagicMock,
) -> None:
    """A missing run ID prevents completion verification."""
    workflow_url = (
        "https://github.com/airbytehq/airbyte-ops-mcp/actions/workflows/example.yml"
    )
    mock_token.return_value = "fake-token"
    mock_dispatch.return_value = WorkflowDispatchResult(
        workflow_url=workflow_url,
    )

    result = trigger_ci_workflow(
        owner="airbytehq",
        repo="airbyte-ops-mcp",
        workflow_file="example.yml",
        inputs={"foo": "bar"},
    )

    assert result.success is True
    assert result.completed is False
    assert "run ID could not be discovered" in result.message
    assert workflow_url in result.message
    mock_wait.assert_not_called()


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
