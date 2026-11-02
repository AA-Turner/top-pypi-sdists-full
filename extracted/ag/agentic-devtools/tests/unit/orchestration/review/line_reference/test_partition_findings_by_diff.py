"""Tests for partition_findings_by_diff (FR-004, SC-002)."""

from agentic_devtools.orchestration.review.line_reference import partition_findings_by_diff
from agentic_devtools.orchestration.schemas.review.finding import FileReviewFinding

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


class TestPartitionFindingsByDiff:
    def test_splits_kept_and_dropped(self):
        kept_finding = FileReviewFinding(severity="low", description="in", diff_side="new", new_line=11, confidence=0.8)
        dropped_finding = FileReviewFinding(
            severity="low", description="out", diff_side="new", new_line=500, confidence=0.8
        )
        kept, dropped = partition_findings_by_diff([kept_finding, dropped_finding], DIFF)
        assert kept == [kept_finding]
        assert dropped == [dropped_finding]
