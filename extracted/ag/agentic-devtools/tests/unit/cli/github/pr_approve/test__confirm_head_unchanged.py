"""Tests for _confirm_head_unchanged helper."""

from unittest.mock import patch

from agentic_devtools.cli.github import pr_approve


class TestConfirmHeadUnchanged:
    """Tests for _confirm_head_unchanged."""

    def test_returns_true_when_head_still_matches(self):
        """The current head matching expected_head reports still_current=True."""
        expected_head = "a" * 40
        with patch.object(pr_approve, "_fetch_current_head_sha", return_value=(expected_head, "")):
            still_current, current_head, error = pr_approve._confirm_head_unchanged(42, "owner/repo", expected_head)

        assert still_current is True
        assert current_head == expected_head
        assert error == ""

    def test_returns_false_when_head_moved(self):
        """A head that moved past expected_head reports still_current=False."""
        expected_head = "a" * 40
        moved_head = "b" * 40
        with patch.object(pr_approve, "_fetch_current_head_sha", return_value=(moved_head, "")):
            still_current, current_head, error = pr_approve._confirm_head_unchanged(42, "owner/repo", expected_head)

        assert still_current is False
        assert current_head == moved_head
        assert error == ""

    def test_returns_false_when_head_lookup_fails(self):
        """A failed head lookup reports still_current=False with the error detail."""
        expected_head = "a" * 40
        with patch.object(pr_approve, "_fetch_current_head_sha", return_value=(None, "network error")):
            still_current, current_head, error = pr_approve._confirm_head_unchanged(42, "owner/repo", expected_head)

        assert still_current is False
        assert current_head is None
        assert error == "network error"
