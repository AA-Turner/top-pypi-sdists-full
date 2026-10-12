"""Site data (Bright Data Web Scraper API): client, catalog, door, read_page route.

Real captured payloads live in tests/fixtures/brightdata/. The transport is faked with
httpx.MockTransport — no network, no spend.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
import pytest

from matrx_scraper import _ext
from matrx_scraper.features import read_page as rp
from matrx_scraper.features import site_data
from matrx_scraper.vendors import brightdata as bd
from matrx_scraper.vendors.site_catalog import CATALOG, entries_for_url, get_entry, match

FIX = Path(__file__).parent / "fixtures" / "brightdata"
GMAPS_URL = "https://www.google.com/maps/place/?q=place_id:ChIJRVY_etDX3IARGYLVpoq7f68&hl=en"
TP_URL = "https://www.trustpilot.com/review/www.amazon.com"


def _fix(name: str) -> Any:
    return json.loads((FIX / name).read_text())


@pytest.fixture(autouse=True)
def _clean_state():
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


class Recorder:
    def __init__(self) -> None:
        self.calls: list[bd.BrightDataBillableCall] = []
        self.guarded: list[str] = []

    def observe(self, call: bd.BrightDataBillableCall) -> None:
        self.calls.append(call)

    async def guard(self, dataset_id: str) -> None:
        self.guarded.append(dataset_id)

    def install(self) -> Recorder:
        bd.register_brightdata_call_observer(self.observe)
        bd.register_brightdata_call_guard(self.guard)
        return self


def _client(handler) -> tuple[bd.BrightDataClient, list[httpx.Request]]:
    seen: list[httpx.Request] = []

    def _h(req: httpx.Request) -> httpx.Response:
        seen.append(req)
        return handler(req)

    return bd.BrightDataClient("test-key", transport=httpx.MockTransport(_h), poll_interval_s=0), seen


# ── Catalog ──────────────────────────────────────────────────────────────


def test_catalog_routes_the_captured_urls():
    assert match(GMAPS_URL).key == "google_maps_place"
    assert match(TP_URL).key == "trustpilot_reviews"
    assert match(_fix("amazon_products.json")[0]["url"]).key == "amazon_product"
    assert match("https://www.linkedin.com/company/anthropic").key == "linkedin_company"


def test_catalog_never_routes_a_known_dead_or_unverified_shape():
    # name-only Maps URL → dead_page on the live API (fixture googlemaps_full_error_not_business)
    assert match(_fix("googlemaps_full_error_not_business.json")[0]["input"]["url"]) is None
    assert match("https://www.yelp.com/biz/some-cafe") is None  # blocked live
    assert get_entry("google_maps_reviews") is None  # sign-in wall live
    assert get_entry("indeed_jobs_search") is None  # discover never finished
    assert get_entry("airbnb_listing") is None  # dataset does not support collection
    assert match("https://example.com/") is None


def test_catalog_has_no_social_profiles_or_posts():
    social = ("instagram", "tiktok", "youtube", "twitter", "x.com", "threads", "reddit", "pinterest")
    for e in CATALOG:
        assert not any(s in e.host_pattern for s in social), e.key
    assert match("https://www.linkedin.com/in/someone") is None
    assert match("https://www.facebook.com/someone/posts/1") is None


def test_place_info_beats_reviews_on_a_shared_host():
    keys = [e.key for e in entries_for_url(TP_URL)]
    assert keys[0] == "trustpilot_reviews"
    assert match(GMAPS_URL).key == "google_maps_place"


# ── Rendering ────────────────────────────────────────────────────────────


def test_rendering_of_a_real_place_is_readable_and_names_the_place():
    rec = _fix("googlemaps_full.json")[0]
    text, cut = site_data.render_records([rec], label="Google Maps place")
    assert text.startswith("Site data via Bright Data — Google Maps place (1 record)")
    assert rec["name"] in text and "**address**" in text
    assert not cut


def test_rendering_is_bounded_and_announces_the_cut():
    recs = _fix("trustpilot_reviews.json")
    text, cut = site_data.render_records(recs, label="Trustpilot reviews", limit=4000)
    assert cut and len(text) < 4600
    assert "Rendering stopped at" in text and "`records`" in text


# ── Client: fail closed ──────────────────────────────────────────────────


async def test_no_observer_means_nothing_is_sent():
    """FORCING: delete the observer check in BrightDataClient.scrape and this goes red."""
    client, seen = _client(lambda r: httpx.Response(200, json=_fix("amazon_products.json")))
    with pytest.raises(bd.BrightDataRecorderMissing):
        await client.scrape("gd_x", [{"url": "https://www.amazon.com/dp/1"}], limit=5)
    assert seen == []


@pytest.mark.parametrize("limit", [None, 0, -1, True])
async def test_uncapped_request_is_refused_before_sending(limit):
    """FORCING: delete the cap check in BrightDataClient.scrape and this goes red."""
    Recorder().install()
    client, seen = _client(lambda r: httpx.Response(200, json=_fix("trustpilot_reviews.json")))
    with pytest.raises(bd.BrightDataUncappedRequest):
        await client.scrape("gd_x", [{"url": TP_URL}], limit=limit)  # type: ignore[arg-type]
    assert seen == []


async def test_every_request_carries_the_cap_and_the_guard_runs_first():
    rec = Recorder().install()
    client, seen = _client(lambda r: httpx.Response(200, json=_fix("amazon_products.json")))
    await client.scrape("gd_l7q7dkf244hwjntr0", [{"url": "https://www.amazon.com/dp/1"}], limit=7)
    q = seen[0].url.params
    assert q["limit_per_input"] == "7" and q["limit_multiple_results"] == "7"
    assert q["include_errors"] == "true" and "type" not in q
    assert rec.guarded == ["gd_l7q7dkf244hwjntr0"]


async def test_guard_refusal_stops_the_request():
    async def refuse(_ds: str) -> None:
        raise PermissionError("out of points")

    bd.register_brightdata_call_observer(lambda c: None)
    bd.register_brightdata_call_guard(refuse)
    client, seen = _client(lambda r: httpx.Response(200, json=[]))
    with pytest.raises(PermissionError):
        await client.scrape("gd_x", [{"url": TP_URL}], limit=3)
    assert seen == []


# ── Client: sync, errors, 202 polling ───────────────────────────────────


async def test_sync_answer_splits_error_records_and_bills_good_ones():
    rec = Recorder().install()
    payload = _fix("trustpilot_reviews.json")[:3] + _fix("yelp_businesses_error_blocked.json")
    client, _ = _client(lambda r: httpx.Response(200, json=payload))
    res = await client.scrape("gd_lm5zmhwd2sni130p", [{"url": TP_URL}], limit=10)
    assert res.mode == "sync" and len(res.records) == 3 and res.records_billed == 3
    assert res.errors[0]["error_code"] == "blocked"
    assert [c.records_billed for c in rec.calls] == [3]


async def test_the_ledger_write_is_flushed_before_scrape_returns():
    order: list[str] = []
    bd.register_brightdata_call_observer(lambda c: order.append("observed"))

    async def flush() -> None:
        order.append("flushed")

    bd.register_brightdata_call_flusher(flush)
    client, _ = _client(lambda r: httpx.Response(200, json=_fix("amazon_products.json")))
    await client.scrape("gd_x", [{"url": "https://www.amazon.com/dp/1"}], limit=2)
    order.append("returned")
    assert order == ["observed", "flushed", "returned"]


async def test_billing_counts_every_returned_record_even_past_the_cap():
    rec = Recorder().install()
    client, _ = _client(lambda r: httpx.Response(200, json=_fix("trustpilot_reviews.json")))
    res = await client.scrape("gd_lm5zmhwd2sni130p", [{"url": TP_URL}], limit=5)
    assert len(res.records) == 5
    assert res.records_billed == 20 and rec.calls[0].records_billed == 20


async def test_all_error_answer_bills_nothing():
    rec = Recorder().install()
    client, _ = _client(lambda r: httpx.Response(200, json=_fix("googlemaps_reviews_error_signin_modal.json")))
    res = await client.scrape("gd_luzfs1dn2oa0teb81", [{"url": GMAPS_URL}], limit=5)
    assert res.records == [] and res.records_billed == 0 and rec.calls == []


async def test_202_is_polled_to_the_snapshot():
    rec = Recorder().install()
    progress = iter(["running", "running", "ready"])

    def handler(req: httpx.Request) -> httpx.Response:
        if req.method == "POST":
            return httpx.Response(202, json={"snapshot_id": "sd_test1"})
        if "/progress/" in req.url.path:
            return httpx.Response(200, json={"status": next(progress)})
        assert req.url.path.endswith("/snapshot/sd_test1")
        return httpx.Response(200, json=_fix("trustpilot_reviews.json")[:4])

    client, seen = _client(handler)
    res = await client.scrape("gd_lm5zmhwd2sni130p", [{"url": TP_URL}], limit=10)
    assert res.mode == "snapshot" and res.snapshot_id == "sd_test1" and len(res.records) == 4
    assert sum("/progress/" in r.url.path for r in seen) == 3
    assert rec.calls[0].snapshot_id == "sd_test1"


async def test_202_that_never_finishes_times_out_with_the_snapshot_id():
    rec = Recorder().install()

    def handler(req: httpx.Request) -> httpx.Response:
        if req.method == "POST" and req.url.path.endswith("/scrape"):
            return httpx.Response(202, json={"snapshot_id": "sd_slow"})
        if req.url.path.endswith("/cancel"):
            return httpx.Response(200, text="OK")
        return httpx.Response(200, json={"status": "running"})

    client, seen = _client(handler)
    with pytest.raises(bd.BrightDataTimeout) as exc:
        await client.scrape("gd_x", [{"url": TP_URL}], limit=5, timeout_s=0.05)
    assert exc.value.snapshot_id == "sd_slow"
    # delivery is unknown: the cap is booked conservatively, announced as estimated
    assert len(rec.calls) == 1 and rec.calls[0].records_billed == 5 and rec.calls[0].estimated
    assert "estimated" in rec.calls[0].detail and rec.calls[0].snapshot_id == "sd_slow"
    # the abandoned job is cancelled so it cannot bill records nobody records
    assert seen[-1].method == "POST" and seen[-1].url.path.endswith("/snapshot/sd_slow/cancel")
    assert "cancelled" in str(exc.value)


async def test_total_record_bound_is_enforced_in_the_client_before_anything_is_sent():
    rec = Recorder().install()
    client, seen = _client(lambda r: httpx.Response(200, json=[]))
    rows = [{"url": TP_URL}] * 11  # too many inputs
    with pytest.raises(bd.BrightDataCapExceeded):
        await client.scrape("gd_x", rows, limit=1)
    with pytest.raises(bd.BrightDataCapExceeded):  # 5 x 21 = 105 > 100 total
        await client.scrape("gd_x", [{"url": TP_URL}] * 5, limit=21)
    assert seen == [] and rec.guarded == [] and rec.calls == []
    await client.scrape("gd_x", [{"url": TP_URL}] * 5, limit=20)  # exactly 100 is allowed
    assert len(seen) == 1


async def test_door_refuses_a_total_over_the_bound_with_an_agent_readable_input_error():
    Recorder().install()
    client, seen = _client(lambda r: httpx.Response(200, json=[]))
    _ext.configure_ext(brightdata_client=client)
    inputs = [{"url": TP_URL}] * 6
    res = await site_data.fetch(site="trustpilot_reviews", inputs=inputs, max_records=50)
    assert res.status == "input_error" and "300" in res.message and "100" in res.message and seen == []
    res = await site_data.fetch(site="trustpilot_reviews", inputs=[{"url": TP_URL}] * 11, max_records=1)
    assert res.status == "input_error" and "10 inputs" in res.message and seen == []


async def test_validation_400_names_the_fields():
    Recorder().install()
    body = {"error": "Invalid input provided", "code": "validation_error",
            "errors": [["url", "Required field"], ["days", "Required field"]]}
    client, _ = _client(lambda r: httpx.Response(400, json=body))
    with pytest.raises(bd.BrightDataInputError, match="days: Required field"):
        await client.scrape("gd_x", [{"bogus": 1}], limit=5)


# ── Door ─────────────────────────────────────────────────────────────────


async def test_door_without_a_client_says_not_configured():
    _ext._registry.pop(site_data.EXT_CLIENT, None)
    res = await site_data.fetch(url=TP_URL)
    assert res.status == "not_configured" and "not configured" in res.message


async def test_door_fetch_renders_and_carries_provenance():
    Recorder().install()
    client, seen = _client(lambda r: httpx.Response(200, json=_fix("googlemaps_full.json")))
    _ext.configure_ext(brightdata_client=client)
    res = await site_data.fetch(url=GMAPS_URL)
    assert res.ok and res.provenance["dataset"] == "google_maps_place"
    assert res.provenance["announcement"] == "site data via Bright Data, Google Maps place"
    assert json.loads(seen[0].content) == [{"url": GMAPS_URL}]


async def test_door_fills_the_dataset_limit_field_with_the_cap():
    Recorder().install()
    client, seen = _client(lambda r: httpx.Response(200, json=_fix("trustpilot_reviews.json")[:2]))
    _ext.configure_ext(brightdata_client=client)
    await site_data.fetch(url=TP_URL, max_records=4)
    assert json.loads(seen[0].content) == [{"url": TP_URL, "num_of_reviews_limit": 4}]
    assert seen[0].url.params["limit_multiple_results"] == "4"


async def test_door_caps_max_records_at_100_and_names_missing_inputs():
    Recorder().install()
    client, seen = _client(lambda r: httpx.Response(200, json=[]))
    _ext.configure_ext(brightdata_client=client)
    res = await site_data.fetch(site="glassdoor_jobs_search", query="nurse")
    assert res.status == "input_error" and "location" in res.message and seen == []
    await site_data.fetch(site="glassdoor_jobs_search", query="nurse", location="Irvine, CA", max_records=999)
    q = seen[0].url.params
    assert q["limit_per_input"] == "100" and q["type"] == "discover_new" and q["discover_by"] == "keyword"


# ── read_page route-first ────────────────────────────────────────────────


async def _no_http(url: str):
    raise AssertionError("the HTTP fetch ran for a routed URL")


async def test_read_page_routes_a_catalog_url_before_the_http_fetch(monkeypatch):
    Recorder().install()
    client, _ = _client(lambda r: httpx.Response(200, json=_fix("googlemaps_full.json")))
    _ext.configure_ext(brightdata_client=client)
    monkeypatch.setattr(rp, "fetch_normally_with_proxy", _no_http)
    out = await rp.read_page_mcp_quick(url=GMAPS_URL)
    assert out["status"] == "success" and out["engine"] == "site_data:brightdata"
    assert out["provenance"]["announcement"] == "site data via Bright Data, Google Maps place"
    assert out["text"].startswith("Site data via Bright Data")
    assert out["page"]["text_data"] == out["text"]


async def test_read_page_does_not_route_when_the_knob_is_off(monkeypatch):
    client, seen = _client(lambda r: httpx.Response(200, json=[]))

    async def off() -> bool:
        return False

    _ext.configure_ext(brightdata_client=client, site_data_route_enabled=off)
    called: list[str] = []

    async def fake_http(url: str) -> dict[str, Any]:
        called.append(url)
        return {"status": "success", "text": "plain page", "result": "plain page"}

    monkeypatch.setattr(rp, "_read_page_http", fake_http)
    out = await rp.read_page_mcp_quick(url=GMAPS_URL)
    assert called == [GMAPS_URL] and seen == [] and out["text"] == "plain page"


async def test_read_page_without_a_client_never_routes(monkeypatch):
    _ext._registry.pop(site_data.EXT_CLIENT, None)

    async def fake_http(url: str) -> dict[str, Any]:
        return {"status": "success", "text": "plain page"}

    monkeypatch.setattr(rp, "_read_page_http", fake_http)
    out = await rp.read_page_mcp_quick(url=GMAPS_URL)
    assert out["text"] == "plain page" and "site_data_notice" not in out


async def test_read_page_falls_through_and_says_so_when_site_data_fails(monkeypatch):
    Recorder().install()
    client, _ = _client(lambda r: httpx.Response(200, json=_fix("googlemaps_full_error_not_business.json")))
    _ext.configure_ext(brightdata_client=client)

    async def fake_http(url: str) -> dict[str, Any]:
        return {"status": "success", "text": "plain page"}

    monkeypatch.setattr(rp, "_read_page_http", fake_http)
    out = await rp.read_page_mcp_quick(url=GMAPS_URL)
    assert "did not answer" in out["site_data_notice"]
    assert out["text"].startswith("[Site data via Bright Data (Google Maps place)")
    assert out["text"].endswith("plain page")


async def test_read_page_falls_through_on_a_spend_refusal(monkeypatch):
    class Refused(Exception):
        is_caller_refusal = True

    async def refuse(_ds: str) -> None:
        raise Refused("out of points")

    bd.register_brightdata_call_observer(lambda c: None)
    bd.register_brightdata_call_guard(refuse)
    client, seen = _client(lambda r: httpx.Response(200, json=[]))
    _ext.configure_ext(brightdata_client=client)

    async def fake_http(url: str) -> dict[str, Any]:
        return {"status": "success", "text": "plain page"}

    monkeypatch.setattr(rp, "_read_page_http", fake_http)
    out = await rp.read_page_mcp_quick(url=GMAPS_URL)
    assert seen == [] and "was not used (Refused" in out["site_data_notice"]


def test_the_package_never_reads_the_bright_data_key_from_the_environment():
    """The host constructs the client and injects it; no module may read the key itself."""
    import re

    root = Path(bd.__file__).resolve().parents[1]
    readers = [
        str(p.relative_to(root))
        for p in root.rglob("*.py")
        if re.search(r"""os\.(?:environ\s*(?:\[|\.get\s*\()|getenv\s*\()\s*["']BRIGHT_DATA""", p.read_text())
    ]
    assert readers == []
