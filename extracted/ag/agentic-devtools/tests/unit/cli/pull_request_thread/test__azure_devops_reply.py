"""Tests for _azure_devops_reply."""

from unittest.mock import MagicMock, patch

from agentic_devtools.adapters.base import PullRequestThreadReplyRequest
from agentic_devtools.cli.pull_request_thread import _azure_devops_reply


def _request(resolve: bool = False) -> PullRequestThreadReplyRequest:
    return PullRequestThreadReplyRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_number=12,
        discussion_id=34,
        body="reply",
        resolve=resolve,
        azure_organization="org",
        azure_project="proj",
    )


class TestAzureDevOpsReply:
    """Validate reply, resolution, and partial-success paths."""

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-id")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers", return_value={})
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="pat")
    @patch("agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id")
    @patch("agentic_devtools.tools.azure_devops.reply_to_pull_request_thread")
    def test_replied_and_resolved_on_success(
        self,
        mock_reply: MagicMock,
        mock_resolve: MagicMock,
        _mock_pat: MagicMock,
        _mock_headers: MagicMock,
        _mock_repo_id: MagicMock,
        _mock_requests: MagicMock,
    ) -> None:
        _mock_requests.return_value.get.return_value = MagicMock(status_code=200, json=lambda: [])
        mock_reply.return_value = {"comment_id": 99}

        result = _azure_devops_reply(_request(resolve=True))

        assert result.mutation_status == "replied_and_resolved"
        assert result.reply_id == 99
        assert result.resolution_status == "resolved"
        mock_resolve.assert_called_once()

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-id")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers", return_value={})
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="pat")
    @patch("agentic_devtools.tools.azure_devops.reply_to_pull_request_thread")
    def test_replied_only_when_resolve_false(
        self,
        mock_reply: MagicMock,
        _mock_pat: MagicMock,
        _mock_headers: MagicMock,
        _mock_repo_id: MagicMock,
        _mock_requests: MagicMock,
    ) -> None:
        _mock_requests.return_value.get.return_value = MagicMock(status_code=200, json=lambda: [])
        mock_reply.return_value = {"comment_id": 77}

        result = _azure_devops_reply(_request(resolve=False))

        assert result.mutation_status == "replied"
        assert result.reply_id == 77
        assert result.resolution_status == "not_requested"

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-id")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers", return_value={})
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="pat")
    @patch(
        "agentic_devtools.tools.azure_devops.reply_to_pull_request_thread",
        side_effect=RuntimeError("network error"),
    )
    def test_returns_failed_when_reply_raises(
        self,
        _mock_reply: MagicMock,
        _mock_pat: MagicMock,
        _mock_headers: MagicMock,
        _mock_repo_id: MagicMock,
        mock_requests: MagicMock,
    ) -> None:
        result = _azure_devops_reply(_request(resolve=True))

        assert result.mutation_status == "failed"
        assert result.reply_id is None
        mock_requests.assert_not_called()

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-id")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers", return_value={})
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="pat")
    @patch("agentic_devtools.tools.azure_devops.reply_to_pull_request_thread", return_value={"comment_id": 0})
    def test_returns_failed_when_reply_id_is_non_positive(
        self,
        _mock_reply: MagicMock,
        _mock_pat: MagicMock,
        _mock_headers: MagicMock,
        _mock_repo_id: MagicMock,
        mock_requests: MagicMock,
    ) -> None:
        result = _azure_devops_reply(_request(resolve=False))

        assert result.mutation_status == "failed"
        assert result.reply_id is None
        mock_requests.assert_not_called()

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-id")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers", return_value={})
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="pat")
    @patch(
        "agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id",
        side_effect=RuntimeError("resolve failed"),
    )
    @patch("agentic_devtools.tools.azure_devops.reply_to_pull_request_thread")
    def test_partial_success_when_reply_ok_but_resolve_fails(
        self,
        mock_reply: MagicMock,
        _mock_resolve: MagicMock,
        _mock_pat: MagicMock,
        _mock_headers: MagicMock,
        _mock_repo_id: MagicMock,
        mock_requests: MagicMock,
    ) -> None:
        """Reply was posted successfully; resolution failure must yield partial_success."""
        mock_requests.return_value.get.return_value = MagicMock(status_code=200, json=lambda: [])
        mock_reply.return_value = {"comment_id": 55}

        result = _azure_devops_reply(_request(resolve=True))

        assert result.mutation_status == "partial_success"
        assert result.reply_id == 55
        assert result.resolution_status == "failed"
        assert result.diagnostics
        assert "resolve failed" in result.diagnostics[0]

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-id")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers", return_value={})
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    @patch("agentic_devtools.tools.azure_devops.reply_to_pull_request_thread")
    def test_direct_call_uses_state_org_project_and_request_repository(
        self,
        mock_reply: MagicMock,
        mock_from_state: MagicMock,
        _mock_pat: MagicMock,
        _mock_headers: MagicMock,
        _mock_repo_id: MagicMock,
        _mock_requests: MagicMock,
    ) -> None:
        _mock_requests.return_value.get.return_value = MagicMock(status_code=200, json=lambda: [])
        mock_from_state.return_value = MagicMock(
            organization="org-from-state",
            project="project-from-state",
            repository="repo-from-state",
        )
        mock_reply.return_value = {"comment_id": 88}
        request = PullRequestThreadReplyRequest(
            provider="azure_devops",
            repository="repo-from-request",
            pull_request_number=12,
            discussion_id=34,
            body="reply",
            resolve=False,
        )

        _azure_devops_reply(request)

        config = mock_reply.call_args.kwargs["config"]
        assert config.organization == "org-from-state"
        assert config.project == "project-from-state"
        assert config.repository == "repo-from-request"

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-id")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers", return_value={})
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="pat")
    @patch(
        "agentic_devtools.tools.azure_devops.reply_to_pull_request_thread",
        side_effect=RuntimeError("timeout"),
    )
    def test_returns_failed_when_reply_transport_is_ambiguous(
        self,
        _mock_reply: MagicMock,
        _mock_pat: MagicMock,
        _mock_headers: MagicMock,
        _mock_repo_id: MagicMock,
        mock_requests: MagicMock,
    ) -> None:
        result = _azure_devops_reply(_request(resolve=False))

        assert result.mutation_status == "failed"
        assert result.reply_id is None
        mock_requests.assert_not_called()
