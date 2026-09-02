"""Tests for complete_active_session function."""

from datetime import datetime, timezone

from agentic_devtools.cli.azure_devops.review_state import (
    OverallSummary,
    ReviewSession,
    ReviewState,
    complete_active_session,
)


def _make_state_with_sessions(sessions: list[ReviewSession], commit_hash: str | None = None) -> ReviewState:
    state = ReviewState(
        prId=100,
        repoId="repo-guid",
        repoName="repo",
        project="proj",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00Z",
        overallSummary=OverallSummary(threadId=1, commentId=2),
        commitHash=commit_hash,
    )
    state.sessions = sessions
    return state


class TestCompleteActiveSession:
    """Tests for complete_active_session function."""

    def test_returns_none_when_no_sessions(self):
        """Test that None is returned when there are no sessions."""
        state = _make_state_with_sessions([])
        assert complete_active_session(state) is None

    def test_returns_none_when_no_in_progress_session(self):
        """Test that None is returned when no session is in_progress."""
        session = ReviewSession(
            sessionId="s1",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00Z",
            status="completed",
        )
        state = _make_state_with_sessions([session])
        assert complete_active_session(state) is None
        assert session.status == "completed"

    def test_marks_in_progress_session_completed(self):
        """Test that an in_progress session is transitioned to completed."""
        session = ReviewSession(
            sessionId="s1",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00Z",
            status="in_progress",
        )
        state = _make_state_with_sessions([session])
        result = complete_active_session(state)
        assert result is session
        assert session.status == "completed"
        assert session.completedUtc is not None

    def test_marks_latest_in_progress_session_not_first(self):
        """Test that the latest (last) in_progress session is completed, not an earlier one."""
        s1 = ReviewSession(sessionId="s1", modelId="m1", startedUtc="t1", status="in_progress")
        s2 = ReviewSession(sessionId="s2", modelId="m2", startedUtc="t2", status="in_progress")
        state = _make_state_with_sessions([s1, s2])
        result = complete_active_session(state)
        assert result is s2
        assert s2.status == "completed"
        assert s1.status == "in_progress"

    def test_returns_none_when_newest_session_is_terminal(self):
        """A terminal newest session leaves older in-progress sessions untouched."""
        s1 = ReviewSession(sessionId="s1", modelId="m1", startedUtc="t1", status="in_progress")
        s2 = ReviewSession(sessionId="s2", modelId="m2", startedUtc="t2", status="failed")
        state = _make_state_with_sessions([s1, s2])
        assert complete_active_session(state) is None
        assert s1.status == "in_progress"
        assert s2.status == "failed"

    def test_mutates_review_state_in_place(self):
        """Test that the same session object is mutated, not replaced."""
        session = ReviewSession(
            sessionId="s1",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00Z",
            status="in_progress",
        )
        state = _make_state_with_sessions([session])
        complete_active_session(state)
        assert state.sessions[0] is session
        assert state.sessions[0].status == "completed"

    def test_uses_injected_now_for_completed_utc(self):
        """Test that an injected `now` is used for completedUtc instead of the real clock."""
        session = ReviewSession(
            sessionId="s1",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00Z",
            status="in_progress",
        )
        state = _make_state_with_sessions([session])
        fixed_now = datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
        complete_active_session(state, now=fixed_now)
        assert session.completedUtc == fixed_now.isoformat()

    def test_skips_in_progress_session_for_different_commit(self):
        """Test that an in_progress session for a stale commit is left untouched.

        When ``review_state.commitHash`` is set (current re-review), a session
        tagged with a different (older) commit hash must not be completed —
        only the session matching the current commit is eligible.
        """
        stale = ReviewSession(
            sessionId="s1",
            modelId="model-a",
            startedUtc="t1",
            status="in_progress",
            commitHash="old-commit",
        )
        state = _make_state_with_sessions([stale], commit_hash="new-commit")
        assert complete_active_session(state) is None
        assert stale.status == "in_progress"

    def test_completes_session_with_no_commit_hash_when_state_commit_hash_set(self):
        """Test that a legacy session lacking commitHash is still eligible for completion.

        ``ReviewSession.commitHash`` was added after sessions were first
        introduced, so a pre-existing session with ``commitHash=None`` must
        remain eligible even when ``review_state.commitHash`` is set — it
        must not be permanently stuck "in_progress" for lacking a value that
        didn't exist yet when it was created.
        """
        legacy = ReviewSession(
            sessionId="s1",
            modelId="model-a",
            startedUtc="t1",
            status="in_progress",
            commitHash=None,
        )
        state = _make_state_with_sessions([legacy], commit_hash="new-commit")
        result = complete_active_session(state)
        assert result is legacy
        assert legacy.status == "completed"

    def test_completes_session_matching_current_commit(self):
        """Test that the session tagged with the current commit hash is completed."""
        stale = ReviewSession(
            sessionId="s1",
            modelId="model-a",
            startedUtc="t1",
            status="in_progress",
            commitHash="old-commit",
        )
        current = ReviewSession(
            sessionId="s2",
            modelId="model-a",
            startedUtc="t2",
            status="in_progress",
            commitHash="new-commit",
        )
        state = _make_state_with_sessions([stale, current], commit_hash="new-commit")
        result = complete_active_session(state)
        assert result is current
        assert current.status == "completed"
        assert stale.status == "in_progress"

    def test_repeated_calls_do_not_complete_other_models_current_commit_sessions(self):
        """Repeated completion calls must not close another model's active session."""
        other_model = ReviewSession(
            sessionId="s1",
            modelId="model-a",
            startedUtc="t1",
            status="in_progress",
            commitHash="commit-1",
        )
        current_model = ReviewSession(
            sessionId="s2",
            modelId="model-b",
            startedUtc="t2",
            status="in_progress",
            commitHash="commit-1",
        )
        state = _make_state_with_sessions([other_model, current_model], commit_hash="commit-1")
        state.modelId = "model-b"

        first = complete_active_session(state)
        second = complete_active_session(state)

        assert first is current_model
        assert second is None
        assert current_model.status == "completed"
        assert other_model.status == "in_progress"
