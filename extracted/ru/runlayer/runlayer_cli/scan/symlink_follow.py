"""Bounded symlink-target crawling for project scans."""

from __future__ import annotations

import fnmatch
import stat
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, TypeVar

import structlog

from runlayer_cli.scan.concurrency import bounded_thread_pool
from runlayer_cli.scan.scanner_primitives import SymlinkFollowPolicy
from runlayer_cli.scan.skip_dirs import find_excluded_directories

if TYPE_CHECKING:
    from runlayer_cli.scan.resource_governor import ResourceGovernor

logger = structlog.get_logger(__name__)

_CASE_INSENSITIVE_FILENAMES = frozenset({"skill.md"})
_FOLLOW_EXCLUDED_DIRECTORIES = find_excluded_directories()
_SHARD_RESULT = TypeVar("_SHARD_RESULT")
_SearchCallable = Callable[..., list[Path]]


class _PathBudget(Protocol):
    """Result budget supplied by the parent project crawl."""

    def reserve(self) -> bool: ...

    def release(self) -> None: ...


@dataclass
class _PathShardResult:
    """Paths and links surfaced independently by one crawl shard."""

    found_paths: list[Path]
    symlink_paths: list[Path]


@dataclass
class FollowedSymlinkCrawlResult:
    """Physical results plus per-target identity tuples for file-link aliases.

    ``logical_paths`` maps each regular-file link target to its identity
    tuple: the physical target first when any crawl (initial or followed)
    discovered it on disk, followed by the sorted link aliases.
    """

    found_paths: list[Path]
    node_modules_paths: list[Path]
    logical_paths: dict[Path, tuple[Path, ...]]


def _partition_roots(roots: list[Path], group_count: int) -> list[list[Path]]:
    """Split roots deterministically across a modest number of process groups."""
    groups: list[list[Path]] = [[] for _ in range(min(max(1, group_count), len(roots)))]
    for index, root in enumerate(roots):
        groups[index % len(groups)].append(root)
    return groups


def _group_shards(
    root_groups: list[list[Path]],
    shard: Callable[[list[Path]], _SHARD_RESULT],
) -> list[Callable[[], _SHARD_RESULT]]:
    """Bind each root group to one deferred shard call."""
    return [lambda group=group: shard(group) for group in root_groups]


def _run_path_link_shards(
    work: list[Callable[[], _PathShardResult]],
    *,
    max_workers: int,
) -> _PathShardResult:
    """Run shards with private link buffers and merge deterministically."""
    if not work:
        return _PathShardResult(found_paths=[], symlink_paths=[])

    with bounded_thread_pool(
        max_workers=max_workers,
        task_count=len(work),
    ) as pool:
        futures = [pool.submit(task) for task in work]
        shard_results = pool.gather(futures)
    return _PathShardResult(
        found_paths=sorted(
            {path for result in shard_results for path in result.found_paths}
        ),
        symlink_paths=sorted(
            {path for result in shard_results for path in result.symlink_paths}
        ),
    )


def _remaining_shard_timeout(deadline: float, roots: list[Path]) -> float | None:
    """Return this shard's share of the aggregate crawl deadline."""
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        logger.warning(
            "crawl_shard_skipped_deadline",
            roots=[str(root) for root in roots],
        )
        return None
    return remaining


def _unix_shard(
    roots: list[Path],
    *,
    search: _SearchCallable,
    filenames: list[str],
    deadline: float,
    max_depth: int,
    governor: ResourceGovernor | None,
    path_budget: _PathBudget | None,
    discover_node_modules: bool = False,
) -> _PathShardResult:
    """Run one Unix shard with its own surfaced-link buffer."""
    remaining_timeout = _remaining_shard_timeout(deadline, roots)
    if remaining_timeout is None:
        return _PathShardResult(found_paths=[], symlink_paths=[])
    shard_links: list[Path] = []
    return _PathShardResult(
        found_paths=search(
            filenames,
            remaining_timeout,
            max_depth,
            roots=roots,
            governor=governor,
            path_budget=path_budget,
            discover_node_modules=discover_node_modules,
            symlink_paths=shard_links,
        ),
        symlink_paths=shard_links,
    )


