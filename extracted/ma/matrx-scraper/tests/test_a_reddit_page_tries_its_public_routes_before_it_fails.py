"""Reddit failed 6 of 6 reads (bot check / empty page, research_web report, 2026-11-17).

Before a Reddit page is marked failed, the ordinary public routes of the same page are tried:
``old.reddit.com`` and the ``.json`` form of the URL. Both page readers (the research scrape and
``read_page_mcp_quick``) go through the one seam, so every caller gets it. No bot-check is bypassed:
each route is a plain public URL fetched the ordinary way; a route that also answers with a wall is
reported as the failure it is.
"""

from __future__ import annotations

import json

from pathlib import Path

import pytest

from matrx_scraper.features import mcp_tool_helpers as helpers
from matrx_scraper.features import read_page as rp
from matrx_scraper.public_routes import alternate_public_urls
from matrx_scraper.scraper import ContentType, RequestType, Response

THREAD = "https://www.reddit.com/r/LocalLLaMA/comments/abc123/best_gpu_for_inference/"
BODY = "Real discussion text about GPU inference benchmarks and tokens per second. " * 20
WALL = "<html><head><title>Blocked</title></head><body>Whoa there, pardner! Your request has been blocked by network security.</body></html>"


def _response(url: str, *, html: str = "", status: int = 200, ctype: ContentType = ContentType.HTML, failed: bool = False,
              landed: str | None = None) -> Response:
    return Response(
        request_url=url, proxy_used=False, request_type=RequestType.NORMAL, content_type=ctype, extension="",
        content_type_raw="text/html", response_url=landed or url, response_headers={}, status_code=status, content=html,
        failed=failed, title="",
    )


def _page(text: str) -> str:
    return f"<html><head><title>GPU thread</title></head><body><main><div id=\"siteTable\"><p>{text}</p></div></main></body></html>"


def _json_thread() -> str:
    post = {"kind": "t3", "data": {"title": "Best GPU for inference", "selftext": BODY, "author": "u1"}}
    comment = {"kind": "t1", "data": {"author": "u2", "body": "Measured 40 tokens per second on my card. " * 5, "replies": ""}}
    return json.dumps([
        {"data": {"children": [post]}},
        {"data": {"children": [comment]}},
    ])


def _fetcher(routes: dict[str, Response], seen: list[str]):
    async def fetch(url: str):
        seen.append(url)
        return routes.get(url) or _response(url, html=WALL, status=403, failed=True)
    return fetch


def test_the_public_routes_of_a_reddit_url_are_old_reddit_then_json():
    alts = alternate_public_urls(THREAD)
    assert alts[0] == "https://old.reddit.com/r/LocalLLaMA/comments/abc123/best_gpu_for_inference/"
    assert alts[1].startswith("https://www.reddit.com/r/LocalLLaMA/comments/abc123/best_gpu_for_inference.json")


def test_other_hosts_and_the_alternates_themselves_have_no_alternates():
    assert alternate_public_urls("https://example.com/a") == []
    assert alternate_public_urls("https://old.reddit.com/r/x/comments/1/t/") == []
    assert alternate_public_urls("https://www.reddit.com/r/x/comments/1/t.json") == []
    assert alternate_public_urls("https://notreddit.com/r/x") == []


@pytest.mark.asyncio
async def test_research_scrape_reads_a_walled_reddit_page_through_old_reddit(monkeypatch):
    seen: list[str] = []
    old = "https://old.reddit.com/r/LocalLLaMA/comments/abc123/best_gpu_for_inference/"
    monkeypatch.setattr(helpers, "fetch_normally_with_proxy", _fetcher({old: _response(old, html=_page(BODY))}, seen))
    failures: list = []
    page = await helpers.scrape_url_core(THREAD, failures=failures)
    assert page is not None and failures == []
    assert "GPU inference benchmarks" in page["content"]
    assert seen == [THREAD, old]


@pytest.mark.asyncio
async def test_read_page_falls_through_to_the_json_form(monkeypatch):
    seen: list[str] = []
    js = next(u for u in alternate_public_urls(THREAD) if ".json" in u)
    resp = _response(js, html=_json_thread(), ctype=ContentType.JSON)
    monkeypatch.setattr(rp, "fetch_normally_with_proxy", _fetcher({js: resp}, seen))
    out = await rp.read_page_mcp_quick(url=THREAD)
    assert out["status"] == "success", out
    assert "Best GPU for inference" in out["text"] and "40 tokens per second" in out["text"]
    assert seen[0] == THREAD and seen[-1] == js


