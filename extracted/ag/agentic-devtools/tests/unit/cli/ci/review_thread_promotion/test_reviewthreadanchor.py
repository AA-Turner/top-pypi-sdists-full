"""Tests for ReviewThreadAnchor."""

from agentic_devtools.cli.ci.review_thread_promotion import ReviewThreadAnchor


def test_anchor_defaults_to_right_side() -> None:
    assert ReviewThreadAnchor("src/app.py", 12).side == "RIGHT"
