"""The last-resort fit never drops thinking from the turn in progress, and the wire guard places each
dropped-thinking message on exactly one wire item.

Review of b49e55882a00 (2026-11-09):
- P1: ``_latest_turn_start`` took the newest role=user message as the turn start, so a host notice in
  a tool loop (loop guard, ceiling, answer check) let the fit drop the loop's own thinking. Anthropic,
  "Preserving thinking blocks": "within a tool-use turn, pass thinking blocks back"; a tool-use loop
  is one assistant turn that ends only when the model completes its response.
- P3: a declared drop matched EVERY assistant item with the same text, so an unrelated change to a
  second "Let me check." (a tool_use added) was whitelisted.
- A Responses wire carries reasoning as its own item: dropping it shifts every later item, which was
  filed as unexplained drift on every last-resort fit. It is a declared break.
"""

from __future__ import annotations

import asyncio
import copy
import uuid
from types import SimpleNamespace

import pytest

from matrx_ai.config import (
    MessageList,
    ToolCallContent,
    ToolResultContent,
    UnifiedConfig,
    UnifiedMessage,
    input_fit,
)
from matrx_ai.config.message_config import host_authored_user_turn
from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.providers import cache_guard
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.testing.profile_factory import make_profile


@pytest.fixture
def filed(monkeypatch):
    rows: list[dict] = []

    async def record(_exc, **kw):
        rows.append(kw)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda _name: record)
    return rows


@pytest.fixture(autouse=True)
def _never_fits(monkeypatch):
    async def _limits(_config):
        return [{"limit": "host_input_budget", "limit_tokens": 1, "estimated_tokens": 10, "enforced": True}]

    monkeypatch.setattr(input_fit, "_limits", _limits)


def _thinking(n: int) -> ThinkingContent:
    return ThinkingContent(text=f"reasoning {n} " * 20, provider="anthropic", signature=f"sig-{n}")


def _anthropic(config) -> dict:
    return AnthropicTranslator().build_request(
        config, make_profile(model_name="claude-haiku-5-5", wire_format="anthropic_chat")
    )


async def _two_rounds(first, second, declaration) -> None:
    loop = uuid.uuid4().hex
    for body, trim in ((first, None), (second, declaration)):
        cache_guard.observe_cache_usage(
            provider="anthropic", model="claude-haiku-5-5", conversation_id="c", request_id="r",
            loop_id=loop, system_text="S", tool_names=("t",),
            raw_usage={"input_tokens": 200, "cache_read_input_tokens": 9000, "output_tokens": 5},
            wire_payload=body, trimmed_blocks=trim,
        )
    await asyncio.sleep(0.05)


def _declared(stats) -> cache_guard.TrimDeclaration:
    return cache_guard.declared_history_rewrites(SimpleNamespace(trim_report=None, fit={"passes": [stats]}))


def _drift(rows):
    return [r for r in rows if r.get("kind") == "prompt_cache_prefix_drift"]


# ── the turn in progress keeps its thinking ────────────────────────────────────────────────────────


@pytest.mark.parametrize("reason", ["loop_guard_approaching", "iteration_ceiling_wrap_up", "answer_check"])
async def test_a_notice_inside_a_tool_loop_never_lets_the_loop_lose_its_thinking(reason):
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="do it")]),
        UnifiedMessage(role="assistant", content=[_thinking(0), ToolCallContent(id="c0", name="t", arguments={})]),
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="c0", name="t", content="r")]),
        host_authored_user_turn("Write your result now.", reason=reason),
    ]
    config = SimpleNamespace(model="m", messages=messages, tools=[], system_instruction=None)
    stats = await input_fit._stub_history_to_fit(config, messages)
    assert any(isinstance(b, ThinkingContent) for b in messages[1].content), (
        f"{reason}: the in-progress tool loop's thinking was dropped"
    )
    assert stats["thinking_blocks_dropped"] == 0


