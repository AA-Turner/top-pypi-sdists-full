"""Scan for project-level files (MCP configs and skill artifacts) using find.

Note: macOS Spotlight (mdfind) does NOT index hidden files or files in hidden
directories, so we must use the find command instead.
"""

from __future__ import annotations

import os
import platform
import stat
import subprocess
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

import structlog

from runlayer_cli.scan.concurrency import scan_worker_count
from runlayer_cli.scan.resource_governor import (
    terminate_process,
)
from runlayer_cli.scan.scanner_primitives import SymlinkFollowPolicy, is_link_or_reparse
from runlayer_cli.scan.skip_dirs import find_excluded_directories
from runlayer_cli.scan.symlink_follow import (
    _CASE_INSENSITIVE_FILENAMES,
    _PathShardResult,
    _crawl_followed_symlink_targets,
    _group_shards,
    _has_glob_magic,
    _partition_roots,
    _run_path_link_shards,
    _unix_shard,
    _windows_shard,
)
from runlayer_cli.scan.windows_users import is_windows_system_context

if TYPE_CHECKING:
    from runlayer_cli.scan.clients import MCPClientDefinition
    from runlayer_cli.scan.resource_governor import ResourceGovernor

logger = structlog.get_logger(__name__)

_SHARD_RESULT = TypeVar("_SHARD_RESULT")

# Upper bounds for project-scan tuning (shared with the typer flags in
# commands/scan.py and the MDM ProjectDepth / ProjectTimeout fields). Values
# above these are clamped rather than rejected. Defaults (7 / 60) live on the
# typer options; these are only the ceilings.
MAX_PROJECT_DEPTH = 20
MAX_PROJECT_TIMEOUT = 300
NESTED_PROJECT_SCAN_TIMEOUT = 15
NESTED_PROJECT_SCAN_DEPTH = 8
NESTED_PROJECT_SCAN_MAX_PATHS = 10_000
NESTED_PROJECT_SCAN_MAX_ROOTS = 1_000
MAX_DISCOVERED_NODE_MODULES = 256
MAX_FOLLOWED_SYMLINK_TARGETS = 64

# When a governor is active the crawl streams the child's stdout line by line
# and calls governor.checkpoint() every this-many lines — often enough to
# throttle CPU / surface a memory abort promptly, infrequent enough that the
# two clock reads per checkpoint don't dominate the crawl.
_CHECKPOINT_EVERY_LINES = 256
_CRAWL_NICE_VALUE = 10
_WINDOWS_BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
_WINDOWS_REPARSE_PREFIX = "__RUNLAYER_REPARSE__:"


