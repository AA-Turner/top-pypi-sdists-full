"""``site_data`` tool: happy path, not-configured, the TOTAL record bound, typed failures for a
missing recorder / spend refusal, and the web reader stamping site-data provenance.

The Bright Data client is real, over an httpx.MockTransport (no network, nothing billed)."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
from matrx_scraper import _ext
from matrx_scraper.vendors import brightdata as bd

from matrx_ai.tools.implementations.site_data import site_data
from matrx_ai.tools.implementations.web import _stamp_read_engine
from matrx_ai.tools.models import ToolContext

GMAPS_URL = "https://www.google.com/maps/place/?q=place_id:ChIJN1t_tDeuEmsRUsoyG83frY4"
_REC = {"name": "Googleplex", "rating": 4.6, "address": "1600 Amphitheatre Pkwy"}


@pytest.fixture(autouse=True)
def _state():
    saved = dict(_ext._registry)
    bd.clear_brightdata_call_observers()
    bd.clear_brightdata_call_guards()
    bd.clear_brightdata_call_flushers()
    yield
    bd.clear_brightdata_call_observers()
    bd.clear_brightdata_call_guards()
    bd.clear_brightdata_call_flushers()
    _ext._registry.clear()
    _ext._registry.update(saved)


def _install_client() -> list[httpx.Request]:
    seen: list[httpx.Request] = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen.append(req)
        return httpx.Response(200, json=[_REC])

    _ext.configure_ext(brightdata_client=bd.BrightDataClient(
        "k", transport=httpx.MockTransport(handler), poll_interval_s=0))
    return seen


def _ctx() -> ToolContext:
    return ToolContext(call_id="c1")


async def test_happy_path_returns_records_rendering_and_provenance() -> None:
    billed: list[Any] = []
    bd.register_brightdata_call_observer(billed.append)
    _install_client()
    res = await site_data({"url": GMAPS_URL}, _ctx())
    assert res.success
    out = res.output
    assert out["status"] == "success" and out["record_count"] == 1
    assert "Googleplex" in out["rendering"]
    assert out["provenance"]["provider"] == "brightdata" and out["provenance"]["records_billed"] == 1
    assert len(billed) == 1


async def test_not_configured_is_a_typed_failure_with_a_remedy() -> None:
    _ext._registry.pop("brightdata_client", None)
    res = await site_data({"url": GMAPS_URL}, _ctx())
    assert not res.success and res.error is not None
    assert "not configured" in res.error.message and "web" in (res.error.suggested_action or "")


@pytest.mark.parametrize(
    "args",
    [
        {"site": "trustpilot_reviews", "inputs": [{"url": "https://www.trustpilot.com/review/x.com"}] * 11,
         "max_records": 1},
        {"site": "trustpilot_reviews", "inputs": [{"url": "https://www.trustpilot.com/review/x.com"}] * 6,
         "max_records": 20},
    ],
)
async def test_total_record_bound_is_refused_typed_and_nothing_is_sent(args: dict[str, Any]) -> None:
    bd.register_brightdata_call_observer(lambda _c: None)
    seen = _install_client()
    res = await site_data(args, _ctx())
    assert not res.success and res.error is not None and res.error.error_type == "validation"
    assert "100 records in total" in res.error.message and res.error.suggested_action
    assert seen == []


async def test_missing_recorder_is_a_typed_failure_not_a_crash() -> None:
    seen = _install_client()  # no observer registered
    res = await site_data({"url": GMAPS_URL}, _ctx())
    assert not res.success and res.error is not None
    assert "cost" in res.error.message and "nothing was fetched" in res.error.message
    assert res.error.suggested_action and seen == []


async def test_usage_limit_refusal_uses_points_wording() -> None:
    class UsageLimitReachedError(Exception):
        is_caller_refusal = True

    async def refuse(_ds: str) -> None:
        raise UsageLimitReachedError("You've reached your AI usage limit for now.")

    bd.register_brightdata_call_observer(lambda _c: None)
    bd.register_brightdata_call_guard(refuse)
    seen = _install_client()
    res = await site_data({"url": GMAPS_URL}, _ctx())
    assert not res.success and res.error is not None
    assert res.error.message == "You've used all your points for now. Upgrade your plan to keep going."
    assert "AI usage" not in res.error.message and res.error.is_retryable is False and seen == []


async def test_a_non_refusal_guard_bug_is_not_swallowed() -> None:
    async def boom(_ds: str) -> None:
        raise RuntimeError("guard bug")

    bd.register_brightdata_call_observer(lambda _c: None)
    bd.register_brightdata_call_guard(boom)
    _install_client()
    with pytest.raises(RuntimeError, match="guard bug"):
        await site_data({"url": GMAPS_URL}, _ctx())


def test_stamp_read_engine_carries_site_data_provenance_and_notice() -> None:
    prov = {"provider": "brightdata", "engine": "site_data", "announcement": "site data via Bright Data"}
    page = _stamp_read_engine({"engine": "site_data:brightdata", "provenance": prov,
                               "site_data_notice": "fell back to a direct read"}, {"text": "x"})
    assert page["engine"] == "site_data:brightdata" and page["provenance"] == prov
    assert page["site_data_notice"] == "fell back to a direct read"
    plain = _stamp_read_engine({"text": "y"}, {"text": "y"})
    assert plain == {"text": "y"}
    assert _stamp_read_engine("not a dict", {"text": "z"}) == {"text": "z"}
