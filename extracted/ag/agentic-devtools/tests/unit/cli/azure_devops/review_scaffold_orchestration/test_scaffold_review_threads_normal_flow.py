"""Tests for scaffold_review_threads function."""

from itertools import count
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_scaffold_orchestration import scaffold_review_threads
from agentic_devtools.cli.azure_devops.review_state import (
    ReviewState,
    ReviewStatus,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

_ORG = "https://dev.azure.com/testorg"
_PROJECT = "TestProject"
_REPO = "test-repo"
_REPO_ID = "repo-guid-abc"
_PR_ID = 25365


def _make_config(org=_ORG, project=_PROJECT, repo=_REPO) -> AzureDevOpsConfig:
    return AzureDevOpsConfig(organization=org, project=project, repository=repo)


def _make_post_response(thread_id: int, comment_id: int) -> MagicMock:
    """Build a mock requests.post response for thread creation."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {
        "id": thread_id,
        "comments": [{"id": comment_id}],
    }
    return resp


# ---------------------------------------------------------------------------
# Tests: scaffold_review_threads — idempotency
# ---------------------------------------------------------------------------


class TestScaffoldReviewThreadsNormalFlow:
    """Tests for the normal scaffolding flow in scaffold_review_threads."""

    def _run_scaffold(self, files, post_responses=None):
        """Run scaffold_review_threads with mocked dependencies.

        Args:
            files: List of file paths.
            post_responses: Optional list of mock responses for requests.post calls.
                If None, auto-generates sequential IDs.

        Returns:
            Tuple of (result, requests_mock, save_mock).
        """
        requests_mock = MagicMock()
        if post_responses is None:
            # Auto-generate responses: thread_id = i*100, comment_id = i*100+1
            id_gen = count(1)

            def make_resp(*args, **kwargs):
                i = next(id_gen)
                return _make_post_response(thread_id=i * 100, comment_id=i * 100 + 1)

            requests_mock.post.side_effect = make_resp
        else:
            requests_mock.post.side_effect = post_responses

        save_mock = MagicMock()

        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            side_effect=FileNotFoundError,
        ):
            with patch("agentic_devtools.cli.azure_devops.review_scaffold_fresh.save_review_state", save_mock):
                result = scaffold_review_threads(
                    pull_request_id=_PR_ID,
                    files=files,
                    config=_make_config(),
                    repo_id=_REPO_ID,
                    repo_name=_REPO,
                    latest_iteration_id=5,
                    requests_module=requests_mock,
                    headers={"Authorization": "Bearer token"},
                )

        return result, requests_mock, save_mock

    def test_returns_review_state(self):
        """Returns a ReviewState object on success."""
        result, _, _ = self._run_scaffold(["/src/app.ts"])
        assert isinstance(result, ReviewState)

    def test_correct_pr_id(self):
        """ReviewState has the correct PR ID."""
        result, _, _ = self._run_scaffold(["/src/app.ts"])
        assert result.prId == _PR_ID

    def test_correct_repo_metadata(self):
        """ReviewState has correct repo metadata."""
        result, _, _ = self._run_scaffold(["/src/app.ts"])
        assert result.repoId == _REPO_ID
        assert result.repoName == _REPO
        assert result.project == _PROJECT
        assert result.organization == _ORG
        assert result.latestIterationId == 5

    def test_api_call_count_single_consolidated_thread(self):
        """Makes exactly 1 API POST call: the single consolidated review comment."""
        # File count is irrelevant — everything is rendered inline in one comment.
        files = ["/src/a.ts", "/src/b.ts", "/utils/c.ts"]
        _, requests_mock, _ = self._run_scaffold(files)
        assert requests_mock.post.call_count == 1

    def test_no_file_anchored_threads(self):
        """No file-anchored threads are created; the single comment is PR-level."""
        files = ["/src/app.ts", "/utils/b.ts"]
        _, requests_mock, _ = self._run_scaffold(files)

        for call in requests_mock.post.call_args_list:
            body = call[1]["json"]
            assert "threadContext" not in body

    def test_consolidated_thread_is_only_api_call(self):
        """The consolidated review comment is the only POST (PR-level, no file context)."""
        files = ["/src/app.ts"]
        _, requests_mock, _ = self._run_scaffold(files)

        assert requests_mock.post.call_count == 1
        body = requests_mock.post.call_args_list[0][1]["json"]
        assert "threadContext" not in body

    def test_overall_thread_has_no_file_context(self):
        """Overall PR summary thread does not include threadContext."""
        files = ["/src/app.ts"]
        _, requests_mock, _ = self._run_scaffold(files)

        # Last call is for the overall summary thread
        last_call_kwargs = requests_mock.post.call_args_list[-1][1]
        body = last_call_kwargs["json"]
        assert "threadContext" not in body

    def test_file_entries_in_review_state(self):
        """ReviewState.files contains an entry for each scaffolded file."""
        files = ["/src/app.ts", "/utils/helpers.ts"]
        result, _, _ = self._run_scaffold(files)

        assert "/src/app.ts" in result.files
        assert "/utils/helpers.ts" in result.files

    def test_folder_entries_in_review_state(self):
        """ReviewState.folders contains an entry for each folder."""
        files = ["/src/app.ts", "/utils/helpers.ts"]
        result, _, _ = self._run_scaffold(files)

        assert "src" in result.folders
        assert "utils" in result.folders

    def test_file_entry_thread_ids_zero(self):
        """FileEntry has no per-file thread (rendered inline in the consolidated comment)."""
        files = ["/src/app.ts"]
        result, _, _ = self._run_scaffold(files)

        entry = result.files["/src/app.ts"]
        assert entry.threadId == 0
        assert entry.commentId == 0

    def test_folder_entry_has_files(self):
        """FolderGroup has files list after scaffolding."""
        files = ["/src/app.ts"]
        result, _, _ = self._run_scaffold(files)

        folder = result.folders["src"]
        assert "/src/app.ts" in folder.files

    def test_overall_summary_thread_ids_populated(self):
        """OverallSummary has non-zero threadId and commentId after scaffolding."""
        files = ["/src/app.ts"]
        result, _, _ = self._run_scaffold(files)

        assert result.overallSummary.threadId != 0
        assert result.overallSummary.commentId != 0

    def test_file_entry_status_is_unreviewed(self):
        """FileEntry status is 'unreviewed' after scaffolding."""
        files = ["/src/app.ts"]
        result, _, _ = self._run_scaffold(files)

        entry = result.files["/src/app.ts"]
        assert entry.status == ReviewStatus.UNREVIEWED.value

    def test_folder_entry_is_folder_group(self):
        """FolderGroup is a lightweight grouping with files list."""
        files = ["/src/app.ts"]
        result, _, _ = self._run_scaffold(files)

        folder = result.folders["src"]
        assert isinstance(folder.files, list)

    def test_folder_entry_lists_its_files(self):
        """FolderEntry.files lists the file paths belonging to the folder."""
        files = ["/src/app.ts", "/src/utils.ts"]
        result, _, _ = self._run_scaffold(files)

        folder = result.folders["src"]
        assert "/src/app.ts" in folder.files
        assert "/src/utils.ts" in folder.files

    def test_save_review_state_called_once(self):
        """save_review_state is called once with the completed ReviewState."""
        files = ["/src/app.ts"]
        result, _, save_mock = self._run_scaffold(files)

        assert save_mock.call_count == 1
        # The call uses the completed ReviewState
        save_mock.assert_called_with(result)

    def test_saved_state_has_populated_overall_and_zero_file_threads(self):
        """The saved state has the consolidated thread populated and no per-file threads."""
        files = ["/src/app.ts"]
        _, _, save_mock = self._run_scaffold(files)

        saved = save_mock.call_args_list[-1][0][0]
        assert saved.overallSummary.threadId != 0
        assert saved.overallSummary.commentId != 0
        # File entries are populated but carry no per-file thread
        assert "/src/app.ts" in saved.files
        assert saved.files["/src/app.ts"].threadId == 0
        # Folder groups are populated (lightweight, no API calls)
        assert "src" in saved.folders
        assert "/src/app.ts" in saved.folders["src"].files

    def test_root_level_file_assigned_to_root_folder(self):
        """Files at the repository root are assigned to the 'root' folder."""
        files = ["/README.md"]
        result, _, _ = self._run_scaffold(files)

        assert "/README.md" in result.files
        assert "root" in result.folders
        entry = result.files["/README.md"]
        assert entry.folder == "root"
        assert entry.fileName == "README.md"

    def test_multiple_files_same_folder_one_folder_group(self):
        """Multiple files in the same folder produce one folder group and one POST."""
        files = ["/src/a.ts", "/src/b.ts", "/src/c.ts"]
        result, requests_mock, _ = self._run_scaffold(files)

        # Everything is rendered inline in the single consolidated comment.
        assert requests_mock.post.call_count == 1
        assert "src" in result.folders
        assert len(result.folders["src"].files) == 3

    def test_scaffolded_utc_is_set(self):
        """ReviewState.scaffoldedUtc is a non-empty ISO timestamp."""
        files = ["/src/app.ts"]
        result, _, _ = self._run_scaffold(files)

        assert result.scaffoldedUtc
        assert "T" in result.scaffoldedUtc  # ISO format check

    def test_prints_completion_message(self, capsys):
        """Prints a completion message after scaffolding succeeds."""
        with patch(
            "agentic_devtools.cli.azure_devops.review_scaffold_orchestration.load_review_state",
            side_effect=FileNotFoundError,
        ):
            with patch("agentic_devtools.cli.azure_devops.review_scaffold_fresh.save_review_state"):
                requests_mock = MagicMock()
                id_gen = count(1)

                def make_resp(*args, **kwargs):
                    i = next(id_gen)
                    return _make_post_response(i * 100, i * 100 + 1)

                requests_mock.post.side_effect = make_resp

                scaffold_review_threads(
                    pull_request_id=_PR_ID,
                    files=["/src/app.ts"],
                    config=_make_config(),
                    repo_id=_REPO_ID,
                    repo_name=_REPO,
                    latest_iteration_id=1,
                    requests_module=requests_mock,
                    headers={},
                )

        out = capsys.readouterr().out
        assert "Scaffolding complete" in out
        assert f"PR {_PR_ID}" in out
