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
    "TableBlockData":                   "table.py",
    "MermaidBlockData":                 "mermaid.py",
}

# ---------------------------------------------------------------------------
# Ordered class emission list (dep-first — leaf models before composites)
# ---------------------------------------------------------------------------

BLOCK_DATA_CLASS_ORDER: list[str] = [
    # The pre-kind display families' models were deleted in legacy-shapes step 5
    # (LEGACY-5): a kind arrives as a ``__kind`` instance.
    "TextBlockData", "CodeBlockData", "DiffBlockData",
    "ThinkingBlockData", "ReasoningBlockData", "ConsolidatedReasoningBlockData",
    "ImageBlockData", "VideoBlockData",
    "MermaidBlockData", "TableBlockData",
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
    ("decision",                None),
    ("mermaid",                 "MermaidBlockData"),
    ("artifact",                None),
]
