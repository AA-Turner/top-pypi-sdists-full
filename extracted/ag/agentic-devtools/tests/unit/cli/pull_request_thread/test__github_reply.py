"""Tests for _github_reply."""

from unittest.mock import MagicMock, patch

from agentic_devtools.adapters.base import PullRequestThreadReplyRequest
from agentic_devtools.cli.pull_request_thread import _github_reply


def _unsafe_request(
    repository: str,
    *,
    resolve: bool = False,
    review_thread_id: str | None = None,
) -> PullRequestThreadReplyRequest:
    request = PullRequestThreadReplyRequest.__new__(PullRequestThreadReplyRequest)
    object.__setattr__(request, "provider", "github")
    object.__setattr__(request, "repository", repository)
    object.__setattr__(request, "pull_request_number", 12)
    object.__setattr__(request, "discussion_id", 34)
    object.__setattr__(request, "body", "reply")
    object.__setattr__(request, "resolve", resolve)
    object.__setattr__(request, "review_thread_id", review_thread_id)
    object.__setattr__(request, "dry_run", False)
    object.__setattr__(request, "azure_organization", None)
    object.__setattr__(request, "azure_project", None)
    return request


class TestHelper:
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_rejects_invalid_github_repository(self, mock_get_requests: MagicMock) -> None:
        result = _github_reply(_unsafe_request("repo"))
        assert result.mutation_status == "failed"
        mock_get_requests.assert_not_called()

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_fails_when_reply_response_id_is_zero(self, mock_get_requests: MagicMock) -> None:
        """A zero reply ID is treated as malformed and triggers reconciliation/failure."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        response = MagicMock(status_code=201)
        response.json.return_value = {"id": 0, "body": "reply"}
        mock_requests.post.return_value = response
        mock_requests.get.return_value = MagicMock(status_code=500)

        result = _github_reply(_unsafe_request("owner/repo"))

        assert result.mutation_status == "failed"

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_fails_when_reply_response_id_is_string(self, mock_get_requests: MagicMock) -> None:
        """A string reply ID is treated as malformed and triggers reconciliation/failure."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        response = MagicMock(status_code=201)
        response.json.return_value = {"id": "abc", "body": "reply"}
        mock_requests.post.return_value = response
        mock_requests.get.return_value = MagicMock(status_code=500)

        result = _github_reply(_unsafe_request("owner/repo"))

        assert result.mutation_status == "failed"

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_fails_when_reply_response_id_is_negative(self, mock_get_requests: MagicMock) -> None:
        """A negative reply ID is treated as malformed and triggers reconciliation/failure."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        response = MagicMock(status_code=201)
        response.json.return_value = {"id": -1, "body": "reply"}
        mock_requests.post.return_value = response
        mock_requests.get.return_value = MagicMock(status_code=500)

        result = _github_reply(_unsafe_request("owner/repo"))

        assert result.mutation_status == "failed"

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_fails_when_reply_response_id_is_bool(self, mock_get_requests: MagicMock) -> None:
        """A boolean True reply ID must be excluded even though bool is a subclass of int in Python."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        response = MagicMock(status_code=201)
        response.json.return_value = {"id": True, "body": "reply"}
        mock_requests.post.return_value = response
        mock_requests.get.return_value = MagicMock(status_code=500)

        result = _github_reply(_unsafe_request("owner/repo"))

        assert result.mutation_status == "failed"

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_skips_reconciliation_when_baseline_fetch_raises_on_5xx(self, mock_get_requests: MagicMock) -> None:
        """Reconciliation must not run when the pre-POST baseline fetch itself raised; a concurrent
        reply with the same body could otherwise be falsely claimed."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        post_response = MagicMock(status_code=503)
        post_response.headers = {}
        mock_requests.get.side_effect = RuntimeError("baseline unreachable")
        mock_requests.post.return_value = post_response

        result = _github_reply(_unsafe_request("owner/repo"))

        assert result.mutation_status == "failed"
        mock_requests.get.assert_called_once()

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_skips_reconciliation_when_baseline_fetch_raises_on_exception(self, mock_get_requests: MagicMock) -> None:
        """Reconciliation must not run when the pre-POST baseline fetch raised and the POST itself
        also raised; without a trustworthy baseline any historical match would be a false positive."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        mock_requests.get.side_effect = RuntimeError("baseline unreachable")
        mock_requests.post.side_effect = RuntimeError("post failed")

        result = _github_reply(_unsafe_request("owner/repo"))

        assert result.mutation_status == "failed"
        mock_requests.get.assert_called_once()

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_skips_reconciliation_when_baseline_fetch_returns_http_failure(self, mock_get_requests: MagicMock) -> None:
        """A non-2xx baseline response must not mark the baseline as trustworthy."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        mock_requests.get.return_value = MagicMock(status_code=503)
        mock_requests.post.return_value = MagicMock(status_code=503, headers={})

        result = _github_reply(_unsafe_request("owner/repo"))

        assert result.mutation_status == "failed"
        mock_requests.get.assert_called_once()

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_skips_reconciliation_when_baseline_fetch_returns_malformed_payload(
        self, mock_get_requests: MagicMock
    ) -> None:
        """A malformed baseline payload must not mark the baseline as trustworthy."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        baseline = MagicMock(status_code=200)
        baseline.json.return_value = {"not": "a list"}
        mock_requests.get.return_value = baseline
        mock_requests.post.return_value = MagicMock(status_code=503, headers={})

        result = _github_reply(_unsafe_request("owner/repo"))

        assert result.mutation_status == "failed"
        mock_requests.get.assert_called_once()

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_returns_failed_when_reconcile_raises_after_5xx_despite_valid_baseline(
        self, mock_get_requests: MagicMock
    ) -> None:
        """Even with a valid baseline, if the reconcile call itself raises on 5xx, return failed."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        baseline = MagicMock(status_code=200)
        baseline.json.return_value = []
        post_response = MagicMock(status_code=503)
        post_response.headers = {}
        mock_requests.get.side_effect = [baseline, RuntimeError("reconcile failed")]
        mock_requests.post.return_value = post_response

        result = _github_reply(_unsafe_request("owner/repo"))

        assert result.mutation_status == "failed"

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_returns_failed_when_reconcile_raises_after_post_exception_despite_valid_baseline(
        self, mock_get_requests: MagicMock
    ) -> None:
        """Even with a valid baseline, if the reconcile call raises when the POST itself raised, return failed."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        baseline = MagicMock(status_code=200)
        baseline.json.return_value = []
        mock_requests.get.side_effect = [baseline, RuntimeError("reconcile failed")]
        mock_requests.post.side_effect = RuntimeError("post failed")

        result = _github_reply(_unsafe_request("owner/repo"))

        assert result.mutation_status == "failed"

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_fails_before_reply_when_graphql_preflight_request_raises(self, mock_get_requests: MagicMock) -> None:
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        baseline = MagicMock(status_code=200)
        baseline.json.return_value = []
        mock_requests.get.return_value = baseline
        mock_requests.post.side_effect = [RuntimeError("graphql timeout")]

        result = _github_reply(_unsafe_request("owner/repo", resolve=True, review_thread_id="PRRT_123"))

        assert result.mutation_status == "failed"
        assert result.diagnostics
        assert "graphql timeout" in result.diagnostics[0]

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_fails_before_reply_when_graphql_preflight_json_decode_fails(self, mock_get_requests: MagicMock) -> None:
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        baseline = MagicMock(status_code=200)
        baseline.json.return_value = []
        preflight_response = MagicMock(status_code=200)
        preflight_response.json.side_effect = ValueError("bad json")
        mock_requests.get.return_value = baseline
        mock_requests.post.side_effect = [preflight_response]

        result = _github_reply(_unsafe_request("owner/repo", resolve=True, review_thread_id="PRRT_123"))

        assert result.mutation_status == "failed"
        assert result.diagnostics
        assert "bad json" in result.diagnostics[0]

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_accepts_repository_casing_from_github_preflight(self, mock_get_requests: MagicMock) -> None:
        """GitHub repository identity matching is case-insensitive."""
        mock_requests = MagicMock()
        mock_get_requests.return_value = mock_requests
        baseline = MagicMock(status_code=200)
        baseline.json.return_value = []
        preflight = MagicMock(status_code=200)
        preflight.json.return_value = {
            "data": {
                "node": {
                    "__typename": "PullRequestReviewThread",
                    "pullRequest": {
                        "number": 12,
                        "repository": {"nameWithOwner": "OWNER/REPO"},
                    },
                    "comments": {
                        "nodes": [{"databaseId": 34}],
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                    },
                }
            }
        }
        reply = MagicMock(status_code=201)
        reply.json.return_value = {"id": 56}
        resolution = MagicMock(status_code=200)
        resolution.json.return_value = {"data": {"resolveReviewThread": {"thread": {"isResolved": True}}}}
        mock_requests.get.return_value = baseline
        mock_requests.post.side_effect = [preflight, reply, resolution]

        result = _github_reply(_unsafe_request("owner/repo", resolve=True, review_thread_id="PRRT_123"))

        assert result.mutation_status == "replied_and_resolved"
