"""FastAPI middleware for API key authentication."""

from __future__ import annotations

import hashlib
from urllib.parse import quote

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from cube_cloud.auth import api_keys, profiles, session_cookie
from cube_cloud.config import settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Validate API key on every request.

    The key may arrive two ways:
      * ``Authorization: Bearer <key>`` — accepted on every host. This is the
        MCP / agent path and is the ONLY accepted form on ``/mcp`` + ``/tunnel``.
      * a parent-domain session cookie — accepted on app-subdomain hosts (the
        browser app proxy front door) and, on the apex, ONLY under the explicit
        :data:`COOKIE_ALLOWED_APEX_PREFIXES` allowlist. The cookie is the
        browser path.

    **CSRF rule (browser-app-proxy-spec §4.2, as amended by
    docs/console-spec.md §4.2):** the session cookie is scoped to the parent
    domain, so the browser attaches it to apex ``/mcp`` + ``/tunnel`` requests
    too. Cookie-auth is therefore never honored on ``/mcp`` / ``/tunnel``
    regardless of cookie presence or host — that keeps the existing MCP surface
    Bearer-only, and it is the property the original rule exists to protect.

    The original rule stated this as "app-subdomain hosts only". The console
    (docs/console-spec.md) amends it to "app-subdomain hosts, plus an explicit
    apex prefix allowlist", because the threat the rule addresses is a property
    of ``/mcp`` — a *generic, mutating, single-endpoint* POST surface where a
    cross-site request could run ``install_entity`` or ``create_secret`` — not
    of the apex host itself. A closed, enumerable set of console routes does not
    inherit it. Note the allowlist is **narrower** than an app-subdomain host,
    which honors the cookie on every path and method except the two forbidden
    prefixes; the console gets one prefix.

    The allowlist must stay a literal tuple — never a wildcard or a regex.

    Populates request.state with:
      - profile: str (the profile name)
      - apollo_client_id: str
      - apollo_client_secret: str
      - session_key: str (hash of the credential; rate-limiter key)
      - key_id: str (stored API-key hash; tool-call analytics identity)
      - key_description: str (human label for the key)
      - user_domain: str | None (email domain of the key's owner, when known)
      - user_email_hash: str | None (SHA-256 of the owner's email, when known)
    """

    # Paths that skip auth (health checks, browser login/logout).
    #
    # An entry here MUST have a route registered for it. `/setup` used to be
    # listed and outlived its route by nothing but luck: an exempt path with no
    # route skips auth and falls through to the app-proxy catch-all with an empty
    # `request.state`, which on an app-subdomain host is an unauthenticated 500
    # (http_proxy reads `request.state.profile`), not a 404.
    # `/healthz` and `/ready` were listed here without ever having routes — the
    # ALB target group and the ECS container check both poll `/health` only
    # (infra/terraform/alb.tf, ecs.tf). They were the hazard above, not a spare
    # tire, so they are dropped rather than given routes. Add one back only
    # together with its route.
    EXEMPT_PATHS = {
        "/health",
        "/auth/login", "/auth/authenticate", "/auth/logout",
        # Self-service password reset. Exempt for the same reason as the rest of
        # this flow: they render for someone who has no credential — and in this
        # case cannot get one without them.
        "/auth/forgot", "/auth/reset",
    }
    EXEMPT_PREFIXES = ("/auth/session/", "/static/",)

    # Surfaces that must stay Bearer-only even on an app-subdomain host, no
    # matter that the parent-domain cookie is attached to them.
    COOKIE_FORBIDDEN_PREFIXES = ("/mcp", "/tunnel")

    # Apex paths where cookie-auth IS honored (docs/console-spec.md §4.2). A
    # literal tuple by design: adding a surface here widens the CSRF-reachable
    # set, so it must be an explicit, reviewable edit. COOKIE_FORBIDDEN_PREFIXES
    # is still checked first and always wins.
    #
    # Gated at request time by `settings.console_enabled` (see `_apex_cookie_prefixes`):
    # where the console is off, this list is empty and the apex stays Bearer-only
    # exactly as it was before the console existed.
    COOKIE_ALLOWED_APEX_PREFIXES = (session_cookie.CONSOLE_PREFIX,)

    @classmethod
    def _apex_cookie_prefixes(cls) -> tuple[str, ...]:
        """The live apex cookie-auth allowlist — empty when the console is off.

        Read per request rather than resolved at import so the flag is
        patchable in tests and so a stack that flips it needs only a restart.
        """
        return cls.COOKIE_ALLOWED_APEX_PREFIXES if settings.console_enabled else ()

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        host = request.url.hostname or ""
        # The exemptions are OUR paths on OUR hosts. On an app-subdomain host the
        # same path belongs to the proxied in-cube app — MinIO's console serves
        # its JS bundle from `/static/`, and an app may well have its own
        # `/auth/login` or `/health`. Those requests must authenticate like every
        # other app request and then be proxied.
        #
        # Exempting them there was doubly wrong. It let an unauthenticated caller
        # reach the app-proxy handler with an EMPTY `request.state`, which is the
        # unauthenticated-500 hazard documented on EXEMPT_PATHS above (http_proxy
        # reads `request.state.profile`) — the same trap `/healthz` and `/ready`
        # were removed for. And it meant cube-cloud answered those paths itself,
        # so the app never saw them.
        if not session_cookie.is_app_subdomain_host(host) and (
            path in self.EXEMPT_PATHS or path.startswith(self.EXEMPT_PREFIXES)
        ):
            return await call_next(request)

        # Cookie auth is permitted off the Bearer-only surfaces, and then only on
        # an app-subdomain host (the app proxy) or under an allowlisted apex
        # prefix (the console). This single flag also gates the browser
        # 302-to-login front door.
        cookie_allowed = not path.startswith(self.COOKIE_FORBIDDEN_PREFIXES) and (
            session_cookie.is_app_subdomain_host(host)
            or self._under_prefix(path, self._apex_cookie_prefixes())
        )

        # Bearer always wins; cookie is a fallback only where permitted.
        raw_key: str | None = None
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            raw_key = auth_header[7:]  # strip "Bearer "
        elif cookie_allowed:
            raw_key = request.cookies.get(session_cookie.SESSION_COOKIE_NAME)

        if not raw_key:
            return self._reject(request, cookie_allowed)

        item = await api_keys.validate_key(raw_key)
        if not item:
            return self._reject(request, cookie_allowed)

        profile_name = item["profile"]

        try:
            client_id, client_secret = profiles.get_credentials(profile_name)
        except ValueError as e:
            return JSONResponse(
                status_code=403,
                content={"error": str(e)},
            )

        request.state.profile = profile_name
        request.state.apollo_client_id = client_id
        request.state.apollo_client_secret = client_secret
        # Opaque per-session identifier for the app proxy's rate limiter
        # (browser_proxy/rate_limit.py) -- a hash so the raw credential never
        # sits in request.state longer than needed.
        request.state.session_key = hashlib.sha256(raw_key.encode()).hexdigest()[:16]
        # Identity for tool-call analytics ("by whom"). key_id is the stored
        # key hash — a stable, non-reversible per-key identifier.
        request.state.key_id = item.get("key_hash", "")
        request.state.key_description = item.get("description", "")
        request.state.user_domain = item.get("user_domain")
        request.state.user_email_hash = item.get("user_email_hash")
        # actor_type ('user'/'bot'/'test') + bot_name (service label) are derived from
        # the key here so every telemetry row is self-describing — no join back
        # to the keys table needed to separate people from service agents.
        request.state.actor_type, request.state.bot_name = api_keys.classify_actor(item)

        return await call_next(request)

    @staticmethod
    def _under_prefix(path: str, prefixes: tuple[str, ...]) -> bool:
        """Boundary-aware prefix match: exact, or a ``/``-separated descendant.

        A bare ``startswith`` would let ``/consolefoo`` match ``/console`` and so
        widen cookie-auth onto a path the allowlist never named — the same
        prefix-spoof class that ``is_app_subdomain_host`` guards against with its
        leading-label requirement.

        Deliberately NOT used for ``COOKIE_FORBIDDEN_PREFIXES``: on the deny
        side, matching *more* broadly is the fail-safe direction, so that list
        keeps its plain ``startswith``.
        """
        return any(path == p or path.startswith(p + "/") for p in prefixes)

    def _reject(self, request: Request, cookie_allowed: bool):
        """Fail closed (spec §4.4).

        On a gated host a browser navigation is bounced to the centralized apex
        login with a validated ``next``; everything else (API clients, the apex
        MCP surface) gets a 401.
        """
        if cookie_allowed and self._wants_html(request):
            return RedirectResponse(self._login_url(request), status_code=302)
        return JSONResponse(
            status_code=401,
            content={"error": "Missing or invalid credentials. Expected: Bearer <api-key>"},
        )

    @staticmethod
    def _wants_html(request: Request) -> bool:
        return "text/html" in request.headers.get("accept", "")

    @classmethod
    def _login_url(cls, request: Request) -> str:
        """Apex login URL carrying the originally-requested target as ``next``.

        Two shapes, matching the two accepted by
        :func:`session_cookie.validate_next`:

        * a **console** path is carried as-is, relative — no host component, so
          nothing to spoof, and it survives the guard on the receiving end;
        * an **app-subdomain** request is rebuilt as an explicit ``https://``
          URL on the request's own (already app-subdomain-validated) host.

        This is what makes a console deep link bookmarkable while signed out:
        the bounce round-trips through login and lands back on the same page.
        """
        host = request.url.hostname or ""
        path = request.url.path
        # The relative form is ONLY correct for an apex console request. Two gates,
        # both load-bearing:
        #   * the host must not be an app subdomain — otherwise an in-cube app
        #     serving anything under /console would get a host-less `next` and the
        #     user would land on the apex console instead of back in their app
        #     (and, where console_enabled is false, on a bare 401);
        #   * `_apex_cookie_prefixes()` rather than the raw tuple or a bare
        #     `startswith`, so this agrees exactly with the gate in `dispatch` —
        #     including going inert when the console is disabled, and rejecting
        #     `/consolefoo`, which would otherwise produce a `next` that
        #     `validate_next` then refuses, stranding the login.
        if not session_cookie.is_app_subdomain_host(host) and cls._under_prefix(
            path, cls._apex_cookie_prefixes()
        ):
            next_url = path
        else:
            next_url = f"https://{host}{path}"
        if request.url.query:
            next_url += f"?{request.url.query}"
        return (
            f"https://{session_cookie.apex_host()}/auth/login"
            f"?next={quote(next_url, safe='')}"
        )
