"""Tests for _escape_comment_metadata_text()."""

import pytest

from agentic_devtools.cli.ci.github_provider import _escape_comment_metadata_text


class TestEscapeCommentMetadataText:
    """Tests for the single-line metadata escape function."""

    def test_empty_string_returns_empty(self) -> None:
        assert _escape_comment_metadata_text("") == ""

    def test_plain_text_is_unchanged(self) -> None:
        assert _escape_comment_metadata_text("src/foo.py") == "src/foo.py"

    def test_backslash_is_doubled(self) -> None:
        assert _escape_comment_metadata_text("\\") == "\\\\"

    def test_newline_is_escaped(self) -> None:
        assert _escape_comment_metadata_text("\n") == "\\n"

    def test_carriage_return_is_escaped(self) -> None:
        assert _escape_comment_metadata_text("\r") == "\\r"

    def test_tab_is_escaped(self) -> None:
        assert _escape_comment_metadata_text("\t") == "\\t"

    def test_less_than_is_unicode_escaped(self) -> None:
        assert _escape_comment_metadata_text("<") == "\\u003c"

    def test_greater_than_is_unicode_escaped(self) -> None:
        assert _escape_comment_metadata_text(">") == "\\u003e"

    def test_control_character_below_0x20_is_unicode_escaped(self) -> None:
        assert _escape_comment_metadata_text("\x07") == "\\u0007"

    def test_del_0x7f_is_unicode_escaped(self) -> None:
        assert _escape_comment_metadata_text("\x7f") == "\\u007f"

    def test_non_ascii_printable_is_unchanged(self) -> None:
        assert _escape_comment_metadata_text("é") == "é"

    def test_forged_section_marker_in_path_is_fully_escaped(self) -> None:
        raw = "src\\dir/\r\n<!-- repair-section:code-review-agent-comments -->\t<foo>.py"
        result = _escape_comment_metadata_text(raw)
        expected = (
            "src\\\\dir/\\r\\n\\u003c!-- repair-section:code-review-agent-comments --\\u003e\\t\\u003cfoo\\u003e.py"
        )
        assert result == expected

    @pytest.mark.parametrize("char", [chr(c) for c in range(0x01, 0x20) if chr(c) not in "\n\r\t"])
    def test_all_other_c0_control_chars_are_unicode_escaped(self, char: str) -> None:
        result = _escape_comment_metadata_text(char)
        assert result == f"\\u{ord(char):04x}"
