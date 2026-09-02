"""Tests for _reset_files_for_rereview."""

from agentic_devtools.cli.azure_devops.review_scaffold import _reset_files_for_rereview
from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    OverallSummary,
    ReviewState,
    ReviewStatus,
    SuggestionEntry,
)


def _suggestion(thread_id: int = 1) -> SuggestionEntry:
    return SuggestionEntry(
        threadId=thread_id,
        commentId=1,
        line=1,
        endLine=1,
        severity="high",
        outOfScope=False,
        linkText="line 1",
        content="fix",
    )


def _state(fe: FileEntry) -> ReviewState:
    return ReviewState(
        prId=42,
        repoId="repo",
        repoName="repo",
        project="proj",
        organization="org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00Z",
        overallSummary=OverallSummary(threadId=1, commentId=1),
        folders={},
        files={"/src/a.py": fe},
        commitHash="abc123",
    )


class TestResetFilesForRereview:
    """Resetting file state for a forced re-review."""

    def test_resets_status_summary_and_attribution(self):
        fe = FileEntry(
            threadId=1,
            commentId=1,
            folder="src",
            fileName="a.py",
            status=ReviewStatus.APPROVED.value,
            summary="LGTM",
            modelId="old-model",
            providerType="openai_direct",
            latencyMs=123,
            finishReason="stop",
            tokensUsed=42,
        )
        state = _state(fe)
        _reset_files_for_rereview(state, "m")
        assert fe.status == ReviewStatus.UNREVIEWED.value
        assert fe.summary is None
        assert fe.modelId is None
        assert fe.providerType is None
        assert fe.latencyMs is None
        assert fe.finishReason is None
        assert fe.tokensUsed is None

    def test_rotates_suggestions_to_previous(self):
        fe = FileEntry(
            threadId=1,
            commentId=1,
            folder="src",
            fileName="a.py",
            status=ReviewStatus.NEEDS_WORK.value,
            suggestions=[_suggestion(10)],
        )
        state = _state(fe)
        _reset_files_for_rereview(state, "m")
        assert fe.suggestions == []
        assert fe.previousSuggestions is not None
        assert len(fe.previousSuggestions) == 1

    def test_rotation_extends_existing_previous(self):
        fe = FileEntry(
            threadId=1,
            commentId=1,
            folder="src",
            fileName="a.py",
            status=ReviewStatus.NEEDS_WORK.value,
            suggestions=[_suggestion(20)],
            previousSuggestions=[_suggestion(10)],
        )
        state = _state(fe)
        _reset_files_for_rereview(state, "m")
        assert len(fe.previousSuggestions) == 2
        assert fe.suggestions == []

    def test_no_rotation_when_previous_set_and_no_current_suggestions(self):
        fe = FileEntry(
            threadId=1,
            commentId=1,
            folder="src",
            fileName="a.py",
            status=ReviewStatus.NEEDS_WORK.value,
            suggestions=[],
            previousSuggestions=[_suggestion(10)],
        )
        state = _state(fe)
        _reset_files_for_rereview(state, "m")
        assert len(fe.previousSuggestions) == 1
        assert fe.suggestions == []

    def test_resets_overall_summary_status_to_in_progress(self):
        """overallSummary.status must be reset so archived commits record the correct status."""
        fe = FileEntry(
            threadId=1,
            commentId=1,
            folder="src",
            fileName="a.py",
            status=ReviewStatus.APPROVED.value,
            summary="LGTM",
        )
        state = _state(fe)
        state.overallSummary.status = ReviewStatus.APPROVED.value
        _reset_files_for_rereview(state, "m")
        assert state.overallSummary.status == ReviewStatus.IN_PROGRESS.value

    def test_resets_overall_summary_status_from_needs_work(self):
        """overallSummary.status needs-work is also corrected to in-progress."""
        fe = FileEntry(
            threadId=1,
            commentId=1,
            folder="src",
            fileName="a.py",
            status=ReviewStatus.NEEDS_WORK.value,
            summary="Issues found",
        )
        state = _state(fe)
        state.overallSummary.status = ReviewStatus.NEEDS_WORK.value
        _reset_files_for_rereview(state, "m")
        assert state.overallSummary.status == ReviewStatus.IN_PROGRESS.value
