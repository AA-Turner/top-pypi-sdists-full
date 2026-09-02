"""Presentation/slideshow block data models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class SlideTheme(BaseModel):
    """Default theme — used when the LLM does not specify one."""

    model_config = _camel_config

    primary_color: str = "#2563eb"
    secondary_color: str = "#1e40af"
    accent_color: str = "#60a5fa"
    background_color: str = "#ffffff"
    text_color: str = "#1f2937"
    # Visual tier consumed by the FE renderer (SlideView): "generic" | "fancy"
    # | "deluxe". Defaults to "fancy" so decks look good without an explicit
    # choice; an agent sets it via theme.variant.
    variant: str = "fancy"
    font: str | None = None


class Slide(BaseModel):
    """
    A single slide.  LLMs produce different fields per slide type:
      - intro:   title, subtitle
      - content: title, description, bullets
    """

    model_config = _camel_config

    type: str = "content"
    title: str | None = None
    subtitle: str | None = None
    description: str | None = None
    bullets: list[str] = Field(default_factory=list)
    notes: str | None = None
    image_url: str | None = None
    quote: str | None = None
    author: str | None = None
    layout: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class PresentationBlockData(BaseModel):
    """
    Top-level data shape sent in block.data.

    BlockRenderer.tsx reads:
        sd.slides   → the slides array
        sd.theme    → the theme object
        sd.title    → optional presentation title

    The 'presentation' wrapper key is NOT used here — the inner fields
    are promoted to the top level so BlockRenderer can access them directly.
    """

    model_config = _camel_config

    title: str | None = None
    slides: list[Slide] = Field(default_factory=list)
    theme: SlideTheme = Field(default_factory=SlideTheme)
