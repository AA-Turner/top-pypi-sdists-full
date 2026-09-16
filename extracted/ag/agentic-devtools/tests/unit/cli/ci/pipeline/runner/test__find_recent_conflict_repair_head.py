"""Tests for _find_recent_conflict_repair_head."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import cast
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.pipeline.runner import (
    DiffPreservationBlockerLookupError,
    _find_recent_conflict_repair_head,
)
from agentic_devtools.cli.ci.provider import CIPlatformProvider
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class _SupportedProvider:
    """Provider with an implemented authenticated identity lookup."""

    def __init__(self, login: object = "", error: Exception | None = None) -> None:
        self._login = login
        self._error = error

    def get_pr_token_login(self) -> object:
        if self._error is not None:
            raise self._error
        return self._login


class TestFindRecentConflictRepairHead:
    """Tests for the cross-run conflict-repair baseline lookup."""

    def test_returns_empty_when_no_comment(self) -> None:
        provider = MagicMock()
        provider.find_comment.return_value = None
        assert _find_recent_conflict_repair_head(provider, 1, "headsha") == ""

    def test_returns_empty_for_malformed_comment_tuple(self) -> None:
        provider = MagicMock()
        provider.find_comment.return_value = ()
        assert _find_recent_conflict_repair_head(provider, 1, "headsha") == ""

    def test_returns_empty_when_login_lookup_is_not_callable(self) -> None:
        provider = MagicMock()
        provider.get_pr_token_login = ""

        assert _find_recent_conflict_repair_head(provider, 1, "feedbeef") == ""
        provider.find_comment.assert_not_called()

    def test_returns_empty_when_login_lookup_uses_base_default(self) -> None:
        provider = MagicMock()
        provider.get_pr_token_login = CIPlatformProvider.get_pr_token_login.__get__(provider, CIPlatformProvider)

        assert _find_recent_conflict_repair_head(provider, 1, "feedbeef") == ""
        provider.list_issue_comments.assert_not_called()

    def test_returns_empty_for_unparseable_marker(self) -> None:
        provider = MagicMock()
        provider.find_comment.return_value = (1, "not-a-marker")
        assert _find_recent_conflict_repair_head(provider, 1, "headsha") == ""

    def test_returns_empty_for_empty_comment_body(self) -> None:
        provider = MagicMock()
        provider.find_comment.return_value = (1, "")
        assert _find_recent_conflict_repair_head(provider, 1, "headsha") == ""

    def test_returns_empty_when_marker_targets_current_head(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.find_comment.return_value = (1, f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->")
        assert _find_recent_conflict_repair_head(provider, 1, "def456") == ""

    def test_returns_empty_for_invalid_timestamp(self) -> None:
        provider = MagicMock()
        provider.find_comment.return_value = (1, "<!-- agdt:conflict-repair:abc123:def456:not-a-time -->")
        assert _find_recent_conflict_repair_head(provider, 1, "feedbeef") == ""

    def test_uses_recent_naive_timestamp(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).replace(tzinfo=None).isoformat(timespec="seconds")
        provider.find_comment.return_value = (1, f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->")
        assert _find_recent_conflict_repair_head(provider, 1, "feedbeef") == ""
        provider.find_comment.assert_not_called()

    def test_keeps_old_baseline_until_a_repaired_head_is_validated(self) -> None:
        provider = MagicMock()
        marker_time = datetime(2020, 1, 1, tzinfo=UTC).isoformat()
        provider.find_comment.return_value = (1, f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->")
        assert _find_recent_conflict_repair_head(provider, 1, "feedbeef") == ""
        provider.find_comment.assert_not_called()

    def test_uses_latest_trusted_author_marker(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:deadbeef:{marker_time} -->",
            ),
            IssueCommentInfo(
                id=11,
                author="someone-else",
                body=f"<!-- agdt:conflict-repair:abc123:cafebabe:{marker_time} -->",
            ),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "feedbeef") == "deadbeef"
        provider.find_comment.assert_not_called()

    def test_returns_empty_when_no_trusted_marker(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=11,
                author="someone-else",
                body=f"<!-- agdt:conflict-repair:abc123:cafebabe:{marker_time} -->",
            ),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "feedbeef") == ""

    def test_returns_empty_when_latest_trusted_marker_records_current_head_validation(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
            IssueCommentInfo(
                id=11,
                author="trusted-bot",
                body="<!-- agdt:conflict-repair-validated:feedbeef -->",
            ),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "feedbeef") == ""

    def test_consumes_dispatch_when_newer_validation_targets_a_different_head(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
            IssueCommentInfo(
                id=11,
                author="trusted-bot",
                body="<!-- agdt:conflict-repair-validated:def456 -->",
            ),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "laterhead") == ""

    def test_uses_latest_validated_marker_id_even_when_comments_are_unsorted(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=11,
                author="trusted-bot",
                body="<!-- agdt:conflict-repair-validated:feedbeef -->",
            ),
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body="<!-- agdt:conflict-repair-validated:deadc0de -->",
            ),
            IssueCommentInfo(
                id=12,
                author="trusted-bot",
                body=f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
            ),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "laterhead") == "def456"

    def test_updates_to_newer_validated_marker_id(self) -> None:
        provider = MagicMock()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body="<!-- agdt:conflict-repair-validated:deadc0de -->",
            ),
            IssueCommentInfo(
                id=11,
                author="trusted-bot",
                body="<!-- agdt:conflict-repair-validated:feedbeef -->",
            ),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "laterhead") == ""

    def test_ignores_embedded_validated_marker_in_trusted_dispatch_comment(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body="\n".join(
                    [
                        "@copilot repair context",
                        "",
                        "```text",
                        "<!-- agdt:conflict-repair-validated:feedbeef -->",
                        "```",
                        "",
                        f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
                    ]
                ),
            ),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "laterhead") == "def456"

    def test_rejects_dispatch_marker_that_is_not_the_final_line(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.get_pr_token_login.return_value = "trusted-bot"
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=10,
                author="trusted-bot",
                body="\n".join(
                    [
                        f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->",
                        "```text",
                        "embedded context",
                        "```",
                    ]
                ),
            ),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "laterhead") == ""

    def test_returns_empty_when_fallback_validation_marker_is_newer_for_current_head(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.find_comment.side_effect = [
            (10, f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->"),
            (11, "<!-- agdt:conflict-repair-validated:feedbeef -->"),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "feedbeef") == ""

    def test_does_not_use_unauthenticated_dispatch_when_validation_targets_different_head(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.find_comment.side_effect = [
            (10, f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->"),
            (11, "<!-- agdt:conflict-repair-validated:def456 -->"),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "laterhead") == ""
        provider.find_comment.assert_not_called()

    def test_does_not_use_unauthenticated_embedded_validated_marker_text(self) -> None:
        provider = MagicMock()
        marker_time = datetime.now(UTC).isoformat()
        provider.find_comment.side_effect = [
            (10, f"<!-- agdt:conflict-repair:abc123:def456:{marker_time} -->"),
            (11, "```text\n<!-- agdt:conflict-repair-validated:feedbeef -->\n```"),
        ]

        assert _find_recent_conflict_repair_head(provider, 1, "laterhead") == ""
        provider.find_comment.assert_not_called()

    def test_raises_when_login_lookup_raises(self) -> None:
        provider = _SupportedProvider(error=RuntimeError("lookup failed"))

        with pytest.raises(
            DiffPreservationBlockerLookupError, match="failed to resolve authenticated blocker identity"
        ):
            _find_recent_conflict_repair_head(cast(CIPlatformProvider, provider), 1, "feedbeef")

    def test_raises_when_login_lookup_returns_empty(self) -> None:
        provider = _SupportedProvider()

        with pytest.raises(DiffPreservationBlockerLookupError, match="authenticated blocker identity is empty"):
            _find_recent_conflict_repair_head(cast(CIPlatformProvider, provider), 1, "feedbeef")

    def test_raises_when_login_lookup_returns_non_string(self) -> None:
        provider = _SupportedProvider(login=123)

        with pytest.raises(DiffPreservationBlockerLookupError, match="authenticated blocker identity is unusable"):
            _find_recent_conflict_repair_head(cast(CIPlatformProvider, provider), 1, "feedbeef")

    def test_reraises_rate_limit_from_login_lookup(self) -> None:
        provider = _SupportedProvider(
            error=ProviderRateLimitError(
                provider="github",
                credential_identity="SPECKIT_PR_TOKEN",
            )
        )

        with pytest.raises(ProviderRateLimitError):
            _find_recent_conflict_repair_head(cast(CIPlatformProvider, provider), 1, "feedbeef")
