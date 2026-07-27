"""Language and framework detection for SAGE.

This module provides truly language-agnostic detection for:
- Programming languages (Python, JS/TS, Java, Kotlin, C#, PHP, Ruby, Elixir, etc.)
- Package managers (pip, npm, yarn, pnpm, bun, cargo, go, maven, gradle, etc.)
- Test frameworks (pytest, jest, vitest, junit, rspec, phpunit, etc.)
- Build tools and compilers
- Framework detection (React, Vue, Angular, Django, FastAPI, Rails, Spring, etc.)

This addresses P1 items 16-45 from the backlog:
- Items 16-31: First-class language/package manager detection
- Items 32-45: Framework and test framework detection

Key design principles:
- Manifest-driven detection (read actual config files, don't guess)
- Multi-language support in the same project
- Monorepo awareness
- Explicit over implicit
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from collections.abc import Callable

# tomllib is stdlib in Python 3.11+; tomli is the backport for 3.10
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        try:
            import tomli as tomllib  # type: ignore[no-redef]
        except ModuleNotFoundError:
            tomllib = None  # type: ignore[assignment]
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

__all__ = [
    # Enums
    "Language",
    "PackageManager",
    "TestFramework",
    "BuildTool",
    "Framework",
    # Data classes
    "LanguageInfo",
    "ProjectManifest",
    "DetectionResult",
    # Main functions
    "detect_languages",
    "detect_project_manifest",
    "detect_test_framework",
    "detect_build_command",
    "detect_lint_command",
    "detect_format_command",
    "detect_type_check_command",
    "detect_frameworks",
    "get_syntax_check_command",
    "get_language_for_extension",
    # Constants
    "LANGUAGE_EXTENSIONS",
    "MANIFEST_FILES",
]


class Language(str, Enum):
    """Supported programming languages."""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    KOTLIN = "kotlin"
    SCALA = "scala"
    CSHARP = "csharp"
    FSHARP = "fsharp"
    PHP = "php"
    RUBY = "ruby"
    ELIXIR = "elixir"
    RUST = "rust"
    GO = "go"
    C = "c"
    CPP = "cpp"
    SWIFT = "swift"
    DART = "dart"
    LUA = "lua"
    R = "r"
    SHELL = "shell"
    SQL = "sql"
    HTML = "html"
    CSS = "css"
    YAML = "yaml"
    JSON = "json"
    TOML = "toml"
    MARKDOWN = "markdown"
    UNKNOWN = "unknown"


class PackageManager(str, Enum):
    """Package managers for different languages."""

    # Python
    PIP = "pip"
    POETRY = "poetry"
    PDM = "pdm"
    UV = "uv"
    PIPENV = "pipenv"
    CONDA = "conda"
    # JavaScript/TypeScript
    NPM = "npm"
    YARN = "yarn"
    PNPM = "pnpm"
    BUN = "bun"
    DENO = "deno"
    # Java/JVM
    MAVEN = "maven"
    GRADLE = "gradle"
    SBT = "sbt"
    # Other
    CARGO = "cargo"
    GO_MOD = "go"
    COMPOSER = "composer"
    GEM = "gem"
    BUNDLER = "bundler"
    MIX = "mix"
    PUB = "pub"
    NUGET = "nuget"
    SWIFT_PM = "swift"
    VCPKG = "vcpkg"
    CONAN = "conan"
    CMAKE = "cmake"
    MAKE = "make"
    BAZEL = "bazel"
    # Monorepo tools
    NX = "nx"
    TURBOREPO = "turborepo"
    LERNA = "lerna"
    UNKNOWN = "unknown"


class TestFramework(str, Enum):
    """Test frameworks for different languages."""

    # Python
    PYTEST = "pytest"
    UNITTEST = "unittest"
    NOSE = "nose"
    # JavaScript/TypeScript
    JEST = "jest"
    VITEST = "vitest"
    MOCHA = "mocha"
    AVA = "ava"
    PLAYWRIGHT = "playwright"
    CYPRESS = "cypress"
    TESTING_LIBRARY = "testing-library"
    # Java/JVM
    JUNIT = "junit"
    TESTNG = "testng"
    SPOCK = "spock"
    KOTEST = "kotest"
    SCALATEST = "scalatest"
    # Other
    CARGO_TEST = "cargo_test"
    GO_TEST = "go_test"
    RSPEC = "rspec"
    MINITEST = "minitest"
    PHPUNIT = "phpunit"
    PEST = "pest"
    EXUNIT = "exunit"
    SWIFT_TEST = "swift_test"
    XCODE_TEST = "xcode_test"
    DOTNET_TEST = "dotnet_test"
    XUNIT = "xunit"
    NUNIT = "nunit"
    MSTEST = "mstest"
    FLUTTER_TEST = "flutter_test"
    CTEST = "ctest"
    GTEST = "gtest"
    CATCH2 = "catch2"
    BUSTED = "busted"  # Lua
    TESTTHAT = "testthat"  # R
    BATS = "bats"  # Shell
    UNKNOWN = "unknown"


class BuildTool(str, Enum):
    """Build tools and compilers."""

    # Python
    SETUPTOOLS = "setuptools"
    HATCH = "hatch"
    FLIT = "flit"
    MATURIN = "maturin"
    # JavaScript/TypeScript
    TSC = "tsc"
    ESBUILD = "esbuild"
    VITE = "vite"
    WEBPACK = "webpack"
    ROLLUP = "rollup"
    PARCEL = "parcel"
    SWC = "swc"
    # Java/JVM
    JAVAC = "javac"
    KOTLINC = "kotlinc"
    SCALAC = "scalac"
    # Other
    CARGO_BUILD = "cargo_build"
    GO_BUILD = "go_build"
    DOTNET_BUILD = "dotnet_build"
    MSBUILD = "msbuild"
    XCODEBUILD = "xcodebuild"
    SWIFT_BUILD = "swift_build"
    GCC = "gcc"
    CLANG = "clang"
    CMAKE_BUILD = "cmake_build"
    MAKE_BUILD = "make_build"
    NINJA = "ninja"
    FLUTTER_BUILD = "flutter_build"
    MIX_COMPILE = "mix_compile"
    RAKE = "rake"
    UNKNOWN = "unknown"


class Framework(str, Enum):
    """Web and application frameworks."""

    # Python backend
    DJANGO = "django"
    FLASK = "flask"
    FASTAPI = "fastapi"
    STARLETTE = "starlette"
    TORNADO = "tornado"
    SANIC = "sanic"
    AIOHTTP = "aiohttp"
    PYRAMID = "pyramid"
    BOTTLE = "bottle"
    LITESTAR = "litestar"
    # Python ML/Data
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    NUMPY = "numpy"
    PANDAS = "pandas"
    SCIKIT_LEARN = "scikit_learn"
    # JavaScript frontend
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"
    SVELTE = "svelte"
    SOLID = "solid"
    QWIK = "qwik"
    PREACT = "preact"
    HTMX = "htmx"
    ALPINE = "alpine"
    # JavaScript meta-frameworks
    NEXTJS = "nextjs"
    NUXT = "nuxt"
    REMIX = "remix"
    ASTRO = "astro"
    GATSBY = "gatsby"
    SVELTEKIT = "sveltekit"
    # JavaScript backend
    EXPRESS = "express"
    NESTJS = "nestjs"
    FASTIFY = "fastify"
    KOA = "koa"
    HONO = "hono"
    # Ruby
    RAILS = "rails"
    SINATRA = "sinatra"
    HANAMI = "hanami"
    # PHP
    LARAVEL = "laravel"
    SYMFONY = "symfony"
    CODEIGNITER = "codeigniter"
    YII = "yii"
    SLIM = "slim"
    # Java/JVM
    SPRING = "spring"
    SPRING_BOOT = "spring_boot"
    QUARKUS = "quarkus"
    MICRONAUT = "micronaut"
    KTOR = "ktor"
    PLAY = "play"
    SPARK_JAVA = "spark_java"
    # .NET
    ASPNET = "aspnet"
    ASPNET_CORE = "aspnet_core"
    BLAZOR = "blazor"
    MAUI = "maui"
    # Elixir
    PHOENIX = "phoenix"
    ABSINTHE = "absinthe"
    # Rust
    ACTIX = "actix"
    AXUM = "axum"
    ROCKET = "rocket"
    WARP = "warp"
    # Go
    GIN = "gin"
    ECHO = "echo"
    FIBER = "fiber"
    CHI = "chi"
    # Swift
    VAPOR = "vapor"
    PERFECT = "perfect"
    # Dart
    FLUTTER = "flutter"
    # Mobile
    REACT_NATIVE = "react_native"
    IONIC = "ionic"
    CAPACITOR = "capacitor"
    EXPO = "expo"
    # CSS
    TAILWIND = "tailwind"
    BOOTSTRAP = "bootstrap"
    MATERIAL_UI = "material_ui"
    CHAKRA_UI = "chakra_ui"
    UNKNOWN = "unknown"


# File extension to language mapping
LANGUAGE_EXTENSIONS: dict[str, Language] = {
    # Python
    ".py": Language.PYTHON,
    ".pyi": Language.PYTHON,
    ".pyx": Language.PYTHON,
    ".pxd": Language.PYTHON,
    # JavaScript/TypeScript
    ".js": Language.JAVASCRIPT,
    ".mjs": Language.JAVASCRIPT,
    ".cjs": Language.JAVASCRIPT,
    ".jsx": Language.JAVASCRIPT,
    ".ts": Language.TYPESCRIPT,
    ".tsx": Language.TYPESCRIPT,
    ".mts": Language.TYPESCRIPT,
    ".cts": Language.TYPESCRIPT,
    # Java/JVM
    ".java": Language.JAVA,
    ".kt": Language.KOTLIN,
    ".kts": Language.KOTLIN,
    ".scala": Language.SCALA,
    ".sc": Language.SCALA,
    # .NET
    ".cs": Language.CSHARP,
    ".csx": Language.CSHARP,
    ".fs": Language.FSHARP,
    ".fsx": Language.FSHARP,
    # Web
    ".php": Language.PHP,
    ".rb": Language.RUBY,
    ".erb": Language.RUBY,
    ".ex": Language.ELIXIR,
    ".exs": Language.ELIXIR,
    # Systems
    ".rs": Language.RUST,
    ".go": Language.GO,
    ".c": Language.C,
    ".h": Language.C,
    ".cpp": Language.CPP,
    ".cc": Language.CPP,
    ".cxx": Language.CPP,
    ".hpp": Language.CPP,
    ".hxx": Language.CPP,
    ".swift": Language.SWIFT,
    # Other
    ".dart": Language.DART,
    ".lua": Language.LUA,
    ".r": Language.R,
    ".R": Language.R,
    ".sh": Language.SHELL,
    ".bash": Language.SHELL,
    ".zsh": Language.SHELL,
    ".fish": Language.SHELL,
    ".sql": Language.SQL,
    # Markup/Config
    ".html": Language.HTML,
    ".htm": Language.HTML,
    ".css": Language.CSS,
    ".scss": Language.CSS,
    ".sass": Language.CSS,
    ".less": Language.CSS,
    ".yaml": Language.YAML,
    ".yml": Language.YAML,
    ".json": Language.JSON,
    ".jsonc": Language.JSON,
    ".toml": Language.TOML,
    ".md": Language.MARKDOWN,
    ".mdx": Language.MARKDOWN,
}

# Manifest files and their associated package managers
MANIFEST_FILES: dict[str, PackageManager] = {
    # Python
    "pyproject.toml": PackageManager.POETRY,  # Default, will be refined
    "setup.py": PackageManager.PIP,
    "setup.cfg": PackageManager.PIP,
    "requirements.txt": PackageManager.PIP,
    "Pipfile": PackageManager.PIPENV,
    "pdm.lock": PackageManager.PDM,
    "uv.lock": PackageManager.UV,
    "environment.yml": PackageManager.CONDA,
    # JavaScript/TypeScript
    "package.json": PackageManager.NPM,  # Default, will be refined
    "package-lock.json": PackageManager.NPM,
    "yarn.lock": PackageManager.YARN,
    "pnpm-lock.yaml": PackageManager.PNPM,
    "bun.lockb": PackageManager.BUN,
    "bun.lock": PackageManager.BUN,
    "deno.json": PackageManager.DENO,
    "deno.jsonc": PackageManager.DENO,
    # Java/JVM
    "pom.xml": PackageManager.MAVEN,
    "build.gradle": PackageManager.GRADLE,
    "build.gradle.kts": PackageManager.GRADLE,
    "settings.gradle": PackageManager.GRADLE,
    "settings.gradle.kts": PackageManager.GRADLE,
    "gradlew": PackageManager.GRADLE,
    "build.sbt": PackageManager.SBT,
    # Rust
    "Cargo.toml": PackageManager.CARGO,
    "Cargo.lock": PackageManager.CARGO,
    # Go
    "go.mod": PackageManager.GO_MOD,
    "go.sum": PackageManager.GO_MOD,
    # PHP
    "composer.json": PackageManager.COMPOSER,
    "composer.lock": PackageManager.COMPOSER,
    # Ruby
    "Gemfile": PackageManager.BUNDLER,
    "Gemfile.lock": PackageManager.BUNDLER,
    ".gemspec": PackageManager.GEM,
    # Elixir
    "mix.exs": PackageManager.MIX,
    "mix.lock": PackageManager.MIX,
    # Dart/Flutter
    "pubspec.yaml": PackageManager.PUB,
    "pubspec.lock": PackageManager.PUB,
    # .NET
    "*.csproj": PackageManager.NUGET,
    "*.fsproj": PackageManager.NUGET,
    "*.sln": PackageManager.NUGET,
    "Directory.Build.props": PackageManager.NUGET,
    "global.json": PackageManager.NUGET,
    # Swift
    "Package.swift": PackageManager.SWIFT_PM,
    "Package.resolved": PackageManager.SWIFT_PM,
    # C/C++
    "CMakeLists.txt": PackageManager.CMAKE,
    "Makefile": PackageManager.MAKE,
    "makefile": PackageManager.MAKE,
    "GNUmakefile": PackageManager.MAKE,
    "meson.build": PackageManager.MAKE,  # Meson
    "conanfile.txt": PackageManager.CONAN,
    "conanfile.py": PackageManager.CONAN,
    "vcpkg.json": PackageManager.VCPKG,
    # Bazel
    "WORKSPACE": PackageManager.BAZEL,
    "WORKSPACE.bazel": PackageManager.BAZEL,
    "MODULE.bazel": PackageManager.BAZEL,
    "BUILD": PackageManager.BAZEL,
    "BUILD.bazel": PackageManager.BAZEL,
    # Monorepo
    "nx.json": PackageManager.NX,
    "turbo.json": PackageManager.TURBOREPO,
    "lerna.json": PackageManager.LERNA,
}


@dataclass
class LanguageInfo:
    """Information about a detected language in a project."""

    language: Language
    file_count: int = 0
    line_count: int = 0
    extensions: set[str] = field(default_factory=set)
    primary: bool = False  # Is this the primary language?


@dataclass
class ProjectManifest:
    """Detected project manifest and configuration."""

    path: Path
    package_manager: PackageManager
    language: Language
    name: str | None = None
    version: str | None = None
    dependencies: dict[str, str] = field(default_factory=dict)
    dev_dependencies: dict[str, str] = field(default_factory=dict)
    scripts: dict[str, str] = field(default_factory=dict)
    test_framework: TestFramework = TestFramework.UNKNOWN
    build_tool: BuildTool = BuildTool.UNKNOWN
    frameworks: list[Framework] = field(default_factory=list)
    is_monorepo: bool = False
    workspaces: list[str] = field(default_factory=list)


@dataclass
class DetectionResult:
    """Complete detection result for a project."""

    project_root: Path
    languages: dict[Language, LanguageInfo] = field(default_factory=dict)
    primary_language: Language = Language.UNKNOWN
    manifests: list[ProjectManifest] = field(default_factory=list)
    package_managers: set[PackageManager] = field(default_factory=set)
    test_frameworks: set[TestFramework] = field(default_factory=set)
    build_tools: set[BuildTool] = field(default_factory=set)
    frameworks: set[Framework] = field(default_factory=set)
    is_monorepo: bool = False
    workspace_roots: list[Path] = field(default_factory=list)


def get_language_for_extension(ext: str) -> Language:
    """Get the language for a file extension."""
    return LANGUAGE_EXTENSIONS.get(ext.lower(), Language.UNKNOWN)


def _read_json(path: Path) -> dict[str, Any]:
    """Safely read a JSON file."""
    try:
        return json.loads(path.read_text("utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _read_toml(path: Path) -> dict[str, Any]:
    """Safely read a TOML file. Works on Python 3.10+ with or without tomli."""
    if tomllib is None:
        return {}
    try:
        return tomllib.loads(path.read_text("utf-8"))
    except (tomllib.TOMLDecodeError, OSError):
        return {}


def _read_text(path: Path) -> str:
    """Safely read a text file."""
    try:
        return path.read_text("utf-8", errors="replace")
    except OSError:
        return ""


def detect_languages(project_root: Path, max_files: int = 1000) -> dict[Language, LanguageInfo]:
    """Detect languages used in a project by scanning files.

    Args:
        project_root: Path to the project root
        max_files: Maximum number of files to scan

    Returns:
        Dictionary mapping languages to their info
    """
    languages: dict[Language, LanguageInfo] = {}
    files_scanned = 0

    skip_dirs = {
        ".git",
        ".svn",
        ".hg",
        ".venv",
        "venv",
        "env",
        ".env",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        "target",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        "vendor",
        "deps",
        "_build",
        ".next",
        ".nuxt",
        ".output",
        "coverage",
        ".coverage",
        "htmlcov",
    }

    import os

    # Optimization: Use os.walk for efficiency and early directory pruning
    for root, dirs, files in os.walk(project_root):
        # Prune directories in-place
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
        
        root_path = Path(root)
        for f in sorted(files):
            if files_scanned >= max_files:
                break
            
            if f.startswith("."):
                continue
                
            p = root_path / f
            ext = os.path.splitext(f)[1].lower()
            lang = get_language_for_extension(ext)

            if lang == Language.UNKNOWN:
                continue

            if lang not in languages:
                languages[lang] = LanguageInfo(language=lang)

            info = languages[lang]
            info.file_count += 1
            info.extensions.add(ext)

            try:
                content = p.read_text("utf-8", errors="replace")
                info.line_count += len(content.splitlines())
            except OSError:
                pass

            files_scanned += 1
        
        if files_scanned >= max_files:
            break

    # Determine primary language
    if languages:
        primary = max(languages.values(), key=lambda i: (i.file_count, i.line_count))
        primary.primary = True

    return languages


def _detect_python_manifest(path: Path) -> ProjectManifest | None:
    """Detect Python project configuration from pyproject.toml."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.PIP,
        language=Language.PYTHON,
    )

    data = _read_toml(path)
    if not data:
        return None

    # Get project name and version
    project = data.get("project", {})
    manifest.name = project.get("name")
    manifest.version = project.get("version")

    # Get dependencies
    manifest.dependencies = {
        dep: "*" for dep in project.get("dependencies", []) if isinstance(dep, str)
    }

    # Detect package manager from build system
    build_system = data.get("build-system", {})
    requires = build_system.get("requires", [])
    build_backend = build_system.get("build-backend", "")

    if "poetry" in str(requires) or "poetry" in build_backend:
        manifest.package_manager = PackageManager.POETRY
        poetry = data.get("tool", {}).get("poetry", {})
        manifest.dependencies = poetry.get("dependencies", {})
        manifest.dev_dependencies = poetry.get("dev-dependencies", {}) or poetry.get(
            "group", {}
        ).get("dev", {}).get("dependencies", {})
    elif "pdm" in str(requires) or "pdm" in build_backend:
        manifest.package_manager = PackageManager.PDM
    elif "hatchling" in str(requires) or "hatch" in build_backend:
        manifest.build_tool = BuildTool.HATCH
    elif "flit" in str(requires) or "flit" in build_backend:
        manifest.build_tool = BuildTool.FLIT
    elif "maturin" in str(requires):
        manifest.build_tool = BuildTool.MATURIN
    elif "setuptools" in str(requires):
        manifest.build_tool = BuildTool.SETUPTOOLS

    # Check for uv
    if (path.parent / "uv.lock").exists():
        manifest.package_manager = PackageManager.UV

    # Detect test framework
    all_deps = {**manifest.dependencies, **manifest.dev_dependencies}
    dep_str = " ".join(all_deps.keys()).lower()

    if "pytest" in dep_str:
        manifest.test_framework = TestFramework.PYTEST
    elif "unittest" in dep_str:
        manifest.test_framework = TestFramework.UNITTEST
    elif "nose" in dep_str:
        manifest.test_framework = TestFramework.NOSE

    # Detect frameworks
    if "django" in dep_str:
        manifest.frameworks.append(Framework.DJANGO)
    if "flask" in dep_str:
        manifest.frameworks.append(Framework.FLASK)
    if "fastapi" in dep_str:
        manifest.frameworks.append(Framework.FASTAPI)
    if "starlette" in dep_str:
        manifest.frameworks.append(Framework.STARLETTE)
    if "tornado" in dep_str:
        manifest.frameworks.append(Framework.TORNADO)
    if "sanic" in dep_str:
        manifest.frameworks.append(Framework.SANIC)
    if "aiohttp" in dep_str:
        manifest.frameworks.append(Framework.AIOHTTP)
    if "pyramid" in dep_str:
        manifest.frameworks.append(Framework.PYRAMID)
    if "litestar" in dep_str:
        manifest.frameworks.append(Framework.LITESTAR)
    if "pytorch" in dep_str or "torch" in dep_str:
        manifest.frameworks.append(Framework.PYTORCH)
    if "tensorflow" in dep_str:
        manifest.frameworks.append(Framework.TENSORFLOW)

    # Check tool.pytest.ini_options
    pytest_opts = data.get("tool", {}).get("pytest", {}).get("ini_options", {})
    if pytest_opts:
        manifest.test_framework = TestFramework.PYTEST

    return manifest


