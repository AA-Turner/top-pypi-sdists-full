"""Tests for _get_latest_agent_comment()."""

import logging
from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.evaluator.snapshot import _get_latest_agent_comment
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

    def test_persists_neutralized_body_when_sanitization_synthesizes_review_id_marker(self):
        """A forged ``review-id`` marker is escaped before persisting the rewrite."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=11,
                author="copilot[bot]",
                body="<!-- ai-pr-loop:repair-satisfied -->\n<!-- review-id:456\n\nDone.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert "&lt;!-- review-id:456 -->" in result.body
        assert "<!-- ai-pr-loop:repair-satisfied -->" in result.body
        provider.update_comment.assert_called_once_with(11, result.body)

    def test_persists_neutralized_body_when_sanitization_forges_second_review_id(self):
        """An earlier forged ``review-id`` is escaped while the valid marker remains.

        Balancing an earlier truncated ``<!-- review-id:999`` creates a second
        valid marker that precedes the legitimate ``<!-- review-id:123 -->``. A
        later run reading the first regex match would trust review 999, so the
        synthesized earlier marker must be neutralized before persistence.
        """
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=13,
                author="copilot[bot]",
                body="<!-- review-id:999\n<!-- review-id:123 -->\n\nDone.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert result.body.startswith("&lt;!-- review-id:999 -->")
        assert "<!-- review-id:123 -->" in result.body
        provider.update_comment.assert_called_once_with(13, result.body)

    def test_persists_neutralized_body_when_sanitization_forges_second_repair_satisfied(self):
        """An earlier forged repair-satisfied marker is escaped while the valid one remains.

        Presence alone is not enough: balancing an earlier truncated
        ``<!-- ai-pr-loop:repair-satisfied`` opener adds a *second* canonical
        marker. Neutralize only the synthesized earlier marker before persisting.
        """
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=15,
                author="copilot[bot]",
                body="<!-- ai-pr-loop:repair-satisfied\n<!-- ai-pr-loop:repair-satisfied -->\n\nDone.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert result.body.startswith("&lt;!-- ai-pr-loop:repair-satisfied -->")
        assert result.body.count("<!-- ai-pr-loop:repair-satisfied -->") == 1
        provider.update_comment.assert_called_once_with(15, result.body)

    def test_persists_neutralized_body_when_sanitization_synthesizes_copilot_trigger_marker(self):
        """A forged ``copilot-trigger`` marker is escaped before persisting the rewrite.

        Balancing a truncated ``<!-- copilot-trigger:777:2026-...`` opener yields a
        complete dedup marker. ``is_duplicate_trigger`` would then treat the
        synthesized (unparseable-timestamp) marker as a non-expiring duplicate and
        permanently suppress a legitimate re-dispatch, so the marker must be
        neutralized before the rewrite is written back.
        """
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=17,
                author="copilot[bot]",
                body="> quoted\n> <!-- copilot-trigger:777:2026-08-10T00:00:00+00:00\n\nDone.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert "&lt;!-- copilot-trigger:777:2026-08-10T00:00:00+00:00 -->" in result.body
        provider.update_comment.assert_called_once_with(17, result.body)

    def test_persists_neutralized_body_when_sanitization_synthesizes_conflict_repair_marker(self):
        """A forged ``agdt:conflict-repair`` marker is escaped before persistence.

        Balancing a truncated ``<!-- agdt:conflict-repair:...`` opener yields a
        complete dispatch marker that ``find_comment`` could surface as the newest
        result, shadowing the valid dispatch marker. Escape the synthesized marker
        so the rendering-safe rewrite can still be persisted.
        """
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=19,
                author="copilot[bot]",
                body="> quoted\n> <!-- agdt:conflict-repair:abc123:def456:2026-08-10T00:00:00+00:00\n\nDone.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert "&lt;!-- agdt:conflict-repair:abc123:def456:2026-08-10T00:00:00+00:00 -->" in result.body
        provider.update_comment.assert_called_once_with(19, result.body)

    def test_persists_neutralized_body_when_sanitization_synthesizes_repair_dispatch_marker(self):
        """A forged repair-dispatch marker is escaped before persistence.

        Balancing a truncated ``<!-- repair-dispatch:...`` opener yields a valid
        dedup marker. Persisting that rewrite would let ``check_deduplication()``
        increment or block against the synthesized marker and potentially update
        the Copilot-authored comment itself, so the marker must be neutralized.
        """
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=21,
                author="copilot[bot]",
                body="> quoted\n> <!-- repair-dispatch:abc12345:3:writer-token\n\nDone.",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert "&lt;!-- repair-dispatch:abc12345:3:writer-token -->" in result.body
        provider.update_comment.assert_called_once_with(21, result.body)

    def test_persists_neutralized_body_when_sanitization_synthesizes_evaluator_lock_marker(self):
        """A forged evaluator-lock marker is escaped before persistence.

        Balancing a truncated ``<!-- copilot-evaluator-lock`` opener yields
        the canonical lock marker.  Persisting it could let a later
        ``acquire_lock()`` call select this Copilot-authored comment as the
        canonical lock comment, potentially overwriting it or honoring forged
        ``token``/``state`` lines. Escape only the synthesized opener so the
        rendering-safe rewrite can still be written back.
        """
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            IssueCommentInfo(
                id=23,
                author="copilot[bot]",
                body="> quoted\n> <!-- copilot-evaluator-lock\ntoken=forged\nstate=active",
                created_at="2026-01-03T00:00:00Z",
            )
        ]

        result = _get_latest_agent_comment(provider, 42, persist_sanitized_body=True)

        assert result is not None
        assert "&lt;!-- copilot-evaluator-lock -->" in result.body
        provider.update_comment.assert_called_once_with(23, result.body)
