"""The markdown-variant probe, on fake fetches (no network)."""

from __future__ import annotations

import pytest

from matrx_scraper import markdown_variant as mv
from matrx_scraper.markdown_variant import ProbeResponse

PAGE = "https://docs.example.org/guide/install"
PAGE_TEXT = (
    "Install the toolkit with the package manager then configure credentials "
    "and verify the installation completes successfully before continuing"
)
MD = (
    "# Install\n\nInstall the toolkit with the package manager, then configure "
    "credentials and verify the installation completes successfully.\n\n"
    "- step one\n- step two\n\n```sh\nrun install\n```\n"
)
NOT_FOUND_HTML = "<!doctype html><html><body>404 Page not found " + "x" * 200 + "</body></html>"


class FakeSite:
    """Answers by URL; records every request so budgets can be asserted."""

    def __init__(self, routes: dict[str, ProbeResponse]) -> None:
        self.routes = routes
        self.calls: list[tuple[str, bool]] = []

    async def __call__(self, url: str, accept_markdown: bool) -> ProbeResponse | None:
        self.calls.append((url, accept_markdown))
        return self.routes.get(url, ProbeResponse(404, "text/html", NOT_FOUND_HTML, url))


def md_ok(url: str, ctype: str = "text/markdown; charset=utf-8") -> ProbeResponse:
    return ProbeResponse(200, ctype, MD, url)


@pytest.fixture(autouse=True)
def _clean_cache() -> None:
    mv.reset_host_cache()


def page_calls(site: FakeSite) -> list[str]:
    return [u for u, _ in site.calls if "llms" not in u]


@pytest.mark.asyncio
async def test_link_alternate_is_found_and_fetched() -> None:
    html = (
        '<html><head><link rel="alternate" type="text/markdown" '
        'href="/guide/install.md"></head><body>x</body></html>'
    )
    site = FakeSite(
        {
            "https://docs.example.org/guide/install.md": md_ok(
                "https://docs.example.org/guide/install.md"
            )
        }
    )
    out = await mv.probe_markdown_variant(PAGE, html=html, page_text=PAGE_TEXT, fetcher=site)
    assert out.variant is not None
    assert out.variant.signal == mv.SIGNAL_LINK
    assert page_calls(site) == ["https://docs.example.org/guide/install.md"]


def test_link_alternate_ignores_other_alternates() -> None:
    html = '<head><link rel="alternate" hreflang="en" href="/en"><link rel="alternate" type="application/rss+xml" href="/feed"></head>'
    assert mv.find_link_alternate(html, PAGE) is None
    html2 = '<head><link type="application/markdown" rel="alternate" href="x.md"></head>'
    assert mv.find_link_alternate(html2, PAGE) == "https://docs.example.org/guide/x.md"


@pytest.mark.asyncio
async def test_sibling_md_found_when_markdown() -> None:
    site = FakeSite({PAGE + ".md": md_ok(PAGE + ".md")})
    out = await mv.probe_markdown_variant(
        PAGE, html="<html></html>", page_text=PAGE_TEXT, fetcher=site
    )
    assert out.variant is not None and out.variant.signal == mv.SIGNAL_SIBLING


@pytest.mark.asyncio
async def test_sibling_that_is_an_error_page_or_html_is_refused() -> None:
    # 404 page served as 200 (soft 404) with an html content type, and a
    # plain-text "not found" note: neither is accepted.
    site = FakeSite(
        {
            PAGE + ".md": ProbeResponse(200, "text/html", NOT_FOUND_HTML, PAGE + ".md"),
            PAGE + ".md.txt": ProbeResponse(
                200, "text/plain", "404 not found " * 10, PAGE + ".md.txt"
            ),
        }
    )
    out = await mv.probe_markdown_variant(
        PAGE, html="<html></html>", page_text=PAGE_TEXT, fetcher=site
    )
    assert out.variant is None


@pytest.mark.asyncio
async def test_markdown_of_a_different_page_is_refused() -> None:
    other = "# Billing\n\n- invoices payments refunds subscriptions\n\n[link](http://a.b)\n" * 4
    site = FakeSite({PAGE + ".md": ProbeResponse(200, "text/markdown", other, PAGE + ".md")})
    out = await mv.probe_markdown_variant(
        PAGE, html="<html></html>", page_text=PAGE_TEXT, fetcher=site
    )
    assert out.variant is None


@pytest.mark.asyncio
async def test_md_txt_spelling_and_content_negotiation() -> None:
    site = FakeSite({PAGE + ".md.txt": md_ok(PAGE + ".md.txt")})
    out = await mv.probe_markdown_variant(PAGE, html=None, page_text=PAGE_TEXT, fetcher=site)
    assert out.variant is not None and out.variant.signal == mv.SIGNAL_SIBLING_TXT

    mv.reset_host_cache()
    site = FakeSite({PAGE: md_ok(PAGE)})
    out = await mv.probe_markdown_variant(PAGE, html=None, page_text=PAGE_TEXT, fetcher=site)
    assert out.variant is not None and out.variant.signal == mv.SIGNAL_NEGOTIATION
    assert (PAGE, True) in site.calls


@pytest.mark.asyncio
async def test_negotiation_returning_html_is_not_a_markdown_variant() -> None:
    site = FakeSite({PAGE: ProbeResponse(200, "text/html", "<html>" + PAGE_TEXT + "</html>", PAGE)})
    out = await mv.probe_markdown_variant(PAGE, html=None, page_text=PAGE_TEXT, fetcher=site)
    assert out.variant is None


