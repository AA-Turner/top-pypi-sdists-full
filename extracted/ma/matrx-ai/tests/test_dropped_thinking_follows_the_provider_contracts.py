"""The last-resort fit may drop earlier thinking only where the provider contract allows it, and
then names the message so the cache guard accepts the rewrite.

Contracts (read 2026-11-09):
- Anthropic, "Preserving thinking blocks" (platform.claude.com/docs/en/build-with-claude/thinking):
  "Required: within a tool-use turn, pass thinking blocks back ... Allowed: outside tool use, omit
  prior turns' thinking." The fit never touches the latest turn (``_latest_turn_start``), so an
  earlier turn's thinking may go. Dropping it changes the cached prefix from that block onward
  ("Thinking and prompt caching"): a deliberate, declared break, not drift.
- OpenAI Responses (developers.openai.com/api/docs/guides/reasoning): passing reasoning back is
  guidance for the function calls of the turn in progress; earlier turns carry no requirement.
- Gemini (aistudio.google.com/docs/thinking): "You MUST always resend all thought blocks exactly as
  they were received" / "should NOT remove or modify thought blocks from the history." So a
  Gemini thought (provider google, with its signature) is never dropped.

Before: a thinking block dropped from an assistant message with no tool call or result could not be
placed and filed ``prompt_cache_prefix_drift`` on every last-resort fit; Gemini thoughts were
dropped against the contract. SUT: the real ``input_fit._stub_history_to_fit``,
``cache_guard.declared_history_rewrites`` and ``observe_cache_usage``.
"""

from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace

import pytest

from matrx_ai.config import ToolResultContent, UnifiedMessage, input_fit
from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.providers import cache_guard


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    rows: list[dict] = []

    async def record_error(exc, **kwargs):
        rows.append(kwargs)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error)
    return rows


@pytest.fixture(autouse=True)
def _never_fits(monkeypatch):
    async def _limits(_config):
        return [{"limit": "host_input_budget", "limit_tokens": 1, "estimated_tokens": 10, "enforced": True}]

    monkeypatch.setattr(input_fit, "_limits", _limits)


def _thinking(provider: str, n: int) -> ThinkingContent:
    return ThinkingContent(text=f"reasoning {n}", provider=provider, signature=f"sig-{provider}-{n}")


def _conversation(provider: str = "anthropic") -> SimpleNamespace:
    messages = []
    for n in range(3):
        messages.append(UnifiedMessage(role="user", content=[TextContent(text=f"question {n}")]))
        messages.append(UnifiedMessage(role="assistant", content=[_thinking(provider, n), TextContent(text=f"answer {n}")]))
    messages.append(UnifiedMessage(role="user", content=[TextContent(text="latest question")]))
    return SimpleNamespace(model="m", messages=messages, tools=[], system_instruction=None)


def _wire(config: SimpleNamespace) -> dict:
    """Anthropic wire: signed thinking blocks of its own provider, text otherwise."""
    out = []
    for msg in config.messages:
        blocks = []
        for b in msg.content:
            if isinstance(b, ThinkingContent):
                rendered = b.to_anthropic()
                if rendered:
                    blocks.append(rendered)
            elif isinstance(b, ToolResultContent):
                blocks.append({"type": "tool_result", "tool_use_id": b.tool_use_id, "content": b.content})
            else:
                blocks.append({"type": "text", "text": b.text})
        out.append({"role": msg.role, "content": blocks})
    return {"model": "claude-opus-5-5", "system": "S", "messages": out}


async def _rounds(first: dict, second: dict, stats: dict) -> list[dict]:
    trim = cache_guard.declared_history_rewrites(SimpleNamespace(trim_report=None, fit={"passes": [stats]}))
    loop = uuid.uuid4().hex
    for body, declared in ((first, None), (second, trim)):
        cache_guard.observe_cache_usage(
            provider="anthropic", model="claude-opus-5-5", conversation_id="c-think", request_id="r-think",
            loop_id=loop, system_text="S", tool_names=(),
            raw_usage={"input_tokens": 200, "cache_read_input_tokens": 9000, "output_tokens": 5},
            wire_payload=body, trimmed_blocks=declared,
        )
    await asyncio.sleep(0.05)


@pytest.mark.asyncio
async def test_dropped_thinking_in_a_text_only_message_files_no_drift(captured) -> None:
    config = _conversation("anthropic")
    first = _wire(config)
    stats = await input_fit._stub_history_to_fit(config, config.messages)
    assert stats["thinking_blocks_dropped"] == 3, stats
    second = _wire(config)
    second["messages"].append({"role": "assistant", "content": [{"type": "text", "text": "next"}]})
    await _rounds(first, second, stats)
    rows = [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]
    assert rows == [], f"a lawful thinking drop filed drift: {rows and rows[0]['payload']['changed']}"


@pytest.mark.asyncio
async def test_unrelated_drift_beside_a_thinking_drop_still_files_alone(captured) -> None:
    config = _conversation("anthropic")
    first = _wire(config)
    stats = await input_fit._stub_history_to_fit(config, config.messages)
    second = _wire(config)
    second["messages"].append({"role": "assistant", "content": [{"type": "text", "text": "next"}]})
    second["messages"][2]["content"][0]["text"] = "question 1 (re-rendered)"
    await _rounds(first, second, stats)
    rows = [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]
    assert rows and [c for c in rows[0]["payload"]["changed"] if "messages[2]" in c]
    assert len(rows[0]["payload"]["changed"]) == 1, rows[0]["payload"]["changed"]


@pytest.mark.asyncio
async def test_a_gemini_thought_is_never_dropped() -> None:
    config = _conversation("google")
    stats = await input_fit._stub_history_to_fit(config, config.messages)
    kept = [b for m in config.messages for b in m.content if isinstance(b, ThinkingContent)]
    assert len(kept) == 3, "a Gemini thought was dropped; its contract says resend every thought block"
    assert stats["thinking_blocks_dropped"] == 0
