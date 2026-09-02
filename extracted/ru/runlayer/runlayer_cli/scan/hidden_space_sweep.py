"""Bounded discovery of filesystem spaces omitted by the normal project crawl.

The sweep selects roots by hiding technique (OS data/cache namespaces, hidden
home children, and hidden temporary directories), never by a benchmark-specific
directory name. Artifact-specific scanners remain responsible for deciding
whether anything found below those roots is relevant.

Must stay stdlib-only: this module is in the AI Watch bundle import closure.
"""

from __future__ import annotations

import os
import platform
import posixpath
import stat
import tempfile
import time
from collections import deque
from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowPolicy,
    drain_round_robin,
    has_link_or_reparse_component,
    is_contained_real_directory,
    is_link_or_reparse,
    is_real_directory,
    realpath_key,
)
from runlayer_cli.scan.skip_dirs import SKIP_DIR_NAMES
from runlayer_cli.scan.windows_users import is_windows_system_context

MAX_HIDDEN_ROOTS = 128
MAX_ROOT_DISCOVERY_ENTRIES = 10_000
MAX_DIRECTORIES = 2000
MAX_ENTRIES = 10_000
MAX_DEPTH = 6
MAX_FILES = 10_000
MAX_FOLLOWED_SYMLINK_TARGETS = 64
MAX_NODE_MODULES_PATHS = 256
# G5-only output cap; reaching it does not stop the shared G1/G3 traversal.
MAX_PYTHON_ENV_ROOTS = 16

_WINDOWS_HIDDEN_ATTRIBUTE = 0x2
_SKIP_DIR_NAMES_FOLDED = frozenset(name.casefold() for name in SKIP_DIR_NAMES)
_KNOWN_BENIGN_DOT_DIRS = frozenset(
    {
        *(name.casefold() for name in SKIP_DIR_NAMES if name.startswith(".")),
        ".cargo",
        ".ivy2",
        ".m2",
        ".npm",
        ".rustup",
        ".yarn",
    }
)


@dataclass
class HiddenSpaceScanResult:
    """Paths discovered during one shared hidden-space traversal.

    ``files`` keeps logical reporting paths; ``file_targets`` carries resolved
    open targets only when those paths differ.
    """

    files: list[Path] = field(default_factory=list)
    node_modules_paths: list[Path] = field(default_factory=list)
    node_modules_paths_truncated: bool = False
    python_env_roots: list[Path] = field(default_factory=list)
    python_env_roots_truncated: bool = False
    truncated: bool = False
    file_targets: dict[Path, Path] = field(default_factory=dict)


@dataclass
class _SweepBudget:
    root_entries: int = 0
    directories: int = 0
    entries: int = 0
    deadline: float | None = None
    discovery_truncated: bool = False
    root_selection_truncated: bool = False
    truncated: bool = False


@dataclass(frozen=True)
class _RootCandidate:
    path: Path
    is_directory: bool
    source_name: str
    followed: bool = False


@dataclass(frozen=True)
class _DiscoveryBase:
    anchor: Path


@dataclass(frozen=True)
class _WalkNode:
    path: Path
    depth: int


@dataclass(frozen=True)
class _WalkEntryResult:
    output: Path | None = None
    child_directory: _WalkNode | None = None


def _deadline_expired(budget: _SweepBudget) -> bool:
    if budget.deadline is not None and time.monotonic() >= budget.deadline:
        budget.truncated = True
    return budget.truncated


def is_hidden_container_path(path: str, *, root_path: str) -> bool:
    """Whether a contained POSIX path uses a dot-prefixed hiding directory."""
    normalized_root = posixpath.normpath(root_path)
    normalized_path = posixpath.normpath(path)
    if (
        not normalized_root.startswith("/")
        or not normalized_path.startswith("/")
        or (
            normalized_path != normalized_root
            and not normalized_path.startswith(normalized_root.rstrip("/") + "/")
        )
    ):
        return False
    relative = posixpath.relpath(normalized_path, normalized_root)
    directory_parts = relative.split("/")[:-1]
    hidden_parts = (
        posixpath.basename(normalized_root),
        *(part for part in directory_parts if part not in {".", ".."}),
    )
    return any(part.startswith(".") for part in hidden_parts) and not any(
        part.casefold() in _KNOWN_BENIGN_DOT_DIRS for part in hidden_parts
    )


