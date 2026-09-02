"""Tests for ``escape_marker_tokens``."""

from agentic_devtools.cli.speckit.scaffold_update_agent_context import (
    SPECKIT_END_MARKER,
    SPECKIT_START_MARKER,
    escape_marker_tokens,
)


class TestEscapeMarkerTokens:
    """escape_marker_tokens replaces literal marker tokens with HTML-escaped equivalents."""

    def test_passthrough_for_plain_string(self) -> None:
        assert escape_marker_tokens("hello world") == "hello world"

    def test_escapes_start_marker(self) -> None:
        result = escape_marker_tokens(SPECKIT_START_MARKER)

        assert SPECKIT_START_MARKER not in result
        assert "&lt;" in result

    def test_escapes_end_marker(self) -> None:
        result = escape_marker_tokens(SPECKIT_END_MARKER)

        assert SPECKIT_END_MARKER not in result
        assert "&lt;" in result

    def test_escapes_both_markers_in_same_value(self) -> None:
        value = f"prefix {SPECKIT_START_MARKER} middle {SPECKIT_END_MARKER} suffix"

        result = escape_marker_tokens(value)

        assert SPECKIT_START_MARKER not in result
        assert SPECKIT_END_MARKER not in result
        assert "prefix" in result
        assert "middle" in result
        assert "suffix" in result

    def test_empty_string(self) -> None:
        assert escape_marker_tokens("") == ""
