"""Canonical URL identity for crawl, sitemap, GSC, GA4, and Bing observations."""

from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from collections.abc import Awaitable, Callable, Iterable
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Literal
from urllib.parse import urlparse
from uuid import uuid4

from matrx_orm import transaction
from matrx_orm.operations.bulk_update_values import bulk_update_by_pk
from matrx_utils import utcnow
from pydantic import BaseModel, Field

from matrx_scraper.db.models_web import (
    CrawlUrl as WebCrawlUrl,
    GscPageStat,
    Page as WebPage,
    PageSitemap as WebPageSitemap,
    Snapshot as WebSnapshot,
)
from matrx_scraper.db.web import WEB_DB_NAME
from matrx_scraper.utils.url import normalize_url, url_hash, url_match_key
from matrx_scraper.web_crawl.contracts import UrlReconciliationSummary

logger = logging.getLogger(__name__)

_PAGE_BATCH_SIZE = 500
_MAX_CHAIN_HOPS = 32
_PROVENANCES = {"gsc", "sitemap", "crawl", "manual", "ga4", "bing_webmaster"}

ProgressCallback = Callable[[str, UrlReconciliationSummary], Awaitable[None]]
RelationKind = Literal["existing", "equivalent", "direct", "redirect", "canonical"]


# --- Dismissal memory (Arman's ruling, 2026-08-08) -------------------------
# The crawler represents REALITY: a user "delete" of a crawler-observed row is
# a DISMISSAL — hidden, but if a later crawl/sync re-observes the thing, it
# comes back visibly AND permanently carries the fact that the user dismissed
# it before. Never silently ignored, never forgotten.


class RevivedDismissal(BaseModel):
    """One revive of a previously user-dismissed crawler-observed row."""

    row_id: str
    url: str
    dismissed_at: str | None
    dismissal_count: int


def append_dismissal_marker(
    metadata: dict[str, Any] | None,
    *,
    dismissed_at: datetime | str | None,
    session_id: str | None = None,
    now: datetime | None = None,
    reason: str = "reobserved",
) -> dict[str, Any]:
    """Return NEW metadata with this dismiss/revive cycle appended to
    ``metadata.dismissals``. Every cycle is preserved — repeated dismissals
    each add an entry, so the history is complete.

    ``reason`` names WHY the row came back: ``reobserved`` (the crawler saw it
    again — reality) or ``planned`` (a human put the URL in the content plan —
    intent). Both are revives and both are remembered; conflating them would
    lose which one the user actually did.
    """

    merged = dict(metadata or {})
    dismissals = list(merged.get("dismissals") or [])
    if isinstance(dismissed_at, datetime):
        dismissed_at_value: str | None = dismissed_at.isoformat()
    else:
        dismissed_at_value = str(dismissed_at) if dismissed_at else None
    dismissals.append(
        {
            "dismissed_at": dismissed_at_value,
            "revived_at": (now or utcnow()).isoformat(),
            "revive_reason": reason,
            "revived_by_session": session_id,
        }
    )
    merged["dismissals"] = dismissals
    return merged


class UrlRelation(BaseModel):
    source_url: str
    target_url: str
    kind: RelationKind
    observed_at: datetime
    status_code: int | None = None


class PageIdentityNode(BaseModel):
    id: str
    url: str
    canonical_page_id: str
    first_seen: datetime
    deleted_at: datetime | None = None
    latest_snapshot_id: str | None = None


class CanonicalIdentityPlan(BaseModel):
    canonical_by_page_id: dict[str, str] = Field(default_factory=dict)
    canonical_url_by_page_id: dict[str, str] = Field(default_factory=dict)
    relation_count: int = 0
    cycle_count: int = 0


class ResolvedPageUrl(BaseModel):
    observed_url: str
    observed_page_id: str
    canonical_page_id: str
    canonical_url: str


class CrawlIdentityResolution(BaseModel):
    requested_url: str
    final_url: str
    canonical_url: str
    page_id: str
    alias_page_ids: list[str] = Field(default_factory=list)
    canonical_was_new: bool = False


class UrlReconciliationResult:
    def __init__(self, summary: UrlReconciliationSummary) -> None:
        self.summary = summary


def _host_without_www(url: str) -> str:
    return (urlparse(normalize_url(url)).hostname or "").lower().removeprefix("www.")


def _is_same_site(url: str, root_url: str) -> bool:
    host = _host_without_www(url)
    root_host = _host_without_www(root_url)
    if not host or not root_host:
        return False
    if host == root_host:
        return True
    return host.endswith(f".{root_host}") or root_host.endswith(f".{host}")


def _relation_priority(kind: RelationKind) -> int:
    return {
        "existing": 0,
        "equivalent": 1,
        "direct": 2,
        "redirect": 3,
        "canonical": 4,
    }[kind]


def _follow_page_pointer(page_id: str, pages_by_id: dict[str, Any]) -> str:
    seen: set[str] = set()
    current = page_id
    for _ in range(_MAX_CHAIN_HOPS):
        if current in seen:
            return min(seen)
        seen.add(current)
        page = pages_by_id.get(current)
        if page is None:
            return page_id
        target = str(page.canonical_page_id)
        if target == current:
            return current
        current = target
    raise RuntimeError(f"canonical page pointer exceeds {_MAX_CHAIN_HOPS} hops")


