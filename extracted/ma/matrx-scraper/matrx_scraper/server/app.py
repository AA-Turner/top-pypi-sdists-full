"""
Standalone FastAPI app factory for the scraper microservice.

Creates a fully wired application with auth middleware, database,
cache, domain config, and browser pool — no aidream dependency.
"""

from __future__ import annotations

import asyncio
import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from matrx_connect import require_authenticated, require_authenticated_or_service
from matrx_connect.middleware import AuthMiddleware
from matrx_orm import call_function
from matrx_utils import vcprint

from matrx_scraper._ext import configure_ext, get_ext, has_ext
from matrx_scraper.browser_pool import PLAYWRIGHT_AVAILABLE
from matrx_scraper.db import PACKAGE_DB_NAME
from matrx_scraper.db.web import WEB_DB_NAME
from matrx_scraper.server.config import ServerConfig
from matrx_utils import capture_error

_DEFAULT_CORS_ORIGIN_REGEX = (
    r"^(?:"
    r"https://(?:[a-z0-9-]+\.)*aimatrx\.com"
    r"|https://(?:[a-z0-9-]+\.)*aidream\.ai"
    r"|https://(?:[a-z0-9-]+\.)*matrxserver\.com"
    r"|https?://localhost(?::\d+)?"
    r"|https?://127\.0\.0\.1(?::\d+)?"
    r"|https?://\[::1\](?::\d+)?"
    r"|https://(?:[a-z0-9-]+\.)*vercel\.app"
    r")$"
)

try:
    PACKAGE_VERSION = version("matrx-scraper")
except PackageNotFoundError:
    PACKAGE_VERSION = "unknown"

_ACCESS_LEVEL_TO_DB: dict[str, str] = {
    "read": "viewer",
    "write": "editor",
    "admin": "admin",
}


async def canonical_file_access_allowed(
    user_id: str,
    resource_type: str,
    resource_id: str,
    level: str,
) -> bool:
    if not user_id or not resource_id:
        return False
    try:
        db_level = _ACCESS_LEVEL_TO_DB[level]
    except KeyError:
        raise ValueError(
            f"unknown file access level {level!r}; expected one of {sorted(_ACCESS_LEVEL_TO_DB)}"
        ) from None
    if resource_type == "file":
        return bool(
            await call_function(
                WEB_DB_NAME,
                "files",
                "has_access_for",
                user_id,
                resource_id,
                db_level,
            )
        )
    return bool(
        await call_function(
            WEB_DB_NAME,
            "iam",
            "has_access_for",
            user_id,
            resource_type,
            resource_id,
            db_level,
        )
    )


def _configure_standalone_filesystem(config: ServerConfig) -> str:
    """Provide the legacy file helpers with a safe standalone workspace.

    The crawler's HTML parser still uses ``matrx_files.FileManager`` for its
    cached EasyList data. ``FileManager`` resolves ``settings.BASE_DIR``
    lazily, so a standalone scraper without an AI Dream settings object used
    to fail only after the first page had been fetched. BASE_DIR is config,
    not an environment variable — ``matrx_utils.conf`` no longer reads a
    ``BASE_DIR`` env var at all. Wire it explicitly via ``configure_settings``
    (a host, e.g. aidream, may have already configured it earlier in this
    process — that registration stays authoritative and this is a no-op).
    """
    import types

    from matrx_utils.conf import configure_settings, settings

    base_dir = config.base_dir  # from MATRX_SCRAPER_BASE_DIR, a real per-deploy setting
    Path(base_dir).mkdir(parents=True, exist_ok=True)

    if not getattr(settings, "_configured", False):
        configure_settings(
            types.SimpleNamespace(BASE_DIR=base_dir, TEMP_DIR=os.path.join(base_dir, "temp")),
            env_first=True,
        )

    return base_dir


