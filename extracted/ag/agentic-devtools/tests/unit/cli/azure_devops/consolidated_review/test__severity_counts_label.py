"""Tests for _severity_counts_label."""

from agentic_devtools.cli.azure_devops.consolidated_review import _severity_counts_label
from agentic_devtools.cli.azure_devops.review_state import SuggestionEntry


def _suggestion(severity: object) -> SuggestionEntry:
    return SuggestionEntry(
        threadId=1,
        commentId=1,
        line=1,
        endLine=1,
        severity=severity,  # type: ignore[arg-type]
        outOfScope=False,
        linkText="line 1",
        content="fix",
    )


class TestSeverityCountsLabel:
    """Tests for _severity_counts_label."""

    def test_empty_when_no_suggestions(self):
        assert _severity_counts_label([]) == ""

    def test_counts_known_severities_in_order(self):
        label = _severity_counts_label([_suggestion("high"), _suggestion("medium"), _suggestion("medium")])
        assert label == "1 High, 2 Medium"

    def test_unknown_severity_counted_as_other(self):
        label = _severity_counts_label([_suggestion("blocker")])
        assert label == "1 Other"

    def test_mixed_known_and_unknown(self):
        label = _severity_counts_label([_suggestion("low"), _suggestion("weird"), _suggestion(None)])
        assert label == "1 Low, 2 Other"
