"""Tests for effective gate-review HEAD provenance."""

import pytest

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.gate_verdict import CopilotGateVerdict
from agentic_devtools.cli.ci.pipeline.snapshot_reviews import _head_changed_since_effective_gate_review


@pytest.mark.parametrize(
    ("review_id", "review_sha", "current_sha", "expected"),
    [
        (42, "head", "head", False),
        (42, "old", "head", True),
        (42, "", "head", True),
        (42, "head", "", True),
    ],
)
def test_uses_the_gate_review_and_fails_closed_without_sha(
    review_id: int,
    review_sha: str,
    current_sha: str,
    expected: bool,
) -> None:
    review = ReviewInfo(id=review_id, user="Copilot", state="COMMENTED", commit_sha=review_sha)

    result = _head_changed_since_effective_gate_review(
        reviews=[review],
        current_head_sha=current_sha,
        verdict=CopilotGateVerdict(passed=False, reason="blocked", review_id=review_id),
    )

    assert result is expected


def test_fails_closed_when_gate_review_is_missing() -> None:
    result = _head_changed_since_effective_gate_review(
        reviews=[],
        current_head_sha="head",
        verdict=CopilotGateVerdict(passed=False, reason="blocked", review_id=42),
    )

    assert result is True


@pytest.mark.parametrize(
    ("reviews", "current_sha", "expected"),
    [
        ([], "head", True),
        ([ReviewInfo(id=42, user="Copilot", state="COMMENTED")], "head", True),
        ([ReviewInfo(id=42, user="Copilot", state="COMMENTED", commit_sha="head")], "", True),
        ([ReviewInfo(id=42, user="Copilot", state="COMMENTED", commit_sha="head")], "head", False),
        ([ReviewInfo(id=42, user="Copilot", state="COMMENTED", commit_sha="old")], "head", True),
    ],
)
def test_fallback_uses_latest_copilot_review_and_fails_closed(
    reviews: list[ReviewInfo],
    current_sha: str,
    expected: bool,
) -> None:
    result = _head_changed_since_effective_gate_review(
        reviews=reviews,
        current_head_sha=current_sha,
        verdict=CopilotGateVerdict(passed=False, reason="blocked", review_id=0),
    )

    assert result is expected
