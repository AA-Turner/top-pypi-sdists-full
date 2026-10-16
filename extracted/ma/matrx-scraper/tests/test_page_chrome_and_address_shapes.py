"""MKT-086 / MKT-087: addresses are real address shapes only; site text carries no nav/menu/cart/toggle chrome."""

from __future__ import annotations

import pytest

from matrx_scraper.clean_content import clean_page_content, contact_footer_text, looks_like_address, strip_chrome_text
from matrx_scraper.events import PageSummary
from matrx_scraper.web_crawl.candidates import extract_homepage_candidates

DIRECTIONS = "Head east on 541 West for 12 miles. Take County Road"


@pytest.mark.parametrize("text", [
    DIRECTIONS,
    "541 West for 12 miles. Take County Road 12 to our door",
    "In 2020 We Opened On Main Street",
    "Take exit 12 and follow 4 miles to Old Mill Road",
    "Turn left onto 300 yards past the Church Road",
])
def test_sentences_are_not_addresses(text):
    assert not looks_like_address(text)


@pytest.mark.parametrize("text", [
    "7400 Center Ave, Huntington Beach, CA 92647",
    "123 Main Street",
    "1600 N. Pennsylvania Avenue NW",
    "55 West 5th St, Suite 200",
    "PO Box 4412",
    "Taos, NM 87571",
])
def test_real_shapes_stay_addresses(text):
    assert looks_like_address(text)


CHROME_BARE = """<html><body><span>0</span> <span>0</span> <div>Open Menu</div><div>Close Menu</div>
<div>Cart (0)</div><p>Hand thrown pottery made in a small studio, sold as mugs, bowls and vases.</p></body></html>"""

CHROME_CLASSED = """<html><body><header><div class="header-menu-toggle">Open Menu Close Menu</div>
<a class="cart-link">0</a></header><div class="content"><p>Hand made pottery from Taos.</p></div></body></html>"""


@pytest.mark.parametrize("html", [CHROME_BARE, CHROME_CLASSED])
def test_clean_page_content_has_no_chrome(html):
    out = clean_page_content(html, "https://x.example/")
    assert "pottery" in out
    for junk in ("Open Menu", "Close Menu", "Cart (0)"):
        assert junk not in out
    assert not any(line.strip() in ("0", "") and line for line in out.splitlines())


def test_dump_line_is_stripped():
    assert strip_chrome_text("· 0 · 0 · Open Menu Close Menu ·") == ""
    assert strip_chrome_text("About\n· 0 · 0 · Open Menu Close Menu ·\nWe make pots.") == "About\nWe make pots."
    assert strip_chrome_text("Open since 1998\n24 hours a day") == "Open since 1998\n24 hours a day"


def test_footer_with_chrome_keeps_contact_only():
    html = "<footer>Open Menu\n<p>Call 415-555-0100</p><div>Cart (0)</div></footer>"
    foot = contact_footer_text(html)
    assert foot and "415-555-0100" in foot and "Menu" not in foot and "Cart" not in foot


def test_direction_text_yields_no_address_candidate():
    html = f"<html><body><p>{DIRECTIONS} to find us. Call 415-555-0100.</p><p>Visit 7400 Center Ave today.</p></body></html>"
    summary = PageSummary(url="https://a.example/", final_url="https://a.example/", title="A", meta_description="",
                          og_tags={}, twitter_tags={}, schema_org={"@type": "Organization", "address": "Take County Road"}, links=[])
    found = [c for c in extract_homepage_candidates(html, base_url="https://a.example/", summary=summary)
             if c.guessed_kind == "address"]
    texts = [str(c.value.get("text") or c.value.get("address")) for c in found]
    assert texts == ["7400 Center Ave"], texts


def test_phone_tail_fused_with_label_is_not_part_of_the_address():
    from matrx_scraper.clean_content import street_addresses_in
    text = "Call (208) 555-6340 Address 2621 W Camas St Boise, ID"
    assert [m.group(0) for m in street_addresses_in(text)] == ["2621 W Camas St"]
    text = "6340 Address 2621 W Camas St"
    assert [m.group(0) for m in street_addresses_in(text)] == ["2621 W Camas St"]
    html = f"<html><body><p>{text}</p></body></html>"
    summary = PageSummary(url="https://a.example/", final_url="https://a.example/", title="A", meta_description="",
                          og_tags={}, twitter_tags={}, schema_org={}, links=[])
    found = [str(c.value.get("text")) for c in extract_homepage_candidates(html, base_url="https://a.example/", summary=summary)
             if c.guessed_kind == "address"]
    assert found == ["2621 W Camas St"], found