def build_canonical_identity_plan(
    pages: list[PageIdentityNode],
    relations: list[UrlRelation],
    *,
    root_url: str,
) -> CanonicalIdentityPlan:
    """Build a deterministic, fully flattened page→canonical-page plan."""

    if not pages:
        return CanonicalIdentityPlan(relation_count=len(relations))

    by_id = {page.id: page for page in pages}
    by_url = {normalize_url(page.url): page for page in pages}
    parent = {page.id: page.id for page in pages}

    def find(page_id: str) -> str:
        while parent[page_id] != page_id:
            parent[page_id] = parent[parent[page_id]]
            page_id = parent[page_id]
        return page_id

    def union(left: str, right: str) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[max(left_root, right_root)] = min(left_root, right_root)

    match_groups: dict[str, list[PageIdentityNode]] = defaultdict(list)
    for page in pages:
        match_groups[url_match_key(page.url)].append(page)
        if page.canonical_page_id in by_id:
            union(page.id, page.canonical_page_id)
    for group in match_groups.values():
        for page in group[1:]:
            union(group[0].id, page.id)

    outgoing: dict[str, UrlRelation] = {}
    for relation in relations:
        source_url = normalize_url(relation.source_url)
        target_url = normalize_url(relation.target_url)
        source = by_url.get(source_url)
        target = by_url.get(target_url)
        if source is None or target is None:
            continue
        union(source.id, target.id)
        current = outgoing.get(source_url)
        candidate_key = (relation.observed_at, _relation_priority(relation.kind))
        current_key = (
            (current.observed_at, _relation_priority(current.kind))
            if current is not None
            else (datetime.min.replace(tzinfo=UTC), -1)
        )
        if candidate_key >= current_key:
            outgoing[source_url] = relation.model_copy(
                update={"source_url": source_url, "target_url": target_url}
            )

    relation_target_priority: dict[str, int] = defaultdict(int)
    for relation in outgoing.values():
        target = by_url.get(relation.target_url)
        if target is not None:
            relation_target_priority[target.id] = max(
                relation_target_priority[target.id],
                _relation_priority(relation.kind),
            )

    components: dict[str, list[PageIdentityNode]] = defaultdict(list)
    for page in pages:
        components[find(page.id)].append(page)

    cycles: set[frozenset[str]] = set()
    sink_votes: dict[str, int] = defaultdict(int)
    for page in pages:
        current_url = normalize_url(page.url)
        seen_urls: list[str] = []
        for _ in range(_MAX_CHAIN_HOPS):
            if current_url in seen_urls:
                cycle_urls = seen_urls[seen_urls.index(current_url) :]
                cycles.add(frozenset(cycle_urls))
                current_url = min(cycle_urls)
                break
            seen_urls.append(current_url)
            relation = outgoing.get(current_url)
            if relation is None or relation.target_url == current_url:
                break
            current_url = relation.target_url
        target = by_url.get(current_url)
        if target is not None:
            sink_votes[target.id] += 1

    root_host = (urlparse(normalize_url(root_url)).hostname or "").lower()

    def winner_rank(page: PageIdentityNode) -> tuple[Any, ...]:
        parsed = urlparse(normalize_url(page.url))
        first_seen = page.first_seen.astimezone(UTC)
        return (
            -sink_votes[page.id],
            -relation_target_priority[page.id],
            -(page.latest_snapshot_id is not None),
            -(page.deleted_at is None),
            -(parsed.scheme == "https"),
            -((parsed.hostname or "").lower() == root_host),
            first_seen,
            page.id,
        )

    canonical_by_page_id: dict[str, str] = {}
    canonical_url_by_page_id: dict[str, str] = {}
    for component in components.values():
        winner = min(component, key=winner_rank)
        canonical_url = normalize_url(winner.url)
        for page in component:
            canonical_by_page_id[page.id] = winner.id
            canonical_url_by_page_id[page.id] = canonical_url

    return CanonicalIdentityPlan(
        canonical_by_page_id=canonical_by_page_id,
        canonical_url_by_page_id=canonical_url_by_page_id,
        relation_count=len(relations),
        cycle_count=len(cycles),
    )


async def _load_site_pages(site_id: str) -> list[Any]:
    return await WebPage.filter(site_id=site_id).all(use_cache=False)


