"""Tests for _declared_suppressed_counts_by_review()."""

from agentic_devtools.cli.ci.models import ReviewInfo
from agentic_devtools.cli.ci.pipeline.actions.dispatch_repair import _declared_suppressed_counts_by_review
from agentic_devtools.cli.ci.pipeline.snapshot import PRStateSnapshot

_BODY_WITH_TWO = "### Comments suppressed due to low confidence (2)\n\nsome prose"
_BODY_WITH_ONE = "### Comments suppressed due to low confidence (1)\n\nsome prose"


class TestDeclaredSuppressedCountsByReview:
    """Tests for reading per-review declared suppressed-comment counts."""

    def test_returns_the_count_declared_by_the_named_review(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", body=_BODY_WITH_TWO)],
        )
        assert _declared_suppressed_counts_by_review(snapshot, [10]) == {10: 2}

    def test_includes_only_the_named_reviews(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            reviews=[
                ReviewInfo(id=10, user="Copilot", state="COMMENTED", body=_BODY_WITH_TWO),
                ReviewInfo(id=11, user="Copilot", state="COMMENTED", body=_BODY_WITH_ONE),
            ],
        )
        assert _declared_suppressed_counts_by_review(snapshot, [11]) == {11: 1}

    def test_omits_unknown_review_ids(self) -> None:
        snapshot = PRStateSnapshot(pr_number=1, reviews=[])
        assert _declared_suppressed_counts_by_review(snapshot, [10]) == {}

    def test_omits_reviews_without_a_declaration(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", body="no findings here")],
        )
        assert _declared_suppressed_counts_by_review(snapshot, [10]) == {}

    def test_omits_named_reviews_when_the_declared_count_is_zero(self) -> None:
        snapshot = PRStateSnapshot(
            pr_number=1,
            reviews=[ReviewInfo(id=10, user="Copilot", state="COMMENTED", body="")],
        )
        assert _declared_suppressed_counts_by_review(snapshot, [10]) == {}
