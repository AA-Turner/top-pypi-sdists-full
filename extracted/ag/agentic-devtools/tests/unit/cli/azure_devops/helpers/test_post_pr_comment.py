"""Tests for post_pr_comment helper function."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.azure_devops.helpers import PrCommentResolveFailedError, post_pr_comment


class TestPostPrComment:
    """Tests for post_pr_comment() — explicit-arg PR comment posting."""

    @pytest.fixture(autouse=True)
    def mock_pat_identity(self):
        with patch(
            "agentic_devtools.cli.azure_devops.finalization.identity.resolve_pat_identity",
            return_value="user-1",
        ):
            yield

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

    def test_idempotency_key_posts_new_thread_when_marker_belongs_to_another_author(
        self, mock_azure_devops_env
    ) -> None:
        """A marker from another identity does not suppress this approver's comment."""
        mock_requests = MagicMock()
        list_response = MagicMock()
        list_response.json.return_value = {
            "value": [
                {
                    "id": 41,
                    "status": "closed",
                    "comments": [
                        {
                            "id": 7,
                            "author": {"id": "other-user"},
                            "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nGreat PR!",
                        }
                    ],
                }
            ]
        }
        mock_requests.get.return_value = list_response
        post_response = MagicMock()
        post_response.json.return_value = {"id": 99}
        mock_requests.post.return_value = post_response
        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
            patch("agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id"),
            patch(
                "agentic_devtools.cli.azure_devops.finalization.identity.resolve_pat_identity", return_value="user-1"
            ),
            patch("agentic_devtools.cli.azure_devops.helpers.patch_comment") as mock_patch,
        ):
            thread_id = post_pr_comment(
                pull_request_id=42,
                content="Great PR!",
                config=mock_config,
                idempotency_key="key-1",
            )

        assert thread_id == 99
        mock_requests.post.assert_called_once()
        mock_patch.assert_not_called()

    def test_idempotency_key_fails_closed_when_authenticated_author_is_unknown(self, mock_azure_devops_env) -> None:
        """Without authenticated authorship, idempotent approval reuse and posting are unsafe."""
        mock_requests = MagicMock()
        mock_config = MagicMock()
        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
            patch("agentic_devtools.cli.azure_devops.finalization.identity.resolve_pat_identity", return_value=None),
            pytest.raises(RuntimeError, match="Could not resolve authenticated Azure DevOps identity"),
        ):
            post_pr_comment(
                pull_request_id=42,
                content="Great PR!",
                config=mock_config,
                idempotency_key="key-1",
            )

        mock_requests.get.assert_not_called()
        mock_requests.post.assert_not_called()

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

    def test_idempotency_key_reuses_existing_thread(self, mock_azure_devops_env, capsys) -> None:
        """An existing marker-matched thread is reused instead of posting a duplicate."""
        mock_requests = MagicMock()
        list_response = MagicMock()
        list_response.json.return_value = {
            "value": [
                {
                    "id": 41,
                    "status": "closed",
                    "comments": [
                        {
                            "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nGreat PR!",
                            "author": {"id": "user-1"},
                        }
                    ],
                }
            ]
        }
        mock_requests.get.return_value = list_response

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
                pull_request_id=42,
                content="Great PR!",
                config=mock_config,
                idempotency_key="key-1",
            )

        assert thread_id == 41
        mock_requests.post.assert_not_called()
        mock_resolve.assert_not_called()
        assert "Comment already exists" in capsys.readouterr().out

    def test_idempotency_key_is_embedded_in_new_comment(self, mock_azure_devops_env) -> None:
        """A new idempotent approval post stores the hidden marker in the thread body."""
        mock_requests = MagicMock()
        list_response = MagicMock()
        list_response.json.return_value = {"value": []}
        mock_requests.get.return_value = list_response
        post_response = MagicMock()
        post_response.json.return_value = {"id": 99}
        mock_requests.post.return_value = post_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
            patch("agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id"),
        ):
            post_pr_comment(
                pull_request_id=42,
                content="Great PR!",
                config=mock_config,
                idempotency_key="key-1",
            )

        posted_content = mock_requests.post.call_args.kwargs["json"]["comments"][0]["content"]
        assert posted_content.startswith("<!-- agdt-approval:idempotency-key:key-1 -->\n")
        assert posted_content.endswith("Great PR!")

    def test_idempotency_key_resolves_existing_active_thread(self, mock_azure_devops_env) -> None:
        """A reused active thread is closed instead of posting a duplicate."""
        mock_requests = MagicMock()
        list_response = MagicMock()
        list_response.json.return_value = {
            "value": [
                {
                    "id": 41,
                    "status": "active",
                    "comments": [
                        {
                            "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nGreat PR!",
                            "author": {"id": "user-1"},
                        }
                    ],
                }
            ]
        }
        mock_requests.get.return_value = list_response

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
                pull_request_id=42,
                content="Great PR!",
                config=mock_config,
                idempotency_key="key-1",
            )

        assert thread_id == 41
        mock_requests.post.assert_not_called()
        mock_resolve.assert_called_once()

    def test_idempotency_key_raises_when_existing_active_thread_cannot_be_resolved(self, mock_azure_devops_env) -> None:
        """A reused active thread reports a partial outcome when closing it fails."""
        mock_requests = MagicMock()
        list_response = MagicMock()
        list_response.json.return_value = {
            "value": [
                {
                    "id": 41,
                    "status": "active",
                    "comments": [
                        {
                            "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nGreat PR!",
                            "author": {"id": "user-1"},
                        }
                    ],
                }
            ]
        }
        mock_requests.get.return_value = list_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id",
                side_effect=RuntimeError("boom"),
            ),
            pytest.raises(PrCommentResolveFailedError, match="thread 41"),
        ):
            post_pr_comment(
                pull_request_id=42,
                content="Great PR!",
                config=mock_config,
                idempotency_key="key-1",
            )

    def test_idempotency_key_posts_when_existing_threads_do_not_match(self, mock_azure_devops_env) -> None:
        """Non-matching existing threads do not block a fresh approval post."""
        mock_requests = MagicMock()
        list_response = MagicMock()
        list_response.json.return_value = {
            "value": [{"id": 41, "status": "closed", "comments": [{"content": "Different comment"}]}]
        }
        mock_requests.get.return_value = list_response
        post_response = MagicMock()
        post_response.json.return_value = {"id": 99}
        mock_requests.post.return_value = post_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
            patch("agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id"),
        ):
            thread_id = post_pr_comment(
                pull_request_id=42,
                content="Great PR!",
                config=mock_config,
                idempotency_key="key-1",
            )

        assert thread_id == 99
        mock_requests.post.assert_called_once()

    def test_idempotency_key_reconciles_changed_content_on_reuse(self, mock_azure_devops_env, capsys) -> None:
        """Reusing a thread whose recorded content is stale patches it instead of leaving it outdated."""
        mock_requests = MagicMock()
        list_response = MagicMock()
        list_response.json.return_value = {
            "value": [
                {
                    "id": 41,
                    "status": "closed",
                    "comments": [
                        {
                            "id": 7,
                            "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nOld wording",
                            "author": {"id": "user-1"},
                        }
                    ],
                }
            ]
        }
        mock_requests.get.return_value = list_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
            patch("agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id") as mock_resolve,
            patch("agentic_devtools.cli.azure_devops.helpers.patch_comment") as mock_patch,
        ):
            thread_id = post_pr_comment(
                pull_request_id=42,
                content="New wording",
                config=mock_config,
                idempotency_key="key-1",
            )

        assert thread_id == 41
        mock_patch.assert_called_once()
        patched_content = mock_patch.call_args.args[7]
        assert patched_content.endswith("New wording")
        mock_resolve.assert_not_called()
        assert "updating comment 7" in capsys.readouterr().out

    def test_stale_marker_thread_without_valid_comment_id_raises(self, mock_azure_devops_env) -> None:
        """Stale marker content without a usable comment ID fails instead of reporting success."""
        mock_requests = MagicMock()
        list_response = MagicMock()
        list_response.json.return_value = {
            "value": [
                {
                    "id": 41,
                    "status": "closed",
                    "comments": [
                        {
                            "content": "<!-- agdt-approval:idempotency-key:key-1 -->\nOld wording",
                            "author": {"id": "user-1"},
                        }
                    ],
                }
            ]
        }
        mock_requests.get.return_value = list_response
        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
            patch("agentic_devtools.cli.azure_devops.helpers.patch_comment") as mock_patch,
            patch("agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id") as mock_resolve,
        ):
            with pytest.raises(RuntimeError, match="no valid comment ID"):
                post_pr_comment(
                    pull_request_id=42,
                    content="New wording",
                    config=mock_config,
                    idempotency_key="key-1",
                )

        mock_patch.assert_not_called()
        mock_resolve.assert_not_called()

    def test_http_errors_from_post_call_are_propagated(self, mock_azure_devops_env) -> None:
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

    def test_resolve_failure_raises_structured_error_with_thread_id(self, mock_azure_devops_env) -> None:
        """A resolve failure after a successful post raises a typed error carrying the thread ID.

        The comment was already created, so the caller does not need to re-post a
        duplicate; it can catch `PrCommentResolveFailedError` and report the partial
        outcome (posted but unresolved) using `exc.thread_id` instead of treating the
        whole operation as failed or as fully successful.
        """
        mock_requests = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 55}
        mock_requests.post.return_value = mock_response

        mock_config = MagicMock()
        mock_config.build_api_url.return_value = "https://example.com/threads"

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.require_requests", return_value=mock_requests),
            patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-1"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_pat", return_value="pat"),
            patch("agentic_devtools.cli.azure_devops.helpers.get_auth_headers", return_value={}),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id",
                side_effect=RuntimeError("boom"),
            ),
            pytest.raises(PrCommentResolveFailedError) as exc_info,
        ):
            post_pr_comment(pull_request_id=1, content="Hi", config=mock_config)

        assert exc_info.value.thread_id == 55
        assert "Comment posted (thread 55) but resolving it failed" in str(exc_info.value)

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
