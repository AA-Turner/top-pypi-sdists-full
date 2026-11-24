"""A blocks-v2 reader sees an Anthropic thought live, as ``reasoning.open / grow / close``, from its first delta.

General Chat (claude-opus-5-5, adaptive thinking, display summarized) saved a thinking part with its summarized text
on about a third of replies, while chat.aimatrx.com's Thinking row showed only its label until the answer. The
adapter held every thinking block's text until the block's signature (to tell a progress update from reasoning) and
sent it only at the block's stop when it was under ``_PROGRESS_UPDATE_MAX_CHARS`` — every summarized thought is — so
the thought reached the client in one burst just before the answer. Saved is now streamed: a blocks-v2 reader
(``_LiveBlocksWatcher.streams_thinking_live``) gets each delta as ``reasoning.grow`` the moment it arrives, and the
grown text equals the saved ``ThinkingContent``. A v1 reader keeps the hold (www draws as before:
``test_anthropic_progress_update_is_reply_text.py``). Fixture: the recorded provider stream
``fixtures/anthropic_progress_update_before_tool.json`` (no live provider call).
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import ThinkingContent
from matrx_ai.processing.blocks.live_blocks import _LiveBlocksWatcher
from matrx_ai.processing.blocks.live_blocks_v2 import LiveBlocksStreamV2
from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "anthropic_progress_update_before_tool.json").read_text())
REASONING_BLOCK, NARRATION_BLOCK, _TOOL = FIXTURE["final"]["content"]


def _ns(value: Any) -> Any:
    if isinstance(value, dict):
        return SimpleNamespace(**{k: _ns(v) for k, v in value.items()})
    if isinstance(value, list):
        return [_ns(v) for v in value]
    return value


class _Wire:
    """The stream emitter's wire, in order: each frame stamped with the provider event that produced it."""

    def __init__(self) -> None:
        self.at = -1
        self.frames: list[tuple[int, str, Any]] = []

    async def send_chunk(self, text: str) -> None:
        self.frames.append((self.at, "chunk", text))

    async def send_data(self, payload: Any) -> None:
        self.frames.append((self.at, "data", payload.model_dump() if hasattr(payload, "model_dump") else payload))

    async def send_reasoning_state(self, state: str) -> None:
        self.frames.append((self.at, "reasoning", state))

    async def send_reasoning_chunk(self, text: str) -> None: ...

    async def send_info(self, payload: Any) -> None: ...

    async def send_tool_event(self, payload: Any) -> None: ...


async def _drive(*, v2: bool) -> _Wire:
    wire = _Wire()
    emitter: Any = _LiveBlocksWatcher(wire, LiveBlocksStreamV2("m-1"), v2=True) if v2 else wire
    api = object.__new__(AnthropicChat)
    api.debug = False
    for i, event in enumerate(FIXTURE["events"]):
        wire.at = i
        await api._handle_event(_ns(event), emitter)
    if v2:
        await emitter.finish()
    return wire


def _first_event(kind: str, index: int) -> int:
    for i, event in enumerate(FIXTURE["events"]):
        if event.get("type") == kind and event.get("index") == index:
            return i
    raise AssertionError(f"no {kind} for block {index} in the fixture")


def _signature_of(index: int) -> int:
    for i, event in enumerate(FIXTURE["events"]):
        if event.get("index") == index and (event.get("delta") or {}).get("type") == "signature_delta":
            return i
    raise AssertionError(f"no signature for block {index}")


def _reasoning(wire: _Wire, ordinal: int, kind: str) -> list[tuple[int, dict[str, Any]]]:
    return [(at, d) for at, k, d in wire.frames if k == "data" and isinstance(d, dict) and d.get("type") == kind and d.get("reasoning") == ordinal]


@pytest.mark.asyncio
async def test_the_thought_grows_live_before_its_signature_arrives() -> None:
    wire = await _drive(v2=True)
    first_delta = _first_event("content_block_delta", 0)
    signature = _signature_of(0)
    opens = _reasoning(wire, 0, "reasoning.open")
    grows = _reasoning(wire, 0, "reasoning.grow")
    assert opens and opens[0][0] == first_delta, "the Thinking row must open at the thought's first delta"
    live = [d["text"] for at, d in grows if at < signature]
    assert "".join(live).strip(), "no thought text reached the reader before the block's signature (held back)"
    # Every delta grows on its own provider event, not in one burst at the block's stop.
    assert len({at for at, _ in grows if at < signature}) >= 5


@pytest.mark.asyncio
async def test_what_streamed_as_thought_is_what_is_saved() -> None:
    wire = await _drive(v2=True)
    grown = "".join(d["text"] for _, d in _reasoning(wire, 0, "reasoning.grow"))
    closes = _reasoning(wire, 0, "reasoning.close")
    assert closes and closes[0][1]["complete"] is True
    saved = UnifiedMessage.from_anthropic_content(role="assistant", content=FIXTURE["final"]["content"]).content[0]
    assert isinstance(saved, ThinkingContent)
    assert grown.strip() == saved.text.strip()


@pytest.mark.asyncio
async def test_a_progress_update_still_reaches_the_person_as_reply_text() -> None:
    wire = await _drive(v2=True)
    grown = "".join(d["text"] for _, k, d in wire.frames if k == "data" and isinstance(d, dict) and d.get("type") == "block.grow")
    assert NARRATION_BLOCK["thinking"].strip() in grown


@pytest.mark.asyncio
async def test_a_v1_reader_keeps_the_hold() -> None:
    wire = await _drive(v2=False)
    signature = _signature_of(0)
    early = [t for at, k, t in wire.frames if k == "chunk" and at < signature]
    assert early == [], "a v1 reader (www) must draw exactly as before: the thought is held until its signature"


@pytest.mark.asyncio
async def test_a_thought_that_was_a_progress_update_closes_withdrawn() -> None:
    """The progress update streamed live as a Thinking row, then arrives as reply text: its row is withdrawn."""
    wire = await _drive(v2=True)
    closes = [d for _, d in _reasoning(wire, 1, "reasoning.close")] or [d for _, d in _reasoning(wire, 0, "reasoning.close")]
    withdrawn = [d for _, k, d in wire.frames if k == "data" and isinstance(d, dict) and d.get("type") == "reasoning.close" and d.get("withdrawn") is True]
    assert withdrawn, f"no withdrawn reasoning.close; closes={closes}"
    # A real reasoning close carries no marker (recorded frames stay byte-identical).
    plain = [d for _, k, d in wire.frames if k == "data" and isinstance(d, dict) and d.get("type") == "reasoning.close" and "withdrawn" not in d]
    assert plain, "the genuine reasoning close must not carry the field"
