"""Tests for find_continuation_comment_ids."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    CONSOLIDATED_MARKER_VERSION,
    CONTINUATION_MARKER_TYPE,
    build_continuation_marker,
)
from agentic_devtools.cli.azure_devops.consolidated_scaffold import find_continuation_comment_ids


def _continuation(comment_id: int, seq: int, deleted: bool = False) -> dict:
    return {
        "id": comment_id,
        "isDeleted": deleted,
        "content": build_continuation_marker(42, "a" * 40, seq) + "\n### 🔁 Review (continued)",
    }


def _continuation_no_seq(comment_id: int, deleted: bool = False) -> dict:
    """A v2 continuation comment whose marker has no seq: field (edge case)."""
    marker = f"<!-- agdt-review:v{CONSOLIDATED_MARKER_VERSION} type:{CONTINUATION_MARKER_TYPE} pr:42 -->"
    return {
        "id": comment_id,
        "isDeleted": deleted,
        "content": marker + "\n### 🔁 Review (continued)",
    }


class TestFindContinuationCommentIds:
    """Recovery of continuation reply ids from a thread dict."""

    def test_empty_when_no_continuations(self):
        thread = {"comments": [{"id": 1, "content": "root with no marker"}]}
        assert find_continuation_comment_ids(thread) == []

    def test_returns_ids_in_order(self):
        thread = {"comments": [{"id": 1, "content": "root"}, _continuation(2, 1), _continuation(3, 2)]}
        assert find_continuation_comment_ids(thread) == [2, 3]

    def test_skips_deleted(self):
        thread = {"comments": [_continuation(2, 1, deleted=True), _continuation(3, 2)]}
        assert find_continuation_comment_ids(thread) == [3]

    def test_handles_missing_comments_key(self):
        assert find_continuation_comment_ids({}) == []

    def test_deduplicates_same_seq_keeps_highest_id(self):
        """When two non-deleted comments share the same seq (cross-identity 403
        fallback), only the one with the highest comment id is returned."""
        # seq=1 appears twice: original id=2, fallback reply id=5
        thread = {
            "comments": [
                {"id": 1, "content": "root"},
                _continuation(2, 1),  # original seq=1
                _continuation(3, 2),  # seq=2
                _continuation(5, 1),  # fallback reply for seq=1 (higher id)
            ]
        }
        assert find_continuation_comment_ids(thread) == [5, 3]

    def test_deduplicates_out_of_api_order(self):
        """De-dup and sort works even when the API returns comments out of seq
        order (e.g. seq=2 before seq=1 in the raw list)."""
        thread = {
            "comments": [
                _continuation(10, 2),
                _continuation(7, 1),
                _continuation(11, 2),  # duplicate seq=2, higher id wins
            ]
        }
        # Expected: seq=1 → id=7, seq=2 → id=11, sorted ascending
        assert find_continuation_comment_ids(thread) == [7, 11]

    def test_deleted_duplicate_not_considered_for_dedup(self):
        """A deleted comment with the same seq should be skipped entirely."""
        thread = {
            "comments": [
                _continuation(2, 1),
                _continuation(5, 1, deleted=True),  # deleted — ignored
            ]
        }
        assert find_continuation_comment_ids(thread) == [2]

    def test_deduplicates_same_seq_lower_id_seen_after_higher(self):
        """When the lower-id duplicate for a seq slot appears AFTER the higher-id
        one (reversed API order), the higher id is still kept."""
        thread = {
            "comments": [
                _continuation(5, 1),  # higher id seen first
                _continuation(2, 1),  # lower id seen second — should be ignored
            ]
        }
        assert find_continuation_comment_ids(thread) == [5]

    def test_unsequenced_comment_appended_after_sequenced(self):
        """A v2 continuation comment missing a seq: field is treated as
        unsequenced and appended after all sequenced entries."""
        thread = {
            "comments": [
                _continuation(2, 1),
                _continuation_no_seq(99),  # valid continuation marker, no seq
                _continuation(3, 2),
            ]
        }
        # seq=1→id=2, seq=2→id=3 come first; unsequenced id=99 appended last
        assert find_continuation_comment_ids(thread) == [2, 3, 99]
