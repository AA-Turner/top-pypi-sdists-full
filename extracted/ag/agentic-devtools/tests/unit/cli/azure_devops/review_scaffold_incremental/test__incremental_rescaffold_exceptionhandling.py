"""Tests for _incremental_rescaffold internal function."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_scaffold_changes import FileChangeResult
from agentic_devtools.cli.azure_devops.review_scaffold_incremental import _incremental_rescaffold
from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    FolderGroup,
    OverallSummary,
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


def _make_existing_state(files=None, commit_hash="old_hash"):
    """Build a complete existing state for re-scaffolding tests."""
    file_entries = {}
    folder_files = {}
    for fp in files or ["/src/a.ts"]:
        folder = fp.split("/")[1] if "/" in fp.lstrip("/") else "root"
        file_entries[fp] = FileEntry(
            threadId=100,
            commentId=1,
            folder=folder,
            fileName=fp.split("/")[-1],
            status=ReviewStatus.APPROVED.value,
            summary="Previously reviewed",
        )
        folder_files.setdefault(folder, []).append(fp)

    folders = {k: FolderGroup(files=v) for k, v in folder_files.items()}

    return ReviewState(
        prId=_PR_ID,
        repoId=_REPO_ID,
        repoName=_REPO,
        project=_PROJECT,
        organization=_ORG,
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=500, commentId=1),
        folders=folders,
        files=file_entries,
        commitHash=commit_hash,
        activityLogThreadId=999,
    )


class TestIncrementalRescaffoldExceptionHandling:
    """Tests for exception handling in _incremental_rescaffold."""

    def _make_failing_requests_mock(self):
        """Create a requests mock where GET always fails."""
        requests_mock = MagicMock()
        requests_mock.get.side_effect = Exception("Network error")
        post_resp = MagicMock()
        post_resp.raise_for_status = MagicMock()
        post_resp.json.return_value = {"id": 999, "comments": [{"id": 1}]}
        requests_mock.post.return_value = post_resp
        return requests_mock

    def _run_with_failure(self, existing, files, change_result, requests_mock=None):
        """Run _incremental_rescaffold with failing mocks."""
        if requests_mock is None:
            requests_mock = self._make_failing_requests_mock()
        with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.detect_file_changes") as mock_detect:
            mock_detect.return_value = change_result
            with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.save_review_state"):
                return _incremental_rescaffold(
                    existing_state=existing,
                    pull_request_id=_PR_ID,
                    files=files,
                    config=_make_config(),
                    repo_id=_REPO_ID,
                    repo_name=_REPO,
                    latest_iteration_id=5,
                    requests_module=requests_mock,
                    headers={},
                    dry_run=False,
                    commit_hash="new_hash",
                    model_id="gpt-5",
                )

    def test_consolidated_comment_exception(self, capsys):
        """Consolidated comment update failure is caught and logged."""

        existing = _make_existing_state(files=["/src/a.ts"])
        requests_mock = MagicMock()
        # New top-level thread per commit: the consolidated comment is POSTed as a
        # new thread; make that POST fail.
        requests_mock.post.side_effect = Exception("Summary error")

        result = self._run_with_failure(
            existing, ["/src/a.ts"], FileChangeResult(modified_files=["/src/a.ts"]), requests_mock
        )
        err = capsys.readouterr().err
        assert "Could not update consolidated review comment" in err
        assert result is not None

    def test_activity_log_exception(self, capsys):
        """Activity log posting failure is caught and logged."""

        existing = _make_existing_state(files=["/src/a.ts"])
        requests_mock = MagicMock()
        # The consolidated comment PATCH succeeds; the activity-log POST fails.
        patch_resp = MagicMock()
        patch_resp.raise_for_status = MagicMock()
        requests_mock.patch.return_value = patch_resp
        requests_mock.post.side_effect = Exception("Network error")

        result = self._run_with_failure(
            existing,
            ["/src/a.ts"],
            FileChangeResult(unchanged_files=["/src/a.ts"]),
            requests_mock,
        )
        err = capsys.readouterr().err
        assert "Warning: Could not post activity log entry" in err
        assert result is not None
