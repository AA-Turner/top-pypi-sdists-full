"""Internal-link PageRank scoring — graph assembly, canonical collapse, wiring.

The pure algorithm is `matrx_scraper.pagerank.compute_link_scores`; what can
actually go wrong here is the plumbing around it — which pages become nodes,
whether a link to a redirected URL finds the page it resolves to, and whether
the scores reach `web.page`. So the end-to-end test drives the REAL
`score_site_links` with the two ORM models stubbed out at the boundary, and
asserts on the rows it tried to write.
"""

from __future__ import annotations

import pytest

from matrx_scraper.crawler import _normalise_url
from matrx_scraper.web_crawl import link_score as mod
from matrx_scraper.web_crawl.contracts import LinkScoreSummary
from matrx_scraper.web_crawl.link_score import (
    build_site_graph,
    resolve_edge_rows,
    score_site_links,
)
from matrx_scraper.web_crawl.persistence import url_hash


def _page(page_id: str, url: str, *, canonical: str | None = None, captured: bool = True):
    return {
        "id": page_id,
        "url_hash": url_hash(_normalise_url(url)),
        "canonical_page_id": canonical or page_id,
        "latest_snapshot_id": f"snap-{page_id}" if captured else None,
    }


def _edge(edge_id: str, source: str, target_url: str):
    return {"id": edge_id, "source_page_id": source, "target_url": target_url}


# ---------------------------------------------------------------------------
# Pure graph assembly


def test_uncaptured_page_is_not_a_node_but_still_resolves_links() -> None:
    """A sitemap-only page has no outbound links; counting it as a node would
    dilute every real page's share. Its URL must still resolve to its
    canonical page so links pointing at it are not silently dropped."""

    graph = build_site_graph(
        [
            _page("home", "https://example.com/"),
            _page("about", "https://example.com/about"),
            # never fetched, and it redirects to /about
            _page("about-old", "https://example.com/about-us", canonical="about", captured=False),
        ]
    )
    assert set(graph.group_members) == {"home", "about"}
    assert graph.group_members["about"] == ["about", "about-old"]
    assert graph.pages_captured == 2

    edges, dropped = resolve_edge_rows(graph, [_edge("e1", "home", "https://example.com/about-us")])
    assert dropped == 0
    assert [(e.source_id, e.target_url) for e in edges] == [("home", "about")]


def test_edge_targets_normalize_and_unknown_targets_are_dropped() -> None:
    graph = build_site_graph(
        [_page("home", "https://example.com/"), _page("a", "https://example.com/a")]
    )
    edges, dropped = resolve_edge_rows(
        graph,
        [
            _edge("e1", "home", "https://example.com/a/"),  # trailing slash
            _edge("e2", "home", "https://example.com/a#top"),  # fragment
            _edge("e3", "home", "https://example.com/never-registered"),
            _edge("e4", "ghost", "https://example.com/a"),  # source not a node
        ],
    )
    assert [e.target_url for e in edges] == ["a", "a"]
    assert dropped == 2


def test_link_score_summary_shape() -> None:
    assert LinkScoreSummary().model_dump(mode="json") == {
        "pages_captured": 0,
        "nodes": 0,
        "edges_scanned": 0,
        "edges_resolved": 0,
        "edges_unresolved": 0,
        "pages_scored": 0,
        "top_score": None,
        "computed_at": None,
    }


# ---------------------------------------------------------------------------
# End to end through the real service function, DB boundary stubbed


class _FakeQuery:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def order_by(self, *_a, **_k) -> _FakeQuery:
        return self

    def limit(self, *_a, **_k) -> _FakeQuery:
        return self

    def select(self, *_a, **_k) -> _FakeQuery:
        return self

    async def values(self, *fields: str) -> list[dict]:
        return [{f: row[f] for f in fields} for row in self._rows]


@pytest.fixture
def stub_db(monkeypatch):
    """Stand in for web.page / web.link_edge and capture what gets written."""

    state: dict[str, object] = {"pages": [], "edges": [], "writes": []}

    class _FakePage:
        @staticmethod
        def filter(**kwargs):
            # The edge query passes the page table through Subquery(...);
            # `id__gt` keyset paging is exercised by returning everything once.
            return _FakeQuery(state["pages"])  # type: ignore[arg-type]

    class _FakeLinkEdge:
        @staticmethod
        def filter(**kwargs):
            if "id__gt" in kwargs:
                return _FakeQuery([])
            return _FakeQuery(state["edges"])  # type: ignore[arg-type]

    async def _fake_bulk_update(model, rows, **_kwargs):
        state["writes"].extend(rows)  # type: ignore[attr-defined]
        return len(rows)

    class _NoTransaction:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_exc):
            return False

    monkeypatch.setattr(mod, "WebPage", _FakePage)
    monkeypatch.setattr(mod, "WebLinkEdge", _FakeLinkEdge)
    monkeypatch.setattr(mod, "Subquery", lambda query: query)
    monkeypatch.setattr(mod, "bulk_update_by_pk", _fake_bulk_update)
    monkeypatch.setattr(mod, "transaction", lambda _name: _NoTransaction())
    return state


