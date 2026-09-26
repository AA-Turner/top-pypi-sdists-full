"""
FastAPI application module
Handles all API initialization and configuration
"""

import logging
import os
from contextlib import asynccontextmanager
from urllib.parse import urlsplit

from fastapi import APIRouter, Depends, FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlmodel import Session

from src.api.middleware.license_headers import LicenseHeadersMiddleware
from src.database import get_session
from src.env_loader import get_environment
from src.page_paths import LEGACY_REDIRECTS, UI_PREFIX, app_url

from ..version import get_version

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _assert_schema_at_head() -> None:
    """Refuse to serve a database the migrations have not been applied to.

    Opt-in via ``INNODAY_REQUIRE_SCHEMA_HEAD``, default off, and that default is
    deliberate. The check cannot be switched on until deploys actually run
    ``alembic upgrade head`` -- and Railway's pre-deploy command cannot be
    configured until an image containing ``alembic/`` has already shipped. Enable
    it *after* one deploy has demonstrably applied migrations; enabling it before
    that turns the next deploy into an outage.

    This is the counterweight to dropping ``create_all``. Previously a
    schema/code mismatch produced no signal at all -- the app started happily and
    failed later on whichever query first touched the missing object, which is
    how dev served 500s for an enum label no migration had added (#478).
    """
    if os.getenv("INNODAY_REQUIRE_SCHEMA_HEAD", "").lower() not in ("1", "true", "yes"):
        return

    from alembic.config import Config
    from alembic.script import ScriptDirectory

    from ..database import engine

    expected = ScriptDirectory.from_config(Config("alembic.ini")).get_current_head()
    with engine.connect() as conn:
        actual = conn.execute(text("SELECT version_num FROM alembic_version")).scalar()

    if actual != expected:
        raise RuntimeError(
            f"Database schema is not at head: alembic_version={actual!r}, "
            f"expected {expected!r}. Run `alembic upgrade head` before serving. "
            "Refusing to start rather than fail later on a missing column."
        )
    logger.info("✅ Schema at head (%s)", expected)


