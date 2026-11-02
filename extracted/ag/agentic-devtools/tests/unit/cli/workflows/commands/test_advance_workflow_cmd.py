"""Tests for AdvanceWorkflowCmd."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools import state
from agentic_devtools.prompts import loader


@pytest.fixture
def temp_prompts_dir(tmp_path):
    """Create a temporary prompts directory with test templates."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    with patch.object(loader, "get_prompts_dir", return_value=prompts_dir):
        yield prompts_dir


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory."""
    output_dir = tmp_path / "temp"
    output_dir.mkdir()
    with patch.object(loader, "get_temp_output_dir", return_value=output_dir):
        yield output_dir


@pytest.fixture
def clear_state_before(temp_state_dir):
    """Clear state before each test.

    Note: We only remove the state file, not the entire temp folder,
    to avoid deleting directories created by other fixtures (like temp_prompts_dir).
    """
    state_file = temp_state_dir / "state.json"
    if state_file.exists():
        state_file.unlink()
    yield


@pytest.fixture
def mock_workflow_state_clearing():
    """Mock clear_state_for_workflow_initiation to be a no-op.

    Workflow initiation commands reset workflow tracking keys (workflow,
    agdt_run_id) at the start.  This fixture prevents that reset, which
    is useful when tests pre-set workflow state before calling the command.
    """
    with patch("agentic_devtools.cli.workflows.commands.clear_state_for_workflow_initiation"):
        yield


class TestAdvanceWorkflowCmd:
    """Tests for advance_workflow_cmd entry point."""

    def test_advance_workflow_no_active_workflow(self, temp_state_dir, clear_state_before, capsys):
        """Test advance workflow command when no workflow is active."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        with patch.object(sys, "argv", ["agdt-advance-workflow"]):
            with pytest.raises(SystemExit) as exc_info:
                advance_workflow_cmd()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "No active workflow found" in captured.err
        assert "State directory checked:" in captured.err
        assert "No re-initiation will be attempted" in captured.err

    def test_advance_workflow_no_active_workflow_with_step(self, temp_state_dir, clear_state_before, capsys):
        """Test advance workflow command when no workflow is active and step is provided."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        with patch.object(sys, "argv", ["agdt-advance-workflow", "review"]):
            with pytest.raises(SystemExit) as exc_info:
                advance_workflow_cmd()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "No active workflow found" in captured.err
        assert "Requested step: review" in captured.err
        assert "No re-initiation will be attempted" in captured.err

    def test_advance_workflow_unsupported_workflow(self, temp_state_dir, clear_state_before, capsys):
        """Test advance workflow command with unsupported workflow type."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        state.set_workflow_state(name="unsupported-workflow", status="active", step="step1")

        with patch.object(sys, "argv", ["agdt-advance-workflow"]):
            with pytest.raises(SystemExit) as exc_info:
                advance_workflow_cmd()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "does not support manual advancement" in captured.err

    def test_advance_workflow_work_on_jira_issue(self, temp_state_dir, clear_state_before):
        """Test advance workflow command with work-on-jira-issue workflow."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        state.set_workflow_state(
            name="work-on-jira-issue",
            status="active",
            step="research",
            context={"jira_issue_key": "TEST-123"},
        )

        with patch.object(sys, "argv", ["agdt-advance-workflow"]):
            with patch("agentic_devtools.cli.workflows.advance_work_on_jira_issue_workflow") as mock_advance:
                advance_workflow_cmd()
                mock_advance.assert_called_once_with(None)

    def test_advance_workflow_pull_request_review(self, temp_state_dir, clear_state_before):
        """Test advance workflow command with pull-request-review workflow."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        state.set_workflow_state(
            name="pull-request-review",
            status="active",
            step="review",
            context={"pull_request_id": "456"},
        )

        with patch.object(sys, "argv", ["agdt-advance-workflow"]):
            with patch("agentic_devtools.cli.workflows.advance_pull_request_review_workflow") as mock_advance:
                with patch("agentic_devtools.state.refresh_pin_file_ttl") as mock_refresh:
                    advance_workflow_cmd()
                    mock_advance.assert_called_once_with(None)
                    mock_refresh.assert_called_once()

    def test_advance_workflow_work_on_jira_issue_does_not_refresh_pin(self, temp_state_dir, clear_state_before):
        """Pin file TTL is NOT refreshed for work-on-jira-issue workflows."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        state.set_workflow_state(
            name="work-on-jira-issue",
            status="active",
            step="research",
            context={"jira_issue_key": "TEST-PIN"},
        )

        with patch.object(sys, "argv", ["agdt-advance-workflow"]):
            with patch("agentic_devtools.cli.workflows.advance_work_on_jira_issue_workflow"):
                with patch("agentic_devtools.state.refresh_pin_file_ttl") as mock_refresh:
                    advance_workflow_cmd()
                    mock_refresh.assert_not_called()

    def test_advance_workflow_with_step_argument(self, temp_state_dir, clear_state_before):
        """Test advance workflow command with explicit step argument."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        state.set_workflow_state(
            name="work-on-jira-issue",
            status="active",
            step="research",
            context={"jira_issue_key": "TEST-123"},
        )

        with patch.object(sys, "argv", ["agdt-advance-workflow", "implement"]):
            with patch("agentic_devtools.cli.workflows.advance_work_on_jira_issue_workflow") as mock_advance:
                advance_workflow_cmd()
                mock_advance.assert_called_once_with("implement")

    def test_advance_workflow_pin_refresh_oserror_emits_warning(self, temp_state_dir, clear_state_before, capsys):
        """OSError in refresh_pin_file_ttl emits a warning but does not abort the command."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        state.set_workflow_state(
            name="pull-request-review",
            status="active",
            step="review",
            context={"pull_request_id": "789"},
        )

        with patch.object(sys, "argv", ["agdt-advance-workflow"]):
            with patch("agentic_devtools.cli.workflows.advance_pull_request_review_workflow"):
                with patch(
                    "agentic_devtools.state.refresh_pin_file_ttl",
                    side_effect=OSError("disk full"),
                ):
                    advance_workflow_cmd()  # Should NOT raise

        captured = capsys.readouterr()
        assert "WARNING" in captured.err
        assert "disk full" in captured.err


class TestAdvanceWorkflowCmdDecisionMode:
    """Tests for the --decision mode in advance_workflow_cmd."""

    def test_decision_and_step_mutually_exclusive(self, temp_state_dir, capsys):
        """Passing both --decision and a positional step exits with error."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        with patch.object(
            sys, "argv", ["agdt-advance-workflow", "review", "--decision", "approve", "--decision-id", "abc-123"]
        ):
            with pytest.raises(SystemExit) as exc_info:
                advance_workflow_cmd()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "mutually exclusive" in captured.err

    def test_decision_mode_missing_decision_id(self, temp_state_dir, capsys):
        """--decision without --decision-id exits with error."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        with patch.object(sys, "argv", ["agdt-advance-workflow", "--decision", "approve"]):
            with pytest.raises(SystemExit) as exc_info:
                advance_workflow_cmd()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "--decision-id is required" in captured.err

    def test_decision_mode_missing_run_id(self, temp_state_dir, clear_state_before, capsys):
        """--decision without --run-id and no state key exits with error."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        with patch.object(sys, "argv", ["agdt-advance-workflow", "--decision", "approve", "--decision-id", "uuid-123"]):
            with pytest.raises(SystemExit) as exc_info:
                advance_workflow_cmd()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "agdt_run_id" in captured.err

    def test_decision_mode_run_id_from_state(self, temp_state_dir, capsys):
        """--decision resolves run_id from state when not provided via CLI."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        state.set_value("agdt_run_id", "run-from-state")

        mock_result = MagicMock()
        mock_result.action_name = "deploy-to-prod"

        with patch.object(sys, "argv", ["agdt-advance-workflow", "--decision", "approve", "--decision-id", "uuid-456"]):
            with patch(
                "agentic_devtools.orchestration.execution.decision_gate.resolve_decision", return_value=mock_result
            ) as mock_resolve:
                advance_workflow_cmd()
                mock_resolve.assert_called_once_with(state.get_state_dir(), "run-from-state", "uuid-456", approved=True)

        captured = capsys.readouterr()
        assert "approved" in captured.out
        assert "deploy-to-prod" in captured.out

    def test_decision_mode_approve_with_explicit_run_id(self, temp_state_dir, capsys):
        """--decision approve with explicit --run-id calls resolve_decision correctly."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        mock_result = MagicMock()
        mock_result.action_name = "run-tests"

        with patch.object(
            sys, "argv", ["agdt-advance-workflow", "--decision", "approve", "--decision-id", "d-1", "--run-id", "r-1"]
        ):
            with patch(
                "agentic_devtools.orchestration.execution.decision_gate.resolve_decision", return_value=mock_result
            ) as mock_resolve:
                advance_workflow_cmd()
                mock_resolve.assert_called_once_with(state.get_state_dir(), "r-1", "d-1", approved=True)

        captured = capsys.readouterr()
        assert "approved" in captured.out

    def test_decision_mode_deny(self, temp_state_dir, capsys):
        """--decision deny passes approved=False to resolve_decision."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        mock_result = MagicMock()
        mock_result.action_name = "dangerous-action"

        with patch.object(
            sys, "argv", ["agdt-advance-workflow", "--decision", "deny", "--decision-id", "d-2", "--run-id", "r-2"]
        ):
            with patch(
                "agentic_devtools.orchestration.execution.decision_gate.resolve_decision", return_value=mock_result
            ) as mock_resolve:
                advance_workflow_cmd()
                mock_resolve.assert_called_once_with(state.get_state_dir(), "r-2", "d-2", approved=False)

        captured = capsys.readouterr()
        assert "denied" in captured.out
        assert "dangerous-action" in captured.out

    def test_decision_mode_value_error(self, temp_state_dir, capsys):
        """ValueError from resolve_decision is caught and printed."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        with patch.object(
            sys,
            "argv",
            ["agdt-advance-workflow", "--decision", "approve", "--decision-id", "bad-id", "--run-id", "r-3"],
        ):
            with patch(
                "agentic_devtools.orchestration.execution.decision_gate.resolve_decision",
                side_effect=ValueError("No pending decision with id bad-id"),
            ):
                with pytest.raises(SystemExit) as exc_info:
                    advance_workflow_cmd()
                assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "No pending decision with id bad-id" in captured.err

    def test_decision_mode_whitespace_decision_id_rejected(self, temp_state_dir, capsys):
        """--decision-id with only whitespace is treated as missing and exits with error."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        with patch.object(
            sys, "argv", ["agdt-advance-workflow", "--decision", "approve", "--decision-id", "   ", "--run-id", "r-1"]
        ):
            with pytest.raises(SystemExit) as exc_info:
                advance_workflow_cmd()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "--decision-id is required" in captured.err

    def test_decision_mode_whitespace_run_id_in_state_rejected(self, temp_state_dir, clear_state_before, capsys):
        """agdt_run_id in state that is empty/whitespace is rejected."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        state.set_value("agdt_run_id", "   ")

        with patch.object(sys, "argv", ["agdt-advance-workflow", "--decision", "approve", "--decision-id", "uuid-789"]):
            with pytest.raises(SystemExit) as exc_info:
                advance_workflow_cmd()
        assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "agdt_run_id" in captured.err

    def test_decision_mode_path_like_run_id_cli_rejected(self, temp_state_dir, capsys):
        """Path-like --run-id values are rejected before resolve_decision is called."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        with patch.object(
            sys,
            "argv",
            ["agdt-advance-workflow", "--decision", "approve", "--decision-id", "d-4", "--run-id", "../escape"],
        ):
            with patch("agentic_devtools.orchestration.execution.decision_gate.resolve_decision") as mock_resolve:
                with pytest.raises(SystemExit) as exc_info:
                    advance_workflow_cmd()
                assert exc_info.value.code == 1
                mock_resolve.assert_not_called()

        captured = capsys.readouterr()
        assert "must be a run identifier" in captured.err

    def test_decision_mode_path_like_run_id_from_state_rejected(self, temp_state_dir, capsys):
        """Path-like state agdt_run_id values are rejected before resolve_decision is called."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        state.set_value("agdt_run_id", "run/id")

        with patch.object(sys, "argv", ["agdt-advance-workflow", "--decision", "approve", "--decision-id", "d-5"]):
            with patch("agentic_devtools.orchestration.execution.decision_gate.resolve_decision") as mock_resolve:
                with pytest.raises(SystemExit) as exc_info:
                    advance_workflow_cmd()
                assert exc_info.value.code == 1
                mock_resolve.assert_not_called()

        captured = capsys.readouterr()
        assert "must be a run identifier" in captured.err

    def test_decision_mode_drive_qualified_run_id_cli_rejected(self, temp_state_dir, capsys):
        """Drive-qualified --run-id values are rejected before resolve_decision is called."""
        import sys

        from agentic_devtools.cli.workflows import advance_workflow_cmd

        with patch.object(
            sys,
            "argv",
            ["agdt-advance-workflow", "--decision", "approve", "--decision-id", "d-6", "--run-id", "C:tmp"],
        ):
            with patch("agentic_devtools.orchestration.execution.decision_gate.resolve_decision") as mock_resolve:
                with pytest.raises(SystemExit) as exc_info:
                    advance_workflow_cmd()
                assert exc_info.value.code == 1
                mock_resolve.assert_not_called()

        captured = capsys.readouterr()
        assert "must be a run identifier" in captured.err
