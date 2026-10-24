"""``site_data`` with ``save_to_table``: the tool resolves the source and renders; the HOST's injected
writer (matrx-scraper ``site_data_table_writer``) fetches and writes the table. Fakes only; the real
writer is proven in aidream/services/data_fetch/tests."""

from __future__ import annotations

from typing import Any

import pytest
from matrx_scraper import _ext
from matrx_scraper.features.site_data import SiteDataTableRefused, SiteDataTableSaved

import matrx_ai.tools.implementations.site_data as site_data_module
from matrx_ai.tools.implementations.site_data import site_data
from matrx_ai.tools.models import ToolContext

TP_URL = "https://www.trustpilot.com/review/www.amazon.com"


@pytest.fixture(autouse=True)
def _ext_state():
    saved = dict(_ext._registry)
    yield
    _ext._registry.clear()
    _ext._registry.update(saved)


@pytest.fixture(autouse=True)
def _purposeful_door():
    """The table path is a purposeful screen's; chat never starts a dataset."""
    from matrx_ai.tools.tests.test_agent_projection import _make_ctx
    from matrx_connect.context.app_context import clear_app_context, set_app_context

    token = set_app_context(_make_ctx({"tool_origin": "screen_run"}))
    yield
    clear_app_context(token)


def _ctx() -> ToolContext:
    return ToolContext(call_id="call-1", tool_name="site_data")


def _writer(seen: list[Any], records: list[dict[str, Any]] | None = None):
    async def write(request, progress):
        seen.append(request)
        if progress:
            await progress("Storing records")
        recs = records if records is not None else [{"review_id": "r1", "rating": 5, "review_title": "Great"}]
        return SiteDataTableSaved(records=recs, table={
            "table_id": "tbl-1", "table_name": "Trustpilot - amazon", "rows_created": len(recs),
            "rows_updated": 0, "records_billed": len(recs), "cost_usd": 0.0, "job_id": "j1"})
    return write


async def test_save_to_table_returns_the_table_reference_and_the_usual_rendering():
    seen: list[Any] = []
    _ext.configure_ext(site_data_table_writer=_writer(seen))
    res = await site_data({"url": TP_URL, "max_records": 5, "save_to_table": True, "table_name": "Amazon reviews"}, _ctx())
    assert res.success, res.error
    assert res.output_kind is None
    out = res.output
    assert (out["table_id"], out["table_name"], out["rows_created"], out["rows_updated"], out["records_billed"]) == (
        "tbl-1", "Trustpilot - amazon", 1, 0, 1)
    assert out["rendering"] and out["records"] and out["record_count"] == 1
    assert seen[0].source_key == "trustpilot_reviews" and seen[0].inputs == [{"url": TP_URL}]
    assert seen[0].table_name == "Amazon reviews" and seen[0].max_records == 5


async def test_default_false_never_touches_the_writer():
    seen: list[Any] = []
    _ext.configure_ext(site_data_table_writer=_writer(seen), brightdata_client=None)
    res = await site_data({"url": TP_URL, "max_records": 5}, _ctx())
    assert not seen
    assert not res.success  # no client wired: the normal door answers not_configured, as before


async def test_a_host_refusal_is_a_typed_tool_failure_not_a_silent_success():
    async def refuse(request, progress):
        raise SiteDataTableRefused("usage_limit", "You've used all your points for now.")

    _ext.configure_ext(site_data_table_writer=refuse)
    res = await site_data({"url": TP_URL, "save_to_table": True}, _ctx())
    assert not res.success
    assert res.error.message == "You've used all your points for now."
    assert "Do not retry" in (res.error.suggested_action or "")


async def test_no_writer_injected_says_so():
    _ext._registry.pop("site_data_table_writer", None)
    res = await site_data({"url": TP_URL, "save_to_table": True}, _ctx())
    assert not res.success and "not set up" in res.error.message


@pytest.mark.asyncio
async def test_chat_door_returns_the_typed_not_started_result_without_fetching(monkeypatch):
    import matrx_scraper.features.site_data as door

    monkeypatch.setattr(site_data_module, "is_chat_door", lambda **_: True)

    async def forbidden(*args, **kwargs):
        raise AssertionError("chat must not start a dataset fetch")

    monkeypatch.setattr(door, "fetch", forbidden)
    monkeypatch.setattr(door, "fetch_to_table", forbidden)
    result = await site_data({"url": TP_URL}, _ctx())
    assert result.output_kind == "data_fetch_not_started"
    assert result.output == {
        "__kind": "data_fetch_not_started",
        "status": "not_started",
        "message": "A slower dataset exists for https://www.trustpilot.com/review/www.amazon.com, but it is not started from chat. Tell the person they can start it from the Data Library (/data/library); for a quick answer now, use web with action='read' on the page URL.",
    }
