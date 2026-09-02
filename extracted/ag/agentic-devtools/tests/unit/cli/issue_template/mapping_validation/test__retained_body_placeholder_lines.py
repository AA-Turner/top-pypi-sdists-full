"""Tests for _retained_body_placeholder_lines in agentic_devtools.cli.issue_template.mapping_validation."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.mapping_validation import (
    _retained_body_placeholder_lines,
)
from agentic_devtools.cli.issue_template.renderer import _compute_fence_flags


class TestRetainedBodyPlaceholderLines:
    """Tests for _retained_body_placeholder_lines."""

    def test_finds_placeholder_in_custom_section(self) -> None:
        """Returns the line index of a plain placeholder in a custom section."""
        template = "## Links\n\n{{url}}\n"
        lines = template.split("\n")
        fence_flags = _compute_fence_flags(lines)
        result = _retained_body_placeholder_lines(lines, fence_flags, {"url": "body:Links"})
        assert result == {"url": 2}

    def test_indented_placeholder_in_custom_section_is_skipped(self) -> None:
        """A 4-space-indented placeholder is CommonMark code; it must not be retained."""
        template = "## Links\n\n    {{url}}\n{{url}}\n"
        lines = template.split("\n")
        fence_flags = _compute_fence_flags(lines)
        result = _retained_body_placeholder_lines(lines, fence_flags, {"url": "body:Links"})
        # The indented line (index 2) must be skipped; the non-indented one (index 3) is retained.
        assert result == {"url": 3}

    def test_tab_indented_placeholder_in_custom_section_is_skipped(self) -> None:
        """A tab-indented placeholder is CommonMark code; it must not be retained."""
        template = "## Links\n\n\t{{url}}\n{{url}}\n"
        lines = template.split("\n")
        fence_flags = _compute_fence_flags(lines)
        result = _retained_body_placeholder_lines(lines, fence_flags, {"url": "body:Links"})
        assert result == {"url": 3}

    def test_fenced_placeholder_in_custom_section_is_skipped(self) -> None:
        """Placeholders inside fenced blocks must not be retained."""
        template = "## Links\n\n```\n{{url}}\n```\n{{url}}\n"
        lines = template.split("\n")
        fence_flags = _compute_fence_flags(lines)
        result = _retained_body_placeholder_lines(lines, fence_flags, {"url": "body:Links"})
        assert result == {"url": 5}

    def test_no_matching_section_returns_empty(self) -> None:
        """Returns an empty dict when the section heading is absent."""
        lines = ["no heading", "{{url}}"]
        fence_flags = _compute_fence_flags(lines)
        result = _retained_body_placeholder_lines(lines, fence_flags, {"url": "body:Links"})
        assert result == {}

    def test_non_body_targets_ignored(self) -> None:
        """Only body: targets are considered; frontmatter/omit targets are ignored."""
        template = "## Links\n\n{{url}}\n"
        lines = template.split("\n")
        fence_flags = _compute_fence_flags(lines)
        result = _retained_body_placeholder_lines(lines, fence_flags, {"url": "frontmatter", "created_at": "omit"})
        assert result == {}