def _clamp_scan_bound(value: object, *, default: int, maximum: int) -> int:
    """Clamp a scan bound into ``[1, maximum]``.

    Non-int (or bool, since ``isinstance(True, int)`` is True) falls back to
    *default*; values below 1 clamp to 1; values above *maximum* clamp down.
    Backstop for programmatic callers that bypass the typer ``IntRange`` clamp.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        return default
    if value < 1:
        return 1
    if value > maximum:
        return maximum
    return value


@dataclass
class ProjectConfig:
    """A discovered project-level MCP configuration."""

    config_path: Path
    project_path: Path  # Root of the project (parent of config)
    client_name: str
    servers_key: str


@dataclass
class HomeCrawlResult:
    """Physical crawl results and their logical direct-file identities."""

    found_paths: list[Path]
    node_modules_paths: list[Path]
    logical_paths: dict[Path, tuple[Path, ...]]


# Path segments excluded from the find/PowerShell crawl. Derived from the
# canonical scan skip set (runlayer_cli.scan.skip_dirs) so it can't drift from
# the agent-discovery walk on dependency/build/VCS junk; it keeps editor config
# dirs (e.g. .vscode) and generic build/env basenames (bin/env/out/obj/wheels,
# which double as real project dir names) crawlable, and adds find-only caches
# + installed-plugins. Other client plugin roots stay crawlable for skill
# discovery and are filtered only during project attribution below.
EXCLUDED_DIRECTORIES: list[str] = find_excluded_directories()

_SHARD_ROOT_EXCLUDES = frozenset(
    excluded
    for excluded in EXCLUDED_DIRECTORIES
    if "/" not in excluded and "\\" not in excluded
)

# Plugin-install path markers excluded only from project attribution. Exact
# pairs avoid treating unrelated directories named "plugins" as client caches.
_PLUGIN_INSTALL_PATH_MARKERS: frozenset[str] = frozenset({"installed-plugins"})
_PLUGIN_INSTALL_PATH_SEGMENT_PAIRS: frozenset[tuple[str, str]] = frozenset(
    {
        (".claude", "plugins"),
        (".codex", "plugins"),
        (".cursor", "plugins"),
    }
)


def _is_plugin_install_path(path: Path) -> bool:
    """Return whether a path is under a recognized plugin install root."""
    parts = path.parts
    adjacent_pairs = zip(parts, parts[1:], strict=False)
    return bool(_PLUGIN_INSTALL_PATH_MARKERS.intersection(parts)) or any(
        pair in _PLUGIN_INSTALL_PATH_SEGMENT_PAIRS for pair in adjacent_pairs
    )


class _PathBudget:
    """Thread-safe aggregate result cap shared by crawl shards."""

    def __init__(self, limit: int) -> None:
        self._limit = limit
        self._count = 0
        self._lock = threading.Lock()

    def reserve(self) -> bool:
        with self._lock:
            if self._count >= self._limit:
                return False
            self._count += 1
            return True

    def release(self) -> None:
        with self._lock:
            if self._count <= 0:
                raise RuntimeError("cannot release an unreserved path")
            self._count -= 1


def _is_reparse_point(path: Path) -> bool:
    """Return whether a Windows path is a symlink/junction reparse point."""
    try:
        attrs = getattr(path.lstat(), "st_file_attributes", None)
    except OSError:
        return True
    if attrs is None:
        return path.is_symlink()
    return bool(attrs & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _crawlable_home_subdirs(
    home: Path,
    *,
    windows: bool,
    symlink_paths: list[Path] | None = None,
) -> list[Path]:
    """List real depth-one roots, surfacing links without crawling them."""
    try:
        candidates = sorted(
            home.iterdir(),
            key=lambda path: (path.name.casefold(), path.name),
        )
    except OSError as exc:
        logger.warning(
            "crawl_shard_root_enumeration_failed",
            path=str(home),
            error=str(exc),
        )
        return []

    real_home = os.path.realpath(str(home))
    shard_excludes = (
        {name.casefold() for name in _SHARD_ROOT_EXCLUDES}
        if windows
        else _SHARD_ROOT_EXCLUDES
    )
    roots: list[Path] = []
    for candidate in candidates:
        excluded_name = candidate.name.casefold() if windows else candidate.name
        if excluded_name in shard_excludes:
            continue
        try:
            if is_link_or_reparse(candidate):
                if symlink_paths is not None:
                    symlink_paths.append(candidate)
                continue
            if not candidate.is_dir():
                continue
            if windows:
                if _is_reparse_point(candidate):
                    continue
                candidate_real = os.path.realpath(str(candidate))
                if not _is_within_root(real_home, candidate_real):
                    continue
        except OSError:
            continue
        roots.append(candidate)
    return roots


def _dispatch_platform_work(
    *,
    unix_builder: Callable[[], list[Callable[[], _SHARD_RESULT]]],
    windows_builder: Callable[[], list[Callable[[], _SHARD_RESULT]]],
) -> list[Callable[[], _SHARD_RESULT]]:
    """Build path-shard work for the current supported platform."""
    system = platform.system()
    if system in ("Darwin", "Linux"):
        return unix_builder()
    if system == "Windows":
        return windows_builder()
    logger.warning("unsupported_platform_for_file_search", platform=system)
    return []


def find_files_under_home(
    filenames: list[str],
    timeout: int = 60,
    max_depth: int = 7,
    governor: ResourceGovernor | None = None,
) -> list[Path]:
    """Find files by name under the user's home directory."""
    return _find_files_under_home(
        filenames,
        timeout=timeout,
        max_depth=max_depth,
        governor=governor,
        discover_node_modules=False,
    ).found_paths


def find_files_and_node_modules_under_home(
    filenames: list[str],
    timeout: int = 60,
    max_depth: int = 7,
    governor: ResourceGovernor | None = None,
) -> HomeCrawlResult:
    """Find requested files and pruned ``node_modules`` directories together."""
    return _find_files_under_home(
        filenames,
        timeout=timeout,
        max_depth=max_depth,
        governor=governor,
        discover_node_modules=True,
    )


