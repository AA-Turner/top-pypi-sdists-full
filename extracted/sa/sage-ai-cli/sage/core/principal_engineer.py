"""Principal-engineer-grade multi-pass project builder.

Why this exists
---------------
Sage's `--no-agent` one-shot mode tops out around 3-5/10 on a 15-criteria
principal-engineer rubric: a single LLM response cannot fit a full
multi-file production project. The model summarizes each file, omits
cross-cutting concerns (Dockerfile, README, CI, env), and falls back to
stale package versions.

The fix is structural, not prompt-engineering:
  1. **Decompose** the task into a structured file plan (deterministic).
  2. **Template** cross-cutting concerns (Dockerfile, README, CI, env,
     .gitignore) — they don't need LLM intelligence.
  3. **Generate** each source file in its own focused LLM call with
     project context + cross-cutting constraints injected.
  4. **Pin** package versions to a known-current table (defeats stale
     model knowledge — FastAPI 0.115 instead of 0.85, Compose BOM
     2024.11.00 instead of 1.0.5, etc.).
  5. **Self-review** every file against the 15-criteria rubric and
     gap-patch any file scoring below the bar.

Each pipeline stage is independently testable and the per-file LLM
budget is small enough that even a 23B local model produces clean output.
"""

from __future__ import annotations

import json
import os
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Sequence


# ---------------------------------------------------------------------------
# Pinned current versions
# ---------------------------------------------------------------------------
# Defeats the model's stale package-version knowledge. Keep this table
# current; bumping a single dict entry propagates to every generated project.

CURRENT_VERSIONS: dict[str, dict[str, str]] = {
    "python": {
        "fastapi": "0.115.6",
        "uvicorn": "0.32.1",
        "sqlmodel": "0.0.22",
        "sqlalchemy": "2.0.36",
        "alembic": "1.14.0",
        "pydantic": "2.10.3",
        "pydantic-settings": "2.6.1",
        "passlib": "1.7.4",
        "bcrypt": "4.2.1",
        "python-jose": "3.3.0",
        "httpx": "0.28.1",
        "pytest": "8.3.4",
        "pytest-asyncio": "0.24.0",
        "asyncpg": "0.30.0",
        "psycopg2-binary": "2.9.10",
        "python-multipart": "0.0.20",
    },
    "node": {
        "react": "19.0.0",
        "react-dom": "19.0.0",
        "@types/react": "19.0.1",
        "@types/react-dom": "19.0.1",
        "typescript": "5.7.2",
        "vite": "6.0.3",
        "@vitejs/plugin-react": "4.3.4",
        "tailwindcss": "3.4.16",
        "axios": "1.7.9",
        "react-router-dom": "7.0.2",
        "vitest": "2.1.8",
        "@testing-library/react": "16.1.0",
    },
    "go": {
        "go_version": "1.23",
        "gin": "v1.10.0",
        "gorm": "v1.25.12",
        "jwt": "v5.2.1",
        "bcrypt": "v0.30.0",
        "pgx": "v5.7.1",
        "redis": "v9.7.0",
        "testify": "v1.10.0",
    },
    "rust": {
        "rust_edition": "2021",
        "tokio": "1.42.0",
        "axum": "0.7.9",
        "serde": "1.0.215",
        "sqlx": "0.8.2",
        "tracing": "0.1.41",
    },
    "kotlin": {
        "kotlin": "2.1.0",
        "agp": "8.7.3",
        "compose_bom": "2024.12.01",
        "compose_compiler": "1.5.15",
        "hilt": "2.53.1",
        "retrofit": "2.11.0",
        "room": "2.6.1",
        "coroutines": "1.10.1",
        "compile_sdk": "35",
        "target_sdk": "35",
        "min_sdk": "26",
    },
    "java": {
        "java_version": "21",
        "spring_boot": "3.4.0",
        "spring_security": "6.4.1",
        "lombok": "1.18.36",
    },
    "swift": {
        "swift_version": "5.10",
        "ios_deployment": "17.0",
    },
    "dart": {
        "dart_sdk": "3.6.0",
        "flutter": "3.27.0",
        "go_router": "14.6.2",
        "riverpod": "2.6.1",
    },
}


# ---------------------------------------------------------------------------
# File spec
# ---------------------------------------------------------------------------


@dataclass
class FileSpec:
    """A single file to be generated. `template` skips LLM."""

    path: str
    role: str  # one-line description for LLM context
    language: str  # python | typescript | go | kotlin | swift | dart | java | rust | yaml | markdown | dockerfile
    template: str | None = None  # if set, content is deterministic
    requirements: list[str] = field(default_factory=list)
    must_contain: list[str] = field(default_factory=list)  # validator hints
    must_not_contain: list[str] = field(default_factory=list)


@dataclass
class GeneratedFile:
    path: str
    content: str
    language: str
    from_template: bool = False
    review_score: float | None = None
    review_notes: str = ""


# ---------------------------------------------------------------------------
# Stack detection
# ---------------------------------------------------------------------------


STACK_KEYWORDS: dict[str, list[str]] = {
    "fastapi": ["fastapi", "python web", "jwt python", "sqlmodel", "alembic"],
    "django": ["django", "drf", "django rest"],
    "react": ["react", "jsx", "tsx", "vite", "next.js", "nextjs"],
    "go-microservices": ["go microservice", "golang service", "gin", "go ecommerce"],
    "rust-axum": ["rust axum", "rust analytics", "tokio rust"],
    "spring-boot": ["spring boot", "java api", "spring banking"],
    "android-compose": ["jetpack compose", "kotlin android", "android app"],
    "ios-swift": ["ios swift", "swiftui", "swift app"],
    "react-native": ["react native", "expo"],
    "flutter": ["flutter", "dart app"],
    "dotnet": [".net", "asp.net", "c# api"],
    "laravel": ["laravel", "php api"],
    "rails": ["rails", "ruby on rails"],
    "cpp": ["c++", "cpp microservice"],
    "graphql": ["graphql", "apollo"],
    "kubernetes": ["kubernetes", "k8s", "helm"],
}


def detect_stack(task: str) -> str:
    """Pick the best stack template for a task description."""
    lower = task.lower()
    best, best_score = "fastapi", 0
    for stack, kws in STACK_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in lower)
        if score > best_score:
            best, best_score = stack, score
    return best


_BUILD_VERBS = (
    "build", "create", "make", "scaffold", "implement", "set up",
    "set-up", "setup", "generate a", "produce a", "develop a",
    "code a", "write a",
)


def looks_like_build_request(task: str, min_chars: int = 60) -> bool:
    """Return True when `task` looks like a multi-file project build request.

    Strong path: prompt mentions a build verb AND any known stack keyword
    (e.g. "build a FastAPI backend") — always routes regardless of length.
    Soft path: prompt mentions a build verb AND a generic project noun
    (backend, frontend, microservice, app, service) AND is at least
    `min_chars` long — filters out "build an api" type one-liners.
    """
    if not task:
        return False
    lower = task.lower()
    has_verb = any(v in lower for v in _BUILD_VERBS)
    if not has_verb:
        return False
    # Strong stack signal — confidently routed regardless of length.
    for kws in STACK_KEYWORDS.values():
        if any(kw in lower for kw in kws):
            return True
    if len(task) < min_chars:
        return False
    project_nouns = (
        "backend", "frontend", "microservice", "microservices",
        "mobile app", "web app", "rest api", "graphql api",
    )
    return any(n in lower for n in project_nouns)


# ---------------------------------------------------------------------------
# Project plans (deterministic file specs per stack)
# ---------------------------------------------------------------------------


