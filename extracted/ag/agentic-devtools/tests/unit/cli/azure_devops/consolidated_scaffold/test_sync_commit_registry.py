"""Tests for _sync_commit_registry."""

from agentic_devtools.cli.azure_devops.consolidated_scaffold import _sync_commit_registry
from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    FolderGroup,
    OverallSummary,
    ReviewState,
    ReviewStatus,
)

_COMMIT = "4a8685bda246f3bf826efabaf990fe9c3d1da125"


def _state(thread_id: int = 555, comment_id: int = 7, model: str | None = "claude-opus-4.6") -> ReviewState:
    fe = FileEntry(
        threadId=0,
        commentId=0,
        folder="src",
        fileName="a.py",
        status=ReviewStatus.APPROVED.value,
    )
    return ReviewState(
        prId=42,
        repoId="repo",
        repoName="repo",
        project="proj",
        organization="org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00Z",
        overallSummary=OverallSummary(threadId=thread_id, commentId=comment_id, status=ReviewStatus.APPROVED.value),
        folders={"src": FolderGroup(files=["/src/a.py"])},
        files={"/src/a.py": fe},
        commitHash=_COMMIT,
        modelId=model,
    )


class TestSyncCommitRegistry:
    """Mirrors the current commit's root thread into commitComments."""

    def test_creates_entry_with_model_ref(self):
        state = _state()
        _sync_commit_registry(state)
        entry = state.commitComments[_COMMIT]
        assert entry.threadId == 555
        assert entry.rootCommentId == 7
        assert entry.status == ReviewStatus.APPROVED.value
        ref = entry.get_model("claude-opus-4.6")
        assert ref is not None
        assert ref.commentId == 7

    def test_no_commit_hash_is_noop(self):
        state = _state()
        state.commitHash = ""
        _sync_commit_registry(state)
        assert state.commitComments == {}

    def test_updates_existing_entry(self):
        state = _state(thread_id=100, comment_id=1)
        _sync_commit_registry(state)
        state.overallSummary.commentId = 9
        _sync_commit_registry(state)
        entry = state.commitComments[_COMMIT]
        assert entry.rootCommentId == 9
        # No duplicate model refs created.
        assert len(entry.models) == 1

    def test_unknown_model_label(self):
        state = _state(model=None)
        _sync_commit_registry(state)
        entry = state.commitComments[_COMMIT]
        assert entry.get_model("unknown") is not None

    def test_second_model_does_not_claim_root_comment_id(self):
        # An entry whose first model already owns the root is synced for a
        # different (joining) model; the joining model must not take the root
        # comment id.
        from agentic_devtools.cli.azure_devops.review_state import CommitComment, ModelCommentRef

        state = _state(comment_id=7, model="second-model")
        state.commitComments[_COMMIT] = CommitComment(
            commitHash=_COMMIT,
            threadId=555,
            models=[ModelCommentRef(modelId="first-model", commentId=11)],
        )
        _sync_commit_registry(state)
        entry = state.commitComments[_COMMIT]
        assert entry.models[0].modelId == "first-model"
        assert entry.models[0].commentId == 11
        joining = entry.get_model("second-model")
        assert joining is not None
        assert joining.commentId == 0

    def test_model_ref_status_uses_overall_aggregate(self):
        state = _state()
        state.overallSummary.status = ReviewStatus.APPROVED.value
        state.files["/src/b.py"] = FileEntry(
            threadId=0,
            commentId=0,
            folder="src",
            fileName="b.py",
            status=ReviewStatus.NEEDS_WORK.value,
        )

        _sync_commit_registry(state)

        ref = state.commitComments[_COMMIT].get_model("claude-opus-4.6")
        assert ref is not None
        assert ref.status == ReviewStatus.NEEDS_WORK.value
