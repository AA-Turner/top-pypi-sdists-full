"""Tests for _incremental_rescaffold internal function."""

from itertools import count
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_scaffold import _incremental_rescaffold
from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    FolderGroup,
    OverallSummary,
    ReviewState,
    ReviewStatus,
    SuggestionEntry,
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


class TestIncrementalRescaffold:
    """Tests for _incremental_rescaffold."""

    def _run_rescaffold(self, existing_state, current_files, changed_paths=None, model_id="gpt-5"):
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
        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

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

            with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state", save_mock):
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
                )

        return result, requests_mock, save_mock

    def test_new_files_added_inline(self):
        """New files are added as inline entries with no per-file thread."""
        existing = _make_existing_state(files=["/src/a.ts"])
        result, _, _ = self._run_rescaffold(existing, ["/src/a.ts", "/src/new.ts"])

        assert "/src/new.ts" in result.files
        assert result.files["/src/new.ts"].threadId == 0
        assert result.files["/src/new.ts"].status == ReviewStatus.UNREVIEWED.value

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

        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])

            with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state"):
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

        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])
            with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state", save_mock):
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


class TestIncrementalRescaffoldDryRun:
    """Tests for dry-run mode in _incremental_rescaffold."""

    def _run_dry(self, existing, files, change_result):
        """Run _incremental_rescaffold in dry-run mode with given FileChangeResult."""
        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            mock_detect.return_value = change_result
            with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state"):
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
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

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
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=["/src/a.ts"])
        self._run_dry(existing, ["/src/a.ts"], FileChangeResult(modified_files=["/src/a.ts"]))
        out = capsys.readouterr().out
        assert "[DRY RUN] Modified file: /src/a.ts" in out

    def test_prints_deleted_files(self, capsys):
        """Dry-run mode prints deleted file entries."""
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=["/src/a.ts"])
        self._run_dry(existing, [], FileChangeResult(deleted_files=["/src/a.ts"]))
        out = capsys.readouterr().out
        assert "[DRY RUN] Deleted file: /src/a.ts" in out

    def test_prints_unchanged_files(self, capsys):
        """Dry-run mode prints unchanged file entries."""
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=["/src/a.ts"])
        self._run_dry(existing, ["/src/a.ts"], FileChangeResult(unchanged_files=["/src/a.ts"]))
        out = capsys.readouterr().out
        assert "[DRY RUN] Unchanged file: /src/a.ts" in out


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
        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            mock_detect.return_value = change_result
            with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state"):
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
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

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
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

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


def _make_suggestion(thread_id: int = 300) -> SuggestionEntry:
    return SuggestionEntry(
        threadId=thread_id,
        commentId=301,
        line=10,
        endLine=20,
        severity="high",
        outOfScope=False,
        linkText="lines 10 - 20",
        content="Missing null check",
    )


def _make_existing_state_with_previous_suggestions(
    files=None,
    commit_hash="old_hash",
    previous_suggestions_map=None,
):
    """Build an existing state with previousSuggestions on specific files."""
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

    # Apply previousSuggestions
    if previous_suggestions_map:
        for fp, suggestions in previous_suggestions_map.items():
            if fp in file_entries:
                file_entries[fp].previousSuggestions = suggestions

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


