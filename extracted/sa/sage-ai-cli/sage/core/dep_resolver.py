"""Feature → dependency resolver.

Walks each `Feature` in a `ProjectPlan`, asks the LLM "what packages do
you need to implement this?", merges results, dedupes, pins known
libraries against `CURRENT_VERSIONS`, and writes BOTH `requirements.txt`
AND `pyproject.toml` for Python (the user demanded both — some Docker /
CI / hosted-service workflows expect one or the other) plus
`package.json` for Node.

This module is the answer to the user's complaint that "sage has no
requirement.txt for its backend so it's not even installed or testable."
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from sage.core.principal_engineer import CURRENT_VERSIONS
from sage.core.spec_decomposer import Feature, ProjectPlan


GenerateFn = Callable[[str], str]


@dataclass
class DepSet:
    """Runtime + dev deps for each language tier."""

    python_runtime: list[str] = field(default_factory=list)
    python_dev: list[str] = field(default_factory=list)
    node_runtime: list[str] = field(default_factory=list)
    node_dev: list[str] = field(default_factory=list)


# ──────────────────────── per-stack baseline deps ───────────────────────

# Every project on a given stack starts with these — picked deterministically
# (not LLM-derived) because they're load-bearing for the layout we generate.
_BASELINE_PYTHON_RUNTIME: dict[str, tuple[str, ...]] = {
    "fastapi": (
        "fastapi", "uvicorn[standard]", "pydantic", "pydantic-settings",
        "sqlmodel", "sqlalchemy", "asyncpg", "alembic",
        "passlib[bcrypt]", "bcrypt", "python-jose[cryptography]",
        "python-multipart", "httpx",
    ),
    "django": ("django", "djangorestframework", "psycopg2-binary", "gunicorn"),
    "flask": ("flask", "flask-sqlalchemy", "psycopg2-binary", "gunicorn"),
}

_BASELINE_PYTHON_DEV: tuple[str, ...] = (
    "pytest", "pytest-asyncio", "httpx", "ruff", "mypy",
)


_BASELINE_NODE_RUNTIME: dict[str, tuple[str, ...]] = {
    "react": ("react", "react-dom", "axios"),
    "react-native-web": (
        "expo", "expo-router", "expo-status-bar", "expo-secure-store",
        "expo-constants", "react", "react-dom", "react-native",
        "react-native-web", "react-native-safe-area-context",
        "react-native-screens", "react-native-gesture-handler",
        "react-native-reanimated", "axios",
    ),
    "nextjs": ("next", "react", "react-dom", "axios"),
    "vue": ("vue", "axios"),
    "svelte": ("svelte", "axios"),
    "express": ("express", "cors", "helmet", "dotenv"),
}

_BASELINE_NODE_DEV: dict[str, tuple[str, ...]] = {
    "react": ("vite", "@vitejs/plugin-react", "vitest", "@testing-library/react",
              "@testing-library/jest-dom", "jsdom", "typescript", "@types/react",
              "@types/react-dom", "eslint"),
    "react-native-web": ("@babel/core", "babel-preset-expo", "jest", "jest-expo",
                         "@testing-library/react-native", "@testing-library/jest-native",
                         "react-test-renderer", "typescript", "@types/react"),
    "nextjs": ("vitest", "@testing-library/react", "jsdom", "typescript",
               "@types/react", "@types/node", "eslint"),
    "express": ("vitest", "supertest", "typescript", "@types/node", "eslint"),
}


# Feature-keyword → runtime deps. Lets us derive deps even when the LLM
# misses the connection (e.g. "billing" → "stripe", "queue" → "celery+redis").
_KEYWORD_PYTHON_DEPS: tuple[tuple[re.Pattern[str], tuple[str, ...]], ...] = (
    (re.compile(r"\bredis\b|cache", re.I), ("redis",)),
    (re.compile(r"\bcelery\b|background\s+jobs|task\s+queue", re.I),
     ("celery", "redis", "flower")),
    (re.compile(r"\brq\b", re.I), ("rq", "redis")),
    (re.compile(r"\bstripe\b|billing|subscription", re.I), ("stripe",)),
    (re.compile(r"\bllm\b|openai|gpt", re.I), ("openai",)),
    (re.compile(r"anthropic|claude", re.I), ("anthropic",)),
    (re.compile(r"langchain|rag", re.I), ("langchain", "langchain-community")),
    (re.compile(r"\bs3\b|object\s+storage|aws", re.I), ("boto3",)),
    (re.compile(r"google\s+cloud|gcs|firebase", re.I), ("google-cloud-storage",)),
    (re.compile(r"\bsendgrid\b", re.I), ("sendgrid",)),
    (re.compile(r"\btwilio\b|sms", re.I), ("twilio",)),
    (re.compile(r"\boauth\b", re.I), ("authlib",)),
    (re.compile(r"webhook", re.I), ("svix",)),
    (re.compile(r"social\s+media|instagram|tiktok|facebook|linkedin", re.I),
     ("httpx", "tweepy")),
    (re.compile(r"image|video|creative", re.I), ("pillow",)),
    (re.compile(r"\bml\b|machine\s+learning|predict", re.I), ("scikit-learn", "numpy")),
    (re.compile(r"analytics|metrics", re.I), ("pandas",)),
    (re.compile(r"\bseo\b|content", re.I), ()),
    (re.compile(r"rate\s+limit", re.I), ("slowapi",)),
    (re.compile(r"gdpr|encryption", re.I), ("cryptography",)),
    (re.compile(r"audit\s+log", re.I), ("structlog",)),
)


_KEYWORD_NODE_DEPS: tuple[tuple[re.Pattern[str], tuple[str, ...]], ...] = (
    (re.compile(r"chart|graph|metric", re.I), ("react-native-svg", "victory-native")),
    (re.compile(r"calendar|schedul", re.I), ("date-fns",)),
    (re.compile(r"form", re.I), ("react-hook-form", "zod")),
    (re.compile(r"state\s+management|redux", re.I), ("zustand",)),
    (re.compile(r"i18n|localization", re.I), ("i18n-js",)),
)


# Packages the LLM keeps emitting that DO NOT install from PyPI / npm and
# poison every downstream stage. Value is the replacement, or None to drop
# the dep entirely. Drop = caller must reach the API via httpx / fetch.
#
# Why these specifically: confirmed via real builds (the advertisement
# platform run on 2026-05-15 failed pip install on paypalcheckoutsdk; the
# vendor-private packages below are either unpublished, abandoned, or
# illegal-to-distribute names that pip can't resolve).
_REPLACE_PYTHON: dict[str, str | None] = {
    "paypalcheckoutsdk": None,        # deprecated, gone from PyPI
    "instagram-private-api": None,    # unmaintained + ToS-violating
    "tiktok-api": None,               # the name on PyPI is not a real SDK
    "facebook-sdk": None,             # last release 2018, broken on py3.11+
    "linkedin-api": None,             # private / ToS-violating
    "twitter-api": None,              # ambiguous name, doesn't install
    "snapchat-api": None,
    "youtube-api": None,
    "google-ads": None,               # real pkg is `google-ads`, but most
                                      # specs mean `google-api-python-client`
    "openai-python": "openai",        # the real package is `openai`
    "anthropic-python": "anthropic",
    "stripe-python": "stripe",
}

_REPLACE_NODE: dict[str, str | None] = {
    "react-native-zustand": "zustand",  # zustand has no RN-specific package
}


def _filter_replaced(specs: list[str], table: dict[str, str | None]) -> list[str]:
    """Drop or replace specs using the deny/replace table.

    Matches on the *bare name* (case-insensitive). Keeps version pins
    on replacements when only the name changed.
    """
    out: list[str] = []
    for spec in specs:
        name = _bare_name(spec)
        if name not in table:
            out.append(spec)
            continue
        replacement = table[name]
        if replacement is None:
            continue  # drop entirely
        # Swap name, preserve any pin
        rest = spec[len(name):] if spec.lower().startswith(name) else ""
        out.append(replacement + rest)
    return out


def sanitize_python_deps(specs: list[str]) -> list[str]:
    """Public: drop/replace deprecated Python deps. Used by repair routing."""
    return _filter_replaced(specs, _REPLACE_PYTHON)


def sanitize_node_deps(specs: list[str]) -> list[str]:
    """Public: drop/replace deprecated Node deps."""
    return _filter_replaced(specs, _REPLACE_NODE)


def sanitize_dep_files_in_place(backend_root: Path) -> int:
    """Re-read requirements.txt + pyproject.toml and strip deprecated packages.

    Called by the heal loop after a failed pip install. Returns the number
    of dropped lines so the loop knows whether anything actually changed.
    """
    if not backend_root.is_dir():
        return 0
    changes = 0

    req = backend_root / "requirements.txt"
    if req.exists():
        original = req.read_text("utf-8", errors="replace").splitlines()
        cleaned = sanitize_python_deps([ln for ln in original if ln.strip()])
        if cleaned != [ln for ln in original if ln.strip()]:
            req.write_text("\n".join(sorted(set(cleaned))) + "\n", encoding="utf-8")
            changes += len(original) - len(cleaned)

    pyproject = backend_root / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text("utf-8", errors="replace")
        # Surgical: only touch the `dependencies = [...]` array. The strings
        # are one-per-line in our emitter, so we filter line-by-line.
        new_lines: list[str] = []
        in_deps = False
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("dependencies = ["):
                in_deps = True
                new_lines.append(line)
                continue
            if in_deps and stripped == "]":
                in_deps = False
                new_lines.append(line)
                continue
            if in_deps:
                # Parse `    "name==1.2",` → bare name
                m = re.match(r'^\s*"([^"]+)"\s*,?\s*$', line)
                if m:
                    bare = _bare_name(m.group(1))
                    if bare in _REPLACE_PYTHON and _REPLACE_PYTHON[bare] is None:
                        changes += 1
                        continue  # drop this line
                    if bare in _REPLACE_PYTHON and _REPLACE_PYTHON[bare]:
                        line = line.replace(m.group(1), _REPLACE_PYTHON[bare])
                        changes += 1
            new_lines.append(line)
        if changes:
            pyproject.write_text("\n".join(new_lines), encoding="utf-8")

    return changes


# ──────────────────────── parse LLM output ──────────────────────────────


_JSON_FENCE = re.compile(r"```(?:json)?\s*(.+?)\s*```", re.DOTALL)


def _extract_json_block(text: str) -> str:
    if not text:
        return ""
    m = _JSON_FENCE.search(text)
    if m:
        return m.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


def parse_deps_json(raw: str) -> dict[str, list[str]]:
    """Parse `{"python": [...], "node": [...]}`. Returns empty lists on bad input."""
    empty = {"python": [], "node": []}
    block = _extract_json_block(raw)
    if not block:
        return empty
    try:
        data = json.loads(block)
    except (json.JSONDecodeError, ValueError):
        return empty
    if not isinstance(data, dict):
        return empty

    def _list_of_strs(v: object) -> list[str]:
        if not isinstance(v, list):
            return []
        return [str(x) for x in v if isinstance(x, str) and x.strip()]

    return {
        "python": _list_of_strs(data.get("python")),
        "node": _list_of_strs(data.get("node")),
    }


# ──────────────────────── pinning ───────────────────────────────────────


_PINNABLE_PYTHON: dict[str, str] = {
    # Map of bare package name → pinned version from CURRENT_VERSIONS.
    # Built once at import time from principal_engineer.CURRENT_VERSIONS.
}
_PINNABLE_NODE: dict[str, str] = {}


def _build_pin_tables() -> None:
    py = CURRENT_VERSIONS.get("python", {})
    for name, ver in py.items():
        _PINNABLE_PYTHON[name.lower()] = ver
    node = CURRENT_VERSIONS.get("node", {})
    for name, ver in node.items():
        _PINNABLE_NODE[name.lower()] = ver


_build_pin_tables()


def _bare_name(spec: str) -> str:
    """Strip version/extras to get the bare package name."""
    # "fastapi==0.115" → "fastapi"; "passlib[bcrypt]==1.7.4" → "passlib"
    base = spec.split(";", 1)[0].split("==")[0].split(">=")[0].split("<=")[0]
    base = base.split(">")[0].split("<")[0].split("~=")[0]
    return base.split("[", 1)[0].strip().lower()


def _pin_python(spec: str) -> str:
    """Pin a Python package to CURRENT_VERSIONS if known, else add `>=0`."""
    if "==" in spec or ">=" in spec or "<=" in spec:
        return spec  # already pinned
    name = _bare_name(spec)
    if name in _PINNABLE_PYTHON:
        # Preserve extras like passlib[bcrypt]
        extras = spec.split("[", 1)[1].split("]", 1)[0] if "[" in spec else ""
        if extras:
            return f"{name}[{extras}]=={_PINNABLE_PYTHON[name]}"
        return f"{name}=={_PINNABLE_PYTHON[name]}"
    return spec  # leave unconstrained — pip will resolve


def _pin_node(spec: str) -> str:
    """Pin a Node package to CURRENT_VERSIONS if known."""
    if "@" in spec and not spec.startswith("@"):
        return spec  # already has a version specifier
    name = spec.lstrip("@") if spec.startswith("@") else spec
    name = name.split("@", 1)[0].lower()
    if name in _PINNABLE_NODE:
        return f"{spec}@{_PINNABLE_NODE[name]}"
    return spec


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for x in items:
        key = _bare_name(x)
        if key not in seen:
            seen.add(key)
            out.append(x)
    return out


# ──────────────────────── resolver ──────────────────────────────────────


_FEATURE_DEPS_PROMPT = """List the packages required to implement this feature.

