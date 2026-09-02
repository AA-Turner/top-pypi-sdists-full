"""Tests for sanitize_control_characters in speckit/phase0/observability.py (FR-012a)."""

from __future__ import annotations

from agentic_devtools.cli.speckit.phase0.observability import sanitize_control_characters


class TestSanitizeControlCharacters:
    """Tests for the sanitize_control_characters function."""

    def test_replaces_newline(self) -> None:
        assert sanitize_control_characters("line1\nline2") == "line1\ufffdline2"

    def test_replaces_null_byte(self) -> None:
        assert sanitize_control_characters("a\x00b") == "a\ufffdb"

    def test_replaces_del_character(self) -> None:
        assert sanitize_control_characters("a\x7fb") == "a\ufffdb"

    def test_replaces_unicode_line_separators(self) -> None:
        assert sanitize_control_characters("a\u2028b\u2029c\u0085d") == "a\ufffdb\ufffdc\ufffdd"

    def test_leaves_normal_text_unchanged(self) -> None:
        assert sanitize_control_characters("hello world") == "hello world"

    def test_leaves_unicode_text_unchanged(self) -> None:
        assert sanitize_control_characters("caf\u00e9") == "caf\u00e9"