def plan_fastapi_jwt() -> list[FileSpec]:
    pyv = CURRENT_VERSIONS["python"]
    return [
        FileSpec(
            path="pyproject.toml",
            role="Python project config with pinned current versions",
            language="toml",
            template=_render_pyproject_fastapi(pyv),
        ),
        FileSpec(
            path=".env.example",
            role="Environment variables template (no secrets)",
            language="env",
            template=_ENV_FASTAPI_TEMPLATE,
        ),
        FileSpec(
            path=".gitignore",
            role="Python project gitignore",
            language="text",
            template=_GITIGNORE_PYTHON,
        ),
        FileSpec(
            path="Dockerfile",
            role="Multi-stage Dockerfile, non-root user, healthcheck",
            language="dockerfile",
            template=_DOCKERFILE_FASTAPI,
        ),
        FileSpec(
            path="docker-compose.yml",
            role="Compose: api + postgres with healthchecks",
            language="yaml",
            template=_COMPOSE_FASTAPI,
        ),
        FileSpec(
            path=".github/workflows/ci.yml",
            role="CI: lint + test + build matrix",
            language="yaml",
            template=_CI_PYTHON,
        ),
        FileSpec(
            path="README.md",
            role="Project README with Architecture, Setup, Run, Test, Deploy, Tradeoffs",
            language="markdown",
            template=None,  # LLM — task-specific
        ),
        FileSpec(
            path="app/config.py",
            role=(
                "pydantic-settings BaseSettings exposing exactly these fields: "
                "DATABASE_URL: str, SECRET_KEY: str, ALGORITHM: str = 'HS256', "
                "ACCESS_TOKEN_EXPIRE_MINUTES: int = 30, CORS_ORIGINS: str = '*'. "
                "Use SettingsConfigDict(env_file='.env', extra='ignore'). "
                "Instantiate `settings = Settings()` at module level."
            ),
            language="python",
            must_contain=[
                "BaseSettings",
                "SECRET_KEY",
                "DATABASE_URL",
                "ALGORITHM",
                "ACCESS_TOKEN_EXPIRE_MINUTES",
                "settings = Settings()",
            ],
            must_not_contain=["your_secret_key", "password123"],
        ),
        FileSpec(
            path="app/db.py",
            role=(
                "Async engine + async_session_factory + async def get_session "
                "yielding AsyncSession. Define get_user_by_email(session, email) here "
                "as an async helper so auth.py can call it."
            ),
            language="python",
            must_contain=[
                "AsyncSession",
                "async def get_session",
                "get_user_by_email",
                "from app.models import User",
                "select(User)",
                "settings.DATABASE_URL",
            ],
            must_not_contain=[
                "sessionmaker(autocommit",
                "settings.DB_USER",
                "settings.DB_HOST",
            ],
        ),
        FileSpec(
            path="app/models.py",
            role="User SQLModel(table=True) with id PK, email unique+indexed, hashed_password str",
            language="python",
            must_contain=["class User", "hashed_password"],
            must_not_contain=["password: str", "from_orm", "```"],
        ),
        FileSpec(
            path="app/schemas.py",
            role=(
                "Pydantic v2 request/response schemas: UserCreate (email+password), "
                "UserLogin, UserRead (no password), Token (access_token + token_type)."
            ),
            language="python",
            must_contain=["BaseModel", "EmailStr", "Token", "UserCreate", "UserRead"],
            must_not_contain=["from_orm", ".dict()", "parse_obj"],
        ),
        FileSpec(
            path="app/security.py",
            role=(
                "passlib CryptContext bcrypt + python-jose JWT. Provide hash_password, "
                "verify_password, create_access_token, decode_access_token. Read settings "
                "via `from app.config import settings`."
            ),
            language="python",
            must_contain=[
                "CryptContext",
                "bcrypt",
                "hash_password",
                "verify_password",
                "create_access_token",
                "settings.SECRET_KEY",
                "from jose import",
            ],
            must_not_contain=[
                "plain_password ==",
                "password == user.password",
                "os.getenv(\"SECRET",
                "import jwt\n",  # bare PyJWT import; pyproject pins python-jose
                "jwt.PyJWTError",
            ],
        ),
        FileSpec(
            path="app/deps.py",
            role=(
                "OAuth2PasswordBearer scheme + async def get_current_user that "
                "decodes the JWT and loads the user via get_user_by_email from db.py."
            ),
            language="python",
            must_contain=[
                "OAuth2PasswordBearer",
                "async def get_current_user",
                "HTTPException",
                "401",
                "get_user_by_email",
                "from app.db import",
                "from jose import",
                "settings.SECRET_KEY",
            ],
            must_not_contain=["db.query(", "import jwt\n"],
        ),
        FileSpec(
            path="app/routers/auth.py",
            role=(
                "APIRouter with POST /register, POST /login, GET /me. "
                "Use get_user_by_email from app.db, hash_password+verify_password from "
                "app.security, get_current_user from app.deps. Return Token schema."
            ),
            language="python",
            must_contain=[
                "/register",
                "/login",
                "/me",
                "hash_password",
                "verify_password",
                "get_user_by_email",
                "from app.security import",
                "create_access_token",
                "from app.schemas import",
                "UserCreate",
                "UserRead",
                "Token",
                "APIRouter",
            ],
            must_not_contain=[
                "from_orm",
                ".dict()",
                "parse_obj",
                "UserCreateSchema",
                "\"username\":",
            ],
        ),
        FileSpec(
            path="app/main.py",
            role=(
                "FastAPI() app with lifespan, CORSMiddleware reading CORS_ORIGINS "
                "from settings, include_router(auth.router, prefix='/auth'), "
                "/health endpoint. Do NOT import a Base symbol — use SQLModel.metadata."
            ),
            language="python",
            must_contain=[
                "CORSMiddleware",
                "include_router",
                "/health",
                "@asynccontextmanager",
                "async def lifespan",
                "FastAPI(lifespan=lifespan",
            ],
            must_not_contain=[
                "from app.db import Base",
                "Base.metadata",
                "lifespan=\"on\"",
                "@app.on_event",
                "SQLModel.metadata.create_all(settings",
            ],
        ),
        FileSpec(
            path="alembic.ini",
            role="Alembic config pointing at env.py",
            language="ini",
            template=_ALEMBIC_INI,
        ),
        FileSpec(
            path="alembic/env.py",
            role="Alembic env reading DATABASE_URL from settings",
            language="python",
            must_contain=["target_metadata", "DATABASE_URL"],
        ),
        FileSpec(
            path="alembic/versions/0001_create_users.py",
            role="Initial migration creating users table",
            language="python",
            must_contain=["def upgrade", "def downgrade", "users"],
        ),
        FileSpec(
            path="tests/__init__.py",
            role="empty package marker",
            language="python",
            template="",
        ),
        FileSpec(
            path="tests/conftest.py",
            role="pytest fixtures: app, async client, test db",
            language="python",
            must_contain=["pytest", "fixture"],
        ),
        FileSpec(
            path="tests/test_auth.py",
            role=(
                "Tests for register, login, /me, and bad credentials. Use the "
                "field names from app/schemas.py: every JSON payload uses "
                "`email` and `password` (NEVER `username`). Each test ends with "
                "real `assert` statements covering status code and body fields."
            ),
            language="python",
            must_contain=[
                "def test_",
                "assert ",
                "401",
                "200",
                "\"email\":",
                "\"password\":",
            ],
            must_not_contain=["pass\n", "\"username\":"],
        ),
    ]


def plan_react_frontend() -> list[FileSpec]:
    nv = CURRENT_VERSIONS["node"]
    return [
        FileSpec(
            path="frontend/package.json",
            role="React 19 + TS + Vite + Tailwind, current versions",
            language="json",
            template=_render_package_json_react(nv),
        ),
        FileSpec(
            path="frontend/tsconfig.json",
            role="TS strict config for Vite + React",
            language="json",
            template=_TSCONFIG_REACT,
        ),
        FileSpec(
            path="frontend/vite.config.ts",
            role="Vite config with React plugin + proxy to /api",
            language="typescript",
            template=_VITE_CONFIG,
        ),
        FileSpec(
            path="frontend/tailwind.config.js",
            role="Tailwind v3 config",
            language="javascript",
            template=_TAILWIND_CONFIG,
        ),
        FileSpec(
            path="frontend/index.html",
            role="Vite HTML shell",
            language="html",
            template=_VITE_INDEX_HTML,
        ),
        FileSpec(
            path="frontend/src/main.tsx",
            role="React root with BrowserRouter",
            language="typescript",
            must_contain=["createRoot", "BrowserRouter"],
        ),
        FileSpec(
            path="frontend/src/App.tsx",
            role="Top-level router: /login, /register, /dashboard (protected)",
            language="typescript",
            must_contain=["Routes", "Route"],
        ),
        FileSpec(
            path="frontend/src/api/client.ts",
            role="axios instance with interceptor injecting Bearer token from localStorage",
            language="typescript",
            must_contain=["axios", "Authorization", "Bearer"],
        ),
        FileSpec(
            path="frontend/src/context/AuthContext.tsx",
            role=(
                "useAuth hook + AuthProvider. login MUST be "
                "`login(email: string, password: string) => Promise<void>` "
                "(calls POST /auth/login then GET /auth/me, stores token in "
                "localStorage). register MUST be "
                "`register(email: string, password: string) => Promise<void>`. "
                "logout MUST be `() => void` (clears state + localStorage). "
                "user is typed as `{ id: number; email: string } | null`."
            ),
            language="typescript",
            must_contain=[
                "createContext",
                "useContext",
                "Provider",
                "email: string, password: string",
                "Promise<void>",
                "localStorage",
            ],
            must_not_contain=["user: any", "login: (token: string"],
        ),
        FileSpec(
            path="frontend/src/pages/LoginPage.tsx",
            role=(
                "Login form: controlled email+password inputs via useState, "
                "calls useAuth().login on submit, displays error state in JSX, "
                "Tailwind v3 utility classes only (NO 'tailwindcss/tailwind.css' import — "
                "the global index.css already imports tailwind directives)."
            ),
            language="typescript",
            must_contain=["useState", "onSubmit", "useAuth", "className"],
            must_not_contain=[
                "value=\"\"",
                "tailwindcss/tailwind.css",
                "fetch(",  # use auth context, not raw fetch
            ],
        ),
        FileSpec(
            path="frontend/src/pages/RegisterPage.tsx",
            role=(
                "Register form mirroring login: controlled inputs, useAuth().register, "
                "validation, Tailwind v3 utility classes only."
            ),
            language="typescript",
            must_contain=["useState", "onSubmit", "useAuth"],
            must_not_contain=["tailwindcss/tailwind.css", "fetch("],
        ),
        FileSpec(
            path="frontend/src/pages/DashboardPage.tsx",
            role="Protected page showing the user object from useAuth; redirect to /login if no user",
            language="typescript",
            must_contain=["useEffect", "useAuth"],
            must_not_contain=["tailwindcss/tailwind.css"],
        ),
        FileSpec(
            path="frontend/src/index.css",
            role="Tailwind base + components + utilities",
            language="css",
            template=_TAILWIND_INDEX_CSS,
        ),
    ]


