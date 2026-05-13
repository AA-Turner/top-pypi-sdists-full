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
    "expo": {
        # React Native + Web via Expo. Pinning to currently shipping SDK 52
        # which uses RN 0.76 and react-native-web 0.19.
        "expo": "52.0.20",
        "react": "18.3.1",
        "react_native": "0.76.5",
        "react_native_web": "0.19.13",
        "react_dom": "18.3.1",
        "expo_router": "4.0.16",
        "expo_constants": "17.0.3",
        "expo_status_bar": "2.0.0",
        "expo_secure_store": "14.0.0",
        "expo_image": "2.0.4",
        "typescript": "5.7.2",
        "metro": "0.81.0",
        "babel_preset_expo": "12.0.4",
        "react_native_safe_area_context": "4.12.0",
        "react_native_screens": "4.4.0",
        "react_native_gesture_handler": "2.20.2",
        "axios": "1.7.9",
        "react_native_reanimated": "3.16.5",
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
    "react": ["react ", " react", "vite react", "react typescript", "react ts"],
    "nextjs": ["next.js", "nextjs", "next js"],
    "react-native-web": [
        "react native", "react-native", "expo", "expo-router", "expo router",
        "react native web", "react-native-web", "react native + web",
    ],
    "go-microservices": ["go microservice", "golang service", "gin", "go ecommerce"],
    "rust-axum": ["rust axum", "rust analytics", "tokio rust"],
    "spring-boot": ["spring boot", "java api", "spring banking"],
    "android-compose": ["jetpack compose", "kotlin android", "android app"],
    "ios-swift": ["ios swift", "swiftui", "swift app"],
    "flutter": ["flutter", "dart app"],
    "dotnet": [".net", "asp.net", "c# api"],
    "laravel": ["laravel", "php api"],
    "rails": ["rails", "ruby on rails"],
    "cpp": ["c++", "cpp microservice"],
    "graphql": ["graphql", "apollo"],
    "kubernetes": ["kubernetes", "k8s", "helm"],
}


# Priority order — earlier entries win when both match. Specific cross-platform
# / mobile-first stacks win over generic web frameworks so "React Native with
# Web support" routes to react-native-web (Expo) rather than plain React.
_STACK_PRIORITY: tuple[str, ...] = (
    "react-native-web",
    "flutter",
    "android-compose",
    "ios-swift",
    "nextjs",
    "rust-axum",
    "go-microservices",
    "spring-boot",
    "fastapi",
    "django",
    "rails",
    "laravel",
    "dotnet",
    "graphql",
    "react",
    "kubernetes",
    "cpp",
)


def detect_stack(task: str) -> str:
    """Pick the best stack template for a task description.

    Iterates in `_STACK_PRIORITY` order — the first stack whose keywords
    appear at least once wins. This prevents "React" from outscoring
    "React Native" just because the word "react" appears more times.
    """
    lower = task.lower()
    for stack in _STACK_PRIORITY:
        kws = STACK_KEYWORDS.get(stack, [])
        if any(kw in lower for kw in kws):
            return stack
    return "fastapi"


_BUILD_VERBS = (
    "build", "create", "make", "scaffold", "implement", "set up",
    "set-up", "setup", "generate a", "produce a", "develop a",
    "develop the", "design the", "design a", "design an", "architect a",
    "ship a", "ship an", "deliver a", "deliver an",
    "code a", "write a", "produce", "develop",
)


_BUILD_TASK_HEADER_RE = re.compile(
    r"(?im)^(?:\s*(?:\d+\.\s+|[-*]\s+)?)?(?:build|create|make|scaffold|implement|develop)\s+(?:a|an)\s+",
)


def decompose_multi_build_request(task: str) -> list[tuple[str, str]]:
    """Find multiple distinct build sub-tasks in a single mega-prompt.

    Returns [(label, sub_task)]. If only one task is found (or none look
    independent), returns a single-entry list with the whole task.

    Detection: splits on "Build a ..." / "Create a ..." / "Make a ..."
    headers at line starts. Each chunk from one header to the next becomes
    one sub-task. Useful for prompts like "Build X. Build Y. Build Z."
    """
    if not task:
        return []
    matches = list(_BUILD_TASK_HEADER_RE.finditer(task))
    if len(matches) < 2:
        return [("project", task.strip())]
    chunks: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(task)
        chunk = task[start:end].strip()
        # Per-chunk threshold is lenient — once we've established the prompt
        # is multi-task, even a one-line "Build a X" header is real work.
        if len(chunk) < 25:
            continue
        # Build a meaningful label from the first 6 words of the chunk
        first_line = chunk.split("\n", 1)[0]
        label_words = re.findall(r"[A-Za-z+#.]+", first_line)[:8]
        label = "-".join(w.lower() for w in label_words if len(w) > 1) or f"task-{i+1}"
        label = label[:60]
        chunks.append((label, chunk))
    if not chunks:
        return [("project", task.strip())]
    return chunks


