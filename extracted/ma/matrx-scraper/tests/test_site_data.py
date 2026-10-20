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
    # Defaults lean open: a known-broken source still resolves (and says its issue), but is only
    # reachable by key — never auto-routed, never "verified".
    for key in ("google_maps_reviews", "indeed_jobs_search", "airbnb_listing"):
        assert get_entry(key, verified_only=True) is None
        assert get_entry(key).known_issue
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
    assert text.startswith("Live data — Google Maps place (1 record)")
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
    # the abandoned job is canceled so it cannot bill records nobody records
    assert seen[-1].method == "POST" and seen[-1].url.path.endswith("/snapshot/sd_slow/cancel")
    assert "canceled" in str(exc.value)


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
    assert res.provenance["announcement"] == "live data, Google Maps place"
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


# ── read_page: our scraper ALWAYS reads first (the route-first lane is retired) ──────────


async def test_read_page_reads_a_catalog_url_with_our_scraper_and_never_calls_the_dataset(monkeypatch):
    """A covered URL is read by our scraper; no structured-data call runs (2026-10-16 design)."""
    client, seen = _client(lambda r: httpx.Response(200, json=_fix("googlemaps_full.json")))
    _ext.configure_ext(brightdata_client=client)
    called: list[str] = []

    async def fake_http(url: str):
        called.append(url)
        return {"status": "success", "text": "plain page " * 50, "result": "plain page"}, None

    monkeypatch.setattr(rp, "_read_page_http_judged", fake_http)
    out = await rp.read_page_mcp_quick(url=GMAPS_URL)
    assert called == [GMAPS_URL] and seen == []
    assert out["status"] == "success" and "coverage" not in out


def test_the_route_first_lane_is_gone():
    assert not hasattr(rp, "_route_site_data")
    assert not hasattr(site_data, "EXT_ROUTE_ENABLED")


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


def test_google_maps_place_takes_a_name_or_a_place_id_and_leaves_links_alone():
    """TREG 2: the place source was link-only. A name (+ city) or a place id now reaches the vendor's own
    discover options; a link row is byte-for-byte what it was."""
    from matrx_scraper.features.site_data import build_inputs
    from matrx_scraper.vendors.site_catalog import get_entry

    entry = get_entry("google_maps_place")
    link = {"url": GMAPS_URL}
    assert build_inputs(entry, url=None, query=None, location=None, inputs=[dict(link)], cap=3) == [link]
    assert entry.missing(link) == [] and entry.discover_for(link) is None
    by_name = build_inputs(entry, url=None, query=None, location=None,
                           inputs=[{"name": "Pop-A-Lock", "city": "Ithaca NY"}], cap=3)
    assert by_name == [{"keyword": "Pop-A-Lock Ithaca NY", "country": "US"}]
    assert entry.missing(by_name[0]) == [] and entry.discover_for(by_name[0]) == "location"
    by_id = build_inputs(entry, url=None, query=None, location=None, inputs=[{"place_id": "ChIJbf_1dKkr9ocRNLqDZCKLuqA"}], cap=3)
    assert entry.missing(by_id[0]) == [] and entry.discover_for(by_id[0]) == "place_id"
    # a name alone (no city) still searches; an empty row still needs its link
    assert build_inputs(entry, url=None, query=None, location=None, inputs=[{"name": "Pop-A-Lock"}], cap=3)[0]["keyword"] == "Pop-A-Lock"
    assert entry.missing({}) == ["url"]
    # a source that does not take a name keeps refusing one
    other = get_entry("yelp_business")
    assert build_inputs(other, url=None, query=None, location=None, inputs=[{"name": "x"}], cap=3) == [{"name": "x"}]
