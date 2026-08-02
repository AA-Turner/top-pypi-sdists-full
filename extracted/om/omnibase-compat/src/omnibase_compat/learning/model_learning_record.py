# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.models.learning.model_learning_record
# COMPAT_REMOVAL_DATE: 2027-06-01

"""ModelLearningRecord — one captured outcome for the cross-process learning loop.

Spec: docs/plans/2026-07-06-learning-loop-generalization-spec.md §3.1.
Emitted by any automated process (merge sweep, delegation, dispatch worker,
ci fix, steel, plan governor) after a decision resolves. Consumed by the two
read-back mechanisms named in the spec: a decision overlay (pure function
over a windowed rollup) and advisory injection (top-K prior records
prepended to a dispatched worker prompt). Append-only; never mutated.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from omnibase_compat.learning.enum_failure_class import EnumFailureClass
from omnibase_compat.learning.enum_learning_process_id import EnumLearningProcessId


class EnumLearningOutcome(StrEnum):
    """Outcome of the decision a `ModelLearningRecord` was captured for."""

    SUCCESS = "success"
    FAILURE = "failure"


class ModelLearningRecord(BaseModel):
    """One append-only outcome record for a single automated decision.

    Frozen + extra=forbid: a learning record is immutable once captured —
    corrections are new records, never mutations of a prior one.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    process_id: EnumLearningProcessId = Field(
        ...,
        description="Which automated process captured this record.",
    )
    context_key: dict[str, str] = Field(
        ...,
        description=(
            "Decision dimensions the read-back keys on, per process "
            "(e.g. merge sweep: repo/check_name/failure_class; "
            "dispatch: repo/task_class; delegation: task_type/model_tier/model_id)."
        ),
    )
    outcome: EnumLearningOutcome = Field(
        ...,
        description="Whether the decision succeeded or failed.",
    )
    failure_class: EnumFailureClass | None = Field(
        default=None,
        description="Required when outcome=failure; taxonomy from spec §3.4.",
    )
    remedy: str | None = Field(
        default=None,
        description="Free-text description of what fixed the failure, if known.",
    )
    remedy_recipe_id: str | None = Field(
        default=None,
        description="Optional identifier of a reusable remedy recipe.",
    )
    evidence_ref: str = Field(
        ...,
        min_length=1,
        description="PR/run/receipt URL proving the captured outcome.",
    )
    recorded_at: datetime = Field(
        ...,
        description="Timestamp the record was captured.",
    )

    @model_validator(mode="after")
    def _validate_context_key_non_empty(self) -> Self:
        if not self.context_key:
            raise ValueError("context_key must have at least one dimension")
        return self

    @model_validator(mode="after")
    def _validate_failure_class_matches_outcome(self) -> Self:
        if self.outcome == EnumLearningOutcome.FAILURE and self.failure_class is None:
            raise ValueError("failure_class is required when outcome=failure")
        if self.outcome == EnumLearningOutcome.SUCCESS and self.failure_class is not None:
            raise ValueError("failure_class must be None unless outcome=failure")
        return self


__all__: list[str] = [
    "EnumLearningOutcome",
    "ModelLearningRecord",
]
