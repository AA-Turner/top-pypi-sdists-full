"""Tests for find_suppressed_deferral_issue_number in the deferral module."""

from __future__ import annotations

import json

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.deferral import (
    SUPPRESSED_DEFERRAL_SENTINEL,
    find_suppressed_deferral_issue_number,
)


def _marker_comment(
    comment_id: int,
    payload: dict[str, object],
    *,
    author: str = "copilot",
) -> IssueCommentInfo:
    return IssueCommentInfo(
        id=comment_id,
        author=author,
        body=f"{SUPPRESSED_DEFERRAL_SENTINEL}{json.dumps(payload)} -->",
    )


def _active_payload(review_id: int = 100, issue: int = 4242) -> dict[str, object]:
    return {"review_id": str(review_id), "issue": issue, "active": True}


class TestFindSuppressedDeferralIssueNumber:
    """Tests for find_suppressed_deferral_issue_number."""

    def test_returns_issue_number_of_active_marker(self) -> None:
        comments = [_marker_comment(7, _active_payload(issue=4242))]
        assert find_suppressed_deferral_issue_number(comments) == 4242

    def test_returns_newest_marker_issue_number(self) -> None:
        comments = [
            _marker_comment(7, _active_payload(issue=100)),
            _marker_comment(8, _active_payload(issue=200)),
        ]
        assert find_suppressed_deferral_issue_number(comments) == 200

    def test_ignores_inactive_marker(self) -> None:
        payload = _active_payload()
        payload["active"] = False
        assert find_suppressed_deferral_issue_number([_marker_comment(7, payload)]) is None

    def test_ignores_untrusted_author(self) -> None:
        comments = [_marker_comment(7, _active_payload(), author="random-user")]
        assert find_suppressed_deferral_issue_number(comments) is None

    def test_trusts_author_in_extra_allowed_authors(self) -> None:
        """extra_allowed_authors allows the workflow identity (e.g. SPECKIT_PR_TOKEN login)."""
        comments = [_marker_comment(7, _active_payload(issue=9999), author="amarsnik_swica")]
        assert find_suppressed_deferral_issue_number(comments) is None  # not trusted by default
        assert (
            find_suppressed_deferral_issue_number(comments, extra_allowed_authors=frozenset({"amarsnik_swica"})) == 9999
        )

    def test_extra_allowed_authors_none_uses_static_set(self) -> None:
        """Passing None for extra_allowed_authors falls back to the static set."""
        comments = [_marker_comment(7, _active_payload(issue=1234), author="copilot")]
        assert find_suppressed_deferral_issue_number(comments, extra_allowed_authors=None) == 1234

    def test_ignores_marker_with_non_numeric_issue(self) -> None:
        comments = [_marker_comment(7, {"review_id": "100", "issue": "not-a-number", "active": True})]
        assert find_suppressed_deferral_issue_number(comments) is None

    def test_ignores_marker_with_zero_issue(self) -> None:
        comments = [_marker_comment(7, {"review_id": "100", "issue": 0, "active": True})]
        assert find_suppressed_deferral_issue_number(comments) is None

    def test_returns_none_for_empty_comment_list(self) -> None:
        assert find_suppressed_deferral_issue_number([]) is None
