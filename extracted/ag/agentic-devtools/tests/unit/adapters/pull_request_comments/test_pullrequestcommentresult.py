"""Tests for pull-request comment results."""

from __future__ import annotations

from agentic_devtools.adapters.pull_request_comments import PullRequestCommentResult


def test_as_dict() -> None:
    result = PullRequestCommentResult(True, "github", "created", comment_id="1")
    assert result.as_dict()["comment_id"] == "1"
