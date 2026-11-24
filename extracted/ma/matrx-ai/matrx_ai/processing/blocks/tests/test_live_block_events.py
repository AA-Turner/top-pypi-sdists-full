"""Live block events (P1-CHAT T1, T1b): the real splitter's events, at every chunking, rebuild the saved blocks.

Offline, no model: a client that draws ONLY the live events ends each text part with exactly the blocks
the save computes from the saved text (regions aside — they arrive with ``message_blocks``). Inline
reasoning never sits inside a text part. A client that does not read ``blocks-v1`` gets nothing new.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.processing.blocks.blocks_v1 import blocks_v1_dicts
from matrx_ai.processing.blocks.live_blocks import LiveBlocksStream, live_message_id, streaming_live_blocks
from matrx_ai.processing.blocks.reasoning_parts import inline_reasoning_parts

CORPUS: dict[str, str] = {
    "markdown_code_table": "# Title\n\nSome **text**.\n\n```python\nprint(1)\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |\n",
    "mermaid_html_svg_math": (
        "Diagram:\n\n```mermaid\ngraph TD\nA-->B\n```\n\n```html\n<b>hi</b>\n```\n\n"
        "```svg\n<svg xmlns=\"http://www.w3.org/2000/svg\"><circle r=\"4\"/></svg>\n```\n\n$$x^2$$\n\n![cat](https://example.com/c.png)\n"
    ),
    "kind_fenced": (
        'Cards:\n\n```json\n{"__kind":"flashcard_set",\n"title":"Capitals",\n"cards":[{"front":"France","back":"Paris"},\n'
        '{"front":"Japan","back":"Tokyo"}]}\n```\n\nDone.\n'
    ),
    "kind_bare": '{"__kind":"flashcard_set","title":"x","cards":[]}\n',
    "artifact": '<artifact id="a1" type="html" title="Page">\n<p>hi</p>\n</artifact>\n\nafter\n',
    "decision": '<decision prompt="Pick one">\n- [a] Apples\n- [b] Pears\n</decision>\n\nok\n',
    "protocol": "<heartbeat>\nNOTIFY\n</heartbeat>\n",
    "reasoning_inline": "<reasoning>\nthinking hard\n</reasoning>\n\nThe answer is 4.\n\n```js\nx\n```\n",
    "reasoning_mid": "First words.\n\n<reasoning>\nmore thought\n</reasoning>\n\nSecond words.\n",
    "cut_in_fence": "Hello\n\n```python\nprint(",
    "cut_in_kind": 'Here:\n\n```json\n{"__kind":"flashcard_set","title":"x",\n"cards":[{"front":"a"',
}


def _clean(block: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in block.items() if k not in ("regions", "canvas") and v is not None}


def _saved_parts(text: str) -> list[list[dict[str, Any]]]:
    texts = [p.text for p in inline_reasoning_parts(text) if p.type == "text"] if "<reasoning>" in text else [text]
    return [[_clean(b) for b in blocks_v1_dicts(t)] for t in texts]


def _events(text: str, size: int) -> list[dict[str, Any]]:
    stream = LiveBlocksStream("m1")
    out = []
    for i in range(0, len(text), size):
        out += stream.feed(text[i : i + size])
    out += stream.finish()
    return [e.model_dump() for e in out]


def _client_state(events: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """What a client that draws only the live events holds at the end: per part, its closed blocks."""
    parts: dict[int, dict[int, dict[str, Any]]] = {}
    opened: set[tuple[int, int]] = set()
    for e in events:
        assert e["message_id"] == "m1"
        if e["type"] == "part.open":
            assert e["part"] not in parts, "a part opens once"
            parts[e["part"]] = {}
        elif e["type"] == "block.open":
            assert e["part"] in parts, "block.open before its part.open"
            opened.add((e["part"], e["index"]))
        elif e["type"] == "block.partial":
            assert (e["part"], e["index"]) in opened
        elif e["type"] == "block.close":
            assert (e["part"], e["index"]) in opened, "block.close before its block.open"
            parts[e["part"]][e["index"]] = _clean(e["block"])
    return [[blocks[i] for i in sorted(blocks)] for _, blocks in sorted(parts.items())]


@pytest.mark.parametrize("name", sorted(CORPUS))
@pytest.mark.parametrize("size", [1, 2, 5, 13, 10_000])
def test_live_events_rebuild_the_saved_blocks_at_every_chunking(name: str, size: int) -> None:
    text = CORPUS[name]
    assert _client_state(_events(text, size)) == _saved_parts(text)


def test_reasoning_never_enters_a_text_part() -> None:
    events = _events(CORPUS["reasoning_mid"], 3)
    assert [e["part"] for e in events if e["type"] == "part.open"] == [0, 1]
    assert all(e.get("block_type") != "reasoning" for e in events)


def test_an_open_kind_streams_growing_partials_then_closes() -> None:
    events = _events(CORPUS["kind_fenced"], 4)
    partials = [e for e in events if e["type"] == "block.partial"]
    assert len(partials) >= 3
    assert [p["seq"] for p in partials] == list(range(1, len(partials) + 1))
    assert all(p["kind"] == "flashcard_set" and p["value"]["__kind"] == "flashcard_set" for p in partials)
    cards = [len(p["value"].get("cards", [])) for p in partials]
    assert cards == sorted(cards) and cards[-1] == 2, "a partial may be incomplete, never shrink"
    close = next(e for e in events if e["type"] == "block.close" and e["block"]["type"] == "kind")
    assert events.index(close) > events.index(partials[-1])


def test_a_reply_cut_in_a_fence_closes_its_markdown_incomplete() -> None:
    closes = [e for e in _events(CORPUS["cut_in_fence"], 2) if e["type"] == "block.close"]
    assert closes[-1]["block"]["type"] == "markdown" and closes[-1]["complete"] is False
    kind = [e for e in _events(CORPUS["cut_in_kind"], 2) if e["type"] == "block.close" and e["block"]["type"] == "kind"]
    assert kind and kind[0]["complete"] is False and kind[0]["block"]["status"] == "incomplete"


def test_a_tool_or_thinking_boundary_opens_a_new_part() -> None:
    stream = LiveBlocksStream("m1")
    events = [*stream.feed("Before the tool.\n"), *stream.boundary(), *stream.feed("After.\n"), *stream.finish()]
    assert [e.part for e in events if e.type == "part.open"] == [0, 1]


def test_the_later_answer_is_addressed_by_the_id_its_row_will_take() -> None:
    config = SimpleNamespace(messages=SimpleNamespace(to_list=lambda: [1, 2, 3]))
    state = SimpleNamespace(reserved_message_ids={3: "first"}, streamed_message_ids={})
    assert live_message_id(state, config) == "first"
    later = SimpleNamespace(messages=SimpleNamespace(to_list=lambda: [1, 2, 3, 4, 5]))
    minted = live_message_id(state, later)
    assert minted and minted != "first"
    assert live_message_id(state, later) == minted, "one id per position"
    assert state.streamed_message_ids == {5: minted}


class _Recorder:
    def __init__(self) -> None:
        self.wire: list[tuple[str, Any]] = []

    async def send_chunk(self, text: str) -> None:
        self.wire.append(("chunk", text))

    async def send_data(self, payload: Any) -> None:
        self.wire.append(("data", payload.model_dump()))

    async def send_reasoning_chunk(self, text: str) -> None:
        self.wire.append(("reasoning", text))


async def _run_call(reads: list[str], chunks: list[str]) -> _Recorder:
    from matrx_connect.context.app_context import AppContext, clear_app_context, get_app_context, set_app_context

    rec = _Recorder()
    token = set_app_context(AppContext(user_id="u", emitter=rec, metadata={"client_reads": reads}))
    try:
        state = SimpleNamespace(reserved_message_ids={1: "row-1"}, streamed_message_ids={})
        config = SimpleNamespace(messages=SimpleNamespace(to_list=lambda: [0]))
        async with streaming_live_blocks(state, config) as live:
            emitter = get_app_context().emitter
            for c in chunks:
                await emitter.send_chunk(c)
            await live.finish()
        assert get_app_context().emitter is rec, "the watcher is removed after the call"
    finally:
        clear_app_context(token)
    return rec


def test_a_client_that_does_not_read_blocks_v1_gets_nothing_new() -> None:
    rec = asyncio.run(_run_call([], ["# Hi\n", "there\n"]))
    assert [kind for kind, _ in rec.wire] == ["chunk", "chunk"]


def test_a_blocks_v1_client_gets_the_chunks_unchanged_and_the_events_after_them() -> None:
    rec = asyncio.run(_run_call(["blocks-v1"], ["# Hi\n", "there\n"]))
    assert [v for k, v in rec.wire if k == "chunk"] == ["# Hi\n", "there\n"]
    types = [v["type"] for k, v in rec.wire if k == "data"]
    assert types == ["part.open", "block.open", "block.close"]
    assert all(v["message_id"] == "row-1" for k, v in rec.wire if k == "data")
    assert rec.wire[0][0] == "chunk", "text first: events never delay a token"
