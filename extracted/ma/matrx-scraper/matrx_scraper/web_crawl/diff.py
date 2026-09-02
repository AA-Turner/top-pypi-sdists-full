"""Run-over-run diff for canonical crawl sessions — DERIVED, never cached.

What changed between two crawls of the same site: which URLs appeared, which
disappeared, which came back, and which pages changed (status, title, meta
description, content hash, word count). Ported from the legacy
`aidream/services/scraper` reads (`diff_runs`, `get_previous_run`,
`list_site_diffs`, `get_site_diff`) as part of the one-crawler consolidation.

## Why there is no `site_run_diffs`-style cache table

The legacy stack precomputed every diff into `scraper.site_run_diffs` from a
plpgsql reconcile function, because its per-run page table
(`scraper.crawl_pages`) had no cheap way to answer "was this URL in the
previous run" — the answer needed a self-join over two runs' worth of
denormalized page rows plus a `canonical_url()` call per row, per request.

The canonical model does not have that problem. `web.page` is the per-URL
identity (one row per URL for the life of the site, carrying `first_seen` and
`canonical_page_id` alias flattening — the identity work the legacy function
redid on every call) and `web.crawl_url` is the per-session ledger of what the
crawl did with each URL. Both are indexed on exactly the keys a diff needs, so
one diff is four indexed reads plus an in-memory set comparison. The per-site
diff LIST is still four reads, because every session in the window is loaded in
ONE `session_id__in` query and the consecutive pairs are compared in memory.

A cache table here would buy nothing measurable and would add a write path, a
staleness class, and a reconcile trigger. If a site ever exceeds
`MAX_PAGES_PER_SESSION` fetched URLs in one session the diff reports
`truncated=True` rather than silently comparing a partial set — that is the
signal to revisit this decision, not a reason to pre-cache today.

## Why `web.crawl_url` and not `web.snapshot`

A snapshot exists only for a SUCCESSFUL capture. A page that returned 200 last
crawl and 404 today writes no snapshot at all (`persistence` records the
failure on `web.crawl_url` + `web.page` instead), so diffing snapshots would
lose every "this page broke" transition — the single most valuable thing a
run-over-run diff reports, and the basis of `pages_status_worse`.
`web.crawl_url` carries the terminal outcome of every URL the crawl attempted,
its observed `http_status`, and a pointer to the snapshot when there is one.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from matrx_utils import utcnow

from matrx_scraper.db.models_web import (
    CrawlSession as WebCrawlSession,
    CrawlUrl as WebCrawlUrl,
    Page as WebPage,
    Snapshot as WebSnapshot,
)
from matrx_scraper.web_crawl.contracts import (
    ChangedPage,
    CrawlDiff,
    CrawlDiffCounts,
    CrawlSessionRef,
    DiffPageRef,
    PreviousSessionResponse,
    SiteDiffList,
    SiteDiffSummary,
)
from matrx_scraper.web_crawl.persistence import WebCrawlRepository

logger = logging.getLogger(__name__)

# A `web.crawl_url` row with one of these outcomes means the crawl reached a
# terminal decision about a real page: it captured it, followed it to a final
# URL, or failed on it. Every one of those rows carries `page_id`. The other
# legal outcomes (`discovered`, `skipped`, `excluded`, `duplicate`,
# `cancelled`) are classification-time decisions about a URL the crawl never
# resolved to page state, and must NOT count as presence in the run.
ATTEMPTED_OUTCOMES = frozenset({"captured", "redirected", "failed"})

# Only a site-WIDE crawl is a meaningful diff baseline. A `page_fetch`,
# `bootstrap`, `analysis`, or `*_sync` session touches one page or none, so
# picking one as "the previous run" would report the entire site as removed.
# Mirrors `service._EXCLUSIVE_CRAWL_MODES`.
DIFFABLE_CRAWL_MODES = frozenset({"full", "list"})

# Per-session ceiling on fetched URLs pulled into a diff. Above it the diff
# reports `truncated=True` instead of silently comparing a partial set.
MAX_PAGES_PER_SESSION = 20_000
# Per-list ceiling on the added / removed / returned / changed arrays of one
# diff response. The COUNTS are always complete; only the arrays are capped,
# and `truncated` says so. Matches the legacy 500-row cap.
MAX_LIST_ITEMS = 500
# Batch sizes for the ledger scan and the `id__in` reads.
LEDGER_BATCH_SIZE = 2_000
ID_BATCH_SIZE = 200
# How many candidate sessions to scan when resolving "the previous crawl".
# Non-diffable modes (page fetches, syncs) are filtered in Python, so the scan
# must look past them.
PREVIOUS_SESSION_SCAN = 50
# Default / maximum window for the per-site diff list.
DEFAULT_SITE_DIFF_LIMIT = 20
MAX_SITE_DIFF_LIMIT = 50

_CHANGE_FIELDS = (
    "http_status",
    "title",
    "meta_description",
    "content_hash",
    "word_count",
)


@dataclass(slots=True)
class PageState:
    """One canonical page's observed state within ONE crawl session."""

    page_id: str
    url: str
    first_seen: datetime | None = None
    http_status: int | None = None
    title: str | None = None
    meta_description: str | None = None
    content_hash: str | None = None
    word_count: int | None = None


