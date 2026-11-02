"""Standalone microservice entry — the SAME package running as its own app.

This factory is what the independence gate boots in CI, and what production
runs on the dedicated host (EC2 us-east-1, next to the buckets). It builds
everything from explicit environment variables (each named in
``_env_config()`` — the complete registry), validated all-at-once, and mounts
the exact router factories a host mounts. No aidream, no host anything.

Two service modes, decided by what env you provide:

* **Full service** (production): ``SUPABASE_MATRIX_*`` (THE ONE DATABASE —
  ONE connection, required — never a second candidate) +
  ``AWS_S3_DEFAULT_BUCKET`` + ``SUPABASE_URL``.
  DB binds via :func:`matrx_files.db.bootstrap_db`, auth verifies real
  Supabase JWTs (ES256 via JWKS + optional HS256 secret), and the file/asset/
  share routers serve authenticated traffic.
* **Smoke mode** (the independence gate / bare CI): no env at all — the app
  still boots and serves ``/files-service/health`` so proof-by-execution
  works without cloud credentials. Protected routers mount ONLY when their
  dependencies are configured; a partially-configured service REFUSES to
  start (loud, all errors at once) rather than serving broken routes.

Run locally:
    uvicorn matrx_files.standalone.app:create_app --factory --port 8080
"""

from __future__ import annotations

import logging
import os
import types

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from matrx_files._config import IndependenceConfigError, configure


def _package_version() -> str:
    """The installed matrx-files version, for /health + deploy verification.

    Reads the real installed distribution so the reported version tracks what
    actually shipped; falls back to "0.0.0+unknown" if the metadata is missing
    (e.g. an editable checkout without an installed dist)."""
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("matrx-files")
    except PackageNotFoundError:
        return "0.0.0+unknown"


_PUBLIC_PATHS = frozenset(
    {
        "/files-service/health",
        "/files-service/ready",
        "/assets/presets",
    }
)
_PUBLIC_PREFIXES = ("/share/",)
# Method-scoped anonymous routes: the TUS OPTIONS capabilities advertisement
# shares its path with the authenticated POST create.
_PUBLIC_OPERATIONS = frozenset({"OPTIONS /files/upload/tus"})

_REQUIRED_CONFIG_KEYS = ("db_host", "s3_bucket", "supabase_url")
# Package default = LOCAL DEVELOPMENT ONLY (loopback). A deployment names its own
# browser origins via MATRX_FILES_CORS_ALLOWED_ORIGINS (exact list) or
# MATRX_FILES_CORS_ALLOWED_ORIGIN_REGEX (patterns, e.g. preview subdomains) —
# our production host does (set 2026-08-09), and so would a customer running
# this service themselves. This default used to hardcode aimatrx.com /
# aidream.ai / matrxserver.com / *.vercel.app, which made the package carry
# AI Dream's identity — the "package hardwired to us" failure in
# common-docs/policies/package-vs-implementation.md.
_DEFAULT_CORS_ORIGIN_REGEX = (
    r"^(?:"
    # Bare localhost AND any lane subdomain of it (http://<lane>.localhost:3001 —
    # the shared preview server every dev/lane checkout browses through, see
    # common-docs/systems/data/custom-data/STATE.md). Still
    # requires the literal `localhost` host — never widens past that word.
    r"https?://(?:[a-z0-9]([a-z0-9-]*[a-z0-9])?\.)*localhost(?::\d+)?"
    r"|https?://127\.0\.0\.1(?::\d+)?"
    r"|https?://\[::1\](?::\d+)?"
    r")$"
)


