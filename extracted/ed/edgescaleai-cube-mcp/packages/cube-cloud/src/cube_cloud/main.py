"""FastAPI application with MCP server (Streamable HTTP transport)."""

from __future__ import annotations

import asyncio
import logging
import logging.config
import time
from contextlib import asynccontextmanager

# Configure root logger so all cube_cloud.* loggers emit to stderr
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")

import uvicorn
from fastapi import FastAPI
from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import Tool, TextContent
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.routing import Mount
from starlette.websockets import WebSocket, WebSocketDisconnect

from cube_common.apollo_client import ApolloClient, ApolloError
from cube_cloud.auth.middleware import APIKeyMiddleware
from cube_cloud.browser_proxy.http_proxy import handle_app_proxy_request
from cube_cloud.browser_proxy.rate_limit import SlidingWindowRateLimiter
from cube_cloud.config import settings
from cube_cloud.tools import (
    environments, entities, acr, clusters, kubectl_exec, apps,
    products, modules, secrets, expose as expose_tool, groundcover, build_image,
    feedback,
)
from cube_cloud._request_context import current_request
from cube_cloud import telemetry

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MCP Server definition
# ---------------------------------------------------------------------------

mcp_server = Server("cube-cloud")


@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    # Import tool schemas from the shared proxy_tools definitions.
    # proxy_tools.py is the single source of truth for tool schemas;
    # cube-cloud just needs to accept and dispatch them.
    from cube_agent.remote.proxy_tools import REMOTE_TOOLS
    return list(REMOTE_TOOLS)


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Route tool calls to the appropriate handler.

    Credentials come from request.state (set by APIKeyMiddleware).
    Threaded via contextvars since MCP handlers don't receive the request.

    Every call is recorded for analytics (see telemetry/). Recording is
    non-blocking and never raises, so it can't break or alter a tool call.
    """
    req = current_request.get()
    client_id = req.state.apollo_client_id
    client_secret = req.state.apollo_client_secret

    start = time.monotonic()
    result = ""
    exc: BaseException | None = None
    record = True
    try:
        async with ApolloClient(client_id, client_secret) as client:
            result = await _dispatch(client, name, arguments)
    except ApolloError as e:
        # Preserve the user-facing string result, but also hand the exception to
        # telemetry so it classifies as apollo_error rather than message text.
        result = f"Error: {e}"
        exc = e
    except asyncio.CancelledError:
        # Client disconnect / shutdown — not a tool outcome; don't record noise.
        record = False
        raise
    except BaseException as e:  # preserve behavior (re-raise) but record it
        exc = e
        raise
    finally:
        if record:
            latency_ms = (time.monotonic() - start) * 1000.0
            telemetry.record_tool_call(req, name, arguments, result, latency_ms, exc)

    return [TextContent(type="text", text=result)]


def _force(args: dict) -> bool:
    """The entity tools' break-glass ``force`` flag. Only a JSON ``true`` sets it.

    An agent released before the flag existed never sends it and so gets the
    module-managed refusal, not an error; a string such as "false" must not read
    as truthy, so anything but the boolean is treated as absent.
    """
    return args.get("force") is True


async def _dispatch(client: ApolloClient, name: str, args: dict) -> str:
    match name:
        # --- Environment management ---
        case "list_environments":
            return await environments.list_environments(client, args.get("search"))

        # --- Entity management ---
        case "install_entity":
            return await environments.install_entity(
                client,
                args["environment"],
                args["entity_name"],
                args["product_id"],
                args.get("k8s_namespace", "default"),
                args.get("config_overrides"),
                args.get("version"),
                force=_force(args),
            )
        case "uninstall_entity":
            return await environments.uninstall_entity(
                client, args["environment"], args["entity_name"]
            )
        case "update_entity_config":
            return await environments.update_entity_config(
                client, args["environment"], args["entity_name"], args["config_overrides"],
                args.get("version"), force=_force(args),
                protected=expose_tool.protected_module_bases(current_request.get().state.profile),
            )
        case "enforce_entity_config":
            return await environments.enforce_entity_config(
                client, args["environment"], args["entity_name"]
            )
        case "entity_health":
            # A scoped caller does not read a Teleport app service's config: its `apps`
            # key is every company's app list on the cube (the list_modules rule below).
            return await entities.entity_health(
                client, args["environment"], args.get("entity_id"),
                protected=expose_tool.protected_module_bases(current_request.get().state.profile),
            )
        case "plan_details":
            return await entities.plan_details(
                client, args["environment"], args["entity_name"], args.get("plan_index", 0)
            )
        case "cancel_active_plan":
            return await entities.cancel_active_plan(
                client, args["environment"], args["entity_name"]
            )

        # --- Module management ---
        # The module tools carry the caller's protected set: a scoped profile may not
        # touch the Teleport multi-app module through the three WRITES, nor read its
        # `apps` list through list_modules (it holds every company's apps on the cube;
        # `expose`/`unexpose`/`list_exposed` are its only door). Unscoped: None.
        case "list_modules":
            return await modules.list_modules(
                client, args["environment"], args.get("search"),
                protected=expose_tool.protected_module_bases(current_request.get().state.profile),
            )
        case "install_module":
            return await modules.install_module(
                client,
                args["environment"],
                args["maven_coordinate"],
                args.get("variables"),
                args.get("display_name"),
                args.get("ignore_secret_requirements", False),
                protected=expose_tool.protected_module_bases(current_request.get().state.profile),
            )
        case "uninstall_module":
            return await modules.uninstall_module(
                client, args["environment"], args["module_name"],
                protected=expose_tool.protected_module_bases(current_request.get().state.profile),
            )
        case "update_module_variables":
            return await modules.update_module_variables(
                client, args["environment"], args["module_name"], args["variables"],
                protected=expose_tool.protected_module_bases(current_request.get().state.profile),
            )

        # --- Teleport app exposure (needs both Apollo client and profile) ---
        case "expose":
            req = current_request.get()
            return await expose_tool.expose(
                client,
                args["environment"],
                args["app_name"],
                args["app_uri"],
                args.get("public_addr"),
                args.get("company"),
                profile=req.state.profile,
                # `.get` with no default, deliberately: None means "leave any
                # existing value alone" and an empty list/dict means "clear",
                # so a default of [] here would silently wipe every rewrite.
                rewrite_headers=args.get("rewrite_headers"),
                labels=args.get("labels"),
            )
        case "unexpose":
            req = current_request.get()
            return await expose_tool.unexpose(
                client,
                args["environment"],
                args.get("app_name"),
                args.get("public_addr"),
                args.get("all", False),
                profile=req.state.profile,
                # Absent from agents installed before multi-company apps: they
                # never send it, and the default (the home company) is what an
                # unexpose meant for them.
                company=args.get("company"),
            )
        case "list_exposed":
            req = current_request.get()
            return await expose_tool.list_exposed(
                client, args["environment"], profile=req.state.profile,
            )
        case "list_services":
            req = current_request.get()
            return await clusters.list_services(
                client, args["environment"], args.get("namespace"), profile=req.state.profile,
            )

        # --- Secret management ---
        case "create_secret":
            return await secrets.create_secret(
                client,
                args["environment"],
                args["entity_name"],
                args["secret_name"],
                args.get("secret_value"),
                args.get("secret_keys"),
                args.get("description"),
            )
        case "update_secret":
            return await secrets.update_secret(
                client,
                args["environment"],
                args["entity_name"],
                args["secret_name"],
                args.get("secret_value"),
                args.get("secret_key"),
                args.get("secret_key_value"),
                args.get("description"),
            )

        # --- Product management ---
        case "list_products":
            return await products.list_products(
                client, args.get("search"), args.get("page_size", 50)
            )
        case "compare_product_versions":
            return await products.compare_product_versions(
                client, args["product_id"], args["environments"]
            )
        case "get_product_releases":
            return await products.get_product_releases(
                client, args["product_id"], args.get("page_size", 10)
            )

        # --- Release channel management ---
        case "list_release_channels":
            return await products.list_release_channels(
                client, args.get("search"), args.get("include_env_specific", False)
            )

        # --- ACR / publish ---
        case "acr_get_token":
            return await acr.acr_get_token(client)
        case "apollo_publish_manifest":
            return await acr.apollo_publish_manifest(client, args["manifest_yaml"])

        # --- Remote image builds (kaniko RunTask); start mints the ACR token ---
        case "build_image_prepare":
            return await build_image.build_image_prepare(args["image_name"], args["tag"])
        case "build_image_start":
            return await build_image.build_image_start(
                client,
                args["job_id"],
                args.get("dockerfile", "Dockerfile"),
                args.get("target"),
                args.get("build_args"),
                args.get("platform", "linux/amd64"),
            )
        case "build_image_status":
            return await build_image.build_image_status(args["job_id"])

        # --- Teleport / kubectl (no Apollo client needed) ---
        case "cube_status" | "cube_list" | "kubectl_exec" | "app_list":
            req = current_request.get()
            profile = req.state.profile
            return await _dispatch_teleport(profile, name, args)

        # --- Groundcover (authz via Apollo `client`, data via Groundcover API) ---
        case "groundcover_list_clusters" | "groundcover_list_workloads" | "groundcover_query_metrics" | "groundcover_list_metrics" | "groundcover_search_logs" | "groundcover_search_traces" | "groundcover_k8s_events":
            return await _dispatch_groundcover(client, name, args)

        # --- Feedback -> Freshservice (support) or the Jira CF board (feature).
        # One tool, two destinations; `feedback.send_feedback` holds the routing and
        # explains why they are different systems. Neither takes an Apollo client —
        # both carry their own credential.
        #
        # BOTH names are matched. `submit_feedback` is what agents installed before
        # the rename still advertise and forward, and they upgrade on their own
        # schedule while this side redeploys on every merge — so dropping it would
        # answer them `"Unknown tool"`, a 200 string the model relays as prose. See
        # `feedback.LEGACY_TOOL_NAME` for when it can go. `normalize_feedback_type`
        # maps that build's retired `bug` value onto `support`. ---
        case "send_feedback" | "submit_feedback":
            return await feedback.send_feedback(
                feedback.normalize_feedback_type(args["feedback_type"]),
                args["summary"],
                args["details"],
                args.get("business_impact"),
                args.get("cube"),
                args.get("submitter_name"),
                args.get("submitter_role"),
                args.get("contact_email"),
            )

        case _:
            return f"Unknown tool: {name}"


async def _dispatch_groundcover(apollo: ApolloClient, name: str, args: dict) -> str:
    """Dispatch Groundcover tools. `apollo` provides the authz (allowed_cubes);
    the Groundcover registry provides the (read-only) data, routed to whichever
    backend the cube actually reports to (tools/groundcover.py, "Multi-backend
    routing"). The registry is a process-lifetime singleton — unlike the old
    single client, it is NOT entered/exited per call; closing it here would tear
    down the cube->backend cache and its httpx connections for every other call."""
    try:
        registry = groundcover.groundcover_registry()
    except groundcover.GroundcoverError as e:
        return f"Error: {e}"

    match name:
        case "groundcover_list_clusters":
            return await groundcover.list_clusters(apollo, registry)
        case "groundcover_list_workloads":
            return await groundcover.list_workloads(
                apollo, registry, args["cube"], args.get("namespace"), args.get("limit", 100)
            )
        case "groundcover_query_metrics":
            return await groundcover.query_metrics(
                apollo, registry, args["cube"], args["metric"],
                args.get("match"), args.get("aggregation"), args.get("window"),
                args.get("start"), args.get("end"), args.get("step"),
            )
        case "groundcover_list_metrics":
            return await groundcover.list_metrics(
                apollo, registry, args["cube"], args.get("start"), args.get("end"),
                args.get("limit", 1000), args.get("filter")
            )
        case "groundcover_search_logs":
            return await groundcover.search_logs(
                apollo, registry, args["cube"], args.get("start"), args.get("end"),
                args.get("query"), args.get("limit", 100)
            )
        case "groundcover_search_traces":
            return await groundcover.search_traces(
                apollo, registry, args["cube"], args.get("start"), args.get("end"),
                args.get("query"), args.get("limit", 100)
            )
        case "groundcover_k8s_events":
            return await groundcover.k8s_events(
                apollo, registry, args["cube"], args.get("start"), args.get("end")
            )
        case _:
            return f"Unknown groundcover tool: {name}"


async def _dispatch_teleport(profile: str, name: str, args: dict) -> str:
    """Dispatch tools that use server-side tbot/kubectl (no Apollo client needed)."""
    match name:
        case "cube_status":
            return await clusters.cube_status(args.get("cluster"), profile=profile)
        case "cube_list":
            return await clusters.cube_list(profile=profile)
        case "kubectl_exec":
            return await kubectl_exec.kubectl_exec(
                args["command"], cluster=args.get("cluster"), profile=profile
            )
        case "app_list":
            return await apps.app_list(args.get("company"), profile=profile)
        case _:
            return f"Unknown teleport tool: {name}"


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

# docs_url/redoc_url/openapi_url are OFF deliberately (docs/console-spec.md §4.8).
# FastAPI's defaults put Swagger UI at /docs, which (a) collides head-on with the
# planned user-facing docs endpoint, and (b) would publish the full internal API
# schema the moment someone added "/docs" to APIKeyMiddleware.EXEMPT_PATHS. They
# are 401'd today, so nothing leaks — this reserves the path before we build on it.
app = FastAPI(
    title="cube-cloud",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.add_middleware(APIKeyMiddleware)


@app.get("/health")
async def health(request: Request):
    # Host-gated like every other literal path registered before the app-proxy
    # catch-all: an exposed app's own /health belongs to the app, not to us.
    # Load balancer probes dial by IP or the ALB hostname, neither of which is an
    # app subdomain, so they still get this handler.
    if console_routes.is_proxy_host(request):
        return await handle_app_proxy_request(request, _app_proxy_rate_limiter)
    from cube_cloud.teleport.tbot_manager import tbot
    return {"status": "ok", "tbot": tbot.status(), "tunnel": _tunnel_conn_mgr.status()}



# ---------------------------------------------------------------------------
# Browser login flow (Cognito)
# ---------------------------------------------------------------------------

from pathlib import Path
from starlette.staticfiles import StaticFiles
from cube_cloud.auth.login_flow import (
    auth_login, auth_authenticate, auth_session, auth_logout,
    auth_forgot, auth_forgot_submit, auth_reset, auth_reset_submit,
)

# Every one of these is registered BEFORE the app-proxy catch-all, so without a
# host gate it reserves its path inside EVERY proxied in-cube app. That is the
# trap `_console_or_proxy` exists for, and these were missed:
#
#   * `/static/*` — a raw `StaticFiles` mount. `docs/console-spec.md` §4.1 already
#     says console assets are served by a route handler "because a mount would
#     bypass the gate"; this mount is exactly that. MinIO's console serves its
#     2.4 MB JS bundle from `/static/js/...`, so the SPA got our JSON 404, never
#     booted, and rendered a permanent spinner. Django, Flask and most SPAs use
#     `/static/` too.
#   * `/auth/login` and friends — the worst of the three: an exposed app with its
#     own login route had it silently replaced by OUR Cognito page, served on the
#     app's own hostname.
#   * `/health` — an app's own health endpoint was shadowed by ours, so anything
#     probing the public URL got a misleading 200.
#
# The gate only ever *adds* delegation on app-subdomain hosts; on the apex every
# one of these behaves exactly as before.
_static_files = StaticFiles(directory=Path(__file__).parent / "static")


def _gated(handler):
    """Wrap a handler so an app-subdomain host gets the proxy instead."""
    async def route(request: Request):
        if console_routes.is_proxy_host(request):
            return await handle_app_proxy_request(request, _app_proxy_rate_limiter)
        return await handler(request)
    return route


app.add_api_route("/auth/login", _gated(auth_login), methods=["GET"])
app.add_api_route("/auth/authenticate", _gated(auth_authenticate), methods=["POST"])
app.add_api_route("/auth/session/{session_id}", _gated(auth_session), methods=["GET"])
app.add_api_route("/auth/logout", _gated(auth_logout), methods=["GET"])
app.add_api_route("/auth/forgot", _gated(auth_forgot), methods=["GET"])
app.add_api_route("/auth/forgot", _gated(auth_forgot_submit), methods=["POST"])
app.add_api_route("/auth/reset", _gated(auth_reset), methods=["GET"])
app.add_api_route("/auth/reset", _gated(auth_reset_submit), methods=["POST"])


# GET **and HEAD**. `StaticFiles` served both; a FastAPI `@app.get` serves only
# GET, and this file already records the consequence one screen down
# (`_CONSOLE_REJECTED_METHODS`): an unmatched method does not 405, it falls
# through to the app-proxy catch-all, which DOES declare HEAD. So `HEAD
# /static/favicon.svg` on the apex 404'd from `resolve_app_name` instead of
# returning the asset's headers. Verified live on dev before the fix.
@app.api_route("/static/{path:path}", methods=["GET", "HEAD"], include_in_schema=False)
async def static_or_proxy(request: Request, path: str):
    """Serve a bundled asset, or hand the path back to the proxied app.

    Delegates to the real `StaticFiles` app rather than re-implementing file
    serving, so path-traversal rejection, media types, ETags and range requests
    keep coming from Starlette instead of from hand-rolled code here.
    """
    if console_routes.is_proxy_host(request):
        return await handle_app_proxy_request(request, _app_proxy_rate_limiter)
    return await _static_files.get_response(path, request.scope)


# ---------------------------------------------------------------------------
# Console (browser UI) — docs/console-spec.md
#
# Registered BEFORE the app-proxy catch-all below, so these literal paths win on
# any host. That is also why every console route is host-gated through
# `_console_or_proxy`: without the gate, registering `/console` here would
# permanently reserve that path inside every proxied in-cube app (the same trap
# `/mcp` documents further down, but far likelier to collide). On an
# app-subdomain host the console hands the request straight to the proxy.
#
# Auth is already done by APIKeyMiddleware: `/console` is the one entry in
# COOKIE_ALLOWED_APEX_PREFIXES, so an unauthenticated browser navigation was
# 302'd to /auth/login?next=/console... and never arrives here.
# ---------------------------------------------------------------------------

from cube_cloud.console import routes as console_routes
# Console usage events. Imported as a module (not `from ... import telemetry`)
# for the reason recorded at `console_cube_utilization` below: `telemetry` is
# already bound at module scope and rebinding it breaks every MCP tool call.
from cube_cloud.telemetry import console_events


async def _console_or_proxy(request: Request, handler):
    """Run a console handler, or hand the request to the app proxy by host.

    The apex branch is the console's single seam — every `/console*` route
    passes through it — so it is also where a console request is recorded as a
    usage event (`telemetry/console_events.py`), the way `call_tool` records a
    tool call. The proxy branch is NOT observed: a proxied in-cube app's asset
    requests are not console usage, and the app proxy keeps its own audit line.
    """
    if console_routes.is_proxy_host(request):
        return await handle_app_proxy_request(request, _app_proxy_rate_limiter)
    return await console_events.observe(request, handler)


@app.get("/console/api/session")
async def console_session(request: Request):
    return await _console_or_proxy(request, console_routes.session)


@app.get("/console/api/cubes")
async def console_cubes(request: Request):
    return await _console_or_proxy(request, console_routes.cubes)


# Every app the caller can open, fleet-wide (docs/console-spec.md §4.22). A GET above
# the deep-link catch-all (AGENTS.md console rule 4), read-only, no arguments.
@app.get("/console/api/apps")
async def console_fleet_apps(request: Request):
    return await _console_or_proxy(request, console_routes.fleet_apps)


# GPS positions for every cube the caller can see, for the landing page's map. A
# fleet read beside /apps, above the deep-link catch-all (AGENTS.md console rule 4).
# Not /console/api/cubes/gps, which /console/api/cubes/{cube} would claim as a cube.
@app.get("/console/api/gps")
async def console_fleet_gps(request: Request):
    return await _console_or_proxy(request, console_routes.fleet_gps)


# MUST stay above /console/{sub_path:path} — Starlette matches in registration
# order, so registering it after the deep-link route would serve the SPA shell to a
# fetch expecting JSON. Guarded by test_specific_console_api_routes_precede_the_deep_link_catch_all.
@app.get("/console/api/cubes/{cube}")
async def console_cube_detail(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_detail(r, cube)
    )


# A GET above the deep-link catch-all (AGENTS.md rule 4). kubectl-backed, so the UI
# fetches it lazily when the expose flow opens — never on cube-page render.
@app.get("/console/api/cubes/{cube}/services")
async def console_cube_services(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_services(r, cube)
    )


# Also a GET above the deep-link catch-all (AGENTS.md rule 4). Polled by the UI to
# resolve a pending unexpose, so it is deliberately the cheap read.
@app.get("/console/api/cubes/{cube}/exposed")
async def console_cube_exposed(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_exposed(r, cube)
    )


# Also a GET above the deep-link catch-all (AGENTS.md rule 4). "Last changed" per
# app, from Apollo plan history (docs/console-spec.md §4.15). Its own endpoint so the
# plan query — which CONSOLE_ENVIRONMENT_ENTITIES omits on purpose as the largest part
# of the entity payload — never delays the apps list it decorates.
@app.get("/console/api/cubes/{cube}/changes")
async def console_cube_changes(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_changes(r, cube)
    )


# Also a GET above the deep-link catch-all (AGENTS.md rule 4). Online/offline for
# ONE cube, from Groundcover log freshness (docs/console-spec.md §4.14). Its own
# endpoint for the same reason as /inventory: a different upstream with its own
# latency, which the apps list must not wait on.
@app.get("/console/api/cubes/{cube}/status")
async def console_cube_status(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_status(r, cube)
    )


# Also a GET above the deep-link catch-all (AGENTS.md rule 4). Where ONE cube's router
# last reported its GPS position, from InControl2. Its own endpoint for the same reason
# as /inventory: a different upstream with its own latency and outages.
@app.get("/console/api/cubes/{cube}/gps")
async def console_cube_gps(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_gps(r, cube)
    )


# Also a GET above the deep-link catch-all (AGENTS.md rule 4). Teleport connectivity
# for ONE cube (docs/console-spec.md §4.17). Its own endpoint because it shells out to
# `tsh`, an upstream neither Apollo nor Groundcover shares.
@app.get("/console/api/cubes/{cube}/teleport")
async def console_cube_teleport(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_teleport(r, cube)
    )


# Also a GET above the deep-link catch-all (AGENTS.md rule 4). The health checks
# behind ONE app's status (docs/console-spec.md §4.21), fetched when the user opens
# it rather than with the page — one Apollo read per app, for the app asked about.
@app.get("/console/api/cubes/{cube}/health")
async def console_app_health(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.app_health(r, cube)
    )


# Also a GET above the deep-link catch-all (AGENTS.md rule 4). Inventory facts for
# ONE cube — its own endpoint rather than a field on `cube_detail`, because
# `/inventory/lookup` is a partition scan (~3.3s cold, measured) and folding it into
# the detail payload would delay the apps list behind a secondary panel. Same shape
# and same reasoning as `/services`: a slow read the page fetches alongside.
@app.get("/console/api/cubes/{cube}/inventory")
async def console_cube_inventory(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_inventory(r, cube)
    )


# Also a GET above the deep-link catch-all (AGENTS.md rule 4). The AI tab: the AI
# Reactor catalog and this cube's gateway and models (docs/ai-reactor-deploy-spec.md),
# fetched only when that tab is open.
@app.get("/console/api/cubes/{cube}/ai")
async def console_cube_ai(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_ai(r, cube)
    )


# A GET, so the binding constraint is the DEEP-LINK catch-all below, not the method
# guard — registered after it, `/console/{sub_path:path}` would swallow this and
# `shell()` would answer a JSON 404 to a fetch expecting log rows (AGENTS.md rule 4).
@app.get("/console/api/cubes/{cube}/logs")
async def console_cube_logs(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_logs(r, cube)
    )


# Cube-wide resource utilization for the Resources tab (docs/console-spec.md §4.18).
# Also a GET above the deep-link catch-all (AGENTS.md rule 4). Its own endpoint, fetched
# only when that tab is open: 12 Groundcover range queries is the wrong tax to put on
# every cube-page load for a tab most visitors never open.
#
# NOTE the module is `console.utilization`, never `console.telemetry` — `telemetry` is
# already bound at module scope above (`from cube_cloud import telemetry`) and is called
# inside `call_tool`'s `finally`, so shadowing it here would replace the result of every
# MCP tool call with an AttributeError.
@app.get("/console/api/cubes/{cube}/utilization")
async def console_cube_utilization(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.cube_utilization(r, cube)
    )


# The Cube Field Guide (docs/console-spec.md §4.11). GETs, so — like the API reads
# above — the binding constraint is the deep-link catch-all: registered after it,
# `/console/{sub_path:path}` swallows both and serves the SPA shell instead of the
# guide, which looks like a routing bug rather than a missing route. Pinned by
# test_specific_console_api_routes_precede_the_deep_link_catch_all.
#
# Under /console on purpose, not at a top-level /guide or /docs: that inherits the
# cookie-auth allowlist, the host gate, and `console_enabled` without widening any
# of them (spec §4.11, AGENTS.md console rule 1).
# The fleet map's outline asset. Above the deep-link catch-all for the same reason as
# the guide: below it, `/console/{sub_path:path}` would answer with the SPA shell (HTML)
# and the map would silently draw no borders.
@app.get("/console/map/outline.json")
async def console_map_outline(request: Request):
    return await _console_or_proxy(request, console_routes.map_outline)


@app.get("/console/guide")
async def console_guide(request: Request):
    return await _console_or_proxy(request, console_routes.guide_shell)


@app.get("/console/guide/{name}")
async def console_guide_asset(request: Request, name: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.guide_asset(r, name)
    )


@app.get("/console")
async def console_root(request: Request):
    return await _console_or_proxy(request, console_routes.shell)


@app.get("/console/{sub_path:path}")
async def console_deep_link(request: Request, sub_path: str):
    return await _console_or_proxy(request, console_routes.shell)


# Mutations. MUST stay above the non-GET method guard below, which would otherwise
# 405 them (AGENTS.md console rule 4). Every capability is its own route with
# enumerated args — never a generic tool proxy (console rule 2).
@app.post("/console/api/cubes/{cube}/expose")
async def console_expose(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.expose_app(r, cube)
    )


@app.post("/console/api/cubes/{cube}/unexpose")
async def console_unexpose(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.unexpose_app(r, cube)
    )


# Deploy or remove an AI Reactor model (docs/ai-reactor-deploy-spec.md §5). Enumerated
# args: the body names a catalog model id, never a product or a chart.
@app.post("/console/api/cubes/{cube}/ai/deploy")
async def console_ai_deploy(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.ai_deploy(r, cube)
    )


@app.post("/console/api/cubes/{cube}/ai/remove")
async def console_ai_remove(request: Request, cube: str):
    return await _console_or_proxy(
        request, lambda r: console_routes.ai_remove(r, cube)
    )


# Also a mutation (files a Jira ticket, not a cube change), so it needs the same
# "above the method guard" placement — but no {cube} path param, since `cube` is
# optional free-text context in the body rather than something this route resolves.
@app.post("/console/api/feedback")
async def console_feedback(request: Request):
    return await _console_or_proxy(request, console_routes.submit_feedback)


# Non-GET under the console prefix. Registered after the GET routes (so it never
# shadows them) but BEFORE the app-proxy catch-all, which would otherwise swallow
# these and 404 from proxy code — see console_routes.method_not_allowed.
#
# HEAD is included. An earlier comment here claimed Starlette already serves HEAD
# from the GET routes above — true of Starlette's `Route`, but FastAPI's `APIRoute`
# does NOT add it, so `HEAD /console/...` fell through to the app-proxy catch-all
# (which does declare HEAD, and a full match beats a partial one), skipping
# is_enabled(), the origin check, and the JSON hardening. Harmless in itself — HEAD
# is safe and the outcome was a 404 either way — but it was a live counterexample
# to the console rule in AGENTS.md, so it is closed rather than documented.
_CONSOLE_REJECTED_METHODS = ["POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]


@app.api_route("/console", methods=_CONSOLE_REJECTED_METHODS, include_in_schema=False)
async def console_root_method_guard(request: Request):
    return await _console_or_proxy(request, console_routes.method_not_allowed)


@app.api_route(
    "/console/{sub_path:path}", methods=_CONSOLE_REJECTED_METHODS, include_in_schema=False
)
async def console_method_guard(request: Request, sub_path: str):
    return await _console_or_proxy(request, console_routes.method_not_allowed)


# ---------------------------------------------------------------------------
# Tunnel relay (Phase 4) — WebSocket endpoint for app proxy
# ---------------------------------------------------------------------------

from cube_cloud.tunnel.connection_manager import ConnectionManager
from cube_cloud.tunnel.relay import TunnelRelay

_tunnel_conn_mgr = ConnectionManager()


@app.websocket("/tunnel")
async def tunnel_endpoint(ws: WebSocket):
    """WebSocket tunnel endpoint for cube-agent app proxy.

    The agent opens a WebSocket here, then sends CONNECT frames to
    request TCP connections to Teleport apps. Data is relayed
    bidirectionally via binary frames.
    """
    # Validate API key from query param or header
    api_key = ws.query_params.get("token") or ws.headers.get("authorization", "").removeprefix("Bearer ").strip()
    if not api_key:
        await ws.close(code=4001, reason="Missing authentication")
        return

    from cube_cloud.auth.api_keys import validate_key
    try:
        profile = await validate_key(api_key)
    except Exception as e:
        logger.error("Tunnel auth error: %s", e)
        await ws.close(code=4001, reason="Auth error")
        return
    if not profile:
        logger.warning("Tunnel auth failed: invalid API key")
        await ws.close(code=4001, reason="Invalid API key")
        return

    logger.info("Tunnel WebSocket authenticated, profile=%s", profile.get("profile"))
    await ws.accept()

    try:
        relay = TunnelRelay(ws, _tunnel_conn_mgr, profile=profile.get("profile", "admin"))
        await relay.run()
    except Exception as e:
        logger.error("Tunnel endpoint error: %s", e)


# ---------------------------------------------------------------------------
# Mount MCP at /mcp using StreamableHTTPSessionManager
# ---------------------------------------------------------------------------
# The session manager is an ASGI app that handles session lifecycle.
# We wrap it to inject the Starlette Request into a contextvar so MCP
# tool handlers can access auth state.

session_manager = StreamableHTTPSessionManager(
    app=mcp_server,
    json_response=True,
    stateless=True,
)


async def mcp_asgi_with_context(scope, receive, send):
    """ASGI wrapper that sets the current_request contextvar."""
    if scope["type"] == "http":
        request = Request(scope, receive, send)
        token = current_request.set(request)
        try:
            await session_manager.handle_request(scope, receive, send)
        finally:
            current_request.reset(token)
    else:
        await session_manager.handle_request(scope, receive, send)


app.mount("/mcp", mcp_asgi_with_context)


# ---------------------------------------------------------------------------
# Browser app proxy (Phase 2a) — real HTTP reverse proxy from an app-subdomain
# host to the matching Teleport app. Supersedes the Phase 1 `/proxy-test`
# scaffold (removed). Not exempt from APIKeyMiddleware: on an app-subdomain
# host, the cookie authenticates the request before this route ever runs;
# unauthenticated requests are 302/401'd by the middleware and never reach
# here, so no dial is ever attempted for them (spec §4.4 fail-closed).
#
# Registered LAST (after /health, /auth/*, /static, /console, /mcp, /tunnel):
# Starlette matches routes in registration order, so those exact paths take
# precedence over this catch-all **on every host**.
#
# Precedence is NOT the same as being served by them. `/mcp` and `/tunnel` are
# genuinely reserved: an app cannot expose content there, an acceptable POC
# limitation. But `/health`, `/auth/*`, `/static` and `/console` all match first
# and then **delegate straight back here** when the host is an app subdomain
# (`_gated` / `static_or_proxy` / `_console_or_proxy`). They have to: a literal
# path registered here reserves that path inside EVERY proxied in-cube app, and
# leaving it reserved is what made MinIO's console hang on a permanent spinner
# (its 2.4 MB bundle lives under `/static/js/`, and cube-cloud was answering it
# with a JSON 404).
#
# ==> ADDING A LITERAL PATH HERE? Host-gate it, or you silently take that path
# away from every customer's app. `console_routes.is_proxy_host(request)` ->
# `handle_app_proxy_request(...)`. If the path is also in
# `APIKeyMiddleware.EXEMPT_PATHS`/`EXEMPT_PREFIXES`, the exemption must stay
# host-aware too, or the proxy receives an unauthenticated request with an empty
# `request.state` and 500s on a public path. `test_proxy_host_gate.py` sweeps the
# registered routes and fails on an ungated one.
# ---------------------------------------------------------------------------

_app_proxy_rate_limiter = SlidingWindowRateLimiter(
    max_requests=settings.app_proxy_rate_limit_max,
    window_seconds=settings.app_proxy_rate_limit_window_seconds,
)


@app.api_route(
    "/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
)
async def app_proxy_catch_all(request: Request, full_path: str):
    return await handle_app_proxy_request(request, _app_proxy_rate_limiter)


# ---------------------------------------------------------------------------
# Browser app proxy — WebSocket (Phase 3). A browser WebSocket arrives as an
# ASGI `websocket` scope, NOT through the HTTP catch-all above, so it needs its
# own catch-all WS route. Registered LAST (after the apex `/tunnel` WS route and
# the `/mcp` mount): Starlette matches in registration order, so `/tunnel` and
# `/mcp` keep precedence for their exact paths, and a WebSocketRoute only ever
# matches `websocket` scopes so it never shadows the HTTP proxy either. The
# handler host-gates to app subdomains and authenticates/authorizes explicitly
# before dialing (APIKeyMiddleware, a BaseHTTPMiddleware, does not run on
# websocket scopes). An app cannot itself serve a WS at `/tunnel` or under
# `/mcp` through the proxy — the same acceptable POC limitation as the HTTP
# catch-all's `/mcp` note above.
# ---------------------------------------------------------------------------

from cube_cloud.browser_proxy.ws_proxy import handle_app_proxy_websocket


@app.websocket("/{full_path:path}")
async def app_proxy_ws_catch_all(ws: WebSocket):
    await handle_app_proxy_websocket(ws)


# ---------------------------------------------------------------------------
# Lifespan — start the MCP session manager's internal task group
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with session_manager.run():
        logger.info("MCP session manager started")
        yield
    logger.info("MCP session manager stopped")


app.router.lifespan_context = lifespan


def cli():
    """Entry point for the cube-cloud CLI."""
    uvicorn.run(
        "cube_cloud.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
    )


if __name__ == "__main__":
    cli()
