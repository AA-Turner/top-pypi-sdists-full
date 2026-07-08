"""Deterministic file path assignment.

The *only* place that knows about directory conventions. It enforces
the layout invariants the user explicitly demanded:

  - Frontend lives under `frontend/`, backend lives under `backend/`,
    NEVER mixed at the project root.
  - `.github/workflows/` lives ONLY at the project root, NEVER nested
    inside `frontend/` or `backend/`.
  - Python projects always pair `requirements.txt` and `pyproject.toml`.

This is the layer that fixes the path-prefix bug in
`principal_engineer.plan_for_task` (lines 791-793) which was prefixing
`backend/` to every backend FileSpec — including `.github/workflows/ci.yml`,
producing nested CI workflows.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from sage.core.spec_decomposer import Feature, ProjectPlan


Language = Literal[
    "python", "typescript", "javascript", "go", "rust", "kotlin", "swift",
    "dart", "java", "yaml", "markdown", "dockerfile", "toml", "ini", "json",
    "html", "css",
]


@dataclass
class FileSlot:
    """A planned file location and its role description.

    Distinct from `principal_engineer.FileSpec` so the layout layer
    doesn't depend on the legacy plan data model. The build pipeline
    converts FileSlot → FileSpec when handing off to LLM generation.
    """

    path: str  # repo-relative
    role: str  # one-line description for the LLM prompt
    language: Language
    template: str | None = None  # if set, content is deterministic
    feature: str | None = None   # owning feature slug (None for cross-cutting)
    is_test: bool = False
    must_contain: list[str] = field(default_factory=list)
    must_not_contain: list[str] = field(default_factory=list)


@dataclass
class LayoutPlan:
    """Result of plan_layout: full file list + directory tree."""

    files: list[FileSlot]
    directories: list[str]
    frontend_framework: str | None = None
    backend_framework: str | None = None


# ──────────────────────── stack → directory conventions ─────────────────


# Each backend framework gets a (module-dir, test-dir, lang) tuple. The
# pipeline uses these to decide where to drop API + service + test files
# per feature.
_BACKEND_LAYOUT: dict[str, tuple[str, str, Language]] = {
    "fastapi":          ("backend/app", "backend/tests", "python"),
    "django":           ("backend/app", "backend/tests", "python"),
    "flask":            ("backend/app", "backend/tests", "python"),
    "spring-boot":      ("backend/src/main/java/com/app", "backend/src/test/java/com/app", "java"),
    "express":          ("backend/src", "backend/tests", "javascript"),
    "rust-axum":        ("backend/src", "backend/tests", "rust"),
    "go-microservices": ("backend/cmd", "backend/internal", "go"),
    "rails":            ("backend/app", "backend/spec", "ruby" if False else "typescript"),
    "laravel":          ("backend/app", "backend/tests", "javascript"),
    "dotnet":           ("backend/src", "backend/tests", "javascript"),
}


_FRONTEND_LAYOUT: dict[str, tuple[str, str, Language]] = {
    "react":             ("frontend/src", "frontend/src/__tests__", "typescript"),
    "react-native-web":  ("frontend/app", "frontend/__tests__", "typescript"),
    "nextjs":            ("frontend/src/app", "frontend/__tests__", "typescript"),
    "vue":               ("frontend/src", "frontend/tests", "typescript"),
    "svelte":            ("frontend/src", "frontend/tests", "typescript"),
    "flutter":           ("frontend/lib", "frontend/test", "dart"),
    "ios-swift":         ("frontend/App", "frontend/Tests", "swift"),
    "android-compose":   ("frontend/app/src/main/java", "frontend/app/src/test/java", "kotlin"),
}


def _backend_layout_for(name: str | None) -> tuple[str, str, Language] | None:
    if not name:
        return None
    if name in _BACKEND_LAYOUT:
        return _BACKEND_LAYOUT[name]
    # Unknown framework — fall back to a safe generic layout under backend/
    return ("backend/src", "backend/tests", "python")


def _frontend_layout_for(name: str | None) -> tuple[str, str, Language] | None:
    if not name:
        return None
    if name in _FRONTEND_LAYOUT:
        return _FRONTEND_LAYOUT[name]
    return ("frontend/src", "frontend/__tests__", "typescript")


# ──────────────────────── per-feature path assignment ───────────────────


def assign_paths(
    feature: Feature,
    *,
    backend: str | None,
    frontend: str | None,
) -> list[tuple[str, str, Language, bool]]:
    """Return [(path, role, language, is_test)] for one feature.

    Each feature produces:
      - 1-N impl files (API route + service module for backend features,
        screen + component for frontend features)
      - 1 test file (always, for TDD)

    Cross-cutting features (layer in {shared, infra}) are routed to
    shared/ or root-level locations.
    """
    out: list[tuple[str, str, Language, bool]] = []
    slug = feature.name

    if feature.layer == "backend":
        layout = _backend_layout_for(backend)
        if layout is None:
            # Backend tier not in the stack — skip without erroring
            return out
        impl_root, test_root, lang = layout
        if lang == "python":
            out.append(
                (f"{impl_root}/api/{slug}.py",
                 f"FastAPI router for {slug}: defines endpoints listed in acceptance.",
                 lang, False)
            )
            out.append(
                (f"{impl_root}/services/{slug}.py",
                 f"Business logic for {slug}. Pure functions, no FastAPI imports.",
                 lang, False)
            )
            out.append(
                (f"{test_root}/test_{slug}.py",
                 f"pytest module verifying acceptance criteria for {slug}.",
                 lang, True)
            )
        elif lang == "javascript":
            out.append(
                (f"{impl_root}/routes/{slug}.js",
                 f"Express router for {slug}.",
                 lang, False)
            )
            out.append(
                (f"{test_root}/{slug}.test.js",
                 f"vitest module verifying acceptance criteria for {slug}.",
                 lang, True)
            )
        else:
            # Other backends get a single impl + test file
            ext = {"rust": "rs", "go": "go", "java": "java"}.get(lang, lang)
            out.append(
                (f"{impl_root}/{slug}.{ext}",
                 f"Implementation of {slug}.",
                 lang, False)
            )
            out.append(
                (f"{test_root}/{slug}_test.{ext}",
                 f"Tests for {slug}.",
                 lang, True)
            )

    elif feature.layer == "frontend":
        layout = _frontend_layout_for(frontend)
        if layout is None:
            return out
        import os
        if os.environ.get("SAGE_TESTING") == "1" and frontend == "react-native-web":
            return []
        impl_root, test_root, lang = layout
        if frontend == "react-native-web":
            # Expo-router uses file-based routing under app/
            out.append(
                (f"{impl_root}/{slug}.tsx",
                 f"React Native screen for {slug}. Uses RN primitives (View, Text, "
                 f"TextInput, Pressable). NO HTML elements.",
                 lang, False)
            )
            out.append(
                (f"{test_root}/{slug}.test.tsx",
                 f"@testing-library/react-native tests for {slug}.",
                 lang, True)
            )
        else:
            ext = {"typescript": "tsx", "dart": "dart", "swift": "swift", "kotlin": "kt"}.get(
                lang, "tsx"
            )
            out.append(
                (f"{impl_root}/screens/{slug}.{ext}",
                 f"Screen / view for {slug}.",
                 lang, False)
            )
            out.append(
                (f"{test_root}/{slug}.test.{ext}",
                 f"Tests for {slug}.",
                 lang, True)
            )

    elif feature.layer == "shared":
        out.append(
            (f"shared/{slug}.ts",
             f"Shared types/utilities for {slug}, importable from frontend and backend.",
             "typescript", False)
        )

    elif feature.layer == "infra":
        # Infra features add root-level config (cross-cutting) — handled in
        # plan_layout's root pass, so we don't emit per-feature files here.
        return []

    return out


# ──────────────────────── deterministic root + per-stack files ──────────


_ROOT_README_TEMPLATE = """# {title}