class TestIncrementalRescaffoldVerificationGate:
    """Tests for the suggestion verification gate in _incremental_rescaffold."""

    def _run_rescaffold_with_mocks(
        self,
        existing_state,
        current_files,
        changed_paths=None,
        dry_run=False,
        fetch_threads_return=None,
        categorize_return=None,
    ):
        """Run _incremental_rescaffold with mocked verification functions."""
        requests_mock = MagicMock()
        id_gen = count(1000)

        def make_resp(*args, **kwargs):
            i = next(id_gen)
            return _make_post_response(i, i + 1)

        requests_mock.post.side_effect = make_resp

        get_resp = MagicMock()
        get_resp.raise_for_status = MagicMock()
        get_resp.json.return_value = {"comments": [{"id": 1, "content": "Old content"}]}
        requests_mock.get.return_value = get_resp

        patch_resp = MagicMock()
        patch_resp.raise_for_status = MagicMock()
        requests_mock.patch.return_value = patch_resp

        save_mock = MagicMock()

        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

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

            with patch("agentic_devtools.cli.azure_devops.review_scaffold.fetch_threads_lookup") as mock_fetch:
                mock_fetch.return_value = fetch_threads_return

                with patch(
                    "agentic_devtools.cli.azure_devops.review_scaffold.categorize_all_suggestions"
                ) as mock_categorize:
                    mock_categorize.return_value = categorize_return or []

                    with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state", save_mock):
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
                            dry_run=dry_run,
                            commit_hash="new_hash",
                            model_id="gpt-5",
                        )

        return result, requests_mock, save_mock, mock_fetch, mock_categorize

    def test_abort_gate_fires_with_unaddressed_suggestions(self, capsys):
        """Abort gate blocks review when unaddressed suggestions exist."""
        from agentic_devtools.cli.azure_devops.suggestion_verification import (
            CATEGORY_NEEDS_REVIEW,
            CATEGORY_UNADDRESSED,
            SuggestionVerificationResult,
        )

        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )

        unaddressed = SuggestionVerificationResult(
            suggestion=suggestion,
            file_path="/src/a.ts",
            category=CATEGORY_UNADDRESSED,
            has_reply=False,
            file_changed=False,
            thread_status="active",
        )
        needs_review = SuggestionVerificationResult(
            suggestion=_make_suggestion(thread_id=301),
            file_path="/src/a.ts",
            category=CATEGORY_NEEDS_REVIEW,
            has_reply=True,
            file_changed=False,
            thread_status="active",
        )

        result, requests_mock, save_mock, _, _ = self._run_rescaffold_with_mocks(
            existing,
            ["/src/a.ts"],
            fetch_threads_return={300: {"id": 300, "comments": [{"id": 1}]}},
            categorize_return=[unaddressed, needs_review],
        )

        # Should return existing_state (early return, not None)
        assert result is not None
        # Session should be marked as failed
        assert len(result.sessions) == 1
        assert result.sessions[0].status == "failed"
        assert result.sessions[0].completedUtc is not None
        # Commit hash should still be updated
        assert result.commitHash == "new_hash"
        # State should be saved
        save_mock.assert_called_once()
        # Should print abort message
        out = capsys.readouterr().out
        assert "Review blocked" in out

    def test_abort_gate_updates_commit_hash_before_consolidated_upsert(self):
        """Abort gate updates commitHash before re-rendering consolidated comment."""
        from agentic_devtools.cli.azure_devops.suggestion_verification import (
            CATEGORY_UNADDRESSED,
            SuggestionVerificationResult,
        )

        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )

        unaddressed = SuggestionVerificationResult(
            suggestion=suggestion,
            file_path="/src/a.ts",
            category=CATEGORY_UNADDRESSED,
            has_reply=False,
            file_changed=False,
            thread_status="active",
        )

        def _assert_new_hash(*args, **kwargs):
            assert kwargs["state"].commitHash == "new_hash"

        with patch("agentic_devtools.cli.azure_devops.review_scaffold.upsert_consolidated_comment") as mock_upsert:
            mock_upsert.side_effect = _assert_new_hash
            self._run_rescaffold_with_mocks(
                existing,
                ["/src/a.ts"],
                fetch_threads_return={300: {"id": 300, "comments": [{"id": 1}]}},
                categorize_return=[unaddressed],
            )

        mock_upsert.assert_called_once()

    def test_abort_gate_records_session_without_activity_log_thread(self, capsys):
        """Abort gate records failed session even when activityLogThreadId is falsy."""
        from agentic_devtools.cli.azure_devops.suggestion_verification import (
            CATEGORY_UNADDRESSED,
            SuggestionVerificationResult,
        )

        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )
        # Set activityLogThreadId to 0 (falsy)
        existing.activityLogThreadId = 0

        unaddressed = SuggestionVerificationResult(
            suggestion=suggestion,
            file_path="/src/a.ts",
            category=CATEGORY_UNADDRESSED,
            has_reply=False,
            file_changed=False,
            thread_status="active",
        )

        result, requests_mock, save_mock, _, _ = self._run_rescaffold_with_mocks(
            existing,
            ["/src/a.ts"],
            fetch_threads_return={300: {"id": 300, "comments": [{"id": 1}]}},
            categorize_return=[unaddressed],
        )

        # Session should still be created and marked as failed
        assert result is not None
        assert len(result.sessions) == 1
        assert result.sessions[0].status == "failed"
        assert result.sessions[0].completedUtc is not None
        # State should be saved
        save_mock.assert_called_once()
        # Abort message should be printed
        out = capsys.readouterr().out
        assert "Review blocked" in out

    def test_all_needs_review_sets_pending_verification(self):
        """When all suggestions are needs_review, files get pending_verification status."""
        from agentic_devtools.cli.azure_devops.suggestion_verification import (
            CATEGORY_NEEDS_REVIEW,
            SuggestionVerificationResult,
        )

        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )

        needs_review = SuggestionVerificationResult(
            suggestion=suggestion,
            file_path="/src/a.ts",
            category=CATEGORY_NEEDS_REVIEW,
            has_reply=True,
            file_changed=False,
            thread_status="active",
        )

        result, _, _, _, _ = self._run_rescaffold_with_mocks(
            existing,
            ["/src/a.ts"],
            fetch_threads_return={300: {"id": 300, "comments": [{"id": 1}, {"id": 2}]}},
            categorize_return=[needs_review],
        )

        assert result is not None
        assert result.files["/src/a.ts"].suggestionVerificationStatus == "pending_verification"

    def test_fetch_threads_returns_none_proceeds(self, capsys):
        """When fetch_threads_lookup returns None, proceed without blocking."""
        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )

        result, _, _, mock_fetch, mock_categorize = self._run_rescaffold_with_mocks(
            existing,
            ["/src/a.ts"],
            fetch_threads_return=None,
        )

        # Should proceed to normal scaffolding (not abort)
        assert result is not None
        # categorize_all_suggestions should NOT have been called
        mock_categorize.assert_not_called()
        # Warning should be printed
        err = capsys.readouterr().err
        assert "Could not fetch PR threads" in err

    def test_dry_run_skips_verification(self):
        """Dry-run mode skips the verification gate entirely."""
        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )

        result, _, _, mock_fetch, mock_categorize = self._run_rescaffold_with_mocks(
            existing,
            ["/src/a.ts"],
            dry_run=True,
            fetch_threads_return={300: {"id": 300, "comments": [{"id": 1}]}},
        )

        # Returns None in dry-run mode
        assert result is None
        # fetch_threads_lookup should NOT have been called (dry_run short-circuits)
        mock_fetch.assert_not_called()
        mock_categorize.assert_not_called()

    def test_no_previous_suggestions_skips_verification(self):
        """No files with previousSuggestions → verification is skipped entirely."""
        existing = _make_existing_state(files=["/src/a.ts"])
        assert existing.files["/src/a.ts"].previousSuggestions is None

        result, _, _, mock_fetch, mock_categorize = self._run_rescaffold_with_mocks(
            existing,
            ["/src/a.ts"],
            fetch_threads_return={},
        )

        assert result is not None
        mock_fetch.assert_not_called()
        mock_categorize.assert_not_called()

    def test_abort_gate_posts_unaddressed_thread_comments(self):
        """Abort gate posts reply comments on each unaddressed suggestion thread."""
        from agentic_devtools.cli.azure_devops.suggestion_verification import (
            CATEGORY_UNADDRESSED,
            SuggestionVerificationResult,
        )

        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )

        unaddressed = SuggestionVerificationResult(
            suggestion=suggestion,
            file_path="/src/a.ts",
            category=CATEGORY_UNADDRESSED,
            has_reply=False,
            file_changed=False,
            thread_status="active",
        )

        result, requests_mock, _, _, _ = self._run_rescaffold_with_mocks(
            existing,
            ["/src/a.ts"],
            fetch_threads_return={300: {"id": 300, "comments": [{"id": 1}]}},
            categorize_return=[unaddressed],
        )

        # Verify POST calls were made (thread comment + activity log)
        assert requests_mock.post.call_count >= 1
        assert result is not None

    def test_abort_gate_thread_comment_exception_handled(self, capsys):
        """Exception posting unaddressed thread comment is caught and logged."""
        from agentic_devtools.cli.azure_devops.suggestion_verification import (
            CATEGORY_UNADDRESSED,
            SuggestionVerificationResult,
        )

        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )

        unaddressed = SuggestionVerificationResult(
            suggestion=suggestion,
            file_path="/src/a.ts",
            category=CATEGORY_UNADDRESSED,
            has_reply=False,
            file_changed=False,
            thread_status="active",
        )

        requests_mock = MagicMock()
        # POST fails (thread comment + activity log)
        requests_mock.post.side_effect = Exception("API error")
        get_resp = MagicMock()
        get_resp.raise_for_status = MagicMock()
        get_resp.json.return_value = {"comments": [{"id": 1, "content": "Old"}]}
        requests_mock.get.return_value = get_resp
        patch_resp = MagicMock()
        patch_resp.raise_for_status = MagicMock()
        requests_mock.patch.return_value = patch_resp

        save_mock = MagicMock()

        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])
            with patch("agentic_devtools.cli.azure_devops.review_scaffold.fetch_threads_lookup") as mock_fetch:
                mock_fetch.return_value = {300: {"id": 300, "comments": [{"id": 1}]}}
                with patch("agentic_devtools.cli.azure_devops.review_scaffold.categorize_all_suggestions") as mock_cat:
                    mock_cat.return_value = [unaddressed]
                    with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state", save_mock):
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
                            commit_hash="new_hash",
                            model_id="gpt-5",
                        )

        err = capsys.readouterr().err
        assert "Could not post unaddressed comment on thread 300" in err
        assert "Could not post activity log" in err
        assert result is not None

    def test_abort_gate_summary_exception_handled(self, capsys):
        """Exception posting abort summary is caught and logged."""
        from agentic_devtools.cli.azure_devops.suggestion_verification import (
            CATEGORY_UNADDRESSED,
            SuggestionVerificationResult,
        )

        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )

        unaddressed = SuggestionVerificationResult(
            suggestion=suggestion,
            file_path="/src/a.ts",
            category=CATEGORY_UNADDRESSED,
            has_reply=False,
            file_changed=False,
            thread_status="active",
        )

        requests_mock = MagicMock()
        post_resp = MagicMock()
        post_resp.raise_for_status = MagicMock()
        post_resp.json.return_value = {"id": 999, "comments": [{"id": 1}]}
        requests_mock.post.return_value = post_resp
        # The consolidated comment is updated via PATCH; make that PATCH fail.
        requests_mock.patch.side_effect = Exception("PATCH error")

        save_mock = MagicMock()

        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])
            with patch("agentic_devtools.cli.azure_devops.review_scaffold.fetch_threads_lookup") as mock_fetch:
                mock_fetch.return_value = {300: {"id": 300, "comments": [{"id": 1}]}}
                with patch("agentic_devtools.cli.azure_devops.review_scaffold.categorize_all_suggestions") as mock_cat:
                    mock_cat.return_value = [unaddressed]
                    with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state", save_mock):
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
                            commit_hash="new_hash",
                            model_id="gpt-5",
                        )

        err = capsys.readouterr().err
        assert "Could not update consolidated review comment" in err
        assert result is not None

    def test_deleted_file_with_suggestions_included_in_changed_set(self, capsys):
        """Deleted file with previous suggestions should be in changed_set, avoiding false unaddressed."""
        from agentic_devtools.cli.azure_devops.suggestion_verification import (
            CATEGORY_NEEDS_REVIEW,
            SuggestionVerificationResult,
        )

        suggestion = _make_suggestion(thread_id=500)
        # File /src/removed.ts exists in state but will NOT be in current_files (deleted).
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts", "/src/removed.ts"],
            previous_suggestions_map={"/src/removed.ts": [suggestion]},
        )

        needs_review = SuggestionVerificationResult(
            suggestion=suggestion,
            file_path="/src/removed.ts",
            category=CATEGORY_NEEDS_REVIEW,
            has_reply=False,
            file_changed=True,  # deleted = changed
            thread_status="active",
        )

        result, _, _, _, mock_categorize = self._run_rescaffold_with_mocks(
            existing,
            ["/src/a.ts"],  # /src/removed.ts deleted
            fetch_threads_return={500: {"id": 500, "comments": [{"id": 1}]}},
            categorize_return=[needs_review],
        )

        # Verify categorize_all_suggestions was called with changed_set including the deleted file
        call_args = mock_categorize.call_args
        changed_files_arg = call_args[0][1]  # second positional arg
        assert "/src/removed.ts" in changed_files_arg
        # No abort — file is needs_review, not unaddressed
        assert result is not None
        assert not any(s.status == "failed" for s in result.sessions)


