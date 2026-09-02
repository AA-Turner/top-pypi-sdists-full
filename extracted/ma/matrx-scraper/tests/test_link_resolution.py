"""Pure-part tests for link-target reconciliation."""

from __future__ import annotations

from matrx_scraper.crawler import _normalise_url
from matrx_scraper.web_crawl.contracts import LinkResolutionSummary
from matrx_scraper.web_crawl.link_resolution import match_edges_to_pages
from matrx_scraper.web_crawl.persistence import url_hash


def _hash(url: str) -> str:
    return url_hash(_normalise_url(url))


def test_match_edges_to_pages_resolves_normalized_variants() -> None:
    pages = {
        _hash("https://example.com/a"): "page-a",
        _hash("https://example.com/b"): "page-b",
    }
    edges = {
        "edge-1": "https://example.com/a",
        "edge-2": "https://example.com/a/",  # trailing slash normalizes to /a
        "edge-3": "https://example.com/a#section",  # fragment dropped
        "edge-4": "https://example.com/b",
        "edge-5": "https://example.com/missing",
    }
    resolutions, unresolved = match_edges_to_pages(edges, pages)
    assert resolutions == {
        "edge-1": "page-a",
        "edge-2": "page-a",
        "edge-3": "page-a",
        "edge-4": "page-b",
    }
    assert unresolved == 1


def test_match_edges_to_pages_empty_registry_leaves_all_unresolved() -> None:
    resolutions, unresolved = match_edges_to_pages({"edge-1": "https://example.com/a"}, {})
    assert resolutions == {}
    assert unresolved == 1


def test_link_resolution_summary_shape() -> None:
    assert LinkResolutionSummary().model_dump(mode="json") == {
        "scanned": 0,
        "resolved": 0,
        "unresolved": 0,
    }
