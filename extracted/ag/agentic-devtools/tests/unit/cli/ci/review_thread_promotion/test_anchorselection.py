"""Tests for AnchorSelection."""

from agentic_devtools.cli.ci.review_thread_promotion import AnchorSelection, ReviewThreadAnchor


def test_anchor_selection_preserves_fallback_status() -> None:
    anchor = ReviewThreadAnchor("src/app.py", 12)

    assert AnchorSelection(anchor, used_fallback=True).used_fallback is True
