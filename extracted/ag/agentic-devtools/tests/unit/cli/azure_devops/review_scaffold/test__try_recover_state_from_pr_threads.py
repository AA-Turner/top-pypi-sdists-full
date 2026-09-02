"""Tests for _try_recover_state_from_pr_threads internal function (consolidated model).

In the consolidated single-comment model, recovery looks only for the **one**
``v2`` consolidated comment on the PR (via ``find_consolidated_thread``). Legacy
``v1`` per-thread comments are intentionally ignored.

Recovery intentionally does NOT refresh (PATCH) the consolidated comment with the
recovered state.  The recovered state has all files reset to ``unreviewed`` and a
PATCH at recovery time would permanently erase review history that is still visible
on the PR.  Instead, recovery only reuses the existing thread/comment IDs and
persists the local state; subsequent file-review operations will PATCH the correct
thread with accurate content.
"""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.review_scaffold import _try_recover_state_from_pr_threads
from agentic_devtools.cli.azure_devops.review_state import ReviewState

_ORG = "https://dev.azure.com/testorg"
_PROJECT = "TestProject"
_REPO = "test-repo"
_REPO_ID = "repo-guid"
_PR_ID = 12345


def _make_config():
    return AzureDevOpsConfig(organization=_ORG, project=_PROJECT, repository=_REPO)


def _make_consolidated_thread(thread_id=900, comment_id=901):
    """Create a mock ADO thread carrying the v2 consolidated marker."""
    marker = f"<!-- agdt-review:v2 type:consolidated pr:{_PR_ID} commit:abc123 -->"
    return {
        "id": thread_id,
        "status": "closed",
        "comments": [{"id": comment_id, "content": f"{marker}\n# PR Review"}],
    }


class TestTryRecoverStateFromPrThreads:
    """Tests for the consolidated-model recovery mechanism."""

    @patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state")
    def test_returns_none_when_no_threads(self, save_mock):
        """Returns None when the API returns no threads."""
        requests_mock = MagicMock()
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {"value": []}
        requests_mock.get.return_value = resp

        result = _try_recover_state_from_pr_threads(
            pull_request_id=_PR_ID,
            files=["/src/a.ts"],
            config=_make_config(),
            repo_id=_REPO_ID,
            repo_name=_REPO,
            latest_iteration_id=5,
            requests_module=requests_mock,
            headers={},
            commit_hash="abc123",
            model_id="gpt-5",
        )

        assert result is None
        save_mock.assert_not_called()

    @patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state")
    def test_returns_none_when_no_consolidated_comment(self, save_mock):
        """Returns None when threads exist but none carry the v2 consolidated marker."""
        requests_mock = MagicMock()
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {
            "value": [
                {"id": 100, "status": "active", "comments": [{"id": 1, "content": "Regular comment"}]},
                # A legacy v1 comment must be ignored.
                {
                    "id": 200,
                    "status": "closed",
                    "comments": [{"id": 2, "content": f"<!-- agdt-review:v1 type:overall-summary pr:{_PR_ID} -->\n#"}],
                },
            ]
        }
        requests_mock.get.return_value = resp

        result = _try_recover_state_from_pr_threads(
            pull_request_id=_PR_ID,
            files=["/src/a.ts"],
            config=_make_config(),
            repo_id=_REPO_ID,
            repo_name=_REPO,
            latest_iteration_id=5,
            requests_module=requests_mock,
            headers={},
            commit_hash="abc123",
            model_id="gpt-5",
        )

        assert result is None
        save_mock.assert_not_called()

    @patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state")
    def test_returns_none_when_fetch_fails(self, save_mock, capsys):
        """Returns None and prints a warning when the threads API call fails."""
        requests_mock = MagicMock()
        requests_mock.get.side_effect = Exception("Network error")

        result = _try_recover_state_from_pr_threads(
            pull_request_id=_PR_ID,
            files=["/src/a.ts"],
            config=_make_config(),
            repo_id=_REPO_ID,
            repo_name=_REPO,
            latest_iteration_id=5,
            requests_module=requests_mock,
            headers={},
            commit_hash="abc123",
            model_id="gpt-5",
        )

        assert result is None
        err = capsys.readouterr().err
        assert "Could not fetch PR threads for recovery check" in err
        save_mock.assert_not_called()

    @patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state")
    def test_recovers_from_consolidated_comment(self, save_mock):
        """Recovers state pointing at the existing consolidated comment without patching it."""
        requests_mock = MagicMock()
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {"value": [_make_consolidated_thread(thread_id=900, comment_id=901)]}
        requests_mock.get.return_value = resp

        result = _try_recover_state_from_pr_threads(
            pull_request_id=_PR_ID,
            files=["/src/a.ts", "/src/b.ts"],
            config=_make_config(),
            repo_id=_REPO_ID,
            repo_name=_REPO,
            latest_iteration_id=5,
            requests_module=requests_mock,
            headers={},
            commit_hash="abc123def",
            model_id="gpt-5",
        )

        assert result is not None
        assert isinstance(result, ReviewState)
        assert result.prId == _PR_ID
        # Points at the existing consolidated comment.
        assert result.overallSummary.threadId == 900
        assert result.overallSummary.commentId == 901
        # No per-file or activity-log threads in the consolidated model.
        assert result.activityLogThreadId == 0
        assert result.files["/src/a.ts"].threadId == 0
        assert result.files["/src/b.ts"].threadId == 0
        # All files reset to unreviewed.
        assert result.files["/src/a.ts"].status == "unreviewed"
        # State is saved; the existing consolidated comment is NOT patched.
        save_mock.assert_called_once()
        # Confirm no API PATCH calls were made during recovery.
        requests_mock.patch.assert_not_called()

    @patch("agentic_devtools.cli.azure_devops.review_scaffold.save_review_state")
    def test_recovers_without_model_id_and_explicit_now(self, save_mock):
        """Empty model_id and explicit now cover the non-default branches."""
        requests_mock = MagicMock()
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {"value": [_make_consolidated_thread(thread_id=910, comment_id=911)]}
        requests_mock.get.return_value = resp

        fixed_now = datetime(2026, 6, 18, 12, 0, 0, tzinfo=timezone.utc)
        result = _try_recover_state_from_pr_threads(
            pull_request_id=_PR_ID,
            files=["/src/a.ts"],
            config=_make_config(),
            repo_id=_REPO_ID,
            repo_name=_REPO,
            latest_iteration_id=5,
            requests_module=requests_mock,
            headers={},
            commit_hash="abc123",
            model_id="",
            now=fixed_now,
        )

        assert result is not None
        assert result.overallSummary.threadId == 910
        assert result.scaffoldedUtc == fixed_now.isoformat()
        # The consolidated comment is NOT patched during recovery.
        requests_mock.patch.assert_not_called()
