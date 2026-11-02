"""Tests for validate_pull_request_review_transition."""

from agentic_devtools.cli.workflows.commands import validate_pull_request_review_transition


def _progress(*, all_complete, completed=0, total=0):
    """Build a compute_review_progress() return dict."""
    return {
        "all_complete": all_complete,
        "completed_count": completed,
        "pending_count": total - completed,
        "total_count": total,
    }


def _submit_result(*, dry_run=False, posted=1, accepted=1, failed=0, pr_id=None):
    """Build a minimal submit-result dict."""
    result: dict = {
        "dryRun": dry_run,
        "counts": {"posted": posted, "accepted": accepted, "failed": failed},
    }
    if pr_id is not None:
        result["prId"] = pr_id
    return result


class TestValidatePullRequestReviewTransition:
    """Guard rails for pull-request-review step advancement."""

    def test_allows_adjacent_forward_transition(self):
        assert (
            validate_pull_request_review_transition("pr-synthesis", "delegate", _progress(all_complete=False, total=39))
            is None
        )

    def test_allows_repeating_current_step(self):
        assert (
            validate_pull_request_review_transition("delegate", "delegate", _progress(all_complete=False, total=39))
            is None
        )

    def test_allows_completion_when_all_files_answered_and_submitted(self):
        assert (
            validate_pull_request_review_transition(
                "decision",
                "completion",
                _progress(all_complete=True, completed=39, total=39),
                _submit_result(posted=39, accepted=39),
            )
            is None
        )

    def test_allows_completion_for_dry_run_with_no_posted(self):
        assert (
            validate_pull_request_review_transition(
                "decision",
                "completion",
                _progress(all_complete=True, completed=5, total=5),
                _submit_result(dry_run=True, posted=0, accepted=5),
            )
            is None
        )

    def test_rejects_completion_when_nothing_accepted_but_ledger_has_files(self):
        """Completion is refused when submit ran but nothing was accepted and the ledger is non-empty."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=5, total=5),
            _submit_result(dry_run=False, posted=0, accepted=0),
        )
        assert message is not None
        assert "0/5" in message
        assert "agdt-pr-review-submit" in message

    def test_rejects_skipping_a_step(self):
        message = validate_pull_request_review_transition(
            "delegate", "completion", _progress(all_complete=True, completed=39, total=39)
        )
        assert message is not None
        assert "Cannot skip from 'delegate' to 'completion'" in message
        assert "agdt-advance-workflow consolidate-and-submit" in message

    def test_rejects_consolidate_when_delegate_incomplete(self):
        message = validate_pull_request_review_transition(
            "delegate", "consolidate-and-submit", _progress(all_complete=False, completed=0, total=39)
        )
        assert message is not None
        assert "Cannot advance from 'delegate' to 'consolidate-and-submit'" in message
        assert "0/39" in message

    def test_rejects_completion_when_review_incomplete(self):
        message = validate_pull_request_review_transition(
            "decision", "completion", _progress(all_complete=False, completed=0, total=39)
        )
        assert message is not None
        assert "the review was never submitted to the PR" in message
        assert "agdt-file-review-write" in message

    def test_rejects_completion_when_no_submit_result(self):
        """Refuse completion when submit-result.json has not been written."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=5, total=5),
            submit_result=None,
        )
        assert message is not None
        assert "no submission outcome recorded" in message
        assert "agdt-pr-review-submit" in message

    def test_rejects_completion_when_real_run_posted_zero_but_accepted_nonzero(self):
        """Refuse completion when a real (non-dry-run) submission posted 0 comments despite acceptances."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=5, total=5),
            _submit_result(dry_run=False, posted=0, accepted=5),
        )
        assert message is not None
        assert "no comments were posted" in message
        assert "submit-result.json" in message

    def test_rejects_completion_when_dry_run_field_is_not_boolean(self):
        """Completion is refused when dryRun is a non-boolean (e.g. the string "false")."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=5, total=5),
            submit_result={"dryRun": "false", "counts": {"posted": 5, "accepted": 5, "failed": 0}},
        )
        assert message is not None
        assert "malformed" in message
        assert "dryRun" in message

    def test_rejects_completion_when_dry_run_field_is_missing(self):
        """Completion is refused when dryRun key is absent from submit-result."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=5, total=5),
            submit_result={"counts": {"posted": 5, "accepted": 5, "failed": 0}},
        )
        assert message is not None
        assert "malformed" in message
        assert "dryRun" in message

    def test_rejects_completion_when_counts_missing_from_submit_result(self):
        """Completion is refused when submit-result lacks the required counts object."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=5, total=5),
            submit_result={"dryRun": False},
        )
        assert message is not None
        assert "missing" in message
        assert "counts" in message

    def test_rejects_completion_when_counts_has_malformed_values(self):
        """Completion is refused when a count field is not a non-negative integer."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=5, total=5),
            submit_result={"dryRun": False, "counts": {"posted": "unknown", "accepted": 5, "failed": 0}},
        )
        assert message is not None
        assert "malformed" in message

    def test_rejects_completion_when_submission_covers_only_partial_ledger(self):
        """Completion is refused when a live submit covered fewer files than the current total."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=39, total=39),
            submit_result={
                "dryRun": False,
                "counts": {"posted": 1, "accepted": 1, "failed": 0, "stale": 0, "skipped": 0},
            },
        )
        assert message is not None
        assert "1/39" in message
        assert "accepted=1" in message
        assert "agdt-pr-review-submit" in message

    def test_rejects_completion_when_partial_ledger_and_stale_skipped_absent(self):
        """Coverage check fires even when stale/skipped keys are absent from counts (treated as 0)."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=39, total=39),
            submit_result={"dryRun": False, "counts": {"posted": 1, "accepted": 1, "failed": 0}},
        )
        assert message is not None
        assert "1/39" in message

    def test_rejects_completion_when_submission_has_stale_files(self):
        """Completion is refused when the submission has stale files that were not posted."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=39, total=39),
            submit_result={
                "dryRun": False,
                "counts": {"posted": 30, "accepted": 30, "failed": 0, "stale": 9, "skipped": 0},
            },
        )
        assert message is not None
        assert "stale" in message
        assert "agdt-pr-review-submit" in message

    def test_ignores_ordering_for_unknown_current_step(self):
        assert (
            validate_pull_request_review_transition(
                "", "consolidate-and-submit", _progress(all_complete=True, completed=1, total=1)
            )
            is None
        )

    def test_rejects_completion_when_real_run_has_failures(self):
        """Refuse completion when a live submission had at least one failed item."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=3, total=3),
            _submit_result(dry_run=False, posted=2, accepted=3, failed=1),
        )
        assert message is not None
        assert "failed to post" in message
        assert "submit-result.json" in message

    def test_allows_completion_for_dry_run_even_with_failures(self):
        """Dry-run runs bypass the live failure check."""
        assert (
            validate_pull_request_review_transition(
                "decision",
                "completion",
                _progress(all_complete=True, completed=3, total=3),
                _submit_result(dry_run=True, posted=0, accepted=3, failed=1),
            )
            is None
        )

    def test_rejects_completion_when_submit_result_belongs_to_different_pr(self):
        """Refuse completion when submit-result.json records a different prId."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=5, total=5),
            _submit_result(posted=5, accepted=5, pr_id=9999),
            pr_id=1234,
        )
        assert message is not None
        assert "9999" in message
        assert "1234" in message

    def test_allows_completion_when_pr_id_matches(self):
        """Completion is allowed when prId in result matches the expected PR ID."""
        assert (
            validate_pull_request_review_transition(
                "decision",
                "completion",
                _progress(all_complete=True, completed=5, total=5),
                _submit_result(posted=5, accepted=5, pr_id=1234),
                pr_id=1234,
            )
            is None
        )

    def test_rejects_completion_when_expected_pr_id_is_missing_from_submit_result(self):
        """Completion is refused when an expected PR ID is not recorded in submit-result.json."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=5, total=5),
            _submit_result(posted=5, accepted=5),
            pr_id=1234,
        )
        assert message is not None
        assert "missing the required 'prId'" in message
        assert "1234" in message

    def test_rejects_completion_when_counts_has_boolean_values(self):
        """Completion is refused when count fields are booleans rather than integers."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=1, total=1),
            submit_result={
                "dryRun": False,
                "prId": 1234,
                "counts": {"posted": True, "accepted": True, "failed": False},
            },
            pr_id=1234,
        )
        assert message is not None
        assert "malformed count fields" in message

    def test_rejects_completion_when_stale_or_skipped_are_non_integer(self):
        """Completion is refused when stale/skipped are present but not non-negative integers."""
        message = validate_pull_request_review_transition(
            "decision",
            "completion",
            _progress(all_complete=True, completed=39, total=39),
            submit_result={
                "dryRun": False,
                "prId": 1234,
                "counts": {"posted": 39, "accepted": 39, "failed": 0, "stale": "9", "skipped": 0},
            },
            pr_id=1234,
        )
        assert message is not None
        assert "malformed count fields" in message
