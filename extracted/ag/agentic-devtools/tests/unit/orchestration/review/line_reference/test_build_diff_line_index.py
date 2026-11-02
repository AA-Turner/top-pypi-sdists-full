"""Tests for build_diff_line_index (FR-004, SC-002)."""

from agentic_devtools.orchestration.review.line_reference import build_diff_line_index

DIFF = """\
--- a/f.py
+++ b/f.py
@@ -10,3 +10,4 @@ def f():
 context_before
-old_only
+new_added_one
+new_added_two
 context_after
"""


class TestBuildDiffLineIndex:
    def test_parses_added_removed_context(self):
        index = build_diff_line_index(DIFF)
        # context_before: old 10 / new 10
        assert 10 in index.old_lines
        assert 10 in index.new_lines
        # old_only removed -> old 11
        assert 11 in index.old_lines
        # new_added_one/two -> new 11, 12
        assert 11 in index.new_lines
        assert 12 in index.new_lines
        # context_after: old 12 / new 13
        assert 12 in index.old_lines
        assert 13 in index.new_lines

    def test_context_pairs_are_recorded(self):
        index = build_diff_line_index(DIFF)
        assert (10, 10) in index.context_pairs
        assert (12, 13) in index.context_pairs
        # added/removed lines must NOT appear as context pairs
        assert (11, 11) not in index.context_pairs

    def test_ignores_content_before_first_hunk(self):
        index = build_diff_line_index("--- a/f\n+++ b/f\nrandom\n")
        assert index.old_lines == set()
        assert index.new_lines == set()

    def test_ignores_no_newline_marker(self):
        diff = "@@ -1 +1 @@\n-old\n+new\n\\ No newline at end of file\n"
        index = build_diff_line_index(diff)
        assert index.old_lines == {1}
        assert index.new_lines == {1}

    def test_hunk_without_counts(self):
        index = build_diff_line_index("@@ -5 +7 @@\n+added\n")
        assert index.new_lines == {7}

    def test_empty_diff(self):
        index = build_diff_line_index("")
        assert index.old_lines == set()
        assert index.new_lines == set()
        assert index.context_pairs == set()

    def test_hunk_without_trailing_newline(self):
        index = build_diff_line_index("@@ -5 +7 @@\n+added")
        assert index.new_lines == {7}

    def test_truncation_marker_terminates_hunk(self):
        # A budget-truncation marker must not be treated as a context line; the
        # hunk must be closed so that subsequent lines are not indexed.
        diff = "@@ -1,3 +1,3 @@\n context\n[... diff truncated — budget exceeded ...]\n after_truncation\n"
        index = build_diff_line_index(diff)
        # Only the context line before the marker should have been indexed.
        assert 1 in index.old_lines
        assert 1 in index.new_lines
        # Lines after the truncation marker must NOT be indexed.
        assert 2 not in index.old_lines
        assert 2 not in index.new_lines

    def test_unknown_line_in_hunk_terminates_subsequent_indexing(self):
        # Any unrecognized line other than +/-/space/backslash must close the
        # hunk so that real content after it cannot gain false coordinates.
        diff = "@@ -1,2 +1,2 @@\n+added\nUNKNOWN_MARKER\n context\n"
        index = build_diff_line_index(diff)
        assert index.new_lines == {1}
        # The context line following UNKNOWN_MARKER must not be indexed.
        assert 2 not in index.old_lines
        assert 2 not in index.new_lines

    def test_unicode_line_separator_inside_diff_line_does_not_end_hunk(self):
        diff = "@@ -1,2 +1,2 @@\n context\u2028still_same_line\n+added_after_unicode_separator\n"
        index = build_diff_line_index(diff)
        assert index.old_lines == {1}
        assert index.new_lines == {1, 2}
        assert (1, 1) in index.context_pairs
