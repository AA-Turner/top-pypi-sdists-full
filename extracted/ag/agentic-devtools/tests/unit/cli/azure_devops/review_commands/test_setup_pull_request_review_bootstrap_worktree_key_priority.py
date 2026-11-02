"""Tests for the review_commands module and helper functions."""

from unittest.mock import MagicMock, patch


class TestSetupPullRequestReviewBootstrapWorktreeKeyPriority:
    """Tests that setup_pull_request_review() uses issue key as worktree_key when available."""

    def _make_pr_details(self):
        return {
            "pullRequest": {
                "pullRequestId": 123,
                "title": "Test PR",
                "createdBy": {"displayName": "Test User"},
                "sourceRefName": "refs/heads/feature/PROJECT-1234/test",
                "targetRefName": "refs/heads/main",
            },
            "files": [],
            "threads": [],
        }

    def _run_setup_with_issue_key(self, jira_issue_key):
        """Run setup_pull_request_review with a jira_issue_key and capture set_bootstrap_state."""
        from agentic_devtools.cli.azure_devops.review_commands import setup_pull_request_review

        def get_value_with_issue_key(key, default=None):
            mapping = {
                "pull_request_id": "123",
                "jira.issue_key": jira_issue_key,
                "include_reviewed": "false",
            }
            return mapping.get(key, default)

        mock_git_result = MagicMock()
        mock_git_result.returncode = 0
        mock_git_result.stdout = "/repo/root\n"

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        mock_set_bootstrap = MagicMock()

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=get_value_with_issue_key,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
        ):
            with patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=self._make_pr_details(),
            ):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = __import__("json").dumps(
                        self._make_pr_details()
                    )
                    with patch("pathlib.Path.exists", return_value=True):
                        with patch(
                            "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                            return_value=(True, None, set(), False, None),
                        ):
                            with patch(
                                "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                                return_value=(3, 0, 0, MagicMock(), []),
                            ):
                                with patch(
                                    "agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"
                                ):
                                    with patch("agentic_devtools.state.set_workflow_state"):
                                        with patch("agentic_devtools.prompts.loader.load_and_render_prompt"):
                                            with patch(
                                                "agentic_devtools.config.load_review_focus_areas",
                                                return_value=None,
                                            ):
                                                with patch(
                                                    "agentic_devtools.cli.azure_devops.review_commands.run_safe",
                                                    return_value=mock_git_result,
                                                ):
                                                    with patch(
                                                        "agentic_devtools.cli.azure_devops.review_commands.AzureDevOpsConfig.from_state",
                                                        return_value=mock_config,
                                                    ):
                                                        with patch(
                                                            "agentic_devtools.state.set_bootstrap_state",
                                                            mock_set_bootstrap,
                                                        ):
                                                            with patch("agentic_devtools.state.set_value"):
                                                                with patch("agentic_devtools.state.delete_value"):
                                                                    setup_pull_request_review()

        return mock_set_bootstrap

    def test_uses_issue_key_as_worktree_key_when_both_available(self):
        """When both pull_request_id and jira.issue_key are in state, worktree_key is the issue key.

        Issue key takes priority over PR ID as the worktree_key, matching the
        resolve_worktree_key() priority in agdt_branch.py.
        """
        mock_set_bootstrap = self._run_setup_with_issue_key("PROJECT-1234")
        mock_set_bootstrap.assert_called_once_with(worktree_key="PROJECT-1234")

    def test_falls_back_to_pr_id_when_no_issue_key(self):
        """When only pull_request_id is in state (no jira.issue_key), worktree_key is PR{id}."""
        mock_set_bootstrap = self._run_setup_with_issue_key(None)
        mock_set_bootstrap.assert_called_once_with(worktree_key="PR123")

    def test_falls_back_to_pr_id_when_issue_key_is_whitespace_only(self):
        """When jira.issue_key is whitespace-only, worktree_key falls back to PR{id}."""
        mock_set_bootstrap = self._run_setup_with_issue_key("   ")
        mock_set_bootstrap.assert_called_once_with(worktree_key="PR123")

    def test_falls_back_to_pr_id_when_issue_key_is_non_string(self):
        """When jira.issue_key is a non-string truthy value, worktree_key falls back to PR{id}."""
        mock_set_bootstrap = self._run_setup_with_issue_key(42)
        mock_set_bootstrap.assert_called_once_with(worktree_key="PR123")