def _detect_javascript_manifest(path: Path) -> ProjectManifest | None:
    """Detect JavaScript/TypeScript project configuration from package.json."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.NPM,
        language=Language.JAVASCRIPT,
    )

    data = _read_json(path)
    if not data:
        return None

    manifest.name = data.get("name")
    manifest.version = data.get("version")
    manifest.dependencies = data.get("dependencies", {})
    manifest.dev_dependencies = data.get("devDependencies", {})
    manifest.scripts = data.get("scripts", {})

    # Detect package manager from lockfiles
    parent = path.parent
    if (parent / "yarn.lock").exists():
        manifest.package_manager = PackageManager.YARN
    elif (parent / "pnpm-lock.yaml").exists():
        manifest.package_manager = PackageManager.PNPM
    elif (parent / "bun.lockb").exists() or (parent / "bun.lock").exists():
        manifest.package_manager = PackageManager.BUN

    # Check if TypeScript
    all_deps = {**manifest.dependencies, **manifest.dev_dependencies}
    if "typescript" in all_deps:
        manifest.language = Language.TYPESCRIPT

    # Detect workspaces (monorepo)
    workspaces = data.get("workspaces", [])
    if isinstance(workspaces, dict):
        workspaces = workspaces.get("packages", [])
    if workspaces:
        manifest.is_monorepo = True
        manifest.workspaces = workspaces

    # Detect test framework
    dep_str = " ".join(all_deps.keys()).lower()
    scripts_str = " ".join(manifest.scripts.values()).lower()

    if "vitest" in dep_str or "vitest" in scripts_str:
        manifest.test_framework = TestFramework.VITEST
    elif "jest" in dep_str or "jest" in scripts_str:
        manifest.test_framework = TestFramework.JEST
    elif "mocha" in dep_str or "mocha" in scripts_str:
        manifest.test_framework = TestFramework.MOCHA
    elif "ava" in dep_str or "ava" in scripts_str:
        manifest.test_framework = TestFramework.AVA
    elif "playwright" in dep_str:
        manifest.test_framework = TestFramework.PLAYWRIGHT
    elif "cypress" in dep_str:
        manifest.test_framework = TestFramework.CYPRESS

    # Detect build tool
    if "vite" in dep_str:
        manifest.build_tool = BuildTool.VITE
    elif "esbuild" in dep_str:
        manifest.build_tool = BuildTool.ESBUILD
    elif "webpack" in dep_str:
        manifest.build_tool = BuildTool.WEBPACK
    elif "rollup" in dep_str:
        manifest.build_tool = BuildTool.ROLLUP
    elif "parcel" in dep_str:
        manifest.build_tool = BuildTool.PARCEL
    elif "swc" in dep_str:
        manifest.build_tool = BuildTool.SWC
    elif "typescript" in dep_str:
        manifest.build_tool = BuildTool.TSC

    # Detect frameworks
    if "react" in dep_str:
        manifest.frameworks.append(Framework.REACT)
    if "vue" in dep_str:
        manifest.frameworks.append(Framework.VUE)
    if "@angular/core" in dep_str or "angular" in dep_str:
        manifest.frameworks.append(Framework.ANGULAR)
    if "svelte" in dep_str:
        manifest.frameworks.append(Framework.SVELTE)
    if "solid-js" in dep_str:
        manifest.frameworks.append(Framework.SOLID)
    if "@builder.io/qwik" in dep_str:
        manifest.frameworks.append(Framework.QWIK)
    if "preact" in dep_str:
        manifest.frameworks.append(Framework.PREACT)

    # Meta-frameworks
    if "next" in dep_str:
        manifest.frameworks.append(Framework.NEXTJS)
    if "nuxt" in dep_str:
        manifest.frameworks.append(Framework.NUXT)
    if "@remix-run" in dep_str or "remix" in dep_str:
        manifest.frameworks.append(Framework.REMIX)
    if "astro" in dep_str:
        manifest.frameworks.append(Framework.ASTRO)
    if "gatsby" in dep_str:
        manifest.frameworks.append(Framework.GATSBY)
    if "@sveltejs/kit" in dep_str:
        manifest.frameworks.append(Framework.SVELTEKIT)

    # Backend frameworks
    if "express" in dep_str:
        manifest.frameworks.append(Framework.EXPRESS)
    if "@nestjs/core" in dep_str:
        manifest.frameworks.append(Framework.NESTJS)
    if "fastify" in dep_str:
        manifest.frameworks.append(Framework.FASTIFY)
    if "koa" in dep_str:
        manifest.frameworks.append(Framework.KOA)
    if "hono" in dep_str:
        manifest.frameworks.append(Framework.HONO)

    # CSS frameworks
    if "tailwindcss" in dep_str:
        manifest.frameworks.append(Framework.TAILWIND)
    if "bootstrap" in dep_str:
        manifest.frameworks.append(Framework.BOOTSTRAP)
    if "@mui/material" in dep_str or "@material-ui" in dep_str:
        manifest.frameworks.append(Framework.MATERIAL_UI)
    if "@chakra-ui" in dep_str:
        manifest.frameworks.append(Framework.CHAKRA_UI)

    # Mobile
    if "react-native" in dep_str:
        manifest.frameworks.append(Framework.REACT_NATIVE)
    if "@ionic" in dep_str:
        manifest.frameworks.append(Framework.IONIC)
    if "@capacitor" in dep_str:
        manifest.frameworks.append(Framework.CAPACITOR)
    if "expo" in dep_str:
        manifest.frameworks.append(Framework.EXPO)

    return manifest


def _detect_cargo_manifest(path: Path) -> ProjectManifest | None:
    """Detect Rust project configuration from Cargo.toml."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.CARGO,
        language=Language.RUST,
        test_framework=TestFramework.CARGO_TEST,
        build_tool=BuildTool.CARGO_BUILD,
    )

    data = _read_toml(path)
    if not data:
        return None

    package = data.get("package", {})
    manifest.name = package.get("name")
    manifest.version = package.get("version")

    deps = data.get("dependencies", {})
    manifest.dependencies = {
        k: str(v) if isinstance(v, str) else v.get("version", "*") for k, v in deps.items()
    }

    dev_deps = data.get("dev-dependencies", {})
    manifest.dev_dependencies = {
        k: str(v) if isinstance(v, str) else v.get("version", "*") for k, v in dev_deps.items()
    }

    # Check for workspaces
    workspace = data.get("workspace", {})
    if workspace:
        manifest.is_monorepo = True
        manifest.workspaces = workspace.get("members", [])

    # Detect frameworks
    all_deps = " ".join(manifest.dependencies.keys()).lower()
    if "actix" in all_deps:
        manifest.frameworks.append(Framework.ACTIX)
    if "axum" in all_deps:
        manifest.frameworks.append(Framework.AXUM)
    if "rocket" in all_deps:
        manifest.frameworks.append(Framework.ROCKET)
    if "warp" in all_deps:
        manifest.frameworks.append(Framework.WARP)

    return manifest


