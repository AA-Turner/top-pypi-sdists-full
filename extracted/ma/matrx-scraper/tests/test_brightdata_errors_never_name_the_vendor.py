"""Forcing function: nothing a person or an agent can read names the data-source vendor.

Arman: "We don't ever want to say it's from brightdata." Every exception the client raises and
every message site_data hands back is checked for the vendor's name and dataset ids. Vendor
detail belongs in server logs only. No network, no spend (httpx.MockTransport).
"""

from __future__ import annotations

import re

import httpx
import pytest

from matrx_scraper import _ext
from matrx_scraper.features import site_data
from matrx_scraper.vendors import brightdata as bd

LEAK = re.compile(r"bright\s*-?data|brightdata|\bgd_[a-z0-9]+", re.IGNORECASE)
URL = "https://www.trustpilot.com/review/www.amazon.com"


@pytest.fixture(autouse=True)
def _clean():
    saved = dict(_ext._registry)
    bd.clear_brightdata_call_observers()
    bd.clear_brightdata_call_guards()
    bd.clear_brightdata_call_flushers()
    bd.register_brightdata_call_observer(lambda call: None)
    yield
    bd.clear_brightdata_call_observers()
    bd.clear_brightdata_call_guards()
    bd.clear_brightdata_call_flushers()
    _ext._registry.clear()
    _ext._registry.update(saved)


def _client(handler):
    return bd.BrightDataClient("k", transport=httpx.MockTransport(handler), poll_interval_s=0)


def _assert_clean(exc: BaseException) -> None:
    assert not LEAK.search(str(exc)), f"vendor named in user-facing text: {exc!s}"


HANDLERS = {
    "validation_400": lambda r: httpx.Response(
        400, json={"code": "validation_error", "error": "Bright Data says no",
                   "errors": [["gd_l1abc.url", "bad Bright Data url"]]}),
    "server_500": lambda r: httpx.Response(500, json={"error": "Bright Data internal gd_l1abc failure"}),
    "plain_text_502": lambda r: httpx.Response(502, text="Bad gateway from brightdata"),
    "no_snapshot": lambda r: httpx.Response(200, json={}),
}


@pytest.mark.parametrize("name", sorted(HANDLERS))
async def test_trigger_errors_are_vendor_free(name):
    with pytest.raises(bd.BrightDataError) as err:
        await _client(HANDLERS[name]).trigger("gd_l1abc", [{"url": URL}], limit=5)
    _assert_clean(err.value)


async def test_http_status_is_plain_and_class_name_is_not_the_message():
    with pytest.raises(bd.BrightDataError) as err:
        await _client(HANDLERS["server_500"]).trigger("gd_l1abc", [{"url": URL}], limit=5)
    assert str(err.value) == "The data source answered with an error (HTTP 500)"


async def test_input_refusal_reads_plainly():
    with pytest.raises(bd.BrightDataInputError) as err:
        await _client(HANDLERS["validation_400"]).trigger("gd_l1abc", [{"url": URL}], limit=5)
    assert str(err.value).startswith("The data source refused these inputs: ")
    _assert_clean(err.value)


async def test_transport_failure_is_vendor_free():
    def boom(req):
        raise httpx.ConnectError("cannot reach api.brightdata.com")

    with pytest.raises(bd.BrightDataError) as err:
        await _client(boom).trigger("gd_l1abc", [{"url": URL}], limit=5)
    _assert_clean(err.value)
    assert "ConnectError" not in str(err.value)


async def test_pre_flight_refusals_are_vendor_free():
    with pytest.raises(bd.BrightDataUncappedRequest) as e1:
        await _client(HANDLERS["no_snapshot"]).trigger("gd_l1abc", [{"url": URL}], limit=0)
    _assert_clean(e1.value)
    with pytest.raises(bd.BrightDataCapExceeded) as e2:
        await _client(HANDLERS["no_snapshot"]).trigger("gd_l1abc", [{"url": URL}], limit=10_000)
    _assert_clean(e2.value)
    bd.clear_brightdata_call_observers()
    with pytest.raises(bd.BrightDataRecorderMissing) as e3:
        await _client(HANDLERS["no_snapshot"]).trigger("gd_l1abc", [{"url": URL}], limit=5)
    _assert_clean(e3.value)


async def test_failed_job_and_unready_snapshot_are_vendor_free():
    def h(req):
        if req.url.path.endswith("/scrape"):
            return httpx.Response(202, json={"snapshot_id": "s_1"})
        return httpx.Response(200, json={"status": "failed"})

    with pytest.raises(bd.BrightDataError) as e1:
        await _client(h).scrape("gd_l1abc", [{"url": URL}], limit=5, timeout_s=5)
    _assert_clean(e1.value)
    with pytest.raises(bd.BrightDataError) as e2:
        await _client(lambda r: httpx.Response(202, json={"status": "building"})).collect(
            "s_1", dataset_id="gd_l1abc", limit_total=5)
    _assert_clean(e2.value)


@pytest.mark.parametrize("name", ["validation_400", "server_500", "plain_text_502"])
async def test_site_data_tool_message_is_vendor_free(name):
    _ext.configure_ext(brightdata_client=_client(HANDLERS[name]))
    res = await site_data.fetch(url=URL, max_records=5)
    assert res.status in {"input_error", "error"}
    assert not LEAK.search(res.message), res.message


async def test_unreadable_limits_setting_announces_the_stand_in():
    async def broken():
        raise RuntimeError("settings store is down")

    _ext.configure_ext(site_data_limits=broken)
    lim = await bd.current_limits()
    assert lim.max_total_records == bd.DEFAULT_LIMITS.max_total_records
    assert lim.notice == (f"Using the built-in limit of {bd.DEFAULT_LIMITS.max_total_records} records "
                          "because your organization's setting could not be read.")

    def ok(req):
        return httpx.Response(200, json=[{"url": URL, "n": 1}])

    _ext.configure_ext(brightdata_client=_client(ok), site_data_limits=broken)
    res = await site_data.fetch(url=URL, max_records=5)
    assert "built-in limit" in res.message


async def test_a_working_limits_setting_carries_no_notice():
    assert (await bd.current_limits()).notice is None
