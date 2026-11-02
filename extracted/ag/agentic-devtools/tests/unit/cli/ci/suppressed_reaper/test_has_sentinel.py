"""Tests for suppressed_reaper.has_sentinel()."""

from __future__ import annotations

from agentic_devtools.cli.ci.suppressed_reaper import has_sentinel
from tests.unit.cli.ci.suppressed_reaper._fixtures import SENTINEL


class TestHasSentinel:
    """The sentinel counts only on a line of its own."""

    def test_true_on_its_own_line(self) -> None:
        """A standalone sentinel line satisfies the condition."""
        assert has_sentinel(f"text\n\n{SENTINEL}\n\nmore") is True

    def test_true_with_surrounding_whitespace(self) -> None:
        """Indentation does not break the anchor."""
        assert has_sentinel(f"  {SENTINEL}\t") is True

    def test_false_when_inline(self) -> None:
        """A sentinel quoted inside a sentence does not count."""
        assert has_sentinel(f"not {SENTINEL} really") is False

    def test_false_when_absent(self) -> None:
        """A body without the sentinel fails the condition."""
        assert has_sentinel("nothing here") is False

    def test_false_for_empty_body(self) -> None:
        """An empty body is handled without raising."""
        assert has_sentinel("") is False
