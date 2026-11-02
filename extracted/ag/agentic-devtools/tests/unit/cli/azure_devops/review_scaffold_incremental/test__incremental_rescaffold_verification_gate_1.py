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


class TestIncrementalRescaffoldVerificationGatePart1:
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

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_incremental.upsert_consolidated_comment"
        ) as mock_upsert:
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
