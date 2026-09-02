"""Flashcards block data models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class FlashcardItem(BaseModel):
    """
    A single flashcard.

    `back` is None when the front has been sealed but the back is still being
    written (Loader Exception — React renders a spinner on the back face).
    `back` is an empty string only if the LLM explicitly produced no back text.
    """

    front: str
    back: str | None = None


class FlashcardsBlockData(BaseModel):
    """
    Parsed flashcard data — a growing snapshot of all cards seen so far.

    React reads a single `cards` list. Cards appear as the LLM writes them:
      - front sealed, back being written → back=None (show spinner)
      - both sides sealed → back=str (show answer)
    No `partial_card` field — React always reads one list.
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    cards: list[FlashcardItem]
    is_complete: bool = False
