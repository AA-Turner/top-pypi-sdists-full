"""Cross-cutting infrastructure modules.

Emits the load-bearing files that EVERY production backend needs but
that aren't tied to a specific feature: auth middleware, DB session
dependency injection, Celery worker entrypoint, global exception
handlers, rate limiting, structured logging, multi-tenant context,
alembic configuration, etc.

The principal-engineer rule: features should be thin vertical slices
on top of a robust horizontal layer. This module IS that horizontal
layer.

A feature's API file should ALREADY have `Depends(get_current_user)`,
`Depends(get_session)`, `Depends(get_tenant_id)`, and a global
exception handler that turns the service's `NotFoundError` into HTTP
404. None of that works unless the cross-cutting modules exist.
"""

from __future__ import annotations

from sage.core.project_layout import FileSlot
from sage.core.spec_decomposer import ProjectPlan, StackProfile


# ──────────────────────── backend infra ─────────────────────────────────


def _fastapi_infra_files(stack: StackProfile) -> list[FileSlot]:
    needs_celery = stack.queue == "celery" or True  # ad platform always wants it
    needs_redis = stack.cache == "redis"
    needs_postgres = stack.database in {"postgres", None}  # default to postgres

    files: list[FileSlot] = [
        # ── Core db / session layer ─────────────────────────────────
        FileSlot(
            path="backend/app/db/__init__.py",
            role="DB package marker.",
            language="python",
            template="",
        ),
        FileSlot(
            path="backend/app/db/base.py",
            role=(
                "Async SQLAlchemy/SQLModel engine + sessionmaker factory. "
                "Reads DATABASE_URL from settings. Provides a Base declarative "
                "metadata class that ALL models inherit from. Includes the "
                "async_session_factory used by Depends(get_session)."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/db/session.py",
            role=(
                "FastAPI `get_session` dependency. Yields an AsyncSession, "
                "commits on success, rolls back on exception, closes always. "
                "Wraps the session factory from db/base.py."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/db/seed.py",
            role=(
                "Idempotent seed script for development data: default tenant, "
                "an admin user, sample subscription plan. Run via "
                "`python -m app.db.seed`. Safe to re-run."
            ),
            language="python",
        ),

        # ── Configuration ───────────────────────────────────────────
        FileSlot(
            path="backend/app/core/__init__.py",
            role="Core package marker.",
            language="python",
            template="",
        ),
        FileSlot(
            path="backend/app/core/config.py",
            role=(
                "pydantic-settings Settings class. CRITICAL: every field MUST have "
                "a default value so tests work without a .env file. "
                "Fields with defaults: "
                "PROJECT_NAME: str = 'App', "
                "API_V1_STR: str = '/api/v1', "
                "DATABASE_URL: str = 'sqlite+aiosqlite:///./dev.db', "
                "REDIS_URL: str = 'redis://localhost:6379/0', "
                "JWT_SECRET: str = 'dev-secret-change-in-prod', "
                "JWT_ALGORITHM: str = 'HS256', "
                "JWT_ACCESS_MINUTES: int = 30, "
                "JWT_REFRESH_DAYS: int = 7, "
                "CELERY_BROKER_URL: str = 'redis://localhost:6379/1', "
                "CELERY_RESULT_BACKEND: str = 'redis://localhost:6379/2', "
                "OPENAI_API_KEY: str = 'sk-placeholder', "
                "STRIPE_API_KEY: Optional[str] = None, "
                "CORS_ORIGINS: List[str] = Field(default_factory=list), "
                "ENVIRONMENT: str = 'development', "
                "LOG_LEVEL: str = 'INFO', "
                "SENTRY_DSN: Optional[str] = None. "
                "Use BaseSettings with env_file='.env', extra='ignore', "
                "case_sensitive=False. Cache via lru_cache. "
                "Expose get_settings() function."
            ),
            language="python",
            must_contain=["BaseSettings", "get_settings", "lru_cache", "database_url"],
        ),
        FileSlot(
            path="backend/app/core/logging.py",
            role=(
                "structlog setup with JSON output in production, pretty "
                "console output in dev. Includes a request_id processor that "
                "reads contextvars set by request_id middleware. Exposes "
                "`get_logger(name)`."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/core/security.py",
            role=(
                "JWT encode/decode helpers using python-jose with HS256. "
                "create_access_token(subject, claims), create_refresh_token, "
                "decode_token (raises ExpiredSignatureError / "
                "InvalidTokenError). Password hashing via passlib bcrypt: "
                "hash_password, verify_password. Constants pulled from settings."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/core/exceptions.py",
            role=(
                "Application exception hierarchy. AppError base, NotFoundError, "
                "PermissionError, ValidationError, ConflictError, "
                "RateLimitedError, IntegrationError. Each maps to an HTTP status "
                "in the global handler. Services raise these — NEVER HTTPException."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/core/exception_handlers.py",
            role=(
                "FastAPI exception handlers wired in main.py via "
                "app.add_exception_handler. Translates each AppError subclass "
                "to a JSONResponse with {error: {code, message, details}}. "
                "Logs full traceback for 5xx, summary for 4xx."
            ),
            language="python",
        ),

        # ── Auth ────────────────────────────────────────────────────
        FileSlot(
            path="backend/app/auth/__init__.py",
            role="Auth package marker.",
            language="python",
            template="",
        ),
        FileSlot(
            path="backend/app/auth/dependencies.py",
            role=(
                "FastAPI dependencies: get_current_user (extracts JWT from "
                "Authorization Bearer header, decodes, loads user from db), "
                "require_role(role_name) factory, get_current_tenant_id "
                "(reads tenant_id from user OR X-Tenant-ID header if user "
                "has multi-tenant access). All async."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/auth/oauth.py",
            role=(
                "OAuth2 authorization-code flow handlers for Google + the "
                "social platforms in the spec (Instagram, Facebook, etc.). "
                "Uses authlib. Token storage is encrypted at rest "
                "(see core/security.py.encrypt_credential). State param "
                "stored in Redis for CSRF protection."
            ),
            language="python",
        ),

        # ── Middleware ──────────────────────────────────────────────
        FileSlot(
            path="backend/app/middleware/__init__.py",
            role="Middleware package marker.",
            language="python",
            template="",
        ),
        FileSlot(
            path="backend/app/middleware/request_id.py",
            role=(
                "ASGI middleware that generates a UUID4 request_id for every "
                "request and stashes it in a contextvar so logging picks it up. "
                "Also returns the id in the X-Request-Id response header."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/middleware/rate_limit.py",
            role=(
                "SlowAPI Limiter instance + helper to apply per-route limits. "
                "Default: 100 req / 15 min per IP, 1000 / 15 min per "
                "authenticated user. Stored in Redis."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/middleware/security_headers.py",
            role=(
                "ASGI middleware adding standard security headers: "
                "X-Content-Type-Options=nosniff, X-Frame-Options=DENY, "
                "Strict-Transport-Security, Referrer-Policy=same-origin, "
                "Permissions-Policy, Content-Security-Policy."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/middleware/tenant.py",
            role=(
                "Multi-tenant context middleware. Extracts tenant_id from the "
                "authenticated user OR the X-Tenant-Id header, stores it in "
                "a contextvar, and rejects cross-tenant access in the "
                "repository layer."
            ),
            language="python",
        ),

        # ── Webhooks ────────────────────────────────────────────────
        FileSlot(
            path="backend/app/webhooks/__init__.py",
            role="Webhooks package marker.",
            language="python",
            template="",
        ),
        FileSlot(
            path="backend/app/webhooks/dispatcher.py",
            role=(
                "FastAPI router at /webhooks/{provider}. Verifies signature "
                "per provider (Stripe, Meta, Slack, etc.) using svix or "
                "provider-specific HMAC. Dispatches to registered handlers. "
                "Returns 200 OK even on handler failure (per webhook etiquette) "
                "but enqueues retry tasks for failed handlers."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/webhooks/handlers.py",
            role=(
                "Webhook handlers: stripe_event, meta_change, slack_event, "
                "google_ads_change, etc. Each is a Celery task that processes "
                "the verified webhook payload."
            ),
            language="python",
        ),

        # ── AI prompt engine (shared across features) ───────────────
        FileSlot(
            path="backend/app/ai/__init__.py",
            role="AI package marker.",
            language="python",
            template="",
        ),
        FileSlot(
            path="backend/app/ai/client.py",
            role=(
                "Unified LLM client wrapping OpenAI + Anthropic via env config. "
                "generate(prompt, model, temperature, max_tokens) returns str. "
                "Handles rate limits, retries with exponential backoff, logs "
                "token usage for billing."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/ai/prompts.py",
            role=(
                "Reusable Jinja2 prompt templates per use case from spec §13: "
                "ad_campaign, social_caption, blog_post, seo_brief, "
                "landing_page, email_campaign, push_notification, video_script, "
                "influencer_outreach, competitor_analysis, growth_strategy, "
                "performance_report. Each is a function returning the "
                "fully-rendered prompt."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/ai/segmentation.py",
            role=(
                "Audience segmentation engine. Clusters users via "
                "scikit-learn KMeans on behavioural features. "
                "Returns labelled segments + suggested ad targeting parameters."
            ),
            language="python",
        ),
        FileSlot(
            path="backend/app/ai/scoring.py",
            role=(
                "Predictive campaign-performance scorer. sklearn regression "
                "predicting CTR + ROAS from campaign attributes + historical "
                "performance. Returns score 0-100 + feature importances."
            ),
            language="python",
        ),
    ]

    # ── Celery worker ───────────────────────────────────────────────
    if needs_celery:
        files.extend([
            FileSlot(
                path="backend/app/tasks/__init__.py",
                role="Tasks package marker.",
                language="python",
                template="",
            ),
            FileSlot(
                path="backend/app/tasks/celery_app.py",
                role=(
                    "Celery app factory. Reads CELERY_BROKER_URL + "
                    "CELERY_RESULT_BACKEND from settings. Configures task "
                    "discovery to auto-import every module under app/tasks. "
                    "Sets task_acks_late=True, task_reject_on_worker_lost=True."
                ),
                language="python",
            ),
            FileSlot(
                path="backend/app/tasks/beat_schedule.py",
                role=(
                    "celery beat periodic-task schedule: hourly campaign "
                    "performance refresh, daily audience segment recompute, "
                    "weekly performance report email, every-5-minute social "
                    "inbox sync."
                ),
                language="python",
            ),
            FileSlot(
                path="backend/worker.py",
                role=(
                    "Celery worker entrypoint: `from app.tasks.celery_app "
                    "import celery_app as app`. Run via "
                    "`celery -A worker worker --loglevel=info`."
                ),
                language="python",
            ),
        ])

    # ── Alembic migrations ──────────────────────────────────────────
    if needs_postgres:
        files.extend([
            FileSlot(
                path="backend/alembic.ini",
                role=(
                    "alembic config. sqlalchemy.url uses an env variable "
                    "interpolation: `${DATABASE_URL}`. Script location: "
                    "`alembic/`."
                ),
                language="ini",
            ),
            FileSlot(
                path="backend/alembic/env.py",
                role=(
                    "alembic env.py loading app.core.config.settings and "
                    "app.db.base.Base.metadata for autogenerate. Async mode "
                    "via run_async_migrations."
                ),
                language="python",
            ),
            FileSlot(
                path="backend/alembic/script.py.mako",
                role="alembic migration template.",
                language="python",
                template=_ALEMBIC_SCRIPT_MAKO,
            ),
            FileSlot(
                path="backend/alembic/versions/.gitkeep",
                role="placeholder so the empty versions dir is tracked",
                language="markdown",
                template="",
            ),
        ])

    # ── Observability ───────────────────────────────────────────────
    files.append(
        FileSlot(
            path="backend/app/observability/__init__.py",
            role="Observability package marker.",
            language="python",
            template="",
        ),
    )
    files.append(
        FileSlot(
            path="backend/app/observability/metrics.py",
            role=(
                "Prometheus metrics: request counter, request duration "
                "histogram, AI tokens-consumed counter, Celery task counter. "
                "Exposed at /metrics by main.py."
            ),
            language="python",
        ),
    )

    # ── Canonical User model (single source of truth) ──────────────
    files.extend([
        FileSlot(
            path="backend/app/models/__init__.py",
            role=(
                "Re-export ONLY the canonical models from this package. "
                "MUST contain exactly: `from .user import User`. "
                "Do NOT invent other imports. Do NOT import from non-existent files."
            ),
            language="python",
            must_contain=["from .user import User"],
            must_not_contain=["from app import", "from .auth import User",
                              "from .asset_management import User",
                              "from .user_profile_management import User"],
        ),
        FileSlot(
            path="backend/app/models/user.py",
            role=(
                "CANONICAL User model — the only definition of the User database table. "
                "SQLModel(table=True) with: id (UUID PK, default uuid4), email (str, unique, "
                "indexed), hashed_password (str), full_name (Optional[str]), role "
                "(str, default 'user'), is_active (bool, default True), tenant_id "
                "(Optional[UUID], indexed), created_at (datetime, default utcnow), "
                "updated_at (Optional[datetime]). "
                "ONLY import from: sqlmodel, sqlalchemy, uuid, datetime, typing. "
                "Do NOT import from other app.models files. "
                "Table name must be 'user' (__tablename__ = 'user')."
            ),
            language="python",
            must_contain=[
                "class User(SQLModel, table=True)",
                "email",
                "hashed_password",
                "__tablename__",
            ],
            must_not_contain=[
                "from app.models", "from .auth import", "from .asset",
                "class User(Auth", "class User(Base",
            ],
        ),
    ])

    # ── FastAPI app entry point ─────────────────────────────────────
    files.append(
        FileSlot(
            path="backend/app/main.py",
            role=(
                "FastAPI application factory. "
                "1. Import Settings instance: `from app.core.config import Settings; "
                "_settings = Settings()` — DO NOT access class attributes (Settings.FIELD). "
                "2. Include all feature routers from `from app.api.routes import api_router`. "
                "3. CORSMiddleware using _settings.CORS_ORIGINS. "
                "4. Exception handlers for every AppError subclass. "
                "5. /health endpoint returning {'ok': True}. "
                "6. lifespan context manager (do NOT use @app.on_event). "
                "app = FastAPI(lifespan=lifespan, title=_settings.PROJECT_NAME)."
            ),
            language="python",
            must_contain=[
                "FastAPI",
                "_settings = Settings()",
                "CORSMiddleware",
                "api_router",
                "/health",
                "@asynccontextmanager",
            ],
            must_not_contain=[
                "Settings.PROJECT_NAME",
                "Settings.API_V1_STR",
                "Settings.CORS",
                "@app.on_event",
                "from app.models.user import User",  # main.py doesn't need to import User
            ],
        )
    )

    # ── Main API router (wires all feature routers) ─────────────────
    files.extend([
        FileSlot(
            path="backend/app/api/__init__.py",
            role="API package marker.",
            language="python",
            template="",
        ),
        FileSlot(
            path="backend/app/api/routes.py",
            role=(
                "CRITICAL: Main API router. Use importlib with try/except to load each "
                "router module safely — this prevents one broken router from crashing the app. "
                "Pattern:\n"
                "```python\n"
                "from fastapi import APIRouter\n"
                "import importlib, logging\n"
                "logger = logging.getLogger(__name__)\n"
                "api_router = APIRouter()\n"
                "\n"
                "_MODULES = [\n"
                "    ('app.api.v1.health',    '/health',    ['health']),\n"
                "    # ADD MORE MODULES HERE using the EXACT filenames from app/api/v1/\n"
                "]\n"
                "for path, prefix, tags in _MODULES:\n"
                "    try:\n"
                "        mod = importlib.import_module(path)\n"
                "        router = getattr(mod, 'router', None)\n"
                "        if router: api_router.include_router(router, prefix=prefix, tags=tags)\n"
                "    except Exception as e:\n"
                "        logger.warning('Skipping %s: %s', path, e)\n"
                "```\n"
                "Use the EXACT filenames from app/api/v1/ — do NOT invent singular names. "
                "If the file is named campaigns.py use 'campaigns', if it is campaign_cruds.py "
                "use 'campaign_cruds'. Never add routers that do not exist as files. "
                "Include all v1 modules you create."
            ),
            language="python",
            must_contain=[
                "api_router = APIRouter()",
                "importlib",
                "include_router",
            ],
            must_not_contain=["# All routes commented out", "# TODO"],
        ),
    ])

    # ── conftest.py for tests ───────────────────────────────────────
    files.append(
        FileSlot(
            path="backend/tests/conftest.py",
            role=(
                "pytest conftest.py for the backend test suite. "
                "MUST use in-memory SQLite for tests (never PostgreSQL): "
                "`DATABASE_URL = 'sqlite+aiosqlite:///:memory:'`. "
                "Fixtures: event_loop (session scope), engine (create_all), "
                "db_session (AsyncSession from the test engine), "
                "client (AsyncClient with app, base_url). "
                "Import SQLModel from sqlmodel and run conn.run_sync(SQLModel.metadata.create_all). "
                "Do NOT import Base or anything else from app.models (it is empty)."
            ),
            language="python",
            must_contain=[
                "sqlite+aiosqlite",
                "AsyncSession",
                "pytest",
                "AsyncClient",
            ],
            must_not_contain=[
                "postgresql://",
                "postgres://",
                "asyncpg",
                "from app.models import Base",
            ],
        )
    )

    # ── Health endpoints ────────────────────────────────────────────
    files.append(
        FileSlot(
            path="backend/app/api/v1/__init__.py",
            role="v1 API package marker.",
            language="python",
            template="",
        ),
    )
    files.append(
        FileSlot(
            path="backend/app/api/v1/health.py",
            role=(
                "Health, readiness, liveness probes. "
                "GET /health returns {ok: true}. "
                "GET /ready checks DB + Redis + Celery broker. "
                "GET /live always returns 200 unless the event loop is dead."
            ),
            language="python",
        ),
    )

    # ── Tests for the cross-cutting layer ───────────────────────────
    files.extend([
        FileSlot(
            path="backend/tests/integration/test_auth_dependencies.py",
            role=(
                "Tests get_current_user happy path, expired token, missing "
                "token, malformed token, require_role enforcement."
            ),
            language="python",
            is_test=True,
        ),
        FileSlot(
            path="backend/tests/integration/test_exception_handlers.py",
            role=(
                "Tests that each AppError subclass maps to its expected HTTP "
                "status and that 5xx errors include a request_id in the body."
            ),
            language="python",
            is_test=True,
        ),
        FileSlot(
            path="backend/tests/integration/test_health.py",
            role="Tests /health returns ok, /ready 200 when deps reachable.",
            language="python",
            is_test=True,
        ),
        FileSlot(
            path="backend/tests/integration/test_rate_limit.py",
            role="Tests rate limit middleware returns 429 after threshold.",
            language="python",
            is_test=True,
        ),
    ])

    return files


_ALEMBIC_SCRIPT_MAKO = '''\
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
'''


# ──────────────────────── frontend infra ────────────────────────────────


def _rnw_infra_files() -> list[FileSlot]:
    return [
        FileSlot(
            path="frontend/src/shared/api.ts",
            role=(
                "Shared axios instance. baseURL from EXPO_PUBLIC_API_URL. "
                "Request interceptor injects Authorization Bearer from "
                "expo-secure-store. Response interceptor handles 401 → "
                "refresh token flow, 429 → exponential backoff. Wraps "
                "errors in typed ApiError."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/src/shared/queryClient.ts",
            role=(
                "React Query QueryClient with sensible defaults: "
                "staleTime 30s, gcTime 5min, retry 2 with exponential "
                "backoff, refetchOnWindowFocus true on web."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/src/shared/errors.ts",
            role=(
                "Typed error helpers. parseApiError(err) maps the backend's "
                "{error: {code, message}} into a discriminated union. "
                "User-facing message via getDisplayMessage()."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/src/shared/auth.tsx",
            role=(
                "AuthProvider context. Stores tokens in expo-secure-store "
                "(native) / localStorage (web via Platform.OS branch). "
                "Exposes useAuth() → { user, signIn, signUp, signOut, "
                "refresh }."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/src/shared/theme.ts",
            role=(
                "Design tokens: colors (primary, secondary, danger, success, "
                "neutrals 50-900), spacing (4, 8, 12, 16, 24, 32, 48, 64), "
                "fontSize (xs, sm, base, lg, xl, 2xl, 3xl, 4xl), radii, "
                "shadows. Light + dark variants."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/src/components/ui/Button.tsx",
            role=(
                "Cross-platform Pressable button with primary/secondary/"
                "destructive/ghost variants, sizes sm/md/lg, loading + "
                "disabled states. Uses StyleSheet.create with theme tokens."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/src/components/ui/TextField.tsx",
            role=(
                "Labelled TextInput with error state, helper text, prefix/"
                "suffix slots. Forwards refs for react-hook-form. Focus ring."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/src/components/ui/EmptyState.tsx",
            role="Empty state with icon, title, body, optional CTA button.",
            language="typescript",
        ),
        FileSlot(
            path="frontend/src/components/ui/ErrorBoundary.tsx",
            role=(
                "React error boundary that catches render errors and shows "
                "a fallback. Reports to Sentry if configured."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/src/hooks/useResponsive.ts",
            role=(
                "useResponsive() → { isPhone, isTablet, isDesktop } via "
                "useWindowDimensions breakpoints (640, 1024)."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/app/_layout.tsx",
            role=(
                "Root expo-router Stack. Wraps in SafeAreaProvider, "
                "GestureHandlerRootView, QueryClientProvider, AuthProvider, "
                "ErrorBoundary. Splash screen until fonts loaded."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/app/(auth)/_layout.tsx",
            role="expo-router Stack for unauthenticated routes (login, register).",
            language="typescript",
        ),
        FileSlot(
            path="frontend/app/(auth)/login.tsx",
            role=(
                "Login screen — email + password, useAuth().signIn, "
                "loading + error states, Pressable to navigate to register."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/app/(auth)/register.tsx",
            role="Register screen with confirm-password validation.",
            language="typescript",
        ),
        FileSlot(
            path="frontend/app/(tabs)/_layout.tsx",
            role=(
                "Authenticated Tabs layout. Tabs: dashboard, campaigns, "
                "social, content, analytics, settings. Icons via "
                "@expo/vector-icons. Hidden on signed-out state via "
                "Redirect to /(auth)/login."
            ),
            language="typescript",
        ),
        FileSlot(
            path="frontend/__tests__/shared/auth.test.tsx",
            role="Tests AuthProvider sign-in flow, token persistence.",
            language="typescript",
            is_test=True,
        ),
        FileSlot(
            path="frontend/__tests__/components/ui/Button.test.tsx",
            role="Tests Button variants render + onPress fires.",
            language="typescript",
            is_test=True,
        ),
    ]


# ──────────────────────── deployment artifacts ──────────────────────────


def _deployment_files(stack: StackProfile) -> list[FileSlot]:
    files: list[FileSlot] = []
    files.append(
        FileSlot(
            path="deploy/k8s/namespace.yaml",
            role=(
                "k8s Namespace + NetworkPolicy isolating the app from "
                "other namespaces."
            ),
            language="yaml",
        ),
    )
    files.append(
        FileSlot(
            path="deploy/k8s/backend.yaml",
            role=(
                "k8s Deployment + Service + HorizontalPodAutoscaler for "
                "the backend. Liveness probe → /live, readiness → /ready. "
                "Resource requests/limits set. envFrom Secret + ConfigMap."
            ),
            language="yaml",
        ),
    )
    if stack.queue == "celery":
        files.append(
            FileSlot(
                path="deploy/k8s/celery.yaml",
                role=(
                    "Celery worker + beat Deployments. Worker scales on CPU "
                    "+ queue depth (KEDA). Beat is a singleton "
                    "(replicas: 1, strategy: Recreate)."
                ),
                language="yaml",
            ),
        )
    if stack.frontend:
        files.append(
            FileSlot(
                path="deploy/k8s/frontend.yaml",
                role=(
                    "k8s Deployment + Service for the frontend web build "
                    "served via Caddy/nginx."
                ),
                language="yaml",
            ),
        )
    files.append(
        FileSlot(
            path="deploy/k8s/ingress.yaml",
            role=(
                "Ingress with TLS via cert-manager. Routes /api/* → backend "
                "Service, everything else → frontend Service."
            ),
            language="yaml",
        ),
    )
    files.append(
        FileSlot(
            path="deploy/k8s/secrets.example.yaml",
            role=(
                "Example Secret manifest. ACTUAL secrets come from "
                "External-Secrets-Operator + AWS Secrets Manager / Vault."
            ),
            language="yaml",
        ),
    )
    files.append(
        FileSlot(
            path="deploy/terraform/main.tf",
            role=(
                "Terraform skeleton: VPC, EKS cluster, RDS Postgres, "
                "ElastiCache Redis, S3 for media, CloudFront CDN. "
                "Outputs cluster endpoint + DB DSN."
            ),
            language="yaml",
        ),
    )
    return files


# ──────────────────────── public entry ─────────────────────────────────


def _bun_infra_files(stack: "StackProfile") -> list["FileSlot"]:
    """Additional files when js_runtime='bun' is specified.

    Bun.js is a fast JavaScript runtime that replaces Node.js:
    - `bun install` instead of `npm install`
    - `bun run` / `bun build` instead of `npm run` / `webpack`
    - Docker image: `oven/bun:1` (NOT `node:`)
    - BullMQ workers run under Bun for background job processing
    - SSR server: `bun --watch src/web/ssr.tsx`
    """
    files = [
        FileSlot(
            path="frontend/src/web/ssr.tsx",
            role=(
                "Bun SSR entry point for server-side rendering of React Native Web components. "
                "Uses Bun's built-in HTTP server: `Bun.serve({ fetch(req) { ... } })`. "
                "Renders the React Native Web app to HTML string using `renderToString`. "
                "Serves static assets and handles hydration. "
                "Pattern:\n"
                "```ts\n"
                "import { renderToString } from 'react-dom/server';\n"
                "import App from '../App';\n"
                "Bun.serve({\n"
                "  port: process.env.PORT || 3000,\n"
                "  async fetch(req) {\n"
                "    const html = renderToString(<App />);\n"
                "    return new Response(`<!DOCTYPE html><html><body>${html}</body></html>`,\n"
                "      { headers: { 'Content-Type': 'text/html' } });\n"
                "  }\n"
                "});\n"
                "```"
            ),
            language="typescript",
        ),
    ]

    # BullMQ worker template when queue="bullmq"
    if stack.queue == "bullmq":
        files.append(FileSlot(
            path="workers/queue_worker.ts",
            role=(
                "BullMQ worker running under Bun. Processes background jobs from Redis queue. "
                "BullMQ is a Redis-based job queue for Node.js / Bun (TypeScript). "
                "Pattern:\n"
                "```ts\n"
                "import { Worker, Queue } from 'bullmq';\n"
                "import IORedis from 'ioredis';\n"
                "const connection = new IORedis(process.env.REDIS_URL || 'redis://localhost:6379');\n"
                "export const adQueue = new Queue('ad-processing', { connection });\n"
                "const worker = new Worker('ad-processing', async (job) => {\n"
                "  const { type, payload } = job.data;\n"
                "  if (type === 'generate-video') { /* call FFmpeg / RunwayML API */ }\n"
                "  if (type === 'publish-ad') { /* call social media API */ }\n"
                "  return { status: 'done' };\n"
                "}, { connection });\n"
                "worker.on('completed', (job) => console.log(`Job ${job.id} done`));\n"
                "worker.on('failed', (job, err) => console.error(err));\n"
                "```\n"
                "Add bullmq and ioredis to package.json dependencies."
            ),
            language="typescript",
        ))

    return files


def architecture_files(plan: ProjectPlan) -> list[FileSlot]:
    """All cross-cutting infrastructure files for a project plan.

    These are emitted ONCE per project (not per feature). Together with
    the per-feature files from `feature_files.files_for_feature`, they
    form the complete principal-engineer scaffold.
    """
    import os
    files: list[FileSlot] = []
    if plan.stack.backend in {"fastapi", "django", "flask"}:
        files.extend(_fastapi_infra_files(plan.stack))
    if plan.stack.frontend == "react-native-web":
        files.extend(_rnw_infra_files())
    # Bun.js: add SSR entry + BullMQ worker files
    if getattr(plan.stack, "js_runtime", "node") == "bun":
        files.extend(_bun_infra_files(plan.stack))
    files.extend(_deployment_files(plan.stack))
    return files


__all__ = ["architecture_files"]
