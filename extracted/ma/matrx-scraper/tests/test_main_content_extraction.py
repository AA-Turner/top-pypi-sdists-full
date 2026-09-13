"""THE MAIN-CONTENT LAW: a page is not its article.

The break these tests catch: the parser hands a consumer the whole page — nav,
sponsor line, staff bios, tag list, donate and newsletter CTAs — as "what this
page says". On 2026-09-12 a Masterwork body-of-work lane distilled 20 saved
Marshall Project articles into 416 draft rules, a large share of which
described the SITE'S FURNITURE ("Sponsor disclosed on its own line", "Staff
bios in the first person, present tense", "Tag places first, then topics"),
because `page-capture` returned `text_data` — the entire rendered page.

The fixture is a real, unedited server-rendered page saved with curl
(`tests/__fixtures__/pages/marshall-project-article.html`). Every expected and
forbidden string below is a literal read off that page, chosen independently of
the extractor's code.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from matrx_scraper.parser.core import ParserOrchestrator

FIXTURE = Path(__file__).parent / "__fixtures__" / "pages" / "marshall-project-article.html"
URL = "https://www.themarshallproject.org/2026/08/29/police-crime-drop-cause-california"

# --- the writing: these MUST survive ---------------------------------------
ARTICLE_HEADLINE = "Why is Crime Falling? The Answers Aren’t"
ARTICLE_FIRST_PARAGRAPH = "In Memphis, Tennessee, violent crime is down"
ARTICLE_BODY_MIDDLE = "the decline is remarkably widespread"
ARTICLE_LAST_PARAGRAPH = "surrounded by police, claiming opponent James Talarico"

# --- the site's furniture: these MUST NOT ----------------------------------
FURNITURE = {
    "staff bio": "I report on criminal justice data and research",
    "staff bio role line": "Data Reporter",
    "donate solicitation": "become a member today",
    "tag list label": "Tags:",
    "tag list entry": "Criminal Justice Statistics",
    "impact rail": "Our reporting has real impact on the criminal justice system",
    "impact rail link": "View All Impact",
}


@pytest.fixture(scope="module")
def parsed() -> dict:
    return ParserOrchestrator().parse_content(FIXTURE.read_text(encoding="utf-8"), url=URL)


def _consumer_text(parsed: dict) -> str:
    """What a "what does this page say?" consumer actually receives.

    Exactly `page-capture`'s rule: the article body when there is one, else the
    full page. Asserting on THIS is what makes these tests falsifiable — with
    the main-content stage removed they fail on the full page rather than
    passing vacuously against an empty string.
    """
    return parsed["main_content_text"] or parsed["text_data"]


def test_fixture_is_the_real_page(parsed: dict) -> None:
    """Guard the guard: a fixture that lost the furniture proves nothing."""
    full = parsed["text_data"]
    assert ARTICLE_FIRST_PARAGRAPH in full
    for label, needle in FURNITURE.items():
        assert needle in full, f"fixture no longer carries the {label} — it cannot prove the fix"


def test_main_content_keeps_the_writing(parsed: dict) -> None:
    assert parsed["main_content_text"], "an article page produced no main content"
    main = _consumer_text(parsed)
    assert ARTICLE_HEADLINE in main
    assert ARTICLE_FIRST_PARAGRAPH in main
    assert ARTICLE_BODY_MIDDLE in main
    assert ARTICLE_LAST_PARAGRAPH in main


@pytest.mark.parametrize("label,needle", sorted(FURNITURE.items()))
def test_main_content_drops_the_furniture(parsed: dict, label: str, needle: str) -> None:
    assert needle not in _consumer_text(parsed), f"{label} leaked into the text a consumer reads"


def test_full_page_is_still_available(parsed: dict) -> None:
    """Main content never destroys the page — SEO/archival callers need it."""
    assert FURNITURE["staff bio"] in parsed["text_data"]
    assert parsed["main_content_selector"] == "article"


def test_non_article_page_keeps_the_full_page() -> None:
    """A listing/app page is not an article — no half page called one."""
    cards = "".join(
        f"<article><h2>Story {i}</h2><p>{f'Teaser copy for story {i}. ' * 12}</p></article>"
        for i in range(6)
    )
    html = f"<html><body><nav>Home About</nav><div class='grid'>{cards}</div></body></html>"
    result = ParserOrchestrator().parse_content(html, url="https://example.test/")
    assert not result["main_content_text"]
    assert result["main_content_selector"] is None
    assert "Teaser copy for story 0" in result["text_data"]


def test_wiki_shaped_page_drops_the_reference_apparatus() -> None:
    """The trial-3 symptom: a wiki page arrived as 210k chars of prose plus
    references, navboxes and category links. The root here IS the body once nav
    is gone, so declining on "root ≈ body" would have kept all of it."""
    prose = "".join(f"<p>{'Real encyclopedia prose about the subject. ' * 8}</p>" for _ in range(4))
    html = (
        "<html><body><main id='content'>"
        "<h1>Deliberate practice</h1>"
        "<div class='hatnote'>For other uses, see Practice (disambiguation).</div>"
        f"{prose}"
        "<div class='mw-references-wrap'><ol><li>Ericsson, Anders (1993). Cited work.</li></ol></div>"
        "<div class='navbox'>Learning · Skill acquisition · Expertise</div>"
        "<div id='catlinks'>Categories: Learning | Skill | Educational psychology</div>"
        "</main></body></html>"
    )
    result = ParserOrchestrator().parse_content(html, url="https://en.wikipedia.test/wiki/X")
    main = result["main_content_text"]
    assert "Real encyclopedia prose about the subject." in main
    assert "Ericsson, Anders (1993)" not in main
    assert "Skill acquisition" not in main
    assert "Educational psychology" not in main
    assert "For other uses" not in main


def test_a_furniture_marker_never_eats_the_article() -> None:
    """The failure mode of every marker list: a wrapper whose class happens to
    match takes the story with it. An element carrying most of the root's text
    is the body, whatever it is called. Asserted on the finder itself — the
    pipeline's earlier noise passes would remove this wrapper before it ever
    reached stage 3b, which would prove nothing about this guard."""
    from bs4 import BeautifulSoup

    from matrx_scraper.parser.main_content import ArticleContentFinder

    body = "<p>" + ("The whole story lives inside this wrapper. " * 40) + "</p>"
    soup = BeautifulSoup(
        f"<html><body><article><h1>Story</h1><div class='promo-wrapper'>{body}</div>"
        "<div class='promo-rail'>Buy our stuff</div></article></body></html>",
        "lxml",
    )
    found = ArticleContentFinder().find(soup)
    assert found is not None
    text = found.get_text(" ", strip=True)
    assert "The whole story lives inside this wrapper." in text
    assert "Buy our stuff" not in text
