"""Verifier result types."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field


class VerifierSignal(str, Enum):
    """Overall signal from a verifier."""

    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"
    ERROR = "error"
    SKIP = "skip"


# ---------------------------------------------------------------------------
# Discriminated union types for finding data
# ---------------------------------------------------------------------------


class ScoreData(BaseModel):
    """Finding backed by a numeric score (e.g. LLM grading)."""

    type: Literal["score"] = "score"
    score: float = Field(ge=0.0, le=1.0, description="Normalized score 0-1")
    threshold: float | None = Field(default=None, description="Pass threshold")
    evidence: str = ""
    raw: dict[str, Any] = Field(default_factory=dict, description="Raw scorer output")


class BooleanCheckData(BaseModel):
    """Finding from a binary pass/fail check (port listening, container healthy, etc.)."""

    type: Literal["boolean_check"] = "boolean_check"
    check_name: str = ""
    expected: str = ""
    actual: str = ""
    details: str = ""


class ErrorData(BaseModel):
    """Finding from an error during verification."""

    type: Literal["error"] = "error"
    exception_type: str = ""
    message: str = ""
    traceback: str | None = None


class IssueData(BaseModel):
    """Finding that describes an identified issue (from session-reviewer or similar)."""

    type: Literal["issue"] = "issue"
    severity: str = ""  # low|medium|high|critical
    category: str = ""  # correctness|reliability|tooling|environment|workflow|performance|prompting|verification
    description: str = ""


class CustomData(BaseModel):
    """Escape hatch for domain-specific data not covered by other types."""

    type: Literal["custom"] = "custom"
    payload: dict[str, Any] = Field(default_factory=dict)


FindingData = Annotated[
    ScoreData | BooleanCheckData | ErrorData | IssueData | CustomData,
    Field(discriminator="type"),
]


class VerifierFinding(BaseModel):
    """Single finding from a verifier run."""

    signal: VerifierSignal
    title: str
    description: str = ""
    span_ids: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    data: FindingData | None = None


class VerifierResult(BaseModel):
    """Complete result from a verifier run."""

    signal: VerifierSignal
    summary: str
    findings: list[VerifierFinding] = Field(default_factory=list)
    data: FindingData | None = None


@dataclass
class SessionData:
    """Pre-fetched session data bundle passed to verifiers."""

    session_id: str
    session: Any  # SessionResponse from chronos
    trajectory: Any  # SessionTrajectory from chronos
    logs: Any  # SessionLogsResponse from chronos
    annotations: list[Any] = field(default_factory=list)  # AnnotationResponse list
    result: dict[str, Any] | None = None
