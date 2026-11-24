"""Tests for various per-block parsers."""

from matrx_ai.processing.blocks.parsers.table_parser import parse_table
from matrx_ai.processing.blocks.parsers.diff_parser import looks_like_diff, detect_diff_style


class TestTableParser:
    def test_basic_table(self):
        content = "| A | B |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |"
        # is_final=True: complete block (streaming withholds the last row until finalize).
        result = parse_table(content, is_final=True)
        assert result is not None
        assert result.headers == ["A", "B"]
        assert len(result.rows) == 2
        assert result.rows[0] == ["1", "2"]

    def test_single_column(self):
        content = "| Name |\n|------|\n| Alice |"
        result = parse_table(content)
        assert result is not None
        assert result.headers == ["Name"]

    def test_invalid_table(self):
        result = parse_table("Not a table")
        assert result is None

    def test_too_few_lines(self):
        result = parse_table("| A |")
        assert result is None


class TestDiffParser:
    def test_search_replace_detection(self):
        content = "<<<<<<< SEARCH\nold code\n=======\nnew code\n>>>>>>> REPLACE"
        assert looks_like_diff(content) is True
        assert detect_diff_style(content) == "search_replace"

    def test_unified_diff_detection(self):
        content = "--- a/file.py\n+++ b/file.py\n@@ -1,3 +1,3 @@"
        assert looks_like_diff(content) is True
        assert detect_diff_style(content) == "unified"

    def test_no_diff(self):
        assert looks_like_diff("regular code") is False