async def upsert_observed_page_urls(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    urls: Iterable[str],
    provenance: str,
    session_id: str | None = None,
    revived: list[RevivedDismissal] | None = None,
    fresh_observation: bool = True,
) -> dict[str, ResolvedPageUrl]:
    """Resolve observed URLs through the one canonical page matcher.

    ``session_id`` stamps dismissal-revive markers with the observing crawl
    session; ``revived`` is an optional caller-supplied collector that
    receives one :class:`RevivedDismissal` per previously-dismissed row this
    observation brought back — so callers can surface it loudly (never
    silent). ``fresh_observation=False`` is reserved for batch reconciliation
    over historical facts: it may ensure a missing identity exists, but it must
    not revive a dismissal or advance ``last_seen`` as though the URL had just
    been observed.
    """

    normalized_provenance = provenance.strip().lower()
    if normalized_provenance not in _PROVENANCES:
        raise ValueError(
            "page provenance must be gsc, sitemap, crawl, manual, ga4, or bing_webmaster"
        )
    normalized_urls = list(dict.fromkeys(normalize_url(url) for url in urls))
    if not normalized_urls:
        return {}

    pages = await _load_site_pages(site_id)
    pages_by_id = {str(page.id): page for page in pages}
    pages_by_url = {normalize_url(str(page.url)): page for page in pages}
    pages_by_match_key: dict[str, list[Any]] = defaultdict(list)
    for page in pages:
        pages_by_match_key[url_match_key(str(page.url))].append(page)

    now = utcnow()
    new_rows: list[dict[str, Any]] = []
    for normalized in normalized_urls:
        if normalized in pages_by_url:
            continue
        candidates = pages_by_match_key.get(url_match_key(normalized), [])
        candidate_ids = {
            _follow_page_pointer(str(candidate.id), pages_by_id) for candidate in candidates
        }
        canonical_id = min(candidate_ids) if candidate_ids else str(uuid4())
        page_id = canonical_id if not candidate_ids else str(uuid4())
        new_rows.append(
            {
                "id": page_id,
                "organization_id": organization_id,
                "created_by": user_id,
                "site_id": site_id,
                "url": normalized,
                "url_hash": url_hash(normalized),
                "path": urlparse(normalized).path or "/",
                "provenance": normalized_provenance,
                "status": "active",
                "first_seen": now,
                "last_seen": now,
                "canonical_page_id": canonical_id,
            }
        )

    if new_rows:
        for start in range(0, len(new_rows), _PAGE_BATCH_SIZE):
            batch = new_rows[start : start + _PAGE_BATCH_SIZE]
            async with transaction(WEB_DB_NAME):
                await WebPage.bulk_upsert(
                    batch,
                    on_conflict=["site_id", "url_hash"],
                    update_fields=["last_seen"],
                )

    pages = await _load_site_pages(site_id)
    pages_by_id = {str(page.id): page for page in pages}
    pages_by_url = {normalize_url(str(page.url)): page for page in pages}
    resolutions: dict[str, ResolvedPageUrl] = {}
    canonical_last_seen_ids: set[str] = set()
    revive_pages: dict[str, Any] = {}
    adopt_pages: dict[str, Any] = {}  # planned rows this observation makes real
    for normalized in normalized_urls:
        page = pages_by_url.get(normalized)
        if page is None:
            raise RuntimeError(f"page upsert did not return persisted URL {normalized}")
        canonical_id = _follow_page_pointer(str(page.id), pages_by_id)
        canonical = pages_by_id.get(canonical_id)
        if canonical is None:
            raise RuntimeError(f"page {page.id} points to missing canonical page {canonical_id}")
        if fresh_observation:
            canonical_last_seen_ids.add(canonical_id)
        resolutions[normalized] = ResolvedPageUrl(
            observed_url=normalized,
            observed_page_id=str(page.id),
            canonical_page_id=canonical_id,
            canonical_url=normalize_url(str(canonical.url)),
        )
        # A freshly OBSERVED page exists again: revive the alias row hit by
        # the observation and its canonical row if either was soft-deleted
        # (the upsert path cannot SET deleted_at to NULL, and last_seen
        # silently advancing on an invisible row hid the page forever).
        if fresh_observation:
            for revive_candidate in (page, canonical):
                if revive_candidate.deleted_at is not None:
                    revive_pages[str(revive_candidate.id)] = revive_candidate
                # THE ADOPTION. A `planned` row is a URL somebody INTENDED —
                # written by the plan/CMS before anything crawled it. The
                # `(site_id, url_hash)` arbiter above already made the upsert
                # find it instead of minting a duplicate; what is left is to
                # say the intent came true. Only a FRESH observation may do
                # this: a historical reconciliation pass must never promote a
                # page nobody has actually seen.
                if str(getattr(revive_candidate, "status", "") or "") == "planned":
                    adopt_pages[str(revive_candidate.id)] = revive_candidate
    for revive_page in revive_pages.values():
        # Dismissal memory: the user hid this row; it came back because the
        # crawler re-observed reality. The revive permanently records the
        # dismiss/revive cycle in metadata.dismissals — per-row
        # read-modify-write is fine at this frequency.
        revived_metadata = append_dismissal_marker(
            getattr(revive_page, "metadata", None),
            dismissed_at=revive_page.deleted_at,
            session_id=session_id,
        )
        await WebPage.update_where(
            {"id": str(revive_page.id)},
            deleted_at=None,
            metadata=revived_metadata,
        )
        dismissal_count = len(revived_metadata["dismissals"])
        logger.warning(
            "re-observed a page the user previously dismissed — reviving with "
            "dismissal memory: %s (dismissed_at=%s, cycles=%d, session=%s)",
            revive_page.url,
            revive_page.deleted_at,
            dismissal_count,
            session_id,
        )
        if revived is not None:
            revived.append(
                RevivedDismissal(
                    row_id=str(revive_page.id),
                    url=normalize_url(str(revive_page.url)),
                    dismissed_at=(
                        revive_page.deleted_at.isoformat()
                        if isinstance(revive_page.deleted_at, datetime)
                        else str(revive_page.deleted_at)
                    ),
                    dismissal_count=dismissal_count,
                )
            )
    if adopt_pages:
        # Loud, because a planned page going live is a real event in the plan
        # loop — the difference between "we intend to publish this" and "this
        # is published" — and nothing else announces it.
        logger.info(
            "adopting %d planned page row(s) on site %s — observed for the first "
            "time, advancing planned -> active: %s",
            len(adopt_pages),
            site_id,
            ", ".join(sorted(str(p.url) for p in adopt_pages.values())[:10]),
        )
        await WebPage.update_where(
            {"id__in": sorted(adopt_pages), "status": "planned"},
            status="active",
            first_seen=now,
            last_seen=now,
        )
    if canonical_last_seen_ids:
        await WebPage.update_where(
            {"id__in": sorted(canonical_last_seen_ids)},
            last_seen=now,
        )
    return resolutions


