"""Tests for the review_commands module and helper functions."""

import json
from unittest.mock import MagicMock, patch

from ._persistence_test_helpers import PersistenceTestHelpers


class TestSetupPullRequestReviewPersistence(PersistenceTestHelpers):
    def test_calls_set_bootstrap_state_with_pr_worktree_key(self):
        """Regression: set_bootstrap_state() must be called with worktree_key=PR{id}."""
        mock_set_bootstrap, _, _ = self._run_setup_with_captures()

        mock_set_bootstrap.assert_called_once_with(worktree_key="PR123")

    def test_skips_set_bootstrap_state_when_env_var_set(self, monkeypatch):
        """FR-004: set_bootstrap_state() must NOT be called when AGENTIC_DEVTOOLS_STATE_DIR is set."""
        monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", "/tmp/pinned-state")
        mock_set_bootstrap, _, _ = self._run_setup_with_captures()

        mock_set_bootstrap.assert_not_called()

    def test_skips_set_bootstrap_state_when_env_var_whitespace_only(self, monkeypatch):
        """FR-004: whitespace-only AGENTIC_DEVTOOLS_STATE_DIR is treated as unset (calls bootstrap)."""
        monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", "   ")
        mock_set_bootstrap, _, _ = self._run_setup_with_captures()

        mock_set_bootstrap.assert_called_once_with(worktree_key="PR123")

    def test_sets_agdt_run_id_with_12_char_hex(self):
        """Regression: agdt_run_id must be stored as a 12-character hex string."""
        import re

        _, mock_set_value, _ = self._run_setup_with_captures()

        run_id_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "agdt_run_id"]
        assert len(run_id_calls) == 1
        run_id = run_id_calls[0][0][1]
        assert re.fullmatch(r"[0-9a-f]{12}", run_id), f"Expected 12-char hex, got {run_id!r}"

    def test_does_not_set_version_control_current_branch(self):
        """Regression: versionControl.currentBranch must NOT be set during bootstrap.

        The function checks out the PR source branch after bootstrap, so
        storing the pre-checkout branch would cause persist_if_dirty() to
        target the wrong -agdt branch.  Let persist_if_dirty() resolve it
        from git at runtime instead.
        """
        _, mock_set_value, _ = self._run_setup_with_captures()

        branch_calls = [c for c in mock_set_value.call_args_list if c[0][0] == "versionControl.currentBranch"]
        assert len(branch_calls) == 0

    def test_bootstrap_failure_logs_warning_and_continues(self, capsys):
        """Regression: bootstrap init failure must log to stderr and not abort review setup."""
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
                                                        with patch(
                                                            "agentic_devtools.state.set_bootstrap_state",
                                                            side_effect=OSError("disk full"),
                                                        ):
                                                            with patch("agentic_devtools.state.set_value"):
                                                                with patch("agentic_devtools.state.delete_value"):
                                                                    setup_pull_request_review()

        captured = capsys.readouterr()
        assert "WARNING: bootstrap state init failed" in captured.err
        assert "disk full" in captured.err
