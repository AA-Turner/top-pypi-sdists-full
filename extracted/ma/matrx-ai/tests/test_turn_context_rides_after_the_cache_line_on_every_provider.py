"""FORCING GUARD — the per-turn block never sits in a provider's cached prefix.

The law (Arman, 2026-10-16): "NOTHING, other than the removal of LARGE tool
outputs should ever modify text behind the cache line." The per-turn
``<turn_context>`` block carries the live clock, so it changes on every turn.

Anthropic and OpenAI were fixed first (aidream e86d3336e9). Google, xAI, Groq,
Cerebras, Together and the generic OpenAI-compatible translator still
concatenated the block into the SYSTEM text — the head of the prefix each
provider's automatic prefix cache reuses (Gemini implicit caching, xAI, Groq
gpt-oss, Cerebras, Together) — so the system text differed on every turn and
nothing after it could be reused.

Each test is parametrized over the six translators. On origin/main before the
fix every case failed (the system text carried the clock and differed between
turns); after the fix they pass.

Owner ruling for defects 23 + 35 (lane L10b, 2026-10-18): host text never rides
inside the person's message.

Owner ruling L29 (2026-10-18): on EVERY provider the block rides its OWN host
turn after the newest message, and the system text is byte-identical between
turns — including the Chat-Completions providers (Groq, Cerebras, Together,
generic/Moonshot). L10b had put it at the END of their system message on the
belief that their templates reject two user turns in a row; live probes of
every active chat offering (2026-10-18) accepted user, user, and all four do
exact-prefix caching that includes the system message, so a per-turn system
message defeated their cache. A model the catalog declares
``strict_role_alternation`` (probe-proven to reject user, user) gets the
documented fallback: the end of the system message, recorded in the snapshot.
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
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.testing.profile_factory import make_profile

SYSTEM = "You are a careful assistant. " * 40

CHAT_COMPLETIONS = [
    ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
    ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
    ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
]
ALL = [
    *CHAT_COMPLETIONS,
    ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
    ("matrx_ai.providers.xai.translator", "XAITranslator", "xai_chat"),
]


def _msg(role: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(role=role, content=[TextContent(text=text)])


def _turn(history: list[UnifiedMessage], live_date: str) -> UnifiedConfig:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=list(history)))
    config.system_instruction = SYSTEM
    config.messages.attach_turn_context(
        f"<live_date>It is now {live_date}.</live_date>", slot="live_date"
    )
    return config


def _build(
    module: str, cls: str, wire_format: str, config: UnifiedConfig, capabilities: dict[str, Any] | None = None
) -> Any:
    """Render ``config`` the way a real send does: the send boundary orders the person's turn
    ONCE (``send_boundary.order_for_wire`` → ``SendPrep``), the translator renders its list."""
    profile = make_profile(model_name="m", wire_format=wire_format, capabilities=capabilities)
    prep = order_for_wire(config, profile)
    translator = getattr(importlib.import_module(module), cls)()
    return translator.build_request(prep.wire_config if prep.wire_config is not None else config, profile)


def _system_text(cls: str, request: Any) -> str:
    """Every byte the request sends in its system channel."""
    if cls == "GoogleTranslator":
        return str(getattr(request["config"], "system_instruction", "") or "")
    if cls == "XAITranslator":
        return "\n".join(
            c.text
            for m in request["messages"]
            if m.role == chat_pb2.MessageRole.ROLE_SYSTEM
            for c in m.content
        )
    return "\n".join(
        m["content"] if isinstance(m["content"], str) else str(m["content"])
        for m in request["messages"]
        if m["role"] == "system"
    )


def _last_turn_texts(cls: str, request: Any) -> tuple[str, list[str]]:
    """(role, text parts) of the request's newest message/content."""
    if cls == "GoogleTranslator":
        last = request["contents"][-1]
        return last["role"], [p.get("text") for p in last["parts"] if isinstance(p, dict)]
    if cls == "XAITranslator":
        last = request["messages"][-1]
        return chat_pb2.MessageRole.Name(last.role), [c.text for c in last.content]
    last = request["messages"][-1]
    content = last["content"]
    if isinstance(content, str):
        return last["role"], [content]
    return last["role"], [p.get("text") for p in content]


