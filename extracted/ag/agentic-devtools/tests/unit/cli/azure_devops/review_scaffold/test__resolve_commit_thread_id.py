"""Tests for _resolve_commit_thread_id."""

from agentic_devtools.cli.azure_devops.review_scaffold import _resolve_commit_thread_id
from agentic_devtools.cli.azure_devops.review_state import (
    CommitComment,
    ModelCommentRef,
    OverallSummary,
    ReviewState,
)


def _state(commit_comments=None, overall_thread=500) -> ReviewState:
    return ReviewState(
        prId=42,
        repoId="repo",
        repoName="repo",
        project="proj",
        organization="org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00Z",
        overallSummary=OverallSummary(threadId=overall_thread, commentId=1),
        folders={},
        files={},
        commitHash="abc123",
        commitComments=commit_comments or {},
    )


class TestResolveCommitThreadId:
    """Resolution of a commit's review thread id."""

    def test_prefers_registry_entry(self):
        cc = CommitComment(commitHash="abc123", threadId=777, models=[ModelCommentRef(modelId="m", commentId=1)])
        state = _state(commit_comments={"abc123": cc})
        assert _resolve_commit_thread_id(state, "abc123") == 777

    def test_falls_back_to_overall_summary(self):
        state = _state()
        assert _resolve_commit_thread_id(state, "abc123") == 500

    def test_falls_back_when_registry_thread_zero(self):
        cc = CommitComment(commitHash="abc123", threadId=0)
        state = _state(commit_comments={"abc123": cc})
        assert _resolve_commit_thread_id(state, "abc123") == 500

    def test_none_commit_uses_overall(self):
        state = _state()
        assert _resolve_commit_thread_id(state, None) == 500