@dataclass(slots=True)
class SessionPages:
    """Everything one session contributes to a diff, keyed by canonical page id."""

    session_id: str
    pages: dict[str, PageState] = field(default_factory=dict)
    truncated: bool = False


# ---------------------------------------------------------------------------
# Pure shaping — no DB. The comparison lives here so it is testable without a
# database and reusable by any caller that already holds the page sets.


def _stat(session: WebCrawlSession, key: str) -> int | None:
    stats = session.stats if isinstance(session.stats, dict) else {}
    value = stats.get(key)
    return int(value) if isinstance(value, int) else None


def session_ref(session: WebCrawlSession, page_count: int | None = None) -> CrawlSessionRef:
    scope = session.scope if isinstance(session.scope, dict) else {}
    mode = scope.get("mode")
    return CrawlSessionRef(
        session_id=str(session.id),
        site_id=str(session.site_id),
        status=str(session.status),
        mode=str(mode) if mode is not None else None,
        started_at=session.started_at,
        finished_at=session.finished_at,
        pages=page_count,
        pages_fetched=_stat(session, "pages_fetched"),
        pages_failed=_stat(session, "pages_failed"),
    )


def session_ran_at(session: WebCrawlSession) -> datetime:
    """When this session actually ran — the newest-first ordering key.

    `finished_at` is the legacy key, but a session still running (or one that
    crashed without a terminal write) has none. Falling back to `started_at`
    then `created_at` keeps such a session in its real chronological place
    instead of sorting it to the very beginning of time.
    """

    for value in (session.finished_at, session.started_at, session.created_at):
        if value is not None:
            return value
    return datetime.min


def is_diffable(session: WebCrawlSession) -> bool:
    """True for a site-wide crawl — the only meaningful diff baseline."""

    scope = session.scope if isinstance(session.scope, dict) else {}
    return scope.get("mode") in DIFFABLE_CRAWL_MODES


def _status_class(status: int | None) -> str:
    if status is None:
        return "unknown"
    if 200 <= status <= 299:
        return "ok"
    if 300 <= status <= 399:
        return "redirect"
    return "error"