SEPARATE_TURN = ALL


def _previous_turn_texts(cls: str, request: Any) -> tuple[str, list[str]]:
    """(role, text parts) of the message just before the request's newest one."""
    if cls == "GoogleTranslator":
        prev = request["contents"][-2]
        return prev["role"], [p.get("text") for p in prev["parts"] if isinstance(p, dict)]
    prev = request["messages"][-2]
    if isinstance(prev, dict):
        content = prev["content"]
        return prev["role"], [content] if isinstance(content, str) else [p.get("text") for p in content]
    return chat_pb2.MessageRole.Name(prev.role), [c.text for c in prev.content]


@pytest.mark.parametrize(("module", "cls", "wire_format"), SEPARATE_TURN)
def test_system_text_is_byte_identical_between_turns(module: str, cls: str, wire_format: str) -> None:
    turn_one = _build(module, cls, wire_format, _turn([_msg("user", "first question")], "09:00"))
    history = [_msg("user", "first question"), _msg("assistant", "first answer")]
    turn_two = _build(
        module, cls, wire_format, _turn([*history, _msg("user", "second question")], "09:05")
    )
    one, two = _system_text(cls, turn_one), _system_text(cls, turn_two)
    assert "live_date" not in one and "live_date" not in two, (
        f"{cls} put the per-turn block (the clock) in the system channel — the "
        f"head of the prefix the provider caches"
    )
    assert one == two


@pytest.mark.parametrize(("module", "cls", "wire_format"), SEPARATE_TURN)
def test_turn_context_is_its_own_turn_before_her_words(module: str, cls: str, wire_format: str) -> None:
    """THE REQUEST ENDS WITH WHAT THE PERSON TYPED (Arman, 2026-10-19): the block is its OWN
    host turn (or, where consecutive user turns merge, its own part) immediately BEFORE her
    message — never a part of her words (defects 23 + 35), never after them."""
    request = _build(module, cls, wire_format, _turn([_msg("user", "HER WORDS")], "09:00"))
    role, texts = _last_turn_texts(cls, request)
    assert role in ("user", "ROLE_USER")
    assert texts[-1] == "HER WORDS", "her own words must stay exactly what she typed, last"
    host = texts[:-1] if len(texts) > 1 else _previous_turn_texts(cls, request)[1]
    assert len(host) == 1 and host[0].startswith("<turn_context") and "live_date" in host[0]


@pytest.mark.parametrize(("module", "cls", "wire_format"), ALL)
def test_mid_loop_the_block_is_never_resent_after_a_tool_result(
    module: str, cls: str, wire_format: str
) -> None:
    """Once per person turn (owner ruling 2026-10-18, PB-05): re-appending the block after
    each tool result made it read as part of that result, and the model told the person
    about "the platform block in that last turn". It rides on the send that ends with the
    person's own message, never on a tool-loop send — and never moves into the system
    channel instead (the cache line law)."""
    history = [
        _msg("user", "weather?"),
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="c1", name="get_weather", arguments={"city": "SF"})],
        ),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="c1", name="get_weather", content="72F")],
        ),
    ]
    request = _build(module, cls, wire_format, _turn(history, "09:00"))
    assert "live_date" not in _system_text(cls, request)
    assert "turn_context" not in str(request), f"{cls} re-sent the per-turn block after a tool result"


@pytest.mark.parametrize(("module", "cls", "wire_format"), CHAT_COMPLETIONS)
def test_chat_completions_send_the_block_as_its_own_user_turn(module: str, cls: str, wire_format: str) -> None:
    """Probed live 2026-10-18 (lane L29): every active Groq, Cerebras, Together and
    Moonshot chat offering accepts user, user. The block is the turn before hers (2026-10-19:
    the request ENDS with what the person typed)."""
    history = [_msg("user", "q1"), _msg("assistant", "a1"), _msg("user", "q2")]
    request = _build(module, cls, wire_format, _turn(history, "09:00"))
    roles = [m["role"] for m in request["messages"]]
    assert roles == ["system", "user", "assistant", "user", "user"], roles
    assert request["messages"][-1]["content"] in ("q2", [{"type": "text", "text": "q2"}])
    assert "<turn_context" in str(request["messages"][-2]["content"])


