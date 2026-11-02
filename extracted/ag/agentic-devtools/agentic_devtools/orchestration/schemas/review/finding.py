"""Review finding models for structured LLM output schemas.

Provides CodeSuggestion and FileReviewFinding models for PR review findings.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator

from .._enums import Severity, normalize_severity

DiffSide = Literal["old", "new", "context"]

_LOW_CONFIDENCE_THRESHOLD = 0.5


class CodeSuggestion(BaseModel):
    """A specific code replacement suggestion attached to a review finding.

    Provides the affected line range and original code context.  The concrete
    ``replacement_code`` is optional (nullable/absent): it is only populated for
    findings that carry usable post-change coordinates in a language covered by
    the FR-014 syntax-validation set.  ``start_line``, ``end_line``, and
    ``original_code`` remain required even when ``replacement_code`` is absent so
    the FR-014 / SC-007 syntax substitution can target a concrete range.
    """

    file_path: str = Field(description="Path to the file containing the code to change")
    start_line: int = Field(description="Starting line number of the code to replace")
    end_line: int = Field(description="Ending line number of the code to replace")
    original_code: str = Field(description="The original code that should be replaced")
    replacement_code: str | None = Field(
        default=None,
        description="The suggested replacement code (absent for old-side/unsupported findings)",
    )
    explanation: str = Field(default="", description="Explanation of why this change is suggested")


class FileReviewFinding(BaseModel):
    """An individual finding from reviewing a file in a pull request.

    Represents a specific issue, concern, or observation found during
    code review, with severity classification and optional fix suggestion.

    Line references identify the applicable unified-diff side via ``diff_side``
    with distinct ``old_line`` / ``new_line`` coordinates.  The deprecated
    ``line`` alias is accepted only for backward compatibility and is normalized
    to ``diff_side="new"`` / ``new_line=line``.
    """

    model_config = ConfigDict(validate_assignment=True)

    severity: Annotated[Severity, BeforeValidator(normalize_severity)] = Field(
        description="Severity level of the finding"
    )
    diff_side: DiffSide = Field(
        description="Unified-diff side the finding applies to: 'old', 'new', or 'context'",
    )
    old_line: int | None = Field(default=None, ge=1, description="1-based pre-change (old-side) line number")
    new_line: int | None = Field(default=None, ge=1, description="1-based post-change (new-side) line number")
    line: int | None = Field(
        default=None,
        ge=1,
        description="Deprecated legacy alias; normalized to new_line",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Normalized confidence score in [0.0, 1.0]",
    )
    low_confidence: bool = Field(
        default=False,
        description="Derived flag set when confidence < 0.5",
    )
    description: str = Field(description="Human-readable description of the finding")
    suggestion: CodeSuggestion | None = Field(
        default=None,
        description="Optional code suggestion to fix the finding",
    )

    @model_validator(mode="before")
    @classmethod
    def _normalize_legacy_shape(cls, value: object) -> object:
        """Infer side only for legacy ``line``-only payloads."""
        if not isinstance(value, dict):
            return value
        line = value.get("line")
        if (
            line is not None
            and value.get("diff_side") is None
            and value.get("new_line") is None
            and value.get("old_line") is None
        ):
            normalized = dict(value)
            normalized["diff_side"] = "new"
            normalized["new_line"] = line
            return normalized
        return value

    @model_validator(mode="after")
    def _normalize_coordinates(self) -> FileReviewFinding:
        """Infer legacy ``line``, validate per-side coordinates, derive flags."""
        # Legacy ``line`` is treated as a new-side coordinate.
        if self.line is not None:
            if self.new_line is not None and self.new_line != self.line:
                raise ValueError("line and new_line disagree; provide only one new-side coordinate")
            object.__setattr__(self, "new_line", self.line)

        # Per-side coordinate validation.
        if self.diff_side == "old":
            if self.new_line is not None:
                raise ValueError("diff_side='old' must not carry a new_line coordinate")
            if self.old_line is None:
                raise ValueError("diff_side='old' requires old_line")
        elif self.diff_side == "new":
            if self.old_line is not None:
                raise ValueError("diff_side='new' must not carry an old_line coordinate")
            if self.new_line is None:
                raise ValueError("diff_side='new' requires new_line")
        else:  # context
            if self.old_line is None or self.new_line is None:
                raise ValueError("diff_side='context' requires both old_line and new_line")

        # Keep the legacy alias mirrored to new_line for backward-compat readers.
        object.__setattr__(self, "line", self.new_line)

        # Derive the low-confidence flag deterministically from confidence.
        object.__setattr__(self, "low_confidence", self.confidence < _LOW_CONFIDENCE_THRESHOLD)
        return self
