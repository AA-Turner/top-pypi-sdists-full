"""Tests for finding_in_diff (FR-004, SC-002)."""

from agentic_devtools.orchestration.review.line_reference import DiffLineIndex, build_diff_line_index, finding_in_diff
from agentic_devtools.orchestration.schemas.review.finding import FileReviewFinding

# context_before: old 10 / new 10; old_only removed: old 11;
# new_added_one/two: new 11/12; context_after: old 12 / new 13.
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


class TestFindingInDiff:
    def test_new_side_in_diff(self):
        index = build_diff_line_index(DIFF)
        finding = FileReviewFinding(severity="low", description="d", diff_side="new", new_line=11, confidence=0.8)
        assert finding_in_diff(finding, index) is True

    def test_new_side_out_of_diff(self):
        index = build_diff_line_index(DIFF)
        finding = FileReviewFinding(severity="low", description="d", diff_side="new", new_line=99, confidence=0.8)
        assert finding_in_diff(finding, index) is False

    def test_old_side_in_diff(self):
        index = build_diff_line_index(DIFF)
        finding = FileReviewFinding(severity="low", description="d", diff_side="old", old_line=11, confidence=0.8)
        assert finding_in_diff(finding, index) is True

    def test_old_side_out_of_diff(self):
        index = DiffLineIndex(old_lines=set(), new_lines={1})
        finding = FileReviewFinding(severity="low", description="d", diff_side="old", old_line=11, confidence=0.8)
        assert finding_in_diff(finding, index) is False

    def test_context_side_exact_pair_accepted(self):
        index = build_diff_line_index(DIFF)
        good = FileReviewFinding(
            severity="low", description="d", diff_side="context", old_line=10, new_line=10, confidence=0.8
        )
        assert finding_in_diff(good, index) is True

    def test_context_side_mismatched_coordinates_rejected(self):
        # old 10 and new 13 each exist in the index on their own side but
        # they belong to different unchanged rows — the pair (10, 13) must be rejected.
        index = build_diff_line_index(DIFF)
        bad = FileReviewFinding(
            severity="low", description="d", diff_side="context", old_line=10, new_line=13, confidence=0.8
        )
        assert finding_in_diff(bad, index) is False

    def test_context_side_out_of_diff(self):
        index = build_diff_line_index(DIFF)
        bad = FileReviewFinding(
            severity="low", description="d", diff_side="context", old_line=10, new_line=99, confidence=0.8
        )
        assert finding_in_diff(bad, index) is False