def compute_diff(
    *,
    site_id: str,
    base: SessionPages | None,
    compare: SessionPages,
    base_ref: CrawlSessionRef | None,
    compare_ref: CrawlSessionRef,
    boundary: datetime | None,
) -> CrawlDiff:
    """Pure page-set comparison of `compare` against `base`.

    `boundary` separates "this URL is brand new to the site" from "this URL
    came BACK": an added page whose `first_seen` predates it was already known
    to the site and is counted as `returned` as well as `added`. Callers pass
    the base session's run time, or None when there IS no base — nothing can
    return from a run that does not exist, and using the compare session's own
    start there would label every page a sitemap sync created "returned".
    """

    base_pages = base.pages if base is not None else {}
    compare_pages = compare.pages

    added_keys = sorted(set(compare_pages) - set(base_pages), key=lambda k: compare_pages[k].url)
    removed_keys = sorted(set(base_pages) - set(compare_pages), key=lambda k: base_pages[k].url)
    both_keys = sorted(set(base_pages) & set(compare_pages), key=lambda k: compare_pages[k].url)

    counts = CrawlDiffCounts(pages_added=len(added_keys), pages_removed=len(removed_keys))

    added: list[DiffPageRef] = []
    returned: list[DiffPageRef] = []
    for key in added_keys:
        state = compare_pages[key]
        ref = DiffPageRef(page_id=state.page_id, url=state.url, http_status=state.http_status)
        if len(added) < MAX_LIST_ITEMS:
            added.append(ref)
        if boundary is not None and state.first_seen is not None and state.first_seen < boundary:
            counts.pages_returned += 1
            if len(returned) < MAX_LIST_ITEMS:
                returned.append(ref)

    removed = [
        DiffPageRef(
            page_id=base_pages[key].page_id,
            url=base_pages[key].url,
            http_status=base_pages[key].http_status,
        )
        for key in removed_keys[:MAX_LIST_ITEMS]
    ]

    changed: list[ChangedPage] = []
    for key in both_keys:
        before = base_pages[key]
        after = compare_pages[key]
        changed_fields = [
            name for name in _CHANGE_FIELDS if getattr(before, name) != getattr(after, name)
        ]
        if not changed_fields:
            counts.pages_unchanged += 1
            continue
        counts.pages_changed += 1
        if "http_status" in changed_fields:
            before_class = _status_class(before.http_status)
            after_class = _status_class(after.http_status)
            if after_class == "error" and before_class in ("ok", "redirect"):
                counts.pages_status_worse += 1
            elif after_class == "ok" and before_class == "error":
                counts.pages_status_better += 1
        if len(changed) < MAX_LIST_ITEMS:
            changed.append(
                ChangedPage(
                    page_id=after.page_id,
                    url=after.url,
                    changed_fields=changed_fields,
                    http_status_before=before.http_status,
                    http_status_after=after.http_status,
                    title_before=before.title,
                    title_after=after.title,
                    meta_description_before=before.meta_description,
                    meta_description_after=after.meta_description,
                    content_hash_before=before.content_hash,
                    content_hash_after=after.content_hash,
                    word_count_before=before.word_count,
                    word_count_after=after.word_count,
                )
            )

    truncated = (
        compare.truncated
        or (base.truncated if base is not None else False)
        or counts.pages_added > len(added)
        or counts.pages_removed > len(removed)
        or counts.pages_changed > len(changed)
        or counts.pages_returned > len(returned)
    )
    return CrawlDiff(
        site_id=site_id,
        base=base_ref,
        compare=compare_ref,
        counts=counts,
        added=added,
        removed=removed,
        returned=returned,
        changed=changed,
        truncated=truncated,
        computed_at=utcnow(),
    )


# ---------------------------------------------------------------------------
# DB reads. Authorization is the caller's RLS-visible site/session read, and
# every query runs inside `repo.rls()` so Postgres — not this module — is the
# authority on what the caller may see. Same contract as `insights.py`.


