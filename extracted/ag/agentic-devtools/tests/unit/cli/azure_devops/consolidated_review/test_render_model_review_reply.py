"""Tests for render_model_review_reply."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    is_model_reply_comment,
    render_model_review_reply,
)
from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    OverallSummary,
    ReviewState,
    ReviewStatus,
)

_BASE_URL = "https://dev.azure.com/org/proj/_git/repo/pullrequest/42"


def _make_state():
    files = {
        "/src/a.ts": FileEntry(
            threadId=0,
            commentId=0,
            folder="src",
            fileName="a.ts",
            status=ReviewStatus.APPROVED.value,
        ),
        "/src/b.ts": FileEntry(
            threadId=0,
            commentId=0,
            folder="src",
            fileName="b.ts",
            status=ReviewStatus.NEEDS_WORK.value,
        ),
    }
    return ReviewState(
        prId=42,
        repoId="guid",
        repoName="repo",
        project="proj",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=10, commentId=1),
        files=files,
        commitHash="abc123def456",
        modelId="gpt-5",
    )


class TestRenderModelReviewReply:
    """Tests for render_model_review_reply."""

    def test_carries_model_reply_marker(self):
        out = render_model_review_reply(_make_state(), "claude", _BASE_URL)
        assert is_model_reply_comment(out)
        assert "model:claude" in out

    def test_includes_model_header_and_short_hash(self):
        out = render_model_review_reply(_make_state(), "claude", _BASE_URL)
        assert "Additional review by" in out
        assert "claude" in out
        assert "abc123d" in out  # short hash (7 chars)

    def test_counts_terminal_files_and_lists_them(self):
        # a.ts approved, b.ts needs-work → 1 approved, 1 need work
        out = render_model_review_reply(_make_state(), "claude", _BASE_URL)
        assert "1 approved" in out
        assert "1 need work" in out
        assert "`/src/a.ts`" in out
        assert "`/src/b.ts`" in out

    def test_omits_non_terminal_files(self):
        state = _make_state()
        state.files["/src/b.ts"].status = ReviewStatus.UNREVIEWED.value
        out = render_model_review_reply(state, "claude", _BASE_URL)
        assert "1 approved" in out
        assert "0 need work" in out
        assert "`/src/a.ts`" in out
        assert "`/src/b.ts`" not in out

    def test_no_terminal_files_yields_zero_counts_and_no_file_list(self):
        state = _make_state()
        state.files["/src/a.ts"].status = ReviewStatus.UNREVIEWED.value
        state.files["/src/b.ts"].status = ReviewStatus.IN_PROGRESS.value
        out = render_model_review_reply(state, "claude", _BASE_URL)
        assert "0 approved" in out
        assert "0 need work" in out
        assert "`/src/a.ts`" not in out
        assert "`/src/b.ts`" not in out

    def test_in_progress_file_is_not_listed(self):
        # A file whose status is neither approved nor needs-work is omitted and
        # counts toward neither tally.
        state = _make_state()
        state.files["/src/a.ts"].status = ReviewStatus.IN_PROGRESS.value
        del state.files["/src/b.ts"]
        out = render_model_review_reply(state, "claude", _BASE_URL)
        assert "0 approved" in out
        assert "0 need work" in out
        assert "`/src/a.ts`" not in out