class ScraperStartupError(RuntimeError):
    """A startup capability could not be brought up.

    Its own exception type so a boot failure is one grep away from every other
    RuntimeError in the log, and so a test can pin the loudness without matching
    on prose. The message is the SHORT pointer; the full state and the fix are in
    the red banner :func:`_fatal_capability` prints immediately before raising.
    """


def _fatal_capability(capability: str, exc: BaseException, *, breaks: str, fix: str) -> None:
    """Scream, then refuse to boot. Never returns.

    WHY NONE OF THE STARTUP CAPABILITIES DEGRADE (2026-08-09). Each of these used
    to be a swallowed `except: print(WARNING)`, which made sense while the whole
    `scraper.*` database binding was itself optional. It no longer is (ee01821d6):
    every init below runs AFTER a pool that already bound and probed successfully,
    so an exception here is not "the optional thing is absent" — it is a missing
    table, a bad grant, or schema drift. There is no retry loop behind any of
    them, so "degraded" means degraded FOREVER, and nobody reads stderr on a
    Coolify container: the server would sit there reporting itself alive while
    every scrape re-fetched at full cost, or every crawl ignored per-host policy.
    A refused boot is loud in ten seconds and fixed in minutes; a silent
    degradation bleeds money for weeks. Crash is the honest posture.

    This is the boot-time layer. The independent second layer is
    :func:`_readiness_snapshot`, which fails `/health/ready` on the same
    capabilities — so if a future change ever softens one of these back into a
    warning, readiness still refuses to call the server healthy.
    """
    vcprint(
        data={
            "capability": capability,
            "exception_type": type(exc).__name__,
            "exception": str(exc),
            "what_breaks_if_we_continue": breaks,
            "how_to_fix": fix,
        },
        title=f"🚨 SCRAPER STARTUP GATE — '{capability}' FAILED TO INITIALIZE",
        color="red",
        pretty=True,
    )
    raise ScraperStartupError(
        f"startup capability {capability!r} failed to initialize ({type(exc).__name__}: {exc}) "
        "— see the red SCRAPER STARTUP GATE banner above for what breaks and how to fix it"
    ) from exc