async def test_earlier_finished_turns_still_lose_their_thinking_before_a_woken_note():
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="q0")]),
        UnifiedMessage(role="assistant", content=[_thinking(0), TextContent(text="a0")]),
        host_authored_user_turn("<helper_report>done</helper_report>", reason="inbox_driver"),
        UnifiedMessage(role="assistant", content=[_thinking(1), ToolCallContent(id="c1", name="t", arguments={})]),
        UnifiedMessage(role="tool", content=[ToolResultContent(tool_use_id="c1", name="t", content="r")]),
    ]
    config = SimpleNamespace(model="m", messages=messages, tools=[], system_instruction=None)
    stats = await input_fit._stub_history_to_fit(config, messages)
    assert not any(isinstance(b, ThinkingContent) for b in messages[1].content), "a finished turn kept its thinking"
    assert any(isinstance(b, ThinkingContent) for b in messages[3].content), "the woken turn lost its thinking"
    assert stats["thinking_blocks_dropped"] == 1


# ── one declared drop, one wire item ───────────────────────────────────────────────────────────────


async def test_an_unrelated_change_to_a_same_text_item_is_filed(filed):
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="q0")]),
        UnifiedMessage(role="assistant", content=[_thinking(0), TextContent(text="Let me check.")]),
        UnifiedMessage(role="user", content=[TextContent(text="q1")]),
        UnifiedMessage(role="assistant", content=[TextContent(text="Let me check.")]),
        UnifiedMessage(role="user", content=[TextContent(text="latest")]),
    ]
    config = UnifiedConfig(model="claude-haiku-5-5", messages=MessageList(_messages=messages))
    config.system_instruction = "S"
    first = _anthropic(config)
    stats = await input_fit._stub_history_to_fit(config, config.messages)
    second = _anthropic(config)
    other = [i for i, m in enumerate(second["messages"]) if m["role"] == "assistant"][1]
    second["messages"][other]["content"].append({"type": "tool_use", "id": "x", "name": "t", "input": {"a": 1}})
    second["messages"].append({"role": "assistant", "content": [{"type": "text", "text": "next"}]})
    await _two_rounds(first, second, _declared(stats))
    rows = _drift(filed)
    assert rows, "the unrelated change was whitelisted by the dropped message's text"
    assert any(f"[{other}]" in c for c in rows[0]["payload"]["changed"])


async def test_two_same_text_drops_are_both_lawful_and_nothing_more(filed):
    messages = []
    for n in range(3):
        messages.append(UnifiedMessage(role="user", content=[TextContent(text=f"q{n}")]))
        messages.append(UnifiedMessage(role="assistant", content=[_thinking(n), TextContent(text="Let me check.")]))
    messages.append(UnifiedMessage(role="user", content=[TextContent(text="latest")]))
    config = UnifiedConfig(model="claude-haiku-5-5", messages=MessageList(_messages=messages))
    config.system_instruction = "S"
    first = _anthropic(config)
    stats = await input_fit._stub_history_to_fit(config, config.messages)
    second = _anthropic(config)
    second["messages"].append({"role": "assistant", "content": [{"type": "text", "text": "next"}]})
    declaration = _declared(stats)
    positions, unplaced = cache_guard.place_trim_on_wire(second, declaration)
    assert unplaced == 0 and len(positions) == stats["thinking_blocks_dropped"] == 3
    await _two_rounds(first, second, declaration)
    assert _drift(filed) == []


def test_an_older_record_without_an_occurrence_is_placed_only_when_its_text_is_unique():
    body = {"messages": [
        {"role": "user", "content": [{"type": "text", "text": "q"}]},
        {"role": "assistant", "content": [{"type": "text", "text": "same"}]},
        {"role": "user", "content": [{"type": "text", "text": "q"}]},
        {"role": "assistant", "content": [{"type": "text", "text": "same"}]},
        {"role": "assistant", "content": [{"type": "text", "text": "unique"}]},
    ]}
    fp = cache_guard.message_text_fingerprint
    ambiguous = cache_guard.TrimDeclaration(messages=frozenset({(fp(["same"]), None)}))
    assert cache_guard.place_trim_on_wire(body, ambiguous) == (frozenset(), 1)
    unique = cache_guard.TrimDeclaration(messages=frozenset({(fp(["unique"]), None)}))
    assert cache_guard.place_trim_on_wire(body, unique) == (frozenset({4}), 0)


# ── Responses: dropped reasoning items shift the wire, a declared break ───────────────────────────