def _find_files_under_home(
    filenames: list[str],
    *,
    timeout: int,
    max_depth: int,
    governor: ResourceGovernor | None,
    discover_node_modules: bool,
) -> HomeCrawlResult:
    """Find files by name under the user's home directory.

    Platform-aware: uses ``find`` on macOS/Linux, PowerShell on Windows.
    Both MCP config scanning and skill scanning share this single crawl.

    Entries containing ``/`` are treated as path-suffix patterns and matched
    with ``find -path "*/<pattern>"`` instead of ``-name``.  This prevents
    generic basenames like ``config.toml`` from flooding the crawl results.

    Args:
        filenames: Exact filenames **or** relative-path patterns to search for
                   (e.g. ``[".mcp.json", ".codex/config.toml", "SKILL.md"]``)
        timeout: Max seconds for the whole crawl across all shards
        max_depth: Directory depth limit
        governor: Optional resource governor. When set, the crawl streams the
                  child's output and checkpoints per batch of lines (CPU
                  throttle + memory-abort kill + path budget). ``None`` keeps the
                  original blocking ``subprocess.run`` behavior unchanged.

    Returns:
        Stable, de-duplicated file paths and, when requested, direct
        ``node_modules`` roots from every shard.
    """
    if not filenames:
        return HomeCrawlResult(
            found_paths=[],
            node_modules_paths=[],
            logical_paths={},
        )

    # Clamp to the supported range before crawling. typer already clamps flag /
    # env values, so this only bites non-typer programmatic callers.
    timeout = _clamp_scan_bound(timeout, default=60, maximum=MAX_PROJECT_TIMEOUT)
    deadline = time.monotonic() + timeout
    max_depth = _clamp_scan_bound(max_depth, default=7, maximum=MAX_PROJECT_DEPTH)

    unique = sorted(set(filenames))
    home = Path.home()
    system = platform.system()
    windows_system = is_windows_system_context()
    max_workers = scan_worker_count(governor)
    path_budget = _PathBudget(governor.max_paths) if governor is not None else None
    seed_symlink_paths: list[Path] = []
    symlink_policy = SymlinkFollowPolicy(
        scan_areas=[(home, max_depth)],
        max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
        windows_system_context=windows_system,
    )

    def build_unix_work() -> list[Callable[[], _PathShardResult]]:
        top_level_shard = partial(
            _unix_shard,
            search=_search_unix,
            filenames=unique,
            deadline=deadline,
            max_depth=1,
            governor=governor,
            path_budget=path_budget,
            discover_node_modules=discover_node_modules,
        )
        work = _group_shards([[home]], top_level_shard)
        if max_depth > 1:
            roots = _crawlable_home_subdirs(
                home,
                windows=False,
                symlink_paths=seed_symlink_paths,
            )
            groups = _partition_roots(roots, max_workers)
            work.extend(
                _group_shards(
                    groups,
                    partial(
                        _unix_shard,
                        search=_search_unix,
                        filenames=unique,
                        deadline=deadline,
                        max_depth=max_depth - 1,
                        governor=governor,
                        path_budget=path_budget,
                        discover_node_modules=discover_node_modules,
                    ),
                )
            )
        return work

    def build_windows_work() -> list[Callable[[], _PathShardResult]]:
        top_level_shard = partial(
            _windows_shard,
            search=_search_windows,
            filenames=unique,
            deadline=deadline,
            max_depth=0,
            containment_root=home,
            governor=governor,
            path_budget=path_budget,
            discover_node_modules=discover_node_modules,
            windows_system_context=windows_system,
            recursive=False,
        )
        work = _group_shards([[home]], top_level_shard)
        # The explicit PowerShell walk counts immediate children as depth zero,
        # matching Get-ChildItem's historical -Depth behavior here. Always
        # shard subdirs — even at max_depth == 1, where depth zero preserves
        # the original second-level coverage.
        windows_roots = _crawlable_home_subdirs(
            home,
            windows=True,
            symlink_paths=seed_symlink_paths,
        )
        groups = _partition_roots(windows_roots, max_workers)
        work.extend(
            _group_shards(
                groups,
                partial(
                    _windows_shard,
                    search=_search_windows,
                    filenames=unique,
                    deadline=deadline,
                    max_depth=max_depth - 1,
                    containment_root=home,
                    governor=governor,
                    path_budget=path_budget,
                    discover_node_modules=discover_node_modules,
                    windows_system_context=windows_system,
                ),
            )
        )
        return work

    work = _dispatch_platform_work(
        unix_builder=build_unix_work,
        windows_builder=build_windows_work,
    )
    initial = _run_path_link_shards(work, max_workers=max_workers)
    found = initial.found_paths
    symlink_paths = sorted(set(seed_symlink_paths).union(initial.symlink_paths))
    followed = _crawl_followed_symlink_targets(
        unique,
        symlink_paths,
        deadline=deadline,
        policy=symlink_policy,
        system=system,
        governor=governor,
        path_budget=path_budget,
        discover_node_modules=discover_node_modules,
        max_workers=max_workers,
        follow_depth=max_depth,
        search_unix=_search_unix,
        search_windows=_search_windows,
        initial_found_paths=initial.found_paths,
    )
    found.extend(followed.found_paths)
    found = sorted(set(found))
    all_node_modules_paths = [
        path for path in found if path.name.casefold() == "node_modules"
    ]
    all_node_modules_paths.extend(followed.node_modules_paths)
    all_node_modules_paths = sorted(set(all_node_modules_paths))
    return HomeCrawlResult(
        found_paths=[path for path in found if path.name.casefold() != "node_modules"],
        node_modules_paths=all_node_modules_paths[:MAX_DISCOVERED_NODE_MODULES],
        logical_paths=followed.logical_paths,
    )


def _safe_project_roots(
    roots: list[Path],
    *,
    inside_home: bool,
) -> list[Path]:
    """Keep bounded roots on one side of home and collapse descendants."""
    home_real = os.path.realpath(str(Path.home()))
    candidates: list[tuple[Path, str]] = []
    seen_real_paths: set[str] = set()
    for root in sorted(set(roots), key=lambda path: (len(path.parts), str(path))):
        if len(candidates) >= NESTED_PROJECT_SCAN_MAX_ROOTS:
            break
        try:
            if not root.is_dir() or _is_reparse_point(root):
                continue
            root_real = os.path.realpath(str(root))
        except OSError:
            continue
        if _is_within_root(home_real, root_real) != inside_home:
            continue
        root_key = os.path.normcase(os.path.normpath(root_real))
        if root_key in seen_real_paths:
            continue
        if any(
            _is_within_root(parent_real, root_real) for _, parent_real in candidates
        ):
            continue
        seen_real_paths.add(root_key)
        # Outside-home inputs are policy-approved physical targets, so crawl
        # their canonical location. In-home roots retain their logical path.
        crawl_root = root if inside_home else Path(root_real)
        candidates.append((crawl_root, root_real))
    return [root for root, _ in candidates]