def _readiness_snapshot() -> tuple[dict[str, object], int]:
    from matrx_files.cloud_sync.permissions import get_access_checker
    from matrx_files.db import PACKAGE_DB_NAME as FILES_DB_NAME
    from matrx_orm import is_database_registered
    from matrx_utils.conf import settings as _matrx_settings

    base_dir = str(_matrx_settings.BASE_DIR)
    domain_config_healthy = False
    if has_ext("domain_config"):
        try:
            domain_config_healthy = bool(getattr(get_ext("domain_config"), "healthy", False))
        except Exception:
            domain_config_healthy = False
    checks = {
        "database": is_database_registered(PACKAGE_DB_NAME),
        "orm": is_database_registered(PACKAGE_DB_NAME),
        "cache": has_ext("cache"),
        "domain_config": domain_config_healthy,
        "browser_pool": has_ext("browser_pool"),
        "web_database": is_database_registered(WEB_DB_NAME),
        "files_database": is_database_registered(FILES_DB_NAME),
        "file_access_checker": get_access_checker() is not None,
        "file_manager": has_ext("file_manager"),
        "canonical_file_pipeline": bool(
            has_ext("canonical_file_pipeline_ready") and get_ext("canonical_file_pipeline_ready")
        ),
        "filesystem": bool(base_dir and Path(base_dir).is_dir() and os.access(base_dir, os.W_OK)),
    }
    try:
        file_manager = get_ext("file_manager")
        checks["s3"] = bool(
            file_manager.sync_engine is not None
            and file_manager.sync_engine._config.storage_backend == "s3"
            and file_manager.cloud.is_configured("s3")
            and file_manager.sync_engine._config.resolve_s3_bucket()
        )
    except Exception:
        checks["s3"] = False
    # CREDENTIALS_ENCRYPTION_KEY must be EXPLICITLY set (the battery's
    # SUPABASE_SECRET_KEY derivation fallback would round-trip fine with the
    # wrong key, so env presence is part of the check) and must survive a
    # local encrypt/decrypt round-trip through the matrx-orm secrets battery.
    # Prerequisite for direct vault reads replacing the aidream credential
    # endpoint. No DB access, nothing secret in the response.
    try:
        from matrx_orm.secrets_battery import decrypt_value, encrypt_value

        checks["credentials_encryption"] = (
            bool(os.environ.get("CREDENTIALS_ENCRYPTION_KEY"))
            and decrypt_value(encrypt_value("selftest")) == "selftest"
        )
    except Exception:
        checks["credentials_encryption"] = False
    required = {
        "filesystem",
        "web_database",
        "files_database",
        "file_access_checker",
        "file_manager",
        "canonical_file_pipeline",
        "s3",
    }
    # The page cache is unconditional and its init is fatal, so a live server
    # always has it. Requiring it here is the second, independent layer: if a
    # future change ever softens the boot gate back into a warning, readiness
    # still refuses to call a cache-less server healthy.
    required.add("cache")
    # The domain-config store is unconditional, so it is unconditionally
    # required. It used to be required only `if has_ext("domain_config")` —
    # i.e. only once it had already started successfully, which is the one case
    # that cannot fail. A store that failed to start reported READY while every
    # fetch silently ran on default policy.
    required.add("domain_config")
    # The browser pool is required on any image that CAN run it. The gate is a
    # real import probe, not a toggle: an image built without the `browser`
    # extra genuinely cannot render, and holding it at not-ready forever would
    # take a healthy fetch-only deployment out of rotation.
    if PLAYWRIGHT_AVAILABLE:
        required.add("browser_pool")
    failed = sorted(name for name in required if not checks[name])
    return (
        {
            "status": "ok" if not failed else "not_ready",
            **checks,
            "failed_components": failed,
        },
        200 if not failed else 503,
    )


# Cadence of the work-item lease reaper (seconds). Well under the item lease
# (DEFAULT_ITEM_LEASE_SECONDS=600) so a dead worker's items return promptly.
# CAPS constant — a code push to change, never an env var.
WORK_ITEM_REAPER_INTERVAL_SECONDS: float = 60.0

# Max crawl sessions each crash-resume sweep continues (sequentially).
# CAPS constant — bound the recovery work, never stampede.
CRASH_RESUME_SWEEP_LIMIT: int = 5
# Sweep cadence. A crashed run only becomes reapable after STALE_SESSION_AFTER
# (30 min of silence), so a boot-only sweep would miss any session that goes
# stale AFTER boot — the loop is the reconciliation the durable-work-queue
# standard requires. CAPS constant.
CRASH_RESUME_INTERVAL_SECONDS: float = 600.0

# Cadence of the stale-session reaper. It runs in its OWN loop, never behind the
# resumer: `resume_crashed_sessions` AWAITS each continued crawl to completion,
# and a full-site crawl legitimately takes hours. While one was in flight the
# reaper did not run at all, so the "reap after 30 minutes of silence" promise
# silently degraded to "reap whenever the last resume finishes, or at the next
# deploy" — live case 2026-08-15: session c5f5d8c6 sat `queued` for 76 minutes.
# CAPS constant.
STALE_SESSION_REAPER_INTERVAL_SECONDS: float = 600.0


async def _run_stale_session_reaper() -> None:
    """Mark orphaned queued/running sessions failed, forever, on a cadence
    NOTHING else can block. Deliberately separate from the crash-resume loop:
    this sweep is one bounded UPDATE, while a resume runs a whole crawl."""
    from matrx_scraper.web_crawl.persistence import WebCrawlRepository

    while True:
        try:
            reaped = await WebCrawlRepository.fail_stale_sessions()
            if reaped:
                print(
                    f"[scraper-server] marked {reaped} orphaned crawl session(s) failed",
                    file=sys.stderr,
                    flush=True,
                )
        except asyncio.CancelledError:
            raise
        except Exception as e:  # noqa: BLE001 — recovery must never kill the server
            print(
                f"[scraper-server] WARNING: stale-session reap failed (will retry): {e}",
                file=sys.stderr,
                flush=True,
            )
            await capture_error(e, kind="scraper_stale_session_reap_failed")
        await asyncio.sleep(STALE_SESSION_REAPER_INTERVAL_SECONDS)


