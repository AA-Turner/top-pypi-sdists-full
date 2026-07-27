"""Detect project language, framework, and conventions from cwd.

Result is injected into the system prompt at `sage run` boot so weak models
write the right language/framework on the first try instead of guessing.

This is intentionally cheap (one cwd scan, no recursive walk) and read-only.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["ProjectContext", "detect_project", "format_for_prompt"]


@dataclass
class ProjectContext:
    cwd: Path
    languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    package_managers: list[str] = field(default_factory=list)
    test_runner: str = ""
    style_tools: list[str] = field(default_factory=list)
    source_dirs: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return not (self.languages or self.frameworks or self.package_managers)


# Marker file → language / package-manager hints.
_LANG_MARKERS: dict[str, tuple[str, str]] = {
    "package.json":         ("JavaScript/TypeScript", "npm/yarn/pnpm"),
    "tsconfig.json":        ("TypeScript", ""),
    "deno.json":            ("TypeScript (Deno)", "deno"),
    "bun.lockb":            ("TypeScript (Bun)", "bun"),
    "pyproject.toml":       ("Python", "uv/poetry/pip"),
    "requirements.txt":     ("Python", "pip"),
    "Pipfile":              ("Python", "pipenv"),
    "setup.py":             ("Python", "pip"),
    "Cargo.toml":           ("Rust", "cargo"),
    "go.mod":               ("Go", "go modules"),
    "pom.xml":              ("Java", "maven"),
    "build.gradle":         ("Java/Kotlin", "gradle"),
    "build.gradle.kts":     ("Kotlin", "gradle"),
    "Gemfile":              ("Ruby", "bundler"),
    "composer.json":        ("PHP", "composer"),
    "mix.exs":              ("Elixir", "mix"),
    "Package.swift":        ("Swift", "spm"),
    "CMakeLists.txt":       ("C/C++", "cmake"),
    "Makefile":             ("", "make"),
    "shard.yml":            ("Crystal", "shards"),
    "rebar.config":         ("Erlang", "rebar3"),
    "stack.yaml":           ("Haskell", "stack"),
    "cabal.project":        ("Haskell", "cabal"),
    "Dockerfile":           ("", ""),
    "Project.toml":         ("Julia", "Pkg"),
    "DESCRIPTION":          ("R", "renv"),
    "renv.lock":            ("R", "renv"),
    "pubspec.yaml":         ("Dart/Flutter", "pub"),
    "Cartfile":             ("Swift", "carthage"),
    "Podfile":              ("Swift/Obj-C", "cocoapods"),
    "build.zig":            ("Zig", "zig"),
    "moon.yml":             ("MoonScript", "moonscript"),
    "elm.json":             ("Elm", "elm"),
    "ocamlformat":          ("OCaml", "opam"),
    "dune-project":         ("OCaml", "dune"),
    "lakefile.lean":        ("Lean", "lake"),
    "Nimble":               ("Nim", "nimble"),
}


def _read_json_safe(p: Path) -> dict | None:
    try:
        return json.loads(p.read_text("utf-8"))
    except Exception:
        return None


def _detect_js_framework(pkg: dict) -> tuple[list[str], str, list[str]]:
    """Return (frameworks, test_runner, style_tools) from package.json."""
    deps: dict[str, str] = {}
    for k in ("dependencies", "devDependencies", "peerDependencies"):
        deps.update(pkg.get(k) or {})
    deps_lower = {k.lower(): v for k, v in deps.items()}

    fw: list[str] = []
    fw_signatures = [
        ("next", "Next.js"),
        ("react", "React"),
        ("vue", "Vue"),
        ("svelte", "Svelte"),
        ("@sveltejs/kit", "SvelteKit"),
        ("@angular/core", "Angular"),
        ("solid-js", "Solid"),
        ("astro", "Astro"),
        ("vite", "Vite"),
        ("webpack", "Webpack"),
        ("express", "Express"),
        ("fastify", "Fastify"),
        ("nestjs/core", "NestJS"),
        ("hono", "Hono"),
        ("@remix-run/react", "Remix"),
    ]
    for sig, label in fw_signatures:
        if any(sig in k for k in deps_lower):
            fw.append(label)

    test_runner = ""
    test_signatures = [
        ("vitest", "Vitest"),
        ("jest", "Jest"),
        ("@playwright/test", "Playwright"),
        ("cypress", "Cypress"),
        ("mocha", "Mocha"),
        ("ava", "AVA"),
    ]
    for sig, label in test_signatures:
        if any(sig in k for k in deps_lower):
            test_runner = label
            break
    if not test_runner:
        scripts = pkg.get("scripts") or {}
        test_cmd = (scripts.get("test") or "").lower()
        if "vitest" in test_cmd:
            test_runner = "Vitest"
        elif "jest" in test_cmd:
            test_runner = "Jest"
        elif "playwright" in test_cmd:
            test_runner = "Playwright"

    style: list[str] = []
    if any("tailwind" in k for k in deps_lower):
        style.append("Tailwind")
    if any("styled-components" in k for k in deps_lower):
        style.append("styled-components")
    if any("@emotion/react" in k for k in deps_lower):
        style.append("Emotion")

    return fw, test_runner, style


def _detect_py_framework(cwd: Path, pyproject: Path) -> tuple[list[str], str]:
    fw: list[str] = []
    test_runner = ""
    try:
        text = pyproject.read_text("utf-8").lower()
    except Exception:
        text = ""
    sigs = [
        ("fastapi", "FastAPI"),
        ("django", "Django"),
        ("flask", "Flask"),
        ("starlette", "Starlette"),
        ("typer", "Typer"),
        ("click", "Click"),
        ("pydantic", "Pydantic"),
        ("sqlalchemy", "SQLAlchemy"),
    ]
    for sig, label in sigs:
        if sig in text:
            fw.append(label)

    if "pytest" in text or (cwd / "pytest.ini").exists():
        test_runner = "pytest"
    elif "unittest" in text:
        test_runner = "unittest"
    return fw, test_runner


def _list_source_dirs(cwd: Path) -> list[str]:
    common = ("src", "app", "lib", "components", "hooks", "pages",
              "services", "api", "core", "internal", "pkg")
    found: list[str] = []
    for name in common:
        if (cwd / name).is_dir():
            found.append(name)
    return found[:6]


def detect_project(cwd: Path) -> ProjectContext:
    """One-pass scan of the cwd. Read-only, fast, never recurses."""
    cwd = cwd.resolve()
    ctx = ProjectContext(cwd=cwd)

    seen_lang: set[str] = set()
    seen_pm: set[str] = set()

    for fname, (lang, pm) in _LANG_MARKERS.items():
        if not (cwd / fname).exists():
            continue
        if lang and lang not in seen_lang:
            ctx.languages.append(lang)
            seen_lang.add(lang)
        if pm and pm not in seen_pm:
            ctx.package_managers.append(pm)
            seen_pm.add(pm)

    pkg_path = cwd / "package.json"
    if pkg_path.exists():
        pkg = _read_json_safe(pkg_path) or {}
        fw, test_runner, style = _detect_js_framework(pkg)
        ctx.frameworks.extend(fw)
        if test_runner and not ctx.test_runner:
            ctx.test_runner = test_runner
        ctx.style_tools.extend(style)
        eng = (pkg.get("engines") or {}).get("node")
        if eng:
            ctx.notes.append(f"Node engine: {eng}")

    pyproject = cwd / "pyproject.toml"
    if pyproject.exists():
        fw, test_runner = _detect_py_framework(cwd, pyproject)
        ctx.frameworks.extend(fw)
        if test_runner and not ctx.test_runner:
            ctx.test_runner = test_runner

    if (cwd / "tailwind.config.js").exists() or (cwd / "tailwind.config.ts").exists():
        if "Tailwind" not in ctx.style_tools:
            ctx.style_tools.append("Tailwind")
    if (cwd / ".prettierrc").exists() or (cwd / "prettier.config.js").exists():
        ctx.style_tools.append("Prettier")
    if (cwd / "ruff.toml").exists() or _file_contains(cwd / "pyproject.toml", "[tool.ruff"):
        ctx.style_tools.append("ruff")

    ctx.source_dirs = _list_source_dirs(cwd)

    if (cwd / ".git").is_dir():
        ctx.notes.append("git-tracked")
    return ctx


def _file_contains(p: Path, needle: str) -> bool:
    try:
        return needle in p.read_text("utf-8")
    except Exception:
        return False


def format_for_prompt(ctx: ProjectContext) -> str:
    """Render the detected context as a system-prompt section. Empty if nothing."""
    if ctx.empty:
        return ""
    parts: list[str] = ["", "## DETECTED PROJECT CONTEXT"]
    if ctx.languages:
        parts.append(f"  Language: {', '.join(ctx.languages)}")
    if ctx.frameworks:
        parts.append(f"  Framework: {', '.join(ctx.frameworks)}")
    if ctx.package_managers:
        parts.append(f"  Package manager: {', '.join(ctx.package_managers)}")
    if ctx.test_runner:
        parts.append(f"  Test runner: {ctx.test_runner}")
    if ctx.style_tools:
        parts.append(f"  Style tools: {', '.join(ctx.style_tools)}")
    if ctx.source_dirs:
        parts.append(f"  Source dirs: {', '.join(ctx.source_dirs)}")
    if ctx.notes:
        parts.append(f"  Notes: {'; '.join(ctx.notes)}")
    parts.append(
        "  → Match this project's language, framework, and conventions. "
        "Do NOT introduce a different stack."
    )
    return "\n".join(parts) + "\n"
