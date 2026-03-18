"""Verifier result types."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_serializer

from plato.worlds.review import ReviewData


class VerifierSignal(str, Enum):
    """Overall signal from a verifier."""

    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    ERROR = "error"
    SKIP = "skip"


class VerifierFinding(BaseModel):
    """Single finding from a verifier run.

    The ``data`` field accepts a :class:`ReviewData` instance (typed review
    model). It is automatically serialized to a dict for the API.
    """

    signal: VerifierSignal
    title: str
    description: str = ""
    span_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    data: ReviewData | None = None

    @model_serializer(mode="wrap")
    def _serialize(self, handler: Any) -> dict[str, Any]:
        result = handler(self)
        # Ensure data is always a plain dict when serialized (for API transport)
        if self.data is not None and isinstance(self.data, ReviewData):
            result["data"] = self.data.model_dump()
        return result


class VerifierResult(BaseModel):
    """Complete result from a verifier run."""

    signal: VerifierSignal
    summary: str
    findings: list[VerifierFinding] = Field(default_factory=list)
    data: ReviewData | None = None

    @model_serializer(mode="wrap")
    def _serialize(self, handler: Any) -> dict[str, Any]:
        result = handler(self)
        if self.data is not None and isinstance(self.data, ReviewData):
            result["data"] = self.data.model_dump()
        return result


@dataclass
class SessionData:
    """Pre-fetched session data bundle passed to verifiers."""

    session_id: str
    session: Any  # SessionResponse from chronos
    trajectory: Any  # SessionTrajectory from chronos
    logs: Any  # SessionLogsResponse from chronos
    annotations: list[Any] = field(default_factory=list)  # AnnotationResponse list
    result: dict[str, Any] | None = None