async def _load_crawl_urls(session_ids: list[str]) -> dict[str, list[dict[str, Any]]]:
    """Terminal per-URL ledger rows for each session, oldest decision first."""

    grouped: dict[str, list[dict[str, Any]]] = {sid: [] for sid in session_ids}
    if not session_ids:
        return grouped
    # Keyset-paged on the ledger's own (session_id, sequence) uniqueness so a
    # large crawl is never pulled in one unbounded read.
    for session_id in session_ids:
        rows_for_session = grouped[session_id]
        last_sequence: int | None = None
        while True:
            filters: dict[str, Any] = {
                "session_id": session_id,
                "outcome__in": sorted(ATTEMPTED_OUTCOMES),
                "page_id__isnull": False,
                "deleted_at__isnull": True,
            }
            if last_sequence is not None:
                filters["sequence__gt"] = last_sequence
            rows = await (
                WebCrawlUrl.filter(**filters)
                .order_by("sequence")
                .limit(LEDGER_BATCH_SIZE)
                .values("page_id", "snapshot_id", "http_status", "sequence")
            )
            if not rows:
                break
            last_sequence = int(rows[-1]["sequence"])
            rows_for_session.extend(rows)
            if len(rows_for_session) > MAX_PAGES_PER_SESSION:
                break
            if len(rows) < LEDGER_BATCH_SIZE:
                break
    return grouped


async def _load_pages(page_ids: set[str]) -> dict[str, WebPage]:
    out: dict[str, WebPage] = {}
    ids = sorted(page_ids)
    for start in range(0, len(ids), ID_BATCH_SIZE):
        chunk = ids[start : start + ID_BATCH_SIZE]
        for page in await WebPage.filter(id__in=chunk).all():
            out[str(page.id)] = page
    return out


async def _load_snapshots(snapshot_ids: set[str]) -> dict[str, WebSnapshot]:
    out: dict[str, WebSnapshot] = {}
    ids = sorted(snapshot_ids)
    for start in range(0, len(ids), ID_BATCH_SIZE):
        chunk = ids[start : start + ID_BATCH_SIZE]
        for snap in await WebSnapshot.filter(id__in=chunk, deleted_at__isnull=True).all():
            out[str(snap.id)] = snap
    return out


def _head_tag(snapshot: WebSnapshot | None, key: str) -> str | None:
    if snapshot is None:
        return None
    head = snapshot.head_tags if isinstance(snapshot.head_tags, dict) else {}
    value = head.get(key)
    return value if isinstance(value, str) and value else None


async def build_session_pages(session_ids: list[str]) -> dict[str, SessionPages]:
    """Resolve each session's fetched URLs into canonical per-page state.

    Aliases are collapsed through `web.page.canonical_page_id` — the canonical
    model's standing answer to what the legacy stack recomputed with
    `scraper.canonical_url(...)` on every diff — so a URL crawled under two
    spellings is ONE page on both sides and never reports as added+removed.

    Must be called inside an `rls()` scope.
    """

    unique_ids = list(dict.fromkeys(session_ids))
    grouped = await _load_crawl_urls(unique_ids)

    page_ids: set[str] = set()
    snapshot_ids: set[str] = set()
    for rows in grouped.values():
        for row in rows:
            page_ids.add(str(row["page_id"]))
            if row["snapshot_id"] is not None:
                snapshot_ids.add(str(row["snapshot_id"]))

    pages = await _load_pages(page_ids)
    # A canonical target can be a page this session never fetched itself (an
    # alias was crawled, its canonical was not) — resolve those too, so every
    # diff key always has a real URL to display.
    canonical_ids = {
        str(page.canonical_page_id) for page in pages.values() if page.canonical_page_id is not None
    }
    missing_canonical = canonical_ids - set(pages)
    if missing_canonical:
        pages.update(await _load_pages(missing_canonical))
    snapshots = await _load_snapshots(snapshot_ids)

    out: dict[str, SessionPages] = {}
    for session_id in unique_ids:
        rows = grouped.get(session_id, [])
        result = SessionPages(session_id=session_id)
        if len(rows) > MAX_PAGES_PER_SESSION:
            logger.warning(
                "crawl session %s has more than %d fetched URLs — diff truncated",
                session_id,
                MAX_PAGES_PER_SESSION,
            )
            result.truncated = True
            rows = rows[:MAX_PAGES_PER_SESSION]
        for row in rows:
            page = pages.get(str(row["page_id"]))
            if page is None:
                # Soft-deleted or RLS-invisible page: it cannot be keyed or
                # displayed, so it is not comparable evidence.
                continue
            canonical_id = (
                str(page.canonical_page_id) if page.canonical_page_id is not None else str(page.id)
            )
            canonical = pages.get(canonical_id, page)
            snapshot = (
                snapshots.get(str(row["snapshot_id"])) if row["snapshot_id"] is not None else None
            )
            # Rows arrive oldest-first, so a later decision for the same
            # canonical page overwrites an earlier one — the same "keep the
            # most recent capture" rule the legacy `DISTINCT ON` applied.
            result.pages[canonical_id] = PageState(
                page_id=canonical_id,
                url=str(canonical.url),
                first_seen=canonical.first_seen,
                http_status=row["http_status"],
                title=_head_tag(snapshot, "title"),
                meta_description=_head_tag(snapshot, "meta_description"),
                content_hash=snapshot.content_hash if snapshot is not None else None,
                word_count=snapshot.word_count if snapshot is not None else None,
            )
        out[session_id] = result
    return out