def find_files_under_project_roots(
    filenames: list[str],
    roots: list[Path],
    *,
    timeout: int = NESTED_PROJECT_SCAN_TIMEOUT,
    max_depth: int = NESTED_PROJECT_SCAN_DEPTH,
    max_paths: int = NESTED_PROJECT_SCAN_MAX_PATHS,
    governor: ResourceGovernor | None = None,
) -> list[Path]:
    """Crawl inside- and outside-home project roots under one shared budget."""
    if not filenames or not roots:
        return []

    windows_system = is_windows_system_context()
    timeout = _clamp_scan_bound(
        timeout,
        default=NESTED_PROJECT_SCAN_TIMEOUT,
        maximum=MAX_PROJECT_TIMEOUT,
    )
    max_depth = _clamp_scan_bound(
        max_depth,
        default=NESTED_PROJECT_SCAN_DEPTH,
        maximum=MAX_PROJECT_DEPTH,
    )
    if not isinstance(max_paths, int) or isinstance(max_paths, bool):
        max_paths = NESTED_PROJECT_SCAN_MAX_PATHS
    max_paths = max(1, min(max_paths, NESTED_PROJECT_SCAN_MAX_PATHS))
    nested_roots = _safe_project_roots(roots, inside_home=True)
    external_roots = (
        _safe_project_roots(roots, inside_home=False) if not windows_system else []
    )
    search_roots = [*nested_roots, *external_roots]
    if not search_roots:
        return []

    unique = sorted(set(filenames))
    deadline = time.monotonic() + timeout
    system = platform.system()
    max_workers = scan_worker_count(governor)
    path_budget = _PathBudget(max_paths)
    symlink_policy = SymlinkFollowPolicy(
        scan_areas=[(root, max_depth) for root in search_roots],
        max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
        windows_system_context=windows_system,
    )
    root_groups = _partition_roots(search_roots, max_workers)
    nested_root_groups = _partition_roots(nested_roots, max_workers)
    external_root_groups = [[root] for root in external_roots]
    unix_shard = partial(
        _unix_shard,
        search=_search_unix,
        filenames=unique,
        deadline=deadline,
        max_depth=max_depth,
        governor=governor,
        path_budget=path_budget,
    )
    nested_windows_shard = partial(
        _windows_shard,
        search=_search_windows,
        filenames=unique,
        deadline=deadline,
        max_depth=max_depth - 1,
        containment_root=Path.home(),
        governor=governor,
        path_budget=path_budget,
        windows_system_context=windows_system,
    )
    external_windows_shard = partial(
        _windows_shard,
        search=_search_windows,
        filenames=unique,
        deadline=deadline,
        max_depth=max_depth - 1,
        containment_root=None,
        governor=governor,
        path_budget=path_budget,
        windows_system_context=windows_system,
    )
    work = _dispatch_platform_work(
        unix_builder=lambda: _group_shards(root_groups, unix_shard),
        windows_builder=lambda: [
            *_group_shards(nested_root_groups, nested_windows_shard),
            *_group_shards(external_root_groups, external_windows_shard),
        ],
    )
    initial = _run_path_link_shards(work, max_workers=max_workers)
    followed = _crawl_followed_symlink_targets(
        unique,
        initial.symlink_paths,
        deadline=deadline,
        policy=symlink_policy,
        system=system,
        governor=governor,
        path_budget=path_budget,
        discover_node_modules=False,
        max_workers=max_workers,
        follow_depth=max_depth,
        search_unix=_search_unix,
        search_windows=_search_windows,
        initial_found_paths=initial.found_paths,
    )
    return sorted(set(initial.found_paths + followed.found_paths))[:max_paths]


