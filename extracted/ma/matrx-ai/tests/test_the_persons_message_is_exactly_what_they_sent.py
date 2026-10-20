"""FORCING GUARD — on EVERY provider, the person's message on the wire is exactly what they sent.

Owner decision (defects 23 + 35, 2026-10-18): host text never travels inside the
person's message. ``place_trailing_on_chat_messages`` appended the per-turn
``<turn_context>`` block as a second part INSIDE her user message on Groq,
Cerebras, Together and generic OpenAI-compatible; Anthropic, Google and xAI did
the same with their own shapes. The model answers her turn, so anything inside
it is answerable (the walk-21 incident in
``test_the_persons_turn_is_the_persons_alone.py``).

Where the block rides now:

* EVERY provider (Arman, 2026-10-19: "The request must always END with the actual
  text the user typed"): it rides its OWN host turn immediately BEFORE the
  person's message, never after it and never glued to her words; the system
  message stays byte-identical between turns (L29: Groq, Cerebras, Together and
  Moonshot/generic accept user, user and their exact-prefix caches include the
  system message). Anthropic and Gemini merge consecutive user turns, so there
  the block is its own block/part before hers.
* A model the catalog declares ``strict_role_alternation`` (probe-proven to
  reject user, user) gets the documented fallback: the END of the system
  message. Either way the placement is recorded with the request snapshot.

Each case builds the real wire request and finds her message in it.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest
from xai_sdk.proto import chat_pb2

from matrx_ai.config import (
    MessageList,
    TextContent,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.testing.profile_factory import make_profile

HER_WORDS = "HER WORDS exactly as typed."

CHAT_COMPLETIONS = [
    ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
    ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
    ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
]
ALL = [
    ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat"),
    ("matrx_ai.providers.openai.translator", "OpenAITranslator", "openai_responses"),
    ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
    ("matrx_ai.providers.xai.translator", "XAITranslator", "xai_chat"),
    *CHAT_COMPLETIONS,
]
STRICT = {
    "input": ["text"],
    "output": ["text"],
    "features": ["function_calling", "strict_role_alternation"],
    "interaction": "turn",
}


def _msg(role: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(role=role, content=[TextContent(text=text)])


def _config(history: list[UnifiedMessage], *, tail: bool = False) -> UnifiedConfig:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=list(history)))
    config.system_instruction = "You are a careful assistant."
    config.messages.attach_turn_context("<live_date>It is now 09:00.</live_date>", slot="live_date")
    if tail:
        config.messages.attach_tail_context("<your_plan>PLAN TAIL</your_plan>", slot="live_plan")
    return config


def _build(
    module: str, cls: str, wire_format: str, config: UnifiedConfig, capabilities: dict | None = None
) -> Any:
    translator = getattr(importlib.import_module(module), cls)()
    return translator.build_request(
        config, make_profile(model_name="m", wire_format=wire_format, capabilities=capabilities)
    )


def _texts_of(part: Any) -> list[str]:
    if isinstance(part, str):
        return [part]
    if isinstance(part, dict):
        for key in ("text",):
            if isinstance(part.get(key), str):
                return [part[key]]
        return []
    return []


def _messages(cls: str, request: Any) -> list[tuple[str, list[str]]]:
    """(role, text parts) of every wire message, in order (system channel excluded)."""
    if cls == "GoogleTranslator":
        return [(c["role"], [t for p in c["parts"] for t in _texts_of(p)]) for c in request["contents"]]
    if cls == "XAITranslator":
        return [
            (chat_pb2.MessageRole.Name(m.role), [c.text for c in m.content if c.text])
            for m in request["messages"]
            if m.role != chat_pb2.MessageRole.ROLE_SYSTEM
        ]
    if cls == "OpenAITranslator":
        out = []
        for item in request["input"]:
            content = item.get("content")
            texts = [content] if isinstance(content, str) else [p.get("text") for p in content or [] if isinstance(p, dict)]
            out.append((item.get("role") or item.get("type"), [t for t in texts if t]))
        return out
    out = []
    for m in request["messages"]:
        if m["role"] == "system":
            continue
        content = m["content"]
        texts = [content] if isinstance(content, str) else [t for p in content or [] for t in _texts_of(p)]
        out.append((m["role"], texts))
    return out


def _system(cls: str, request: Any) -> str:
    if cls == "GoogleTranslator":
        return str(getattr(request["config"], "system_instruction", "") or "")
    if cls == "XAITranslator":
        return "\n".join(
            c.text for m in request["messages"] if m.role == chat_pb2.MessageRole.ROLE_SYSTEM for c in m.content
        )
    if cls == "AnthropicTranslator":
        system = request.get("system")
        if isinstance(system, list):
            return "\n".join(b.get("text", "") for b in system)
        return str(system or "")
    if cls == "OpenAITranslator":
        return str(request.get("instructions") or "")
    return "\n".join(m["content"] for m in request["messages"] if m["role"] == "system")


def _her_message(cls: str, request: Any) -> list[str]:
    """Her words: exactly one part, byte-identical, never sharing a part with host text.

    On a provider that merges consecutive user turns (Anthropic, Gemini) the host block is
    a SEPARATE part of the same wire message, before hers; it is dropped here."""
    hits = [texts for _role, texts in _messages(cls, request) if any(HER_WORDS in t for t in texts)]
    assert len(hits) == 1, f"{cls}: her message not found exactly once: {hits}"
    parts = [t for t in hits[0] if not t.startswith("<turn_context")]
    assert all("<turn_context" not in t for t in parts), f"{cls}: host text glued to her words: {hits[0]}"
    return parts


@pytest.mark.parametrize(("module", "cls", "wire_format"), ALL)
def test_her_message_is_exactly_what_she_sent(module: str, cls: str, wire_format: str) -> None:
    request = _build(module, cls, wire_format, _config([_msg("user", HER_WORDS)]))
    assert _her_message(cls, request) == [HER_WORDS], (
        f"{cls} put platform text inside the person's message"
    )
    assert "live_date" in str(request), f"{cls} lost the per-turn block"


@pytest.mark.parametrize(("module", "cls", "wire_format"), ALL)
def test_her_later_message_is_exactly_what_she_sent(module: str, cls: str, wire_format: str) -> None:
    history = [_msg("user", "q1"), _msg("assistant", "a1"), _msg("user", HER_WORDS)]
    request = _build(module, cls, wire_format, _config(history))
    assert _her_message(cls, request) == [HER_WORDS]


@pytest.mark.parametrize(("module", "cls", "wire_format"), ALL)
def test_the_block_rides_its_own_turn_before_her_words(module: str, cls: str, wire_format: str) -> None:
    """THE REQUEST ENDS WITH WHAT THE PERSON TYPED (Arman, 2026-10-19)."""
    request = _build(module, cls, wire_format, _config([_msg("user", HER_WORDS)]))
    texts = [t for _role, ts in _messages(cls, request) for t in ts]
    assert texts[-1] == HER_WORDS, f"{cls}: the request must end with her words: {texts}"
    host = [i for i, t in enumerate(texts) if t.startswith("<turn_context")]
    assert host and host[-1] < len(texts) - 1, f"{cls}: the block must precede her words: {texts}"
    assert "live_date" not in _system(cls, request)


@pytest.mark.parametrize(("module", "cls", "wire_format"), CHAT_COMPLETIONS)
def test_the_system_message_is_byte_identical_between_turns(module: str, cls: str, wire_format: str) -> None:
    """Their exact-prefix caches include the system message: it never changes per turn."""
    one = _build(module, cls, wire_format, _config([_msg("user", "q1")]))
    config = _config([_msg("user", "q1"), _msg("assistant", "a1"), _msg("user", HER_WORDS)])
    config.messages.attach_turn_context("<live_date>It is now 09:05.</live_date>", slot="live_date")
    two = _build(module, cls, wire_format, config)
    assert _system(cls, one) == _system(cls, two) == "You are a careful assistant."


@pytest.mark.parametrize(("module", "cls", "wire_format"), CHAT_COMPLETIONS)
def test_a_strict_alternation_model_carries_the_block_at_the_end_of_the_system_message(
    module: str, cls: str, wire_format: str
) -> None:
    request = _build(module, cls, wire_format, _config([_msg("user", HER_WORDS)]), STRICT)
    roles = [m["role"] for m in request["messages"]]
    assert roles == ["system", "user"], roles
    system = request["messages"][0]["content"]
    assert system.startswith("You are a careful assistant.")
    assert system.rstrip().endswith("</turn_context>"), system[-200:]
    assert _her_message(cls, request) == [HER_WORDS]


@pytest.mark.parametrize(("module", "cls", "wire_format"), ALL)
def test_mid_loop_tail_never_joins_the_persons_message(module: str, cls: str, wire_format: str) -> None:
    history = [
        _msg("user", HER_WORDS),
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="c1", name="get_weather", arguments={"city": "SF"})],
        ),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="c1", name="get_weather", content="72F")],
        ),
    ]
    request = _build(module, cls, wire_format, _config(history, tail=True))
    assert _her_message(cls, request) == [HER_WORDS]
    assert "PLAN TAIL" in str(request), f"{cls} lost the tail channel"


def test_anthropic_prefill_keeps_the_block_out_of_her_message() -> None:
    prefill = UnifiedMessage.from_dict(
        {"role": "assistant", "content": [{"type": "text", "text": "Dear "}], "flags": {"prefill": True}}
    )
    history = [_msg("user", HER_WORDS), prefill]
    request = _build(
        "matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat", _config(history)
    )
    assert _her_message("AnthropicTranslator", request) == [HER_WORDS]
    assert request["messages"][-1]["role"] == "assistant", "the prefill must stay last"
    assert "live_date" in str(request)


@pytest.mark.parametrize("strict", [False, True])
@pytest.mark.parametrize(("module", "cls", "wire_format"), ALL)
def test_the_placement_is_recorded_for_the_request_snapshot(
    module: str, cls: str, wire_format: str, strict: bool
) -> None:
    """The executor pops ``state.platform_text_placements`` with the wire payload into
    ``chat.request_snapshot.metadata.platform_text_placement``."""
    from matrx_ai.orchestrator.execution_state import ExecutionState, _execution_state, set_execution_state

    state = ExecutionState()
    token = set_execution_state(state)
    try:
        _build(module, cls, wire_format, _config([_msg("user", HER_WORDS)]), STRICT if strict else None)
    finally:
        _execution_state.reset(token)
    expected = "system_message_end" if strict and (module, cls, wire_format) in CHAT_COMPLETIONS else "before_typed_text"
    assert state.platform_text_placements and state.platform_text_placements[0]["where"] == expected, (
        state.platform_text_placements
    )
