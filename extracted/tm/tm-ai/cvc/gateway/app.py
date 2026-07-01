"""
FastAPI application factory for the CVC gateway.

Wires up the redesigned cvc/gateway/ routers, manages the AIAgent
runtime (single in-process instance per worker), and serves the
React dashboard from cvc/web_dist/.
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger("cvc.gateway")

# CVC's web_dist (compiled React dashboard)
CVC_WEB_DIST = Path(__file__).resolve().parent.parent / "web_dist"


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """Initialize the AIAgent runtime + session DB on startup, clean up on shutdown.

    Also delegates to the legacy cvc.gateway_legacy lifespan so its state
    (_workspace_mgr, _manager, _tool_executor, _hermes_api_server, etc.)
    is initialised. The new package owns /api/chat, /api/sessions, etc.;
    the legacy owns /api/workspace, /api/dx, /api/setup, voice, telegram,
    and 80+ other routes. Both must be initialised for the merged app to
    behave like the v2.x line did.
    """
    from cvc.gateway.agent import init_runtime, shutdown_runtime

    # Run the legacy lifespan first — it sets up _workspace_mgr,
    # _manager, _tool_executor, the agent LLM background init,
    # telegram adapter, health poll, and the rest. If this fails
    # we still try our own init so /api/health and /api/chat
    # come up.
    legacy_lifespan_cm = None
    try:
        from cvc.gateway_legacy import lifespan as legacy_lifespan
        legacy_lifespan_cm = legacy_lifespan(app)
        await legacy_lifespan_cm.__aenter__()
    except Exception as e:
        logger.warning("Legacy lifespan failed to enter: %s", e)

    logger.info("CVC gateway starting...")
    try:
        await init_runtime()
    except Exception as e:
        logger.exception("Failed to initialise AIAgent runtime: %s", e)
        # Don't crash — let the gateway come up so /api/health works.

    # Load + start every channel whose config file is present under
    # ``~/.cvc/channels/*.yaml``. ``cvc setup`` writes these files. Each
    # adapter reads its own file via the schema-declared config keys,
    # so this works uniformly for all 7 first-class channels without
    # hard-coding any per-platform code in the gateway.
    try:
        from cvc.integrations.bootstrap import get_registry, start_all as _start_all
        from cvc.integrations.setup import channels_dir, list_all_saved_channels
        _reg = get_registry()
        # Swap the bootstrap-time echo + logging hooks for the real
        # CVC-engine implementations now that the runtime is up. We do
        # this BEFORE start_all so every newly-started adapter is
        # immediately wired to the production commit + agent pipeline.
        try:
            from cvc.integrations.cvc_bindings import (
                make_logging_commit_hook as _log_hook,
            )
            from cvc.integrations.cvc_bindings import (
                make_echo_agent_runner as _echo_runner,
            )
            # Real implementations are best-effort — if the CVC engine
            # isn't fully booted, the fallback logging + echo handlers
            # stay in place. That keeps channels from crashing the gateway.
            try:
                from cvc.operations.engine import CVCEngine as Engine  # noqa: F401
                from cvc.integrations.cvc_bindings import (
                    build_commit_hook,
                    build_agent_runner,
                )
                _reg.set_commit_hook(build_commit_hook())
                _reg.set_agent_runner(build_agent_runner())
                logger.info("Channels wired to real CVC commit + agent pipeline")
            except Exception as e:  # noqa: BLE001
                logger.info(
                    "Real channel hooks unavailable (%s); using fallback echo + logging hooks",
                    e,
                )
                _reg.set_commit_hook(_log_hook())
                _reg.set_agent_runner(_echo_runner())
        except Exception as e:  # noqa: BLE001
            logger.warning("Channel hook wiring skipped: %s", e)
        _configs: dict = {}
        for _name, _path in list_all_saved_channels():
            from cvc.integrations.setup import read_channels_config_from_path
            _cfg = read_channels_config_from_path(_path)
            if _cfg:
                _cfg["enabled"] = True
                _configs[_name] = _cfg
        if _configs:
            logger.info("Channels to start: %s", sorted(_configs.keys()))
            await _start_all(_configs)
        else:
            logger.info("No channel configs found in %s", channels_dir())
    except Exception as e:  # noqa: BLE001
        logger.warning("Channel startup skipped: %s", e)

    # Pre-build the AIAgent so the FIRST chat request is fast. This
    # absorbs the ~1.8s tool-schema-generation cost at startup, not on
    # the user's first message. Build is best-effort; if it fails the
    # first chat request will rebuild it lazily.
    try:
        import asyncio as _asyncio
        from cvc.gateway.agent import create_agent as _build_agent

        def _warm() -> None:
            try:
                _build_agent(session_id="__warmup__")
            except Exception as e:  # pragma: no cover
                logger.debug("AIAgent warmup failed (lazy rebuild will retry): %s", e)

        await _asyncio.get_running_loop().run_in_executor(None, _warm)
        logger.info("AIAgent warmed up.")
    except Exception as e:  # pragma: no cover
        logger.debug("AIAgent warmup skipped: %s", e)

    # C7: boot the spine retention loop. Idempotent — safe if the gateway
    # is reloaded in a single process (e.g. test harness).
    try:
        from cvc.events.retention import start as _retention_start
        _retention_start()
        logger.info("Event spine retention loop started.")
    except Exception as e:  # noqa: BLE001
        logger.debug("retention start failed (non-fatal): %s", e)

    try:
        yield
    finally:
        # C7: stop the spine retention loop so the gateway exits cleanly.
        try:
            from cvc.events.retention import stop as _retention_stop
            _retention_stop(timeout_s=3.0)
        except Exception as e:  # noqa: BLE001
            logger.debug("retention stop failed (non-fatal): %s", e)

        await shutdown_runtime()
        if legacy_lifespan_cm is not None:
            try:
                await legacy_lifespan_cm.__aexit__(None, None, None)
            except Exception as e:
                logger.warning("Legacy lifespan failed to exit cleanly: %s", e)
        logger.info("CVC gateway stopped.")


def create_app() -> FastAPI:
    """Build and return the FastAPI app instance."""
    app = FastAPI(
        title="CVC Gateway",
        version="3.3.6",
        lifespan=_lifespan,
    )

    # CORS — allow the dashboard's localhost dev origin
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Dashboard is local; tighten in prod
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount all routers
    from cvc.gateway.chat import router as chat_router
    from cvc.gateway.sessions import router as sessions_router
    from cvc.gateway.runs import router as runs_router
    from cvc.gateway.skills import router as skills_router
    from cvc.gateway.models import router as models_router
    # NOTE: no workspaces router in the new package. /api/workspace/*
    # is fully owned by the legacy cvc.gateway_legacy app, which uses
    # the real _workspace_mgr (init_workspace, switch_to, list_workspaces)
    # and re-scopes ToolExecutor. The new package previously had a
    # JSON-stub workspaces.py that shadowed the legacy's working routes
    # and returned 501 on /api/workspace/add — removed.
    from cvc.gateway.git_ops import router as git_router
    from cvc.gateway.ops import router as ops_router
    from cvc.gateway.health import router as health_router

    # v3.3.6 — Mount the dashboard routers that the legacy app
    # only includes via lifespan, so they exist on the new app
    # even if the legacy lifespan didn't fire cleanly. These own:
    #   /api/dx/cost, /api/dx/usage           (CostTicker, /api/dx/...)
    #   /api/personas, /api/personas/active    (persona switcher)
    #   /api/conversations                     (thread list/create)
    try:
        from cvc.dashboard.dx_api import router as dx_router
        # dx_api.py builds the router with prefix="/api/dx" already;
        # do NOT add another prefix here or /api/dx/cost will become
        # /api/dx/api/dx/cost.
        app.include_router(dx_router, tags=["dx"])
    except Exception as e:
        logger.warning("Could not mount /api/dx router: %s", e)
    try:
        from cvc.dashboard.personas_api import register_personas_routes
        register_personas_routes(app)
    except Exception as e:
        logger.warning("Could not mount /api/personas router: %s", e)
    try:
        from cvc.dashboard.conversations_api import router as conversations_router
        # conversations_api.py:41 builds the router with
        # prefix="/api/conversations" already; do NOT add another
        # prefix here.
        app.include_router(conversations_router, tags=["conversations"])
    except Exception as e:
        logger.warning("Could not mount /api/conversations router: %s", e)

    app.include_router(health_router, tags=["health"])
    app.include_router(chat_router, prefix="/api", tags=["chat"])
    app.include_router(sessions_router, prefix="/api", tags=["sessions"])
    app.include_router(runs_router, prefix="/api", tags=["runs"])
    app.include_router(skills_router, prefix="/api", tags=["skills"])
    app.include_router(models_router, prefix="/api", tags=["models"])
    # v3.3.43 — Hermes-catalog provider/model picker. Sourced from the
    # vendored Hermes Agent tree + models.dev cache, so the dashboard
    # shows 30+ providers (z.ai/GLM, Kimi, StepFun, Alibaba, OpenCode,
    # Kilo, Arcee, GMI, Ollama Cloud, Azure Foundry, …) without adding
    # a runtime dependency on `hermes-agent`.
    try:
        from cvc.gateway.catalog import router as catalog_router
        app.include_router(catalog_router, prefix="/api", tags=["catalog"])
    except Exception as e:
        logger.warning("Could not mount /api/catalog router: %s", e)
    app.include_router(git_router, prefix="/api/git", tags=["git"])

    # Channel adapters — Telegram / Discord / Slack / WhatsApp / Matrix /
    # Email / Webhook. The /api/channels/* surface lists, starts, stops
    # and probes every registered adapter, and the same router hosts the
    # platform webhooks (WhatsApp Cloud API, generic webhook). This is
    # what the dashboard's "Channels" panel talks to.
    try:
        from cvc.gateway.channels import router as channels_router
        app.include_router(channels_router, prefix="/api/channels", tags=["channels"])
    except Exception as e:
        logger.warning("Could not mount /api/channels router: %s", e)
    app.include_router(ops_router, prefix="/api/ops", tags=["ops"])

    # v3.4.12 — Event Spine (C5) — full activity timeline across all
    # workspaces/channels. Sibling to /api/ops/timeline but reads from
    # ~/.cvc/events/ (singular, append-only) instead of cognitive commits.
    try:
        from cvc.gateway.events import router as events_router
        app.include_router(events_router, prefix="/api", tags=["events"])
    except Exception as e:
        logger.warning("Could not mount /api/events router: %s", e)

    # Soul layer (P5) — life story view, user model inspector, dreams diary.
    # These endpoints expose the soul's growing understanding of its owner
    # so the dashboard can render the narrative arc, not just the commit log.
    try:
        from cvc.gateway.soul import router as soul_router
        app.include_router(soul_router, prefix="/api", tags=["soul"])
    except Exception as e:
        logger.warning("Could not mount /api/soul router: %s", e)

    # Universal adapter system (Phase 7.1) — every brain, capability matrix,
    # live health, negotiation. Powers the dashboard's "Brains" panel.
    try:
        from cvc.gateway.adapters import router as adapters_router
        app.include_router(adapters_router, prefix="/api", tags=["adapters"])
    except Exception as e:
        logger.warning("Could not mount /api/adapters router: %s", e)

    # Apple-grade security (Phase 7.2) — vault, audit log, network sentinel.
    # Powers the dashboard's "Security" panel.
    try:
        from cvc.gateway.security import router as security_router
        app.include_router(security_router, prefix="/api", tags=["security"])
    except Exception as e:
        logger.warning("Could not mount /api/security router: %s", e)

    # Swarm cluster layer (Phase 7.3) — peer identity, share policy,
    # known peers, broadcasts. Powers the dashboard's "Swarm" panel.
    try:
        from cvc.gateway.swarm import router as swarm_router
        app.include_router(swarm_router, prefix="/api", tags=["swarm"])
    except Exception as e:
        logger.warning("Could not mount /api/swarm router: %s", e)

    # Mount the legacy FastAPI app's remaining routes. The legacy god-file
    # has 100+ routes we don't want to re-implement (voice, telemetry, file
    # upload, copilot, etc.). The simplest, safest approach: walk the legacy
    # app's routes and copy the non-conflicting ones onto the new app.
    try:
        from cvc.gateway_legacy import app as legacy_app
        from starlette.routing import Route, WebSocketRoute, Mount

        # v3.3.6 — NARROW the exclusion list. v3.3.5 excluded every
        # ``/api/chat/*`` path, which shadowed the working legacy
        # routes for ``/api/chat/context_meter``,
        # ``/api/chat/reasoning_effort`` and
        # ``/api/chat/approval-mode`` (the dashboard polls all three
        # on mount). The new chat_router only owns ``/api/chat`` and
        # ``/api/ws/chat`` — list those explicitly so the rest of
        # the /api/chat/* tree falls through to the legacy handlers.
        # The conversations, personas, dx, models, git, ops, etc.
        # sub-trees are mounted above so they're already on the
        # new app; we still skip them here to avoid duplicates
        # with conflicting order.
        new_exact_paths = (
            "/api/chat",       # owned by cvc.gateway.chat
            "/api/ws/chat",    # owned by cvc.gateway.chat
            "/api/sessions",   # owned by cvc.gateway.sessions
            "/api/runs",       # owned by cvc.gateway.runs
            "/api/skills",     # owned by cvc.gateway.skills
            "/api/toolsets",   # owned by cvc.gateway.skills (mounted same)
            "/api/capabilities",
            "/api/models",     # owned by cvc.gateway.models
            "/api/git",        # owned by cvc.gateway.git_ops
            "/api/ops",        # owned by cvc.gateway.ops
            "/api/health",     # owned by cvc.gateway.health
            "/health",
            "/openapi.json", "/docs", "/redoc",
        )
        new_prefixes = (
            # Sub-trees whose routers are mounted ABOVE the legacy
            # walk. If we don't skip these we'd append duplicate
            # routes (FastAPI will pick the first match but it's
            # safer to skip them).
            "/api/dx",
            "/api/personas",
            "/api/conversations",
            # The websocket sub-trees owned by the legacy file that
            # we DON'T want to duplicate from legacy — these have
            # issues with concurrent mounts and the new chat layer
            # is the canonical one.
        )

        def _is_new_path(p: str) -> bool:
            if p in new_exact_paths:
                return True
            return any(p == pre or p.startswith(pre + "/") for pre in new_prefixes)

        copied = 0
        for r in legacy_app.routes:
            if isinstance(r, (Route, WebSocketRoute)):
                if not _is_new_path(r.path):
                    # Append directly
                    app.routes.append(r)
                    copied += 1
            elif isinstance(r, Mount):
                if not _is_new_path(r.path):
                    app.routes.append(r)
                    copied += 1
        logger.info("Mounted %d legacy routes onto new app", copied)
    except Exception as e:
        logger.warning("Could not mount legacy routes: %s", e)

    # Serve the React dashboard from cvc/web_dist/
    if CVC_WEB_DIST.exists():
        # v3.3.7 — SPA fallback. StaticFiles with html=True only
        # auto-serves index.html for paths that look like file paths
        # (have an extension, etc.). For client-side routes like
        # ``/chat``, ``/agents``, ``/swarm`` (anything React Router
        # owns), the request 404s and the browser shows a blank
        # page. We add a 404 → index.html middleware for non-API
        # GET requests with ``Accept: text/html`` so the React
        # shell loads and the router takes over from there.
        # Mirrors the legacy's _spa_fallback_middleware (cvc/
        # gateway_legacy.py:11014). Must be registered AFTER all
        # routers so the API routes shadow the catch-all.
        _DASHBOARD_DIR = CVC_WEB_DIST
        _INDEX_HTML = _DASHBOARD_DIR / "index.html"
        _SPA_RESERVED = (
            "/api", "/gateway", "/ws", "/static", "/assets",
            "/ds-assets", "/fonts", "/favicon", "/health",
            "/docs", "/openapi", "/redoc",
        )

        @app.middleware("http")
        async def _spa_fallback_middleware(request, call_next):
            response = await call_next(request)
            try:
                if (
                    response.status_code == 404
                    and request.method == "GET"
                    and not any(
                        request.url.path.startswith(p)
                        for p in _SPA_RESERVED
                    )
                    and "text/html" in request.headers.get("accept", "")
                    and _INDEX_HTML.exists()
                ):
                    # v3.3.12 — Pull the version from the package metadata
                    # instead of hardcoding it (which had drifted to 3.3.7).
                    try:
                        from importlib.metadata import version as _pkg_version
                        _version_str = _pkg_version("tm-ai")
                    except Exception:
                        _version_str = "dev"
                    html = _INDEX_HTML.read_text(
                        encoding="utf-8"
                    ).replace("{{CVC_VERSION}}", _version_str)
                    from fastapi.responses import HTMLResponse
                    return HTMLResponse(
                        content=html,
                        headers={
                            "Cache-Control": "no-cache, no-store, must-revalidate",
                            "Pragma": "no-cache",
                        },
                    )
            except Exception:
                # Never let the SPA fallback break a real 404.
                pass
            return response

        app.mount(
            "/",
            StaticFiles(directory=str(CVC_WEB_DIST), html=True),
            name="dashboard",
        )
    else:
        logger.warning(
            "cvc/web_dist/ not found at %s — dashboard will not be served",
            CVC_WEB_DIST,
        )

    return app


# Module-level app for `uvicorn cvc.gateway:app`
app = create_app()
