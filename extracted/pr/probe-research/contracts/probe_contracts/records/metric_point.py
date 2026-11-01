"""MetricPoint: one recorded value of one metric key on a run, at a step and coordinate."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import Field

from .records import Record

#: What a stored non-finite value was: the wire carries `value: null` plus this marker.
MetricNonFinite = Literal["nan", "inf", "-inf"]


class MetricPoint(Record):
    """A metric point as every surface reads it."""

    id: int
    run_id: UUID
    step_index: int | None = None
    kind: str
    key: str
    # None exactly when `nonfinite` names the stored NaN / +inf / -inf.
    value: float | None
    nonfinite: MetricNonFinite | None = None
    wall_clock: datetime
    dimensions: dict = Field(default_factory=dict)
    labels: dict = Field(default_factory=dict)
    span_id: UUID | None = None