class TestIncrementalRescaffoldEmptyVerificationResults:
    """Tests for empty verification results (1602->1693)."""

    def test_empty_verification_results_proceeds_normally(self):
        """When categorize_all_suggestions returns empty, review proceeds.

        Covers branch 1602->1693: ``if verification_results:`` is False.
        """
        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )

        requests_mock = MagicMock()
        id_gen = count(1000)

        def make_resp(*args, **kwargs):
            i = next(id_gen)
            return _make_post_response(i, i + 1)

        requests_mock.post.side_effect = make_resp
        get_resp = MagicMock()
        get_resp.raise_for_status = MagicMock()
        get_resp.json.return_value = {"comments": [{"id": 1, "content": "Old content"}]}
        requests_mock.get.return_value = get_resp
        patch_resp = MagicMock()
        patch_resp.raise_for_status = MagicMock()
        requests_mock.patch.return_value = patch_resp

        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])
            with patch("agentic_devtools.cli.azure_devops.review_scaffold.fetch_threads_lookup") as mock_fetch:
                mock_fetch.return_value = {300: {"id": 300, "comments": [{"id": 1}]}}
                with patch("agentic_devtools.cli.azure_devops.review_scaffold.categorize_all_suggestions") as mock_cat:
                    mock_cat.return_value = []  # Empty results
                    with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state"):
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
                            commit_hash="new_hash",
                            model_id="gpt-5",
                        )

        assert result is not None
        assert not any(s.status == "failed" for s in result.sessions)


