"""Page fetch replay compares engines, not websites (L7i, 2026-11-09).

Battery's bslbatt.com page rotates its case-study links on every load, so a code read and a workflow read of the
same page wrote different links. With the host recording page answers, the second reader is served exactly what
the first was answered — through the same fetch entries both engines use — so a rotating page reads the same,
while a real difference in how a page is PARSED still shows.
"""

from __future__ import annotations

import asyncio
import itertools
from typing import Any

import pytest

from matrx_scraper import _ext, browser_lane, scraper
from matrx_scraper.page_records import page_records
from matrx_scraper.parser.core import parse_html
from matrx_scraper.scraper import ContentType, FailureReason, Firewall, RequestType, Response

URL = "https://bslbatt.example/blogs/storage-cost/"
_loads = itertools.count()


def _page() -> str:
    n = next(_loads)
    links = "".join(f'<li><a href="/case-study/{n}-{i}/">Case {n}-{i}</a></li>' for i in range(3))
    return (f"<html><head><title>Storage cost</title></head><body><article><h1>Storage cost</h1>"
            f"<p>{'Commercial battery storage costs vary by size. ' * 10}</p><ul>{links}</ul></article></body></html>")


async def _rotating_live(url: str, use_random_proxy: bool = True, user_agent: str | None = None) -> Response:
    html = _page()
    return Response(request_url=url, proxy_used=True, request_type=RequestType.NORMAL, content_type=ContentType.HTML,
                    extension="html", content_type_raw="text/html", response_url=url,
                    response_headers={"server": "cloudflare"}, status_code=200, content=html, title="Storage cost",
                    firewall=Firewall.CLOUDFLARE, failed_reasons=[{FailureReason.LOW_TEXT_CONTENT: "Text length 9"}])


class _Store:
    """The host's page answer store (aidream: services/runtime/page_replay.py), in memory."""

    def __init__(self) -> None:
        self.answers: dict[tuple[str, str], Any] = {}

    async def lookup(self, kind: str, url: str) -> Any:
        return self.answers.get((kind, url))

    async def record(self, kind: str, url: str, answer: Any) -> None:
        self.answers[(kind, url)] = answer


@pytest.fixture
def rotating(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(scraper, "_fetch_normally_with_proxy_live", _rotating_live)


@pytest.fixture
def store(monkeypatch: pytest.MonkeyPatch) -> _Store:
    s = _Store()
    monkeypatch.setitem(_ext._registry, "page_replay", s)
    return s


async def _links(response: Response) -> list[dict]:
    parsed = await parse_html(response.content, page_url=response.response_url)
    return page_records(parsed)[0]


def test_without_replay_a_rotating_page_reads_differently(rotating: None) -> None:
    async def go() -> tuple[list, list]:
        return (await _links(await scraper.fetch_normally_with_proxy(URL)),
                await _links(await scraper.fetch_normally_with_proxy(URL)))

    a, b = asyncio.run(go())
    assert a != b  # the website changed between the two reads


def test_under_replay_a_rotating_page_reads_the_same(rotating: None, store: _Store) -> None:
    async def go() -> tuple[Response, Response]:
        return await scraper.fetch_normally_with_proxy(URL), await scraper.fetch_normally_with_proxy(URL)

    first, second = asyncio.run(go())
    assert list(store.answers) == [("http", URL)]
    # every field the fetch answered comes back exactly (enums, failure reasons, headers, body)
    assert {k: v for k, v in vars(second).items() if k not in ("selectolax_soup", "soup")} == \
        {k: v for k, v in vars(first).items() if k not in ("selectolax_soup", "soup")}
    assert asyncio.run(_links(first)) == asyncio.run(_links(second))


def test_under_replay_a_real_parsing_difference_still_shows(rotating: None, store: _Store) -> None:
    async def go() -> tuple[list, list]:
        first = await scraper.fetch_normally_with_proxy(URL)
        second = await scraper.fetch_normally_with_proxy(URL)  # replayed: the same page
        good = await _links(first)
        # an engine that parses differently (drops the last link) — the replay must not hide it
        parsed = await parse_html(second.content, page_url=second.response_url)
        worse = page_records(parsed)[0][:-1]
        return good, worse

    good, worse = asyncio.run(go())
    assert good != worse


def test_a_browser_render_is_replayed_too(store: _Store) -> None:
    renders = itertools.count()

    async def render(url: str) -> dict:
        return {"success": True, "status_code": 200, "final_url": url, "title": "T", "content_type": "text/html",
                "html": f"<html><body><p>render {next(renders)}</p></body></html>"}

    async def go() -> tuple[Any, Any]:
        return (await browser_lane.render_in_browser_lane(URL, trigger="t", render=render),
                await browser_lane.render_in_browser_lane(URL, trigger="t", render=render))

    a, b = asyncio.run(go())
    assert a.content == b.content and "render 0" in b.content
    assert list(store.answers) == [("browser", URL)]
