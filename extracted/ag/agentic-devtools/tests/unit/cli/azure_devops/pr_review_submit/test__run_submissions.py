"""Tests for _run_submissions."""

from types import SimpleNamespace
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.mark_reviewed import MarkFilesReviewedResult
from agentic_devtools.cli.azure_devops.pr_review_submit import _run_submissions
from agentic_devtools.submission_manager import SubmissionStatus


class _FakeManager:
    def __init__(self, finals, *, lose_items=False):
        # finals: list of (status, attempts, error) in enqueue order
        self._finals = finals
        self._idx = 0
        self._by_id = {}
        self.lose_items = lose_items
        self.shutdown_called = False
        self.enqueued = []

    def enqueue(self, pr_id, file_path, outcome, summary, suggestions):
        item_id = f"id{self._idx}"
        status, attempts, error = self._finals[self._idx]
        self._by_id[item_id] = SimpleNamespace(id=item_id, status=status, attempts=attempts, error_message=error)
        self._idx += 1
        self.enqueued.append((pr_id, file_path, outcome, summary, suggestions))
        return SimpleNamespace(id=item_id)

    def shutdown(self, wait=True):
        self.shutdown_called = True

    def get_item(self, item_id):
        if self.lose_items:
            return None
        return self._by_id.get(item_id)


def _submittable(file_key, file_path):
    return {
        "fileKey": file_key,
        "filePath": file_path,
        "item": {"file_path": file_path, "outcome": "approve", "summary": "ok", "suggestions": None},
    }


