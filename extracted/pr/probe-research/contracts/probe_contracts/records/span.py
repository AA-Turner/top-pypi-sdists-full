"""Span: one timed piece of a run (a step, a rollout, a tool call), nested under a parent span."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import AliasChoices, Field

from .records import Record


class Span(Record):
    """A span as every surface reads it."""

    id: UUID
    customer_id: str
    run_id: UUID
    parent_span_id: UUID | None = None
    span_type: str
    name: str | None = None
    step_index: int | None = None
    external_key: str | None = None
    provider: str | None = None
    status: str
    started_at: datetime
    ended_at: datetime | None = None
    attributes: dict = Field(default_factory=dict)
    #: Headline scalars: what this ACHIEVED, one value with no step axis.
    summary_metrics: dict = Field(
        default_factory=dict, validation_alias=AliasChoices("summary_metrics", "summary"),
    )
    generated_description: str | None = None
    generated_description_meta: dict = Field(default_factory=dict)
    # Below-run coordinate (0059): the canonical coords map and its hash.
    dimensions: dict = Field(default_factory=dict)
    dims_hash: str | None = None
    created_at: datetime
