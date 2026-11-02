"""Tests for the review_commands module and helper functions."""

from unittest.mock import MagicMock, patch

from ._persistence_test_helpers import PersistenceTestHelpers


class TestSetupPullRequestReviewPersistence(PersistenceTestHelpers):
    def test_rescopes_review_metadata_to_post_sync_head(self):
        """Review artifacts use the commit that remains after branch synchronization."""
        from agentic_devtools.cli.azure_devops.review_commands import setup_pull_request_review

        old_commit = "abcdef1234567890abcdef1234567890abcdef12"
        new_commit = "1234567890abcdef1234567890abcdef12345678"
        refreshed_file_path = "/src/refreshed.py"
        pr_details = {
            "pullRequest": {
                "pullRequestId": 123,
                "title": "Test PR",
                "createdBy": {"displayName": "Test User"},
                "sourceRefName": "refs/heads/feature/test",
                "targetRefName": "refs/heads/main",
                "lastMergeSourceCommit": {"commitId": old_commit},
            },
            "files": [],
            "threads": [],
        }
        refreshed_pr_details = {
            "pullRequest": {
                **pr_details["pullRequest"],
                "lastMergeSourceCommit": {"commitId": new_commit},
            },
            "files": [{"path": refreshed_file_path, "changeType": "edit", "lineDiffBlocks": []}],
            "threads": [],
        }
        mock_git_result = MagicMock(returncode=0, stdout="/repo/root\n")
        mock_config = MagicMock(
            organization="https://dev.azure.com/testorg",
            project="TestProject",
            repository="test-repo",
        )
        mock_set_value = MagicMock()
        captured_pr_details = {}
        mock_get_pull_request_details = MagicMock(side_effect=[pr_details, refreshed_pr_details])

        def capture_generate(_pr_id, details, *_args):
            captured_pr_details.update(details)
            return 0, 0, 0, MagicMock(), []

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=self._default_get_value,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                mock_get_pull_request_details,
            ),
            patch("builtins.open", create=True),
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                return_value=(True, None, set(), False, True),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands._get_current_commit_hash",
                return_value=new_commit,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                side_effect=capture_generate,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands._scaffold_threads_for_review"),
            patch("agentic_devtools.cli.azure_devops.review_commands._persist_processing_paths_to_review_state"),
            patch("agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"),
            patch("agentic_devtools.cli.azure_devops.pr_review_artifacts.generate_v2_review_artifacts"),
            patch("agentic_devtools.state.set_workflow_state"),
            patch("agentic_devtools.prompts.loader.load_and_render_prompt"),
            patch("agentic_devtools.config.load_review_focus_areas", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_commands.run_safe", return_value=mock_git_result),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.AzureDevOpsConfig.from_state",
                return_value=mock_config,
            ),
            patch("agentic_devtools.state.set_bootstrap_state"),
            patch("agentic_devtools.state.set_value", mock_set_value),
            patch("agentic_devtools.state.delete_value"),
        ):
            setup_pull_request_review()

        assert captured_pr_details["pullRequest"]["lastMergeSourceCommit"]["commitId"] == new_commit
        assert captured_pr_details["files"][0]["path"] == refreshed_file_path
        assert mock_get_pull_request_details.call_count == 2
        short_hash_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "review.commit_hash_short"]
        assert any(call[0][1] == new_commit[:12] for call in short_hash_calls)

    def test_rescopes_review_metadata_when_head_advances_without_push(self):
        """Review metadata refreshes when reset/fetch advances HEAD without a local push."""
        from agentic_devtools.cli.azure_devops.review_commands import setup_pull_request_review

        old_commit = "abcdef1234567890abcdef1234567890abcdef12"
        new_commit = "1234567890abcdef1234567890abcdef12345678"
        refreshed_file_path = "/src/refreshed-without-push.py"
        pr_details = {
            "pullRequest": {
                "pullRequestId": 123,
                "title": "Test PR",
                "createdBy": {"displayName": "Test User"},
                "sourceRefName": "refs/heads/feature/test",
                "targetRefName": "refs/heads/main",
                "lastMergeSourceCommit": {"commitId": old_commit},
            },
            "files": [],
            "threads": [],
        }
        refreshed_pr_details = {
            "pullRequest": {
                **pr_details["pullRequest"],
                "lastMergeSourceCommit": {"commitId": new_commit},
            },
            "files": [{"path": refreshed_file_path, "changeType": "edit", "lineDiffBlocks": []}],
            "threads": [],
        }
        mock_git_result = MagicMock(returncode=0, stdout="/repo/root\n")
        mock_config = MagicMock(
            organization="https://dev.azure.com/testorg",
            project="TestProject",
            repository="test-repo",
        )
        mock_set_value = MagicMock()
        captured_pr_details = {}
        mock_get_pull_request_details = MagicMock(side_effect=[pr_details, refreshed_pr_details])

        def capture_generate(_pr_id, details, *_args):
            captured_pr_details.update(details)
            return 0, 0, 0, MagicMock(), []

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=self._default_get_value,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                mock_get_pull_request_details,
            ),
            patch("builtins.open", create=True),
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                return_value=(True, None, set(), False, None),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands._get_current_commit_hash",
                return_value=new_commit,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                side_effect=capture_generate,
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands._scaffold_threads_for_review"),
            patch("agentic_devtools.cli.azure_devops.review_commands._persist_processing_paths_to_review_state"),
            patch("agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"),
            patch("agentic_devtools.cli.azure_devops.pr_review_artifacts.generate_v2_review_artifacts"),
            patch("agentic_devtools.state.set_workflow_state"),
            patch("agentic_devtools.prompts.loader.load_and_render_prompt"),
            patch("agentic_devtools.config.load_review_focus_areas", return_value=None),
            patch("agentic_devtools.cli.azure_devops.review_commands.run_safe", return_value=mock_git_result),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.AzureDevOpsConfig.from_state",
                return_value=mock_config,
            ),
            patch("agentic_devtools.state.set_bootstrap_state"),
            patch("agentic_devtools.state.set_value", mock_set_value),
            patch("agentic_devtools.state.delete_value"),
        ):
            setup_pull_request_review()

        assert captured_pr_details["pullRequest"]["lastMergeSourceCommit"]["commitId"] == new_commit
        assert captured_pr_details["files"][0]["path"] == refreshed_file_path
        assert mock_get_pull_request_details.call_count == 2
        short_hash_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "review.commit_hash_short"]
        assert any(call[0][1] == new_commit[:12] for call in short_hash_calls)
