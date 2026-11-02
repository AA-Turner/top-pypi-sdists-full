"""Tests for the review_commands module and helper functions."""

import json
from unittest.mock import MagicMock, patch

from ._persistence_test_helpers import PersistenceTestHelpers


class TestSetupPullRequestReviewPersistence(PersistenceTestHelpers):
    def test_resets_pull_request_id_in_scoped_state(self):
        """Regression: pull_request_id must be re-set after bootstrap changes state dir."""
        _, mock_set_value, _ = self._run_setup_with_captures()

        pr_id_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "pull_request_id"]
        assert len(pr_id_calls) == 1
        assert pr_id_calls[0][0][1] == "123"

    def test_resets_jira_issue_key_when_present(self):
        """Regression: jira.issue_key must be re-set after bootstrap when originally present."""
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        def get_value_with_jira(key, default=None):
            mapping = {
                "pull_request_id": "456",
                "jira.issue_key": "PROJECT-789",
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

        mock_set_value = MagicMock()

        pr_details = self._make_pr_details()

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=get_value_with_jira,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
        ):
            with patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=pr_details,
            ):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(pr_details)
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
                                                            with patch(
                                                                "agentic_devtools.state.set_value",
                                                                mock_set_value,
                                                            ):
                                                                with patch("agentic_devtools.state.delete_value"):
                                                                    setup_pull_request_review()

        jira_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "jira.issue_key"]
        assert len(jira_calls) >= 1
        assert jira_calls[0][0][1] == "PROJECT-789"

    def test_does_not_set_jira_issue_key_when_absent(self):
        """Regression: jira.issue_key must NOT be re-set when it was not in state."""
        _, mock_set_value, _ = self._run_setup_with_captures()

        jira_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "jira.issue_key"]
        assert len(jira_calls) == 0

    def test_resets_include_reviewed_when_true(self):
        """include_reviewed state key is no longer used; test that it's not set."""
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        def get_value_with_include_reviewed(key, default=None):
            mapping = {
                "pull_request_id": "456",
                "jira.issue_key": None,
            }
            return mapping.get(key, default)

        mock_git_result = MagicMock()
        mock_git_result.returncode = 0
        mock_git_result.stdout = "/repo/root\n"

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        mock_set_value = MagicMock()

        pr_details = self._make_pr_details()

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=get_value_with_include_reviewed,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
        ):
            with patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=pr_details,
            ):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(pr_details)
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
                                                            with patch(
                                                                "agentic_devtools.state.set_value",
                                                                mock_set_value,
                                                            ):
                                                                with patch("agentic_devtools.state.delete_value"):
                                                                    setup_pull_request_review()

        # include_reviewed is no longer set after bootstrap
        include_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "include_reviewed"]
        assert len(include_calls) == 0
