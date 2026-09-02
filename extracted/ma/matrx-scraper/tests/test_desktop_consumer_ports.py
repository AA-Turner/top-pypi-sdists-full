"""Behaviours ported in from the matrx-local scraper-service fork (2026-08-09).

matrx-local ran a forked COPY of this engine so it could scrape from the user's
own machine and residential IP. The fork is deleted; the local EXECUTION lane
stays and now consumes this package. Each test below pins one behaviour the
fork had that this package did not — without them the fork's deletion is a
silent feature loss, and the next refactor has nothing telling it these cases
matter.
"""

from __future__ import annotations

import logging

import pytest

from matrx_scraper.parser.core import ParserOrchestrator
from matrx_scraper.parser.link_extractor import LinkExtractor, _determine_filetype
from matrx_scraper.scrape_options import ScrapeOptions, apply_field_flags
from matrx_scraper.search import extract_urls_from_search_results
from matrx_scraper.search.brave_client import BraveSearchClient, configure_client


# ---------------------------------------------------------------------------
# Brave key injection — a desktop host holds the key OUTSIDE the environment
# ---------------------------------------------------------------------------


_RETIRED_KEYS = ("BRAVE_SEARCH_API_KEY", "BRAVE_API_KEY", "BRAVE_SEARCH_API_KEY_AI")
_ALL_KEYS = (*_RETIRED_KEYS, "BRAVE_SEARCH_API_KEY_PRO_AI")


def test_brave_client_accepts_injected_key_with_no_env(monkeypatch):
    """The user-supplied-key path. A desktop host — and every future
    bring-your-own-key surface — hands the key in directly, and it is used
    exactly as given with no environment consulted."""
    for var in _ALL_KEYS:
        monkeypatch.delenv(var, raising=False)

    assert BraveSearchClient(api_key="user-store-key")._api_key == "user-store-key"


def test_brave_client_without_any_key_still_raises(monkeypatch):
    for var in _ALL_KEYS:
        monkeypatch.delenv(var, raising=False)

    with pytest.raises(ValueError, match="No Brave API key"):
        BraveSearchClient()


def test_the_env_key_is_used_when_nothing_is_injected(monkeypatch):
    for var in _RETIRED_KEYS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("BRAVE_SEARCH_API_KEY_PRO_AI", "env-key")

    assert BraveSearchClient()._api_key == "env-key"


@pytest.mark.parametrize("retired", _RETIRED_KEYS)
def test_retired_key_names_are_not_read_at_all(monkeypatch, retired):
    """🚨 The whole point of the 2026-08-20 ruling.

    A retired key does not FAIL — it succeeds with less: no faq / discussions /
    infobox / locations / summarizer section, no extra_snippets, no reach into
    place_search or the summarizer endpoint, and 1 req/sec instead of 50. A
    payload from one looks exactly like a query that happened to have none of
    those things. So the engine must refuse to start rather than quietly fall
    back — a loud failure is the only kind anyone notices.
    """
    for var in _ALL_KEYS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv(retired, "degraded-key")

    with pytest.raises(ValueError, match="No Brave API key"):
        BraveSearchClient()


def test_configure_client_replaces_and_clears_the_process_client(monkeypatch):
    for var in _ALL_KEYS:
        monkeypatch.delenv(var, raising=False)

    first = configure_client("key-one")
    assert first is not None and first._api_key == "key-one"

    second = configure_client("key-two")
    assert second is not first
    assert second._api_key == "key-two"

    # The user deleted their key: clearing must not leave the old one live.
    assert configure_client(None) is None
    from matrx_scraper.search import brave_client

    assert brave_client._client is None


# ---------------------------------------------------------------------------
# Search → scrape hand-off
# ---------------------------------------------------------------------------