def _is_hidden_entry(entry: os.DirEntry[str]) -> bool:
    if entry.name.startswith("."):
        return True
    try:
        attributes = getattr(entry.stat(follow_symlinks=False), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(attributes & _WINDOWS_HIDDEN_ATTRIBUTE)


def _is_known_benign_dot_directory(path: Path) -> bool:
    return path.name.casefold() in _KNOWN_BENIGN_DOT_DIRS


def _is_regular_unlinked_file(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError:
        return False
    attributes = getattr(info, "st_file_attributes", 0)
    return stat.S_ISREG(info.st_mode) and not (
        attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def _record_node_modules(
    path: Path,
    *,
    result: HiddenSpaceScanResult,
) -> None:
    if path in result.node_modules_paths:
        return
    if len(result.node_modules_paths) < MAX_NODE_MODULES_PATHS:
        result.node_modules_paths.append(path)
    else:
        result.node_modules_paths_truncated = True


def _record_python_env(path: Path, *, result: HiddenSpaceScanResult) -> None:
    if path in result.python_env_roots:
        return
    if len(result.python_env_roots) < MAX_PYTHON_ENV_ROOTS:
        result.python_env_roots.append(path)
    else:
        result.python_env_roots_truncated = True


def _python_env_from_site_packages(path: Path) -> Path | None:
    parent = path.parent
    if parent.name.casefold() == "lib":
        return parent.parent
    if (
        parent.name.casefold().startswith("python")
        and parent.parent.name.casefold() == "lib"
    ):
        return parent.parent.parent
    return None


def _probe_pruned_directory(
    directory: Path,
    *,
    result: HiddenSpaceScanResult,
) -> None:
    """Run only direct structural checks before pruning known-benign state."""
    if not is_real_directory(directory):
        return
    if _is_regular_unlinked_file(directory / "pyvenv.cfg"):
        _record_python_env(directory, result=result)
    for relative in (("node_modules",), ("lib", "node_modules")):
        candidate = directory.joinpath(*relative)
        if is_contained_real_directory(directory, candidate):
            _record_node_modules(candidate, result=result)


def _namespace_roots(home: Path, system: str) -> tuple[Path, ...]:
    common = (home / ".cache", home / ".local" / "share", home / ".config")
    if system == "Windows":
        return (
            home / "AppData" / "Local",
            home / "AppData" / "LocalLow",
            home / "AppData" / "Roaming",
        )
    if system == "Darwin":
        return (
            *common,
            home / "Library" / "Caches",
            home / "Library" / "Application Support",
        )
    return common


def _default_temp_roots(system: str) -> tuple[Path, ...]:
    configured = Path(tempfile.gettempdir())
    if system == "Windows":
        return (configured,)
    return tuple(dict.fromkeys((configured, Path("/tmp"), Path("/var/tmp"))))


def _canonical_temp_root(root: Path) -> Path:
    """Resolve trusted temp-root aliases before enforcing descendant safety."""
    try:
        return root.resolve(strict=True)
    except (OSError, RuntimeError):
        return root


def _resolve_namespace_root(
    home: Path,
    namespace: Path,
    *,
    budget: _SweepBudget,
    checkpoint: Callable[[], None] | None,
    symlink_policy: SymlinkFollowPolicy,
) -> Path | None:
    try:
        relative = namespace.relative_to(home)
    except ValueError:
        return None
    current = home
    for part in relative.parts:
        child = current / part
        if is_link_or_reparse(child):
            if budget.root_entries >= MAX_ROOT_DISCOVERY_ENTRIES:
                budget.discovery_truncated = True
                return None
            budget.root_entries += 1
            if checkpoint is not None:
                checkpoint()
            target = symlink_policy.inspect(child)
            if (
                target is None
                or not is_real_directory(target)
                or not symlink_policy.claim(target)
            ):
                return None
            current = target
        elif is_real_directory(child):
            current = child
        else:
            return None
    return current


def _candidate_directories(
    base: Path,
    *,
    hidden_only: bool,
    include_files: bool = False,
    include_skip_names: bool = False,
    require_current_owner: bool = False,
    excluded: frozenset[Path],
    budget: _SweepBudget,
    checkpoint: Callable[[], None] | None,
    symlink_policy: SymlinkFollowPolicy,
) -> Generator[_RootCandidate | None, None, None]:
    if not is_real_directory(base):
        return
    current_uid = (
        os.getuid() if require_current_owner and hasattr(os, "getuid") else None
    )
    try:
        with os.scandir(base) as entries:
            for entry in entries:
                if _deadline_expired(budget):
                    break
                if budget.root_entries >= MAX_ROOT_DISCOVERY_ENTRIES:
                    budget.discovery_truncated = True
                    break
                budget.root_entries += 1
                if checkpoint is not None:
                    checkpoint()
                try:
                    entry_path = Path(entry.path)
                    followed = is_link_or_reparse(entry_path)
                    candidate_path = entry_path
                    if followed:
                        target = symlink_policy.inspect(entry_path)
                        if target is None:
                            yield None
                            continue
                        candidate_path = target
                        info = target.stat()
                    else:
                        info = entry.stat(follow_symlinks=False)
                    is_directory = stat.S_ISDIR(info.st_mode)
                    is_file = stat.S_ISREG(info.st_mode)
                    if require_current_owner and (
                        current_uid is None or info.st_uid != current_uid
                    ):
                        yield None
                        continue
                    if is_directory:
                        if followed and not is_real_directory(candidate_path):
                            yield None
                            continue
                        if (
                            hidden_only
                            and not _is_hidden_entry(entry)
                            and not (
                                include_skip_names
                                and entry.name.casefold() in _SKIP_DIR_NAMES_FOLDED
                            )
                        ):
                            yield None
                            continue
                        if not followed and candidate_path in excluded:
                            yield None
                            continue
                    elif include_files and is_file:
                        if followed and not _is_regular_unlinked_file(candidate_path):
                            yield None
                            continue
                    else:
                        yield None
                        continue
                    yield _RootCandidate(
                        candidate_path,
                        is_directory=is_directory,
                        source_name=entry.name,
                        followed=followed,
                    )
                except OSError:
                    yield None
    except OSError:
        return


def _discover_roots(
    homes: Sequence[Path],
    *,
    home_systems: Sequence[str],
    temp_roots: Sequence[Path],
    include_files: bool,
    budget: _SweepBudget,
    result: HiddenSpaceScanResult,
    checkpoint: Callable[[], None] | None,
    symlink_policy: SymlinkFollowPolicy,
    seen_files: set[str],
) -> list[Path]:
    namespace_pairs: list[tuple[Path, Path]] = []
    for home, namespace_system in zip(homes, home_systems, strict=True):
        for namespace in _namespace_roots(home, namespace_system):
            resolved_namespace = _resolve_namespace_root(
                home,
                namespace,
                budget=budget,
                checkpoint=checkpoint,
                symlink_policy=symlink_policy,
            )
            if resolved_namespace is None:
                continue
            pair = (home, resolved_namespace)
            if pair not in namespace_pairs:
                namespace_pairs.append(pair)
                symlink_policy.add_scan_area(
                    resolved_namespace,
                    MAX_DEPTH,
                )
    excluded_home_children = frozenset(
        namespace
        for home, namespace_system in zip(homes, home_systems, strict=True)
        for namespace in _namespace_roots(home, namespace_system)
    )
    iterators: deque[
        tuple[_DiscoveryBase, Generator[_RootCandidate | None, None, None]]
    ] = deque()
    for home in homes:
        iterators.append(
            (
                _DiscoveryBase(anchor=home),
                _candidate_directories(
                    home,
                    hidden_only=True,
                    include_skip_names=True,
                    excluded=excluded_home_children,
                    budget=budget,
                    checkpoint=checkpoint,
                    symlink_policy=symlink_policy,
                ),
            )
        )
    for _home, namespace in namespace_pairs:
        iterators.append(
            (
                _DiscoveryBase(anchor=namespace),
                _candidate_directories(
                    namespace,
                    hidden_only=False,
                    include_files=include_files,
                    excluded=frozenset(),
                    budget=budget,
                    checkpoint=checkpoint,
                    symlink_policy=symlink_policy,
                ),
            )
        )
    for temp_root in temp_roots:
        iterators.append(
            (
                _DiscoveryBase(anchor=temp_root),
                _candidate_directories(
                    temp_root,
                    hidden_only=False,
                    require_current_owner=True,
                    excluded=frozenset(),
                    budget=budget,
                    checkpoint=checkpoint,
                    symlink_policy=symlink_policy,
                ),
            )
        )

    roots: list[Path] = []
    selected_roots: set[str] = set()
    pruned_roots: set[str] = set()

    def collect(base: _DiscoveryBase, candidate: _RootCandidate | None) -> None:
        if candidate is None:
            return
        path = candidate.path
        if not candidate.is_directory:
            if (
                not include_files
                or (
                    not candidate.followed
                    and not is_contained_real_directory(base.anchor, path.parent)
                )
                or not _is_regular_unlinked_file(path)
            ):
                return
            key = realpath_key(path)
            if key in seen_files:
                return
            if len(result.files) >= MAX_FILES:
                budget.truncated = True
            else:
                if candidate.followed and not symlink_policy.claim(path):
                    return
                seen_files.add(key)
                symlink_policy.mark_visited(path)
                result.files.append(path)
            return
        if not candidate.followed and not is_contained_real_directory(
            base.anchor, path
        ):
            return
        key = realpath_key(path)
        if key in selected_roots:
            return
        source_path = Path(candidate.source_name)
        if _is_known_benign_dot_directory(path) or _is_known_benign_dot_directory(
            source_path
        ):
            if key in pruned_roots:
                return
            pruned_roots.add(key)
            _probe_pruned_directory(path, result=result)
        elif len(roots) < MAX_HIDDEN_ROOTS:
            if candidate.followed and not symlink_policy.claim(path):
                return
            selected_roots.add(key)
            roots.append(path)
            symlink_policy.add_scan_area(path, MAX_DEPTH)
        else:
            if key in pruned_roots:
                return
            pruned_roots.add(key)
            budget.root_selection_truncated = True
            _probe_pruned_directory(path, result=result)

    drain_round_robin(
        iterators,
        visit=collect,
        should_stop=lambda: budget.discovery_truncated or _deadline_expired(budget),
    )
    return roots


def _classify_walk_directory(
    path: Path,
    candidate: Path,
    *,
    name: str,
    depth: int,
    followed: bool,
    result: HiddenSpaceScanResult,
) -> _WalkNode | None:
    """Record terminal directory types or return the next bounded walk node."""
    candidate_name = candidate.name.casefold()
    if name == "node_modules" or candidate_name == "node_modules":
        _record_node_modules(candidate, result=result)
        return None
    if name in {"site-packages", "dist-packages"} or candidate_name in {
        "site-packages",
        "dist-packages",
    }:
        env_root = _python_env_from_site_packages(candidate)
        if env_root is not None and is_real_directory(env_root):
            _record_python_env(env_root, result=result)
        return None
    if _is_known_benign_dot_directory(path) or _is_known_benign_dot_directory(
        candidate
    ):
        _probe_pruned_directory(candidate, result=result)
        return None
    if followed:
        return _WalkNode(candidate, 0)
    if depth < MAX_DEPTH:
        return _WalkNode(candidate, depth + 1)
    return None


def _classify_walk_entry(
    entry: os.DirEntry[str],
    *,
    directory: Path,
    depth: int,
    include_files: bool,
    budget: _SweepBudget,
    seen_files: set[str],
    result: HiddenSpaceScanResult,
    symlink_policy: SymlinkFollowPolicy,
) -> _WalkEntryResult:
    """Classify one directory entry and return its output or next walk node."""
    try:
        path = Path(entry.path)
        name = entry.name.casefold()
        followed = is_link_or_reparse(path)
        candidate = path
        if followed:
            target = symlink_policy.inspect(path)
            if target is None:
                return _WalkEntryResult()
            candidate = target
            candidate_info = target.stat()
            is_directory = stat.S_ISDIR(candidate_info.st_mode)
            is_file = stat.S_ISREG(candidate_info.st_mode)
        else:
            is_directory = entry.is_dir(follow_symlinks=False)
            is_file = entry.is_file(follow_symlinks=False)

        file_is_usable = (
            is_file
            and (include_files or name == "pyvenv.cfg")
            and _is_regular_unlinked_file(candidate)
        )
        if followed:
            target_is_usable = (
                is_directory and is_real_directory(candidate)
            ) or file_is_usable
            if not target_is_usable:
                return _WalkEntryResult()

        if is_directory:
            child_directory = _classify_walk_directory(
                path,
                candidate,
                name=name,
                depth=depth,
                followed=followed,
                result=result,
            )
            if followed and child_directory is not None:
                if not symlink_policy.claim(candidate):
                    child_directory = None
                else:
                    symlink_policy.add_scan_area(candidate, MAX_DEPTH)
            return _WalkEntryResult(child_directory=child_directory)
        if not file_is_usable:
            return _WalkEntryResult()
        if name == "pyvenv.cfg":
            if followed and not symlink_policy.claim(candidate):
                return _WalkEntryResult()
            _record_python_env(candidate.parent, result=result)
        if not include_files:
            return _WalkEntryResult()

        file_key = realpath_key(candidate)
        if file_key in seen_files:
            return _WalkEntryResult()
        if len(result.files) >= MAX_FILES:
            budget.truncated = True
            return _WalkEntryResult()
        if followed and name != "pyvenv.cfg" and not symlink_policy.claim(candidate):
            return _WalkEntryResult()
        seen_files.add(file_key)
        symlink_policy.mark_visited(candidate)
        return _WalkEntryResult(output=candidate)
    except OSError:
        return _WalkEntryResult()


def _walk_root(
    root: Path,
    *,
    include_files: bool,
    budget: _SweepBudget,
    checkpoint: Callable[[], None] | None,
    seen_directories: set[str],
    seen_files: set[str],
    result: HiddenSpaceScanResult,
    symlink_policy: SymlinkFollowPolicy,
) -> Generator[Path | None, None, None]:
    queue = deque([_WalkNode(root, 0)])
    while queue and not _deadline_expired(budget):
        node = queue.popleft()
        directory = node.path
        depth = node.depth
        key = realpath_key(directory)
        if key in seen_directories or not is_real_directory(directory):
            continue
        seen_directories.add(key)
        symlink_policy.mark_visited(directory)
        if directory.name.casefold() == "node_modules":
            _record_node_modules(directory, result=result)
            continue
        if directory.name.casefold() in {"site-packages", "dist-packages"}:
            env_root = _python_env_from_site_packages(directory)
            if env_root is not None and is_real_directory(env_root):
                _record_python_env(env_root, result=result)
            continue
        if _is_known_benign_dot_directory(directory):
            _probe_pruned_directory(directory, result=result)
            continue
        if budget.directories >= MAX_DIRECTORIES:
            budget.truncated = True
            break
        budget.directories += 1
        if checkpoint is not None:
            checkpoint()

        child_directories: list[_WalkNode] = []
        yielded_entry = False
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    if _deadline_expired(budget):
                        break
                    if budget.entries >= MAX_ENTRIES:
                        budget.truncated = True
                        break
                    budget.entries += 1
                    classified = _classify_walk_entry(
                        entry,
                        directory=directory,
                        depth=depth,
                        include_files=include_files,
                        budget=budget,
                        seen_files=seen_files,
                        result=result,
                        symlink_policy=symlink_policy,
                    )
                    if classified.child_directory is not None:
                        child_directories.append(classified.child_directory)
                    yielded_entry = True
                    yield classified.output
        except OSError:
            continue

        if not yielded_entry:
            # Let the shared drain interleave structural-only walks by root.
            yield None
        queue.extend(sorted(child_directories, key=lambda item: str(item.path)))


def scan_hidden_spaces(
    *,
    home: Path | None = None,
    system: str | None = None,
    extra_home_roots: Sequence[Path] = (),
    include_files: bool = False,
    temp_roots: Sequence[Path] | None = None,
    time_budget_s: float | None = None,
    checkpoint: Callable[[], None] | None = None,
) -> HiddenSpaceScanResult:
    """Discover bounded candidate paths in normally omitted filesystem spaces."""
    deadline = (
        time.monotonic() + max(time_budget_s, 0.0)
        if time_budget_s is not None
        else None
    )
    native_home = home or Path.home()
    actual_system = system or platform.system()
    configured_homes = (native_home, *extra_home_roots)
    configured_temp_roots = (
        tuple(
            dict.fromkeys(
                _canonical_temp_root(root)
                for root in _default_temp_roots(actual_system)
            )
        )
        if temp_roots is None
        else tuple(temp_roots)
    )
    budget = _SweepBudget(deadline=deadline)
    result = HiddenSpaceScanResult()
    windows_system_context = is_windows_system_context()
    admissible_homes = [
        (index, root)
        for index, root in enumerate(configured_homes)
        if not (windows_system_context and has_link_or_reparse_component(root))
    ]
    admissible_temp_roots = [
        root
        for root in configured_temp_roots
        if not (windows_system_context and has_link_or_reparse_component(root))
    ]
    symlink_policy = SymlinkFollowPolicy(
        scan_areas=(),
        max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
        windows_system_context=windows_system_context,
    )

    def admit_root(root: Path) -> Path | None:
        if is_link_or_reparse(root):
            target = symlink_policy.inspect(root)
            if (
                target is None
                or not is_real_directory(target)
                or not symlink_policy.claim(target)
            ):
                return None
            symlink_policy.add_scan_area(target, MAX_DEPTH)
            return target
        return root if is_real_directory(root) else None

    admitted_homes: list[Path] = []
    home_systems: list[str] = []
    logical_home_mappings: list[tuple[Path, Path]] = []
    for index, configured_home in admissible_homes:
        admitted = admit_root(configured_home)
        if admitted is None:
            continue
        admitted_homes.append(admitted)
        if admitted != configured_home:
            logical_home_mappings.append((admitted, configured_home))
        home_systems.append(
            "Linux" if actual_system == "Windows" and index > 0 else actual_system
        )
    admitted_temp_roots = tuple(
        dict.fromkeys(
            admitted
            for root in admissible_temp_roots
            if (admitted := admit_root(root)) is not None
        )
    )
    seen_files: set[str] = set()
    roots = _discover_roots(
        admitted_homes,
        home_systems=home_systems,
        temp_roots=admitted_temp_roots,
        include_files=include_files,
        budget=budget,
        result=result,
        checkpoint=checkpoint,
        symlink_policy=symlink_policy,
        seen_files=seen_files,
    )
    seen_directories: set[str] = set()
    walkers = deque(
        (
            root,
            _walk_root(
                root,
                include_files=include_files,
                budget=budget,
                checkpoint=checkpoint,
                seen_directories=seen_directories,
                seen_files=seen_files,
                result=result,
                symlink_policy=symlink_policy,
            ),
        )
        for root in roots
    )

    def collect(_root: Path, path: Path | None) -> None:
        if path is not None:
            result.files.append(path)

    drain_round_robin(
        walkers,
        visit=collect,
        should_stop=lambda: _deadline_expired(budget),
        checkpoint=checkpoint,
    )
    result.truncated = (
        budget.discovery_truncated
        or budget.root_selection_truncated
        or budget.truncated
    )

    # Preserve the linked home prefix; deeper follows outside it report realpaths.
    def logical_home_path(path: Path) -> Path:
        for actual_home, logical_home in logical_home_mappings:
            try:
                relative = path.relative_to(actual_home)
            except ValueError:
                continue
            return logical_home.joinpath(*relative.parts)
        return path

    logical_files = [(logical_home_path(target), target) for target in result.files]
    result.files = [logical_path for logical_path, _target in logical_files]
    result.file_targets = {
        logical_path: target
        for logical_path, target in logical_files
        if logical_path != target
    }
    result.node_modules_paths = [
        logical_home_path(path) for path in result.node_modules_paths
    ]
    result.python_env_roots = [
        logical_home_path(path) for path in result.python_env_roots
    ]
    return result
