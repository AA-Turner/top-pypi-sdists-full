"""Tests for suppressed_reaper.parse_no_change_marker()."""

from __future__ import annotations

from agentic_devtools.cli.ci.suppressed_reaper import parse_no_change_marker
from tests.unit.cli.ci.suppressed_reaper._fixtures import ISSUE, MARKER, REVIEW_ID


class TestParseNoChangeMarker:
    """The anchored marker is read from the raw body only."""

    def test_returns_review_id_and_deferred_issue(self) -> None:
        """Both identifiers are captured from a marker on its own line."""
        assert parse_no_change_marker(f"intro\n\n{MARKER}\n\nCloses #1") == (REVIEW_ID, ISSUE)

    def test_tolerates_leading_whitespace(self) -> None:
        """Leading tabs or spaces still anchor the marker to its own line."""
        assert parse_no_change_marker(f"\t{MARKER}  ") == (REVIEW_ID, ISSUE)

    def test_returns_none_when_absent(self) -> None:
        """A body without the marker yields nothing."""
        assert parse_no_change_marker("no marker here") is None

    def test_returns_none_for_empty_body(self) -> None:
        """An empty body is handled without raising."""
        assert parse_no_change_marker("") is None

    def test_returns_none_when_inline(self) -> None:
        """A marker sharing its line with prose is not anchored."""
        assert parse_no_change_marker(f"see {MARKER}") is None

    def test_returns_none_when_repeated(self) -> None:
        """Two markers name two issues; the body is ambiguous."""
        assert parse_no_change_marker(f"{MARKER}\n{MARKER}") is None

    def test_returns_none_for_non_numeric_ids(self) -> None:
        """A malformed identifier does not match the anchored pattern."""
        body = "<!-- agdt:suppressed-eval:no-changes-needed review-id:abc deferred-issue:1 -->"
        assert parse_no_change_marker(body) is None
