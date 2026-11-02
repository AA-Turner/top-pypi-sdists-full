"""Tests for the review_commands module and helper functions."""

import json
from unittest.mock import MagicMock, patch

import pytest


class TestSetupPullRequestReviewSkippedFiles:
    """Tests for skipped files persistence in setup_pull_request_review."""

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

    def test_persists_skipped_files_to_review_state(self):
        """Test that skipped files are persisted to review state after scaffolding."""
        from agentic_devtools.cli.azure_devops.review_commands import setup_pull_request_review
        from agentic_devtools.cli.azure_devops.review_state import SkippedFile

        skipped = [SkippedFile(path="/src/gone.ts", reason="not_on_branch")]

        mock_git_result = MagicMock()
        mock_git_result.returncode = 0
        mock_git_result.stdout = "/repo/root\n"

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        mock_review_state = MagicMock()

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
                                return_value=(3, 0, 1, MagicMock(), skipped),
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
                                                                        "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state"
                                                                    ) as mock_rmw:
                                                                        mock_rmw.return_value.__enter__ = MagicMock(
                                                                            return_value=mock_review_state
                                                                        )
                                                                        mock_rmw.return_value.__exit__ = MagicMock(
                                                                            return_value=False
                                                                        )
                                                                        setup_pull_request_review()
                                                                        mock_rmw.assert_called_once_with(123)
                                                                        assert mock_review_state.skippedFiles == skipped

    def test_skips_persistence_when_no_skipped_files(self):
        """Test that read_modify_write_review_state is not called when skipped_files is empty."""
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
                                                                        "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state"
                                                                    ) as mock_rmw:
                                                                        setup_pull_request_review()
                                                                        mock_rmw.assert_not_called()

    @pytest.mark.parametrize(
        "exc_class",
        [
            FileNotFoundError,
            OSError,
            ValueError,
        ],
        ids=["FileNotFoundError", "OSError", "ValueError"],
    )
    def test_handles_persist_errors_gracefully(self, capsys, exc_class):
        """Test that errors from read_modify_write_review_state log a warning and don't abort setup."""
        from agentic_devtools.cli.azure_devops.review_commands import setup_pull_request_review
        from agentic_devtools.cli.azure_devops.review_state import SkippedFile

        skipped = [SkippedFile(path="/src/gone.ts", reason="not_on_branch")]

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
                                return_value=(3, 0, 1, MagicMock(), skipped),
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
                                                                        "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
                                                                        side_effect=exc_class("test error"),
                                                                    ):
                                                                        # Should not raise â€” exception is caught
                                                                        setup_pull_request_review()

        captured = capsys.readouterr()
        assert "Could not persist skipped files" in captured.err

    def test_handles_file_lock_error_gracefully(self, capsys):
        """Test that FileLockError from read_modify_write_review_state logs a warning and doesn't abort."""
        from agentic_devtools.cli.azure_devops.review_commands import setup_pull_request_review
        from agentic_devtools.cli.azure_devops.review_state import SkippedFile
        from agentic_devtools.file_locking import FileLockError

        skipped = [SkippedFile(path="/src/gone.ts", reason="not_on_branch")]

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
                                return_value=(3, 0, 1, MagicMock(), skipped),
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
                                                                        "agentic_devtools.cli.azure_devops.review_state.read_modify_write_review_state",
                                                                        side_effect=FileLockError("lock contention"),
                                                                    ):
                                                                        # Should not raise â€” FileLockError is caught
                                                                        setup_pull_request_review()

        captured = capsys.readouterr()
        assert "Could not persist skipped files" in captured.err

    def test_sets_rebase_conflicts_detected_when_conflicts_present(self):
        """When had_rebase_conflicts is True, set_value('review.rebase_conflicts_detected', 'true') is called.

        Covers line 940.
        """
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        mock_git_result = MagicMock()
        mock_git_result.returncode = 0
        mock_git_result.stdout = "/repo/root\n"

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        mock_set_value = MagicMock()

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
                            return_value=(True, None, set(), True, None),
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

        rebase_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "review.rebase_conflicts_detected"]
        assert len(rebase_calls) == 1
        assert rebase_calls[0][0][1] == "true"
