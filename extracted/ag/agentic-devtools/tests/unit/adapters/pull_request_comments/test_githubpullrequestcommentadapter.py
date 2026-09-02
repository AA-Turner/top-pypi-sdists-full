"""Tests for provider-neutral pull-request comment contracts."""

from __future__ import annotations

import json
from typing import cast
from unittest.mock import MagicMock

import pytest
import requests

from agentic_devtools.adapters.pull_request_comments import (
    GitHubPullRequestCommentAdapter,
    PullRequestCommentRequest,
)


def _response(status_code: int, payload: object, headers: dict[str, str] | None = None) -> MagicMock:
    response = MagicMock()
    response.status_code = status_code
    response.text = json.dumps(payload)
    response.json.return_value = payload
    response.headers = headers or {}
    return response


class TestGitHubPullRequestCommentAdapter:
    """Verify the GitHub issue-comment transport."""

    def test_posts_to_pull_request_issue_comments_with_token(self, monkeypatch: pytest.MonkeyPatch) -> None:
        responses = [
            _response(200, {"number": 42}),
            _response(200, []),
            _response(201, {"id": 9001, "html_url": "https://github.com/owner/repo/issues/9001"}),
        ]
        request = PullRequestCommentRequest(
            provider="github",
            repository="owner/repo",
            pull_request_id=42,
            content="line one\nline two",
        )
        calls: list[tuple[str, str, dict[str, object]]] = []

        def fake_request(method: str, url: str, **kwargs: object) -> MagicMock:
            calls.append((method, url, kwargs))
            return responses.pop(0)

        monkeypatch.setenv("SPECKIT_PR_TOKEN", "secret-token")
        adapter = GitHubPullRequestCommentAdapter(request_fn=fake_request)

        result = adapter.add_comment(request)

        assert result.success is True
        assert result.comment_id == "9001"
        assert calls[-1][0:2] == (
            "POST",
            "https://api.github.com/repos/owner/repo/issues/42/comments",
        )
        assert calls[-1][2]["json"] == {"body": "line one\nline two"}
        headers = cast(dict[str, str], calls[-1][2]["headers"])
        assert headers["Authorization"] == "Bearer " + "secret-" + "token"

    def test_rejects_github_anchoring_before_post(self) -> None:
        request = PullRequestCommentRequest(
            provider="github",
            repository="owner/repo",
            pull_request_id=42,
            content="inline",
            path="src/app.py",
            line=10,
        )
        adapter = GitHubPullRequestCommentAdapter(token="token")

        result = adapter.add_comment(request)

        assert result.success is False
        assert "anchoring" in result.error.lower()

    def test_dry_run_has_no_external_requests(self) -> None:
        request_fn = MagicMock()
        adapter = GitHubPullRequestCommentAdapter(token="", request_fn=request_fn)
        result = adapter.add_comment(PullRequestCommentRequest("github", "owner/repo", 42, "comment", dry_run=True))
        assert result.status == "dry_run"
        request_fn.assert_not_called()

    def test_missing_token_and_readiness_failure(self) -> None:
        request = PullRequestCommentRequest("github", "owner/repo", 42, "comment")
        assert GitHubPullRequestCommentAdapter(token="").readiness(request).success is False
        adapter = GitHubPullRequestCommentAdapter(token="token", request_fn=MagicMock())
        mismatch = PullRequestCommentRequest("azure_devops", "repo", 42, "comment")
        assert adapter.readiness(mismatch).success is False
        object.__setattr__(request, "repository", "invalid")
        assert adapter.readiness(request).success is False
        request = PullRequestCommentRequest("github", "owner/repo", 42, "comment")
        assert GitHubPullRequestCommentAdapter(token="", request_fn=MagicMock()).add_comment(request).success is False

    @pytest.mark.parametrize(
        ("responses", "expected"),
        [
            ([_response(404, {"message": "no"})], "readiness"),
            ([_response(200, {}), _response(403, {"message": "no"})], "readability"),
        ],
    )
    def test_readiness_failures(self, responses: list[MagicMock], expected: str) -> None:
        def fake_request(method: str, url: str, **kwargs: object) -> MagicMock:
            return responses.pop(0)

        adapter = GitHubPullRequestCommentAdapter(token="token", request_fn=fake_request)
        result = adapter.readiness(PullRequestCommentRequest("github", "owner/repo", 42, "comment"))
        assert result.success is False
        assert expected in result.error

    def test_readiness_exception_is_sanitized(self) -> None:
        adapter = GitHubPullRequestCommentAdapter(
            token="token", request_fn=MagicMock(side_effect=RuntimeError("token leaked"))
        )
        result = adapter.readiness(PullRequestCommentRequest("github", "owner/repo", 42, "comment"))
        assert result.success is False
        assert "token" not in result.error

    def test_readiness_rejects_read_only_classic_token(self) -> None:
        read_only_response = _response(200, {}, headers={"X-OAuth-Scopes": "read:org, read:user"})

        def fake_request(method: str, url: str, **kwargs: object) -> MagicMock:
            return read_only_response

        adapter = GitHubPullRequestCommentAdapter(token="token", request_fn=fake_request)
        result = adapter.readiness(PullRequestCommentRequest("github", "owner/repo", 42, "comment"))
        assert result.success is False
        assert "scope" in result.error

    def test_readiness_accepts_write_scope_classic_token(self) -> None:
        responses = [
            _response(200, {}, headers={"X-OAuth-Scopes": "repo"}),
            _response(200, []),
        ]

        def fake_request(method: str, url: str, **kwargs: object) -> MagicMock:
            return responses.pop(0)

        adapter = GitHubPullRequestCommentAdapter(token="token", request_fn=fake_request)
        result = adapter.readiness(PullRequestCommentRequest("github", "owner/repo", 42, "comment"))
        assert result.success is True

    def test_readiness_skips_scope_check_for_fine_grained_pat(self) -> None:
        responses = [
            _response(200, {}, headers={}),
            _response(200, []),
        ]

        def fake_request(method: str, url: str, **kwargs: object) -> MagicMock:
            return responses.pop(0)

        adapter = GitHubPullRequestCommentAdapter(token="token", request_fn=fake_request)
        result = adapter.readiness(PullRequestCommentRequest("github", "owner/repo", 42, "comment"))
        assert result.success is True

    def test_idempotency_reuses_existing_comment(self) -> None:
        request_fn = MagicMock(return_value=_response(200, [{"id": 7, "body": "x marker", "html_url": "url"}]))
        adapter = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn)
        request = PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        request_fn.side_effect = [
            _response(200, {}),
            _response(200, []),
            _response(200, [{"id": 7, "body": "marker", "html_url": "url"}]),
        ]
        result = adapter.add_comment(request)
        assert result.status == "already_exists"
        assert result.comment_id == "7"

    def test_idempotency_check_failure_does_not_post(self) -> None:
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(500, {"message": "ambiguous"}),
                _response(500, {"message": "ambiguous"}),
                _response(500, {"message": "ambiguous"}),
            ]
        )
        adapter = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn)
        result = adapter.add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.success is False
        assert request_fn.call_count == 5

    def test_idempotency_lookup_failure_does_not_post(self) -> None:
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(404, {}),
                _response(201, {"id": 8}),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.success is False
        assert result.status == "failed"
        assert request_fn.call_count == 3

    def test_idempotency_ignores_nonmatching_comments(self) -> None:
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, [{"body": "different"}, "not-a-dict"]),
                _response(201, {"id": 8}),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.comment_id == "8"

    def test_idempotency_ignores_non_string_marker_body(self) -> None:
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, [{"id": 7, "body": {"text": "marker"}}]),
                _response(201, {"id": 8}),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.status == "created"
        assert result.comment_id == "8"

    def test_idempotency_ignores_marker_matches_without_valid_comment_id(self) -> None:
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(
                    200,
                    [
                        {"id": True, "body": "marker", "html_url": "url"},
                        {"id": {"nested": "id"}, "body": "marker", "html_url": "url"},
                    ],
                ),
                _response(201, {"id": 8}),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.status == "created"
        assert result.comment_id == "8"

    def test_idempotency_trims_string_comment_id(self) -> None:
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, [{"id": " 9 ", "body": "marker", "html_url": "url"}]),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.status == "already_exists"
        assert result.comment_id == "9"

    def test_idempotency_ignores_blank_string_comment_id(self) -> None:
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, [{"id": "   ", "body": "marker", "html_url": "url"}]),
                _response(201, {"id": 8}),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.status == "created"
        assert result.comment_id == "8"

    def test_idempotency_non_list_payload_raises(self) -> None:
        """A 200 response whose JSON is not a list raises RuntimeError (fail-closed)."""
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, {"message": "unexpected dict"}),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.success is False
        assert "expected a list of comments" in (result.error or "")

    def test_post_failure_and_malformed_response(self) -> None:
        for response in (_response(500, {"message": "failed"}), _response(201, {"body": "no id"})):
            post_responses = [response] * 3 if response.status_code == 500 else [response]
            request_fn = MagicMock(side_effect=[_response(200, {}), _response(200, []), *post_responses])
            result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
                PullRequestCommentRequest("github", "owner/repo", 42, "comment")
            )
            assert result.success is False

    def test_post_response_rejects_boolean_comment_id(self) -> None:
        request_fn = MagicMock(side_effect=[_response(200, {}), _response(200, []), _response(201, {"id": True})])
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment")
        )
        assert result.success is False
        assert result.error == "GitHub response did not contain a comment ID"

    def test_post_response_uses_empty_url_sentinel_for_non_string_html_url(self) -> None:
        request_fn = MagicMock(
            side_effect=[_response(200, {}), _response(200, []), _response(201, {"id": 8, "html_url": {"k": "v"}})]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment")
        )
        assert result.success is True
        assert result.comment_id == "8"
        assert result.url == ""

    def test_request_exception_is_sanitized(self) -> None:
        request_fn = MagicMock(side_effect=[_response(200, {}), _response(200, []), RuntimeError("token leaked")])
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment")
        )
        assert result.success is False
        assert "token" not in result.error

    def test_retries_transport_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        request_fn = MagicMock(side_effect=[requests.Timeout("temporary"), _response(200, {})])
        monkeypatch.setattr("agentic_devtools.adapters.pull_request_comments.time.sleep", lambda _: None)
        response = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn)._request_with_retry(
            "GET", "url"
        )
        assert response.status_code == 200
        assert request_fn.call_count == 2

    def test_transport_failure_after_retries_is_raised(self, monkeypatch: pytest.MonkeyPatch) -> None:
        request_fn = MagicMock(side_effect=requests.Timeout("temporary"))
        monkeypatch.setattr("agentic_devtools.adapters.pull_request_comments.time.sleep", lambda _: None)
        with pytest.raises(requests.Timeout):
            GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn)._request_with_retry("GET", "url")

    def test_marker_reconciles_after_transport_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("agentic_devtools.adapters.pull_request_comments.time.sleep", lambda _: None)
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, []),
                requests.Timeout("temporary"),
                _response(200, []),
                _response(201, {"id": 8}),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.comment_id == "8"

    def test_marker_reconciles_after_transient_response(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("agentic_devtools.adapters.pull_request_comments.time.sleep", lambda _: None)
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, []),
                _response(500, {}),
                _response(200, []),
                _response(201, {"id": 8}),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.comment_id == "8"

    def test_marker_does_not_retry_ordinary_forbidden_response(self) -> None:
        request_fn = MagicMock(
            side_effect=[_response(200, {}), _response(200, []), _response(200, []), _response(403, {})]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.success is False
        assert request_fn.call_count == 4

    def test_empty_marker_uses_single_post_without_retry(self) -> None:
        request_fn = MagicMock(side_effect=[_response(200, {}), _response(200, []), _response(201, {"id": 8})])
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="")
        )
        assert result.comment_id == "8"
        post_calls = [c for c in request_fn.call_args_list if c.args and c.args[0] == "POST"]
        assert len(post_calls) == 1

    def test_marker_stops_after_three_ambiguous_transport_failures(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr("agentic_devtools.adapters.pull_request_comments.time.sleep", lambda _: None)
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, []),
                requests.Timeout("temporary"),
                _response(200, []),
                requests.Timeout("temporary"),
                _response(200, []),
                requests.Timeout("temporary"),
                _response(200, []),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.success is False

    def test_marker_returns_reconciled_comment_after_transport_failure(self) -> None:
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, []),
                requests.Timeout("temporary"),
                _response(200, [{"id": 9, "body": "marker"}]),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.status == "already_exists"

    def test_marker_returns_reconciled_comment_after_transient_response(self) -> None:
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, []),
                _response(500, {}),
                _response(200, [{"id": 9, "body": "marker"}]),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.status == "already_exists"

    def test_invalid_retry_after_uses_backoff(self, monkeypatch: pytest.MonkeyPatch) -> None:
        first = _response(500, {"message": "retry"})
        first.headers = {"Retry-After": "invalid"}
        request_fn = MagicMock(side_effect=[first, _response(200, {})])
        sleeps: list[float] = []
        monkeypatch.setattr("agentic_devtools.adapters.pull_request_comments.time.sleep", sleeps.append)
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn)._request_with_retry("GET", "url")
        assert result.status_code == 200
        assert sleeps == [1]

    def test_idempotency_follows_next_page(self) -> None:
        first = _response(200, [{"body": "different"}])
        first.links = {"next": {"url": "https://api.github.com/page-2"}}
        first.headers = {"Link": '<https://api.github.com/page-2>; rel="next"'}
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                first,
                _response(200, [{"id": 9, "body": "marker", "html_url": "url"}]),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.status == "already_exists"
        assert result.comment_id == "9"

    def test_idempotency_rejects_untrusted_next_page_host(self) -> None:
        first = _response(200, [{"body": "different"}])
        first.links = {"next": {"url": "https://evil.example/page-2"}}
        request_fn = MagicMock(side_effect=[_response(200, {}), _response(200, []), first])
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.success is False
        assert "unexpected pagination host" in result.error

    def test_idempotency_rejects_untrusted_next_page_host_from_link_header(self) -> None:
        first = _response(200, [{"body": "different"}])
        first.links = {}
        first.headers = {"Link": '<https://evil.example/page-2>; rel="next"'}
        request_fn = MagicMock(side_effect=[_response(200, {}), _response(200, []), first])
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.success is False
        assert "unexpected pagination host" in result.error

    def test_marker_reconciles_after_third_transport_failure(self) -> None:
        """Marker lookup on the 3rd transport exception finds a comment created by the lost POST."""
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, []),
                requests.Timeout("temporary"),
                _response(200, []),
                requests.Timeout("temporary"),
                _response(200, []),
                requests.Timeout("temporary"),
                _response(200, [{"id": 9, "body": "marker", "html_url": "url"}]),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.status == "already_exists"
        assert result.comment_id == "9"

    def test_marker_stops_after_three_retryable_responses(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Three retryable HTTP responses with no marker match → failure."""
        monkeypatch.setattr("agentic_devtools.adapters.pull_request_comments.time.sleep", lambda _: None)
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, []),
                _response(500, {}),
                _response(200, []),
                _response(500, {}),
                _response(200, []),
                _response(500, {}),
                _response(200, []),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.success is False

    def test_marker_reconciles_after_third_retryable_response(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Marker lookup on the 3rd retryable HTTP response finds a comment created by the ambiguous POST."""
        monkeypatch.setattr("agentic_devtools.adapters.pull_request_comments.time.sleep", lambda _: None)
        request_fn = MagicMock(
            side_effect=[
                _response(200, {}),
                _response(200, []),
                _response(200, []),
                _response(500, {}),
                _response(200, []),
                _response(500, {}),
                _response(200, []),
                _response(500, {}),
                _response(200, [{"id": 9, "body": "marker", "html_url": "url"}]),
            ]
        )
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment", idempotency_marker="marker")
        )
        assert result.status == "already_exists"
        assert result.comment_id == "9"

    def test_post_response_rejects_zero_comment_id(self) -> None:
        request_fn = MagicMock(side_effect=[_response(200, {}), _response(200, []), _response(201, {"id": 0})])
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment")
        )
        assert result.success is False
        assert result.error == "GitHub response did not contain a comment ID"

    def test_post_response_rejects_empty_string_comment_id(self) -> None:
        request_fn = MagicMock(side_effect=[_response(200, {}), _response(200, []), _response(201, {"id": ""})])
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment")
        )
        assert result.success is False
        assert result.error == "GitHub response did not contain a comment ID"

    def test_post_response_rejects_whitespace_comment_id(self) -> None:
        request_fn = MagicMock(side_effect=[_response(200, {}), _response(200, []), _response(201, {"id": "  "})])
        result = GitHubPullRequestCommentAdapter(token="token", request_fn=request_fn).add_comment(
            PullRequestCommentRequest("github", "owner/repo", 42, "comment")
        )
        assert result.success is False
        assert result.error == "GitHub response did not contain a comment ID"
