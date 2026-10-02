"""Standalone FastAPI service for the matrx-seo vertical.

The same package code aidream hosts, behind its own boundary: the ``svc_seo``
Postgres role (``bootstrap_db`` + ``assert_service_role``), the matrx-orm
secrets battery (``CREDENTIALS_ENCRYPTION_KEY`` verified at boot), and
matrx-connect ``AuthMiddleware`` (Supabase JWTs only — no static tokens, no dev
bypass). Construction (``create_app``) needs no environment; lifespan startup
refuses loudly when the env contract is not met.
"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib.metadata import version as distribution_version
from pathlib import Path
from typing import Any
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from matrx_connect import AppContext, context_dep, require_authenticated
from matrx_connect.middleware import DEFAULT_ORG_EXEMPT_PATHS, AuthMiddleware
from matrx_orm.secrets_battery import SecretDecryptError, SecretNotFoundError

from matrx_seo.access import collection_run_discoverable, collection_run_readable
from matrx_seo.adapters_registry import ADAPTER_FACTORIES
from matrx_seo.api_contracts import (
    BacklinkRefreshCreateRequest,
    CollectionCreateRequest,
    DataForSeoOperationsResponse,
    LoginRequest,
    LoginResponse,
    RankObservationOut,
    RunEvidenceResponse,
    RunListResponse,
    RunObservationsResponse,
    RunStatusResponse,
    WhoAmIResponse,
    dataforseo_operations_catalog,
    run_evidence_response,
    run_status_response,
)
from matrx_seo.backlink_refresh import (
    BacklinkRefreshOptions,
    BacklinkRefreshReceipt,
    BacklinkRefreshService,
)
from matrx_seo.contracts import (
    CollectionInProgressError,
    CollectionReceipt,
    CollectionRequest,
    ProviderResponseError,
)
from matrx_seo.db import PACKAGE_DB_NAME, SERVICE_ROLE_NAME, assert_service_role, bootstrap_db
from matrx_seo.orm_identity import OrmHostBindingResolver, OrmSeoIdentityResolver
from matrx_seo.orm_repository import OrmSeoRepository
from matrx_seo.service import SeoCollectionService

_ENCRYPTION_SELFTEST = "matrx-seo-standalone-selftest"
logger = logging.getLogger(__name__)


_CONSOLE_HTML = Path(__file__).with_name("console.html")


async def _standalone_resolve_active_organization(
    user_id: str, claimed_org_id: str | None
) -> str | None:
    """Verify ``X-Organization-Id`` against real membership before admitting it.

    Without this resolver, ``AuthMiddleware._resolve_organization`` TRUSTS a
    claimed org header as-is (documented as "acceptable in dev, never in
    production" — this standalone service is production). That is worse than
    the no-fallback-org defect this whole gate exists to close: it lets any
    authenticated caller name ANY organization and be admitted into it, no
    membership required. Mirrors ``_standalone_collection_authorizer``'s own
    membership check (``iam.has_org_access_for``) so there is exactly one
    membership rule for this service, not two.
    """
    if not claimed_org_id or not user_id:
        return None
    from matrx_orm import call_function

    # 🚨 A DB failure is NOT "no organization". It used to return None here,
    # which is the same value a caller who named no org at all produces — so an
    # outage silently changed the scope every downstream feature runs in. The
    # error now propagates: ``AuthMiddleware._resolve_organization`` marks the
    # context ``organization_admission="unverifiable"`` and org-scoped features
    # refuse with words instead of quietly answering for a different scope.
    has_access = await call_function(
        PACKAGE_DB_NAME,
        "iam",
        "has_org_access_for",
        user_id,
        claimed_org_id,
    )
    return claimed_org_id if has_access is True else None


async def _standalone_collection_authorizer(request: CollectionRequest) -> CollectionRequest:
    if not request.organization_id.strip():
        raise ValueError("SEO collections require a nonblank organization_id")
    if not request.created_by.strip():
        raise ValueError("SEO collections require an authenticated created_by")
    from matrx_orm import call_function

    has_access = await call_function(
        PACKAGE_DB_NAME,
        "iam",
        "has_org_access_for",
        request.created_by,
        request.organization_id,
    )
    if has_access is not True:
        raise PermissionError(
            "SEO collections require active membership in the requested organization"
        )
    return request


def _verify_credentials_encryption() -> None:
    """Boot gate: the battery key must be EXPLICITLY set (the battery has a
    derivation fallback that would round-trip fine with the wrong key, so env
    presence is part of the contract) and must survive a round-trip."""
    if not os.environ.get("CREDENTIALS_ENCRYPTION_KEY"):
        raise RuntimeError(
            "matrx-seo standalone requires CREDENTIALS_ENCRYPTION_KEY (the secrets-battery "
            "Fernet key) to be set explicitly — refusing to boot without it"
        )
    from matrx_orm.secrets_battery import decrypt_value, encrypt_value

    if decrypt_value(encrypt_value(_ENCRYPTION_SELFTEST)) != _ENCRYPTION_SELFTEST:
        raise RuntimeError("CREDENTIALS_ENCRYPTION_KEY failed the encrypt/decrypt round-trip")


def _credentials_encryption_healthy() -> bool:
    try:
        from matrx_orm.secrets_battery import decrypt_value, encrypt_value

        return (
            bool(os.environ.get("CREDENTIALS_ENCRYPTION_KEY"))
            and decrypt_value(encrypt_value(_ENCRYPTION_SELFTEST)) == _ENCRYPTION_SELFTEST
        )
    except Exception:
        return False


def _models_registered() -> bool:
    try:
        from matrx_orm import model_registry

        return (
            model_registry.get_model("CollectionRun", schema="seo", database=PACKAGE_DB_NAME)
            is not None
        )
    except Exception:
        return False


async def _readiness_snapshot(app: FastAPI) -> tuple[dict[str, object], int]:
    from matrx_orm.core.async_db_manager import AsyncDatabaseManager

    database_healthy = False
    service_role_healthy = False
    local_dev_database_override = False
    try:
        identity = await AsyncDatabaseManager.connection_identity(PACKAGE_DB_NAME)
        database_healthy = True
        service_role_healthy = identity.current_user == SERVICE_ROLE_NAME
        local_dev_database_override = (
            bool(getattr(app.state, "local_dev_enabled", False)) and not service_role_healthy
        )
    except Exception:
        logger.exception("matrx-seo readiness database identity probe failed")

    checks: dict[str, bool] = {
        "database": database_healthy,
        "service_role": service_role_healthy,
        "local_dev_database_override": local_dev_database_override,
        "models": _models_registered(),
        "credentials_encryption": _credentials_encryption_healthy(),
        "service": getattr(app.state, "seo_service", None) is not None,
    }
    required_checks = {
        name: healthy
        for name, healthy in checks.items()
        if name not in {"service_role", "local_dev_database_override"}
    }
    required_checks["database_role"] = bool(
        checks["service_role"] or checks["local_dev_database_override"]
    )
    failed = sorted(name for name, healthy in required_checks.items() if not healthy)
    payload: dict[str, object] = {
        "status": "ok" if not failed else "not_ready",
        **checks,
        "providers": sorted(ADAPTER_FACTORIES),
        "failed_components": failed,
    }
    return payload, 200 if not failed else 503


async def _visible_run(run_id: UUID, ctx: AppContext) -> Any:
    """READ gate — DEF-12/WS-5: canonical ``iam.has_access_for`` (see
    ``matrx_seo.access``). Owner always passes regardless of active org; a
    non-owner needs org admin/owner, an explicit grant, or reachability —
    never bare org membership."""
    from matrx_seo.db import models_seo as m

    row = await m.CollectionRun.load_by_id_or_none(str(run_id))
    if row is None or not await collection_run_readable(ctx.user_id, str(run_id)):
        raise HTTPException(
            status_code=404,
            detail={"error": "run_not_found", "run_id": str(run_id)},
        )
    return row


def _cors_origins() -> list[str]:
    configured = os.environ.get("MATRX_SEO_ALLOWED_ORIGINS", "")
    if configured.strip():
        origins = [item.strip().rstrip("/") for item in configured.split(",") if item.strip()]
        if not origins:
            raise RuntimeError("MATRX_SEO_ALLOWED_ORIGINS was set but contained no origins")
        return origins
    # Package default = LOCAL DEVELOPMENT ONLY. A deployment names its own
    # browser origins in MATRX_SEO_ALLOWED_ORIGINS — our production hosts do
    # (set 2026-08-09), and so would a customer running this service themselves.
    # Shipping OUR domains here made the package carry AI Dream's identity, which
    # is the "package hardwired to us" failure in
    # common-docs/policies/package-vs-implementation.md.
    return [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    if not (app.state.jwt_secret or app.state.jwks_url):
        raise RuntimeError(
            "matrx-seo standalone has no JWT verification material — set "
            "SUPABASE_MATRIX_URL (JWKS) and/or SUPABASE_JWT_SECRET; a service "
            "that can never authenticate anyone must not boot"
        )
    bootstrap_db()
    local_dev = os.environ.get("MATRX_SEO_LOCAL_DEV") == "1"
    database_role = await assert_service_role(allow_local_dev=local_dev)
    app.state.local_dev_enabled = local_dev
    local_dev_database_override = local_dev and database_role != SERVICE_ROLE_NAME
    if local_dev_database_override:
        logger.warning(
            "MATRX_SEO_LOCAL_DEV=1: running on broad database role %r; "
            "the supported launcher binds this process to 127.0.0.1 only",
            database_role,
        )
    _verify_credentials_encryption()

    from matrx_orm.secrets_battery import configure_secrets

    configure_secrets(db_config_name=PACKAGE_DB_NAME)

    app.state.seo_service = SeoCollectionService(
        OrmSeoRepository(),
        identity_resolver=OrmSeoIdentityResolver(),
        host_binding_resolver=OrmHostBindingResolver(),
        collection_authorizer=_standalone_collection_authorizer,
    )
    yield
    app.state.seo_service = None
    app.state.local_dev_enabled = False


def create_app() -> FastAPI:
    """Build the standalone SEO service. Environment is read here for auth
    wiring only; the DB/role/encryption env contract is enforced at startup
    (lifespan), so construction always succeeds."""
    package_version = distribution_version("matrx-seo")
    app = FastAPI(
        title="Matrx SEO",
        description="Standalone SEO collection microservice powered by matrx-seo",
        version=package_version,
        lifespan=_lifespan,
    )

    supabase_url = os.environ.get("SUPABASE_MATRIX_URL", "") or os.environ.get("SUPABASE_URL", "")
    jwt_secret = os.environ.get("SUPABASE_JWT_SECRET", "") or os.environ.get(
        "SUPABASE_MATRIX_JWT_SECRET", ""
    )
    jwks_url = f"{supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json" if supabase_url else None
    app.state.jwt_secret = jwt_secret
    app.state.jwks_url = jwks_url
    app.state.seo_service = None
    app.state.local_dev_enabled = False

    # Supabase-signed JWTs only — no static tokens, no dev bypass.
    app.add_middleware(
        AuthMiddleware,
        jwt_secret=jwt_secret,
        jwks_url=jwks_url,
        jwt_algorithms=("HS256", "ES256"),
        resolve_active_organization=_standalone_resolve_active_organization,
        # Declared explicitly, not inherited silently: the platform defaults
        # (liveness, OpenAPI, /auth/) PLUS "/me" — the identity-and-org probe
        # ``whoami()`` (below) exists specifically so the console can learn
        # which organization to scope to BEFORE it can send X-Organization-Id.
        # Every entry here is a hole in the admission contract; keep it short
        # enough to read aloud.
        organization_exempt_paths=DEFAULT_ORG_EXEMPT_PATHS + ("/me",),
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    def _service(request: Request) -> SeoCollectionService:
        service = getattr(request.app.state, "seo_service", None)
        if service is None:
            raise HTTPException(
                status_code=503,
                detail={"error": "not_ready", "message": "SEO service has not finished startup"},
            )
        return service

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "matrx-seo", "version": package_version}

    @app.get("/health/ready")
    async def health_ready() -> JSONResponse:
        payload, status_code = await _readiness_snapshot(app)
        return JSONResponse(content=payload, status_code=status_code)

    @app.get(
        "/providers/dataforseo/operations",
        response_model=DataForSeoOperationsResponse,
        dependencies=[Depends(require_authenticated)],
    )
    async def dataforseo_operations() -> DataForSeoOperationsResponse:
        return dataforseo_operations_catalog()

    @app.post(
        "/sites/{site_id}/backlinks/refresh",
        response_model=BacklinkRefreshReceipt,
        dependencies=[Depends(require_authenticated)],
    )
    async def refresh_site_backlinks(
        site_id: str,
        body: BacklinkRefreshCreateRequest,
        request: Request,
        ctx: AppContext = Depends(context_dep),
    ) -> BacklinkRefreshReceipt:
        try:
            return await BacklinkRefreshService(_service(request)).refresh_site(
                BacklinkRefreshOptions(
                    organization_id=body.organization_id,
                    created_by=ctx.user_id,
                    site_id=site_id,
                    profile=body.profile,
                    detail_limit=body.detail_limit,
                    detail_max_rows=body.detail_max_rows,
                    force_refresh=body.force_refresh,
                    request_id=body.request_id,
                    source_crawl_session_id=body.source_crawl_session_id,
                )
            )
        except (SecretNotFoundError, SecretDecryptError) as exc:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "provider_credential_unavailable",
                    "provider": "dataforseo",
                    "message": str(exc),
                    "fix": "Add or re-save DataForSEO credentials in Settings → Secrets.",
                },
            ) from exc
        except CollectionInProgressError as exc:
            raise HTTPException(
                status_code=409,
                detail={"error": "collection_in_progress", "run_id": exc.run_id},
            ) from exc
        except ProviderResponseError as exc:
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "provider_response_failed",
                    "run_id": exc.run_id,
                    "provider_error": exc.error,
                },
            ) from exc
        except PermissionError as exc:
            raise HTTPException(
                status_code=403,
                detail={"error": "organization_access_denied", "message": str(exc)},
            ) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail={"error": "invalid_backlink_refresh", "message": str(exc)},
            ) from exc

    @app.post(
        "/collections",
        response_model=CollectionReceipt,
        dependencies=[Depends(require_authenticated)],
    )
    async def create_collection(
        body: CollectionCreateRequest,
        request: Request,
        ctx: AppContext = Depends(context_dep),
    ) -> CollectionReceipt:
        factory = ADAPTER_FACTORIES.get(body.provider)
        if factory is None:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "unknown_provider",
                    "provider": body.provider,
                    "known_providers": sorted(ADAPTER_FACTORIES),
                },
            )
        collection = CollectionRequest(
            organization_id=body.organization_id,
            created_by=ctx.user_id,
            capability=body.capability,
            operation=body.operation,
            target_ref=body.target_ref,
            site_id=body.site_id,
            page_id=body.page_id,
            source_crawl_session_id=body.source_crawl_session_id,
            observation_period=body.observation_period,
            settings=body.settings,
            trigger=body.trigger,
            credential_reference_id=body.credential_reference_id,
            credential_reference_kind=body.credential_reference_kind,
            request_id=body.request_id,
            execution_id=body.execution_id,
            resume_existing=body.resume_existing,
            force_refresh=body.force_refresh,
        )
        workflow = body.settings.get("workflow") if isinstance(body.settings, dict) else None
        logger.info(
            "collection start provider=%s operation=%s workflow=%s target_ref=%s "
            "org=%s user=%s force_refresh=%s",
            body.provider,
            body.operation,
            workflow,
            body.target_ref,
            body.organization_id,
            ctx.user_id,
            body.force_refresh,
        )
        try:
            receipt = await _service(request).collect(factory(), collection)
            logger.info(
                "collection done run_id=%s from_cache=%s reused=%s observations=%s",
                receipt.run_id,
                receipt.from_cache,
                receipt.reused_completed_run,
                receipt.created_observations + receipt.existing_observations,
            )
            return receipt
        except SecretNotFoundError as exc:
            # A missing provider key is the CALLER's configuration gap, not a
            # server fault — a 500 + traceback tells them nothing. Name the key
            # and where to add it. (Same class as SecretDecryptError below.)
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "provider_credential_missing",
                    "provider": body.provider,
                    "message": str(exc),
                    "fix": (
                        f"Add the {body.provider} API key to your secrets vault "
                        "(Settings → Secrets), then run this collection again."
                    ),
                },
            ) from exc
        except SecretDecryptError as exc:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": "provider_credential_undecryptable",
                    "provider": body.provider,
                    "message": str(exc),
                    "fix": (
                        "This secret was encrypted with a different key and cannot be "
                        "read. Re-save it in Settings → Secrets."
                    ),
                },
            ) from exc
        except CollectionInProgressError as exc:
            raise HTTPException(
                status_code=409,
                detail={"error": "collection_in_progress", "run_id": exc.run_id},
            ) from exc
        except ProviderResponseError as exc:
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "provider_response_failed",
                    "run_id": exc.run_id,
                    "provider_error": exc.error,
                },
            ) from exc
        except PermissionError as exc:
            raise HTTPException(
                status_code=403,
                detail={"error": "organization_access_denied", "message": str(exc)},
            ) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail={"error": "invalid_collection_request", "message": str(exc)},
            ) from exc

    @app.get(
        "/collections/{run_id}",
        response_model=RunStatusResponse,
        dependencies=[Depends(require_authenticated)],
    )
    async def get_collection(
        run_id: UUID,
        request: Request,
        ctx: AppContext = Depends(context_dep),
    ) -> RunStatusResponse:
        _service(request)
        row = await _visible_run(run_id, ctx)
        return await run_status_response(OrmSeoRepository(), row)

    @app.get(
        "/collections/{run_id}/evidence",
        response_model=RunEvidenceResponse,
        dependencies=[Depends(require_authenticated)],
    )
    async def collection_evidence(
        run_id: UUID,
        request: Request,
        ctx: AppContext = Depends(context_dep),
    ) -> RunEvidenceResponse:
        _service(request)
        row = await _visible_run(run_id, ctx)
        return await run_evidence_response(row)

    @app.get(
        "/collections",
        response_model=RunListResponse,
        dependencies=[Depends(require_authenticated)],
    )
    async def list_collections(
        request: Request,
        organization_id: str = Query(min_length=1),
        limit: int = Query(default=25, ge=1, le=100),
        ctx: AppContext = Depends(context_dep),
    ) -> RunListResponse:
        """LIST gate — DEF-12/WS-5: bounded by ``organization_id`` for query
        scope, then narrowed to ``iam.is_discoverable`` per row so a run only
        contextually reachable (never a deliberate grant) does not leak into
        this enumeration — see ``common-docs/systems/platform/access/CONTEXTUAL_ACCESS.md``."""
        _service(request)
        from matrx_seo.api_contracts import discoverable_run_status_page

        return RunListResponse(
            organization_id=organization_id,
            runs=await discoverable_run_status_page(
                OrmSeoRepository(), ctx.user_id, organization_id=organization_id, limit=limit
            ),
        )

    @app.post("/auth/login", response_model=LoginResponse)
    async def login(body: LoginRequest) -> LoginResponse:
        """Server-side sign-in so the console talks to ONE origin.

        A browser call straight to Supabase works, but any ad blocker, privacy
        extension, or corporate proxy that filters third-party requests turns it
        into an opaque ``TypeError: Failed to fetch`` the user cannot act on.
        Proxying here removes the cross-origin hop AND keeps the publishable key
        out of the page. Credentials are forwarded, never stored or logged."""
        import httpx

        base = (
            os.environ.get("SUPABASE_MATRIX_URL") or os.environ.get("SUPABASE_URL") or ""
        ).rstrip("/")
        key = os.environ.get("SUPABASE_MATRIX_PUBLISHABLE_KEY", "")
        if not base or not key:
            raise HTTPException(
                status_code=503,
                detail={
                    "error": "auth_not_configured",
                    "message": "This deployment is missing SUPABASE_MATRIX_URL / "
                    "SUPABASE_MATRIX_PUBLISHABLE_KEY.",
                },
            )
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.post(
                    f"{base}/auth/v1/token?grant_type=password",
                    headers={"apikey": key, "Content-Type": "application/json"},
                    json={"email": body.email, "password": body.password},
                )
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "auth_unreachable",
                    "message": f"Could not reach the sign-in service: {exc}",
                },
            ) from exc
        data = resp.json() if resp.content else {}
        token = data.get("access_token")
        if not token:
            raise HTTPException(
                status_code=401,
                detail={
                    "error": "sign_in_failed",
                    "message": data.get("error_description") or data.get("msg") or "Sign-in failed",
                },
            )
        return LoginResponse(
            access_token=token,
            user_id=str((data.get("user") or {}).get("id") or ""),
            email=str((data.get("user") or {}).get("email") or body.email),
        )

    @app.get("/me", response_model=WhoAmIResponse, dependencies=[Depends(require_authenticated)])
    async def whoami(ctx: AppContext = Depends(context_dep)) -> WhoAmIResponse:
        """Identity + the org the console should scope to: the one the request
        was admitted for, else the person's ONLY organization (the platform's
        sole-membership rule). Several and none selected answers with an empty
        organization — nothing here guesses between them."""
        org = ctx.organization_id
        if not org:
            from matrx_orm import call_function

            rows = await call_function(
                PACKAGE_DB_NAME, "public", "get_user_organizations", ctx.user_id, mode="rows"
            )
            ids = {str(row["id"]) for row in rows or []}
            org = next(iter(ids)) if len(ids) == 1 else None
        return WhoAmIResponse(user_id=ctx.user_id, organization_id=org or "")

    @app.get(
        "/collections/{run_id}/observations",
        response_model=RunObservationsResponse,
        dependencies=[Depends(require_authenticated)],
    )
    async def run_observations(
        run_id: UUID, ctx: AppContext = Depends(context_dep)
    ) -> RunObservationsResponse:
        """The rank rows a run produced — what the console renders."""
        from matrx_seo.db import models_seo as m

        await _visible_run(run_id, ctx)
        obs = await m.RankObservation.filter(run_id=str(run_id)).order_by("organic_rank").all()
        return RunObservationsResponse(
            run_id=str(run_id),
            observations=[
                RankObservationOut(
                    organic_rank=o.organic_rank,
                    absolute_rank=o.absolute_rank,
                    matched_domain=o.matched_domain,
                    matched_url=o.matched_url,
                    engine=o.engine,
                    device=o.device,
                    observed_at=o.observed_at,
                )
                for o in obs
            ],
        )

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def console() -> HTMLResponse:
        """The operator console — a self-contained page. Config is injected
        server-side so the page ships no secrets and needs no build step."""
        html = _CONSOLE_HTML.read_text(encoding="utf-8")
        cfg = json.dumps(
            {
                "supabaseUrl": (
                    os.environ.get("SUPABASE_MATRIX_URL") or os.environ.get("SUPABASE_URL") or ""
                ).rstrip("/"),
                "supabaseKey": os.environ.get("SUPABASE_MATRIX_PUBLISHABLE_KEY", ""),
            }
        )
        injected = f"<script>window.__SEO_CFG__={cfg}</script></head>"
        return HTMLResponse(html.replace("</head>", injected))

    return app
