"""Tests for replacement_is_valid (FR-014, SC-007)."""

from agentic_devtools.orchestration.review.suggestion_syntax import replacement_is_valid

FILE = "def f():\n    x = 1\n    return x\n"


class TestReplacementIsValid:
    def test_valid_substitution(self):
        assert (
            replacement_is_valid(
                file_content=FILE,
                start_line=2,
                end_line=2,
                replacement_code="    x = 2",
                language="python",
            )
            is True
        )

    def test_invalid_substitution(self):
        assert (
            replacement_is_valid(
                file_content=FILE,
                start_line=2,
                end_line=2,
                replacement_code="    x = (",
                language="python",
            )
            is False
        )

    def test_unknown_language(self):
        assert (
            replacement_is_valid(
                file_content=FILE,
                start_line=1,
                end_line=1,
                replacement_code="x",
                language="cobol",
            )
            is False
        )

    def test_out_of_range_start(self):
        assert (
            replacement_is_valid(
                file_content=FILE,
                start_line=0,
                end_line=1,
                replacement_code="x = 1",
                language="python",
            )
            is False
        )

    def test_end_before_start(self):
        assert (
            replacement_is_valid(
                file_content=FILE,
                start_line=2,
                end_line=1,
                replacement_code="x = 1",
                language="python",
            )
            is False
        )

    def test_end_beyond_file(self):
        assert (
            replacement_is_valid(
                file_content=FILE,
                start_line=2,
                end_line=99,
                replacement_code="x = 1",
                language="python",
            )
            is False
        )

    def test_multi_line_replacement_in_context(self):
        assert (
            replacement_is_valid(
                file_content=FILE,
                start_line=2,
                end_line=3,
                replacement_code="    x = 2\n    return x + 1",
                language="python",
            )
            is True
        )

    def test_untrusted_parse_error_returns_false(self):
        # compile() raises SyntaxError (and may raise ValueError/RecursionError on
        # some inputs); all are caught so untrusted content never propagates.
        assert (
            replacement_is_valid(
                file_content=FILE,
                start_line=2,
                end_line=2,
                replacement_code="    x = '\x00'",
                language="python",
            )
            is False
        )

    def test_top_level_return_rejected(self):
        # ast.parse() accepts a top-level ``return`` (produces a valid AST node),
        # but compile(..., 'exec') raises SyntaxError, enforcing module-level
        # validity. This is the key difference between parse and compile.
        assert (
            replacement_is_valid(
                file_content="x = 1\n",
                start_line=1,
                end_line=1,
                replacement_code="return 42",
                language="python",
            )
            is False
        )

    def test_unicode_line_separator_in_replacement_preserves_syntax_error(self):
        assert (
            replacement_is_valid(
                file_content="x = 1\n",
                start_line=1,
                end_line=1,
                replacement_code="x = 1\u2028y = 2",
                language="python",
            )
            is False
        )

    def test_unicode_line_separator_in_file_content_does_not_split_line(self):
        assert (
            replacement_is_valid(
                file_content='value = "left\u2028right"\nresult = value\n',
                start_line=2,
                end_line=2,
                replacement_code="result = value.upper()",
                language="python",
            )
            is True
        )
