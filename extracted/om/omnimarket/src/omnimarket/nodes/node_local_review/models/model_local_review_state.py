"""ModelLocalReviewState and EnumLocalReviewPhase for the local review FSM."""

from __future__ import annotations

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EnumLocalReviewPhase(StrEnum):
    """FSM phases for the local review loop.

    Phase Transitions:
        INIT -> REVIEW -> FIX -> COMMIT -> CHECK_CLEAN -> DONE
        CHECK_CLEAN -> REVIEW (loop on failure, not yet clean)
        Any -> FAILED: Circuit breaker tripped or unrecoverable error
    """

    INIT = "init"
    REVIEW = "review"
    FIX = "fix"
    COMMIT = "commit"
    CHECK_CLEAN = "check_clean"
    DONE = "done"
    FAILED = "failed"


_PHASE_ORDER: tuple[EnumLocalReviewPhase, ...] = (
    EnumLocalReviewPhase.REVIEW,
    EnumLocalReviewPhase.FIX,
    EnumLocalReviewPhase.COMMIT,
    EnumLocalReviewPhase.CHECK_CLEAN,
)

TERMINAL_PHASES: frozenset[EnumLocalReviewPhase] = frozenset(
    {EnumLocalReviewPhase.DONE, EnumLocalReviewPhase.FAILED}
)


def next_phase(
    current: EnumLocalReviewPhase,
    is_clean: bool = False,
) -> EnumLocalReviewPhase:
    """Return the next phase in the local review progression.

    At CHECK_CLEAN: if is_clean, go to DONE; otherwise loop back to REVIEW.
    """
    if current == EnumLocalReviewPhase.INIT:
        return EnumLocalReviewPhase.REVIEW
    if current == EnumLocalReviewPhase.CHECK_CLEAN:
        return EnumLocalReviewPhase.DONE if is_clean else EnumLocalReviewPhase.REVIEW
    if current in TERMINAL_PHASES:
        msg = f"No next phase from terminal state: {current}"
        raise ValueError(msg)

    idx = _PHASE_ORDER.index(current)
    return _PHASE_ORDER[idx + 1]


class ModelLocalReviewState(BaseModel):
    """Immutable FSM state for the local review loop."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(..., description="Review run correlation ID.")
    current_phase: EnumLocalReviewPhase = Field(
        default=EnumLocalReviewPhase.INIT, description="Current FSM phase."
    )
    consecutive_failures: int = Field(default=0, ge=0)
    max_consecutive_failures: int = Field(default=3, ge=1)
    dry_run: bool = Field(default=False)
    iteration_count: int = Field(default=0, ge=0, description="Review iterations.")
    max_iterations: int = Field(default=10, ge=1)
    consecutive_clean_runs: int = Field(
        default=0, ge=0, description="Consecutive clean review runs."
    )
    required_clean_runs: int = Field(default=2, ge=1)
    issues_found: int = Field(default=0, ge=0)
    issues_fixed: int = Field(default=0, ge=0)
    error_message: str | None = Field(default=None)


__all__: list[str] = [
    "TERMINAL_PHASES",
    "EnumLocalReviewPhase",
    "ModelLocalReviewState",
    "next_phase",
]
