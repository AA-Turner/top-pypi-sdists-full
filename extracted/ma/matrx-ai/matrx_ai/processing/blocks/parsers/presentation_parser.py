"""Presentation parser.

Accepts both snake_case and camelCase field names from the LLM.

Expected LLM JSON shape:
    {
        "presentation": {
            "title": "string",
            "slides": [
                {"type": "intro",    "title": "...", "subtitle": "..."},
                {"type": "content",  "title": "...", "description": "...", "bullets": [...]}
            ],
            "theme": { ... }   # optional — defaults applied if missing
        }
    }

The inner dict may also be passed without the "presentation" wrapper key.

Output (block.data):
    {
        "title": "...",
        "slides": [...],
        "theme": { "primaryColor": ..., ... }
    }

BlockRenderer.tsx reads sd.slides and sd.theme directly off the data object,
so we return these fields at the top level (no "presentation" nesting).
"""

from __future__ import annotations

import json
import re

from matrx_ai.processing.blocks.models.presentation import PresentationBlockData, Slide, SlideTheme
from matrx_ai.processing.blocks.parsers._llm_json import loads_block_json

_CODE_BLOCK_RE = re.compile(r'```(?:json)?\s*([\s\S]*?)\s*```')

_KNOWN_SLIDE_KEYS = {
    "type", "title", "subtitle", "description", "bullets",
    "notes", "image_url", "imageUrl", "quote", "author", "layout",
}


def _get(d: dict, *keys: str, default=None):
    for k in keys:
        if k in d:
            return d[k]
    return default


def parse_presentation(content: str) -> PresentationBlockData | None:
    """
    Parse presentation JSON into PresentationBlockData.

    Returns None if the content is not parseable or structurally invalid.
    """
    try:
        json_content = content.strip()
        m = _CODE_BLOCK_RE.search(json_content)
        if m:
            json_content = m.group(1).strip()
        parsed = loads_block_json(json_content)
    except (json.JSONDecodeError, ValueError):
        return None

    if not isinstance(parsed, dict):
        return None

    # Accept {"presentation": {...}} wrapper or the inner dict directly
    if "presentation" in parsed and isinstance(parsed["presentation"], dict):
        inner_raw = parsed["presentation"]
    else:
        inner_raw = parsed

    slides_raw = _get(inner_raw, "slides")
    if not isinstance(slides_raw, list) or len(slides_raw) == 0:
        return None

    slides: list[Slide] = []
    for raw_slide in slides_raw:
        slide = _parse_slide(raw_slide)
        if slide is None:
            return None
        slides.append(slide)

    # Theme — optional, use defaults if absent or malformed
    theme_raw = inner_raw.get("theme")
    if isinstance(theme_raw, dict):
        theme = SlideTheme(
            primary_color=_get(theme_raw, "primaryColor", "primary_color", default="#2563eb"),
            secondary_color=_get(theme_raw, "secondaryColor", "secondary_color", default="#1e40af"),
            accent_color=_get(theme_raw, "accentColor", "accent_color", default="#60a5fa"),
            background_color=_get(theme_raw, "backgroundColor", "background_color", default="#ffffff"),
            text_color=_get(theme_raw, "textColor", "text_color", default="#1f2937"),
        )
    else:
        theme = SlideTheme()

    return PresentationBlockData(
        title=inner_raw.get("title"),
        slides=slides,
        theme=theme,
    )


def _parse_slide(raw: object) -> Slide | None:
    if not isinstance(raw, dict):
        return None
    extra = {k: v for k, v in raw.items() if k not in _KNOWN_SLIDE_KEYS}
    return Slide(
        type=raw.get("type", "content"),
        title=raw.get("title"),
        subtitle=raw.get("subtitle"),
        description=raw.get("description"),
        bullets=raw.get("bullets") if isinstance(raw.get("bullets"), list) else [],
        notes=raw.get("notes"),
        image_url=_get(raw, "image_url", "imageUrl"),
        quote=raw.get("quote"),
        author=raw.get("author"),
        layout=raw.get("layout"),
        extra=extra,
    )