def _reap_orphaned_syncs() -> None:
    """Correct sync rows a previous process left running -- see
    `reap_orphaned_syncs` for what boot does and does not tell us about them.

    Failures here are logged and swallowed on purpose. This is housekeeping, not
    a precondition of serving: an unreachable database at boot must not turn a
    deploy into an outage, and the reap will simply happen on the next start.
    That is the opposite of `_assert_schema_at_head`, which is a precondition
    and so is deliberately allowed to raise. (An *unresponsive* database is a
    different hazard, and is bounded by the engine's `connect_timeout` --
    `src/database/connect_args_for`; without it this call would hang the boot
    rather than fail it.)

    Uses `session_scope()`, which is what `get_session`'s own docstring directs
    code outside a request to use. Hand-calling the FastAPI dependency -- even
    through `app.dependency_overrides` -- is the shape #482 was about, and the
    override indirection bought nothing: it existed so a test could point the
    reap at its own database, and patching `src.database.engine` does that
    identically for either form (`test_it_runs_without_a_dependency_override`
    already proved so for the production branch).
    """
    try:
        from ..database import session_scope
        from ..services.board_sync_service import reap_orphaned_syncs

        with session_scope() as session:
            reaped = reap_orphaned_syncs(session)
    except Exception as exc:
        logger.warning("Could not reap orphaned board syncs at startup: %s", exc)
        return

    if reaped:
        # Not "orphaned": at boot we know only that another process left these
        # running, not that it is gone -- see `ORPHANED_SYNC_ERROR`.
        logger.info(
            "🧹 Marked %d board sync run(s) failed at startup: left running by "
            "another process",
            reaped,
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    #
    # `create_db_and_tables_sync()` is deliberately NOT called here any more. It
    # was `SQLModel.metadata.create_all()`, which builds missing tables from the
    # models and never ALTERs, renames, or advances `alembic_version`. That made
    # every missing migration invisible: the table appeared, the app served
    # traffic, and only the things a model cannot express -- indexes, named
    # constraints, RLS policies, grants, renames -- silently did not exist.
    # Migrations are the only thing that builds this schema now (#478 / PF-399).
    _assert_schema_at_head()

    # After the schema check, because it needs the schema to be trustworthy --
    # and before serving, so the first sync request of the new process is not
    # refused by a row the process it replaced left behind.
    _reap_orphaned_syncs()

    logger.info("\n🎉 InnoDay API is ready!")

    yield

    # Shutdown
    logger.info("👋 Shutting down InnoDay API...")


# Initialize FastAPI app with enhanced configuration
app = FastAPI(
    title="InnoDay Platform",
    description="""
    🤖 **AI-Powered Team Orchestration Platform**

    Captures team updates, prepares SCRUM meetings, directs workloads,
    organizes releases, and connects people to information.

    ## Architecture

    InnoDay is **organization-centric** — every resource is scoped to an `organization_id`.
    Board integrations (Jira, Trello, Linear, GitHub) are connected per-organization
    at board-registration time, not at platform startup.

    **Board credentials are never stored as platform environment variables.**
    Pass them at connect time via the `X-Integration-Token` request header.

    ## Quick Start

    ### 1. Platform environment (required)
    ```bash
    DATABASE_URL=postgresql://...
    CLAUDE_API_KEY=sk-ant-...
    GITHUB_ORG=your-org
    ```

    **A tenant's GitHub calls do NOT authenticate with a `GITHUB_TOKEN`
    environment variable.** Per-org GitHub credentials live in Supabase Vault
    (`org_credentials`) and are resolved per request; an `X-Integration-Token`
    header overrides them for a one-off call. An org with no stored credential
    gets an actionable 4xx rather than silently borrowing the operator's token.

    ### 2. Create an organization and connect a board
    ```
    POST /api/v1/organizations
    POST /api/v1/organizations/{org_id}/boards/register
         X-Integration-Token: <jira-email:api-token | trello-key:token | linear-api-key>
    ```

    ### 3. Sync tickets
    ```
    POST /api/v1/organizations/{org_id}/boards/{board_id}/sync
    ```

    ## Security

    - Board tokens are passed in request headers, never stored on the platform
    - All operations are scoped to `organization_id`
    - GitHub credentials are per-organization (Vault), never a shared process
      environment variable. Required scopes: `read:org`, `read:user`, `repo`

    Built with ❤️ by Haviland Software
    """,
    version=get_version(),
    contact={
        "name": "Haviland Software",
        "email": "support@haviland-software.com",
    },
    license_info={
        "name": "AGPL-3.0",
        "url": "https://www.gnu.org/licenses/agpl-3.0.html",
    },
    lifespan=lifespan,
)


# Health check endpoints
@app.get("/", tags=["Health"])
async def root(request: Request):
    """Platform info for API clients; the sign-in page for a browser.

    `/` is where a person lands when they type the bare domain, and it is also
    where Supabase falls back if a redirect URL is not allowlisted -- so a
    browser arriving here got a wall of raw JSON at the end of what should have
    been a sign-in.

    It cannot simply redirect, though: `innoday ping api` GETs this exact path
    and parses the JSON (`src/cli/client.py:141`), with `follow_redirects=True`,
    so a blanket redirect would hand every already-installed CLI an HTML page it
    cannot parse. Deployed clients are not upgraded in lockstep with the server.

    So the response depends on who is asking. A browser says `Accept:
    text/html` and gets sent to the UI; anything else keeps the JSON it has
    always had.
    """
    if "text/html" in (request.headers.get("accept") or "").lower():
        return RedirectResponse(url=UI_PREFIX, status_code=307)

    from sqlmodel import select

    from ..database import session_scope
    from ..domain.organization import (
        Organization,
    )

    # Get platform organization info for branding.
    #
    # `session_scope()`, not `next(get_session())`. The latter advances the
    # dependency generator and then drops it, so the session is only released
    # when the garbage collector finalises it -- and this is `/`, which every
    # `innoday ping api` and every browser landing hits, so the leak compounds
    # faster here than anywhere else (#482).
    platform_info = {}
    try:
        with session_scope() as session:
            # Look for platform organization (usually the first one or one with
            # special settings)
            statement = (
                select(Organization)
                .where(Organization.support_email.is_not(None))
                .limit(1)
            )
            platform_org = session.exec(statement).first()

            if platform_org:
                platform_info = {
                    "provider": platform_org.name,
                    "contact": platform_org.support_email,
                    "website": platform_org.website,
                    "support": platform_org.website,
                }
    except Exception:
        platform_info = {}

    response = {
        "message": "🎉 Welcome to InnoDay Platform!",
        "status": "✅ Healthy",
        "version": get_version(),
        "description": "AI-Powered Team Orchestration Platform",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_version": "v1",
    }

    if platform_info:
        response["platform"] = platform_info

    return response


@app.get("/health", tags=["Health"])
async def health_check(response: Response, db: Session = Depends(get_session)):
    """Health check endpoint — performs a real database connectivity check."""
    # Uses Depends(get_session) rather than calling next(get_session())
    # directly -- the latter bypasses FastAPI's DI container entirely, so
    # app.dependency_overrides[get_session] (used by every test file that
    # needs an isolated DB) had no effect on this endpoint.
    db_status = "disconnected"
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        pass

    healthy = db_status == "connected"
    if not healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "healthy" if healthy else "unhealthy",
        "service": "InnoDay Platform",
        "version": get_version(),
        "database": db_status,
        # get_environment(), not a local DEBUG check. This used to be
        # `"development" if DEBUG else "production"` -- "is DEBUG off" reported
        # under the name `environment` -- so the dev deployment behind
        # www.inno.day answered `production` here while /api/v1/public/status,
        # same process, answered `dev` (#619). Same resolver both sides now, so
        # they cannot disagree again.
        "environment": get_environment(),
        # No `port`: this route is anonymous, and the port is deployment detail
        # (PF-463). Platform admins still see it on /api/v1/public/status.
    }


# Add middleware for license compliance
app.add_middleware(LicenseHeadersMiddleware)

# No global team-secret gate: identity is the Bearer token, and the secret is a
# route-level dependency on platform-lifecycle routes only (PF-455).

# Include routers
from src.routers import (
    admin,  # NEW: Consolidated admin router
    ai,  # NEW: Consolidated AI router
    auth,
    boards,  # CONSOLIDATED: boards + board_tickets + board_summaries
    container_execution,  # REIMPLEMENTED: Organization-scoped container execution
    device,
    identities,
    integrations,  # NEW: Consolidated integrations router
    invites,
    licenses,
    onboarding,
    organizations,  # CLEANED: Only org CRUD and membership
    platform,
    project_timeline,  # NEW: Curated project event history (PF-102)
    projects,
    public,  # NEW: Public health/status endpoints
    releases,
    repositories,  # CONSOLIDATED: repositories + git_registrations + repository_issues + github
    scopes,
    scrums,  # Scrum runs + per-ticket visits (#626)
    search,  # REIMPLEMENTED: Organization-scoped search
    summaries,
    tickets,
    users,
)


def _ui_redirects() -> APIRouter:
    """301 every old page address to the same page on innoday-ui, at ``APP_URL``.

    This app no longer renders pages; innoday-ui does, at the very same paths.
    The addresses still matter: bookmarks, and invite emails **already
    delivered**, carry ``www.inno.day/ui/...`` -- and the pre-``/ui`` forms
    (``LEGACY_REDIRECTS``) before that. Dropping them would send those people to
    a 404, the failure #414 fixed.

    A 301 is safe for ``/auth/callback`` because the access token arrives in the
    URL *fragment*, which the browser reattaches to the redirect target.

    If ``APP_URL`` names this same host, redirecting would loop, so the route
    answers 404 and says why instead. Locally, with APP_URL at its default,
    this 301s to innoday-ui's dev server on :3000 -- run it, or nothing answers.

    The target path is the *raw* request path: the decoded one would turn
    ``/ui/..%2f..%2fx`` into a path that climbs out of ``/ui`` on APP_URL.
    """
    router = APIRouter(include_in_schema=False, tags=["compat"])

    def _to_ui(path: str, request: Request) -> Response:
        base = app_url()
        if urlsplit(base).netloc == request.url.netloc:
            return Response(
                "The web pages are served by innoday-ui, not by this API. "
                "Set APP_URL to where innoday-ui runs.",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        query = request.url.query
        target = f"{base}{path}"
        return RedirectResponse(
            url=f"{target}?{query}" if query else target,
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
        )

    def _legacy(target: str):
        async def _redirect(request: Request) -> Response:
            return _to_ui(target, request)

        return _redirect

    for legacy_path, target_path in LEGACY_REDIRECTS.items():
        router.add_api_route(legacy_path, _legacy(target_path), methods=["GET"])

    @router.get(UI_PREFIX)
    @router.get(UI_PREFIX + "/{rest:path}")
    async def _old_ui(request: Request) -> Response:
        return _to_ui(request.scope["raw_path"].decode("latin-1"), request)

    return router


# Public endpoints (no auth required)
app.include_router(
    public.router
)  # Health checks and status - Has /api/v1/public prefix

# Authentication
app.include_router(auth.router, tags=["Authentication"])  # Has its own prefix
app.include_router(device.router)  # CLI device flow (API half)

# Browser pages live in innoday-ui at APP_URL; old addresses here 301 there.
app.include_router(_ui_redirects())

# Core API routes (all have /api/v1 prefix defined in router)
app.include_router(organizations.router)  # Organization CRUD and membership
app.include_router(invites.router)  # Org invites + self-registration (auth P3)
app.include_router(onboarding.router)  # Workspace onboard resolution (auth P4)
app.include_router(identities.router)  # Handle -> user mappings (#569)
app.include_router(users.router)  # User management
app.include_router(projects.router)  # Project management
app.include_router(scopes.router)  # Project scopes
app.include_router(tickets.router)  # Ticket management
app.include_router(releases.router)  # Release tracking
app.include_router(scrums.router)  # Scrum runs + per-ticket visits (#626)
app.include_router(project_timeline.router)  # Curated project event history (PF-102)
app.include_router(summaries.router)  # Project summary engine + history (PF-398)
app.include_router(boards.router)  # Consolidated board operations
app.include_router(repositories.router)  # Consolidated repository operations
app.include_router(licenses.router)  # License management

# Search and execution routes
app.include_router(search.router)  # Organization-scoped search
app.include_router(container_execution.router)  # Container execution

# Integration and AI routes
app.include_router(
    integrations.router
)  # All external integrations (GitHub, Jira, Trello, Slack)
app.include_router(ai.router)  # All AI/Claude functionality

# Platform administration
app.include_router(admin.router)  # Admin and platform management
app.include_router(platform.router)  # Platform-specific operations
