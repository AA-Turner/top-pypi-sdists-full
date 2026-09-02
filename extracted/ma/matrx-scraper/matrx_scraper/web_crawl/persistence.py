"""RLS-scoped persistence for the direct canonical crawler.

Every database operation uses matrx-orm against ``web.*``. Artifact bytes use
the canonical matrx-files/S3 pipeline and web rows retain only ``files.files``
UUIDs. There is no raw SQL and no legacy-storage fallback.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import socket
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any
from collections.abc import AsyncIterator, Awaitable, Callable
from urllib.parse import urlparse
from uuid import NAMESPACE_URL, UUID, uuid4, uuid5

from matrx_connect import AppContext, Emitter
from matrx_files import SCRAPER, FileManager
from matrx_files.cloud_sync.models import SyncResult
from matrx_files.service import FileService
from matrx_orm import IntegrityError, call_function, rls_session, transaction
from matrx_utils import utcnow

from matrx_scraper.crawler import (
    CapturedShot,
    PersistRequest,
    PersistResult,
    _normalise_url,
    resolve_body_artifact_format,
)

# Re-export, NEVER a second implementation: the stored-identity digest lives
# beside the normalizer it is derived from (`matrx_scraper.utils.url`). This
# module used to compute its own `sha256(_normalise_url(...))`, and
# `url_identity._url_hash` computed a third — three copies of one identity rule.
from matrx_scraper.utils.url import url_hash as url_hash
from matrx_scraper.audit_metrics import build_stored_audit_metrics
from matrx_scraper.meta_metrics import build_stored_seo_metrics
from matrx_scraper.db.models_web import (
    CrawlEvent as WebCrawlEvent,
    CrawlSession as WebCrawlSession,
    CrawlUrl as WebCrawlUrl,
    DiscoveredItem,
    LinkEdge as WebLinkEdge,
    Page as WebPage,
    PageEvidence as WebPageEvidence,
    Screenshot as WebScreenshot,
    Site as WebSite,
    Snapshot as WebSnapshot,
)
from matrx_scraper.db.web import WEB_DB_NAME
from matrx_scraper.events import (
    CrawlCompletedEvent,
    CrawlEvent,
    CrawlPageDiscoveredEvent,
    CrawlPageFailedEvent,
    CrawlPageFetchedEvent,
    CrawlProgressEvent,
    CrawlStartedEvent,
    CrawlUrlClassifiedEvent,
    CrawlUrlsClassifiedEvent,
    PageSummary,
)
from matrx_scraper.screenshot_dimensions import resolve_screenshot_dimensions
from matrx_scraper.web_crawl.broker import CrawlEventBroker
from matrx_scraper.web_crawl.candidates import DiscoveredCandidate, SiteIdentity
from matrx_utils.web_page_class import (
    HTML_CONTENT_TYPE,
    is_machine_resource,
)
from matrx_scraper.web_crawl.url_identity import (
    CrawlIdentityResolution,
    RevivedDismissal,
    resolve_crawl_page_identity,
)

AUTHENTICATED_ROLE = "authenticated"
logger = logging.getLogger(__name__)

# Screenshot retention: per (site_id, page_id, kind) keep the current capture
# plus at most this many priors. Everything older is soft-deleted (row AND
# files.files row) — storage purge belongs to the platform media machinery.
SCREENSHOT_HISTORY_KEEP_PRIOR = 3
# Canonical page presence is debounced: a page only becomes `gone` (and
# soft-deleted) after this many CONSECUTIVE authoritative misses (404s or
# coverage-qualified reconciliation misses). One flaky observation must never
# erase a page.
GONE_AFTER_CONSECUTIVE_MISSES = 3
STALE_SESSION_AFTER = timedelta(minutes=30)
STALE_SESSION_ERROR = (
    "Crawler service restarted or stopped receiving progress before this session "
    "could write a terminal status."
)
# A GRACEFUL shutdown (deploy, container stop) cancels the worker, which
# writes this marker. It is just as crash-shaped as a stale reap — the run
# died for infrastructure reasons, not because the crawl was wrong — so the
# boot sweep auto-resumes both. User cancellation never produces this: it
# finishes the run as `partial` via CrawlCompletedEvent(status="canceled").
WORKER_STOPPED_ERROR = "CancelledError: crawler worker stopped before completion"

# How a session came to exist. Mirrors the `crawl_session_trigger_valid` CHECK
# — a Python-side gate so a bad value names itself here instead of surfacing as
# an opaque integrity error one layer down.
SESSION_TRIGGERS = frozenset({"manual", "scheduled"})

# --- Cross-process run ownership (the run lease) ---------------------------
# A crawl session may have exactly ONE live run across the whole fleet. The
# lease is `metadata.run_lease` = {owner, epoch, acquired_at, heartbeat_at,
# host}; it is CLAIMED by a compare-and-swap on the row's `version` column
# (bumped by the platform `_touch_row` trigger on every UPDATE, so it is a
# real optimistic-lock discriminator that no application code has to maintain).
#
# Why: before this, `mark_session_resumed` was a blind update and the only
# double-run guard was the in-process broker registry. Two processes — the
# resume endpoint vs. a live run, or two containers' boot sweeps — could both
# seed from the same MAX(sequence), collide on
# `crawl_event_session_sequence_unique`, and the LOSER's error path would then
# mark the WINNER's session failed. Every terminal/status write is now gated on
# holding the lease, so a loser can only log, never corrupt.
#
# A lease is live while its holder is heartbeating. The TTL is deliberately the
# same window the stale-session reaper uses: "lease still live" and "the reaper
# would not have reaped it" must never disagree.
RUN_LEASE_TTL = STALE_SESSION_AFTER
RUN_LEASE_HEARTBEAT_EVERY = timedelta(seconds=30)
# Bounded re-read-and-retry for the event ledger's unique (session_id,
# sequence). Layer TWO under the lease: even if ownership is somehow shared,
# a sequence collision must be recoverable, never run-fatal.
EVENT_SEQUENCE_MAX_RETRIES = 8


def build_user_claims(ctx: AppContext) -> dict[str, Any]:
    """Build Postgres RLS claims from a JWT already verified by middleware."""

    if not ctx.is_authenticated or not ctx.user_id:
        raise PermissionError("direct web crawls require an authenticated Supabase user")
    claims: dict[str, Any] = {}
    if ctx.token:
        try:
            import jwt

            decoded = jwt.decode(
                ctx.token,
                options={"verify_signature": False, "verify_exp": False, "verify_aud": False},
            )
            if isinstance(decoded, dict):
                claims.update(decoded)
        except Exception:
            pass
    claims["sub"] = ctx.user_id
    claims["role"] = AUTHENTICATED_ROLE
    if ctx.email and not claims.get("email"):
        claims["email"] = ctx.email
    return claims


_REDIRECT_CHAIN_MAX_HOPS = 25


def crawl_url_fetch_metadata(redirect_chain: Any) -> dict[str, Any]:
    """Insert-time ``web.crawl_url.metadata`` for a fetched URL.

    Records the full hop chain (``{status, url}`` per hop, oldest first,
    final URL last — length 1 = no redirect) so redirect evidence survives
    for URLs that never get a snapshot: failures, redirect-to-404/410.
    Presence of the ``redirect_chain`` key — even as a 1-hop chain — is how
    report readers distinguish "no redirect happened" from "this crawl
    predates hop capture". Hop shape mirrors ``PageSummary.redirect_chain``
    and MUST stay readable by ``url_identity._relations_from_crawl_facts``.
    """
    hops: list[dict[str, Any]] = []
    if isinstance(redirect_chain, list):
        for hop in redirect_chain[:_REDIRECT_CHAIN_MAX_HOPS]:
            if not isinstance(hop, dict) or not hop.get("url"):
                continue
            status = hop.get("status")
            hops.append(
                {
                    "status": int(status) if isinstance(status, int | float) else None,
                    "url": str(hop["url"]),
                }
            )
    return {"redirect_chain": hops}


@dataclass(frozen=True)
class FailedFetchDisposition:
    """How one fetch failure may touch CANONICAL page state.

    Canonical presence changes ONLY on authoritative negative HTTP evidence:

    - ``410`` → immediate ``gone`` + soft delete (the origin declared the
      page intentionally removed).
    - ``404`` → debounced like coverage reconciliation: ``missing``
      immediately, ``gone`` (+ soft delete) only at
      ``GONE_AFTER_CONSECUTIVE_MISSES`` consecutive misses.
    - anything else (network/timeout/render/5xx/429) → NOT authoritative:
      the ``crawl_url`` failure outcome is recorded, but an existing page's
      status is never touched. A transient outage must not corrupt canonical
      state a prior successful crawl established.
    """

    authoritative: bool
    status: str | None
    soft_delete: bool
    consecutive_misses: int | None


@dataclass(frozen=True)
class ArtifactRef:
    """A snapshot's pointer to one stored artifact (body html or markdown).

    ``reused=True`` means the bytes were identical to the page's PREVIOUS
    capture, so this snapshot points at the previously stored ``files.files``
    object instead of a fresh copy (content-hash dedupe). Snapshot rows stay
    append-only either way — only the file reference dedupes.
    """

    file_id: str
    reused: bool = False


def failed_fetch_disposition(
    http_status: int | None, prior_consecutive_misses: int = 0
) -> FailedFetchDisposition:
    if http_status == 410:
        return FailedFetchDisposition(True, "gone", True, None)
    if http_status == 404:
        misses = max(0, int(prior_consecutive_misses)) + 1
        if misses >= GONE_AFTER_CONSECUTIVE_MISSES:
            return FailedFetchDisposition(True, "gone", True, misses)
        return FailedFetchDisposition(True, "missing", False, misses)
    return FailedFetchDisposition(False, None, False, None)


def _parse_event_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _as_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    if isinstance(value, str) and value:
        try:
            return _parse_event_time(value)
        except ValueError:
            return None
    return None


def read_run_lease(session: object) -> dict[str, Any]:
    """The session's `metadata.run_lease` (empty dict when it has never run)."""

    metadata = getattr(session, "metadata", None) or {}
    lease = metadata.get("run_lease") if isinstance(metadata, dict) else None
    return dict(lease) if isinstance(lease, dict) else {}


EVENT_SEQUENCE_CONSTRAINT = "crawl_event_session_sequence_unique"


def _is_event_sequence_collision(exc: BaseException) -> bool:
    """True only for a duplicate `(session_id, sequence)` on the event ledger.

    Narrow on purpose: every OTHER integrity error is a real bug and must keep
    failing the run. Matched on the constraint NAME in the driver's message —
    matrx-orm's `IntegrityError` reports the category (`unique`), the name
    lives in the wrapped error text.
    """

    details = getattr(exc, "details", None) or {}
    if details.get("constraint") not in (None, "unique"):
        return False
    return EVENT_SEQUENCE_CONSTRAINT in f"{details.get('original_error') or ''}{exc.args}"


def _warn_if_lease_lost(
    session_id: str, lease_token: str | None, rows_affected: int, intent: str
) -> bool:
    """Report whether a lease-gated session write landed — LOUDLY when it didn't.

    A suppressed write here is the guard doing its job (a losing process was
    stopped from stamping a terminal status over a live run), but it is never
    routine: it means two runs of one session existed at the same time.
    """

    if rows_affected:
        return True
    if not lease_token:
        # Unleased caller: nothing matched for an ordinary reason (deleted row).
        return False
    logger.error(
        "REFUSED to mark crawl session %s '%s': this process no longer holds the run "
        "lease (%s) — another run owns the session. Two runs of one session were live "
        "at the same time; investigate the caller that started the second one.",
        session_id,
        intent,
        lease_token,
    )
    return False


