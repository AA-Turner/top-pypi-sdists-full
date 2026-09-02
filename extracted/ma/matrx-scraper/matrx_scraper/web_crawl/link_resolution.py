"""Link-target reconciliation — backfills ``web.link_edge.target_page_id``.

The crawl write path resolves internal link targets against the canonical
page registry at write time but NEVER creates pages from links, so an edge
written before its target page existed (or before target resolution shipped)
carries ``target_page_id IS NULL``. This importable service walks a site's
unresolved internal edges in id-keyset batches, maps each ``target_url``
through the same normalization + ``url_hash`` discipline as every other
writer, and resolves what the registry now knows — loudly reporting
``{scanned, resolved, unresolved}``. No pages are ever created here either.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

from matrx_orm import Now, transaction
from matrx_orm.operations.bulk_update_values import bulk_update_by_pk

from matrx_scraper.crawler import _normalise_url
from matrx_scraper.db.models_web import (
    LinkEdge as WebLinkEdge,
    Page as WebPage,
)
from matrx_scraper.db.web import WEB_DB_NAME
from matrx_scraper.web_crawl.contracts import LinkResolutionSummary
from matrx_scraper.web_crawl.persistence import url_hash

logger = logging.getLogger(__name__)

_EDGE_BATCH_SIZE = 1_000

ProgressCallback = Callable[[str, LinkResolutionSummary], Awaitable[None]]


class LinkResolutionResult:
    """Outcome of one link-target backfill run."""

    def __init__(self, summary: LinkResolutionSummary) -> None:
        self.summary = summary


def match_edges_to_pages(
    edge_targets: dict[str, str],
    page_ids_by_hash: dict[str, str],
) -> tuple[dict[str, str], int]:
    """Pure mapping step: ``{edge_id: target_url}`` + ``{url_hash: page_id}``
    → (``{edge_id: page_id}`` resolutions, unresolved count)."""

    resolutions: dict[str, str] = {}
    unresolved = 0
    for edge_id, target_url in edge_targets.items():
        digest = url_hash(_normalise_url(target_url))
        page_id = page_ids_by_hash.get(digest)
        if page_id is None:
            unresolved += 1
        else:
            resolutions[edge_id] = page_id
    return resolutions, unresolved


async def _report(
    on_progress: ProgressCallback | None,
    message: str,
    summary: LinkResolutionSummary,
) -> None:
    if on_progress is not None:
        await on_progress(message, summary)


async def resolve_site_link_targets(
    *,
    site_id: str,
    batch_size: int = _EDGE_BATCH_SIZE,
    on_progress: ProgressCallback | None = None,
) -> LinkResolutionResult:
    """Resolve ``target_page_id`` for a site's unresolved internal edges.

    Keyset-paginated on edge id so unresolvable edges (target URL still not
    in the registry) can never loop the walk. Idempotent and re-runnable —
    each run only touches edges whose ``target_page_id`` is still NULL."""

    summary = LinkResolutionSummary()
    last_id: str | None = None
    while True:
        filters: dict[str, object] = {
            "site_id": site_id,
            "is_internal": True,
            "target_page_id__isnull": True,
            "deleted_at__isnull": True,
        }
        if last_id is not None:
            filters["id__gt"] = last_id
        edges = await (
            WebLinkEdge.filter(**filters).order_by("id").limit(batch_size).all(use_cache=False)
        )
        if not edges:
            break
        last_id = str(edges[-1].id)
        summary.scanned += len(edges)

        edge_targets = {str(edge.id): str(edge.target_url) for edge in edges}
        digests = list({url_hash(_normalise_url(url)) for url in edge_targets.values()})
        pages = await WebPage.filter(
            site_id=site_id,
            url_hash__in=digests,
        ).all(use_cache=False)
        page_ids_by_hash = {str(page.url_hash): str(page.canonical_page_id) for page in pages}

        resolutions, unresolved = match_edges_to_pages(edge_targets, page_ids_by_hash)
        summary.unresolved += unresolved
        if resolutions:
            updates = [
                {"id": edge_id, "target_page_id": page_id}
                for edge_id, page_id in resolutions.items()
            ]
            async with transaction(WEB_DB_NAME):
                updated = await bulk_update_by_pk(
                    WebLinkEdge,
                    updates,
                    casts={"id": "uuid", "target_page_id": "uuid"},
                    set_expressions={"updated_at": Now()},
                )
            if updated != len(updates):
                raise RuntimeError(
                    f"link resolution updated {updated} of {len(updates)} edges — "
                    "refusing to under-report silently"
                )
            summary.resolved += updated
        await _report(
            on_progress,
            (
                f"Scanned {summary.scanned} edges; resolved {summary.resolved}, "
                f"{summary.unresolved} unresolved…"
            ),
            summary,
        )
        if len(edges) < batch_size:
            break
    return LinkResolutionResult(summary)


__all__ = [
    "LinkResolutionResult",
    "ProgressCallback",
    "match_edges_to_pages",
    "resolve_site_link_targets",
]