def _env_config() -> dict[str, object]:
    """Map explicit env vars → the app's wiring flags. EVERY var consumed by
    the standalone app is named here — this function is the complete registry.
    """
    return {
        # DB — THE ONE DATABASE (Matrx Main). One prefix, no alternatives.
        "db_host": os.environ.get("SUPABASE_MATRIX_HOST"),
        # Storage
        "s3_bucket": os.environ.get("AWS_S3_DEFAULT_BUCKET"),
        # Auth — Supabase project URL; JWKS derived, HS256 secret optional
        "supabase_url": os.environ.get("SUPABASE_URL")
        or os.environ.get("SUPABASE_MATRIX_URL"),
        "jwt_secret": os.environ.get("SUPABASE_JWT_SECRET")
        or os.environ.get("SUPABASE_MATRIX_JWT_SECRET", ""),
        # HMAC secret behind the mx_files_session cookie AND guest
        # fingerprints. The cookie is minted by the MAIN server and verified
        # HERE, so this value must be the SAME GUEST_FINGERPRINT_SECRET every
        # Matrx service holds — one value, one name, no fallback chain. Empty
        # → matrx-connect falls back to a RANDOM per-process secret and every
        # cross-service (and cross-restart) private <img> render 401s with a
        # CRITICAL MX_COOKIE_SIGNATURE_MISMATCH scream (the 2026-08-30/31
        # private-file outage class).
        "guest_fingerprint_secret": os.environ.get("GUEST_FINGERPRINT_SECRET", ""),
        "session_authority_url": os.environ.get("MATRX_SESSION_AUTHORITY_URL"),
        "file_session_authority_url": os.environ.get("MATRX_FILE_SESSION_AUTHORITY_URL"),
        "file_session_mint_url": os.environ.get("MATRX_FILE_SESSION_MINT_URL"),
        # Browser-direct clients. Exact comma-separated origins override the
        # default/regex; the regex covers Matrx production, previews, and local
        # loopback development without opening arbitrary origins.
        "cors_allowed_origins": os.environ.get(
            "MATRX_FILES_CORS_ALLOWED_ORIGINS", ""
        ),
        "cors_allowed_origin_regex": os.environ.get(
            "MATRX_FILES_CORS_ALLOWED_ORIGIN_REGEX", ""
        ),
    }


def _add_cors_middleware(app: FastAPI, cfg: dict[str, object]) -> None:
    raw_origins = str(cfg["cors_allowed_origins"] or "").strip()
    if raw_origins:
        origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
        if "*" in origins:
            raise IndependenceConfigError(
                "MATRX_FILES_CORS_ALLOWED_ORIGINS cannot contain '*' while "
                "credentialed browser requests are enabled; list trusted origins "
                "explicitly or use MATRX_FILES_CORS_ALLOWED_ORIGIN_REGEX."
            )
        origin_regex: str | None = None
    else:
        origins = []
        origin_regex = (
            str(cfg["cors_allowed_origin_regex"] or "").strip()
            or _DEFAULT_CORS_ORIGIN_REGEX
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=origin_regex,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
        allow_headers=["*"],
        expose_headers=[
            "Accept-Ranges",
            "Content-Disposition",
            "Content-Length",
            "Content-Range",
            "ETag",
            "Last-Modified",
            "Location",
            "Tus-Resumable",
            "Tus-Version",
            "Tus-Extension",
            "Tus-Max-Size",
            "Upload-Offset",
            "Upload-Length",
            "Upload-Complete",
            "X-Cld-File-Id",
            "X-Request-ID",
        ],
        max_age=3600,
    )


def _configure_settings_for_standalone() -> None:
    """Give the matrx-utils settings registry an env-first standalone object.

    FileService/FileManager read BASE_DIR/TEMP_DIR + cloud settings through
    ``matrx_utils.conf.settings``. Hosted, aidream configures this; standalone,
    we install a minimal env-first object once (idempotent across factory calls).
    """
    from matrx_utils.conf import configure_settings, settings

    if getattr(settings, "_configured", False):
        return
    base_dir = os.environ.get("MATRX_FILES_BASE_DIR", "/tmp/matrx-files")
    obj = types.SimpleNamespace(
        BASE_DIR=base_dir,
        TEMP_DIR=os.path.join(base_dir, "temp"),
        DEBUG=False,
    )
    configure_settings(obj, env_first=True)


def _configure_context_for_standalone() -> None:
    """Join matrx-connect's AppContext to the matrx-utils ambient context seam.

    🚨 THE 2026-09-19 OUTAGE. ``AuthMiddleware`` pins the VERIFIED organization
    onto the matrx-connect ``AppContext``; every package that asks "what
    organization is this request in?" through ``matrx_utils.ctx`` reads a
    DIFFERENT object, and the two are joined only by a host calling
    ``configure_context``. ``aidream`` does it in ``package_integration.py``.
    This standalone service — the one the browser actually uploads to — never
    did, so ``get_active_organization_id()`` answered ``None`` for every
    request, and the file write funnel refused all 21 files of a Masterwork
    source drop with "this write carries no organization" while a correct,
    verified ``X-Organization-Id`` sat one layer away.

    The write path no longer DEPENDS on this (the edge resolves the
    organization once and threads it explicitly, and
    ``request_organization.admitted_organization_id`` reads the AppContext
    directly). This call makes the ambient seam honest too, so every other
    ``matrx_utils.ctx`` reader in this process — the change-feed logger, the
    db layer's scope check — sees the same request the router sees, instead of
    quietly seeing nobody.
    """
    from matrx_utils import configure_context

    def _active_context():
        try:
            from matrx_connect import get_app_context

            return get_app_context()
        except Exception:
            return None

    configure_context(_active_context)