def test_extract_urls_dedupes_across_queries_and_keeps_rank_order():
    results = [
        (
            "q1",
            {
                "web": {
                    "results": [
                        {"url": "https://a.test/1", "title": "A", "description": "da"},
                        {"url": "https://b.test/2", "title": "B", "description": "db"},
                    ]
                }
            },
        ),
        (
            "q2",
            {
                "web": {
                    "results": [
                        {"url": "https://b.test/2", "title": "B again", "description": ""},
                        {"url": "https://c.test/3", "title": "C", "description": "dc"},
                    ]
                }
            },
        ),
        ("q3", None),
    ]

    urls = extract_urls_from_search_results(results)

    assert [u["url"] for u in urls] == [
        "https://a.test/1",
        "https://b.test/2",
        "https://c.test/3",
    ]
    assert urls[1]["title"] == "B"  # first occurrence wins, not the later one
    assert urls[0]["description"] == "da"


def test_extract_urls_tolerates_empty_and_malformed_payloads():
    assert extract_urls_from_search_results([]) == []
    assert extract_urls_from_search_results([("q", {})]) == []
    assert extract_urls_from_search_results([("q", {"web": {"results": [{}]}})]) == []


# ---------------------------------------------------------------------------
# main_image — raw <meta> fallbacks (extruct is an OPTIONAL extra)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "meta_name,attr",
    [
        ("og:image", "property"),
        ("twitter:image", "name"),
        ("image", "name"),
        ("thumbnail", "name"),
        ("msapplication-TileImage", "name"),
    ],
)
def test_main_image_resolves_from_each_meta_tag_without_extruct(meta_name, attr):
    html = f"""
        <html><head>
          <title>t</title>
          <meta {attr}="{meta_name}" content="https://img.test/hero.png">
        </head><body><p>{"body text " * 40}</p></body></html>
    """

    parsed = ParserOrchestrator().parse_content(html, url="https://example.test/page")

    assert parsed["main_image"] == "https://img.test/hero.png"


def test_main_image_prefers_og_over_the_long_tail_tags():
    html = """
        <html><head><title>t</title>
          <meta property="og:image" content="https://img.test/og.png">
          <meta name="thumbnail" content="https://img.test/thumb.png">
          <meta name="msapplication-TileImage" content="https://img.test/tile.png">
        </head><body><p>text</p></body></html>
    """

    parsed = ParserOrchestrator().parse_content(html, url="https://example.test/page")

    assert parsed["main_image"] == "https://img.test/og.png"


def test_main_image_is_none_when_no_tag_carries_one():
    html = "<html><head><title>t</title></head><body><p>text</p></body></html>"

    parsed = ParserOrchestrator().parse_content(html, url="https://example.test/page")

    assert parsed["main_image"] is None


# ---------------------------------------------------------------------------
# Link classification — extensions that fell through to "others"
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://x.test/scan.bmp", "image"),
        ("https://x.test/scan.tiff", "image"),
        ("https://x.test/scan.tif", "image"),
        ("https://x.test/archive.tar.xz", "archive"),
        ("https://x.test/photo.jpg", "image"),
        ("https://x.test/page", None),
    ],
)
def test_media_extensions_classify(url, expected):
    assert _determine_filetype(url) == expected


# ---------------------------------------------------------------------------
# Archives are their OWN category — the "archives" bucket must actually fill.
# Until v0.1.104 the document branch also tested the archive list and returned
# first, so every archive link landed in "documents" and the archive branch was
# unreachable: crawler.py's ("archives", "archive") resource mapping and the
# published PageLinks.archives field were permanently empty.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://x.test/a.zip", "archive"),
        ("https://x.test/a.tar.gz", "archive"),
        ("https://x.test/a.xz", "archive"),
        ("https://x.test/a.rar", "archive"),
        ("https://x.test/a.7z", "archive"),
        ("https://x.test/a.dmg", "archive"),
        ("https://x.test/a.pdf", "document"),
        ("https://x.test/a.docx", "document"),
    ],
)
def test_archives_are_not_classified_as_documents(url, expected):
    assert _determine_filetype(url) == expected


def test_extract_fills_the_archives_bucket_separately_from_documents():
    html = (
        "<html><body>"
        '<a href="https://x.test/release.zip">zip</a>'
        '<a href="https://x.test/release.tar.gz">tgz</a>'
        '<a href="https://x.test/manual.pdf">pdf</a>'
        "</body></html>"
    )

    links = LinkExtractor("https://x.test/").extract(html)

    assert links["archives"] == [
        "https://x.test/release.tar.gz",
        "https://x.test/release.zip",
    ]
    assert links["documents"] == ["https://x.test/manual.pdf"]