async def ensure_planned_page_urls(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    urls: Iterable[str],
) -> dict[str, str]:
    """Ensure a `web.page` anchor exists for each INTENDED URL. Returns
    ``{normalized_url: page_id}``.

    This is the plan-time twin of :func:`upsert_observed_page_urls`, and it
    exists because of Arman's one-source-of-truth ruling (2026-08-16): a page's
    SEO plan lives on ``web.page`` and only there, so the row has to be
    creatable BEFORE anything has ever fetched the URL — for a plan-born page,
    a CMS-authored page, or a page a human simply intends to build.

    It shares the identity machinery and NOTHING else:

    * the SAME ``normalize_url`` / ``url_hash`` / ``UNIQUE (site_id, url_hash)``
      arbiter, so the crawler later ADOPTS this row rather than minting a
      duplicate (the adoption itself is in ``upsert_observed_page_urls``);
    * ``status='planned'`` and ``provenance='manual'`` — intent, not evidence;
    * it NEVER advances ``last_seen``, never revives a dismissal, and never
      touches a row that already exists. An existing row of any status wins:
      observed reality always outranks a plan, and a page that is already
      ``active`` must not be dragged back to ``planned``.
    """

    normalized_urls = list(dict.fromkeys(normalize_url(url) for url in urls))
    if not normalized_urls:
        return {}

    pages = await _load_site_pages(site_id)
    pages_by_url = {normalize_url(str(page.url)): page for page in pages}
    pages_by_match_key: dict[str, list[Any]] = defaultdict(list)
    pages_by_id = {str(page.id): page for page in pages}
    for page in pages:
        pages_by_match_key[url_match_key(str(page.url))].append(page)

    now = utcnow()
    new_rows: list[dict[str, Any]] = []
    for normalized in normalized_urls:
        if normalized in pages_by_url:
            continue
        # An alias of a URL we already know is NOT a new page — point the new
        # row at the same canonical row the observed path would have chosen.
        candidates = pages_by_match_key.get(url_match_key(normalized), [])
        candidate_ids = {
            _follow_page_pointer(str(candidate.id), pages_by_id) for candidate in candidates
        }
        canonical_id = min(candidate_ids) if candidate_ids else str(uuid4())
        page_id = canonical_id if not candidate_ids else str(uuid4())
        new_rows.append(
            {
                "id": page_id,
                "organization_id": organization_id,
                "created_by": user_id,
                "site_id": site_id,
                "url": normalized,
                "url_hash": url_hash(normalized),
                "path": urlparse(normalized).path or "/",
                "provenance": "manual",
                "status": "planned",
                "first_seen": now,
                "last_seen": now,
                "canonical_page_id": canonical_id,
            }
        )

    if new_rows:
        from matrx_orm.operations.conflict_writes import bulk_insert_ignore

        for start in range(0, len(new_rows), _PAGE_BATCH_SIZE):
            batch = new_rows[start : start + _PAGE_BATCH_SIZE]
            async with transaction(WEB_DB_NAME):
                # DO NOTHING, deliberately — not DO UPDATE. A row that already
                # exists is REALITY (a crawl saw it, GSC reported it); planning
                # must never write over it, and an upsert here would drag an
                # `active` page's columns back to plan-time values and bump its
                # `version` under every optimistic-concurrency writer.
                await bulk_insert_ignore(
                    WebPage,
                    batch,
                    on_conflict=["site_id", "url_hash"],
                )
        pages_by_url = {
            normalize_url(str(page.url)): page for page in await _load_site_pages(site_id)
        }

    resolved: dict[str, str] = {}
    revive: dict[str, Any] = {}
    for normalized in normalized_urls:
        page = pages_by_url.get(normalized)
        if page is None:
            raise RuntimeError(f"planned page upsert did not return persisted URL {normalized}")
        resolved[normalized] = str(page.id)
        # The row exists but the user DISMISSED it. Planning the URL is that
        # same user saying the page should exist — a later, deliberate,
        # human statement, so the row comes back. Silently returning the
        # soft-deleted id instead would put the page's whole SEO plan on a row
        # every reader filters out, and nothing would say why it vanished.
        if page.deleted_at is not None:
            revive[str(page.id)] = page

    for page in revive.values():
        revived_metadata = append_dismissal_marker(
            getattr(page, "metadata", None),
            dismissed_at=page.deleted_at,
            reason="planned",
        )
        await WebPage.update_where({"id": str(page.id)}, deleted_at=None, metadata=revived_metadata)
        logger.warning(
            "a URL the user previously dismissed was PLANNED — reviving it with "
            "dismissal memory so its SEO plan has a visible home: %s "
            "(dismissed_at=%s, cycles=%d)",
            page.url,
            page.deleted_at,
            len(revived_metadata["dismissals"]),
        )
    return resolved


