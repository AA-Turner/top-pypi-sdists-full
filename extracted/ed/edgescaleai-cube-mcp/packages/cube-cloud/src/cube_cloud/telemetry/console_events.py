"""Console usage events — the console's analog of `record_tool_call`.

The MCP surface records every tool call at ONE seam (`main.py::call_tool`). The
console has the same shape: every `/console*` route in `main.py` is a thin
wrapper that passes through `_console_or_proxy`, and that function hands the
apex branch to `observe` here. So a console request is recorded the way a tool
call is — one `ToolCallEvent`, the same identity fields off `request.state`, the
same two sinks (S3 archive + Groundcover span) — and lands in the same Parquet
store under `source="console"`, where the adoption dashboard already counts
every row as an operation.

Three decisions make this usage tracking rather than request logging:

1. **A REGISTRY decides what counts, keyed on the route's PATH TEMPLATE.** The
   matched `APIRoute` is on `request.scope["route"]` (FastAPI stamps it in
   `APIRoute.matches`), so nothing about the route registrations in `main.py`
   changes and a test can walk `app.routes` and demand every console path is
   declared. A cube page fans out to ~7 parallel GETs; recording all of them
   makes one page view look like seven operations. Only the request that
   expresses the INTENT is counted (`view_cube`), and the satellites that ride
   along with it (services, exposed, changes, status, teleport, inventory, gps) are
   declared `None`. `/console/{sub_path:path}` also serves the SPA's ASSETS, so
   the shell is `None` too; "console opened" is the session fetch instead.
2. **Repeated successful READS are suppressed, and emission is capped per
   session.** The logs page polls every 10s and the SPA re-fetches on focus. The
   same (session, event, cube, app) is recorded once per
   `telemetry_console_suppress_seconds`, server-side so the browser cannot opt
   out and no SPA change is needed. Mutations and ERRORS are never suppressed —
   a read that fails after a success in the same window must still land, or an
   outage hides behind the one `ok` row. The caller-supplied parts of the key
   are HASHED, because the same repo has already written down what happens when
   a limiter keys on a raw submitted string (`auth/login_flow.py::_reset_email_allowed`).
   And because suppression is content-keyed it bounds nothing for a caller who
   varies the content, so a second limiter caps how many rows one session can
   emit per minute, whatever it asks for.
3. **No body is ever stored.** Status comes from the HTTP code, args are the
   path + query params through the tool-call redaction, and the response is
   dropped (size kept). See `events.build_console_event`.

Everything is best-effort and never raises: `observe` runs the handler exactly as
before and records in a `finally`, so a telemetry fault cannot alter a console
response. Gated by `telemetry_enabled` AND `telemetry_console_enabled`.

This module lives under `telemetry/`, never under `console/` — `main.py` binds
`from cube_cloud import telemetry` at module scope and calls it inside
`call_tool`'s `finally`; a `console.telemetry` import beside the existing
`console.routes` one would shadow that binding and break every MCP tool call
(the `utilization` note in AGENTS.md).
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import time
from typing import Any, Awaitable, Callable

from starlette.requests import Request
from starlette.responses import Response

from cube_cloud.browser_proxy.rate_limit import SlidingWindowRateLimiter
from cube_cloud.config import settings
from cube_cloud.telemetry import archive, classify, otlp
from cube_cloud.telemetry.events import ToolCallEvent, build_console_event

logger = logging.getLogger(__name__)

# Path template (as registered in main.py) -> event name, or None for a route
# that is declared but never recorded. Every `/console*` route MUST appear here;
# `test_console_telemetry.py` walks `app.routes` and fails on one that does not,
# so adding a route is a conscious decision about whether it is a usage signal.
#
# Event names are what the dashboard shows (labelled in its ACT map; an unknown
# name renders as a derived label, never an error). Keep the `console.` prefix —
# it is what keeps a console row distinguishable from a tool of the same name in
# `tool`, independent of the `source` column.
CONSOLE_ROUTES: dict[str, str | None] = {
    # Fired once per SPA load: the "console opened" signal. Suppressed like any
    # read, so a route change that re-checks the session is not a second open.
    "/console/api/session": "console.open",
    "/console/api/cubes": "console.list_cubes",
    # The fleet Apps page (§4.22): its own URL and one fetch per view.
    "/console/api/apps": "console.view_apps",
    # The landing page's map, fetched only when a viewer switches to it: its own
    # intent, not a satellite of the list, which never fetches it.
    "/console/api/gps": "console.view_map",
    "/console/api/cubes/{cube}": "console.view_cube",
    # Satellites of view_cube — fetched alongside the detail payload, not on
    # their own intent. Counting them multiplies one page view by seven.
    "/console/api/cubes/{cube}/services": None,
    "/console/api/cubes/{cube}/exposed": None,
    "/console/api/cubes/{cube}/changes": None,
    "/console/api/cubes/{cube}/status": None,
    "/console/api/cubes/{cube}/teleport": None,
    "/console/api/cubes/{cube}/inventory": None,
    "/console/api/cubes/{cube}/gps": None,
    # A distinct page (its own URL) and a distinct tab (fetched only when open).
    "/console/api/cubes/{cube}/logs": "console.view_logs",
    # Fetched only when a user opens an app's status — its own intent, not a
    # satellite of the page load.
    "/console/api/cubes/{cube}/health": "console.view_app_health",
    "/console/api/cubes/{cube}/utilization": "console.view_resources",
    # The AI tab (docs/ai-reactor-deploy-spec.md). The page PREFETCHES it with the
    # tab hidden (`?prefetch=1`, see _PREFETCHED below), so only the read made when
    # the tab is opened counts.
    "/console/api/cubes/{cube}/ai": "console.view_ai",
    # The Field Guide document; its css/js are assets.
    "/console/guide": "console.view_guide",
    "/console/guide/{name}": None,
    # The fleet map's outline: an asset fetched with `/console/api/gps`, which is the
    # counted intent (`console.view_map`).
    "/console/map/outline.json": None,
    # The SPA shell — also serves /console/assets/*, so a hit is not a view.
    # The non-GET method guards share these two templates and are 405s.
    "/console": None,
    "/console/{sub_path:path}": None,
    # Mutations. Never suppressed.
    "/console/api/cubes/{cube}/expose": "console.expose",
    "/console/api/cubes/{cube}/unexpose": "console.unexpose",
    "/console/api/feedback": "console.feedback",
    "/console/api/cubes/{cube}/ai/deploy": "console.ai_deploy",
    "/console/api/cubes/{cube}/ai/remove": "console.ai_remove",
}

COUNTED_EVENTS: frozenset[str] = frozenset(v for v in CONSOLE_ROUTES.values() if v)

# Reads the SPA makes ahead of intent, so a hit carrying `prefetch=1` is not a view.
# The AI tab loads with the cube page so switching to it is instant, and opening the
# tab then makes one unmarked read, which is the counted view. Only these templates
# honour the flag: a caller can hide its own usage row and nothing else.
_PREFETCHED: frozenset[str] = frozenset({"/console/api/cubes/{cube}/ai"})

# HTTP methods whose repeats are suppressed. A POST is an action each time.
_SAFE_METHODS = frozenset({"GET", "HEAD"})

# Query params that join the suppression key: the same cube's logs for a
# different app is a different thing being looked at.
_SUPPRESS_KEY_QUERY_PARAMS = ("app",)

# Bounds the suppression dict by COUNT. Size is bounded separately: every
# caller-supplied component of a key is reduced to a fixed-width digest before it
# is stored (`_suppression_key`), so a key is ~90 bytes whatever the request line
# carried. The password-reset limiter is the precedent — it capped the count and
# still let a caller park arbitrarily long strings for a full window.
_SUPPRESS_MAX_KEYS = 20_000

# Per-session emission ceiling, independent of the content-keyed suppressor. A
# cooperative SPA never approaches it (a cube page is ~1 counted request, the
# logs poll is one row per suppression window). It exists for the uncooperative
# case — `GET /console/api/cubes/probe-<i>` in a loop is a fresh suppression key
# every time — where each recorded row is an S3 PutObject and a span, attributed
# to that session and landing junk in the `cube` dimension. Two per second is far
# above any real console use and far below what a loop can generate.
_SESSION_CAP_WINDOW_SECONDS = 60.0
_SESSION_CAP_PER_WINDOW = 120
# Sessions, not requests — bounded by concurrent authenticated users, but passed
# because the limiter's docstring says to pass it for any key a caller influences.
_SESSION_CAP_MAX_KEYS = 10_000

_suppressor: SlidingWindowRateLimiter | None = None
_suppressor_window: float | None = None
_session_cap: SlidingWindowRateLimiter | None = None
# Warns once per session per cap window rather than once per dropped request, so
# a flood is visible in CloudWatch without the log itself becoming the flood.
_cap_warned: SlidingWindowRateLimiter | None = None


def enabled() -> bool:
    return bool(settings.telemetry_enabled and settings.telemetry_console_enabled)


def event_for(request: Request) -> str | None:
    """The event name for the matched route, or None when it is not counted.

    Unknown (no matched route on the scope, or a template not in the registry) is
    also None: fail toward recording nothing. The registry test is what keeps
    "unknown" from being a route someone forgot.
    """
    route = request.scope.get("route")
    template = getattr(route, "path", None)
    if not isinstance(template, str):
        return None
    if template in _PREFETCHED and request.query_params.get("prefetch") == "1":
        return None
    return CONSOLE_ROUTES.get(template)


def reset_suppression() -> None:
    """Drop the suppression + cap state (tests; a settings change at runtime)."""
    global _suppressor, _suppressor_window, _session_cap, _cap_warned
    _suppressor = None
    _suppressor_window = None
    _session_cap = None
    _cap_warned = None


def _session_id(request: Request) -> str:
    """The caller's session, as the middleware's own hash — never anything the
    request line carried. `session_key` is a SHA-256 prefix and `key_id` is the
    stored key hash, so this component is fixed-width by construction."""
    state = getattr(request, "state", None)
    return getattr(state, "session_key", None) or getattr(state, "key_id", None) or ""


def _suppression_key(request: Request, event_name: str, cube: str | None) -> str:
    """(session, event, digest of the caller-supplied parts).

    `cube` is the raw path segment and `app` the raw query value — neither is
    validated before this runs (it runs after the handler, including after a 403
    or 404), so they are reduced to one fixed-width digest rather than stored.
    Same rule, same reason, as the password-reset limiter's email key.
    """
    extra = "|".join(
        f"{k}={request.query_params.get(k) or ''}" for k in _SUPPRESS_KEY_QUERY_PARAMS
    )
    digest = hashlib.sha256(f"{cube or ''}|{extra}".encode("utf-8")).hexdigest()[:32]
    return f"{_session_id(request)}|{event_name}|{digest}"


def _suppressed(request: Request, event_name: str, cube: str | None, status: str) -> bool:
    """True when this SUCCESSFUL read repeats one already recorded inside the window.

    Errors are never suppressed: the outcome is known here (this runs after the
    handler), and a read that fails after a success in the same window must
    still land, or a five-minute outage records one `ok` row and nothing else.
    The cost is that a failing poll loop records every tick — bounded by the
    per-session cap, and it is the signal an error panel exists to show.
    """
    global _suppressor, _suppressor_window
    if request.method.upper() not in _SAFE_METHODS:
        return False
    if status != classify.STATUS_OK:
        return False
    window = float(settings.telemetry_console_suppress_seconds or 0)
    if window <= 0:
        return False
    if _suppressor is None or _suppressor_window != window:
        _suppressor = SlidingWindowRateLimiter(
            max_requests=1, window_seconds=window, max_keys=_SUPPRESS_MAX_KEYS
        )
        _suppressor_window = window
    # `allow` records a hit only when it returns True, so a suppressed repeat does
    # not extend the window: an open logs tab is one row per window, not zero.
    return not _suppressor.allow(_suppression_key(request, event_name, cube))


def _over_session_cap(request: Request, event_name: str) -> bool:
    """True when this session has already emitted its per-minute allowance."""
    global _session_cap, _cap_warned
    if _session_cap is None:
        _session_cap = SlidingWindowRateLimiter(
            max_requests=_SESSION_CAP_PER_WINDOW,
            window_seconds=_SESSION_CAP_WINDOW_SECONDS,
            max_keys=_SESSION_CAP_MAX_KEYS,
        )
        _cap_warned = SlidingWindowRateLimiter(
            max_requests=1, window_seconds=_SESSION_CAP_WINDOW_SECONDS,
            max_keys=_SESSION_CAP_MAX_KEYS,
        )
    session = _session_id(request)
    if _session_cap.allow(session):
        return False
    if _cap_warned is not None and _cap_warned.allow(session):
        # The session id is the middleware's hash, not a person; the event name
        # is ours. Nothing caller-supplied is logged.
        logger.warning(
            "telemetry: console events for one session exceeded %d/%.0fs; "
            "dropping until the window clears (profile=%s event=%s)",
            _SESSION_CAP_PER_WINDOW, _SESSION_CAP_WINDOW_SECONDS,
            getattr(getattr(request, "state", None), "profile", "?"), event_name,
        )
    return True


def classify_http(status_code: int | None, exc: BaseException | None) -> tuple[str, str | None]:
    """(status, error_class) from the HTTP outcome, mirroring `classify.classify`.

    An exception wins, as it does for tool calls. Codes map onto the SAME enum the
    tool rows use so the dashboard's failure dimension needs no new labels; a
    code with no natural bucket is `unknown` rather than a new value.
    """
    if exc is not None:
        return classify.classify("", exc)
    code = int(status_code or 0)
    if code < 400:
        return classify.STATUS_OK, None
    if code in (401, 403):
        return classify.STATUS_ERROR, classify.AUTH_DENIED
    if code == 404:
        return classify.STATUS_ERROR, classify.NOT_FOUND
    if code == 504 or code == 408:
        return classify.STATUS_ERROR, classify.TIMEOUT
    if 400 <= code < 500:
        return classify.STATUS_ERROR, classify.BAD_REQUEST
    return classify.STATUS_ERROR, classify.UNKNOWN


def _response_size(response: Response | None) -> int:
    if response is None:
        return 0
    try:
        length = response.headers.get("content-length")
        if length is not None:
            return int(length)
        body = getattr(response, "body", None)
        if isinstance(body, (bytes, bytearray)):
            return len(body)
    except Exception:
        return 0
    return 0


def build_request_event(
    request: Request,
    event_name: str,
    response: Response | None,
    exc: BaseException | None,
    latency_ms: float,
) -> ToolCallEvent:
    """The event for one observed console request. Pure; never reads a body."""
    path_params = dict(getattr(request, "path_params", {}) or {})
    args: dict[str, Any] = {**path_params, **dict(request.query_params)}
    cube = path_params.get("cube")
    status, error_class = classify_http(getattr(response, "status_code", None), exc)
    return build_console_event(
        request,
        event_name,
        args,
        cube if isinstance(cube, str) else None,
        status,
        error_class,
        latency_ms,
        response_size_bytes=_response_size(response),
    )


def record_console_request(
    request: Request,
    event_name: str,
    response: Response | None,
    exc: BaseException | None,
    latency_ms: float,
) -> None:
    """Build and emit the event for one console request. Never raises."""
    if not enabled():
        return
    try:
        # Built before the suppression decision because the decision needs the
        # outcome: an error is never suppressed. Building is cheap (no I/O).
        event = build_request_event(request, event_name, response, exc, latency_ms)
        if _suppressed(request, event_name, event.cube, event.status):
            return
        if _over_session_cap(request, event_name):
            return
        # OTLP first so the span's trace_id is stamped onto the event before the
        # S3 record is written — the same order as record_tool_call.
        otlp.emit_span(event)
        archive.emit(event)
    except BaseException:
        # Invoked from `observe`'s `finally`: an escaping error here would replace
        # the handler's own exception or response. Swallow everything and log.
        logger.exception("telemetry: record_console_request failed (swallowed)")


async def observe(
    request: Request, handler: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Run a console handler and record the request as a usage event.

    The console analog of the `try/finally` in `main.py::call_tool`. The handler
    runs exactly as it would unobserved; recording happens afterwards and cannot
    change the outcome. A client disconnect (`CancelledError`) is not a usage
    outcome and records nothing, as in the tool wrapper.
    """
    event_name = event_for(request)
    if event_name is None or not enabled():
        return await handler(request)

    start = time.monotonic()
    response: Response | None = None
    exc: BaseException | None = None
    record = True
    try:
        response = await handler(request)
        return response
    except asyncio.CancelledError:
        record = False
        raise
    except BaseException as e:
        exc = e
        raise
    finally:
        if record:
            latency_ms = (time.monotonic() - start) * 1000.0
            record_console_request(request, event_name, response, exc, latency_ms)
