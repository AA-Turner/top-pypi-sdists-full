"""Search-and-scrape: the rows sent equal the Sources landed; nothing landed is said; no
placeholder rows (SOURCE-CONVERGENCE §1 rule 6 — a search hit is not a Source until its content lands).

Web-app walk, 2026-09-26: a search-and-scrape with a max of 2 reported 6 pages and rendered a
placeholder sentence as a hit. Breaks these tests name: more hits than asked for; a hit with no
web address; a failed page sent as a result row; a closing count that differs from the rows
sent; a run that landed nothing without saying so.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_scraper import service as svc
from matrx_scraper._ext import configure_ext
from matrx_scraper.orchestrator import ScrapeResult
from matrx_scraper.service import ScrapeService, SearchResultItem


class _Emitter:
    def __init__(self) -> None:
        self.data: list[Any] = []
        self.info: list[Any] = []

    async def send_data(self, payload: Any) -> None:
        self.data.append(payload)

    async def send_info(self, payload: Any) -> None:
        self.info.append(payload)


def _hit(url: str, kind: str = "web") -> SearchResultItem:
    return SearchResultItem(keyword="k", type=kind, title=url or "No results", url=url, description="")  # type: ignore[arg-type]


def _page(url: str, ok: bool) -> ScrapeResult:
    r = ScrapeResult(url=url, response_url=url, success=ok, content_type="html")
    r.title = f"Title of {url}"
    r.text_data = "Words on the page. " * 20 if ok else ""
    if not ok:
        r.failure_reason = "request_error"
        r.failure_message = f"We could not reach {url}: that address does not exist."
    return r


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch):
    async def no_failure_log(_result: Any) -> None:
        return None

    monkeypatch.setattr(svc, "_fire_and_forget_failure_log", no_failure_log)
    state: dict[str, Any] = {"hits": [], "ok": set(), "landed": []}

    async def brave(self, keyword: str, count: int | None = None) -> list[SearchResultItem]:
        return list(state["hits"])

    async def many(urls: list[str], **_: Any):
        for u in urls:
            yield _page(u, u in state["ok"])

    async def hook(landing: dict[str, Any]) -> dict[str, Any]:
        state["landed"].append(landing["canonical_identity"])
        return {"processed_document_id": f"doc-{len(state['landed'])}", "source_id": "s", "notices": []}

    monkeypatch.setattr(ScrapeService, "_brave_search", brave)
    monkeypatch.setattr(svc, "scrape_many_stream", many)
    monkeypatch.setattr(svc.asyncio, "sleep", lambda *_a, **_k: _noop())
    configure_ext(source_landing=hook)
    return state


async def _noop() -> None:
    return None


def _service(emitter: _Emitter) -> ScrapeService:
    s = ScrapeService(emitter=emitter, organization_id="org", acting_user_id="user")
    s.land_as = "web"
    return s


def _rows(emitter: _Emitter) -> list[dict[str, Any]]:
    return [p for d in emitter.data if getattr(d, "type", "") == "fetch_results" for p in d.model_dump()["results"]]


def _summary(emitter: _Emitter) -> Any:
    [s] = [i for i in emitter.info if i.code == "sources_landed"]
    return s


async def test_hits_are_capped_real_and_rows_equal_sources_landed(world: dict[str, Any]) -> None:
    world["hits"] = [_hit("https://a.test/1"), _hit(""), _hit("https://a.test/2"), _hit("https://a.test/1", "news"), _hit("https://a.test/3", "news")]
    world["ok"] = {"https://a.test/1"}
    e = _Emitter()
    s = _service(e)
    s.keywords, s.total_results_per_keyword = ["k"], 2
    await s.search_and_scrape()
    [hits] = [d for d in e.data if getattr(d, "type", "") == "search_results"]
    assert [h.url for h in hits.results] == ["https://a.test/1", "https://a.test/2"]
    rows = _rows(e)
    assert len(rows) == 1 and rows[0]["processed_document_id"]
    summary = _summary(e)
    assert summary.metadata["sources_landed"] == len(rows) == 1
    assert [u["url"] for u in summary.metadata["pages_not_saved"]] == ["https://a.test/2"]


async def test_a_run_that_lands_nothing_says_so(world: dict[str, Any]) -> None:
    world["hits"] = [_hit("https://gone.test/1")]
    e = _Emitter()
    s = _service(e)
    s.keyword, s.max_page_read = "k", 2
    await s.search_and_scrape_limited()
    assert _rows(e) == []
    summary = _summary(e)
    assert summary.metadata["sources_landed"] == 0
    assert summary.user_message.startswith("No Sources were saved") and "gone.test" in summary.user_message


async def test_limited_stops_at_max_sources_landed(world: dict[str, Any]) -> None:
    world["hits"] = [_hit(f"https://b.test/{i}") for i in range(6)]
    world["ok"] = {f"https://b.test/{i}" for i in (1, 2, 3, 4)}
    e = _Emitter()
    s = _service(e)
    s.keyword, s.max_page_read = "k", 2
    await s.search_and_scrape_limited()
    assert len(_rows(e)) == 2 == _summary(e).metadata["sources_landed"]


async def test_an_unkept_landing_is_captured_never_saved(world: dict[str, Any]) -> None:
    """The door calls an unkept landing 'Captured, not saved'; the closing sentence must too."""
    world["hits"] = [_hit("https://c.test/1"), _hit("https://c.test/2")]
    world["ok"] = {"https://c.test/1", "https://c.test/2"}
    e = _Emitter()
    s = _service(e)
    s.keyword, s.max_page_read = "k", 2
    await s.search_and_scrape_limited()
    summary = _summary(e)
    assert summary.metadata["sources_landed"] == 2 and summary.metadata["sources_saved"] == 0
    assert not summary.user_message.startswith("Saved") and "not saved yet" in summary.user_message


async def test_search_hits_are_announced_as_candidates_not_rows(world: dict[str, Any]) -> None:
    """Seated walk #2: a max-2 run rendered 6 rows with duplicates — the 4 candidate addresses the
    limited search reads from plus the 2 pages. The wire now says the hits are candidates and the
    Sources are the fetch_results rows; the rows still equal sources_landed."""
    world["hits"] = [_hit(f"https://d.test/{i}") for i in range(4)]
    world["ok"] = {"https://d.test/0", "https://d.test/1"}
    e = _Emitter()
    s = _service(e)
    s.keyword, s.max_page_read = "k", 2
    await s.search_and_scrape_limited()
    [hits] = [d for d in e.data if getattr(d, "type", "") == "search_results"]
    assert hits.metadata["role"] == "candidates" and hits.metadata["max_page_read"] == 2
    assert len(_rows(e)) == 2 == _summary(e).metadata["sources_landed"]
