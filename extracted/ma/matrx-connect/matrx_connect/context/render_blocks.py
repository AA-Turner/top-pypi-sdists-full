"""Render block type registry.

Maps RenderBlockPayload.type values to their typed data model classes from
matrx_ai.processing.blocks.models.  The TS generator reads this to emit
TypedRenderBlock discriminated union members without any hardcoded strings.

None as the data entry means no structured data model — the TS side uses
Record<string, unknown> for the data field.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Block model location map
# class_name → module filename inside matrx_ai/processing/blocks/models/
# ---------------------------------------------------------------------------

BLOCK_MODEL_FILES: dict[str, str] = {
    "TextBlockData":                    "text.py",
    "CodeBlockData":                    "text.py",
    "DiffBlockData":                    "text.py",
    "ThinkingBlockData":                "thinking.py",
    "ReasoningBlockData":               "thinking.py",
    "ConsolidatedReasoningBlockData":   "thinking.py",
    "ImageBlockData":                   "media.py",
    "VideoBlockData":                   "media.py",
    "FlashcardsBlockData":              "flashcards.py",
    "FlashcardItem":                    "flashcards.py",
    "TranscriptBlockData":              "transcript.py",
    "TranscriptSegment":                "transcript.py",
    "TasksBlockData":                   "tasks.py",
    "TaskItem":                         "tasks.py",
    "QuizBlockData":                    "quiz.py",
    "QuizQuestion":                     "quiz.py",
    "PresentationBlockData":            "presentation.py",
    "Slide":                            "presentation.py",
    "SlideTheme":                       "presentation.py",
    "RecipeBlockData":                  "recipe.py",
    "Ingredient":                       "recipe.py",
    "RecipeStep":                       "recipe.py",
    "TimelineBlockData":                "timeline.py",
    "TimelinePeriod":                   "timeline.py",
    "TimelineEvent":                    "timeline.py",
    "DiagramBlockData":                 "diagram.py",
    "DiagramNode":                      "diagram.py",
    "DiagramEdge":                      "diagram.py",
    "DiagramLayout":                    "diagram.py",
    "Position":                         "diagram.py",
    "TableBlockData":                   "table.py",
    "ResearchBlockData":                "research.py",
    "ResearchSection":                  "research.py",
    "ResourcesBlockData":               "resources.py",
    "ResourceCategory":                 "resources.py",
    "ResourceItem":                     "resources.py",
    "ProgressTrackerBlockData":         "progress.py",
    "ProgressCategory":                 "progress.py",
    "ProgressItem":                     "progress.py",
    "ComparisonBlockData":              "comparison.py",
    "ComparisonCriterion":              "comparison.py",
    "TroubleshootingBlockData":         "troubleshooting.py",
    "TroubleshootingIssue":             "troubleshooting.py",
    "TroubleshootingSolution":          "troubleshooting.py",
    "TroubleshootingStep":              "troubleshooting.py",
    "DecisionTreeBlockData":            "decision_tree.py",
    "DecisionNode":                     "decision_tree.py",
    "MathProblemBlockData":             "math_problem.py",
    "MermaidBlockData":                 "mermaid.py",
    "QuestionnaireBlockData":           "questionnaire.py",
    "QuestionnaireSection":             "questionnaire.py",
}

# ---------------------------------------------------------------------------
# Ordered class emission list (dep-first — leaf models before composites)
# ---------------------------------------------------------------------------

BLOCK_DATA_CLASS_ORDER: list[str] = [
    # Leaf models
    "FlashcardItem", "TranscriptSegment", "TaskItem", "QuizQuestion",
    "Slide", "SlideTheme", "Ingredient", "RecipeStep",
    "TimelineEvent", "TimelinePeriod",
    "Position", "DiagramNode", "DiagramEdge", "DiagramLayout",
    "ResourceItem", "ResourceCategory",
    "ProgressItem", "ProgressCategory",
    "ComparisonCriterion",
    "TroubleshootingStep", "TroubleshootingSolution", "TroubleshootingIssue",
    "DecisionNode",
    "QuestionnaireSection",
    # Top-level block data models
    "TextBlockData", "CodeBlockData", "DiffBlockData",
    "ThinkingBlockData", "ReasoningBlockData", "ConsolidatedReasoningBlockData",
    "ImageBlockData", "VideoBlockData",
    "FlashcardsBlockData", "TranscriptBlockData", "TasksBlockData", "QuizBlockData",
    "PresentationBlockData", "RecipeBlockData", "TimelineBlockData",
    "DiagramBlockData", "MermaidBlockData", "TableBlockData",
    "ResearchSection", "ResearchBlockData",
    "ResourcesBlockData", "ProgressTrackerBlockData",
    "ComparisonBlockData", "TroubleshootingBlockData", "DecisionTreeBlockData",
    "MathProblemBlockData", "QuestionnaireBlockData",
]

# ---------------------------------------------------------------------------
# Block type → data model class name
# None means no structured data → TS side emits Record<string, unknown>
# ---------------------------------------------------------------------------

RENDER_BLOCK_DATA_MAP: list[tuple[str, str | None]] = [
    ("text",                    "TextBlockData"),
    ("code",                    "CodeBlockData"),
    ("table",                   "TableBlockData"),
    ("thinking",                "ThinkingBlockData"),
    ("reasoning",               "ReasoningBlockData"),
    ("consolidated_reasoning",  "ConsolidatedReasoningBlockData"),
    ("image",                   "ImageBlockData"),
    ("video",                   "VideoBlockData"),
    ("tasks",                   "TasksBlockData"),
    ("transcript",              "TranscriptBlockData"),
    ("structured_info",         None),
    ("questionnaire",           "QuestionnaireBlockData"),
    ("flashcards",              "FlashcardsBlockData"),
    ("quiz",                    "QuizBlockData"),
    ("presentation",            "PresentationBlockData"),
    ("cooking_recipe",          "RecipeBlockData"),
    ("timeline",                "TimelineBlockData"),
    ("progress_tracker",        "ProgressTrackerBlockData"),
    ("comparison_table",        "ComparisonBlockData"),
    ("troubleshooting",         "TroubleshootingBlockData"),
    ("resources",               "ResourcesBlockData"),
    ("decision_tree",           "DecisionTreeBlockData"),
    ("decision",                None),
    ("research",                "ResearchBlockData"),
    ("diagram",                 "DiagramBlockData"),
    ("mermaid",                 "MermaidBlockData"),
    ("math_problem",            "MathProblemBlockData"),
    ("artifact",                None),
    # XML pass-through types — text channel, no structured data field
    ("info",                    "TextBlockData"),
    ("task",                    "TextBlockData"),
    ("database",                "TextBlockData"),
    ("private",                 "TextBlockData"),
    ("plan",                    "TextBlockData"),
    ("event",                   "TextBlockData"),
    ("tool",                    "TextBlockData"),
]
