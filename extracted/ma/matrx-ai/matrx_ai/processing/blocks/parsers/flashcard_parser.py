"""Flashcard parser — port of flashcard-parser.ts."""

from __future__ import annotations

import re

from matrx_ai.processing.blocks.models.flashcards import FlashcardItem, FlashcardsBlockData

_FRONT_RE = re.compile(r'^(?:Front|Question):\s*(.*)', re.IGNORECASE)
_BACK_RE = re.compile(r'^(?:Back|Answer):\s*(.*)', re.IGNORECASE)


def parse_flashcards(content: str, *, is_final: bool = False) -> FlashcardsBlockData:
    """
    Parse flashcard content into a growing snapshot.

    Returns a single `cards` list that grows as the LLM writes:
      - Front sealed, back still being written → card appended with back=None
        (React shows a spinner on the back face — Loader Exception).
      - Both sides sealed → card appended with back=str.
      - On finalize (is_final=True) → in-progress back is flushed as-is.

    React reads one list. No partial_card field to merge.
    """
    lines = content.split("\n")
    cards: list[FlashcardItem] = []
    current_front: str | None = None
    current_back_lines: list[str] = []
    collecting_back = False
    is_complete = "</flashcards>" in content

    def seal_card(back_text: str | None) -> None:
        nonlocal current_front, current_back_lines, collecting_back
        if current_front is not None:
            cards.append(FlashcardItem(front=current_front, back=back_text))
            current_front = None
        collecting_back = False
        current_back_lines = []

    for line in lines:
        stripped = line.strip()

        if stripped == "---":
            if collecting_back:
                back_text = "\n".join(current_back_lines).strip() or None
                seal_card(back_text)
            elif current_front:
                seal_card(None)
            continue

        front_m = _FRONT_RE.match(stripped)
        if front_m:
            # Starting a new card — seal whatever was in progress
            if collecting_back:
                back_text = "\n".join(current_back_lines).strip() or None
                seal_card(back_text)
            elif current_front:
                seal_card(None)
            current_front = front_m.group(1).strip()
            collecting_back = False
            current_back_lines = []
            continue

        back_m = _BACK_RE.match(stripped)
        if back_m:
            collecting_back = True
            current_back_lines = []
            inline = back_m.group(1).strip()
            if inline:
                current_back_lines.append(inline)
            continue

        if collecting_back:
            current_back_lines.append(stripped if stripped else "")
            continue

        # Continuation of front text
        if current_front and not collecting_back and stripped:
            current_front += " " + stripped

    # Handle in-progress card at end of content
    if collecting_back:
        back_text = "\n".join(current_back_lines).strip() or None
        if is_final:
            # Finalize — include whatever back text exists
            seal_card(back_text)
        elif current_front is not None:
            # Streaming — front is sealed, back is still being written → back=None
            # (Loader Exception: React shows a spinner)
            seal_card(None)
    elif current_front:
        # Front seen, no back started yet
        if is_final:
            seal_card(None)
        else:
            # Still streaming — front may still be growing, withhold it
            pass

    return FlashcardsBlockData(cards=cards, is_complete=is_complete)
