"""A Gemini part flagged ``thought: true`` never lands in the visible reply.

Real-test PB-03 round 3 (conversation 6a692e15, copy G, gemini flash-lite at
MINIMAL thinking) returned ~1,800 characters of reasoning in the visible reply.
The stored raw response showed the model sent that text as a part with
``thought: null`` and ``thoughts_token_count: null`` (the reasoning rode in the
answer text, with the answer glued on): model behaviour, not a translator gap.
These tests pin the half our pipeline owns: a FLAGGED thought part is
ThinkingContent on the persisted path and a ``<reasoning>`` fence on the stream
path, never plain text.
"""

from __future__ import annotations

import pytest
from google.genai import types

from matrx_ai.providers.google.google_api import GoogleChat
from matrx_ai.providers.google.translator import GoogleTranslator

THOUGHT = "**Defining Route Parameters** Okay, I'm defining the route parameters."
ANSWER = "Los Angeles | Fog | G-7A41\n\nHeld by settings desk"


def _chunk(*parts: types.Part) -> types.GenerateContentResponse:
    return types.GenerateContentResponse(
        candidates=[
            types.Candidate(
                content=types.Content(role="model", parts=list(parts)),
                finish_reason=types.FinishReason.STOP,
            )
        ]
    )


@pytest.mark.asyncio
async def test_flagged_thought_part_is_thinking_not_text():
    chunks = [_chunk(types.Part(text=THOUGHT, thought=True), types.Part(text=ANSWER))]
    resp = await GoogleTranslator().from_google_async(chunks, "gemini-flash-lite-latest")
    items = [c for m in resp.messages for c in m.content]
    visible = "".join(c.text for c in items if getattr(c, "type", "") == "text")
    thinking = [c for c in items if getattr(c, "type", "") == "thinking"]
    assert THOUGHT not in visible
    assert ANSWER in visible
    assert thinking and THOUGHT in thinking[0].text


class _Emitter:
    def __init__(self) -> None:
        self.chunks: list[str] = []

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_reasoning_state(self, state: str) -> None: ...


@pytest.mark.asyncio
async def test_flagged_thought_part_streams_inside_the_reasoning_fence():
    em = _Emitter()
    chat = GoogleChat.__new__(GoogleChat)
    await chat._handle_part(types.Part(text=THOUGHT, thought=True), em)
    await chat._handle_part(types.Part(text=ANSWER), em)
    joined = "".join(em.chunks)
    before_close, _, after_close = joined.partition("</reasoning>")
    assert THOUGHT in before_close and before_close.lstrip().startswith("<reasoning>")
    assert THOUGHT not in after_close and ANSWER in after_close
