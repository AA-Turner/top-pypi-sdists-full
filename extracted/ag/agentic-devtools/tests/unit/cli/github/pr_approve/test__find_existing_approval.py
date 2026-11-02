from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.github import pr_approve


def test_returns_matching_review() -> None:
    review = {"id": 7, "submitted_at": "2026-04-07T09:00:00Z"}
    with patch.object(pr_approve, "_verify_approval", return_value=(review, 0, True)) as mock_verify:
        result, lookup_ok = pr_approve._find_existing_approval(42, "owner/repo", "alice", "a" * 40)

    assert result == review
    assert lookup_ok is True
    assert mock_verify.call_args.kwargs["max_retries"] == 0
    assert mock_verify.call_args.kwargs["retry_delay"] == 0.0


def test_returns_none_when_no_matching_review_exists() -> None:
    with patch.object(pr_approve, "_verify_approval", return_value=(None, 0, True)):
        result, lookup_ok = pr_approve._find_existing_approval(42, "owner/repo", "alice", "a" * 40)

    assert result is None
    assert lookup_ok is True


def test_reports_lookup_failure_when_verification_could_not_confirm_a_miss() -> None:
    with patch.object(pr_approve, "_verify_approval", return_value=(None, 0, False)):
        result, lookup_ok = pr_approve._find_existing_approval(42, "owner/repo", "alice", "a" * 40)

    assert result is None
    assert lookup_ok is False
