"""Canonical work identity tests."""

from dataclasses import replace

from agentic_devtools.cli.ci.models import CheckRunStatus, ReviewCommentInfo
from agentic_devtools.cli.ci.repair_accounting import repair_work_key


def test_repair_work_key_ignores_order_timestamps_and_replies() -> None:
    root = ReviewCommentInfo(1, "x.py", "finding", "", source_review_id=10)
    synthetic = ReviewCommentInfo(-1, "x.py", "body", "", source_review_id=20)
    reply = replace(root, id=2, in_reply_to_id=1)
    check = CheckRunStatus(1, "lint", "completed", "failure", app_slug="github-actions")
    assert repair_work_key(10, [root, synthetic], [check]) == repair_work_key(
        10,
        [synthetic, replace(root, created_at="tomorrow"), reply, root],
        [replace(check, id=99, html_url="other")],
    )


def test_repair_work_key_qualifies_negative_ids_and_combined_ci() -> None:
    finding = ReviewCommentInfo(-1, "x", "body", "", source_review_id=10)
    original = repair_work_key(10, [finding], [])
    assert original != repair_work_key(10, [replace(finding, source_review_id=20)], [])
    assert original != repair_work_key(10, [finding], [CheckRunStatus(1, "lint", "completed")])
    assert original != repair_work_key(10, [finding], [], {10: 2})