STRICT = {
    "input": ["text"],
    "output": ["text"],
    "features": ["function_calling", "strict_role_alternation"],
    "interaction": "turn",
}


@pytest.mark.parametrize(("module", "cls", "wire_format"), CHAT_COMPLETIONS)
def test_a_strict_alternation_model_gets_the_documented_fallback(
    module: str, cls: str, wire_format: str
) -> None:
    """Only a model the CATALOG declares ``strict_role_alternation`` (probe-proven to
    reject user, user) gets the fallback: the end of the system message. Her
    message stays exactly her words and no second user turn is added."""
    history = [_msg("user", "q1"), _msg("assistant", "a1"), _msg("user", "HER WORDS")]
    request = _build(module, cls, wire_format, _turn(history, "09:00"), capabilities=STRICT)
    roles = [m["role"] for m in request["messages"]]
    assert roles == ["system", "user", "assistant", "user"], roles
    assert _system_text(cls, request).rstrip().endswith("</turn_context>")
    assert _last_turn_texts(cls, request) == ("user", ["HER WORDS"])


@pytest.mark.parametrize(
    ("module", "cls", "wire_format"),
    [
        ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat"),
        ("matrx_ai.providers.openai.translator", "OpenAITranslator", "openai_responses"),
    ],
)
def test_anthropic_and_openai_never_resend_it_after_a_tool_result(
    module: str, cls: str, wire_format: str
) -> None:
    history = [
        _msg("user", "weather?"),
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="c1", name="get_weather", arguments={"city": "SF"})],
        ),
        UnifiedMessage(
            role="tool",
            content=[ToolResultContent(tool_use_id="c1", name="get_weather", content="72F")],
        ),
    ]
    mid_loop = _build(module, cls, wire_format, _turn(history, "09:00"))
    assert "turn_context" not in str(mid_loop), f"{cls} re-sent the per-turn block after a tool result"
    first = _build(module, cls, wire_format, _turn([_msg("user", "weather?")], "09:00"))
    assert "live_date" in str(first), f"{cls} lost the block on the person's own turn"


@pytest.mark.parametrize(("module", "cls", "wire_format"), ALL)
def test_a_prefill_call_keeps_the_clock_out_of_the_system_channel(
    module: str, cls: str, wire_format: str
) -> None:
    """Adversarial M1 (2026-10-18): a call ending on a pre-filled assistant message put
    the per-turn block (the clock) into the system text on Google, Groq, Cerebras,
    Together, xAI and the generic OpenAI-compatible wire, so that request's prefix
    differed from turn one's. It now rides its own user turn just before the prefill,
    the prefill stays last, and each wire keeps its role rules. Owner ruling L29
    (2026-10-18): the block is its OWN user turn, never part of the person's message."""
    history = [_msg("user", "first question"), _msg("assistant", "Sure. The answer is")]
    request = _build(module, cls, wire_format, _turn(history, "09:00"))
    system = _system_text(cls, request)
    assert "live_date" not in system and "turn_context" not in system, (
        f"{cls} put the per-turn block into the system channel on a prefill call"
    )
    assert system == _system_text(
        cls, _build(module, cls, wire_format, _turn([_msg("user", "first question")], "09:05"))
    )
    if cls == "GoogleTranslator":
        roles = [c["role"] for c in request["contents"]]
        texts = [[p.get("text") for p in c["parts"] if isinstance(p, dict)] for c in request["contents"]]
    elif cls == "XAITranslator":
        roles = [chat_pb2.MessageRole.Name(m.role) for m in request["messages"]]
        texts = [[c.text for c in m.content] for m in request["messages"]]
    else:
        roles = [m["role"] for m in request["messages"]]
        texts = [
            [m["content"]] if isinstance(m["content"], str) else [p.get("text") for p in m["content"]]
            for m in request["messages"]
        ]
    assert roles[-1] in ("assistant", "model", "ROLE_ASSISTANT"), "the prefill must stay last"
    assert roles[-2] in ("user", "ROLE_USER"), roles
    assert len(texts[-2]) == 1 and "live_date" in texts[-2][0], "the block is its own host turn"
    assert ["first question"] in texts, "her own words must stay exactly what she typed"
