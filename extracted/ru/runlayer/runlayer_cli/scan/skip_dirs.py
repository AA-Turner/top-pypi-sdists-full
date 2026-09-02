"""Canonical directory-skip sets for the scan engine.

The scan walks the filesystem with two different mechanisms, so there are two
shapes here -- but they share one source of truth so they can't silently drift
(which would make ``find`` and the agent walk disagree on coverage):

* :data:`SKIP_DIR_NAMES` -- directory *basenames* pruned during ``os.walk``.
  Used by the agent-discovery walk (:mod:`runlayer_cli.scan.agents.discover`).
  Dependency caches, build outputs, VCS metadata, and editor/tooling state
  never hold first-party source worth scanning.

* :data:`SKIP_DIR_PATH_SUFFIXES` -- exact multi-segment directory suffixes
  pruned by both crawls. These target known cache/fixture paths without
  dropping unrelated directories with generic names such as ``extensions``.

* :func:`find_excluded_directories` -- path-segment excludes for the
  ``find`` / PowerShell crawl (:mod:`runlayer_cli.scan.project_scanner`).
  Derived from :data:`SKIP_DIR_NAMES` and
  :data:`SKIP_DIR_PATH_SUFFIXES` (so the two never diverge on the
  dependency/build/VCS junk that matters) *minus* two basename carve-outs the
  broader config/skill crawl must still descend into -- the editor dot-dirs
  that hold MCP client configs (:data:`_CONFIG_BEARING_DIRS`, e.g.
  ``.vscode/mcp.json``) and the generic build/env basenames that double as real
  project directory names (:data:`_CRAWL_SAFE_DIRS`, e.g. ``bin`` / ``env`` /
  ``out``) -- *plus* find-only caches and the plugin-install marker.

:data:`CONTENT_SKIP_DIRS` is the deliberately-minimal subset used when
collecting an *artifact's own content* (:mod:`runlayer_cli.scan.file_collector`)
-- there we want most files, only pruning obvious dependency/build/VCS junk.

Standard-library only; safe for the frozen ``aiwatch`` bundle.
"""

from __future__ import annotations

# Directory basenames pruned during a tree walk looking for projects/agents.
SKIP_DIR_NAMES: frozenset[str] = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "venv",
        "env",
        ".tox",
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "node_modules",
        ".pnpm-store",
        "bower_components",
        ".mintlify",
        "dist",
        "build",
        "out",
        ".next",
        ".nuxt",
        "target",
        "bin",
        "obj",
        "wheels",
        "vendor",
        ".gradle",
        ".idea",
        ".vscode",
    }
)

# Exact directory path suffixes shared by the agent walk and find crawl.
# Segment tuples stay separator-independent for os.walk; the find-facing
# representation is normalized to "/" in find_excluded_directories().
SKIP_DIR_PATH_SUFFIXES: frozenset[tuple[str, ...]] = frozenset(
    {
        (".cursor", "extensions"),
        (".vscode", "extensions"),
        ("tests", "fixtures", "agent_detection"),
    }
)

# Minimal skip set for collecting an artifact's own content (skills/plugins):
# only dependency/build/VCS junk, never editor or cache dirs, so artifact
# payloads keep their files. Must stay a subset of SKIP_DIR_NAMES.
CONTENT_SKIP_DIRS: frozenset[str] = frozenset(
    {"node_modules", ".venv", "venv", "vendor", "dist", ".tox", ".git"}
)

# Editor/IDE dot-dirs the tree walk prunes, but the find crawl must still
# descend because client MCP configs live inside them (e.g. .vscode/mcp.json).
_CONFIG_BEARING_DIRS: frozenset[str] = frozenset({".vscode"})

# Generic build/output/env *basenames* the agent-source walk prunes (they hold
# no first-party source) but the find crawl must still descend into. Unlike
# node_modules/.venv, these names double as ordinary project directories -- a
# repo literally named ``env`` or ``bin``, a package dir ``out`` / ``obj`` --
# and ``find -prune`` on a bare basename drops the *entire* subtree, so pruning
# them silently hides project-level MCP configs and skill files nested anywhere
# beneath (e.g. ``~/code/env/.mcp.json``, ``bin/SKILL.md``). The pre-skip_dirs
# EXCLUDED_DIRECTORIES list never pruned these; keeping them crawlable preserves
# that coverage. Only bare, ambiguous names belong here: tool-specific dot-dirs
# (.tox, .mypy_cache, .gradle, .next, ...) and dependency caches
# (bower_components, .pnpm-store) stay pruned since they never hold
# hand-authored configs or skills.
_CRAWL_SAFE_DIRS: frozenset[str] = frozenset({"bin", "env", "out", "obj", "wheels"})

# Excludes only the find crawl needs: multi-segment OS data/cache paths, and
# the plugin-install cache (its bundled configs are reported with
# config_scope="plugin", so the project crawl must not surface them again).
_FIND_ONLY_EXCLUDES: tuple[str, ...] = (
    "Library/Caches",
    "Library/Application Support",
    "AppData",
    ".Trash",
    "tmp",
    "temp",
    ".cache",
    ".npm",
    ".yarn",
    "installed-plugins",
    # Host bridge for OrbStack VM/container filesystems; Docker reports these.
    "OrbStack",
)


def find_excluded_directories() -> list[str]:
    """Path-segment excludes for the ``find`` / PowerShell project crawl.

    Sorted for stable command output and tests.
    """
    basenames = SKIP_DIR_NAMES - _CONFIG_BEARING_DIRS - _CRAWL_SAFE_DIRS
    path_suffixes = {"/".join(parts) for parts in SKIP_DIR_PATH_SUFFIXES}
    return sorted(basenames | path_suffixes | set(_FIND_ONLY_EXCLUDES))
