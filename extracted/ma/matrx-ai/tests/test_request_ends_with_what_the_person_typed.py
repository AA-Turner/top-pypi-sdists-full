"""RELEASE GATE — every provider request ENDS with what the person typed.

Arman (2026-10-19): "there is content added AFTER the user's message!!!! That is NEVER EVER
allowed because it completely poisons the request. The request must always END with the actual
text the user typed. The things we add from the harness have to come before the user's message,
never after."

Before this gate every chat translator put the per-turn ``<turn_context source="platform">``
block AFTER the person's message (its own host turn / developer item / trailing part): live
audit 2026-10-19, 59 of 75 person-typed sends in 6 h. And a person's attachments (with their
``<attachment …/>`` labels) rode after the typed text.

Each case builds the person's turn through the real door (``append_or_extend_user_input``,
which marks typed content as data), renders it through every chat translator, and reads the
provider payload: the final user turn must end with the typed text, byte-identical, and the
platform block must be in it, before the typed text. On the tree before the fix every
turn-context case fails; after it they pass.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest
from xai_sdk.proto import chat_pb2

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.send_boundary import order_for_wire
from matrx_ai.config.typed_text_last import (
    TURN_CONTEXT_MARK,
    place_before_typed_text,
    typed_text_problem,
)
from matrx_ai.testing.profile_factory import make_profile

TYPED = "What should I post on Friday?"
MARK = "<live_date>It is now 09:00.</live_date>"

TRANSLATORS = [
    ("matrx_ai.providers.anthropic.translator", "AnthropicTranslator", "anthropic_chat"),
    ("matrx_ai.providers.openai.translator", "OpenAITranslator", "openai_responses"),
    ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
    ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
    ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
    ("matrx_ai.providers.google.translator", "GoogleTranslator", "google_chat"),
    ("matrx_ai.providers.xai.translator", "XAITranslator", "xai_chat"),
]


def _config(history: list[UnifiedMessage], *, typed: str | None, context: bool = True) -> UnifiedConfig:
    config = UnifiedConfig(model="m", messages=MessageList(_messages=list(history)))
    config.system_instruction = "You are a careful assistant."
    if typed is not None:
        config.messages.append_or_extend_user_input(typed)
    if context:
        config.messages.attach_turn_context(MARK, slot="live_date")
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


def _tail_text(cls: str, request: Any) -> str:
    """Every text byte after the newest model turn, in wire order."""
    if cls == "GoogleTranslator":
        items = [(c["role"], [p.get("text") or "" for p in c["parts"] if isinstance(p, dict)]) for c in request["contents"]]
    elif cls == "XAITranslator":
        items = [(chat_pb2.MessageRole.Name(m.role), [c.text for c in m.content]) for m in request["messages"]]
    else:
        raw = request["input"] if cls == "OpenAITranslator" else request["messages"]
        items = []
        for m in raw:
            content = m.get("content")
            parts = [content] if isinstance(content, str) else [p.get("text") or "" for p in content or [] if isinstance(p, dict)]
            items.append((str(m.get("role") or m.get("type")), parts))
    out: list[str] = []
    for role, parts in reversed(items):
        if role.lower() in ("assistant", "model", "role_assistant"):
            break
        if role.lower() in ("system", "role_system"):
            continue
        out[:0] = parts
    return "\n".join(p for p in out if p)


@pytest.mark.parametrize(("module", "cls", "wire_format"), TRANSLATORS)
def test_a_new_conversation_ends_with_the_typed_text(module: str, cls: str, wire_format: str) -> None:
    request = _build(module, cls, wire_format, _config([], typed=TYPED))
    tail = _tail_text(cls, request)
    assert tail.rstrip().endswith(TYPED), f"{cls}: the request does not end with the typed text: {tail[-200:]!r}"
    assert MARK in tail and tail.index(MARK) < tail.rindex(TYPED), f"{cls}: the platform block is not before the typed text"


@pytest.mark.parametrize(("module", "cls", "wire_format"), TRANSLATORS)
def test_a_follow_up_ends_with_the_typed_text(module: str, cls: str, wire_format: str) -> None:
    history = [
        UnifiedMessage(role="user", content=[TextContent(text="first question")], id="m1", position=0),
        UnifiedMessage(role="assistant", content=[TextContent(text="first answer")], id="m2", position=1),
    ]
    request = _build(module, cls, wire_format, _config(history, typed=TYPED))
    tail = _tail_text(cls, request)
    assert tail.rstrip().endswith(TYPED), f"{cls}: {tail[-200:]!r}"
    assert TURN_CONTEXT_MARK in tail, f"{cls}: the platform block is missing from the person's turn"


@pytest.mark.parametrize(("module", "cls", "wire_format"), TRANSLATORS)
def test_typed_text_glued_to_an_authored_template_stays_last(module: str, cls: str, wire_format: str) -> None:
    template = UnifiedMessage(role="user", content=[TextContent(text="Write the brief for this request:\n")])
    request = _build(module, cls, wire_format, _config([template], typed=TYPED))
    tail = _tail_text(cls, request)
    assert tail.rstrip().endswith(TYPED), f"{cls}: {tail[-200:]!r}"
    assert tail.index("Write the brief") < tail.index(TURN_CONTEXT_MARK) < tail.rindex(TYPED), (
        f"{cls}: order must be authored template, platform block, typed text: {tail!r}"
    )


@pytest.mark.parametrize(("module", "cls", "wire_format"), TRANSLATORS)
def test_a_system_job_keeps_its_instruction_last(module: str, cls: str, wire_format: str) -> None:
    job = UnifiedMessage(role="user", content=[TextContent(text="Summarize the record. Answer in JSON.")])
    request = _build(module, cls, wire_format, _config([job], typed=None))
    tail = _tail_text(cls, request)
    assert tail.rstrip().endswith("Answer in JSON."), f"{cls}: {tail[-200:]!r}"


def test_the_persons_attachments_ride_before_their_typed_text() -> None:
    from matrx_ai.config.media_config import ImageContent

    config = _config([], typed=None, context=False)
    config.messages.append_or_extend_user_input(
        [{"type": "text", "text": TYPED}, {"type": "image", "url": "https://example.com/a.png"}]
    )
    messages = list(config.messages)
    assert typed_text_problem(messages), "the guard must see the image after the typed text"
    placed, _ = place_before_typed_text(messages, None)
    assert typed_text_problem(placed) is None
    assert isinstance(placed[-1].content[0], ImageContent)
    assert placed[-1].content[-1].text.strip() == TYPED
    assert isinstance(messages[-1].content[-1], ImageContent), "the stored message is never reordered"


def test_the_ledger_never_carries_the_platform_block() -> None:
    config = _config([], typed=TYPED)
    _build(*TRANSLATORS[0], config)
    stored = config.messages[-1]
    assert all(TURN_CONTEXT_MARK not in (getattr(c, "text", "") or "") for c in stored.content)


def test_anthropic_caches_up_to_the_platform_block_never_through_it() -> None:
    history = [
        UnifiedMessage(role="user", content=[TextContent(text="first question")], id="m1", position=0),
        UnifiedMessage(role="assistant", content=[TextContent(text="first answer")], id="m2", position=1),
    ]
    request = _build(*TRANSLATORS[0], _config(history, typed=TYPED))
    marked = [
        (i, b.get("text"))
        for i, m in enumerate(request["messages"])
        for b in m["content"]
        if isinstance(b, dict) and "cache_control" in b
    ]
    rolling = [t for i, t in marked if i > 0 or t == "first answer"]
    assert rolling and rolling[-1] == "first answer", f"rolling mark must sit before the block: {marked}"