class TestIncrementalRescaffoldAbortWithoutOverallThread:
    """Test abort gate when overall.threadId is 0 (1628->1644)."""

    def test_abort_gate_skips_demote_when_no_overall_thread(self, capsys):
        """Abort gate skips demote call when overall.threadId is 0.

        Covers branch 1628->1644: ``if overall.threadId:`` is False.
        """
        from agentic_devtools.cli.azure_devops.suggestion_verification import (
            CATEGORY_UNADDRESSED,
            SuggestionVerificationResult,
        )

        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )
        existing.overallSummary.threadId = 0

        unaddressed = SuggestionVerificationResult(
            suggestion=suggestion,
            file_path="/src/a.ts",
            category=CATEGORY_UNADDRESSED,
            has_reply=False,
            file_changed=False,
            thread_status="active",
        )

        requests_mock = MagicMock()
        post_resp = MagicMock()
        post_resp.raise_for_status = MagicMock()
        post_resp.json.return_value = {"id": 999, "comments": [{"id": 1}]}
        requests_mock.post.return_value = post_resp

        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])
            with patch("agentic_devtools.cli.azure_devops.review_scaffold.fetch_threads_lookup") as mock_fetch:
                mock_fetch.return_value = {300: {"id": 300, "comments": [{"id": 1}]}}
                with patch("agentic_devtools.cli.azure_devops.review_scaffold.categorize_all_suggestions") as mock_cat:
                    mock_cat.return_value = [unaddressed]
                    with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state"):
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
                            commit_hash="new_hash",
                            model_id="gpt-5",
                        )

        assert result is not None
        assert result.sessions[-1].status == "failed"
        out = capsys.readouterr().out
        assert "Review blocked" in out