def _assert_block_ledger_seam() -> None:
    """Refuse to boot a service that would silently lose every file-reader wall.

    🚨 BOARD ROW H8. Before this call existed, `matrx_files.standalone.app`
    never wired `matrx_files.blocks` at all: a DRM-protected ebook, an
    unsupported container, an empty file, or a missing OCR binary hit by
    THIS process announced through `matrx_utils.block_sink.announce_block`
    into a documented no-op nobody had configured, and the finding — the
    entire point of the Block Ledger — was lost with only an INFO log line.
    Same posture as `_assert_organization_seam`: a missing wire is a
    boot-time misconfiguration, said once at boot, never a silent per-request
    shrug.
    """
    from matrx_files.blocks import assert_block_sink_ready

    assert_block_sink_ready()


def _assert_organization_seam() -> None:
    """Refuse to boot a service that cannot carry an organization into a write.

    Without a seam, EVERY org-scoped write this process serves refuses at
    request time with a message about a header the caller did send. That is a
    boot-time misconfiguration wearing a request-time costume; say it at boot.
    """
    from matrx_files.request_organization import context_seam_status

    seams = context_seam_status()
    if not any(seams.values()):
        raise IndependenceConfigError(
            "matrx-files standalone has NO organization context seam "
            f"({seams}). Every organization-scoped write would refuse at "
            "request time with 'this write carries no organization' even when "
            "the caller sends a valid X-Organization-Id. Wire "
            "matrx_utils.configure_context (see _configure_context_for_standalone) "
            "or make matrx_connect.get_app_context importable."
        )


async def _standalone_resolve_active_organization(
    user_id: str, claimed_org_id: str | None
) -> str | None:
    """Verify ``X-Organization-Id`` against real membership before admitting it.

    Without this resolver, ``AuthMiddleware._resolve_organization`` TRUSTS a
    claimed org header as-is ("acceptable in dev, never in production" — this
    standalone service is production). ``files.*`` rows are org-scoped
    (``organization_id`` is ``NOT NULL`` on the core file models), and
    ``SyncEngine._resolve_write_organization_id_async`` already calls this
    exact RPC to verify a caller-supplied org on a write — this resolver
    makes the SAME check happen at the admission gate, before any route
    code runs, using the package's own DB binding (independence-compliant,
    same posture as ``access_checker.py``).
    """
    if not claimed_org_id or not user_id:
        return None
    from matrx_orm import call_function

    from matrx_files.db import PACKAGE_DB_NAME

    # 🚨 A DB failure is NOT "no organization" — returning None here made an
    # outage indistinguishable from a caller who named no org at all, silently
    # changing the scope downstream work ran in. The error now propagates:
    # ``AuthMiddleware._resolve_organization`` marks the context
    # ``organization_admission="unverifiable"`` and org-scoped features refuse.
    has_access = await call_function(
        PACKAGE_DB_NAME, "iam", "has_org_access_for", user_id, claimed_org_id
    )
    return claimed_org_id if has_access is True else None


def _user_id_dep():
    """FastAPI dependency: the authenticated user id from matrx-connect.

    AuthMiddleware (mounted below) verified the Supabase JWT and installed the
    AppContext; anonymous requests are refused here — this service has no
    guest surface.
    """
    from fastapi import HTTPException
    from matrx_connect import get_app_context

    ctx = get_app_context()
    user_id = getattr(ctx, "user_id", None) if ctx else None
    if not user_id:
        raise HTTPException(status_code=401, detail="authentication required")
    return user_id


def create_app() -> FastAPI:
    cfg = _env_config()
    # Interactive docs + the OpenAPI schema are DISABLED on the internet-exposed
    # standalone service — they would let an anonymous caller enumerate the full
    # API surface. (Hosted-in-aidream keeps its own docs behind aidream's edge.)
    # Re-enable deliberately behind auth if ever needed.
    app = FastAPI(
        title="Matrx Files",
        # Derive from the installed package so /health and the deploy
        # verify-version-in-image check report the ACTUAL shipped version. A
        # hardcoded string (was "0.1.2") silently masks whether a fix landed.
        version=_package_version(),
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    app.state.standalone_session_policy_required = True

    # Health is ALWAYS served — the independence gate's proof of boot.
    from matrx_files.api.router import router as health_router

    app.include_router(health_router)

    wired = {key: bool(cfg[key]) for key in _REQUIRED_CONFIG_KEYS}
    fully_configured = all(wired.values())
    if not any(wired.values()) and not any(
        cfg[k] for k in ("session_authority_url", "file_session_authority_url", "file_session_mint_url")
    ):
        # Smoke mode — bare boot with zero cloud env (CI gate). configure()
        # records the mode so get_config() callers see a real object.
        configure()
        _add_cors_middleware(app, cfg)
        _assert_auth_coverage(app)
        return app
    from matrx_files.standalone.session_policy import build_session_policy

    session_policy = build_session_policy(cfg)
    if not fully_configured:
        missing = [k for k, v in wired.items() if not v]
        raise IndependenceConfigError(
            "matrx-files standalone is PARTIALLY configured — refusing to "
            f"serve broken routes. Missing: {missing}. Provide "
            "SUPABASE_MATRIX_* (the ONE database), "
            "AWS_S3_DEFAULT_BUCKET (storage), SUPABASE_URL (auth) — or none "
            "at all for bare smoke mode."
        )

    # ---- full service wiring ------------------------------------------------
    configure(
        # Durable render-URL base for this service's absolute
        # /files/{id}/download URLs (see cloud_sync/render_urls.py).
        files_public_base_url=os.environ.get("MATRX_FILES_PUBLIC_BASE_URL")
        or os.environ.get("PUBLIC_URL")
        or "https://files.matrxserver.com",
    )
    _configure_settings_for_standalone()
    _configure_context_for_standalone()

    from matrx_files.db import bootstrap_db

    bootstrap_db()
    from matrx_files.db.readiness import clear_readiness_cache

    clear_readiness_cache()

    # Board row H8: wire this package's own Block Ledger sink now that the
    # pool is bound (`OrmBlockStore` needs a registered database). Deferential
    # by design — see `matrx_files.blocks.sink.configure_block_ledger` — so a
    # process that also hosts a richer sink (aidream) keeps its own.
    from matrx_files.blocks import configure_block_ledger

    configure_block_ledger()

    # Make the authoritative DB policy (`files.has_access_for` /
    # `iam.has_access_for`) the single source of truth for the async file gate —
    # the same wiring aidream does via `install_file_access_checker`. Without it
    # the standalone service falls back to the Python permission SUBSET, which
    # cannot see orgs/memberships/reachability or the contextual crawl-artifact →
    # web.site container grant, and silently denies files an org member should
    # see (`has 'none'`). MUST run after bootstrap_db() so the pool is bound.
    from matrx_files.standalone.access_checker import install_standalone_access_checker

    install_standalone_access_checker()

    from matrx_files.api import (
        build_asset_router,
        build_file_router,
        build_share_router,
        build_sync_mappings_router,
        build_tus_router,
    )
    from matrx_files.service import FileService

    file_service = FileService.from_env(app_name="matrx-files-service")
    app.include_router(build_file_router(
        file_service, user_id_dep=_user_id_dep, require_file_session_source=True,
    ))
    app.include_router(build_asset_router(file_service, user_id_dep=_user_id_dep))
    # Folder-sync mappings (SPEC-SERVER §6.3). Creation goes through the service
    # so D20's admission rules can run; the daemon's status reports ride
    # PATCH under If-Match. The browser reads and writes INTENT
    # (desired_state / direction / knobs) direct-to-Supabase under RLS.
    app.include_router(build_sync_mappings_router(user_id_dep=_user_id_dep))
    # TUS resumable uploads. SPEC-SERVER §8 / S16: the quota pre-flight and the
    # metering finalize are the PACKAGE's now, not a host injection — before
    # this, the live service every client is cut over to metered nothing and
    # enqueued nothing. Sanitizer and system-origin relocation were already the
    # package defaults. Automatic analysis and content-processing dispatch stay
    # aidream's (S16) and are deliberately still absent here.
    #
    # 🚨 The usage delta this finalize writes is keyed on the USER, while D11
    # meters storage to the ORGANIZATION. FS-L6 must re-grain the ledger before
    # any grandfather floor is computed from it. See matrx_files/upload_policy.py.
    #
    # index_for_knowledge is passed EXPLICITLY as None: the knob that decides it
    # (knowledge.index_for_knowledge in files.sync_mappings.knobs — C11, registry
    # FS-C7) is not live yet, so this deployment has no source to read and says
    # so out loud at boot rather than skipping silently on every upload.
    # ONE factory. `build_upload_policy` is the same call the liveness guard
    # exercises (`assert_upload_policy_is_live`), so the object this service
    # serves and the object the guard proves are built by the same code -- not
    # two descriptions of the same intention. Every earlier guard on this wiring
    # only ever INSPECTED create_app's source or AST, and each was defeated by a
    # stub wearing the right kwarg name.
    from matrx_files.upload_policy import build_upload_policy

    _policy = build_upload_policy(file_service, index_for_knowledge=None)
    _quota_checker = _policy["quota_checker"]
    _finalize = _policy["finalize"]

    def _standalone_quota_checker_dep():
        return _quota_checker

    # Declared on the app so a guard can read what this service ACTUALLY wired,
    # rather than re-deriving it from the source of this function (§10.1).
    app.state.matrx_upload_policy = _policy
    logging.getLogger(__name__).info("[matrx-files-service] %s", _policy["arming"])
    app.include_router(
        build_tus_router(
            file_service,
            user_id_dep=_user_id_dep,
            quota_checker_dep=_standalone_quota_checker_dep,
            finalize=_finalize,
        )
    )
    # Share resolver is deliberately auth-free — the share token IS the auth.
    app.include_router(build_share_router(file_service))
    # AuthMiddleware is added AFTER every router is mounted: its admission kwargs are composed
    # from the route table the service actually serves (file reads decided by access, the
    # identity-only session mint) — see matrx_files/standalone/admission.py. Starlette builds
    # the middleware stack at first request, so the ORDER relative to CORS below is unchanged.
    from matrx_connect.middleware.auth import AuthMiddleware
    from matrx_files.standalone.admission import admission_config

    supabase_url = str(cfg["supabase_url"]).rstrip("/")
    app.add_middleware(
        AuthMiddleware,
        jwt_secret=str(cfg["jwt_secret"]),
        guest_fingerprint_secret=str(cfg["guest_fingerprint_secret"]),
        jwks_url=f"{supabase_url}/auth/v1/.well-known/jwks.json",
        jwt_algorithms=("HS256", "ES256"),
        quiet_paths=("/files-service/health",),
        log_requests=False,
        resolve_active_organization=_standalone_resolve_active_organization,
        resolve_current_session=session_policy.login,
        resolve_file_session=session_policy.file,
        require_file_session_source=True,
        # Declared explicitly, reusing the SAME public-surface list this
        # module already maintains for its own auth-coverage assertion
        # (_PUBLIC_PATHS / _PUBLIC_PREFIXES) — one list of "doesn't need a
        # caller identity", not two. /share is the token-IS-the-auth resolver
        # (a stray bearer token on that request must never trip the org gate).
        **admission_config(
            app,
            public_paths=tuple(_PUBLIC_PATHS)
            + tuple(prefix.rstrip("/") for prefix in _PUBLIC_PREFIXES),
        ),
    )
    from matrx_files.standalone.remote_mint import RemoteFileSessionMintMiddleware

    app.add_middleware(RemoteFileSessionMintMiddleware, mint=session_policy.mint)
    app.state.file_session_policy = session_policy
    # Last-added middleware is outermost in Starlette. CORS must wrap auth so
    # unauthenticated browser OPTIONS preflights never reach AuthMiddleware.
    _add_cors_middleware(app, cfg)
    _assert_auth_coverage(app)
    _assert_organization_seam()
    _assert_block_ledger_seam()
    return app


def _assert_auth_coverage(app: FastAPI) -> None:
    from matrx_files.standalone.security import assert_route_auth_coverage

    assert_route_auth_coverage(
        app,
        auth_dependency=_user_id_dep,
        public_paths=_PUBLIC_PATHS,
        public_prefixes=_PUBLIC_PREFIXES,
        public_operations=_PUBLIC_OPERATIONS,
    )