def _responses(drop_reasoning: bool) -> dict:
    items: list[dict] = []
    for n in range(3):
        items.append({"role": "user", "content": [{"type": "input_text", "text": f"q{n}"}]})
        if not drop_reasoning:
            items.append({"type": "reasoning", "id": f"rs_{n}", "encrypted_content": f"enc-{n}" * 30, "summary": []})
        items.append({"role": "assistant", "content": [{"type": "output_text", "text": f"a{n}"}]})
    items.append({"role": "user", "content": [{"type": "input_text", "text": "latest"}]})
    return {"model": "gpt-5", "instructions": "S", "input": items}


async def _responses_rounds(first, second, declaration):
    loop = uuid.uuid4().hex
    for body, trim in ((first, None), (second, declaration)):
        cache_guard.observe_cache_usage(
            provider="openai", model="gpt-5", conversation_id="c", request_id="r",
            loop_id=loop, system_text="S", tool_names=("t",),
            raw_usage={"input_tokens": 200, "input_tokens_details": {"cached_tokens": 9000}, "output_tokens": 5},
            wire_payload=body, trimmed_blocks=trim,
        )
    await asyncio.sleep(0.05)


async def test_dropped_responses_reasoning_items_are_a_declared_break_not_drift(filed):
    first, second = _responses(False), _responses(True)
    second["input"].append({"role": "assistant", "content": [{"type": "output_text", "text": "next"}]})
    declaration = cache_guard.TrimDeclaration(thinking_dropped=3)
    prev = cache_guard.wire_prefix(first)
    drift = cache_guard.compare_wire_prefix(prev, cache_guard.wire_prefix(second), reasoning_dropped=True)
    assert drift.changed == ()
    assert any("declared break" in note and "3 reasoning" in note for note in drift.lawful)
    await _responses_rounds(first, second, declaration)
    assert _drift(filed) == []


async def test_unrelated_drift_beside_dropped_reasoning_is_still_filed(filed):
    first, second = _responses(False), _responses(True)
    second["input"][1]["content"][0]["text"] = "a0 EDITED"
    second["input"].append({"role": "assistant", "content": [{"type": "output_text", "text": "next"}]})
    await _responses_rounds(first, second, cache_guard.TrimDeclaration(thinking_dropped=3))
    rows = _drift(filed)
    assert rows and any("changed" in c for c in rows[0]["payload"]["changed"])


def test_the_stub_pass_names_each_drop_with_its_occurrence():
    stats = asyncio.run(_stub([UnifiedMessage(role="user", content=[TextContent(text="q")]),
                               UnifiedMessage(role="assistant", content=[_thinking(0), TextContent(text="x")]),
                               UnifiedMessage(role="user", content=[TextContent(text="latest")])]))
    assert stats["rewritten_blocks"] == [
        {"message": cache_guard.message_text_fingerprint(["x"]), "occurrence": 0}
    ]


async def _stub(messages):
    config = SimpleNamespace(model="m", messages=copy.copy(messages), tools=[], system_instruction=None)
    return await input_fit._stub_history_to_fit(config, config.messages)


async def test_a_hidden_message_never_shifts_the_occurrence():
    """The wire drops ``is_visible_to_model=False`` messages; the n-th count must too."""
    hidden = UnifiedMessage(role="assistant", content=[TextContent(text="Let me check.")])
    hidden.is_visible_to_model = False
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="q0")]),
        UnifiedMessage(role="user", content=[TextContent(text="q1")]),
        UnifiedMessage(role="assistant", content=[_thinking(1), TextContent(text="Let me check.")]),
        UnifiedMessage(role="user", content=[TextContent(text="q2")]),
        UnifiedMessage(role="assistant", content=[TextContent(text="Let me check.")]),
        UnifiedMessage(role="user", content=[TextContent(text="latest")]),
    ]
    config = UnifiedConfig(model="claude-haiku-5-5", messages=MessageList(_messages=messages))
    config.system_instruction = "S"
    config.messages._messages.insert(1, hidden)  # as stored history holds it (construction drops it)
    stats = await input_fit._stub_history_to_fit(config, config.messages)
    wire = _anthropic(config)
    positions, unplaced = cache_guard.place_trim_on_wire(wire, _declared(stats))
    assistant = [i for i, m in enumerate(wire["messages"]) if m["role"] == "assistant"]
    assert assistant[0] in positions and assistant[1] not in positions and unplaced == 0