def _process_identity() -> str:
    """Host + pid of the process holding a lease — for the human reading a 409."""

    return f"{socket.gethostname()}:{os.getpid()}"


def _lease_filter(lease_token: str | None) -> dict[str, Any]:
    """Extra `update_where` filter that pins a write to the lease holder.

    Empty when the caller holds no token (legacy/unleased callers keep their
    previous unconditional behaviour); otherwise a JSONB containment test on
    `metadata @> {"run_lease": {"owner": <token>}}`, which the database
    re-evaluates at UPDATE time — so a process whose lease was stolen matches
    zero rows instead of overwriting the new owner's truth.
    """

    if not lease_token:
        return {}
    return {"metadata__json_contains": {"run_lease": {"owner": lease_token}}}


def _lease_signal_is_fresh(session: object, *, now: datetime | None = None) -> bool:
    """True when SOME process recently signalled ownership of this session,
    regardless of status — unlike `run_lease_is_live`, which only judges
    `running` rows. Used to decide whether a QUEUED session still has a live
    worker about to run it (a `prepare_start` claims the lease while the row
    is still queued) or is an orphan nothing will ever poll.

    Only LEASE signals count here — deliberately NOT the row's `updated_at`,
    which `run_lease_is_live` may use because a `running` session's progress
    events touch the row. A queued session emits no progress events, so its
    `updated_at` records write noise and nothing else — including the cancel
    stamp's own UPDATE. Counting it would make a stale-leased orphan read as
    live the moment anything wrote to the row, restoring the exact trap this
    path exists to close: a cooperative stamp nobody polls, bumping on every
    Cancel click the very freshness signal that blocks the next crawl.
    """
    lease = read_run_lease(session)
    if not lease.get("owner"):
        return False
    signals = [
        signal
        for signal in (
            _as_datetime(lease.get("heartbeat_at")),
            _as_datetime(lease.get("acquired_at")),
        )
        if signal is not None
    ]
    signal = max(signals, default=None)
    if signal is None:
        return False
    return (now or utcnow()) - signal < RUN_LEASE_TTL


def run_lease_is_live(session: object, *, now: datetime | None = None) -> bool:
    """True when another process is (or very recently was) running this session.

    Live means: status is `running`, a lease owner is recorded, and the run has
    signalled within `RUN_LEASE_TTL` — via its own heartbeat, or failing that
    the row's own `updated_at` (progress events touch the row, and a session
    written by an older build carries no heartbeat at all). Anything staler is
    a crash the reaper has claimed or will claim, and is free to resume.
    """

    if str(getattr(session, "status", "") or "") != "running":
        return False
    lease = read_run_lease(session)
    if not lease.get("owner"):
        # Pre-lease build, or a run that never claimed one. `running` + a fresh
        # `updated_at` still means someone is very likely on it — fail closed.
        signal = _as_datetime(getattr(session, "updated_at", None))
    else:
        signals = [
            signal
            for signal in (
                _as_datetime(lease.get("heartbeat_at")),
                _as_datetime(getattr(session, "updated_at", None)),
            )
            if signal is not None
        ]
        signal = max(signals, default=None)
    if signal is None:
        return False
    return (now or utcnow()) - signal < RUN_LEASE_TTL


@dataclass(frozen=True)
class DiscoveryFact:
    raw_url: str
    normalized_url: str
    depth: int
    parent_url: str | None
    source: str
    discovered_at: datetime


@dataclass(frozen=True)
class HomepageCapture:
    html: str
    summary: PageSummary
    page_id: str
    snapshot_id: str
    final_url: str


@dataclass
class CrawlPersistenceState:
    site_id: str
    session_id: str
    user_id: str
    organization_id: str
    file_owner_id: str
    coverage_qualified: bool
    homepage_bootstrap: bool = False
    site_initialization: bool = False
    brand_id: str | None = None
    homepage_capture: HomepageCapture | None = None
    discovered: dict[str, DiscoveryFact] = field(default_factory=dict)
    fetched: dict[str, CrawlPageFetchedEvent] = field(default_factory=dict)
    failed: dict[str, CrawlPageFailedEvent] = field(default_factory=dict)
    seen_hashes: set[str] = field(default_factory=set)
    # Pages whose consecutive-miss evidence was ALREADY written by this
    # session's failure path (authoritative 404/410). Coverage reconciliation
    # must skip these or the same crawl double-counts one miss.
    missed_hashes: set[str] = field(default_factory=set)
    new_pages: int = 0
    gone_pages: int = 0
    # Captures whose stored body bytes were identical to the page's previous
    # capture (content-hash dedupe): the snapshot row was appended, but it
    # points at the previously stored files instead of fresh copies.
    pages_unchanged: int = 0
    homepage_screenshot_id: str | None = None
    screenshots_expected: int = 0
    screenshots_captured: int = 0
    screenshots_persisted: int = 0
    url_sequence: int = 0
    # Starting point for the crawl_event sequence. Fresh sessions start at 0;
    # a RESUME seeds it from MAX(crawl_event.sequence) — the event sink
    # restarting at 0 minted a duplicate (session_id, 1) and IntegrityError'd
    # the resumed run on its very first event, permanently failing the session.
    event_sequence: int = 0
    # This run's ownership token (`metadata.run_lease.owner`). Every session
    # status/terminal write is gated on it, so a process that lost the race
    # can never mark the WINNER's session failed. None = unleased legacy path:
    # the guards degrade to their old unconditional behaviour.
    run_lease_token: str | None = None
    crawl_url_ids: dict[str, str] = field(default_factory=dict)
    page_identity_lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def record_discovery(self, event: CrawlPageDiscoveredEvent) -> None:
        normalized = _normalise_url(event.url)
        async with self.lock:
            self.discovered[normalized] = DiscoveryFact(
                raw_url=event.url,
                normalized_url=normalized,
                depth=event.depth,
                parent_url=event.parent_url,
                source=event.source,
                discovered_at=_parse_event_time(event.ts),
            )

    async def record_fetched(self, event: CrawlPageFetchedEvent) -> None:
        async with self.lock:
            self.fetched[_normalise_url(event.url)] = event

    async def record_failed(self, event: CrawlPageFailedEvent) -> None:
        async with self.lock:
            self.failed[_normalise_url(event.url)] = event

    async def failure_for(self, url: str) -> CrawlPageFailedEvent | None:
        async with self.lock:
            return self.failed.get(_normalise_url(url))

    async def discovery_for(self, url: str) -> DiscoveryFact:
        normalized = _normalise_url(url)
        async with self.lock:
            return self.discovered.get(
                normalized,
                DiscoveryFact(url, normalized, 0, None, "seed", utcnow()),
            )

    async def next_url_sequence(self) -> int:
        async with self.lock:
            self.url_sequence += 1
            return self.url_sequence

    async def reserve_url_sequences(self, count: int) -> list[int]:
        """Reserve `count` consecutive ledger sequence numbers in one hop."""
        if count <= 0:
            return []
        async with self.lock:
            start = self.url_sequence + 1
            self.url_sequence += count
            return list(range(start, self.url_sequence + 1))

    async def record_crawl_url(self, url: str, crawl_url_id: str) -> None:
        async with self.lock:
            self.crawl_url_ids[_normalise_url(url)] = crawl_url_id

    async def record_screenshots_expected(self, count: int) -> None:
        async with self.lock:
            self.screenshots_expected += count

    async def record_screenshots_captured(self, count: int) -> None:
        async with self.lock:
            self.screenshots_captured += count

    async def crawl_url_for(self, url: str) -> str | None:
        async with self.lock:
            return self.crawl_url_ids.get(_normalise_url(url))


