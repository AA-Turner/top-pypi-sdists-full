"""Tests for _json_escape in retro_spec/synthesis.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.retro_spec.synthesis import _json_escape


class TestJsonEscape:
    """Tests for the _json_escape function."""

    def test_escapes_quotes_and_newlines_for_json_embedding(self) -> None:
        """Test that text is JSON-escaped via json.dumps."""
        assert _json_escape('line "one"\nline two') == '"line \\"one\\"\\nline two"'
