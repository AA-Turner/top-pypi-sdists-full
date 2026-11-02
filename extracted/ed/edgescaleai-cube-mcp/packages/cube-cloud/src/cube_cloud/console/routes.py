"""Console HTTP routes (docs/console-spec.md §4.2, §5).

Phase 1 serves the SPA shell and one session endpoint. Every route here is a GET;
the read contract in spec §4.2 is enforced by :func:`guard_read`.

Authentication happened already, in `APIKeyMiddleware`: `/console` is the single
entry in `COOKIE_ALLOWED_APEX_PREFIXES`, so an unauthenticated browser navigation
was 302'd to login and never reaches these handlers. Nothing here re-checks the
credential; what it *does* check is that the request is same-origin, which the
middleware does not and cannot know about.
"""

from __future__ import annotations

import logging
from pathlib import Path
from urllib.parse import urlsplit

from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse, Response

from cube_common.apollo_client import ApolloClient, ApolloError
from cube_cloud._request_context import current_request
from cube_cloud import ic2
from cube_cloud.auth import session_cookie
from cube_cloud.config import settings
from cube_cloud.auth.app_companies import app_companies, combinable_companies, reads_stored_sets
from cube_cloud.console import csrf, reads, utilization, writes
from cube_cloud.tools import feedback as feedback_tool
from cube_cloud.tools import freshservice as freshservice_tool
from cube_cloud.tools import groundcover

logger = logging.getLogger(__name__)

# Feedback field limits, enforced by `submit_feedback` below.
#
# `SUMMARY_MAX_CHARS` is Freshservice's own documented `subject` cap. Matching it
# exactly is the point: one character over and Freshservice answers 400, which
# `freshservice._explain_failure` reads as a changed field contract and reports to the
# submitter as "its required fields have changed" — a confident misdiagnosis pointing
# at our configuration when the actual problem is the text they just typed.
#
# The body limits are ours, not upstream's, and are deliberately generous — a genuine
# incident report with logs pasted in should fit. They exist because this route writes
# into a live helpdesk queue shared by dev and prod, so an unbounded body is a way to
# make a real ticket unusable.
#
# **These are NOT a rate limit and must not be mistaken for one.** Nothing here stops
# an authenticated caller looping the endpoint; the only rate limiter in this codebase
# is the app proxy's. That gap is real and is tracked separately.
SUMMARY_MAX_CHARS = 255
BODY_MAX_CHARS = 20_000
CUBE_MAX_CHARS = 200

# Built SPA assets land here (the Dockerfile's node stage copies them in). Absent
# in a plain checkout, which `shell` handles — see `_PLACEHOLDER_SHELL`.
STATIC_DIR = Path(__file__).parent / "static"
INDEX_HTML = STATIC_DIR / "index.html"

# The Cube Field Guide (docs/console-spec.md §4.11). Lives in the repo at
# `console/web/public/guide/` — committed source, edited in place — which Vite
# copies verbatim into STATIC_DIR, so it rides the SPA's existing build and
# packaging. Like the bundle, that means it is absent from a plain checkout.
GUIDE_PREFIX = f"{session_cookie.CONSOLE_PREFIX}/guide"
GUIDE_DIR = STATIC_DIR / "guide"
GUIDE_INDEX = GUIDE_DIR / "index.html"

# The fleet map's outline (country and state/province borders), built once from
# Natural Earth by `scripts/build-map-outline.py` into `console/web/public/map/`, which
# Vite copies verbatim into STATIC_DIR like the guide. Served by `map_outline` because
# the shell's CSP (`connect-src 'self'`) allows no third-party tiles.
MAP_OUTLINE = STATIC_DIR / "map" / "outline.json"

# Cross-site request detection. `Sec-Fetch-Site` is sent by every current browser
# and is the primary signal; `same-origin` is the only value the JSON API accepts.
# Documents (the shell and the guide) additionally accept `none` (a typed URL or a
# bookmark) and a TOP-LEVEL navigation from any site (a link clicked in Slack, Gmail
# or Jira) — see `_is_top_level_navigation` for why that is safe. Neither is ever
# accepted for the JSON API.
_SAFE_FETCH_SITES = {"same-origin"}


def _shell_headers(*, allow_inline_style: bool = False) -> dict[str, str]:
    """Security headers for the console shell document.

    **Why a CSP at all.** Cube names come from Apollo and are rendered into the
    page. React escapes them, and a review confirmed the SPA uses no `innerHTML`,
    `dangerouslySetInnerHTML`, `eval`, or `new Function` — but that made React's
    escaping the *only* layer. This adds a second one, ahead of Phase 4 introducing
    mutations that a successful injection could drive.

    The policy is strict because the console can afford it: the SPA loads exactly
    its own hashed bundle and stylesheet from `/console/assets`, talks only to its
    own origin, embeds no images or fonts, and has no `<form>`.

    * `default-src 'none'` — allowlist from zero rather than trimming a default.
    * `script-src 'self'` — Vite emits an external module script, never inline, so
      no nonce or `'unsafe-inline'` is needed.
    * `style-src 'self'` — the built CSS is a real file. React's `style={{…}}` sets
      properties through CSSOM (`node.style.x = …`) rather than writing a `style`
      attribute, and CSSOM mutation is not subject to CSP, so inline style props
      keep working. Verified in a browser rather than assumed.
    * `form-action 'none'` + `base-uri 'none'` — nothing to submit, and no `<base>`
      to hijack asset resolution.
    * `frame-ancestors 'none'` — the console must never be framed; combined with
      the legacy `X-Frame-Options` for older agents.
    * `connect-src 'self'` — the JSON API only. An exfiltration attempt to a
      foreign host is blocked even if script execution were achieved.

    Deliberately NOT applied globally: the `/auth/*` pages carry inline `<style>`
    blocks and would break under `style-src 'self'`. Scoping this to the console
    shell keeps that decision explicit rather than a middleware side effect.
    """
    style = "'self' 'unsafe-inline'" if allow_inline_style else "'self'"
    csp = "; ".join([
        "default-src 'none'",
        "script-src 'self'",
        f"style-src {style}",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'self'",
        "base-uri 'none'",
        "form-action 'none'",
        "frame-ancestors 'none'",
        "object-src 'none'",
    ])
    return {
        # no-store: the shell is per-session authenticated, and a cached copy served
        # after logout would render a signed-out frame.
        "Cache-Control": "no-store",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": csp,
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
    }


def _guide_headers() -> dict[str, str]:
    """Security headers for the field-guide document (spec §4.11).

    **A SECOND, LOOSER PROFILE — deliberately not a flag on `_shell_headers`.**
    The guide needs `'unsafe-inline'` in `style-src` and the console shell must
    never have it; keeping the two builders as separate functions is what stops a
    later "let's unify these" from handing the SPA a policy it cannot afford. Do
    not merge them, and do not widen the shell's policy to match this one.

    Why the relaxation is safe *here* and not there: the guide is a static
    document that interpolates **no** server, tenant, or user data — every string
    it renders is its own literal — so there is no vector through which a style
    could be injected. The shell renders Apollo-supplied cube names, which is
    exactly the case `style-src 'self'` is guarding.

    * `style-src 'self' 'unsafe-inline'` — the guide carries over 500 inline `style="…"`
      attributes. Migrating them to classes is *possible* (the
      document is ours to edit) but buys no security here, for the reason above —
      so it stays a legitimate future cleanup rather than a prerequisite.
    * `script-src 'self'` — **no `'unsafe-inline'`, no `'unsafe-eval'`.** The
      document's script is external, and it contains no `eval` and no
      `new Function`. Both halves are asserted in `console/web/src/guide.test.ts`,
      which runs on every build.
    * `connect-src 'none'` — stricter than the console's `'self'`. The guide makes
      no requests at all: no `fetch`, no WebSocket, no beacon. So even a
      hypothetical injection has nowhere to send anything.
    * `img-src`/`font-src` allow `data:` — seven embedded base64 images and one
      `@font-face` with an inlined woff2.

    `Cache-Control` differs from the shell's `no-store`: the guide carries nothing
    per-session, so a short private cache is correct and keeps the 500 KB of JS
    off the wire while someone reads.
    """
    csp = "; ".join([
        "default-src 'none'",
        "script-src 'self'",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data:",
        "font-src 'self' data:",
        "connect-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
        "frame-ancestors 'none'",
        "object-src 'none'",
    ])
    return {
        "Cache-Control": "private, max-age=600",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": csp,
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
    }


