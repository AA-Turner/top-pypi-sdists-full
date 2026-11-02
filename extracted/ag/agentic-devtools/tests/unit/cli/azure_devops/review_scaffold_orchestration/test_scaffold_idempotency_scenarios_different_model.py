"""Tests for scaffold_review_threads idempotency scenarios.

These tests exercise the commit-hash-based idempotency paths within
scaffold_review_threads(), covering all 6 scenarios:
  - already_reviewed, in_progress, resume_stale,
  - different_model, different_commit, first_review
"""

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


class TestScaffoldDifferentModel:
    """Same commit, different model → skip scaffolding, post activity log."""

    def test_returns_existing_state(self):
        """Returns existing state for a different model joining."""
        session = ReviewSession(
            sessionId="s1",
            modelId="claude-4",
            startedUtc="2026-01-01T00:00:00+00:00",
            completedUtc="2026-01-01T01:00:00+00:00",
            status="completed",
            commitHash="abc123",
        )
        state = _make_existing_state(sessions=[session])
        requests_mock = _make_requests_mock()

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            return_value=state,
        ):
            with patch("agentic_devtools.cli.azure_devops.review_scaffold_orchestration.save_review_state"):
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
        # New session appended for the new model
        assert len(state.sessions) == 2
        assert state.sessions[1].modelId == "gpt-5"

    def test_prints_additional_reviewer_message(self, capsys):
        """Prints that an additional reviewer is joining."""
        session = ReviewSession(
            sessionId="s1",
            modelId="claude-4",
            startedUtc="2026-01-01T00:00:00+00:00",
            completedUtc="2026-01-01T01:00:00+00:00",
            status="completed",
            commitHash="abc123",
        )
        state = _make_existing_state(sessions=[session])
        requests_mock = _make_requests_mock()

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            return_value=state,
        ):
            with patch("agentic_devtools.cli.azure_devops.review_scaffold_orchestration.save_review_state"):
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

        out = capsys.readouterr().out
        assert "Additional reviewer" in out
