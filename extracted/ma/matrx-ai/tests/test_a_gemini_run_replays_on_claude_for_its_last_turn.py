"""Debrief / last-turn switch: a Gemini-run conversation, forked, with ONLY the
last turn on Claude Opus 5.5 — the replayed history must be a wire payload the
Anthropic Messages API accepts.

The history is a real production Gemini tool turn (the wire-replay fixture:
signed functionCall parts, tool results) plus a Gemini thought and a final
answer, then the debrief question. What Anthropic rejects with a 400, and what
this asserts never reaches the wire:

* a Gemini thought signature (bytes or ``__b64``) anywhere in the payload;
* a ``thinking`` block without an Anthropic signature (foreign thinking must
  become plain text);
* a ``tool_use`` whose id is outside ``^[a-zA-Z0-9_-]+$`` or that has no
  ``tool_result`` in the very next user message;
* two consecutive messages with the same role, or a first message that is not
  ``user``, or a last message that is not the debrief question.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile

FIXTURE = Path(__file__).parent / "fixtures" / "wire_replay" / "gemini_tool_turn_snapshot.json"
DEBRIEF = "Speaking as yourself: what went wrong in this run, and what would you change?"
_TOOL_ID = re.compile(r"^[a-zA-Z0-9_-]+$")


def _forked_gemini_run_with_last_turn_on_claude():
    unified = json.loads(FIXTURE.read_text())["unified_payload"]
    request = AIMatrixRequest.from_dict(dict(unified))
    config = request.config
    # The fixture stops mid-loop (a signed call with no result yet). A debrief
    # forks a FINISHED run: close the open call the way the run did, then the
    # Gemini thought + answer, then the one debrief question.
    last = config.messages[-1]
    open_calls = [c for c in last.content if getattr(c, "type", None) == "tool_call"]
    if last.role == "assistant" and open_calls:
        config.messages.pop()
    config.messages.append(
        UnifiedMessage(
            role="assistant",
            content=[
                ThinkingContent(text="Three violations; summarize.", provider="google", signature=b"SIGNATURE-BYTES"),
                TextContent(text="Audit complete: 3 violations."),
            ],
        )
    )
    config.begin_model_this_turn_only()
    config.apply_overrides(LLMParams(model="claude-opus-5-5"))
    config.append_or_extend_user_input(DEBRIEF)
    return config


def _profile():
    return make_profile(
        model_name="claude-opus-5-5",
        wire_format="anthropic_chat",
        capabilities={
            "input": ["text"],
            "output": ["text"],
            "features": ["function_calling", "structured_output", "reasoning"],
            "interaction": "turn",
        },
    )


def _wire() -> dict[str, Any]:
    return AnthropicTranslator().to_anthropic(_forked_gemini_run_with_last_turn_on_claude(), _profile())


def test_the_fork_runs_on_claude_and_keeps_gemini_as_the_conversation_model() -> None:
    config = _forked_gemini_run_with_last_turn_on_claude()
    assert config.model == "claude-opus-5-5"
    assert config.to_storage_dict()["model"] != "claude-opus-5-5"


def test_no_gemini_signature_material_reaches_the_anthropic_wire() -> None:
    blob = json.dumps(_wire()["messages"], default=repr)
    assert "thought_signature" not in blob
    assert "thoughtSignature" not in blob
    assert "SIGNATURE-BYTES" not in blob
    assert "__b64" not in blob


def test_foreign_thinking_is_never_sent_as_an_unsigned_thinking_block() -> None:
    for message in _wire()["messages"]:
        for block in message["content"]:
            if isinstance(block, dict) and block.get("type") in {"thinking", "redacted_thinking"}:
                raise AssertionError(f"foreign thinking sent as {block['type']}: {block}")


def test_every_tool_use_is_answered_in_the_next_user_turn_with_a_legal_id() -> None:
    messages = _wire()["messages"]
    tool_uses = 0
    for index, message in enumerate(messages):
        for block in message["content"]:
            if not (isinstance(block, dict) and block.get("type") == "tool_use"):
                continue
            tool_uses += 1
            assert _TOOL_ID.match(block["id"]), block["id"]
            nxt = messages[index + 1]
            assert nxt["role"] == "user"
            answered = {b.get("tool_use_id") for b in nxt["content"] if isinstance(b, dict)}
            assert block["id"] in answered, f"tool_use {block['id']} has no tool_result next"
    assert tool_uses >= 2, "the Gemini tool calls did not survive the replay at all"


def test_roles_alternate_and_the_debrief_question_is_last() -> None:
    messages = _wire()["messages"]
    assert messages[0]["role"] == "user"
    for prev, cur in zip(messages, messages[1:]):
        assert prev["role"] != cur["role"], (prev["role"], cur["role"])
    assert messages[-1]["role"] == "user"
    texts = [b.get("text") for b in messages[-1]["content"] if isinstance(b, dict)]
    assert DEBRIEF in texts
