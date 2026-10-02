"""ModelPrPolishState and EnumPrPolishPhase for the PR polish FSM."""

from __future__ import annotations

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EnumPrPolishPhase(StrEnum):
    """FSM phases for PR polish.

    Phase Transitions:
        INIT -> RESOLVE_CONFLICTS -> FIX_CI -> ADDRESS_COMMENTS -> LOCAL_REVIEW -> DONE
        Any -> FAILED: Circuit breaker tripped or unrecoverable error
    """

    INIT = "init"
    RESOLVE_CONFLICTS = "resolve_conflicts"
    FIX_CI = "fix_ci"
    ADDRESS_COMMENTS = "address_comments"
    LOCAL_REVIEW = "local_review"
    DONE = "done"
    FAILED = "failed"


_PHASE_ORDER: tuple[EnumPrPolishPhase, ...] = (
    EnumPrPolishPhase.RESOLVE_CONFLICTS,
    EnumPrPolishPhase.FIX_CI,
    EnumPrPolishPhase.ADDRESS_COMMENTS,
    EnumPrPolishPhase.LOCAL_REVIEW,
)

TERMINAL_PHASES: frozenset[EnumPrPolishPhase] = frozenset(
    {EnumPrPolishPhase.DONE, EnumPrPolishPhase.FAILED}
)


def next_phase(
    current: EnumPrPolishPhase,
    skip_conflicts: bool = False,
) -> EnumPrPolishPhase:
    """Return the next phase in the PR polish progression."""
    if current == EnumPrPolishPhase.INIT:
        return (
            EnumPrPolishPhase.FIX_CI
            if skip_conflicts
            else EnumPrPolishPhase.RESOLVE_CONFLICTS
        )
    if current == EnumPrPolishPhase.LOCAL_REVIEW:
        return EnumPrPolishPhase.DONE
    if current in TERMINAL_PHASES:
        msg = f"No next phase from terminal state: {current}"
        raise ValueError(msg)

    idx = _PHASE_ORDER.index(current)
    next_idx = idx + 1
    if skip_conflicts and _PHASE_ORDER[next_idx] == EnumPrPolishPhase.RESOLVE_CONFLICTS:
        next_idx += 1
    return _PHASE_ORDER[next_idx]


class ModelPrPolishState(BaseModel):
    """Immutable FSM state for PR polish."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    correlation_id: UUID = Field(..., description="Polish run correlation ID.")
    pr_number: int | None = Field(default=None, description="PR number.")
    current_phase: EnumPrPolishPhase = Field(
        default=EnumPrPolishPhase.INIT, description="Current FSM phase."
    )
    consecutive_failures: int = Field(default=0, ge=0)
    max_consecutive_failures: int = Field(default=3, ge=1)
    skip_conflicts: bool = Field(default=False)
    dry_run: bool = Field(default=False)
    conflicts_resolved: int = Field(default=0, ge=0)
    ci_fixes_applied: int = Field(default=0, ge=0)
    comments_addressed: int = Field(default=0, ge=0)
    error_message: str | None = Field(default=None)


__all__: list[str] = [
    "TERMINAL_PHASES",
    "EnumPrPolishPhase",
    "ModelPrPolishState",
    "next_phase",
]
