"""Tests for get_pull_request_details function."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.azure_devops import get_pull_request_details


class TestGetPullRequestDetails:
    """Tests for get_pull_request_details command."""

    def test_dry_run_output(self, temp_state_dir, clear_state_before, capsys):
        """Should show dry run output when dry_run is set."""
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "23046")
        set_value("dry_run", "true")

        get_pull_request_details()

        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out
        assert "23046" in captured.out
        assert "Organization" in captured.out
        assert "Project" in captured.out
        assert "Repository" in captured.out

    def test_dry_run_shows_output_path(self, temp_state_dir, clear_state_before, capsys):
        """Should show output file path in dry run."""
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "true")

        get_pull_request_details()

        captured = capsys.readouterr()
        assert "Output" in captured.out
        assert "temp-get-pull-request-details-response.json" in captured.out

    def test_missing_pull_request_id(self, temp_state_dir, clear_state_before, capsys):
        """Should raise KeyError if pull_request_id is not set."""
        from agentic_devtools.state import set_value

        set_value("dry_run", "true")  # Don't set pull_request_id

        with pytest.raises(KeyError, match="pull_request_id"):
            get_pull_request_details()


class TestGetPullRequestDetailsExecution:
    """Tests for get_pull_request_details when not in dry-run mode."""

    def test_exits_when_rest_returns_none(self, temp_state_dir, clear_state_before, capsys):
        """Should exit with error when the project-scoped REST PR fetch returns None.

        The REST helper returns None on any failure (non-200 status, network error,
        unparseable body), so this single path replaces the previous az-CLI failure
        and invalid-JSON cases.
        """
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={"Authorization": "Basic xxx"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=None,
            ),
        ):
            with pytest.raises(SystemExit) as exc_info:
                get_pull_request_details()

            assert exc_info.value.code == 1

        captured = capsys.readouterr()
        assert "Error" in captured.err
        assert "Failed to get pull request details" in captured.err

    def test_successful_execution(self, temp_state_dir, clear_state_before, tmp_path, capsys):
        """Should successfully retrieve and save PR details."""
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")

        # Mock PR data
        pr_data = {
            "pullRequestId": 12345,
            "title": "Test PR",
            "isDraft": False,
            "status": "active",
            "autoCompleteSetBy": None,
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature",
            "lastMergeTargetCommit": {"commitId": "abc123"},
            "lastMergeSourceCommit": {"commitId": "def456"},
            "repository": {
                "id": "repo-id-123",
                "project": {"id": "project-id-123"},
            },
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={"Authorization": "Basic xxx"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=pr_data,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.sync_git_ref"),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=[{"id": 1}],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_reviewer_payload",
                return_value={"reviewedFiles": []},
            ),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details()

        captured = capsys.readouterr()
        assert "12345" in captured.out
        assert "Test PR" in captured.out
        assert "Pull request details retrieved successfully" in captured.out

    def test_handles_auto_complete_set_by(self, temp_state_dir, clear_state_before, capsys):
        """Should display auto-complete info when set."""
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")

        pr_data = {
            "pullRequestId": 12345,
            "title": "Test PR",
            "isDraft": False,
            "status": "active",
            "autoCompleteSetBy": {"displayName": "John Doe"},
            "targetRefName": "refs/heads/main",
            "sourceRefName": "refs/heads/feature",
            "repository": {"id": "repo-id", "project": {"id": "project-id"}},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=pr_data,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.sync_git_ref"),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
                return_value=None,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_reviewer_payload",
                return_value=None,
            ),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details()

        captured = capsys.readouterr()
        assert "Auto-Complete" in captured.out
        assert "John Doe" in captured.out

    def test_skips_sync_and_reviewer_when_no_branches_or_repo_id(self, temp_state_dir, clear_state_before, capsys):
        """Should skip sync_git_ref and reviewer fetch when branches/repo_id missing."""
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")

        # PR data with no branch refs, no repo id
        pr_data = {
            "pullRequestId": 12345,
            "title": "Minimal PR",
            "isDraft": False,
            "status": "active",
            "autoCompleteSetBy": None,
            "repository": {},
        }

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=pr_data,
            ),
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.sync_git_ref") as mock_sync,
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_threads",
            ) as mock_threads,
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_pull_request_iterations",
            ) as mock_iterations,
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands._get_reviewer_payload",
            ) as mock_reviewer,
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details()

        # sync_git_ref not called because no branches
        mock_sync.assert_not_called()
        # threads/iterations/reviewer not called because no repo_id
        mock_threads.assert_not_called()
        mock_iterations.assert_not_called()
        mock_reviewer.assert_not_called()

    def test_rest_fetch_receives_pr_id_and_config(self, temp_state_dir, clear_state_before):
        """The REST fetch must receive the PR id and the resolved config (project scope).

        This is the essence of the fix: unlike the previous org-scoped
        ``az repos pr show``, the REST path passes the full ``AzureDevOpsConfig``
        (org + project + repository) so the request is project-scoped and
        authenticated with the PAT-derived headers.
        """
        from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
        from agentic_devtools.state import set_value

        set_value("pull_request_id", "12345")
        set_value("dry_run", "false")
        set_value("organization", "my-org")
        set_value("project", "my-project")
        set_value("repository", "my-repo")

        pr_data = {"pullRequestId": 12345, "title": "Test PR", "repository": {}}

        with (
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pat",
                return_value="fake-pat",
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_auth_headers",
                return_value={"Authorization": "Basic xxx"},
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.fetch_pull_request_via_rest",
                return_value=pr_data,
            ) as mock_fetch,
            patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.sync_git_ref"),
            patch(
                "agentic_devtools.cli.azure_devops.pull_request_details_commands.get_diff_entries",
                return_value=[],
            ),
            patch("pathlib.Path.mkdir"),
            patch("builtins.open", MagicMock()),
        ):
            get_pull_request_details()

        mock_fetch.assert_called_once()
        call_args = mock_fetch.call_args.args
        assert call_args[0] == 12345
        assert isinstance(call_args[1], AzureDevOpsConfig)
        assert call_args[1].organization == "https://dev.azure.com/my-org"
        assert call_args[1].project == "my-project"
        assert call_args[1].repository == "my-repo"
        assert call_args[2] == {"Authorization": "Basic xxx"}
