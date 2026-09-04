"""Tests for ``validate_review_budget``."""

import pytest

from agentic_devtools.orchestration.trio_config import ReviewCap, ReviewCapViolation, validate_review_budget


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"round_number": 0, "point_count": 0, "elapsed_minutes": 0}, "round_number"),
        ({"round_number": 6, "point_count": 0, "elapsed_minutes": 0}, "round_number"),
        ({"round_number": 1, "point_count": 21, "elapsed_minutes": 0}, "point_count"),
        ({"round_number": 1, "point_count": 0, "elapsed_minutes": -1}, "elapsed_minutes"),
        ({"round_number": 1, "point_count": 0, "elapsed_minutes": 31}, "elapsed_minutes"),
    ],
)
def test_validate_review_budget_rejects_overflows(kwargs: dict[str, int], message: str) -> None:
    with pytest.raises(ReviewCapViolation, match=message):
        validate_review_budget(ReviewCap(), phase="standard", **kwargs)
    with pytest.raises(ReviewCapViolation):
        validate_review_budget(
            ReviewCap(), phase="heavyweight_checkpoint", round_number=3, point_count=0, elapsed_minutes=0
        )


def test_validate_review_budget_accepts_boundaries_and_validates_argument_types() -> None:
    validate_review_budget(ReviewCap(), phase="standard", round_number=5, point_count=20, elapsed_minutes=30)
    validate_review_budget(
        ReviewCap(max_rounds=5),
        phase="heavyweight_checkpoint",
        round_number=2,
        point_count=20,
        elapsed_minutes=30,
    )
    with pytest.raises(ValueError):
        validate_review_budget(object(), phase="standard", round_number=1, point_count=0, elapsed_minutes=0)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        validate_review_budget(ReviewCap(), phase="invalid", round_number=1, point_count=0, elapsed_minutes=0)  # type: ignore[arg-type]
    with pytest.raises(ReviewCapViolation):
        validate_review_budget(ReviewCap(), phase="standard", round_number=True, point_count=0, elapsed_minutes=0)  # type: ignore[arg-type]
    with pytest.raises(ReviewCapViolation):
        validate_review_budget(ReviewCap(), phase="standard", round_number=1, point_count=True, elapsed_minutes=0)  # type: ignore[arg-type]
    with pytest.raises(ReviewCapViolation):
        validate_review_budget(ReviewCap(), phase="standard", round_number=1, point_count=0, elapsed_minutes=True)  # type: ignore[arg-type]
