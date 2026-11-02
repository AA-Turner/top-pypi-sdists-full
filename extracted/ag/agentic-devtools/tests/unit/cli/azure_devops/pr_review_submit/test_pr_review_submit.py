"""Tests for the pr_review_submit worker."""

import json
from contextlib import ExitStack, contextmanager
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.azure_devops.pr_review_submit import pr_review_submit
from agentic_devtools.file_locking import FileLockError

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_submit"


@contextmanager
def _noop_lock(pull_request_id, *args, **kwargs):
    yield object()


@contextmanager
def _raising_lock(pull_request_id, *args, **kwargs):
    raise FileLockError("held")
    yield  # pragma: no cover


@contextmanager
def _state_txn(state):
    yield state


def _submittable(file_key="a", file_path="/a"):
    return {
        "fileKey": file_key,
        "filePath": file_path,
        "item": {"file_path": file_path, "outcome": "approve", "summary": "ok", "suggestions": None},
    }


def _common_patches(stack, answers_dir, *, classify, commit_value="abc", lock=_noop_lock):
    resolve_answers_dir = stack.enter_context(patch(f"{_MODULE}.resolve_answers_dir", return_value=answers_dir))
    stack.enter_context(patch(f"{_MODULE}.read_ledger_entries", return_value=[]))
    stack.enter_context(patch(f"{_MODULE}.latest_accepted_by_file_key", return_value={}))
    stack.enter_context(patch(f"{_MODULE}.classify_accepted_answers", return_value=classify))
    stack.enter_context(patch(f"{_MODULE}.get_value", return_value=commit_value))
    stack.enter_context(patch(f"{_MODULE}.pipeline_lock", new=lock))
    return resolve_answers_dir


def _read_result(answers_dir):
    return json.loads((answers_dir / "submit-result.json").read_text(encoding="utf-8"))