async def adopt_published_page_url(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    live_url: str,
    planned_url: str | None = None,
) -> str:
    """Return the one ``web.page`` row a newly-published page serves.

    A CMS publication is stronger than plan-time intent but is not crawl
    evidence.  When the plan and renderer use different public origins (for
    example ``https://example.com/about`` versus
    ``https://mymatrx.com/c/example/about``), publication adopts the existing
    ``planned`` row by the plan-derived URL and moves that SAME identity onto
    the actual live URL.  Only when no planned candidate exists does the
    canonical planned-row writer create the live-URL row.

    This function deliberately lives beside :func:`ensure_planned_page_urls`:
    it is the canonical URL-identity writer extending that seam, not a CMS-side
    reimplementation of ``normalize_url`` / ``url_hash``.
    """

    normalized_live = normalize_url(live_url)
    normalized_planned = normalize_url(planned_url) if planned_url else None
    pages = await _load_site_pages(site_id)
    pages_by_url = {normalize_url(str(page.url)): page for page in pages}

    # The linked plan node wins over URL-only matching.  This is the branch
    # that prevents domainless /c/{site} publication from minting a second row
    # beside the custom-domain row created while planning.
    planned_page = pages_by_url.get(normalized_planned) if normalized_planned else None
    live_page = pages_by_url.get(normalized_live)
    if planned_page is not None and str(planned_page.id) != str(getattr(live_page, "id", "")):
        if live_page is not None:
            raise RuntimeError(
                "published URL already belongs to a different web.page row: "
                f"planned={planned_page.id}, live={live_page.id}, url={normalized_live}"
            )
        if str(getattr(planned_page, "status", "") or "") != "planned":
            raise RuntimeError(
                "refusing to move an observed web.page onto a different published URL: "
                f"page={planned_page.id}, status={planned_page.status}, "
                f"planned_url={normalized_planned}, live_url={normalized_live}"
            )
        await WebPage.update_item(
            str(planned_page.id),
            url=normalized_live,
            url_hash=url_hash(normalized_live),
            path=urlparse(normalized_live).path or "/",
            status="active",
        )
        logger.info(
            "adopted planned page %s at CMS publish: %s -> %s",
            planned_page.id,
            normalized_planned,
            normalized_live,
        )
        return str(planned_page.id)

    if live_page is not None:
        if str(getattr(live_page, "status", "") or "") == "planned":
            await WebPage.update_where(
                {"id": str(live_page.id), "status": "planned"}, status="active"
            )
        return str(live_page.id)

    # Creation still goes through THE planned-row writer.  Publication then
    # advances intent to active without pretending a crawler observed it.
    ids_by_url = await ensure_planned_page_urls(
        site_id=site_id,
        organization_id=organization_id,
        user_id=user_id,
        urls=[normalized_live],
    )
    page_id = ids_by_url.get(normalized_live)
    if page_id is None:
        raise RuntimeError(f"published page writer returned no row for {normalized_live}")
    await WebPage.update_where({"id": page_id, "status": "planned"}, status="active")
    return page_id


def _crawl_observed_urls(
    requested_url: str,
    final_url: str,
    redirect_chain: list[dict[str, Any]],
    canonical_url: str | None,
    root_url: str,
) -> list[str]:
    urls = [requested_url]
    urls.extend(
        str(hop.get("url")) for hop in redirect_chain if isinstance(hop, dict) and hop.get("url")
    )
    urls.append(final_url)
    if canonical_url and _is_same_site(canonical_url, root_url):
        urls.append(canonical_url)
    return list(dict.fromkeys(normalize_url(url) for url in urls))


