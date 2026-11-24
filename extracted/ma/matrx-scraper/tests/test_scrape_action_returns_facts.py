"""``scraper.scrape`` returns FACTS about one read, never a verdict (research/FEATURE.md § Actions a research workflow may run).

Beside the page it reports the host's main text (the site-rules selector, moved out of research), the links and
media, and the rule judge's walls (``read_judge.judge_read``) — a workflow step decides what they mean. It can be
asked for a browser read (``mode: browser``), can hand back a failed read as facts (``when_unread: facts``), and
paces reads of one host by the step's interval. Only the network edge (``matrx_scraper.scrape``) and the
site-rules lookup are replaced; the projection, the selector run and the rule judge run for real.
"""

from __future__ import annotations

import time
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_graph.actions import run_as_step
from matrx_graph.types.result import Failure, Success

from matrx_scraper import site_rules
from matrx_scraper.graph_nodes import scrape_actions
from matrx_scraper.graph_nodes.scrape_actions import ScrapedPageFacts, ScrapeInput, scraper_scrape
from matrx_scraper.scraper import RequestType

ARTICLE_HTML = (
    "<html><head><title>Green tea</title></head><body><nav>Home | Shop | Login</nav>"
    "<article class='story'><p>Green tea is steamed within hours of picking.</p></article></body></html>"
)
SIGN_IN_TEXT = "Log in to continue. Sign in with your account to see this page."


def _result(**over: Any) -> dict[str, Any]:
    base = {
        "url": "https://news.example/tea", "response_url": "https://news.example/tea", "success": True,
        "status_code": 200, "title": "Green tea", "content_type": "html", "raw_html": ARTICLE_HTML,
        "main_content_text": "Green tea is steamed within hours of picking.", "engine": "http",
        "links": {"internal": ["https://news.example/a"], "external": ["https://other.example/b"],
                  "images": ["https://news.example/tea.jpg"], "documents": ["https://news.example/r.pdf"]},
    }
    return {**base, **over}


def _install(monkeypatch: pytest.MonkeyPatch, result: dict[str, Any], selector: str | None = None) -> list[dict]:
    calls: list[dict] = []

    async def _scrape(**kw: Any) -> dict[str, Any]:
        calls.append(kw)
        return result

    async def _rules(url: str) -> site_rules.EffectivePolicy:
        return site_rules.EffectivePolicy(content_selector=selector, category="news" if selector else None)

    import matrx_scraper

    monkeypatch.setattr(matrx_scraper, "scrape", _scrape)
    monkeypatch.setattr(site_rules, "resolve", _rules)
    monkeypatch.setattr(scrape_actions, "_host_pacer", None)
    return calls


async def _run(**inputs: Any) -> Any:
    inputs.setdefault("host_interval_seconds", 0)
    inputs.setdefault("host_interval_jitter_seconds", 0)
    return await run_as_step(scraper_scrape, SimpleNamespace(user_id="u"), ScrapeInput(**inputs))


def _ok(result: Any) -> ScrapedPageFacts:
    assert isinstance(result, Success), result
    return result.result


@pytest.mark.asyncio
async def test_a_read_reports_host_main_text_links_and_media(monkeypatch: pytest.MonkeyPatch) -> None:
    _install(monkeypatch, _result(), selector="article.story")
    out = _ok(await _run(url="https://news.example/tea"))
    # Only the selector run produces this: the nav words are in the HTML but not in the main text.
    assert out.main_text == "Green tea is steamed within hours of picking."
    assert out.main_text_chars == 45 and out.main_text_selector == "article.story" and out.host_category == "news"
    assert out.links == ["https://news.example/a", "https://other.example/b"]
    assert out.media == ["https://news.example/tea.jpg", "https://news.example/r.pdf"]
    assert out.read is True and out.rule_walls == [] and out.engine == "http"


@pytest.mark.asyncio
async def test_no_selector_means_nothing_measured(monkeypatch: pytest.MonkeyPatch) -> None:
    _install(monkeypatch, _result(), selector=None)
    out = _ok(await _run(url="https://news.example/tea"))
    assert out.main_text is None and out.main_text_chars is None and out.main_text_selector is None


@pytest.mark.asyncio
async def test_a_sign_in_wall_is_a_fact_not_a_verdict(monkeypatch: pytest.MonkeyPatch) -> None:
    _install(monkeypatch, _result(title="Log in", main_content_text=SIGN_IN_TEXT, raw_html=f"<p>{SIGN_IN_TEXT}</p>"))
    out = _ok(await _run(url="https://news.example/tea"))
    # Closing pass 2026-11-17: a short page with a sign-in title or phrase and no password form is read, never walled.
    assert out.rule_walls == []
    assert out.read is True  # the scraper read a page; whether it is any good is a step's rule
    assert not {"is_good", "verdict", "good"} & set(ScrapedPageFacts.model_fields)


