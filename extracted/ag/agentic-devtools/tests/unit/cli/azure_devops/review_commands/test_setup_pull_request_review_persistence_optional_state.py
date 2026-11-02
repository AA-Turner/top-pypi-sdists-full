"""Tests for the review_commands module and helper functions."""

import json
from unittest.mock import MagicMock, patch

from ._persistence_test_helpers import PersistenceTestHelpers


class TestSetupPullRequestReviewPersistence(PersistenceTestHelpers):
    def test_resets_copilot_model_id_when_present(self):
        """Regression: copilot.model_id must be re-set after bootstrap when originally present."""
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        def get_value_with_model_id(key, default=None):
            mapping = {
                "pull_request_id": "456",
                "jira.issue_key": None,
                "include_reviewed": "false",
                "copilot.model_id": "gpt-4o",
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
                side_effect=get_value_with_model_id,
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

        model_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "copilot.model_id"]
        assert len(model_calls) >= 1
        assert model_calls[0][0][1] == "gpt-4o"

    def test_does_not_set_copilot_model_id_when_absent(self):
        """Regression: copilot.model_id must NOT be re-set when it was not in state."""
        _, mock_set_value, _ = self._run_setup_with_captures()

        model_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "copilot.model_id"]
        assert len(model_calls) == 0

    def test_resets_dry_run_when_present(self):
        """Regression: dry_run must be re-set after bootstrap when originally present."""
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        def get_value_with_dry_run(key, default=None):
            mapping = {
                "pull_request_id": "456",
                "jira.issue_key": None,
                "include_reviewed": "false",
                "dry_run": "true",
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
                side_effect=get_value_with_dry_run,
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

        dry_run_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "dry_run"]
        assert len(dry_run_calls) >= 1
        assert dry_run_calls[0][0][1] == "true"

    def test_does_not_set_dry_run_when_absent(self):
        """Regression: dry_run must NOT be re-set when it was not in state."""
        _, mock_set_value, _ = self._run_setup_with_captures()

        dry_run_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "dry_run"]
        assert len(dry_run_calls) == 0