async def test_score_site_links_writes_pagerank_to_every_page_in_the_group(stub_db) -> None:
    """Three pages linking to a hub: the hub must score 100, and the hub's
    redirect alias must receive the same score rather than staying NULL."""

    stub_db["pages"] = [
        _page("home", "https://example.com/"),
        _page("a", "https://example.com/a"),
        _page("b", "https://example.com/b"),
        _page("hub", "https://example.com/hub"),
        _page("hub-old", "https://example.com/hub-legacy", canonical="hub", captured=False),
    ]
    stub_db["edges"] = [
        _edge("e1", "home", "https://example.com/hub"),
        _edge("e2", "a", "https://example.com/hub"),
        # via the alias URL — must still credit the hub
        _edge("e3", "b", "https://example.com/hub-legacy"),
        _edge("e4", "home", "https://example.com/a"),
        _edge("e5", "home", "https://example.com/offsite-unknown"),
    ]

    result = await score_site_links(site_id="site-1")
    summary = result.summary

    assert summary.nodes == 4
    assert summary.pages_captured == 4
    assert summary.edges_scanned == 5
    assert summary.edges_resolved == 4
    assert summary.edges_unresolved == 1

    written = {row["id"]: row["link_score"] for row in stub_db["writes"]}
    # Every node's group member is written, alias included — no NULL rows left.
    assert set(written) == {"home", "a", "b", "hub", "hub-old"}
    assert written["hub"] == pytest.approx(100.0)
    assert written["hub-old"] == written["hub"]
    assert written["hub"] > written["a"] > written["b"]
    assert summary.pages_scored == 5
    assert summary.top_score == pytest.approx(100.0)
    assert summary.computed_at is not None
    assert all(row["link_score_computed_at"] is not None for row in stub_db["writes"])


async def test_partial_graph_never_scores_but_a_completed_full_crawl_does(monkeypatch) -> None:
    """The rule from the crawl side: score a WHOLE graph or nothing.

    A list crawl (hand-picked URLs) and the short homepage/initialization runs
    see only a fragment of the site's links — scoring them produces confident,
    wrong numbers. And because the step hangs off the success path of
    `run_prepared`, a failed or cancelled session never reaches it at all.
    """

    from matrx_scraper.web_crawl import service as service_mod

    scored: list[str] = []

    async def _fake_score(*, site_id: str, on_progress=None):
        scored.append(site_id)
        return mod.LinkScoreResult(LinkScoreSummary())

    monkeypatch.setattr(service_mod, "score_site_links", _fake_score)
    svc = service_mod.WebCrawlService()

    class _Prepared:
        def __init__(self, mode: str) -> None:
            self.mode = mode
            self.site_id = f"site-{mode}"
            self.session_id = "sess"

    class _Sink:
        def __init__(self) -> None:
            self.warnings: list[object] = []

        async def emit(self, event) -> None:
            self.warnings.append(event)

    for mode in ("list", "homepage", "initialization", "page_fetch"):
        await svc._run_post_crawl_link_scoring(_Prepared(mode), _Sink())
    assert scored == []

    await svc._run_post_crawl_link_scoring(_Prepared("full"), _Sink())
    assert scored == ["site-full"]


async def test_post_crawl_scoring_failure_warns_and_never_fails_the_crawl(monkeypatch) -> None:
    """The capture already succeeded — a scoring bug must not turn a good
    crawl into a failed one, but it must not vanish either."""

    from matrx_scraper.web_crawl import service as service_mod

    async def _boom(*, site_id: str, on_progress=None):
        raise RuntimeError("pagerank exploded")

    monkeypatch.setattr(service_mod, "score_site_links", _boom)

    class _Prepared:
        mode = "full"
        site_id = "site-1"
        session_id = "sess"

    emitted: list[object] = []

    class _Sink:
        async def emit(self, event) -> None:
            emitted.append(event)

    await service_mod.WebCrawlService()._run_post_crawl_link_scoring(_Prepared(), _Sink())

    assert len(emitted) == 1
    warning = emitted[0]
    assert warning.context == {"reason": "post_crawl_link_scoring_failed"}
    assert "pagerank exploded" in warning.message


async def test_score_site_links_no_captured_pages_is_a_no_op(stub_db) -> None:
    """A site whose pages are all sitemap-only must not write anything (and
    must not raise) — there is no graph to score yet."""

    stub_db["pages"] = [_page("home", "https://example.com/", captured=False)]
    stub_db["edges"] = []

    result = await score_site_links(site_id="site-1")

    assert result.summary.nodes == 0
    assert result.summary.pages_scored == 0
    assert stub_db["writes"] == []
