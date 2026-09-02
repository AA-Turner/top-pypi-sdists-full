"""Anchor text survives link extraction.

`LinkExtractor.extract()` answers "which URLs does this page point at" and its
buckets are bare URL strings — a shape hosts persist and read, so it is frozen.
Anchor text (the strongest human-authored label a link carries, and
unrecoverable once the parse is discarded) rides alongside it in
`extract_anchors()` / `ScrapeResult.link_records`.
"""

from __future__ import annotations

from matrx_scraper.parser.core import ParserOrchestrator
from matrx_scraper.parser.link_extractor import (
    ANCHOR_RECORD_LIMIT,
    ANCHOR_TEXT_MAX_CHARS,
    LinkExtractor,
)

BASE = "https://example.com/blog/post"


def _records(html: str, base: str = BASE) -> list[dict]:
    return LinkExtractor(base_url=base).extract_anchors(html)


def _by_url(records: list[dict], url: str) -> list[dict]:
    return [r for r in records if r["target_url"] == url]


def test_anchor_text_is_captured_with_rel_type_and_region() -> None:
    html = """
    <html><body>
      <nav><a href="/pricing">Our Pricing</a></nav>
      <main><a href="https://other.test/x" rel="nofollow ugc">Best CRM tools</a></main>
      <footer><a href="https://docs.example.com/api">API docs</a></footer>
    </body></html>
    """
    records = _records(html)
    by_url = {r["target_url"]: r for r in records}

    internal = by_url["https://example.com/pricing"]
    assert internal["anchor_text"] == "Our Pricing"
    assert internal["text_source"] == "anchor"
    assert internal["link_type"] == "internal"
    assert internal["region"] == "nav"
    assert internal["nofollow"] is False
    assert internal["rel"] is None

    external = by_url["https://other.test/x"]
    assert external["anchor_text"] == "Best CRM tools"
    assert external["link_type"] == "external"
    assert external["region"] == "main"
    assert external["nofollow"] is True
    assert "ugc" in external["rel"]

    subdomain = by_url["https://docs.example.com/api"]
    assert subdomain["link_type"] == "subdomain"
    assert subdomain["region"] == "footer"


def test_whitespace_only_anchor_text_collapses_to_empty() -> None:
    html = '<a href="/a">   \n\t </a><a href="/b">  Spaced   out  label </a>'
    records = _records(html)

    empty = _by_url(records, "https://example.com/a")[0]
    assert empty["anchor_text"] == ""
    assert empty["text_source"] == ""

    # Internal whitespace collapses; the label is one clean line.
    spaced = _by_url(records, "https://example.com/b")[0]
    assert spaced["anchor_text"] == "Spaced out label"


def test_image_only_link_falls_back_to_alt_text_and_says_so() -> None:
    html = (
        '<a href="/product"><img src="/p.png" alt="  Blue Widget  "></a>'
        '<a href="/other"><img src="/o.png"></a>'
    )
    records = _records(html)

    with_alt = _by_url(records, "https://example.com/product")[0]
    assert with_alt["anchor_text"] == "Blue Widget"
    assert with_alt["text_source"] == "image_alt"

    # No text and no alt is a real state, not a reason to drop the link.
    without_alt = _by_url(records, "https://example.com/other")[0]
    assert without_alt["anchor_text"] == ""
    assert without_alt["text_source"] == ""


def test_same_url_with_different_anchor_text_is_kept_separately() -> None:
    html = """
      <nav><a href="/plans">Pricing</a></nav>
      <main><a href="/plans">see our plans</a></main>
      <footer><a href="/plans">Pricing</a></footer>
    """
    records = _by_url(_records(html), "https://example.com/plans")

    # The repeated nav/footer "Pricing" is ONE fact; the differing in-body
    # anchor is the signal and must survive.
    assert sorted(r["anchor_text"] for r in records) == ["Pricing", "see our plans"]
    assert [r["region"] for r in records if r["anchor_text"] == "Pricing"] == ["nav"]


def test_anchor_text_is_truncated_and_record_count_is_capped() -> None:
    long_text = "word " * 400
    html = f'<a href="/long">{long_text}</a>'
    assert len(_records(html)[0]["anchor_text"]) == ANCHOR_TEXT_MAX_CHARS

    many = "".join(f'<a href="/p{i}">label {i}</a>' for i in range(ANCHOR_RECORD_LIMIT + 50))
    assert len(_records(many)) == ANCHOR_RECORD_LIMIT


def test_non_http_and_fragment_hrefs_are_skipped() -> None:
    html = (
        '<a href="mailto:a@b.test">Mail us</a>'
        '<a href="javascript:void(0)">Menu</a>'
        '<a href="#section">Jump</a>'
        '<a href="/real">Real</a>'
    )
    records = _records(html)
    assert [r["target_url"] for r in records] == ["https://example.com/real"]


def test_url_buckets_are_unchanged_by_anchor_extraction() -> None:
    """The frozen contract: `extract()` still returns bucket -> list[str]."""
    html = (
        '<a href="/pricing">Our Pricing</a>'
        '<a href="https://other.test/x">Elsewhere</a>'
        '<img src="/big.png" width="400" height="400">'
    )
    buckets = LinkExtractor(base_url=BASE).extract(html)

    assert buckets["internal"] == ["https://example.com/pricing"]
    assert buckets["external"] == ["https://other.test/x"]
    assert all(isinstance(url, str) for urls in buckets.values() for url in urls), (
        "links buckets must stay bare URL strings — hosts persist this shape"
    )


def test_pipeline_surfaces_link_records_alongside_links() -> None:
    html = '<html><body><a href="/pricing">Our Pricing</a></body></html>'
    parsed = ParserOrchestrator().parse_content(html, BASE)

    assert parsed["links"]["internal"] == ["https://example.com/pricing"]
    assert parsed["link_records"][0]["anchor_text"] == "Our Pricing"


def test_fast_mode_skips_anchor_records_with_links() -> None:
    html = '<html><body><a href="/pricing">Our Pricing</a></body></html>'
    parsed = ParserOrchestrator().parse_content(html, BASE, skip_links=True)

    assert parsed["links"] == {}
    assert parsed["link_records"] == []