@pytest.mark.asyncio
async def test_a_failed_read_fails_by_default_and_is_facts_on_request(monkeypatch: pytest.MonkeyPatch) -> None:
    failed = _result(success=False, status_code=403, failure_reason="cloudflare_block", main_content_text="",
                     raw_html="", links=None)
    _install(monkeypatch, failed)
    assert isinstance(await _run(url="https://news.example/tea"), Failure)  # unchanged default
    out = _ok(await _run(url="https://news.example/tea", when_unread="facts"))
    assert out.read is False and out.failure_reason == "cloudflare_block" and out.status_code == 403
    assert [w.kind for w in out.rule_walls] == ["challenge"]


@pytest.mark.asyncio
async def test_browser_mode_asks_for_a_browser_read(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = _install(monkeypatch, _result())
    _ok(await _run(url="https://news.example/tea"))
    out = _ok(await _run(url="https://news.example/tea", mode="browser"))
    assert [c["request_type"] for c in calls] == [RequestType.NORMAL, RequestType.BROWSER] and out.mode == "browser"


@pytest.mark.asyncio
async def test_same_host_reads_are_paced_by_the_step_interval(monkeypatch: pytest.MonkeyPatch) -> None:
    _install(monkeypatch, _result())
    started = time.monotonic()
    _ok(await _run(url="https://news.example/one", host_interval_seconds=0.4))
    _ok(await _run(url="https://news.example/two", host_interval_seconds=0.4))
    assert time.monotonic() - started >= 0.4  # the second read waited for the first one's gap
    assert ScrapeInput(url="https://x.example").host_interval_seconds == 2.0
    assert ScrapeInput(url="https://x.example").host_interval_jitter_seconds == 0.75


def test_typed_contract() -> None:
    from matrx_graph.actions import default_action_registry
    from matrx_scraper.graph_nodes import register_with_graph

    register_with_graph()
    spec = default_action_registry().get("scraper.scrape")
    assert spec.output_schema is ScrapedPageFacts
    inp = spec.input_schema.model_json_schema()["properties"]
    assert inp["mode"]["enum"] == ["auto", "browser"] and inp["when_unread"]["enum"] == ["fail", "facts"]
    out = ScrapedPageFacts.model_json_schema()
    assert out.get("additionalProperties") is False
    assert {"text", "main_text", "main_text_chars", "links", "media", "content_type", "status_code",
            "failure_reason", "rule_walls", "read"} <= set(out["properties"])


@pytest.mark.asyncio
async def test_head_walls_read_only_what_a_page_judge_reads(monkeypatch: pytest.MonkeyPatch) -> None:
    """A wall that shows only in the HTML is a rule wall, never a head wall: head walls read the status, the
    title and the first 6,000 characters of text, exactly what the research page verdict's rule reads."""
    from matrx_scraper.read_judge import judge_read

    long_text = "A long article paragraph about tea with real detail. " * 200
    shell = "<div id='root'></div><script src='app.js'></script>" * 3
    _install(monkeypatch, _result(main_content_text=long_text, raw_html=shell, title="Tea"))
    out = _ok(await _run(url="https://news.example/tea"))
    expected = judge_read(status=out.status_code or None, text=long_text[:6000], title="Tea")
    assert [w.kind for w in out.head_walls] == ([expected.reason] if expected.failed else [])
    _install(monkeypatch, _result(title="Log in", main_content_text=SIGN_IN_TEXT, raw_html=f"<p>{SIGN_IN_TEXT}</p>"))
    out = _ok(await _run(url="https://news.example/tea"))
    assert out.head_walls == []  # a sign-in title and phrase on a short page, no password form: read (closing pass 2026-11-17)


@pytest.mark.asyncio
async def test_the_host_floors_and_action_are_facts(monkeypatch: pytest.MonkeyPatch) -> None:
    _install(monkeypatch, _result())

    async def _rules(url: str) -> site_rules.EffectivePolicy:
        return site_rules.EffectivePolicy(min_content_chars=2500, min_real_content_chars=800, policy_action="force_l3",
                                          matched_pattern="news.example/*")

    monkeypatch.setattr(site_rules, "resolve", _rules)
    out = _ok(await _run(url="https://news.example/tea"))
    assert (out.min_content_chars, out.min_real_content_chars, out.policy_action, out.policy_pattern) == (
        2500, 800, "force_l3", "news.example/*")


def test_the_facts_never_claim_the_page_record_kind() -> None:
    """scraped_page is the distilled page record; ScrapedPageFacts is not that shape, and under kind
    enforcement a claimed kind it does not match fails every live run (2026-11-09, run df3b7746)."""
    from matrx_graph.actions import default_action_registry
    from matrx_scraper.graph_nodes import register_with_graph

    register_with_graph()
    spec = default_action_registry().get("scraper.scrape")
    assert getattr(spec, "output_kind", None) != "scraped_page"


PAGE_HTML = (
    "<html><head><title>Tea</title></head><body><article><h1>Tea</h1>"
    + "<p>A long paragraph about tea with real detail and history. </p>" * 40
    + "<a href='https://other.example/x'>Other site</a><a href='/inner'>Inner</a>"
    + "<img src='https://news.example/a.jpg' alt='A cup' width='640' height='480'>"
    + "<img src='data:image/png;base64,AAAA'></article></body></html>"
)


@pytest.mark.asyncio
async def test_records_and_ai_text_are_the_research_parse(monkeypatch: pytest.MonkeyPatch) -> None:
    """The records and AI text are what research's own read derives from the same HTML (parse_html + page_records)."""
    from matrx_scraper.page_records import page_records, page_text
    from matrx_scraper.parser.core import parse_html

    _install(monkeypatch, _result(raw_html=PAGE_HTML, title="Tea"))
    out = _ok(await _run(url="https://news.example/tea"))
    parsed = await parse_html(PAGE_HTML, out.response_url or "https://news.example/tea")
    links, images, videos, audios, dropped = page_records(parsed)
    assert out.ai_text == page_text(parsed) and out.ai_text
    assert (out.link_records, out.image_records, out.video_records, out.audio_records) == (links, images, videos, audios)
    assert dropped == 1 and all(not str(i["src"]).startswith("data:") for i in out.image_records)


@pytest.mark.asyncio
async def test_a_site_rule_block_is_never_fetched(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = _install(monkeypatch, _result())

    async def _rules(url: str) -> site_rules.EffectivePolicy:
        return site_rules.EffectivePolicy(policy_action="block", matched_pattern="news.example/*")

    monkeypatch.setattr(site_rules, "resolve", _rules)
    out = _ok(await _run(url="https://news.example/tea", skip_policy_actions=["block", "force_l3", "force_l4"]))
    assert calls == [] and out.read is False and (out.policy_action, out.policy_pattern) == ("block", "news.example/*")
    _ok(await _run(url="https://news.example/tea"))  # not asked to skip: read as before
    assert len(calls) == 1


@pytest.mark.asyncio
async def test_the_parse_is_held_on_the_server_for_the_landing(monkeypatch: pytest.MonkeyPatch) -> None:
    """With hold_page_in_run the whole parse (plus the url asked for, the served url, the title and the raw HTML,
    as research lands a page) is stored once in the run and only its reference travels; without it, no page."""
    from matrx_graph.checkpoint import value_store

    from matrx_scraper.parser.core import parse_html

    held: list[tuple[str, Any]] = []

    async def _hold(run_id: str, value: Any, *, organization_id: str | None = None) -> Any:
        held.append((run_id, value))
        return {value_store.HELD_KEY: "ref-1"}

    monkeypatch.setattr(value_store, "hold_on_server", _hold)
    _install(monkeypatch, _result(raw_html=ARTICLE_HTML, response_url="https://news.example/tea?x=1"))
    assert _ok(await _run(url="https://news.example/tea")).page is None and not held

    out = _ok(await _run(url="https://news.example/tea", hold_page_in_run="run-9"))
    assert out.page == {value_store.HELD_KEY: "ref-1"}
    ((run_id, page),) = held
    parsed = await parse_html(ARTICLE_HTML, "https://news.example/tea?x=1")
    assert run_id == "run-9"
    assert (page["url"], page["response_url"], page["title"], page["raw_html"]) == (
        "https://news.example/tea", "https://news.example/tea?x=1", "Green tea", ARTICLE_HTML)
    assert page["ai_research_content"] == parsed["ai_research_content"]
    assert page["organized_data"] == __import__("json").loads(__import__("json").dumps(parsed["organized_data"], default=str))


@pytest.mark.asyncio
async def test_browser_mode_renders_in_the_hosts_browser_lane(monkeypatch: pytest.MonkeyPatch) -> None:
    """mode browser takes the host's browser lane (the scraper service's pooled browser) — the same render research's
    own rescue takes — never a local browser; without a lane it falls back to the scraper's own browser fetch."""
    from matrx_scraper import _ext

    calls = _install(monkeypatch, _result())
    rendered: list[str] = []

    async def _render(url: str) -> dict[str, Any]:
        rendered.append(url)
        return {"success": True, "status_code": 200, "final_url": url, "title": "Green tea", "content_type": "text/html",
                "html": ARTICLE_HTML, "error": None}

    monkeypatch.setitem(_ext._registry, "browser_render", _render)
    out = _ok(await _run(url="https://news.example/tea", mode="browser", when_unread="facts"))
    assert rendered == ["https://news.example/tea"] and calls == []
    assert out.read and out.engine == "browser_lane" and "steamed within hours" in (out.ai_text or out.text)

    async def _miss(url: str) -> dict[str, Any]:
        return {"success": False, "error": "render failed"}

    monkeypatch.setitem(_ext._registry, "browser_render", _miss)
    out = _ok(await _run(url="https://news.example/tea", mode="browser", when_unread="facts"))
    assert out.read is False and out.failure_reason == "browser_render_miss" and calls == []

    monkeypatch.delitem(_ext._registry, "browser_render")
    _ok(await _run(url="https://news.example/tea", mode="browser"))
    assert calls[-1]["request_type"] == RequestType.BROWSER


@pytest.mark.asyncio
async def test_the_pages_iframe_sources_travel_as_a_fact(monkeypatch: pytest.MonkeyPatch) -> None:
    """A step after the read (the gallery) gets the page's embedded players from ``iframe_srcs``, never the HTML
    (lane M2, 2026-11-19: the held page with its raw HTML was decoded once more per reading step)."""
    html = ARTICLE_HTML.replace(
        "</body>",
        "<iframe src='https://www.youtube.com/embed/dQw4w9WgXcQ'></iframe><iframe data-src='x' src=\"https://a.example/f\">"
        "</iframe></body>",
    )
    _install(monkeypatch, _result(raw_html=html))
    out = _ok(await _run(url="https://news.example/tea"))
    assert out.iframe_srcs == ["https://www.youtube.com/embed/dQw4w9WgXcQ", "https://a.example/f"]


#: A page that answered 200 with HTML and no words (an app shell): the scraper's sanity gate calls it
#: ``empty_content`` and success false, but the HTML is in hand and its links are real.
SHELL_WITH_LINKS = (
    "<html><head><title>Rain barrel</title><link rel='preconnect' href='https://cdn.example'></head><body>"
    "<div id='root'></div><a href='https://cdn.example/x'></a><a href='/how-to'></a></body></html>"
)


@pytest.mark.asyncio
async def test_an_empty_content_page_still_reports_its_parsed_records(monkeypatch: pytest.MonkeyPatch) -> None:
    """research saves an ``empty_content`` read as a read (its capture row keeps the page's links), and research's own
    read parses any HTML the fetch answered (research/scraper.py ``_extract_html_payload``). The facts carry that parse's
    records, so both engines save the same ``extracted_links`` (parity pair 1a58f588, instructables.com, 2026-11-19)."""
    from matrx_scraper.page_records import page_records, page_text
    from matrx_scraper.parser.core import parse_html

    _install(monkeypatch, _result(success=False, failure_reason="empty_content", main_content_text="",
                                  raw_html=SHELL_WITH_LINKS, title="Rain barrel"))
    out = _ok(await _run(url="https://news.example/tea", when_unread="facts"))
    parsed = await parse_html(SHELL_WITH_LINKS, "https://news.example/tea")
    links, images, videos, audios, _ = page_records(parsed)
    assert links, "the shell's anchors parse to link records"
    assert out.read is False and out.failure_reason == "empty_content"
    assert (out.link_records, out.image_records, out.video_records, out.audio_records) == (links, images, videos, audios)
    assert out.ai_text == page_text(parsed)


@pytest.mark.asyncio
async def test_a_blocked_page_reports_no_records(monkeypatch: pytest.MonkeyPatch) -> None:
    """A read that failed for any other reason (a bot wall's HTML) is not a page: no records, as research saves none."""
    _install(monkeypatch, _result(success=False, status_code=403, failure_reason="cloudflare_block",
                                  main_content_text="", raw_html=SHELL_WITH_LINKS))
    out = _ok(await _run(url="https://news.example/tea", when_unread="facts"))
    assert out.link_records == [] and out.image_records == [] and out.ai_text == ""
