"""Base models for the render block streaming protocol."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BlockStatus(str, Enum):
    """Lifecycle status of a content block."""

    STREAMING = "streaming"
    COMPLETE = "complete"
    ERROR = "error"


class StreamingBehavior(str, Enum):
    """How a block type behaves during streaming."""

    INCREMENTAL = "incremental"          # Text-like: content grows token-by-token (Text Channel)
    SEMANTIC_STREAM = "semantic_stream"  # Stateful parser emits growing snapshot at semantic boundaries
    PARTIAL_UPDATES = "partial_updates"  # Stateless parser on every change; returns completed items only
    MARKDOWN_COMPLETE = "markdown_complete"  # Stream raw content; parse data only on close
    COMPLETE_ONLY = "complete_only"      # JSON-based: parse only when complete and valid


class BlockType(str, Enum):
    """All supported content block types."""

    TEXT = "text"
    CODE = "code"
    TABLE = "table"
    THINKING = "thinking"
    REASONING = "reasoning"
    CONSOLIDATED_REASONING = "consolidated_reasoning"
    IMAGE = "image"
    VIDEO = "video"
    TASKS = "tasks"
    TRANSCRIPT = "transcript"
    STRUCTURED_INFO = "structured_info"
    QUESTIONNAIRE = "questionnaire"
    FLASHCARDS = "flashcards"
    QUIZ = "quiz"
    PRESENTATION = "presentation"
    COOKING_RECIPE = "cooking_recipe"
    TIMELINE = "timeline"
    PROGRESS_TRACKER = "progress_tracker"
    COMPARISON_TABLE = "comparison_table"
    TROUBLESHOOTING = "troubleshooting"
    RESOURCES = "resources"
    DECISION_TREE = "decision_tree"
    DECISION = "decision"
    RESEARCH = "research"
    DIAGRAM = "diagram"
    MERMAID = "mermaid"
    MATH_PROBLEM = "math_problem"
    ARTIFACT = "artifact"
    # XML pass-through types (rendered as markdown text)
    INFO = "info"
    TASK = "task"
    DATABASE = "database"
    PRIVATE = "private"
    PLAN = "plan"
    EVENT = "event"
    TOOL = "tool"


# ---------------------------------------------------------------------------
# RenderBlockEvent — the NDJSON payload sent to the client
# ---------------------------------------------------------------------------

class RenderBlockEvent(BaseModel):
    """
    A single NDJSON event representing a render block or an update to one.

    Sent as: {"event": "render_block", "data": <this model>}

    All fields are serialized as camelCase so every client receives a uniform
    contract without any field renaming on the client side.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    block_id: str = Field(description="Stable ID for this block within the message (e.g. 'blk_0')")
    block_index: int = Field(description="Ordering position among all blocks")
    type: str = Field(description="Block type key, e.g. 'text', 'flashcards', 'quiz'")
    status: BlockStatus = Field(description="Lifecycle status")
    content: str | None = Field(default=None, description="For text-like blocks: raw content string (append-friendly)")
    data: dict[str, Any] | None = Field(default=None, description="For structured blocks: parsed, render-ready data")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Optional metadata (language, isComplete, counts, etc.)")

    def to_stream_event(self) -> dict[str, Any]:
        """Serialize to the NDJSON stream event format with camelCase keys."""
        return {
            "event": "render_block",
            "data": self.model_dump(by_alias=True, exclude_none=True),
        }


# ---------------------------------------------------------------------------
# RenderBlockState — internal representation used by the processor
# ---------------------------------------------------------------------------

class RenderBlockState(BaseModel):
    """Internal block state maintained by StreamBlockProcessor."""

    block_id: str
    block_index: int
    type: str
    status: BlockStatus = BlockStatus.STREAMING
    content: str = ""
    data: dict[str, Any] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    raw_content: str = ""  # Accumulator for unparsed content (used by structured blocks)

    def to_event(self) -> RenderBlockEvent:
        """Convert to a streamable event."""
        return RenderBlockEvent(
            block_id=self.block_id,
            block_index=self.block_index,
            type=self.type,
            status=self.status,
            content=self.content if self.content else None,
            data=self.data,
            metadata=self.metadata,
        )