class TestPrReviewSubmit:
    def test_missing_pr_returns_2(self):
        with patch(f"{_MODULE}.get_pull_request_id", return_value=None):
            assert pr_review_submit() == 2

    def test_dry_run_skips_manager_and_writes_result(self, tmp_path):
        answers_dir = tmp_path / "answers"
        build = MagicMock()
        run = MagicMock()
        with ExitStack() as stack:
            resolve_answers_dir = _common_patches(stack, answers_dir, classify=([_submittable()], [], []))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", build))
            stack.enter_context(patch(f"{_MODULE}._run_submissions", run))
            rc = pr_review_submit(pull_request_id=5, dry_run=True, now_fn=lambda: "t")
        assert rc == 0
        resolve_answers_dir.assert_called_once_with(5, backfill=False)
        build.assert_not_called()
        run.assert_not_called()
        result = _read_result(answers_dir)
        assert result["dryRun"] is True
        assert result["accepted"] == ["a"]
        assert result["posted"] == []
        assert result["commitHash"] == "abc"

    def test_commit_hash_from_ledger_entry(self, tmp_path):
        """Full commitHash is taken from ledger entries, not the short state key."""
        full_hash = "a" * 40
        answers_dir = tmp_path / "answers"
        with ExitStack() as stack:
            stack.enter_context(patch(f"{_MODULE}.resolve_answers_dir", return_value=answers_dir))
            stack.enter_context(patch(f"{_MODULE}.read_ledger_entries", return_value=[]))
            stack.enter_context(
                patch(
                    f"{_MODULE}.latest_accepted_by_file_key",
                    return_value={
                        "k": {"commitHash": full_hash, "filePath": "/a", "status": "complete", "outcome": "approve"}
                    },
                )
            )
            stack.enter_context(patch(f"{_MODULE}.classify_accepted_answers", return_value=([], [], [])))
            stack.enter_context(patch(f"{_MODULE}.get_value", return_value="short"))
            stack.enter_context(patch(f"{_MODULE}.pipeline_lock", new=_noop_lock))
            rc = pr_review_submit(pull_request_id=5, dry_run=True, now_fn=lambda: "t")
        assert rc == 0
        assert _read_result(answers_dir)["commitHash"] == full_hash

    def test_commit_hash_falls_back_to_state_when_ledger_empty(self, tmp_path):
        """Falls back to review.commit_hash_short state key when ledger has no entries."""
        answers_dir = tmp_path / "answers"
        with ExitStack() as stack:
            resolve_answers_dir = _common_patches(stack, answers_dir, classify=([], [], []), commit_value="short123")
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=True))
            rc = pr_review_submit(pull_request_id=5)
        assert rc == 0
        resolve_answers_dir.assert_called_once_with(5, backfill=False)
        assert _read_result(answers_dir)["commitHash"] == "short123"

    def test_empty_submittable_skips_manager(self, tmp_path):
        answers_dir = tmp_path / "answers"
        build = MagicMock()
        with ExitStack() as stack:
            resolve_answers_dir = _common_patches(stack, answers_dir, classify=([], [], []), commit_value=None)
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=False))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", build))
            rc = pr_review_submit(pull_request_id=5)
        assert rc == 0
        resolve_answers_dir.assert_called_once_with(5, backfill=True)
        build.assert_not_called()
        result = _read_result(answers_dir)
        assert result["commitHash"] == ""
        assert result["dryRun"] is False

    def test_real_submit_posts_and_finalizes(self, tmp_path):
        answers_dir = tmp_path / "answers"
        with ExitStack() as stack:
            resolve_answers_dir = _common_patches(stack, answers_dir, classify=([_submittable()], [], []))
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=False))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", return_value=MagicMock()))
            stack.enter_context(
                patch(
                    f"{_MODULE}._run_submissions",
                    return_value={"a": {"status": "posted", "error": None, "attempts": 1}},
                )
            )
            finalize = stack.enter_context(patch(f"{_MODULE}._finalize_consolidated_comment"))
            rc = pr_review_submit(pull_request_id=5, dry_run=False)
        assert rc == 0
        resolve_answers_dir.assert_called_once_with(5, backfill=True)
        assert _read_result(answers_dir)["posted"] == ["a"]
        finalize.assert_called_once_with(5, None)

    def test_finalize_error_still_writes_result(self, tmp_path, capsys):
        """Completion-render failure must not lose the already-built result file."""
        answers_dir = tmp_path / "answers"
        with ExitStack() as stack:
            _common_patches(stack, answers_dir, classify=([_submittable()], [], []))
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=False))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", return_value=MagicMock()))
            stack.enter_context(
                patch(
                    f"{_MODULE}._run_submissions",
                    return_value={"a": {"status": "posted", "error": None, "attempts": 1}},
                )
            )
            stack.enter_context(patch(f"{_MODULE}._finalize_consolidated_comment", side_effect=OSError("net")))
            rc = pr_review_submit(pull_request_id=5, dry_run=False)
        assert rc == 0
        assert _read_result(answers_dir)["posted"] == ["a"]
        assert "Warning" in capsys.readouterr().err

    def test_failed_outcome_returns_1(self, tmp_path):
        answers_dir = tmp_path / "answers"
        with ExitStack() as stack:
            _common_patches(stack, answers_dir, classify=([_submittable()], [], []))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", return_value=MagicMock()))
            stack.enter_context(patch(f"{_MODULE}._finalize_consolidated_comment"))
            stack.enter_context(
                patch(
                    f"{_MODULE}._run_submissions",
                    return_value={"a": {"status": "failed", "error": "boom", "attempts": 2}},
                )
            )
            rc = pr_review_submit(pull_request_id=5, dry_run=False)
        assert rc == 1
        assert _read_result(answers_dir)["failed"][0]["error"] == "boom"

    def test_failed_outcome_does_not_complete_session(self, tmp_path):
        """Do not close the review session when any current submission failed."""
        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            OverallSummary,
            ReviewSession,
            ReviewState,
        )

        answers_dir = tmp_path / "answers"
        session = ReviewSession(
            sessionId="session-submit",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00+00:00",
            status="in_progress",
        )
        real_review_state = ReviewState(
            prId=5,
            repoId="repo-guid",
            repoName="repo",
            project="proj",
            organization="https://dev.azure.com/org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=1, commentId=2, status="approved"),
            files={"/src/a.py": FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status="approved")},
            sessions=[session],
        )

        with ExitStack() as stack:
            _common_patches(stack, answers_dir, classify=([_submittable()], [], []))
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=False))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", return_value=MagicMock()))
            stack.enter_context(
                patch(
                    f"{_MODULE}._run_submissions",
                    return_value={"a": {"status": "failed", "error": "boom", "attempts": 2}},
                )
            )
            txn = stack.enter_context(
                patch(f"{_MODULE}.read_modify_write_review_state", return_value=_state_txn(real_review_state))
            )
            complete = stack.enter_context(patch(f"{_MODULE}.complete_active_session"))
            finalize = stack.enter_context(patch(f"{_MODULE}._finalize_consolidated_comment"))

            rc = pr_review_submit(pull_request_id=5, dry_run=False)

        assert rc == 1
        txn.assert_not_called()
        complete.assert_not_called()
        finalize.assert_called_once_with(5, None)
        assert session.status == "in_progress"
        assert session.completedUtc is None

    def test_lock_contention_returns_1(self, tmp_path):
        answers_dir = tmp_path / "answers"
        get_value = MagicMock(return_value="abc")
        resolve_answers_dir = MagicMock(return_value=answers_dir)
        read_ledger_entries = MagicMock(return_value=[])
        classify_accepted_answers = MagicMock(return_value=([_submittable()], [], []))
        with ExitStack() as stack:
            stack.enter_context(patch(f"{_MODULE}.resolve_answers_dir", resolve_answers_dir))
            stack.enter_context(patch(f"{_MODULE}.read_ledger_entries", read_ledger_entries))
            stack.enter_context(patch(f"{_MODULE}.latest_accepted_by_file_key", return_value={}))
            stack.enter_context(patch(f"{_MODULE}.classify_accepted_answers", classify_accepted_answers))
            stack.enter_context(patch(f"{_MODULE}.get_value", get_value))
            stack.enter_context(patch(f"{_MODULE}.pipeline_lock", new=_raising_lock))
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=False))
            rc = pr_review_submit(pull_request_id=5)
        assert rc == 1
        get_value.assert_not_called()
        resolve_answers_dir.assert_not_called()
        read_ledger_entries.assert_not_called()
        classify_accepted_answers.assert_not_called()
        assert not (answers_dir / "submit-result.json").exists()

    def test_missing_review_state_returns_2(self, tmp_path):
        answers_dir = tmp_path / "answers"
        with ExitStack() as stack:
            _common_patches(stack, answers_dir, classify=([_submittable()], [], []))
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=False))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", side_effect=FileNotFoundError))
            rc = pr_review_submit(pull_request_id=5)
        assert rc == 2
        assert not (answers_dir / "submit-result.json").exists()

    def test_real_submit_marks_session_completed_before_finalize(self, tmp_path):
        """complete_active_session must be called before _finalize_consolidated_comment.

        Regression guard for issue #1181: the Activity Log embedded in the
        consolidated PR comment must reflect the terminal ``"completed"`` status
        even when the workflow completion step is never reached (submit-only path).
        """
        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            OverallSummary,
            ReviewSession,
            ReviewState,
        )

        answers_dir = tmp_path / "answers"

        session = ReviewSession(
            sessionId="session-submit",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00+00:00",
            status="in_progress",
        )
        real_review_state = ReviewState(
            prId=5,
            repoId="repo-guid",
            repoName="repo",
            project="proj",
            organization="https://dev.azure.com/org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=1, commentId=2, status="approved"),
            files={"/src/a.py": FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status="approved")},
            sessions=[session],
        )

        with ExitStack() as stack:
            _common_patches(stack, answers_dir, classify=([_submittable()], [], []))
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=False))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", return_value=MagicMock()))
            stack.enter_context(
                patch(
                    f"{_MODULE}._run_submissions",
                    return_value={"a": {"status": "posted", "error": None, "attempts": 1}},
                )
            )
            txn = stack.enter_context(
                patch(f"{_MODULE}.read_modify_write_review_state", return_value=_state_txn(real_review_state))
            )
            finalize = stack.enter_context(patch(f"{_MODULE}._finalize_consolidated_comment"))

            rc = pr_review_submit(pull_request_id=5, dry_run=False)

        assert rc == 0
        # Session must be marked completed before the finalization render
        assert session.status == "completed"
        assert session.completedUtc is not None
        txn.assert_called_once_with(5)
        finalize.assert_called_once_with(5, None)

    def test_real_submit_leaves_session_in_progress_when_review_incomplete(self, tmp_path):
        """A partial batch submit must not mark the session completed.

        Regression guard for issue #1181's refined spec: session completion
        is only appropriate once every file has reached a terminal status
        (``is_review_complete()``), not merely because *some* answers were
        submitted in this batch.
        """
        from agentic_devtools.cli.azure_devops.review_state import (
            FileEntry,
            OverallSummary,
            ReviewSession,
            ReviewState,
        )

        answers_dir = tmp_path / "answers"

        session = ReviewSession(
            sessionId="session-submit",
            modelId="model-a",
            startedUtc="2026-01-01T00:00:00+00:00",
            status="in_progress",
        )
        real_review_state = ReviewState(
            prId=5,
            repoId="repo-guid",
            repoName="repo",
            project="proj",
            organization="https://dev.azure.com/org",
            latestIterationId=1,
            scaffoldedUtc="2026-01-01T00:00:00+00:00",
            overallSummary=OverallSummary(threadId=1, commentId=2, status="in-progress"),
            files={
                "/src/a.py": FileEntry(threadId=0, commentId=0, folder="src", fileName="a.py", status="approved"),
                "/src/b.py": FileEntry(threadId=0, commentId=0, folder="src", fileName="b.py", status="unreviewed"),
            },
            sessions=[session],
        )

        with ExitStack() as stack:
            _common_patches(stack, answers_dir, classify=([_submittable()], [], []))
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=False))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", return_value=MagicMock()))
            stack.enter_context(
                patch(
                    f"{_MODULE}._run_submissions",
                    return_value={"a": {"status": "posted", "error": None, "attempts": 1}},
                )
            )
            txn = stack.enter_context(
                patch(f"{_MODULE}.read_modify_write_review_state", return_value=_state_txn(real_review_state))
            )
            finalize = stack.enter_context(patch(f"{_MODULE}._finalize_consolidated_comment"))

            rc = pr_review_submit(pull_request_id=5, dry_run=False)

        assert rc == 0
        assert session.status == "in_progress"
        assert session.completedUtc is None
        txn.assert_called_once_with(5)
        finalize.assert_called_once_with(5, None)

    def test_real_submit_leaves_session_in_progress_when_latest_answers_are_skipped_or_stale(self, tmp_path):
        """Terminal review state alone is insufficient when the latest answer set is incomplete."""
        answers_dir = tmp_path / "answers"

        with ExitStack() as stack:
            _common_patches(
                stack,
                answers_dir,
                classify=(
                    [_submittable()],
                    [{"fileKey": "b", "reason": "status:pending"}],
                    [{"fileKey": "c", "errors": ["stale commitHash"]}],
                ),
            )
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=False))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", return_value=MagicMock()))
            stack.enter_context(
                patch(
                    f"{_MODULE}._run_submissions",
                    return_value={"a": {"status": "posted", "error": None, "attempts": 1}},
                )
            )
            txn = stack.enter_context(patch(f"{_MODULE}.read_modify_write_review_state"))
            finalize = stack.enter_context(patch(f"{_MODULE}._finalize_consolidated_comment"))

            rc = pr_review_submit(pull_request_id=5, dry_run=False)

        assert rc == 0
        txn.assert_not_called()
        finalize.assert_called_once_with(5, None)

    def test_dry_run_does_not_mark_session_completed(self, tmp_path):
        """Dry-run submit must not mark the session completed or call finalize."""
        answers_dir = tmp_path / "answers"
        with ExitStack() as stack:
            _common_patches(stack, answers_dir, classify=([_submittable()], [], []))
            mock_txn = stack.enter_context(patch(f"{_MODULE}.read_modify_write_review_state"))
            finalize = stack.enter_context(patch(f"{_MODULE}._finalize_consolidated_comment"))
            rc = pr_review_submit(pull_request_id=5, dry_run=True, now_fn=lambda: "t")

        assert rc == 0
        mock_txn.assert_not_called()
        finalize.assert_not_called()

    def test_session_completion_error_does_not_block_finalize(self, tmp_path, capsys):
        """A failure marking the session complete must not prevent finalization."""
        answers_dir = tmp_path / "answers"
        with ExitStack() as stack:
            _common_patches(stack, answers_dir, classify=([_submittable()], [], []))
            stack.enter_context(patch(f"{_MODULE}.is_dry_run", return_value=False))
            stack.enter_context(patch(f"{_MODULE}._build_submission_manager", return_value=MagicMock()))
            stack.enter_context(
                patch(
                    f"{_MODULE}._run_submissions",
                    return_value={"a": {"status": "posted", "error": None, "attempts": 1}},
                )
            )
            stack.enter_context(
                patch(f"{_MODULE}.read_modify_write_review_state", side_effect=OSError("state read error"))
            )
            finalize = stack.enter_context(patch(f"{_MODULE}._finalize_consolidated_comment"))

            rc = pr_review_submit(pull_request_id=5, dry_run=False)

        assert rc == 0
        assert "Warning: could not mark review session completed" in capsys.readouterr().err
        finalize.assert_called_once_with(5, None)
