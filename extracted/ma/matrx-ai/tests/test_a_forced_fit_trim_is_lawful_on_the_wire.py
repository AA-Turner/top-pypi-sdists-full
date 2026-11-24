"""A make-it-fit trim (``input_fit`` forced trims, the last-resort stub) is a declared, lawful rewrite.

Before: the fit passes recorded only counts, so the cache guard could not place their rewrites on
the wire and filed ``prompt_cache_prefix_drift`` every time an over-limit call was made to fit: a
false system error on a lawful rewrite, the kind that trains people to ignore the drift alarm. Now
each pass records the call ids it rewrote, and only an unexplained change files.

SUT: the real ``input_fit.ensure_fits`` with the real ``send_boundary._forced_trim``, the real
``cache_guard.declared_history_rewrites`` and ``observe_cache_usage``. The wire body is the
Anthropic shape of the same canonical messages, before and after the fit.
"""

from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace

import pytest

from matrx_ai.config import (
    ToolCallContent,
    ToolResultContent,
    UnifiedMessage,
    context_preflight,
    input_fit,
)
from matrx_ai.config.context_preflight import estimate_prompt_tokens
from matrx_ai.config.send_boundary import STAGE_LOOP, _forced_trim
from matrx_ai.providers import cache_guard


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    context_preflight.configure_context_preflight(enabled=True, trip_fraction=1.0)
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: 1_000_000)
    input_fit.set_compactor(None)
    yield
    input_fit.set_input_budget_resolver(None)
    input_fit.set_compactor(None)


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    rows: list[dict] = []

    async def record_error(exc, **kwargs):
        rows.append(kwargs)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error)
    return rows


def _loop(iterations: int = 12, chars: int = 60_000) -> SimpleNamespace:
    messages = [UnifiedMessage(role="user", content=[ToolResultContent(tool_use_id="seed", content="start")])]
    for i in range(iterations):
        messages.append(UnifiedMessage(role="assistant", position=None, content=[
            ToolCallContent(id=f"call-{i}", name="shell_execute", arguments={"command": f"step {i}"}),
        ]))
        messages.append(UnifiedMessage(role="tool", position=None, content=[
            ToolResultContent(tool_use_id=f"call-{i}", name="shell_execute", content="x" * chars, output_chars=chars),
        ]))
    return SimpleNamespace(
        model="claude-opus-5-5", matrx_model_name="claude-opus-5-5", messages=messages,
        system_instruction=None, tools=[], prompt_cache_key=None,
    )


def _wire(config: SimpleNamespace) -> dict:
    """The Anthropic wire shape of the canonical messages (tool results ride in a user turn)."""
    out: list[dict] = []
    for msg in config.messages:
        blocks: list[dict] = []
        for b in msg.content:
            if isinstance(b, ToolCallContent):
                blocks.append({"type": "tool_use", "id": b.id, "name": b.name, "input": b.arguments})
            elif isinstance(b, ToolResultContent):
                blocks.append({"type": "tool_result", "tool_use_id": b.tool_use_id, "content": b.content})
            else:
                blocks.append({"type": "text", "text": getattr(b, "text", "")})
        out.append({"role": "assistant" if msg.role == "assistant" else "user", "content": blocks})
    return {"model": "claude-opus-5-5", "system": "S", "messages": out}


async def _forced_fit_rounds(captured, *, drift_elsewhere: bool) -> dict:
    config = _loop()
    first = _wire(config)
    limit = estimate_prompt_tokens(config) // 3
    input_fit.set_input_budget_resolver(lambda _c, cfg, _p: (limit, estimate_prompt_tokens(cfg)))
    record = await input_fit.ensure_fits(config, policy=None, stage=STAGE_LOOP, conversation_id="c", trim=_forced_trim)
    assert record and record["fits"], record
    second = _wire(config)
    second["messages"].append({"role": "user", "content": [{"type": "text", "text": "next"}]})
    if drift_elsewhere:
        second["messages"][0]["content"][0]["content"] = "start (re-rendered)"
    trim = cache_guard.declared_history_rewrites(SimpleNamespace(trim_report=None, fit=record))
    loop = uuid.uuid4().hex
    for body, declared in ((first, None), (second, trim)):
        cache_guard.observe_cache_usage(
            provider="anthropic", model="claude-opus-5-5", conversation_id="c-fit", request_id="r-fit",
            loop_id=loop, system_text="S", tool_names=(),
            raw_usage={"input_tokens": 200, "cache_read_input_tokens": 9000, "output_tokens": 5},
            wire_payload=body, trimmed_blocks=declared,
        )
    await asyncio.sleep(0.05)
    return record


@pytest.mark.asyncio
async def test_a_forced_fit_trim_files_no_drift_row(captured) -> None:
    record = await _forced_fit_rounds(captured, drift_elsewhere=False)
    assert any(p.get("blocks_rewritten") for p in record["passes"]), "the forced trim rewrote nothing"
    rows = [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]
    assert rows == [], f"a lawful forced trim filed drift: {rows and rows[0]['payload']['changed']}"


@pytest.mark.asyncio
async def test_unrelated_drift_during_a_forced_trim_still_files(captured) -> None:
    await _forced_fit_rounds(captured, drift_elsewhere=True)
    rows = [r for r in captured if r["kind"] == "prompt_cache_prefix_drift"]
    assert rows, "drift in an item the trim never touched was not filed"
    changed = rows[0]["payload"]["changed"]
    assert any("messages[0]" in c for c in changed)
    assert len(changed) == 1, f"the trimmed items were filed too: {changed}"


@pytest.mark.asyncio
async def test_the_last_resort_stub_pass_names_what_it_rewrote() -> None:
    config = _loop(iterations=6, chars=4_000)
    config.messages.append(UnifiedMessage(role="user", content=[ToolResultContent(tool_use_id="late", content="now")]))
    stats = await input_fit._stub_history_to_fit(config, config.messages)
    ids = {b.get("call_id") or b.get("tool_use_id") for b in stats.get("rewritten_blocks", [])}
    assert stats["stubbed_blocks"] and ids, f"the stub pass recorded only counts: {stats}"