async def _run_crash_resume_loop(service) -> None:
    """Fail-then-resume reconciliation, forever: reap sessions whose process
    died (stale heartbeat), then continue the recent ones from their durable
    frontiers. Sequential within a sweep; a sweep blip is loud-logged and the
    loop continues; cancellation propagates for shutdown.

    The reap here keeps `fail_stale_sessions` immediately BEFORE the resume
    candidate read (a session is only resumable once it has been marked failed),
    and is cheap + idempotent. The standalone `_run_stale_session_reaper` is what
    guarantees the reap still happens on cadence while this sweep is inside a
    multi-hour resumed crawl.
    """
    from matrx_scraper.web_crawl.persistence import WebCrawlRepository

    while True:
        try:
            reaped = await WebCrawlRepository.fail_stale_sessions()
            if reaped:
                print(
                    f"[scraper-server] marked {reaped} orphaned crawl session(s) failed",
                    file=sys.stderr,
                    flush=True,
                )
            resumed = await service.resume_crashed_sessions(limit=CRASH_RESUME_SWEEP_LIMIT)
            if resumed:
                print(
                    f"[scraper-server] crash-resume: continued {resumed} crawl session(s) "
                    "from their durable frontiers",
                    file=sys.stderr,
                    flush=True,
                )
        except asyncio.CancelledError:
            raise
        except Exception as e:  # noqa: BLE001 — recovery must never kill the server
            print(
                f"[scraper-server] WARNING: crash-resume sweep failed (will retry): {e}",
                file=sys.stderr,
                flush=True,
            )
            await capture_error(e, kind="scraper_crash_resume_failed")
        await asyncio.sleep(CRASH_RESUME_INTERVAL_SECONDS)


