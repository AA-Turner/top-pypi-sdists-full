"""Site-level evidence capture — the fetch, the shape, and the round trip.

The probe is the ONLY reason the site-level checks can score anything: before
it, robots.txt was read into an in-memory cache and discarded, and nothing ever
looked at the www/non-www × http/https variants. These tests drive the real
``probe_site`` over a mock transport, so the code under test is the code that
runs in production — not a stand-in.
"""

from __future__ import annotations

import httpx
import pytest

from matrx_scraper.web_crawl import site_probe as sp
from matrx_scraper.web_crawl.site_probe import (
    SITE_PROBE_FORMAT_VERSION,
    RobotsCapture,
    SiteProbe,
    TlsCapture,
    UrlProbe,
    host_form,
    http_origin_probe,
    http_variant_url,
    load_site_probe,
    page_http_variant_probe,
    probe_site,
    sample_page_urls,
    slash_pair_urls,
    variant_urls,
)

ROOT = "https://example.com/"


@pytest.fixture(autouse=True)
def _allow_public_urls(monkeypatch):
    """The SSRF gate resolves DNS; these hosts are fictional."""

    async def passthrough(url: str) -> str:
        return url

    monkeypatch.setattr(sp, "validate_public_http_url", passthrough)


def install(monkeypatch, handler) -> None:
    """Point the probe's httpx client at a mock transport."""

    real_init = httpx.AsyncClient.__init__

    def patched(self, *args, **kwargs):
        kwargs["transport"] = httpx.MockTransport(handler)
        real_init(self, *args, **kwargs)

    monkeypatch.setattr(httpx.AsyncClient, "__init__", patched)

    async def captured_tls(_root_url: str) -> TlsCapture:
        return TlsCapture(
            hostname="example.com",
            trusted=True,
            hostname_match=True,
            expired=False,
            issuer="organizationName=Example CA",
            not_after="2027-08-09T00:00:00+00:00",
        )

    monkeypatch.setattr(sp, "_capture_tls", captured_tls)


# ---------------------------------------------------------------------------
# Pure shape


def test_host_form_normalises_case_and_default_ports():
    assert host_form("https://Example.COM/a/b?c=1") == "https://example.com"
    assert host_form("https://example.com:443/") == "https://example.com"
    assert host_form("http://example.com:80/") == "http://example.com"
    assert host_form("http://example.com:8080/") == "http://example.com:8080"
    assert host_form("https://www.example.com/") == "https://www.example.com"


def test_variant_urls_are_the_four_forms_regardless_of_which_was_registered():
    assert set(variant_urls("https://www.example.com/deep/path")) == set(
        variant_urls("http://example.com")
    )
    assert len(variant_urls(ROOT)) == 4


def test_probe_round_trips_through_the_site_metadata_shape():
    probe = SiteProbe(
        captured_at="2026-08-09T00:00:00+00:00",
        root_url=ROOT,
        robots=RobotsCapture(url="https://example.com/robots.txt", http_status=200, content="x"),
        tls=TlsCapture(
            hostname="example.com",
            trusted=True,
            hostname_match=True,
            expired=False,
            not_after="2027-08-09T00:00:00+00:00",
        ),
        variants=[UrlProbe(url=ROOT, http_status=200, final_url=ROOT, final_status=200)],
        sitemap_locations=[UrlProbe(url="https://example.com/sitemap.xml", http_status=200)],
    )
    restored = SiteProbe.from_dict(probe.to_dict())
    assert restored is not None
    assert restored.to_dict() == probe.to_dict()


def test_a_probe_from_an_unknown_format_is_ignored_not_misread():
    raw = SiteProbe(captured_at="t", root_url=ROOT).to_dict()
    raw["format_version"] = SITE_PROBE_FORMAT_VERSION + 1
    assert SiteProbe.from_dict(raw) is None
    assert SiteProbe.from_dict("nonsense") is None
    assert SiteProbe.from_dict(None) is None


def test_load_site_probe_reads_the_metadata_key():
    class FakeSite:
        metadata = {"site_probe": SiteProbe(captured_at="t", root_url=ROOT).to_dict()}

    assert load_site_probe(FakeSite()) is not None

    class NoProbe:
        metadata = {"something_else": 1}

    assert load_site_probe(NoProbe()) is None