def scan_for_project_configs(
    clients: list[MCPClientDefinition],
    timeout: int = 60,
    max_depth: int = 7,
    precomputed_paths: list[Path] | None = None,
    governor: ResourceGovernor | None = None,
) -> list[ProjectConfig]:
    """Scan for project-level MCP configuration files.

    When *precomputed_paths* is supplied the filesystem crawl is skipped and
    results are matched against the already-discovered paths instead.  This
    lets the caller run a single ``find_files_under_home`` for both MCP and
    skill filenames and split the results afterward.

    Args:
        clients: Client definitions with ``project_config`` patterns.
        timeout: Search timeout (ignored when *precomputed_paths* given).
        max_depth: Search depth (ignored when *precomputed_paths* given).
        precomputed_paths: Optional pre-crawled paths to match against.
        governor: Optional resource governor forwarded to the crawl when this
                  function runs its own ``find_files_under_home`` (i.e. when
                  *precomputed_paths* is not supplied).

    Returns:
        List of discovered ``ProjectConfig`` instances.
    """
    search_patterns: dict[str, list[tuple[str, str, str | None]]] = {}
    global_config_paths: set[Path] = set()

    for client in clients:
        for pc in client.iter_project_configs():
            rel_path = pc.relative_path
            filename = Path(rel_path).name
            path_contains = None
            if "/" in rel_path:
                path_contains = rel_path.rsplit("/", 1)[0]

            if filename not in search_patterns:
                search_patterns[filename] = []
            search_patterns[filename].append(
                (
                    client.name,
                    pc.servers_key,
                    path_contains,
                )
            )

        for config_path_def in client.paths:
            resolved = config_path_def.resolve()
            if resolved is not None:
                global_config_paths.add(resolved.resolve())

    if not search_patterns:
        logger.debug("No clients with project configs to scan")
        return []

    if precomputed_paths is not None:
        found_paths = precomputed_paths
    else:
        logger.info("Scanning for project configs", max_depth=max_depth)
        find_patterns: list[str] = []
        for client in clients:
            for pc in client.iter_project_configs():
                rel = pc.relative_path
                pattern = rel if "/" in rel else Path(rel).name
                if pattern not in find_patterns:
                    find_patterns.append(pattern)
        found_paths = find_files_under_home(
            find_patterns, timeout, max_depth, governor=governor
        )

    found_configs: list[ProjectConfig] = []
    for path in found_paths:
        filename = path.name
        if filename not in search_patterns:
            continue

        if _is_plugin_install_path(path):
            continue

        if path.resolve() in global_config_paths:
            continue

        best_match_by_client: dict[str, tuple[str, str | None, int]] = {}
        for client_name, servers_key, path_contains in search_patterns[filename]:
            expected_parent_suffix = Path(path_contains).parts if path_contains else ()
            if (
                expected_parent_suffix
                and path.parent.parts[-len(expected_parent_suffix) :]
                != expected_parent_suffix
            ):
                continue

            specificity = len(expected_parent_suffix)
            current_match = best_match_by_client.get(client_name)
            if current_match is None or specificity > current_match[2]:
                best_match_by_client[client_name] = (
                    servers_key,
                    path_contains,
                    specificity,
                )

        for client_name, (
            servers_key,
            path_contains,
            _,
        ) in best_match_by_client.items():
            project_path = _get_project_root(path, path_contains)

            found_configs.append(
                ProjectConfig(
                    config_path=path,
                    project_path=project_path,
                    client_name=client_name,
                    servers_key=servers_key,
                )
            )
            logger.debug("Found project config", client=client_name)

    logger.info("Project config scan complete", found=len(found_configs))
    return found_configs


def _accept_unix_path(
    line: str,
    *,
    discover_node_modules: bool = False,
) -> Path | None:
    """Map one ``find`` output line to a real file or requested npm root."""
    path = Path(line)
    if path.is_file():
        return path
    if (
        discover_node_modules
        and path.name == "node_modules"
        and path.is_dir()
        and not path.is_symlink()
    ):
        return path
    return None


def _deprioritize_crawl_process(proc: subprocess.Popen) -> None:
    """Best-effort POSIX niceness after thread-safe child creation."""
    if os.name != "posix":
        return
    try:
        os.setpriority(os.PRIO_PROCESS, proc.pid, _CRAWL_NICE_VALUE)
    except (AttributeError, OSError) as exc:
        logger.debug(
            "crawl_child_deprioritization_failed",
            pid=proc.pid,
            error=str(exc),
        )