def _windows_shard(
    roots: list[Path],
    *,
    search: _SearchCallable,
    filenames: list[str],
    deadline: float,
    max_depth: int,
    containment_root: Path | None,
    governor: ResourceGovernor | None,
    path_budget: _PathBudget | None,
    windows_system_context: bool,
    discover_node_modules: bool = False,
    recursive: bool = True,
) -> _PathShardResult:
    """Run one Windows shard with its own surfaced-link buffer."""
    remaining_timeout = _remaining_shard_timeout(deadline, roots)
    if remaining_timeout is None:
        return _PathShardResult(found_paths=[], symlink_paths=[])
    if containment_root is None:
        if len(roots) != 1:
            raise ValueError("per-root containment requires exactly one root")
        containment_root = roots[0]
    shard_links: list[Path] = []
    return _PathShardResult(
        found_paths=search(
            filenames,
            remaining_timeout,
            max_depth,
            roots=roots,
            recursive=recursive,
            containment_root=containment_root,
            governor=governor,
            path_budget=path_budget,
            discover_node_modules=discover_node_modules,
            symlink_paths=shard_links,
            windows_system_context=windows_system_context,
        ),
        symlink_paths=shard_links,
    )


def _matches_requested_path(path: Path, patterns: list[str], *, windows: bool) -> bool:
    """Match a surfaced link path with the crawl's filename semantics."""
    candidate = str(path).replace("\\", "/")
    candidate_name = candidate.rsplit("/", 1)[-1]
    for raw_pattern in patterns:
        pattern = raw_pattern.replace("\\", "/")
        case_insensitive = windows or pattern.casefold() in _CASE_INSENSITIVE_FILENAMES
        match_candidate = candidate.casefold() if case_insensitive else candidate
        match_name = candidate_name.casefold() if case_insensitive else candidate_name
        match_pattern = pattern.casefold() if case_insensitive else pattern
        if "/" in pattern:
            if fnmatch.fnmatchcase(match_candidate, f"*/{match_pattern}"):
                return True
        elif fnmatch.fnmatchcase(match_name, match_pattern):
            return True
    return False


def _has_glob_magic(pattern: str) -> bool:
    """Whether a filename uses supported shell/PowerShell wildcard syntax."""
    return any(character in pattern for character in "*?[")


def _is_excluded_symlink_path(
    path: Path,
    *,
    windows: bool,
    discover_node_modules: bool,
) -> bool:
    """Keep followed links subject to the normal directory-prune contract."""
    candidate_parts = tuple(
        part for part in str(path).replace("\\", "/").split("/") if part
    )
    if windows:
        candidate_parts = tuple(part.casefold() for part in candidate_parts)
    for excluded in _FOLLOW_EXCLUDED_DIRECTORIES:
        if discover_node_modules and excluded == "node_modules":
            continue
        excluded_parts = tuple(excluded.replace("\\", "/").split("/"))
        if windows:
            excluded_parts = tuple(part.casefold() for part in excluded_parts)
        if (
            len(candidate_parts) >= len(excluded_parts)
            and candidate_parts[-len(excluded_parts) :] == excluded_parts
        ):
            return True
    return False


def _reserve_followed_path(path_budget: _PathBudget | None) -> bool:
    """Charge manually surfaced targets to the parent crawl's path budget."""
    return path_budget is None or path_budget.reserve()


def _claim_followed_path(
    policy: SymlinkFollowPolicy,
    target: Path,
    path_budget: _PathBudget | None,
) -> bool:
    """Reserve both follow and result capacity without leaking either."""
    if not _reserve_followed_path(path_budget):
        return False
    if policy.claim(target):
        return True
    if path_budget is not None:
        path_budget.release()
    return False


