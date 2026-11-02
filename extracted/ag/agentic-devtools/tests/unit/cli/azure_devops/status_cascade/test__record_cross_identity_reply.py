"""Tests for _record_cross_identity_reply."""

from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    FolderGroup,
    OverallSummary,
    ReviewState,
    ReviewStatus,
)
from agentic_devtools.cli.azure_devops.status_cascade import (
    CascadeResult,
    PatchOperation,
    _record_cross_identity_reply,
)


def _state(thread_id: int, comment_id: int) -> ReviewState:
    fe = FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status=ReviewStatus.APPROVED.value)
    return ReviewState(
        prId=42,
        repoId="repo-guid",
        repoName="repo",
        project="proj",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00Z",
        overallSummary=OverallSummary(threadId=thread_id, commentId=comment_id),
        folders={"src": FolderGroup(files=["/src/a.py"])},
        files={"/src/a.py": fe},
        commitHash="4a8685bda246f3bf826efabaf990fe9c3d1da125",
        modelId="claude-opus-4.6",
    )


def _op(thread_id: int = 10, comment_id: int = 20) -> PatchOperation:
    return PatchOperation(thread_id=thread_id, comment_id=comment_id, new_content="x", thread_status="active")


class TestRecordCrossIdentityReply:
    """Branch coverage for the cross-identity reply id feedback helper."""

    def test_empty_reply_result_is_noop(self):
        """A falsy reply_result ({}) records nothing and leaves state untouched."""
        result = CascadeResult()
        state = _state(thread_id=10, comment_id=20)

        _record_cross_identity_reply(_op(10, 20), {}, result, state)

        assert result.reply_comment_ids == {}
        assert state.overallSummary.commentId == 20

    def test_missing_id_is_noop(self):
        """A reply_result without an 'id' key records nothing."""
        result = CascadeResult()
        state = _state(10, 20)

        _record_cross_identity_reply(_op(10, 20), {"content": "no id"}, result, state)

        assert result.reply_comment_ids == {}
        assert state.overallSummary.commentId == 20

    def test_none_id_is_noop(self):
        """An explicit None id records nothing."""
        result = CascadeResult()
        state = _state(10, 20)

        _record_cross_identity_reply(_op(10, 20), {"id": None}, result, state)

        assert result.reply_comment_ids == {}
        assert state.overallSummary.commentId == 20

    def test_non_numeric_id_is_noop(self):
        """A non-numeric id is ignored (ValueError swallowed)."""
        result = CascadeResult()
        state = _state(10, 20)

        _record_cross_identity_reply(_op(10, 20), {"id": "not-a-number"}, result, state)

        assert result.reply_comment_ids == {}
        assert state.overallSummary.commentId == 20

    def test_non_coercible_id_is_noop(self):
        """A non-coercible id (list) is ignored (TypeError swallowed)."""
        result = CascadeResult()
        state = _state(10, 20)

        _record_cross_identity_reply(_op(10, 20), {"id": [1, 2]}, result, state)

        assert result.reply_comment_ids == {}
        assert state.overallSummary.commentId == 20

    def test_records_id_without_state(self):
        """With state=None the id is still recorded in the result."""
        result = CascadeResult()

        _record_cross_identity_reply(_op(10, 20), {"id": 999}, result, None)

        assert result.reply_comment_ids == {10: 999}

    def test_matching_op_updates_state(self):
        """When the op targets overallSummary, its comment id is re-targeted."""
        result = CascadeResult()
        state = _state(thread_id=10, comment_id=20)

        _record_cross_identity_reply(_op(10, 20), {"id": 999}, result, state)

        assert result.reply_comment_ids == {10: 999}
        assert state.overallSummary.commentId == 999

    def test_numeric_string_id_is_coerced(self):
        """A numeric string id is coerced to int before being applied."""
        result = CascadeResult()
        state = _state(thread_id=10, comment_id=20)

        _record_cross_identity_reply(_op(10, 20), {"id": "999"}, result, state)

        assert result.reply_comment_ids == {10: 999}
        assert state.overallSummary.commentId == 999

    def test_non_matching_thread_does_not_update_state(self):
        """An op on a different thread records the id but does not touch state."""
        result = CascadeResult()
        state = _state(thread_id=10, comment_id=20)

        _record_cross_identity_reply(_op(99, 20), {"id": 999}, result, state)

        assert result.reply_comment_ids == {99: 999}
        assert state.overallSummary.commentId == 20

    def test_non_matching_comment_does_not_update_state(self):
        """An op whose comment id differs from overallSummary leaves state untouched."""
        result = CascadeResult()
        state = _state(thread_id=10, comment_id=20)

        _record_cross_identity_reply(_op(10, 77), {"id": 999}, result, state)

        assert result.reply_comment_ids == {10: 999}
        assert state.overallSummary.commentId == 20

    def test_same_id_does_not_rewrite_state(self):
        """When the new id equals the current comment id, no rewrite occurs."""
        result = CascadeResult()
        state = _state(thread_id=10, comment_id=999)

        _record_cross_identity_reply(_op(10, 999), {"id": 999}, result, state)

        assert result.reply_comment_ids == {10: 999}
        assert state.overallSummary.commentId == 999
