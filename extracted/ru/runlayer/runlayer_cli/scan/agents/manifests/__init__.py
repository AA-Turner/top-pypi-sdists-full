"""Dependency-manifest parsing for the static agent-detection engine.

The public surface is small and stable -- :class:`ManifestInfo`,
:func:`parse_manifest`, :func:`manifest_kind`, :func:`manifest_ecosystem`,
:func:`normalize_dep`, :func:`agent_manifest_search_filenames`, and
:data:`MANIFEST_KINDS`. The per-ecosystem parsers live in sibling modules
(``python``, ``npm``, ``cargo``, ``go``, ``jvm``, ``dotnet``) and register
themselves into the :func:`parse_manifest` dispatch via their ``PARSERS`` maps,
so adding an ecosystem is a new small module here, not more mass in one file.

Parsing uses only the Python standard library plus ``structlog`` for debug
logging, so the package is safe for the frozen ``aiwatch`` bundle.

Ecosystems and the manifests that feed them:

* python -- ``pyproject.toml``, ``requirements*.txt``, ``setup.py``,
  ``setup.cfg``, and the ``uv.lock`` / ``poetry.lock`` / ``Pipfile.lock`` locks
* npm    -- ``package.json`` and the ``package-lock.json`` / ``pnpm-lock.yaml``
  / ``yarn.lock`` locks
* cargo  -- ``Cargo.toml``
* go     -- ``go.mod``
* maven  -- ``pom.xml`` and ``build.gradle`` / ``build.gradle.kts``
* nuget  -- ``*.csproj``
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import structlog

from runlayer_cli import regex_safe
from runlayer_cli.scan.agents.languages import ECOSYSTEM_LANGUAGE
from runlayer_cli.scan.agents.manifests import (
    cargo,
    dotnet,
    go,
    jvm,
    npm,
    python,
)

logger = structlog.get_logger(__name__)

# Exact manifest filename -> ecosystem. ``*.csproj`` is matched separately by
# suffix in :func:`manifest_kind`.
MANIFEST_KINDS: dict[str, str] = {
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "setup.py": "python",
    "setup.cfg": "python",
    "uv.lock": "python",
    "poetry.lock": "python",
    "Pipfile.lock": "python",
    "package.json": "npm",
    "package-lock.json": "npm",
    "pnpm-lock.yaml": "npm",
    "yarn.lock": "npm",
    "Cargo.toml": "cargo",
    "go.mod": "go",
    "pom.xml": "maven",
    "build.gradle": "maven",
    "build.gradle.kts": "maven",
}

# Canonical manifest token -> parser, assembled from the per-ecosystem modules.
# Each module owns its tokens; merging here keeps the dispatch in one place
# without a single giant parser file.
_PARSERS: dict[str, Callable[[Path], list[str]]] = {
    **python.PARSERS,
    **npm.PARSERS,
    **cargo.PARSERS,
    **go.PARSERS,
    **jvm.PARSERS,
    **dotnet.PARSERS,
}


@dataclass
class ManifestInfo:
    """Normalized view of a single dependency manifest."""

    path: Path
    kind: str  # canonical manifest token, e.g. "pyproject.toml" or ".csproj"
    ecosystem: str  # python | npm | cargo | go | maven | nuget
    deps: list[str] = field(default_factory=list)  # normalized dependency ids

    @property
    def language(self) -> str:
        return ECOSYSTEM_LANGUAGE.get(self.ecosystem, "Unknown")


def manifest_kind(filename: str) -> str | None:
    """Return the canonical manifest token for ``filename`` or ``None``.

    ``requirements*.txt`` variants (``requirements-dev.txt`` etc.) all canonicalize
    to ``requirements.txt`` so they share the Python parser.
    """
    if filename in MANIFEST_KINDS:
        return filename
    if filename.endswith(".csproj"):
        return ".csproj"
    if filename.startswith("requirements") and filename.endswith(".txt"):
        return "requirements.txt"
    return None


def manifest_ecosystem(kind: str) -> str:
    if kind == ".csproj":
        return "nuget"
    return MANIFEST_KINDS[kind]


def agent_manifest_search_filenames() -> list[str]:
    """Basenames/globs the project crawl searches to locate agent roots.

    Sourced from :data:`MANIFEST_KINDS` (single source of truth with the
    parsers) plus the ``*.csproj`` glob, so root discovery never drifts from
    what the detector can actually parse. ``find -name`` matches the glob on
    Unix; the Windows crawl routes globs through ``-like``.
    """
    return [*MANIFEST_KINDS.keys(), "*.csproj"]


def normalize_dep(name: str, ecosystem: str) -> str:
    """Canonicalize a dependency identifier for cross-comparison.

    The same function is applied to manifest-declared dependencies and to the
    knowledge-base signatures so equality checks are apples-to-apples.
    """
    name = name.strip()
    if ecosystem == "python":
        # PEP 503 normalization (case-insensitive, runs of -_. collapse to -).
        return regex_safe.sub(r"[-_.]+", "-", name).lower()
    if ecosystem == "go":
        # Go module paths are case-sensitive; do not lowercase.
        return name
    # npm / cargo / maven / nuget compare case-insensitively.
    return name.lower()


def parse_manifest(path: Path) -> ManifestInfo | None:
    """Parse a manifest file into a :class:`ManifestInfo`.

    Returns ``None`` if ``path`` is not a recognized manifest. Parsing errors
    yield a :class:`ManifestInfo` with an empty dependency list (the file is
    still a real manifest, we just could not read its dependencies).
    """
    kind = manifest_kind(path.name)
    if kind is None:
        return None
    ecosystem = manifest_ecosystem(kind)
    try:
        raw_deps = _PARSERS[kind](path)
    except Exception as exc:
        # Keep going with empty deps -- the file is still a real manifest, we
        # just couldn't read its dependencies. Log so signature tuning against
        # real-world broken manifests isn't guesswork.
        logger.debug(
            "agent_manifest_parse_failed",
            path=str(path),
            kind=kind,
            error_type=type(exc).__name__,
        )
        raw_deps = []
    deps = sorted({normalize_dep(d, ecosystem) for d in raw_deps if d})
    return ManifestInfo(path=path, kind=kind, ecosystem=ecosystem, deps=deps)


__all__ = [
    "MANIFEST_KINDS",
    "ManifestInfo",
    "agent_manifest_search_filenames",
    "manifest_ecosystem",
    "manifest_kind",
    "normalize_dep",
    "parse_manifest",
]
