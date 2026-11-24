"""Pydantic models for the render block types the server engine emits.

The pre-kind display families (flashcards, transcript, tasks, quiz, presentation,
recipe, timeline, diagram, research, structured_info, resources, progress,
comparison, troubleshooting, decision_tree, math_problem, questionnaire,
item_presentation, schema_proposal) were deleted in legacy-shapes step 5
(LEGACY-5): a kind arrives as a ``__kind`` instance.
"""

from .base import (
    BlockStatus,
    BlockType,
    RenderBlockEvent,
    RenderBlockState,
    StreamingBehavior,
)
from .media import ImageBlockData, VideoBlockData
from .mermaid import MermaidBlockData
from .table import TableBlockData
from .text import CodeBlockData, DiffBlockData, TextBlockData
from .thinking import ConsolidatedReasoningBlockData, ReasoningBlockData, ThinkingBlockData

__all__ = [
    # Base
    "BlockStatus",
    "BlockType",
    "RenderBlockState",
    "RenderBlockEvent",
    "StreamingBehavior",
    # Block data models
    "TextBlockData",
    "CodeBlockData",
    "DiffBlockData",
    "ThinkingBlockData",
    "ReasoningBlockData",
    "ConsolidatedReasoningBlockData",
    "ImageBlockData",
    "VideoBlockData",
    "MermaidBlockData",
    "TableBlockData",
]
