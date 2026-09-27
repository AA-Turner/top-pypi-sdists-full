"""The `context` tool bounds its own result — and its self-cap claim is TRUE.

Production (ops ``tool_result_overflow:context``): ``mode='full'`` returned whole
bodies — ``full_document_text`` 114,525 chars (x4, 07-14), ``extraction_rows``
104,487 (08-10), ``content`` 51,236 (09-21) — and on 09-12 the lazy
``platform_capabilities`` source returned 113,535 chars while declaring
``output_self_capped``, so the gate recorded nothing. Every read now carries at
most ``_MAX_RESULT_CHARS`` of content (a whole batch included) with an exact
continuation; these tests drive the real tool through the real size gate.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from matrx_ai.tools.implementations import ctx as ctx_mod
from matrx_ai.tools.implementations.ctx import context
from matrx_ai.tools.models import ToolContext
from matrx_ai.tools.output_caps import TOOL_RESULT_SOFT_CAP_CHARS
from matrx_ai.tools.result_gate import (
    _SINKS,
    ToolResultGateEvent,
    apply_size_gate,
    register_tool_result_gate_sink,
)

BUDGET = getattr(ctx_mod, "_MAX_RESULT_CHARS", 40_000)


def _ctx() -> ToolContext:
    return ToolContext(call_id="call_ctx", user_id="u", conversation_id="c", emitter=None)


def _inline(key: str, content: Any) -> SimpleNamespace:
    import json

    text = content if isinstance(content, str) else json.dumps(content)
    return SimpleNamespace(
        key=key,
        type=SimpleNamespace(value="text" if isinstance(content, str) else "json"),
        label=key,
        summary_agent_id=None,
        descriptor=None,
        source=None,
        content=content,
        is_lazy_source=lambda: False,
        content_as_str=lambda: text,
    )


def _lazy(key: str, body: str, calls: list[dict[str, Any]]) -> tuple[SimpleNamespace, Any]:
    obj = SimpleNamespace(
        key=key,
        type=SimpleNamespace(value="json"),
        label="Platform capabilities",
        summary_agent_id=None,
        descriptor=None,
        source=SimpleNamespace(kind="platform_capability_inventory", id="p"),
        is_lazy_source=lambda: True,
        content_as_str=lambda: "",
    )

    async def materialize(source: Any, *, mode: str, offset: int, chars: int | None, user_id: str):
        calls.append({"mode": mode, "offset": offset, "chars": chars})
        end = len(body) if chars is None else min(len(body), offset + chars)
        return SimpleNamespace(
            representation="inventory",
            text=body[offset:end],
            offset=offset,
            total_chars=len(body),
            has_more=end < len(body),
            next_offset=end if end < len(body) else None,
            page_range=None,
        )

    return obj, materialize


async def _call(objs: list[SimpleNamespace], args: dict[str, Any], **ext: Any):
    manifest = MagicMock()
    by_key = {o.key: o for o in objs}
    manifest.get.side_effect = by_key.get
    manifest.all.return_value = objs

    def _get_ext(name: str) -> Any:
        if name == "load_manifest_from_ctx":
            return lambda _app: manifest
        return ext[name]

    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=MagicMock(user_id="u")),
        patch("matrx_ai._ext.get_ext", side_effect=_get_ext),
        patch("matrx_ai._ext.has_ext", side_effect=lambda name: name in ext),
    ):
        return await context(args, _ctx())


@pytest.fixture
def gate_events():
    events: list[ToolResultGateEvent] = []
    register_tool_result_gate_sink(events.append)
    yield events
    _SINKS.remove(events.append)


def _through_gate(result) -> str:
    cd, _ = apply_size_gate(
        result.to_tool_result_content(),
        output_self_capped=result.output_self_capped,
        tool_name="context",
        tool_kind="native",
        conversation_id="c",
        user_id="u",
    )
    return cd["content"]


async def test_inline_full_over_budget_becomes_an_announced_first_page(gate_events) -> None:
    body = "".join(f"line {i:06d} of the full document text\n" for i in range(3_000))  # ~114K
    r = await _call([_inline("full_document_text", body)], {"action": "get", "key": "full_document_text", "mode": "full"})
    assert r.success and r.output_self_capped
    out = r.output
    assert out.content == body[:BUDGET]
    assert (out.mode, out.fell_back_from, out.has_more) == ("page", "full", True)
    assert (out.offset, out.next_offset, out.total_chars) == (0, BUDGET, len(body))
    assert "mode='page'" in out.note and f"offset={BUDGET}" in out.note
    wire = _through_gate(r)
    assert len(wire) < TOOL_RESULT_SOFT_CAP_CHARS
    assert gate_events == []


async def test_inline_full_structured_over_budget_is_sliced_as_json_text(gate_events) -> None:
    rows = [{"__text__": "x" * 900, "i": i} for i in range(120)]  # ~110K as JSON
    r = await _call([_inline("extraction_rows", rows)], {"action": "get", "key": "extraction_rows", "mode": "full"})
    assert r.success and isinstance(r.output.content, str) and len(r.output.content) == BUDGET
    assert r.output.has_more is True
    assert len(_through_gate(r)) < TOOL_RESULT_SOFT_CAP_CHARS
    assert gate_events == []


async def test_small_full_read_is_unchanged_and_native() -> None:
    rows = [{"a": 1}]
    r = await _call([_inline("rows", rows)], {"action": "get", "key": "rows", "mode": "full"})
    assert r.output.content == rows
    assert r.output.has_more is None and r.output.note is None


async def test_lazy_full_asks_the_resolver_for_the_budget_not_everything(gate_events) -> None:
    calls: list[dict[str, Any]] = []
    body = "PLATFORM CAPABILITY INVENTORY\n" + "tool_name — description\n" * 4_700  # ~113K
    obj, mat = _lazy("platform_capabilities", body, calls)
    r = await _call([obj], {"action": "get", "key": "platform_capabilities", "mode": "full"}, materialize_context_source=mat)
    assert calls == [{"mode": "full", "offset": 0, "chars": BUDGET}]
    assert r.output.content == body[:BUDGET]
    assert (r.output.fell_back_from, r.output.next_offset) == ("full", BUDGET)
    assert "offset=" in r.output.note
    assert len(_through_gate(r)) < TOOL_RESULT_SOFT_CAP_CHARS
    assert gate_events == []  # the self-cap claim is now true: no self_cap_exceeded


async def test_page_chars_are_clamped_to_the_budget() -> None:
    body = "y" * 200_000
    r = await _call([_inline("big", body)], {"action": "get", "key": "big", "mode": "page", "offset": 10, "chars": 150_000})
    assert r.output.chars_returned == BUDGET
    assert r.output.next_offset == 10 + BUDGET
    assert "lowered" in r.output.note


async def test_batch_shares_one_budget_and_defers_what_does_not_fit(gate_events) -> None:
    objs = [_inline(f"doc{i}", chr(97 + i) * 30_000) for i in range(3)]
    r = await _call(objs, {"action": "batch", "requests": [{"key": f"doc{i}", "mode": "full"} for i in range(3)]})
    assert r.output_self_capped
    results = r.output.results
    assert [e.success for e in results] == [True, True, True]
    assert results[0].output["content"] == "a" * 30_000  # first fits whole
    assert results[1].output["has_more"] is True  # second gets what is left
    assert results[2].output["chars_returned"] == 0 and "action='get'" in results[2].output["note"]
    assert "doc2" in r.output.note
    assert len(_through_gate(r)) < TOOL_RESULT_SOFT_CAP_CHARS
    assert gate_events == []
