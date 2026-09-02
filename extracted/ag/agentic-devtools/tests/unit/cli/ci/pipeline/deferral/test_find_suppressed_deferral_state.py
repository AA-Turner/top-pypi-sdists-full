"""Tests for find_suppressed_deferral_state in the deferral module."""

from __future__ import annotations

import json

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.deferral import (
    SUPPRESSED_DEFERRAL_SENTINEL,
    find_suppressed_deferral_state,
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


class TestFindSuppressedDeferralState:
    """Tests for find_suppressed_deferral_state — atomic two-value read."""

    def test_returns_both_values_from_same_active_marker(self) -> None:
        comments = [_marker_comment(7, _active_payload(review_id=100, issue=4242))]
        assert find_suppressed_deferral_state(comments) == (100, 4242)

    def test_returns_none_none_when_no_active_marker(self) -> None:
        assert find_suppressed_deferral_state([]) == (None, None)

    def test_returns_from_newest_active_marker(self) -> None:
        """Both values come from the single newest active marker, not two different markers."""
        comments = [
            _marker_comment(7, _active_payload(review_id=100, issue=11)),
            _marker_comment(8, _active_payload(review_id=200, issue=22)),
        ]
        assert find_suppressed_deferral_state(comments) == (200, 22)

    def test_both_values_from_same_marker_prevents_aliasing(self) -> None:
        """A partial marker (valid review_id but issue=0) is skipped entirely.

        Previously two independent scans could pick review_id from marker B
        and issue_number from marker A (older fallback).  The atomic read
        requires both to be positive: a partial newest marker does not expose
        a stale gate-clearing review_id from a different marker.
        """
        no_issue_payload: dict[str, object] = {"review_id": "200", "active": True, "issue": 0}
        comments = [
            _marker_comment(7, _active_payload(review_id=100, issue=42)),  # older, has issue
            _marker_comment(8, no_issue_payload),  # newer, issue=0 → skipped
        ]
        # The newest marker is partial (no valid issue), so it is skipped.
        # The older marker is also skipped because we do not fall back to it —
        # the loop continues but the second oldest is the first candidate after
        # the partial newest is rejected.
        assert find_suppressed_deferral_state(comments) == (100, 42)

    def test_ignores_inactive_marker(self) -> None:
        payload = _active_payload()
        payload["active"] = False
        assert find_suppressed_deferral_state([_marker_comment(7, payload)]) == (None, None)

    def test_ignores_untrusted_author(self) -> None:
        comments = [_marker_comment(7, _active_payload(), author="random-user")]
        assert find_suppressed_deferral_state(comments) == (None, None)

    def test_trusts_extra_allowed_authors(self) -> None:
        comments = [_marker_comment(7, _active_payload(review_id=77, issue=99), author="amarsnik_swica")]
        assert find_suppressed_deferral_state(comments) == (None, None)  # not trusted by default
        assert find_suppressed_deferral_state(comments, extra_allowed_authors=frozenset({"amarsnik_swica"})) == (77, 99)

    def test_returns_none_none_for_marker_with_non_numeric_review_id(self) -> None:
        payload: dict[str, object] = {"review_id": "not-a-number", "issue": 99, "active": True}
        assert find_suppressed_deferral_state([_marker_comment(7, payload)]) == (None, None)

    def test_partial_marker_with_valid_review_id_but_no_issue_returns_none_none(self) -> None:
        """A marker carrying a valid review_id but a missing/zero issue is skipped (fail-closed)."""
        payload: dict[str, object] = {"review_id": "200", "active": True}
        assert find_suppressed_deferral_state([_marker_comment(7, payload)]) == (None, None)

    def test_partial_marker_with_valid_issue_but_no_review_id_returns_none_none(self) -> None:
        """A marker carrying a valid issue but a missing/zero review_id is skipped (fail-closed)."""
        payload: dict[str, object] = {"issue": 42, "active": True}
        assert find_suppressed_deferral_state([_marker_comment(7, payload)]) == (None, None)

    def test_boolean_review_id_is_rejected(self) -> None:
        """A marker with a boolean review_id (e.g., ``true``) is skipped as a malformed payload."""
        payload: dict[str, object] = {"review_id": True, "issue": 42, "active": True}
        assert find_suppressed_deferral_state([_marker_comment(7, payload)]) == (None, None)

    def test_boolean_issue_is_rejected(self) -> None:
        """A marker with a boolean issue field (e.g., ``true``) is skipped as a malformed payload."""
        payload: dict[str, object] = {"review_id": "100", "issue": True, "active": True}
        assert find_suppressed_deferral_state([_marker_comment(7, payload)]) == (None, None)
