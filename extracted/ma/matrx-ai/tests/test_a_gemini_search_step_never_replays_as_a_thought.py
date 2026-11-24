"""Gemini's built-in tool steps never come back to Gemini as signed empty thoughts.

Live defect 2026-11-19 (chat-agent-skills; conversations f9c592c8, d11bc8f1, 735c85b2): The Real News
(gemini-3.8-flash, Google Search + URL context beside function tools, so the request carries
``include_server_side_tool_invocations``) searched on turn 1. Gemini returned the search as ``tool_call``
/ ``tool_response`` parts, each with a thought signature. The parser's catch-all stored each as a
thinking part with no text; the next turn replayed them as ``{"text": "", "thought": true,
"thoughtSignature": ...}`` and Gemini refused the WHOLE request: 400 "Invalid thought signature."
(INVALID_THOUGHT_SIGNATURE). Every second message after a search failed, chat mode or not. Probe
(direct to Gemini): the turn replayed verbatim = 200; the search parts as empty thoughts = 400; the
search parts left out = 200.

Two layers, each alone enough:
1. parse: ``is_server_tool_invocation`` parts are not stored as thinking;
2. replay: a Google thinking part with a signature and no text is never sent (heals stored rows).
"""

from __future__ import annotations

import pytest
from google.genai import types

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import ThinkingContent, reconstruct_content
from matrx_ai.providers.google.translator import GoogleTranslator, is_server_tool_invocation

SIG = b"sig-bytes-0123"
THOUGHT = "**Checking the latest news** I'm searching for today's coverage."
ANSWER = "The Fed held rates steady."


def _chunk(*parts: types.Part) -> types.GenerateContentResponse:
    return types.GenerateContentResponse(
        candidates=[types.Candidate(content=types.Content(role="model", parts=list(parts)),
                                    finish_reason=types.FinishReason.STOP)]
    )


def _search_turn() -> list[types.GenerateContentResponse]:
    return [_chunk(
        types.Part(text=THOUGHT, thought=True),
        types.Part(tool_call=types.ToolCall(), thought_signature=SIG),
        types.Part(tool_response=types.ToolResponse(), thought_signature=SIG),
        types.Part(text=ANSWER, thought_signature=SIG),
    )]


def _replayed_parts(message: UnifiedMessage) -> list[dict]:
    content = message.to_google_content()
    return list((content or {}).get("parts") or [])


def test_the_detector_names_both_server_tool_parts():
    assert is_server_tool_invocation(types.Part(tool_call=types.ToolCall()))
    assert is_server_tool_invocation(types.Part(tool_response=types.ToolResponse()))
    assert not is_server_tool_invocation(types.Part(text="x", thought_signature=SIG))
    assert not is_server_tool_invocation(types.Part(thought_signature=SIG))


@pytest.mark.asyncio
async def test_a_search_step_is_not_stored_as_a_thought():
    resp = await GoogleTranslator().from_google_async(_search_turn(), "gemini-3.8-flash")
    items = [c for m in resp.messages for c in m.content]
    thinking = [c for c in items if isinstance(c, ThinkingContent)]
    assert [t.text for t in thinking] == [THOUGHT], "only the real thought is a thinking part"
    assert not any(t.signature is not None and not t.text for t in thinking)


@pytest.mark.asyncio
async def test_the_next_turn_never_sends_a_signature_without_a_thought():
    resp = await GoogleTranslator().from_google_async(_search_turn(), "gemini-3.8-flash")
    for message in resp.messages:
        for part in _replayed_parts(message):
            assert not (part.get("thoughtSignature") and not part.get("text")), part


def test_a_stored_row_from_before_the_fix_replays_without_the_bad_signature():
    """The shape the failing conversations stored: signed thinking parts with no text."""
    import base64

    sig = base64.b64encode(SIG).decode()
    stored = [
        {"type": "thinking", "text": THOUGHT, "provider": "google", "summary": []},
        {"type": "thinking", "text": "", "provider": "google", "summary": [],
         "signature": sig, "signature_encoding": "base64"},
        {"type": "thinking", "text": "Reading the coverage", "provider": "google", "summary": [],
         "signature": sig, "signature_encoding": "base64"},
        {"type": "text", "text": ANSWER},
    ]
    message = UnifiedMessage(role="assistant", content=[reconstruct_content(b) for b in stored])
    parts = _replayed_parts(message)
    assert not any(p.get("thoughtSignature") and not p.get("text") for p in parts), parts
    signed = [p for p in parts if p.get("thoughtSignature")]
    assert signed == [{"text": "Reading the coverage", "thought": True, "thoughtSignature": SIG}], (
        "a signed thought WITH text still replays verbatim"
    )
    assert any(p.get("text") == ANSWER for p in parts)