class TestIncrementalRescaffoldNeedsReviewMissingFile:
    """Test needs_review loop skips missing file (1688->1686)."""

    def test_needs_review_skips_file_not_in_state(self):
        """When needs_review result references a file not in state, it is skipped.

        Covers branch 1688->1686: ``if fe:`` is False, loop continues.
        """
        from agentic_devtools.cli.azure_devops.suggestion_verification import (
            CATEGORY_NEEDS_REVIEW,
            SuggestionVerificationResult,
        )

        suggestion = _make_suggestion(thread_id=300)
        existing = _make_existing_state_with_previous_suggestions(
            files=["/src/a.ts"],
            previous_suggestions_map={"/src/a.ts": [suggestion]},
        )

        needs_review = SuggestionVerificationResult(
            suggestion=suggestion,
            file_path="/src/nonexistent.ts",
            category=CATEGORY_NEEDS_REVIEW,
            has_reply=True,
            file_changed=False,
            thread_status="active",
        )

        requests_mock = MagicMock()
        id_gen = count(1000)

        def make_resp(*args, **kwargs):
            i = next(id_gen)
            return _make_post_response(i, i + 1)

        requests_mock.post.side_effect = make_resp
        get_resp = MagicMock()
        get_resp.raise_for_status = MagicMock()
        get_resp.json.return_value = {"comments": [{"id": 1, "content": "Old content"}]}
        requests_mock.get.return_value = get_resp
        patch_resp = MagicMock()
        patch_resp.raise_for_status = MagicMock()
        requests_mock.patch.return_value = patch_resp

        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])
            with patch("agentic_devtools.cli.azure_devops.review_scaffold.fetch_threads_lookup") as mock_fetch:
                mock_fetch.return_value = {300: {"id": 300, "comments": [{"id": 1}]}}
                with patch("agentic_devtools.cli.azure_devops.review_scaffold.categorize_all_suggestions") as mock_cat:
                    mock_cat.return_value = [needs_review]
                    with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state"):
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
                            commit_hash="new_hash",
                            model_id="gpt-5",
                        )

        assert result is not None
        # File /src/a.ts should NOT have pending_verification status
        assert existing.files["/src/a.ts"].suggestionVerificationStatus is None


