"""Tests for post_suppressed_deferral_marker in the deferral module."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.deferral import (
    _DEFERRAL_SENTINEL,
    SUPPRESSED_DEFERRAL_SENTINEL,
    post_suppressed_deferral_marker,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def _marker_comment(
    comment_id: int,
    payload: dict[str, object],
    *,
    author: str = "copilot",
    sentinel: str = SUPPRESSED_DEFERRAL_SENTINEL,
) -> IssueCommentInfo:
    return IssueCommentInfo(
        id=comment_id,
        author=author,
        body=f"{sentinel}{json.dumps(payload)} -->",
    )


def _active_payload(review_id: int = 100, issue: int = 4242) -> dict[str, object]:
    return {"review_id": str(review_id), "issue": issue, "active": True}


class TestPostSuppressedDeferralMarker:
    """Tests for post_suppressed_deferral_marker."""

    def test_posts_marker_when_none_exists(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        assert post_suppressed_deferral_marker(provider, 1, 100, 4242) is True

        body = provider.post_comment.call_args[0][1]
        assert body.startswith(SUPPRESSED_DEFERRAL_SENTINEL)
        payload = json.loads(body.split(SUPPRESSED_DEFERRAL_SENTINEL, 1)[1].rsplit(" -->", 1)[0])
        assert payload["review_id"] == "100"
        assert payload["issue"] == 4242
        assert payload["active"] is True
        assert payload["posted_at"].endswith("Z")

    def test_ignores_autofix_marker_for_the_same_review(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            _marker_comment(7, {"review_id": "100", "active": True}, sentinel=_DEFERRAL_SENTINEL)
        ]

        assert post_suppressed_deferral_marker(provider, 1, 100, 4242) is True
        provider.post_comment.assert_called_once()

    def test_skips_when_marker_already_exists(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_marker_comment(7, _active_payload())]

        assert post_suppressed_deferral_marker(provider, 1, 100, 4242) is False
        provider.post_comment.assert_not_called()

    def test_returns_false_on_post_failure(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = []
        provider.post_comment.side_effect = RuntimeError("API error")

        assert post_suppressed_deferral_marker(provider, 1, 100, 4242) is False

    def test_reraises_rate_limit_when_listing_comments(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.side_effect = ProviderRateLimitError(60.0)

        import pytest

        with pytest.raises(ProviderRateLimitError):
            post_suppressed_deferral_marker(provider, 1, 100, 4242)

    def test_reraises_rate_limit_when_posting_marker(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = []
        provider.post_comment.side_effect = ProviderRateLimitError(60.0)

        import pytest

        with pytest.raises(ProviderRateLimitError):
            post_suppressed_deferral_marker(provider, 1, 100, 4242)
