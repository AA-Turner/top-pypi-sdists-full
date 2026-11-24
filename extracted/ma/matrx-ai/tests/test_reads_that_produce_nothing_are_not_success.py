"""Research-tool-repair lane S1: work that produced nothing is never success, and every cut and
failure is carried as a structured fact (agent-tools VISION, "Research tool results").

E3 web_read / web batch_read all pages failed · E4 advanced_read all items failed ·
D1 the summarizer failing to load · B2 the summarizer's input cut · D2 the compliance gate
erroring · F the tool-limit knob seam.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools.models import ToolContext


def _ctx() -> ToolContext:
    return ToolContext(conversation_id="c1", call_id="call-1", emitter=None)


def _failing_reader(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_scraper.features.read_page as read_page

    async def fake_read(url: str) -> dict[str, Any]:
        return {"status": "error", "result": f"403 Forbidden at {url}", "text": ""}

    monkeypatch.setattr(read_page, "read_page_mcp_quick", fake_read)


@pytest.mark.asyncio
async def test_web_read_where_every_page_failed_is_a_failure_naming_each_reason(monkeypatch) -> None:
    from matrx_ai.tools.implementations import web as web_mod

    _failing_reader(monkeypatch)
    result = await web_mod.web_read({"urls": ["https://a.example/x", "https://b.example/y"]}, _ctx())
    assert result.success is False
    assert result.error.error_type == "all_pages_failed"
    assert "https://a.example/x" in result.error.message
    assert "https://b.example/y" in result.error.message
    # The per-page facts still ride the output.
    assert result.output["failed"] == 2


@pytest.mark.asyncio
async def test_web_read_with_one_good_page_stays_success(monkeypatch) -> None:
    import matrx_scraper.features.read_page as read_page

    from matrx_ai.tools.implementations import web as web_mod

    async def fake_read(url: str) -> dict[str, Any]:
        if "good" in url:
            return {"status": "success", "result": "A real page."}
        return {"status": "error", "result": "timeout", "text": ""}

    monkeypatch.setattr(read_page, "read_page_mcp_quick", fake_read)

    async def no_landing(result, ctx, page):
        return page

    monkeypatch.setattr(web_mod, "land_agent_read", no_landing)
    result = await web_mod.web_read({"urls": ["https://good.example", "https://bad.example"]}, _ctx())
    assert result.success is True


@pytest.mark.asyncio
async def test_web_batch_read_where_every_page_failed_is_a_failure(monkeypatch) -> None:
    import time

    from matrx_ai.tools.implementations import web as web_mod

    _failing_reader(monkeypatch)
    result = await web_mod._web_batch_read(
        {"urls": ["https://a.example/x", "https://b.example/y"]}, _ctx(), time.time()
    )
    assert result.success is False
    assert result.error.error_type == "all_pages_failed"
    assert "403 Forbidden at https://b.example/y" in result.error.message


@pytest.mark.asyncio
async def test_advanced_read_where_every_item_failed_is_a_failure_with_each_reason(monkeypatch) -> None:
    import matrx_scraper._ext as scraper_ext
    from matrx_scraper.coverage import EXT_READER

    from matrx_ai.tools.implementations.advanced_read import advanced_read

    async def reader(urls, allow):
        return [
            {"url": urls[0], "ok": False, "reader": "advanced reader", "message": "The site blocked it.",
             "points": 0},
            {"url": urls[1], "ok": False, "reader": "social reader", "message": "", "points": 7},
        ]

    monkeypatch.setitem(scraper_ext._registry, EXT_READER, reader)
    result = await advanced_read({"urls": ["https://a.example", "https://b.example"]}, _ctx())
    assert result.success is False
    assert result.error.error_type == "all_pages_failed"
    assert "https://a.example: The site blocked it." in result.error.message
    # A failed item with no message says the reader gave no reason — never a bare "Not read."
    assert "The social reader returned no reason." in result.error.message
    # Billing is said, never hidden: the points the host already charged are named.
    assert "7 points were still spent" in result.error.message
    assert result.output["points_total"] == 7


@pytest.mark.asyncio
async def test_summarizer_that_cannot_load_is_a_declared_failure_not_raw_text(monkeypatch) -> None:
    from matrx_ai.tools.implementations import _summarize_helper
    from matrx_ai.utils.carried_failure import carried_exception

    def broken_runner():
        raise ImportError("no module named the_agent_runtime")

    monkeypatch.setattr(_summarize_helper, "get_mandate_runner", broken_runner)
    out, usage = await _summarize_helper.summarize_content("RAW PAGE TEXT " * 400, "Summarize", None)
    assert out.startswith(_summarize_helper.SUMMARIZE_FAILURE_PREFIX)
    assert "RAW PAGE TEXT" not in out
    assert isinstance(carried_exception(out), ImportError)
    assert usage == []


@pytest.mark.asyncio
async def test_summarizer_input_cap_is_the_organizations_knob(monkeypatch) -> None:
    from matrx_ai.testing.holders import install_named_runner
    from matrx_ai.tools import tool_knobs
    from matrx_ai.tools.implementations import _summarize_helper

    seen: dict[str, Any] = {}

    async def fake_run(agent_cls, **kwargs):
        seen.update(kwargs)

        class R:
            success = True
            output = "summary"
            usage_history: list[Any] = []

        return R()

    install_named_runner(monkeypatch, fake_run)

    async def resolver(feature, key, organization_id):
        assert (feature, key) == ("agents.web_read", "summarize_max_input_chars")
        return 50

    monkeypatch.setattr(tool_knobs, "_resolver", resolver)
    out, _ = await _summarize_helper.summarize_content("y" * 80, "Summarize", None)
    assert seen["inputs"].content.startswith("y" * 50 + "\n\n[Content capped for summarizing: 50 of 80")
    assert out.endswith(_summarize_helper.summarize_cut_marker(50, 80))


@pytest.mark.asyncio
async def test_tool_knob_missing_row_files_it_and_uses_the_mirror(monkeypatch) -> None:
    from matrx_ai.tools import tool_knobs

    class KnobNotRegisteredError(LookupError):
        pass

    async def missing(feature, key, organization_id):
        raise KnobNotRegisteredError(f"{feature}.{key}")

    monkeypatch.setattr(tool_knobs, "_resolver", missing)
    assert await tool_knobs.tool_knob_int("fs_read_max_chars", 40_000, "org") == 40_000

    async def broken(feature, key, organization_id):
        raise RuntimeError("database down")

    monkeypatch.setattr(tool_knobs, "_resolver", broken)
    with pytest.raises(RuntimeError):
        await tool_knobs.tool_knob_int("fs_read_max_chars", 40_000, "org")


@pytest.mark.asyncio
async def test_sql_cell_cap_reads_the_knob(monkeypatch) -> None:
    from matrx_ai.tools import tool_knobs
    from matrx_ai.tools.implementations import database

    async def resolver(feature, key, organization_id):
        assert (feature, key) == ("tools.sql", "cell_max_chars")
        return 123

    monkeypatch.setattr(tool_knobs, "_resolver", resolver)
    assert await database._sql_cell_cap(_ctx()) == 123


@pytest.mark.asyncio
async def test_a_broken_compliance_gate_refuses_naming_its_cause(monkeypatch) -> None:
    from matrx_ai.tools import compliance_gate
    from matrx_ai.utils.carried_failure import carried_exception

    boom = ConnectionError("compliance rules table unreachable")

    async def gate(name, app_ctx):
        raise boom

    monkeypatch.setattr(compliance_gate, "_gate", gate)
    refusal = await compliance_gate.tool_compliance_refusal("web_read", None)
    assert refusal is not None
    assert "ConnectionError: compliance rules table unreachable" in refusal
    assert carried_exception(refusal) is boom