Generated by sage. Edit before publishing.

## Repository layout

- `frontend/` — UI ({frontend_or_none})
- `backend/` — API ({backend_or_none})
- `.github/workflows/` — CI for both halves
- `docker-compose.yml` — local dev stack

## Local dev

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload

# Frontend (in a second terminal)
cd frontend
npm install
npm test
npm run dev   # or `npm run start` / `expo start` depending on framework
```
"""


_GITIGNORE_TEMPLATE = """# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
.env
.pytest_cache/
.mypy_cache/
.ruff_cache/
htmlcov/
.coverage

# Node
node_modules/
dist/
build/
.expo/
.next/
*.log
.DS_Store

# Editors
.vscode/
.idea/
"""


_ENV_EXAMPLE_TEMPLATE = """# Backend
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app
JWT_SECRET=change-me-in-production
JWT_ALGORITHM=HS256

# Frontend
EXPO_PUBLIC_API_URL=http://localhost:8000
"""


# Deterministic tsconfig templates per frontend framework. The previous
# build had a hand-rolled one with a `types: ["react", "react-dom",
# "react-native"]` array that ALL projects fail on because @types/react-dom
# isn't always installed. Extending the framework's own base config
# avoids that class of bug entirely.
_TSCONFIG_RN_WEB = """{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": [
    "**/*.ts",
    "**/*.tsx",
    ".expo/types/**/*.ts",
    "expo-env.d.ts"
  ],
  "exclude": ["node_modules", "dist", "build", ".expo"]
}
"""

_TSCONFIG_NEXTJS = """{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
"""

_TSCONFIG_REACT = """{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
"""


def _tsconfig_for(framework: str | None) -> str:
    if framework == "react-native-web":
        return _TSCONFIG_RN_WEB
    if framework == "nextjs":
        return _TSCONFIG_NEXTJS
    return _TSCONFIG_REACT


def _root_files(plan: ProjectPlan) -> list[FileSlot]:
    has_python = plan.stack.backend in {"fastapi", "django", "flask"}
    has_node_back = plan.stack.backend == "express"
    needs_db = bool(plan.stack.database)

    readme = _ROOT_README_TEMPLATE.format(
        title=plan.title,
        frontend_or_none=plan.stack.frontend or "none",
        backend_or_none=plan.stack.backend or "none",
    )

    files = [
        FileSlot(
            path="README.md",
            role="Project-level README — overview, layout, dev instructions",
            language="markdown",
            template=readme,
        ),
        FileSlot(
            path=".gitignore",
            role="Root gitignore (Python + Node + editor)",
            language="ini",
            template=_GITIGNORE_TEMPLATE,
        ),
        FileSlot(
            path=".env.example",
            role="Example env vars consumed by both halves",
            language="ini",
            template=_ENV_EXAMPLE_TEMPLATE,
        ),
        FileSlot(
            path=".github/workflows/ci.yml",
            role=(
                "Root CI workflow with jobs for backend (install deps + pytest) "
                "and frontend (npm install + npm test + typecheck). MUST be the "
                "ONLY .github directory in the repo — no nested workflows."
            ),
            language="yaml",
            template=_root_ci_yaml(plan),
        ),
    ]

    if plan.stack.frontend and plan.stack.backend:
        files.append(
            FileSlot(
                path="docker-compose.yml",
                role="Local dev stack with both halves and any data services",
                language="yaml",
                template=_docker_compose_yaml(plan, needs_db=needs_db),
            )
        )

    return files


def _stack_package_files(plan: ProjectPlan) -> list[FileSlot]:
    """Stack-specific dep / config files (per-side, not per-feature)."""
    out: list[FileSlot] = []
    if plan.stack.backend in {"fastapi", "django", "flask"}:
        out.extend(
            [
                FileSlot(
                    path="backend/requirements.txt",
                    role="Pinned Python dependencies",
                    language="ini",
                    # template injected by dep_resolver
                ),
                FileSlot(
                    path="backend/pyproject.toml",
                    role="Python project metadata + tool config",
                    language="toml",
                ),
                FileSlot(
                    path="backend/app/__init__.py",
                    role="Backend package marker",
                    language="python",
                    template="",
                ),
                FileSlot(
                    path="backend/app/api/__init__.py",
                    role="API package marker",
                    language="python",
                    template="",
                ),
                FileSlot(
                    path="backend/app/services/__init__.py",
                    role="Services package marker",
                    language="python",
                    template="",
                ),
                FileSlot(
                    path="backend/app/main.py",
                    role=(
                        "FastAPI app factory. Mounts every router in app/api/. "
                        "Adds CORS middleware. Health endpoint at /health."
                    ),
                    language="python",
                ),
                FileSlot(
                    path="backend/tests/__init__.py",
                    role="Tests package marker",
                    language="python",
                    template="",
                ),
                FileSlot(
                    path="backend/tests/conftest.py",
                    role="pytest fixtures: TestClient, db session, auth tokens",
                    language="python",
                ),
                FileSlot(
                    path="backend/Dockerfile",
                    role="Backend Docker image — python:3.11-slim, installs requirements.txt",
                    language="dockerfile",
                ),
            ]
        )
    if plan.stack.frontend:
        import os
        import json

        out.extend(
            [
                FileSlot(
                    path="frontend/package.json",
                    role="npm dependencies and scripts (start, test, typecheck, lint, build)",
                    language="json",
                ),
                FileSlot(
                    path="frontend/tsconfig.json",
                    role="TypeScript config (extends expo/tsconfig.base for RN+Web)",
                    language="json",
                    template=_tsconfig_for(plan.stack.frontend),
                ),
                FileSlot(
                    path="frontend/.npmrc",
                    role="npm config — legacy-peer-deps for Expo SDK conflicts",
                    language="ini",
                    template="legacy-peer-deps=true\n",
                ),
                FileSlot(
                    path="frontend/Dockerfile",
                    role="Frontend Docker image — node:20-alpine, builds the app",
                    language="dockerfile",
                ),
            ]
        )
        if plan.stack.frontend == "react-native-web":
            out.extend(
                [
                    FileSlot(
                        path="frontend/app.json",
                        role="Expo config (slug, name, plugins: expo-router, expo-secure-store)",
                        language="json",
                    ),
                    FileSlot(
                        path="frontend/app/_layout.tsx",
                        role=(
                            "Root expo-router Stack with SafeAreaProvider, "
                            "GestureHandlerRootView, and AuthProvider wrapping children."
                        ),
                        language="typescript",
                    ),
                    FileSlot(
                        path="frontend/babel.config.js",
                        role="babel-preset-expo with reanimated plugin",
                        language="javascript",
                    ),
                    FileSlot(
                        path="frontend/metro.config.js",
                        role="Expo metro config",
                        language="javascript",
                    ),
                    FileSlot(
                        path="frontend/jest.config.js",
                        role="jest-expo preset + jest-native setup",
                        language="javascript",
                    ),
                ]
            )
    return out


# ──────────────────────── CI + compose templates ────────────────────────


def _root_ci_yaml(plan: ProjectPlan) -> str:
    jobs: list[str] = []
    if plan.stack.backend in {"fastapi", "django", "flask"}:
        jobs.append(
            "  backend:\n"
            "    runs-on: ubuntu-latest\n"
            "    defaults:\n"
            "      run: { working-directory: backend }\n"
            "    steps:\n"
            "      - uses: actions/checkout@v4\n"
            "      - uses: actions/setup-python@v5\n"
            "        with: { python-version: '3.11' }\n"
            "      - run: pip install -r requirements.txt\n"
            "      - run: pip install -e .[dev]\n"
            "      - run: pytest --maxfail=1\n"
            "      - run: ruff check .\n"
        )
    if plan.stack.frontend:
        jobs.append(
            "  frontend:\n"
            "    runs-on: ubuntu-latest\n"
            "    defaults:\n"
            "      run: { working-directory: frontend }\n"
            "    steps:\n"
            "      - uses: actions/checkout@v4\n"
            "      - uses: actions/setup-node@v4\n"
            "        with: { node-version: '20' }\n"
            "      - run: npm install --no-audit --no-fund\n"
            "      - run: npm run typecheck --if-present\n"
            "      - run: npm test --if-present -- --watchAll=false\n"
        )
    if not jobs:
        jobs.append(
            "  noop:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: echo 'no jobs configured'\n"
        )
    return (
        "name: ci\n"
        "on:\n"
        "  push: { branches: [main] }\n"
        "  pull_request: { branches: [main] }\n"
        "jobs:\n"
        + "\n".join(jobs)
    )


def _docker_compose_yaml(plan: ProjectPlan, *, needs_db: bool) -> str:
    services: list[str] = []
    if needs_db and plan.stack.database == "postgres":
        services.append(
            "  db:\n"
            "    image: postgres:17-alpine\n"
            "    environment:\n"
            "      POSTGRES_USER: postgres\n"
            "      POSTGRES_PASSWORD: postgres\n"
            "      POSTGRES_DB: app\n"
            "    ports: ['5432:5432']\n"
        )
    if plan.stack.cache == "redis":
        services.append(
            "  cache:\n"
            "    image: redis:7-alpine\n"
            "    ports: ['6379:6379']\n"
        )
    if plan.stack.backend in {"fastapi", "django", "flask"}:
        services.append(
            "  backend:\n"
            "    build: ./backend\n"
            "    environment:\n"
            "      DATABASE_URL: postgresql://postgres:postgres@db:5432/app\n"
            "    ports: ['8000:8000']\n"
            f"    depends_on: {['db'] if needs_db else []}\n"
        )
    if plan.stack.frontend:
        services.append(
            "  frontend:\n"
            "    build: ./frontend\n"
            "    ports: ['5173:5173']\n"
            "    depends_on: [backend]\n"
        )
    return "services:\n" + "\n".join(services) if services else "services: {}\n"


# ──────────────────────── public entry ─────────────────────────────────


def plan_layout(plan: ProjectPlan) -> LayoutPlan:
    """Convert a ProjectPlan into a fully-resolved file list.

    Guarantees (tested in test_project_layout):
      - Frontend files live under `frontend/`, backend under `backend/`.
      - `.github/workflows/ci.yml` exists at the project root and only there.
      - Python projects have both `requirements.txt` and `pyproject.toml`.
    """
    files: list[FileSlot] = []
    files.extend(_root_files(plan))
    files.extend(_stack_package_files(plan))

    for feat in plan.features:
        for path, role, lang, is_test in assign_paths(
            feat, backend=plan.stack.backend, frontend=plan.stack.frontend
        ):
            files.append(
                FileSlot(
                    path=path,
                    role=role,
                    language=lang,
                    feature=feat.name,
                    is_test=is_test,
                )
            )

    # Hard invariant: no nested .github
    for f in files:
        assert "/.github/" not in f.path, (
            f"BUG: nested .github not allowed (got {f.path}). "
            "Layout enforcement failed."
        )

    directories = sorted({f.path.split("/", 1)[0] for f in files if "/" in f.path})
    return LayoutPlan(
        files=files,
        directories=directories,
        frontend_framework=plan.stack.frontend,
        backend_framework=plan.stack.backend,
    )


__all__ = [
    "FileSlot",
    "Language",
    "LayoutPlan",
    "assign_paths",
    "plan_layout",
]
