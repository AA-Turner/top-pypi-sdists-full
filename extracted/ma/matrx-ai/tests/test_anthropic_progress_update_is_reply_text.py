"""A progress update the model writes before a tool call is REPLY TEXT: streamed, stored and read as text.

Recent Claude models return the text they write between tool calls as a ``thinking`` block whose signature is
labelled ``narration`` (a "progress update"), not as a ``text`` block. Until this guard, the adapter took the wire
type at its word: the advice an agent wrote before ``ask_person`` streamed inside ``<reasoning>``, was stored as a
``thinking`` part and rendered in the collapsed "Thought process" — the person never saw it, while the model (which
reads its full note on replay) believed it had answered (agent-understanding review 9/10 C-A). The fixture is a
recorded provider stream (``fixtures/anthropic_progress_update_before_tool.json``).

The contract proven here:
1. ``from_anthropic`` turns the narration block into a ``TextContent`` that carries the provider block in
   ``metadata.replay_as``; a reasoning block stays ``ThinkingContent``.
2. The stored row round-trips, and replay to Anthropic sends the provider's block back byte-for-byte (type, text,
   signature) — the history the model wrote is never edited.
3. The live stream sends the narration as visible text, never inside ``<reasoning>``; reasoning stays wrapped.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.progress_updates import REPLAY_AS_KEY, is_progress_update_signature
from matrx_ai.config.unified_content import TextContent, ThinkingContent, ToolCallContent, reconstruct_content
from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat

FIXTURE = json.loads(
    (Path(__file__).parent / "fixtures" / "anthropic_progress_update_before_tool.json").read_text()
)
FINAL = FIXTURE["final"]
REASONING_BLOCK, NARRATION_BLOCK, TOOL_BLOCK = FINAL["content"]


def _ns(value):
    if isinstance(value, dict):
        return SimpleNamespace(**{k: _ns(v) for k, v in value.items()})
    if isinstance(value, list):
        return [_ns(v) for v in value]
    return value


class _Emitter:
    def __init__(self) -> None:
        self.chunks: list[str] = []

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_reasoning_state(self, state: str) -> None: ...

    async def send_info(self, payload) -> None: ...

    async def send_data(self, payload) -> None: ...


def test_the_fixture_is_the_shape_the_provider_sends() -> None:
    assert [b["type"] for b in FINAL["content"]] == ["thinking", "thinking", "tool_use"]
    assert not is_progress_update_signature(REASONING_BLOCK["signature"])
    assert is_progress_update_signature(NARRATION_BLOCK["signature"])
    assert not is_progress_update_signature(None)
    assert not is_progress_update_signature("not base64 !!")


def test_a_progress_update_is_parsed_as_text_and_reasoning_stays_thinking() -> None:
    message = UnifiedMessage.from_anthropic_content(role="assistant", content=FINAL["content"])
    reasoning, narration, call = message.content
    assert isinstance(reasoning, ThinkingContent)
    assert reasoning.text == REASONING_BLOCK["thinking"]
    assert isinstance(narration, TextContent), "the advice written before the tool call must be reply text"
    assert narration.text == NARRATION_BLOCK["thinking"].strip()
    assert isinstance(call, ToolCallContent)


def test_the_stored_part_replays_the_providers_block_unchanged() -> None:
    message = UnifiedMessage.from_anthropic_content(role="assistant", content=FINAL["content"])
    stored = message.content[1].to_storage_dict()
    assert stored["type"] == "text"
    assert stored["text"] == NARRATION_BLOCK["thinking"].strip()
    rebuilt = reconstruct_content(json.loads(json.dumps(stored)))
    assert isinstance(rebuilt, TextContent)
    assert rebuilt.to_anthropic() == {
        "type": "thinking",
        "thinking": NARRATION_BLOCK["thinking"],
        "signature": NARRATION_BLOCK["signature"],
    }
    assert rebuilt.metadata[REPLAY_AS_KEY]["provider"] == "anthropic"
    # Another provider reads it as the assistant's own words.
    assert rebuilt.to_openai(role="assistant")["text"] == NARRATION_BLOCK["thinking"].strip()


@pytest.mark.asyncio
async def test_the_stream_shows_the_progress_update_as_visible_text() -> None:
    api = object.__new__(AnthropicChat)
    api.debug = False
    emitter = _Emitter()
    for event in FIXTURE["events"]:
        await api._handle_event(_ns(event), emitter)
    streamed = "".join(emitter.chunks)
    narration = NARRATION_BLOCK["thinking"].strip()
    reasoning_region = streamed.split("<reasoning>", 1)[1].split("</reasoning>", 1)[0]
    visible = streamed.replace(f"<reasoning>{reasoning_region}</reasoning>", "")
    assert REASONING_BLOCK["thinking"].strip() in reasoning_region
    assert narration not in reasoning_region, "the advice streamed inside the thought process"
    assert narration in visible
    assert streamed.count("<reasoning>") == 1

