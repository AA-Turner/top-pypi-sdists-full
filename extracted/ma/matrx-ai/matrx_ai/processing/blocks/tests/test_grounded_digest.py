"""The grounded Gemini digest is working text, never the answer (P1-CHAT).

The translator's grounded JSON contract makes the model START with ``GROUNDED_DIGEST_HEADING`` and write a
150-word digest before its one ``json`` fence. The ONE splitter reads exactly that heading (any ``#`` level or
bold form) as one ``reasoning`` block, tag ``digest``, from the heading to the fence; the JSON after it reads as
it always did. Every door agrees: the save's blocks, the live v1 events (reasoning never sits in a text part),
the stopped partial's thinking part, the staged ``label`` behind ``blocks_v2_save_enabled``.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.processing.blocks.blocks_v1 import blocks_v1_dicts, could_become_digest_heading, is_digest_heading
from matrx_ai.processing.blocks.live_blocks import LiveBlocksStream
from matrx_ai.processing.blocks.reasoning_parts import inline_reasoning_parts
from matrx_ai.schema.answer_contract import GROUNDED_DIGEST_HEADING

JSON = '```json\n{"__kind":"flashcard_set","title":"x","cards":[{"front":"a","back":"b"}]}\n```\n'
DIGEST = f"{GROUNDED_DIGEST_HEADING}\nThe line opened in 2024 [1]. Ridership grew.\n\nMore sourced facts.\n\n"


def test_the_translator_contract_names_the_one_constant() -> None:
    from matrx_ai.providers.google.translator import GoogleTranslator

    assert f"heading `{GROUNDED_DIGEST_HEADING}`" in GoogleTranslator._grounded_json_text_contract({"type": "object"})


@pytest.mark.parametrize(
    "heading",
    [GROUNDED_DIGEST_HEADING, f"# {GROUNDED_DIGEST_HEADING}", f"### {GROUNDED_DIGEST_HEADING}", f"**{GROUNDED_DIGEST_HEADING}**",
     f"`{GROUNDED_DIGEST_HEADING}`", f"{GROUNDED_DIGEST_HEADING}:", f"## **{GROUNDED_DIGEST_HEADING}:**"],
)
def test_every_form_of_the_heading_opens_the_digest(heading: str) -> None:
    assert is_digest_heading(heading + "\n")
    blocks = blocks_v1_dicts(f"{heading}\nfacts\n\n{JSON}")
    assert [b["type"] for b in blocks] == ["reasoning", "kind"]
    digest = blocks[0]
    assert (digest["tag"], digest["complete"]) == ("digest", True)


@pytest.mark.parametrize("line", ["Grounded research digest", f"{GROUNDED_DIGEST_HEADING} today", f"- {GROUNDED_DIGEST_HEADING}", f"> {GROUNDED_DIGEST_HEADING}"])
def test_only_the_contracts_exact_heading_counts(line: str) -> None:
    assert not is_digest_heading(line)
    assert all(b["type"] != "reasoning" for b in blocks_v1_dicts(f"{line}\nfacts\n"))


def test_only_the_first_non_blank_line_can_open_it() -> None:
    assert all(b["type"] != "reasoning" for b in blocks_v1_dicts(f"Intro.\n\n{DIGEST}{JSON}"))
    blocks = blocks_v1_dicts(f"\n\n{DIGEST}{JSON}")
    assert [b["type"] for b in blocks] == ["markdown", "reasoning", "kind"]


def test_the_digest_spans_heading_to_the_json_fence_and_the_json_reads_as_before() -> None:
    text = DIGEST + JSON
    raw = text.encode()
    digest, kind = blocks_v1_dicts(text)
    assert raw[digest["start"] : digest["start"] + 24] == GROUNDED_DIGEST_HEADING.encode()
    assert raw[digest["end"] :].startswith(b"```json")
    assert raw[digest["body_start"] : digest["body_end"]].startswith(b"The line opened")
    assert (kind["type"], kind["kind"], kind["complete"]) == ("kind", "flashcard_set", True)
    assert kind["start"] == digest["end"]


def test_another_fence_inside_the_digest_does_not_end_it() -> None:
    blocks = blocks_v1_dicts(f"{GROUNDED_DIGEST_HEADING}\nsee\n```python\nx = 1\n```\nmore\n{JSON}")
    assert [b["type"] for b in blocks] == ["reasoning", "kind"]


def test_no_fence_ever_arriving_the_whole_text_is_the_digest_incomplete() -> None:
    (digest,) = blocks_v1_dicts(f"{GROUNDED_DIGEST_HEADING}\nfacts so far")
    assert digest["type"] == "reasoning" and digest["complete"] is False


def test_a_cut_inside_the_json_leaves_the_digest_complete_and_the_kind_incomplete() -> None:
    digest, kind = blocks_v1_dicts(f'{DIGEST}```json\n{{"__kind":"flashcard_set","title":"x",\n"cards":[{{"front":"a"')
    assert digest["complete"] is True
    assert (kind["type"], kind["complete"]) == ("kind", False)


def test_a_saved_partial_keeps_the_digest_as_a_thinking_part_and_the_json_as_text() -> None:
    parts = inline_reasoning_parts(DIGEST + JSON)
    assert [type(p) for p in parts] == [ThinkingContent, TextContent]
    assert parts[0].text.startswith("The line opened") and parts[1].text.startswith("```json")


def test_live_v1_never_draws_the_digest_as_a_text_part() -> None:
    stream = LiveBlocksStream("m1")
    events = []
    for i in range(0, len(DIGEST + JSON), 7):
        events += stream.feed((DIGEST + JSON)[i : i + 7])
    events += stream.finish()
    opened = [e for e in events if e.type == "block.open"]
    assert [e.block_type for e in opened] == ["kind"]
    assert not any(e.type == "block.close" and e.block.type == "markdown" for e in events)


def test_live_v2_opens_the_digest_on_its_heading_line_with_the_servers_label() -> None:
    from matrx_ai.processing.blocks.live_blocks_v2 import LiveBlocksStreamV2

    stream = LiveBlocksStreamV2("m1")
    held = stream.feed(GROUNDED_DIGEST_HEADING)
    assert held == [], "a line that could still become the heading draws nothing"
    events = stream.feed("\nThe line")
    opened = next(e for e in events if e.type == "reasoning.open")
    assert (opened.tag, opened.label, opened.position) == ("digest", "Research notes", 0)
    assert "".join(e.text for e in events if e.type == "reasoning.grow") == "The line"
    rest = stream.feed(" opened.\n\n" + JSON) + stream.finish()
    assert next(e for e in rest if e.type == "reasoning.close").complete is True
    assert next(e for e in rest if e.type == "block.open").block_type == "kind"


def test_a_first_line_that_is_not_the_heading_streams_at_once() -> None:
    from matrx_ai.processing.blocks.live_blocks_v2 import LiveBlocksStreamV2

    stream = LiveBlocksStreamV2("m1")
    assert any(e.type == "block.grow" for e in stream.feed("GROUNDED RESEARCH is something else"))


def test_the_label_is_staged_behind_the_save_knob() -> None:
    from matrx_ai.processing.blocks import saved_blocks

    text = DIGEST + JSON
    off = saved_blocks.block_fields(text)["blocks"][0]
    assert off["tag"] == "digest" and "label" not in off
    saved_blocks.configure_block_regions_save(lambda: True)
    saved_blocks.configure_blocks_v2_save(lambda: True)
    try:
        fields = saved_blocks.block_fields(text)
    finally:
        saved_blocks.configure_blocks_v2_save(None)
        saved_blocks.configure_block_regions_save(None)
    # The label lives in blocks2 (the full reading); v1 stays exactly as installed readers decode it.
    assert "label" not in fields["blocks"][0]
    assert fields["blocks2"]["blocks"][0]["label"] == "Research notes"


def test_a_heading_prefix_is_held_and_a_longer_line_is_not() -> None:
    assert could_become_digest_heading("")
    assert could_become_digest_heading("## GROUND")
    assert could_become_digest_heading(f"**{GROUNDED_DIGEST_HEADING}")
    assert could_become_digest_heading(f"{GROUNDED_DIGEST_HEADING}**")
    assert not could_become_digest_heading("Hello")
    assert not could_become_digest_heading(f"{GROUNDED_DIGEST_HEADING} and")


def test_a_digest_after_an_inline_thought_is_still_the_digest() -> None:
    # Gemini streams its thought inline first: the text part after it starts with the heading.
    blocks = blocks_v1_dicts(f"<reasoning>\nthinking\n</reasoning>\n{DIGEST}{JSON}")
    assert [(b["type"], b.get("tag")) for b in blocks] == [("reasoning", "reasoning"), ("reasoning", "digest"), ("kind", None)]


def test_a_latex_deck_after_a_non_ascii_digest_is_one_kind_at_its_fence_byte() -> None:
    """Message 63ade91c: a digest with non-ASCII text (``–``) then a deck whose JSON holds LaTeX (``\\\\(`` in the
    source). The server reads it right — one digest, one kind valued from the JSON, offsets in UTF-8 bytes with the kind
    starting at its fence. (The client's reader called this kind prose; its guard is rich-content's
    a-kind-with-escaped-backslashes-draws-as-its-card and chat-app's a-saved-deck-after-a-digest-draws-as-cards.)"""
    import json

    deck = {"__kind": "flashcard_set", "title": "Volcanoes", "cards": [{"front": "Silica?", "back": "Basalt: \\(\\approx 45\\text{--}52\\%\\)"}]}
    digest = f"{GROUNDED_DIGEST_HEADING}\nMafic magmas are low in silica (\\(\\sim 45\\text{{--}}52\\%\\)) – hotter and fluid.\n\n"
    fence = "```json\n" + json.dumps(deck) + "\n```"
    text = digest + fence
    blocks = blocks_v1_dicts(text)
    assert [b["type"] for b in blocks] == ["reasoning", "kind"]
    assert blocks[0]["tag"] == "digest"
    raw = text.encode("utf-8")
    assert blocks[1]["start"] == len(digest.encode("utf-8")) and raw[blocks[1]["start"] :].startswith(b"```json")
    assert blocks[1]["end"] == len(raw)
    assert blocks[1]["value"]["cards"][0]["back"] == deck["cards"][0]["back"]