def _disabled_response(path: str) -> Response:
    """What an off-console serves: a plain 404, as if the surface didn't exist.

    404 rather than 403 deliberately — a "forbidden" advertises that something is
    there. JSON for the API paths (the SPA's fetch would choke on HTML), plain
    text otherwise.
    """
    if path.startswith(f"{session_cookie.CONSOLE_PREFIX}/api/"):
        return _json({"error": "Not found."}, status_code=404)
    return Response("Not found.", status_code=404, media_type="text/plain")


def is_enabled() -> bool:
    """Whether the console is served on this stack (`CUBE_CLOUD_CONSOLE_ENABLED`).

    Read per request, not captured at import, so the flag is patchable in tests
    and a stack that flips it needs only a restart.
    """
    return settings.console_enabled


def ai_enabled() -> bool:
    """Whether the AI tab is served (`CUBE_CLOUD_CONSOLE_AI_ENABLED`, under the console flag)."""
    return settings.console_enabled and settings.console_ai_enabled


def is_proxy_host(request: Request) -> bool:
    """True when this request belongs to the app proxy rather than the console.

    The host gate from spec §4.1. Registering `/console` before the app-proxy
    catch-all reserves that path on **every** host, which would silently claim
    `/console` inside every proxied in-cube app. Delegating on an app-subdomain
    host gives the path back: `/console` is the console on the apex only.
    """
    return session_cookie.is_app_subdomain_host(request.url.hostname or "")


def _is_top_level_navigation(request: Request) -> bool:
    """Whether the browser says this is a top-level document navigation.

    True for a link followed in the address bar's window, from ANY site. That is
    what a shared deep link is: someone pastes `/console/cubes/<name>` into Slack,
    Gmail or Jira and a colleague clicks it, and the browser reports
    `Sec-Fetch-Site: cross-site` (or `same-site` from a sibling host under the
    apex). Refusing those made every shared link a raw JSON 403 for anyone already
    signed in — a signed-out user never saw it, because the login form's redirect
    back is same-origin.

    Accepting it is sound because of what answers it, not because the request is
    trusted: the shell and the guide are static documents, identical for every
    caller, carrying no tenant data; every byte of data comes from `/console/api/*`,
    whose `guard_read` never accepts a navigation; framing is refused by
    `frame-ancestors 'none'` and `X-Frame-Options`; and `SameSite=Lax` already sends
    the session cookie on exactly this request, so nothing is newly authenticated.
    **The invariant this leans on is that URL state never triggers a server-side
    write** — no non-GET request, and no state-changing GET, may be issued because of
    a path or query parameter; every write is a click that sends the CSRF token. A
    deep link that performed an action on load would turn this into a CSRF hole.
    (`?theme=` writing the viewer's own `localStorage` is the one client-local
    exception, and is named as such in AGENTS.md console rule 1a.) The client half is
    pinned by `console/web/src/deepLinks.test.tsx`.

    `Sec-Fetch-Dest: document` is what makes it TOP-LEVEL: an iframe navigation
    also reports `mode: navigate` but `dest: iframe`, and a subresource
    (`<script src>`, `fetch`) never reports `navigate`. Page script cannot set any
    `Sec-` header, so a page cannot claim to be a navigation it is not.
    """
    return (
        request.headers.get("sec-fetch-mode", "").lower() == "navigate"
        and request.headers.get("sec-fetch-dest", "").lower() == "document"
    )


def _same_origin(request: Request, *, allow_navigation: bool) -> bool:
    """Whether the request is same-origin, per spec §4.2 read contract item 2.

    Prefers `Sec-Fetch-Site`; falls back to an `Origin`/`Referer` host match
    against the configured apex when the header is absent (non-browser or very
    old client). Fail closed: no usable signal ⇒ False.

    `allow_navigation` is for DOCUMENTS only (the shell and the guide): it also
    accepts a typed URL or bookmark (`none`) and a top-level navigation from any
    site. The JSON API passes False and accepts `same-origin` alone.
    """
    site = request.headers.get("sec-fetch-site", "").lower()
    if site:
        if site in _SAFE_FETCH_SITES:
            return True
        if not allow_navigation:
            return False
        # A typed URL or a bookmark reports "none"; a link clicked on another site
        # reports "cross-site"/"same-site" and is accepted only as a top-level
        # navigation.
        return site == "none" or _is_top_level_navigation(request)

    # No Sec-Fetch-Site. If the client states an origin, verify it; an origin we
    # cannot verify (apex unconfigured) is refused rather than assumed good.
    apex = session_cookie.apex_host()
    for header in ("origin", "referer"):
        value = request.headers.get(header)
        if not value:
            continue
        try:
            parts = urlsplit(value)
            host = (parts.hostname or "").lower()
            # `.port` RAISES on a malformed port — `urlsplit("https://apex:notaport")
            # .port` -> ValueError. Both guards are called outside any try/except, so
            # an authenticated request with `Origin: https://<apex>:notaport` and no
            # Sec-Fetch-Site returned a 500 with a traceback instead of a 403. Read it
            # here so the whole parse is covered by one handler.
            port = parts.port
        except ValueError:
            # Unparseable is not same-origin. Fail closed, and keep looking at the
            # next header rather than accepting.
            continue
        if not host:
            continue
        if not apex:
            return False
        # Full scheme + host + port comparison, not host alone. This branch exists
        # for clients that send no Sec-Fetch-Site, so it must not accept
        # `http://apex` or `https://apex:8443` as same-origin. (There is no HSTS
        # header on this app or the ALB, so nothing else closes the scheme hole.)
        return parts.scheme == "https" and host == apex and port in (None, 443)

    # No Sec-Fetch-Site, no Origin, no Referer. A same-origin navigation from a
    # bookmark legitimately has none of these, so allow it for HTML only. Note
    # this must NOT depend on the apex being configured — an unset domain (local
    # dev) would otherwise 403 the whole console.
    return allow_navigation


def _json(payload: dict, status_code: int = 200) -> JSONResponse:
    """JSON response meeting spec §4.2 read-contract items 3 and 4.

    `nosniff` stops a browser from re-interpreting the body as script, and the
    payload is always an **object** — never a top-level array, which historically
    was readable cross-origin via `<script src>`.
    """
    if not isinstance(payload, dict):  # pragma: no cover - programming error
        raise TypeError("console JSON responses must be objects, not arrays")
    return JSONResponse(
        payload,
        status_code=status_code,
        headers={
            "X-Content-Type-Options": "nosniff",
            # Every console JSON response is per-session authenticated, and
            # /console/api/session carries the CSRF token — none of it may sit in
            # a shared or heuristic cache.
            "Cache-Control": "no-store",
        },
    )


def _log_write_failure(action: str, profile: str, cube: str, exc: BaseException) -> None:
    """Record a failed console mutation by exception CLASS only. Never the message.

    AGENTS.md console rule 3, applied to the write path rather than the read. Both
    mutations run `modules._fetch_module_installations` (LIST_MODULES), which selects
    **every** module's variable values on the cube — a module variable can hold a
    secret, and `ApolloError` embeds the raw GraphQL response body in its message. So
    `"%s" % e` here is the same disclosure `reads._exposed_apps_read` is careful to
    avoid, and `logger.exception` is worse: it prints the whole `__cause__` chain, so
    an `ApolloError` re-raised as something else leaks through the generic handler too.

    This costs real debuggability, and the accepted replacement is the one the read
    layer already names: reproduce with the `list_modules` MCP tool, which is allowed
    to show the underlying error. Centralized so a third mutating route cannot get
    this wrong by copying the wrong sibling.
    """
    logger.error(
        "console %s failed for profile=%s cube=%s (%s) — message withheld; reproduce "
        "with the list_modules tool to see the underlying error.",
        action, profile, cube, type(exc).__name__,
    )


