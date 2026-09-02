"""Tests for post_pr_comment helper function."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.azure_devops.helpers import post_pr_comment


class TestPostPrComment:
    """Tests for post_pr_comment() — explicit-arg PR comment posting."""

    def test_dry_run_returns_none(self, mock_azure_devops_env, capsys) -> None:
        """Dry-run mode prints intent and returns None without making API calls."""
        result = post_pr_comment(pull_request_id=42, content="Hello", dry_run=True)

        assert result is None
        captured = capsys.readouterr()
        assert "DRY RUN" in captured.out
        assert "42" in captured.out
        assert "Hello" in captured.out

    def test_dry_run_leave_thread_active_suppresses_resolve_message(self, mock_azure_devops_env, capsys) -> None:
        """Dry-run with leave_thread_active=True does not print the resolve message."""
        post_pr_comment(pull_request_id=1, content="x", dry_run=True, leave_thread_active=True)

        captured = capsys.readouterr()
        assert "resolve" not in captured.out.lower()

    def test_dry_run_default_prints_resolve_message(self, mock_azure_devops_env, capsys) -> None:
        """Dry-run with default leave_thread_active=False prints the resolve message."""
        post_pr_comment(pull_request_id=1, content="x", dry_run=True)

        captured = capsys.readouterr()
        assert "resolve" in captured.out.lower()

    def test_posts_comment_and_returns_thread_id(self, mock_azure_devops_env) -> None:
        """Successful post returns the thread ID from the API response."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 99}
        mock_requests.post.return_value = mock_response

        mock_config = MagicMock()
        mock_config.organization = "https://dev.azure.com/org"
        mock_config.project = "MyProject"
        mock_config.repository = "my-repo"
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.get_auth_headers",
                return_value={"Authorization": "Basic xxx"},
            ),
            patch("agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id") as mock_resolve,
        ):
            thread_id = post_pr_comment(
                pull_request_id=42,
                content="Great PR!",
                config=mock_config,
            )

        assert thread_id == 99
        mock_requests.post.assert_called_once()
        # Thread is resolved by default
        mock_resolve.assert_called_once()

    def test_leave_thread_active_skips_resolve(self, mock_azure_devops_env) -> None:
        """leave_thread_active=True skips the thread resolution step."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 7}
        mock_requests.post.return_value = mock_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
            patch("agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id") as mock_resolve,
        ):
            thread_id = post_pr_comment(
                pull_request_id=5,
                content="Comment",
                config=mock_config,
                leave_thread_active=True,
            )

        assert thread_id == 7
        mock_resolve.assert_not_called()

    def test_http_error_propagates(self, mock_azure_devops_env) -> None:
        """HTTP errors from the POST call are propagated to the caller."""
        import requests as req_lib

        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = req_lib.HTTPError("500 error")
        mock_requests.post.return_value = mock_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
        ):
            with pytest.raises(req_lib.HTTPError):
                post_pr_comment(pull_request_id=1, content="Hi", config=mock_config)

    def test_uses_config_from_state_when_not_provided(self, mock_azure_devops_env) -> None:
        """When config is None, AzureDevOpsConfig.from_state() is called."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1}
        mock_requests.post.return_value = mock_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
                return_value=mock_config,
            ) as mock_from_state,
            patch("agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id"),
        ):
            post_pr_comment(pull_request_id=1, content="Hi")

        mock_from_state.assert_called_once()

    def test_raises_when_response_missing_id(self, mock_azure_devops_env) -> None:
        """RuntimeError is raised when the API response lacks a valid positive integer 'id'."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}  # no 'id'
        mock_requests.post.return_value = mock_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
        ):
            with pytest.raises(RuntimeError, match="'id' is missing or not a positive integer"):
                post_pr_comment(pull_request_id=1, content="Hi", config=mock_config)

    def test_raises_when_response_id_is_string(self, mock_azure_devops_env) -> None:
        """RuntimeError is raised when the API response 'id' is a non-integer type."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "not-an-int"}
        mock_requests.post.return_value = mock_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
        ):
            with pytest.raises(RuntimeError, match="'id' is missing or not a positive integer"):
                post_pr_comment(pull_request_id=1, content="Hi", config=mock_config)

    def test_raises_when_response_id_is_zero(self, mock_azure_devops_env) -> None:
        """RuntimeError is raised when the API response 'id' is 0 (invalid thread ID)."""
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 0}
        mock_requests.post.return_value = mock_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
        ):
            with pytest.raises(RuntimeError, match="'id' is missing or not a positive integer"):
                post_pr_comment(pull_request_id=1, content="Hi", config=mock_config)
