"""An oversized JSON tool result reaches the model as VALID JSON, with a
continuation the model can actually take.

Live (seo_site findings, 64.8 KB): the size gate cut the text by position, so
the model got an unterminated object, plus a pointer to ``fetch_tool_result`` —
a tool it is only offered if the run can queue it. Now whole trailing items are
dropped (counted in the notice, with the offset where they start in the cached
full text), ``fetch_tool_result`` joins the next turn's tools, and where it
cannot be offered the pointer names a re-call instead.
"""

from __future__ import annotations

import json
import re
from typing import Any

import pytest
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType
from matrx_ai.tools.registry import ToolRegistry

FINDINGS = {
    "status": "ok",
    "data": {
        "findings": [
            {
                "check": "title_missing",
                "severity": "high",
                "page": f"https://example.com/page/{i}",
                "message": "The page has no <title>; add one that names the page. " * 3,
            }
            for i in range(500)
        ]
    },
    "notices": ["stored crawl from 2026-09-27"],
}


class _NullEmitter(SilentEmitter):
    """Every Emitter method is a no-op (SilentEmitter mirrors the protocol); overrides below."""

    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_tool_event(self, *_a: Any, **_kw: Any) -> None: ...
    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


def _tool(name: str, body) -> ToolDefinition:
    td = ToolDefinition(
        name=name,
        description=name,
        parameters={},
        tool_type=ToolType.LOCAL,
        function_path=f"tests.{name}",
        source_kind="native",
    )
    td._callable = body
    return td


@pytest.fixture
def run(monkeypatch):
    from matrx_connect import AppContext
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    registry = ToolRegistry.get_instance()
    saved = dict(registry._tools)
    app = AppContext(emitter=_NullEmitter(), metadata={}, is_authenticated=True)
    token = set_app_context(app)

    async def findings(*_a: Any, **_kw: Any) -> dict[str, Any]:
        return {"result": json.loads(json.dumps(FINDINGS))}

    async def fetch(*_a: Any, **_kw: Any) -> str:
        return ""

    registry._tools["seo_site"] = _tool("seo_site", findings)

    async def execute(*, offer_fetch: bool) -> tuple[str, Any]:
        if offer_fetch:
            registry._tools["fetch_tool_result"] = _tool("fetch_tool_result", fetch)
        content, _result = await ToolExecutor(registry=registry).execute(
            "seo_site", {}, ToolContext(call_id="call-big", tool_name="seo_site", emitter=_NullEmitter())
        )
        return content["content"], app

    yield execute
    registry._tools = saved
    clear_app_context(token)


async def test_the_model_gets_valid_json_and_where_the_rest_starts(run) -> None:
    text, _app = await run(offer_fetch=True)
    full = json.dumps(FINDINGS, ensure_ascii=False)
    assert len(full) > 50_000

    body, sep, notice = text.partition("\n\n[")
    assert sep, "no size-gate notice"
    shown = json.loads(body)  # parses — no half object
    kept = len(shown["data"]["findings"])
    assert 0 < kept < 500
    assert f"data.findings shows {kept} of 500 items ({500 - kept} more not shown)" in notice
    offset = int(re.search(r"offset=(\d+)", notice).group(1))
    assert full[offset:].startswith(json.dumps(FINDINGS["data"]["findings"][kept], ensure_ascii=False))


async def test_fetch_tool_result_is_on_the_next_turns_tools(run) -> None:
    from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.tools.dynamic_drain import drain_tool_mutations

    text, app = await run(offer_fetch=True)
    assert "call the `fetch_tool_result` tool" in text
    config = UnifiedConfig(
        model="gpt-5-mini",
        messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])],
        tools=["seo_site"],
    )
    await drain_tool_mutations(config, app)
    assert "fetch_tool_result" in config.tools


async def test_without_fetch_tool_result_the_pointer_names_a_step_the_model_can_take(run) -> None:
    text, _app = await run(offer_fetch=False)
    json.loads(text.partition("\n\n[")[0])
    assert "call the `fetch_tool_result` tool" not in text
    assert "call `seo_site` again asking for less at a time" in text


# ── review of c61fa8460a ────────────────────────────────────────────────────


async def test_the_production_gate_never_calls_a_structural_cut_positional() -> None:
    """apply_size_gate_async appends the no-relevance-judge note; on a structural
    cut it must not claim "the first characters were kept"."""
    from matrx_ai.tools.result_gate import GateContext, apply_size_gate_async

    full = json.dumps(FINDINGS, ensure_ascii=False)
    gated, truncated = await apply_size_gate_async(
        {"call_id": "call-gate", "content": full, "output_chars": len(full)},
        output_self_capped=False,
        tool_name="seo_site",
        tool_kind="native",
        conversation_id=None,
        user_id=None,
        gate_context=GateContext(user_question="which pages are missing a title?"),
    )
    text = gated["content"]
    assert truncated
    json.loads(text.partition("\n\n[")[0])
    assert "first characters were kept" not in text
    assert "not chosen by relevance" in text


def _cut(value: object, limit: int):
    from matrx_ai.tools.output_caps import truncate_json_structurally

    return truncate_json_structurally(json.dumps(value, ensure_ascii=False), limit=limit)


def test_equal_sibling_lists_share_the_cut() -> None:
    row = {"x": "y" * 80}
    text, cuts, _offset, _std = _cut({"findings": [row] * 300, "other": [row] * 300}, 20_000)
    shown = json.loads(text)
    assert abs(len(shown["findings"]) - len(shown["other"])) <= 1
    assert len(shown["findings"]) > 0, cuts


def test_a_list_whose_removal_cannot_help_is_left_whole() -> None:
    value = {"l": [1, 2], "s": "z" * 60_000}
    text, cuts, offset, _std = _cut(value, 50_000)
    shown = json.loads(text)
    assert shown["l"] == [1, 2]
    assert shown["s"].startswith("z" * 1000) and "more characters not shown" in shown["s"]
    # 3. the pointer is the actual cut position inside the string
    full = json.dumps(value, ensure_ascii=False)
    kept = len(shown["s"].split("…")[0])
    assert offset == full.index('"s": "') + len('"s": "') + kept


def test_a_non_standard_layout_says_the_offset_is_unknown() -> None:
    from matrx_ai.tools.output_caps import truncate_with_notice

    pretty = json.dumps(FINDINGS, indent=2)
    out = truncate_with_notice(
        pretty, limit=50_000, total_chars=len(pretty), call_id="c", tool_name="seo_site"
    )
    json.loads(out.partition("\n\n[")[0])
    assert "position of the dropped content in the full text is unknown" in out