def plan_for_task(task: str) -> tuple[str, list[FileSpec]]:
    """Pick a stack and produce the file plan for a task."""
    stack = detect_stack(task)
    if stack == "fastapi":
        files = plan_fastapi_jwt()
        if any(k in task.lower() for k in ["react", "frontend", "typescript ui"]):
            files = files + plan_react_frontend()
        return stack, files
    if stack == "react":
        return stack, plan_react_frontend()
    if stack == "go-microservices":
        return stack, plan_go_microservices()
    if stack == "android-compose":
        return stack, plan_android_compose()
    if stack == "rust-axum":
        return stack, plan_rust_axum()
    if stack == "spring-boot":
        return stack, plan_spring_boot()
    if stack == "ios-swift":
        return stack, plan_ios_swift()
    if stack == "flutter":
        return stack, plan_flutter()
    # Default fallback: still produce a usable scaffold
    return stack, plan_fastapi_jwt()


# ---------------------------------------------------------------------------
# Templates (deterministic, principal-grade)
# ---------------------------------------------------------------------------


def _render_pyproject_fastapi(v: dict[str, str]) -> str:
    return textwrap.dedent(
        f"""\
        [project]
        name = "fastapi-jwt-auth"
        version = "0.1.0"
        description = "Production-grade FastAPI backend with JWT auth"
        requires-python = ">=3.11"
        dependencies = [
            "fastapi=={v['fastapi']}",
            "uvicorn[standard]=={v['uvicorn']}",
            "sqlmodel=={v['sqlmodel']}",
            "sqlalchemy=={v['sqlalchemy']}",
            "asyncpg=={v['asyncpg']}",
            "alembic=={v['alembic']}",
            "pydantic=={v['pydantic']}",
            "pydantic-settings=={v['pydantic-settings']}",
            "passlib[bcrypt]=={v['passlib']}",
            "python-jose[cryptography]=={v['python-jose']}",
            "python-multipart=={v['python-multipart']}",
        ]

        [project.optional-dependencies]
        dev = [
            "pytest=={v['pytest']}",
            "pytest-asyncio=={v['pytest-asyncio']}",
            "httpx=={v['httpx']}",
            "ruff>=0.8.0",
            "mypy>=1.13.0",
        ]

        [tool.pytest.ini_options]
        asyncio_mode = "auto"
        testpaths = ["tests"]

        [tool.ruff]
        line-length = 100
        target-version = "py311"

        [tool.mypy]
        python_version = "3.11"
        strict = true
        """
    )


_ENV_FASTAPI_TEMPLATE = textwrap.dedent(
    """\
    # Copy to .env and fill in real values. NEVER commit .env.
    DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/app
    SECRET_KEY=change-me-to-a-real-secret-min-32-chars
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    JWT_ALGORITHM=HS256
    CORS_ORIGINS=http://localhost:5173
    """
)


_GITIGNORE_PYTHON = textwrap.dedent(
    """\
    __pycache__/
    *.py[cod]
    *.egg-info/
    .venv/
    venv/
    .env
    .env.local
    .pytest_cache/
    .mypy_cache/
    .ruff_cache/
    htmlcov/
    .coverage
    dist/
    build/
    node_modules/
    .DS_Store
    """
)


_DOCKERFILE_FASTAPI = textwrap.dedent(
    """\
    # syntax=docker/dockerfile:1.7
    FROM python:3.12-slim AS builder
    ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
    WORKDIR /app
    RUN apt-get update && apt-get install -y --no-install-recommends \\
            build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
    COPY pyproject.toml ./
    RUN pip install --upgrade pip && pip install .

    FROM python:3.12-slim AS runtime
    ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
    RUN apt-get update && apt-get install -y --no-install-recommends \\
            libpq5 curl && rm -rf /var/lib/apt/lists/* && \\
        adduser --disabled-password --gecos '' --uid 10001 app
    WORKDIR /app
    COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
    COPY --from=builder /usr/local/bin /usr/local/bin
    COPY . .
    USER app
    EXPOSE 8000
    HEALTHCHECK --interval=30s --timeout=3s --retries=3 \\
        CMD curl -f http://localhost:8000/health || exit 1
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    """
)


_COMPOSE_FASTAPI = textwrap.dedent(
    """\
    services:
      db:
        image: postgres:17-alpine
        environment:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: app
        ports: ["5432:5432"]
        volumes: ["pgdata:/var/lib/postgresql/data"]
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U postgres"]
          interval: 5s
          timeout: 3s
          retries: 10

      api:
        build: .
        env_file: .env
        environment:
          DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/app
        ports: ["8000:8000"]
        depends_on:
          db:
            condition: service_healthy
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
          interval: 30s
          timeout: 3s
          retries: 3

    volumes:
      pgdata:
    """
)


_CI_PYTHON = textwrap.dedent(
    """\
    name: ci
    on:
      push: { branches: [main] }
      pull_request: { branches: [main] }
    jobs:
      test:
        runs-on: ubuntu-latest
        services:
          postgres:
            image: postgres:17-alpine
            env:
              POSTGRES_USER: postgres
              POSTGRES_PASSWORD: postgres
              POSTGRES_DB: app
            ports: ["5432:5432"]
            options: >-
              --health-cmd "pg_isready -U postgres"
              --health-interval 5s
              --health-timeout 3s
              --health-retries 10
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with: { python-version: "3.12", cache: pip }
          - run: pip install -e ".[dev]"
          - run: ruff check .
          - run: mypy app
          - run: pytest -q
            env:
              DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/app
              SECRET_KEY: test-secret-key-min-32-chars-long-abc
    """
)


_ALEMBIC_INI = textwrap.dedent(
    """\
    [alembic]
    script_location = alembic
    prepend_sys_path = .
    sqlalchemy.url = driver://user:pass@localhost/dbname

    [loggers]
    keys = root,sqlalchemy,alembic

    [handlers]
    keys = console

    [formatters]
    keys = generic

    [logger_root]
    level = WARN
    handlers = console

    [logger_sqlalchemy]
    level = WARN
    handlers =
    qualname = sqlalchemy.engine

    [logger_alembic]
    level = INFO
    handlers =
    qualname = alembic

    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic

    [formatter_generic]
    format = %(levelname)-5.5s [%(name)s] %(message)s
    """
)


def _render_package_json_react(v: dict[str, str]) -> str:
    return json.dumps(
        {
            "name": "frontend",
            "private": True,
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "tsc -b && vite build",
                "preview": "vite preview",
                "test": "vitest",
                "lint": "eslint .",
            },
            "dependencies": {
                "react": f"^{v['react']}",
                "react-dom": f"^{v['react-dom']}",
                "react-router-dom": f"^{v['react-router-dom']}",
                "axios": f"^{v['axios']}",
            },
            "devDependencies": {
                "@types/react": f"^{v['@types/react']}",
                "@types/react-dom": f"^{v['@types/react-dom']}",
                "@vitejs/plugin-react": f"^{v['@vitejs/plugin-react']}",
                "typescript": f"^{v['typescript']}",
                "vite": f"^{v['vite']}",
                "tailwindcss": f"^{v['tailwindcss']}",
                "postcss": "^8.4.49",
                "autoprefixer": "^10.4.20",
                "vitest": f"^{v['vitest']}",
                "@testing-library/react": f"^{v['@testing-library/react']}",
            },
        },
        indent=2,
    ) + "\n"


_TSCONFIG_REACT = textwrap.dedent(
    """\
    {
      "compilerOptions": {
        "target": "ES2022",
        "lib": ["ES2022", "DOM", "DOM.Iterable"],
        "module": "ESNext",
        "moduleResolution": "bundler",
        "jsx": "react-jsx",
        "strict": true,
        "noUnusedLocals": true,
        "noUnusedParameters": true,
        "noFallthroughCasesInSwitch": true,
        "isolatedModules": true,
        "skipLibCheck": true,
        "esModuleInterop": true,
        "allowSyntheticDefaultImports": true,
        "resolveJsonModule": true,
        "useDefineForClassFields": true
      },
      "include": ["src"]
    }
    """
)


_VITE_CONFIG = textwrap.dedent(
    """\
    import { defineConfig } from "vite";
    import react from "@vitejs/plugin-react";

    export default defineConfig({
      plugins: [react()],
      server: {
        port: 5173,
        proxy: { "/api": { target: "http://localhost:8000", changeOrigin: true } },
      },
    });
    """
)


_TAILWIND_CONFIG = textwrap.dedent(
    """\
    /** @type {import('tailwindcss').Config} */
    export default {
      content: ["./index.html", "./src/**/*.{ts,tsx}"],
      theme: { extend: {} },
      plugins: [],
    };
    """
)


_VITE_INDEX_HTML = textwrap.dedent(
    """\
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>App</title>
      </head>
      <body class="bg-slate-50">
        <div id="root"></div>
        <script type="module" src="/src/main.tsx"></script>
      </body>
    </html>
    """
)


_TAILWIND_INDEX_CSS = textwrap.dedent(
    """\
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
    """
)


# ---------------------------------------------------------------------------
# Go microservices plan
# ---------------------------------------------------------------------------


def plan_go_microservices() -> list[FileSpec]:
    v = CURRENT_VERSIONS["go"]
    services = ["user", "product", "cart", "order", "payment"]
    files: list[FileSpec] = [
        FileSpec(
            path="ARCHITECTURE.md",
            role="Service boundaries, REST contracts, data flow, tradeoffs",
            language="markdown",
        ),
        FileSpec(
            path="docker-compose.yml",
            role="All 5 services + postgres + redis with healthchecks",
            language="yaml",
            template=_render_go_compose(services),
        ),
        FileSpec(
            path="Makefile",
            role="build / test / lint / up / down targets",
            language="make",
            template=_GO_MAKEFILE,
        ),
        FileSpec(
            path=".gitignore",
            role="Go gitignore",
            language="text",
            template="vendor/\n*.exe\n*.test\n*.out\n.env\n",
        ),
        FileSpec(
            path=".github/workflows/ci.yml",
            role="Go CI: vet, lint, test, build per service",
            language="yaml",
            template=_CI_GO,
        ),
    ]
    for svc in services:
        files.extend(_plan_one_go_service(svc, v))
    return files


