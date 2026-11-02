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

        with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.detect_file_changes") as mock_detect:
            mock_detect.return_value = FileChangeResult(unchanged_files=["/src/a.ts"])
            with patch(
                "agentic_devtools.cli.azure_devops.review_scaffold_incremental.fetch_threads_lookup"
            ) as mock_fetch:
                mock_fetch.return_value = {300: {"id": 300, "comments": [{"id": 1}]}}
                with patch(
                    "agentic_devtools.cli.azure_devops.review_scaffold_incremental.categorize_all_suggestions"
                ) as mock_cat:
                    mock_cat.return_value = [needs_review]
                    with patch("agentic_devtools.cli.azure_devops.review_scaffold_incremental.save_review_state"):
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