async def _resolve_previous(session: WebCrawlSession) -> WebCrawlSession | None:
    """Most recent site-wide crawl of the same site that ran BEFORE this one.

    Must be called inside an `rls()` scope.
    """

    boundary = session_ran_at(session)
    candidates = await (
        WebCrawlSession.filter(site_id=str(session.site_id), deleted_at__isnull=True)
        .order_by("-created_at")
        .limit(PREVIOUS_SESSION_SCAN)
        .all()
    )
    earlier = [
        candidate
        for candidate in candidates
        if str(candidate.id) != str(session.id)
        and is_diffable(candidate)
        and session_ran_at(candidate) < boundary
    ]
    if not earlier:
        return None
    return max(earlier, key=session_ran_at)


async def _diff(
    base_session: WebCrawlSession | None,
    compare_session: WebCrawlSession,
) -> CrawlDiff:
    """Full page-level diff. Must be called inside an `rls()` scope."""

    session_ids = [str(compare_session.id)]
    if base_session is not None:
        session_ids.append(str(base_session.id))
    loaded = await build_session_pages(session_ids)
    compare_pages = loaded[str(compare_session.id)]
    base_pages = loaded.get(str(base_session.id)) if base_session is not None else None

    boundary = session_ran_at(base_session) if base_session is not None else None
    return compute_diff(
        site_id=str(compare_session.site_id),
        base=base_pages,
        compare=compare_pages,
        base_ref=(
            session_ref(base_session, len(base_pages.pages))
            if base_session is not None and base_pages is not None
            else None
        ),
        compare_ref=session_ref(compare_session, len(compare_pages.pages)),
        boundary=boundary,
    )


# ---------------------------------------------------------------------------
# Public loaders — one per route, `claims`-first like `insights.py`.


async def load_session_diff(
    claims: dict[str, Any],
    base_session_id: str,
    compare_session_id: str,
) -> CrawlDiff:
    """Diff two explicitly named sessions.

    Both must be readable by the caller and belong to the SAME site — diffing
    two sites' page sets would report every page of each as added/removed,
    which is noise dressed up as a finding.
    """

    repo = WebCrawlRepository(claims)
    base_session = await repo.assert_session_access(base_session_id)
    compare_session = await repo.assert_session_access(compare_session_id)
    if str(base_session.site_id) != str(compare_session.site_id):
        raise ValueError(
            f"crawl sessions {base_session_id} and {compare_session_id} belong to "
            "different sites and cannot be compared"
        )
    async with repo.rls():
        return await _diff(base_session, compare_session)


