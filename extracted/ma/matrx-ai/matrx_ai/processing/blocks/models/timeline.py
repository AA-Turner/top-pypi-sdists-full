"""Timeline block data models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class TimelineEvent(BaseModel):
    model_config = _camel_config

    id: str
    title: str
    date: str = "TBD"
    description: str = ""
    status: Literal["completed", "in-progress", "pending"] | None = None
    category: str | None = None


class TimelinePeriod(BaseModel):
    model_config = _camel_config

    period: str
    events: list[TimelineEvent] = Field(default_factory=list)


class TimelineBlockData(BaseModel):
    model_config = _camel_config

    title: str = "Timeline"
    description: str | None = None
    periods: list[TimelinePeriod] = Field(default_factory=list)
