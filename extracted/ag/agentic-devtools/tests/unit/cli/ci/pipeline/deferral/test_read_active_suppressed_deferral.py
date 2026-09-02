"""Tests for read_active_suppressed_deferral in the deferral module."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.deferral import (
    SUPPRESSED_DEFERRAL_SENTINEL,
    read_active_suppressed_deferral,
)


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


class TestReadActiveSuppressedDeferral:
    """Tests for read_active_suppressed_deferral."""

    def test_returns_payload_for_active_marker(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_marker_comment(7, _active_payload())]

        payload = read_active_suppressed_deferral(provider, 1, 100)

        assert payload is not None
        assert payload["issue"] == 4242

    def test_returns_none_when_marker_absent(self) -> None:
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        assert read_active_suppressed_deferral(provider, 1, 100) is None

    def test_never_expires(self) -> None:
        """The suppressed marker carries no TTL — it must stay readable forever."""
        provider = MagicMock()
        payload = _active_payload()
        payload["posted_at"] = "2020-01-01T00:00:00Z"
        provider.list_issue_comments.return_value = [_marker_comment(7, payload)]

        assert read_active_suppressed_deferral(provider, 1, 100) is not None

    def test_trusts_pr_token_login_from_provider(self) -> None:
        """Marker posted by the workflow identity is trusted when provider resolves the login."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_marker_comment(7, _active_payload(), author="amarsnik_swica")]
        provider.get_pr_token_login.return_value = "AMARSNIK_swica"  # case-insensitive match

        payload = read_active_suppressed_deferral(provider, 1, 100)

        assert payload is not None
        assert payload["issue"] == 4242

    def test_ignores_workflow_identity_marker_when_token_login_unavailable(self) -> None:
        """Without get_pr_token_login, only the static allowed set applies."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_marker_comment(7, _active_payload(), author="amarsnik_swica")]
        provider.get_pr_token_login.side_effect = RuntimeError("token not set")

        assert read_active_suppressed_deferral(provider, 1, 100) is None

    def test_empty_pr_token_login_uses_static_set_only(self) -> None:
        """An empty string returned by get_pr_token_login falls back to the static allowed set."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_marker_comment(7, _active_payload(), author="copilot")]
        provider.get_pr_token_login.return_value = ""  # falsy → skipped

        payload = read_active_suppressed_deferral(provider, 1, 100)

        assert payload is not None
        assert payload["issue"] == 4242

    def test_returns_none_when_issue_is_zero(self) -> None:
        """A zero issue number does not identify a valid triage target; treat as absent."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_marker_comment(7, {**_active_payload(), "issue": 0})]

        assert read_active_suppressed_deferral(provider, 1, 100) is None

    def test_returns_none_when_issue_is_negative(self) -> None:
        """A negative issue number is invalid; return None so approve/merge remain gated."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_marker_comment(7, {**_active_payload(), "issue": -1})]

        assert read_active_suppressed_deferral(provider, 1, 100) is None

    def test_returns_none_when_issue_is_boolean(self) -> None:
        """bool is a subclass of int in Python; True (==1) must still be rejected."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_marker_comment(7, {**_active_payload(), "issue": True})]

        assert read_active_suppressed_deferral(provider, 1, 100) is None

    def test_returns_none_when_issue_is_string(self) -> None:
        """A string issue value is not a valid integer; treat as absent."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_marker_comment(7, {**_active_payload(), "issue": "42"})]

        assert read_active_suppressed_deferral(provider, 1, 100) is None

    def test_returns_none_when_issue_key_is_absent(self) -> None:
        """A marker without an issue key cannot identify a triage target."""
        payload = _active_payload()
        del payload["issue"]
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_marker_comment(7, payload)]

        assert read_active_suppressed_deferral(provider, 1, 100) is None
