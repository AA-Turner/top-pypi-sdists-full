"""Review result types for the unified review system.

These models are used by review worlds to represent their findings.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_serializer

from plato.worlds.review.data import ReviewData


class ReviewSignal(str, Enum):
    """Overall signal from a review."""

    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    ERROR = "error"
    SKIP = "skip"


class ReviewFinding(BaseModel):
    """Single finding from a review.

    The ``data`` field accepts a :class:`ReviewData` instance (typed review
    model).  It is automatically serialized to a dict for the API.
    """

    signal: ReviewSignal
    title: str
    description: str = ""
    span_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    data: ReviewData | None = None

    @model_serializer(mode="wrap")
    def _serialize(self, handler: Any) -> dict[str, Any]:
        result = handler(self)
        if self.data is not None and isinstance(self.data, ReviewData):
            result["data"] = self.data.model_dump()
        return result


class ReviewResult(BaseModel):
    """Complete result from a review."""

    signal: ReviewSignal
    summary: str
    findings: list[ReviewFinding] = Field(default_factory=list)
    data: ReviewData | None = None

    @model_serializer(mode="wrap")
    def _serialize(self, handler: Any) -> dict[str, Any]:
        result = handler(self)
        if self.data is not None and isinstance(self.data, ReviewData):
            result["data"] = self.data.model_dump()
        return result


class SessionData(BaseModel):
    """Pre-fetched session data bundle passed to reviewers."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    session_id: str
    session: Any = None
    trajectory: Any = None
    logs: Any = None
    annotations: list[Any] = Field(default_factory=list)
    result: dict[str, Any] | None = None
