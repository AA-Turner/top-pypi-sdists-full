"""Tests for _post_or_update_model_reply internal helper."""

from datetime import datetime, timezone
from itertools import count
from unittest.mock import MagicMock

from agentic_devtools.cli.azure_devops.review_scaffold import _post_or_update_model_reply
from agentic_devtools.cli.azure_devops.review_state import (
    CommitComment,
    FileEntry,
    OverallSummary,
    ReviewState,
    ReviewStatus,
)

_THREADS_URL = "https://dev.azure.com/org/proj/_apis/git/repositories/guid/pullRequests/42/threads"
_BASE_URL = "https://dev.azure.com/org/proj/_git/repo/pullrequest/42"
_NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _make_state(commit_comments=None, commit_hash="abc123", files=None):
    files = files or {
        "/src/a.ts": FileEntry(
            threadId=0,
            commentId=0,
            folder="src",
            fileName="a.ts",
            status=ReviewStatus.APPROVED.value,
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
        overallSummary=OverallSummary(threadId=500, commentId=1),
        files=files,
        commitHash=commit_hash,
        modelId="gpt-5",
        commitComments=commit_comments or {},
    )


def _make_requests_mock():
    requests_mock = MagicMock()
    id_gen = count(1000)

    def make_post(*args, **kwargs):
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {"id": next(id_gen)}
        return resp

    requests_mock.post.side_effect = make_post
    patch_resp = MagicMock()
    patch_resp.raise_for_status = MagicMock()
    patch_resp.status_code = 200
    requests_mock.patch.return_value = patch_resp
    return requests_mock


def _make_requests_mock_with_403():
    """Mock where PATCH always returns 403 (cross-identity), triggering the reply fallback."""
    requests_mock = MagicMock()
    id_gen = count(2000)

    def make_post(*args, **kwargs):
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {"id": next(id_gen)}
        return resp

    requests_mock.post.side_effect = make_post
    patch_resp = MagicMock()
    patch_resp.status_code = 403
    requests_mock.patch.return_value = patch_resp
    return requests_mock


class TestPostOrUpdateModelReply:
    """Tests for _post_or_update_model_reply."""

    def test_posts_new_reply_and_records_comment_id(self):
        state = _make_state()
        requests_mock = _make_requests_mock()

        comment_id = _post_or_update_model_reply(
            requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW
        )

        assert comment_id == 1000
        requests_mock.post.assert_called_once()
        entry = state.commitComments["abc123"]
        assert entry.threadId == 500  # fell back to overallSummary thread
        assert entry.get_model("claude").commentId == 1000

    def test_updates_existing_reply_in_place(self):
        existing = CommitComment(commitHash="abc123", threadId=500)
        ref = existing.upsert_model("claude")
        ref.commentId = 777
        state = _make_state(commit_comments={"abc123": existing})
        requests_mock = _make_requests_mock()

        comment_id = _post_or_update_model_reply(
            requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW
        )

        assert comment_id == 777
        requests_mock.post.assert_not_called()
        requests_mock.patch.assert_called_once()
        assert state.commitComments["abc123"].get_model("claude").commentId == 777

    def test_prefers_per_commit_thread_over_overall_summary(self):
        existing = CommitComment(commitHash="abc123", threadId=900)
        state = _make_state(commit_comments={"abc123": existing})
        requests_mock = _make_requests_mock()

        _post_or_update_model_reply(requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW)

        # POST URL must target thread 900, not the overall-summary thread 500.
        post_url = requests_mock.post.call_args.args[0]
        assert "/threads/900/comments" in post_url

    def test_returns_none_when_no_thread_resolvable(self):
        state = _make_state()
        state.overallSummary.threadId = 0
        requests_mock = _make_requests_mock()

        result = _post_or_update_model_reply(
            requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW
        )

        assert result is None
        requests_mock.post.assert_not_called()

    def test_backfills_thread_id_on_existing_entry_without_thread(self):
        """An existing registry entry with threadId<=0 is backfilled from the resolved thread."""
        existing = CommitComment(commitHash="abc123", threadId=0)
        state = _make_state(commit_comments={"abc123": existing})
        requests_mock = _make_requests_mock()

        comment_id = _post_or_update_model_reply(
            requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW
        )

        assert comment_id == 1000
        # threadId was backfilled from the overall-summary fallback thread.
        assert state.commitComments["abc123"].threadId == 500
        assert state.commitComments["abc123"].get_model("claude").commentId == 1000

    def test_falls_back_to_state_commit_hash_when_arg_hash_is_none(self):
        """When commit_hash arg is None, use existing_state.commitHash as registry key."""
        state = _make_state(commit_hash="abc123")
        requests_mock = _make_requests_mock()

        comment_id = _post_or_update_model_reply(
            requests_mock, {}, _THREADS_URL, state, None, "claude", _BASE_URL, _NOW
        )

        assert comment_id == 1000
        # Entry must be stored under the state's commit hash, not the empty string.
        assert "abc123" in state.commitComments
        assert "" not in state.commitComments

    def test_returns_none_when_both_commit_hashes_are_empty(self):
        """When commit_hash is None and state has no hash either, return None."""
        state = _make_state(commit_hash="")
        requests_mock = _make_requests_mock()

        result = _post_or_update_model_reply(requests_mock, {}, _THREADS_URL, state, None, "claude", _BASE_URL, _NOW)

        assert result is None
        requests_mock.post.assert_not_called()
        assert "" not in state.commitComments

    def test_updates_comment_id_on_403_fallback(self):
        """On PATCH 403, ref.commentId is updated to the newly posted reply id."""
        existing = CommitComment(commitHash="abc123", threadId=500)
        ref = existing.upsert_model("claude")
        ref.commentId = 777  # pre-existing reply that is now cross-identity
        state = _make_state(commit_comments={"abc123": existing})
        requests_mock = _make_requests_mock_with_403()

        comment_id = _post_or_update_model_reply(
            requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW
        )

        # A new reply was posted (fallback), so comment_id != 777.
        assert comment_id == 2000
        # The registry must be updated to the new reply id.
        assert state.commitComments["abc123"].get_model("claude").commentId == 2000

    def test_updates_commit_comment_timestamp_on_post(self):
        """CommitComment.timestamp is updated to now when a new model reply is posted."""
        state = _make_state()
        requests_mock = _make_requests_mock()

        _post_or_update_model_reply(requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW)

        entry = state.commitComments["abc123"]
        assert entry.timestamp == _NOW.isoformat()

    def test_updates_commit_comment_timestamp_on_patch(self):
        """CommitComment.timestamp is updated to now when an existing model reply is updated."""
        existing = CommitComment(commitHash="abc123", threadId=500, timestamp="2020-01-01T00:00:00+00:00")
        ref = existing.upsert_model("claude")
        ref.commentId = 777
        state = _make_state(commit_comments={"abc123": existing})
        requests_mock = _make_requests_mock()

        _post_or_update_model_reply(requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW)

        assert state.commitComments["abc123"].timestamp == _NOW.isoformat()

    def test_new_entry_status_synced_from_overall_summary(self):
        """A newly created registry entry inherits status from overallSummary, not 'unreviewed'."""
        state = _make_state()
        state.overallSummary.status = ReviewStatus.APPROVED.value
        requests_mock = _make_requests_mock()

        _post_or_update_model_reply(requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW)

        entry = state.commitComments["abc123"]
        assert entry.status == ReviewStatus.APPROVED.value

    def test_new_entry_status_synced_needs_work(self):
        """A newly created registry entry syncs 'needs-work' from overallSummary."""
        state = _make_state()
        state.overallSummary.status = ReviewStatus.NEEDS_WORK.value
        requests_mock = _make_requests_mock()

        _post_or_update_model_reply(requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW)

        entry = state.commitComments["abc123"]
        assert entry.status == ReviewStatus.NEEDS_WORK.value

    def test_model_ref_status_uses_overall_aggregate_on_post(self):
        state = _make_state()
        state.overallSummary.status = ReviewStatus.APPROVED.value
        requests_mock = _make_requests_mock()

        _post_or_update_model_reply(requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW)

        ref = state.commitComments["abc123"].get_model("claude")
        assert ref is not None
        assert ref.status == ReviewStatus.APPROVED.value

    def test_model_ref_status_uses_overall_aggregate_on_patch(self):
        existing = CommitComment(commitHash="abc123", threadId=500)
        ref = existing.upsert_model("claude")
        ref.commentId = 777
        state = _make_state(commit_comments={"abc123": existing})
        state.files["/src/a.ts"].status = ReviewStatus.NEEDS_WORK.value
        requests_mock = _make_requests_mock()

        _post_or_update_model_reply(requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW)

        assert state.commitComments["abc123"].get_model("claude").status == ReviewStatus.NEEDS_WORK.value

    def test_model_ref_status_is_in_progress_when_a_file_is_not_terminal(self):
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
                status=ReviewStatus.IN_PROGRESS.value,
            ),
        }
        state = _make_state(files=files)
        state.overallSummary.status = ReviewStatus.APPROVED.value
        requests_mock = _make_requests_mock()

        _post_or_update_model_reply(requests_mock, {}, _THREADS_URL, state, "abc123", "claude", _BASE_URL, _NOW)

        ref = state.commitComments["abc123"].get_model("claude")
        assert ref is not None
        assert ref.status == ReviewStatus.IN_PROGRESS.value
