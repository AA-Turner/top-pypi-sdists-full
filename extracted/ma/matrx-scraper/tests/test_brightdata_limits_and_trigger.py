"""The host-injected limits seam and trigger mode (durable jobs) of the Bright Data client.

No network, no spend: httpx.MockTransport with the real captured Trustpilot payload.
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from matrx_scraper import _ext
from matrx_scraper.features import site_data
from matrx_scraper.vendors import brightdata as bd

FIX = Path(__file__).parent / "fixtures" / "brightdata"
TP = json.loads((FIX / "trustpilot_reviews.json").read_text())
TP_URL = "https://www.trustpilot.com/review/www.amazon.com"


@pytest.fixture(autouse=True)
def _clean():
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


def _client(handler):
    seen: list[httpx.Request] = []

    def _h(req: httpx.Request) -> httpx.Response:
        seen.append(req)
        return handler(req)

    return bd.BrightDataClient("k", transport=httpx.MockTransport(_h), poll_interval_s=0), seen


def _bills() -> list[bd.BrightDataBillableCall]:
    calls: list[bd.BrightDataBillableCall] = []
    bd.register_brightdata_call_observer(calls.append)
    return calls


def _inject(max_inputs: int, max_total: int) -> None:
    async def hook():
        return bd.BrightDataLimits(max_inputs=max_inputs, max_total_records=max_total,
                                   max_inputs_setting="org.inputs", max_total_records_setting="org.records")

    _ext.configure_ext(site_data_limits=hook)


async def test_package_defaults_hold_when_nothing_is_injected():
    assert await bd.current_limits() == bd.DEFAULT_LIMITS
    assert (bd.DEFAULT_LIMITS.max_inputs, bd.DEFAULT_LIMITS.max_total_records) == (10, 100)


async def test_injected_ceiling_lifts_the_default_and_the_request_goes_out():
    _bills()
    _inject(10, 500)
    client, seen = _client(lambda r: httpx.Response(200, json={"snapshot_id": "s_1"}))
    assert await client.trigger("gd_x", [{"url": TP_URL}], limit=300) == "s_1"
    assert seen[0].url.path == "/datasets/v3/trigger"
    assert seen[0].url.params["limit_per_input"] == "300"


async def test_over_the_injected_ceiling_is_refused_before_anything_is_sent():
    _bills()
    _inject(2, 50)
    client, seen = _client(lambda r: httpx.Response(200, json={"snapshot_id": "s"}))
    with pytest.raises(bd.BrightDataCapExceeded) as err:
        await client.trigger("gd_x", [{"url": TP_URL}], limit=51)
    assert err.value.limits is not None and err.value.limits.max_total_records == 50
    with pytest.raises(bd.BrightDataCapExceeded):
        await client.trigger("gd_x", [{"url": "a"}, {"url": "b"}, {"url": "c"}], limit=1)
    assert seen == []


async def test_a_broken_hook_never_lifts_the_ceiling():
    async def broken():
        raise RuntimeError("knob store down")

    _ext.configure_ext(site_data_limits=broken)
    got = await bd.current_limits()
    assert (got.max_inputs, got.max_total_records) == (bd.DEFAULT_LIMITS.max_inputs, bd.DEFAULT_LIMITS.max_total_records)
    assert got.notice and "built-in limit" in got.notice  # the stand-in announces itself


async def test_uncapped_trigger_is_refused_and_no_observer_refuses():
    client, seen = _client(lambda r: httpx.Response(200, json={"snapshot_id": "s"}))
    with pytest.raises(bd.BrightDataRecorderMissing):
        await client.trigger("gd_x", [{"url": TP_URL}], limit=5)
    _bills()
    with pytest.raises(bd.BrightDataUncappedRequest):
        await client.trigger("gd_x", [{"url": TP_URL}], limit=0)
    assert seen == []


async def test_collect_bills_once_and_a_resumed_collect_bills_nothing():
    calls = _bills()

    def h(req: httpx.Request) -> httpx.Response:
        if req.url.path.startswith("/datasets/v3/progress/"):
            return httpx.Response(200, json={"status": "ready", "records": len(TP)})
        return httpx.Response(200, json=TP)

    client, _ = _client(h)
    assert (await client.progress("s_9"))["status"] == "ready"
    first = await client.collect("s_9", dataset_id="gd_tp", limit_total=25)
    assert len(first.records) == len(TP) and first.records_billed == len(TP)
    assert [c.records_billed for c in calls] == [len(TP)]
    again = await client.collect("s_9", dataset_id="gd_tp", limit_total=25, bill=False)
    assert len(again.records) == len(TP)
    assert len(calls) == 1  # the restart re-download is not a second bill


async def test_collect_of_a_snapshot_still_building_is_an_error_not_a_bill():
    calls = _bills()
    client, _ = _client(lambda r: httpx.Response(202, json={"status": "building"}))
    with pytest.raises(bd.BrightDataError) as err:
        await client.collect("s_1", dataset_id="gd", limit_total=5)
    assert err.value.status_code == 202 and calls == []


async def test_door_and_agent_ceiling_follow_the_injected_limit():
    _bills()
    _inject(10, 30)
    seen: list[httpx.Request] = []

    def h(req: httpx.Request) -> httpx.Response:
        seen.append(req)
        return httpx.Response(200, json=TP)

    _ext.configure_ext(brightdata_client=bd.BrightDataClient("k", transport=httpx.MockTransport(h)))
    res = await site_data.fetch(url=TP_URL, max_records=500)
    assert res.ok
    assert seen[0].url.params["limit_per_input"] == "30"  # clamped to the injected ceiling
