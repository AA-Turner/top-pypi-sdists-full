"""Tests for _incremental_rescaffold internal function."""

from datetime import datetime
from itertools import count
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

from ._test_helpers import _make_suggestion

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


class TestIncrementalRescaffold:
    """Tests for _incremental_rescaffold."""

    def _run_rescaffold(self, existing_state, current_files, changed_paths=None, model_id="gpt-5", now=None):
        """Run _incremental_rescaffold with mocked detect_file_changes."""
        requests_mock = MagicMock()
        id_gen = count(1000)

        def make_resp(*args, **kwargs):
            i = next(id_gen)
            return _make_post_response(i, i + 1)

        requests_mock.post.side_effect = make_resp

        # Mock the GET for _get_thread_comments (returns main comment)
        get_resp = MagicMock()
        get_resp.raise_for_status = MagicMock()
        get_resp.json.return_value = {"comments": [{"id": 1, "content": "Old content"}]}
        requests_mock.get.return_value = get_resp

        # Mock PATCH
        patch_resp = MagicMock()
        patch_resp.raise_for_status = MagicMock()
        requests_mock.patch.return_value = patch_resp

        save_mock = MagicMock()

        # Mock detect_file_changes to return controlled results
        with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.detect_file_changes") as mock_detect:
            existing_files = set(existing_state.files.keys())
            current_set = set(current_files)
            changed_set = set(changed_paths or [])

            result_obj = FileChangeResult(
                new_files=sorted(current_set - existing_files),
                modified_files=sorted(existing_files & current_set & changed_set),
                deleted_files=sorted(existing_files - current_set),
                unchanged_files=sorted((existing_files & current_set) - changed_set),
            )
            mock_detect.return_value = result_obj

            with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.save_review_state", save_mock):
                result = _incremental_rescaffold(
                    existing_state=existing_state,
                    pull_request_id=_PR_ID,
                    files=current_files,
                    config=_make_config(),
                    repo_id=_REPO_ID,
                    repo_name=_REPO,
                    latest_iteration_id=5,
                    requests_module=requests_mock,
                    headers={},
                    dry_run=False,
                    commit_hash="new_hash",
                    model_id=model_id,
                    now=now,
                )

        return result, requests_mock, save_mock

    def test_new_files_added_inline(self):
        """New files are added as inline entries with no per-file thread."""
        existing = _make_existing_state(files=["/src/a.ts"])
        result, _, _ = self._run_rescaffold(existing, ["/src/a.ts", "/src/new.ts"])

        assert "/src/new.ts" in result.files
        assert result.files["/src/new.ts"].threadId == 0
        assert result.files["/src/new.ts"].status == ReviewStatus.UNREVIEWED.value

    def test_uses_supplied_current_time(self):
        """A supplied timestamp bypasses the wall-clock default."""
        existing = _make_existing_state(files=["/src/a.ts"])
        now = datetime.fromisoformat("2026-01-01T00:00:00+00:00")
        with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.datetime") as mock_datetime:
            result, _, _ = self._run_rescaffold(existing, ["/src/a.ts"], now=now)

        mock_datetime.now.assert_not_called()
        assert result.commitHash == "new_hash"

    def test_modified_files_reset_to_unreviewed(self):
        """Modified files are reset to unreviewed status."""
        existing = _make_existing_state(files=["/src/a.ts"])
        file_entry = existing.files["/src/a.ts"]
        file_entry.modelId = "old-model"
        file_entry.providerType = "openai_direct"
        file_entry.latencyMs = 123
        file_entry.finishReason = "stop"
        file_entry.tokensUsed = 42
        result, _, _ = self._run_rescaffold(
            existing,
            ["/src/a.ts"],
            changed_paths=["/src/a.ts"],
        )

        assert result.files["/src/a.ts"].status == ReviewStatus.UNREVIEWED.value
        assert result.files["/src/a.ts"].summary is None
        assert file_entry.modelId is None
        assert file_entry.providerType is None
        assert file_entry.latencyMs is None
        assert file_entry.finishReason is None
        assert file_entry.tokensUsed is None

    def test_modified_files_rotate_suggestions(self):
        """Modified files move suggestions to previousSuggestions."""
        existing = _make_existing_state(files=["/src/a.ts"])
        existing.files["/src/a.ts"].suggestions = []
        result, _, _ = self._run_rescaffold(
            existing,
            ["/src/a.ts"],
            changed_paths=["/src/a.ts"],
        )

        assert result.files["/src/a.ts"].suggestions == []
        assert result.files["/src/a.ts"].previousSuggestions == []

    def test_modified_files_preserve_existing_previous_suggestions(self):
        """Modified files keep existing previousSuggestions when there are no new suggestions."""
        existing = _make_existing_state(files=["/src/a.ts"])
        prior = _make_suggestion(thread_id=401)
        existing.files["/src/a.ts"].previousSuggestions = [prior]
        existing.files["/src/a.ts"].suggestions = []

        result, _, _ = self._run_rescaffold(
            existing,
            ["/src/a.ts"],
            changed_paths=["/src/a.ts"],
        )

        assert result.files["/src/a.ts"].suggestions == []
        assert result.files["/src/a.ts"].previousSuggestions == [prior]

    def test_modified_files_append_new_suggestions_to_previous_suggestions(self):
        """Modified files append current suggestions to existing previousSuggestions."""
        existing = _make_existing_state(files=["/src/a.ts"])
        prior = _make_suggestion(thread_id=401)
        current = _make_suggestion(thread_id=402)
        existing.files["/src/a.ts"].previousSuggestions = [prior]
        existing.files["/src/a.ts"].suggestions = [current]

        result, _, _ = self._run_rescaffold(
            existing,
            ["/src/a.ts"],
            changed_paths=["/src/a.ts"],
        )

        assert result.files["/src/a.ts"].suggestions == []
        assert result.files["/src/a.ts"].previousSuggestions == [prior, current]

    def test_modified_file_resets_in_consolidated_comment(self):
        """A modified file is reset to unreviewed and a NEW per-commit thread is POSTed."""
        existing = _make_existing_state(files=["/src/a.ts"])
        result, requests_mock, _ = self._run_rescaffold(existing, ["/src/a.ts"], changed_paths=["/src/a.ts"])
        assert result is not None

        # New top-level thread per reviewed commit: a fresh thread is POSTed for
        # the new commit (overallSummary pointer was reset), and the prior commit
        # is archived into the per-commit registry for the "Previous reviews" index.
        assert result.files["/src/a.ts"].status == ReviewStatus.UNREVIEWED.value
        comment_post_contents = [
            call.kwargs.get("json", {})
            for call in requests_mock.post.call_args_list
            if call.kwargs.get("json", {}).get("comments")
        ]
        assert comment_post_contents, "Expected a new consolidated thread to be POSTed for the new commit"
        assert "old_hash" in result.commitComments
        assert result.commitComments["old_hash"].threadId == 500

    def test_deleted_files_marked_approved(self):
        """Deleted files are marked as approved with 'File removed' summary."""
        existing = _make_existing_state(files=["/src/a.ts", "/src/deleted.ts"])
        result, _, _ = self._run_rescaffold(existing, ["/src/a.ts"])

        assert result.files["/src/deleted.ts"].status == ReviewStatus.APPROVED.value
        assert result.files["/src/deleted.ts"].summary == "File removed"

    def test_unchanged_files_preserve_state(self):
        """Unchanged files keep their existing state."""
        existing = _make_existing_state(files=["/src/a.ts"])
        existing.files["/src/a.ts"].status = ReviewStatus.APPROVED.value
        existing.files["/src/a.ts"].summary = "LGTM"

        result, _, _ = self._run_rescaffold(existing, ["/src/a.ts"])

        assert result.files["/src/a.ts"].status == ReviewStatus.APPROVED.value
        assert result.files["/src/a.ts"].summary == "LGTM"

    def test_commit_hash_updated(self):
        """Commit hash is updated to the new value."""
        existing = _make_existing_state(commit_hash="old_hash")
        result, _, _ = self._run_rescaffold(existing, ["/src/a.ts"])

        assert result.commitHash == "new_hash"

    def test_new_session_created(self):
        """A new session is created for the re-scaffolding."""
        existing = _make_existing_state()
        result, _, _ = self._run_rescaffold(existing, ["/src/a.ts"])

        assert len(result.sessions) == 1
        assert result.sessions[0].status == "in_progress"

    def test_state_saved(self):
        """State is saved after re-scaffolding (once for state + once for activity log comment ID)."""
        existing = _make_existing_state()
        _, _, save_mock = self._run_rescaffold(existing, ["/src/a.ts"])

        assert save_mock.call_count == 2

    def test_dry_run_returns_none(self):
        """Returns None in dry-run mode."""
        existing = _make_existing_state()

        with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.detect_file_changes") as mock_detect:
            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])

            with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.save_review_state"):
                result = _incremental_rescaffold(
                    existing_state=existing,
                    pull_request_id=_PR_ID,
                    files=["/src/a.ts"],
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

        assert result is None

    def test_folder_groups_updated_for_new_files(self):
        """Folder groups are updated when new files are added."""
        existing = _make_existing_state(files=["/src/a.ts"])
        result, _, _ = self._run_rescaffold(existing, ["/src/a.ts", "/utils/b.ts"])

        assert "utils" in result.folders
        assert "/utils/b.ts" in result.folders["utils"].files

    def test_empty_folder_preserved_when_all_files_deleted(self):
        """Folder group is preserved (empty) when all its files are deleted."""
        existing = _make_existing_state(files=["/old/only.ts", "/src/a.ts"])
        # All files in "old" folder are deleted, only /src/a.ts remains
        result, _, _ = self._run_rescaffold(existing, ["/src/a.ts"])

        assert "old" in result.folders
        assert result.folders["old"].files == []

    def test_rebase_no_changes_updates_commit_hash(self):
        """Rebase with no file changes still updates the commit hash."""
        existing = _make_existing_state(files=["/src/a.ts"])
        result, _, _ = self._run_rescaffold(existing, ["/src/a.ts"])

        assert result.commitHash == "new_hash"

    def test_no_archive_when_old_commit_hash_empty(self):
        """No prior commit is archived when the existing state has no commit hash."""
        existing = _make_existing_state(commit_hash="")
        result, _, _ = self._run_rescaffold(existing, ["/src/a.ts"])

        assert result.commitHash == "new_hash"
        # The empty old hash is not archived into the per-commit registry.
        assert "" not in result.commitComments

    def test_no_archive_and_commit_hash_preserved_when_new_hash_is_none(self):
        """When commit_hash is None the prior commit thread is not archived and
        the existing commitHash is preserved (not overwritten with None)."""
        existing = _make_existing_state(commit_hash="old_hash")
        save_mock = MagicMock()

        requests_mock = MagicMock()
        patch_resp = MagicMock()
        patch_resp.raise_for_status = MagicMock()
        patch_resp.status_code = 200
        patch_resp.json.return_value = {}
        requests_mock.patch.return_value = patch_resp
        get_resp = MagicMock()
        get_resp.raise_for_status = MagicMock()
        get_resp.json.return_value = {"comments": [{"id": 1, "content": "existing"}]}
        requests_mock.get.return_value = get_resp

        with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.detect_file_changes") as mock_detect:
            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])
            with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.save_review_state", save_mock):
                result = _incremental_rescaffold(
                    existing_state=existing,
                    pull_request_id=_PR_ID,
                    files=["/src/a.ts"],
                    config=_make_config(),
                    repo_id=_REPO_ID,
                    repo_name=_REPO,
                    latest_iteration_id=5,
                    requests_module=requests_mock,
                    headers={},
                    dry_run=False,
                    commit_hash=None,
                    model_id="gpt-5",
                )

        assert result is not None
        # commitHash should not have been overwritten with None
        assert result.commitHash == "old_hash"
        # overallSummary.threadId must NOT have been reset to 0 (archive was skipped),
        # so no new POST thread was triggered for a null-hash commit.
        assert result.overallSummary.threadId == 500