async def _run_work_item_reaper(engine) -> None:
    """Return expired in-flight work items to pending, forever. A sweep blip is
    loud-logged and the loop continues; cancellation propagates for shutdown."""
    from datetime import UTC, datetime

    while True:
        try:
            reclaimed = await engine.store.reclaim_expired_work_items(now=datetime.now(UTC))
            if reclaimed:
                print(
                    f"[scraper-server] work-item reaper returned {reclaimed} expired "
                    "in-flight item(s) to pending (a worker died mid-claim)",
                    file=sys.stderr,
                    flush=True,
                )
        except asyncio.CancelledError:
            raise
        except Exception as e:  # noqa: BLE001 — a sweep blip must never kill recovery
            print(
                f"[scraper-server] WARNING: work-item reaper sweep failed (will retry): {e}",
                file=sys.stderr,
                flush=True,
            )
            await capture_error(e, kind="scraper_work_item_reap_failed")
        await asyncio.sleep(WORK_ITEM_REAPER_INTERVAL_SECONDS)


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    config: ServerConfig = app.state.config
    _configure_standalone_filesystem(config)

    domain_config_store = None
    browser_pool = None
    file_manager = None
    try:
        from matrx_scraper.db.web import bootstrap_web_db

        bootstrap_web_db()
        print(
            "[scraper-server] canonical web database registered (matrx_web)",
            file=sys.stderr,
            flush=True,
        )
    except Exception as e:
        raise RuntimeError("canonical web database bootstrap failed") from e
    try:
        from matrx_files import FileManager, configure_access_checker
        from matrx_files.cloud_sync import CloudSyncConfig
        from matrx_files.db import bind_to_host

        bind_to_host(WEB_DB_NAME)
        configure_access_checker(canonical_file_access_allowed, sync_checker=None)
        cloud_sync = CloudSyncConfig(storage_backend="s3")
        file_manager = FileManager(
            "matrx-scraper-canonical",
            new_instance=True,
            cloud_sync=cloud_sync,
        )
        bucket = (cloud_sync.resolve_s3_bucket() or "").strip()
        if not file_manager.cloud.is_configured("s3") or not bucket:
            raise RuntimeError(
                "canonical S3 backend is unavailable; set AWS_ACCESS_KEY_ID, "
                "AWS_SECRET_ACCESS_KEY, AWS_REGION, and AWS_S3_DEFAULT_BUCKET "
                "on the scraper Coolify service (same values as ai-dream-server)"
            )
        await asyncio.wait_for(
            file_manager.cloud.s3.assert_bucket_accessible_async(bucket),
            timeout=15.0,
        )

        from matrx_files.db.readiness import probe_database_readiness

        from matrx_scraper.db.models_web import Screenshot, Snapshot

        files_ready = await probe_database_readiness(max_age_seconds=0)
        if not files_ready.ready:
            raise RuntimeError(f"canonical files database probe failed: {files_ready.error_type}")
        await Snapshot.filter(body_file_id__isnull=True).limit(1).all()
        await Screenshot.filter(file_id__isnull=True).limit(1).all()
        print(
            "[scraper-server] canonical files database and S3 writer ready",
            file=sys.stderr,
            flush=True,
        )
    except Exception as e:
        raise RuntimeError("canonical files/S3 bootstrap failed") from e
    # `scraper.*` binds to the SAME ONE database as `web.*` (same resolver), and
    # binding is FATAL. It used to be "optional": a failure here left the server
    # up with the page cache, domain policy, and retry queue silently dark —
    # or, worse, pointed at a second Postgres nobody read.
    try:
        from matrx_scraper.db import bootstrap_db

        bootstrap_db()
        print(
            "[scraper-server] scraper database registered (matrx_scraper)",
            file=sys.stderr,
            flush=True,
        )
    except Exception as e:
        raise RuntimeError("scraper database bootstrap failed") from e

    # Standalone host owns the same package-level durable capture injection
    # that aidream/package_integration installs in monolith mode.
    from matrx_orm import record_error
    from matrx_utils import configure_error_capture

    configure_error_capture(record_error)

    # ONE DATABASE runtime proof (this service is the incident site): ask every
    # registered pool which physical Postgres it actually reached and scream if
    # `scraper.*` and `web.*` ever disagree again. Env vars cannot answer this —
    # a var set only here is exactly how the split happened. Loud, never fatal;
    # the fatal part is the binding above. Static twin: aidream
    # scripts/check_one_database.py.
    try:
        from matrx_orm.core.one_database import audit_one_database

        await audit_one_database(platform_config_name=WEB_DB_NAME)
    except Exception as e:  # noqa: BLE001 — a guard never breaks boot
        print(f"[scraper-server] one-database check skipped: {e}", file=sys.stderr, flush=True)

    ext_kwargs: dict = {}

    if file_manager is not None:
        ext_kwargs["file_manager"] = file_manager
        ext_kwargs["canonical_file_pipeline_ready"] = True

    try:
        from matrx_scraper.cache import TwoTierCache
        from matrx_scraper.db.models_scraper import ScrapeParsedPage

        await ScrapeParsedPage.filter().limit(1).exists()
        ext_kwargs["cache"] = TwoTierCache()
        print("[scraper-server] Two-tier cache enabled", file=sys.stderr, flush=True)
    except Exception as e:
        # A cache is a cost/latency optimization, but the thing that fails here
        # is a `scraper.scrape_parsed_page` probe on an ALREADY-BOUND pool — that
        # is a schema/grant signal, not a cache-health one, and the same schema
        # carries the retry queue and the failure log.
        _fatal_capability(
            "cache",
            e,
            breaks="Every scrape re-fetches every page at full network + proxy + "
            "time cost, forever, with the server reporting itself alive.",
            fix="The scraper.* pool bound, so this is the schema, not the "
            "connection: confirm scraper.scrape_parsed_page exists in the ONE "
            "database (Matrx Main) and that SUPABASE_MATRIX_USER can SELECT it. "
            "If the table moved, regenerate models (python db/generate.py).",
        )

    try:
        from matrx_scraper.domain_config import PostgresDomainConfigStore

        domain_config_store = PostgresDomainConfigStore()
        await domain_config_store.start()
        ext_kwargs["domain_config"] = domain_config_store
        print("[scraper-server] Domain config store started", file=sys.stderr, flush=True)
    except Exception as e:
        # `PostgresDomainConfigStore.start()` already raises on a failed initial
        # load and leaves `healthy=False`; this except was the only thing turning
        # that into a warning. Readiness holds the server at 503 forever after a
        # failure here, and nothing retries — so it is never going to become
        # healthy on its own, and staying up is a lie.
        _fatal_capability(
            "domain_config",
            e,
            breaks="Every fetch and every crawl silently ignores per-host policy "
            "(rate limits, proxy rules, path patterns) and runs on defaults — "
            "and /health/ready would stay 503 forever with no recovery path.",
            fix="Confirm scraper.scrape_domain / scrape_domain_* / "
            "scrape_path_pattern exist in the ONE database (Matrx Main) and are "
            "readable by SUPABASE_MATRIX_USER.",
        )

    # Gated on the real capability, never a toggle: an image built without the
    # `browser` extra has no Playwright to start. Readiness keys off the same
    # probe, so on an image that CAN render, a failed pool is not-ready.
    if PLAYWRIGHT_AVAILABLE:
        try:
            from matrx_scraper.browser_pool import PlaywrightBrowserPool

            # Size is the code CAPS constant (DEFAULT_BROWSER_POOL_SIZE), never
            # an env var — see browser_pool.py for why.
            browser_pool = PlaywrightBrowserPool()
            await browser_pool.start()
            ext_kwargs["browser_pool"] = browser_pool
            print(
                f"[scraper-server] Browser pool started (size={browser_pool.size})",
                file=sys.stderr,
                flush=True,
            )
        except Exception as e:
            # Only reachable on an image that HAS Playwright — so this is a real
            # failure to launch Chromium, not a missing extra. Nothing restarts
            # the pool, so the loss is permanent.
            _fatal_capability(
                "browser_pool",
                e,
                breaks="Every JS-rendered page, every screenshot, and the whole "
                "ai_browser surface fails — on the ONE container that is "
                "supposed to be the platform's only Playwright runtime.",
                fix="Chromium is present (the `browser` extra imported) but would "
                "not launch: check the container has its Playwright browsers "
                "installed (playwright install chromium) and enough shared "
                "memory / RAM — the service is capped at 4 GB.",
            )
    else:
        print(
            "[scraper-server] WARNING: playwright is not installed — no rendering, "
            "screenshots, or ai_browser on this image (install the `browser` extra)",
            file=sys.stderr,
            flush=True,
        )

    # Durable crawl frontier — runtime.work_item over the same Supabase project
    # the web DB pool already points at. FATAL on failure: silently skipping
    # this registration is exactly how the frontier ran dark for weeks while
    # every crawl died with its process (FOUND_DEFECTS 2026-07-29).
    work_item_reaper: asyncio.Task[None] | None = None
    try:
        import matrx_runtime
        from matrx_runtime import ExecutionEngine, OrmExecutionStore

        from matrx_scraper.web_crawl.runtime_queue import make_work_queue_factory

        matrx_runtime.configure(db_config_name=WEB_DB_NAME)
        # configure() silently SKIPS binding when the config name isn't
        # registered; ensure_bound() forces resolution and raises if the pool
        # never bound — the doctrine bans a silent config failure.
        from matrx_runtime.db import ensure_bound as _runtime_ensure_bound

        _runtime_ensure_bound()
        runtime_engine = ExecutionEngine(OrmExecutionStore())
        ext_kwargs["work_queue_factory"] = make_work_queue_factory(runtime_engine)
        print(
            "[scraper-server] Durable crawl frontier enabled (runtime.work_item)",
            file=sys.stderr,
            flush=True,
        )
    except Exception as e:
        raise RuntimeError("durable crawl frontier bootstrap failed") from e

    if config.brave_api_key:
        import os

        # ONE name. The Brave engine reads BRAVE_SEARCH_API_KEY_PRO_AI and
        # nothing else (Arman's ruling 2026-08-20) — the retired names returned
        # a degraded search rather than an error, so mirroring a value into them
        # would quietly re-create exactly the fallback that was deleted.
        os.environ.setdefault("BRAVE_SEARCH_API_KEY_PRO_AI", config.brave_api_key)

    if ext_kwargs:
        configure_ext(**ext_kwargs)

    from matrx_scraper.web_crawl.persistence import WebCrawlRepository

    reaped_sessions = await WebCrawlRepository.fail_stale_sessions()
    if reaped_sessions:
        print(
            f"[scraper-server] ERROR: marked {reaped_sessions} orphaned crawl session(s) failed",
            file=sys.stderr,
            flush=True,
        )

    # The work-item lease reaper: returns in-flight items whose worker died to
    # pending. Without it the frontier's crash-recovery guarantee is theater —
    # a dead process's claims would stay leased forever.
    work_item_reaper = asyncio.create_task(_run_work_item_reaper(runtime_engine))

    # Crash-resume reconciliation loop: reap stale sessions + continue recent
    # crashed ones from their durable frontiers — the durable-work-queue
    # standard's boot/ongoing reconciliation. Background + sequential; never
    # blocks boot, never stampedes.
    from matrx_scraper.web_crawl.service import get_web_crawl_service

    crash_resume = asyncio.create_task(_run_crash_resume_loop(get_web_crawl_service()))

    # Stale-session reaper, in its OWN task: the crash-resume loop above awaits
    # each continued crawl (hours), and while it does, nothing else was marking
    # orphaned queued/running sessions failed. This loop cannot be starved.
    stale_session_reaper = asyncio.create_task(_run_stale_session_reaper())

    print("[scraper-server] Ready", file=sys.stderr, flush=True)
    yield

    crash_resume.cancel()
    await asyncio.gather(crash_resume, return_exceptions=True)
    stale_session_reaper.cancel()
    await asyncio.gather(stale_session_reaper, return_exceptions=True)
    if work_item_reaper is not None:
        work_item_reaper.cancel()
        await asyncio.gather(work_item_reaper, return_exceptions=True)

    if browser_pool:
        try:
            await browser_pool.stop()
        except Exception:
            pass

    if domain_config_store:
        try:
            await domain_config_store.stop()
        except Exception:
            pass

    # The pool is owned by matrx-orm's shared AsyncDatabaseManager; closing it
    # here would race other ORM users.

    print("[scraper-server] Shutdown complete", file=sys.stderr, flush=True)