# ---------------------------------------------------------------------------
# Field flags — the shape is defined ONCE, importable without matrx-orm
# ---------------------------------------------------------------------------


def test_apply_field_flags_drops_only_unrequested_fields():
    page = {
        "url": "https://x.test",
        "text_data": "body",
        "links": {"internal": []},
        "overview": {"page_title": "t"},
        "main_image": "https://x.test/i.png",
        "organized_data": object(),
        "structured_data": {},
        "content_filter_removal_details": [],
        "noise_remover_removal_details": [],
    }

    kept = apply_field_flags(page, ScrapeOptions(get_text_data=True, get_links=True))

    assert set(kept) == {"url", "text_data", "links"}


def test_scrape_options_import_needs_no_db_or_connect_stack():
    """Importing the options shape must not drag in matrx-orm / matrx-connect."""
    import subprocess
    import sys

    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys\n"
            "import matrx_scraper.scrape_options as m\n"
            "assert m.ScrapeOptions().get_text_data is True\n"
            "bad = [n for n in sys.modules if n.startswith(('matrx_orm', 'matrx_connect'))]\n"
            "assert not bad, bad\n",
        ],
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 0, proc.stderr


# ---------------------------------------------------------------------------
# Browser pool — a clean shutdown must not report a false incident
# ---------------------------------------------------------------------------


class _DeadDriverBrowser:
    def __init__(self, message: str) -> None:
        self._message = message

    async def close(self) -> None:
        raise RuntimeError(self._message)


@pytest.mark.asyncio
async def test_driver_already_closed_is_debug_not_an_exception(caplog):
    from matrx_scraper.browser_pool import DRIVER_ALREADY_CLOSED, PlaywrightBrowserPool

    pool = PlaywrightBrowserPool.__new__(PlaywrightBrowserPool)
    pool._browsers = [_DeadDriverBrowser(f"Error: {DRIVER_ALREADY_CLOSED}")]
    pool._playwright = None

    with caplog.at_level(logging.DEBUG, logger="matrx_scraper.browser_pool"):
        await pool.stop()

    assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert any("already closed" in r.message for r in caplog.records)


@pytest.mark.asyncio
async def test_any_other_close_failure_still_screams(caplog):
    from matrx_scraper.browser_pool import PlaywrightBrowserPool

    pool = PlaywrightBrowserPool.__new__(PlaywrightBrowserPool)
    pool._browsers = [_DeadDriverBrowser("Target page crashed")]
    pool._playwright = None

    with caplog.at_level(logging.DEBUG, logger="matrx_scraper.browser_pool"):
        await pool.stop()

    assert [r for r in caplog.records if r.levelno >= logging.ERROR]


# ---------------------------------------------------------------------------
# text_data must not be empty on a page that clearly has text
# ---------------------------------------------------------------------------


def test_html_result_reports_its_text(monkeypatch):
    """A successful HTML scrape reporting zero text is a poisoned result.

    `parse_content`'s `_build_text_data` used to pass the OrganizedData OBJECT
    to `json_to_text_lines`, which only walked dicts/lists — so it returned ""
    for every page. Rendering now lives on `OrganizedData.to_text()`; this pins
    the end of the chain, `ScrapeResult.text_data`.
    """
    from matrx_scraper.orchestrator import _build_result_from_response
    from matrx_scraper.scraper import ContentType, RequestType, Response

    html = (
        "<html><head><title>T</title></head><body>"
        "<h1>Hello</h1><p>Some real body text here for the parser.</p>"
        "<ul><li>a</li><li>b</li></ul></body></html>"
    )
    response = Response(
        request_url="https://example.test/x",
        proxy_used=False,
        request_type=RequestType.NORMAL,
        content_type=ContentType.HTML,
        extension="",
        content_type_raw="text/html",
        response_url="https://example.test/x",
        response_headers={},
        title="T",
        status_code=200,
        content=html,
    )

    result = _build_result_from_response(response)

    assert result.success
    assert result.text_data, "HTML result reported no text at all"
    assert "Some real body text" in result.text_data
