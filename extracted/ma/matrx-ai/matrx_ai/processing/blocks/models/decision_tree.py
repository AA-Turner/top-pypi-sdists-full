"""Decision tree block data models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class DecisionNode(BaseModel):
    """A node in a decision tree (recursive)."""

    model_config = _camel_config

    id: str
    question: str | None = None
    action: str | None = None
    type: str = "decision"  # "decision" | "action" | "outcome"
    yes: DecisionNode | None = None
    no: DecisionNode | None = None
    priority: str | None = None
    category: str | None = None
    estimated_time: str | None = None


class DecisionTreeBlockData(BaseModel):
    """Parsed decision tree data."""

    title: str
    description: str | None = None
    root: DecisionNode
