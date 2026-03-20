"""Built-in review model schemas for session-level reviews.

These are the review models produced by the session-reviewer world.
They use the unified review data system from ``plato.worlds.review``.

Usage from the session-reviewer world::

    class SessionReviewerWorld(BaseReviewWorld[SessionReviewerConfig]):
        output_models = [
            SessionReviewIssue,
            SessionReviewRecommendation,
            SessionChunkSummary,
            SessionReviewSummary,
        ]
"""

from __future__ import annotations

from typing import Annotated, ClassVar

from pydantic import Field

from plato.worlds.review import RenderHint, ReviewData, StandardFeedback, review_model

# ---------------------------------------------------------------------------
# Session review issue
# ---------------------------------------------------------------------------


@review_model(
    name="session_review_issue",
    description="Issue identified during session review",
)
class SessionReviewIssue(ReviewData):
    """A single issue found by a session reviewer."""

    title: Annotated[str, RenderHint(widget="markdown", label="Title")] = ""
    description: Annotated[str, RenderHint(widget="markdown", label="Description")] = ""
    severity: Annotated[str, RenderHint(widget="severity_badge", label="Severity")] = "medium"
    category: Annotated[str, RenderHint(widget="tag_list", label="Category")] = ""
    supporting_span_ids: Annotated[list[str], RenderHint(widget="span_list", label="Evidence Spans")] = Field(
        default_factory=list
    )
    chunk_ids: Annotated[list[str], RenderHint(widget="tag_list", label="Inspected Chunks")] = Field(
        default_factory=list
    )

    Feedback: ClassVar[type] = StandardFeedback


# ---------------------------------------------------------------------------
# Session review recommendation
# ---------------------------------------------------------------------------


@review_model(
    name="session_review_recommendation",
    description="Actionable recommendation from session review",
)
class SessionReviewRecommendation(ReviewData):
    """An actionable recommendation from a session reviewer."""

    title: Annotated[str, RenderHint(widget="markdown", label="Title")] = ""
    description: Annotated[str, RenderHint(widget="markdown", label="Description")] = ""
    priority: Annotated[str, RenderHint(widget="severity_badge", label="Priority")] = "medium"
    category: Annotated[str, RenderHint(widget="tag_list", label="Category")] = ""
    supporting_span_ids: Annotated[list[str], RenderHint(widget="span_list", label="Evidence Spans")] = Field(
        default_factory=list
    )

    Feedback: ClassVar[type] = StandardFeedback


# ---------------------------------------------------------------------------
# Chunk summary (from session reviewer pipeline)
# ---------------------------------------------------------------------------


@review_model(
    name="session_chunk_summary",
    description="Summary of a span chunk from session analysis",
)
class SessionChunkSummary(ReviewData):
    """Summary annotation for a chunk of spans."""

    chunk_id: Annotated[str, RenderHint(widget="tag_list", label="Chunk ID")] = ""
    summary: Annotated[str, RenderHint(widget="markdown", label="Summary")] = ""
    span_count: Annotated[int, RenderHint(widget="score_bar", label="Spans")] = 0
    highlights: Annotated[str, RenderHint(widget="markdown", label="Highlights")] = ""
    supporting_span_ids: Annotated[list[str], RenderHint(widget="span_list", label="Evidence Spans")] = Field(
        default_factory=list
    )

    Feedback: ClassVar[type] = StandardFeedback


# ---------------------------------------------------------------------------
# Session review summary (overview report)
# ---------------------------------------------------------------------------


@review_model(
    name="session_review_summary",
    description="Overall session review summary with findings",
)
class SessionReviewSummary(ReviewData):
    """Top-level summary from a session review."""

    summary: Annotated[str, RenderHint(widget="markdown", label="Summary")] = ""
    issue_count: Annotated[int, RenderHint(widget="score_bar", label="Issues Found")] = 0
    recommendation_count: Annotated[int, RenderHint(widget="score_bar", label="Recommendations")] = 0
    inspected_chunks: Annotated[int, RenderHint(widget="score_bar", label="Chunks Inspected")] = 0
    review_kind: Annotated[str, RenderHint(widget="tag_list", label="Review Type")] = ""

    Feedback: ClassVar[type] = StandardFeedback


# All built-in review models — used as default for BaseWorld.review_models
DEFAULT_REVIEW_MODELS: list[type] = [
    SessionReviewIssue,
    SessionReviewRecommendation,
    SessionChunkSummary,
    SessionReviewSummary,
]
