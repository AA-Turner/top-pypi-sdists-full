"""Tests for scaffold_review_threads idempotency scenarios.

These tests exercise the commit-hash-based idempotency paths within
scaffold_review_threads(), covering all 6 scenarios:
  - already_reviewed, in_progress, resume_stale,
  - different_model, different_commit, first_review
"""

from datetime import UTC, datetime, timedelta
from itertools import count
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_scaffold_orchestration import scaffold_review_threads
from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    FolderGroup,
    OverallSummary,
    ReviewSession,
    ReviewState,
    ReviewStatus,
)

_ORG = "https://dev.azure.com/testorg"
_PROJECT = "TestProject"
_REPO = "test-repo"
_REPO_ID = "repo-guid"
_PR_ID = 12345


def _make_config():
    return AzureDevOpsConfig(organization=_ORG, project=_PROJECT, repository=_REPO)


def _make_post_response(thread_id, comment_id):
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {"id": thread_id, "comments": [{"id": comment_id}]}
    return resp


def _make_existing_state(
    commit_hash="abc123",
    sessions=None,
    model_id="gpt-5",
    activity_log_thread_id=900,
    files=None,
):
    """Build a complete existing state."""
    file_entries = files or {
        "/src/a.ts": FileEntry(
            threadId=100,
            commentId=1,
            folder="src",
            fileName="a.ts",
            status=ReviewStatus.APPROVED.value,
        ),
    }
    return ReviewState(
        prId=_PR_ID,
        repoId=_REPO_ID,
        repoName=_REPO,
        project=_PROJECT,
        organization=_ORG,
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=500, commentId=1),
        folders={"src": FolderGroup(files=["/src/a.ts"])},
        files=file_entries,
        commitHash=commit_hash,
        modelId=model_id,
        activityLogThreadId=activity_log_thread_id,
        sessions=sessions or [],
    )


def _make_requests_mock():
    """Create a requests mock that handles GET/POST/PATCH for activity log calls."""
    requests_mock = MagicMock()
    id_gen = count(1000)

    def make_post_resp(*args, **kwargs):
        i = next(id_gen)
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {"id": i, "comments": [{"id": i + 1}]}
        return resp

    requests_mock.post.side_effect = make_post_resp

    get_resp = MagicMock()
    get_resp.raise_for_status = MagicMock()
    get_resp.json.return_value = {"comments": [{"id": 1, "content": "Old content"}]}
    requests_mock.get.return_value = get_resp

    patch_resp = MagicMock()
    patch_resp.raise_for_status = MagicMock()
    requests_mock.patch.return_value = patch_resp

    return requests_mock