def _detect_go_manifest(path: Path) -> ProjectManifest | None:
    """Detect Go project configuration from go.mod."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.GO_MOD,
        language=Language.GO,
        test_framework=TestFramework.GO_TEST,
        build_tool=BuildTool.GO_BUILD,
    )

    content = _read_text(path)
    if not content:
        return None

    # Parse module name
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("module "):
            manifest.name = line[7:].strip()
            break

    # Parse dependencies (simplified)
    in_require = False
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("require ("):
            in_require = True
            continue
        if line == ")" and in_require:
            in_require = False
            continue
        if in_require and line:
            parts = line.split()
            if len(parts) >= 2:
                manifest.dependencies[parts[0]] = parts[1]

    # Detect frameworks
    dep_str = " ".join(manifest.dependencies.keys()).lower()
    if "gin" in dep_str or "gin-gonic" in dep_str:
        manifest.frameworks.append(Framework.GIN)
    if "echo" in dep_str or "labstack/echo" in dep_str:
        manifest.frameworks.append(Framework.ECHO)
    if "fiber" in dep_str or "gofiber" in dep_str:
        manifest.frameworks.append(Framework.FIBER)
    if "chi" in dep_str or "go-chi" in dep_str:
        manifest.frameworks.append(Framework.CHI)

    return manifest


def _detect_java_manifest(path: Path) -> ProjectManifest | None:
    """Detect Java project configuration from pom.xml or build.gradle."""
    if path.name == "pom.xml":
        return _detect_maven_manifest(path)
    else:
        return _detect_gradle_manifest(path)


def _detect_maven_manifest(path: Path) -> ProjectManifest | None:
    """Detect Maven project configuration."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.MAVEN,
        language=Language.JAVA,
        test_framework=TestFramework.JUNIT,  # Default for Maven
        build_tool=BuildTool.JAVAC,
    )

    content = _read_text(path)
    if not content:
        return None

    # Simple XML parsing for key elements

    # Get artifact ID
    match = re.search(r"<artifactId>([^<]+)</artifactId>", content)
    if match:
        manifest.name = match.group(1)

    # Get version
    match = re.search(r"<version>([^<]+)</version>", content)
    if match:
        manifest.version = match.group(1)

    # Detect test framework
    content_lower = content.lower()
    if "testng" in content_lower:
        manifest.test_framework = TestFramework.TESTNG
    elif "spock" in content_lower:
        manifest.test_framework = TestFramework.SPOCK
    elif "junit" in content_lower:
        manifest.test_framework = TestFramework.JUNIT

    # Detect frameworks
    if "spring-boot" in content_lower:
        manifest.frameworks.append(Framework.SPRING_BOOT)
    elif "spring" in content_lower:
        manifest.frameworks.append(Framework.SPRING)
    if "quarkus" in content_lower:
        manifest.frameworks.append(Framework.QUARKUS)
    if "micronaut" in content_lower:
        manifest.frameworks.append(Framework.MICRONAUT)

    return manifest


