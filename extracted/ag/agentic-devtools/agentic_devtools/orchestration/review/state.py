"""LangGraph state schema for the autonomous PR review workflow.

Defines ``ReviewGraphState`` (the TypedDict flowing through the LangGraph
StateGraph) and ``FileReviewResult`` (the per-file review output dataclass).
"""

from __future__ import annotations

import operator
from dataclasses import dataclass, field
from typing import Annotated, Any, Literal, NotRequired, TypedDict

from pydantic import BaseModel, Field, model_validator


class ReviewGraphState(TypedDict, total=False):
    """State schema for the LangGraph PR review pipeline.

    Carries all information flowing between nodes for a single review run.
    Uses LangGraph's ``Annotated`` channel pattern where append semantics
    are needed (``errors``).  ``file_results`` uses last-writer-wins
    semantics because ``review_files_node`` writes the entire list at once;
    append semantics would duplicate results on graph retry/resume.
    """

    # Inputs (populated by fetch_pr_details node)
    pr_id: int
    jira_issue_key: NotRequired[str]
    repo_id: str
    project: str
    organization: str
    commit_hash: str
    base_commit_hash: NotRequired[str]
    latest_iteration_id: NotRequired[int]
    iterations: NotRequired[list[dict[str, Any]]]
    jira_issue: NotRequired[dict[str, Any] | None]
    files: list[dict[str, Any]]
    threads: list[dict[str, Any]]
    config: dict[str, Any]

    # Populated by scaffold_comments node
    review_state_path: str

    # Populated by review_files node (last-writer-wins: the node emits the full list)
    file_results: list[Any]

    # Populated by summarize_and_decide node
    overall_decision: str
    summary: str

    # Error tracking (append-only)
    errors: Annotated[list[str], operator.add]

    # Source context enrichment flag
    source_context_enabled: NotRequired[bool]

    # Repo-root-resolved LLM provider config path
    llm_config_path: NotRequired[str]

    # Model routing config
    model_config_raw: NotRequired[dict[str, Any]]
    requested_model: NotRequired[str]


@dataclass
class FileReviewResult:
    """Per-file output from the ``review_files`` node.

    Attributes:
        file_path: Repository-relative path of the reviewed file.
        outcome: LLM verdict for the file.
        summary: Human-readable summary of the review.
        suggestions: Draft suggestions from the LLM (ADO thread/comment
            IDs are assigned later in ``post_results``).
        model_id: Identifier of the LLM model that produced this review, when available.
        provider_type: Provider backend that produced this review.
        latency_ms: Provider call latency in milliseconds, when available.
        finish_reason: Provider-reported termination reason, when available.
        tokens_used: Total tokens consumed for this file review, when available.
    """

    file_path: str
    outcome: Literal["approve", "request-changes", "request-changes-with-suggestion"]
    summary: str
    suggestions: list[dict[str, Any]] = field(default_factory=list)
    model_id: str | None = None
    provider_type: str | None = None
    latency_ms: int | None = None
    finish_reason: str | None = None
    tokens_used: int | None = None


# ---------------------------------------------------------------------------
# Pydantic models for LLM structured output (FR-003)
# ---------------------------------------------------------------------------


class SuggestionOutput(BaseModel):
    """Structured suggestion from the LLM for a single finding.

    All suggestions — including those marked ``out_of_scope=True`` — require a
    ``line`` anchor.  The ``out_of_scope`` flag classifies findings that reference
    a line not present in the diff (e.g., an architectural concern pointing at an
    unchanged file location); the finding is still posted as a line-anchored ADO
    thread, matching the v2 review pipeline's "still line-anchored" behaviour.
    """

    severity: Literal["high", "medium", "low"]
    content: str
    replacement_code: str | None = None
    line: int
    endLine: int | None = None
    out_of_scope: bool = False

    @model_validator(mode="after")
    def validate_anchor_fields(self) -> SuggestionOutput:
        """Enforce the line-anchor invariants used by the v2 review pipeline."""
        if self.line < 1:
            raise ValueError("line must be >= 1")
        if self.endLine is not None:
            if self.endLine < 1:
                raise ValueError("endLine must be >= 1")
            if self.endLine < self.line:
                raise ValueError("endLine must be >= line")
        return self


class FileReviewOutput(BaseModel):
    """Structured output schema passed to ``llm.with_structured_output()``.

    The LLM produces one of these per reviewed file.
    """

    outcome: Literal["approve", "request-changes", "request-changes-with-suggestion"]
    summary: str = Field(description="1-3 sentence rationale for the decision")
    suggestions: list[SuggestionOutput] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_outcome_requirements(self) -> FileReviewOutput:
        """Enforce outcome-specific suggestion requirements."""
        if self.outcome == "request-changes-with-suggestion":
            if not self.suggestions:
                raise ValueError("request-changes-with-suggestion requires at least one suggestion")
            if not any(
                suggestion.replacement_code and suggestion.replacement_code.strip() for suggestion in self.suggestions
            ):
                raise ValueError(
                    "request-changes-with-suggestion requires at least one suggestion with non-empty replacement_code"
                )
        return self
