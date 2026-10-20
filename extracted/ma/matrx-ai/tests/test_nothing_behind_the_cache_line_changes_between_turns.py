"""FORCING GUARD — nothing behind the cache line changes between turns.

The law (Arman, 2026-10-16): "NOTHING, other than the removal of LARGE tool
outputs should ever modify text behind the cache line." The time must never
update inside cached content, and the organization catalog in the system
prompt can never flip mid-conversation.

Live evidence this guard is built from (``chat.request_snapshot``):

* Every Anthropic request sent the per-turn ``<turn_context>`` block (live
  date, active selection, value list) as a SECOND SYSTEM BLOCK. Anthropic
  caches tools -> system -> messages, so a system block that changes every
  turn sits in front of the whole history: conversation 3787dd66 read 53,807
  tokens (tools + block 1) on every turn and re-WROTE 49k-150k of history.
* Conversation 88a134af sent a system prompt of 8,764 chars (with the
  ``<org_catalog>``), then 3,676 (without), then 8,764 again, on three
  successive person turns. Cause: ``_strip_ephemeral_for_storage`` cleared the
  turn-one catalog off the frozen in-memory SystemInstruction, and that object
  is what ``AgentCache`` hands the next turn on the same server task.
* The prompt-cache guard compared rounds of ONE request only, so neither
  defect ever made it scream.

Each test below failed on origin/main before the fix (red) and passes after
it (green).
"""

from __future__ import annotations

import copy
from typing import Any

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.instructions.core import SystemInstruction
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.testing.profile_factory import make_profile

SYSTEM = "You are a careful assistant. " * 40
CATALOG = '<org_catalog condensed="true">Acme, Beta, Gamma</org_catalog>'