def _detect_gradle_manifest(path: Path) -> ProjectManifest | None:
    """Detect Gradle project configuration."""
    is_kotlin = path.suffix == ".kts"
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.GRADLE,
        language=Language.KOTLIN if is_kotlin else Language.JAVA,
        test_framework=TestFramework.JUNIT,
        build_tool=BuildTool.JAVAC,
    )

    content = _read_text(path)
    if not content:
        return None

    content_lower = content.lower()

    # Detect if Kotlin
    if "kotlin" in content_lower:
        manifest.language = Language.KOTLIN
        manifest.build_tool = BuildTool.KOTLINC
        if "kotest" in content_lower:
            manifest.test_framework = TestFramework.KOTEST

    # Detect test framework
    if "testng" in content_lower:
        manifest.test_framework = TestFramework.TESTNG
    elif "spock" in content_lower:
        manifest.test_framework = TestFramework.SPOCK

    # Detect frameworks
    if "spring-boot" in content_lower:
        manifest.frameworks.append(Framework.SPRING_BOOT)
    elif "spring" in content_lower:
        manifest.frameworks.append(Framework.SPRING)
    if "ktor" in content_lower:
        manifest.frameworks.append(Framework.KTOR)
    if "quarkus" in content_lower:
        manifest.frameworks.append(Framework.QUARKUS)
    if "micronaut" in content_lower:
        manifest.frameworks.append(Framework.MICRONAUT)

    return manifest