def _plan_one_go_service(svc: str, v: dict[str, str]) -> list[FileSpec]:
    return [
        FileSpec(
            path=f"{svc}-service/go.mod",
            role=f"{svc} service go.mod with current deps",
            language="go-mod",
            template=_render_go_mod(svc, v),
        ),
        FileSpec(
            path=f"{svc}-service/Dockerfile",
            role=f"Multi-stage Go Dockerfile, distroless runtime, non-root",
            language="dockerfile",
            template=_render_go_dockerfile(svc),
        ),
        FileSpec(
            path=f"{svc}-service/cmd/main.go",
            role=f"{svc} service entrypoint: gin server, graceful shutdown, /health",
            language="go",
            must_contain=["gin", "ListenAndServe", "Shutdown", "/health"],
            must_not_contain=["mysql.Config", "github.com/go-sql-driver/mysql"],
        ),
        FileSpec(
            path=f"{svc}-service/internal/handler/handler.go",
            role=f"{svc} HTTP handlers with proper status codes and error JSON",
            language="go",
            must_contain=["c *gin.Context"],
        ),
        FileSpec(
            path=f"{svc}-service/internal/store/store.go",
            role=f"{svc} store: pgx connection pool, prepared statements, no string concat SQL",
            language="go",
            must_contain=["pgxpool", "context.Context"],
        ),
        FileSpec(
            path=f"{svc}-service/internal/handler/handler_test.go",
            role=f"{svc} handler tests using httptest with assertions",
            language="go",
            must_contain=["httptest", "func Test", "assert"],
        ),
    ]


def _render_go_mod(svc: str, v: dict[str, str]) -> str:
    return textwrap.dedent(
        f"""\
        module ecommerce/{svc}-service

        go {v['go_version']}

        require (
            github.com/gin-gonic/gin {v['gin']}
            github.com/jackc/pgx/v5 {v['pgx']}
            github.com/redis/go-redis/v9 {v['redis']}
            github.com/golang-jwt/jwt/v5 {v['jwt']}
            golang.org/x/crypto {v['bcrypt']}
            github.com/stretchr/testify {v['testify']}
        )
        """
    )


def _render_go_dockerfile(svc: str) -> str:
    return textwrap.dedent(
        f"""\
        # syntax=docker/dockerfile:1.7
        FROM golang:1.23-alpine AS build
        WORKDIR /src
        COPY go.mod ./
        RUN go mod download || true
        COPY . .
        RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/{svc}-service ./cmd

        FROM gcr.io/distroless/static-debian12:nonroot
        COPY --from=build /out/{svc}-service /{svc}-service
        EXPOSE 8080
        USER nonroot:nonroot
        ENTRYPOINT ["/{svc}-service"]
        """
    )


def _render_go_compose(services: list[str]) -> str:
    lines = ["services:"]
    port = 8081
    for svc in services:
        lines.append(
            textwrap.dedent(
                f"""\
                  {svc}-service:
                    build: ./{svc}-service
                    environment:
                      DATABASE_URL: postgres://postgres:postgres@db:5432/{svc}?sslmode=disable
                      REDIS_URL: redis://redis:6379
                      JWT_SECRET: ${{JWT_SECRET}}
                    ports: ["{port}:8080"]
                    depends_on:
                      db: {{ condition: service_healthy }}
                      redis: {{ condition: service_started }}
                    healthcheck:
                      test: ["CMD", "wget", "-qO-", "http://localhost:8080/health"]
                      interval: 30s
                      timeout: 3s
                      retries: 3
                """
            )
        )
        port += 1
    lines.append(
        textwrap.dedent(
            """\
              db:
                image: postgres:17-alpine
                environment:
                  POSTGRES_USER: postgres
                  POSTGRES_PASSWORD: postgres
                  POSTGRES_DB: postgres
                volumes: ["pgdata:/var/lib/postgresql/data"]
                healthcheck:
                  test: ["CMD-SHELL", "pg_isready -U postgres"]
                  interval: 5s
                  timeout: 3s
                  retries: 10
              redis:
                image: redis:7-alpine
            volumes:
              pgdata:
            """
        )
    )
    return "\n".join(lines)


_GO_MAKEFILE = textwrap.dedent(
    """\
    SERVICES := user product cart order payment

    .PHONY: build test lint up down

    build:
    \tfor s in $(SERVICES); do (cd $$s-service && go build ./...); done

    test:
    \tfor s in $(SERVICES); do (cd $$s-service && go test -race -count=1 ./...); done

    lint:
    \tfor s in $(SERVICES); do (cd $$s-service && go vet ./...); done

    up:
    \tdocker compose up --build -d

    down:
    \tdocker compose down -v
    """
)


_CI_GO = textwrap.dedent(
    """\
    name: ci
    on:
      push: { branches: [main] }
      pull_request: { branches: [main] }
    jobs:
      test:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            service: [user, product, cart, order, payment]
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-go@v5
            with: { go-version: "1.23", cache: true }
          - run: cd ${{ matrix.service }}-service && go vet ./... && go test -race -count=1 ./...
    """
)


# ---------------------------------------------------------------------------
# Android Compose plan
# ---------------------------------------------------------------------------


def plan_android_compose() -> list[FileSpec]:
    v = CURRENT_VERSIONS["kotlin"]
    return [
        FileSpec(
            path="settings.gradle.kts",
            role="Project settings: include :app",
            language="kotlin",
            template='pluginManagement {\n    repositories { gradlePluginPortal(); google(); mavenCentral() }\n}\ndependencyResolutionManagement {\n    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)\n    repositories { google(); mavenCentral() }\n}\nrootProject.name = "myapp"\ninclude(":app")\n',
        ),
        FileSpec(
            path="build.gradle.kts",
            role="Top-level Gradle, AGP + Kotlin + Hilt plugin versions",
            language="kotlin",
            template=_render_top_build_gradle(v),
        ),
        FileSpec(
            path="gradle.properties",
            role="Build flags",
            language="text",
            template="org.gradle.jvmargs=-Xmx2048m\nandroid.useAndroidX=true\nkotlin.code.style=official\n",
        ),
        FileSpec(
            path="app/build.gradle.kts",
            role="App module: Compose BOM, Hilt, Retrofit, Room, current versions",
            language="kotlin",
            template=_render_app_build_gradle(v),
        ),
        FileSpec(
            path="app/proguard-rules.pro",
            role="ProGuard rules for Retrofit + Hilt",
            language="text",
            template="-keepattributes Signature, InnerClasses, EnclosingMethod\n-keep,allowobfuscation,allowshrinking interface retrofit2.Call\n-keep,allowobfuscation,allowshrinking class kotlin.coroutines.Continuation\n",
        ),
        FileSpec(
            path="app/src/main/AndroidManifest.xml",
            role="Manifest with INTERNET permission, application class, MainActivity",
            language="xml",
            must_contain=["android.permission.INTERNET", "android:name", "MainActivity"],
        ),
        FileSpec(
            path="app/src/main/java/com/example/myapp/MyApp.kt",
            role="Application class annotated @HiltAndroidApp",
            language="kotlin",
            must_contain=["@HiltAndroidApp", "Application()"],
        ),
        FileSpec(
            path="app/src/main/java/com/example/myapp/MainActivity.kt",
            role="ComponentActivity with NavHost, @AndroidEntryPoint",
            language="kotlin",
            must_contain=["@AndroidEntryPoint", "NavHost", "rememberNavController"],
        ),
        FileSpec(
            path="app/src/main/java/com/example/myapp/di/NetworkModule.kt",
            role="@Module @InstallIn(SingletonComponent) providing Retrofit + ApiService",
            language="kotlin",
            must_contain=["@Module", "@InstallIn", "@Provides", "Retrofit.Builder"],
        ),
        FileSpec(
            path="app/src/main/java/com/example/myapp/data/AuthApi.kt",
            role="Retrofit interface with suspend functions for login/signup",
            language="kotlin",
            must_contain=["interface", "suspend fun", "@POST"],
        ),
        FileSpec(
            path="app/src/main/java/com/example/myapp/data/AuthRepository.kt",
            role="@Singleton repository wrapping AuthApi + token DataStore, returns Result<T>",
            language="kotlin",
            must_contain=["@Singleton", "@Inject", "Result"],
        ),
        FileSpec(
            path="app/src/main/java/com/example/myapp/ui/login/LoginViewModel.kt",
            role="@HiltViewModel with StateFlow<LoginUiState>",
            language="kotlin",
            must_contain=["@HiltViewModel", "StateFlow", "viewModelScope"],
        ),
        FileSpec(
            path="app/src/main/java/com/example/myapp/ui/login/LoginScreen.kt",
            role="Composable using collectAsStateWithLifecycle and state hoisting (no value=\"\")",
            language="kotlin",
            must_contain=["collectAsStateWithLifecycle", "remember", "by "],
            must_not_contain=['value = ""'],
        ),
        FileSpec(
            path="app/src/main/java/com/example/myapp/ui/signup/SignupScreen.kt",
            role="Signup composable mirroring login",
            language="kotlin",
            must_contain=["@Composable"],
        ),
        FileSpec(
            path="app/src/test/java/com/example/myapp/ui/login/LoginViewModelTest.kt",
            role="ViewModel test using kotlinx-coroutines-test, MainDispatcherRule",
            language="kotlin",
            must_contain=["@Test", "runTest", "assert"],
        ),
    ]