def _msg(role: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(role=role, content=[TextContent(text=text)])


def _turn(history: list[UnifiedMessage], live_date: str, model: str) -> UnifiedConfig:
    config = UnifiedConfig(model=model, messages=MessageList(_messages=list(history)))
    config.system_instruction = SYSTEM
    config.messages.attach_turn_context(
        f"<live_date>It is now {live_date}.</live_date>", slot="live_date"
    )
    return config


def _anthropic(config: UnifiedConfig) -> dict[str, Any]:
    profile = make_profile(model_name=config.model, wire_format="anthropic")
    return AnthropicTranslator().build_request(config, profile)


def _strip_cache_control(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _strip_cache_control(v) for k, v in value.items() if k != "cache_control"}
    if isinstance(value, list):
        return [_strip_cache_control(v) for v in value]
    return value


def _cached_prefix(request: dict[str, Any]) -> list[Any]:
    """Every message block up to and including the LAST cache breakpoint."""
    flat: list[Any] = []
    last_breakpoint = -1
    for message in request["messages"]:
        content = message["content"]
        blocks = content if isinstance(content, list) else [{"type": "text", "text": content}]
        for block in blocks:
            flat.append((message["role"], _strip_cache_control(block)))
            if isinstance(block, dict) and "cache_control" in block:
                last_breakpoint = len(flat) - 1
    return flat[: last_breakpoint + 1]


def _all_blocks(request: dict[str, Any]) -> list[Any]:
    flat: list[Any] = []
    for message in request["messages"]:
        content = message["content"]
        blocks = content if isinstance(content, list) else [{"type": "text", "text": content}]
        flat.extend((message["role"], _strip_cache_control(b)) for b in blocks)
    return flat


# ── 1. The per-turn block (the clock) rides AFTER the last cache line ──────


def test_anthropic_system_channel_is_byte_identical_between_turns() -> None:
    model = "claude-sonnet-4-5"
    turn_one = _anthropic(_turn([_msg("user", "first question")], "09:00", model))
    history = [_msg("user", "first question"), _msg("assistant", "first answer")]
    turn_two = _anthropic(_turn([*history, _msg("user", "second question")], "09:05", model))

    assert turn_one["system"] == turn_two["system"]
    for block in turn_two["system"]:
        assert "<turn_context" not in block["text"]
        assert "live_date" not in block["text"]


def test_anthropic_turn_two_cached_prefix_is_a_prefix_of_turn_three() -> None:
    """What a turn wrote to the cache is exactly what the next turn sends first.

    THE REQUEST ENDS WITH WHAT THE PERSON TYPED (Arman, 2026-10-19): the per-turn block rides
    BEFORE her words, so the rolling breakpoint sits on the block before it (the previous
    answer) — the cached prefix never contains a per-turn byte."""
    model = "claude-sonnet-4-5"
    history = [_msg("user", "first question"), _msg("assistant", "first answer")]
    turn_two = _anthropic(_turn([*history, _msg("user", "second question")], "09:00", model))
    history3 = [*history, _msg("user", "second question"), _msg("assistant", "second answer")]
    turn_three = _anthropic(_turn([*history3, _msg("user", "third question")], "09:05", model))

    cached = _cached_prefix(turn_two)
    assert cached, "turn two carries no message breakpoint at all"
    assert "<turn_context" not in str(cached)
    assert _all_blocks(turn_three)[: len(cached)] == cached


def test_anthropic_turn_context_is_before_her_words_and_never_inside_them() -> None:
    model = "claude-sonnet-4-5"
    history = [_msg("user", "q1"), _msg("assistant", "a1")]
    request = _anthropic(_turn([*history, _msg("user", "HER WORDS")], "09:00", model))
    last = request["messages"][-1]
    assert last["role"] == "user"
    texts = [b["text"] for b in last["content"]]
    # Her words: their own block, exactly what she typed, LAST.
    assert texts[-1] == "HER WORDS"
    # The platform block is its own block before hers, uncached; the breakpoint is on a1.
    assert len(texts) == 2 and texts[0].startswith("<turn_context") and "live_date" in texts[0]
    assert all("cache_control" not in b for b in last["content"])
    assert "cache_control" in request["messages"][-2]["content"][-1]


def test_openai_turn_context_is_a_user_item_before_her_words() -> None:
    model = "gpt-5"
    config = _turn([_msg("user", "HER WORDS")], "09:00", model)
    profile = make_profile(model_name=model, wire_format="openai")
    request = OpenAITranslator().build_request(config, profile)
    items = request["input"]
    assert items[0]["role"] == "developer"
    assert "<turn_context" not in items[0]["content"][0]["text"]
    assert items[-1]["content"][-1]["text"] == "HER WORDS"
    assert items[-2]["content"][0]["text"].startswith("<turn_context")


CHAT_COMPLETIONS = [
    ("matrx_ai.providers.groq.translator", "GroqTranslator", "groq_chat"),
    ("matrx_ai.providers.cerebras.translator", "CerebrasTranslator", "cerebras_chat"),
    ("matrx_ai.providers.together.translator", "TogetherTranslator", "together_chat"),
    ("matrx_ai.providers.generic_openai.translator", "GenericOpenAITranslator", "openai_chat"),
]


@pytest.mark.parametrize(("module", "cls", "wire_format"), CHAT_COMPLETIONS)
def test_chat_completions_turn_one_is_an_exact_prefix_of_turn_two(module: str, cls: str, wire_format: str) -> None:
    """Groq, Cerebras, Together and Moonshot cache the EXACT prefix of the request,
    system message included (owner ruling L29, 2026-10-18). Everything turn one sent
    before its own per-turn host turn is sent unchanged, first, by turn two — so the
    system message never carries the clock."""
    import importlib

    translator = getattr(importlib.import_module(module), cls)()
    profile = make_profile(model_name="m", wire_format=wire_format)
    turn_one = translator.build_request(_turn([_msg("user", "first question")], "09:00", "m"), profile)
    history = [_msg("user", "first question"), _msg("assistant", "first answer")]
    turn_two = translator.build_request(_turn([*history, _msg("user", "second question")], "09:05", "m"), profile)

    one, two = turn_one["messages"], turn_two["messages"]
    assert one[0]["role"] == "system" and "<turn_context" not in str(one[0])
    # THE REQUEST ENDS WITH WHAT THE PERSON TYPED (2026-10-19): the block is its own turn
    # just BEFORE her words; everything before it is resent unchanged, first, next turn.
    assert one[-2]["role"] == "user" and "It is now 09:00." in str(one[-2]), "the block precedes her words"
    assert one[-1] == {"role": "user", "content": "first question"} or one[-1]["content"] == [
        {"type": "text", "text": "first question"}
    ], one[-1]
    assert two[: len(one) - 2] == one[:-2], f"{cls}: turn two does not resend turn one's prefix unchanged"
    assert "It is now 09:05." in str(two[-2]) and "second question" in str(two[-1])


# ── 2. The org catalog never flips off a frozen prompt ─────────────────────


def test_end_of_turn_strip_keeps_the_frozen_catalog() -> None:
    from matrx_ai.orchestrator.executor import _strip_ephemeral_for_storage

    config = UnifiedConfig(
        model="claude-sonnet-4-5", messages=MessageList(_messages=[_msg("user", "hi")])
    )
    si = SystemInstruction(base_instruction=SYSTEM, include_date=False)
    si.inject_context_block(CATALOG)
    config.system_instruction = si
    before = config.resolved_system_instruction
    # The per-turn barrier froze the prompt mid-turn (persistence.py).
    config.system_prompt_frozen = True

    _strip_ephemeral_for_storage(config)

    # This very object is what AgentCache hands the next turn.
    assert copy.deepcopy(config).resolved_system_instruction == before
    assert CATALOG in (config.resolved_system_instruction or "")


# ── 3. The checker screams across turns, on every send ─────────────────────


def test_cache_guard_screams_when_a_frozen_prompt_changes_between_turns(monkeypatch) -> None:
    from matrx_ai.providers import cache_guard

    screams: list[dict[str, Any]] = []
    monkeypatch.setattr(
        cache_guard,
        "scream_cache_line_violation",
        lambda **kw: screams.append(kw),
        raising=False,
    )
    usage = {"input_tokens": 4, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 9000}
    common = dict(
        provider="anthropic",
        model="claude-sonnet-4-5",
        conversation_id="conv-cache-line",
        tool_names=(),
        raw_usage=usage,
    )
    cache_guard.observe_cache_usage(
        request_id="turn-1", system_text=SYSTEM + CATALOG, prefix_frozen=True, **common
    )
    cache_guard.observe_cache_usage(
        request_id="turn-2", system_text=SYSTEM, prefix_frozen=True, **common
    )
    assert len(screams) == 1
    assert screams[0]["kind"] == "system_prompt_changed_between_turns"

    # The same text on the next turn is silent.
    cache_guard.observe_cache_usage(
        request_id="turn-3", system_text=SYSTEM, prefix_frozen=True, **common
    )
    assert len(screams) == 1


@pytest.mark.asyncio
async def test_send_boundary_restores_the_frozen_prompt_and_screams(monkeypatch) -> None:
    from types import SimpleNamespace

    from matrx_ai.config import send_boundary
    from matrx_ai.providers import cache_guard

    screams: list[dict[str, Any]] = []
    monkeypatch.setattr(
        cache_guard, "scream_cache_line_violation", lambda **kw: screams.append(kw), raising=False
    )
    stored = SYSTEM + "\n\n" + CATALOG
    row = SimpleNamespace(
        system_instruction=stored, created_at=None, last_request_status="completed"
    )
    config = UnifiedConfig(
        model="claude-sonnet-4-5", messages=MessageList(_messages=[_msg("user", "hi")])
    )
    config.system_instruction = SystemInstruction(base_instruction=SYSTEM, include_date=False)
    config.system_prompt_frozen = True

    await send_boundary.prepare_for_send(
        config,
        stage=send_boundary.STAGE_RESOLVE,
        conversation_id="conv-frozen",
        conversation_row=row,
        policy=send_boundary.TrimPolicy(),
    )

    assert config.resolved_system_instruction == stored
    assert screams and screams[0]["kind"] == "frozen_prompt_differs_from_row"
