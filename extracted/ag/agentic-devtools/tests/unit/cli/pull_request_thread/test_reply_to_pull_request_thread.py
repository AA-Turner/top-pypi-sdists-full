"""Tests for provider-neutral pull-request thread reply operations."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.adapters.base import PullRequestThreadReplyRequest
from agentic_devtools.cli.pull_request_thread import (
    reply_to_pull_request_thread,
)


class TestReplyToPullRequestThread:
    """Test provider dispatch and public reply behavior."""

    @staticmethod
    def _preflight_payload(
        *,
        discussion_ids: list[int] | None = None,
        has_next_page: bool = False,
        end_cursor: str | None = None,
        repository: str = "owner/repo",
        pull_request_number: int = 12,
    ) -> dict[str, object]:
        return {
            "data": {
                "node": {
                    "__typename": "PullRequestReviewThread",
                    "pullRequest": {"number": pull_request_number, "repository": {"nameWithOwner": repository}},
                    "comments": {
                        "nodes": [{"databaseId": value} for value in (discussion_ids or [])],
                        "pageInfo": {"hasNextPage": has_next_page, "endCursor": end_cursor},
                    },
                }
            }
        }

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    @patch("agentic_devtools.cli.azure_devops.helpers.get_repository_id", return_value="repo-id")
    @patch("agentic_devtools.cli.azure_devops.auth.get_auth_headers", return_value={})
    @patch("agentic_devtools.cli.azure_devops.helpers.resolve_thread_by_id")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig")
    @patch("agentic_devtools.tools.azure_devops.reply_to_pull_request_thread")
    def test_azure_devops_dispatch_preserves_compatibility_result(
        self,
        mock_reply: MagicMock,
        mock_config: MagicMock,
        mock_pat: MagicMock,
        mock_resolve: MagicMock,
        _mock_headers: MagicMock,
        _mock_repo_id: MagicMock,
        _mock_requests: MagicMock,
    ) -> None:
        mock_pat.return_value = "pat"
        mock_config.from_state.return_value = MagicMock()
        mock_reply.return_value = {"comment_id": 78}

        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest(
                provider="azure_devops",
                repository="project/repo",
                pull_request_number=12,
                discussion_id=34,
                body="fixed",
                resolve=True,
                azure_organization="org",
                azure_project="project",
            )
        )

        assert result.reply_id == 78
        assert result.resolution_status == "resolved"
        mock_reply.assert_called_once()
        assert mock_reply.call_args.kwargs["thread_id"] == 34
        # Reply is now posted without resolution; resolution is a separate call.
        assert mock_reply.call_args.kwargs["resolve_thread"] is False
        mock_resolve.assert_called_once()

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_dry_run_does_not_require_credentials_or_make_requests(self, mock_get_requests: MagicMock) -> None:
        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest(
                provider="github",
                repository="owner/repo",
                pull_request_number=12,
                discussion_id=34,
                body="preview",
                dry_run=True,
            )
        )

        assert result.mutation_status == "dry_run"
        assert result.reply_id is None
        mock_get_requests.assert_not_called()

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_dry_run_reports_unsupported_resolution_without_review_thread_id(
        self, mock_get_requests: MagicMock
    ) -> None:
        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest(
                provider="github",
                repository="owner/repo",
                pull_request_number=12,
                discussion_id=34,
                body="preview",
                resolve=True,
                dry_run=True,
            )
        )

        assert result.mutation_status == "dry_run"
        assert result.resolution_status == "unsupported"
        mock_get_requests.assert_not_called()

    @pytest.mark.parametrize("status", [401, 403, 404, 409, 422, 429, 500])
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_normalizes_github_reply_http_errors(self, mock_get_requests: MagicMock, status: int) -> None:
        requests = MagicMock()
        requests.post.return_value = MagicMock(status_code=status)
        mock_get_requests.return_value = requests
        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))
        assert result.mutation_status == "failed"
        assert str(status) in result.diagnostics[0]

    @pytest.mark.parametrize("payload", [{}, {"id": None}, []])
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_rejects_malformed_github_reply(self, mock_get_requests: MagicMock, payload: object) -> None:
        response = MagicMock(status_code=201)
        response.json.return_value = payload
        requests = MagicMock()
        requests.post.return_value = response
        mock_get_requests.return_value = requests
        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))
        assert result.mutation_status == "failed"

    @patch.dict("os.environ", {}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_reports_missing_github_credential(self, mock_get_requests: MagicMock) -> None:
        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))
        assert "GH_TOKEN" in result.diagnostics[0]
        mock_get_requests.assert_not_called()

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_reports_resolution_failure_without_retrying_reply(self, mock_get_requests: MagicMock) -> None:
        requests = MagicMock()
        resolution_response = MagicMock(status_code=200)
        resolution_response.json.return_value = {"errors": [{"message": "stale"}]}
        preflight_response = MagicMock(status_code=200)
        preflight_response.json.return_value = self._preflight_payload(discussion_ids=[34])
        reply_response = MagicMock(status_code=201)
        reply_response.json.return_value = {"id": 56}
        requests.post.side_effect = [preflight_response, reply_response, resolution_response]
        mock_get_requests.return_value = requests
        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply", True, "PRRT_kwDO")
        )
        assert result.resolution_status == "failed"
        assert requests.post.call_count == 3

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_successful_github_reply_without_resolution(self, mock_get_requests: MagicMock) -> None:
        response = MagicMock(status_code=201)
        response.json.return_value = {"id": 56}
        requests = MagicMock()
        requests.post.return_value = response
        mock_get_requests.return_value = requests
        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))
        assert result.mutation_status == "replied"

    @patch("agentic_devtools.cli.pull_request_thread.time.sleep")
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_retries_rate_limit_before_success(self, mock_get_requests: MagicMock, _mock_sleep: MagicMock) -> None:
        requests = MagicMock()
        limited = MagicMock(status_code=429, headers={"Retry-After": "invalid"})
        success = MagicMock(status_code=201)
        success.json.return_value = {"id": 56}
        requests.post.side_effect = [limited, success]
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))

        assert result.mutation_status == "replied"
        assert requests.post.call_count == 2

    @patch("agentic_devtools.cli.pull_request_thread.time.sleep")
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_retries_github_403_rate_limit_before_success(
        self, mock_get_requests: MagicMock, _mock_sleep: MagicMock
    ) -> None:
        requests = MagicMock()
        limited = MagicMock(status_code=403, headers={"Retry-After": "1", "X-RateLimit-Remaining": "0"})
        success = MagicMock(status_code=201)
        success.json.return_value = {"id": 56}
        requests.post.side_effect = [limited, success]
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))

        assert result.mutation_status == "replied"
        assert requests.post.call_count == 2

    @patch("agentic_devtools.cli.pull_request_thread.time.sleep")
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_reconciles_reply_after_transport_failure(
        self, mock_get_requests: MagicMock, _mock_sleep: MagicMock
    ) -> None:
        requests = MagicMock()
        requests.post.side_effect = OSError("timeout")
        baseline = MagicMock(status_code=200)
        baseline.json.return_value = [{"body": "reply", "id": 55, "in_reply_to_id": 34}]
        reconcile = MagicMock(status_code=200)
        reconcile.json.return_value = [
            {"body": "reply", "id": 55, "in_reply_to_id": 34},
            {"body": "reply", "id": 56, "in_reply_to_id": 34},
        ]
        requests.get.side_effect = [baseline, reconcile]
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))

        assert result.mutation_status == "replied"
        assert result.reply_id == 56

    @patch("agentic_devtools.cli.pull_request_thread.time.sleep")
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_does_not_reconcile_to_preexisting_matching_reply(
        self, mock_get_requests: MagicMock, _mock_sleep: MagicMock
    ) -> None:
        requests = MagicMock()
        requests.post.side_effect = OSError("timeout")
        baseline = MagicMock(status_code=200)
        baseline.json.return_value = [{"body": "reply", "id": 55, "in_reply_to_id": 34}]
        reconcile = MagicMock(status_code=200)
        reconcile.json.return_value = [{"body": "reply", "id": 55, "in_reply_to_id": 34}]
        requests.get.side_effect = [baseline, reconcile]
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))

        assert result.mutation_status == "failed"

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_reconciles_reply_after_github_5xx_response(self, mock_get_requests: MagicMock) -> None:
        requests = MagicMock()
        requests.post.return_value = MagicMock(status_code=503, headers={})
        baseline = MagicMock(status_code=200)
        baseline.json.return_value = [{"body": "reply", "id": 55, "in_reply_to_id": 34}]
        reconcile = MagicMock(status_code=200)
        reconcile.json.return_value = [
            {"body": "reply", "id": 55, "in_reply_to_id": 34},
            {"body": "reply", "id": 56, "in_reply_to_id": 34},
        ]
        requests.get.side_effect = [baseline, reconcile]
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))

        assert result.mutation_status == "replied"
        assert result.reply_id == 56

    @patch("agentic_devtools.cli.pull_request_thread.time.sleep")
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_stops_after_three_rate_limit_responses(self, mock_get_requests: MagicMock, _mock_sleep: MagicMock) -> None:
        requests = MagicMock()
        requests.post.return_value = MagicMock(status_code=429, headers={})
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))

        assert result.mutation_status == "failed"
        assert requests.post.call_count == 3

    @patch("agentic_devtools.cli.pull_request_thread.time.sleep")
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_reports_github_403_rate_limit_as_rate_limited(
        self, mock_get_requests: MagicMock, _mock_sleep: MagicMock
    ) -> None:
        requests = MagicMock()
        requests.post.return_value = MagicMock(
            status_code=403,
            headers={"Retry-After": "1", "X-RateLimit-Remaining": "0"},
        )
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply"))

        assert result.mutation_status == "failed"
        assert "HTTP 429" in result.diagnostics[0]

    @pytest.mark.parametrize(
        "resolution_payload",
        [
            {"data": {"resolveReviewThread": {"thread": {"isResolved": False}}}},
            {"data": {"resolveReviewThread": {"thread": {}}}},
        ],
    )
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_reports_unconfirmed_github_resolution(
        self, mock_get_requests: MagicMock, resolution_payload: dict[str, object]
    ) -> None:
        requests = MagicMock()
        preflight_response = MagicMock(status_code=200)
        preflight_response.json.return_value = self._preflight_payload(discussion_ids=[34])
        reply_response = MagicMock(status_code=201)
        reply_response.json.return_value = {"id": 56}
        resolution_response = MagicMock(status_code=200)
        resolution_response.json.return_value = resolution_payload
        requests.post.side_effect = [preflight_response, reply_response, resolution_response]
        mock_get_requests.return_value = requests
        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply", True, "PRRT_kwDO")
        )
        assert result.resolution_status == "failed"

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_normalizes_github_resolution_http_error(self, mock_get_requests: MagicMock) -> None:
        requests = MagicMock()
        preflight_response = MagicMock(status_code=200)
        preflight_response.json.return_value = self._preflight_payload(discussion_ids=[34])
        reply_response = MagicMock(status_code=201)
        reply_response.json.return_value = {"id": 56}
        requests.post.side_effect = [preflight_response, reply_response, MagicMock(status_code=409)]
        mock_get_requests.return_value = requests
        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply", True, "PRRT_kwDO")
        )
        assert result.resolution_status == "failed"

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_github_reply_uses_numeric_comment_and_graphql_thread(self, mock_get_requests: MagicMock) -> None:
        requests = MagicMock()
        preflight_response = MagicMock(status_code=200)
        preflight_response.json.return_value = self._preflight_payload(discussion_ids=[34])
        reply_response = MagicMock(status_code=201)
        reply_response.json.return_value = {"id": 56}
        resolve_response = MagicMock(status_code=200)
        resolve_response.json.return_value = {"data": {"resolveReviewThread": {"thread": {"isResolved": True}}}}
        requests.post.side_effect = [preflight_response, reply_response, resolve_response]
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest(
                provider="github",
                repository="owner/repo",
                pull_request_number=12,
                discussion_id=34,
                body="quote `x`\n✓",
                resolve=True,
                review_thread_id="PRRT_kwDO",
            )
        )

        assert result.reply_id == 56
        assert result.resolution_status == "resolved"
        assert requests.post.call_args_list[0].kwargs["json"]["variables"] == {"threadId": "PRRT_kwDO", "after": None}
        assert requests.post.call_args_list[1].args[0].endswith("/comments/34/replies")
        assert requests.post.call_args_list[1].kwargs["json"] == {"body": "quote `x`\n✓"}
        assert requests.post.call_args_list[2].kwargs["json"]["variables"] == {"threadId": "PRRT_kwDO"}

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_github_resolution_preflight_blocks_mismatched_thread(self, mock_get_requests: MagicMock) -> None:
        requests = MagicMock()
        preflight_response = MagicMock(status_code=200)
        preflight_response.json.return_value = self._preflight_payload(discussion_ids=[99])
        requests.post.side_effect = [preflight_response]
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply", True, "PRRT_kwDO")
        )

        assert result.mutation_status == "failed"
        assert result.resolution_status == "not_attempted"
        assert "does not contain discussion_id" in result.diagnostics[0]
        assert requests.post.call_count == 1

    @pytest.mark.parametrize(
        ("preflight_status", "preflight_payload", "diagnostic_fragment"),
        [
            (503, {"ignored": True}, "GitHub review-thread lookup returned HTTP 503"),
            (200, ["invalid"], "malformed payload"),
            (200, {"errors": [{"message": "x"}]}, "returned errors"),
            (200, {"data": None}, "payload missing data"),
            (200, {"data": {"node": {"__typename": "PullRequest"}}}, "not a pull-request review thread node"),
            (
                200,
                {"data": {"node": {"__typename": "PullRequestReviewThread", "pullRequest": None}}},
                "missing pull-request context",
            ),
            (
                200,
                {
                    "data": {
                        "node": {
                            "__typename": "PullRequestReviewThread",
                            "pullRequest": {"number": 12, "repository": {"nameWithOwner": "owner/other"}},
                            "comments": {
                                "nodes": [{"databaseId": 34}],
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                            },
                        }
                    }
                },
                "configured repository",
            ),
            (
                200,
                {
                    "data": {
                        "node": {
                            "__typename": "PullRequestReviewThread",
                            "pullRequest": {"number": 99, "repository": {"nameWithOwner": "owner/repo"}},
                            "comments": {
                                "nodes": [{"databaseId": 34}],
                                "pageInfo": {"hasNextPage": False, "endCursor": None},
                            },
                        }
                    }
                },
                "configured pull request",
            ),
            (
                200,
                {
                    "data": {
                        "node": {
                            "__typename": "PullRequestReviewThread",
                            "pullRequest": {"number": 12, "repository": {"nameWithOwner": "owner/repo"}},
                            "comments": None,
                        }
                    }
                },
                "missing review-thread comments",
            ),
            (
                200,
                {
                    "data": {
                        "node": {
                            "__typename": "PullRequestReviewThread",
                            "pullRequest": {"number": 12, "repository": {"nameWithOwner": "owner/repo"}},
                            "comments": {"nodes": None, "pageInfo": {"hasNextPage": False, "endCursor": None}},
                        }
                    }
                },
                "comments payload is malformed",
            ),
            (
                200,
                {
                    "data": {
                        "node": {
                            "__typename": "PullRequestReviewThread",
                            "pullRequest": {"number": 12, "repository": {"nameWithOwner": "owner/repo"}},
                            "comments": {"nodes": [], "pageInfo": None},
                        }
                    }
                },
                "page metadata is missing",
            ),
            (
                200,
                {
                    "data": {
                        "node": {
                            "__typename": "PullRequestReviewThread",
                            "pullRequest": {"number": 12, "repository": {"nameWithOwner": "owner/repo"}},
                            "comments": {"nodes": [], "pageInfo": {"hasNextPage": True, "endCursor": None}},
                        }
                    }
                },
                "pagination cursor was missing",
            ),
            (
                200,
                {
                    "data": {
                        "node": {
                            "__typename": "PullRequestReviewThread",
                            "pullRequest": {"number": 12, "repository": {"nameWithOwner": "owner/repo"}},
                            "comments": {"nodes": [], "pageInfo": {"hasNextPage": "bad", "endCursor": None}},
                        }
                    }
                },
                "page metadata is malformed",
            ),
        ],
    )
    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_github_resolution_preflight_failure_paths(
        self,
        mock_get_requests: MagicMock,
        preflight_status: int,
        preflight_payload: object,
        diagnostic_fragment: str,
    ) -> None:
        requests = MagicMock()
        preflight_response = MagicMock(status_code=preflight_status)
        preflight_response.json.return_value = preflight_payload
        requests.post.side_effect = [preflight_response]
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply", True, "PRRT_kwDO")
        )

        assert result.mutation_status == "failed"
        assert result.resolution_status == "not_attempted"
        assert diagnostic_fragment in result.diagnostics[0]
        assert requests.post.call_count == 1

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_github_resolution_preflight_paginates_until_discussion_match(self, mock_get_requests: MagicMock) -> None:
        requests = MagicMock()
        preflight_page_one = MagicMock(status_code=200)
        preflight_page_one.json.return_value = self._preflight_payload(
            discussion_ids=[], has_next_page=True, end_cursor="c1"
        )
        preflight_page_two = MagicMock(status_code=200)
        preflight_page_two.json.return_value = self._preflight_payload(discussion_ids=[34], has_next_page=False)
        reply_response = MagicMock(status_code=201)
        reply_response.json.return_value = {"id": 56}
        resolve_response = MagicMock(status_code=200)
        resolve_response.json.return_value = {"data": {"resolveReviewThread": {"thread": {"isResolved": True}}}}
        requests.post.side_effect = [preflight_page_one, preflight_page_two, reply_response, resolve_response]
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply", True, "PRRT_kwDO")
        )

        assert result.mutation_status == "replied_and_resolved"
        assert requests.post.call_args_list[0].kwargs["json"]["variables"] == {"threadId": "PRRT_kwDO", "after": None}
        assert requests.post.call_args_list[1].kwargs["json"]["variables"] == {"threadId": "PRRT_kwDO", "after": "c1"}

    @patch.dict("os.environ", {"GH_TOKEN": "token"}, clear=True)
    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_github_resolution_failure_when_graphql_returns_errors(self, mock_get_requests: MagicMock) -> None:
        requests = MagicMock()
        preflight_response = MagicMock(status_code=200)
        preflight_response.json.return_value = self._preflight_payload(discussion_ids=[34])
        reply_response = MagicMock(status_code=201)
        reply_response.json.return_value = {"id": 56}
        resolve_response = MagicMock(status_code=200)
        resolve_response.json.return_value = {"errors": [{"message": "failure"}]}
        requests.post.side_effect = [preflight_response, reply_response, resolve_response]
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply", True, "PRRT_kwDO")
        )

        assert result.mutation_status == "partial_success"
        assert result.resolution_status == "failed"
        assert "GraphQL review thread resolution returned errors" in result.diagnostics[0]

    @patch("agentic_devtools.cli.pull_request_thread._get_requests")
    def test_missing_github_thread_id_posts_reply_without_claiming_resolution(
        self, mock_get_requests: MagicMock, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("GITHUB_TOKEN", "token")
        requests = MagicMock()
        response = MagicMock(status_code=201)
        response.json.return_value = {"id": 56}
        requests.post.return_value = response
        mock_get_requests.return_value = requests

        result = reply_to_pull_request_thread(
            PullRequestThreadReplyRequest(
                provider="github",
                repository="owner/repo",
                pull_request_number=12,
                discussion_id=34,
                body="reply",
                resolve=True,
            )
        )

        assert result.reply_id == 56
        assert result.resolution_status == "unsupported"
        assert requests.post.call_count == 1

    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", side_effect=OSError("missing"))
    def test_normalizes_azure_failure(self, _mock_pat: MagicMock) -> None:
        result = reply_to_pull_request_thread(PullRequestThreadReplyRequest("azure_devops", "repo", 12, 34, "reply"))
        assert result.mutation_status == "failed"

    @patch("agentic_devtools.cli.pull_request_thread.build_reply_request")
    def test_builds_request_when_worker_receives_no_argument(self, mock_build: MagicMock) -> None:
        request = PullRequestThreadReplyRequest("github", "owner/repo", 12, 34, "reply", dry_run=True)
        mock_build.return_value = request
        assert reply_to_pull_request_thread().mutation_status == "dry_run"

    def test_accepts_serialized_request_mapping(self) -> None:
        result = reply_to_pull_request_thread(
            {
                "provider": "github",
                "repository": "owner/repo",
                "pull_request_number": 12,
                "discussion_id": 34,
                "body": "preview",
                "dry_run": True,
            }
        )
        assert result.mutation_status == "dry_run"