def _detect_dotnet_manifest(path: Path) -> ProjectManifest | None:
    """Detect .NET project configuration from .csproj/.fsproj."""
    is_fsharp = path.suffix == ".fsproj"
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.NUGET,
        language=Language.FSHARP if is_fsharp else Language.CSHARP,
        test_framework=TestFramework.DOTNET_TEST,
        build_tool=BuildTool.DOTNET_BUILD,
    )

    content = _read_text(path)
    if not content:
        return None

    content_lower = content.lower()

    # Detect test framework
    if "xunit" in content_lower:
        manifest.test_framework = TestFramework.XUNIT
    elif "nunit" in content_lower:
        manifest.test_framework = TestFramework.NUNIT
    elif "mstest" in content_lower:
        manifest.test_framework = TestFramework.MSTEST

    # Detect frameworks
    if "microsoft.aspnetcore" in content_lower:
        manifest.frameworks.append(Framework.ASPNET_CORE)
    elif "microsoft.aspnet" in content_lower:
        manifest.frameworks.append(Framework.ASPNET)
    if "blazor" in content_lower:
        manifest.frameworks.append(Framework.BLAZOR)
    if "maui" in content_lower:
        manifest.frameworks.append(Framework.MAUI)

    return manifest


def _detect_ruby_manifest(path: Path) -> ProjectManifest | None:
    """Detect Ruby project configuration from Gemfile."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.BUNDLER,
        language=Language.RUBY,
    )

    content = _read_text(path)
    if not content:
        return None

    content_lower = content.lower()

    # Detect test framework
    if "rspec" in content_lower:
        manifest.test_framework = TestFramework.RSPEC
    elif "minitest" in content_lower:
        manifest.test_framework = TestFramework.MINITEST

    # Detect frameworks
    if "rails" in content_lower:
        manifest.frameworks.append(Framework.RAILS)
    if "sinatra" in content_lower:
        manifest.frameworks.append(Framework.SINATRA)
    if "hanami" in content_lower:
        manifest.frameworks.append(Framework.HANAMI)

    return manifest


def _detect_php_manifest(path: Path) -> ProjectManifest | None:
    """Detect PHP project configuration from composer.json."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.COMPOSER,
        language=Language.PHP,
    )

    data = _read_json(path)
    if not data:
        return None

    manifest.name = data.get("name")
    manifest.dependencies = data.get("require", {})
    manifest.dev_dependencies = data.get("require-dev", {})

    all_deps = " ".join({**manifest.dependencies, **manifest.dev_dependencies}.keys()).lower()

    # Detect test framework
    if "phpunit" in all_deps:
        manifest.test_framework = TestFramework.PHPUNIT
    elif "pest" in all_deps:
        manifest.test_framework = TestFramework.PEST

    # Detect frameworks
    if "laravel" in all_deps:
        manifest.frameworks.append(Framework.LARAVEL)
    if "symfony" in all_deps:
        manifest.frameworks.append(Framework.SYMFONY)
    if "codeigniter" in all_deps:
        manifest.frameworks.append(Framework.CODEIGNITER)
    if "yii" in all_deps:
        manifest.frameworks.append(Framework.YII)
    if "slim" in all_deps:
        manifest.frameworks.append(Framework.SLIM)

    return manifest