class TestScaffoldResumeStale:
    """Same commit, same model, stale session → mark failed and resume."""

    def test_returns_existing_state(self):
        """Returns existing state with new session appended."""
        now = datetime.now(UTC)
        stale_started = now - timedelta(hours=3)
        session = ReviewSession(
            sessionId="stale-sess",
            modelId="gpt-5",
            startedUtc=stale_started.isoformat(),
            status="in_progress",
            commitHash="abc123",
        )
        state = _make_existing_state(sessions=[session])
        requests_mock = _make_requests_mock()

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            return_value=state,
        ):
            with patch("agentic_devtools.cli.azure_devops.review_scaffold_session_state.save_review_state"):
                result = scaffold_review_threads(
                    pull_request_id=_PR_ID,
                    files=["/src/a.ts"],
                    config=_make_config(),
                    repo_id=_REPO_ID,
                    repo_name=_REPO,
                    latest_iteration_id=1,
                    requests_module=requests_mock,
                    headers={},
                    commit_hash="abc123",
                    model_id="gpt-5",
                )

        assert result is state
        assert len(state.sessions) == 2  # original stale + new session

    def test_marks_stale_session_as_failed(self):
        """The stale session is marked as failed."""
        now = datetime.now(UTC)
        stale_started = now - timedelta(hours=3)
        session = ReviewSession(
            sessionId="stale-sess",
            modelId="gpt-5",
            startedUtc=stale_started.isoformat(),
            status="in_progress",
            commitHash="abc123",
        )
        state = _make_existing_state(sessions=[session])
        requests_mock = _make_requests_mock()

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            return_value=state,
        ):
            with patch("agentic_devtools.cli.azure_devops.review_scaffold_session_state.save_review_state"):
                scaffold_review_threads(
                    pull_request_id=_PR_ID,
                    files=["/src/a.ts"],
                    config=_make_config(),
                    repo_id=_REPO_ID,
                    repo_name=_REPO,
                    latest_iteration_id=1,
                    requests_module=requests_mock,
                    headers={},
                    commit_hash="abc123",
                    model_id="gpt-5",
                )

        assert session.status == "failed"

    def test_updates_failed_activity_log_comment_before_resuming(self):
        """Updates the stale session activity log reply before creating the new session."""
        now = datetime.now(UTC)
        stale_started = now - timedelta(hours=3)
        session = ReviewSession(
            sessionId="stale-sess",
            modelId="gpt-5",
            startedUtc=stale_started.isoformat(),
            status="in_progress",
            commitHash="abc123",
            activityLogCommentId=42,
        )
        state = _make_existing_state(sessions=[session])
        requests_mock = _make_requests_mock()

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
                return_value=state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_session_state._update_activity_log_comment_status"
            ) as mock_update,
            patch("agentic_devtools.cli.azure_devops.review_scaffold_session_state.save_review_state"),
        ):
            result = scaffold_review_threads(
                pull_request_id=_PR_ID,
                files=["/src/a.ts"],
                config=_make_config(),
                repo_id=_REPO_ID,
                repo_name=_REPO,
                latest_iteration_id=1,
                requests_module=requests_mock,
                headers={},
                commit_hash="abc123",
                model_id="gpt-5",
            )

        assert result is state
        mock_update.assert_called_once()
        call_args = mock_update.call_args[0]
        assert call_args[3] == state.activityLogThreadId
        assert call_args[4] == 42
        assert call_args[5] == "❌"
        assert call_args[6] == "Failed"
        assert call_args[7].sessionId == "stale-sess"
        assert call_args[8] == "abc123"
        assert call_args[9] == 1
        assert call_args[10] == "Session timed out (stale)."
        assert state.sessions[0].status == "failed"
        assert state.sessions[1].status == "in_progress"

    def test_updates_only_newly_transitioned_failed_sessions(self):
        """Does not rewrite comments for sessions that were already failed before resume_stale."""
        now = datetime.now(UTC)
        stale_started = now - timedelta(hours=3)
        already_failed = ReviewSession(
            sessionId="blocked-sess",
            modelId="gpt-5",
            startedUtc=stale_started.isoformat(),
            status="failed",
            completedUtc=stale_started.isoformat(),
            commitHash="abc123",
            activityLogCommentId=99,
        )
        stale_in_progress = ReviewSession(
            sessionId="stale-sess",
            modelId="gpt-5",
            startedUtc=stale_started.isoformat(),
            status="in_progress",
            commitHash="abc123",
            activityLogCommentId=42,
        )
        state = _make_existing_state(sessions=[already_failed, stale_in_progress])
        requests_mock = _make_requests_mock()

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
                return_value=state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_session_state._update_activity_log_comment_status"
            ) as mock_update,
            patch("agentic_devtools.cli.azure_devops.review_scaffold_session_state.save_review_state"),
        ):
            scaffold_review_threads(
                pull_request_id=_PR_ID,
                files=["/src/a.ts"],
                config=_make_config(),
                repo_id=_REPO_ID,
                repo_name=_REPO,
                latest_iteration_id=1,
                requests_module=requests_mock,
                headers={},
                commit_hash="abc123",
                model_id="gpt-5",
            )

        mock_update.assert_called_once()
        # Only the newly transitioned stale session should be updated.
        assert mock_update.call_args[0][4] == 42
        assert mock_update.call_args[0][7].sessionId == "stale-sess"
        # Resume entry should also reference the newly transitioned stale session,
        # not an older failed session with the same commit/model.
        post_calls = str(requests_mock.post.call_args_list)
        assert "stale-sess" in post_calls
        assert "blocked-sess" not in post_calls

    def test_stale_id_scoped_to_current_commit(self):
        """stale_id lookup only picks up failed sessions from the current commit, not older commits."""
        now = datetime.now(UTC)
        stale_started = now - timedelta(hours=3)
        # Old failed session from a prior commit — should NOT be selected as stale_id
        old_session = ReviewSession(
            sessionId="old-failed-sess",
            modelId="gpt-5",
            startedUtc=stale_started.isoformat(),
            status="failed",
            completedUtc=stale_started.isoformat(),
            commitHash="old_hash",
        )
        # Current stale in-progress session for the current commit — will be marked failed
        current_session = ReviewSession(
            sessionId="current-stale-sess",
            modelId="gpt-5",
            startedUtc=stale_started.isoformat(),
            status="in_progress",
            commitHash="abc123",
        )
        state = _make_existing_state(sessions=[old_session, current_session])
        state.activityLogThreadId = 900
        requests_mock = _make_requests_mock()

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            return_value=state,
        ):
            with patch("agentic_devtools.cli.azure_devops.review_scaffold_session_state.save_review_state"):
                scaffold_review_threads(
                    pull_request_id=_PR_ID,
                    files=["/src/a.ts"],
                    config=_make_config(),
                    repo_id=_REPO_ID,
                    repo_name=_REPO,
                    latest_iteration_id=1,
                    requests_module=requests_mock,
                    headers={},
                    commit_hash="abc123",
                    model_id="gpt-5",
                )

        # The activity log entry should reference "current-stale-sess" (just marked failed)
        # not "old-failed-sess" (from a prior commit).
        # The entry content is POSTed as a reply to the activity log thread.
        post_calls = str(requests_mock.post.call_args_list)
        assert "current-stale-sess" in post_calls
        assert "old-failed-sess" not in post_calls

    def test_fallback_stale_id_when_no_sessions_transitioned(self):
        """Falls back to scanning existing failed sessions when _mark_stale_sessions_failed returns empty."""
        now = datetime.now(UTC)
        stale_started = now - timedelta(hours=3)
        # A stale in-progress session triggers "resume_stale" from _check_session_status
        stale_session = ReviewSession(
            sessionId="stale-sess",
            modelId="gpt-5",
            startedUtc=stale_started.isoformat(),
            status="in_progress",
            commitHash="abc123",
        )
        # A previously failed session with matching model/commit — the fallback should find it
        prev_failed = ReviewSession(
            sessionId="prev-failed-sess",
            modelId="gpt-5",
            startedUtc=stale_started.isoformat(),
            status="failed",
            completedUtc=stale_started.isoformat(),
            commitHash="abc123",
        )
        state = _make_existing_state(sessions=[prev_failed, stale_session])
        requests_mock = _make_requests_mock()

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
                return_value=state,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_session_state._mark_stale_sessions_failed",
                return_value=[],
            ),
            patch("agentic_devtools.cli.azure_devops.review_scaffold_session_state.save_review_state"),
        ):
            result = scaffold_review_threads(
                pull_request_id=_PR_ID,
                files=["/src/a.ts"],
                config=_make_config(),
                repo_id=_REPO_ID,
                repo_name=_REPO,
                latest_iteration_id=1,
                requests_module=requests_mock,
                headers={},
                commit_hash="abc123",
                model_id="gpt-5",
            )

        assert result is state
        # The resume activity log entry should reference the fallback failed session
        post_calls = str(requests_mock.post.call_args_list)
        assert "prev-failed-sess" in post_calls
