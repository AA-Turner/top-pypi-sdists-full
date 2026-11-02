"""Tests for _cap_content in retro_spec/synthesis.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.retro_spec.synthesis import _cap_content


class TestCapContent:
    """Tests for the _cap_content helper."""

    def test_returns_content_unchanged_when_under_limit(self) -> None:
        """Content that fits within the limit passes through unchanged."""
        assert _cap_content("hello", 100) == "hello"

    def test_truncates_with_note_when_over_limit(self) -> None:
        """Content exceeding the limit is truncated and a summary note appended."""
        content = "x\n" * 6000
        result = _cap_content(content, 10_000)
        assert len(result) <= 10_000
        assert "summarized due to extensive artifacts" in result

    def test_truncates_at_line_boundary_when_newline_is_near(self) -> None:
        """Truncation snaps to the last newline when it is within 400 chars of the cut point."""
        note = "\n\n> **Note**: This spec was summarized due to extensive artifacts.\n"
        content = "line one\n" + "x" * 500 + "\n" + "x" * 300
        result = _cap_content(content, 700)
        raw_truncated = content[: 700 - len(note)]
        expected_prefix = raw_truncated[: raw_truncated.rfind("\n")]
        assert result == expected_prefix + note
        assert len(result) <= 700

    def test_truncates_without_newline_boundary_when_newline_is_far(self) -> None:
        """Falls back to hard truncation when the last newline is far from the cut point."""
        content = "header\n" + "x" * 12000
        result = _cap_content(content, 10_000)
        assert "summarized" in result
        assert len(result) <= 10_000

    def test_handles_very_small_limit_without_note(self) -> None:
        """Very small limit values safely truncate without appending the summary note."""
        assert _cap_content("abcdef", 3) == "abc"