def looks_like_build_request(task: str, min_chars: int = 60) -> bool:
    """Return True when `task` looks like a multi-file project build request.

    Path 1 (strict): prompt mentions a build verb AND a known stack keyword.
    Path 2 (medium): prompt mentions a build verb AND a generic project
    noun (backend, frontend, microservice, app, service) AND is at least
    `min_chars` long.
    Path 3 (loose): prompt is long (>400 chars) AND contains a stack
    keyword AND mentions any of [platform, system, application, service,
    saas, backend, frontend, dashboard, mobile]. Catches platform-spec
    prompts like "Design a modern SaaS platform with FastAPI..." that
    don't use the literal "Build a" pattern.
    """
    if not task:
        return False
    lower = task.lower()
    has_verb = any(v in lower for v in _BUILD_VERBS)
    # Path 1: build verb + stack keyword (any length)
    if has_verb:
        for kws in STACK_KEYWORDS.values():
            if any(kw in lower for kw in kws):
                return True
    # Path 2: build verb + project noun + min length
    project_nouns = (
        "backend", "frontend", "microservice", "microservices",
        "mobile app", "web app", "rest api", "graphql api",
    )
    if has_verb and len(task) >= min_chars:
        if any(n in lower for n in project_nouns):
            return True
    # Path 3: long platform-spec prompts without an explicit build verb
    if len(task) >= 400:
        platform_nouns = (
            "platform", "system", "application", "service", "saas",
            "dashboard", "backend", "frontend", "mobile app", "web app",
        )
        has_platform = any(n in lower for n in platform_nouns)
        has_stack = any(
            kw in lower for kws in STACK_KEYWORDS.values() for kw in kws
        )
        if has_platform and has_stack:
            return True
    return False


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


def _spec_mentions_backend(task: str) -> str | None:
    """Return the backend framework keyword the spec mentions, if any.

    Used so a primarily-frontend spec (RN + Web, React, Flutter) that ALSO
    requests a backend produces both halves instead of only the frontend.

    Uses regex word boundaries so e.g. "login" doesn't accidentally match
    "gin", and "raining" doesn't match "rain".
    """
    lower = task.lower()
    if re.search(r"\bfastapi\b", lower) or re.search(r"\bdjango\b", lower):
        return "fastapi"
    if "python" in lower and "backend" in lower:
        return "fastapi"
    if re.search(r"\bspring[- ]boot\b", lower):
        return "spring-boot"
    if re.search(r"\b(go microservice|golang backend|go backend|gin framework)\b", lower):
        return "go-microservices"
    if re.search(r"\baxum\b", lower) or re.search(r"\bactix\b", lower):
        return "rust-axum"
    return None


def _backend_plan_for(name: str) -> list[FileSpec]:
    if name == "fastapi":
        return plan_fastapi_jwt()
    if name == "spring-boot":
        return plan_spring_boot()
    if name == "go-microservices":
        return plan_go_microservices()
    if name == "rust-axum":
        return plan_rust_axum()
    return []


def plan_for_task(task: str) -> tuple[str, list[FileSpec]]:
    """Pick a stack and produce the file plan.

    Multi-stack rule: if the picked primary stack is a frontend/mobile
    framework but the spec also names a backend framework, the returned
    plan is the union of both. This matches what users mean when they
    say "Build a React Native app with a FastAPI backend."
    """
    stack = detect_stack(task)
    if stack == "fastapi":
        files = plan_fastapi_jwt()
        if any(k in task.lower() for k in ["react", "frontend", "typescript ui"]):
            files = files + plan_react_frontend()
        return stack, files

    primary_files: list[FileSpec]
    if stack == "react":
        primary_files = plan_react_frontend()
    elif stack == "react-native-web":
        primary_files = plan_react_native_web()
    elif stack == "go-microservices":
        return stack, plan_go_microservices()
    elif stack == "android-compose":
        primary_files = plan_android_compose()
    elif stack == "rust-axum":
        return stack, plan_rust_axum()
    elif stack == "spring-boot":
        return stack, plan_spring_boot()
    elif stack == "ios-swift":
        primary_files = plan_ios_swift()
    elif stack == "flutter":
        primary_files = plan_flutter()
    else:
        return stack, plan_fastapi_jwt()

    # Multi-stack: append backend plan if the spec names one. The backend
    # files live under `backend/` so they don't collide with frontend files.
    backend_name = _spec_mentions_backend(task)
    if backend_name:
        backend_files = _backend_plan_for(backend_name)
        # Prefix backend file paths with `backend/` so they coexist with
        # the frontend in the same project root.
        for f in backend_files:
            if not f.path.startswith("backend/") and not f.path.startswith("frontend/"):
                f.path = f"backend/{f.path}"
        return f"{stack}+{backend_name}", primary_files + backend_files

    return stack, primary_files


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
# React Native + Web (Expo) plan
# ---------------------------------------------------------------------------


