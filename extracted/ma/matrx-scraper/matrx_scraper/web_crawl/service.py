"""Orchestration for browser-direct canonical crawl commands."""

from __future__ import annotations

import asyncio
import contextlib
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from matrx_utils import utcnow
from urllib.parse import urlparse

from matrx_connect import AppContext, Emitter, RequestControlRegistry, system_app_context

from matrx_scraper._ext import get_ext, has_ext
from matrx_scraper.crawler import (
    RENDER_BROWSER_ALWAYS,
    RENDER_HTTP_FIRST,
    RENDER_BROWSER_WITH_SCREENSHOT,
    CapturedShot,
    SiteCrawler,
    SiteCrawlerConfig,
    _is_same_host,
)
from matrx_scraper.events import (
    CrawlCompletedEvent,
    CrawlSessionCreatedEvent,
    CrawlWarningEvent,
)
from matrx_scraper.queue_backend import InMemoryQueueBackend
from matrx_scraper.web_crawl.broker import (
    CrawlBrokerRegistry,
    CrawlEventBroker,
)
from matrx_scraper.web_crawl.candidates import (
    DiscoveredCandidate,
    derive_site_identity,
    extract_homepage_candidates,
)
from matrx_scraper.rate_limiter import host_key
from matrx_scraper.web_crawl.pacing_memory import (
    load_remembered_pacing,
    save_learned_pacing,
)
from matrx_scraper.web_crawl.contracts import (
    INITIALIZATION_SCREENSHOT_KINDS,
    CrawlPresetDeleteResponse,
    CrawlPresetListResponse,
    CrawlPresetRecord,
    CrawlPresetSaveRequest,
    CrawlStartRequest,
    RecrawlConfigResponse,
    GscSyncProgressEvent,
    AnalysisProgressEvent,
    AnalysisSummary,
    GscSyncSummary,
    InitializationError,
    InitializationStep,
    InitializationStepStatus,
    InitializeStepEvent,
    InitializeStepName,
    InitializeStepStatus,
    LinkCheckProgressEvent,
    LinkCheckSummary,
    LinkResolutionProgressEvent,
    LinkResolutionSummary,
    LinkScoreProgressEvent,
    LinkScoreSummary,
    SiteInitializationProgressEvent,
    SiteInitializationSummary,
    SitemapSyncProgressEvent,
    SitemapSyncSummary,
    UrlReconciliationProgressEvent,
    UrlReconciliationSummary,
)
from matrx_scraper.web_crawl.presets import (
    CrawlPresetRepository,
    derive_recrawl_config,
)
from matrx_scraper.web_crawl.analysis import analyze_site_pages
from matrx_scraper.web_crawl.gsc_sync import parse_gsc_binding, sync_site_gsc
from matrx_scraper.web_crawl.link_check import check_site_links
from matrx_scraper.web_crawl.link_resolution import resolve_site_link_targets
from matrx_scraper.web_crawl.link_score import score_site_links
from matrx_scraper.web_crawl.site_probe import capture_site_probe
from matrx_scraper.web_crawl.sitemap_sync import sync_site_sitemaps
from matrx_scraper.web_crawl.url_identity import reconcile_site_urls
from matrx_scraper.web_crawl.persistence import (
    RUN_LEASE_HEARTBEAT_EVERY,
    STALE_SESSION_AFTER,
    WORKER_STOPPED_ERROR,
    CanonicalBodyPersister,
    CrawlPersistenceState,
    DurableCrawlEventSink,
    WebCrawlRepository,
    build_user_claims,
    read_run_lease,
    run_lease_is_live,
)
from matrx_scraper.utils.url import validate_public_http_url

logger = logging.getLogger(__name__)

GrowthStageSettle = Callable[..., Awaitable[None]]


async def _noop_growth_settle(*_args: object, **_kwargs: object) -> None:
    return None


async def _track_growth_stage(
    *, stage: str, site_id: str, ref_kind: str | None = None, ref_id: str | None = None
) -> GrowthStageSettle:
    """Ask the embedding host to observe a stage; standalone stays independent."""
    if not has_ext("growth_stage_tracker"):
        return _noop_growth_settle
    try:
        return await get_ext("growth_stage_tracker")(
            stage=stage,
            site_id=site_id,
            ref_kind=ref_kind,
            ref_id=ref_id,
        )
    except Exception:
        # Observability can never take down the stage it observes, but a broken
        # configured host seam is a genuine failure and must be loud.
        logger.exception("growth_stage_tracker could not open %s for site %s", stage, site_id)
        return _noop_growth_settle


# Resume policy — CAPS constants (a code push to change, never env vars).
# A session that keeps dying needs investigation, not endless resurrection:
# the attempt counter is durable (session.metadata.resume.attempts) so the cap
# holds across restarts. The lookback bounds boot-time auto-resume to recent
# crashes — ancient failures stay failed.
RESUME_MAX_ATTEMPTS = 3
CRASH_RESUME_LOOKBACK = timedelta(hours=24)

# Only runs with a durable frontier are resumable (short single-page runs
# deliberately skip it — see _resolve_durable_queue).
_RESUMABLE_MODES = frozenset({"full", "list", "page_fetch"})


def _assert_session_resumable(session: object) -> dict:
    """Gate a session for resume; returns the persisted request dump.

    Raises ValueError naming the exact reason — callers surface it verbatim
    (422 on the endpoint, an info log in the boot sweep) — except a session
    that is genuinely RUNNING somewhere, which raises RuntimeError ("already
    active") so the endpoint answers 409, not 422.
    """
    scope = dict(getattr(session, "scope", None) or {})
    mode = scope.get("mode")
    if mode not in _RESUMABLE_MODES:
        raise ValueError(
            f"session mode {mode!r} is not resumable — short runs have no durable frontier"
        )
    status = str(getattr(session, "status", "") or "")
    if status in ("complete", "partial"):
        raise ValueError(
            f"session already finished with status {status!r} — start a new crawl instead"
        )
    # A live run holds the durable lease. The in-process broker registry only
    # ever saw runs in THIS process; two containers (or the resume endpoint vs.
    # a running crawl) sailed past it, both seeded from the same MAX(sequence),
    # and the loser's error path failed the winner's session.
    if run_lease_is_live(session):
        lease = read_run_lease(session)
        raise RuntimeError(
            f"crawl session is already active elsewhere (lease owner "
            f"{lease.get('owner') or 'unknown'} on host {lease.get('host') or 'unknown'}) — "
            "cancel it or wait for it to finish or crash before resuming"
        )
    metadata = dict(getattr(session, "metadata", None) or {})
    if (metadata.get("cancel_request") or {}).get("requested"):
        raise ValueError("session was cancelled by a user — start a new crawl instead of resuming")
    attempts = int((metadata.get("resume") or {}).get("attempts") or 0)
    if attempts >= RESUME_MAX_ATTEMPTS:
        raise ValueError(
            f"session was already resumed {attempts} time(s) (cap {RESUME_MAX_ATTEMPTS}) — "
            "a run that keeps dying needs investigation, not another retry"
        )
    request_dump = scope.get("request")
    if not isinstance(request_dump, dict) or not request_dump:
        raise ValueError("session has no persisted request in scope['request']; cannot resume")
    return request_dump


def _rebuild_resume_request(request_dump: dict, stats: dict | None) -> CrawlStartRequest:
    """The original request with `max_pages` shrunk by pages already fetched.

    The durable frontier never re-claims a succeeded item, but the crawler's
    page budget counts THIS run's fetches — without the shrink, a crawl that
    crashed at 2,900/3,000 could fetch up to 3,000 more. `stats.pages_fetched`
    is the last persisted progress snapshot; clamped at 1 (`max_pages ge=1`)
    so an already-satisfied budget still runs the terminal reconcile pass.
    Validated through model_validate — never model_copy — so shrunk values
    re-pass the contract.
    """
    fetched = 0
    try:
        fetched = max(0, int((stats or {}).get("pages_fetched") or 0))
    except (TypeError, ValueError):
        fetched = 0
    payload = dict(request_dump)
    try:
        original = int(payload.get("max_pages") or 0)
    except (TypeError, ValueError):
        original = 0
    if original > 0:
        payload["max_pages"] = max(1, original - fetched)
    return CrawlStartRequest.model_validate(payload)


# One ACTIVE site-wide crawl per site: N concurrent "start crawl" POSTs must
# not mint N sessions all crawling the same site at once. Only the site-wide
# modes are exclusive — bootstrap / initialization / page_fetch / sitemap /
# gsc runs stay unrestricted.
_EXCLUSIVE_CRAWL_MODES = frozenset({"full", "list"})


def _session_blocks_new_crawl(session: object, *, now: datetime | None = None) -> bool:
    """True when this queued/running session should refuse a NEW full/list
    crawl of its site.

    A `running` session blocks while its run lease (or `updated_at` fallback)
    is live — the same judgment `run_lease_is_live` makes for resume. A
    `queued` session blocks only while it is fresh enough that the stale
    reaper would not claim it; a queued row with an unreadable `updated_at`
    fails CLOSED (blocks).
    """
    scope = dict(getattr(session, "scope", None) or {})
    if scope.get("mode") not in _EXCLUSIVE_CRAWL_MODES:
        return False
    status = str(getattr(session, "status", "") or "")
    if status == "running":
        return run_lease_is_live(session, now=now)
    if status == "queued":
        updated_at = getattr(session, "updated_at", None)
        if not isinstance(updated_at, datetime):
            return True
        if updated_at.tzinfo is None:
            updated_at = updated_at.replace(tzinfo=UTC)
        return (now or utcnow()) - updated_at < STALE_SESSION_AFTER
    return False


def _start_race_key(session: object) -> tuple[datetime, str]:
    created_at = getattr(session, "created_at", None)
    if not isinstance(created_at, datetime):
        created_at = datetime.max.replace(tzinfo=UTC)
    elif created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)
    return (created_at, str(getattr(session, "id", "")))


def _losing_start_conflict(own_session: object, conflicts: list[object]) -> object | None:
    """Deterministic loser election for two starts racing past the pre-check.

    Both racers re-list after creating their sessions; the one with the
    LARGER `(created_at, id)` yields to the smaller. Exactly one of two
    mutually visible racers loses, so at most one crawl survives.
    """
    own_key = _start_race_key(own_session)
    older = [s for s in conflicts if _start_race_key(s) < own_key]
    if not older:
        return None
    return min(older, key=_start_race_key)


@dataclass
class PreparedCrawl:
    site_id: str
    session_id: str
    root_url: str
    request: CrawlStartRequest
    repository: WebCrawlRepository
    state: CrawlPersistenceState
    broker: CrawlEventBroker
    # The session's scope mode (full/list/homepage/initialization/page_fetch).
    # Site-wide post-crawl analysis runs only for full/list crawls.
    mode: str = "full"