@pytest.mark.asyncio
async def test_llms_txt_is_probed_once_per_host() -> None:
    llms = ProbeResponse(
        200, "text/plain", "# Site\n\n> docs index\n\n- [a](https://x.y/a): " + "z" * 100, ""
    )
    site = FakeSite({"https://docs.example.org/llms.txt": llms})
    first = await mv.probe_markdown_variant(
        PAGE, html="<html></html>", page_text=PAGE_TEXT, fetcher=site
    )
    assert first.site_index and first.site_index.llms_txt_url == "https://docs.example.org/llms.txt"
    second = await mv.probe_markdown_variant(
        "https://docs.example.org/guide/other",
        html="<html></html>",
        page_text=PAGE_TEXT,
        fetcher=site,
    )
    assert second.site_index and second.site_index.llms_txt_url
    llms_calls = [u for u, _ in site.calls if "llms" in u]
    assert llms_calls.count("https://docs.example.org/llms.txt") == 1


@pytest.mark.asyncio
async def test_negative_host_is_not_reprobed() -> None:
    site = FakeSite({})
    first = await mv.probe_markdown_variant(
        PAGE, html="<html></html>", page_text=PAGE_TEXT, fetcher=site
    )
    assert first.variant is None
    assert 1 <= first.requests_made <= mv.MAX_EXTRA_REQUESTS_FIRST_CONTACT
    before = len(site.calls)
    second = await mv.probe_markdown_variant(
        "https://docs.example.org/guide/other",
        html="<html></html>",
        page_text=PAGE_TEXT,
        fetcher=site,
    )
    assert second.variant is None and second.requests_made == 0
    assert len(site.calls) == before  # not even llms.txt again


@pytest.mark.asyncio
async def test_request_budget_is_bounded() -> None:
    site = FakeSite({})
    html = '<head><link rel="alternate" type="text/markdown" href="/a.md"></head>'
    out = await mv.probe_markdown_variant(PAGE, html=html, page_text=PAGE_TEXT, fetcher=site)
    assert out.requests_made <= mv.MAX_EXTRA_REQUESTS_FIRST_CONTACT


@pytest.mark.asyncio
async def test_repo_page_maps_to_raw_readme() -> None:
    assert (
        mv.raw_source_url("https://github.com/o/r")
        == "https://raw.githubusercontent.com/o/r/HEAD/README.md"
    )
    assert mv.raw_source_url("https://example.org/o/r") is None


class FakeResult:
    def __init__(self) -> None:
        self.url = self.response_url = PAGE
        self.success = True
        self.content_type = "html"
        self.raw_html = "<html><body>hi</body></html>"
        self.main_content_text = PAGE_TEXT
        self.text_data = PAGE_TEXT
        self.markdown_renderable = PAGE_TEXT
        self.markdown = self.markdown_url = self.markdown_source = self.markdown_note = None
        self.site_index = None


@pytest.mark.asyncio
async def test_knob_off_means_no_probe_at_all() -> None:
    site = FakeSite({PAGE + ".md": md_ok(PAGE + ".md")})
    result = FakeResult()
    await mv.attach_markdown_variant(result, fetcher=site, enabled=False)
    assert site.calls == [] and result.markdown is None


@pytest.mark.asyncio
async def test_knob_read_through_the_host_ext() -> None:
    from matrx_scraper._ext import _registry, configure_ext

    seen: list[str | None] = []

    async def off(org: str | None) -> bool:
        seen.append(org)
        return False

    configure_ext(prefer_markdown_variant=off)
    try:
        site = FakeSite({PAGE + ".md": md_ok(PAGE + ".md")})
        result = FakeResult()
        await mv.attach_markdown_variant(result, organization_id="org-1", fetcher=site)
        assert seen == ["org-1"] and site.calls == [] and result.markdown is None
    finally:
        _registry.pop("prefer_markdown_variant", None)


@pytest.mark.asyncio
async def test_attach_adds_markdown_and_keeps_html_fields() -> None:
    site = FakeSite({PAGE + ".md": md_ok(PAGE + ".md")})
    result = FakeResult()
    await mv.attach_markdown_variant(result, fetcher=site, enabled=True)
    assert result.markdown == MD
    assert result.markdown_source == mv.SIGNAL_SIBLING
    assert "markdown" in (result.markdown_note or "")
    assert result.raw_html and result.main_content_text == PAGE_TEXT


@pytest.mark.asyncio
async def test_failed_html_read_is_rescued_by_explicit_markdown() -> None:
    site = FakeSite({PAGE + ".md": md_ok(PAGE + ".md")})
    result = FakeResult()
    result.success = False
    result.raw_html = None
    result.main_content_text = result.text_data = result.markdown_renderable = None
    for name in (
        "failure_reason",
        "failure_message",
        "next_rung",
        "next_rung_reason",
        "next_rung_note",
        "next_rung_what_to_do",
        "next_rung_estimated_seconds",
        "stopped_because",
        "content_chars",
    ):
        setattr(result, name, "x")
    await mv.attach_markdown_variant(result, fetcher=site, enabled=True)
    assert result.success is True and result.text_data == MD and result.failure_reason is None