def _search_unix(
    filenames: list[str],
    timeout: float,
    max_depth: int,
    governor: ResourceGovernor | None = None,
    *,
    roots: list[Path] | None = None,
    path_budget: _PathBudget | None = None,
    discover_node_modules: bool = False,
    symlink_paths: list[Path] | None = None,
) -> list[Path]:
    """
    Use find command to locate MCP config files on macOS/Linux.

    Excluded directories are *pruned* (``-prune``), not filtered out of the
    results. With ``! -path "*/excluded/*"`` find still **descends into** huge
    dependency/cache trees (``node_modules``, ``.venv``, ``Library/Caches`` ...)
    and tests every file inside them only to discard it -- on a real developer
    home that traversal is the entire cost of the crawl (cold-cache: a minute-
    plus, enough to hit the find timeout and return partial results). ``-prune``
    stops find from entering those directories at all, turning a minute-plus
    crawl into a sub-second one with identical results.

    Note: We use find instead of mdfind because Spotlight does NOT index
    hidden files (starting with .) or files in hidden directories.

    With a *governor* the crawl streams find's stdout under CPU/memory control
    (see :func:`_stream_crawl`); with ``None`` it keeps the original blocking
    ``subprocess.run`` behavior.
    """
    found_paths: list[Path] = []
    search_roots = roots if roots is not None else [Path.home()]
    if not search_roots:
        return found_paths

    # Build match conditions.  Plain filenames use -name; entries with "/"
    # use -path to avoid matching generic basenames like "config.toml" everywhere.
    name_conditions: list[str] = []
    for filename in filenames:
        if "/" in filename:
            cond = ["-path", f"*/{filename}"]
        elif filename.casefold() in _CASE_INSENSITIVE_FILENAMES:
            # SKILL.md matches case-insensitively: skills stored as skill.md /
            # Skill.md (case-insensitive filesystems, casing evasion) must
            # still crawl out. PowerShell's -in on Windows is already
            # case-insensitive.
            cond = ["-iname", filename]
        else:
            cond = ["-name", filename]
        if name_conditions:
            name_conditions.extend(["-o", *cond])
        else:
            name_conditions.extend(cond)

    # Build prune conditions: directories find must not descend into. Basenames
    # (node_modules, .venv, ...) match by -name; multi-segment markers
    # (e.g. "Library/Caches") match the directory itself by -path.
    prune_conditions: list[str] = []
    pruned_directories = [
        excluded
        for excluded in EXCLUDED_DIRECTORIES
        if not (discover_node_modules and excluded == "node_modules")
    ]
    for excluded in pruned_directories:
        if "/" in excluded:
            cond = ["-path", f"*/{excluded}"]
        else:
            cond = ["-name", excluded]
        if prune_conditions:
            prune_conditions.extend(["-o", *cond])
        else:
            prune_conditions.extend(cond)

    # When npm-root discovery is enabled, print node_modules before pruning it.
    # The crawl never enters dependency trees.
    cmd = ["find", *(str(root) for root in search_roots), "-maxdepth", str(max_depth)]
    if discover_node_modules:
        cmd.extend(
            [
                "(",
                "-type",
                "d",
                "-name",
                "node_modules",
                "-print",
                "-prune",
                ")",
                "-o",
            ]
        )
    if prune_conditions:
        cmd.extend(
            ["(", "-type", "d", "(", *prune_conditions, ")", "-prune", ")", "-o"]
        )
    cmd.extend(
        [
            "(",
            "-type",
            "l",
            "-print",
            ")",
            "-o",
            "(",
            "-type",
            "f",
            "(",
            *name_conditions,
            ")",
            "-print",
            ")",
        ]
    )

    logger.debug(
        "running_find_command",
        roots=len(search_roots),
        filename_patterns=len(filenames),
    )

    def accept(line: str) -> Path | None:
        path = Path(line)
        if is_link_or_reparse(path):
            if symlink_paths is not None:
                symlink_paths.append(path)
            return None
        return _accept_unix_path(
            line,
            discover_node_modules=discover_node_modules,
        )

    if governor is not None:
        return _stream_crawl(
            cmd,
            timeout,
            accept,
            governor,
            label="find",
            path_budget=path_budget,
        )

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        # find returns exit code 1 if some dirs are unreadable, but still outputs results
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue

            path = accept(line)
            if path is not None:
                found_paths.append(path)

    except subprocess.TimeoutExpired:
        logger.warning(f"find command timed out after {timeout}s")
    except FileNotFoundError:
        logger.warning("find command not found")
    except Exception as e:
        logger.warning(f"find command failed: {e}")

    return found_paths


def _escape_powershell_string(value: str) -> str:
    """
    Escape a string for safe use in PowerShell single-quoted strings.

    In PowerShell single-quoted strings, only single quotes need escaping
    (doubled to ''). Other special characters like $, `, and " are treated
    literally within single quotes.
    """
    return value.replace("'", "''")


def _is_within_root(root_real: str, candidate_real: str) -> bool:
    """Whether *candidate_real* is the same as or under *root_real*.

    Both args must already be canonical (``os.path.realpath``-resolved) so a
    reparse point in the path has been followed to its true target. Case- and
    separator-normalized for Windows (case-insensitive filesystem).
    """
    root_n = os.path.normcase(os.path.normpath(root_real))
    cand_n = os.path.normcase(os.path.normpath(candidate_real))
    if cand_n == root_n:
        return True
    return cand_n.startswith(root_n + os.sep)


def _accept_windows_path(
    line: str,
    real_home: str,
    *,
    discover_node_modules: bool = False,
) -> Path | None:
    """Map one PowerShell output line to a Path with link-safe containment.

    Mirrors the POSIX intent in ``hook_install``/``console_user`` (CWE-59/61): a
    ``--all-users`` scan runs as SYSTEM over user-controlled home trees, so a
    non-admin could plant a junction/symlink to redirect a crawl outside their
    profile (e.g. ``C:\\Users\\bob\\x -> C:\\Windows``). Resolve each hit's real
    path and drop anything that is itself a symlink or whose canonical path
    escapes *real_home*, so SYSTEM never reads a redirected file.
    """
    path = Path(line)
    is_file = path.is_file()
    is_node_modules = (
        discover_node_modules
        and path.name.casefold() == "node_modules"
        and path.is_dir()
    )
    if not is_file and not is_node_modules:
        return None
    try:
        if _is_reparse_point(path):
            return None
        real = os.path.realpath(str(path))
    except OSError:
        return None
    if not _is_within_root(real_home, real):
        return None
    return path