async def load_previous_session(
    claims: dict[str, Any],
    session_id: str,
) -> PreviousSessionResponse:
    """The baseline a 'what changed' widget should diff this session against."""

    repo = WebCrawlRepository(claims)
    session = await repo.assert_session_access(session_id)
    async with repo.rls():
        previous = await _resolve_previous(session)
    return PreviousSessionResponse(
        session_id=session_id,
        site_id=str(session.site_id),
        previous=session_ref(previous) if previous is not None else None,
    )


async def load_site_session_diff(
    claims: dict[str, Any],
    site_id: str,
    session_id: str,
) -> CrawlDiff:
    """Diff one of a site's sessions against its own predecessor.

    The canonical replacement for legacy `get_site_diff(site_id, run_id)` —
    same question, computed instead of read from a cache table.
    """

    repo = WebCrawlRepository(claims)
    session = await repo.assert_session_access(session_id)
    if str(session.site_id) != str(site_id):
        raise LookupError(f"crawl session {session_id} does not belong to site {site_id}")
    async with repo.rls():
        previous = await _resolve_previous(session)
        return await _diff(previous, session)


async def load_site_diffs(
    claims: dict[str, Any],
    site_id: str,
    *,
    limit: int = DEFAULT_SITE_DIFF_LIMIT,
) -> SiteDiffList:
    """Counts-only diff of each recent site-wide crawl against its predecessor.

    The canonical replacement for the legacy precomputed
    `scraper.site_run_diffs` LIST. Every session in the window is loaded in one
    pass and consecutive pairs are compared in memory, so the whole list costs
    the same handful of queries a single diff does.
    """

    window_size = max(1, min(int(limit), MAX_SITE_DIFF_LIMIT))
    repo = WebCrawlRepository(claims)
    await repo.site_root(site_id)

    async with repo.rls():
        candidates = await (
            WebCrawlSession.filter(site_id=site_id, deleted_at__isnull=True)
            .order_by("-created_at")
            .limit(window_size * 4 + PREVIOUS_SESSION_SCAN)
            .all()
        )
        ordered = sorted(
            (session for session in candidates if is_diffable(session)),
            key=session_ran_at,
            reverse=True,
        )
        # One extra session past the requested window, so the OLDEST reported
        # diff still has a real baseline instead of a fake "everything is new".
        window = ordered[: window_size + 1]
        if not window:
            return SiteDiffList(site_id=site_id, diffs=[])
        loaded = await build_session_pages([str(session.id) for session in window])

    summaries: list[SiteDiffSummary] = []
    for index, session in enumerate(window[:window_size]):
        previous = window[index + 1] if index + 1 < len(window) else None
        compare_pages = loaded[str(session.id)]
        base_pages = loaded.get(str(previous.id)) if previous is not None else None
        diff = compute_diff(
            site_id=site_id,
            base=base_pages,
            compare=compare_pages,
            base_ref=None,
            compare_ref=session_ref(session, len(compare_pages.pages)),
            boundary=session_ran_at(previous) if previous is not None else None,
        )
        summaries.append(
            SiteDiffSummary(
                site_id=site_id,
                session=session_ref(session, len(compare_pages.pages)),
                previous_session=(
                    session_ref(previous, len(base_pages.pages))
                    if previous is not None and base_pages is not None
                    else None
                ),
                counts=diff.counts,
                truncated=diff.truncated,
                computed_at=diff.computed_at,
            )
        )
    return SiteDiffList(site_id=site_id, diffs=summaries)


__all__ = [
    "ATTEMPTED_OUTCOMES",
    "DEFAULT_SITE_DIFF_LIMIT",
    "DIFFABLE_CRAWL_MODES",
    "MAX_LIST_ITEMS",
    "MAX_PAGES_PER_SESSION",
    "MAX_SITE_DIFF_LIMIT",
    "PageState",
    "SessionPages",
    "build_session_pages",
    "compute_diff",
    "is_diffable",
    "load_previous_session",
    "load_session_diff",
    "load_site_diffs",
    "load_site_session_diff",
    "session_ran_at",
    "session_ref",
]