def guard_read(request: Request) -> JSONResponse | None:
    """Enforce the read contract on a JSON API request. Returns a 403 or None.

    Call this first in every `/console/api/*` handler.
    """
    if not _same_origin(request, allow_navigation=False):
        return _json({"error": "Cross-site request refused."}, status_code=403)
    return None


# Header carrying the synchronizer token on a mutating console request. Named on the
# request side only — the token is delivered in the /console/api/session body.
CSRF_HEADER = "X-Console-CSRF"


def guard_write(request: Request) -> JSONResponse | None:
    """Enforce the spec §4.2 WRITE contract. Returns an error response, or None.

    Call this first in every mutating console handler, before any Apollo work.

    Two independent controls, and both must pass:

    1. **Origin enforcement** (the primary control). Identical to the read contract
       except that a navigation is never acceptable for a mutation — `Sec-Fetch-Site`
       must be `same-origin`, or a stated `Origin`/`Referer` must match the apex on
       scheme, host and port.
    2. **A synchronizer token** in `X-Console-CSRF`, verified against
       `HMAC(csrf_secret, key_id)`. `key_id` is the stored key hash, which the browser
       never sees, so the token cannot be derived by an attacker who merely knows the
       victim's session exists.

    Why both, when `SameSite=Lax` already blocks a cross-site POST from carrying the
    cookie: Lax is a *browser* behavior and this is the surface where a mistake
    executes `install_entity`-class work under someone else's identity. The token also
    fails closed when the secret is unavailable (`csrf.verify` → False), so a stack
    that never provisioned it cannot mutate at all — which is why
    `/console/api/session` reports `mutations_available` rather than letting the UI
    discover it at click time.
    """
    if not _same_origin(request, allow_navigation=False):
        return _json({"error": "Cross-site request refused."}, status_code=403)

    key_id = getattr(request.state, "key_id", "") or ""
    presented = request.headers.get(CSRF_HEADER)
    if not csrf.verify(key_id, presented):
        # Deliberately does not distinguish "no token", "wrong token" and "secret
        # unavailable" — a caller learns only that it was refused.
        logger.warning(
            "console mutation refused: CSRF token invalid or unavailable (profile=%s)",
            getattr(request.state, "profile", "?"),
        )
        return _json({"error": "Invalid or missing CSRF token."}, status_code=403)
    return None


async def method_not_allowed(request: Request) -> Response:
    """405 for a non-GET under the console prefix.

    Async purely so it is awaitable like the other handlers routed through
    ``main.py::_console_or_proxy``.

    Every Phase 1–3 console route is a GET, but Starlette only rejects a method
    for a path it actually matched — so without this, a `POST /console/...` fell
    through to the app-proxy catch-all, skipping `is_enabled()`, the origin check,
    and the JSON hardening, and 404ing from proxy code instead. Benign in itself
    (`SameSite=Lax` keeps a cross-site POST from carrying the cookie at all), but
    it is the exact seam the Phase 4 mutation routes land in: a mutating path
    registered after the catch-all, or forgotten, would silently reach the proxy
    rather than being refused here.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    return _json(
        {"error": f"{request.method} is not allowed on the console."},
        status_code=405,
    )


async def session(request: Request) -> Response:
    """`GET /console/api/session` — who the caller is, plus the CSRF token.

    Deliberately minimal: the profile name, the owner's email *domain* (never the
    address — only a domain and a hash are stored, see `auth/api_keys.py`), and
    the mint of `console/csrf.py`. **Never the API key** — it stays in the
    HttpOnly cookie and the browser never needs to see it.

    The token is delivered here rather than templated into the shell HTML. Both
    are same-origin-only and unreadable cross-origin (no CORS headers are set);
    this way the shell stays a static file with no templating.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    token = csrf.issue(getattr(state, "key_id", "") or "")
    return _json({
        "profile": getattr(state, "profile", None),
        "user_domain": getattr(state, "user_domain", None),
        "actor_type": getattr(state, "actor_type", None),
        "csrf_token": token,
        # Surfaced so the UI can say why an action is unavailable instead of
        # failing mysteriously once the Phase 4 mutations land.
        "mutations_available": token is not None,
        # Mirrors CUBE_CLOUD_JIRA_ENABLED so the "Send feedback" entry point can
        # hide itself on a stack where a submission would only 502 — the same
        # "hide, don't fail at click time" rule `mutations_available` follows.
        "feedback_enabled": settings.jira_enabled,
        # Mirrors CUBE_CLOUD_CONSOLE_AI_ENABLED so the cube page shows its AI tab only
        # on a stack that serves it (docs/ai-reactor-deploy-spec.md).
        "ai_enabled": ai_enabled(),
        # Which app companies this profile holds (home first) and whether this stack
        # lets an app be shared with several of them. The page offers only these
        # companies; `writes` re-checks whatever comes back.
        "app_companies": _session_app_companies(getattr(state, "profile", None)),
        "multi_company": reads_stored_sets(),
        # Which companies may share one app (null: any). Only meaningful with
        # `multi_company`: a baseline stack combines nothing, whatever this says. The picker
        # needs it to say before the click that a join would be refused (`can_combine`).
        # It goes to EVERY session on the stack, unscoped: never put a customer's company in
        # `app_companies_combinable` (prod never sets it; the brake is the empty list).
        "combinable": _session_combinable(),
        # Whether this stack has the GPS feature on, so the landing page can decide to
        # offer its List / Map switch without fetching the map route (an inventory read
        # plus an InControl2 refresh). The flag only: nothing upstream is touched here.
        "gps_enabled": ic2.is_enabled(),
    })


def _session_combinable() -> list[str] | None:
    allowed = combinable_companies()
    return None if allowed is None else sorted(allowed)


def _session_app_companies(profile: str | None) -> dict | None:
    companies = app_companies(profile) if profile else None
    if companies is None:
        return None
    rest = sorted(c for c in companies.held if c != companies.home)
    return {"home": companies.home, "held": [companies.home, *rest] if not companies.unscoped else [],
            "unscoped": companies.unscoped}


def _asset_response(path: str) -> Response | None:
    """Serve a built SPA asset, or None if `path` isn't one.

    Assets are served from here rather than a `StaticFiles` mount so that every
    console URL — shell, API, and assets alike — passes through the single host
    gate in `main.py`. A mount would bypass it and re-introduce the path
    reservation inside proxied in-cube apps that the gate exists to prevent.
    """
    prefix = f"{session_cookie.CONSOLE_PREFIX}/assets/"
    if not path.startswith(prefix):
        return None

    try:
        assets_root = (STATIC_DIR / "assets").resolve()
        candidate = (assets_root / path[len(prefix):]).resolve()
        # Containment check: `..` in the URL must never escape the assets
        # directory. `resolve()` collapses traversal AND resolves symlinks, so an
        # escaping symlink is rejected rather than followed.
        contained = candidate.is_relative_to(assets_root) and candidate.is_file()
    except (ValueError, OSError):
        # A NUL byte in the path makes pathlib raise ValueError("embedded null
        # byte") — uvicorn decodes %00 straight into scope["path"], so this is
        # reachable and would otherwise surface as an unhandled 500.
        return _json({"error": "Not found."}, status_code=404)

    if not contained:
        return _json({"error": "Not found."}, status_code=404)

    # Vite content-hashes asset filenames, so they are safe to cache hard.
    return FileResponse(
        candidate,
        headers={
            "Cache-Control": "public, max-age=31536000, immutable",
            "X-Content-Type-Options": "nosniff",
        },
    )


