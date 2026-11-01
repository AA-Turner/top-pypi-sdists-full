"""Experiment: a leaf project that answers one question and holds runs."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import AliasChoices, Field

from .records import Record


class Experiment(Record):
    """An experiment as every surface reads it."""

    id: UUID
    customer_id: str
    project_id: UUID
    slug: str
    # A plain `str` over a nullable column: an unnamed experiment reads as its slug.
    name: str
    question: str
    description: str | None = None
    # Server-stamped creator (0081): 'user:<uuid>' | 'ingest:<token-uuid>'. NULL on
    # pre-0081 rows, which read as "unknown", never as either side of agent/human.
    created_by: str | None = None
    tags: list[str] = Field(default_factory=list)
    #: Headline scalars: what this ACHIEVED, one value with no step axis.
    summary_metrics: dict = Field(
        default_factory=dict, validation_alias=AliasChoices("summary_metrics", "summary"),
    )
    metadata: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime
