"""Shared-secret gate for restricting the deployed API to the team."""

import hmac
import os

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.page_paths import LEGACY_PAGE_PATHS, UI_PAGE_PATHS, UI_PREFIX

EXEMPT_PATHS = {
    # The site root. Supabase's Site URL is this deployment's bare origin, and any
    # auth redirect whose `redirect_to` is missing or not allowlisted falls back to
    # it -- so an un-exempt "/" turns the end of a working sign-in into a raw
    # `Missing or invalid X-Team-Secret header`. It serves the same
    # name/version/status payload as /health, which is already exempt below.
    "/",
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc",
    # Atlassian's browser redirect after OAuth 2.0 (3LO) consent hits this
    # route directly -- it cannot send an X-Team-Secret header (a plain
    # HTTP redirect only carries the code/state query params Atlassian
    # controls). This route's actual security boundary is the signed
    # `state` parameter (see parse_and_verify_state in
    # src.services.jira_oauth_service), not this header gate. GitHub
    # issue #296.
    "/api/v1/boards/oauth/jira/callback",
    # CLI device flow: the polling client has no team secret (it's pre-auth),
    # and the /ui/device browser page is exempted with the other pages below.
    # Their real security boundary is the high-entropy device_code / the
    # approver's own Bearer token, not this header gate. (auth P2, PF-350)
    "/api/v1/device/code",
    "/api/v1/device/token",
    "/api/v1/device/approve",
    # The one call the /ui/auth/callback page makes. It still requires a
    # JWKS-verified Supabase JWT and can only ever confirm the caller
    # themselves, so exempt-from-the-door-key is not the same as public. (#414)
    "/api/v1/auth/confirm-email",
    # The three browser pages (/ui/auth/callback, /ui/invite/accept,
    # /ui/device). A browser arriving from an email or an OAuth redirect cannot
    # send this header. Three code paths pointed Supabase at the callback for a
    # while with nothing exempted or even served, so every recipient hit a 401
    # -- confirmed at the IdP but still unverified in InnoDay, exactly the
    # lockout the flag was meant to avoid. (#414)
    *UI_PAGE_PATHS,
    # Bare ``/ui`` -- the redirect to your default org. Its subpaths are covered
    # by EXEMPT_PREFIXES below, but an exact match needs naming here.
    UI_PREFIX,
    # Their pre-/ui addresses, still served as 301s (see src/api/app.py). These
    # must stay exempt too: the middleware runs before routing, so without them
    # a magic link from an already-delivered email would 401 rather than
    # redirect -- reintroducing #414 by a different route.
    *LEGACY_PAGE_PATHS,
}
# ``/ui/`` is a prefix, not a path list: the dashboard is ``/ui/{org_alias}``, so
# the set of valid page paths is unbounded and cannot be enumerated here. Every
# page's real boundary is the session cookie -- see src/routers/webui/session.py.
# The trailing slash matters: a bare ``/ui`` prefix would also exempt ``/uixyz``.
EXEMPT_PREFIXES = ("/api/v1/public", UI_PREFIX + "/")


class TeamSecretMiddleware(BaseHTTPMiddleware):
    """
    Requires an X-Team-Secret header matching TEAM_ACCESS_SECRET on all
    routes except health/public/docs endpoints. No-op if TEAM_ACCESS_SECRET
    is unset, so local dev is unaffected.
    """

    async def dispatch(self, request: Request, call_next):
        secret = os.getenv("TEAM_ACCESS_SECRET")
        if not secret:
            return await call_next(request)

        path = request.url.path
        if path in EXEMPT_PATHS or path.startswith(EXEMPT_PREFIXES):
            return await call_next(request)

        if not hmac.compare_digest(request.headers.get("X-Team-Secret", ""), secret):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid X-Team-Secret header"},
            )

        return await call_next(request)


def require_team_secret(request: Request) -> None:
    """Explicit route-level team-secret gate (defense-in-depth on top of
    TeamSecretMiddleware). No-op when TEAM_ACCESS_SECRET is unset (local dev),
    matching the middleware's own posture. Raises 401 on missing/invalid header.

    Attach it to a route as an additional dependency so the gate is guaranteed
    even if the global middleware's config/exemptions changed:

        @router.post("/users", dependencies=[Depends(require_team_secret)])
    """
    secret = os.getenv("TEAM_ACCESS_SECRET")
    if not secret:
        return
    if not hmac.compare_digest(request.headers.get("X-Team-Secret", ""), secret):
        raise HTTPException(
            status_code=401, detail="Missing or invalid X-Team-Secret header"
        )