class WebCrawlRepository:
    def __init__(self, claims: dict[str, Any]) -> None:
        self.claims = dict(claims)

    @asynccontextmanager
    async def rls(self) -> AsyncIterator[None]:
        async with rls_session(
            self.claims,
            role=AUTHENTICATED_ROLE,
            database=WEB_DB_NAME,
        ):
            yield

    async def assert_site_editor(self, site_id: str, user_id: str) -> None:
        """Require the canonical editor capability before mutating crawl state."""

        try:
            # ``iam.has_access_for`` is an internal helper and intentionally has
            # no EXECUTE grant for application roles.  The public authorization
            # primitive is ``iam.has_access``; it resolves the caller from the
            # JWT claims installed by ``rls_session``.  Keeping this call inside
            # the claim-bound session is essential: outside it the database
            # would see the scraper connection owner instead of the user whose
            # browser issued the command.
            async with self.rls():
                allowed = await call_function(
                    WEB_DB_NAME,
                    "iam",
                    "has_access",
                    "web_site",
                    UUID(site_id),
                    "editor",
                    mode="scalar",
                )
        except Exception as exc:
            raise PermissionError("site editor access could not be verified") from exc
        if not allowed:
            raise PermissionError("site editor access is required for crawler commands")

    async def create_session(
        self,
        site_id: str,
        *,
        scope: dict[str, Any],
        user_id: str,
        session_id: str | None = None,
        trigger: str = "manual",
    ) -> tuple[str, str, str, str]:
        if trigger not in SESSION_TRIGGERS:
            raise ValueError(
                f"crawl session trigger {trigger!r} is not one of {sorted(SESSION_TRIGGERS)}"
            )
        canonical_session_id = session_id or str(uuid4())
        # Authorization is the caller's RLS-visible site read.
        #
        # NOTE (verified live 2026-08-15): `authenticated` now holds the standard
        # component grant set on `web.crawl_session` — SELECT/INSERT/UPDATE/DELETE
        # under the `std_*` policies, gated on site-editor access. The foundation
        # migration's SELECT-only posture did NOT survive canonicalization, so a
        # client CAN insert a session row directly. That is safe only because a
        # row this service did not create carries no `scope.mode`, and
        # `_session_blocks_new_crawl` treats a modeless session as non-blocking
        # (it can never wedge the one-active-crawl gate) while the stale-session
        # reaper terminates it. Do not add a code path that trusts a session row
        # merely because it exists.
        async with self.rls():
            site = await WebSite.get_or_none(
                use_cache=False,
                id=site_id,
                deleted_at__isnull=True,
            )
            if site is None:
                raise LookupError(f"site {site_id} does not exist or is not accessible")
            root_url = str(site.root_url)
            organization_id = str(site.organization_id)
            if site.created_by is None:
                raise RuntimeError(f"site {site_id} has no canonical owner")
            file_owner_id = str(site.created_by)
        async with transaction(WEB_DB_NAME):
            await WebCrawlSession.create(
                id=canonical_session_id,
                organization_id=organization_id,
                created_by=user_id,
                site_id=site_id,
                status="queued",
                trigger=trigger,
                scope=scope,
                stats={},
            )
        return root_url, canonical_session_id, organization_id, file_owner_id

    async def site_root(self, site_id: str) -> str:
        async with self.rls():
            site = await WebSite.get_or_none(
                use_cache=False,
                id=site_id,
                deleted_at__isnull=True,
            )
            if site is None:
                raise LookupError(f"site {site_id} does not exist or is not accessible")
            return str(site.root_url)

    async def site_integrations(self, site_id: str) -> dict[str, Any]:
        async with self.rls():
            site = await WebSite.get_or_none(
                use_cache=False,
                id=site_id,
                deleted_at__isnull=True,
            )
            if site is None:
                raise LookupError(f"site {site_id} does not exist or is not accessible")
            integrations = site.integrations
            return dict(integrations) if isinstance(integrations, dict) else {}

    async def site_brand_id(self, site_id: str) -> str | None:
        async with self.rls():
            site = await WebSite.get_or_none(
                use_cache=False,
                id=site_id,
                deleted_at__isnull=True,
            )
            if site is None:
                raise LookupError(f"site {site_id} does not exist or is not accessible")
            return str(site.brand_id) if site.brand_id is not None else None

    async def update_initialization(
        self,
        site_id: str,
        summary: dict[str, Any],
        *,
        completed: bool = False,
    ) -> None:
        updates: dict[str, Any] = {"initialization": summary}
        if completed:
            updates["initialized_at"] = utcnow()
        async with transaction(WEB_DB_NAME):
            updated = await WebSite.update_where({"id": site_id}, **updates)
        if updated.rows_affected != 1:
            raise LookupError(f"site {site_id} could not be updated")

    async def update_site_identity(
        self,
        site_id: str,
        identity: SiteIdentity,
    ) -> dict[str, list[str]]:
        """Persist OBSERVED site identity, filling ONLY null/empty columns.

        ``description`` / ``favicon_url`` / ``og_image_url`` / ``logo_url``
        are user-editable; a non-null value the user may have set is NEVER
        overwritten. Returns ``{"written": [...], "skipped_existing": [...]}``.
        """

        desired: dict[str, str | None] = {
            "description": identity.description,
            "favicon_url": identity.favicon_url,
            "og_image_url": identity.og_image_url,
            "logo_url": identity.logo_url,
        }
        written: list[str] = []
        skipped_existing: list[str] = []
        async with transaction(WEB_DB_NAME):
            site = await WebSite.get_or_none(
                use_cache=False,
                id=site_id,
                deleted_at__isnull=True,
            )
            if site is None:
                raise LookupError(f"site {site_id} does not exist or is not accessible")
            updates: dict[str, str] = {}
            for field_name, value in desired.items():
                if value is None or not value.strip():
                    continue
                current = getattr(site, field_name, None)
                if current is None or (isinstance(current, str) and not current.strip()):
                    updates[field_name] = value
                    written.append(field_name)
                else:
                    skipped_existing.append(field_name)
            if updates:
                updated = await WebSite.update_where({"id": site_id}, **updates)
                if updated.rows_affected != 1:
                    raise LookupError(f"site {site_id} identity could not be updated")
        return {"written": written, "skipped_existing": skipped_existing}

    async def persist_discovered_items(
        self,
        state: CrawlPersistenceState,
        candidates: list[DiscoveredCandidate],
        *,
        snapshot_id: str,
    ) -> dict[str, int]:
        if not state.brand_id:
            raise ValueError("site has no brand_id; discovered candidates require a brand")

        rows: list[dict[str, Any]] = []
        counts: dict[str, int] = {}
        # In-batch dedupe MUST key on the same identity the DB dedup index
        # arbitrates: (category, guessed_kind, url, value) — value via its
        # canonical JSON, matching the stored generated ``value_hash``
        # (md5(value::text)) column. Without this, one batch can collide with
        # itself inside a single multi-row INSERT (ON CONFLICT cannot skip a
        # duplicate that arrives twice in the same statement).
        seen: set[tuple[str, str | None, str | None, str]] = set()
        for candidate in candidates:
            stable_value = json.dumps(
                candidate.value,
                sort_keys=True,
                separators=(",", ":"),
            )
            dedupe_key = (
                candidate.category,
                candidate.guessed_kind,
                candidate.url,
                stable_value,
            )
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            identity = "|".join(
                (
                    state.brand_id,
                    candidate.category,
                    candidate.guessed_kind,
                    candidate.url or "",
                    stable_value,
                )
            )
            rows.append(
                {
                    "id": str(uuid5(NAMESPACE_URL, f"matrx:web:discovered:{identity}")),
                    "organization_id": state.organization_id,
                    "created_by": state.user_id,
                    "brand_id": state.brand_id,
                    "site_id": state.site_id,
                    "snapshot_id": snapshot_id,
                    "source": "homepage_scrape",
                    "category": candidate.category,
                    "guessed_kind": candidate.guessed_kind,
                    "url": candidate.url,
                    "value": candidate.value,
                    "context": candidate.context,
                    "confidence": candidate.confidence,
                    "status": "pending",
                }
            )
            counts[candidate.category] = counts.get(candidate.category, 0) + 1

        if rows:
            # ``discovered_item_dedup`` is UNIQUE (brand_id, category,
            # guessed_kind, url, value_hash) NULLS NOT DISTINCT, where
            # ``value_hash`` is a STORED GENERATED column (md5(value::text)) —
            # it is never inserted, but it IS a valid ON CONFLICT arbiter
            # column, so two different facts with the same url (including
            # url IS NULL) no longer collide.
            await DiscoveredItem.bulk_insert_ignore(
                rows,
                on_conflict=["brand_id", "category", "guessed_kind", "url", "value_hash"],
            )
        return counts

    async def assert_session_access(self, session_id: str) -> WebCrawlSession:
        async with self.rls():
            session = await WebCrawlSession.get_or_none(
                use_cache=False,
                id=session_id,
                deleted_at__isnull=True,
            )
            if session is None:
                raise LookupError(f"crawl session {session_id} does not exist or is not accessible")
            return session

    async def mark_session_running(
        self, session_id: str, *, lease_token: str | None = None
    ) -> None:
        async with transaction(WEB_DB_NAME):
            await WebCrawlSession.update_where(
                {
                    "id": session_id,
                    "deleted_at__isnull": True,
                    **_lease_filter(lease_token),
                },
                status="running",
                started_at=utcnow(),
            )

    async def site_identity(self, site_id: str) -> tuple[str, str, str]:
        """(root_url, organization_id, file_owner_id) for a live site — the same
        facts create_session derives; a RESUME re-derives them from the site row
        because file_owner_id is deliberately not persisted on the session."""
        async with self.rls():
            site = await WebSite.get_or_none(use_cache=False, id=site_id, deleted_at__isnull=True)
            if site is None:
                raise LookupError(f"site {site_id} does not exist or is not accessible")
            if site.created_by is None:
                raise RuntimeError(f"site {site_id} has no canonical owner")
            return str(site.root_url), str(site.organization_id), str(site.created_by)

    async def max_url_sequence(self, session_id: str) -> int:
        """Highest crawl_url ledger sequence already written for a session.

        A resumed run MUST seed its in-memory sequence counter from this — a
        counter restarting at 0 would mint duplicate sequences in the ledger.
        """
        async with self.rls():
            row = (
                await WebCrawlUrl.filter(session_id=session_id)
                .order_by("-sequence")
                .limit(1)
                .first()
            )
            return int(row.sequence) if row is not None and row.sequence is not None else 0

    async def max_event_sequence(self, session_id: str) -> int:
        """Highest crawl_event sequence already written for a session.

        A resumed run MUST seed the event sink's counter from this — the sink
        restarting at 0 re-mints sequence 1, which violates
        `crawl_event_session_sequence_unique` on the resumed run's FIRST event
        and fails the whole resume (live incident 2026-07-30: two crashed
        crawls were permanently failed by their own recovery).
        """
        async with self.rls():
            row = (
                await WebCrawlEvent.filter(session_id=session_id)
                .order_by("-sequence")
                .limit(1)
                .first()
            )
            return int(row.sequence) if row is not None and row.sequence is not None else 0

    async def claim_run_lease(self, session_id: str, *, is_resume: bool) -> tuple[str, int]:
        """Take exclusive cross-process ownership of a session's run.

        ONE atomic compare-and-swap on the row's `version` (the platform
        `_touch_row` trigger bumps it on every UPDATE, so it is a genuine
        optimistic-lock discriminator): read the row, refuse if someone else's
        lease is live, then write the new lease pinned to the version we read.
        Zero rows affected means another process claimed it in the gap — that
        loser raises instead of running, which is the whole point.

        A resume also clears the stale terminal marks (`finished_at`/`error`
        written by fail_stale_sessions) and any leftover `cancel_request` (a
        resumed run must not insta-cancel on a flag from a previous life), and
        bumps the durable resume-attempt counter.

        Returns `(lease_token, resume_attempt)`. Raises `RuntimeError`
        ("already active") when a live lease is held elsewhere.
        """
        async with transaction(WEB_DB_NAME):
            session = await WebCrawlSession.get_or_none(
                use_cache=False, id=session_id, deleted_at__isnull=True
            )
            if session is None:
                raise LookupError(f"crawl session {session_id} does not exist")
            if run_lease_is_live(session):
                lease = read_run_lease(session)
                raise RuntimeError(
                    f"crawl session {session_id} is already active elsewhere "
                    f"(lease owner {lease.get('owner') or 'unknown'} on host "
                    f"{lease.get('host') or 'unknown'}, last heartbeat "
                    f"{lease.get('heartbeat_at') or session.updated_at}) — "
                    "wait for it to finish or crash before resuming"
                )
            observed_version = int(getattr(session, "version", None) or 0)
            metadata = dict(session.metadata or {})
            previous = read_run_lease(session)
            now = utcnow()
            token = str(uuid4())
            metadata["run_lease"] = {
                "owner": token,
                "epoch": int(previous.get("epoch") or 0) + 1,
                "acquired_at": now.isoformat(),
                "heartbeat_at": now.isoformat(),
                "host": _process_identity(),
            }
            updates: dict[str, Any] = {"status": "running", "started_at": now, "metadata": metadata}
            attempt = int((metadata.get("resume") or {}).get("attempts") or 0)
            if is_resume:
                metadata.pop("cancel_request", None)
                resume = dict(metadata.get("resume") or {})
                attempt = int(resume.get("attempts") or 0) + 1
                resume["attempts"] = attempt
                resume["last_resumed_at"] = now.isoformat()
                metadata["resume"] = resume
                updates["finished_at"] = None
                updates["error"] = None
            result = await WebCrawlSession.update_where(
                {"id": session_id, "deleted_at__isnull": True, "version": observed_version},
                **updates,
            )
            if not result.rows_affected:
                raise RuntimeError(
                    f"crawl session {session_id} is already active elsewhere — another "
                    "process claimed the run lease while this one was preparing"
                )
            return token, attempt

    async def heartbeat_run_lease(self, session_id: str, lease_token: str) -> bool:
        """Refresh this run's lease. False = we no longer hold it (stop working).

        The heartbeat is what makes `run_lease_is_live` meaningful for a crawl
        that goes quiet between progress events, and losing it is how a run
        that was declared dead learns to stop instead of fighting its successor.
        """

        async with transaction(WEB_DB_NAME):
            session = await WebCrawlSession.get_or_none(
                use_cache=False, id=session_id, deleted_at__isnull=True
            )
            if session is None:
                return False
            lease = read_run_lease(session)
            if lease.get("owner") != lease_token:
                return False
            metadata = dict(session.metadata or {})
            lease["heartbeat_at"] = utcnow().isoformat()
            metadata["run_lease"] = lease
            result = await WebCrawlSession.update_where(
                {
                    "id": session_id,
                    "deleted_at__isnull": True,
                    **_lease_filter(lease_token),
                },
                metadata=metadata,
            )
            return bool(result.rows_affected)

    @staticmethod
    async def list_crash_resumable_sessions(
        *, lookback: timedelta, limit: int
    ) -> list[WebCrawlSession]:
        """Sessions the boot sweep may auto-resume: failed for INFRASTRUCTURE
        reasons — reaped as stale (STALE_SESSION_ERROR) or gracefully cancelled
        by a shutdown/deploy (WORKER_STOPPED_ERROR) — recent, and not
        soft-deleted. Mode/cancel/attempt gates are enforced by prepare_resume
        per session (worker-owned read, no RLS — the sweep acts as each
        session's own creator). Deploys are the COMMON killer: without the
        WORKER_STOPPED_ERROR arm, every mid-crawl deploy permanently killed
        the crawl (observed live 2026-08-08)."""
        return (
            await WebCrawlSession.filter(
                status="failed",
                error__in=[STALE_SESSION_ERROR, WORKER_STOPPED_ERROR],
                deleted_at__isnull=True,
                finished_at__gte=utcnow() - lookback,
            )
            .order_by("-finished_at")
            .limit(limit)
            .all()
        )

    @staticmethod
    async def fail_stale_sessions() -> int:
        """Fail orphaned queued/running sessions after a scraper restart."""

        now = utcnow()
        result = await WebCrawlSession.update_where(
            {
                "status__in": ["queued", "running"],
                "updated_at__lt": now - STALE_SESSION_AFTER,
                "deleted_at__isnull": True,
            },
            status="failed",
            finished_at=now,
            error=STALE_SESSION_ERROR,
        )
        if result.rows_affected:
            logger.error(
                "reaped %s orphaned crawl session(s) left active by a prior process",
                result.rows_affected,
            )
        return result.rows_affected

    @staticmethod
    async def list_active_sessions_for_site(site_id: str) -> list[WebCrawlSession]:
        """Every non-deleted queued/running session on this site (worker-owned
        read). Callers decide which of them actually BLOCK a new start."""
        return await WebCrawlSession.filter(
            site_id=site_id,
            status__in=["queued", "running"],
            deleted_at__isnull=True,
        ).all(use_cache=False)

    @staticmethod
    async def abandon_duplicate_session(session_id: str, active_session_id: str) -> None:
        """Terminate a just-created session that lost the one-active-crawl
        race — a fresh queued row left behind would itself block every later
        start for STALE_SESSION_AFTER."""
        await WebCrawlSession.update_where(
            {"id": session_id},
            status="failed",
            finished_at=utcnow(),
            error=(
                f"start refused: crawl session {active_session_id} is already active for this site"
            ),
        )

    async def complete_session(
        self, session_id: str, stats: dict[str, Any], *, lease_token: str | None = None
    ) -> bool:
        async with transaction(WEB_DB_NAME):
            result = await WebCrawlSession.update_where(
                {
                    "id": session_id,
                    "deleted_at__isnull": True,
                    **_lease_filter(lease_token),
                },
                status="complete",
                stats=stats,
                finished_at=utcnow(),
            )
        return _warn_if_lease_lost(session_id, lease_token, result.rows_affected, "complete")

    async def fail_session(
        self, session_id: str, error: str, *, lease_token: str | None = None
    ) -> bool:
        """Mark the session failed — ONLY if we still own the run.

        This is the write that made the cross-process bug destructive: the
        process that LOST a race would land here and stamp `failed` over the
        winner's live session. Gated on the lease, a loser now writes nothing
        and screams instead.
        """

        async with transaction(WEB_DB_NAME):
            result = await WebCrawlSession.update_where(
                {
                    "id": session_id,
                    "deleted_at__isnull": True,
                    **_lease_filter(lease_token),
                },
                status="failed",
                finished_at=utcnow(),
                error=error[:4_000],
            )
        return _warn_if_lease_lost(session_id, lease_token, result.rows_affected, "failed")

    async def request_cancel(self, session_id: str, requested_by: str) -> None:
        """Persist a cross-worker cancellation signal after RLS authorization.

        A RUNNING (or freshly leased) session is cancelled cooperatively: the
        metadata stamp is polled by the run's cancel watcher. But a QUEUED
        session with no live lease has NO worker to poll it — a metadata-only
        stamp would never terminate it, and worse, the UPDATE bumps
        `updated_at`, which is exactly the freshness signal that blocks new
        crawl starts: every Cancel click EXTENDED the 30-minute block. Such a
        session is transitioned straight to terminal (`partial`, matching the
        canceled→partial mapping) so a new crawl can start immediately.
        """

        async with transaction(WEB_DB_NAME):
            session = await WebCrawlSession.get(use_cache=False, id=session_id)
            metadata = dict(session.metadata or {})
            metadata["cancel_request"] = {
                "requested": True,
                "requested_by": requested_by,
                "requested_at": utcnow().isoformat(),
            }
            if str(session.status or "") == "queued" and not _lease_signal_is_fresh(session):
                result = await WebCrawlSession.update_where(
                    # `status` in the filter: if a worker flipped it to
                    # running between our read and this write, fall through
                    # to the cooperative stamp instead of clobbering a live
                    # run's status.
                    {"id": session_id, "status": "queued"},
                    metadata=metadata,
                    status="partial",
                    finished_at=utcnow(),
                    error="cancelled by user before the crawl started",
                )
                if result.rows_affected:
                    logger.info(
                        "cancel terminated queued crawl session %s directly "
                        "(no live worker to poll the cancel request)",
                        session_id,
                    )
                    return
            await WebCrawlSession.update_where(
                {"id": session_id},
                metadata=metadata,
            )

    async def is_cancel_requested(self, session_id: str) -> bool:
        async with transaction(WEB_DB_NAME):
            session = await WebCrawlSession.get_or_none(
                use_cache=False,
                id=session_id,
                deleted_at__isnull=True,
            )
            if session is None:
                return False
            request = (session.metadata or {}).get("cancel_request") or {}
            return bool(request.get("requested"))

    async def persist_event(
        self,
        event: CrawlEvent,
        state: CrawlPersistenceState,
    ) -> None:
        """Append the event and apply its canonical side effect atomically."""

        if event.sequence is None or event.site_id is None or event.session_id is None:
            raise ValueError("canonical crawl event is missing site/session/sequence")

        async with transaction(WEB_DB_NAME):
            crawl_url_id: str | None = None
            # Every session-row write below is pinned to this run's lease: a
            # process that lost cross-process ownership may still append its
            # own event rows (they are a log), but it must never rewrite the
            # session's status, stats, or terminal outcome.
            session_filter = {"id": state.session_id, **_lease_filter(state.run_lease_token)}
            if isinstance(event, CrawlStartedEvent):
                await WebCrawlSession.update_where(
                    session_filter,
                    status="running",
                    started_at=_parse_event_time(event.ts),
                )
            elif isinstance(event, CrawlPageFailedEvent):
                await state.record_failed(event)
                crawl_url_id = await self._persist_failed_url_in_active_transaction(event, state)
            elif isinstance(event, CrawlProgressEvent):
                await WebCrawlSession.update_where(
                    session_filter,
                    stats=self._stats_from_progress(event, state),
                )
            elif isinstance(event, CrawlUrlClassifiedEvent):
                normalized = event.normalized_url or event.raw_url
                parent_page_id = None
                if event.parent_url:
                    parent_page = await WebPage.get_or_none(
                        use_cache=False,
                        site_id=state.site_id,
                        url_hash=url_hash(event.parent_url),
                        deleted_at__isnull=True,
                    )
                    parent_page_id = str(parent_page.id) if parent_page else None
                decision = await WebCrawlUrl.create(
                    organization_id=state.organization_id,
                    created_by=state.user_id,
                    site_id=state.site_id,
                    session_id=state.session_id,
                    sequence=await state.next_url_sequence(),
                    raw_url=event.raw_url,
                    normalized_url=event.normalized_url,
                    url_hash=url_hash(normalized),
                    discovery_source=event.source,
                    discovered_from_page_id=parent_page_id,
                    classification=event.classification,
                    outcome=event.outcome,
                    is_in_scope=event.is_in_scope,
                    depth=event.depth,
                    reason_code=event.reason_code,
                    reason=event.reason,
                    discovered_at=_parse_event_time(event.ts),
                    completed_at=_parse_event_time(event.ts),
                )
                crawl_url_id = str(decision.id)
            elif isinstance(event, CrawlUrlsClassifiedEvent):
                # The batched twin of the CrawlUrlClassifiedEvent branch above:
                # one page's entire URL decision set lands as ONE bulk insert.
                #
                # ONLY terminal-outcome decisions become ledger rows here —
                # rejects (excluded/skipped) and duplicates. An ACCEPTED URL is
                # NOT written now: its crawl_url row is created later, at fetch
                # time, with the real terminal outcome (captured/redirected/
                # failed — see the CrawlPageParsedEvent branch). Writing an
                # accepted row here both violates crawl_url_outcome_valid (no
                # 'accepted' member) and would double-write the ledger for every
                # fetched page. `accepted` stays on the event only for the live
                # counts, which the wire copy carries without the ledger.
                ledger_decisions = [d for d in event.decisions if d.outcome != "accepted"]
                if ledger_decisions:
                    parent_page_id = None
                    if event.parent_url:
                        parent_page = await WebPage.get_or_none(
                            use_cache=False,
                            site_id=state.site_id,
                            url_hash=url_hash(event.parent_url),
                            deleted_at__isnull=True,
                        )
                        parent_page_id = str(parent_page.id) if parent_page else None
                    discovered_at = _parse_event_time(event.ts)
                    sequences = await state.reserve_url_sequences(len(ledger_decisions))
                    rows = [
                        {
                            "organization_id": state.organization_id,
                            "created_by": state.user_id,
                            "site_id": state.site_id,
                            "session_id": state.session_id,
                            "sequence": sequence,
                            "raw_url": decision.raw_url,
                            "normalized_url": decision.normalized_url,
                            "url_hash": url_hash(decision.normalized_url or decision.raw_url),
                            "discovery_source": decision.source,
                            "discovered_from_page_id": parent_page_id,
                            "classification": decision.classification,
                            "outcome": decision.outcome,
                            "is_in_scope": decision.is_in_scope,
                            "depth": decision.depth,
                            "reason_code": decision.reason_code,
                            "reason": decision.reason,
                            "discovered_at": discovered_at,
                            "completed_at": discovered_at,
                        }
                        for sequence, decision in zip(sequences, ledger_decisions, strict=True)
                    ]
                    created = await WebCrawlUrl.bulk_create(rows)
                    for decision, row in zip(ledger_decisions, created, strict=True):
                        target = decision.normalized_url or decision.raw_url
                        await state.record_crawl_url(target, str(row.id))
            elif isinstance(event, CrawlCompletedEvent):
                state.coverage_qualified = state.coverage_qualified and event.coverage_complete
                reconciliation = await self._reconcile_in_active_transaction(state)
                status = {
                    "completed": "complete",
                    "canceled": "partial",
                    "failed": "failed",
                }[event.status]
                terminal = await WebCrawlSession.update_where(
                    session_filter,
                    status=status,
                    stats={
                        "pages_discovered": event.pages_discovered,
                        "pages_fetched": event.pages_fetched,
                        "pages_failed": event.pages_failed,
                        "pages_unchanged": state.pages_unchanged,
                        "bytes_downloaded": event.bytes_downloaded,
                        "duration_ms": event.duration_ms,
                        "termination": event.status,
                        "limit_reached": event.limit_reached,
                        "remaining_queue_depth": event.remaining_queue_depth,
                        "screenshots_expected": state.screenshots_expected,
                        "screenshots_captured": state.screenshots_captured,
                        "screenshots_persisted": state.screenshots_persisted,
                        "screenshots_failed": max(
                            0,
                            state.screenshots_expected - state.screenshots_persisted,
                        ),
                        "coverage_qualified": state.coverage_qualified,
                        "reconciliation": reconciliation,
                    },
                    finished_at=_parse_event_time(event.ts),
                    error=event.error_message,
                )
                _warn_if_lease_lost(
                    state.session_id,
                    state.run_lease_token,
                    terminal.rows_affected,
                    status,
                )

            page_id: str | None = None
            event_page = getattr(event, "page", None)
            if event_page is not None:
                page_id = getattr(event_page, "page_id", None)
                crawl_url_id = crawl_url_id or await state.crawl_url_for(event_page.url)
            await WebCrawlEvent.create(
                organization_id=state.organization_id,
                created_by=state.user_id,
                site_id=event.site_id,
                session_id=event.session_id,
                sequence=event.sequence,
                event_type=event.event_type,
                phase=self._event_phase(event),
                level=self._event_level(event),
                message=self._event_message(event),
                page_id=page_id,
                crawl_url_id=crawl_url_id,
                payload=event.model_dump(mode="json"),
                occurred_at=_parse_event_time(event.ts),
            )

    @staticmethod
    def _stats_from_progress(
        event: CrawlProgressEvent, state: CrawlPersistenceState
    ) -> dict[str, Any]:
        return {
            "pages_discovered": event.pages_discovered,
            "pages_fetched": event.pages_fetched,
            "pages_failed": event.pages_failed,
            # Captures byte-identical to the page's previous capture: the
            # snapshot appended but pointed at the previously stored files.
            # bytes_downloaded stays honest — it counts network download,
            # which dedupe does not change.
            "pages_unchanged": state.pages_unchanged,
            "pages_in_flight": event.pages_in_flight,
            "queue_depth": event.queue_depth,
            "bytes_downloaded": event.bytes_downloaded,
            "elapsed_ms": event.elapsed_ms,
            "screenshots_expected": state.screenshots_expected,
            "screenshots_captured": state.screenshots_captured,
            "screenshots_persisted": state.screenshots_persisted,
            "screenshots_failed": max(0, state.screenshots_expected - state.screenshots_persisted),
            "coverage_qualified": state.coverage_qualified,
        }

    async def _persist_failed_url_in_active_transaction(
        self,
        event: CrawlPageFailedEvent,
        state: CrawlPersistenceState,
    ) -> str:
        normalized = _normalise_url(event.url)
        digest = url_hash(normalized)
        discovery = await state.discovery_for(normalized)
        fetched = state.fetched.get(normalized)
        http_status = fetched.http_status if fetched else None
        content_type = fetched.mime_type if fetched else None
        page = await WebPage.get_or_none(
            use_cache=False,
            site_id=state.site_id,
            url_hash=digest,
        )
        now = _parse_event_time(event.ts)
        created = False
        if page is None:
            # A URL that has never succeeded may be born `missing` — there is
            # no established canonical state to protect.
            page = await WebPage.create(
                organization_id=state.organization_id,
                created_by=state.user_id,
                site_id=state.site_id,
                url=normalized,
                url_hash=digest,
                path=urlparse(normalized).path or "/",
                provenance="crawl",
                status="missing",
                first_seen=discovery.discovered_at,
                last_seen=now,
                http_status_last=http_status,
                content_type_last=content_type,
            )
            state.new_pages += 1
            created = True

        prior_misses = 0
        if http_status == 404 and not created:
            prior_misses = await self._prior_consecutive_misses(state, str(page.id))
        disposition = failed_fetch_disposition(http_status, prior_misses)

        if not created and page.deleted_at is None:
            if disposition.authoritative:
                await WebPage.update_where(
                    {"id": str(page.id)},
                    status=disposition.status,
                    http_status_last=http_status,
                    content_type_last=content_type,
                )
            elif http_status is not None:
                # Transient HTTP evidence (5xx/429): record the observed
                # status, but canonical presence/status stays exactly as the
                # last authoritative observation left it.
                await WebPage.update_where(
                    {"id": str(page.id)},
                    http_status_last=http_status,
                    content_type_last=content_type,
                )
            # Network/timeout/render failure (no status): page row untouched.

        outcome = "failed"
        if disposition.soft_delete and page.deleted_at is None:
            # Guarded on deleted_at: the page lookup above does NOT filter
            # soft-deleted rows, and re-soft-deleting an already-trashed page
            # would re-stamp its tombstone and inflate gone_pages.
            await WebPage.update_where({"id": str(page.id)}, status="gone")
            refreshed = await WebPage.get(use_cache=False, id=str(page.id))
            await refreshed.soft_delete()
            state.gone_pages += 1

        if disposition.authoritative:
            # This session has now recorded its ONE authoritative miss for
            # this page. Coverage reconciliation walks pages NOT seen this
            # session — without this marker it would re-read the evidence
            # this write just produced and count the same miss AGAIN (one
            # crawl = +2 misses; a persistently-404 page went gone on the
            # second crawl instead of the third).
            async with state.lock:
                state.missed_hashes.add(digest)

        parent_page_id = None
        if discovery.parent_url:
            parent_page = await WebPage.get_or_none(
                use_cache=False,
                site_id=state.site_id,
                url_hash=url_hash(discovery.parent_url),
                deleted_at__isnull=True,
            )
            parent_page_id = str(parent_page.id) if parent_page else None

        crawl_url = await WebCrawlUrl.create(
            organization_id=state.organization_id,
            created_by=state.user_id,
            site_id=state.site_id,
            session_id=state.session_id,
            sequence=await state.next_url_sequence(),
            page_id=str(page.id),
            raw_url=discovery.raw_url,
            normalized_url=normalized,
            url_hash=digest,
            discovery_source=discovery.source,
            discovered_from_page_id=parent_page_id,
            classification="internal",
            outcome=outcome,
            is_in_scope=True,
            depth=discovery.depth,
            http_status=http_status,
            final_url=fetched.final_url if fetched else None,
            metadata=crawl_url_fetch_metadata(
                getattr(fetched, "redirect_chain", None) if fetched else None
            ),
            reason_code=("http_410" if http_status == 410 else event.error_class)[:200],
            reason=f"{event.error_class}: {event.error_message}"[:2_000],
            discovered_at=discovery.discovered_at,
            completed_at=now,
        )
        evidence: dict[str, Any] = {
            "session_id": state.session_id,
            "crawl_url_id": str(crawl_url.id),
            "outcome": outcome,
            "http_status": http_status,
            "error_class": event.error_class,
        }
        if disposition.consecutive_misses is not None:
            evidence["consecutive_misses"] = disposition.consecutive_misses
        await self._record_page_evidence_in_active_transaction(
            state,
            str(page.id),
            # Only authoritative negatives (404/410) flip presence; a
            # transient failure records last_checked_at + this failure's
            # evidence while PRESERVING the prior presence verdict and its
            # consecutive-miss count.
            is_present=False if (disposition.authoritative or created) else None,
            observed_at=now,
            evidence=evidence,
        )
        await state.record_crawl_url(normalized, str(crawl_url.id))
        return str(crawl_url.id)

    async def _reconcile_in_active_transaction(
        self, state: CrawlPersistenceState
    ) -> dict[str, int]:
        missing = 0
        gone = 0
        if state.coverage_qualified:
            pages = await WebPage.filter(
                site_id=state.site_id,
                deleted_at__isnull=True,
            ).all()
            for page in pages:
                if (
                    page.url_hash not in state.seen_hashes
                    and page.url_hash not in state.missed_hashes
                    and page.status != "gone"
                ):
                    prior_evidence = await WebPageEvidence.get_or_none(
                        use_cache=False,
                        site_id=state.site_id,
                        page_id=str(page.id),
                        source_type="crawl",
                        source_binding_id__isnull=True,
                        external_key__isnull=True,
                        deleted_at__isnull=True,
                    )
                    prior_payload = (
                        prior_evidence.evidence
                        if prior_evidence is not None and isinstance(prior_evidence.evidence, dict)
                        else {}
                    )
                    consecutive_misses = int(prior_payload.get("consecutive_misses", 0) or 0) + 1
                    await WebPage.update_where(
                        {"id": str(page.id)},
                        status=(
                            "gone"
                            if consecutive_misses >= GONE_AFTER_CONSECUTIVE_MISSES
                            else "missing"
                        ),
                    )
                    await self._record_page_evidence_in_active_transaction(
                        state,
                        str(page.id),
                        is_present=False,
                        observed_at=utcnow(),
                        evidence={
                            "session_id": state.session_id,
                            "outcome": "missed_by_coverage_qualified_crawl",
                            "consecutive_misses": consecutive_misses,
                        },
                    )
                    if consecutive_misses >= GONE_AFTER_CONSECUTIVE_MISSES:
                        refreshed = await WebPage.get(use_cache=False, id=str(page.id))
                        await refreshed.soft_delete()
                        gone += 1
                    else:
                        missing += 1
        return {
            "new": state.new_pages,
            "seen": len(state.seen_hashes),
            "missing": missing,
            "gone": state.gone_pages + gone,
        }

    async def _prior_consecutive_misses(self, state: CrawlPersistenceState, page_id: str) -> int:
        """The consecutive-miss count carried in the page's crawl evidence.

        Reset to 0 by every successful capture (``is_present=True``); the
        404-debounce and coverage reconciliation both increment it.
        """
        existing = await WebPageEvidence.get_or_none(
            use_cache=False,
            site_id=state.site_id,
            page_id=page_id,
            source_type="crawl",
            source_binding_id__isnull=True,
            external_key__isnull=True,
            deleted_at__isnull=True,
        )
        payload = (
            existing.evidence
            if existing is not None and isinstance(existing.evidence, dict)
            else {}
        )
        try:
            return max(0, int(payload.get("consecutive_misses", 0) or 0))
        except (TypeError, ValueError):
            return 0

    async def _record_page_evidence_in_active_transaction(
        self,
        state: CrawlPersistenceState,
        page_id: str,
        *,
        is_present: bool | None,
        observed_at: datetime,
        evidence: dict[str, Any],
    ) -> None:
        """Refresh the page's crawl evidence row.

        ``is_present=None`` means "presence unknown" — a transient fetch
        failure. The check is recorded (``last_checked_at`` + evidence) but
        the prior presence verdict and its ``consecutive_misses`` count are
        PRESERVED, never overwritten by non-authoritative evidence.
        """
        if is_present:
            evidence = {**evidence, "consecutive_misses": 0}
        existing = await WebPageEvidence.get_or_none(
            use_cache=False,
            site_id=state.site_id,
            page_id=page_id,
            source_type="crawl",
            source_binding_id__isnull=True,
            external_key__isnull=True,
            deleted_at__isnull=True,
        )
        if existing is None:
            await WebPageEvidence.create(
                organization_id=state.organization_id,
                created_by=state.user_id,
                site_id=state.site_id,
                page_id=page_id,
                source_type="crawl",
                # A first-ever observation that failed transiently still has
                # no proof of presence.
                is_present=bool(is_present),
                first_seen_at=observed_at,
                last_seen_at=observed_at,
                last_checked_at=observed_at,
                evidence=evidence,
            )
            return
        if is_present is None:
            prior_payload = existing.evidence if isinstance(existing.evidence, dict) else {}
            if "consecutive_misses" in prior_payload:
                evidence = {
                    **evidence,
                    "consecutive_misses": prior_payload["consecutive_misses"],
                }
            await WebPageEvidence.update_where(
                {"id": str(existing.id)},
                last_checked_at=observed_at,
                evidence=evidence,
            )
            return
        updates: dict[str, Any] = {
            "is_present": is_present,
            "last_checked_at": observed_at,
            "evidence": evidence,
        }
        if is_present:
            updates["last_seen_at"] = observed_at
        await WebPageEvidence.update_where({"id": str(existing.id)}, **updates)

    @staticmethod
    def _event_phase(event: CrawlEvent) -> str:
        event_type = event.event_type
        if event_type in {"crawl_session_created", "crawl_started"}:
            return "session"
        if event_type in {"page_discovered", "url_classified"}:
            return "discovery"
        if event_type in {"page_fetched", "page_failed"}:
            return "fetch"
        if event_type in {"page_parsed", "issue_detected"}:
            return "analysis"
        if event_type == "crawl_progress":
            return "progress"
        return "complete" if event_type == "crawl_completed" else "crawl"

    @staticmethod
    def _event_level(event: CrawlEvent) -> str:
        if event.event_type == "crawl_warning":
            return "warning"
        if event.event_type == "page_failed":
            return "error"
        if isinstance(event, CrawlCompletedEvent) and event.status == "failed":
            return "error"
        return "info"

    @staticmethod
    def _event_message(event: CrawlEvent) -> str | None:
        if event.event_type == "crawl_warning":
            return str(getattr(event, "message", ""))[:2_000]
        if isinstance(event, CrawlPageFailedEvent):
            return f"{event.error_class}: {event.error_message}"[:2_000]
        if isinstance(event, CrawlCompletedEvent):
            return event.error_message
        return None


async def prune_screenshot_history(
    *,
    site_id: str,
    keys: set[tuple[str | None, str]],
    file_manager: FileManager,
) -> dict[str, int]:
    """Bounded screenshot retention for the given ``(page_id, kind)`` keys.

    Per key (``page_id`` may be None for site-level captures) the newest
    capture is current; up to ``SCREENSHOT_HISTORY_KEEP_PRIOR`` priors are
    kept. Anything older gets its ``web.screenshot`` row soft-deleted AND its
    ``files.files`` row soft-deleted (via the canonical cascade-aware
    primitive) so storage cleanup can follow — never hard-deleted here.
    Returns ``{"superseded": n, "pruned": n}``; per-row failures are counted
    in ``prune_failed`` and logged loudly instead of killing the capture that
    already persisted.
    """

    keep = 1 + SCREENSHOT_HISTORY_KEEP_PRIOR
    superseded = 0
    pruned = 0
    prune_failed = 0
    for page_id, kind in keys:
        filters: dict[str, Any] = {
            "site_id": site_id,
            "kind": kind,
            "deleted_at__isnull": True,
        }
        if page_id is None:
            filters["page_id__isnull"] = True
        else:
            filters["page_id"] = page_id
        rows = await WebScreenshot.filter(**filters).order_by("-created_at").all()
        superseded += max(0, len(rows) - 1)
        for row in rows[keep:]:
            try:
                async with transaction(WEB_DB_NAME):
                    await WebScreenshot.update_where(
                        {"id": str(row.id)},
                        deleted_at=utcnow(),
                    )
                if row.file_id is not None:
                    await file_manager.sync_engine.db.soft_delete_file_async(str(row.file_id))
                pruned += 1
            except Exception:
                prune_failed += 1
                logger.exception(
                    "screenshot retention prune failed for screenshot=%s file=%s "
                    "(site=%s page=%s kind=%s)",
                    row.id,
                    row.file_id,
                    site_id,
                    page_id,
                    kind,
                )
    counts = {"superseded": superseded, "pruned": pruned}
    if prune_failed:
        counts["prune_failed"] = prune_failed
    return counts


class CanonicalBodyPersister:
    """Write immutable S3 artifacts and their canonical snapshot rows."""

    def __init__(
        self,
        repository: WebCrawlRepository,
        state: CrawlPersistenceState,
        *,
        file_manager: FileManager,
        root_url: str | None = None,
    ) -> None:
        self.repository = repository
        self.state = state
        self.file_manager = file_manager
        self.files = FileService(file_manager)
        self.root_url = root_url

    async def _write_artifact(
        self,
        *,
        file_path: str,
        content: bytes | str,
        mime_type: str,
        artifact_kind: str,
        capture_id: str,
    ) -> SyncResult:
        payload = content.encode("utf-8") if isinstance(content, str) else content
        upload_kwargs = {
            "intent": "force_new_copy",
            "file_path": file_path,
            "owner_id": self.state.file_owner_id,
            "organization_id": self.state.organization_id,
            "mime_type": mime_type,
            # ORG-INTERNAL, never personal. A crawl artifact belongs to the
            # organization, not the individual who triggered the run — every
            # member (e.g. the marketing team) must be able to see it. `personal`
            # is owner-only and would hide crawl data from the org. This is a hard
            # product rule (Arman): crawler output is NEVER personal.
            "visibility": "internal",
            "change_summary": "Immutable web crawl capture",
            "metadata": {
                "organization_id": self.state.organization_id,
                "system_artifact": True,
                "system_immutable": True,
                "artifact_domain": "web_crawl",
                "artifact_kind": artifact_kind,
                "web_site_id": self.state.site_id,
                "crawl_session_id": self.state.session_id,
                "capture_id": capture_id,
                "capture_requested_by": self.state.user_id,
            },
            "reason": "Immutable web crawl capture requires a distinct file row",
            "auto_thumbnail": False,
            "auto_rekey": False,
        }
        upload = await self.files.upload_with_intent(payload, **upload_kwargs)
        result = upload.get("result")
        if not isinstance(result, SyncResult):
            raise RuntimeError(f"canonical file write returned no result for {file_path}")
        if not result.is_new:
            raise RuntimeError(f"immutable artifact reused an existing file row: {file_path}")
        if result.visibility != "internal":
            raise RuntimeError(
                f"crawler artifact must be org-internal, not {result.visibility!r}: "
                f"{result.file_id} (crawl output is never personal — the org must see it)"
            )
        if not result.storage_uri.startswith("s3://"):
            raise RuntimeError(
                f"crawler artifact used forbidden storage backend: {result.storage_uri}"
            )
        return result

    async def record_screenshots_expected(self, count: int) -> None:
        await self.state.record_screenshots_expected(count)

    async def record_screenshots_captured(self, count: int) -> None:
        await self.state.record_screenshots_captured(count)

    async def persist_initialization_screenshots(
        self,
        shots: list[CapturedShot],
        *,
        capture: HomepageCapture,
    ) -> tuple[dict[str, str], dict[str, int]]:
        captured_at = utcnow()
        # One immutable capture set per run. The DB guard
        # ``web.assert_crawl_artifact_file`` requires every screenshot
        # ``file_id`` to be a fresh ``files.files`` row carrying
        # ``system_immutable`` + ``artifact_domain=web_crawl`` metadata whose
        # ``crawl_session_id`` matches the snapshot's session — exactly what
        # ``_write_artifact`` produces. A managed/versioned write does NOT
        # satisfy that contract (its returned identity is not a fresh
        # ``files.files`` row), which is why this step previously failed in
        # production with CheckViolationError.
        capture_id = str(uuid4())
        written: list[tuple[str, SyncResult]] = []
        try:
            for shot in shots:
                file_path = SCRAPER.path(
                    "web",
                    self.state.site_id,
                    "sessions",
                    self.state.session_id,
                    "initialization",
                    f"{capture_id}-homepage-{shot.kind}.png",
                )
                result = await self._write_artifact(
                    file_path=file_path,
                    content=shot.bytes,
                    mime_type="image/png",
                    artifact_kind=f"screenshot:{shot.kind}",
                    capture_id=capture_id,
                )
                written.append((file_path, result))

            screenshot_ids: dict[str, str] = {}
            async with transaction(WEB_DB_NAME):
                # Append-only: every capture creates a NEW web.screenshot row
                # (newest wins — the frontend resolves the latest live row per
                # kind). Bounded history is enforced by the retention prune
                # below; the previous update-in-place behaviour left the prior
                # immutable file row floating with no referencing screenshot.
                for shot, (_, result) in zip(shots, written, strict=True):
                    width, height = resolve_screenshot_dimensions(
                        shot.width,
                        shot.height,
                        shot.bytes,
                    )
                    screenshot = await WebScreenshot.create(
                        organization_id=self.state.organization_id,
                        created_by=self.state.user_id,
                        site_id=self.state.site_id,
                        page_id=capture.page_id,
                        snapshot_id=capture.snapshot_id,
                        kind=shot.kind,
                        file_id=result.file_id,
                        width=width,
                        height=height,
                        captured_at=captured_at,
                        metadata={"initialization": True},
                    )
                    screenshot_ids[shot.kind] = str(screenshot.id)

                # site.homepage_screenshot_id is deliberately NOT written here.
                # The DB guard (web_marketing_integrity_contracts.sql) requires
                # that column to reference kind='homepage', and these captures
                # are the four responsive kinds. The frontend hero resolves the
                # latest screenshot by kind (desktop_fold preferred) directly —
                # only the bootstrap flow's genuine kind='homepage' capture may
                # stamp the column.
            self.state.screenshots_persisted += len(screenshot_ids)
            prune_counts = await prune_screenshot_history(
                site_id=self.state.site_id,
                keys={(capture.page_id, shot.kind) for shot in shots},
                file_manager=self.file_manager,
            )
            return screenshot_ids, prune_counts
        except asyncio.CancelledError:
            await asyncio.shield(self._purge_unreferenced(written))
            raise
        except Exception:
            await self._purge_unreferenced(written)
            raise

    async def _purge_unreferenced(
        self,
        artifacts: list[tuple[str, SyncResult]],
    ) -> None:
        for file_path, result in reversed(artifacts):
            if not result.is_new:
                continue
            try:
                # Transaction compensation is a trusted, exact-identity purge,
                # not a user file operation. A new contextual artifact has no
                # direct web artifact row yet, so the canonical access judge
                # correctly denies even its historical owner. The hard-delete
                # primitive removes the DB row first and leaves storage intact
                # if an FK proves that the artifact became referenced.
                await self.file_manager.sync_engine.hard_delete_and_purge_async(
                    result.file_id,
                    result.storage_uri,
                )
            except Exception:
                logger.exception(
                    "failed to purge unreferenced crawl artifact file_id=%s path=%s",
                    result.file_id,
                    file_path,
                )

    async def __call__(self, request: PersistRequest) -> PersistResult:
        summary = request.page_summary
        if summary is None:
            raise ValueError("canonical persistence requires page_summary")
        if not request.body:
            raise ValueError("canonical persistence requires a non-empty response body")
        if self.state.homepage_bootstrap and not request.screenshots:
            raise RuntimeError("homepage bootstrap did not produce a screenshot")

        revived_dismissals: list[RevivedDismissal] = []
        identity = await resolve_crawl_page_identity(
            site_id=self.state.site_id,
            organization_id=self.state.organization_id,
            user_id=self.state.user_id,
            root_url=self.root_url or request.url,
            requested_url=request.url,
            final_url=request.final_url or request.url,
            redirect_chain=summary.redirect_chain,
            declared_canonical_url=summary.canonical_url,
            session_id=self.state.session_id,
            revived=revived_dismissals,
        )
        normalized = identity.canonical_url
        digest = url_hash(normalized)

        # Content-hash dedupe (approved 2026-08-08): when the exact bytes we
        # would store are identical to the page's PREVIOUS capture, append the
        # snapshot row as usual (observation history stays truthful) but point
        # it at the previously stored files.files objects instead of writing
        # fresh copies. Body html and markdown hash + dedupe independently,
        # and comparison is ONLY against the page's current capture
        # (latest_snapshot_id) — its files are live by definition, and no
        # retention path deletes snapshot body/markdown files.
        body_bytes = request.body.encode("utf-8") if isinstance(request.body, str) else request.body
        body_sha = hashlib.sha256(body_bytes).hexdigest()
        markdown_sha: str | None = None
        if request.markdown:
            markdown_bytes = (
                request.markdown.encode("utf-8")
                if isinstance(request.markdown, str)
                else request.markdown
            )
            markdown_sha = hashlib.sha256(markdown_bytes).hexdigest()
        previous = await self._load_previous_snapshot(digest)
        prior_hashes: dict[str, Any] = {}
        if previous is not None and isinstance(previous.metadata, dict):
            prior_hashes = dict(previous.metadata.get("artifact_hashes") or {})
        reuse_body = bool(
            previous is not None and previous.body_file_id and previous.content_hash == body_sha
        )
        reuse_markdown = bool(
            previous is not None
            and previous.markdown_file_id
            and markdown_sha is not None
            and prior_hashes.get("markdown_sha256") == markdown_sha
        )
        artifact_hashes: dict[str, str] = {"body_sha256": body_sha}
        if markdown_sha is not None:
            artifact_hashes["markdown_sha256"] = markdown_sha

        capture_id = str(uuid4())
        prefix = SCRAPER.path(
            "web",
            self.state.site_id,
            "sessions",
            self.state.session_id,
            "pages",
            digest,
            "captures",
            capture_id,
        )
        written: list[tuple[str, SyncResult]] = []
        screenshot_artifacts: list[tuple[Any, SyncResult]] = []
        try:
            body_artifact: ArtifactRef | None = None
            markdown_artifact: ArtifactRef | None = None
            if request.body:
                if reuse_body and previous is not None:
                    # Identical bytes: point at the previous capture's file.
                    # Deliberately NOT appended to `written` — compensation
                    # (`_purge_unreferenced`) purges only newly written
                    # artifacts, so a failed persist can never touch a file an
                    # older snapshot still references.
                    body_artifact = ArtifactRef(file_id=str(previous.body_file_id), reused=True)
                else:
                    body_extension, body_mime = resolve_body_artifact_format(request.mime_type)
                    body_path = f"{prefix}/body.{body_extension}"
                    body_result = await self._write_artifact(
                        file_path=body_path,
                        content=request.body,
                        mime_type=body_mime,
                        artifact_kind="response_body",
                        capture_id=capture_id,
                    )
                    written.append((body_path, body_result))
                    body_artifact = ArtifactRef(file_id=body_result.file_id)
            if request.markdown:
                if reuse_markdown and previous is not None:
                    markdown_artifact = ArtifactRef(
                        file_id=str(previous.markdown_file_id), reused=True
                    )
                else:
                    markdown_path = f"{prefix}/body.md"
                    markdown_result = await self._write_artifact(
                        file_path=markdown_path,
                        content=request.markdown,
                        mime_type="text/markdown",
                        artifact_kind="markdown_body",
                        capture_id=capture_id,
                    )
                    written.append((markdown_path, markdown_result))
                    markdown_artifact = ArtifactRef(file_id=markdown_result.file_id)
            for shot in request.screenshots:
                shot_path = f"{prefix}/screenshot-{shot.kind}.png"
                shot_result = await self._write_artifact(
                    file_path=shot_path,
                    content=shot.bytes,
                    mime_type="image/png",
                    artifact_kind=f"screenshot:{shot.kind}",
                    capture_id=capture_id,
                )
                written.append((shot_path, shot_result))
                screenshot_artifacts.append((shot, shot_result))

            result = await self._persist_rows(
                request=request,
                identity=identity,
                normalized=normalized,
                digest=digest,
                body_artifact=body_artifact,
                markdown_artifact=markdown_artifact,
                artifact_hashes=artifact_hashes,
                reused_from_snapshot_id=(
                    str(previous.id)
                    if previous is not None and (reuse_body or reuse_markdown)
                    else None
                ),
                screenshot_artifacts=screenshot_artifacts,
                revived_dismissals=revived_dismissals,
            )
            if body_artifact is not None and body_artifact.reused:
                # Body bytes identical to the previous capture = an unchanged
                # page observation (markdown derives from the body).
                async with self.state.lock:
                    self.state.pages_unchanged += 1
            if screenshot_artifacts and result.page_id:
                canonical_kinds = {
                    (
                        "homepage"
                        if self.state.homepage_bootstrap
                        else "full"
                        if shot.kind == "full_page"
                        else "viewport"
                    )
                    for shot, _ in screenshot_artifacts
                }
                prune_counts = await prune_screenshot_history(
                    site_id=self.state.site_id,
                    keys={(result.page_id, kind) for kind in canonical_kinds},
                    file_manager=self.file_manager,
                )
                if prune_counts.get("pruned") or prune_counts.get("prune_failed"):
                    logger.info(
                        "screenshot retention for page %s: %s",
                        result.page_id,
                        prune_counts,
                    )
            if (
                self.state.site_initialization
                and isinstance(request.body, str)
                and resolve_body_artifact_format(request.mime_type)[1] == "text/html"
                and request.page_summary is not None
                and result.page_id
                and result.snapshot_id
            ):
                self.state.homepage_capture = HomepageCapture(
                    html=request.body,
                    summary=request.page_summary,
                    page_id=result.page_id,
                    snapshot_id=result.snapshot_id,
                    final_url=request.final_url,
                )
        except asyncio.CancelledError:
            await asyncio.shield(self._purge_unreferenced(written))
            raise
        except Exception:
            await self._purge_unreferenced(written)
            raise
        return result

    async def _load_previous_snapshot(self, digest: str) -> Any | None:
        """The page's CURRENT capture (``latest_snapshot_id``), if any.

        Content-hash dedupe compares ONLY against this snapshot — never an
        arbitrary older one — so a reused file is always one an undeleted,
        current snapshot references. No retention path deletes snapshot
        body/markdown files (screenshot retention prunes ONLY
        ``web.screenshot`` rows and their PNG files), which is the invariant
        that keeps shared references safe; any future snapshot-file retention
        MUST refcount ``artifact_reuse`` chains before touching storage.
        """
        page = await WebPage.get_or_none(
            use_cache=False,
            site_id=self.state.site_id,
            url_hash=digest,
        )
        latest_id = getattr(page, "latest_snapshot_id", None) if page is not None else None
        if not latest_id:
            return None
        return await WebSnapshot.get_or_none(
            use_cache=False,
            id=str(latest_id),
            deleted_at__isnull=True,
        )

    async def _persist_rows(
        self,
        *,
        request: PersistRequest,
        identity: CrawlIdentityResolution,
        normalized: str,
        digest: str,
        body_artifact: ArtifactRef | None,
        markdown_artifact: ArtifactRef | None,
        artifact_hashes: dict[str, str],
        reused_from_snapshot_id: str | None,
        screenshot_artifacts: list[tuple[Any, SyncResult]],
        revived_dismissals: list[RevivedDismissal] | None = None,
    ) -> PersistResult:
        summary = request.page_summary
        if summary is None:
            raise ValueError("canonical persistence requires page_summary")
        revived_dismissals = revived_dismissals or []

        captured_at = utcnow()
        # An HTML response served from a machine endpoint (a WordPress REST
        # error page, a feed rendered as HTML) is still not a page a human
        # visits — never score it. ONE rule: matrx_utils.web_page_class.
        audit_eligible = summary.mime_type == HTML_CONTENT_TYPE and not is_machine_resource(
            identity.requested_url, summary.mime_type
        )
        discovery = await self.state.discovery_for(request.url)
        async with self.state.page_identity_lock:
            async with transaction(WEB_DB_NAME):
                page = await WebPage.get_or_none(
                    use_cache=False,
                    id=identity.page_id,
                    site_id=self.state.site_id,
                )
                created = identity.canonical_was_new
                if page is None:
                    page = await WebPage.create(
                        id=identity.page_id,
                        organization_id=self.state.organization_id,
                        created_by=self.state.user_id,
                        site_id=self.state.site_id,
                        url=normalized,
                        url_hash=digest,
                        path=urlparse(normalized).path or "/",
                        provenance="crawl",
                        status="active",
                        first_seen=discovery.discovered_at,
                        last_seen=captured_at,
                        http_status_last=summary.http_status,
                        content_type_last=summary.mime_type,
                        canonical_page_id=identity.page_id,
                    )
                elif page.deleted_at is not None:
                    await WebPage.update_where(
                        {"id": str(page.id)},
                        deleted_at=None,
                        status="active",
                    )

                snapshot = await WebSnapshot.create(
                    organization_id=self.state.organization_id,
                    created_by=self.state.user_id,
                    site_id=self.state.site_id,
                    page_id=str(page.id),
                    session_id=self.state.session_id,
                    captured_at=captured_at,
                    final_url=identity.final_url,
                    http_status=summary.http_status,
                    content_hash=artifact_hashes["body_sha256"],
                    word_count=summary.word_count,
                    body_file_id=body_artifact.file_id if body_artifact else None,
                    markdown_file_id=markdown_artifact.file_id if markdown_artifact else None,
                    # `artifact_hashes` makes markdown dedupe possible on the
                    # NEXT capture; `artifact_reuse` is the opt-in marker the
                    # DB guard (0306) validates reused references under, and
                    # the durable record of which snapshot the bytes came
                    # from.
                    metadata={
                        "artifact_hashes": artifact_hashes,
                        **(
                            {
                                "artifact_reuse": {
                                    "body": bool(body_artifact and body_artifact.reused),
                                    "markdown": bool(
                                        markdown_artifact and markdown_artifact.reused
                                    ),
                                    "reused_from_snapshot_id": reused_from_snapshot_id,
                                }
                            }
                            if reused_from_snapshot_id
                            else {}
                        ),
                    },
                    head_tags={
                        "title": summary.title,
                        "meta_description": summary.meta_description,
                        "meta_robots": summary.meta_robots,
                        "canonical_url": summary.canonical_url,
                        "lang": summary.lang,
                        "hreflang": [item.model_dump(mode="json") for item in summary.hreflang],
                        "og": summary.og_tags,
                        "twitter": summary.twitter_tags,
                        # {"viewport", "refresh"} — absent (None) when the
                        # capture never parsed HTML, which the viewport and
                        # meta-refresh checks read as "not measured".
                        "meta": summary.head_meta,
                    },
                    # Audit metrics describe an HTML PAGE. A machine resource
                    # (JSON/XML endpoint, asset) has no og: tags and no <h1>, so
                    # scoring it manufactures errors on a URL nobody publishes.
                    # ONE rule — matrx_utils.web_page_class.
                    # Deterministic SERP metrics for the OBSERVED metadata —
                    # contract v1 (matrx-frontend migrations/web_seo_metrics.sql).
                    # Same char-width table as the frontend evaluator, so the
                    # stored numbers never depend on who computed them.
                    seo_metrics=(
                        build_stored_seo_metrics(
                            summary.title or "",
                            summary.meta_description or "",
                            source="scraper",
                        )
                        if audit_eligible
                        else None
                    ),
                    # Deterministic page audit (social card / headings /
                    # indexability) — contract v1 (matrx-frontend
                    # migrations/web_audit_metrics.sql), mirrored by
                    # features/seo/audit/ in the browser.
                    audit_metrics=(
                        build_stored_audit_metrics(
                            og_tags=summary.og_tags,
                            twitter_tags=summary.twitter_tags,
                            headings=[
                                item.model_dump(mode="json") for item in summary.headings_full
                            ],
                            http_status=summary.http_status,
                            meta_robots=summary.meta_robots,
                            canonical_url=summary.canonical_url,
                            redirect_chain=summary.redirect_chain,
                            final_url=identity.final_url,
                            url=identity.requested_url,
                            source="scraper",
                        )
                        if audit_eligible
                        else None
                    ),
                    headings={
                        "h1": summary.h1,
                        "h2": summary.h2,
                        "h1_count": summary.h1_count,
                        "all": [item.model_dump(mode="json") for item in summary.headings_full],
                    },
                    links_summary={
                        "internal": summary.internal_links,
                        "external": summary.external_links,
                        "total": summary.link_count,
                    },
                    images={
                        "count": summary.images_count,
                        "missing_alt": summary.images_missing_alt,
                        "items": summary.image_inventory,
                    },
                    structured_data=summary.structured_data
                    or {
                        "schema_org": summary.schema_org,
                        "schema_types": summary.schema_types,
                    },
                    perf={
                        # Two DIFFERENT measurements, never interchangeable:
                        # response_time_ms is the whole fetch (server + body
                        # download); ttfb_ms is the server's own latency, and
                        # is what `ttfb_server_response` grades. A snapshot
                        # written before 2026-08-09 has no ttfb_ms key at all,
                        # which the check reads as "not measured".
                        "response_time_ms": summary.response_time_ms,
                        "ttfb_ms": summary.ttfb_ms,
                        "bytes": summary.bytes,
                    },
                    extracted={
                        "sentence_count": summary.sentence_count,
                        # UTF-8 bytes of the same visible text `word_count`
                        # counts — the numerator of the text_html_ratio check
                        # (its denominator is perf.bytes, the raw HTML).
                        "text_bytes": summary.text_bytes,
                        "flesch_reading_ease": summary.flesch_reading_ease,
                        "text_hash": summary.text_hash,
                        # Versioned duplicate-detection fingerprint
                        # (exact_sha256 + simhash64 hex) — computed at capture
                        # time by parser/hashing.compute_text_fingerprint and
                        # read by the frontend content report's duplicate
                        # clustering. None for empty/non-text captures.
                        "fingerprint": summary.content_fingerprint,
                        "mixed_content": summary.mixed_content,
                        # Security headers, allowlisted at the source
                        # (`seo_audit.SECURITY_RESPONSE_HEADERS`). Absent/None
                        # means the fetch recorded none — the security checks
                        # answer `n_a` rather than passing on nothing.
                        "response_headers": summary.response_headers,
                        "redirect_chain": summary.redirect_chain,
                        "pagination": summary.pagination,
                        "content_type": summary.mime_type,
                        "resources": summary.resources,
                        "page_identity": summary.page_identity,
                        "custom": request.extractor_results,
                    },
                )

                for position, link in enumerate(summary.links):
                    target_normalized = _normalise_url(link.target_url)
                    target_page = None
                    if link.link_type != "external":
                        # Resolve the internal target against the canonical
                        # page registry at write time — links NEVER create
                        # pages. A URL not yet in the registry leaves
                        # target_page_id NULL; the standalone
                        # /links/resolve backfill picks it up once the page
                        # exists (sitemap, crawl, or GSC provenance).
                        target_digest = url_hash(target_normalized)
                        target_page = await WebPage.get_or_none(
                            use_cache=False,
                            site_id=self.state.site_id,
                            url_hash=target_digest,
                        )
                    await WebLinkEdge.create(
                        organization_id=self.state.organization_id,
                        created_by=self.state.user_id,
                        site_id=self.state.site_id,
                        snapshot_id=str(snapshot.id),
                        source_page_id=str(page.id),
                        target_url=target_normalized,
                        target_page_id=(
                            str(target_page.canonical_page_id) if target_page else None
                        ),
                        is_internal=link.link_type != "external",
                        rel=link.rel or ("nofollow" if link.nofollow else None),
                        anchor_text=link.anchor_text,
                        position=position,
                    )

                screenshot_ids: dict[str, str] = {}
                for shot, shot_result in screenshot_artifacts:
                    width, height = resolve_screenshot_dimensions(
                        shot.width,
                        shot.height,
                        shot.bytes,
                    )
                    canonical_kind = (
                        "homepage"
                        if self.state.homepage_bootstrap
                        else "full"
                        if shot.kind == "full_page"
                        else "viewport"
                    )
                    screenshot = await WebScreenshot.create(
                        organization_id=self.state.organization_id,
                        created_by=self.state.user_id,
                        site_id=self.state.site_id,
                        page_id=str(page.id),
                        snapshot_id=str(snapshot.id),
                        kind=canonical_kind,
                        file_id=shot_result.file_id,
                        width=width,
                        height=height,
                        captured_at=captured_at,
                        metadata={"capture_kind": shot.kind},
                    )
                    screenshot_ids[shot.kind] = str(screenshot.id)
                    if self.state.homepage_bootstrap and self.state.homepage_screenshot_id is None:
                        self.state.homepage_screenshot_id = str(screenshot.id)
                        await WebSite.update_where(
                            {"id": self.state.site_id},
                            homepage_screenshot_id=str(screenshot.id),
                        )

                await WebPage.update_where(
                    {"id": str(page.id)},
                    status="active",
                    last_seen=captured_at,
                    http_status_last=summary.http_status,
                    content_type_last=summary.mime_type,
                    latest_snapshot_id=str(snapshot.id),
                )
                parent_page_id = None
                if discovery.parent_url:
                    parent_page = await WebPage.get_or_none(
                        use_cache=False,
                        site_id=self.state.site_id,
                        url_hash=url_hash(discovery.parent_url),
                    )
                    parent_page_id = str(parent_page.canonical_page_id) if parent_page else None
                fact_digest = url_hash(discovery.normalized_url)
                crawl_url = await WebCrawlUrl.create(
                    organization_id=self.state.organization_id,
                    created_by=self.state.user_id,
                    site_id=self.state.site_id,
                    session_id=self.state.session_id,
                    sequence=await self.state.next_url_sequence(),
                    page_id=str(page.id),
                    snapshot_id=str(snapshot.id),
                    raw_url=discovery.raw_url,
                    normalized_url=discovery.normalized_url,
                    url_hash=fact_digest,
                    discovery_source=discovery.source,
                    discovered_from_page_id=parent_page_id,
                    classification="internal",
                    outcome=(
                        "redirected"
                        if discovery.normalized_url != identity.final_url
                        else "captured"
                    ),
                    is_in_scope=True,
                    depth=discovery.depth,
                    http_status=summary.http_status,
                    final_url=identity.final_url,
                    metadata=crawl_url_fetch_metadata(summary.redirect_chain),
                    discovered_at=discovery.discovered_at,
                    completed_at=captured_at,
                )
                await self.repository._record_page_evidence_in_active_transaction(
                    self.state,
                    str(page.id),
                    is_present=True,
                    observed_at=captured_at,
                    evidence={
                        "session_id": self.state.session_id,
                        "crawl_url_id": str(crawl_url.id),
                        "snapshot_id": str(snapshot.id),
                        "outcome": crawl_url.outcome,
                        "http_status": summary.http_status,
                    },
                )

        await self.state.record_crawl_url(request.url, str(crawl_url.id))

        async with self.state.lock:
            self.state.seen_hashes.add(digest)
            self.state.new_pages += int(created)
            self.state.screenshots_persisted += len(screenshot_ids)
        return PersistResult(
            body_file_id=body_artifact.file_id if body_artifact else None,
            markdown_file_id=markdown_artifact.file_id if markdown_artifact else None,
            screenshot_file_ids={
                shot.kind: shot_result.file_id for shot, shot_result in screenshot_artifacts
            },
            page_id=str(page.id),
            snapshot_id=str(snapshot.id),
            # Dismissal memory is never silent: each revive of a
            # user-dismissed page becomes a durable crawl_warning on the
            # session (the crawler emits one event per entry).
            warnings=[
                {
                    "message": (
                        "Re-observed a page you previously dismissed — it is "
                        f"visible again and remembers the dismissal: {entry.url}"
                    ),
                    "context": {
                        "reason": "revived_after_dismissal",
                        "page_id": entry.row_id,
                        "url": entry.url,
                        "dismissed_at": entry.dismissed_at,
                        "dismissal_count": entry.dismissal_count,
                    },
                }
                for entry in revived_dismissals
            ],
        )