def plan_react_native_web() -> list[FileSpec]:
    """Expo SDK 52 + expo-router + react-native-web. Single codebase for
    iOS, Android, and Web with SSR via the Metro web bundler. All current
    versions pinned."""
    v = CURRENT_VERSIONS["expo"]
    package_json = json.dumps(
        {
            "name": "app",
            "version": "0.1.0",
            "main": "expo-router/entry",
            "scripts": {
                "start": "expo start",
                "android": "expo start --android",
                "ios": "expo start --ios",
                "web": "expo start --web",
                "build:web": "expo export --platform web",
                "lint": "expo lint",
                "test": "jest --watchAll=false",
                "typecheck": "tsc --noEmit",
            },
            "dependencies": {
                "expo": f"^{v['expo']}",
                "expo-constants": f"^{v['expo_constants']}",
                "expo-router": f"^{v['expo_router']}",
                "expo-status-bar": f"^{v['expo_status_bar']}",
                "expo-secure-store": f"^{v['expo_secure_store']}",
                "expo-image": f"^{v['expo_image']}",
                "react": v["react"],
                "react-dom": v["react_dom"],
                "react-native": v["react_native"],
                "react-native-web": f"^{v['react_native_web']}",
                "react-native-safe-area-context": v["react_native_safe_area_context"],
                "react-native-screens": v["react_native_screens"],
                "react-native-gesture-handler": f"~{v['react_native_gesture_handler']}",
                "react-native-reanimated": f"~{v['react_native_reanimated']}",
                "axios": f"^{v['axios']}",
            },
            "devDependencies": {
                "@babel/core": "^7.25.0",
                "@types/react": "~18.3.12",
                "babel-preset-expo": f"^{v['babel_preset_expo']}",
                "jest": "^29.7.0",
                "jest-expo": f"~{v['expo']}",
                "@testing-library/react-native": "^12.9.0",
                "@testing-library/jest-native": "^5.4.3",
                "react-test-renderer": v["react"],  # peer of @testing-library/react-native
                "typescript": f"^{v['typescript']}",
            },
            "private": True,
        },
        indent=2,
    ) + "\n"

    app_json = json.dumps(
        {
            "expo": {
                "name": "AppName",
                "slug": "appname",
                "version": "1.0.0",
                "orientation": "portrait",
                "icon": "./assets/icon.png",
                "scheme": "appname",
                "userInterfaceStyle": "automatic",
                "splash": {
                    "image": "./assets/splash.png",
                    "resizeMode": "contain",
                    "backgroundColor": "#ffffff",
                },
                "ios": {"supportsTablet": True, "bundleIdentifier": "com.example.appname"},
                "android": {
                    "adaptiveIcon": {
                        "foregroundImage": "./assets/adaptive-icon.png",
                        "backgroundColor": "#ffffff",
                    },
                    "package": "com.example.appname",
                },
                "web": {
                    "bundler": "metro",
                    "output": "static",
                    "favicon": "./assets/favicon.png",
                },
                "plugins": ["expo-router", "expo-secure-store"],
                "experiments": {"typedRoutes": True},
            }
        },
        indent=2,
    ) + "\n"

    babel_config = textwrap.dedent(
        """\
        module.exports = function (api) {
          api.cache(true);
          return {
            presets: ['babel-preset-expo'],
            plugins: ['react-native-reanimated/plugin'],
          };
        };
        """
    )

    metro_config = textwrap.dedent(
        """\
        const { getDefaultConfig } = require('expo/metro-config');
        const config = getDefaultConfig(__dirname);
        module.exports = config;
        """
    )

    tsconfig = json.dumps(
        {
            "extends": "expo/tsconfig.base",
            "compilerOptions": {
                "strict": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noFallthroughCasesInSwitch": True,
                "paths": {"@/*": ["./*"]},
            },
            "include": ["**/*.ts", "**/*.tsx", ".expo/types/**/*.ts", "expo-env.d.ts"],
        },
        indent=2,
    ) + "\n"

    expo_env = "/// <reference types=\"expo/types\" />\n// NOTE: This file should not be edited and should be in your git ignore.\n"

    gitignore = textwrap.dedent(
        """\
        node_modules/
        .expo/
        dist/
        web-build/
        npm-debug.*
        *.jks
        *.p8
        *.p12
        *.key
        *.mobileprovision
        *.orig.*
        .env*.local
        .env
        .DS_Store
        # Expo router auto-generated types
        expo-env.d.ts
        """
    )

    ci = textwrap.dedent(
        """\
        name: ci
        on:
          push: { branches: [main] }
          pull_request: { branches: [main] }
        jobs:
          test:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - uses: actions/setup-node@v4
                with: { node-version: "20", cache: npm }
              - run: npm ci
              - run: npm run typecheck
              - run: npm test
              - run: npm run build:web
        """
    )

    return [
        FileSpec(path="package.json", role="Expo SDK 52 + react-native-web pinned",
                 language="json", template=package_json),
        FileSpec(
            path=".npmrc",
            role="legacy-peer-deps so Expo SDK 52 + RN 0.76 resolve cleanly",
            language="text",
            template="legacy-peer-deps=true\nfund=false\naudit=false\n",
        ),
        FileSpec(path="app.json", role="Expo app config with web bundler enabled",
                 language="json", template=app_json),
        FileSpec(path="babel.config.js", role="Babel preset-expo + reanimated plugin",
                 language="javascript", template=babel_config),
        FileSpec(path="metro.config.js", role="Metro bundler defaults",
                 language="javascript", template=metro_config),
        FileSpec(path="tsconfig.json", role="TS strict + path alias + expo types",
                 language="json", template=tsconfig),
        FileSpec(path="expo-env.d.ts", role="Expo TS type reference",
                 language="typescript", template=expo_env),
        FileSpec(path=".gitignore", role="Expo / Node gitignore", language="text",
                 template=gitignore),
        FileSpec(path=".github/workflows/ci.yml", role="CI: typecheck + test + web build",
                 language="yaml", template=ci),
        FileSpec(path="README.md", role="App overview, run on iOS/Android/Web, deploy",
                 language="markdown"),

        # ── Expo Router app/ tree (file-based routing for iOS/Android/Web) ──
        FileSpec(
            path="app/_layout.tsx",
            role=(
                "Root layout using expo-router Stack. Must wrap with "
                "GestureHandlerRootView + SafeAreaProvider + AuthProvider. "
                "Uses react-native StyleSheet, NOT styled-components."
            ),
            language="typescript",
            must_contain=[
                "from 'expo-router'",
                "Stack",
                "SafeAreaProvider",
                "GestureHandlerRootView",
                "AuthProvider",
            ],
            must_not_contain=["from 'react-router-dom'", "styled-components"],
        ),
        FileSpec(
            path="app/index.tsx",
            role=(
                "Landing route. Uses react-native primitives (View, Text, "
                "Pressable) — NOT HTML elements (div, span, button). "
                "Uses expo-router Link or router.push for navigation."
            ),
            language="typescript",
            must_contain=[
                "from 'react-native'",
                "View",
                "Text",
                "from 'expo-router'",
            ],
            must_not_contain=["<div", "<span", "<button", "className=", "react-router"],
        ),
        FileSpec(
            path="app/(auth)/login.tsx",
            role=(
                "Polished login screen — React Native TextInput, Pressable, Text. "
                "Uses useAuth().signIn(email, password). keyboardType=email-address. "
                "Visual polish: StyleSheet.create with named colors/spacing, "
                "ActivityIndicator while submitting, error Text in red when "
                "auth fails, KeyboardAvoidingView for iOS, rounded inputs with "
                "border + padding, primary button with hover/pressed states. "
                "Responsive: max-width on web/tablet via useWindowDimensions."
            ),
            language="typescript",
            must_contain=[
                "from 'react-native'",
                "TextInput",
                "useAuth",
                "useState",
                "keyboardType",
                "StyleSheet.create",
                "ActivityIndicator",
                "KeyboardAvoidingView",
            ],
            must_not_contain=["<input", "<form", "<button", "className=", "<div"],
        ),
        FileSpec(
            path="app/(auth)/register.tsx",
            role="Register screen mirroring login with TextInput + Pressable",
            language="typescript",
            must_contain=["from 'react-native'", "TextInput", "useAuth", "useState"],
            must_not_contain=["<input", "<form", "<div", "className="],
        ),
        FileSpec(
            path="app/(auth)/_layout.tsx",
            role="Auth route group layout via expo-router Stack",
            language="typescript",
            must_contain=["from 'expo-router'", "Stack"],
        ),
        FileSpec(
            path="app/(tabs)/_layout.tsx",
            role="Tabs layout using expo-router Tabs + ionicons",
            language="typescript",
            must_contain=["from 'expo-router'", "Tabs"],
        ),
        FileSpec(
            path="app/(tabs)/dashboard.tsx",
            role=(
                "Dashboard tab — React Native FlatList of campaigns from API. "
                "Responsive: useWindowDimensions for tablet/web breakpoints. "
                "Use Platform.OS to branch behaviour only when needed."
            ),
            language="typescript",
            must_contain=[
                "from 'react-native'",
                "FlatList",
                "useWindowDimensions",
                "Platform",
            ],
            must_not_contain=["<div", "<table", "className="],
        ),
        FileSpec(
            path="app/(tabs)/settings.tsx",
            role="Settings tab — Switch components, profile edit, logout button",
            language="typescript",
            must_contain=["from 'react-native'", "Switch", "useAuth"],
            must_not_contain=["<div", "<input", "className="],
        ),

        # ── Shared modules ─────────────────────────────────────────
        FileSpec(
            path="context/AuthContext.tsx",
            role=(
                "Auth provider exposing signIn(email,password), signUp, signOut, "
                "user. Tokens stored via expo-secure-store on native, "
                "AsyncStorage / localStorage fallback on web via Platform.OS."
            ),
            language="typescript",
            must_contain=[
                "createContext",
                "useAuth",
                "signIn",
                "signUp",
                "signOut",
                "Platform.OS",
                "expo-secure-store",
            ],
            must_not_contain=["document.", "<div"],
        ),
        FileSpec(
            path="services/api.ts",
            role=(
                "axios instance with baseURL from process.env.EXPO_PUBLIC_API_URL "
                "and Authorization header injected from stored token. "
                "No DOM dependencies — must work on RN + Web."
            ),
            language="typescript",
            must_contain=[
                "axios",
                "EXPO_PUBLIC_API_URL",
                "Authorization",
                "Bearer",
            ],
            must_not_contain=["window.", "document.", "localStorage.getItem('token')  // unsafe"],
        ),
        FileSpec(
            path="components/Button.tsx",
            role=(
                "Polished cross-platform Button — Pressable with hover/pressed "
                "visual feedback via pressed style fn. Variants: primary, "
                "secondary, destructive. Loading state shows ActivityIndicator. "
                "Disabled state dims opacity. NO HTML, NO className — "
                "StyleSheet.create with named color/spacing tokens."
            ),
            language="typescript",
            must_contain=[
                "Pressable",
                "StyleSheet.create",
                "ActivityIndicator",
                "pressed",
                "disabled",
            ],
            must_not_contain=["<button", "className=", "<div"],
        ),
        FileSpec(
            path="components/TextField.tsx",
            role=(
                "Polished labelled TextInput. View + Text label + TextInput + "
                "error Text in red below. Visual: rounded border, focused "
                "ring colour via onFocus/onBlur state, placeholder colour, "
                "padding for touch targets, accessible labels."
            ),
            language="typescript",
            must_contain=[
                "TextInput",
                "from 'react-native'",
                "StyleSheet.create",
                "onFocus",
                "onBlur",
            ],
            must_not_contain=["<input", "<label", "className="],
        ),
        FileSpec(
            path="hooks/useResponsive.ts",
            role=(
                "useResponsive() returning { isPhone, isTablet, isDesktop } via "
                "useWindowDimensions breakpoints (768, 1024)."
            ),
            language="typescript",
            must_contain=["useWindowDimensions", "isPhone", "isTablet", "isDesktop"],
        ),

        # ── Tests (Jest + @testing-library/react-native) ────────────
        FileSpec(
            path="__tests__/auth.test.tsx",
            role=(
                "Tests for login form: renders TextInput, validates email "
                "format, calls signIn on submit. Uses @testing-library/react-native."
            ),
            language="typescript",
            must_contain=[
                "@testing-library/react-native",
                "render",
                "fireEvent",
                "expect",
            ],
            must_not_contain=["@testing-library/react'", "jsdom"],
        ),
        FileSpec(
            path="jest.config.js",
            role="jest-expo preset",
            language="javascript",
            template=textwrap.dedent("""\
                module.exports = {
                  preset: 'jest-expo',
                  transformIgnorePatterns: [
                    'node_modules/(?!((jest-)?react-native|@react-native(-community)?|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg))',
                  ],
                };
                """),
        ),
        FileSpec(
            path=".env.example",
            role="Example env vars — only EXPO_PUBLIC_* are exposed at runtime",
            language="env",
            template="EXPO_PUBLIC_API_URL=http://localhost:8000\n",
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
# Task compression for very long inputs
# ---------------------------------------------------------------------------


_LONG_TASK_THRESHOLD = 2000
"""Char count above which the task is compressed to a brief before being
embedded into per-file LLM prompts. Below this, the full task is passed."""

_COMPRESSION_CHUNK_SIZE = 40_000
"""Maximum chars per compression LLM call. ~40K chars ≈ ~10K tokens, leaves
comfortable headroom in a 32K-token context window for the prompt template
and the generated brief. Inputs larger than this are chunked and
map-reduced into a single final brief."""

_HARD_INPUT_CAP = 2_000_000
"""Absolute char limit beyond which input is head/tail-truncated even
before chunking, to avoid pathological loop counts. 2M chars ≈ ~500K
tokens — far larger than any realistic prompt."""


def _build_compression_prompt(task: str) -> str:
    return textwrap.dedent(
        f"""\
        You are condensing a long project specification into a structured
        technical brief that will guide code generation. Preserve EVERY
        feature, integration, and cross-cutting requirement the user
        mentioned — do not summarise away features. Use bullet lists.

        ## Input specification
        {task.strip()}

        ## Output format (fill in exactly this template — keep ALL items)
        PROJECT: <one-line summary of what to build>
        STACK:
        - <every technology / library / framework mentioned, one per line>
        AUTH: <auth scheme + any special requirements>
        FEATURES:
        - <EVERY feature the user wants, one per line — do not omit any>
        INTEGRATIONS:
        - <EVERY external API / service to wire up, one per line>
        CROSS-CUTTING:
        - <EVERY observability / security / performance / compliance line>
        TENANCY: <single-tenant or multi-tenant + brief notes>
        DEPLOYMENT: <docker/k8s/cloud target + any infra notes>
        DATA:
        - <data stores, queues, caches, object storage>

        Do NOT collapse multiple features into one line. Do NOT skip
        features that seem similar. The next stage will use this brief
        verbatim and only see what is in it.

        Output ONLY the filled brief. No prose, no markdown fences, no
        commentary before or after.
        """
    )


def _chunk_text(text: str, max_chunk_chars: int) -> list[str]:
    """Split `text` into chunks at most `max_chunk_chars` long, preferring
    paragraph and line boundaries so semantic units stay intact."""
    if len(text) <= max_chunk_chars:
        return [text]
    chunks: list[str] = []
    remaining = text
    while len(remaining) > max_chunk_chars:
        cut = max_chunk_chars
        # Prefer a paragraph break, then a sentence break, then a newline,
        # then a space. Search backward from the max position.
        for delim in ("\n\n", ". ", "\n", " "):
            idx = remaining.rfind(delim, max_chunk_chars // 2, max_chunk_chars)
            if idx != -1:
                cut = idx + len(delim)
                break
        chunks.append(remaining[:cut].strip())
        remaining = remaining[cut:]
    if remaining.strip():
        chunks.append(remaining.strip())
    return chunks


def _head_tail_truncate(task: str) -> str:
    """Last-resort fallback: keep the most-signal bookends of the input."""
    head = task[:1500]
    tail = task[-1000:] if len(task) > 2500 else ""
    if tail:
        return f"{head}\n\n... [middle omitted] ...\n\n{tail}".strip()
    return head.strip()


def compress_task_brief(task: str, generate: GenerateFn) -> str:
    """Reduce any-size spec to a ~500-token compact brief.

    Strategy:
      - Below `_LONG_TASK_THRESHOLD` (2K chars): return unchanged.
      - Up to `_COMPRESSION_CHUNK_SIZE` (40K chars): one LLM compression call.
      - Larger: split into chunks at paragraph boundaries, summarise each
        chunk separately (map step), then summarise the concatenated
        mini-summaries into the final brief (reduce step).
      - `_HARD_INPUT_CAP` (2M chars): head/tail-truncate before chunking
        so we never spawn a pathological number of map calls.
      - Any exception or obviously-bad output: fall back to head/tail
        truncation. Function never raises.
    """
    if not task or len(task) < _LONG_TASK_THRESHOLD:
        return task

    working = task
    if len(working) > _HARD_INPUT_CAP:
        working = _head_tail_truncate(working[:_HARD_INPUT_CAP])

    # Map step: chunked compression for inputs that won't fit one call.
    if len(working) > _COMPRESSION_CHUNK_SIZE:
        chunks = _chunk_text(working, _COMPRESSION_CHUNK_SIZE)
        mini_briefs: list[str] = []
        for chunk in chunks:
            try:
                mb = strip_code_fences(generate(_build_chunk_summary_prompt(chunk)))
            except Exception:
                mb = ""
            if mb and len(mb) > 50:
                mini_briefs.append(mb)
        if not mini_briefs:
            return _head_tail_truncate(working)
        # Reduce step: compress the concatenated mini-briefs into the
        # final structured brief. If the concatenation itself is large
        # we recurse — but the chunked map step is guaranteed to shrink
        # input each round so we converge in O(log n) passes.
        joined = "\n\n".join(mini_briefs)
        return compress_task_brief(joined, generate)

    # Single-call path: input fits in one LLM compression call.
    try:
        brief = strip_code_fences(generate(_build_compression_prompt(working)))
    except Exception:
        return _head_tail_truncate(working)
    # A comprehensive brief that preserves all features can legitimately be
    # 60–80% of the original size for a feature-rich spec. Only reject as
    # "not a brief" if the model returned nothing useful or longer than input.
    if not brief or len(brief) < 100 or len(brief) > len(working) * 1.05:
        return _head_tail_truncate(working)
    return brief


def _build_chunk_summary_prompt(chunk: str) -> str:
    """Map-step prompt: extract structured signal from one chunk."""
    return textwrap.dedent(
        f"""\
        You are extracting key requirements from ONE chunk of a larger
        project specification. Other chunks will be summarised separately
        and the summaries combined later.

        ## Chunk
        {chunk.strip()}

        ## Output format
        Extract any of the following that appear in this chunk. Use exactly
        this template, leaving sections blank if nothing applies. Be terse.

        TECH:
        - <technology / library mentioned, one per line>
        FEATURES:
        - <feature requirement, one per line>
        INTEGRATIONS:
        - <external service or API, one per line>
        SECURITY:
        - <security/auth requirement, one per line>
        PERFORMANCE:
        - <performance/scalability requirement, one per line>
        OTHER:
        - <anything else worth carrying forward, one per line>

        Output ONLY the filled template. No prose, no fences, no commentary.
        """
    )


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
# Runtime validation (install + test pass)
# ---------------------------------------------------------------------------


def _run_command(cmd: list[str], cwd: Path, timeout: int = 300) -> tuple[int, str]:
    """Run a subprocess command, return (returncode, combined-output)."""
    import subprocess
    try:
        result = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout
        )
        out = (result.stdout or "") + (result.stderr or "")
        return result.returncode, out
    except subprocess.TimeoutExpired:
        return 124, f"Command timed out after {timeout}s: {' '.join(cmd)}"
    except FileNotFoundError:
        return 127, f"Tool not found: {cmd[0]}"
    except OSError as exc:
        return 1, f"Failed to run {' '.join(cmd)}: {exc}"


def validate_node_project(out_dir: Path, log: Callable[[str], None] | None = None
                          ) -> dict:
    """Run `npm install` + `npm test` in a Node project root. Returns a
    diagnostic dict the orchestrator uses to decide whether to regen.

    Returns: {ran: bool, install_ok: bool, test_ok: bool, errors: [str]}.
    """
    import shutil

    def _log(msg: str) -> None:
        if log:
            log(msg)

    if not (out_dir / "package.json").exists():
        return {"ran": False, "reason": "no package.json"}
    if not shutil.which("npm"):
        return {"ran": False, "reason": "npm not installed"}

    _log("  ▶ npm install")
    code, install_log = _run_command(
        ["npm", "install", "--no-fund", "--no-audit", "--silent",
         "--legacy-peer-deps"],
        out_dir, timeout=300,
    )
    install_ok = code == 0
    errors: list[str] = []
    if not install_ok:
        # Keep the most signal-dense tail of the npm log for the regen prompt
        errors.append("npm install failed:\n" + install_log[-2000:])

    test_ok = False
    test_log = ""
    if install_ok:
        _log("  ▶ npm test")
        code, test_log = _run_command(
            ["npm", "test", "--silent", "--", "--passWithNoTests"],
            out_dir, timeout=180,
        )
        test_ok = code == 0
        if not test_ok:
            errors.append("npm test failed:\n" + test_log[-2000:])

    return {
        "ran": True,
        "install_ok": install_ok,
        "test_ok": test_ok,
        "errors": errors,
    }


def validate_python_project(out_dir: Path, log: Callable[[str], None] | None = None
                            ) -> dict:
    """Run `pip install -e .` + `pytest` in a Python project root."""
    import shutil

    def _log(msg: str) -> None:
        if log:
            log(msg)

    has_pyproject = (out_dir / "pyproject.toml").exists()
    if not has_pyproject:
        return {"ran": False, "reason": "no pyproject.toml"}
    if not shutil.which("pip") and not shutil.which("pip3"):
        return {"ran": False, "reason": "pip not installed"}

    pip = "pip" if shutil.which("pip") else "pip3"
    # Use a temp venv to avoid contaminating the user's env
    import subprocess, sys
    venv_path = out_dir / ".sage" / "venv"
    venv_path.parent.mkdir(parents=True, exist_ok=True)
    if not venv_path.exists():
        _log("  ▶ creating .sage/venv")
        code, log_text = _run_command(
            [sys.executable, "-m", "venv", str(venv_path)], out_dir, timeout=120
        )
        if code != 0:
            return {"ran": False, "reason": f"venv create failed: {log_text[:500]}"}

    venv_pip = venv_path / "bin" / "pip"
    if not venv_pip.exists():
        venv_pip = venv_path / "Scripts" / "pip.exe"
    _log("  ▶ pip install -e .[dev]")
    code, install_log = _run_command(
        [str(venv_pip), "install", "-q", "-e", ".[dev]"], out_dir, timeout=600
    )
    install_ok = code == 0
    errors: list[str] = []
    if not install_ok:
        errors.append("pip install failed:\n" + install_log[-2000:])

    test_ok = False
    if install_ok:
        venv_pytest = venv_path / "bin" / "pytest"
        if not venv_pytest.exists():
            venv_pytest = venv_path / "Scripts" / "pytest.exe"
        _log("  ▶ pytest")
        code, test_log = _run_command(
            [str(venv_pytest), "-q", "--no-header"], out_dir, timeout=300
        )
        test_ok = code == 0
        if not test_ok:
            errors.append("pytest failed:\n" + test_log[-2000:])

    return {
        "ran": True,
        "install_ok": install_ok,
        "test_ok": test_ok,
        "errors": errors,
    }


def build_runtime_fix_prompt(
    error_text: str,
    relevant_files: dict[str, str],
) -> str:
    """Prompt the model with actual install/test errors so it can fix them."""
    files_block = "\n\n".join(
        f"## {p}\n```\n{c[:2500]}\n```" for p, c in relevant_files.items()
    )
    return textwrap.dedent(
        f"""\
        Your generated project fails install or test. Fix it.

        ## Error output
        ```
        {error_text[:3000]}
        ```

        ## Relevant project files
        {files_block}

        ## Required fix
        Identify which file(s) need to change to clear this error. Output
        a JSON object mapping each file path to its new full content:

        {{"path/to/file.ext": "<new full file contents>", ...}}

        Output ONLY the JSON. No prose, no markdown fences. Only include
        files that need to change.
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

    # Compress long inputs to a compact brief before per-file generation.
    # The full task remains available for stack detection (above) and for
    # writing into the README so nothing is lost.
    if len(task) >= _LONG_TASK_THRESHOLD:
        log(f"  Task is {len(task)} chars — compressing to brief...")
        brief = compress_task_brief(task, generate)
        log(f"  Compressed: {len(brief)} chars")
        # Internal artifact — goes into hidden .sage/ subdir to keep the
        # project root clean.
        sage_meta_dir = out_dir / ".sage"
        sage_meta_dir.mkdir(parents=True, exist_ok=True)
        (sage_meta_dir / "PROJECT_BRIEF.md").write_text(
            "# Project Brief\n\n" + brief + "\n\n---\n\n# Original Spec\n\n" + task,
            encoding="utf-8",
        )
    else:
        brief = task

    report: dict = {
        "stack": stack,
        "out_dir": str(out_dir),
        "files": [],
        "template_count": 0,
        "llm_count": 0,
        "review_failures": 0,
        "task_chars": len(task),
        "brief_chars": len(brief),
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

        prompt = build_file_prompt(brief, spec, tree, stack, versions)
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
            review = parse_review_response(generate(build_review_prompt(brief, spec, content)))
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
                    generate(build_review_prompt(brief, spec, content))
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

    # ── Runtime install + test pass ────────────────────────────────────
    # Run `npm install` + `npm test` for Node projects and `pip install`
    # + `pytest` for Python projects. Any failures get one regen pass with
    # the actual error log fed back to the model.
    report["install_ok"] = None
    report["tests_ok"] = None
    runtime_errors: list[str] = []

    if (out_dir / "package.json").exists():
        node_diag = validate_node_project(out_dir, log=log)
        if node_diag.get("ran"):
            report["install_ok"] = node_diag["install_ok"]
            report["tests_ok"] = node_diag["test_ok"]
            runtime_errors.extend(node_diag.get("errors", []))

    backend_root = out_dir / "backend"
    if backend_root.exists() and (backend_root / "pyproject.toml").exists():
        py_diag = validate_python_project(backend_root, log=log)
        if py_diag.get("ran"):
            report["backend_install_ok"] = py_diag["install_ok"]
            report["backend_tests_ok"] = py_diag["test_ok"]
            runtime_errors.extend(py_diag.get("errors", []))
    elif (out_dir / "pyproject.toml").exists():
        py_diag = validate_python_project(out_dir, log=log)
        if py_diag.get("ran"):
            report["install_ok"] = py_diag["install_ok"]
            report["tests_ok"] = py_diag["test_ok"]
            runtime_errors.extend(py_diag.get("errors", []))

    # If runtime checks failed, give the model one chance to fix them
    # using the actual error output. Reads the most-likely-relevant files
    # (package.json, jest config, tests) into the prompt.
    if runtime_errors:
        report["runtime_fixes"] = 0
        for err in runtime_errors[:2]:  # cap to avoid runaway regen loops
            relevant: dict[str, str] = {}
            for candidate in (
                "package.json", ".npmrc", "jest.config.js",
                "backend/pyproject.toml",
                "pyproject.toml",
                "__tests__/auth.test.tsx",
                "backend/tests/test_auth.py",
                "tests/test_auth.py",
            ):
                p = out_dir / candidate
                if p.exists():
                    relevant[candidate] = p.read_text("utf-8", errors="replace")
            try:
                raw = generate(build_runtime_fix_prompt(err, relevant))
                import json as _json
                # Find JSON block tolerantly
                start = raw.find("{")
                end = raw.rfind("}")
                if start != -1 and end != -1 and end > start:
                    fixes = _json.loads(raw[start : end + 1])
                    if isinstance(fixes, dict):
                        for path, new_content in fixes.items():
                            if isinstance(new_content, str) and len(new_content) > 10:
                                target = out_dir / path
                                target.parent.mkdir(parents=True, exist_ok=True)
                                target.write_text(new_content, encoding="utf-8")
                                report["runtime_fixes"] += 1
                                log(f"  ⚒ runtime-fix wrote {path}")
            except Exception as exc:
                log(f"  runtime-fix skipped: {exc}")

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
    "build_runtime_fix_prompt",
    "compress_task_brief",
    "decompose_multi_build_request",
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
    "plan_react_native_web",
    "plan_rust_axum",
    "plan_spring_boot",
    "strip_code_fences",
    "validate_file",
    "validate_node_project",
    "validate_python_project",
]