def test_robots_capture_only_parses_a_2xx_body():
    assert RobotsCapture(url="u", http_status=404).parsed() is None
    assert RobotsCapture(url="u", http_status=None, content="User-agent: *").parsed() is None
    assert RobotsCapture(url="u", http_status=200, content="User-agent: *").parsed() is not None


# ---------------------------------------------------------------------------
# The real fetch, over a mock transport


@pytest.mark.asyncio
async def test_probe_captures_robots_variants_and_sitemap_locations(monkeypatch):
    robots_body = "User-agent: *\nDisallow: /admin/\nSitemap: https://example.com/sm.xml\n"

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url == "https://example.com/robots.txt":
            return httpx.Response(200, text=robots_body)
        if url == "https://example.com/":
            return httpx.Response(200, text="<html></html>")
        if url in ("https://www.example.com/", "http://example.com/", "http://www.example.com/"):
            return httpx.Response(301, headers={"Location": "https://example.com/"})
        if url == "https://example.com/sm.xml":
            return httpx.Response(200, text="<urlset/>")
        return httpx.Response(404)

    install(monkeypatch, handler)
    probe = await probe_site(ROOT)

    assert probe.robots is not None
    assert probe.robots.http_status == 200
    assert probe.robots.parsed().sitemaps == ["https://example.com/sm.xml"]
    assert probe.tls is not None and probe.tls.trusted is True
    assert len(probe.variants) == 4
    by_url = {p.url: p for p in probe.variants}
    # The FIRST status is what is recorded — a 301 here is the measured fact.
    assert by_url["https://www.example.com/"].http_status == 301
    assert by_url["https://www.example.com/"].final_status == 200
    assert by_url["https://example.com/"].http_status == 200
    # Robots' own Sitemap: directive is probed before the conventional paths.
    assert probe.sitemap_locations[0].url == "https://example.com/sm.xml"
    assert [p.url for p in probe.reachable_sitemap_locations] == ["https://example.com/sm.xml"]


