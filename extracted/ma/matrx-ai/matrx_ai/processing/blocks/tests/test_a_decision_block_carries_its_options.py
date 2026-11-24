"""A <decision> block carries the options the agent wrote (P1-CHAT T12 r2): ONE reading, saved == v1 live == v2 live.

The splitter reads the body with ``parsers/decision_parser.py`` (``<option label="…">…</option>``) into ``questions[0]``
({id, prompt, options[{id, label, text}]}); the chat draws that as its choice card. A body with no option tags carries
no questions (the chat then draws the words). Golden cases below; every chunking of the live streams lands the same block.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.processing.blocks.blocks_v1 import blocks_v1_dicts
from matrx_ai.processing.blocks.live_blocks import LiveBlocksStream
from matrx_ai.processing.blocks.live_blocks_v2 import LiveBlocksStreamV2

FRUIT = (
    'Pick one:\n\n<decision prompt="Which fruit?">\n<option label="Apple">A crisp, sweet apple.</option>\n'
    '<option label="Pear">A soft, juicy pear.</option>\n</decision>\n\nThanks.\n'
)
FRUIT_Q = [{"id": "decision-0", "prompt": "Which fruit?", "options": [
    {"id": "opt-0", "label": "Apple", "text": "A crisp, sweet apple."},
    {"id": "opt-1", "label": "Pear", "text": "A soft, juicy pear."},
]}]
GOLDEN: dict[str, tuple[str, list[dict[str, Any]]]] = {
    "two options with text": (FRUIT, FRUIT_Q),
    "own ids, single quotes, no label (first line is the label)": (
        "<decision prompt='Next step?'>\n  <option id='go' label='Ship it'>Release today.</option>\n"
        "  <option>Wait a week\nfor the review.</option>\n</decision>\n",
        [{"id": "decision-0", "prompt": "Next step?", "options": [
            {"id": "go", "label": "Ship it", "text": "Release today."},
            {"id": "opt-1", "label": "Wait a week", "text": "Wait a week\nfor the review."},
        ]}],
    ),
    "no option tags: no questions": ('<decision prompt="Which?">\n- [a] A\n- [b] B\n</decision>\n', []),
}


def _decisions(blocks: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    return [b.get("questions") for b in blocks if b.get("type") == "decision"]


def _live(stream: LiveBlocksStream, text: str, size: int) -> list[list[dict[str, Any]]]:
    out = []
    for i in range(0, len(text), size):
        out += stream.feed(text[i : i + size])
    out += stream.finish()
    closes = [e.model_dump() for e in out]
    return [c["block"].get("questions") for c in closes if c.get("type") == "block.close" and c["block"].get("type") == "decision"]


@pytest.mark.parametrize("name", list(GOLDEN))
def test_the_saved_decision_carries_its_options(name: str) -> None:
    text, questions = GOLDEN[name]
    assert _decisions(blocks_v1_dicts(text)) == [questions]


@pytest.mark.parametrize("name", list(GOLDEN))
@pytest.mark.parametrize("size", [1, 7, 4096])
@pytest.mark.parametrize("make", [LiveBlocksStream, LiveBlocksStreamV2], ids=["v1", "v2"])
def test_the_live_decision_carries_the_same_options(name: str, size: int, make: type) -> None:
    text, questions = GOLDEN[name]
    assert _live(make("m1"), text, size) == [questions]