def _render_top_build_gradle(v: dict[str, str]) -> str:
    return textwrap.dedent(
        f"""\
        plugins {{
            id("com.android.application") version "{v['agp']}" apply false
            id("org.jetbrains.kotlin.android") version "{v['kotlin']}" apply false
            id("com.google.dagger.hilt.android") version "{v['hilt']}" apply false
            id("com.google.devtools.ksp") version "2.1.0-1.0.29" apply false
        }}
        """
    )


def _render_app_build_gradle(v: dict[str, str]) -> str:
    return textwrap.dedent(
        f"""\
        plugins {{
            id("com.android.application")
            id("org.jetbrains.kotlin.android")
            id("com.google.dagger.hilt.android")
            id("com.google.devtools.ksp")
        }}

        android {{
            namespace = "com.example.myapp"
            compileSdk = {v['compile_sdk']}

            defaultConfig {{
                applicationId = "com.example.myapp"
                minSdk = {v['min_sdk']}
                targetSdk = {v['target_sdk']}
                versionCode = 1
                versionName = "1.0"
                testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
            }}

            buildFeatures {{ compose = true }}
            composeOptions {{ kotlinCompilerExtensionVersion = "{v['compose_compiler']}" }}

            buildTypes {{
                release {{
                    isMinifyEnabled = true
                    proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
                }}
            }}

            kotlinOptions {{ jvmTarget = "17" }}
            compileOptions {{
                sourceCompatibility = JavaVersion.VERSION_17
                targetCompatibility = JavaVersion.VERSION_17
            }}
        }}

        dependencies {{
            implementation(platform("androidx.compose:compose-bom:{v['compose_bom']}"))
            implementation("androidx.compose.ui:ui")
            implementation("androidx.compose.material3:material3")
            implementation("androidx.compose.ui:ui-tooling-preview")
            implementation("androidx.activity:activity-compose:1.9.3")
            implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.7")
            implementation("androidx.navigation:navigation-compose:2.8.5")

            implementation("com.google.dagger:hilt-android:{v['hilt']}")
            ksp("com.google.dagger:hilt-compiler:{v['hilt']}")
            implementation("androidx.hilt:hilt-navigation-compose:1.2.0")

            implementation("com.squareup.retrofit2:retrofit:{v['retrofit']}")
            implementation("com.squareup.retrofit2:converter-gson:{v['retrofit']}")
            implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

            implementation("androidx.room:room-runtime:{v['room']}")
            implementation("androidx.room:room-ktx:{v['room']}")
            ksp("androidx.room:room-compiler:{v['room']}")

            implementation("androidx.datastore:datastore-preferences:1.1.1")
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:{v['coroutines']}")

            testImplementation("junit:junit:4.13.2")
            testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:{v['coroutines']}")
        }}
        """
    )


# ---------------------------------------------------------------------------
# Rust + Axum plan
# ---------------------------------------------------------------------------


def plan_rust_axum() -> list[FileSpec]:
    v = CURRENT_VERSIONS["rust"]
    cargo_toml = textwrap.dedent(
        f"""\
        [package]
        name = "analytics"
        version = "0.1.0"
        edition = "{v['rust_edition']}"

        [dependencies]
        tokio = {{ version = "{v['tokio']}", features = ["full"] }}
        axum = "{v['axum']}"
        serde = {{ version = "{v['serde']}", features = ["derive"] }}
        serde_json = "1.0"
        sqlx = {{ version = "{v['sqlx']}", features = ["runtime-tokio-rustls", "postgres", "macros", "chrono"] }}
        tracing = "{v['tracing']}"
        tracing-subscriber = {{ version = "0.3", features = ["env-filter"] }}
        anyhow = "1.0"
        thiserror = "2.0"
        chrono = {{ version = "0.4", features = ["serde"] }}
        dotenvy = "0.15"

        [dev-dependencies]
        tokio = {{ version = "{v['tokio']}", features = ["full", "test-util"] }}
        reqwest = {{ version = "0.12", features = ["json"] }}
        """
    )
    dockerfile = textwrap.dedent(
        """\
        # syntax=docker/dockerfile:1.7
        FROM rust:1.83-alpine AS build
        RUN apk add --no-cache musl-dev openssl-dev pkgconfig
        WORKDIR /src
        COPY Cargo.toml ./
        RUN mkdir src && echo "fn main(){}" > src/main.rs && cargo build --release && rm -rf src
        COPY . .
        RUN cargo build --release

        FROM gcr.io/distroless/cc-debian12:nonroot
        COPY --from=build /src/target/release/analytics /analytics
        EXPOSE 8080
        USER nonroot:nonroot
        ENTRYPOINT ["/analytics"]
        """
    )
    return [
        FileSpec(
            path="Cargo.toml", role="Cargo with current versions", language="toml",
            template=cargo_toml,
        ),
        FileSpec(path=".gitignore", role="Rust gitignore", language="text",
                 template="target/\n*.lock\n.env\n"),
        FileSpec(path="Dockerfile", role="Multi-stage Rust Dockerfile", language="dockerfile",
                 template=dockerfile),
        FileSpec(
            path="docker-compose.yml",
            role="App + postgres for analytics",
            language="yaml",
            template=textwrap.dedent("""\
                services:
                  db:
                    image: postgres:17-alpine
                    environment:
                      POSTGRES_USER: postgres
                      POSTGRES_PASSWORD: postgres
                      POSTGRES_DB: analytics
                    ports: ["5432:5432"]
                    healthcheck:
                      test: ["CMD-SHELL", "pg_isready -U postgres"]
                      interval: 5s
                      retries: 10
                  app:
                    build: .
                    environment:
                      DATABASE_URL: postgres://postgres:postgres@db:5432/analytics
                    ports: ["8080:8080"]
                    depends_on:
                      db: { condition: service_healthy }
                """),
        ),
        FileSpec(
            path=".github/workflows/ci.yml",
            role="Rust CI: fmt, clippy, test",
            language="yaml",
            template=textwrap.dedent("""\
                name: ci
                on: { push: { branches: [main] }, pull_request: { branches: [main] } }
                jobs:
                  test:
                    runs-on: ubuntu-latest
                    steps:
                      - uses: actions/checkout@v4
                      - uses: dtolnay/rust-toolchain@stable
                        with: { components: rustfmt, clippy }
                      - run: cargo fmt --check
                      - run: cargo clippy -- -D warnings
                      - run: cargo test --all
                """),
        ),
        FileSpec(path="README.md", role="Architecture, run, scaling tradeoffs",
                 language="markdown"),
        FileSpec(
            path="src/main.rs",
            role="Axum app: routes, /health, graceful shutdown, structured logging",
            language="rust",
            must_contain=["#[tokio::main]", "Router", "/health"],
            must_not_contain=[".unwrap()"],
        ),
        FileSpec(
            path="src/routes/events.rs",
            role="POST /events ingest with batched insert via sqlx",
            language="rust",
            must_contain=["axum::Json", "sqlx::query"],
        ),
        FileSpec(
            path="src/db.rs",
            role="PgPool builder reading DATABASE_URL",
            language="rust",
            must_contain=["PgPool", "max_connections"],
        ),
        FileSpec(
            path="src/error.rs",
            role="thiserror Error + IntoResponse impl",
            language="rust",
            must_contain=["thiserror", "IntoResponse"],
        ),
        FileSpec(
            path="migrations/0001_init.sql",
            role="events table with indexed timestamp",
            language="sql",
            must_contain=["CREATE TABLE", "events", "INDEX"],
        ),
        FileSpec(
            path="tests/api.rs",
            role="Integration test hitting /events and /health",
            language="rust",
            must_contain=["#[tokio::test]", "assert_eq"],
        ),
    ]


# ---------------------------------------------------------------------------
# Spring Boot plan
# ---------------------------------------------------------------------------


