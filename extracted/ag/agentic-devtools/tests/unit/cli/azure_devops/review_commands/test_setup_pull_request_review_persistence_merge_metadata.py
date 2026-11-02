"""Tests for the review_commands module and helper functions."""

import json
from unittest.mock import MagicMock, patch

from ._persistence_test_helpers import PersistenceTestHelpers


class TestSetupPullRequestReviewPersistence(PersistenceTestHelpers):
    def test_handles_non_dict_last_merge_source_commit(self, capsys):
        """A null lastMergeSourceCommit does not raise and clears the stale key."""
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        pr_details_with_null_last_merge = {
            "pullRequest": {
                "pullRequestId": 123,
                "title": "Test PR",
                "createdBy": {"displayName": "Test User"},
                "sourceRefName": "refs/heads/feature/test",
                "targetRefName": "refs/heads/main",
                "lastMergeSourceCommit": None,  # JSON null: must not raise AttributeError
            },
            "files": [],
            "threads": [],
        }

        mock_git_result = MagicMock()
        mock_git_result.returncode = 0
        mock_git_result.stdout = "/repo/root\n"

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        mock_set_value = MagicMock()
        mock_delete_value = MagicMock()

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
                return_value=pr_details_with_null_last_merge,
            ):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
                        pr_details_with_null_last_merge
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
                                                            with patch(
                                                                "agentic_devtools.state.set_value",
                                                                mock_set_value,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.state.delete_value",
                                                                    mock_delete_value,
                                                                ):
                                                                    setup_pull_request_review()

        # commit_hash_short must NOT be set â€” null lastMergeSourceCommit treated as absent
        commit_hash_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "review.commit_hash_short"]
        assert len(commit_hash_calls) == 0

        # delete_value should have been called to clear any stale key
        delete_calls = [c for c in mock_delete_value.call_args_list if c[0][0] == "review.commit_hash_short"]
        assert len(delete_calls) == 1

        # No type warning for None (it's simply absent, not an unexpected type)
        captured = capsys.readouterr()
        assert "unexpected type" not in captured.err

    def test_warns_on_non_null_non_dict_last_merge_source_commit(self, capsys):
        """When lastMergeSourceCommit is not a dict and not None, emits warning and clears stale key."""
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        pr_details_with_invalid_last_merge = {
            "pullRequest": {
                "pullRequestId": 123,
                "title": "Test PR",
                "createdBy": {"displayName": "Test User"},
                "sourceRefName": "refs/heads/feature/test",
                "targetRefName": "refs/heads/main",
                "lastMergeSourceCommit": [],  # non-null, non-dict: should trigger warning
            },
            "files": [],
            "threads": [],
        }

        mock_git_result = MagicMock()
        mock_git_result.returncode = 0
        mock_git_result.stdout = "/repo/root\n"

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        mock_set_value = MagicMock()
        mock_delete_value = MagicMock()

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
                return_value=pr_details_with_invalid_last_merge,
            ):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
                        pr_details_with_invalid_last_merge
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
                                                            with patch(
                                                                "agentic_devtools.state.set_value",
                                                                mock_set_value,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.state.delete_value",
                                                                    mock_delete_value,
                                                                ):
                                                                    setup_pull_request_review()

        commit_hash_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "review.commit_hash_short"]
        assert len(commit_hash_calls) == 0

        delete_calls = [c for c in mock_delete_value.call_args_list if c[0][0] == "review.commit_hash_short"]
        assert len(delete_calls) == 1

        captured = capsys.readouterr()
        assert "unexpected type" in captured.err
        assert "list" in captured.err