def _search_windows(
    filenames: list[str],
    timeout: float,
    max_depth: int,
    governor: ResourceGovernor | None = None,
    *,
    roots: list[Path] | None = None,
    recursive: bool = True,
    containment_root: Path | None = None,
    path_budget: _PathBudget | None = None,
    discover_node_modules: bool = False,
    symlink_paths: list[Path] | None = None,
    windows_system_context: bool | None = None,
) -> list[Path]:
    """
    Use PowerShell to find MCP config files on Windows.

    With a *governor* the crawl streams PowerShell's stdout under CPU/memory
    control (see :func:`_stream_crawl`); with ``None`` it keeps the original
    blocking ``subprocess.run`` behavior.
    """
    found_paths: list[Path] = []
    home = Path.home()
    search_roots = roots if roots is not None else [home]
    if not search_roots:
        return found_paths
    system_context = (
        is_windows_system_context()
        if windows_system_context is None
        else windows_system_context
    )

    # Escape all user-controlled strings for PowerShell single-quoted context
    safe_roots = [_escape_powershell_string(str(root)) for root in search_roots]
    safe_excludes = [
        _escape_powershell_string(d.replace("/", "\\")) for d in EXCLUDED_DIRECTORIES
    ]

    # Split into exact basenames (-in), glob basenames like "*.csproj" (-like),
    # and path-suffix patterns that contain "/" (-like on the full path).
    plain_exact = [
        _escape_powershell_string(f)
        for f in filenames
        if "/" not in f and not _has_glob_magic(f)
    ]
    plain_glob = [
        _escape_powershell_string(f)
        for f in filenames
        if "/" not in f and _has_glob_magic(f)
    ]
    path_patterns = [
        _escape_powershell_string(f).replace("/", "\\") for f in filenames if "/" in f
    ]

    exclude_list = ", ".join([f"'{d}'" for d in safe_excludes])

    if not isinstance(max_depth, int) or max_depth < 0 or max_depth > MAX_PROJECT_DEPTH:
        logger.warning(
            f"Invalid max_depth '{max_depth}' provided. Using default max_depth=7."
        )
        max_depth = 7

    # Build a file filter: exact names with -in, glob names and path-suffix
    # patterns with -like.
    clauses: list[str] = []
    if plain_exact:
        filename_list = ", ".join([f"'{f}'" for f in plain_exact])
        clauses.append(f"$item.Name -in @({filename_list})")
    for glob in plain_glob:
        clauses.append(f"$item.Name -like '{glob}'")
    for pp in path_patterns:
        clauses.append(f"$path -like '*\\{pp}'")
    where_match = " -or ".join(clauses) if clauses else "$false"

    # Walk explicitly so excluded directories and node_modules can be pruned
    # before descent. Get-ChildItem -Recurse has no prune hook and would still
    # traverse dependency trees that its output filter later discards.
    root_list = ", ".join(f"'{root}'" for root in safe_roots)
    recursive_value = "$true" if recursive else "$false"
    discover_node_modules_value = "$true" if discover_node_modules else "$false"
    emit_reparse_value = "$false" if system_context else "$true"
    cmd = f"""
    $excludeDirs = @({exclude_list})
    $maxDepth = {max_depth}
    $recursive = {recursive_value}
    $discoverNodeModules = {discover_node_modules_value}
    $emitReparse = {emit_reparse_value}
    $reparsePrefix = '{_WINDOWS_REPARSE_PREFIX}'
    $pending = [System.Collections.Generic.Stack[object]]::new()
    Get-ChildItem -Path {root_list} -Force -ErrorAction SilentlyContinue |
    ForEach-Object {{
        $pending.Push([PSCustomObject]@{{ Item = $_; Depth = 0 }})
    }}
    while ($pending.Count -gt 0) {{
        $entry = $pending.Pop()
        $item = $entry.Item
        $path = $item.FullName
        if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {{
            if ($emitReparse) {{
                "$reparsePrefix$path"
            }}
            continue
        }}
        if ($item.PSIsContainer) {{
            if ($item.Name -ieq 'node_modules') {{
                if ($discoverNodeModules) {{
                    $path
                }}
                continue
            }}
            $excluded = $false
            foreach ($excludeDir in $excludeDirs) {{
                if ($path -like "*\\$excludeDir" -or $path -like "*\\$excludeDir\\*") {{
                    $excluded = $true
                    break
                }}
            }}
            if ($excluded -or -not $recursive -or $entry.Depth -ge $maxDepth) {{
                continue
            }}
            Get-ChildItem -LiteralPath $path -Force -ErrorAction SilentlyContinue |
            ForEach-Object {{
                $pending.Push(
                    [PSCustomObject]@{{ Item = $_; Depth = $entry.Depth + 1 }}
                )
            }}
            continue
        }}
        if ({where_match}) {{
            $path
        }}
    }}
    """

    logger.debug(
        "running_powershell_search",
        roots=len(search_roots),
        recursive=recursive,
        filename_patterns=len(filenames),
    )

    ps_cmd = ["powershell", "-NoProfile", "-Command", cmd]
    real_home = os.path.realpath(str(containment_root or home))

    def accept(line: str) -> Path | None:
        if line.startswith(_WINDOWS_REPARSE_PREFIX):
            if not system_context and symlink_paths is not None:
                symlink_paths.append(Path(line.removeprefix(_WINDOWS_REPARSE_PREFIX)))
            return None
        return _accept_windows_path(
            line,
            real_home,
            discover_node_modules=discover_node_modules,
        )

    if governor is not None:
        return _stream_crawl(
            ps_cmd,
            timeout,
            accept,
            governor,
            label="powershell",
            path_budget=path_budget,
        )

    try:
        result = subprocess.run(
            ps_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            path = accept(line)
            if path is not None:
                found_paths.append(path)

    except subprocess.TimeoutExpired:
        logger.warning(f"PowerShell search timed out after {timeout}s")
    except Exception as e:
        logger.warning(f"PowerShell search failed: {e}")

    return found_paths


def _stream_crawl(
    cmd: list[str],
    timeout: float,
    accept: Callable[[str], Path | None],
    governor: ResourceGovernor,
    *,
    label: str,
    path_budget: _PathBudget | None = None,
) -> list[Path]:
    """Run *cmd*, streaming stdout line-by-line under governor control.

    Reads the child's stdout as it arrives so the governor can throttle CPU and
    surface a memory abort every ``_CHECKPOINT_EVERY_LINES`` lines via
    :meth:`ResourceGovernor.checkpoint`, and so a memory abort can kill the child
    directly. ``accept`` maps each raw line to a keep-worthy ``Path`` or ``None``.

    A watchdog thread enforces the wall-clock *timeout* (streaming ``Popen`` reads
    have no built-in timeout). On POSIX the child starts in its own session so the
    governor's ``killpg`` reaps the whole ``find`` pipeline. ``checkpoint()`` may
    raise :class:`ScanResourceLimitExceeded`, which propagates out to abort the
    scan after the child + watchdog are cleaned up.
    """
    found_paths: list[Path] = []
    budget = path_budget or _PathBudget(governor.max_paths)
    # On POSIX, own session/group so killpg reaps find + any subshell in one
    # shot; the flag is a no-op on Windows. Explicit kwargs (not **dict) keep the
    # inferred type Popen[str] so the streamed lines type-check as str.
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            start_new_session=(os.name == "posix"),
            creationflags=(
                getattr(
                    subprocess,
                    "BELOW_NORMAL_PRIORITY_CLASS",
                    _WINDOWS_BELOW_NORMAL_PRIORITY_CLASS,
                )
                if os.name == "nt"
                else 0
            ),
        )
    except FileNotFoundError:
        logger.warning(f"{label} command not found")
        return found_paths
    except Exception as e:
        logger.warning(f"{label} command failed to start: {e}")
        return found_paths

    _deprioritize_crawl_process(proc)
    governor.register_child(proc)
    done = threading.Event()
    timed_out = threading.Event()

    def _watchdog() -> None:
        if not done.wait(timeout):
            timed_out.set()
            terminate_process(proc)

    watchdog = threading.Thread(target=_watchdog, name=f"{label}-watchdog", daemon=True)
    watchdog.start()

    try:
        line_count = 0
        stream = proc.stdout
        if stream is not None:
            for raw in stream:
                line_count += 1
                if line_count % _CHECKPOINT_EVERY_LINES == 0:
                    governor.checkpoint()
                line = raw.strip()
                if not line:
                    continue
                path = accept(line)
                if path is None:
                    continue
                if not budget.reserve():
                    logger.warning(
                        "crawl_path_budget_reached",
                        label=label,
                        max_paths=governor.max_paths,
                    )
                    break
                found_paths.append(path)
        # Final checkpoint so a memory abort during the last batch (or a child
        # the monitor just killed) surfaces here rather than only at the next
        # phase boundary. Only raises on a real abort; timeout never does.
        governor.checkpoint()
    finally:
        done.set()
        governor.unregister_child(proc)
        if proc.poll() is None:
            terminate_process(proc)
        try:
            proc.wait(timeout=2.0)
        except Exception:
            pass
        try:
            if proc.stdout is not None:
                proc.stdout.close()
        except Exception:
            pass
        watchdog.join(timeout=1.0)

    if timed_out.is_set():
        logger.warning(f"{label} search timed out after {timeout}s")

    return found_paths


def _get_project_root(config_path: Path, path_contains: str | None) -> Path:
    """
    Determine the project root directory from a config file path.

    For ".mcp.json" -> parent directory is project root
    For ".vscode/mcp.json" -> grandparent directory is project root
    For ".junie/mcp/mcp.json" -> strip both config directories
    """
    project_root = config_path.parent
    if path_contains:
        for _ in Path(path_contains).parts:
            project_root = project_root.parent
    return project_root
