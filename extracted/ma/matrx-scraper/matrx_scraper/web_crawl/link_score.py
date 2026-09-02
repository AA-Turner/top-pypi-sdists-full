"""Internal-link PageRank scoring — populates ``web.page.link_score``.

The Screaming-Frog-style "Link Score" is the single best at-a-glance signal of
which pages on a site actually matter: a 0..100 PageRank over the site's own
internal link graph, where the most-linked-to page is 100. The frontend uses it
for the "strongest pages" list and to size nodes in the link graph.

The algorithm itself is pure and lives in :mod:`matrx_scraper.pagerank` — this
module is only the ``web.*`` plumbing: read the graph out of ``web.page`` +
``web.link_edge``, run it, write the scores back.

**What the graph is.** Nodes are the site's live pages that have actually been
captured (``page.latest_snapshot_id`` set); edges are the internal
``web.link_edge`` rows belonging to those latest snapshots. That is the same
"current state of the site" definition ``link_check`` uses when it stamps an
edge from its target page's latest snapshot — one meaning of "current" across
the module, and no dependence on any single crawl session.

**Canonical collapse.** A redirected/duplicate page carries
``canonical_page_id`` pointing at the page that represents the group. Both ends
of every edge collapse to the canonical page BEFORE scoring, so a link to a
redirecting URL credits the page it actually resolves to instead of being
dropped. Because that collapse is many-to-one (the pure algorithm accepts only
one alias per node), edge targets are pre-resolved here and handed to
``compute_link_scores`` already keyed by page id — for that call, "url" is
simply the join key. Target resolution reuses the ``url_hash(_normalise_url())``
discipline every other writer in this module uses, so it matches the registry
exactly. Every page in a canonical group is written the group's score, so no
row is left NULL just for being an alias.

**When it runs.** Wholesale recompute after a COMPLETED full crawl (see
``service._run_post_crawl_link_scoring``) and on demand via
``POST /crawler/sites/{site_id}/links/score``. Never mid-crawl, never after a
partial, cancelled, or list crawl: scoring a half-crawled site produces
confident, wrong numbers, and a stale-but-coherent score beats a fresh
incoherent one. ``page.link_score_computed_at`` records when the number was
produced so a consumer can tell a fresh score from one left over from an
older crawl.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable, Iterable, Mapping
from datetime import UTC, datetime

from matrx_orm import Now, Subquery, transaction
from matrx_orm.operations.bulk_update_values import bulk_update_by_pk

from matrx_scraper.crawler import _normalise_url
from matrx_scraper.db.models_web import (
    LinkEdge as WebLinkEdge,
    Page as WebPage,
)
from matrx_scraper.db.web import WEB_DB_NAME
from matrx_scraper.pagerank import Edge, compute_link_scores
from matrx_scraper.web_crawl.contracts import LinkScoreSummary
from matrx_scraper.web_crawl.persistence import url_hash

logger = logging.getLogger(__name__)

_EDGE_BATCH_SIZE = 5_000
_UPDATE_CHUNK = 2_000

ProgressCallback = Callable[[str, LinkScoreSummary], Awaitable[None]]


class LinkScoreResult:
    """Outcome of one link-score computation."""

    def __init__(self, summary: LinkScoreSummary) -> None:
        self.summary = summary


class SiteLinkGraph:
    """The resolved node material for one site, ready to score."""

    def __init__(self) -> None:
        # canonical page id -> every page id that shares its score
        self.group_members: dict[str, list[str]] = {}
        # url_hash of any live page -> its canonical page id
        self.canonical_by_hash: dict[str, str] = {}
        # page id -> canonical page id (for edge sources)
        self.canonical_by_page: dict[str, str] = {}
        # how many pages have actually been captured (have a latest snapshot)
        self.pages_captured: int = 0


def build_site_graph(page_rows: Iterable[Mapping[str, object]]) -> SiteLinkGraph:
    """Pure node-assembly step: page registry rows → the scorable graph.

    A page with no ``latest_snapshot_id`` was never captured (sitemap-only,
    never fetched). It is not a node — it has no outbound links, and treating
    it as one dilutes every real page's share — but it still contributes its
    URL alias so links pointing at it resolve to its canonical page.
    """

    graph = SiteLinkGraph()
    captured: set[str] = set()
    for row in page_rows:
        page_id = str(row["id"])
        canonical_id = str(row["canonical_page_id"] or page_id)
        graph.canonical_by_page[page_id] = canonical_id
        graph.canonical_by_hash[str(row["url_hash"])] = canonical_id
        if row["latest_snapshot_id"] is not None:
            captured.add(page_id)

    # Only canonical groups with at least one captured member are nodes.
    node_ids = {graph.canonical_by_page[page_id] for page_id in captured}
    for page_id, canonical_id in graph.canonical_by_page.items():
        if canonical_id in node_ids:
            graph.group_members.setdefault(canonical_id, []).append(page_id)
    graph.pages_captured = len(captured)
    return graph


def resolve_edge_rows(
    graph: SiteLinkGraph, edge_rows: Iterable[Mapping[str, object]]
) -> tuple[list[Edge], int]:
    """Pure edge-resolution step: link_edge rows → (canonical edges, dropped).

    An edge whose target URL is not in the page registry (an internal link to
    a URL we never registered) is dropped and counted — it can only be scored
    once the target exists, which is what ``/links/resolve`` and the next crawl
    are for. Same for an edge whose source page is not a node.
    """

    edges: list[Edge] = []
    dropped = 0
    for row in edge_rows:
        source = graph.canonical_by_page.get(str(row["source_page_id"]))
        target = graph.canonical_by_hash.get(url_hash(_normalise_url(str(row["target_url"]))))
        if (
            source is None
            or target is None
            or source not in graph.group_members
            or target not in graph.group_members
        ):
            dropped += 1
            continue
        edges.append(Edge(source_id=source, target_url=target))
    return edges, dropped


async def _load_site_graph(site_id: str) -> SiteLinkGraph:
    return build_site_graph(
        await WebPage.filter(site_id=site_id, deleted_at__isnull=True).values(
            "id", "url_hash", "canonical_page_id", "latest_snapshot_id"
        )
    )


async def _load_edges(site_id: str, graph: SiteLinkGraph, summary: LinkScoreSummary) -> list[Edge]:
    """Read the site's CURRENT internal edges, keyset-paginated, and resolve them.

    "Current" = edges belonging to each page's latest snapshot; historical
    crawl edges would score links the site no longer has. Expressed as the
    same sub-select ``insights.load_link_graph`` uses, so hundreds of
    thousands of edge rows are filtered in Postgres instead of shipping every
    snapshot id into an IN list.
    """

    current_snapshots = Subquery(
        WebPage.filter(
            site_id=site_id,
            deleted_at__isnull=True,
            latest_snapshot_id__isnull=False,
        ).select("latest_snapshot_id")
    )
    edges: list[Edge] = []
    last_id: str | None = None
    while True:
        filters: dict[str, object] = {
            "site_id": site_id,
            "is_internal": True,
            "deleted_at__isnull": True,
            "snapshot_id__in": current_snapshots,
        }
        if last_id is not None:
            filters["id__gt"] = last_id
        rows = await (
            WebLinkEdge.filter(**filters)
            .order_by("id")
            .limit(_EDGE_BATCH_SIZE)
            .values("id", "source_page_id", "target_url")
        )
        if not rows:
            break
        last_id = str(rows[-1]["id"])
        summary.edges_scanned += len(rows)
        resolved, dropped = resolve_edge_rows(graph, rows)
        summary.edges_unresolved += dropped
        edges.extend(resolved)
        if len(rows) < _EDGE_BATCH_SIZE:
            break
    summary.edges_resolved = len(edges)
    return edges


async def _persist_scores(
    graph: SiteLinkGraph, scores: dict[str, float], computed_at: datetime
) -> int:
    updates = [
        {
            "id": page_id,
            "link_score": round(score, 2),
            "link_score_computed_at": computed_at,
        }
        for canonical_id, score in scores.items()
        for page_id in graph.group_members[canonical_id]
    ]
    written = 0
    for start in range(0, len(updates), _UPDATE_CHUNK):
        chunk = updates[start : start + _UPDATE_CHUNK]
        async with transaction(WEB_DB_NAME):
            applied = await bulk_update_by_pk(
                WebPage,
                chunk,
                casts={
                    "id": "uuid",
                    "link_score": "numeric",
                    "link_score_computed_at": "timestamptz",
                },
                set_expressions={"updated_at": Now()},
            )
        if applied != len(chunk):
            raise RuntimeError(
                f"link scoring wrote {applied} of {len(chunk)} page scores — "
                "refusing to under-report silently"
            )
        written += applied
    return written


async def score_site_links(
    *,
    site_id: str,
    on_progress: ProgressCallback | None = None,
) -> LinkScoreResult:
    """Compute and persist ``web.page.link_score`` for one site.

    Wholesale and idempotent: every captured page's score is recomputed from
    the current graph on every run, so a re-run after new pages land simply
    replaces the old numbers. A site with nothing captured yet returns
    ``pages_scored == 0`` rather than raising.
    """

    summary = LinkScoreSummary()
    graph = await _load_site_graph(site_id)
    summary.pages_captured = graph.pages_captured
    summary.nodes = len(graph.group_members)
    if not graph.group_members:
        logger.info("link scoring skipped for site %s — no captured pages", site_id)
        if on_progress is not None:
            await on_progress("No captured pages to score.", summary)
        return LinkScoreResult(summary)

    if on_progress is not None:
        await on_progress(f"Reading internal links across {summary.nodes} pages…", summary)
    edges = await _load_edges(site_id, graph, summary)

    if on_progress is not None:
        await on_progress(
            f"Scoring {summary.nodes} pages over {summary.edges_resolved} internal links…",
            summary,
        )
    nodes = [(canonical_id, canonical_id, None) for canonical_id in graph.group_members]
    scores = compute_link_scores(nodes, edges)
    computed_at = datetime.now(UTC)
    summary.pages_scored = await _persist_scores(graph, scores, computed_at)
    summary.computed_at = computed_at.isoformat()
    if scores:
        summary.top_score = round(max(scores.values()), 2)
    logger.info(
        "link scoring for site %s: %s nodes, %s/%s internal edges resolved, %s page rows scored",
        site_id,
        summary.nodes,
        summary.edges_resolved,
        summary.edges_scanned,
        summary.pages_scored,
    )
    if on_progress is not None:
        await on_progress(f"Scored {summary.pages_scored} pages.", summary)
    return LinkScoreResult(summary)


__all__ = [
    "LinkScoreResult",
    "ProgressCallback",
    "SiteLinkGraph",
    "build_site_graph",
    "resolve_edge_rows",
    "score_site_links",
]
