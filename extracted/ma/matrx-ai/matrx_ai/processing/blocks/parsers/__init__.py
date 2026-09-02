"""Per-block parser functions for the server-side markdown processing pipeline."""

from matrx_ai.processing.blocks.parsers.comparison_parser import parse_comparison
from matrx_ai.processing.blocks.parsers.decision_tree_parser import parse_decision_tree
from matrx_ai.processing.blocks.parsers.diagram_parser import parse_diagram
from matrx_ai.processing.blocks.parsers.diff_parser import detect_diff_style, looks_like_diff
from matrx_ai.processing.blocks.parsers.flashcard_parser import parse_flashcards
from matrx_ai.processing.blocks.parsers.progress_parser import parse_progress
from matrx_ai.processing.blocks.parsers.questionnaire_parser import parse_questionnaire
from matrx_ai.processing.blocks.parsers.quiz_parser import parse_quiz
from matrx_ai.processing.blocks.parsers.recipe_parser import parse_recipe
from matrx_ai.processing.blocks.parsers.research_parser import parse_research
from matrx_ai.processing.blocks.parsers.resources_parser import parse_resources
from matrx_ai.processing.blocks.parsers.structured_info_parser import parse_structured_info
from matrx_ai.processing.blocks.parsers.table_parser import parse_table
from matrx_ai.processing.blocks.parsers.task_parser import parse_tasks
from matrx_ai.processing.blocks.parsers.timeline_parser import parse_timeline
from matrx_ai.processing.blocks.parsers.transcript_parser import parse_transcript
from matrx_ai.processing.blocks.parsers.troubleshooting_parser import parse_troubleshooting

__all__ = [
    "parse_comparison",
    "parse_decision_tree",
    "parse_diagram",
    "parse_flashcards",
    "parse_progress",
    "parse_questionnaire",
    "parse_quiz",
    "parse_recipe",
    "parse_research",
    "parse_resources",
    "parse_structured_info",
    "parse_table",
    "parse_tasks",
    "parse_timeline",
    "parse_transcript",
    "parse_troubleshooting",
    "looks_like_diff",
    "detect_diff_style",
]
