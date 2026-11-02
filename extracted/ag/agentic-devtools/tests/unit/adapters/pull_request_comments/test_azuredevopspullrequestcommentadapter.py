"""Tests for provider-neutral pull-request comment contracts."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from agentic_devtools.adapters.pull_request_comments import (
    AzureDevOpsPullRequestCommentAdapter,
    PullRequestCommentRequest,
)
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig


def _response(status_code: int, payload: object) -> MagicMock:
    response = MagicMock()
    response.status_code = status_code
    response.text = json.dumps(payload)
    response.json.return_value = payload
    return response


def _ready(*_: object) -> MagicMock:
    return _response(200, {"id": "repo-id"})


class TestAzureDevOpsPullRequestCommentAdapter:
    def _request(self, **kwargs: object) -> PullRequestCommentRequest:
        return PullRequestCommentRequest(
            provider="azure_devops",
            repository="repo",
            pull_request_id=42,
            content="comment",
            **kwargs,  # type: ignore[arg-type]
        )

    def test_readiness_rejects_mismatch_and_missing_values(self) -> None:
        config = AzureDevOpsConfig("org", "project", "repo")
        adapter = AzureDevOpsPullRequestCommentAdapter(config, "")
        mismatch = PullRequestCommentRequest("github", "owner/repo", 42, "comment")
        assert adapter.readiness(mismatch).success is False
        assert adapter.readiness(self._request()).success is False
        assert (
            AzureDevOpsPullRequestCommentAdapter(config, "pat", readiness_fn=_ready).readiness(self._request()).success
            is True
        )
        assert (
            AzureDevOpsPullRequestCommentAdapter(AzureDevOpsConfig("org", "project", ""), "pat")
            .readiness(self._request())
            .success
            is False
        )

    @patch("agentic_devtools.adapters.pull_request_comments.requests.get")
    def test_readiness_checks_repository_access(self, get: MagicMock) -> None:
        get.side_effect = [_response(200, {"id": "repo-id"}), _response(200, {"pullRequestId": 42})]
        result = AzureDevOpsPullRequestCommentAdapter(AzureDevOpsConfig("org", "project", "repo"), "pat").readiness(
            self._request()
        )
        assert result.success is True
        assert result.status == "ready_unverified"
        assert get.call_count == 2

    @patch("agentic_devtools.adapters.pull_request_comments.requests.get")
    def test_readiness_rejects_missing_pull_request(self, get: MagicMock) -> None:
        get.side_effect = [_response(200, {"id": "repo-id"}), _response(404, {"message": "Not found"})]
        result = AzureDevOpsPullRequestCommentAdapter(AzureDevOpsConfig("org", "project", "repo"), "pat").readiness(
            self._request()
        )
        assert result.success is False
        assert "pull-request readiness check failed (404)" in result.error

    def test_readiness_rejects_access_failure(self) -> None:
        result = AzureDevOpsPullRequestCommentAdapter(
            AzureDevOpsConfig("org", "project", "repo"), "pat", readiness_fn=lambda *_: _response(403, {})
        ).readiness(self._request())
        assert result.success is False

    def test_readiness_uses_backward_compatible_readiness_hook_signature(self) -> None:
        def readiness_fn(config: AzureDevOpsConfig, pat: str) -> MagicMock:
            assert config.repository == "repo"
            assert pat == "pat"
            return _response(200, {"id": "repo-id"})

        result = AzureDevOpsPullRequestCommentAdapter(
            AzureDevOpsConfig("org", "project", "repo"), "pat", readiness_fn=readiness_fn
        ).readiness(self._request())
        assert result.success is True

    def test_readiness_uses_pull_request_aware_readiness_hook_signature(self) -> None:
        calls: list[tuple[AzureDevOpsConfig, str, int]] = []

        def readiness_fn(config: AzureDevOpsConfig, pat: str, pull_request_id: int) -> MagicMock:
            calls.append((config, pat, pull_request_id))
            return _response(200, {"pullRequestId": pull_request_id})

        result = AzureDevOpsPullRequestCommentAdapter(
            AzureDevOpsConfig("org", "project", "repo"), "pat", readiness_fn=readiness_fn
        ).readiness(self._request())
        assert result.success is True
        assert calls == [(AzureDevOpsConfig("org", "project", "repo"), "pat", 42)]

    def test_readiness_handles_uninspectable_readiness_hook_signature(self) -> None:
        calls: list[tuple[AzureDevOpsConfig, str]] = []

        def readiness_fn(config: AzureDevOpsConfig, pat: str) -> MagicMock:
            calls.append((config, pat))
            return _response(200, {"id": "repo-id"})

        with patch("agentic_devtools.adapters.pull_request_comments.signature", side_effect=ValueError("invalid")):
            result = AzureDevOpsPullRequestCommentAdapter(
                AzureDevOpsConfig("org", "project", "repo"), "pat", readiness_fn=readiness_fn
            ).readiness(self._request())
        assert result.success is True
        assert len(calls) == 1

    def test_readiness_handles_access_exception(self) -> None:
        result = AzureDevOpsPullRequestCommentAdapter(
            AzureDevOpsConfig("org", "project", "repo"),
            "pat",
            readiness_fn=MagicMock(side_effect=RuntimeError("pat leaked")),
        ).readiness(self._request())
        assert result.success is False
        assert "pat" not in result.error

    def test_dry_run_does_not_require_credentials(self) -> None:
        adapter = AzureDevOpsPullRequestCommentAdapter(AzureDevOpsConfig("o", "p", "r"), "")
        result = adapter.add_comment(self._request(dry_run=True))
        assert result.status == "dry_run"

    def test_add_comment_rejects_readiness_failure(self) -> None:
        result = AzureDevOpsPullRequestCommentAdapter(AzureDevOpsConfig("o", "p", "r"), "").add_comment(self._request())
        assert result.success is False

    def test_posts_and_preserves_ids(self) -> None:
        post = MagicMock(return_value={"comment_id": 4, "thread_id": 5})
        adapter = AzureDevOpsPullRequestCommentAdapter(AzureDevOpsConfig("o", "p", "r"), "pat", post, _ready)
        result = adapter.add_comment(self._request())
        assert result.success is True
        assert result.comment_id == "4"
        post.assert_called_once()

    def test_post_errors_are_sanitized(self) -> None:
        post = MagicMock(side_effect=RuntimeError("pat leaked"))
        adapter = AzureDevOpsPullRequestCommentAdapter(AzureDevOpsConfig("o", "p", "r"), "pat", post, _ready)
        result = adapter.add_comment(self._request())
        assert result.success is False
        assert "pat" not in result.error

    def test_uses_default_post_function(self) -> None:
        with patch(
            "agentic_devtools.tools.azure_devops.add_pull_request_comment",
            return_value={"comment_id": 1, "thread_id": 2},
        ) as post:
            result = AzureDevOpsPullRequestCommentAdapter(
                AzureDevOpsConfig("o", "p", "r"), "pat", readiness_fn=_ready
            ).add_comment(self._request())
        assert result.success is True
        post.assert_called_once()

    def test_post_rejects_missing_thread_id(self) -> None:
        post = MagicMock(return_value={"comment_id": 4})
        adapter = AzureDevOpsPullRequestCommentAdapter(AzureDevOpsConfig("o", "p", "r"), "pat", post, _ready)
        result = adapter.add_comment(self._request())
        assert result.success is False
        assert "thread ID" in (result.error or "")

    def test_post_rejects_zero_thread_id(self) -> None:
        post = MagicMock(return_value={"comment_id": 4, "thread_id": 0})
        adapter = AzureDevOpsPullRequestCommentAdapter(AzureDevOpsConfig("o", "p", "r"), "pat", post, _ready)
        result = adapter.add_comment(self._request())
        assert result.success is False
        assert "thread ID" in (result.error or "")

    def test_post_omits_zero_comment_id(self) -> None:
        post = MagicMock(return_value={"comment_id": 0, "thread_id": 5})
        adapter = AzureDevOpsPullRequestCommentAdapter(AzureDevOpsConfig("o", "p", "r"), "pat", post, _ready)
        result = adapter.add_comment(self._request())
        assert result.success is True
        assert result.comment_id == ""
        assert result.thread_id == "5"