async def resolve_crawl_page_identity(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    root_url: str,
    requested_url: str,
    final_url: str,
    redirect_chain: list[dict[str, Any]],
    declared_canonical_url: str | None,
    session_id: str | None = None,
    revived: list[RevivedDismissal] | None = None,
) -> CrawlIdentityResolution:
    """Persist every crawl alias and return the one canonical page identity."""

    requested = normalize_url(requested_url)
    final = normalize_url(final_url)
    declared = (
        normalize_url(declared_canonical_url)
        if declared_canonical_url and _is_same_site(declared_canonical_url, root_url)
        else None
    )
    observed_urls = _crawl_observed_urls(
        requested,
        final,
        redirect_chain,
        declared,
        root_url,
    )
    target_url = declared or final
    target_existed = await WebPage.exists(
        site_id=site_id,
        url_hash=url_hash(target_url),
    )
    resolutions = await upsert_observed_page_urls(
        site_id=site_id,
        organization_id=organization_id,
        user_id=user_id,
        urls=observed_urls,
        provenance="crawl",
        session_id=session_id,
        revived=revived,
    )

    target_observation = resolutions[target_url]
    target_page_id = target_observation.observed_page_id
    now = utcnow()
    updates: list[dict[str, Any]] = []
    alias_ids: list[str] = []
    for observed_url in observed_urls:
        observation = resolutions[observed_url]
        page_id = observation.observed_page_id
        is_target = page_id == target_page_id
        updates.append(
            {
                "id": page_id,
                "canonical_page_id": target_page_id,
                "status": "active",
                "last_seen": now,
            }
        )
        if not is_target:
            alias_ids.append(page_id)
    deduped_updates = list({row["id"]: row for row in updates}.values())
    async with transaction(WEB_DB_NAME):
        updated = await bulk_update_by_pk(
            WebPage,
            deduped_updates,
            casts={
                "id": "uuid",
                "canonical_page_id": "uuid",
                "last_seen": "timestamptz",
            },
        )
    if updated != len(deduped_updates):
        raise RuntimeError(f"crawl identity updated {updated} of {len(deduped_updates)} URL rows")
    await WebPage.update_where(
        {"id": target_page_id},
        deleted_at=None,
        status="active",
    )
    return CrawlIdentityResolution(
        requested_url=requested,
        final_url=final,
        canonical_url=target_url,
        page_id=target_page_id,
        alias_page_ids=sorted(set(alias_ids)),
        canonical_was_new=not target_existed,
    )


def _relations_from_crawl_facts(
    crawl_urls: list[Any],
    snapshots: list[Any],
    *,
    root_url: str,
) -> list[UrlRelation]:
    relations: list[UrlRelation] = []
    for crawl_url in crawl_urls:
        source = crawl_url.normalized_url or crawl_url.raw_url
        target = crawl_url.final_url or source
        if not source or not target:
            continue
        observed_at = crawl_url.completed_at or crawl_url.created_at
        relations.append(
            UrlRelation(
                source_url=str(source),
                target_url=str(target),
                kind=(
                    "direct"
                    if normalize_url(str(source)) == normalize_url(str(target))
                    else "redirect"
                ),
                observed_at=observed_at,
                status_code=crawl_url.http_status,
            )
        )

    for snapshot in snapshots:
        observed_at = snapshot.captured_at or snapshot.created_at
        final_url = str(snapshot.final_url or "")
        extracted = snapshot.extracted if isinstance(snapshot.extracted, dict) else {}
        chain = extracted.get("redirect_chain")
        if isinstance(chain, list):
            valid_hops = [hop for hop in chain if isinstance(hop, dict) and hop.get("url")]
            hop_urls = [normalize_url(str(hop["url"])) for hop in valid_hops]
            targets = hop_urls[1:] + ([normalize_url(final_url)] if final_url else [])
            for hop, target in zip(valid_hops, targets, strict=False):
                relations.append(
                    UrlRelation(
                        source_url=str(hop["url"]),
                        target_url=target,
                        kind="redirect",
                        observed_at=observed_at,
                        status_code=(int(hop["status"]) if hop.get("status") is not None else None),
                    )
                )
        head_tags = snapshot.head_tags if isinstance(snapshot.head_tags, dict) else {}
        declared = head_tags.get("canonical_url")
        if (
            final_url
            and isinstance(declared, str)
            and declared
            and _is_same_site(declared, root_url)
        ):
            relations.append(
                UrlRelation(
                    source_url=final_url,
                    target_url=declared,
                    kind="canonical",
                    observed_at=observed_at,
                )
            )
    return relations


def _prepare_crawl_relations(
    crawl_urls: list[Any],
    snapshots: list[Any],
    *,
    root_url: str,
) -> tuple[list[UrlRelation], set[str]]:
    """Build and normalize historical relation evidence off the event loop."""

    relations = _relations_from_crawl_facts(
        crawl_urls,
        snapshots,
        root_url=root_url,
    )
    relation_urls = {
        normalize_url(url)
        for relation in relations
        for url in (relation.source_url, relation.target_url)
        if _is_same_site(url, root_url)
    }
    return relations, relation_urls


async def _merge_gsc_stats(
    *,
    site_id: str,
    canonical_by_page_id: dict[str, str],
) -> int:
    stats = await GscPageStat.filter(
        site_id=site_id,
        deleted_at__isnull=True,
    ).all(use_cache=False)
    groups: dict[tuple[str, Any], list[Any]] = defaultdict(list)
    alias_ids: list[str] = []
    for stat in stats:
        page_id = str(stat.page_id)
        canonical_id = canonical_by_page_id.get(page_id, page_id)
        groups[(canonical_id, stat.date)].append(stat)
        if canonical_id != page_id:
            alias_ids.append(str(stat.id))

    rows: list[dict[str, Any]] = []
    for (canonical_id, day), day_stats in groups.items():
        if not any(str(stat.page_id) != canonical_id for stat in day_stats):
            continue
        clicks = sum(int(stat.clicks or 0) for stat in day_stats)
        impressions = sum(int(stat.impressions or 0) for stat in day_stats)
        positioned = [
            (Decimal(str(stat.position)), int(stat.impressions or 0))
            for stat in day_stats
            if stat.position is not None
        ]
        positioned_impressions = sum(weight for _, weight in positioned)
        position = (
            sum(value * weight for value, weight in positioned) / Decimal(positioned_impressions)
            if positioned and positioned_impressions
            else (
                sum(value for value, _ in positioned) / Decimal(len(positioned))
                if positioned
                else None
            )
        )
        exemplar = day_stats[0]
        rows.append(
            {
                "organization_id": str(exemplar.organization_id),
                "created_by": str(exemplar.created_by) if exemplar.created_by else None,
                "site_id": site_id,
                "page_id": canonical_id,
                "date": day,
                "clicks": clicks,
                "impressions": impressions,
                "ctr": Decimal(clicks) / Decimal(impressions) if impressions else Decimal(0),
                "position": position,
            }
        )
    async with transaction(WEB_DB_NAME):
        for start in range(0, len(rows), _PAGE_BATCH_SIZE):
            await GscPageStat.bulk_upsert(
                rows[start : start + _PAGE_BATCH_SIZE],
                on_conflict=["page_id", "date"],
                update_fields=["clicks", "impressions", "ctr", "position"],
            )
        if alias_ids:
            await GscPageStat.delete_where(id__in=alias_ids)
    return len(alias_ids)