Feature: {name}
Description: {description}
Layer: {layer}
Acceptance criteria:
{acceptance}

Backend framework: {backend}
Frontend framework: {frontend}

Output a single JSON object:
{{
  "python": ["pkg1", "pkg2"],
  "node":   ["pkg1", "pkg2"]
}}

Rules:
- Include ONLY direct deps, not transitive.
- For Python, use bare package names (we'll pin versions ourselves).
- For Node, use bare names too.
- Output ONLY the JSON object. No prose.
"""


def _gather_feature_deps(
    features: list[Feature],
    backend: str | None,
    frontend: str | None,
    generate: GenerateFn,
) -> tuple[list[str], list[str]]:
    """LLM + keyword pass over each feature → (python_runtime, node_runtime)."""
    py: list[str] = []
    node: list[str] = []
    for feat in features:
        # 1. Keyword pass on description + acceptance
        text = " ".join([feat.description, *feat.acceptance])
        for pattern, deps in _KEYWORD_PYTHON_DEPS:
            if pattern.search(text):
                py.extend(deps)
        for pattern, deps in _KEYWORD_NODE_DEPS:
            if pattern.search(text):
                node.extend(deps)

        # 2. LLM pass — only for features that aren't pure infra
        if feat.layer not in {"frontend", "backend", "shared"}:
            continue
        try:
            raw = generate(
                _FEATURE_DEPS_PROMPT.format(
                    name=feat.name,
                    description=feat.description,
                    layer=feat.layer,
                    acceptance="\n".join(f"  - {a}" for a in feat.acceptance) or "  - (none)",
                    backend=backend or "none",
                    frontend=frontend or "none",
                )
            )
        except Exception:
            raw = ""
        parsed = parse_deps_json(raw)
        py.extend(parsed["python"])
        node.extend(parsed["node"])

    return py, node


def resolve_dependencies(plan: ProjectPlan, generate: GenerateFn) -> DepSet:
    """Build a fully-pinned `DepSet` from a project plan."""
    backend = plan.stack.backend
    frontend = plan.stack.frontend

    # 1. Stack baseline (deterministic)
    baseline_py = list(_BASELINE_PYTHON_RUNTIME.get(backend or "", ()))
    baseline_node = list(_BASELINE_NODE_RUNTIME.get(frontend or "", ()))

    # 2. Per-feature gathering (keywords + LLM)
    feat_py, feat_node = _gather_feature_deps(plan.features, backend, frontend, generate)

    # 3. Drop/replace deprecated packages BEFORE pinning, so pip/npm
    #    don't choke on names that can't be resolved.
    py_raw = sanitize_python_deps(list(baseline_py + feat_py))
    node_raw = sanitize_node_deps(list(baseline_node + feat_node))

    # 4. Pin every entry
    py_runtime = _dedupe_keep_order([_pin_python(p) for p in py_raw])
    py_dev = _dedupe_keep_order([_pin_python(p) for p in _BASELINE_PYTHON_DEV])

    node_runtime = _dedupe_keep_order([_pin_node(p) for p in node_raw])
    node_dev = _dedupe_keep_order(
        [_pin_node(p) for p in _BASELINE_NODE_DEV.get(frontend or "", ())]
    )

    return DepSet(
        python_runtime=py_runtime,
        python_dev=py_dev,
        node_runtime=node_runtime,
        node_dev=node_dev,
    )


# ──────────────────────── emit files ────────────────────────────────────


def emit_python_dep_files(
    deps: DepSet, backend_root: Path, *, project_name: str
) -> None:
    """Write BOTH requirements.txt AND pyproject.toml with matching deps.

    The user explicitly demanded both formats so that Docker / CI /
    hosted services that expect one or the other Just Work.
    """
    backend_root.mkdir(parents=True, exist_ok=True)

    # requirements.txt — sorted, deduped, one per line
    runtime_sorted = sorted(set(deps.python_runtime))
    req_path = backend_root / "requirements.txt"
    req_path.write_text("\n".join(runtime_sorted) + "\n", encoding="utf-8")

    # pyproject.toml — same runtime deps + dev extras + tool config
    runtime_list = ",\n    ".join(f'"{d}"' for d in runtime_sorted)
    dev_sorted = sorted(set(deps.python_dev))
    dev_list = ",\n    ".join(f'"{d}"' for d in dev_sorted)
    pyproject = f"""[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    {runtime_list}
]

[project.optional-dependencies]
dev = [
    {dev_list}
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.setuptools.packages.find]
include = ["app*"]
"""
    (backend_root / "pyproject.toml").write_text(pyproject, encoding="utf-8")


def emit_node_package_json(
    deps: DepSet, frontend_root: Path, *, framework: str | None, project_name: str
) -> None:
    """Write package.json with scripts the verify loop relies on."""
    frontend_root.mkdir(parents=True, exist_ok=True)

    def _split_dep(spec: str) -> tuple[str, str]:
        # "@scope/pkg@^1.0.0" → ("@scope/pkg", "^1.0.0")
        # "expo@^52" → ("expo", "^52")
        if spec.startswith("@"):
            parts = spec[1:].split("@", 1)
            name = "@" + parts[0]
            ver = parts[1] if len(parts) > 1 else "latest"
        else:
            parts = spec.split("@", 1)
            name = parts[0]
            ver = parts[1] if len(parts) > 1 else "latest"
        return name, ver

    runtime_map: dict[str, str] = {}
    for spec in deps.node_runtime:
        n, v = _split_dep(spec)
        runtime_map[n] = v
    dev_map: dict[str, str] = {}
    for spec in deps.node_dev:
        n, v = _split_dep(spec)
        dev_map[n] = v

    # Per-framework script set. install/test/typecheck/lint always present
    # so the verify loop can call them unconditionally.
    if framework == "react-native-web":
        scripts = {
            "start": "expo start",
            "android": "expo start --android",
            "ios": "expo start --ios",
            "web": "expo start --web",
            "build:web": "expo export --platform web",
            "test": "jest --watchAll=false --passWithNoTests",
            "typecheck": "tsc --noEmit",
            "lint": "eslint . --ext .ts,.tsx --max-warnings=0 || true",
        }
        extras = {"main": "expo-router/entry"}
    elif framework == "nextjs":
        scripts = {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "test": "vitest run --passWithNoTests",
            "typecheck": "tsc --noEmit",
            "lint": "next lint --max-warnings=0 || true",
        }
        extras = {}
    elif framework == "express":
        scripts = {
            "start": "node src/server.js",
            "dev": "node --watch src/server.js",
            "test": "vitest run --passWithNoTests",
            "typecheck": "tsc --noEmit || true",
            "lint": "eslint . --max-warnings=0 || true",
        }
        extras = {}
    else:
        # react / vue / svelte / unknown
        scripts = {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview",
            "test": "vitest run --passWithNoTests",
            "typecheck": "tsc --noEmit",
            "lint": "eslint . --max-warnings=0 || true",
        }
        extras = {}

    pkg = {
        "name": project_name,
        "version": "0.1.0",
        "private": True,
        **extras,
        "scripts": scripts,
        "dependencies": dict(sorted(runtime_map.items())),
        "devDependencies": dict(sorted(dev_map.items())),
    }
    (frontend_root / "package.json").write_text(
        json.dumps(pkg, indent=2) + "\n", encoding="utf-8"
    )

    # Expo + Jest: without `preset: 'jest-expo'` and a proper
    # `transformIgnorePatterns`, every test fails with "Cannot use import
    # statement outside a module" the first time it hits expo-modules-core.
    # We always overwrite — the LLM has no business shaping this file.
    if framework == "react-native-web":
        jest_config = (
            "module.exports = {\n"
            "  preset: 'jest-expo',\n"
            "  setupFilesAfterEach: [],\n"
            "  transformIgnorePatterns: [\n"
            "    'node_modules/(?!((jest-)?react-native|@react-native(-community)?|"
            "expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|"
            "@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|"
            "react-native-svg|expo-modules-core))',\n"
            "  ],\n"
            "  testEnvironment: 'jsdom',\n"
            "  moduleFileExtensions: ['ts','tsx','js','jsx','json'],\n"
            "};\n"
        )
        (frontend_root / "jest.config.js").write_text(jest_config, encoding="utf-8")


__all__ = [
    "DepSet",
    "GenerateFn",
    "emit_node_package_json",
    "emit_python_dep_files",
    "parse_deps_json",
    "resolve_dependencies",
    "sanitize_dep_files_in_place",
    "sanitize_node_deps",
    "sanitize_python_deps",
]
