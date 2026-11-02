"""Fingerprint available review and CI work for fail-closed exhaustion holds."""

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import CheckRunStatus, ReviewCommentInfo, ReviewInfo
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot
from agentic_devtools.cli.ci.repair_accounting import repair_hold_observation_key


def test_repair_hold_observation_key_tracks_root_feedback_and_failed_checks() -> None:
    provider = MagicMock()
    root = ReviewCommentInfo(11, "src.py", "Fix this", "", source_review_id=10)
    reply = ReviewCommentInfo(12, "src.py", "Acknowledged", "", source_review_id=10, in_reply_to_id=11)
    provider.list_review_comments.return_value = [root, reply]
    snapshot = PRStateSnapshot(
        pr_number=42,
        head_sha="head",
        review_state="CHANGES_REQUESTED",
        copilot_review_id=10,
        reviews=[ReviewInfo(10, "Copilot", "CHANGES_REQUESTED", "Please fix the issue")],
        ci_status="failing",
        ci_failed_checks=["lint"],
        check_runs=[
            CheckRunStatus(1, "lint", "completed", "failure", app_slug="actions"),
            CheckRunStatus(2, "tests", "completed", "success", app_slug="actions"),
        ],
    )

    original = repair_hold_observation_key(provider, snapshot)

    provider.list_review_comments.return_value = [root, reply]
    assert repair_hold_observation_key(provider, snapshot) == original

    provider.list_review_comments.return_value = [
        ReviewCommentInfo(11, "src.py", "Different feedback", "", source_review_id=10),
        reply,
    ]
    assert repair_hold_observation_key(provider, snapshot) != original
    provider.list_review_comments.assert_called_with(42, 10)
