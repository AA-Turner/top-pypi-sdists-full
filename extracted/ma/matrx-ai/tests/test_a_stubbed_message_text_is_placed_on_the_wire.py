"""FORCING GUARD — the last-resort fit's stubbed message TEXT is a declared, placed rewrite, not drift.

Live (system_error ``prompt_cache_prefix_drift``, chat 0fbc8c1f, claude-opus-5-5, 2026-11-12): "messages[0]
(user) changed (6,492 -> 1,817 bytes) (possible cause: the send boundary rewrote 22 block(s) it could not
place on the wire)". A history made of the person's own words was over the input limit; the stub pass
(``input_fit._stub_history_to_fit`` step c) replaced earlier texts with ``STUB_TEXT`` and declared them
only as an unplaceable count, so every lawful fit of a long chat filed a false prefix break. Each stub is
now declared, and the guard places it by the stub's own words in an item that changed, never more than
declared.

SUT: the real stub pass, the real ``declared_history_rewrites`` and ``observe_cache_usage``.
"""

from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace

import pytest

from matrx_ai.config import TextContent, UnifiedMessage, input_fit
from matrx_ai.config.input_fit import STUB_TEXT
from matrx_ai.providers import cache_guard


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    rows: list[dict] = []

    async def record_error(exc, **kwargs):
        rows.append(kwargs)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error)
    return rows


def _chat(turns: int = 6) -> SimpleNamespace:
    messages = []
    for i in range(turns):
        messages.append(UnifiedMessage(role="user", content=[TextContent(text=f"question {i} " + "words " * 800)]))
        messages.append(UnifiedMessage(role="assistant", content=[TextContent(text=f"answer {i}")]))
    messages.append(UnifiedMessage(role="user", content=[TextContent(text="the newest turn")]))
    return SimpleNamespace(messages=messages)


def _wire(config: SimpleNamespace) -> dict:
    return {
        "model": "claude-opus-5-5",
        "system": "S",
        "messages": [
            {"role": m.role if m.role == "assistant" else "user",
             "content": [{"type": "text", "text": b.text} for b in m.content]}
            for m in config.messages
        ],
    }


async def _rounds(captured, monkeypatch, *, drift_elsewhere: bool) -> dict:
    async def _never_fits(_config):
        return [{"estimated_tokens": 10, "limit_tokens": 1, "enforced": True}]

    monkeypatch.setattr(input_fit, "_limits", _never_fits)
    config = _chat()
    first = _wire(config)
    stats = await input_fit._stub_history_to_fit(config, config.messages)
    assert stats["text_blocks_stubbed"], stats
    second = _wire(config)
    second["messages"].append({"role": "assistant", "content": [{"type": "text", "text": "ok"}]})
    if drift_elsewhere:
        second["messages"][1]["content"][0]["text"] = "answer 0 (re-rendered)"
    trim = cache_guard.declared_history_rewrites(SimpleNamespace(trim_report=None, fit={"passes": [stats]}))
    loop = uuid.uuid4().hex
    for body, declared in ((first, None), (second, trim)):
        cache_guard.observe_cache_usage(
            provider="anthropic", model="claude-opus-5-5", conversation_id="c-stub", request_id="r-stub",
            loop_id=loop, system_text="S", tool_names=(),
            raw_usage={"input_tokens": 200, "cache_read_input_tokens": 9000, "output_tokens": 5},
            wire_payload=body, trimmed_blocks=declared,
        )
    await asyncio.sleep(0.05)
    return stats


@pytest.mark.asyncio
async def test_stubbed_message_text_files_no_drift(captured, monkeypatch) -> None:
    await _rounds(captured, monkeypatch, drift_elsewhere=False)
    rows = [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]
    assert rows == [], f"a declared text stub was filed as drift: {rows and rows[0]['payload']['changed']}"


@pytest.mark.asyncio
async def test_unrelated_drift_beside_text_stubs_still_files(captured, monkeypatch) -> None:
    await _rounds(captured, monkeypatch, drift_elsewhere=True)
    rows = [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]
    assert rows, "drift in an item the stub never touched was not filed"
    changed = rows[0]["payload"]["changed"]
    assert len(changed) == 1 and "messages[1]" in changed[0], changed


def test_an_old_stub_in_an_unchanged_item_does_not_whitelist() -> None:
    body = {"messages": [{"role": "user", "content": [{"type": "text", "text": STUB_TEXT}]}]}
    positions, unplaced = cache_guard.place_trim_on_wire(
        body, cache_guard.TrimDeclaration(text_stubs=1), changed_at=frozenset()
    )
    assert not positions and unplaced == 1
