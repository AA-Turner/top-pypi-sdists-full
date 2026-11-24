"""selectolax 1.0 removed the Modest backend; the audit now parses with Lexbor (``LexborHTMLParser``).

``fixtures/seo_audit_lexbor_page.expected.json`` is ``dataclasses.asdict(audit_html(page))`` recorded by the
PRE-migration code on selectolax 0.4.12 (Modest). The migrated code must produce the identical audit: meta tags,
canonical, hreflang, og:, links with rel/href, img alt (absent / empty / present), an SVG ``<use xlink:href>``.
"""

from __future__ import annotations

import dataclasses
import json
from pathlib import Path

from matrx_scraper.seo_audit import audit_html

FIXTURES = Path(__file__).parent / "fixtures"
BASE = "https://www.acme.test/"


def _audit(html: str | None = None) -> dict:
    html = html if html is not None else (FIXTURES / "seo_audit_lexbor_page.html").read_text(encoding="utf-8")
    return json.loads(json.dumps(dataclasses.asdict(audit_html(html, BASE)), default=str))


def test_audit_of_a_real_looking_page_matches_the_modest_era_answer() -> None:
    expected = json.loads((FIXTURES / "seo_audit_lexbor_page.expected.json").read_text(encoding="utf-8"))
    assert _audit() == expected


def test_the_headline_fields_are_what_the_page_says() -> None:
    got = _audit()
    assert got["canonical"] == "https://www.acme.test/"
    assert got["lang"] == "en-US"
    assert got["og"]["og:title"].startswith("Acme Widgets")
    assert {h["lang"] for h in got["hreflang"]} == {"en-us", "de", "x-default"}
    assert [i["alt"] for i in got["image_inventory"]][:3] == ["A blue widget on a bench", "", None]


def test_present_but_empty_attributes_read_as_the_old_parser_did() -> None:
    # Lexbor reports lang="" as "" where Modest said None; the audit keeps "absent".
    assert _audit('<html lang=""><head><title>t</title></head><body><p>x</p></body></html>')["lang"] is None
    assert _audit('<html><body><p>x</p></body></html>')["lang"] is None