def create_app(config: ServerConfig | None = None) -> FastAPI:
    if config is None:
        config = ServerConfig.from_env()

    app = FastAPI(
        title="Matrx Scraper",
        description="Standalone web scraping microservice powered by matrx-scraper",
        version=PACKAGE_VERSION,
        lifespan=_lifespan,
    )

    app.state.config = config

    raw_origins = config.cors_allowed_origins.strip()
    allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    if "*" in allowed_origins:
        raise ValueError(
            "MATRX_SCRAPER_CORS_ALLOWED_ORIGINS cannot contain '*' for "
            "credentialed browser requests"
        )
    origin_regex = (
        None
        if allowed_origins
        else (config.cors_allowed_origin_regex.strip() or _DEFAULT_CORS_ORIGIN_REGEX)
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_origin_regex=origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=[
            "X-Crawl-Session-Id",
            "X-Site-Id",
            "X-Request-ID",
            "X-Conversation-ID",
        ],
    )

    # admin_token / admin_user_id intentionally NOT passed — the static
    # escape hatch was removed from matrx-connect's AuthMiddleware in 2026-05.
    # The standalone server now accepts only Supabase-signed JWTs.
    app.add_middleware(
        AuthMiddleware,
        jwt_secret=config.supabase_jwt_secret,
        jwks_url=(
            f"{config.supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"
            if config.supabase_url
            else None
        ),
        jwt_algorithms=("HS256", "ES256"),
    )

    from matrx_scraper.api import (
        browser_router,
        crawl_router,
        ext_router,
        preview_router,
        scrape_router,
    )

    # Admit EITHER a real user login OR an approved server (shared ADMIN_API_TOKEN
    # + optional X-Matrx-User-Id "act as" header). This is what lets aidream's
    # server-initiated calls (AI browser tools, unattended preview/cron) reach the
    # scraper — the user-login-only path 401'd them. The canonical primitive lives
    # in matrx_connect.service_auth (shared with the sandbox bridge + media-heal).
    #
    # organization_optional: every write route behind this dependency demands
    # its OWN explicit `organization_id` request-body field and validates it
    # itself (e.g. scrape_router.py's `if not (request.organization_id and
    # ...)`) — the tenant fact never comes from `ctx.organization_id` here.
    # The dependency's own X-Organization-Id requirement would be a second,
    # redundant gate this host does not use.
    scraper_caller = require_authenticated_or_service(
        config.admin_api_token,
        organization_optional=True,
        organization_optional_reason=(
            "every scraper write route validates its own request-body "
            "organization_id field; ctx.organization_id is never read"
        ),
    )

    app.include_router(
        scrape_router,
        prefix="/api/scraper",
        tags=["scrape"],
        dependencies=[Depends(scraper_caller)],
    )
    app.include_router(
        ext_router,
        prefix="/api/scraper",
        tags=["external"],
        dependencies=[Depends(scraper_caller)],
    )
    app.include_router(
        browser_router,
        prefix="/api/scraper",
        tags=["browser"],
        dependencies=[Depends(scraper_caller)],
    )
    app.include_router(
        preview_router,
        prefix="/api/scraper",
        tags=["preview"],
        dependencies=[Depends(scraper_caller)],
    )
    app.include_router(
        crawl_router,
        prefix="/api/scraper",
        tags=["crawler"],
        dependencies=[Depends(require_authenticated)],
    )

    @app.get("/health")
    async def health():
        return {
            "status": "ok",
            "service": "matrx-scraper",
            "version": PACKAGE_VERSION,
        }

    @app.get("/health/ready")
    async def health_ready() -> JSONResponse:
        payload, status_code = _readiness_snapshot()
        return JSONResponse(content=payload, status_code=status_code)

    @app.get("/health/version")
    async def health_version():
        """Build identity — "what is deployed?" without shell access.

        Mirrors aidream's `/health/version` contract: the package version is
        always present; the git SHA resolves from `GIT_SHA` (Docker build arg)
        or `SOURCE_COMMIT` (Coolify injects it at runtime) and degrades to
        "unknown" — never raises, a broken probe must not take down health.
        """
        return {
            "service": "matrx-scraper",
            "version": PACKAGE_VERSION,
            "git_sha": (os.environ.get("GIT_SHA") or os.environ.get("SOURCE_COMMIT") or "unknown"),
            "built_at": os.environ.get("BUILD_TIME") or "unknown",
            "branch": os.environ.get("COOLIFY_BRANCH"),
        }

    return app