async def cubes(request: Request) -> Response:
    """`GET /console/api/cubes` — the caller's RBAC-scoped cube list.

    Apollo credentials come from `request.state`, resolved by `APIKeyMiddleware`
    from the caller's profile — so this reads as the *caller's* tenant, never as a
    shared or elevated identity, and the authorization decision stays in
    `auth/apollo_rbac.py` rather than being restated here.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    # Resolved BEFORE the try: the handlers below log it, and dereferencing
    # request.state inside an except block that may have fired *because* an
    # attribute was missing makes the diagnostic raise and swallow itself (a probe
    # captured zero log output for exactly that case).
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.list_cubes(client, profile)
    except ApolloError as e:
        # Apollo's own refusals (auth, RBAC, malformed query) are the caller's
        # problem to see, but the text can carry internals — so the browser gets a
        # stable message and the detail goes to the log.
        logger.warning("console cube list failed for profile=%s: %s", profile, e)
        return _json(
            {"error": "Could not read the cube list from Apollo."}, status_code=502
        )
    except Exception:
        logger.exception("console cube list errored for profile=%s", profile)
        return _json({"error": "Could not read the cube list."}, status_code=500)

    return _json(payload)


async def fleet_apps(request: Request) -> Response:
    """`GET /console/api/apps` — every app the caller can open, across the fleet.

    Read-only, and no arguments: the one thing it varies on is who is asking. The
    authorization is `reads.fleet_apps`' own (`can_see` over the admin Teleport
    listing, spec §4.22), so there is no access check here to reorder. A Teleport
    failure is a 200 with `available: false`, like the other secondary reads; Apollo
    only places apps on cubes, so it degrades inside the read rather than here.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.fleet_apps(client, profile)
    except Exception as e:
        # Class only: nothing on this path should raise, and whatever did may carry an
        # upstream body in its message.
        logger.error("console fleet apps errored for profile=%s (%s)", profile, type(e).__name__)
        return _json({"error": "Could not read the app list."}, status_code=500)

    return _json(payload)


