"""Tests for parse_env_file's inline-comment handling.

The regression: every line in `.env` like `PORT=8090   # local` was being
loaded with value `'8090   # local'`, breaking pydantic-settings parsing
and poisoning test runs.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from sage.core.credentials import parse_env_file


@pytest.fixture
def env_file(tmp_path):
    def _make(content: str) -> Path:
        p = tmp_path / ".env"
        p.write_text(content, encoding="utf-8")
        return p
    return _make


class TestInlineCommentStripping:

    def test_strips_trailing_comment_with_whitespace(self, env_file):
        path = env_file("AI_PLATFORM_PORT=8090   # local\n")
        values = parse_env_file(path)
        assert values["AI_PLATFORM_PORT"] == "8090"

    def test_strips_trailing_comment_with_lots_of_whitespace(self, env_file):
        path = env_file("PATH_VAR=value           # an explanation\n")
        values = parse_env_file(path)
        assert values["PATH_VAR"] == "value"

    def test_preserves_hash_without_leading_space(self, env_file):
        """A `#` in the middle of a value (no leading whitespace) is part of
        the value, not a comment delimiter — common in passwords/tokens."""
        path = env_file("PASSWORD=ab#cd1234\n")
        values = parse_env_file(path)
        assert values["PASSWORD"] == "ab#cd1234"

    def test_preserves_hash_inside_quoted_value(self, env_file):
        path = env_file('NOTE="this has # in it"\n')
        values = parse_env_file(path)
        assert values["NOTE"] == "this has # in it"

    def test_full_line_comments_still_skipped(self, env_file):
        path = env_file(
            "# This whole line is a comment\n"
            "KEY=value\n"
            "  # Indented comment\n"
        )
        values = parse_env_file(path)
        assert values == {"KEY": "value"}

    def test_export_prefix_still_handled(self, env_file):
        path = env_file("export PORT=8090   # comment\n")
        values = parse_env_file(path)
        assert values["PORT"] == "8090"

    def test_url_with_hash_fragment_in_quotes(self, env_file):
        """URLs with #fragment must survive when quoted."""
        path = env_file("CALLBACK_URL='https://example.com/cb#step2'\n")
        values = parse_env_file(path)
        assert values["CALLBACK_URL"] == "https://example.com/cb#step2"

    def test_actual_ai_platform_env_line(self, env_file):
        """The exact line that triggered the bug."""
        path = env_file(
            "AI_PLATFORM_PORT=8090                                                     # local\n"
        )
        values = parse_env_file(path)
        assert values["AI_PLATFORM_PORT"] == "8090"
