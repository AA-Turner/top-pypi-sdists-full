"""I/O contracts for `pysae-ai-tools glab issue ready-check`."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class TicketType(str, Enum):
    FEATURE = "feat"
    BUG = "bug"
    TECHNICAL = "tech"
    UNKNOWN = "unknown"


class SectionViolation(BaseModel):
    kind: Literal["section"] = "section"
    section: str
    reason: str


class CheckboxViolation(BaseModel):
    kind: Literal["checkbox"] = "checkbox"
    checkbox: str
    reason: str


Violation = SectionViolation | CheckboxViolation


class LLMReview(BaseModel):
    quality_score: int = Field(ge=1, le=5)
    missing_aspects: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    comment_md: str | None = None


class ReadyCheckResult(BaseModel):
    ready: bool
    type: TicketType
    violations: list[Violation] = Field(default_factory=list)
    comment_md: str | None = None
    llm_review: LLMReview | None = None
    actions_applied: list[str] = Field(default_factory=list)
