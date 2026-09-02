"""Tests for CreatePlaceholderAndSetupWorktree."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.worktree_setup import (
    PlaceholderIssueResult,
    WorktreeSetupResult,
    create_placeholder_and_setup_worktree,
)


class TestCreatePlaceholderAndSetupWorktree:
    """Tests for create_placeholder_and_setup_worktree function."""

    @patch("agentic_devtools.cli.workflows.worktree_setup.setup_worktree_environment")
    @patch("agentic_devtools.cli.workflows.worktree_setup.check_worktree_exists")
    @patch("agentic_devtools.state.set_value")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_placeholder_issue")
    def test_full_workflow_success(
        self,
        mock_create_issue,
        mock_set_value,
        mock_check_exists,
        mock_setup,
    ):
        """Test successful full workflow - create issue and setup worktree."""
        mock_create_issue.return_value = PlaceholderIssueResult(success=True, issue_key="PROJECT-9999")
        mock_check_exists.return_value = None  # No existing worktree
        mock_setup.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-9999",
            branch_name="feature/PROJECT-9999/implementation",
            vscode_opened=False,
        )

        success, issue_key = create_placeholder_and_setup_worktree(
            project_key="PROJECT",
            issue_type="Task",
            workflow_name="create-jira-issue",
        )

        assert success is True
        assert issue_key == "PROJECT-9999"
        mock_set_value.assert_called_with("jira.issue_key", "PROJECT-9999")
        mock_setup.assert_called_once()
        # Verify open_vscode=False is passed
        call_kwargs = mock_setup.call_args[1]
        assert call_kwargs["open_vscode"] is False

    @patch("agentic_devtools.cli.workflows.worktree_setup.create_placeholder_issue")
    def test_fails_when_issue_creation_fails(self, mock_create_issue):
        """Test failure when issue creation fails."""
        mock_create_issue.return_value = PlaceholderIssueResult(success=False, error_message="API error")

        success, issue_key = create_placeholder_and_setup_worktree(
            project_key="PROJECT",
            issue_type="Task",
        )

        assert success is False
        assert issue_key is None

    @patch("agentic_devtools.cli.workflows.worktree_setup.create_placeholder_issue")
    def test_fails_when_success_but_issue_key_is_none(self, mock_create_issue):
        """Test failure when issue creation succeeds but returns None issue_key."""
        mock_create_issue.return_value = PlaceholderIssueResult(success=True, issue_key=None)

        success, issue_key = create_placeholder_and_setup_worktree(
            project_key="PROJECT",
            issue_type="Task",
        )

        assert success is False
        assert issue_key is None

    @patch("agentic_devtools.cli.workflows.worktree_setup.check_worktree_exists")
    @patch("agentic_devtools.state.set_value")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_placeholder_issue")
    def test_uses_existing_worktree(
        self,
        mock_create_issue,
        mock_set_value,
        mock_check_exists,
    ):
        """Test using existing worktree when it already exists."""
        mock_create_issue.return_value = PlaceholderIssueResult(success=True, issue_key="PROJECT-9999")
        mock_check_exists.return_value = "/repos/PROJECT-9999"  # Worktree exists

        success, issue_key = create_placeholder_and_setup_worktree(
            project_key="PROJECT",
            issue_type="Task",
        )

        assert success is True
        assert issue_key == "PROJECT-9999"

    @patch("agentic_devtools.cli.workflows.worktree_setup.setup_worktree_environment")
    @patch("agentic_devtools.cli.workflows.worktree_setup.check_worktree_exists")
    @patch("agentic_devtools.state.set_value")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_placeholder_issue")
    def test_returns_issue_key_even_when_worktree_fails(
        self,
        mock_create_issue,
        mock_set_value,
        mock_check_exists,
        mock_setup,
    ):
        """Test returning issue key even when worktree setup fails."""
        mock_create_issue.return_value = PlaceholderIssueResult(success=True, issue_key="PROJECT-9999")
        mock_check_exists.return_value = None
        mock_setup.return_value = WorktreeSetupResult(
            success=False,
            worktree_path="",
            branch_name="",
            error_message="Git worktree failed",
        )

        success, issue_key = create_placeholder_and_setup_worktree(
            project_key="PROJECT",
            issue_type="Task",
        )

        # Should return False but still have the issue_key
        assert success is False
        assert issue_key == "PROJECT-9999"

    @patch("agentic_devtools.cli.workflows.worktree_setup.setup_worktree_environment")
    @patch("agentic_devtools.cli.workflows.worktree_setup.check_worktree_exists")
    @patch("agentic_devtools.state.set_value")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_placeholder_issue")
    def test_does_not_open_vscode(
        self,
        mock_create_issue,
        mock_set_value,
        mock_check_exists,
        mock_setup,
    ):
        """Test that VS Code is not opened by the helper (caller owns auto-setup)."""
        mock_create_issue.return_value = PlaceholderIssueResult(success=True, issue_key="PROJECT-9999")
        mock_check_exists.return_value = None
        mock_setup.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-9999",
            branch_name="feature/PROJECT-9999/implementation",
            vscode_opened=False,
        )

        create_placeholder_and_setup_worktree(
            project_key="PROJECT",
            issue_type="Task",
            workflow_name="create-jira-issue",
        )

        # Verify open_vscode=False is passed to setup_worktree_environment
        call_kwargs = mock_setup.call_args[1]
        assert call_kwargs["open_vscode"] is False

    @patch("agentic_devtools.cli.workflows.worktree_setup.check_worktree_exists")
    @patch("agentic_devtools.state.set_value")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_placeholder_issue")
    def test_existing_worktree_does_not_open_vscode(
        self,
        mock_create_issue,
        mock_set_value,
        mock_check_exists,
    ):
        """Test that existing worktree path does not trigger VS Code open."""
        mock_create_issue.return_value = PlaceholderIssueResult(success=True, issue_key="PROJECT-9999")
        mock_check_exists.return_value = "/repos/PROJECT-9999"  # Worktree exists

        with patch("agentic_devtools.cli.workflows.worktree_setup.open_vscode_workspace") as mock_vscode:
            create_placeholder_and_setup_worktree(
                project_key="PROJECT",
                issue_type="Task",
            )
            mock_vscode.assert_not_called()