@pytest.mark.asyncio
async def test_when_every_route_is_walled_the_failure_stands_and_names_the_original_url(monkeypatch):
    seen: list[str] = []
    monkeypatch.setattr(helpers, "fetch_normally_with_proxy", _fetcher({}, seen))
    failures: list = []
    page = await helpers.scrape_url_core(THREAD, failures=failures)
    assert page is None and len(failures) == 1
    assert failures[0]["url"] == THREAD
    assert len(seen) == 1 + len(alternate_public_urls(THREAD))


@pytest.mark.asyncio
async def test_a_page_that_reads_the_first_time_never_tries_an_alternate(monkeypatch):
    seen: list[str] = []
    monkeypatch.setattr(helpers, "fetch_normally_with_proxy", _fetcher({THREAD: _response(THREAD, html=_page(BODY))}, seen))
    page = await helpers.scrape_url_core(THREAD)
    assert page is not None and seen == [THREAD]


_REAL = Path(__file__).parent / "fixtures" / "read_judge"
#: Real responses captured 2026-11-17 (fixtures/read_judge/manifest.json): old.reddit.com redirects a thread to its
#: JavaScript login landing (no password field in the HTML); www.reddit.com answers 200 with "Prove your humanity".
LOGIN = (_REAL / "reddit_old.html").read_text()
LOGIN_AT = "https://old.reddit.com/login/?reason=lor2"
POW = (_REAL / "reddit_www.html").read_text()


@pytest.mark.asyncio
async def test_a_login_page_from_old_reddit_is_not_a_read(monkeypatch):
    """Measured 2026-11-17 from this Mac: old.reddit.com answers a thread with its login landing page, HTTP 200,
    and the read judge does not call it failed. The seam must not hand it back as the thread."""
    seen: list[str] = []
    old = alternate_public_urls(THREAD)[0]
    wall = _response(THREAD, html=WALL, status=403, failed=True)
    routes = {THREAD: wall, old: _response(old, html=LOGIN, landed=LOGIN_AT)}
    monkeypatch.setattr(helpers, "fetch_normally_with_proxy", _fetcher(routes, seen))
    from matrx_scraper.public_routes import fetch_with_public_routes

    got = await fetch_with_public_routes(THREAD, _fetcher(routes, seen))
    assert got is wall and "Welcome to Reddit" not in (got.content or "")


@pytest.mark.asyncio
@pytest.mark.parametrize("hollow", [LOGIN, POW])
async def test_a_hollow_200_original_with_failing_alternates_is_a_failed_read(monkeypatch, hollow):
    """The ORIGINAL answer is judged like every route: a login or bot-check shell served with HTTP 200 is not a read."""
    seen: list[str] = []
    routes = {THREAD: _response(THREAD, html=hollow, landed=LOGIN_AT if hollow is LOGIN else None)}
    monkeypatch.setattr(helpers, "fetch_normally_with_proxy", _fetcher(routes, seen))
    failures: list = []
    page = await helpers.scrape_url_core(THREAD, failures=failures)
    assert page is None, "a login/bot-check shell must never be returned as a read"
    assert len(failures) == 1 and failures[0]["url"] == THREAD and failures[0]["verdict"]["reason"] in ("challenge", "sign_in_wall")
    assert len(seen) == 1 + len(alternate_public_urls(THREAD))


@pytest.mark.asyncio
async def test_a_hollow_login_page_of_any_site_is_a_failed_read(monkeypatch):
    other = "https://forum.example.org/thread/9"
    page_html = ("<html><head><title>Members</title></head><body><form><input type=\"password\" name=\"p\">"
                 "<p>" + "Members only area. " * 30 + "</p></form></body></html>")
    seen: list[str] = []
    monkeypatch.setattr(helpers, "fetch_normally_with_proxy", _fetcher({other: _response(other, html=page_html)}, seen))
    failures: list = []
    assert await helpers.scrape_url_core(other, failures=failures) is None
    assert len(failures) == 1


@pytest.mark.asyncio
async def test_a_long_article_with_a_comment_login_form_is_still_a_read(monkeypatch):
    other = "https://blog.example.org/post"
    page_html = ("<html><head><title>Post</title></head><body><article><p>" + "Real long article sentence here. " * 200
                 + "</p></article><input type=\"password\"></body></html>")
    monkeypatch.setattr(helpers, "fetch_normally_with_proxy", _fetcher({other: _response(other, html=page_html)}, []))
    assert await helpers.scrape_url_core(other) is not None
