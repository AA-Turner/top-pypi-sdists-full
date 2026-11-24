"""A Stop inside an OPEN kind block saves the value the screen drew, not the grow text past it (P8-RUNS).

Live 2026-11-15 (Flashcard Generator, 30 cards, Stop ~55 s in, inside a ``flashcard_set`` block): 480
characters on screen at the press, 523 saved. A blocks-v2 client draws an open kind from its LAST
``block.partial`` value; partials are re-read only every eighth of growth (CPU budget), so the grow
watermark — where the stop used to cut — ran ahead of the drawn value. The cut (``shown_chars``, the one
point the seal, the stopped save and the close-off use) now stops at the last partial's source.
"""

from __future__ import annotations

import json

from matrx_graph.content_ir.partial import parse_partial_json

from matrx_ai.processing.blocks.blocks_v1 import blocks_v1_dicts
from matrx_ai.processing.blocks.live_blocks_v2 import LiveBlocksStreamV2

CARDS = ",\n".join(json.dumps({"front": f"Question number {i}?", "back": f"Answer {i}"}) for i in range(30))
TEXT = f'Here are your cards:\n\n```json\n{{"__kind":"flashcard_set","title":"Capitals",\n"cards":[\n{CARDS}\n]}}\n```\n\nDone.\n'


def _saved_kind_value(text: str):
    """The value a reload reads from the saved, cut-off kind: its source so far, read like a live partial."""
    kinds = [b for b in blocks_v1_dicts(text) if b.get("type") == "kind"]
    if not kinds:
        return None
    if kinds[-1].get("complete", True) is not False:
        return kinds[-1].get("value")
    body = text.encode("utf-8")[kinds[-1]["start"] :].decode("utf-8", errors="ignore").split("\n", 1)[1]
    return parse_partial_json(body)


def test_every_stop_inside_an_open_kind_saves_exactly_the_last_drawn_partial() -> None:
    stream = LiveBlocksStreamV2("m1")
    fed = ""
    drawn = None
    checked = 0
    mismatches: list[str] = []
    for i in range(0, len(TEXT), 7):  # a slow kind stream: a few characters at a time
        chunk = TEXT[i : i + 7]
        fed += chunk
        for ev in stream.feed(chunk):
            if ev.type == "block.partial":
                drawn = ev.model_dump()["value"]
            elif ev.type == "block.close" and ev.model_dump()["block"]["type"] == "kind":
                drawn = None
        if drawn is None:
            continue
        checked += 1
        saved = _saved_kind_value(fed[: stream.shown_chars])
        if saved != drawn:
            mismatches.append(
                f"at {len(fed)} chars: drew {len(drawn.get('cards', []))} cards, saved "
                f"{len((saved or {}).get('cards', []))}"
            )
    assert checked > 20, "the stream never drew an open kind"
    assert not mismatches, f"{len(mismatches)} of {checked} Stops saved more than was drawn: {mismatches[:3]}"


def test_the_close_off_closes_an_open_kind_at_the_drawn_value() -> None:
    stream = LiveBlocksStreamV2("m1")
    drawn = None
    cut_at = TEXT.index('"Question number 20')
    for i in range(0, cut_at, 7):
        for ev in stream.feed(TEXT[i : min(i + 7, cut_at)]):
            if ev.type == "block.partial":
                drawn = ev.model_dump()["value"]
    closes = [e.model_dump() for e in stream.close_off() if e.type == "block.close"]
    kind_close = next(c for c in closes if c["block"]["type"] == "kind")
    end = kind_close["end"]  # bytes into the part (one part here, starting at the reply's first byte)
    assert _saved_kind_value(TEXT.encode("utf-8")[:end].decode("utf-8")) == drawn, (
        "the close-off closed the kind past the value the screen drew"
    )