@pytest.mark.asyncio
async def test_a_dead_variant_never_costs_us_the_rest_of_the_picture(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.scheme == "http":
            raise httpx.ConnectError("connection refused")
        if str(request.url).endswith("/robots.txt"):
            return httpx.Response(200, text="User-agent: *\nDisallow:\n")
        return httpx.Response(200, text="ok")

    install(monkeypatch, handler)
    probe = await probe_site(ROOT)

    assert probe.robots.http_status == 200
    http_probes = [p for p in probe.variants if p.url.startswith("http://")]
    assert http_probes and all(not p.answered for p in http_probes)
    assert all(p.fetch_error for p in http_probes)
    https_probes = [p for p in probe.variants if p.url.startswith("https://")]
    assert all(p.answered for p in https_probes)


@pytest.mark.asyncio
async def test_a_missing_robots_is_a_status_not_an_error(monkeypatch):
    """404 and "never answered" are different facts and must stay different."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404)

    install(monkeypatch, handler)
    probe = await probe_site(ROOT)
    assert probe.robots.http_status == 404
    assert probe.robots.fetch_error is None
    assert probe.robots.content is None


@pytest.mark.asyncio
async def test_an_unreachable_robots_records_the_error_and_no_status(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out")

    install(monkeypatch, handler)
    probe = await probe_site(ROOT)
    assert probe.robots.http_status is None
    assert "ReadTimeout" in probe.robots.fetch_error


@pytest.mark.asyncio
async def test_an_oversized_robots_is_truncated_and_flagged(monkeypatch):
    body = "User-agent: *\nDisallow: /x\n" + ("# pad\n" * 200_000)

    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url).endswith("/robots.txt"):
            return httpx.Response(200, text=body)
        return httpx.Response(200, text="ok")

    install(monkeypatch, handler)
    probe = await probe_site(ROOT)
    assert probe.robots.truncated
    assert len(probe.robots.content.encode()) <= sp.ROBOTS_MAX_BYTES


@pytest.mark.asyncio
async def test_sitemap_location_probes_are_capped(monkeypatch):
    listed = "\n".join(f"Sitemap: https://example.com/s{i}.xml" for i in range(50))

    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url).endswith("/robots.txt"):
            return httpx.Response(200, text=f"User-agent: *\nDisallow:\n{listed}\n")
        return httpx.Response(200, text="ok")

    install(monkeypatch, handler)
    probe = await probe_site(ROOT)
    assert len(probe.sitemap_locations) == sp.SITEMAP_LOCATION_PROBE_LIMIT


# ---------------------------------------------------------------------------
# Per-page evidence — the http:// twin and the slash pair


def test_sample_is_https_non_root_and_one_per_path():
    sampled = sample_page_urls(
        [
            "https://example.com/",  # root — the variants already cover it
            "http://example.com/a",  # not https — there is no http twin to probe
            "https://example.com/a",
            "https://example.com/a",  # same path twice
            "https://www.example.com/a",  # same path on another host form
            "https://example.com/b",
        ]
    )
    assert sampled == ["https://example.com/a", "https://example.com/b"]


def test_the_page_sample_is_capped():
    urls = [f"https://example.com/p{i}" for i in range(200)]
    assert len(sample_page_urls(urls)) == sp.PAGE_HTTP_VARIANT_PROBE_LIMIT


def test_http_variant_url_is_the_scheme_and_nothing_else():
    assert http_variant_url("https://example.com/a?b=1") == "http://example.com/a?b=1"
    assert http_variant_url("http://example.com/a") is None
    assert http_variant_url("ftp://example.com/a") is None


def test_slash_pair_urls_skips_what_a_slash_does_not_apply_to():
    assert slash_pair_urls("https://example.com/a") == (
        "https://example.com/a",
        "https://example.com/a/",
    )
    assert slash_pair_urls("https://example.com/a/") == (
        "https://example.com/a",
        "https://example.com/a/",
    )
    assert slash_pair_urls("https://example.com/") is None
    assert slash_pair_urls("https://example.com/a?x=1") is None
    assert slash_pair_urls("https://example.com/report.pdf") is None


def test_slash_pair_verdict_needs_two_independent_200s():
    def probe_at(url: str, *, final: str, status: int = 200) -> UrlProbe:
        return UrlProbe(url=url, http_status=status, final_url=final, final_status=200)

    bare_url, slashed_url = "https://example.com/a", "https://example.com/a/"
    duplicated = sp.SlashPairProbe(
        path="/a",
        bare=probe_at(bare_url, final=bare_url),
        slashed=probe_at(slashed_url, final=slashed_url),
    )
    assert duplicated.duplicated is True

    consolidated = sp.SlashPairProbe(
        path="/a",
        bare=probe_at(bare_url, final=bare_url),
        slashed=probe_at(slashed_url, final=bare_url, status=301),
    )
    assert consolidated.duplicated is False

    unanswered = sp.SlashPairProbe(
        path="/a",
        bare=probe_at(bare_url, final=bare_url),
        slashed=UrlProbe(url=slashed_url, fetch_error="ConnectTimeout"),
    )
    assert unanswered.both_answered is False
    assert unanswered.duplicated is False


@pytest.mark.asyncio
async def test_probe_captures_the_per_page_http_twin_and_slash_pair(monkeypatch):
    """A server that redirects its ROOT while serving a deep path over HTTP."""

    seen: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        seen.append((request.method, url))
        if url == "http://example.com/":
            return httpx.Response(301, headers={"Location": "https://example.com/"})
        if url == "http://example.com/deep":
            # The whole point: the origin redirects, this path does not.
            return httpx.Response(200, text="insecure duplicate")
        if url == "https://example.com/deep/":
            return httpx.Response(200, text="the slash twin, live in its own right")
        return httpx.Response(200, text="ok")

    install(monkeypatch, handler)
    probe = await probe_site(ROOT, ["https://example.com/deep"])

    assert [p.url for p in probe.page_http_variants] == ["http://example.com/deep"]
    assert probe.page_http_variants[0].http_status == 200
    assert [p.path for p in probe.slash_pairs] == ["/deep"]
    assert probe.slash_pairs[0].duplicated is True
    # Sampled probes are HEAD — dozens against one host, no body ever read.
    assert ("HEAD", "http://example.com/deep") in seen

    variant = page_http_variant_probe(probe, "https://example.com/deep")
    assert variant == {
        "scope": "page",
        "url": "http://example.com/deep",
        "status": 200,
        "location": "http://example.com/deep",
    }
    # A page outside the sample gets nothing here — the caller falls back to
    # the origin probe rather than borrowing another page's verdict.
    assert page_http_variant_probe(probe, "https://example.com/other") is None
    # …and the origin probe still reports the root's own (correct) redirect.
    origin = http_origin_probe(probe, ROOT)
    assert origin["scope"] == "origin" and origin["status"] == 301


@pytest.mark.asyncio
async def test_a_host_that_refuses_head_is_retried_with_get(monkeypatch):
    methods: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == "http://example.com/deep":
            methods.append(request.method)
            if request.method == "HEAD":
                return httpx.Response(405)
            return httpx.Response(200, text="body")
        return httpx.Response(200, text="ok")

    install(monkeypatch, handler)
    probe = await probe_site(ROOT, ["https://example.com/deep"])

    assert methods == ["HEAD", "GET"]
    assert probe.page_http_variants[0].http_status == 200


@pytest.mark.asyncio
async def test_a_probe_with_no_page_sample_is_the_old_shape(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="ok")

    install(monkeypatch, handler)
    probe = await probe_site(ROOT)

    assert probe.page_http_variants == [] and probe.slash_pairs == []
    assert page_http_variant_probe(probe, "https://example.com/deep") is None


def test_page_evidence_round_trips_and_an_older_probe_still_loads():
    probe = SiteProbe(
        captured_at="2026-08-13T00:00:00+00:00",
        root_url=ROOT,
        page_http_variants=[UrlProbe(url="http://example.com/a", http_status=200)],
        slash_pairs=[
            sp.SlashPairProbe(
                path="/a",
                bare=UrlProbe(url="https://example.com/a", http_status=200),
                slashed=UrlProbe(url="https://example.com/a/", http_status=200),
            )
        ],
    )
    restored = SiteProbe.from_dict(probe.to_dict())
    assert restored is not None and restored.to_dict() == probe.to_dict()

    # A probe captured before per-page evidence existed is still a valid probe.
    legacy = probe.to_dict()
    legacy.pop("page_http_variants")
    legacy.pop("slash_pairs")
    older = SiteProbe.from_dict(legacy)
    assert older is not None
    assert older.page_http_variants == [] and older.slash_pairs == []


@pytest.mark.asyncio
async def test_tls_capture_records_verified_certificate_evidence(monkeypatch):
    class FakeSslObject:
        def getpeercert(self):
            return {
                "issuer": ((("organizationName", "Example CA"),),),
                "notAfter": "Aug  9 00:00:00 2027 GMT",
            }

    class FakeWriter:
        def get_extra_info(self, name):
            assert name == "ssl_object"
            return FakeSslObject()

        def close(self):
            return None

        async def wait_closed(self):
            return None

    async def open_connection(*args, **kwargs):
        assert args == ("example.com", 443)
        assert kwargs["server_hostname"] == "example.com"
        return object(), FakeWriter()

    monkeypatch.setattr(sp.asyncio, "open_connection", open_connection)
    capture = await sp._capture_tls(ROOT)

    assert capture is not None
    assert (capture.trusted, capture.hostname_match, capture.expired) == (True, True, False)
    assert capture.issuer == "organizationName=Example CA"
    assert capture.not_after == "2027-08-09T00:00:00+00:00"
    assert capture.fetch_error is None


@pytest.mark.asyncio
async def test_tls_capture_failure_is_persisted_as_missing_evidence(monkeypatch):
    async def open_connection(*args, **kwargs):
        raise OSError("connection refused")

    monkeypatch.setattr(sp.asyncio, "open_connection", open_connection)
    capture = await sp._capture_tls(ROOT)

    assert capture is not None
    assert capture.trusted is None
    assert capture.fetch_error == "OSError: connection refused"
