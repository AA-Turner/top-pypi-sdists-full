"""Progress tracker block data models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ProgressItem(BaseModel):
    model_config = _camel_config

    id: str
    text: str
    completed: bool = False
    priority: Literal["high", "medium", "low"] | None = None
    estimated_hours: float | None = None
    optional: bool = False
    category: str | None = None


class ProgressCategory(BaseModel):
    model_config = _camel_config

    id: str
    name: str
    description: str | None = None
    color: str | None = None
    completion_percentage: float = 0.0
    items: list[ProgressItem] = Field(default_factory=list)


class ProgressTrackerBlockData(BaseModel):
    model_config = _camel_config

    title: str
    description: str | None = None
    overall_progress: float = 0.0
    total_items: int = 0
    completed_items: int = 0
    categories: list[ProgressCategory] = Field(default_factory=list)
