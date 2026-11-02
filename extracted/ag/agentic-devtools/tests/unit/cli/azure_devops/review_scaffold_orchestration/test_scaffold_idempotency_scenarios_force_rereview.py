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


class TestScaffoldForceRereview:
    """Same commit, same model, completed → re-run when force_rereview=True."""

    def test_force_resets_files_and_updates_in_place(self):
        """Resets files to unreviewed, opens a session, and patches in place."""
        session = ReviewSession(
            sessionId="s1",
            modelId="gpt-5",
            startedUtc="2026-01-01T00:00:00+00:00",
            completedUtc="2026-01-01T01:00:00+00:00",
            status="completed",
            commitHash="abc123",
        )
        state = _make_existing_state(sessions=[session])
        requests_mock = _make_requests_mock()

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
                return_value=state,
            ),
            patch("agentic_devtools.cli.azure_devops.review_scaffold_orchestration.save_review_state"),
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
                force_rereview=True,
            )

        assert result is state
        # Files reset to unreviewed for a fresh review.
        assert all(fe.status == ReviewStatus.UNREVIEWED.value for fe in state.files.values())
        # A new in-progress session was opened.
        assert any(s.status == "in_progress" for s in state.sessions)

    def test_force_dry_run_returns_state_without_changes(self):
        """In dry-run, force re-review returns existing state and makes no calls."""
        session = ReviewSession(
            sessionId="s1",
            modelId="gpt-5",
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
                dry_run=True,
                force_rereview=True,
            )

        assert result is state
        assert state.files["/src/a.ts"].status == ReviewStatus.APPROVED.value

    def test_force_survives_consolidated_comment_failure(self, capsys):
        """Force re-review still resets files and saves when the comment update fails."""
        session = ReviewSession(
            sessionId="s1",
            modelId="gpt-5",
            startedUtc="2026-01-01T00:00:00+00:00",
            completedUtc="2026-01-01T01:00:00+00:00",
            status="completed",
            commitHash="abc123",
        )
        state = _make_existing_state(sessions=[session])
        requests_mock = _make_requests_mock()

        with (
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
                return_value=state,
            ),
            patch("agentic_devtools.cli.azure_devops.review_scaffold_orchestration.save_review_state") as mock_save,
            patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.upsert_consolidated_comment",
                side_effect=Exception("patch boom"),
            ),
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
                force_rereview=True,
            )

        err = capsys.readouterr().err
        assert "Warning: Could not update consolidated review comment: patch boom" in err
        assert result is state
        assert all(fe.status == ReviewStatus.UNREVIEWED.value for fe in state.files.values())
        mock_save.assert_called_once()
