"""Tests for provider-neutral pull-request comment contracts."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.pull_request_comments import PullRequestCommentRequest


class TestPullRequestCommentRequest:
    """Validate request fields before provider dispatch."""

    def test_preserves_multiline_content(self) -> None:
        request = PullRequestCommentRequest(
            provider="github",
            repository="owner/repo",
            pull_request_id=42,
            content="first line\n\n✓ second line",
        )

        assert request.content == "first line\n\n✓ second line"

    @pytest.mark.parametrize(
        ("kwargs", "message"),
        [
            ({"provider": "unknown"}, "provider"),
            ({"repository": "repo"}, "repository"),
            ({"pull_request_id": 0}, "pull_request_id"),
            ({"content": ""}, "content"),
            ({"repository": "owner/repo/extra"}, "repository"),
            ({"pull_request_id": True}, "pull_request_id"),
            ({"content": 42}, "content"),
            ({"line": 0}, "line"),
            ({"line": True}, "line"),
            ({"line": "bad"}, "line"),
            ({"line": 3}, "path"),
            ({"end_line": 2}, "path"),
            ({"path": "src/app.py", "end_line": 2}, "end_line"),
            ({"end_line": 0}, "end_line"),
            ({"end_line": True}, "end_line"),
            ({"end_line": "bad"}, "end_line"),
            ({"path": "src/app.py", "line": 3, "end_line": 2}, "end_line"),
            ({"path": 42}, "path"),
            ({"resolve_after_posting": "false"}, "resolve_after_posting"),
            ({"dry_run": "false"}, "dry_run"),
            ({"idempotency_marker": 42}, "idempotency_marker"),
            ({"organization": ""}, "organization"),
            ({"organization": 42}, "organization"),
            ({"project": ""}, "project"),
            ({"project": 42}, "project"),
        ],
    )
    def test_rejects_invalid_values(self, kwargs: dict[str, object], message: str) -> None:
        values: dict[str, object] = {
            "provider": "github",
            "repository": "owner/repo",
            "pull_request_id": 42,
            "content": "comment",
        }
        values.update(kwargs)

        with pytest.raises(ValueError, match=message):
            PullRequestCommentRequest(**values)  # type: ignore[arg-type]

    def test_rejects_non_string_repository(self) -> None:
        with pytest.raises(ValueError, match="repository"):
            PullRequestCommentRequest(
                provider="github",
                repository=42,  # type: ignore[arg-type]
                pull_request_id=42,
                content="comment",
            )
