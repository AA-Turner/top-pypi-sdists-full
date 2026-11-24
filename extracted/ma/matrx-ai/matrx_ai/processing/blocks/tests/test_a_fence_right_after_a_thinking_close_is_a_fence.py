"""`</thinking>```json` — a fence opening on the same line a reasoning tag closed — is a fence in v2 ONLY (chat.message a9a5ebf2).

v1 `blocks` (www, frozen by Arman) read this shape exactly as before until he rules otherwise.

Before: the rest of the line was a markdown fragment, so the fence was never seen: the kind inside it was lifted from the
middle of an unseen fence, leaving "```json" and the closing "```" as two cut-off code regions around the deck.
"""

from __future__ import annotations

from matrx_ai.processing.blocks.blocks_v1 import blocks_v1_dicts, split_blocks_v1
from matrx_ai.processing.blocks.saved_blocks import block_fields

DECK = '{"__kind": "flashcard_set", "title": "T", "cards": [{"__kind": "flashcard", "front": "a", "back": "b"}]}'


def _shape(text: str) -> list[tuple[str, int, int]]:
    return [(b.type, b.start, b.end) for b in split_blocks_v1(text, fence_after_tag=True)]


def test_fence_after_a_closed_thinking_tag_holds_the_kind_whole() -> None:
    text = f"<thinking>\nplan\n</thinking>```json\n{DECK}\n```"
    blocks = split_blocks_v1(text, fence_after_tag=True)
    assert [b.type for b in blocks] == ["reasoning", "kind"]
    kind = blocks[1]
    assert text[kind.start : kind.end].startswith("```json") and text[kind.start : kind.end].endswith("```")


def test_same_after_a_newline_is_unchanged() -> None:
    text = f"<thinking>\nplan\n</thinking>\n```json\n{DECK}\n```"
    assert [t for t, _, _ in _shape(text)][-1] == "kind"
    assert "markdown" not in [t for t, s, e in _shape(text) if text[s:e].strip() in ("```json", "```")]


def test_v1_blocks_of_the_glued_shape_are_exactly_what_they_were() -> None:
    text = f"<thinking>\nplan\n</thinking>```json\n{DECK}\n```"
    blocks = blocks_v1_dicts(text)
    assert [b["type"] for b in blocks] == ["reasoning", "markdown", "kind", "markdown"]
    assert [(b["start"], b["end"]) for b in blocks] == [(0, 27), (27, 35), (35, 140), (140, 143)]


def test_the_save_keeps_v1_as_before_and_reads_blocks2_with_the_fence() -> None:
    text = f"<thinking>\nplan\n</thinking>```json\n{DECK}\n```"
    fields = block_fields(text)
    assert [b["type"] for b in fields["blocks"]] == ["reasoning", "markdown", "kind", "markdown"]
    blocks2 = fields.get("blocks2")
    if blocks2 is not None:
        assert [b["type"] for b in blocks2["blocks"]] == ["reasoning", "kind"]
