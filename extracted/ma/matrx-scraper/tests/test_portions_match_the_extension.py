"""The server's portioner and the extension's cut the same page into the same sections.

``tests/fixtures/portions/*.json`` are three real pages (example.com, the Wikipedia HTTP article,
python.org with tracking parameters), each with its HTML-path and markdown-path sections as the
extension's ``portions.ts`` produces them (measured 2026-09-25: 0 differing portions of 92 against
the extension's own code under happy-dom; 86 differed before the port). matrx-extend pins its tests
to the same files, so either side drifting turns one of the two suites red.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from matrx_scraper.canonical import canonical_url
from matrx_scraper.portions import from_article_html, from_markdown

FIXTURES = sorted((Path(__file__).parent / "fixtures" / "portions").glob("*.json"))


def test_the_three_pages_are_pinned() -> None:
    assert {p.stem for p in FIXTURES} == {"example_com", "wikipedia_http", "python_org_tracking"}


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda p: p.stem)
def test_server_sections_equal_the_pinned_extension_sections(fixture: Path) -> None:
    fx = json.loads(fixture.read_text(encoding="utf-8"))
    assert from_article_html(fx["html"]) == fx["html_portions"]
    assert from_markdown(fx["markdown"]) == fx["markdown_portions"]
    assert canonical_url(fx["url"]) == fx["canonical_url"]


def test_heading_path_is_by_level_and_inline_markup_adds_no_space() -> None:
    """The two defects the fixtures caught, stated small."""
    html = "<h2>Versions</h2><p>a</p><h2>Use</h2><p>HTTP (<b>Hypertext</b> Transfer)</p>"
    ps = from_article_html(html)
    assert [p["locator"]["heading_path"] for p in ps] == [["Versions"], ["Use"]]
    assert "HTTP (Hypertext Transfer)" in ps[1]["text"]
    md = from_markdown("## Versions\na\n## Use\nb")
    assert [p["locator"]["heading_path"] for p in md] == [["Versions"], ["Use"]]
