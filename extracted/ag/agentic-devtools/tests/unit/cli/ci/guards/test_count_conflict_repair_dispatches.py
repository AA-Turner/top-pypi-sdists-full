"""Tests for count_conflict_repair_dispatches() guard helper."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.guards import count_conflict_repair_dispatches
from agentic_devtools.cli.ci.models import IssueCommentInfo

_HEAD = "abc" * 13 + "a"  # 40-char hex-like head SHA
_OTHER_HEAD = "111" * 13 + "1"
_BASE = "def" * 13 + "d"


def _marker(base_sha: str, head_sha: str) -> str:
    return f"<!-- agdt:conflict-repair:{base_sha}:{head_sha}:2024-06-01T12:00:00+00:00 -->"


def _comment(body: str, *, author: str = "ci-bot", comment_id: int = 1) -> IssueCommentInfo:
    return IssueCommentInfo(id=comment_id, author=author, body=body, created_at="2024-06-01T12:00:00Z")


class TestCountConflictRepairDispatches:
    """Tests for the per-HEAD conflict-repair dispatch counter."""

    def test_returns_zero_when_no_comments(self) -> None:
        """No PR comments → zero dispatches."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = []

        assert count_conflict_repair_dispatches(provider, 7, _HEAD) == 0
        provider.list_issue_comments.assert_called_once_with(7)

    def test_counts_dispatch_markers_for_current_head(self) -> None:
        """Each non-Copilot comment carrying a marker for HEAD counts once."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            _comment(_marker(_BASE, _HEAD), comment_id=1),
            _comment(_marker(_BASE, _HEAD), comment_id=2),
        ]

        assert count_conflict_repair_dispatches(provider, 7, _HEAD) == 2

    def test_ignores_markers_for_other_head_shas(self) -> None:
        """Markers targeting a superseded HEAD are not counted."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [_comment(_marker(_BASE, _OTHER_HEAD))]

        assert count_conflict_repair_dispatches(provider, 7, _HEAD) == 0

    def test_ignores_comments_without_marker(self) -> None:
        """Unrelated comments (including empty bodies) are not counted."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            _comment("", comment_id=1),
            _comment("Just a normal review comment", comment_id=2),
        ]

        assert count_conflict_repair_dispatches(provider, 7, _HEAD) == 0

    def test_ignores_copilot_authored_quote_echoes(self) -> None:
        """A Copilot comment quoting the dispatch marker does not inflate the count."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            _comment(_marker(_BASE, _HEAD), author="Copilot", comment_id=1),
        ]

        assert count_conflict_repair_dispatches(provider, 7, _HEAD) == 0

    def test_counts_each_comment_at_most_once(self) -> None:
        """A comment containing several markers for HEAD counts as one dispatch."""
        provider = MagicMock()
        body = f"{_marker(_BASE, _HEAD)}\n\n{_marker(_BASE, _HEAD)}"
        provider.list_issue_comments.return_value = [_comment(body)]

        assert count_conflict_repair_dispatches(provider, 7, _HEAD) == 1

    def test_dispatch_login_restricts_count_to_that_author(self) -> None:
        """When dispatch_login is provided, only comments from that login are counted."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            _comment(_marker(_BASE, _HEAD), author="automation-bot", comment_id=1),
            _comment(_marker(_BASE, _HEAD), author="other-user", comment_id=2),
        ]

        assert count_conflict_repair_dispatches(provider, 7, _HEAD, "automation-bot") == 1

    def test_dispatch_login_excludes_other_authors_even_if_not_copilot(self) -> None:
        """With dispatch_login set, non-dispatch non-Copilot comments are excluded."""
        provider = MagicMock()
        provider.list_issue_comments.return_value = [
            _comment(_marker(_BASE, _HEAD), author="ci-bot", comment_id=1),
        ]

        # "ci-bot" is not Copilot, but also not the expected dispatch_login
        assert count_conflict_repair_dispatches(provider, 7, _HEAD, "automation-bot") == 0