class TestRunSubmissions:
    def test_posted_outcome(self):
        manager = _FakeManager([(SubmissionStatus.SUCCEEDED, 1, None)])
        outcomes = _run_submissions(manager, 5, [_submittable("a", "/a")])
        assert manager.shutdown_called is True
        assert outcomes["a"] == {"status": "posted", "error": None, "attempts": 1}
        assert manager.enqueued[0] == (5, "/a", "approve", "ok", None)

    def test_failed_outcome(self):
        manager = _FakeManager([(SubmissionStatus.FAILED, 3, "boom")])
        outcomes = _run_submissions(manager, 5, [_submittable("a", "/a")])
        assert outcomes["a"] == {"status": "failed", "error": "boom", "attempts": 3}

    def test_lost_item_outcome(self):
        manager = _FakeManager([(SubmissionStatus.SUCCEEDED, 0, None)], lose_items=True)
        outcomes = _run_submissions(manager, 5, [_submittable("a", "/a")])
        assert outcomes["a"] == {"status": "failed", "error": "submission item lost", "attempts": 0}

    @patch(
        "agentic_devtools.cli.azure_devops.mark_reviewed.mark_files_reviewed",
        return_value=MarkFilesReviewedResult(synced_paths=["/a"], failed_paths=[]),
    )
    @patch("agentic_devtools.cli.azure_devops.pr_review_submit.require_requests", create=True)
    @patch("agentic_devtools.cli.azure_devops.pr_review_submit.get_auth_headers", return_value={})
    @patch("agentic_devtools.cli.azure_devops.pr_review_submit.get_pat", return_value="pat")
    @patch("agentic_devtools.cli.azure_devops.pr_review_submit.execute_cascade")
    @patch("agentic_devtools.cli.azure_devops.pr_review_submit.cascade_overall_summary_update")
    def test_finalizes_overall_summary_after_queue_drains(
        self, mock_cascade, mock_execute, mock_get_pat, mock_get_headers, mock_require_requests, mock_mark
    ):
        """Successful batch submissions update the overall summary after draining."""
        manager = _FakeManager([(SubmissionStatus.SUCCEEDED, 1, None)])
        mock_execute.return_value = SimpleNamespace(blocked=[])
        mock_require_requests.return_value = object()
        with patch("agentic_devtools.cli.azure_devops.pr_review_submit.read_modify_write_review_state") as state:
            state.return_value.__enter__.return_value = SimpleNamespace(
                organization="https://dev.azure.com/org",
                project="project",
                repoName="repo",
                repoId="repo-guid",
            )
            state.return_value.__exit__.return_value = False
            with patch(
                "agentic_devtools.cli.azure_devops.pr_review_submit.load_review_state",
                return_value=state.return_value.__enter__.return_value,
            ):
                outcomes = _run_submissions(manager, 5, [_submittable("a", "/a")], True)

        assert outcomes["a"]["status"] == "posted"
        mock_cascade.assert_called_once()
        mock_execute.assert_called_once()

    def test_batch_mark_failure_marks_successful_items_failed(self):
        """A failed batch viewed-status update changes successful outcomes to failed."""
        manager = _FakeManager([(SubmissionStatus.SUCCEEDED, 1, None)])
        with (
            patch(
                "agentic_devtools.cli.azure_devops.mark_reviewed.mark_files_reviewed",
                return_value=MarkFilesReviewedResult(
                    synced_paths=[],
                    failed_paths=["/a"],
                    error="Failed to mark reviewed files for the pull request",
                ),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_submit.load_review_state",
                return_value=SimpleNamespace(repoId="repo-guid"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_submit.AzureDevOpsConfig.from_state",
                return_value=SimpleNamespace(),
            ),
            patch("agentic_devtools.cli.azure_devops.pr_review_submit.read_modify_write_review_state"),
        ):
            outcomes = _run_submissions(manager, 5, [_submittable("a", "/a")], True)

        assert outcomes["a"]["status"] == "failed"

    def test_batch_mark_failure_only_marks_unsynchronized_items_failed(self):
        """Only paths missing viewed-status sync are converted to failed outcomes."""
        manager = _FakeManager([(SubmissionStatus.SUCCEEDED, 1, None), (SubmissionStatus.SUCCEEDED, 1, None)])
        with (
            patch(
                "agentic_devtools.cli.azure_devops.mark_reviewed.mark_files_reviewed",
                return_value=MarkFilesReviewedResult(
                    synced_paths=["/a"],
                    failed_paths=["/b"],
                    error="Failed to sync viewed status for some files",
                ),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_submit.load_review_state",
                return_value=SimpleNamespace(repoId="repo-guid"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_submit.AzureDevOpsConfig.from_state",
                return_value=SimpleNamespace(),
            ),
        ):
            outcomes = _run_submissions(manager, 5, [_submittable("a", "/a"), _submittable("b", "/b")], True)

        assert outcomes["a"]["status"] == "posted"
        assert outcomes["b"]["status"] == "failed"

    def test_batch_mark_exception_marks_all_successful_items_failed(self):
        """Unexpected batch finalization exceptions keep successful submissions retriable."""
        manager = _FakeManager([(SubmissionStatus.SUCCEEDED, 1, None)])
        with (
            patch(
                "agentic_devtools.cli.azure_devops.mark_reviewed.mark_files_reviewed",
                side_effect=RuntimeError("boom"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_submit.load_review_state",
                return_value=SimpleNamespace(repoId="repo-guid"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_submit.AzureDevOpsConfig.from_state",
                return_value=SimpleNamespace(),
            ),
        ):
            outcomes = _run_submissions(manager, 5, [_submittable("a", "/a")], True)

        assert outcomes["a"] == {"status": "failed", "error": "boom", "attempts": 1}

    def test_batch_finalization_exception_marks_successful_items_failed(self):
        """An overall-summary cascade failure changes successful outcomes to failed."""
        manager = _FakeManager([(SubmissionStatus.SUCCEEDED, 1, None)])
        with (
            patch(
                "agentic_devtools.cli.azure_devops.mark_reviewed.mark_files_reviewed",
                return_value=MarkFilesReviewedResult(synced_paths=["/a"], failed_paths=[]),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_submit.load_review_state",
                return_value=SimpleNamespace(repoId="repo-guid"),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_submit.AzureDevOpsConfig.from_state",
                return_value=SimpleNamespace(),
            ),
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_submit.read_modify_write_review_state",
                side_effect=RuntimeError("cascade unavailable"),
            ),
        ):
            outcomes = _run_submissions(manager, 5, [_submittable("a", "/a")], True)

        assert outcomes["a"] == {"status": "failed", "error": "cascade unavailable", "attempts": 1}

    def test_skips_shared_finalization_when_no_items_succeeded(self):
        """A batch with no successful submissions skips shared finalization."""
        outcomes = _run_submissions(
            _FakeManager([(SubmissionStatus.FAILED, 1, "boom")]),
            5,
            [_submittable("a", "/a")],
            True,
        )

        assert outcomes["a"]["status"] == "failed"

    @patch(
        "agentic_devtools.cli.azure_devops.mark_reviewed.mark_files_reviewed",
        return_value=MarkFilesReviewedResult(synced_paths=["/a"], failed_paths=[]),
    )
    @patch("agentic_devtools.cli.azure_devops.pr_review_submit.get_auth_headers", return_value={})
    @patch("agentic_devtools.cli.azure_devops.pr_review_submit.get_pat", return_value="pat")
    @patch("agentic_devtools.cli.azure_devops.pr_review_submit.execute_cascade")
    @patch("agentic_devtools.cli.azure_devops.pr_review_submit.cascade_overall_summary_update")
    def test_blocked_cascade_marks_successful_items_failed(
        self, mock_cascade, mock_execute, mock_get_pat, mock_get_headers, mock_mark
    ):
        """A blocked overall-summary cascade changes successful outcomes to failed."""
        mock_execute.return_value = SimpleNamespace(blocked=[1])
        state = SimpleNamespace(
            organization="https://dev.azure.com/org",
            project="project",
            repoName="repo",
            repoId="repo-guid",
        )
        with (
            patch("agentic_devtools.cli.azure_devops.pr_review_submit.load_review_state", return_value=state),
            patch("agentic_devtools.cli.azure_devops.pr_review_submit.read_modify_write_review_state") as context,
        ):
            context.return_value.__enter__.return_value = state
            context.return_value.__exit__.return_value = False
            outcomes = _run_submissions(
                _FakeManager([(SubmissionStatus.SUCCEEDED, 1, None)]),
                5,
                [_submittable("a", "/a")],
                True,
            )

        assert outcomes["a"]["status"] == "failed"