async def _merge_sitemap_memberships(
    *,
    site_id: str,
    canonical_by_page_id: dict[str, str],
) -> int:
    memberships = await WebPageSitemap.filter(
        site_id=site_id,
        deleted_at__isnull=True,
    ).all(use_cache=False)
    groups: dict[tuple[str, str], list[Any]] = defaultdict(list)
    alias_ids: list[str] = []
    for membership in memberships:
        page_id = str(membership.page_id)
        canonical_id = canonical_by_page_id.get(page_id, page_id)
        groups[(canonical_id, str(membership.sitemap_id))].append(membership)
        if canonical_id != page_id:
            alias_ids.append(str(membership.id))
    rows: list[dict[str, Any]] = []
    for (canonical_id, sitemap_id), group in groups.items():
        if not any(str(item.page_id) != canonical_id for item in group):
            continue
        exemplar = max(group, key=lambda item: item.last_seen or item.first_seen)
        rows.append(
            {
                "organization_id": str(exemplar.organization_id),
                "created_by": str(exemplar.created_by) if exemplar.created_by else None,
                "site_id": site_id,
                "page_id": canonical_id,
                "sitemap_id": sitemap_id,
                "lastmod": exemplar.lastmod,
                "changefreq": exemplar.changefreq,
                "priority": exemplar.priority,
                "first_seen": min(item.first_seen for item in group),
                "last_seen": max(
                    (item.last_seen for item in group if item.last_seen is not None),
                    default=None,
                ),
            }
        )
    async with transaction(WEB_DB_NAME):
        for start in range(0, len(rows), _PAGE_BATCH_SIZE):
            upserted = await WebPageSitemap.bulk_upsert(
                rows[start : start + _PAGE_BATCH_SIZE],
                on_conflict=["page_id", "sitemap_id"],
                update_fields=["lastmod", "changefreq", "priority", "last_seen"],
            )
            # Evidence moving onto the canonical row means the membership
            # exists again — a soft-deleted conflict target must revive
            # (upsert cannot SET deleted_at to NULL).
            revive_ids = [str(row.id) for row in upserted if row.deleted_at is not None]
            if revive_ids:
                await WebPageSitemap.update_where({"id__in": revive_ids}, deleted_at=None)
        if alias_ids:
            await WebPageSitemap.delete_where(id__in=alias_ids)
    return len(alias_ids)


async def _merge_page_intent(
    *,
    pages: list[Any],
    canonical_by_page_id: dict[str, str],
) -> int:
    pages_by_id = {str(page.id): page for page in pages}
    conflicts = 0
    updates: dict[str, dict[str, Any]] = {}
    scalar_fields = (
        "target_keyword",
        "meta_title_desired",
        "meta_description_desired",
        "seo_metrics_desired",
    )
    for page in pages:
        page_id = str(page.id)
        canonical_id = canonical_by_page_id.get(page_id, page_id)
        if canonical_id == page_id:
            continue
        canonical = pages_by_id[canonical_id]
        target_updates = updates.setdefault(canonical_id, {})
        for field in scalar_fields:
            alias_value = getattr(page, field, None)
            canonical_value = target_updates.get(field, getattr(canonical, field, None))
            if alias_value is None:
                continue
            if canonical_value is None:
                target_updates[field] = alias_value
            elif canonical_value != alias_value:
                conflicts += 1
        alias_desired = page.desired_values if isinstance(page.desired_values, dict) else {}
        canonical_desired = target_updates.get("desired_values") or (
            canonical.desired_values if isinstance(canonical.desired_values, dict) else {}
        )
        merged_desired = {**alias_desired, **canonical_desired}
        if merged_desired != canonical_desired:
            target_updates["desired_values"] = merged_desired
    for canonical_id, fields in updates.items():
        if fields:
            await WebPage.update_where({"id": canonical_id}, **fields)
    return conflicts


async def _report(
    on_progress: ProgressCallback | None,
    message: str,
    summary: UrlReconciliationSummary,
) -> None:
    if on_progress is not None:
        await on_progress(message, summary)


