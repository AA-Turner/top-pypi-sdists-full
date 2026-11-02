"""Tests for _get_latest_agent_comment()."""

import logging
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.evaluator.snapshot_comments import _get_latest_agent_comment
from agentic_devtools.cli.ci.models import IssueCommentInfo


class TestGetLatestAgentComment:
    """Tests for _get_latest_agent_comment helper."""

    def test_returns_none_without_copilot_comments(self):
        """Latest agent helper returns None when no Copilot-authored comments exist."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=1, author="dev", body="x", created_at="2026-01-01T00:00:00Z"),
        ]

        result = _get_latest_agent_comment(provider, 42)

        assert result is None

    def test_returns_none_without_provider_support(self):
        """Latest agent helper returns None when provider has no issue-comment method."""
        provider = MagicMock()
        provider.list_issue_comments = None

        result = _get_latest_agent_comment(provider, 42)

        assert result is None

    def test_uses_supplied_comments_without_fetching(self):
        """Uses an explicit comment list without querying the provider."""
        provider = MagicMock()

        assert _get_latest_agent_comment(provider, 42, comments=[]) is None
        provider.list_issue_comments.assert_not_called()

    def test_returns_latest_copilot_comment(self):
        """Returns the newest Copilot-authored comment as a CommentInfo."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=1, author="copilot[bot]", body="older", created_at="2026-01-01T00:00:00Z"),
            IssueCommentInfo(id=2, author="copilot[bot]", body="newer", created_at="2026-01-02T00:00:00Z"),
        ]

        result = _get_latest_agent_comment(provider, 42)

        assert result is not None
        assert result.id == 2
        assert result.body == "newer"

    def test_fetches_comments_when_none_are_supplied(self):
        """Fetches issue comments from the provider when no comment list is supplied."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(id=2, author="copilot[bot]", body="latest", created_at="2026-01-02T00:00:00Z"),
        ]

        result = _get_latest_agent_comment(provider, 42)

        assert result is not None
        assert result.id == 2
        provider.list_issue_comments.assert_called_once_with(42)

    def test_sanitizes_unterminated_html_comment_in_body(self):
        """A cut-off ``<!--`` in the agent reply is balanced so following text renders."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=3,
                author="copilot[bot]",
                body="> quoted\n> <!-- copilo\n\nFixed in the latest commit.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42)

        assert result is not None
        # The cut-off marker is closed at the end of its line; trailing content survives.
        assert "> <!-- copilo -->" in result.body
        assert "Fixed in the latest commit." in result.body

    def test_persists_sanitized_body_when_opted_in(self):
        """A changed sanitized body is patched back to the provider when requested."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=3,
                author="copilot[bot]",
                body="> quoted\n> <!-- copilo\n\nFixed in the latest commit.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert result.body == "> quoted\n> <!-- copilo -->\n\nFixed in the latest commit."
        provider.update_comment.assert_called_once_with(3, result.body)

    def test_skips_persist_when_provider_has_no_update_comment(self):
        """Opt-in persistence is best-effort when the provider cannot update comments."""
        provider = MagicMock()
        provider.update_comment = None
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=3,
                author="copilot[bot]",
                body="> quoted\n> <!-- copilo\n\nFixed in the latest commit.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert result.body == "> quoted\n> <!-- copilo -->\n\nFixed in the latest commit."

    def test_logs_when_persisting_sanitized_body_fails(self, caplog: pytest.LogCaptureFixture):
        """A failed best-effort PATCH is logged without blocking sanitization."""
        provider = MagicMock()
        provider.update_comment.side_effect = RuntimeError("patch failed")
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=3,
                author="copilot[bot]",
                body="> quoted\n> <!-- copilo\n\nFixed in the latest commit.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        with caplog.at_level(logging.WARNING):
            result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert result.body == "> quoted\n> <!-- copilo -->\n\nFixed in the latest commit."
        assert "Failed to persist sanitized Copilot comment 3 on PR #42" in caplog.text

    def test_persists_neutralized_body_when_sanitization_introduces_completion_sentinel(self):
        """A synthesized completion marker is escaped before the rewrite is patched."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=7,
                author="copilot[bot]",
                body="<!-- copilot-agent-result\nHEAD: `abc12345`. Done.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert result.body == "&lt;!-- copilot-agent-result -->\nHEAD: `abc12345`. Done."
        provider.update_comment.assert_called_once_with(7, result.body)

    def test_persists_neutralized_body_when_sanitization_synthesizes_repair_satisfied_marker(self):
        """A forged repair-satisfied marker is escaped while unrelated markers survive.

        Balancing a truncated ``<!-- ai-pr-loop:repair-satisfied`` opener yields
        the canonical :data:`REPAIR_SATISFIED_MARKER`; persisting it would let a
        later evaluator run accept it as a genuine Copilot signal and clear the
        suppressed-comments block. Escape only the synthesized opener so the
        rendering-safe rewrite can still be persisted.
        """
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=9,
                author="copilot[bot]",
                body="> quoted\n> <!-- ai-pr-loop:repair-satisfied\n> <!-- review-id:123 -->",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert "> &lt;!-- ai-pr-loop:repair-satisfied -->" in result.body
        assert "> <!-- review-id:123 -->" in result.body
        provider.update_comment.assert_called_once_with(9, result.body)