async def fleet_gps(request: Request) -> Response:
    """`GET /console/api/gps` — GPS positions for every cube the caller can see, for
    the landing page's map.

    A fleet read with no arguments, like `/console/api/apps`; it varies only on who is
    asking. Not under `/console/api/cubes/`, where `gps` would be read as a cube name.
    Authorization is `reads.fleet_gps`'s: the caller's Apollo-visible set is resolved
    before inventory or IC2 is asked anything, and nothing outside it is returned. An
    inventory or IC2 failure is a 200 with `gps_source.available: false`; only an
    Apollo failure is an error, as for the cube list.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.fleet_gps(client, profile)
    except ApolloError as e:
        logger.warning("console fleet gps read failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube list from Apollo."}, status_code=502)
    except Exception as e:
        # Class only: whatever raised may carry an upstream body in its message.
        logger.error("console fleet gps errored for profile=%s (%s)", profile, type(e).__name__)
        return _json({"error": "Could not read the cube locations."}, status_code=500)

    return _json(payload)


async def cube_detail(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}` — apps running on one cube.

    Returns 404 when the caller cannot see the cube, which is the SAME response an
    unknown cube gets. That is deliberate: distinguishing "exists but not yours"
    from "does not exist" would let anyone enumerate the fleet's cube names, and the
    tenancy boundary is the point of this surface.

    Authorization is not re-checked here — `reads.cube_apps` resolves out of the
    already-RBAC-filtered environment set and returns None, so there is no access
    check at this layer for a future edit to forget or reorder.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.cube_apps(client, profile, cube)
    except ApolloError as e:
        logger.warning("console cube detail failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.exception("console cube detail errored for profile=%s", profile)
        return _json({"error": "Could not read the cube."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube."}, status_code=404)
    if payload.get("not_found"):
        # Still a 404 with the SAME message — the response must not reveal whether
        # the cube exists. The extra flag says only that the CALLER's environment
        # list is truncated, which is a property of their own list rather than of any
        # cube, so the page can stop blaming their Apollo roles without leaking.
        return _json(
            {"error": "No such cube.", "environments_truncated": True}, status_code=404
        )
    return _json(payload)


async def cube_services(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/services` — the Service ports on one cube.

    **The only console read backed by kubectl rather than Apollo.** The cube page
    fetches it on load as its own request, beside the apps list rather than inside it,
    so a slow or unreachable cube never holds the apps back; `reads.cube_services`
    caches it per (profile, cube). A tbot or kubectl failure comes back as a populated
    `error` with an empty candidate set rather than a 5xx, because "no services" and
    "could not look" must stay distinguishable — the page must never mark a port "Not
    exposed" when it could not read the ports.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.cube_services(client, profile, cube)
    except ApolloError as e:
        logger.warning("console services read failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.exception("console services read errored for profile=%s", profile)
        return _json({"error": "Could not read the cube's services."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube."}, status_code=404)
    return _json(payload)


async def cube_inventory(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/inventory` — the inventory identity fields.

    Its own endpoint rather than a field on `cube_detail`, because
    `/inventory/lookup` is a server-side partition scan (~3.3s cold, measured against
    prod) and folding it into the detail payload would hold the apps list — the page's
    primary content — behind a secondary panel. Same shape as `cube_services`.

    Authorization is not re-checked here: `reads.cube_inventory` resolves the cube out
    of the already-RBAC-filtered environment set and returns None otherwise, so a
    caller can only ever cause an inventory lookup for a cube they can already see.
    That is the tenancy boundary for this feature, since a read-capable inventory
    credential sees the whole fleet.

    A 5xx is deliberately NOT raised for an inventory failure — `reads.cube_inventory`
    reports it as `inventory_source.available = false` and the panel says so, because
    Apollo is the authority for whether a cube exists and an inventory outage must not
    look like a missing cube.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.cube_inventory(client, profile, cube)
    except ApolloError as e:
        logger.warning("console inventory read failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.exception("console inventory read errored for profile=%s", profile)
        return _json({"error": "Could not read the cube."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube."}, status_code=404)
    if payload.get("not_found"):
        # Same message and status as above — the response must not reveal whether the
        # cube exists. See `cube_detail` for the full reasoning.
        return _json(
            {"error": "No such cube.", "environments_truncated": True}, status_code=404
        )
    return _json(payload)


async def cube_gps(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/gps` — where the cube's router last reported its
    GPS position.

    Its own endpoint for the reason `/inventory` has one: a different upstream
    (InControl2) with its own latency and its own outages, which nothing else on the
    page should wait on. Authorization is `reads.cube_gps`'s, the same as
    `cube_inventory`'s: an invisible cube is a 404 before inventory or IC2 is asked
    anything. An IC2 or inventory failure is a 200 with `state: "unavailable"`, never
    a 5xx.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.cube_gps(client, profile, cube)
    except ApolloError as e:
        logger.warning("console gps read failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.exception("console gps read errored for profile=%s", profile)
        return _json({"error": "Could not read the cube."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube."}, status_code=404)
    if payload.get("not_found"):
        # Same message and status as above, so the response can't reveal whether the
        # cube exists. See `cube_detail`.
        return _json(
            {"error": "No such cube.", "environments_truncated": True}, status_code=404
        )
    return _json(payload)


async def cube_exposed(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/exposed` — just the exposed apps.

    Exists to be polled: after a `pending` unexpose the UI resolves the outcome
    itself rather than asking the user to refresh. TWO Apollo queries, gathered — the
    module read cannot say whether the cube has stopped serving a removed app, which
    is the whole reason this is polled. (It was one before the rollout signal was
    added; three comments claimed it still was.)
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.cube_exposed(client, profile, cube)
    except ApolloError as e:
        logger.warning("console exposed read failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.exception("console exposed read errored for profile=%s", profile)
        return _json({"error": "Could not read the cube."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube."}, status_code=404)
    return _json(payload)


async def cube_changes(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/changes` — "last changed" per app.

    The most recent successful Apollo plan per entity. Its own endpoint rather than a
    field on `cube_detail` so the plan query — which `CONSOLE_ENVIRONMENT_ENTITIES`
    deliberately omits as "by far the largest part of the entity payload" — cannot
    delay the apps list it decorates.

    Authorization is not re-checked here: `reads.cube_changes` resolves the cube out
    of the already-RBAC-filtered environment set and returns None otherwise.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.cube_changes(client, profile, cube)
    except ApolloError as e:
        logger.warning("console changes failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.exception("console changes errored for profile=%s", profile)
        return _json({"error": "Could not read the cube."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube."}, status_code=404)
    if payload.get("not_found"):
        return _json(
            {"error": "No such cube.", "environments_truncated": True}, status_code=404
        )
    return _json(payload)


async def cube_status(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/status` — online / offline / unknown.

    Derived from the freshness of the newest Groundcover log for the cube. See
    `reads.cube_status` for why that signal was chosen over Apollo's `healthStatus`
    (no timestamp) and over plan activity (only advances when there is a plan).

    Its own endpoint, fetched alongside the cube detail, for the same reason the
    inventory read is: it is a different upstream with its own latency, and the apps
    list must not wait on it.

    **A Groundcover failure is a 200 with `state: "unknown"`, not a 5xx.** The badge
    is secondary content and Apollo decides whether the cube exists, so an
    observability outage must not make a working cube look broken — and it must not
    render as "offline" either, which would be a claim rather than an absence.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")

    threshold = max(1, int(settings.console_cube_online_threshold_seconds))
    unknown = {
        "cube": cube, "state": "unknown", "last_seen": None, "age_seconds": None,
        "reason": "unavailable", "threshold_seconds": threshold,
        "window_minutes": None,
    }

    try:
        # Process-lifetime singleton, not entered/exited per request.
        registry = groundcover.groundcover_registry()
    except Exception:
        # A stack with no Groundcover credentials is a supported deployment; the
        # badge reports unknown rather than the route 503ing, because unlike the logs
        # view this is not the thing the user asked to see.
        #
        # `registry = None` rather than an early return: `reads.cube_status` still has
        # to resolve the cube out of the caller's RBAC-filtered set first, so this
        # route answers 404 for a cube they cannot see whether or not Groundcover is
        # configured. Returning `unknown` here skipped that resolve entirely, which
        # answered 200 for ANY cube name on a stack with no Groundcover credentials.
        # Not a leak — the payload is identical for every name and echoes only the
        # caller's own input — but it made this the one console read where
        # authorization did not come first, which is not a property to leave lying
        # around for the next edit to build on.
        logger.warning("console status: no Groundcover client on this deployment")
        registry = None

    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.cube_status(client, registry, profile, cube)
    except ApolloError as e:
        logger.warning("console status failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.exception("console status errored for profile=%s", profile)
        return _json({"error": "Could not read the cube."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube."}, status_code=404)
    return _json(payload)


async def cube_teleport(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/teleport` — Teleport connectivity for one cube.

    The third reachability chip on the cube page. Its own endpoint, fetched alongside
    the detail, for the same reason `/status` and `/inventory` are: a different
    upstream with its own latency — here a `tsh` subprocess — which the apps list must
    not wait on.

    **A Teleport failure is a 200 with `state: "unknown"`, not a 5xx**, matching
    `/status`. The chip is secondary content, Apollo decides whether the cube exists,
    and an unreachable `tsh` must not render as "Disconnected" — that would be a claim
    about the cube rather than about our own reach.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")

    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.cube_teleport(client, profile, cube)
    except ApolloError as e:
        logger.warning("console teleport failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.exception("console teleport errored for profile=%s", profile)
        return _json({"error": "Could not read the cube."}, status_code=500)

    if payload is None:
        # Same body and status as every other per-cube 404.
        return _json({"error": "No such cube."}, status_code=404)
    return _json(payload)


async def app_health(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/health?app=<entity>` — why one app has its status.

    The health checks behind the status on an app row (docs/console-spec.md §4.21),
    fetched when the user opens it. Read-only, so `guard_read`. `app` is the ENTITY
    name, resolved against the cube's own entity list — never an entity id, which
    Apollo resolves fleet-wide.

    A failed check read is a 200 with `state: "unavailable"` (the row already shows
    the status; this is detail), while a failed Apollo read of the cube itself is the
    usual 502. A 404 means "no such cube, or no such app on it".
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    app = (request.query_params.get("app") or "").strip()
    if not app:
        return _json({"error": "Query parameter 'app' is required."}, status_code=400)

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.app_health(client, profile, cube, app)
    except ApolloError as e:
        # Class name only — unlike its siblings, this read's failure text could
        # carry a check's raw `params` (internal hosts and database names).
        logger.warning(
            "console app health failed for profile=%s: %s", profile, type(e).__name__
        )
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.error("console app health errored for profile=%s", profile)
        return _json({"error": "Could not read the app's health."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube or app."}, status_code=404)
    return _json(payload)


async def cube_ai(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/ai` — the AI Reactor catalog and this cube's state.

    Read-only, so `guard_read`, and it never repairs what it finds out of sync: a GET
    must not change state (console rule 1a). 404 when the AI tab is off, exactly as if
    the route did not exist. A failed read of the GATEWAY's config is reported in the
    payload (`gateway.status: "unknown"`); a failed read of the cube's entity list is the
    usual 502.
    """
    if not ai_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.cube_ai(client, profile, cube)
    except ApolloError as e:
        # Class only: this read selects a gateway's declared config.
        logger.warning("console ai read failed for profile=%s: %s", profile, type(e).__name__)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception as e:
        logger.error("console ai read errored for profile=%s (%s)", profile, type(e).__name__)
        return _json({"error": "Could not read the cube's AI models."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube."}, status_code=404)
    return _json(payload)


async def cube_logs(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/logs?app=<entity>` — recent logs for one app.

    Read-only, so `guard_read` rather than `guard_write`. Backed by
    `groundcover_search_logs`'s own client and authorization, not a new path to
    Groundcover: the API key is workspace-scoped and sees the whole fleet, so the
    tenancy check has to be the one the MCP tool uses.

    A 404 here means "no such cube, or no such app on it" — the same
    non-enumerable answer `cube_detail` gives, for the same reason.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    app = request.query_params.get("app") or ""
    if not app.strip():
        return _json({"error": "Query parameter 'app' is required."}, status_code=400)
    app = app.strip()

    raw_limit = request.query_params.get("limit") or ""
    limit = reads.LOG_LIMIT_DEFAULT
    if raw_limit:
        try:
            limit = int(raw_limit)
        except ValueError:
            return _json({"error": "'limit' must be an integer."}, status_code=400)

    since, since_err = reads.parse_since(request.query_params.get("since") or "")
    if since_err:
        return _json({"error": since_err}, status_code=400)

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        # Built before any Apollo/Groundcover use so a missing/unreadable API key
        # is a clean 503 rather than a 500 — the console is deployable on a stack
        # that has no Groundcover credentials, and the UI should say so. Unlike
        # the old single client, the registry is a process-lifetime singleton
        # (tools/groundcover.py) — it is NOT entered/exited per request; only the
        # ApolloClient below is request-scoped.
        registry = groundcover.groundcover_registry()
    except Exception:
        logger.exception("console logs: could not build a Groundcover client")
        return _json(
            {"error": "Log search is not configured on this deployment."},
            status_code=503,
        )

    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            # `reads.cube_logs` does its own Apollo/Groundcover authorization
            # (see its docstring); resolving a backend here is routing, not a
            # security check. A cube absent from every backend (or not yet in
            # the cache) falls back to whichever backend is first in the
            # registry, so the existing "no workloads" soft-fail path handles
            # it exactly as it did back when there was only one backend.
            backend_id = await registry.resolve_backend(cube)
            gc = registry.clients[backend_id or next(iter(registry.clients))]
            payload = await reads.cube_logs(
                client, gc, profile, cube, app, limit, since=since
            )
    except ApolloError as e:
        logger.warning("console logs failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.exception("console logs errored for profile=%s", profile)
        return _json({"error": "Could not read logs."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube or app."}, status_code=404)
    return _json(payload)


async def cube_utilization(request: Request, cube: str) -> Response:
    """`GET /console/api/cubes/{name}/utilization?window=1h|6h|24h` — resource graphs.

    Cube-wide CPU / memory / filesystem / volume utilization (docs/console-spec.md
    §4.18). Read-only, so `guard_read` rather than `guard_write`, and backed by
    `reads.cube_utilization`'s own Apollo + Groundcover authorization pair rather than a
    new path to Groundcover.

    A missing registry is a **503 here and a degraded 200 in `cube_status`**, and the
    difference is deliberate: the graphs ARE what the user asked to see, so a stack with
    no Groundcover credentials should say so rather than render four empty panels. The
    badge is secondary content, which is why it degrades instead. Per-metric failures
    still degrade to a panel-level `unavailable` inside a 200.

    Note this endpoint takes `?window=` from an enumerated set while the sibling `/logs`
    takes an RFC3339 `?since=`. Two vocabularies for "how far back", on purpose: a window
    here has to map to a query step, which a free timestamp cannot do.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_read(request)) is not None:
        return blocked

    window = request.query_params.get("window") or utilization.DEFAULT_WINDOW
    if utilization.resolve_window(window) is None:
        # Validated BEFORE Apollo is dialled, so a bad parameter costs no upstream call.
        # The allowed set is named rather than hinted — this is an enumerated-args
        # surface, so there is nothing to discover by probing.
        allowed = ", ".join(utilization.WINDOWS)
        return _json({"error": f"'window' must be one of: {allowed}."}, status_code=400)

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        # Built before any Apollo/Groundcover use so a missing key is a clean 503 rather
        # than a 500. Process-lifetime singleton — not entered/exited per request.
        registry = groundcover.groundcover_registry()
    except Exception:
        logger.warning("console utilization: no Groundcover client on this deployment")
        return _json(
            {"error": "Resource metrics are not configured on this deployment."},
            status_code=503,
        )

    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await reads.cube_utilization(
                client, registry, profile, cube, window
            )
    except ApolloError as e:
        logger.warning("console utilization failed for profile=%s: %s", profile, e)
        return _json({"error": "Could not read the cube from Apollo."}, status_code=502)
    except Exception:
        logger.exception("console utilization errored for profile=%s", profile)
        return _json({"error": "Could not read resource metrics."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube."}, status_code=404)
    return _json(payload)


def _optional_company(body: dict) -> tuple[str | None, Response | None]:
    """The optional `company` field -> (value, error response). Absent or "" = home.

    Only the SHAPE is checked here; whether the caller holds it is decided by
    `writes`, through the same rule the MCP tools use. A baseline ("map") stack takes no
    `company` at all: the page never sends one there, and the tool would write an admin's
    value verbatim as a label, so an un-enumerated field is refused outright rather than
    carried to it (console rule 2).
    """
    company = body.get("company")
    if company is None or company == "":
        return None, None
    if not reads_stored_sets():
        return None, _json({"error": "Field 'company' is not accepted on this stack."}, status_code=400)
    if not isinstance(company, str) or len(company) > 63:
        return None, _json({"error": "Field 'company' must be a short string."}, status_code=400)
    return company.strip(), None


async def expose_app(request: Request, cube: str) -> Response:
    """`POST /console/api/cubes/{name}/expose` — publish one in-cluster service.

    Same gate order as unexpose — `is_enabled()`, `guard_write()`, body validation,
    then any cube contact — so a cross-site or token-less attempt costs nothing and
    reaches neither Apollo nor kubectl.

    `uri` is required and must be one the console enumerated; `writes.expose_app`
    checks it against `cube_services`, which is what keeps this an enumerated-args
    surface rather than a thin proxy for the tool (AGENTS.md console rule 2).
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_write(request)) is not None:
        return blocked

    try:
        body = await request.json()
    except Exception:
        return _json({"error": "Expected a JSON body."}, status_code=400)
    if not isinstance(body, dict):
        return _json({"error": "Expected a JSON object."}, status_code=400)

    app_name = body.get("app")
    app_uri = body.get("uri")
    if not isinstance(app_name, str) or not app_name.strip():
        return _json({"error": "Field 'app' is required."}, status_code=400)
    if not isinstance(app_uri, str) or not app_uri.strip():
        return _json({"error": "Field 'uri' is required."}, status_code=400)
    app_name, app_uri = app_name.strip(), app_uri.strip()

    # Two NAMED optional fields, not a header list. The console stays an
    # enumerated-args surface because its field set is fixed here (AGENTS.md
    # console rule 2); only the values are free text, and `writes.expose_app`
    # runs the MCP tool's own validator over what it composes, so the console
    # cannot emit a header the tool would reject.
    rewrite_host = body.get("rewrite_host")
    rewrite_origin = body.get("rewrite_origin")
    for field, value in (("rewrite_host", rewrite_host), ("rewrite_origin", rewrite_origin)):
        if value is not None and not isinstance(value, str):
            return _json({"error": f"Field '{field}' must be a string."}, status_code=400)
    rewrite_host = (rewrite_host or "").strip()
    rewrite_origin = (rewrite_origin or "").strip()
    company, company_err = _optional_company(body)
    if company_err:
        return company_err

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await writes.expose_app(
                client, profile, cube, app_name, app_uri,
                rewrite_host=rewrite_host, rewrite_origin=rewrite_origin, company=company,
            )
    except ApolloError as e:
        _log_write_failure("expose", profile, cube, e)
        return _json({"error": "Apollo rejected the change."}, status_code=502)
    except Exception as e:
        _log_write_failure("expose", profile, cube, e)
        return _json({"error": "Could not apply the change."}, status_code=500)

    if payload is None:
        # Same body and status as every other per-cube 404.
        return _json({"error": "No such cube."}, status_code=404)
    return _json(payload)


async def unexpose_app(request: Request, cube: str) -> Response:
    """`POST /console/api/cubes/{name}/unexpose` — stop publishing one app.

    The only mutating console route. Ordered deliberately:

    1. `is_enabled()` — a stack with the console off must not expose a write at all.
    2. `guard_write()` — origin + CSRF, BEFORE the body is read and before any Apollo
       work, so a cross-site attempt costs nothing and touches no cube.
    3. body validation — `app` must be a non-empty string; nothing is inferred.
    4. `writes.unexpose_app` — which resolves authorization out of the RBAC-filtered
       environment set and returns None for a cube the caller cannot see, giving the
       same 404 `cube_detail` gives so the fleet stays non-enumerable.

    A refused write returns 200 with `ok: false` rather than a 4xx: the request was
    well-formed and authorized, and the outcome ("that app is not yours to manage")
    is data the UI renders inline. Auth failures above still return 403/404.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_write(request)) is not None:
        return blocked

    try:
        body = await request.json()
    except Exception:
        return _json({"error": "Expected a JSON body."}, status_code=400)
    if not isinstance(body, dict):
        return _json({"error": "Expected a JSON object."}, status_code=400)
    app_name = body.get("app")
    if not isinstance(app_name, str) or not app_name.strip():
        return _json({"error": "Field 'app' is required."}, status_code=400)
    app_name = app_name.strip()
    company, company_err = _optional_company(body)
    if company_err:
        return company_err

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            payload = await writes.unexpose_app(client, profile, cube, app_name, company=company)
    except ApolloError as e:
        _log_write_failure("unexpose", profile, cube, e)
        return _json({"error": "Apollo rejected the change."}, status_code=502)
    except Exception as e:
        _log_write_failure("unexpose", profile, cube, e)
        return _json({"error": "Could not apply the change."}, status_code=500)

    if payload is None:
        # Same body and status as cube_detail's — see that handler.
        return _json({"error": "No such cube."}, status_code=404)
    return _json(payload)


_AI_MODEL_ID_MAX_CHARS = 64


def _ai_model_field(body: dict, field: str, required: bool) -> tuple[str | None, Response | None]:
    """A model id from the body: shape only. Membership in the catalog is checked by
    `reactor.service`, which refuses anything the catalog does not list."""
    value = body.get(field)
    if value is None or value == "":
        if required:
            return None, _json({"error": f"Field '{field}' is required."}, status_code=400)
        return None, None
    if not isinstance(value, str) or len(value) > _AI_MODEL_ID_MAX_CHARS:
        return None, _json({"error": f"Field '{field}' must be a model id."}, status_code=400)
    return value.strip(), None


async def _ai_write(request: Request, cube: str, action: str) -> Response:
    """Shared body of the two AI write routes. Gate order as for expose/unexpose:
    the AI flag, then `guard_write` BEFORE the body is read or Apollo is dialed."""
    if not ai_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_write(request)) is not None:
        return blocked

    try:
        body = await request.json()
    except Exception:
        return _json({"error": "Expected a JSON body."}, status_code=400)
    if not isinstance(body, dict):
        return _json({"error": "Expected a JSON object."}, status_code=400)
    model_id, err = _ai_model_field(body, "model", required=True)
    if err:
        return err
    replace = None
    if action == "deploy":
        replace, err = _ai_model_field(body, "replace", required=False)
        if err:
            return err

    state = request.state
    profile = getattr(state, "profile", "?")
    try:
        async with ApolloClient(
            state.apollo_client_id, state.apollo_client_secret
        ) as client:
            if action == "deploy":
                payload = await writes.ai_deploy(client, profile, cube, model_id, replace)
            else:
                payload = await writes.ai_remove(client, profile, cube, model_id)
    except ApolloError as e:
        _log_write_failure(f"ai {action}", profile, cube, e)
        return _json({"error": "Apollo rejected the change."}, status_code=502)
    except Exception as e:
        _log_write_failure(f"ai {action}", profile, cube, e)
        return _json({"error": "Could not apply the change."}, status_code=500)

    if payload is None:
        return _json({"error": "No such cube."}, status_code=404)
    return _json(payload)


async def ai_deploy(request: Request, cube: str) -> Response:
    """`POST /console/api/cubes/{name}/ai/deploy` — body `{model, replace?}`.

    A refused or partial deploy is a 200 with `ok: false`: the request was well-formed
    and authorized, and the outcome is data the AI tab renders. `model` must be a
    catalog id (console rule 2: enumerated arguments, never a product id or a chart).
    """
    return await _ai_write(request, cube, "deploy")


async def ai_remove(request: Request, cube: str) -> Response:
    """`POST /console/api/cubes/{name}/ai/remove` — body `{model}`. Only a model the
    console deployed (its gateway entry carries the Edgeport marker) can be removed."""
    return await _ai_write(request, cube, "remove")


async def submit_feedback(request: Request) -> Response:
    """`POST /console/api/feedback` — file a support request or a feature request.

    Two destinations behind one route: `support` files a Freshservice ticket,
    `feature` raises a customer request on the Jira CF board. `writes.submit_feedback`
    holds the dispatch and explains why they are different systems. Kept as ONE route
    because the console's mutating surface is a fixed set and the route tests fail
    when that set changes.

    Much thinner than expose/unexpose: there is no cube to resolve, no RBAC to
    check, and no Apollo/kubectl I/O — `cube` is optional free-text context here,
    exactly as it is for the MCP `submit_feedback` tool. The gate order is the
    same as every other mutating route regardless: `is_enabled()`, then
    `guard_write()` before the body is even read.

    **There is no email field, and there must never be one.** The reporter is
    resolved server-side by `tools.feedback.submit_feedback_from_console` from the
    authenticated cookie's key — the same identity-resolution `_submitter_email`
    already does for the Bearer-key MCP path — so accepting a caller-supplied
    address here would reopen exactly the spoofing the tool module's design
    closes off (see `feedback.py::_submitter_email`).

    **Why this sets `current_request` itself.** `_submitter_email` (and the
    context block it stamps into the ticket body) read `request.state` through
    the `current_request` contextvar, not a parameter — that is what lets a tool
    handler resolve identity without MCP dispatch passing `Request` explicitly.
    The contextvar is normally set by `main.py::mcp_asgi_with_context`, an ASGI
    wrapper around `/mcp` only; a console route reaches this function through a
    plain Starlette handler that never passes through it. `request.state` is
    populated identically either way by `APIKeyMiddleware` (`key_description`,
    `profile`, `actor_type`), so setting the same contextvar here for the
    duration of the call reproduces exactly what the MCP path does, rather than
    threading a second parameter through `feedback.py` for one caller.

    Unlike expose/unexpose, a `FeedbackError` here is not a tenancy concern — the
    message is the upstream's own (a stale field id, a 401) and already deemed safe
    to hand to an MCP caller verbatim, so it is safe to hand to the browser too.
    That holds because the two credential-loading paths take themselves out of it:
    `feedback._misconfigured` / `freshservice._misconfigured` log the operator detail
    and raise a submitter-facing message naming no infrastructure. Without them this
    body published a Secrets Manager id to whoever filed the form — and the
    `logger.warning` below put it in CloudWatch as well. It is still not a 200 with
    `ok: false`: there is no
    partial/pending state to model the way expose/unexpose have one, so a failure
    is a plain non-2xx `{"error": ...}` like every read route uses.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if (blocked := guard_write(request)) is not None:
        return blocked

    try:
        body = await request.json()
    except Exception:
        return _json({"error": "Expected a JSON body."}, status_code=400)
    if not isinstance(body, dict):
        return _json({"error": "Expected a JSON object."}, status_code=400)

    feedback_type = body.get("feedback_type")
    # The CONSOLE's set, not the Jira module's: `support` goes to Freshservice and
    # `feature` to the CF board. `feedback_tool.FEEDBACK_TYPES` still governs the MCP
    # tool, which did not change.
    if feedback_type not in writes.CONSOLE_FEEDBACK_TYPES:
        return _json(
            {"error": "Field 'feedback_type' must be one of: "
                      f"{', '.join(writes.CONSOLE_FEEDBACK_TYPES)}."},
            status_code=400,
        )

    summary = body.get("summary")
    details = body.get("details")
    business_impact = body.get("business_impact")
    cube = body.get("cube")
    if not isinstance(summary, str) or not summary.strip():
        return _json({"error": "Field 'summary' is required."}, status_code=400)
    if not isinstance(details, str) or not details.strip():
        return _json({"error": "Field 'details' is required."}, status_code=400)
    # Required for a FEATURE request, optional for support — the same line the MCP
    # tool's schema already drew, and the two surfaces disagreeing about one field was
    # the defect. "Who is blocked and what does it cost" is how a backlog gets ordered,
    # so it is fair to ask of a roadmap request; in front of a question it is pure
    # friction, and the person asking is the one least able to answer it.
    if feedback_type == writes.SUPPORT_TYPE:
        if business_impact is not None and not isinstance(business_impact, str):
            return _json(
                {"error": "Field 'business_impact' must be a string."}, status_code=400
            )
        business_impact = business_impact or ""
    elif not isinstance(business_impact, str) or not business_impact.strip():
        return _json({"error": "Field 'business_impact' is required."}, status_code=400)
    if cube is not None and not isinstance(cube, str):
        return _json({"error": "Field 'cube' must be a string."}, status_code=400)

    # Length limits, checked HERE rather than left to the upstream. Two reasons, and
    # the first is the one that bites: Freshservice caps `subject` at 255, so an
    # over-long summary comes back as a 400 that `_explain_failure` misdiagnoses to
    # the submitter as "its required fields have changed" — pointing at a stale field
    # contract when the actual problem is the text they just typed. Refusing it here
    # says which field and what the limit is, which is something they can act on.
    #
    # The second is that this route writes into a live helpdesk queue that dev and
    # prod SHARE, so an unbounded body is a way to make a real ticket unusable. This
    # is not a rate limit and is not pretending to be one — see the note below.
    for field, value, limit in (
        ("summary", summary, SUMMARY_MAX_CHARS),
        ("details", details, BODY_MAX_CHARS),
        ("business_impact", business_impact, BODY_MAX_CHARS),
        ("cube", cube or "", CUBE_MAX_CHARS),
    ):
        if len(value) > limit:
            return _json(
                {"error": f"Field '{field}' is too long (limit {limit} characters)."},
                status_code=400,
            )

    profile = getattr(request.state, "profile", "?")
    # See the docstring: this is what lets `_submitter_email` resolve the
    # caller's identity from `request.state` the same way it does on the MCP
    # path, without a second request-threading mechanism in feedback.py.
    token = current_request.set(request)
    try:
        result = await writes.submit_feedback(
            profile,
            feedback_type,
            summary.strip(),
            details.strip(),
            business_impact.strip(),
            (cube or "").strip() or None,
        )
    except (feedback_tool.FeedbackError, freshservice_tool.FreshserviceError) as e:
        # Both messages are authored to be shown to the submitter — a stale field id, a
        # rejected credential, a 400 naming the field the upstream refused. Collapsing
        # them into "submission failed" would discard the only diagnostic either
        # credential can produce, since neither can introspect its own schema.
        logger.warning("console feedback failed for profile=%s: %s", profile, e)
        return _json({"error": str(e)}, status_code=502)
    except Exception:
        logger.exception("console feedback errored for profile=%s", profile)
        return _json({"error": "Could not submit feedback."}, status_code=500)
    finally:
        current_request.reset(token)

    return _json({"ticket_key": result})


# The guide's complete asset set. An explicit allowlist rather than
# `_asset_response`'s containment check, because unlike Vite's open set of
# content-hashed bundles this set is CLOSED — `scripts/vendor-field-guide.py`
# emits exactly these two. Matching literal basenames means the served path is
# never built from request input, so there is no traversal surface to contain.
_GUIDE_ASSETS = frozenset({"guide.css", "guide.js"})


async def guide_shell(request: Request) -> Response:
    """`GET /console/guide` — the Cube Field Guide (spec §4.11).

    Gated in the same order as `shell()`: `is_enabled()` first (so an off-console
    404s before anything else runs), then the same-origin check with navigation
    allowed, because opening the guide from a bookmark is the normal case.

    Absent in a plain checkout, exactly like the SPA bundle. It 404s rather than
    borrowing `_PLACEHOLDER_SHELL`: the placeholder tells a developer how to build
    the console, and a missing guide is not a broken console.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if not _same_origin(request, allow_navigation=True):
        return _json({"error": "Cross-site request refused."}, status_code=403)

    if not GUIDE_INDEX.is_file():
        logger.warning(
            "field guide requested but %s is missing. Run "
            "scripts/vendor-field-guide.py, then the SPA build.", GUIDE_INDEX,
        )
        return Response("Not found.", status_code=404, media_type="text/plain")

    return FileResponse(GUIDE_INDEX, media_type="text/html", headers=_guide_headers())


async def guide_asset(request: Request, name: str) -> Response:
    """`GET /console/guide/{name}` — the guide's stylesheet and script.

    Filenames are fixed rather than content-hashed, so `_guide_headers`' 600s
    private cache is the whole cache-busting story: after the guide is edited and
    deployed, a browser may serve the previous pair for up to ten minutes.
    Harmless — the guide is one self-contained document, so a stale cache renders
    the previous revision of it rather than a mismatched half. Worth knowing when
    checking an edit on the dev stack: a hard reload, or you are reading the
    version from before your change.

    `allow_navigation=True` matches how the SPA's own assets are gated (they reach
    `_asset_response` through `shell()`, which passes True), so console assets have
    one behaviour rather than two. It also matters more here than there: the guide
    document sends `Referrer-Policy: no-referrer`, so its subresource requests
    carry no `Origin` and no `Referer` — on a browser old enough to omit
    `Sec-Fetch-Site` too, the stricter setting would 403 the stylesheet and script
    and serve an empty page. Nothing is given away either way: both files are
    static, identical for every caller, and carry no tenant data.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if not _same_origin(request, allow_navigation=True):
        return _json({"error": "Cross-site request refused."}, status_code=403)

    if name not in _GUIDE_ASSETS:
        return Response("Not found.", status_code=404, media_type="text/plain")

    candidate = GUIDE_DIR / name
    if not candidate.is_file():
        return Response("Not found.", status_code=404, media_type="text/plain")

    return FileResponse(candidate, headers=_guide_headers())


async def map_outline(request: Request) -> Response:
    """`GET /console/map/outline.json` — the fleet map's border outline.

    Static, public-domain data, identical for every caller and carrying no tenant data,
    fetched by the landing page only when a viewer opens its map. Gated like the guide's
    assets: `is_enabled()` first, then the same-origin check with navigation allowed.

    One literal path, never built from request input, so there is nothing to traverse.
    The filename carries no content hash, so the cache is private and bounded rather than
    Vite's year-long `immutable`: after a rebuild a browser may draw the previous outline
    for up to an hour, which is harmless.

    Absent in a plain checkout (the static tree is built, never committed), and a 404
    then is the map's "outline missing" case: it draws its dots on a blank background.
    """
    if not is_enabled():
        return _disabled_response(request.url.path)
    if not _same_origin(request, allow_navigation=True):
        return _json({"error": "Cross-site request refused."}, status_code=403)

    if not MAP_OUTLINE.is_file():
        logger.warning(
            "map outline requested but %s is missing. Build it with "
            "scripts/build-map-outline.py, then the SPA build.", MAP_OUTLINE,
        )
        return Response("Not found.", status_code=404, media_type="text/plain")

    return FileResponse(
        MAP_OUTLINE,
        media_type="application/json",
        headers={
            "Cache-Control": "private, max-age=3600",
            "X-Content-Type-Options": "nosniff",
        },
    )


async def shell(request: Request) -> Response:
    """Serve the SPA shell for `/console` and any `/console/...` deep link.

    Returning the same document for every path is what makes a deep link like
    `/console/cubes/lear-hammond-2` bookmarkable: the server hands back the
    shell and the client router resolves the path.

    An unmatched `/console/api/...` path must NOT get HTML — the SPA's fetch
    would parse it as JSON and fail confusingly — so those 404 as JSON.
    """
    path = request.url.path
    if not is_enabled():
        return _disabled_response(path)
    if path.startswith(f"{session_cookie.CONSOLE_PREFIX}/api/"):
        return _json({"error": f"No such console endpoint: {path}"}, status_code=404)

    if not _same_origin(request, allow_navigation=True):
        return _json({"error": "Cross-site request refused."}, status_code=403)

    if (asset := _asset_response(path)) is not None:
        return asset

    if INDEX_HTML.is_file():
        # no-store: the shell is per-session-authenticated, and a cached copy
        # served after logout would render a signed-out frame.
        return FileResponse(
            INDEX_HTML,
            media_type="text/html",
            headers=_shell_headers(),
        )

    logger.warning(
        "console shell requested but %s is missing — serving the placeholder. "
        "Run the SPA build (npm ci && npm run build in console/web).", INDEX_HTML,
    )
    return Response(
        _PLACEHOLDER_SHELL,
        media_type="text/html",
        # The placeholder's own <style> block needs inline styles, unlike the built
        # SPA — hence the relaxation. It ships no script at all.
        headers=_shell_headers(allow_inline_style=True),
    )


# Served when the SPA bundle is absent: a plain checkout, or a container built
# without the node stage. Deliberately honest rather than blank, so the failure
# is diagnosable in a browser instead of looking like a routing bug.
_PLACEHOLDER_SHELL = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Edgeport Console</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
         background: #1a1a1a; color: #F5F4F0; display: flex; min-height: 100vh;
         align-items: center; justify-content: center; margin: 0; }
  .card { max-width: 30rem; padding: 2rem; border: 1px solid #2e2e2e; border-radius: 12px; }
  h1 { font-size: 1.25rem; font-weight: 600; margin: 0 0 .75rem; }
  p { color: #BEBCBE; font-size: .875rem; line-height: 1.6; margin: 0 0 .5rem; }
  code { color: #93aafe; }
</style></head>
<body><div class="card">
  <h1>Console assets not built</h1>
  <p>You are authenticated — the console shell is served, but the SPA bundle is
     missing from this deployment.</p>
  <p>Build it with <code>npm ci &amp;&amp; npm run build</code> in
     <code>console/web</code>, or rebuild the container image so the node stage runs.</p>
</div></body>
</html>"""
