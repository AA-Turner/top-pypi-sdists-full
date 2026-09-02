"""Tests for _render_file_block."""

from agentic_devtools.cli.azure_devops.consolidated_review import _render_file_block
from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    ReviewStatus,
    SuggestionEntry,
)

_BASE_URL = "https://dev.azure.com/org/proj/_git/repo/pullrequest/42"


def _suggestion(severity: object, line: int = 1) -> SuggestionEntry:
    return SuggestionEntry(
        threadId=1,
        commentId=1,
        line=line,
        endLine=line,
        severity=severity,  # type: ignore[arg-type]
        outOfScope=False,
        linkText=f"line {line}",
        content="fix it",
    )


def _file(suggestions: list[SuggestionEntry]) -> FileEntry:
    return FileEntry(
        threadId=3,
        commentId=1,
        folder="src",
        fileName="a.ts",
        status=ReviewStatus.NEEDS_WORK.value,
        summary="needs work",
        suggestions=suggestions,
    )


class TestRenderFileBlock:
    """Tests for _render_file_block."""

    def test_renders_details_block(self):
        lines = _render_file_block(_BASE_URL, _file([]))
        text = "\n".join(lines)
        assert "<details>" in text
        assert "a.ts" in text
        assert "- None" in text

    def test_known_severity_grouped(self):
        lines = _render_file_block(_BASE_URL, _file([_suggestion("high")]))
        text = "\n".join(lines)
        assert "High" in text

    def test_unknown_severity_rendered_in_other_group(self):
        lines = _render_file_block(_BASE_URL, _file([_suggestion("blocker")]))
        text = "\n".join(lines)
        assert "Other Severity (Blocker)" in text

    def test_empty_severity_rendered_as_unknown(self):
        lines = _render_file_block(_BASE_URL, _file([_suggestion(None)]))
        text = "\n".join(lines)
        assert "Other Severity (Unknown)" in text

    def test_repeated_unknown_severity_grouped_once(self):
        # Two None-severity suggestions both normalize to "" but are stored
        # under the "unknown" key, so the second re-enters the else branch and
        # finds the key already present (the 403->406 skip arm).
        lines = _render_file_block(
            _BASE_URL,
            _file([_suggestion(None, line=1), _suggestion(None, line=2)]),
        )
        text = "\n".join(lines)
        assert text.count("Other Severity (Unknown)") == 1
        assert "line 1" in text
        assert "line 2" in text
