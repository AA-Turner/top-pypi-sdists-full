"""Pydantic models for all render block types."""

from .base import (
    BlockStatus,
    BlockType,
    RenderBlockEvent,
    RenderBlockState,
    StreamingBehavior,
)
from .comparison import ComparisonBlockData, ComparisonCriterion
from .decision_tree import DecisionNode, DecisionTreeBlockData
from .diagram import DiagramBlockData, DiagramEdge, DiagramLayout, DiagramNode, Position
from .flashcards import FlashcardItem, FlashcardsBlockData
from .math_problem import MathProblemBlockData
from .media import ImageBlockData, VideoBlockData
from .mermaid import MermaidBlockData
from .presentation import PresentationBlockData, Slide, SlideTheme
from .progress import ProgressCategory, ProgressItem, ProgressTrackerBlockData
from .questionnaire import QuestionnaireBlockData, QuestionnaireSection
from .quiz import QuizBlockData, QuizQuestion
from .recipe import Ingredient, RecipeBlockData, RecipeStep
from .research import ResearchBlockData, ResearchSection
from .resources import ResourceCategory, ResourceItem, ResourcesBlockData
from .structured_info import (
    StructuredInfoBlockData,
    StructuredInfoItem,
    StructuredInfoSection,
)
from .table import TableBlockData
from .tasks import TaskItem, TasksBlockData
from .text import CodeBlockData, DiffBlockData, TextBlockData
from .thinking import ConsolidatedReasoningBlockData, ReasoningBlockData, ThinkingBlockData
from .timeline import TimelineBlockData, TimelineEvent, TimelinePeriod
from .transcript import TranscriptBlockData, TranscriptSegment
from .troubleshooting import (
    TroubleshootingBlockData,
    TroubleshootingIssue,
    TroubleshootingSolution,
    TroubleshootingStep,
)

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
    "FlashcardItem",
    "FlashcardsBlockData",
    "TranscriptSegment",
    "TranscriptBlockData",
    "TaskItem",
    "TasksBlockData",
    "QuizQuestion",
    "QuizBlockData",
    "Slide",
    "SlideTheme",
    "PresentationBlockData",
    "Ingredient",
    "RecipeStep",
    "RecipeBlockData",
    "TimelineEvent",
    "TimelinePeriod",
    "TimelineBlockData",
    "Position",
    "DiagramNode",
    "DiagramEdge",
    "DiagramLayout",
    "DiagramBlockData",
    "MermaidBlockData",
    "TableBlockData",
    "ResearchSection",
    "ResearchBlockData",
    "StructuredInfoItem",
    "StructuredInfoSection",
    "StructuredInfoBlockData",
    "ResourceItem",
    "ResourceCategory",
    "ResourcesBlockData",
    "ProgressItem",
    "ProgressCategory",
    "ProgressTrackerBlockData",
    "ComparisonCriterion",
    "ComparisonBlockData",
    "TroubleshootingStep",
    "TroubleshootingSolution",
    "TroubleshootingIssue",
    "TroubleshootingBlockData",
    "DecisionNode",
    "DecisionTreeBlockData",
    "MathProblemBlockData",
    "QuestionnaireSection",
    "QuestionnaireBlockData",
]
