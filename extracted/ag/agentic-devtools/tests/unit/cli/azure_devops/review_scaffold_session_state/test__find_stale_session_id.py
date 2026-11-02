"""Tests for _find_stale_session_id."""

from agentic_devtools.cli.azure_devops.review_scaffold_session_state import _find_stale_session_id
from agentic_devtools.cli.azure_devops.review_state import OverallSummary, ReviewSession, ReviewState


def _state(session=None):
    return ReviewState(
        prId=1,
        repoId="repo",
        repoName="repo",
        project="project",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=1, commentId=1),
        sessions=[session] if session else [],
    )


def test_returns_transitioned_session_id_first():
    session = ReviewSession("transitioned", "model", "2020-01-01T00:00:00+00:00")

    result = _find_stale_session_id(_state(), [session], "model", "commit")

    assert result == "transitioned"


def test_finds_matching_failed_session_when_no_transitioned_sessions():
    session = ReviewSession(
        "failed",
        "model",
        "2020-01-01T00:00:00+00:00",
        status="failed",
        commitHash="commit",
    )

    result = _find_stale_session_id(_state(session), [], "model", "commit")

    assert result == "failed"


def test_returns_unknown_when_no_matching_session_exists():
    assert _find_stale_session_id(_state(), [], "model", "commit") == "unknown"


def test_continues_searching_past_nonmatching_sessions():
    matching = ReviewSession(
        "failed",
        "model",
        "2020-01-01T00:00:00+00:00",
        status="failed",
        commitHash="commit",
    )
    other = ReviewSession(
        "other",
        "other-model",
        "2020-01-01T00:00:00+00:00",
        status="failed",
        commitHash="commit",
    )
    state = _state()
    state.sessions = [matching, other]

    assert _find_stale_session_id(state, [], "model", "commit") == "failed"
