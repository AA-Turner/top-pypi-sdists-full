"""Tests for the review_commands module and helper functions."""

import json
from unittest.mock import MagicMock, patch


class TestSetupPullRequestReviewV2Artifacts:
    """Tests for the best-effort v2 artifact generation step (5d)."""

    def _make_pr_details(self):
        return {
            "pullRequest": {
                "pullRequestId": 123,
                "title": "Test PR",
                "createdBy": {"displayName": "Test User"},
                "sourceRefName": "refs/heads/feature/test",
                "targetRefName": "refs/heads/main",
            },
            "files": [],
            "threads": [],
        }

    def _default_get_value(self, key, default=None):
        mapping = {
            "pull_request_id": "123",
            "jira.issue_key": None,
            "include_reviewed": "false",
        }
        return mapping.get(key, default)

    def test_v2_artifact_failure_logs_warning_and_does_not_abort(self, capsys):
        """If generate_v2_review_artifacts raises, a warning is printed and setup continues."""
        from agentic_devtools.cli.azure_devops.review_commands import setup_pull_request_review

        mock_git_result = MagicMock()
        mock_git_result.returncode = 0
        mock_git_result.stdout = "/repo/root\n"

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=self._default_get_value,
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
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
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
                                                        with patch("agentic_devtools.state.set_bootstrap_state"):
                                                            with patch("agentic_devtools.state.set_value"):
                                                                with patch("agentic_devtools.state.delete_value"):
                                                                    with patch(
                                                                        "agentic_devtools.cli.azure_devops.pr_review_artifacts.generate_v2_review_artifacts",
                                                                        side_effect=RuntimeError("boom"),
                                                                    ):
                                                                        # Must not raise
                                                                        setup_pull_request_review()

        captured = capsys.readouterr()
        assert "Warning: v2 review artifact generation failed" in captured.err
        assert "setup unaffected" in captured.err
