"""Tests for _review_has_comments()."""

from types import SimpleNamespace
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.watchdog_command import _review_has_comments


class TestReviewHasComments:
    """Tests for actionable review comment detection."""

    def test_nonempty_review_body_is_actionable(self) -> None:
        provider = MagicMock()
        assert _review_has_comments(provider, 42, SimpleNamespace(body=" Please fix ")) is True
        provider.list_review_comments.assert_not_called()

    def test_invalid_review_ids_are_not_actionable(self) -> None:
        provider = MagicMock()
        for review_id in (0, -1, True, "7"):
            assert _review_has_comments(provider, 42, SimpleNamespace(body="", id=review_id)) is False
        provider.list_review_comments.assert_not_called()

    def test_inline_comments_make_empty_body_actionable(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.return_value = [object()]
        review = SimpleNamespace(body="", id=7)
        assert _review_has_comments(provider, 42, review) is True
        provider.list_review_comments.assert_called_once_with(42, 7)

    def test_empty_inline_comments_are_not_actionable(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.return_value = []
        assert _review_has_comments(provider, 42, SimpleNamespace(body="", id=7)) is False

    def test_comment_lookup_errors_are_not_actionable(self, caplog) -> None:
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("comments unavailable")
        assert _review_has_comments(provider, 42, SimpleNamespace(body="", id=7)) is False
        assert "Could not inspect comments for PR #42 review 7" in caplog.text