def _crawl_followed_symlink_targets(
    filenames: list[str],
    symlink_paths: list[Path],
    *,
    deadline: float,
    policy: SymlinkFollowPolicy,
    system: str,
    governor: ResourceGovernor | None,
    path_budget: _PathBudget | None,
    discover_node_modules: bool,
    max_workers: int,
    follow_depth: int,
    search_unix: _SearchCallable,
    search_windows: _SearchCallable,
    initial_found_paths: Sequence[Path] = (),
) -> FollowedSymlinkCrawlResult:
    """Drain approved link targets through one bounded iterative frontier."""
    found_paths: list[Path] = []
    found_path_set = set(initial_found_paths)
    # Targets surfaced on disk by the initial crawl or a followed directory
    # crawl, as opposed to targets reachable only through a direct file link.
    physically_found = set(initial_found_paths)
    node_modules_paths: list[Path] = []
    logical_paths: dict[Path, list[Path]] = {}
    frontier = sorted(set(symlink_paths))
    windows = system == "Windows"

    while frontier:
        approved_roots: list[Path] = []
        ordered_frontier = sorted(
            set(frontier),
            key=lambda path: (
                not _matches_requested_path(path, filenames, windows=windows),
                str(path).casefold() if windows else str(path),
            ),
        )
        for link_path in ordered_frontier:
            if time.monotonic() >= deadline:
                break
            if governor is not None:
                governor.checkpoint()
            if _is_excluded_symlink_path(
                link_path,
                windows=windows,
                discover_node_modules=discover_node_modules,
            ):
                continue
            target = policy.inspect(link_path)
            target_is_covered = target is None
            if target_is_covered:
                target = policy.inspect_covered_link(link_path)
            if target is None:
                continue
            try:
                target_mode = target.stat().st_mode
            except OSError:
                continue
            target_is_directory = stat.S_ISDIR(target_mode)
            is_node_modules = target_is_directory and (
                link_path.name.casefold() == "node_modules"
                or target.name.casefold() == "node_modules"
            )
            if (
                target_is_directory
                and not is_node_modules
                and _is_excluded_symlink_path(
                    target,
                    windows=windows,
                    discover_node_modules=discover_node_modules,
                )
            ):
                continue
            if stat.S_ISREG(target_mode):
                if _matches_requested_path(link_path, filenames, windows=windows):
                    target_is_found = target in found_path_set
                    accepted = target_is_found or (
                        _reserve_followed_path(path_budget)
                        if target_is_covered
                        else _claim_followed_path(policy, target, path_budget)
                    )
                    if accepted:
                        if not target_is_found:
                            found_paths.append(target)
                            found_path_set.add(target)
                        logical_paths.setdefault(target, []).append(link_path)
                continue
            if not target_is_directory:
                continue
            if is_node_modules:
                if discover_node_modules and _claim_followed_path(
                    policy, target, path_budget
                ):
                    node_modules_paths.append(target)
                continue
            if not policy.claim(target):
                continue
            policy.add_scan_area(target, follow_depth)
            approved_roots.append(target)

        if not approved_roots:
            break

        if system in ("Darwin", "Linux"):
            root_groups = _partition_roots(approved_roots, max_workers)
            work = _group_shards(
                root_groups,
                partial(
                    _unix_shard,
                    search=search_unix,
                    filenames=filenames,
                    deadline=deadline,
                    max_depth=follow_depth,
                    governor=governor,
                    path_budget=path_budget,
                    discover_node_modules=discover_node_modules,
                ),
            )
        elif system == "Windows":
            root_groups = [[root] for root in approved_roots]
            work = _group_shards(
                root_groups,
                partial(
                    _windows_shard,
                    search=search_windows,
                    filenames=filenames,
                    deadline=deadline,
                    max_depth=follow_depth - 1,
                    containment_root=None,
                    governor=governor,
                    path_budget=path_budget,
                    discover_node_modules=discover_node_modules,
                    windows_system_context=False,
                ),
            )
        else:
            work = []

        crawled = _run_path_link_shards(work, max_workers=max_workers)
        for path in crawled.found_paths:
            physically_found.add(path)
            if path in found_path_set:
                continue
            found_path_set.add(path)
            if path.name.casefold() == "node_modules":
                node_modules_paths.append(path)
            else:
                found_paths.append(path)
        frontier = crawled.symlink_paths

    return FollowedSymlinkCrawlResult(
        found_paths=found_paths,
        node_modules_paths=node_modules_paths,
        logical_paths={
            target: ((target,) if target in physically_found else ())
            + tuple(
                sorted(
                    set(aliases),
                    key=lambda path: (
                        str(path).casefold() if windows else str(path),
                        str(path),
                    ),
                )
            )
            for target, aliases in logical_paths.items()
        },
    )