def _alias_visibility_updates(
    pages: list[PageIdentityNode],
    canonical_by_page_id: dict[str, str],
    *,
    dismissed_at: datetime,
) -> list[dict[str, object]]:
    """Dismiss live aliases without ever reviving historical canonical rows."""

    return [
        {
            "id": page.id,
            "deleted_at": dismissed_at,
        }
        for page in pages
        if canonical_by_page_id[page.id] != page.id and page.deleted_at is None
    ]


async def reconcile_site_urls(
    *,
    site_id: str,
    organization_id: str,
    user_id: str,
    root_url: str,
    on_progress: ProgressCallback | None = None,
) -> UrlReconciliationResult:
    """Recompute and flatten every URL alias for a site in bounded writes."""

    summary = UrlReconciliationSummary()
    pages = await _load_site_pages(site_id)
    crawl_urls = await WebCrawlUrl.filter(site_id=site_id).all(use_cache=False)
    snapshots = await WebSnapshot.filter(site_id=site_id).all(use_cache=False)
    relations, relation_urls = await asyncio.to_thread(
        _prepare_crawl_relations,
        crawl_urls,
        snapshots,
        root_url=root_url,
    )
    await upsert_observed_page_urls(
        site_id=site_id,
        organization_id=organization_id,
        user_id=user_id,
        urls=relation_urls,
        provenance="crawl",
        fresh_observation=False,
    )
    pages = await _load_site_pages(site_id)
    nodes = [
        PageIdentityNode(
            id=str(page.id),
            url=str(page.url),
            canonical_page_id=str(page.canonical_page_id),
            first_seen=page.first_seen,
            deleted_at=page.deleted_at,
            latest_snapshot_id=(str(page.latest_snapshot_id) if page.latest_snapshot_id else None),
        )
        for page in pages
    ]
    plan = await asyncio.to_thread(
        build_canonical_identity_plan,
        nodes,
        relations,
        root_url=root_url,
    )
    summary.pages_scanned = len(pages)
    summary.relations_scanned = plan.relation_count
    summary.cycles = plan.cycle_count

    pointer_updates = [
        {"id": page.id, "canonical_page_id": plan.canonical_by_page_id[page.id]}
        for page in nodes
        if page.canonical_page_id != plan.canonical_by_page_id[page.id]
    ]
    for start in range(0, len(pointer_updates), _PAGE_BATCH_SIZE):
        batch = pointer_updates[start : start + _PAGE_BATCH_SIZE]
        async with transaction(WEB_DB_NAME):
            updated = await bulk_update_by_pk(
                WebPage,
                batch,
                casts={"id": "uuid", "canonical_page_id": "uuid"},
            )
        if updated != len(batch):
            raise RuntimeError(f"canonical reconciliation updated {updated} of {len(batch)} pages")
    summary.aliases_matched = sum(
        page_id != canonical_id for page_id, canonical_id in plan.canonical_by_page_id.items()
    )
    summary.pointers_changed = len(pointer_updates)
    await _report(
        on_progress,
        (f"Matched {summary.aliases_matched} aliases across {summary.pages_scanned} URL rows…"),
        summary,
    )

    summary.intent_conflicts = await _merge_page_intent(
        pages=pages,
        canonical_by_page_id=plan.canonical_by_page_id,
    )
    summary.gsc_rows_moved = await _merge_gsc_stats(
        site_id=site_id,
        canonical_by_page_id=plan.canonical_by_page_id,
    )
    summary.sitemap_memberships_moved = await _merge_sitemap_memberships(
        site_id=site_id,
        canonical_by_page_id=plan.canonical_by_page_id,
    )

    now = utcnow()
    # Reconciliation may dismiss aliases, but historical facts are not a fresh
    # observation and therefore must NEVER revive a user-dismissed canonical
    # row. Fresh crawl/sitemap/GSC writers own revival and dismissal memory.
    visibility_updates = _alias_visibility_updates(
        nodes,
        plan.canonical_by_page_id,
        dismissed_at=now,
    )
    for start in range(0, len(visibility_updates), _PAGE_BATCH_SIZE):
        batch = visibility_updates[start : start + _PAGE_BATCH_SIZE]
        async with transaction(WEB_DB_NAME):
            await bulk_update_by_pk(
                WebPage,
                batch,
                casts={"id": "uuid", "deleted_at": "timestamptz"},
            )

    if summary.cycles:
        logger.error(
            "canonical URL reconciliation found %s redirect/canonical cycles for site %s",
            summary.cycles,
            site_id,
        )
    if summary.intent_conflicts:
        logger.error(
            "canonical URL reconciliation preserved canonical intent over %s alias conflicts "
            "for site %s",
            summary.intent_conflicts,
            site_id,
        )
    await _report(
        on_progress,
        (
            f"Moved {summary.gsc_rows_moved} GSC rows and "
            f"{summary.sitemap_memberships_moved} sitemap memberships."
        ),
        summary,
    )
    return UrlReconciliationResult(summary)


__all__ = [
    "CanonicalIdentityPlan",
    "CrawlIdentityResolution",
    "PageIdentityNode",
    "ProgressCallback",
    "ResolvedPageUrl",
    "UrlReconciliationResult",
    "UrlRelation",
    "build_canonical_identity_plan",
    "reconcile_site_urls",
    "resolve_crawl_page_identity",
    "upsert_observed_page_urls",
]
