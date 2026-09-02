"""Tests for JSONC comment stripping."""

import json

from agentic_devtools.cli.workflows.worktree_setup import _strip_jsonc_comments


class TestStripJsoncComments:
    """Tests for _strip_jsonc_comments function."""

    def test_strips_single_line_comments(self) -> None:
        """Single-line comments are stripped."""
        text = '{"key": "value"} // This is a comment\n'
        assert _strip_jsonc_comments(text) == '{"key": "value"} \n'

    def test_strips_multi_line_comments(self) -> None:
        """Multi-line comments are stripped."""
        text = '{"key": "value"} /* This is a comment */\n'
        assert _strip_jsonc_comments(text) == '{"key": "value"} \n'

    def test_preserves_strings_with_comment_syntax(self) -> None:
        """Strings containing comment syntax are not stripped."""
        text = '{"url": "http://example.com/path", "regex": "/* pattern */"}'
        assert _strip_jsonc_comments(text) == '{"url": "http://example.com/path", "regex": "/* pattern */"}'

    def test_strips_comments_and_preserves_strings(self) -> None:
        """Combination of strings and comments."""
        text = """{
            // comment 1
            "url": "http://example.com", /* comment 2 */
            "key": "value" // comment 3
        }"""
        stripped = _strip_jsonc_comments(text)
        assert json.loads(stripped) == {"url": "http://example.com", "key": "value"}

    def test_preserves_escaped_quotes(self) -> None:
        """Strings with escaped quotes are handled correctly."""
        text = '{"key": "value \\"with quotes\\""} // comment'
        assert _strip_jsonc_comments(text) == '{"key": "value \\"with quotes\\""} '

    def test_strips_trailing_comma_before_close_brace(self) -> None:
        """Trailing commas before } are removed."""
        text = '{"key": "value",}'
        assert json.loads(_strip_jsonc_comments(text)) == {"key": "value"}

    def test_strips_trailing_comma_before_close_bracket(self) -> None:
        """Trailing commas before ] are removed."""
        text = '{"items": [1, 2, 3,]}'
        assert json.loads(_strip_jsonc_comments(text)) == {"items": [1, 2, 3]}

    def test_strips_trailing_commas_and_comments_combined(self) -> None:
        """Trailing commas and comments in the same document are both removed."""
        text = """{
            // comment
            "key": "value", /* inline */
            "nested": {"a": 1,},
        }"""
        assert json.loads(_strip_jsonc_comments(text)) == {"key": "value", "nested": {"a": 1}}

    def test_preserves_comma_inside_string(self) -> None:
        """A comma followed by } inside a string value is not stripped."""
        text = '{"key": "a,}"}'
        assert json.loads(_strip_jsonc_comments(text)) == {"key": "a,}"}
