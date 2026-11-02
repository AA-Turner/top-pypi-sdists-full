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


class TestIncrementalRescaffoldDryRun:
    """Tests for dry-run mode in _incremental_rescaffold."""

    def _run_dry(self, existing, files, change_result):
        """Run _incremental_rescaffold in dry-run mode with given FileChangeResult."""
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
                    requests_module=MagicMock(),
                    headers={},
                    dry_run=True,
                    commit_hash="new_hash",
                    model_id="gpt-5",
                )

    def test_prints_new_files(self, capsys):
        """Dry-run mode prints new file entries."""

        existing = _make_existing_state(files=["/src/a.ts"])
        self._run_dry(
            existing,
            ["/src/a.ts", "/src/new.ts"],
            FileChangeResult(new_files=["/src/new.ts"], unchanged_files=["/src/a.ts"]),
        )
        out = capsys.readouterr().out
        assert "[DRY RUN] New file: /src/new.ts" in out

    def test_prints_modified_files(self, capsys):
        """Dry-run mode prints modified file entries."""

        existing = _make_existing_state(files=["/src/a.ts"])
        self._run_dry(existing, ["/src/a.ts"], FileChangeResult(modified_files=["/src/a.ts"]))
        out = capsys.readouterr().out
        assert "[DRY RUN] Modified file: /src/a.ts" in out

    def test_prints_deleted_files(self, capsys):
        """Dry-run mode prints deleted file entries."""

        existing = _make_existing_state(files=["/src/a.ts"])
        self._run_dry(existing, [], FileChangeResult(deleted_files=["/src/a.ts"]))
        out = capsys.readouterr().out
        assert "[DRY RUN] Deleted file: /src/a.ts" in out

    def test_prints_unchanged_files(self, capsys):
        """Dry-run mode prints unchanged file entries."""

        existing = _make_existing_state(files=["/src/a.ts"])
        self._run_dry(existing, ["/src/a.ts"], FileChangeResult(unchanged_files=["/src/a.ts"]))
        out = capsys.readouterr().out
        assert "[DRY RUN] Unchanged file: /src/a.ts" in out
