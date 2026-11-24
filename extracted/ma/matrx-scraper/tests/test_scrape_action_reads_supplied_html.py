"""``scraper.scrape`` given ``html`` reads that capture with the scraper's own parse and fetches nothing.

A browser capture (the extension's page check) is already in hand; a workflow must get exactly what the code's page
check gets from it (``research.multisource.process_extension_content``: ``parse_html`` -> content =
``ai_research_with_images`` else ``ai_research_content``; links and images through ``page_records``) — in one step, by an argument on the
one scraper Action, never a parser rebuilt in workflow steps (Arman, 2026-11-16).

WHAT BREAKS IT: a fetch when html is given, a second parser, the stored content differing from the parse's
``ai_research_with_images``, or empty HTML reading as a good page.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from matrx_graph.actions import run_as_step
from matrx_graph.types.result import Success

from matrx_scraper import site_rules
from matrx_scraper.graph_nodes import scrape_actions
from matrx_scraper.graph_nodes.scrape_actions import ScrapeInput

URL = "https://news.example/tea"
HTML = (
    "<html><head><title>Green tea</title></head><body><nav>Home | Shop</nav><article>"
    "<h1>Green tea</h1><p>Green tea is steamed within hours of picking, which keeps it green.</p>"
    "<p>Shaded leaves make matcha.</p><img src='https://news.example/leaf.jpg' alt='A leaf' width='640' height='480'>"
    "<a href='https://other.example/b'>Other</a> <a href='/a'>More tea</a></article></body></html>"
)


@pytest.fixture(autouse=True)
def _no_network(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    fetched: list[dict] = []

    async def _scrape(**kw: Any) -> Any:
        fetched.append(kw)
        raise AssertionError("scraper.scrape fetched although html was supplied")

    async def _rules(url: str) -> site_rules.EffectivePolicy:
        return site_rules.EffectivePolicy()

    import matrx_scraper

    monkeypatch.setattr(matrx_scraper, "scrape", _scrape)
    monkeypatch.setattr(site_rules, "resolve", _rules)
    return fetched


async def _the_codes_capture(html: str) -> dict[str, Any]:
    """What the code's page check takes from the capture: the same parse and the one record projection
    (``page_records``; process_extension_content read string links as dicts and saved none until 2026-11-16)."""
    from matrx_scraper.page_records import page_records
    from matrx_scraper.parser.core import parse_html

    parsed = await parse_html(html, URL)
    links, images, _videos, _audios, _ = page_records(parsed)
    return {"content": parsed.get("ai_research_with_images", "") or parsed.get("ai_research_content", ""),
            "links": links, "images": images}


async def test_supplied_html_is_read_by_the_scrapers_own_parse_and_nothing_is_fetched(_no_network):
    result = await run_as_step(scrape_actions.scraper_scrape, SimpleNamespace(user_id="u"), ScrapeInput(url=URL, html=HTML, title="Green tea"))
    assert isinstance(result, Success), result
    facts = result.result
    code = await _the_codes_capture(HTML)
    assert _no_network == []
    assert facts.read is True and facts.engine == "supplied" and facts.title == "Green tea"
    assert facts.ai_text_with_images == code["content"] and "steamed" in facts.ai_text_with_images
    assert facts.link_records == code["links"] and len(code["links"]) == 2
    assert facts.image_records == code["images"] and code["images"][0]["src"].endswith("leaf.jpg")


async def test_empty_supplied_html_is_an_unread_page_with_facts(_no_network):
    result = await run_as_step(scrape_actions.scraper_scrape, SimpleNamespace(user_id="u"), ScrapeInput(url=URL, html="", when_unread="facts"))
    assert isinstance(result, Success), result
    assert result.result.read is False and result.result.failure_reason and _no_network == []


def test_the_html_argument_is_on_the_one_scraper_action():
    assert "html" in ScrapeInput.model_fields and scrape_actions.scraper_scrape is not None


WALL_IN_AN_IMAGE = (
    "<html><head><title>Members</title></head><body><article><h1>Members area</h1>"
    "<p>Our weekly notes on tea growing, picking and drying for every member of the club.</p>"
    "<img src='https://news.example/gate.png' alt='Sign in to continue' width='640' height='480'></article></body></html>"
)


@pytest.mark.parametrize("html", [HTML, WALL_IN_AN_IMAGE])
async def test_a_capture_head_is_judged_as_the_codes_extension_door_judges_it(_no_network, html):
    """head_reads='capture': the rule judge reads what the code's page check reads (research/domain_policy._rule_verdict
    over build_capture_offer: the stored text with images written in, its first 6,000 characters, no status). The
    default read judges the plain text with the supplied page's status 200 — a wall written only in an image's words
    was missed there (H13d gap, lane H21)."""
    from matrx_scraper.read_judge import judge_read

    result = await run_as_step(scrape_actions.scraper_scrape, SimpleNamespace(user_id="u"),
                               ScrapeInput(url=URL, html=html, title=None, head_reads="capture"))
    assert isinstance(result, Success), result
    code = await _the_codes_capture(html)
    verdict = judge_read(status=None, text=code["content"][:scrape_actions.HEAD_CHARS], title=result.result.title)
    expected = [verdict.reason] if verdict.failed and verdict.reason else []
    assert [w.kind for w in result.result.head_walls] == expected
    if html is WALL_IN_AN_IMAGE:
        # The image's words are in the capture's text (what the judge reads); a phrase on a short page no longer fails it.
        assert "Sign in to continue" in code["content"] and expected == []


async def test_dates_answer_the_first_real_iso_date_as_the_code_reads_it(_no_network):
    """date_candidates -> dates: research's extension door keeps a page date only when ``datetime.fromisoformat``
    reads it (multisource._valid_iso, now this Action's valid_iso_date). The page check workflow matched an ISO-looking
    pattern instead: it kept 2024-13-45 and dropped 20240101 (H13d gap, lane H21)."""
    result = await run_as_step(scrape_actions.scraper_scrape, SimpleNamespace(user_id="u"), ScrapeInput(
        url=URL, html=HTML, date_candidates={
            "published_at": ["2024-13-45", None, "20240101"],
            "modified_at": ["  2024-01-02T03:04:05Z ", "2024-01-01"],
            "none": ["yesterday", ""],
        }))
    assert isinstance(result, Success), result
    assert result.result.dates == {"published_at": "20240101", "modified_at": "2024-01-02T03:04:05Z", "none": None}