class TestIncrementalRescaffoldEdgeCases:
    """Edge case tests for _incremental_rescaffold."""

    def _run_with_change_result(self, existing, files, change_result, activity_log_thread_id=999):
        """Run _incremental_rescaffold with a specific FileChangeResult."""
        existing.activityLogThreadId = activity_log_thread_id

        requests_mock = MagicMock()
        id_gen = count(1000)

        def make_resp(*args, **kwargs):
            i = next(id_gen)
            return _make_post_response(i, i + 1)

        requests_mock.post.side_effect = make_resp
        get_resp = MagicMock()
        get_resp.raise_for_status = MagicMock()
        get_resp.json.return_value = {"comments": [{"id": 1, "content": "Old content"}]}
        requests_mock.get.return_value = get_resp
        patch_resp = MagicMock()
        patch_resp.raise_for_status = MagicMock()
        requests_mock.patch.return_value = patch_resp

        save_mock = MagicMock()

        with patch("agentic_devtools.cli.azure_devops.review_scaffold.detect_file_changes") as mock_detect:
            mock_detect.return_value = change_result
            with patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state", save_mock):
                result = _incremental_rescaffold(
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

        return result, requests_mock, save_mock

    def test_modified_file_reset_regardless_of_thread_id(self):
        """A modified file is reset to unreviewed regardless of its (legacy) threadId.

        In the consolidated model files have no per-file thread (threadId == 0), so the
        reset is no longer gated on threadId.
        """
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=["/src/a.ts"])
        existing.files["/src/a.ts"].threadId = 0
        result, _, _ = self._run_with_change_result(
            existing,
            ["/src/a.ts"],
            FileChangeResult(modified_files=["/src/a.ts"]),
        )

        assert result is not None
        # File state IS reset even though threadId is 0 (no per-file thread).
        assert result.files["/src/a.ts"].status == ReviewStatus.UNREVIEWED.value

    def test_deleted_file_marked_regardless_of_thread_id(self):
        """A deleted file is marked removed regardless of its (legacy) threadId."""
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=["/src/a.ts", "/src/del.ts"])
        existing.files["/src/del.ts"].threadId = 0
        result, _, _ = self._run_with_change_result(
            existing,
            ["/src/a.ts"],
            FileChangeResult(deleted_files=["/src/del.ts"], unchanged_files=["/src/a.ts"]),
        )

        assert result is not None
        # File status IS updated even though threadId is 0 (no per-file thread).
        assert result.files["/src/del.ts"].status == ReviewStatus.APPROVED.value
        assert result.files["/src/del.ts"].summary == "File removed"

    def test_modified_file_missing_from_state_skipped(self):
        """A modified file absent from review state is skipped (defensive ``if fe`` guard)."""
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=["/src/a.ts"])
        result, _, _ = self._run_with_change_result(
            existing,
            ["/src/a.ts"],
            FileChangeResult(modified_files=["/src/ghost.ts"], unchanged_files=["/src/a.ts"]),
        )

        assert result is not None
        assert "/src/ghost.ts" not in result.files

    def test_deleted_file_missing_from_state_skipped(self):
        """A deleted file absent from review state is skipped (defensive ``if fe`` guard)."""
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=["/src/a.ts"])
        result, _, _ = self._run_with_change_result(
            existing,
            ["/src/a.ts"],
            FileChangeResult(deleted_files=["/src/ghost.ts"], unchanged_files=["/src/a.ts"]),
        )

        assert result is not None
        assert "/src/ghost.ts" not in result.files

    def test_no_overall_thread_skips_summary_update(self, capsys):
        """Overall summary update is skipped when overall.threadId is 0.

        Covers branch 1840->1875: ``if overall.threadId:`` is False.
        """
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=["/src/a.ts"])
        existing.overallSummary.threadId = 0
        result, requests_mock, _ = self._run_with_change_result(
            existing,
            ["/src/a.ts"],
            FileChangeResult(modified_files=["/src/a.ts"]),
        )

        assert result is not None
        assert result.commitHash == "new_hash"

    def test_no_changes_at_all_skips_both_summary_branches(self, capsys):
        """When all file counts are 0, neither summary branch is entered.

        Covers branch 1855->1875: ``elif`` condition is False.
        """
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=[])
        existing.folders = {}
        result, _, _ = self._run_with_change_result(
            existing,
            [],
            FileChangeResult(),
        )

        assert result is not None
        assert result.commitHash == "new_hash"

    def test_rebase_no_changes_without_overall_thread(self, capsys):
        """Rebase with no changes skips summary update when overall.threadId is 0.

        Covers branch 1858->1875: ``if overall.threadId:`` is False inside elif.
        """
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=["/src/a.ts"])
        existing.overallSummary.threadId = 0
        result, requests_mock, _ = self._run_with_change_result(
            existing,
            ["/src/a.ts"],
            FileChangeResult(unchanged_files=["/src/a.ts"]),
        )

        assert result is not None
        assert result.commitHash == "new_hash"

    def test_no_activity_log_skips_log_posting(self, capsys):
        """Activity log posting is skipped when activityLogThreadId is 0.

        Covers branch 1881->1915: ``if existing_state.activityLogThreadId:`` is False.
        """
        from agentic_devtools.cli.azure_devops.review_scaffold import FileChangeResult

        existing = _make_existing_state(files=["/src/a.ts"])
        result, requests_mock, save_mock = self._run_with_change_result(
            existing,
            ["/src/a.ts"],
            FileChangeResult(unchanged_files=["/src/a.ts"]),
            activity_log_thread_id=0,
        )

        assert result is not None
        # State should be saved only once (no second save for activity log comment ID)
        assert save_mock.call_count == 1
        out = capsys.readouterr().out
        assert "Incremental re-scaffolding complete" in out