@dataclass
class PreparedSitemapSync:
    site_id: str
    session_id: str
    root_url: str
    repository: WebCrawlRepository
    state: CrawlPersistenceState


@dataclass
class PreparedGscSync:
    site_id: str
    session_id: str
    root_url: str
    integrations: dict[str, object]
    repository: WebCrawlRepository
    state: CrawlPersistenceState


@dataclass
class PreparedLinkResolution:
    site_id: str
    session_id: str
    root_url: str
    repository: WebCrawlRepository
    state: CrawlPersistenceState


@dataclass
class PreparedUrlReconciliation:
    site_id: str
    session_id: str
    root_url: str
    repository: WebCrawlRepository
    state: CrawlPersistenceState


@dataclass
class PreparedLinkCheck:
    site_id: str
    session_id: str
    root_url: str
    repository: WebCrawlRepository
    state: CrawlPersistenceState


@dataclass
class PreparedLinkScore:
    site_id: str
    session_id: str
    root_url: str
    repository: WebCrawlRepository
    state: CrawlPersistenceState


@dataclass
class PreparedAnalysis:
    site_id: str
    session_id: str
    root_url: str
    repository: WebCrawlRepository
    state: CrawlPersistenceState


class WebCrawlService:
    def __init__(self) -> None:
        self.brokers = CrawlBrokerRegistry.get_instance()
        self.controls = RequestControlRegistry.get_instance()

    # ------------------------------------------------------------------
    # Crawl presets + one-click rescrape
    #
    # A preset is a saved CrawlStartRequest for one site; rescrape derives the
    # config a "run it again" button should use. Both authorize through the
    # site — reads need `viewer` (RLS), writes need `editor` (the same
    # assert_site_editor gate every other crawler command uses).

    def _presets(self, ctx: AppContext) -> CrawlPresetRepository:
        return CrawlPresetRepository(WebCrawlRepository(build_user_claims(ctx)))

    async def list_presets(self, ctx: AppContext, site_id: str) -> CrawlPresetListResponse:
        presets = self._presets(ctx)
        records = await presets.list_for_site(site_id)
        return CrawlPresetListResponse(
            site_id=site_id,
            presets=records,
            count=len(records),
            default_preset_id=await presets.default_preset_id(site_id),
        )

    async def save_preset(
        self, ctx: AppContext, site_id: str, request: CrawlPresetSaveRequest
    ) -> CrawlPresetRecord:
        presets = self._presets(ctx)
        await presets.repository.assert_site_editor(site_id, ctx.user_id)
        return await presets.save(site_id, request)

    async def delete_preset(
        self, ctx: AppContext, site_id: str, preset_id: str
    ) -> CrawlPresetDeleteResponse:
        presets = self._presets(ctx)
        await presets.repository.assert_site_editor(site_id, ctx.user_id)
        row = await presets.load(preset_id)
        if str(row.site_id) != str(site_id):
            raise PermissionError(f"crawl preset {preset_id} belongs to another site")
        deleted = await presets.delete(preset_id)
        if not deleted:
            raise LookupError(f"crawl preset {preset_id} does not exist or is not accessible")
        return CrawlPresetDeleteResponse(preset_id=preset_id)

    async def recrawl_config(
        self, ctx: AppContext, site_id: str, *, preset_id: str | None = None
    ) -> RecrawlConfigResponse:
        """What a one-click rescrape WOULD run, without running it."""

        return await derive_recrawl_config(self._presets(ctx), site_id, preset_id=preset_id)

    async def prepare_rescrape(
        self,
        ctx: AppContext,
        site_id: str,
        *,
        preset_id: str | None = None,
        trigger: str = "manual",
    ) -> PreparedCrawl:
        """One-click "crawl this site again" — no request body required.

        The preset's use counter is bumped only AFTER the crawl is accepted, so
        a start that is refused (another crawl already active, screenshots
        unavailable) never registers as a use.

        `trigger` is provenance, not behaviour: a recurring `web.crawl_schedule`
        firing passes `"scheduled"` so its session is honestly labelled, and
        runs the SAME derivation a human clicking Rescrape runs.
        """

        presets = self._presets(ctx)
        resolved = await derive_recrawl_config(presets, site_id, preset_id=preset_id)
        prepared = await self.prepare_start(ctx, site_id, resolved.config, trigger=trigger)
        if resolved.preset_id:
            await presets.touch(resolved.preset_id)
        return prepared

    async def prepare_start(
        self,
        ctx: AppContext,
        site_id: str,
        request: CrawlStartRequest,
        *,
        homepage_bootstrap: bool = False,
        site_initialization: bool = False,
        page_fetch: bool = False,
        trigger: str = "manual",
    ) -> PreparedCrawl:
        if not has_ext("file_manager"):
            raise RuntimeError("canonical file manager is unavailable")
        file_manager = get_ext("file_manager")
        if (
            file_manager is None
            or file_manager.sync_engine is None
            or file_manager.sync_engine._config.storage_backend != "s3"
            or not file_manager.cloud.is_configured("s3")
        ):
            raise RuntimeError("canonical S3 file pipeline is unavailable")
        wants_screenshots = (
            request.capture_screenshots or request.render_mode == RENDER_BROWSER_WITH_SCREENSHOT
        )
        if wants_screenshots and not has_ext("browser_pool"):
            raise RuntimeError("screenshot capture requires the browser pool")

        claims = build_user_claims(ctx)
        repository = WebCrawlRepository(claims)
        await repository.assert_site_editor(site_id, ctx.user_id)
        root_url = await repository.site_root(site_id)
        await validate_public_http_url(root_url)
        root_host = urlparse(root_url).netloc.lower()
        invalid_seeds = [
            url
            for url in request.seed_urls
            if not _is_same_host(url, root_host, request.follow_subdomains)
        ]
        if invalid_seeds:
            raise ValueError(
                "seed_urls must belong to the canonical site host; invalid values: "
                + ", ".join(invalid_seeds[:3])
            )
        mode = (
            "initialization"
            if site_initialization
            else "homepage"
            if homepage_bootstrap
            else "page_fetch"
            if page_fetch
            else "list"
            if request.list_mode
            else "full"
        )
        if mode in _EXCLUSIVE_CRAWL_MODES:
            # ONE active site-wide crawl per site. Reap crashed leftovers
            # first so a dead run never blocks a legitimate start, then
            # refuse while a live full/list session exists.
            await WebCrawlRepository.fail_stale_sessions()
            for existing in await WebCrawlRepository.list_active_sessions_for_site(site_id):
                if _session_blocks_new_crawl(existing):
                    raise RuntimeError(
                        f"crawl session {existing.id} is already active for this "
                        f"site (status {existing.status}) — cancel it or wait for "
                        "it to finish or crash before starting another crawl"
                    )
        scope = {
            "mode": mode,
            "coverage_qualified": request.coverage_qualified() and not homepage_bootstrap,
            "requested_by": ctx.user_id,
            "request": request.model_dump(mode="json"),
        }
        (
            verified_root_url,
            session_id,
            organization_id,
            file_owner_id,
        ) = await repository.create_session(
            site_id, scope=scope, user_id=ctx.user_id, trigger=trigger
        )
        if mode in _EXCLUSIVE_CRAWL_MODES:
            # Race backstop: two concurrent starts can both pass the
            # pre-check before either row exists. Both re-list AFTER
            # creating; the racer with the larger (created_at, id) yields —
            # its just-created session is terminated so it cannot itself
            # block later starts. (A DB partial-unique arbiter would be
            # airtight; this application-level election covers the practical
            # window without a migration.)
            active = await WebCrawlRepository.list_active_sessions_for_site(site_id)
            own = next((s for s in active if str(s.id) == session_id), None)
            conflicts = [
                s for s in active if str(s.id) != session_id and _session_blocks_new_crawl(s)
            ]
            blocker = (
                _losing_start_conflict(own, conflicts)
                if own is not None
                else (min(conflicts, key=_start_race_key) if conflicts else None)
            )
            if blocker is not None:
                await WebCrawlRepository.abandon_duplicate_session(session_id, str(blocker.id))
                raise RuntimeError(
                    f"crawl session {blocker.id} is already active for this site — "
                    "concurrent start refused"
                )
        broker = await self.brokers.create(session_id)
        # A fresh session takes the same durable run lease a resume does, so
        # every session-status write this run makes is ownership-checked and a
        # later resume can tell "live" from "crashed" without guessing.
        lease_token, _ = await repository.claim_run_lease(session_id, is_resume=False)
        state = CrawlPersistenceState(
            site_id=site_id,
            session_id=session_id,
            user_id=ctx.user_id,
            organization_id=organization_id,
            file_owner_id=file_owner_id,
            coverage_qualified=bool(scope["coverage_qualified"]),
            homepage_bootstrap=homepage_bootstrap,
            site_initialization=site_initialization,
            run_lease_token=lease_token,
        )
        return PreparedCrawl(
            site_id=site_id,
            session_id=session_id,
            root_url=verified_root_url,
            request=request,
            repository=repository,
            state=state,
            broker=broker,
            mode=mode,
        )

    async def prepare_resume(self, ctx: AppContext, session_id: str) -> PreparedCrawl:
        """Re-prepare a CRASHED session so `run_prepared` continues its durable
        frontier instead of starting from zero.

        Loads (never creates) the session: the persisted `scope["request"]` is
        rebuilt with `max_pages` shrunk by pages already fetched, the site row
        re-supplies root_url/org/file-owner, the in-memory ledger sequence is
        seeded from the DB (a counter restarting at 0 would mint duplicate
        `crawl_url.sequence` values), and the stale terminal marks + any
        leftover `cancel_request` are cleared. `run_prepared` then finds the
        SAME batch execution by session link and claims the SAME pending
        frontier — the whole point of the durable queue.

        Raises `ValueError` for a non-resumable session (finished, cancelled,
        short-run mode, attempt cap, no persisted request), `RuntimeError`
        ("already active") when another run owns the session — either its
        broker in this process, its live durable run lease, or the lease
        compare-and-swap being lost to a racing claimant.
        """
        claims = build_user_claims(ctx)
        repository = WebCrawlRepository(claims)
        session = await repository.assert_session_access(session_id)
        site_id = str(session.site_id)
        await repository.assert_site_editor(site_id, ctx.user_id)

        request_dump = _assert_session_resumable(session)
        request = _rebuild_resume_request(request_dump, session.stats)

        # Same canonical-pipeline bar as prepare_start.
        if not has_ext("file_manager"):
            raise RuntimeError("canonical file manager is unavailable")
        file_manager = get_ext("file_manager")
        if (
            file_manager is None
            or file_manager.sync_engine is None
            or file_manager.sync_engine._config.storage_backend != "s3"
            or not file_manager.cloud.is_configured("s3")
        ):
            raise RuntimeError("canonical S3 file pipeline is unavailable")
        wants_screenshots = (
            request.capture_screenshots or request.render_mode == RENDER_BROWSER_WITH_SCREENSHOT
        )
        if wants_screenshots and not has_ext("browser_pool"):
            raise RuntimeError("screenshot capture requires the browser pool")

        root_url, organization_id, file_owner_id = await repository.site_identity(site_id)
        await validate_public_http_url(root_url)

        # Two double-run guards, in order of strength. The broker registry is
        # the cheap in-process one; `claim_run_lease` is the CROSS-process one
        # — a compare-and-swap on the session row that exactly one claimant can
        # win. Both raise RuntimeError("already active…") → 409.
        broker = await self.brokers.create(session_id)
        try:
            lease_token, attempt = await repository.claim_run_lease(session_id, is_resume=True)
            state = CrawlPersistenceState(
                site_id=site_id,
                session_id=session_id,
                user_id=ctx.user_id,
                organization_id=organization_id,
                file_owner_id=file_owner_id,
                coverage_qualified=bool((session.scope or {}).get("coverage_qualified")),
                run_lease_token=lease_token,
            )
            state.url_sequence = await repository.max_url_sequence(session_id)
            # BOTH monotonic counters must resume past the crashed run's rows.
            # Seeding only crawl_url left the event sink at 0, so the resumed
            # run's first event violated crawl_event_session_sequence_unique
            # and the "recovery" itself failed the session.
            state.event_sequence = await repository.max_event_sequence(session_id)
        except Exception:
            await broker.close()
            await self.brokers.remove(session_id, broker)
            raise
        logger.warning(
            "resuming crawl session %s (attempt %s/%s, remaining max_pages=%s, "
            "ledger sequence resumes at %s, event sequence resumes at %s, run lease %s)",
            session_id,
            attempt,
            RESUME_MAX_ATTEMPTS,
            request.max_pages,
            state.url_sequence,
            state.event_sequence,
            lease_token,
        )
        return PreparedCrawl(
            site_id=site_id,
            session_id=session_id,
            root_url=root_url,
            request=request,
            repository=repository,
            state=state,
            broker=broker,
            mode=str((session.scope or {}).get("mode") or "full"),
        )

    async def resume_crashed_sessions(
        self,
        *,
        limit: int = 5,
        lookback: timedelta = CRASH_RESUME_LOOKBACK,
    ) -> int:
        """Boot-time crash recovery: continue recently-reaped sessions from
        their durable frontiers, SEQUENTIALLY (a restart must never stampede N
        concurrent crawls). Each session runs under its own creator's identity
        (`system_app_context`) with a console emitter — headless, no client.
        Non-resumable candidates (cancelled, finished, attempt-capped, short
        runs) are skipped quietly; real failures are loud and move on.
        """
        candidates = await WebCrawlRepository.list_crash_resumable_sessions(
            lookback=lookback, limit=max(limit * 3, limit)
        )
        resumed = 0
        for session in candidates:
            if resumed >= limit:
                break
            session_id = str(session.id)
            try:
                async with system_app_context(
                    "web_crawl_crash_resume",
                    user_id=str(session.created_by),
                    organization_id=str(session.organization_id),
                ) as ctx:
                    prepared = await self.prepare_resume(ctx, session_id)
                    resumed += 1
                    logger.warning(
                        "crash-resume: continuing crawl session %s (site %s)",
                        session_id,
                        prepared.site_id,
                    )
                    await self.run_prepared(ctx.emitter, prepared)
            except asyncio.CancelledError:
                raise
            except ValueError as exc:
                logger.info("crash-resume: session %s not resumable: %s", session_id, exc)
            except RuntimeError as exc:
                if "already active" not in str(exc):
                    logger.exception("crash-resume failed for crawl session %s", session_id)
                    continue
                # Another container's sweep (or a user's resume) won the lease
                # — exactly what the lease is for, not an error. `resumed` is
                # only incremented after a successful prepare, so this session
                # correctly never counted against the sweep's budget.
                logger.info(
                    "crash-resume: session %s claimed by another process: %s", session_id, exc
                )
            except Exception:
                logger.exception("crash-resume failed for crawl session %s", session_id)
        return resumed

    async def prepare_bootstrap(self, ctx: AppContext, site_id: str) -> PreparedCrawl:
        request = CrawlStartRequest(
            max_pages=1,
            max_depth=0,
            concurrency=1,
            seed_from_sitemap=False,
            list_mode=True,
            render_mode=RENDER_BROWSER_WITH_SCREENSHOT,
            capture_screenshots=True,
            screenshot_kinds=["viewport_desktop"],
            respect_robots=False,
        )
        return await self.prepare_start(
            ctx,
            site_id,
            request,
            homepage_bootstrap=True,
        )

    async def prepare_page_fetch(
        self,
        ctx: AppContext,
        site_id: str,
        url: str,
        *,
        capture_screenshot: bool = True,
    ) -> PreparedCrawl:
        """Fetch ONE page on demand — the freshest capture of a single URL.

        Reuses the exact single-URL capture pipeline the homepage bootstrap
        uses (snapshot + head_tags + seo_metrics + screenshot), seeded with the
        requested URL instead of the homepage. `prepare_start` enforces the
        canonical-host boundary (www/apex equivalent) and creates a durable
        session with scope mode "page_fetch"; crawl discovery never runs
        (list_mode, max_pages=1).
        """

        target = url.strip()
        if not target:
            raise ValueError("url is required")
        request = CrawlStartRequest(
            max_pages=1,
            max_depth=0,
            concurrency=1,
            seed_from_sitemap=False,
            list_mode=True,
            seed_urls=[target],
            render_mode=(
                RENDER_BROWSER_WITH_SCREENSHOT if capture_screenshot else RENDER_HTTP_FIRST
            ),
            capture_screenshots=capture_screenshot,
            screenshot_kinds=["viewport_desktop"] if capture_screenshot else [],
            respect_robots=False,
        )
        return await self.prepare_start(
            ctx,
            site_id,
            request,
            page_fetch=True,
        )

    async def prepare_initialize(self, ctx: AppContext, site_id: str) -> PreparedCrawl:
        # Initialization is the authoritative identity read, not a cheap crawl.
        # Start it with the browser identity directly: an HTTP-first request can
        # receive a generic 403 from a WAF, then spend the same browser navigation
        # as a fallback while retaining only the less-useful HTTP diagnosis if
        # that fallback is interrupted. The command captures screenshots later
        # in the same run, so a browser pool is already a hard requirement.
        if not has_ext("browser_pool"):
            raise RuntimeError("site initialization requires the browser pool")
        request = CrawlStartRequest(
            max_pages=1,
            max_depth=0,
            concurrency=1,
            seed_from_sitemap=False,
            list_mode=True,
            render_mode=RENDER_BROWSER_ALWAYS,
            capture_screenshots=False,
            screenshot_kinds=[],
            respect_robots=False,
        )
        prepared = await self.prepare_start(
            ctx,
            site_id,
            request,
            site_initialization=True,
        )
        prepared.state.brand_id = await prepared.repository.site_brand_id(site_id)
        return prepared

    async def prepare_sitemap_sync(self, ctx: AppContext, site_id: str) -> PreparedSitemapSync:
        """Authorize and create the durable session for a standalone sitemap sync."""

        claims = build_user_claims(ctx)
        repository = WebCrawlRepository(claims)
        await repository.assert_site_editor(site_id, ctx.user_id)
        root_url = await repository.site_root(site_id)
        await validate_public_http_url(root_url)
        scope = {"mode": "sitemap_sync", "requested_by": ctx.user_id}
        (
            verified_root_url,
            session_id,
            organization_id,
            file_owner_id,
        ) = await repository.create_session(site_id, scope=scope, user_id=ctx.user_id)
        state = CrawlPersistenceState(
            site_id=site_id,
            session_id=session_id,
            user_id=ctx.user_id,
            organization_id=organization_id,
            file_owner_id=file_owner_id,
            coverage_qualified=False,
        )
        return PreparedSitemapSync(
            site_id=site_id,
            session_id=session_id,
            root_url=verified_root_url,
            repository=repository,
            state=state,
        )

    async def run_sitemap_sync(self, emitter: Emitter, prepared: PreparedSitemapSync) -> None:
        """Standalone streaming sitemap sync — same operation as the
        initialize-site sitemaps step, exposed as its own command."""

        async def emit(
            status: str,
            message: str,
            summary: SitemapSyncSummary,
            errors: list[str] | None = None,
        ) -> None:
            await emitter.send_data(
                SitemapSyncProgressEvent(
                    site_id=prepared.site_id,
                    session_id=prepared.session_id,
                    status=status,  # type: ignore[arg-type]
                    message=message,
                    summary=summary,
                    errors=list(errors or []),
                )
            )

        async def on_progress(message: str, summary: SitemapSyncSummary) -> None:
            await emit("progress", message, summary)

        await prepared.repository.mark_session_running(
            prepared.session_id, lease_token=prepared.state.run_lease_token
        )
        await emit("started", "Syncing sitemaps…", SitemapSyncSummary())
        try:
            result = await sync_site_sitemaps(
                site_id=prepared.site_id,
                organization_id=prepared.state.organization_id,
                user_id=prepared.state.user_id,
                root_url=prepared.root_url,
                on_progress=on_progress,
                session_id=prepared.session_id,
            )
            await reconcile_site_urls(
                site_id=prepared.site_id,
                organization_id=prepared.state.organization_id,
                user_id=prepared.state.user_id,
                root_url=prepared.root_url,
            )
        except asyncio.CancelledError:
            try:
                await prepared.repository.fail_session(
                    prepared.session_id,
                    WORKER_STOPPED_ERROR,
                    lease_token=prepared.state.run_lease_token,
                )
            except Exception:
                logger.exception("failed to mark canceled crawl session failed")
            raise
        except Exception as exc:
            await prepared.repository.fail_session(
                prepared.session_id,
                f"{type(exc).__name__}: {exc}",
                lease_token=prepared.state.run_lease_token,
            )
            raise
        await prepared.repository.complete_session(
            prepared.session_id,
            {
                "sitemaps": result.summary.model_dump(mode="json"),
                "errors": result.errors[:50],
            },
            lease_token=prepared.state.run_lease_token,
        )
        await emit(
            "ok",
            (
                f"Synced {result.summary.found} sitemaps; upserted "
                f"{result.summary.pages_upserted} pages from {result.summary.urls} URLs."
                + (" TRUNCATED at the sync bounds." if result.summary.truncated else "")
            ),
            result.summary,
            result.errors,
        )
        await emitter.send_end()

    async def prepare_gsc_sync(self, ctx: AppContext, site_id: str) -> PreparedGscSync:
        """Authorize and create the durable session for a GSC sync."""

        claims = build_user_claims(ctx)
        repository = WebCrawlRepository(claims)
        await repository.assert_site_editor(site_id, ctx.user_id)
        integrations = await repository.site_integrations(site_id)
        # Validate the binding BEFORE creating a session so a site without a
        # GSC binding gets a clean 422 instead of an instantly-failed session.
        parse_gsc_binding(integrations)
        scope = {"mode": "gsc_sync", "requested_by": ctx.user_id}
        (
            verified_root_url,
            session_id,
            organization_id,
            file_owner_id,
        ) = await repository.create_session(site_id, scope=scope, user_id=ctx.user_id)
        state = CrawlPersistenceState(
            site_id=site_id,
            session_id=session_id,
            user_id=ctx.user_id,
            organization_id=organization_id,
            file_owner_id=file_owner_id,
            coverage_qualified=False,
        )
        return PreparedGscSync(
            site_id=site_id,
            session_id=session_id,
            root_url=verified_root_url,
            integrations=integrations,
            repository=repository,
            state=state,
        )

    async def run_gsc_sync(self, emitter: Emitter, prepared: PreparedGscSync) -> None:
        """Streaming GSC sync — Search Analytics daily page stats + canonical
        page upserts + the property's submitted-sitemaps listing."""

        async def emit(status: str, message: str, summary: GscSyncSummary) -> None:
            await emitter.send_data(
                GscSyncProgressEvent(
                    site_id=prepared.site_id,
                    session_id=prepared.session_id,
                    status=status,  # type: ignore[arg-type]
                    message=message,
                    summary=summary,
                )
            )

        async def on_progress(message: str, summary: GscSyncSummary) -> None:
            await emit("progress", message, summary)

        await prepared.repository.mark_session_running(
            prepared.session_id, lease_token=prepared.state.run_lease_token
        )
        await emit("started", "Syncing Google Search Console…", GscSyncSummary())
        try:
            result = await sync_site_gsc(
                site_id=prepared.site_id,
                organization_id=prepared.state.organization_id,
                user_id=prepared.state.user_id,
                root_url=prepared.root_url,
                integrations=prepared.integrations,
                on_progress=on_progress,
            )
            await reconcile_site_urls(
                site_id=prepared.site_id,
                organization_id=prepared.state.organization_id,
                user_id=prepared.state.user_id,
                root_url=prepared.root_url,
            )
        except Exception as exc:
            await prepared.repository.fail_session(
                prepared.session_id,
                f"{type(exc).__name__}: {exc}",
                lease_token=prepared.state.run_lease_token,
            )
            raise
        await prepared.repository.complete_session(
            prepared.session_id,
            {"gsc": result.summary.model_dump(mode="json")},
            lease_token=prepared.state.run_lease_token,
        )
        await emit(
            "ok",
            (
                f"Synced {result.summary.stats_rows} daily stats across "
                f"{result.summary.pages} pages from {result.summary.property}."
                + (f" {len(result.summary.errors)} warning(s)." if result.summary.errors else "")
            ),
            result.summary,
        )
        await emitter.send_end()

    async def prepare_url_reconciliation(
        self, ctx: AppContext, site_id: str
    ) -> PreparedUrlReconciliation:
        claims = build_user_claims(ctx)
        repository = WebCrawlRepository(claims)
        await repository.assert_site_editor(site_id, ctx.user_id)
        scope = {"mode": "url_reconciliation", "requested_by": ctx.user_id}
        (
            root_url,
            session_id,
            organization_id,
            file_owner_id,
        ) = await repository.create_session(site_id, scope=scope, user_id=ctx.user_id)
        state = CrawlPersistenceState(
            site_id=site_id,
            session_id=session_id,
            user_id=ctx.user_id,
            organization_id=organization_id,
            file_owner_id=file_owner_id,
            coverage_qualified=False,
        )
        return PreparedUrlReconciliation(
            site_id=site_id,
            session_id=session_id,
            root_url=root_url,
            repository=repository,
            state=state,
        )

    async def run_url_reconciliation(
        self,
        emitter: Emitter,
        prepared: PreparedUrlReconciliation,
    ) -> None:
        async def emit(
            status: str,
            message: str,
            summary: UrlReconciliationSummary,
        ) -> None:
            await emitter.send_data(
                UrlReconciliationProgressEvent(
                    site_id=prepared.site_id,
                    session_id=prepared.session_id,
                    status=status,  # type: ignore[arg-type]
                    message=message,
                    summary=summary,
                )
            )

        async def on_progress(
            message: str,
            summary: UrlReconciliationSummary,
        ) -> None:
            await emit("progress", message, summary)

        await prepared.repository.mark_session_running(
            prepared.session_id, lease_token=prepared.state.run_lease_token
        )
        await emit(
            "started",
            "Reconciling every observed URL to one canonical page…",
            UrlReconciliationSummary(),
        )
        try:
            result = await reconcile_site_urls(
                site_id=prepared.site_id,
                organization_id=prepared.state.organization_id,
                user_id=prepared.state.user_id,
                root_url=prepared.root_url,
                on_progress=on_progress,
            )
        except Exception as exc:
            await prepared.repository.fail_session(
                prepared.session_id,
                f"{type(exc).__name__}: {exc}",
                lease_token=prepared.state.run_lease_token,
            )
            raise
        await prepared.repository.complete_session(
            prepared.session_id,
            {"url_reconciliation": result.summary.model_dump(mode="json")},
            lease_token=prepared.state.run_lease_token,
        )
        await emit(
            "ok",
            (
                f"Matched {result.summary.aliases_matched} aliases; moved "
                f"{result.summary.gsc_rows_moved} GSC rows and "
                f"{result.summary.sitemap_memberships_moved} sitemap memberships."
            ),
            result.summary,
        )
        await emitter.send_end()

    async def prepare_link_resolution(
        self, ctx: AppContext, site_id: str
    ) -> PreparedLinkResolution:
        """Authorize and create the durable session for a link-target backfill."""

        claims = build_user_claims(ctx)
        repository = WebCrawlRepository(claims)
        await repository.assert_site_editor(site_id, ctx.user_id)
        scope = {"mode": "link_resolution", "requested_by": ctx.user_id}
        (
            verified_root_url,
            session_id,
            organization_id,
            file_owner_id,
        ) = await repository.create_session(site_id, scope=scope, user_id=ctx.user_id)
        state = CrawlPersistenceState(
            site_id=site_id,
            session_id=session_id,
            user_id=ctx.user_id,
            organization_id=organization_id,
            file_owner_id=file_owner_id,
            coverage_qualified=False,
        )
        return PreparedLinkResolution(
            site_id=site_id,
            session_id=session_id,
            root_url=verified_root_url,
            repository=repository,
            state=state,
        )

    async def run_link_resolution(self, emitter: Emitter, prepared: PreparedLinkResolution) -> None:
        """Streaming link-target backfill over the site's internal edges."""

        async def emit(status: str, message: str, summary: LinkResolutionSummary) -> None:
            await emitter.send_data(
                LinkResolutionProgressEvent(
                    site_id=prepared.site_id,
                    session_id=prepared.session_id,
                    status=status,  # type: ignore[arg-type]
                    message=message,
                    summary=summary,
                )
            )

        async def on_progress(message: str, summary: LinkResolutionSummary) -> None:
            await emit("progress", message, summary)

        await prepared.repository.mark_session_running(
            prepared.session_id, lease_token=prepared.state.run_lease_token
        )
        await emit("started", "Resolving internal link targets…", LinkResolutionSummary())
        try:
            result = await resolve_site_link_targets(
                site_id=prepared.site_id,
                on_progress=on_progress,
            )
        except Exception as exc:
            await prepared.repository.fail_session(
                prepared.session_id,
                f"{type(exc).__name__}: {exc}",
                lease_token=prepared.state.run_lease_token,
            )
            raise
        await prepared.repository.complete_session(
            prepared.session_id,
            {"link_resolution": result.summary.model_dump(mode="json")},
            lease_token=prepared.state.run_lease_token,
        )
        await emit(
            "ok",
            (
                f"Scanned {result.summary.scanned} internal edges; resolved "
                f"{result.summary.resolved}; {result.summary.unresolved} remain "
                "unresolved (target URL not in the page registry)."
            ),
            result.summary,
        )
        await emitter.send_end()

    async def prepare_link_check(self, ctx: AppContext, site_id: str) -> PreparedLinkCheck:
        """Authorize and create the durable session for a link-status check."""

        claims = build_user_claims(ctx)
        repository = WebCrawlRepository(claims)
        await repository.assert_site_editor(site_id, ctx.user_id)
        await repository.site_root(site_id)
        scope = {"mode": "link_check", "requested_by": ctx.user_id}
        (
            verified_root_url,
            session_id,
            organization_id,
            file_owner_id,
        ) = await repository.create_session(site_id, scope=scope, user_id=ctx.user_id)
        state = CrawlPersistenceState(
            site_id=site_id,
            session_id=session_id,
            user_id=ctx.user_id,
            organization_id=organization_id,
            file_owner_id=file_owner_id,
            coverage_qualified=False,
        )
        return PreparedLinkCheck(
            site_id=site_id,
            session_id=session_id,
            root_url=verified_root_url,
            repository=repository,
            state=state,
        )

    async def run_link_check(self, emitter: Emitter, prepared: PreparedLinkCheck) -> None:
        """Streaming link-status verification over the site's edges."""

        async def emit(status: str, message: str, summary: LinkCheckSummary) -> None:
            await emitter.send_data(
                LinkCheckProgressEvent(
                    site_id=prepared.site_id,
                    session_id=prepared.session_id,
                    status=status,  # type: ignore[arg-type]
                    message=message,
                    summary=summary,
                )
            )

        async def on_progress(message: str, summary: LinkCheckSummary) -> None:
            await emit("progress", message, summary)

        await prepared.repository.mark_session_running(
            prepared.session_id, lease_token=prepared.state.run_lease_token
        )
        await emit("started", "Checking link targets…", LinkCheckSummary())
        try:
            result = await check_site_links(
                site_id=prepared.site_id,
                on_progress=on_progress,
            )
        except Exception as exc:
            await prepared.repository.fail_session(
                prepared.session_id,
                f"{type(exc).__name__}: {exc}",
                lease_token=prepared.state.run_lease_token,
            )
            raise
        await prepared.repository.complete_session(
            prepared.session_id,
            {"link_check": result.summary.model_dump(mode="json")},
            lease_token=prepared.state.run_lease_token,
        )
        summary = result.summary
        await emit(
            "ok",
            (
                f"Internal: {summary.internal_updated} edges stamped from crawled "
                f"snapshots ({summary.internal_uncrawled} targets never crawled, "
                f"{summary.internal_unresolved} unresolved). External: "
                f"{summary.external_checked}/{summary.external_targets} targets "
                f"checked — {summary.external_ok} ok, {summary.external_broken} "
                f"broken, {summary.external_unreachable} unreachable"
                + (" (truncated)." if summary.external_truncated else ".")
            ),
            summary,
        )
        await emitter.send_end()

    async def prepare_link_score(self, ctx: AppContext, site_id: str) -> PreparedLinkScore:
        """Authorize and create the durable session for a link-score recompute."""

        claims = build_user_claims(ctx)
        repository = WebCrawlRepository(claims)
        await repository.assert_site_editor(site_id, ctx.user_id)
        scope = {"mode": "link_score", "requested_by": ctx.user_id}
        (
            verified_root_url,
            session_id,
            organization_id,
            file_owner_id,
        ) = await repository.create_session(site_id, scope=scope, user_id=ctx.user_id)
        state = CrawlPersistenceState(
            site_id=site_id,
            session_id=session_id,
            user_id=ctx.user_id,
            organization_id=organization_id,
            file_owner_id=file_owner_id,
            coverage_qualified=False,
        )
        return PreparedLinkScore(
            site_id=site_id,
            session_id=session_id,
            root_url=verified_root_url,
            repository=repository,
            state=state,
        )

    async def run_link_score(self, emitter: Emitter, prepared: PreparedLinkScore) -> None:
        """Streaming internal-link PageRank recompute for one site."""

        async def emit(status: str, message: str, summary: LinkScoreSummary) -> None:
            await emitter.send_data(
                LinkScoreProgressEvent(
                    site_id=prepared.site_id,
                    session_id=prepared.session_id,
                    status=status,  # type: ignore[arg-type]
                    message=message,
                    summary=summary,
                )
            )

        async def on_progress(message: str, summary: LinkScoreSummary) -> None:
            await emit("progress", message, summary)

        await prepared.repository.mark_session_running(
            prepared.session_id, lease_token=prepared.state.run_lease_token
        )
        await emit("started", "Computing internal link scores…", LinkScoreSummary())
        try:
            result = await score_site_links(
                site_id=prepared.site_id,
                on_progress=on_progress,
            )
        except Exception as exc:
            await prepared.repository.fail_session(
                prepared.session_id,
                f"{type(exc).__name__}: {exc}",
                lease_token=prepared.state.run_lease_token,
            )
            raise
        await prepared.repository.complete_session(
            prepared.session_id,
            {"link_score": result.summary.model_dump(mode="json")},
            lease_token=prepared.state.run_lease_token,
        )
        summary = result.summary
        await emit(
            "ok",
            (
                f"Scored {summary.pages_scored} pages across {summary.nodes} "
                f"canonical page(s) using {summary.edges_resolved} of "
                f"{summary.edges_scanned} internal links "
                f"({summary.edges_unresolved} pointed outside the page registry)."
            ),
            summary,
        )
        await emitter.send_end()

    async def prepare_analysis(self, ctx: AppContext, site_id: str) -> PreparedAnalysis:
        """Authorize and create the durable session for a page-analysis run."""

        claims = build_user_claims(ctx)
        repository = WebCrawlRepository(claims)
        await repository.assert_site_editor(site_id, ctx.user_id)
        await repository.site_root(site_id)
        scope = {"mode": "analysis", "requested_by": ctx.user_id}
        (
            verified_root_url,
            session_id,
            organization_id,
            file_owner_id,
        ) = await repository.create_session(site_id, scope=scope, user_id=ctx.user_id)
        # The same cross-process ownership crawls carry. Without a lease there
        # is no heartbeat, and without a heartbeat `fail_stale_sessions` reaped
        # every analysis run longer than 30 minutes while it was still working
        # (datadestruction, 3× on 2026-08-11).
        lease_token, _attempt = await repository.claim_run_lease(session_id, is_resume=False)
        state = CrawlPersistenceState(
            site_id=site_id,
            session_id=session_id,
            user_id=ctx.user_id,
            organization_id=organization_id,
            file_owner_id=file_owner_id,
            coverage_qualified=False,
            run_lease_token=lease_token,
        )
        return PreparedAnalysis(
            site_id=site_id,
            session_id=session_id,
            root_url=verified_root_url,
            repository=repository,
            state=state,
        )

    async def run_analysis(self, emitter: Emitter, prepared: PreparedAnalysis) -> None:
        """Streaming deterministic page analysis over the site's evidence.

        The run heartbeats its lease for its whole lifetime (a quiet loader
        phase must not read as a crash to the stale-session reaper), and EVERY
        death path — a crash, a lost lease, a cancellation from a server
        shutdown — leaves a terminal status WITH an error on the session row.
        A run that dies silently is the bug this replaced.
        """

        async def emit(status: str, message: str, summary: AnalysisSummary) -> None:
            await emitter.send_data(
                AnalysisProgressEvent(
                    site_id=prepared.site_id,
                    session_id=prepared.session_id,
                    status=status,  # type: ignore[arg-type]
                    message=message,
                    summary=summary,
                )
            )

        async def on_progress(message: str, summary: AnalysisSummary) -> None:
            await emit("progress", message, summary)

        lease_token = prepared.state.run_lease_token
        work_task = asyncio.current_task()

        async def _heartbeat() -> None:
            # Refresh the lease (which also touches the row's `updated_at` —
            # the exact signal `fail_stale_sessions` reads) until the run ends.
            # Losing the lease means another process owns this session now:
            # cancel the work instead of racing the new owner's writes.
            while True:
                await asyncio.sleep(RUN_LEASE_HEARTBEAT_EVERY.total_seconds())
                if not lease_token:
                    continue
                try:
                    alive = await prepared.repository.heartbeat_run_lease(
                        prepared.session_id, lease_token
                    )
                except Exception:
                    logger.warning(
                        "run-lease heartbeat failed for analysis session %s",
                        prepared.session_id,
                        exc_info=True,
                    )
                    continue
                if not alive and work_task is not None:
                    logger.error(
                        "analysis session %s lost its run lease (%s) to another process — "
                        "stopping this run so the new owner runs alone",
                        prepared.session_id,
                        lease_token,
                    )
                    work_task.cancel()
                    return

        await prepared.repository.mark_session_running(prepared.session_id, lease_token=lease_token)
        await emit("started", "Analyzing pages against the audit catalogue…", AnalysisSummary())
        await self._refresh_site_probe(prepared.site_id)
        heartbeat_task = asyncio.create_task(_heartbeat())
        analysis_settle = await _track_growth_stage(
            stage="analyze",
            site_id=prepared.site_id,
            ref_kind="crawl_session",
            ref_id=prepared.session_id,
        )
        try:
            result = await analyze_site_pages(
                site_id=prepared.site_id,
                run_id=prepared.session_id,
                on_progress=on_progress,
            )
        except asyncio.CancelledError:
            # Server shutdown, or the heartbeat detected a stolen lease. Either
            # way the session must not linger `running` with no explanation —
            # shielded so the cancellation itself cannot interrupt the write.
            with contextlib.suppress(Exception):
                await asyncio.shield(
                    prepared.repository.fail_session(
                        prepared.session_id,
                        WORKER_STOPPED_ERROR,
                        lease_token=lease_token,
                    )
                )
            with contextlib.suppress(asyncio.CancelledError):
                await asyncio.shield(analysis_settle("cancelled"))
            raise
        except Exception as exc:
            await prepared.repository.fail_session(
                prepared.session_id,
                f"{type(exc).__name__}: {exc}",
                lease_token=lease_token,
            )
            await analysis_settle(
                "failed",
                error={"type": type(exc).__name__, "message": str(exc)[:2000]},
            )
            raise
        finally:
            heartbeat_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await heartbeat_task
        try:
            await prepared.repository.complete_session(
                prepared.session_id,
                {"analysis": result.summary.model_dump(mode="json")},
                lease_token=lease_token,
            )
        except Exception as exc:
            await analysis_settle(
                "failed",
                error={"type": type(exc).__name__, "message": str(exc)[:2000]},
                ref_kind="analysis_result" if result.result_id else "crawl_session",
                ref_id=result.result_id or prepared.session_id,
            )
            raise
        summary = result.summary
        await analysis_settle(
            "completed",
            outcome={
                "pages_analyzed": summary.pages_analyzed,
                "results_written": summary.results_written,
                "findings_opened": summary.findings_opened,
            },
            ref_kind="analysis_result" if result.result_id else "crawl_session",
            ref_id=result.result_id or prepared.session_id,
        )
        await emit(
            "ok",
            (
                f"Analyzed {summary.pages_analyzed} pages × "
                f"{len(summary.items_evaluated)} checks: {summary.fails} fails, "
                f"{summary.warns} warns, {summary.passes} passes "
                f"({summary.not_applicable} not applicable). Findings: "
                f"{summary.findings_opened} opened, {summary.findings_refreshed} "
                f"refreshed, {summary.findings_reopened} reopened, "
                f"{summary.findings_resolved} resolved."
            ),
            summary,
        )
        await emitter.send_end()

    async def _refresh_site_probe(self, site_id: str) -> None:
        """Capture the site-level evidence the SITE checks score, before they run.

        robots.txt, the sitemap locations, and the www/non-www × http/https
        variants are facts about the HOST that no page capture records. The
        analysis sweep is network-free by contract, so the capture happens here
        — on BOTH paths into the sweep, so a site analyzed standalone scores the
        same evidence a post-crawl one does.

        A failed probe is never fatal: the checks fall back to their
        missing-evidence `n_a` (which carries a one-click retry), which is the
        honest answer. It is never silent either.
        """

        try:
            await capture_site_probe(site_id)
        except Exception:
            logger.exception(
                "site probe failed for site %s — robots.txt, sitemap-location and "
                "host-variant checks will report missing evidence for this run",
                site_id,
            )

    async def _run_post_crawl_analysis(self, prepared: PreparedCrawl, sink) -> None:
        """Site analysis as a post-crawl step for full/list crawls.

        The capture already succeeded; a broken analysis must not fail the
        crawl session — it degrades to a DURABLE crawl warning (never a silent
        log line) and the standalone /analyze command remains the retry path.
        """

        if prepared.mode not in ("full", "list"):
            return
        analysis_settle = await _track_growth_stage(
            stage="analyze",
            site_id=prepared.site_id,
            ref_kind="crawl_session",
            ref_id=prepared.session_id,
        )
        await self._refresh_site_probe(prepared.site_id)
        try:
            result = await analyze_site_pages(
                site_id=prepared.site_id,
                run_id=prepared.session_id,
            )
        except asyncio.CancelledError:
            with contextlib.suppress(asyncio.CancelledError):
                await asyncio.shield(analysis_settle("cancelled"))
            raise
        except Exception as exc:
            logger.exception("post-crawl analysis failed for site %s", prepared.site_id)
            await analysis_settle(
                "failed",
                error={"type": type(exc).__name__, "message": str(exc)[:2000]},
            )
            await sink.emit(
                CrawlWarningEvent(
                    run_id=prepared.session_id,
                    message=(
                        "Post-crawl page analysis failed — audit scores and findings "
                        f"were NOT refreshed: {type(exc).__name__}: {exc}. Re-run it "
                        "with the site's Analyze command."
                    ),
                    context={"reason": "post_crawl_analysis_failed"},
                )
            )
            return
        summary = result.summary
        await analysis_settle(
            "completed",
            outcome={
                "pages_analyzed": summary.pages_analyzed,
                "results_written": summary.results_written,
                "findings_opened": summary.findings_opened,
            },
            ref_kind="analysis_result" if result.result_id else "crawl_session",
            ref_id=result.result_id or prepared.session_id,
        )
        logger.info(
            "post-crawl analysis for site %s: %s pages, %s fails, %s warns, %s findings opened",
            prepared.site_id,
            summary.pages_analyzed,
            summary.fails,
            summary.warns,
            summary.findings_opened,
        )

    async def _reconcile_urls_after_incomplete_crawl(
        self,
        prepared: PreparedCrawl,
        sink: DurableCrawlEventSink,
    ) -> None:
        """Apply safe positive URL facts even when the crawl ends early.

        URL identity reconciliation does not infer absence: it only flattens
        observed scheme/www, redirect, and declared-canonical relationships.
        Deferring it to the success path left aliases from failed/cancelled
        crawls live in the page registry forever.  A failure here must preserve
        the crawl's original terminal cause, but it must also be durable and
        visible because the standalone URL-reconciliation command is the fix.
        """

        try:
            await reconcile_site_urls(
                site_id=prepared.site_id,
                organization_id=prepared.state.organization_id,
                user_id=prepared.state.user_id,
                root_url=prepared.root_url,
            )
        except Exception as exc:
            logger.exception(
                "URL reconciliation after incomplete crawl failed for site %s",
                prepared.site_id,
            )
            try:
                await sink.emit(
                    CrawlWarningEvent(
                        run_id=prepared.session_id,
                        message=(
                            "The crawl ended early and its observed URL aliases could "
                            "not be reconciled: "
                            f"{type(exc).__name__}: {exc}. Run the site's URL "
                            "reconciliation command."
                        ),
                        context={"reason": "incomplete_crawl_url_reconciliation_failed"},
                    )
                )
            except Exception:
                # The crawl's original terminal cause still wins if even the
                # durable warning path is unavailable.
                logger.exception(
                    "failed to persist incomplete-crawl reconciliation warning for %s",
                    prepared.site_id,
                )

    async def _populate_link_status_before_completion(self, prepared: PreparedCrawl) -> None:
        """Make link status part of a successful full/list crawl's contract.

        Both operations are idempotent. The sink invokes this before it writes
        the successful terminal event, so cancellation leaves the session for
        the existing boot resume sweep. External work is processed in bounded
        500-target rounds; each round persists as it goes, and a resumed run
        naturally skips the statuses that already landed.
        """

        if prepared.mode not in ("full", "list"):
            return
        resolution = await resolve_site_link_targets(site_id=prepared.site_id)
        rounds = 0
        checked = 0
        cached = 0
        updated = 0
        while True:
            rounds += 1
            result = await check_site_links(
                site_id=prepared.site_id,
                session_id=prepared.session_id,
            )
            checked += result.summary.external_checked
            cached += result.summary.external_cached
            updated += result.summary.internal_updated + result.summary.external_edges_updated
            if not result.summary.external_truncated:
                break
        logger.info(
            "pre-completion link evidence for site %s: %s resolved, %s network "
            "targets checked, %s cache hits, %s edges updated in %s round(s)",
            prepared.site_id,
            resolution.summary.resolved,
            checked,
            cached,
            updated,
            rounds,
        )

    async def _run_post_crawl_link_scoring(self, prepared: PreparedCrawl, sink) -> None:
        """Recompute ``web.page.link_score`` after a COMPLETED full crawl.

        Why only ``full``: the score is a PageRank over the site's own internal
        link graph, so it is only meaningful when that graph is whole. A
        ``list`` crawl captures a hand-picked set of URLs — most of the site's
        links point at pages that were never fetched, and every page in the
        list would look artificially isolated. A homepage bootstrap / site
        initialization is one page. And this runs only on the success path of
        ``run_prepared``, so a cancelled or failed session never scores either:
        a partial graph would produce confident, wrong numbers, and a
        stale-but-coherent score beats a fresh incoherent one. A resumed
        session that finishes IS complete and does score.

        Like post-crawl analysis, a failure here degrades to a DURABLE crawl
        warning — the capture already succeeded — and the standalone
        ``/links/score`` command is the retry path.
        """

        if prepared.mode != "full":
            return
        try:
            result = await score_site_links(site_id=prepared.site_id)
        except Exception as exc:
            logger.exception("post-crawl link scoring failed for site %s", prepared.site_id)
            await sink.emit(
                CrawlWarningEvent(
                    run_id=prepared.session_id,
                    message=(
                        "Post-crawl internal link scoring failed — page link scores "
                        f"were NOT refreshed: {type(exc).__name__}: {exc}. Re-run it "
                        "with the site's Score Links command."
                    ),
                    context={"reason": "post_crawl_link_scoring_failed"},
                )
            )
            return
        summary = result.summary
        logger.info(
            "post-crawl link scoring for site %s: %s pages scored over %s internal links",
            prepared.site_id,
            summary.pages_scored,
            summary.edges_resolved,
        )

    async def _resolve_durable_queue(self, prepared: PreparedCrawl) -> object | None:
        """A crash-safe durable frontier when a host wired `work_queue_factory`; else
        None (the caller uses the in-memory frontier — fine for short runs, no resume).

        The factory lives host-side (where the matrx-runtime engine is): it creates the
        batch `global_execution` linked to this crawl session and returns a QueueBackend
        (see web_crawl/runtime_queue.py::RuntimeWorkQueueBackend). If durability is
        CONFIGURED but the factory fails, we DO NOT silently fall back to the in-memory
        frontier — that would invisibly re-create the no-resume bug. It fails loud.
        """
        if not has_ext("work_queue_factory"):
            return None
        # Short single-page runs (homepage bootstrap / site initialization)
        # don't need resume — minting a global_request + execution + one work
        # item per bootstrap is pure table growth. Full crawls only.
        if prepared.state.homepage_bootstrap or prepared.state.site_initialization:
            return None
        return await get_ext("work_queue_factory")(prepared)

    @staticmethod
    async def _finalize_durable_queue(
        queue_backend: object | None, status: str, *, error_message: str | None = None
    ) -> None:
        """Settle a durable frontier's batch execution when the run ends.

        Duck-typed (`finalize`) so the service stays engine-agnostic and the
        in-memory frontier is a no-op. Never raises — the crawl's own outcome
        (success, error, cancel) must always win the stream.
        """
        finalize = getattr(queue_backend, "finalize", None)
        if finalize is None:
            return
        try:
            await finalize(status, error_message=error_message)
        except Exception:
            logger.exception("durable frontier finalize(%s) failed", status)

    async def _build_crawler(
        self,
        prepared: PreparedCrawl,
        sink: DurableCrawlEventSink,
        queue_backend: object | None = None,
    ) -> tuple[SiteCrawler, CanonicalBodyPersister]:
        request = prepared.request
        body_persister = CanonicalBodyPersister(
            prepared.repository,
            prepared.state,
            file_manager=get_ext("file_manager"),
            root_url=prepared.root_url,
        )
        browser_pool = get_ext("browser_pool") if has_ext("browser_pool") else None
        # Per-host scrape policy (proxy type, content selectors, noise overrides)
        # authored in the domain-rules UI and stored in scraper.scrape_domain.
        # Until 2026-08-09 the canonical crawler never received it, so every
        # policy a user set was silently ignored on every site crawl while the
        # quick-scrape lane honoured it — a UI editing a setting nothing read.
        #
        # The L2 page cache is deliberately NOT wired here: a site crawl must
        # report the site's CURRENT state, and serving a cached parse would make
        # a re-crawl silently report stale content. The cache belongs to the
        # quick-scrape lane. The crawler already forces cache=None on its own
        # proxy-bypass retries for the same reason.
        domain_config = get_ext("domain_config") if has_ext("domain_config") else None
        wants_screenshots = (
            request.capture_screenshots or request.render_mode == RENDER_BROWSER_WITH_SCREENSHOT
        )
        if wants_screenshots and browser_pool is None:
            raise RuntimeError("screenshot capture requires the browser pool")
        effective_concurrency = request.concurrency
        if wants_screenshots and browser_pool is not None:
            effective_concurrency = min(request.concurrency, browser_pool.size)
        short_homepage_run = prepared.state.homepage_bootstrap or prepared.state.site_initialization
        crawler = SiteCrawler(
            run_id=prepared.session_id,
            config=SiteCrawlerConfig(
                base_url=prepared.root_url,
                max_pages=request.max_pages,
                max_depth=request.max_depth,
                concurrency=effective_concurrency,
                follow_subdomains=request.follow_subdomains,
                respect_robots=request.respect_robots,
                seed_from_sitemap=request.seed_from_sitemap,
                include_patterns=request.include_patterns,
                exclude_patterns=request.exclude_patterns,
                politeness_delay_ms=request.politeness_delay_ms,
                render_mode=request.render_mode,
                capture_screenshots=request.capture_screenshots,
                browser_navigation_timeout_ms=8_000 if short_homepage_run else 45_000,
                browser_settle_timeout_ms=2_500 if short_homepage_run else 5_000,
                seed_urls=request.seed_urls,
                list_mode=request.list_mode,
                host_rps=request.host_rps,
                host_burst=request.host_burst,
                user_agent_override=request.user_agent,
            ),
            # What the last crawl of this site discovered about the host's real
            # limit, so this one opens near it instead of re-probing from zero.
            # None (nothing learned yet, or an unreadable row) simply means the
            # ramp starts from the floor — never a failure.
            remembered_pacing=await load_remembered_pacing(
                prepared.site_id, host_key(prepared.root_url)
            ),
            event_sink=sink,
            # A durable frontier (crash-safe, resumable) when the host wired one; the
            # in-memory frontier otherwise. Short runs (initialize/bootstrap) never
            # pass one — they don't need resume.
            queue_backend=queue_backend or InMemoryQueueBackend(),
            body_persister=body_persister,
            browser_pool=browser_pool,
            domain_config=domain_config,
            screenshot_kinds=request.screenshot_kinds,
            strict_persistence=True,
            retain_results=False,
        )
        return crawler, body_persister

    async def run_prepared(self, emitter: Emitter, prepared: PreparedCrawl) -> None:
        async def before_completed() -> None:
            await self._populate_link_status_before_completion(prepared)

        sink = DurableCrawlEventSink(
            prepared.repository,
            prepared.state,
            prepared.broker,
            emitter,
            before_completed=before_completed,
        )
        crawler: SiteCrawler | None = None
        cancel_watcher: asyncio.Task[None] | None = None
        queue_backend: object | None = None
        crawl_settle = await _track_growth_stage(
            stage="crawl",
            site_id=prepared.site_id,
            ref_kind="crawl_session",
            ref_id=prepared.session_id,
        )
        crawl_settled = False
        try:
            await sink.emit(
                CrawlSessionCreatedEvent(
                    run_id=prepared.session_id,
                    session_id=prepared.session_id,
                    site_id=prepared.site_id,
                )
            )
            queue_backend = await self._resolve_durable_queue(prepared)
            crawler, _ = await self._build_crawler(prepared, sink, queue_backend=queue_backend)
            cancel_watcher = asyncio.create_task(
                self._watch_for_cancel(
                    prepared.session_id,
                    crawler,
                    prepared.repository,
                    lease_token=prepared.state.run_lease_token,
                )
            )
            await crawler.run()
            # Persist the discovered ceiling BEFORE the post-crawl analysis
            # below, which is the longest and most failure-prone stretch of the
            # run: what the crawl learned about the host is already true, and
            # losing it to an unrelated analysis error would make every future
            # crawl of this site re-probe.
            await save_learned_pacing(prepared.site_id, crawler.remembered_pacing())
            await reconcile_site_urls(
                site_id=prepared.site_id,
                organization_id=prepared.state.organization_id,
                user_id=prepared.state.user_id,
                root_url=prepared.root_url,
            )
            if prepared.state.homepage_bootstrap and not prepared.state.homepage_screenshot_id:
                raise RuntimeError("homepage bootstrap completed without a canonical screenshot")
            await crawl_settle(
                "completed",
                outcome={"mode": prepared.mode},
            )
            crawl_settled = True
            # Order matters: URL reconciliation fixes canonical pointers, link
            # scoring reads them, analysis may report on the resulting scores.
            await self._run_post_crawl_link_scoring(prepared, sink)
            await self._run_post_crawl_analysis(prepared, sink)
            await self._finalize_durable_queue(queue_backend, "completed")
            await emitter.send_end()
        except Exception as exc:
            if not crawl_settled:
                await crawl_settle(
                    "failed",
                    error={"type": type(exc).__name__, "message": str(exc)[:2000]},
                )
            # Positive URL facts are safe on an incomplete crawl.  Negative
            # presence reconciliation remains gated by coverage_qualified in
            # the persistence layer, so this cannot mark unseen pages missing.
            await self._reconcile_urls_after_incomplete_crawl(prepared, sink)
            # Best-effort terminal fact. If canonical persistence itself is the
            # failure, fail_session will also raise and the original error remains
            # the stream's fatal error through exception chaining. The durable
            # execution settles in a finally: even a double failure (emit AND
            # fail_session both raising) must not leave it RUNNING-unleased
            # forever — the watchdog could scream about that but never clear it.
            try:
                try:
                    await sink.emit(
                        CrawlCompletedEvent(
                            run_id=prepared.session_id,
                            pages_fetched=0,
                            pages_failed=1,
                            issues_count=0,
                            duration_ms=0,
                            status="failed",
                            error_message=f"{type(exc).__name__}: {exc}",
                        )
                    )
                except Exception:
                    await prepared.repository.fail_session(
                        prepared.session_id,
                        f"{type(exc).__name__}: {exc}",
                        lease_token=prepared.state.run_lease_token,
                    )
            finally:
                await self._finalize_durable_queue(
                    queue_backend, "failed", error_message=f"{type(exc).__name__}: {exc}"
                )
            raise
        except asyncio.CancelledError:
            if not crawl_settled:
                with contextlib.suppress(asyncio.CancelledError):
                    await asyncio.shield(crawl_settle("cancelled"))
            # A deploy/cancel may arrive after many redirects/canonicals were
            # already observed.  Preserve those facts before settling the run.
            with contextlib.suppress(asyncio.CancelledError):
                await asyncio.shield(self._reconcile_urls_after_incomplete_crawl(prepared, sink))
            try:
                await prepared.repository.fail_session(
                    prepared.session_id,
                    WORKER_STOPPED_ERROR,
                    lease_token=prepared.state.run_lease_token,
                )
            except Exception:
                logger.exception("failed to mark canceled crawl session failed")
            # Shield the settle so an already-cancelled task still lands the
            # terminal fact — otherwise the execution stays RUNNING forever.
            with contextlib.suppress(asyncio.CancelledError):
                await asyncio.shield(
                    self._finalize_durable_queue(
                        queue_backend,
                        "cancelled",
                        error_message="crawler worker stopped before completion",
                    )
                )
            raise
        finally:
            if cancel_watcher is not None:
                cancel_watcher.cancel()
                await asyncio.gather(cancel_watcher, return_exceptions=True)
            await prepared.broker.close()
            await self.brokers.remove(prepared.session_id, prepared.broker)

    async def run_initialize(self, emitter: Emitter, prepared: PreparedCrawl) -> None:
        """Initialize a site: homepage + identity FIRST (seconds), then the
        remaining steps concurrently. Per-step ``initialize_step`` events are
        the frontend contract; a slow step never blocks a finished one."""

        summary = SiteInitializationSummary()
        sink = DurableCrawlEventSink(
            prepared.repository,
            prepared.state,
            prepared.broker,
            emitter,
        )
        body_persister: CanonicalBodyPersister | None = None
        cancel_watcher: asyncio.Task[None] | None = None
        candidates: list[DiscoveredCandidate] = []
        extraction_succeeded = False
        # Concurrent steps checkpoint the shared summary and stream through
        # one emitter; serialize both behind a single lock.
        progress_lock = asyncio.Lock()

        async def emit_step(
            step: InitializeStepName,
            status: InitializeStepStatus,
            message: str,
            *,
            counts: dict[str, int] | None = None,
            error: str | None = None,
        ) -> None:
            async with progress_lock:
                await emitter.send_data(
                    InitializeStepEvent(
                        site_id=prepared.site_id,
                        session_id=prepared.session_id,
                        step=step,
                        status=status,
                        message=message,
                        counts=counts or {},
                        error=error,
                    )
                )

        async def finish_step(
            step: InitializeStepName,
            message: str,
            *,
            status: InitializeStepStatus = "complete",
            counts: dict[str, int] | None = None,
            error: str | None = None,
        ) -> None:
            async with progress_lock:
                try:
                    await prepared.repository.update_initialization(
                        prepared.site_id,
                        summary.model_dump(mode="json"),
                    )
                except Exception as exc:
                    self._record_initialization_error(summary, "site_update", exc)
                    logger.exception("failed to checkpoint site initialization after %s", step)
                await emitter.send_data(
                    InitializeStepEvent(
                        site_id=prepared.site_id,
                        session_id=prepared.session_id,
                        step=step,
                        status=status,
                        message=message,
                        counts=counts or {},
                        error=error,
                    )
                )

        try:
            await sink.emit(
                CrawlSessionCreatedEvent(
                    run_id=prepared.session_id,
                    session_id=prepared.session_id,
                    site_id=prepared.site_id,
                )
            )

            # ---- Step 1: identity — homepage fetch + immediate site write.
            await emit_step(
                "identity",
                "started",
                "Fetching the homepage and reading site identity…",
            )
            capture_ok = False
            try:
                crawler, body_persister = await self._build_crawler(prepared, sink)
                cancel_watcher = asyncio.create_task(
                    self._watch_for_cancel(
                        prepared.session_id,
                        crawler,
                        prepared.repository,
                    )
                )
                await crawler.run()
                if prepared.state.homepage_capture is None:
                    failure = await prepared.state.failure_for(prepared.root_url)
                    if failure is not None:
                        raise RuntimeError(
                            "Homepage fetch failed — "
                            f"{failure.error_class}: {failure.error_message}"
                        )
                    raise RuntimeError(
                        "Homepage fetch completed without a persisted snapshot; "
                        "inspect the crawl session for the upstream fetch or persistence failure"
                    )
                summary.homepage = "ok"
                capture_ok = True
            except Exception as exc:
                summary.homepage = "failed"
                self._record_initialization_error(summary, "identity", exc)
                try:
                    await prepared.repository.fail_session(
                        prepared.session_id,
                        f"{type(exc).__name__}: {exc}",
                        lease_token=prepared.state.run_lease_token,
                    )
                except Exception:
                    logger.exception("failed to mark initialization homepage session failed")
                await finish_step(
                    "identity",
                    f"Homepage failed: {type(exc).__name__}: {exc}",
                    status="failed",
                    error=f"{type(exc).__name__}: {exc}",
                )
            finally:
                if cancel_watcher is not None:
                    cancel_watcher.cancel()
                    await asyncio.gather(cancel_watcher, return_exceptions=True)
                    cancel_watcher = None

            if capture_ok:
                try:
                    capture = prepared.state.homepage_capture
                    assert capture is not None
                    candidates = extract_homepage_candidates(
                        capture.html,
                        base_url=capture.final_url,
                        summary=capture.summary,
                    )
                    extraction_succeeded = True
                    identity = derive_site_identity(candidates, summary=capture.summary)
                    identity_result = await prepared.repository.update_site_identity(
                        prepared.site_id,
                        identity,
                    )
                    summary.identity = identity_result
                    counts = {
                        "written": len(identity_result["written"]),
                        "skipped_existing": len(identity_result["skipped_existing"]),
                        "candidates": len(candidates),
                    }
                    await finish_step(
                        "identity",
                        (
                            f"Site identity persisted ({counts['written']} fields "
                            f"written, {counts['skipped_existing']} already set)."
                        ),
                        counts=counts,
                    )
                except Exception as exc:
                    self._record_initialization_error(summary, "identity", exc)
                    await finish_step(
                        "identity",
                        f"Identity persistence failed: {type(exc).__name__}: {exc}",
                        status="failed",
                        error=f"{type(exc).__name__}: {exc}",
                    )

            # ---- Steps 2-4: independent — run CONCURRENTLY. Each persists
            # its own results the moment it completes; each catches its own
            # failure so a slow or broken step never blocks the others.
            async def screenshots_step() -> None:
                if not capture_ok:
                    await finish_step(
                        "screenshots",
                        "Skipped because the homepage fetch did not produce a snapshot.",
                        status="skipped",
                    )
                    return
                await emit_step(
                    "screenshots",
                    "started",
                    "Capturing desktop and mobile homepage screenshots…",
                )
                try:
                    capture = prepared.state.homepage_capture
                    assert capture is not None
                    if not has_ext("browser_pool"):
                        raise RuntimeError("screenshot capture requires the browser pool")
                    browser_pool = get_ext("browser_pool")
                    captured = await browser_pool.fetch_with_capture(
                        capture.final_url,
                        timeout_ms=45_000,
                        settle_timeout_ms=5_000,
                        screenshot_kinds=list(INITIALIZATION_SCREENSHOT_KINDS),
                    )
                    shots = [
                        CapturedShot(
                            kind=shot.kind,
                            width=shot.width,
                            height=shot.height,
                            bytes=shot.bytes,
                        )
                        for shot in captured.screenshots
                    ]
                    actual_kinds = [shot.kind for shot in shots]
                    expected_kinds = list(INITIALIZATION_SCREENSHOT_KINDS)
                    if actual_kinds != expected_kinds:
                        raise RuntimeError(
                            f"screenshot capture was incomplete: expected={expected_kinds}, "
                            f"actual={actual_kinds}"
                        )
                    persister = body_persister or CanonicalBodyPersister(
                        prepared.repository,
                        prepared.state,
                        file_manager=get_ext("file_manager"),
                        root_url=prepared.root_url,
                    )
                    (
                        screenshot_ids,
                        prune_counts,
                    ) = await persister.persist_initialization_screenshots(
                        shots,
                        capture=capture,
                    )
                    summary.screenshots = {
                        "captured": len(screenshot_ids),
                        "kinds": list(screenshot_ids),
                        "retention": prune_counts,
                    }
                    if prune_counts.get("prune_failed"):
                        summary.warnings.append(
                            InitializationError(
                                step="screenshots",
                                error_type="ScreenshotPruneError",
                                message=(
                                    f"{prune_counts['prune_failed']} superseded "
                                    "screenshot(s) could not be soft-deleted"
                                ),
                            )
                        )
                    await finish_step(
                        "screenshots",
                        f"Captured {len(screenshot_ids)} canonical S3 screenshots.",
                        counts={"captured": len(screenshot_ids), **prune_counts},
                    )
                except Exception as exc:
                    self._record_initialization_error(summary, "screenshots", exc)
                    await finish_step(
                        "screenshots",
                        f"Screenshots failed: {type(exc).__name__}: {exc}",
                        status="failed",
                        error=f"{type(exc).__name__}: {exc}",
                    )

            async def sitemaps_step() -> None:
                await emit_step(
                    "sitemaps",
                    "started",
                    "Syncing sitemap documents into the canonical page registry…",
                )
                try:
                    sync_result = await sync_site_sitemaps(
                        site_id=prepared.site_id,
                        organization_id=prepared.state.organization_id,
                        user_id=prepared.state.user_id,
                        root_url=prepared.root_url,
                        session_id=prepared.session_id,
                    )
                    summary.sitemaps = sync_result.summary.model_dump(mode="json")
                    failed = bool(sync_result.errors and not sync_result.summary.found)
                    notices = summary.errors if failed else summary.warnings
                    for error in sync_result.errors:
                        notices.append(
                            InitializationError(
                                step="sitemaps",
                                error_type="SitemapSyncError",
                                message=error[:2_000],
                            )
                        )
                    await finish_step(
                        "sitemaps",
                        (
                            f"Synced {sync_result.summary.found} sitemap documents; upserted "
                            f"{sync_result.summary.pages_upserted} pages from "
                            f"{sync_result.summary.urls} URLs."
                            + (
                                " TRUNCATED at the sync bounds."
                                if sync_result.summary.truncated
                                else ""
                            )
                        ),
                        status="failed" if failed else "complete",
                        counts={
                            "found": sync_result.summary.found,
                            "urls": sync_result.summary.urls,
                            "pages_upserted": sync_result.summary.pages_upserted,
                        },
                    )
                except Exception as exc:
                    self._record_initialization_error(summary, "sitemaps", exc)
                    await finish_step(
                        "sitemaps",
                        f"Sitemap discovery failed: {type(exc).__name__}: {exc}",
                        status="failed",
                        error=f"{type(exc).__name__}: {exc}",
                    )

            async def discovered_step() -> None:
                if not extraction_succeeded:
                    await finish_step(
                        "discovered",
                        "Skipped because homepage candidate extraction did not complete.",
                        status="skipped",
                    )
                    return
                await emit_step(
                    "discovered",
                    "started",
                    "Writing pending discovered-item candidates…",
                )
                try:
                    capture = prepared.state.homepage_capture
                    assert capture is not None
                    counts = await prepared.repository.persist_discovered_items(
                        prepared.state,
                        candidates,
                        snapshot_id=capture.snapshot_id,
                    )
                    summary.discovered = {
                        "media": counts.get("media", 0),
                        "facts": counts.get("fact", 0),
                        "socials": counts.get("social", 0),
                        "links": counts.get("link", 0),
                        "identity": counts.get("identity", 0),
                    }
                    await finish_step(
                        "discovered",
                        f"Recorded {sum(counts.values())} pending candidates.",
                        counts=dict(summary.discovered),
                    )
                except Exception as exc:
                    self._record_initialization_error(summary, "discovered", exc)
                    await finish_step(
                        "discovered",
                        f"Candidate persistence failed: {type(exc).__name__}: {exc}",
                        status="failed",
                        error=f"{type(exc).__name__}: {exc}",
                    )

            await asyncio.gather(screenshots_step(), sitemaps_step(), discovered_step())

            await self._emit_initialization_progress(
                emitter,
                prepared,
                summary,
                step="url_reconciliation",
                status="started",
                message="Reconciling every observed URL to one canonical page…",
            )
            try:
                reconciliation = await reconcile_site_urls(
                    site_id=prepared.site_id,
                    organization_id=prepared.state.organization_id,
                    user_id=prepared.state.user_id,
                    root_url=prepared.root_url,
                )
                summary.url_reconciliation = reconciliation.summary.model_dump(mode="json")
                await self._emit_initialization_progress(
                    emitter,
                    prepared,
                    summary,
                    step="url_reconciliation",
                    status="ok",
                    message=(
                        f"Matched {reconciliation.summary.aliases_matched} URL aliases "
                        "to canonical pages."
                    ),
                )
            except Exception as exc:
                self._record_initialization_error(summary, "url_reconciliation", exc)
                await self._emit_initialization_progress(
                    emitter,
                    prepared,
                    summary,
                    step="url_reconciliation",
                    status="failed",
                    message=f"URL reconciliation failed: {type(exc).__name__}: {exc}",
                )

            try:
                await prepared.repository.update_initialization(
                    prepared.site_id,
                    summary.model_dump(mode="json"),
                    completed=True,
                )
                await self._emit_initialization_progress(
                    emitter,
                    prepared,
                    summary,
                    step="site_update",
                    status="ok",
                    message="Site initialization summary saved.",
                )
            except Exception as exc:
                self._record_initialization_error(summary, "site_update", exc)
                await self._emit_initialization_progress(
                    emitter,
                    prepared,
                    summary,
                    step="site_update",
                    status="failed",
                    message=f"Site summary update failed: {type(exc).__name__}: {exc}",
                )
            await emitter.send_end()
        except asyncio.CancelledError:
            try:
                await prepared.repository.fail_session(
                    prepared.session_id,
                    "CancelledError: initialization worker stopped before completion",
                    lease_token=prepared.state.run_lease_token,
                )
            except Exception:
                logger.exception("failed to mark canceled initialization session failed")
            raise
        finally:
            if cancel_watcher is not None:
                cancel_watcher.cancel()
                await asyncio.gather(cancel_watcher, return_exceptions=True)
            await prepared.broker.close()
            await self.brokers.remove(prepared.session_id, prepared.broker)

    @staticmethod
    def _record_initialization_error(
        summary: SiteInitializationSummary,
        step: InitializationStep,
        exc: Exception,
    ) -> None:
        error = InitializationError(
            step=step,
            error_type=type(exc).__name__,
            message=str(exc)[:2_000],
        )
        if error not in summary.errors:
            summary.errors.append(error)

    @staticmethod
    async def _emit_initialization_progress(
        emitter: Emitter,
        prepared: PreparedCrawl,
        summary: SiteInitializationSummary,
        *,
        step: InitializationStep,
        status: InitializationStepStatus,
        message: str,
    ) -> None:
        await emitter.send_data(
            SiteInitializationProgressEvent(
                site_id=prepared.site_id,
                session_id=prepared.session_id,
                step=step,
                status=status,
                message=message,
                summary=summary,
            )
        )

    async def cancel(self, ctx: AppContext, session_id: str) -> None:
        repository = WebCrawlRepository(build_user_claims(ctx))
        session = await repository.assert_session_access(session_id)
        await repository.assert_site_editor(str(session.site_id), ctx.user_id)
        await repository.request_cancel(session_id, ctx.user_id)
        await self.controls.cancel(session_id)

    async def _watch_for_cancel(
        self,
        session_id: str,
        crawler: SiteCrawler,
        repository: WebCrawlRepository,
        *,
        lease_token: str | None = None,
    ) -> None:
        """Poll the durable cancel signal — and keep this run's lease alive.

        The heartbeat is what lets another process tell a LIVE run from a
        crashed one (`run_lease_is_live`). Losing the lease means someone else
        now owns this session: this run stops immediately rather than racing
        the new owner's writes and its event sequence.
        """
        last_heartbeat = 0.0
        while True:
            if self.controls.is_cancelled(session_id):
                crawler.cancel()
                return
            # The durable signal makes cancellation work even when the command
            # lands on another process/container than the active crawl.
            try:
                if await repository.is_cancel_requested(session_id):
                    crawler.cancel()
                    return
            except Exception:
                logger.warning(
                    "durable cancel poll failed for crawl session %s",
                    session_id,
                    exc_info=True,
                )
            now = asyncio.get_running_loop().time()
            if lease_token and now - last_heartbeat >= RUN_LEASE_HEARTBEAT_EVERY.total_seconds():
                last_heartbeat = now
                try:
                    if not await repository.heartbeat_run_lease(session_id, lease_token):
                        logger.error(
                            "crawl session %s lost its run lease (%s) to another process — "
                            "stopping this run so the new owner runs alone",
                            session_id,
                            lease_token,
                        )
                        crawler.cancel()
                        return
                except Exception:
                    logger.warning(
                        "run-lease heartbeat failed for crawl session %s",
                        session_id,
                        exc_info=True,
                    )
            await asyncio.sleep(1.0)


_SERVICE = WebCrawlService()


def get_web_crawl_service() -> WebCrawlService:
    return _SERVICE


__all__ = [
    "PreparedAnalysis",
    "PreparedCrawl",
    "PreparedGscSync",
    "PreparedLinkCheck",
    "PreparedLinkScore",
    "PreparedLinkResolution",
    "PreparedSitemapSync",
    "PreparedUrlReconciliation",
    "WebCrawlService",
    "get_web_crawl_service",
]