def _detect_elixir_manifest(path: Path) -> ProjectManifest | None:
    """Detect Elixir project configuration from mix.exs."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.MIX,
        language=Language.ELIXIR,
        test_framework=TestFramework.EXUNIT,
        build_tool=BuildTool.MIX_COMPILE,
    )

    content = _read_text(path)
    if not content:
        return None

    content_lower = content.lower()

    # Detect frameworks
    if "phoenix" in content_lower:
        manifest.frameworks.append(Framework.PHOENIX)
    if "absinthe" in content_lower:
        manifest.frameworks.append(Framework.ABSINTHE)

    return manifest


def _detect_dart_manifest(path: Path) -> ProjectManifest | None:
    """Detect Dart/Flutter project configuration from pubspec.yaml."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.PUB,
        language=Language.DART,
        test_framework=TestFramework.FLUTTER_TEST,
    )

    try:
        import yaml

        data = yaml.safe_load(_read_text(path))
    except Exception:
        return None

    if not data:
        return None

    manifest.name = data.get("name")
    manifest.version = data.get("version")
    manifest.dependencies = data.get("dependencies", {}) or {}
    manifest.dev_dependencies = data.get("dev_dependencies", {}) or {}

    # Check for Flutter
    if "flutter" in manifest.dependencies:
        manifest.frameworks.append(Framework.FLUTTER)
        manifest.build_tool = BuildTool.FLUTTER_BUILD

    return manifest


