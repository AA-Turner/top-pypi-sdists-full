"""ReviewVerdict model for structured LLM output from file review nodes.

Provides the per-file verdict used by ``review_file_node`` to determine
the appropriate tool action (approve, request-changes, etc.).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ReviewOutcome = Literal["approve", "request-changes", "request-changes-with-suggestion"]


class ReviewSuggestion(BaseModel):
    """A single code suggestion from the LLM file-reviewer.

    Attributes:
        line: Diff-line anchor.  Required unless ``out_of_scope=True``.
        endLine: Optional inclusive end line.
        content: Human-readable suggestion body forwarded to the ADO thread.
        replacement_code: Optional replacement code; wrapped in a fenced
            ``suggestion`` block by the submit mapper.
        out_of_scope: Set to ``True`` for observations not tied to a diff line.
            When ``True`` and ``line`` is ``None`` the suggestion is silently
            skipped by the mapper (the engine can only post line-anchored threads).
        severity: Optional severity label (e.g. ``"high"``, ``"medium"``, ``"low"``).
        link_text: Optional anchor link text passed through to the engine.
    """

    model_config = ConfigDict(extra="allow")

    line: int | None = Field(
        default=None,
        description="Diff-line anchor (required unless out_of_scope=True)",
    )
    endLine: int | None = Field(
        default=None,
        description="Optional inclusive end line number",
    )
    content: str = Field(default="", description="Human-readable suggestion body")
    replacement_code: str | None = Field(
        default=None,
        description="Replacement code to wrap in a fenced suggestion block",
    )
    out_of_scope: bool = Field(
        default=False,
        description="True when the suggestion is not tied to a specific diff line",
    )
    severity: str | None = Field(
        default=None,
        description="Optional severity level (e.g. 'high', 'medium', 'low')",
    )
    link_text: str | None = Field(
        default=None,
        description="Optional anchor link text passed through to the engine",
    )

    @model_validator(mode="after")
    def check_line_required_unless_out_of_scope(self) -> ReviewSuggestion:
        """Require *line* for in-scope suggestions."""
        if not self.out_of_scope and self.line is None:
            raise ValueError(
                "suggestion 'line' is required when 'out_of_scope' is False; "
                "set out_of_scope=True for suggestions not tied to a diff line"
            )
        return self


class ReviewVerdict(BaseModel):
    """Per-file review verdict from the LLM.

    Used by ``review_file_node`` to determine which tool action to invoke.

    Attributes:
        outcome: The file review outcome.
        summary: Human-readable summary of the review decision.
        suggestions: Optional list of code suggestions (for suggestion outcomes).
    """

    outcome: ReviewOutcome = Field(
        description="Review outcome: approve, request-changes, or request-changes-with-suggestion",
    )
    summary: str = Field(default="", description="Human-readable summary of the review")
    suggestions: list[ReviewSuggestion] = Field(
        default_factory=list,
        description="Inline code suggestions; each must supply 'line' unless 'out_of_scope' is True",
    )