class DurableCrawlEventSink:
    """Sequence, durably append, publish, then live-emit each crawl event."""

    def __init__(
        self,
        repository: WebCrawlRepository,
        state: CrawlPersistenceState,
        broker: CrawlEventBroker,
        emitter: Emitter,
        before_completed: Callable[[], Awaitable[None]] | None = None,
    ) -> None:
        self.repository = repository
        self.state = state
        self.broker = broker
        self.emitter = emitter
        self.before_completed = before_completed
        self._completion_barrier_passed = False
        # Resume-safe: a fresh session starts at 0; a resumed session's state
        # carries MAX(crawl_event.sequence) so the next emit appends instead of
        # colliding with the crashed run's rows.
        self._sequence = int(state.event_sequence or 0)
        self._lock = asyncio.Lock()

    async def emit(self, event: CrawlEvent) -> None:
        # A successful terminal event is the durable resume boundary. Run
        # required, idempotent post-crawl evidence BEFORE persisting it: if a
        # deploy cancels this task, the session remains resumable and the boot
        # sweep reaches the barrier again instead of burying missing evidence
        # behind a completed crawl. This stays outside `_lock` so the callback
        # may emit ordinary progress/warning events through this same sink.
        if (
            isinstance(event, CrawlCompletedEvent)
            and event.status == "completed"
            and self.before_completed is not None
            and not self._completion_barrier_passed
        ):
            await self.before_completed()
            self._completion_barrier_passed = True
        async with self._lock:
            self._sequence += 1
            payload = event.model_dump(mode="python")
            payload.update(
                {
                    "run_id": self.state.session_id,
                    "session_id": self.state.session_id,
                    "site_id": self.state.site_id,
                    "sequence": self._sequence,
                }
            )
            canonical = type(event).model_validate(payload)
            if isinstance(canonical, CrawlPageDiscoveredEvent):
                await self.state.record_discovery(canonical)
            elif isinstance(canonical, CrawlPageFetchedEvent):
                await self.state.record_fetched(canonical)
            canonical = await self._persist_with_sequence_recovery(canonical, payload)
            # The DB gets the full event; the wire gets the client-shaped one.
            # A page's URL-decision ledger can carry hundreds of rows that no
            # client ever reads — persisting them is required, streaming them
            # is pure bandwidth.
            wire_event = (
                canonical.for_wire()
                if isinstance(canonical, CrawlUrlsClassifiedEvent)
                else canonical
            )
            await self.broker.publish(wire_event)
            await self.emitter.send_data(wire_event)

    async def _persist_with_sequence_recovery(
        self, canonical: CrawlEvent, payload: dict[str, Any]
    ) -> CrawlEvent:
        """Append the event, re-sequencing around a `(session_id, sequence)` clash.

        The unique constraint `crawl_event_session_sequence_unique` is correct
        and stays. What is NOT acceptable is it being RUN-FATAL: a duplicate
        sequence means our in-memory counter is behind the ledger, which is a
        fact we can simply re-read. The run lease is the first layer that stops
        two runs existing at all; this is the doctrine's required second layer,
        so a collision that slips through (a stolen lease, a legacy unleased
        run, a manual DB write) degrades to a loud retry instead of killing a
        live crawl — the exact failure mode that permanently failed two real
        sessions on 2026-07-30.

        `persist_event` runs entirely inside one transaction, so a failed
        attempt leaves no partial side effect to undo before retrying.
        """

        for attempt in range(1, EVENT_SEQUENCE_MAX_RETRIES + 1):
            try:
                await self.repository.persist_event(canonical, self.state)
                return canonical
            except IntegrityError as exc:
                if not _is_event_sequence_collision(exc) or attempt == EVENT_SEQUENCE_MAX_RETRIES:
                    raise
                ledger_max = await self.repository.max_event_sequence(self.state.session_id)
                self._sequence = max(self._sequence, ledger_max) + 1
                logger.error(
                    "crawl event sequence collision on session %s (attempt %s/%s): the ledger "
                    "is at %s, re-sequencing this event to %s and retrying. A collision means "
                    "another writer touched this session's event ledger — check the run lease.",
                    self.state.session_id,
                    attempt,
                    EVENT_SEQUENCE_MAX_RETRIES,
                    ledger_max,
                    self._sequence,
                )
                payload["sequence"] = self._sequence
                canonical = type(canonical).model_validate(payload)
        raise AssertionError("unreachable: sequence recovery loop always returns or raises")


__all__ = [
    "CanonicalBodyPersister",
    "CrawlPersistenceState",
    "DurableCrawlEventSink",
    "HomepageCapture",
    "SCREENSHOT_HISTORY_KEEP_PRIOR",
    "WebCrawlRepository",
    "build_user_claims",
    "prune_screenshot_history",
    "url_hash",
]
