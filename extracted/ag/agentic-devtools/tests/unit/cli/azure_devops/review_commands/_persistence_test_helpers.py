"""Shared setup helpers for pull-request review persistence tests."""

import json
from contextlib import ExitStack
from unittest.mock import MagicMock, patch


class PersistenceTestHelpers:
    """Common setup runners used by persistence test modules."""

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

    def _run_setup_with_captures(self):
        """Run setup_pull_request_review and capture set_bootstrap_state/set_value/delete_value calls."""
        from agentic_devtools.cli.azure_devops.review_commands import setup_pull_request_review

        mock_git_result = MagicMock()
        mock_git_result.returncode = 0
        mock_git_result.stdout = "/repo/root\n"

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/testorg"
        mock_config.project = "TestProject"
        mock_config.repository = "test-repo"

        mock_set_bootstrap = MagicMock()
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
                                                            mock_set_bootstrap,
                                                        ):
                                                            with patch(
                                                                "agentic_devtools.state.set_value",
                                                                mock_set_value,
                                                            ):
                                                                with patch(
                                                                    "agentic_devtools.state.delete_value",
                                                                    mock_delete_value,
                                                                ):
                                                                    setup_pull_request_review()

        return mock_set_bootstrap, mock_set_value, mock_delete_value

    def _run_setup_with_post_sync_head(
        self,
        pr_details,
        current_commit_hash,
        *,
        write_error=False,
        capture_json_dump=False,
        fetch_side_effect=None,
    ):
        """Run setup with a pushed post-sync HEAD and return persisted state calls."""
        from agentic_devtools.cli.azure_devops.review_commands import setup_pull_request_review

        mock_git_result = MagicMock(returncode=0, stdout="/repo/root\n")
        mock_config = MagicMock(
            organization="https://dev.azure.com/testorg",
            project="TestProject",
            repository="test-repo",
        )
        mock_set_value = MagicMock()
        read_handle = MagicMock()
        read_handle.__enter__.return_value = read_handle
        mock_json_dump = MagicMock()

        def open_side_effect(_path, mode="r", **_kwargs):
            if write_error and "w" in mode:
                raise OSError("disk full")
            return read_handle

        with ExitStack() as stack:
            stack.enter_context(
                patch(
                    "agentic_devtools.cli.azure_devops.review_commands.get_value",
                    side_effect=self._default_get_value,
                )
            )
            stack.enter_context(
                patch(
                    "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                    return_value=False,
                )
            )
            fetch_details = stack.enter_context(
                patch(
                    "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                    return_value=pr_details,
                )
            )
            if fetch_side_effect is not None:
                fetch_details.side_effect = fetch_side_effect
            stack.enter_context(patch("builtins.open", side_effect=open_side_effect))
            stack.enter_context(
                patch(
                    "agentic_devtools.cli.azure_devops.review_branch_sync.json.dump",
                    mock_json_dump,
                )
            )
            stack.enter_context(patch("pathlib.Path.exists", return_value=True))
            stack.enter_context(
                patch(
                    "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                    return_value=(True, None, set(), False, True),
                )
            )
            stack.enter_context(
                patch(
                    "agentic_devtools.cli.azure_devops.review_commands._get_current_commit_hash",
                    return_value=current_commit_hash,
                )
            )
            stack.enter_context(patch("agentic_devtools.cli.azure_devops.review_branch_sync.time.sleep"))
            stack.enter_context(
                patch(
                    "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                    return_value=(3, 0, 0, MagicMock(), []),
                )
            )
            stack.enter_context(patch("agentic_devtools.cli.azure_devops.review_commands._scaffold_threads_for_review"))
            stack.enter_context(
                patch("agentic_devtools.cli.azure_devops.review_commands._persist_processing_paths_to_review_state")
            )
            stack.enter_context(patch("agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"))
            stack.enter_context(
                patch("agentic_devtools.cli.azure_devops.pr_review_artifacts.generate_v2_review_artifacts")
            )
            stack.enter_context(patch("agentic_devtools.state.set_workflow_state"))
            stack.enter_context(patch("agentic_devtools.prompts.loader.load_and_render_prompt"))
            stack.enter_context(patch("agentic_devtools.config.load_review_focus_areas", return_value=None))
            stack.enter_context(
                patch("agentic_devtools.cli.azure_devops.review_commands.run_safe", return_value=mock_git_result)
            )
            stack.enter_context(
                patch(
                    "agentic_devtools.cli.azure_devops.review_commands.AzureDevOpsConfig.from_state",
                    return_value=mock_config,
                )
            )
            stack.enter_context(patch("agentic_devtools.state.set_bootstrap_state"))
            stack.enter_context(patch("agentic_devtools.state.set_value", mock_set_value))
            stack.enter_context(patch("agentic_devtools.state.delete_value"))
            setup_pull_request_review()

        if capture_json_dump:
            return mock_set_value, mock_json_dump
        return mock_set_value