def _detect_swift_manifest(path: Path) -> ProjectManifest | None:
    """Detect Swift project configuration from Package.swift."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.SWIFT_PM,
        language=Language.SWIFT,
        test_framework=TestFramework.SWIFT_TEST,
        build_tool=BuildTool.SWIFT_BUILD,
    )

    content = _read_text(path)
    if not content:
        return None

    content_lower = content.lower()

    # Detect frameworks
    if "vapor" in content_lower:
        manifest.frameworks.append(Framework.VAPOR)
    if "perfect" in content_lower:
        manifest.frameworks.append(Framework.PERFECT)

    return manifest


def _detect_scala_manifest(path: Path) -> ProjectManifest | None:
    """Detect Scala project configuration from build.sbt."""
    manifest = ProjectManifest(
        path=path,
        package_manager=PackageManager.SBT,
        language=Language.SCALA,
        build_tool=BuildTool.SCALAC,
    )

    content = _read_text(path)
    if not content:
        return None

    content_lower = content.lower()

    # Detect test framework
    if "scalatest" in content_lower:
        manifest.test_framework = TestFramework.SCALATEST
    elif "specs2" in content_lower:
        manifest.test_framework = TestFramework.SCALATEST  # Similar

    # Detect frameworks
    if "play" in content_lower:
        manifest.frameworks.append(Framework.PLAY)

    return manifest


def detect_project_manifest(project_root: Path) -> list[ProjectManifest]:
    """Detect all project manifests in a project root.

    Args:
        project_root: Path to the project root

    Returns:
        List of detected project manifests
    """
    manifests: list[ProjectManifest] = []

    # Check for each manifest type
    detectors: dict[str, Callable[[Path], ProjectManifest | None]] = {
        "pyproject.toml": _detect_python_manifest,
        "package.json": _detect_javascript_manifest,
        "Cargo.toml": _detect_cargo_manifest,
        "go.mod": _detect_go_manifest,
        "pom.xml": _detect_maven_manifest,
        "build.gradle": _detect_gradle_manifest,
        "build.gradle.kts": _detect_gradle_manifest,
        "Gemfile": _detect_ruby_manifest,
        "composer.json": _detect_php_manifest,
        "mix.exs": _detect_elixir_manifest,
        "pubspec.yaml": _detect_dart_manifest,
        "Package.swift": _detect_swift_manifest,
        "build.sbt": _detect_scala_manifest,
    }

    for filename, detector in detectors.items():
        manifest_path = project_root / filename
        if manifest_path.exists():
            manifest = detector(manifest_path)
            if manifest:
                manifests.append(manifest)

    # Check for .NET projects (glob for *.csproj and *.fsproj)
    for csproj in project_root.glob("*.csproj"):
        manifest = _detect_dotnet_manifest(csproj)
        if manifest:
            manifests.append(manifest)

    for fsproj in project_root.glob("*.fsproj"):
        manifest = _detect_dotnet_manifest(fsproj)
        if manifest:
            manifests.append(manifest)

    return manifests


def detect_test_framework(project_root: Path) -> TestFramework:
    """Detect the primary test framework for a project.

    Args:
        project_root: Path to the project root

    Returns:
        The detected test framework, or UNKNOWN
    """
    manifests = detect_project_manifest(project_root)
    for manifest in manifests:
        if manifest.test_framework != TestFramework.UNKNOWN:
            return manifest.test_framework
    return TestFramework.UNKNOWN


def detect_build_command(project_root: Path) -> str | None:
    """Detect the build command for a project.

    Args:
        project_root: Path to the project root

    Returns:
        Build command string, or None if not detectable
    """
    manifests = detect_project_manifest(project_root)

    for manifest in manifests:
        if manifest.package_manager == PackageManager.NPM:
            if "build" in manifest.scripts:
                return "npm run build"
        elif manifest.package_manager == PackageManager.YARN:
            if "build" in manifest.scripts:
                return "yarn build"
        elif manifest.package_manager == PackageManager.PNPM:
            if "build" in manifest.scripts:
                return "pnpm build"
        elif manifest.package_manager == PackageManager.BUN:
            if "build" in manifest.scripts:
                return "bun run build"
        elif manifest.package_manager == PackageManager.CARGO:
            return "cargo build"
        elif manifest.package_manager == PackageManager.GO_MOD:
            return "go build ./..."
        elif manifest.package_manager == PackageManager.MAVEN:
            return "mvn compile"
        elif manifest.package_manager == PackageManager.GRADLE:
            return "./gradlew build" if (project_root / "gradlew").exists() else "gradle build"
        elif manifest.package_manager == PackageManager.NUGET:
            return "dotnet build"
        elif manifest.package_manager == PackageManager.MIX:
            return "mix compile"
        elif manifest.package_manager == PackageManager.SBT:
            return "sbt compile"
        elif manifest.package_manager == PackageManager.SWIFT_PM:
            return "swift build"
        elif manifest.package_manager == PackageManager.PUB:
            if Framework.FLUTTER in manifest.frameworks:
                return "flutter build"
            return "dart compile"

    return None


def detect_lint_command(project_root: Path) -> str | None:
    """Detect the lint command for a project.

    Args:
        project_root: Path to the project root

    Returns:
        Lint command string, or None if not detectable
    """
    manifests = detect_project_manifest(project_root)

    # Check for Python linters
    if (project_root / "pyproject.toml").exists():
        data = _read_toml(project_root / "pyproject.toml")
        tool = data.get("tool", {})
        if "ruff" in tool:
            return "ruff check ."
        if "pylint" in tool:
            return "pylint ."
        if "flake8" in tool:
            return "flake8 ."
        # Default for Python
        return "ruff check . || python -m flake8 ."

    for manifest in manifests:
        if manifest.package_manager in {
            PackageManager.NPM,
            PackageManager.YARN,
            PackageManager.PNPM,
            PackageManager.BUN,
        }:
            if "lint" in manifest.scripts:
                pm = manifest.package_manager.value
                if pm == "npm":
                    return "npm run lint"
                elif pm == "yarn":
                    return "yarn lint"
                elif pm == "pnpm":
                    return "pnpm lint"
                elif pm == "bun":
                    return "bun run lint"
        elif manifest.package_manager == PackageManager.CARGO:
            return "cargo clippy"
        elif manifest.package_manager == PackageManager.GO_MOD:
            return "go vet ./..."
        elif manifest.package_manager == PackageManager.MIX:
            return "mix credo"

    return None


def detect_format_command(project_root: Path) -> str | None:
    """Detect the format command for a project.

    Args:
        project_root: Path to the project root

    Returns:
        Format command string, or None if not detectable
    """
    manifests = detect_project_manifest(project_root)

    # Check for Python formatters
    if (project_root / "pyproject.toml").exists():
        data = _read_toml(project_root / "pyproject.toml")
        tool = data.get("tool", {})
        if "ruff" in tool:
            return "ruff format ."
        if "black" in tool:
            return "black ."
        # Default for Python
        return "ruff format . || black ."

    for manifest in manifests:
        if manifest.package_manager in {
            PackageManager.NPM,
            PackageManager.YARN,
            PackageManager.PNPM,
            PackageManager.BUN,
        }:
            if "format" in manifest.scripts:
                pm = manifest.package_manager.value
                if pm == "npm":
                    return "npm run format"
                elif pm == "yarn":
                    return "yarn format"
                elif pm == "pnpm":
                    return "pnpm format"
                elif pm == "bun":
                    return "bun run format"
        elif manifest.package_manager == PackageManager.CARGO:
            return "cargo fmt"
        elif manifest.package_manager == PackageManager.GO_MOD:
            return "go fmt ./..."
        elif manifest.package_manager == PackageManager.MIX:
            return "mix format"

    return None


def detect_type_check_command(project_root: Path) -> str | None:
    """Detect the type check command for a project.

    Args:
        project_root: Path to the project root

    Returns:
        Type check command string, or None if not detectable
    """
    manifests = detect_project_manifest(project_root)

    # Check for Python type checkers
    if (project_root / "pyproject.toml").exists():
        data = _read_toml(project_root / "pyproject.toml")
        tool = data.get("tool", {})
        if "mypy" in tool:
            return "mypy ."
        if "pyright" in tool:
            return "pyright"

    for manifest in manifests:
        if manifest.language == Language.TYPESCRIPT:
            return "npx tsc --noEmit"
        elif manifest.package_manager == PackageManager.CARGO:
            return "cargo check"
        elif manifest.package_manager == PackageManager.GO_MOD:
            return "go build ./..."

    return None


def detect_frameworks(project_root: Path) -> set[Framework]:
    """Detect all frameworks used in a project.

    Args:
        project_root: Path to the project root

    Returns:
        Set of detected frameworks
    """
    frameworks: set[Framework] = set()
    manifests = detect_project_manifest(project_root)

    for manifest in manifests:
        frameworks.update(manifest.frameworks)

    return frameworks


def get_syntax_check_command(filepath: str, language: Language | None = None) -> str | None:
    """Get the syntax check command for a file.

    Args:
        filepath: Path to the file to check
        language: Optional language override

    Returns:
        Syntax check command, or None if not available
    """
    if language is None:
        ext = Path(filepath).suffix.lower()
        language = get_language_for_extension(ext)

    tmp_dir = tempfile.gettempdir()
    kotlin_out = str(Path(tmp_dir) / "sage_kotlin_out.jar")

    # Map language to syntax check command
    commands: dict[Language, str] = {
        Language.PYTHON: f'python -m py_compile "{filepath}"',
        Language.JAVASCRIPT: f'node --check "{filepath}"',
        Language.TYPESCRIPT: f'npx tsc --noEmit "{filepath}"',
        Language.JSON: f"python -c \"import json; json.load(open('{filepath}'))\"",
        Language.YAML: f"python -c \"import yaml; yaml.safe_load(open('{filepath}'))\"",
        Language.RUBY: f'ruby -c "{filepath}"',
        Language.PHP: f'php -l "{filepath}"',
        Language.RUST: "cargo check",  # Checks whole project
        Language.GO: f'go build "{filepath}"',
        Language.JAVA: f'javac -Xlint:all -d "{tmp_dir}" "{filepath}"',
        Language.KOTLIN: f'kotlinc -Werror "{filepath}" -include-runtime -d "{kotlin_out}"',
        Language.SCALA: f'scalac "{filepath}"',
        Language.SWIFT: f'swiftc -parse "{filepath}"',
        Language.CSHARP: "dotnet build",  # Checks whole project
        Language.SHELL: f'bash -n "{filepath}"',
        Language.LUA: f'luac -p "{filepath}"',
        Language.ELIXIR: f'elixir -e "Code.compile_file(\\"{filepath}\\")"',
        Language.DART: f'dart analyze "{filepath}"',
    }

    return commands.get(language)
