"""Tests for _archive_commit_thread internal helper."""

from datetime import datetime, timezone

from agentic_devtools.cli.azure_devops.review_scaffold import _archive_commit_thread
from agentic_devtools.cli.azure_devops.review_state import (
    CommitComment,
    FileEntry,
    ModelCommentRef,
    OverallSummary,
    ReviewState,
    ReviewStatus,
)

_NOW = datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
_NOW_ISO = "2026-01-15T12:00:00+00:00"


def _make_state(commit_hash="old_hash", thread_id=500, comment_id=7, status="approved"):
    return ReviewState(
        prId=123,
        repoId="repo-guid",
        repoName="repo",
        project="Proj",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=thread_id, commentId=comment_id, status=status),
        files={
            "/src/a.ts": FileEntry(
                threadId=0,
                commentId=0,
                folder="src",
                fileName="a.ts",
                status=ReviewStatus.APPROVED.value,
            )
        },
        commitHash=commit_hash,
        modelId="claude-opus-4.6",
    )


class TestArchiveCommitThread:
    """Tests for _archive_commit_thread."""

    def test_records_prior_commit_in_registry(self):
        """The old commit's thread/comment is recorded in commitComments."""
        state = _make_state()
        _archive_commit_thread(state, "old_hash", now=_NOW)

        assert "old_hash" in state.commitComments
        entry = state.commitComments["old_hash"]
        assert entry.threadId == 500
        assert entry.rootCommentId == 7
        assert entry.status == "approved"
        assert entry.models[0].modelId == "claude-opus-4.6"

    def test_sets_entry_timestamp(self):
        """The archived commit entry's timestamp is set from the now argument."""
        state = _make_state()
        _archive_commit_thread(state, "old_hash", now=_NOW)

        entry = state.commitComments["old_hash"]
        assert entry.timestamp == _NOW_ISO

    def test_sets_model_ref_timestamp(self):
        """The archived model ref's timestamp is set from the now argument."""
        state = _make_state()
        _archive_commit_thread(state, "old_hash", now=_NOW)

        ref = state.commitComments["old_hash"].models[0]
        assert ref.timestamp == _NOW_ISO

    def test_resets_overall_summary_pointer(self):
        """overallSummary is reset so the next upsert POSTs a new thread."""
        state = _make_state()
        _archive_commit_thread(state, "old_hash", now=_NOW)

        assert state.overallSummary.threadId == 0
        assert state.overallSummary.commentId == 0
        assert state.overallSummary.status == ReviewStatus.IN_PROGRESS.value

    def test_reuses_existing_registry_entry(self):
        """An existing commitComments entry for the old hash is updated in place."""
        state = _make_state()
        # Pre-seed a registry entry (e.g. from initial scaffold).
        _archive_commit_thread(state, "old_hash", now=_NOW)
        first_entry = state.commitComments["old_hash"]

        # Simulate the pointer being repopulated then archived again (idempotent).
        state.overallSummary.threadId = 500
        state.overallSummary.commentId = 7
        _archive_commit_thread(state, "old_hash", now=_NOW)

        assert state.commitComments["old_hash"] is first_entry
        assert len(first_entry.models) == 1

    def test_no_thread_id_still_creates_entry_without_overwriting(self):
        """When overallSummary has no thread, the registry entry is created but not populated."""
        state = _make_state(thread_id=0, comment_id=0)
        _archive_commit_thread(state, "old_hash", now=_NOW)

        assert "old_hash" in state.commitComments
        entry = state.commitComments["old_hash"]
        assert entry.threadId == 0
        # No thread to archive → timestamp should not be set
        assert entry.timestamp is None

    def test_second_model_does_not_overwrite_root_comment_id(self):
        """A joining model's ref does not claim the thread root comment id."""
        state = _make_state()
        state.modelId = "gpt-5"
        # Pre-seed the registry entry whose first (root-owning) model differs
        # from the model archiving now.
        entry = CommitComment(
            commitHash="old_hash",
            threadId=500,
            models=[ModelCommentRef(modelId="claude-opus-4.6", commentId=11)],
        )
        state.commitComments["old_hash"] = entry

        _archive_commit_thread(state, "old_hash", now=_NOW)

        # The new model's ref was appended; the root comment id stays with the
        # first model and the joining model's commentId is left untouched.
        assert entry.models[0].modelId == "claude-opus-4.6"
        assert entry.models[0].commentId == 11
        assert entry.rootCommentId == 11
        joining = entry.get_model("gpt-5")
        assert joining is not None
        assert joining.commentId == 0
        assert joining.timestamp == _NOW_ISO

    def test_timestamps_default_to_utc_now_when_not_provided(self):
        """When now is omitted, timestamps are set to a non-None UTC string."""
        state = _make_state()
        _archive_commit_thread(state, "old_hash")

        entry = state.commitComments["old_hash"]
        assert entry.timestamp is not None
        assert entry.timestamp.endswith("+00:00") or entry.timestamp.endswith("Z")
        assert entry.models[0].timestamp is not None

    def test_archived_model_ref_status_uses_overall_aggregate(self):
        state = _make_state(status=ReviewStatus.APPROVED.value)
        state.files["/src/b.ts"] = FileEntry(
            threadId=0,
            commentId=0,
            folder="src",
            fileName="b.ts",
            status=ReviewStatus.IN_PROGRESS.value,
        )

        _archive_commit_thread(state, "old_hash", now=_NOW)

        ref = state.commitComments["old_hash"].get_model("claude-opus-4.6")
        assert ref is not None
        assert ref.status == ReviewStatus.IN_PROGRESS.value
