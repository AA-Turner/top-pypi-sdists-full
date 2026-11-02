"""Tests for _incremental_rescaffold internal function."""

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

from ._test_helpers import _make_existing_state_with_previous_suggestions, _make_suggestion

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


class TestIncrementalRescaffoldVerificationGatePart2:
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

        with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.detect_file_changes") as mock_detect:
            from agentic_devtools.cli.azure_devops.review_scaffold_changes import FileChangeResult

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

            with patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_incremental.fetch_threads_lookup"
            ) as mock_fetch:
                mock_fetch.return_value = fetch_threads_return

                with patch(
                    "agentic_devtools.cli.azure_devops.review_scaffold_incremental.categorize_all_suggestions"
                ) as mock_categorize:
                    mock_categorize.return_value = categorize_return or []

                    with patch(
                        "agentic_devtools.cli.azure_devops.review_scaffold_incremental.save_review_state", save_mock
                    ):
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

        with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.detect_file_changes") as mock_detect:
            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])
            with patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_incremental.fetch_threads_lookup"
            ) as mock_fetch:
                mock_fetch.return_value = {300: {"id": 300, "comments": [{"id": 1}]}}
                with patch(
                    "agentic_devtools.cli.azure_devops.review_scaffold_incremental.categorize_all_suggestions"
                ) as mock_cat:
                    mock_cat.return_value = [unaddressed]
                    with patch(
                        "agentic_devtools.cli.azure_devops.review_scaffold_incremental.save_review_state", save_mock
                    ):
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

        with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.detect_file_changes") as mock_detect:
            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])
            with patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_incremental.fetch_threads_lookup"
            ) as mock_fetch:
                mock_fetch.return_value = {300: {"id": 300, "comments": [{"id": 1}]}}
                with patch(
                    "agentic_devtools.cli.azure_devops.review_scaffold_incremental.categorize_all_suggestions"
                ) as mock_cat:
                    mock_cat.return_value = [unaddressed]
                    with patch(
                        "agentic_devtools.cli.azure_devops.review_scaffold_incremental.save_review_state", save_mock
                    ):
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
