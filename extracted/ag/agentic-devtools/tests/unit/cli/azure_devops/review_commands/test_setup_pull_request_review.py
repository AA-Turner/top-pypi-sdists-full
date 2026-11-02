"""Tests for the review_commands module and helper functions."""

import json
from unittest.mock import MagicMock, patch

import pytest


class TestSetupPullRequestReview:
    """Tests for setup_pull_request_review function."""

    def test_exits_when_pull_request_id_missing(self, capsys):
        """Test exits with error when pull_request_id not in state."""
        from unittest.mock import patch

        with patch(
            "agentic_devtools.cli.azure_devops.review_commands.get_value",
            return_value=None,
        ):
            from agentic_devtools.cli.azure_devops.review_commands import (
                setup_pull_request_review,
            )

            with pytest.raises(SystemExit) as exc_info:
                setup_pull_request_review()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "pull_request_id is required" in captured.err

    def test_fetches_jira_issue_when_key_provided(self):
        """Test fetches Jira issue when jira.issue_key in state."""
        import json
        from unittest.mock import MagicMock, patch

        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        mock_pr_details = {
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
        mock_git_result = MagicMock(returncode=0, stdout="/repo/root\n")
        mock_config = MagicMock(
            organization="https://dev.azure.com/testorg",
            project="TestProject",
            repository="test-repo",
        )

        def get_value_side_effect(key, default=None):
            mapping = {
                "pull_request_id": "123",
                "jira.issue_key": "PROJECT-1234",
                "include_reviewed": "false",
            }
            return mapping.get(key, default)

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=get_value_side_effect,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
        ):
            with patch(
                "agentic_devtools.cli.azure_devops.review_commands._fetch_and_display_jira_issue"
            ) as mock_fetch_jira:
                with patch(
                    "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                    return_value=mock_pr_details,
                ):
                    with patch("builtins.open", create=True) as mock_open:
                        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_pr_details)
                        with patch("pathlib.Path.exists", return_value=True):
                            with patch(
                                "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                                return_value=(True, None, set(), False, None),
                            ):
                                with patch(
                                    "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                                    return_value=(5, 0, 0, MagicMock(), []),
                                ):
                                    with patch(
                                        "agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"
                                    ):
                                        with patch("agentic_devtools.prompts.loader.load_and_render_prompt"):
                                            with patch("agentic_devtools.state.set_workflow_state"):
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
                                                                        setup_pull_request_review()
                                                                    mock_fetch_jira.assert_called_once_with(
                                                                        "PROJECT-1234"
                                                                    )

    def test_exits_when_pr_details_fetch_returns_no_payload(self, capsys):
        """Setup stops when the provider-neutral details fetch returns no payload."""
        from unittest.mock import patch

        def get_value_side_effect(key, default=None):
            mapping = {
                "pull_request_id": "123",
                "jira.issue_key": None,
                "include_reviewed": "false",
            }
            return mapping.get(key, default)

        with patch(
            "agentic_devtools.cli.azure_devops.review_commands.get_value",
            side_effect=get_value_side_effect,
        ):
            with patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=None,
            ):
                with patch("agentic_devtools.state.set_bootstrap_state"):
                    with patch("agentic_devtools.state.set_value"):
                        from agentic_devtools.cli.azure_devops.review_commands import (
                            setup_pull_request_review,
                        )

                        with pytest.raises(SystemExit) as exc_info:
                            setup_pull_request_review()
                        assert exc_info.value.code == 1
                        captured = capsys.readouterr()
                        assert "PR details fetch did not return a valid payload" in captured.err

    def test_exits_on_checkout_failure(self, capsys):
        """Test exits with error when checkout fails."""
        import json
        from unittest.mock import patch

        mock_pr_details = {
            "pullRequest": {
                "sourceRefName": "refs/heads/feature/test",
            },
            "files": [],
            "threads": [],
        }

        def get_value_side_effect(key, default=None):
            mapping = {
                "pull_request_id": "123",
                "jira.issue_key": None,
                "include_reviewed": "false",
            }
            return mapping.get(key, default)

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=get_value_side_effect,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
        ):
            with patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=mock_pr_details,
            ):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_pr_details)
                    with patch("pathlib.Path.exists", return_value=True):
                        with patch(
                            "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                            return_value=(False, "Checkout error", set(), False, None),
                        ):
                            with patch("agentic_devtools.state.set_bootstrap_state"):
                                with patch("agentic_devtools.state.set_value"):
                                    with patch("agentic_devtools.state.delete_value"):
                                        from agentic_devtools.cli.azure_devops.review_commands import (
                                            setup_pull_request_review,
                                        )

                                        with pytest.raises(SystemExit) as exc_info:
                                            setup_pull_request_review()
                                    assert exc_info.value.code == 1

    def test_warns_when_no_source_branch(self, capsys):
        """Test prints warning when source branch cannot be determined."""
        import json
        from unittest.mock import MagicMock, patch

        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        mock_pr_details = {
            "pullRequest": {
                "sourceRefName": "",  # Empty source branch
                "title": "Test PR",
                "createdBy": {"displayName": "Test"},
                "targetRefName": "refs/heads/main",
            },
            "files": [],
            "threads": [],
        }
        mock_git_result = MagicMock(returncode=0, stdout="/repo/root\n")
        mock_config = MagicMock(
            organization="https://dev.azure.com/testorg",
            project="TestProject",
            repository="test-repo",
        )

        def get_value_side_effect(key, default=None):
            mapping = {
                "pull_request_id": "123",
                "jira.issue_key": None,
                "include_reviewed": "false",
            }
            return mapping.get(key, default)

        with patch(
            "agentic_devtools.cli.azure_devops.review_commands.get_value",
            side_effect=get_value_side_effect,
        ):
            with patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=mock_pr_details,
            ):
                with patch("builtins.open", create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_pr_details)
                    with patch("pathlib.Path.exists", return_value=True):
                        with patch(
                            "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                            return_value=(5, 0, 0, MagicMock(), []),
                        ):
                            with patch("agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"):
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
                                                                setup_pull_request_review()
                                                            captured = capsys.readouterr()
                                                            assert "Could not determine source branch" in captured.err

    def test_exits_when_workflow_prompt_initialization_fails(self, capsys):
        """Test exits with error when workflow prompt rendering fails."""
        from agentic_devtools.cli.azure_devops.review_commands import (
            setup_pull_request_review,
        )

        mock_pr_details = {
            "pullRequest": {
                "pullRequestId": 123,
                "sourceRefName": "refs/heads/feature/test",
                "title": "Test PR",
                "createdBy": {"displayName": "Test User"},
                "targetRefName": "refs/heads/main",
            },
            "files": [],
            "threads": [],
        }

        mock_git_result = MagicMock(returncode=0, stdout="/repo/root\n")
        mock_config = MagicMock(
            organization="https://dev.azure.com/testorg",
            project="TestProject",
            repository="test-repo",
        )

        def get_value_side_effect(key, default=None):
            mapping = {
                "pull_request_id": "123",
                "jira.issue_key": None,
                "include_reviewed": "false",
            }
            return mapping.get(key, default)

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.get_value",
                side_effect=get_value_side_effect,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.is_dry_run",
                return_value=False,
            ),
            patch(
                "agentic_devtools.cli.pull_request_details.get_pull_request_details",
                return_value=mock_pr_details,
            ),
            patch("builtins.open", create=True) as mock_open,
            patch("pathlib.Path.exists", return_value=True),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.checkout_and_sync_branch",
                return_value=(True, None, set(), False, False),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.generate_review_prompts",
                return_value=(5, 0, 0, MagicMock(), []),
            ),
            patch("agentic_devtools.cli.azure_devops.review_commands.print_review_instructions"),
            patch("agentic_devtools.state.set_workflow_state"),
            patch(
                "agentic_devtools.prompts.loader.load_and_render_prompt",
                side_effect=RuntimeError("prompt render failed"),
            ),
            patch("agentic_devtools.config.load_review_focus_areas", return_value=None),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.run_safe",
                return_value=mock_git_result,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_commands.AzureDevOpsConfig.from_state",
                return_value=mock_config,
            ),
            patch("agentic_devtools.state.set_bootstrap_state"),
            patch("agentic_devtools.state.set_value"),
            patch("agentic_devtools.state.delete_value"),
        ):
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_pr_details)

            with pytest.raises(SystemExit) as exc_info:
                setup_pull_request_review()

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "ERROR: Could not initialize workflow: prompt render failed" in captured.err
