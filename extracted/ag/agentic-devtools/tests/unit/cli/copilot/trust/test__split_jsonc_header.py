"""Tests for _split_jsonc_header."""

from agentic_devtools.cli.copilot.trust import _split_jsonc_header


class TestSplitJsoncHeader:
    """Tests for _split_jsonc_header."""

    def test_splits_leading_comments(self):
        """Leading // comment lines are peeled into the header."""
        raw = '// a\n// b\n{\n  "k": 1\n}\n'
        header, body = _split_jsonc_header(raw)
        assert header == "// a\n// b\n"
        assert body == '{\n  "k": 1\n}\n'

    def test_no_header(self):
        """Plain JSON yields an empty header and the original body."""
        raw = '{"k": 1}'
        header, body = _split_jsonc_header(raw)
        assert header == ""
        assert body == raw

    def test_blank_lines_included_in_header(self):
        """Leading blank lines and comments are both captured."""
        raw = "\n// c\n\n{}"
        header, body = _split_jsonc_header(raw)
        assert header == "\n// c\n\n"
        assert body == "{}"

    def test_splits_crlf_leading_comments(self):
        """Leading CRLF comment/header lines are peeled into the header."""
        raw = '\r\n// a\r\n\r\n// b\r\n{\r\n  "k": 1\r\n}\r\n'
        header, body = _split_jsonc_header(raw)
        assert header == "\r\n// a\r\n\r\n// b\r\n"
        assert body == '{\r\n  "k": 1\r\n}\r\n'
