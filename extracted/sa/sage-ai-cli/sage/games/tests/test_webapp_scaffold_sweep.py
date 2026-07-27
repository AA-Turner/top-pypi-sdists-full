"""Per-stack webapp + mobile scaffold integrity sweep.

User asked for "all coding languages for websites and mobile apps"
verified. This test sweeps every stack sage *advertises* and records
which ones actually get a framework-specific scaffold vs which produce
a generic file layout.

Honest assessment from this sweep:

  Tier 1 — FULLY scaffolded (root + dep file + framework conventions):
    fastapi, django, react, nextjs, react-native-web

  Tier 2 — Stack-aware layout (right file extension, generic structure)
    BUT missing framework-specific build file:
    rust-axum (.rs files but no Cargo.toml), go-microservices (.go but
    no go.mod), spring-boot (.java but no pom.xml), flutter (.dart but
    no pubspec.yaml), dotnet (.cs but no .csproj), laravel/rails/cpp
    (similar pattern).

  Tier 3 — Generic scaffold only (engine-specific files would come from
    the LLM at emit-time, not from the layout planner):
    android-compose, ios-swift, kubernetes, graphql.

These tests assert what's REAL — they pass when sage produces what it
actually produces today, and they'll fail (productively) when sage adds
or removes scaffold coverage for any stack.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import pytest

from sage.core.principal_engineer import detect_stack
from sage.core.project_layout import plan_layout
from sage.core.spec_decomposer import decompose_spec


# ───────────────────────── helpers ────────────────────────────────────


# Map: "the spec mentions <X>" → return this stack profile to the
# decomposer. The extract_stack prompt template injects the user spec
# *after* the literal phrase "Spec:" — so we slice on that boundary to
# avoid matching keywords from the prompt template itself (which mentions
# every framework name in its description of valid values).
_SPEC_DELIMITER = "spec:"


# Order matters: backend-specific keywords FIRST, then mobile, then
# generic frontends. First match wins.
_STACK_BY_KEYWORD: list[tuple[str, tuple[str | None, str | None]]] = [
    ("flutter",            ("flutter",       None)),
    ("android",            ("android-compose", None)),
    ("ios",                ("ios-swift",     None)),
    ("django",             (None,            "django")),
    ("fastapi",            (None,            "fastapi")),
    ("rust",               (None,            "rust-axum")),
    ("go ",                (None,            "go-microservices")),
    ("spring",             (None,            "spring-boot")),
    ("laravel",            (None,            "laravel")),
    ("rails",              (None,            "rails")),
    (".net",               (None,            "dotnet")),
    ("c++",                (None,            "cpp")),
    ("kubernetes",         (None,            "fastapi")),
    ("graphql",            (None,            "fastapi")),
    ("react native",       ("react-native-web", None)),
    ("next.js",            ("nextjs",        None)),
    ("react",              ("react",         None)),
]


def _stack_for_spec(spec: str) -> dict:
    lower = spec.lower()
    for kw, (frontend, backend) in _STACK_BY_KEYWORD:
        if kw in lower:
            return {"frontend": frontend, "backend": backend}
    return {"frontend": None, "backend": "fastapi"}


def _stub_gen(prompt_text: str) -> str:
    """Mimic LLM responses to extract_features + extract_stack.

    The extract_stack prompt template embeds the user's spec text inside
    a known marker; we slice on that marker so we don't match keywords
    from the prompt's *instructions* (which list every framework name).
    """
    lower = prompt_text.lower()
    # extract_stack: response must be a stack JSON.
    if "frontend" in lower and "backend" in lower:
        idx = lower.find(_SPEC_DELIMITER)
        spec_only = prompt_text[idx + len(_SPEC_DELIMITER):] if idx >= 0 else prompt_text
        return json.dumps(_stack_for_spec(spec_only))
    # extract_features: response is a list.
    return json.dumps([
        {"name": "users",  "acceptance": "Users can be registered + listed"},
        {"name": "health", "acceptance": "Health endpoint returns 200"},
    ])


def _files_for(prompt: str) -> set[str]:
    plan = decompose_spec(prompt, _stub_gen)
    layout = plan_layout(plan)
    return {f.path for f in layout.files}


# ───────────────────────── stacks: detection + routing ────────────────


_STACKS = [
    ("Build me a FastAPI backend with JWT auth and PostgreSQL",     "fastapi"),
    ("Build a Django app with DRF, admin, and a model layer",       "django"),
    ("Build a React + Vite TypeScript SPA",                          "react"),
    ("Build a Next.js 14 dashboard with App Router",                 "nextjs"),
    ("Build a React Native + Web app with Expo Router",              "react-native-web"),
    ("Build a Go microservice with Gin for orders",                  "go-microservices"),
    ("Build a Rust Axum API for analytics",                          "rust-axum"),
    ("Build a Spring Boot Java API for banking",                     "spring-boot"),
    ("Build an Android app with Jetpack Compose in Kotlin",          "android-compose"),
    ("Build an iOS app with SwiftUI",                                "ios-swift"),
    ("Build a Flutter app for note-taking",                          "flutter"),
    ("Build a .NET ASP.NET Core API",                                "dotnet"),
    ("Build a Laravel PHP API",                                      "laravel"),
    ("Build a Ruby on Rails app for a forum",                        "rails"),
    ("Build a C++ microservice for trading",                         "cpp"),
    ("Build a GraphQL API with Apollo Server",                       "graphql"),
    ("Build a Kubernetes deployment with Helm",                      "kubernetes"),
]


@pytest.mark.parametrize("prompt,expected_stack", _STACKS)
def test_decompose_spec_routes_each_stack_to_webapp_task_type(prompt, expected_stack):
    """Every stack prompt must classify as webapp (not game) so it routes
    through the principal pipeline — not the games pipeline."""
    plan = decompose_spec(prompt, _stub_gen)
    assert plan.task_type == "webapp"
    assert detect_stack(prompt) == expected_stack


# ───────────────────────── universal scaffold invariants ──────────────


@pytest.mark.parametrize("prompt,stack", _STACKS)
def test_every_stack_scaffold_includes_root_hygiene_files(prompt, stack):
    """Every stack scaffold must produce README + .gitignore + CI workflow
    + .env.example. These are tier-0 hygiene files; their absence indicates
    sage forgot to emit root templates for this stack."""
    files = _files_for(prompt)
    for required in (
        "README.md",
        ".gitignore",
        ".env.example",
        ".github/workflows/ci.yml",
    ):
        assert required in files, f"{stack}: missing {required}"


# ───────────────────────── Tier 1 — fully scaffolded stacks ───────────


def test_fastapi_layout_includes_python_dep_files_and_app_init():
    files = _files_for("Build me a FastAPI backend with JWT auth")
    assert "backend/requirements.txt" in files
    assert "backend/pyproject.toml" in files
    assert "backend/app/main.py" in files
    # Per-feature backend files
    assert any(f.startswith("backend/app/api/") for f in files)
    assert any(f.startswith("backend/app/services/") for f in files)


def test_django_layout_emits_python_dep_files():
    """Django shares the Python-backend dep emission path with FastAPI.
    Verify requirements.txt + pyproject.toml ship."""
    files = _files_for("Build a Django app with DRF and admin")
    assert "backend/requirements.txt" in files
    assert "backend/pyproject.toml" in files


def test_react_layout_includes_package_json():
    files = _files_for("Build a React + Vite TypeScript SPA")
    has_frontend_pkg = "frontend/package.json" in files or "package.json" in files
    assert has_frontend_pkg, f"React scaffold has no package.json. Files: {sorted(files)}"


def test_nextjs_layout_includes_package_json():
    files = _files_for("Build a Next.js 14 dashboard")
    has_frontend_pkg = "frontend/package.json" in files or "package.json" in files
    assert has_frontend_pkg


def test_react_native_web_layout_includes_package_json():
    files = _files_for("Build a React Native + Web app with Expo")
    has_pkg = "frontend/package.json" in files or "package.json" in files
    assert has_pkg


# ───────────────────────── Tier 2 — stack-aware extensions ────────────


@pytest.mark.parametrize("prompt,expected_ext", [
    ("Build a Rust Axum API for analytics",              ".rs"),
    ("Build a Go microservice with Gin for orders",      ".go"),
    ("Build a Spring Boot Java API for banking",         ".java"),
])
def test_tier2_backend_stacks_produce_correct_file_extensions(prompt, expected_ext):
    """Backend stacks in tier 2 don't get framework-specific build files
    yet, but the file extensions in backend/src/ should match the
    language. Wrong extension means the language pick is broken."""
    files = _files_for(prompt)
    has_lang_files = any(f.endswith(expected_ext) for f in files)
    assert has_lang_files, (
        f"prompt {prompt!r} produced no {expected_ext} files. "
        f"Files: {sorted(files)}"
    )


@pytest.mark.xfail(
    reason="Flutter is a FRONTEND framework (mobile + web) but sage's "
           "_stack_package_files + per-feature path-assignment only knows "
           "React/Next.js for frontend. Flutter prompts get a React "
           "scaffold + .npmrc + tsconfig instead of pubspec.yaml + .dart "
           "files. Same gap exists for android-compose + ios-swift.",
    strict=True,
)
def test_flutter_layout_includes_dart_files():
    files = _files_for("Build a Flutter app for note-taking")
    assert any(f.endswith(".dart") for f in files), \
        f"Flutter scaffold has no .dart files. Got: {sorted(files)}"


# ───────────────────────── KNOWN GAPS — documented xfails ─────────────


@pytest.mark.xfail(
    reason="Sage advertises support for these stacks but plan_layout only "
           "emits framework-specific build files for fastapi/django/flask "
           "and react/nextjs/react-native-web. Other stacks (rust-axum, "
           "go-microservices, spring-boot, flutter, dotnet, laravel, rails, "
           "cpp) produce stack-aware file extensions but NO Cargo.toml / "
           "go.mod / pom.xml / pubspec.yaml / .csproj / composer.json / "
           "Gemfile / CMakeLists.txt. The LLM must fill this in at emit "
           "time, which is unreliable. Adding deterministic dep-file "
           "templates for these stacks is a real product gap.",
    strict=True,
)
@pytest.mark.parametrize("prompt,dep_file", [
    ("Build a Rust Axum API for analytics",                       "backend/Cargo.toml"),
    ("Build a Go microservice with Gin for orders",               "backend/go.mod"),
    ("Build a Spring Boot Java API for banking",                  "backend/pom.xml"),
    ("Build a Flutter app for note-taking",                       "frontend/pubspec.yaml"),
    ("Build a .NET ASP.NET Core API",                             "backend/app.csproj"),
    ("Build a Laravel PHP API",                                   "backend/composer.json"),
    ("Build a Ruby on Rails app for a forum",                     "backend/Gemfile"),
    ("Build a C++ microservice for trading",                      "backend/CMakeLists.txt"),
    ("Build an Android app with Jetpack Compose in Kotlin",       "frontend/build.gradle"),
    ("Build an iOS app with SwiftUI",                             "frontend/Package.swift"),
])
def test_tier3_stack_gap_no_framework_dep_file(prompt, dep_file):
    """KNOWN GAP — these stacks don't get a deterministic build/dep file.
    This test is xfailed so the gap is visible in test reports without
    blocking CI. When sage adds the missing template, remove the xfail."""
    files = _files_for(prompt)
    assert dep_file in files, (
        f"sage does not scaffold {dep_file!r} for prompt {prompt!r}. "
        f"Files: {sorted(files)}"
    )


# ───────────────────────── stack-package-files probe ──────────────────


def test_stack_package_files_only_handles_python_and_node():
    """_stack_package_files only emits framework files for python +
    node stacks. Lock down what's actually supported so the gap is
    visible in the source-of-truth tests, not just docs."""
    from sage.core.project_layout import _stack_package_files
    from sage.core.spec_decomposer import ProjectPlan, StackProfile

    # Python backend → requirements.txt + pyproject.toml
    plan = ProjectPlan(title="x", features=[], task_type="webapp",
                       stack=StackProfile(backend="fastapi"))
    paths = {f.path for f in _stack_package_files(plan)}
    assert "backend/requirements.txt" in paths
    assert "backend/pyproject.toml" in paths

    # React frontend → package.json + tsconfig
    plan = ProjectPlan(title="x", features=[], task_type="webapp",
                       stack=StackProfile(frontend="react"))
    paths = {f.path for f in _stack_package_files(plan)}
    assert "frontend/package.json" in paths
    assert "frontend/tsconfig.json" in paths

    # Rust backend → nothing today (gap)
    plan = ProjectPlan(title="x", features=[], task_type="webapp",
                       stack=StackProfile(backend="rust-axum"))
    paths = {f.path for f in _stack_package_files(plan)}
    assert paths == set(), (
        f"Rust-axum produced package files {paths} — gap may have been closed, "
        "update this test."
    )