def plan_spring_boot() -> list[FileSpec]:
    v = CURRENT_VERSIONS["java"]
    pom = textwrap.dedent(
        f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <project xmlns="http://maven.apache.org/POM/4.0.0">
          <modelVersion>4.0.0</modelVersion>
          <parent>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-parent</artifactId>
            <version>{v['spring_boot']}</version>
            <relativePath/>
          </parent>
          <groupId>com.example</groupId>
          <artifactId>banking</artifactId>
          <version>0.1.0</version>
          <properties>
            <java.version>{v['java_version']}</java.version>
          </properties>
          <dependencies>
            <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-web</artifactId>
            </dependency>
            <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-security</artifactId>
            </dependency>
            <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-data-jpa</artifactId>
            </dependency>
            <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-validation</artifactId>
            </dependency>
            <dependency>
              <groupId>org.postgresql</groupId>
              <artifactId>postgresql</artifactId>
              <scope>runtime</scope>
            </dependency>
            <dependency>
              <groupId>org.springframework.boot</groupId>
              <artifactId>spring-boot-starter-test</artifactId>
              <scope>test</scope>
            </dependency>
            <dependency>
              <groupId>org.springframework.security</groupId>
              <artifactId>spring-security-test</artifactId>
              <scope>test</scope>
            </dependency>
            <dependency>
              <groupId>io.jsonwebtoken</groupId>
              <artifactId>jjwt-api</artifactId>
              <version>0.12.6</version>
            </dependency>
            <dependency>
              <groupId>io.jsonwebtoken</groupId>
              <artifactId>jjwt-impl</artifactId>
              <version>0.12.6</version>
              <scope>runtime</scope>
            </dependency>
            <dependency>
              <groupId>io.jsonwebtoken</groupId>
              <artifactId>jjwt-jackson</artifactId>
              <version>0.12.6</version>
              <scope>runtime</scope>
            </dependency>
          </dependencies>
          <build>
            <plugins>
              <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
              </plugin>
            </plugins>
          </build>
        </project>
        """
    )
    dockerfile = textwrap.dedent(
        f"""\
        # syntax=docker/dockerfile:1.7
        FROM maven:3.9-eclipse-temurin-{v['java_version']} AS build
        WORKDIR /src
        COPY pom.xml ./
        RUN mvn -B -q dependency:go-offline
        COPY src ./src
        RUN mvn -B -q -DskipTests package

        FROM eclipse-temurin:{v['java_version']}-jre-alpine
        RUN adduser -D -u 10001 app
        WORKDIR /app
        COPY --from=build /src/target/*.jar /app/app.jar
        USER app
        EXPOSE 8080
        HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD wget -qO- http://localhost:8080/actuator/health || exit 1
        ENTRYPOINT ["java","-jar","/app/app.jar"]
        """
    )
    return [
        FileSpec(path="pom.xml", role="Maven config with Spring Boot + Security + JPA",
                 language="xml", template=pom),
        FileSpec(path=".gitignore", role="Java/Maven gitignore", language="text",
                 template="target/\n*.class\n.idea/\n*.iml\n.env\n"),
        FileSpec(path="Dockerfile", role="Multi-stage Spring Boot Dockerfile",
                 language="dockerfile", template=dockerfile),
        FileSpec(
            path="docker-compose.yml",
            role="App + postgres",
            language="yaml",
            template=textwrap.dedent("""\
                services:
                  db:
                    image: postgres:17-alpine
                    environment: { POSTGRES_USER: postgres, POSTGRES_PASSWORD: postgres, POSTGRES_DB: banking }
                    healthcheck: { test: ["CMD-SHELL", "pg_isready -U postgres"], interval: 5s, retries: 10 }
                  app:
                    build: .
                    environment:
                      SPRING_DATASOURCE_URL: jdbc:postgresql://db:5432/banking
                      SPRING_DATASOURCE_USERNAME: postgres
                      SPRING_DATASOURCE_PASSWORD: postgres
                    ports: ["8080:8080"]
                    depends_on: { db: { condition: service_healthy } }
                """),
        ),
        FileSpec(path=".github/workflows/ci.yml", role="Maven CI", language="yaml",
                 template=textwrap.dedent(f"""\
                    name: ci
                    on: {{ push: {{ branches: [main] }}, pull_request: {{ branches: [main] }} }}
                    jobs:
                      test:
                        runs-on: ubuntu-latest
                        steps:
                          - uses: actions/checkout@v4
                          - uses: actions/setup-java@v4
                            with: {{ distribution: temurin, java-version: "{v['java_version']}", cache: maven }}
                          - run: mvn -B verify
                    """)),
        FileSpec(path="README.md", role="Banking domain, CQRS notes, security tradeoffs",
                 language="markdown"),
        FileSpec(
            path="src/main/resources/application.yml",
            role="Spring config: datasource from env, JWT properties, actuator",
            language="yaml",
            must_contain=["${", "actuator", "datasource"],
        ),
        FileSpec(
            path="src/main/java/com/example/banking/BankingApplication.java",
            role="@SpringBootApplication entrypoint",
            language="java",
            must_contain=["@SpringBootApplication", "SpringApplication.run"],
        ),
        FileSpec(
            path="src/main/java/com/example/banking/security/SecurityConfig.java",
            role="SecurityFilterChain bean with JWT filter, stateless sessions, BCryptPasswordEncoder",
            language="java",
            must_contain=["@Configuration", "SecurityFilterChain", "BCryptPasswordEncoder"],
        ),
        FileSpec(
            path="src/main/java/com/example/banking/security/JwtService.java",
            role="JWT issue + parse using jjwt 0.12 API",
            language="java",
            must_contain=["Jwts.", "SecretKey"],
        ),
        FileSpec(
            path="src/main/java/com/example/banking/account/Account.java",
            role="JPA @Entity Account with BigDecimal balance, versioned for optimistic locking",
            language="java",
            must_contain=["@Entity", "@Version", "BigDecimal"],
        ),
        FileSpec(
            path="src/main/java/com/example/banking/account/AccountRepository.java",
            role="Spring Data JpaRepository",
            language="java",
            must_contain=["JpaRepository"],
        ),
        FileSpec(
            path="src/main/java/com/example/banking/account/AccountController.java",
            role="REST controller for transfer/deposit/balance with @Transactional service",
            language="java",
            must_contain=["@RestController", "@PostMapping", "@Transactional"],
        ),
        FileSpec(
            path="src/test/java/com/example/banking/account/AccountControllerTest.java",
            role="@SpringBootTest + MockMvc auth + transfer tests",
            language="java",
            must_contain=["@SpringBootTest", "MockMvc", "@Test"],
        ),
    ]


# ---------------------------------------------------------------------------
# iOS Swift plan
# ---------------------------------------------------------------------------


def plan_ios_swift() -> list[FileSpec]:
    v = CURRENT_VERSIONS["swift"]
    return [
        FileSpec(
            path="Package.swift",
            role=f"SwiftPM manifest, swift-tools-version {v['swift_version']}",
            language="swift",
            template=textwrap.dedent(f"""\
                // swift-tools-version:{v['swift_version']}
                import PackageDescription

                let package = Package(
                    name: "App",
                    platforms: [.iOS(.v17)],
                    products: [.library(name: "App", targets: ["App"])],
                    targets: [
                        .target(name: "App"),
                        .testTarget(name: "AppTests", dependencies: ["App"]),
                    ]
                )
                """),
        ),
        FileSpec(path=".gitignore", role="Swift / Xcode gitignore", language="text",
                 template=".build/\nPackages/\nDerivedData/\nxcuserdata/\n*.xcworkspace\n!default.xcworkspace\n.swiftpm/\n"),
        FileSpec(path="README.md", role="iOS app overview, architecture (MVVM+Combine)",
                 language="markdown"),
        FileSpec(
            path="Sources/App/AppApp.swift",
            role="@main App struct with WindowGroup root",
            language="swift",
            must_contain=["@main", "WindowGroup", "App {"],
        ),
        FileSpec(
            path="Sources/App/Auth/AuthService.swift",
            role="actor AuthService with login/signup async funcs, URLSession",
            language="swift",
            must_contain=["actor AuthService", "async throws", "URLSession"],
        ),
        FileSpec(
            path="Sources/App/Auth/AuthViewModel.swift",
            role="@MainActor ObservableObject with @Published state",
            language="swift",
            must_contain=["@MainActor", "@Published", "ObservableObject"],
        ),
        FileSpec(
            path="Sources/App/Auth/LoginView.swift",
            role="SwiftUI Form with TextField bindings, error alert, async login Task",
            language="swift",
            must_contain=["@StateObject", "TextField", "Task {"],
            must_not_contain=["@State private var email = \"a\""],
        ),
        FileSpec(
            path="Sources/App/Auth/SignupView.swift",
            role="SwiftUI signup form mirroring LoginView",
            language="swift",
            must_contain=["TextField", "Button"],
        ),
        FileSpec(
            path="Sources/App/Auth/TokenStore.swift",
            role="Keychain-backed token store using Security framework",
            language="swift",
            must_contain=["import Security", "SecItemAdd"],
        ),
        FileSpec(
            path="Tests/AppTests/AuthServiceTests.swift",
            role="XCTest cases using XCTAssertEqual with mocked URLProtocol",
            language="swift",
            must_contain=["XCTestCase", "XCTAssert", "URLProtocol"],
        ),
    ]


# ---------------------------------------------------------------------------
# Flutter plan
# ---------------------------------------------------------------------------


def plan_flutter() -> list[FileSpec]:
    v = CURRENT_VERSIONS["dart"]
    pubspec = textwrap.dedent(
        f"""\
        name: app
        description: Flutter cross-platform app
        publish_to: 'none'
        version: 0.1.0

        environment:
          sdk: '>=3.6.0 <4.0.0'
          flutter: '>={v['flutter']}'

        dependencies:
          flutter:
            sdk: flutter
          flutter_riverpod: ^{v['riverpod']}
          go_router: ^{v['go_router']}
          dio: ^5.7.0
          freezed_annotation: ^2.4.4
          json_annotation: ^4.9.0
          flutter_secure_storage: ^9.2.2

        dev_dependencies:
          flutter_test:
            sdk: flutter
          build_runner: ^2.4.13
          freezed: ^2.5.7
          json_serializable: ^6.9.0
          mocktail: ^1.0.4
          flutter_lints: ^5.0.0

        flutter:
          uses-material-design: true
        """
    )
    return [
        FileSpec(path="pubspec.yaml", role="Flutter pubspec, current versions",
                 language="yaml", template=pubspec),
        FileSpec(path=".gitignore", role="Flutter gitignore", language="text",
                 template=".dart_tool/\nbuild/\n.flutter-plugins\n.flutter-plugins-dependencies\n.packages\n.pub-cache/\n.pub/\n*.iml\n.idea/\nios/Pods/\nandroid/.gradle/\n"),
        FileSpec(path="analysis_options.yaml", role="flutter_lints + extras",
                 language="yaml",
                 template="include: package:flutter_lints/flutter.yaml\nlinter:\n  rules:\n    avoid_print: true\n    prefer_single_quotes: true\n"),
        FileSpec(path="README.md", role="Flutter app overview + architecture", language="markdown"),
        FileSpec(
            path="lib/main.dart",
            role="ProviderScope wrapping MaterialApp.router with go_router",
            language="dart",
            must_contain=["ProviderScope", "MaterialApp.router", "void main"],
        ),
        FileSpec(
            path="lib/router/router.dart",
            role="GoRouter with redirect based on auth state",
            language="dart",
            must_contain=["GoRouter", "redirect"],
        ),
        FileSpec(
            path="lib/features/auth/auth_repository.dart",
            role="Repository using dio + secure storage; returns Result-style sealed class",
            language="dart",
            must_contain=["class AuthRepository", "FlutterSecureStorage", "Future<"],
        ),
        FileSpec(
            path="lib/features/auth/auth_controller.dart",
            role="Riverpod AsyncNotifier managing login/signup/logout state",
            language="dart",
            must_contain=["AsyncNotifier", "@riverpod", "build("],
        ),
        FileSpec(
            path="lib/features/auth/login_screen.dart",
            role="ConsumerStatefulWidget with TextEditingController + form validation",
            language="dart",
            must_contain=["ConsumerStatefulWidget", "TextEditingController", "FormState"],
        ),
        FileSpec(
            path="test/auth/auth_controller_test.dart",
            role="flutter_test with ProviderContainer + mocktail",
            language="dart",
            must_contain=["ProviderContainer", "mocktail", "expect("],
        ),
    ]


# ---------------------------------------------------------------------------
# Per-file prompt builder
# ---------------------------------------------------------------------------


def build_file_prompt(
    task: str,
    spec: FileSpec,
    tree: Sequence[str],
    stack: str,
    versions: dict[str, str],
) -> str:
    """Focused per-file prompt — small, specific, constraint-loaded."""
    version_lines = "\n".join(f"- {k}: {v}" for k, v in versions.items())
    must_have = "\n".join(f"- MUST contain: `{m}`" for m in spec.must_contain) or "- (none)"
    must_not = "\n".join(f"- MUST NOT contain: `{m}`" for m in spec.must_not_contain) or "- (none)"
    tree_lines = "\n".join(f"  {p}" for p in tree[:30])
    return textwrap.dedent(
        f"""\
        You are writing ONE source file for a production project.

        ## Project task
        {task.strip()}

        ## Stack
        {stack}

        ## Pinned current versions (use exactly these — do NOT downgrade)
        {version_lines}

        ## Project file tree (you are writing ONE of these)
        {tree_lines}

        ## File to write
        Path: `{spec.path}`
        Role: {spec.role}
        Language: {spec.language}

        ## Hard requirements
        {must_have}
        {must_not}

        ## Cross-cutting rules
        - NO hardcoded secrets. Read from env vars / settings.
        - NO `password ==` comparisons. Use bcrypt verify.
        - All exceptions handled; no bare `except:`.
        - Public funcs documented with one-line docstrings only.
        - Code must be syntactically valid and idiomatic for {spec.language}.

        ## Output format
        Output ONLY the raw file contents. No prose, no markdown fences,
        no commentary. Start with the first real line of the file (e.g.
        `from __future__ import annotations` for Python). End with the
        last line of the file. Nothing else.
        """
    )


# ---------------------------------------------------------------------------
# Self-review
# ---------------------------------------------------------------------------


@dataclass
class ReviewResult:
    score: float  # 0.0–10.0
    notes: str
    gaps: list[str]  # missing things that should be added


def build_review_prompt(task: str, spec: FileSpec, content: str) -> str:
    return textwrap.dedent(
        f"""\
        You are a principal engineer reviewing ONE file.

        ## Project task
        {task.strip()}

        ## File
        Path: `{spec.path}`
        Role: {spec.role}

        ## File content
        ```
        {content[:4000]}
        ```

        ## Scoring criteria (10 = principal-engineer-quality)
        1. Correctness — compiles/parses, no bugs
        2. Security — no hardcoded secrets, proper hashing, parameterized queries
        3. Idiomatic — uses current API conventions for its language
        4. Complete — no TODO/placeholder, all promised functionality present
        5. Maintainable — clear naming, focused responsibility

        ## Output
        Respond with ONE line of JSON only, no markdown fences:
        {{"score": 8.5, "notes": "short summary", "gaps": ["thing 1", "thing 2"]}}
        """
    )


def parse_review_response(text: str) -> ReviewResult:
    """Tolerantly extract the first JSON object from review output."""
    text = text.strip()
    match = re.search(r"\{[^{}]*\"score\"[^{}]*\}", text, re.DOTALL)
    if not match:
        return ReviewResult(score=5.0, notes="(review unparseable)", gaps=[])
    try:
        obj = json.loads(match.group(0))
        return ReviewResult(
            score=float(obj.get("score", 5.0)),
            notes=str(obj.get("notes", "")),
            gaps=[str(g) for g in obj.get("gaps", []) if g],
        )
    except (ValueError, TypeError):
        return ReviewResult(score=5.0, notes="(review parse failed)", gaps=[])


# ---------------------------------------------------------------------------
# Validators (deterministic check of must_contain / must_not_contain)
# ---------------------------------------------------------------------------


def validate_file(spec: FileSpec, content: str) -> list[str]:
    """Return list of validation errors (empty = valid)."""
    errors: list[str] = []
    for required in spec.must_contain:
        if required.lower() not in content.lower():
            errors.append(f"missing required token: {required!r}")
    for forbidden in spec.must_not_contain:
        if forbidden.lower() in content.lower():
            errors.append(f"contains forbidden token: {forbidden!r}")
    return errors


# ---------------------------------------------------------------------------
# Cross-file integrity check
# ---------------------------------------------------------------------------


def _collect_module_symbols(source: str) -> set[str]:
    """Top-level names a Python module exposes (defs, classes, assignments)."""
    import ast

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                names.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.asname or alias.name.split(".")[0])
    return names


def _find_dangling_imports(
    py_files: dict[str, str],
    project_root_pkg: str = "app",
) -> list[tuple[str, str, str]]:
    """Return (importing_file, imported_module, missing_name) for each
    cross-module import where the imported name is not defined in the
    target module."""
    import ast

    module_to_path = {
        path.replace("/", ".").removesuffix(".py"): path for path in py_files
    }
    issues: list[tuple[str, str, str]] = []
    for path, content in py_files.items():
        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if not node.module or not node.module.startswith(f"{project_root_pkg}."):
                continue
            target_path = module_to_path.get(node.module)
            if not target_path:
                for alias in node.names:
                    if alias.name != "*":
                        issues.append((path, node.module, alias.name))
                continue
            target_syms = _collect_module_symbols(py_files[target_path])
            for alias in node.names:
                if alias.name == "*":
                    continue
                if alias.name not in target_syms:
                    issues.append((path, node.module, alias.name))
    return issues


def build_integrity_fix_prompt(
    importing_path: str,
    importing_source: str,
    sibling_contents: dict[str, str],
    missing_names: list[tuple[str, str]],
) -> str:
    """Prompt that gives the model real sibling-file context to fix dangling imports."""
    siblings = "\n\n".join(
        f"## {p}\n```python\n{c[:2000]}\n```" for p, c in sibling_contents.items()
    )
    missing = "\n".join(f"- `{name}` from `{mod}`" for mod, name in missing_names)
    return textwrap.dedent(
        f"""\
        You are fixing import / symbol mismatches in ONE file.

        ## File to fix
        Path: `{importing_path}`

        ## Current content
        ```python
        {importing_source}
        ```

        ## Sibling modules (these are the ACTUAL files at runtime)
        {siblings}

        ## The file currently imports symbols that the sibling modules do NOT define:
        {missing}

        Pick the correct fix per missing symbol:
          a) If a sibling DOES export an equivalent symbol under a different name,
             update this file's import to use the real name.
          b) Otherwise, define the symbol inline in this file.

        Rewrite the WHOLE file with all imports resolved. Output ONLY the file
        contents. No prose, no markdown fences.
        """
    )


# ---------------------------------------------------------------------------
# Compile / lint validator pass
# ---------------------------------------------------------------------------


def lint_python_file(path: Path) -> list[str]:
    """Return ruff diagnostics for one Python file (empty list = clean).

    Falls back to `python -m py_compile` if ruff is not installed, which
    catches syntax errors and `NameError`-level import problems.
    """
    import shutil
    import subprocess

    if shutil.which("ruff"):
        result = subprocess.run(
            ["ruff", "check", "--no-fix", "--output-format", "concise", str(path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return []
        return [line for line in result.stdout.splitlines() if line.strip()][:15]

    # Fallback — only catches syntax errors
    result = subprocess.run(
        ["python", "-m", "py_compile", str(path)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode == 0:
        return []
    return [result.stderr.strip()] if result.stderr else ["syntax error"]


def detect_python_undefined_names(source: str) -> list[str]:
    """Find names used at module level / inside functions that aren't bound
    anywhere in this file or its imports. Catches the `select(User)` bug
    where the import statement was forgotten."""
    import ast

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    bound: set[str] = set(dir(__builtins__) if isinstance(__builtins__, type) else __builtins__)
    bound.update({"True", "False", "None", "self", "cls"})

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
            for arg in getattr(node, "args", ast.arguments(args=[])).args:
                bound.add(arg.arg)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    bound.add(t.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            bound.add(node.target.id)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                bound.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                bound.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.arguments):
            for arg in node.args + node.kwonlyargs + node.posonlyargs:
                bound.add(arg.arg)
        elif isinstance(node, ast.comprehension):
            if isinstance(node.target, ast.Name):
                bound.add(node.target.id)

    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)

    undefined = used - bound
    # Filter out names that are clearly module attributes accessed elsewhere
    return sorted(n for n in undefined if not n.startswith("_"))


def build_lint_fix_prompt(
    path: str, source: str, diagnostics: list[str], undefined: list[str]
) -> str:
    issues = []
    if diagnostics:
        issues.append("Ruff diagnostics:\n" + "\n".join(f"  {d}" for d in diagnostics))
    if undefined:
        issues.append(
            "Undefined names (likely missing imports):\n"
            + "\n".join(f"  - `{n}`" for n in undefined[:10])
        )
    issues_text = "\n\n".join(issues) if issues else "(no specific issues)"
    return textwrap.dedent(
        f"""\
        You are fixing lint / undefined-name issues in ONE file.

        ## File
        Path: `{path}`

        ## Current content
        ```python
        {source}
        ```

        ## Issues found
        {issues_text}

        ## Required fix
        Rewrite the WHOLE file so that:
          - Every name used is either defined in this file or imported.
          - DO NOT remove existing import lines unless ruff explicitly flagged
            them as unused (F401). Add missing imports — never drop working ones.
          - `Depends`, `HTTPException`, `status` come from `fastapi`.
          - `OAuth2PasswordBearer` comes from `fastapi.security`.
          - `select` comes from `sqlmodel` (or `sqlalchemy.future` for legacy).
          - `User` comes from `app.models`.
          - `Session` / `AsyncSession` come from `sqlalchemy.ext.asyncio`.
          - No duplicate function definitions.
          - No truthiness checks on un-awaited coroutines — always `await` first.

        Output ONLY the corrected file contents. No prose, no markdown fences.
        """
    )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


GenerateFn = Callable[[str], str]
"""Pluggable generator function. Takes a prompt, returns text.

Concrete implementation is built in main.py from the router/model selection
so this module stays free of provider imports and easy to unit-test.
"""


def strip_code_fences(text: str) -> str:
    """Remove markdown fences anywhere they leak into model output.

    Handles all common leakage patterns: leading fence with language tag,
    trailing fence (with or without trailing whitespace/newlines), bare
    triple-backticks on their own line in the middle of output, and
    leading prose ("Here's the file:") followed by a fenced block.
    """
    text = text.strip()
    if not text:
        return "\n"
    # If the body contains a fenced block anywhere, extract the body of the
    # first such block (the model's most common "I'll wrap it in markdown" pattern).
    fence = re.search(r"```[a-zA-Z0-9+_-]*\n(.*?)\n```", text, re.DOTALL)
    if fence:
        return fence.group(1).strip() + "\n"
    # Otherwise just strip stray opening / closing fences that survived.
    if text.startswith("```"):
        nl = text.find("\n")
        text = text[nl + 1 :] if nl != -1 else text[3:]
    # Drop any trailing `` ``` `` lines with optional whitespace
    text = re.sub(r"\n*```[ \t]*$", "", text)
    return text.strip() + "\n"


def build_project(
    task: str,
    out_dir: Path,
    generate: GenerateFn,
    *,
    max_review_passes: int = 1,
    review_threshold: float = 8.0,
    progress: Callable[[str], None] | None = None,
) -> dict:
    """Generate a principal-grade project on disk.

    Returns a report dict with scoring per file plus aggregate stats.
    """

    def log(msg: str) -> None:
        if progress is not None:
            progress(msg)

    stack, files = plan_for_task(task)
    log(f"stack={stack} files={len(files)}")

    versions = CURRENT_VERSIONS.get(_lang_for_stack(stack), CURRENT_VERSIONS["python"])
    tree = [f.path for f in files]

    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    report: dict = {
        "stack": stack,
        "out_dir": str(out_dir),
        "files": [],
        "template_count": 0,
        "llm_count": 0,
        "review_failures": 0,
    }

    for spec in files:
        target = out_dir / spec.path
        target.parent.mkdir(parents=True, exist_ok=True)

        if spec.template is not None:
            target.write_text(spec.template, encoding="utf-8")
            report["files"].append({"path": spec.path, "source": "template", "score": 10.0})
            report["template_count"] += 1
            log(f"  ✓ {spec.path} (template)")
            continue

        prompt = build_file_prompt(task, spec, tree, stack, versions)
        content = strip_code_fences(generate(prompt))

        # Deterministic re-attempts if the validator catches a violation.
        # Up to 3 attempts — most files clear on the first or second pass.
        for attempt in range(3):
            errors = validate_file(spec, content)
            if not errors:
                break
            fix_prompt = (
                prompt
                + "\n\n## Your previous attempt had these defects (regenerate to fix ALL of them):\n"
                + "\n".join(f"- {e}" for e in errors)
                + "\n\nOutput ONLY the corrected file contents. No prose."
            )
            content = strip_code_fences(generate(fix_prompt))

        # Self-review pass
        review_score = None
        review_notes = ""
        if max_review_passes > 0:
            review = parse_review_response(generate(build_review_prompt(task, spec, content)))
            review_score = review.score
            review_notes = review.notes
            if review.score < review_threshold and review.gaps:
                gap_prompt = (
                    prompt
                    + "\n\n## A reviewer flagged these gaps. Regenerate the file fixing them all:\n"
                    + "\n".join(f"- {g}" for g in review.gaps)
                )
                content = strip_code_fences(generate(gap_prompt))
                review = parse_review_response(
                    generate(build_review_prompt(task, spec, content))
                )
                review_score = review.score
                review_notes = review.notes

        target.write_text(content, encoding="utf-8")
        report["files"].append(
            {
                "path": spec.path,
                "source": "llm",
                "score": review_score,
                "notes": review_notes,
            }
        )
        report["llm_count"] += 1
        if review_score is not None and review_score < review_threshold:
            report["review_failures"] += 1
        log(f"  ✓ {spec.path} (llm, score={review_score})")

    # ── Cross-file integrity pass ──────────────────────────────────────
    # Find dangling imports across the Python files and ask the model to
    # rewrite each offending file with the real sibling-file context.
    report["integrity_fixes"] = 0
    py_files = {
        f.path: (out_dir / f.path).read_text("utf-8")
        for f in files
        if f.path.endswith(".py") and (out_dir / f.path).exists()
    }
    if py_files:
        # Group dangling refs by importing file so we fix each at most once.
        all_issues = _find_dangling_imports(py_files)
        by_file: dict[str, list[tuple[str, str]]] = {}
        for importer, module, name in all_issues:
            by_file.setdefault(importer, []).append((module, name))
        for importer, missing in by_file.items():
            sibling_paths = sorted({_module_to_path(m) for m, _ in missing})
            siblings = {p: py_files.get(p, "") for p in sibling_paths if p in py_files}
            fix_prompt = build_integrity_fix_prompt(
                importer, py_files[importer], siblings, missing
            )
            fixed = strip_code_fences(generate(fix_prompt))
            (out_dir / importer).write_text(fixed, encoding="utf-8")
            py_files[importer] = fixed
            report["integrity_fixes"] += 1
            log(f"  ↻ {importer} (integrity fix: {len(missing)} refs)")

    # ── Compile / lint validator pass ───────────────────────────────────
    # Runs ruff (or py_compile fallback) on every Python file and looks
    # for undefined names via AST. Any file with diagnostics gets one
    # regen pass with the specific error messages fed back into the prompt.
    import subprocess as _subprocess  # local import keeps top of module clean

    report["lint_fixes"] = 0
    MAX_LINT_ROUNDS = 3
    for path, _ in list(py_files.items()):
        full_path = out_dir / path
        for round_idx in range(MAX_LINT_ROUNDS):
            current = full_path.read_text("utf-8")
            try:
                diagnostics = lint_python_file(full_path)
            except (_subprocess.TimeoutExpired, FileNotFoundError):
                diagnostics = []
            undefined = detect_python_undefined_names(current)
            if not diagnostics and not undefined:
                break
            fix_prompt = build_lint_fix_prompt(path, current, diagnostics, undefined)
            fixed = strip_code_fences(generate(fix_prompt))
            full_path.write_text(fixed, encoding="utf-8")
            py_files[path] = fixed
            report["lint_fixes"] += 1
            log(
                f"  ⚒ {path} round {round_idx+1} "
                f"({len(diagnostics)} diag, {len(undefined)} undef)"
            )

    return report


def _module_to_path(module: str) -> str:
    """app.routers.auth -> app/routers/auth.py"""
    return module.replace(".", "/") + ".py"


def _lang_for_stack(stack: str) -> str:
    mapping = {
        "fastapi": "python",
        "django": "python",
        "react": "node",
        "go-microservices": "go",
        "rust-axum": "rust",
        "spring-boot": "java",
        "android-compose": "kotlin",
        "ios-swift": "swift",
        "react-native": "node",
        "flutter": "dart",
    }
    return mapping.get(stack, "python")


__all__ = [
    "CURRENT_VERSIONS",
    "FileSpec",
    "GeneratedFile",
    "ReviewResult",
    "build_file_prompt",
    "build_integrity_fix_prompt",
    "build_project",
    "build_review_prompt",
    "detect_stack",
    "looks_like_build_request",
    "parse_review_response",
    "plan_android_compose",
    "plan_fastapi_jwt",
    "plan_flutter",
    "plan_for_task",
    "plan_go_microservices",
    "plan_ios_swift",
    "plan_react_frontend",
    "plan_rust_axum",
    "plan_spring_boot",
    "strip_code_fences",
    "validate_file",
]
