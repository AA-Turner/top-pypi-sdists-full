"""Bounded content probe for skills hidden in browser and updater data."""

from __future__ import annotations

import fnmatch
import hashlib
import os
import stat
import time
from collections import deque
from collections.abc import Callable, Generator, Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import structlog

from runlayer_cli.scan.file_collector import MAX_SINGLE_FILE_BYTES, MAX_TOTAL_BYTES
from runlayer_cli.scan.hidden_space_sweep import scan_hidden_spaces
from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowPolicy,
    drain_round_robin,
    has_link_or_reparse_component,
    is_contained_real_directory,
    is_link_or_reparse,
    is_real_directory,
    realpath_key,
)
from runlayer_cli.scan.skill_scanner import (
    DiscoveredSkillArtifact,
    SkillFile,
    apply_retention_policy,
    build_skill_artifact_from_files,
    has_skill_structure,
)
from runlayer_cli.scan.windows_users import is_windows_system_context

logger = structlog.get_logger(__name__)

MAX_PROBE_DEPTH = 6
MAX_PROBE_ROOTS = 128
MAX_ROOT_EXPANSION_ENTRIES = 10_000
MAX_PROBE_DIRECTORIES = 2000
MAX_PROBE_ENTRIES = 10_000
MAX_ENTRIES_PER_DIRECTORY = 5000
MAX_CANDIDATES = 256
MAX_CANDIDATE_BYTES = MAX_SINGLE_FILE_BYTES
MAX_TOTAL_CANDIDATE_BYTES = MAX_TOTAL_BYTES
MAX_CANDIDATE_SNIFF_BYTES = 16
MAX_CANDIDATE_PREFIX_BYTES = 512
MAX_FOLLOWED_SYMLINK_TARGETS = 64

_SUPPORTS_POSIX_DESCRIPTOR_WALK = (
    os.name == "posix" and hasattr(os, "O_NOFOLLOW") and os.open in os.supports_dir_fd
)

_CACHE_FAMILY_SUBTREES = (
    "Cache",
    "Code Cache",
    "Service Worker/CacheStorage",
)
_ELECTRON_APP_NAMES = ("Cursor", "Code", "Windsurf", "Claude")


def _cache_family_patterns(bases: Sequence[str]) -> tuple[str, ...]:
    return tuple(
        f"{base}/{subtree}" for base in bases for subtree in _CACHE_FAMILY_SUBTREES
    )


_MACOS_ELECTRON_CACHE_BASES = tuple(
    f"Library/Application Support/{app}" for app in _ELECTRON_APP_NAMES
)
_WINDOWS_ELECTRON_CACHE_BASES = tuple(
    f"AppData/Roaming/{app}" for app in _ELECTRON_APP_NAMES
)
_LINUX_ELECTRON_CACHE_BASES = tuple(f".config/{app}" for app in _ELECTRON_APP_NAMES)

# Keep these legacy vendor/product probes explicit. Generic omitted-space
# coverage comes from the separately bounded hidden-space sweep, not wildcard
# expansion of this list.
_ALLOWLISTED_ROOT_PATTERNS: tuple[str, ...] = (
    # macOS Chromium-family profile caches.
    "Library/Application Support/Google/Chrome/*/Cache",
    "Library/Application Support/Google/Chrome/*/Code Cache",
    "Library/Application Support/Google/Chrome/*/Service Worker/CacheStorage",
    "Library/Application Support/Google/Chrome/*/Local Extension Settings",
    "Library/Application Support/Microsoft Edge/*/Cache",
    "Library/Application Support/Microsoft Edge/*/Code Cache",
    "Library/Application Support/Microsoft Edge/*/Service Worker/CacheStorage",
    "Library/Application Support/Microsoft Edge/*/Local Extension Settings",
    "Library/Application Support/BraveSoftware/Brave-Browser/*/Cache",
    "Library/Application Support/BraveSoftware/Brave-Browser/*/Code Cache",
    "Library/Application Support/BraveSoftware/Brave-Browser/*/Service Worker/CacheStorage",
    "Library/Application Support/BraveSoftware/Brave-Browser/*/Local Extension Settings",
    *_cache_family_patterns(("Library/Application Support/Chromium/*",)),
    "Library/Application Support/Chromium/*/Local Extension Settings",
    *_cache_family_patterns(_MACOS_ELECTRON_CACHE_BASES),
    "Library/Caches/Google/Chrome/*/Cache",
    "Library/Caches/Microsoft Edge/*/Cache",
    "Library/Caches/BraveSoftware/Brave-Browser/*/Cache",
    "Library/Caches/Chromium/*/Cache",
    "Library/Application Support/Firefox/Profiles/*/storage",
    "Library/Caches/Firefox/Profiles/*/cache2",
    "Library/Caches/Google/GoogleSoftwareUpdate",
    "Library/Caches/Microsoft/EdgeUpdater",
    "Library/Caches/com.brave.Browser",
    # Windows Chromium-family profiles and update caches.
    "AppData/Local/Google/Chrome/User Data/*/Cache",
    "AppData/Local/Google/Chrome/User Data/*/Code Cache",
    "AppData/Local/Google/Chrome/User Data/*/Service Worker/CacheStorage",
    "AppData/Local/Google/Chrome/User Data/*/Local Extension Settings",
    "AppData/Local/Microsoft/Edge/User Data/*/Cache",
    "AppData/Local/Microsoft/Edge/User Data/*/Code Cache",
    "AppData/Local/Microsoft/Edge/User Data/*/Service Worker/CacheStorage",
    "AppData/Local/Microsoft/Edge/User Data/*/Local Extension Settings",
    "AppData/Local/BraveSoftware/Brave-Browser/User Data/*/Cache",
    "AppData/Local/BraveSoftware/Brave-Browser/User Data/*/Code Cache",
    "AppData/Local/BraveSoftware/Brave-Browser/User Data/*/Service Worker/CacheStorage",
    "AppData/Local/BraveSoftware/Brave-Browser/User Data/*/Local Extension Settings",
    *_cache_family_patterns(("AppData/Local/Chromium/User Data/*",)),
    "AppData/Local/Chromium/User Data/*/Local Extension Settings",
    *_cache_family_patterns(_WINDOWS_ELECTRON_CACHE_BASES),
    "AppData/Local/Mozilla/Firefox/Profiles/*/cache2",
    "AppData/Roaming/Mozilla/Firefox/Profiles/*/storage",
    "AppData/Local/Google/Update",
    "AppData/Local/Microsoft/EdgeUpdate",
    "AppData/Local/BraveSoftware/Update",
    # Linux Chromium-family and Firefox profile caches.
    ".cache/google-chrome/*/Cache",
    ".cache/google-chrome/*/Code Cache",
    ".cache/chromium/*/Cache",
    ".cache/chromium/*/Code Cache",
    ".cache/microsoft-edge/*/Cache",
    ".cache/microsoft-edge/*/Code Cache",
    ".cache/BraveSoftware/Brave-Browser/*/Cache",
    ".cache/BraveSoftware/Brave-Browser/*/Code Cache",
    ".config/google-chrome/*/Service Worker/CacheStorage",
    ".config/google-chrome/*/Local Extension Settings",
    ".config/chromium/*/Service Worker/CacheStorage",
    ".config/chromium/*/Local Extension Settings",
    ".config/microsoft-edge/*/Service Worker/CacheStorage",
    ".config/microsoft-edge/*/Local Extension Settings",
    ".config/BraveSoftware/Brave-Browser/*/Service Worker/CacheStorage",
    ".config/BraveSoftware/Brave-Browser/*/Local Extension Settings",
    *_cache_family_patterns(_LINUX_ELECTRON_CACHE_BASES),
    ".cache/mozilla/firefox/*/cache2",
    ".mozilla/firefox/*/storage",
)

# Populate only with trustworthy full-content hashes. The valid-structure path
# remains the normal classifier; this hook supports exact known copies without
# introducing filename or benchmark-specific aliases.
KNOWN_SKILL_CONTENT_SHA256: frozenset[str] = frozenset()


@dataclass
class _ProbeBudget:
    root_expansion_entries: int = 0
    directories: int = 0
    entries: int = 0
    candidates: int = 0
    bytes_read: int = 0
    deadline: float | None = None
    truncated: bool = False


def _deadline_expired(budget: _ProbeBudget) -> bool:
    if budget.deadline is not None and time.monotonic() >= budget.deadline:
        budget.truncated = True
    return budget.truncated


@dataclass(frozen=True)
class _ExpandedRoot:
    path: Path
    is_directory: bool
    followed: bool = False


@dataclass(frozen=True)
class _CandidatePath:
    path: Path
    reported_path: Path
    followed_target: Path | None = None


@dataclass(frozen=True)
class _AllowlistedEntryResult:
    next_parent: Path | None = None
    next_followed: bool = False
    expanded_root: _ExpandedRoot | None = None


def _inspect_allowlisted_link_target(
    link_path: Path,
    *,
    symlink_policy: SymlinkFollowPolicy,
) -> Path | None:
    """Resolve a claimable target or one already covered capacity-free."""
    target = symlink_policy.inspect(link_path)
    if target is None:
        target = symlink_policy.inspect_covered_link(link_path)
    return target


def _classify_allowlisted_entry(
    entry: os.DirEntry[str],
    *,
    pattern_component: str,
    final_component: bool,
    followed: bool,
    symlink_policy: SymlinkFollowPolicy,
) -> _AllowlistedEntryResult:
    """Classify one wildcard match as a terminal root or next expansion node."""
    try:
        if not fnmatch.fnmatch(entry.name, pattern_component):
            return _AllowlistedEntryResult()
        entry_path = Path(entry.path)
        if is_link_or_reparse(entry_path):
            target = _inspect_allowlisted_link_target(
                entry_path,
                symlink_policy=symlink_policy,
            )
            if target is None:
                return _AllowlistedEntryResult()
            target_info = target.stat()
            if stat.S_ISDIR(target_info.st_mode):
                if not symlink_policy.admit_targets((target,)):
                    return _AllowlistedEntryResult()
                return _AllowlistedEntryResult(
                    next_parent=target,
                    next_followed=True,
                )
            if stat.S_ISREG(target_info.st_mode) and final_component:
                if not symlink_policy.admit_targets((target,)):
                    return _AllowlistedEntryResult()
                return _AllowlistedEntryResult(
                    expanded_root=_ExpandedRoot(
                        target,
                        is_directory=False,
                        followed=True,
                    )
                )
            return _AllowlistedEntryResult()
        if entry.is_dir(follow_symlinks=False):
            return _AllowlistedEntryResult(
                next_parent=entry_path,
                next_followed=followed,
            )
    except OSError:
        pass
    return _AllowlistedEntryResult()


def _expand_allowlisted_pattern(
    home: Path,
    pattern: str,
    *,
    budget: _ProbeBudget,
    checkpoint: Callable[[], None] | None,
    symlink_policy: SymlinkFollowPolicy,
) -> Iterator[_ExpandedRoot | None]:
    parts = Path(pattern).parts

    def walk(
        parent: Path,
        index: int,
        *,
        followed: bool = False,
    ) -> Iterator[_ExpandedRoot | None]:
        if index >= len(parts):
            try:
                info = parent.lstat()
            except OSError:
                return
            if stat.S_ISDIR(info.st_mode):
                yield _ExpandedRoot(parent, is_directory=True, followed=followed)
            elif stat.S_ISREG(info.st_mode):
                yield _ExpandedRoot(parent, is_directory=False, followed=followed)
            return

        part = parts[index]
        if any(character in part for character in "*?["):
            try:
                with os.scandir(parent) as entries:
                    entry_iterator = iter(entries)
                    while (
                        budget.root_expansion_entries < MAX_ROOT_EXPANSION_ENTRIES
                        and not _deadline_expired(budget)
                    ):
                        try:
                            entry = next(entry_iterator)
                        except StopIteration:
                            break
                        budget.root_expansion_entries += 1
                        if checkpoint is not None:
                            checkpoint()
                        classified = _classify_allowlisted_entry(
                            entry,
                            pattern_component=part,
                            final_component=index + 1 == len(parts),
                            followed=followed,
                            symlink_policy=symlink_policy,
                        )
                        if classified.expanded_root is not None:
                            yield classified.expanded_root
                            continue
                        if classified.next_parent is None:
                            yield None
                            continue
                        yielded = False
                        for result in walk(
                            classified.next_parent,
                            index + 1,
                            followed=classified.next_followed,
                        ):
                            yielded = True
                            yield result
                        if not yielded:
                            yield None
            except OSError:
                return
        else:
            child = parent / part
            if is_link_or_reparse(child):
                if budget.root_expansion_entries >= MAX_ROOT_EXPANSION_ENTRIES:
                    return
                budget.root_expansion_entries += 1
                if checkpoint is not None:
                    checkpoint()
                target = _inspect_allowlisted_link_target(
                    child,
                    symlink_policy=symlink_policy,
                )
                if target is None:
                    return
                try:
                    target_info = target.stat()
                except OSError:
                    return
                if stat.S_ISDIR(target_info.st_mode):
                    if symlink_policy.admit_targets((target,)):
                        yield from walk(target, index + 1, followed=True)
                elif stat.S_ISREG(target_info.st_mode) and index + 1 == len(parts):
                    if symlink_policy.admit_targets((target,)):
                        yield _ExpandedRoot(target, is_directory=False, followed=True)
            elif is_real_directory(child):
                yield from walk(child, index + 1, followed=followed)

    yield from walk(home, 0)


def _tolerant_expansion(
    home: Path,
    pattern: str,
    *,
    budget: _ProbeBudget,
    checkpoint: Callable[[], None] | None,
    symlink_policy: SymlinkFollowPolicy,
) -> Generator[_ExpandedRoot | None, None, None]:
    try:
        yield from _expand_allowlisted_pattern(
            home,
            pattern,
            budget=budget,
            checkpoint=checkpoint,
            symlink_policy=symlink_policy,
        )
    except OSError:
        return


def _probe_roots(
    homes: Sequence[Path],
    *,
    budget: _ProbeBudget,
    checkpoint: Callable[[], None] | None,
    symlink_policy: SymlinkFollowPolicy,
) -> list[_ExpandedRoot]:
    """Expand allowlisted patterns round-robin across homes and patterns.

    Each (home, pattern) pair contributes one root per turn, so a
    profile-heavy browser family or an early home cannot fill
    ``MAX_PROBE_ROOTS`` before later allowlist entries and WSL homes are
    considered.
    """
    roots: list[_ExpandedRoot] = []
    seen: set[str] = set()
    expansions: deque[tuple[Path, Generator[_ExpandedRoot | None, None, None]]] = deque(
        (
            home,
            _tolerant_expansion(
                home,
                pattern,
                budget=budget,
                checkpoint=checkpoint,
                symlink_policy=symlink_policy,
            ),
        )
        for home in homes
        for pattern in _ALLOWLISTED_ROOT_PATTERNS
    )

    def _collect(home: Path, root: _ExpandedRoot | None) -> None:
        if root is None:
            return
        if root.is_directory:
            valid = root.followed or is_contained_real_directory(home, root.path)
        else:
            valid = (
                root.followed or is_contained_real_directory(home, root.path.parent)
            ) and not is_link_or_reparse(root.path)
        if not valid:
            return
        key = realpath_key(root.path)
        if key not in seen:
            seen.add(key)
            roots.append(root)
            if root.is_directory:
                symlink_policy.add_scan_area(root.path, MAX_PROBE_DEPTH)

    drain_round_robin(
        expansions,
        visit=_collect,
        should_stop=lambda: (
            len(roots) >= MAX_PROBE_ROOTS
            or budget.root_expansion_entries >= MAX_ROOT_EXPANSION_ENTRIES
            or _deadline_expired(budget)
        ),
    )
    return roots


def _candidate_paths(
    root: Path,
    *,
    budget: _ProbeBudget,
    checkpoint: Callable[[], None] | None,
    symlink_policy: SymlinkFollowPolicy,
    seen_directories: set[str],
) -> Generator[_CandidatePath | None, None, None]:
    queue: deque[tuple[Path, int]] = deque([(root, 0)])
    while queue and not _deadline_expired(budget):
        directory, depth = queue.popleft()
        directory_key = realpath_key(directory)
        if directory_key in seen_directories or not is_real_directory(directory):
            continue
        seen_directories.add(directory_key)
        symlink_policy.mark_visited(directory)
        if budget.directories >= MAX_PROBE_DIRECTORIES:
            budget.truncated = True
            break
        budget.directories += 1
        if checkpoint is not None:
            checkpoint()

        child_directories: list[tuple[Path, int]] = []
        yielded_entry = False
        try:
            entries_seen = 0
            with os.scandir(directory) as entries:
                for entry in entries:
                    if _deadline_expired(budget):
                        break
                    if entries_seen >= MAX_ENTRIES_PER_DIRECTORY:
                        break
                    if budget.entries >= MAX_PROBE_ENTRIES:
                        budget.truncated = True
                        break
                    entries_seen += 1
                    budget.entries += 1
                    output: _CandidatePath | None = None
                    try:
                        path = Path(entry.path)
                        followed = is_link_or_reparse(path)
                        candidate = path
                        if followed:
                            target = symlink_policy.inspect(path)
                            if target is None:
                                yielded_entry = True
                                yield None
                                continue
                            target_info = target.stat()
                            is_directory = stat.S_ISDIR(target_info.st_mode)
                            is_file = stat.S_ISREG(target_info.st_mode)
                            if not (is_directory or is_file):
                                yielded_entry = True
                                yield None
                                continue
                            candidate = target
                        else:
                            is_directory = entry.is_dir(follow_symlinks=False)
                            is_file = entry.is_file(follow_symlinks=False)

                        if is_directory:
                            if followed:
                                if not symlink_policy.claim(candidate):
                                    yielded_entry = True
                                    yield None
                                    continue
                                symlink_policy.add_scan_area(
                                    candidate,
                                    MAX_PROBE_DEPTH,
                                )
                                child_directories.append((candidate, 0))
                            if depth < MAX_PROBE_DEPTH:
                                if not followed:
                                    child_directories.append((candidate, depth + 1))
                        elif is_file:
                            output = _CandidatePath(
                                candidate,
                                reported_path=candidate,
                                followed_target=candidate if followed else None,
                            )
                    except OSError:
                        pass
                    yielded_entry = True
                    yield output
        except OSError:
            continue

        if not yielded_entry:
            yield None
        queue.extend(sorted(child_directories, key=lambda item: str(item[0])))


def _relative_to_logical_home(candidate: Path, home: Path) -> Path | None:
    try:
        relative = Path(os.path.abspath(candidate)).relative_to(
            Path(os.path.abspath(home))
        )
    except ValueError:
        return None
    return relative if relative.parts and os.pardir not in relative.parts else None


def _derive_hidden_candidate_targets(
    paths: Sequence[Path],
    homes: Sequence[Path],
    *,
    targets: Mapping[Path, Path],
    symlink_policy: SymlinkFollowPolicy,
) -> dict[Path, Path]:
    """Map logical candidates through configured linked homes under one cap."""
    resolved_targets = dict(targets)
    for home in homes:
        logical_candidates = [
            (path, relative)
            for path in paths
            if path not in resolved_targets
            and (relative := _relative_to_logical_home(path, home)) is not None
        ]
        if not logical_candidates or not has_link_or_reparse_component(home):
            continue

        resolved_home = symlink_policy.inspect(home)
        if resolved_home is not None:
            if not is_real_directory(resolved_home) or not symlink_policy.claim(
                resolved_home
            ):
                continue
        else:
            resolved_home = symlink_policy.inspect_covered_link(home)
            if resolved_home is None or not is_real_directory(resolved_home):
                continue

        for path, relative in logical_candidates:
            resolved_targets.setdefault(
                path,
                resolved_home.joinpath(*relative.parts),
            )
    return resolved_targets


def _candidate_path_stream(
    paths: Sequence[Path],
    *,
    targets: Mapping[Path, Path],
    symlink_policy: SymlinkFollowPolicy,
) -> Generator[_CandidatePath | None, None, None]:
    seen: set[str] = set()
    for path in sorted(paths):
        mapped_target = targets.get(path)
        candidate = mapped_target if mapped_target is not None else path
        reported_path = path
        followed = mapped_target is None and is_link_or_reparse(candidate)
        if followed:
            target = symlink_policy.inspect(candidate)
            if target is None:
                yield None
                continue
            try:
                target_info = target.stat()
            except OSError:
                yield None
                continue
            if not stat.S_ISREG(target_info.st_mode):
                yield None
                continue
            candidate = target
            reported_path = target
        key = realpath_key(candidate)
        if key in seen:
            continue
        seen.add(key)
        yield _CandidatePath(
            candidate,
            reported_path=reported_path,
            followed_target=candidate if followed else None,
        )


def _normal_skill_prefix(path: Path) -> str:
    normalized = os.path.normcase(os.path.abspath(path))
    return normalized if normalized.endswith(os.sep) else normalized + os.sep


def _is_covered_by_normal_skill(
    candidate_absolute: str,
    normal_skill_prefixes: Sequence[str],
) -> bool:
    candidate_prefix = (
        candidate_absolute
        if candidate_absolute.endswith(os.sep)
        else candidate_absolute + os.sep
    )
    return any(
        candidate_prefix.startswith(skill_prefix)
        for skill_prefix in normal_skill_prefixes
    )


def _has_skill_frontmatter_prefix(content_bytes: bytes) -> bool:
    lines = content_bytes.splitlines()
    return bool(lines) and lines[0].strip() == b"---"


def _has_skill_frontmatter_sniff(content_bytes: bytes) -> bool:
    stripped = content_bytes.lstrip()
    return stripped.startswith(b"---") and (
        len(stripped) == 3 or stripped[3:4].isspace()
    )


def validate_disguised_skill_content(content_bytes: bytes) -> str | None:
    """Return decoded content only when it has durable skill identity."""
    if not content_bytes or len(content_bytes) > MAX_CANDIDATE_BYTES:
        return None
    try:
        content = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return None
    fingerprint = hashlib.sha256(content_bytes).hexdigest()
    if fingerprint not in KNOWN_SKILL_CONTENT_SHA256 and not has_skill_structure(
        content
    ):
        return None
    return content


def _is_reparse(info: os.stat_result) -> bool:
    attributes = getattr(info, "st_file_attributes", 0)
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def _path_matches_opened_file(candidate: Path, opened: os.stat_result) -> bool:
    absolute = Path(os.path.abspath(candidate))
    current = Path(absolute.anchor)
    try:
        root_info = current.lstat()
        if not stat.S_ISDIR(root_info.st_mode) or _is_reparse(root_info):
            return False
        for part in absolute.parts[1:-1]:
            current /= part
            info = current.lstat()
            if not stat.S_ISDIR(info.st_mode) or _is_reparse(info):
                return False
        final = absolute.lstat()
    except OSError:
        return False
    return (
        stat.S_ISREG(final.st_mode)
        and not _is_reparse(final)
        and (final.st_dev, final.st_ino) == (opened.st_dev, opened.st_ino)
    )


def _open_posix_candidate(candidate: Path) -> tuple[int, os.stat_result]:
    absolute = Path(os.path.abspath(candidate))
    if not absolute.anchor or len(absolute.parts) < 2:
        raise OSError("candidate has no anchored filename")
    directory_flags = (
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    )
    file_flags = (
        os.O_RDONLY
        | os.O_NOFOLLOW
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_BINARY", 0)
    )
    directory_descriptor = os.open(absolute.anchor, directory_flags)
    try:
        for part in absolute.parts[1:-1]:
            next_descriptor = os.open(
                part,
                directory_flags,
                dir_fd=directory_descriptor,
            )
            next_info = os.fstat(next_descriptor)
            if not stat.S_ISDIR(next_info.st_mode):
                os.close(next_descriptor)
                raise OSError("candidate ancestor is not a directory")
            os.close(directory_descriptor)
            directory_descriptor = next_descriptor
        descriptor = os.open(
            absolute.parts[-1],
            file_flags,
            dir_fd=directory_descriptor,
        )
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            os.close(descriptor)
            raise OSError("candidate is not a regular file")
        return descriptor, opened
    finally:
        os.close(directory_descriptor)


def _open_conservative_candidate(candidate: Path) -> tuple[int, os.stat_result]:
    initial = candidate.lstat()
    if (
        not stat.S_ISREG(initial.st_mode)
        or _is_reparse(initial)
        or not _path_matches_opened_file(candidate, initial)
    ):
        raise OSError("candidate path is not a real regular file")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(candidate, flags)
    opened = os.fstat(descriptor)
    if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (
        initial.st_dev,
        initial.st_ino,
    ):
        os.close(descriptor)
        raise OSError("candidate changed while opening")
    return descriptor, opened


def _open_candidate(candidate: Path) -> tuple[int, os.stat_result]:
    if _SUPPORTS_POSIX_DESCRIPTOR_WALK:
        return _open_posix_candidate(candidate)
    return _open_conservative_candidate(candidate)


def _artifact_from_candidate(
    candidate: Path,
    *,
    budget: _ProbeBudget,
    reported_path: Path | None = None,
) -> DiscoveredSkillArtifact | None:
    descriptor: int | None = None
    try:
        prefiltered_size = candidate.lstat().st_size
        if prefiltered_size <= 0 or prefiltered_size > MAX_CANDIDATE_BYTES:
            return None
        descriptor, opened = _open_candidate(candidate)
        size = opened.st_size
        remaining_budget = MAX_TOTAL_CANDIDATE_BYTES - budget.bytes_read
        if (
            size <= 0
            or size > MAX_CANDIDATE_BYTES
            or remaining_budget <= 0
            or size > remaining_budget
        ):
            return None

        with os.fdopen(descriptor, "rb") as handle:
            descriptor = None
            sniff = handle.read(
                min(
                    MAX_CANDIDATE_SNIFF_BYTES,
                    MAX_CANDIDATE_PREFIX_BYTES,
                    MAX_CANDIDATE_BYTES,
                    remaining_budget,
                )
            )
            budget.bytes_read += len(sniff)
            if not sniff:
                return None
            if not KNOWN_SKILL_CONTENT_SHA256 and not _has_skill_frontmatter_sniff(
                sniff
            ):
                return None

            remaining_budget = MAX_TOTAL_CANDIDATE_BYTES - budget.bytes_read
            prefix_tail = handle.read(
                min(
                    MAX_CANDIDATE_PREFIX_BYTES - len(sniff),
                    MAX_CANDIDATE_BYTES - len(sniff),
                    remaining_budget,
                )
            )
            budget.bytes_read += len(prefix_tail)
            prefix = sniff + prefix_tail
            if not KNOWN_SKILL_CONTENT_SHA256 and not _has_skill_frontmatter_prefix(
                prefix
            ):
                return None
            if budget.candidates >= MAX_CANDIDATES:
                budget.truncated = True
                return None
            budget.candidates += 1

            remaining_budget = MAX_TOTAL_CANDIDATE_BYTES - budget.bytes_read
            remaining_size = size - len(prefix)
            if remaining_size < 0 or remaining_size > remaining_budget:
                return None
            content_tail = handle.read(remaining_size)
            budget.bytes_read += len(content_tail)
            content_bytes = prefix + content_tail
            final = os.fstat(handle.fileno())
            if (
                len(content_bytes) > MAX_CANDIDATE_BYTES
                or final.st_size != len(content_bytes)
                or final.st_mtime_ns != opened.st_mtime_ns
                or not _path_matches_opened_file(candidate, opened)
            ):
                return None
    except OSError:
        return None
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass

    content = validate_disguised_skill_content(content_bytes)
    if content is None:
        return None

    artifact_path = reported_path or candidate
    artifact = build_skill_artifact_from_files(
        skill_path=str(artifact_path.absolute()),
        files=[SkillFile(title="SKILL.md", content=content)],
        marker_content=content,
        scope="user",
        tool="browser_cache",
        fallback_name=artifact_path.stem or artifact_path.name,
        source_type="user",
    )
    if artifact is not None:
        apply_retention_policy(artifact)
    return artifact


def scan_disguised_skills(
    *,
    home: Path | None = None,
    extra_home_roots: Sequence[Path] = (),
    hidden_candidates: Sequence[Path] | None = None,
    hidden_candidate_targets: Mapping[Path, Path] | None = None,
    normal_skill_paths: Sequence[Path] = (),
    time_budget_s: float | None = None,
    checkpoint: Callable[[], None] | None = None,
) -> list[DiscoveredSkillArtifact]:
    """Probe bounded omitted filesystem spaces for structurally valid skills.

    Resolved hidden-candidate targets are opened securely while their mapping
    keys remain the artifact reporting paths. Missing mappings are derived only
    beneath configured linked homes through the shared follow policy.
    """
    started_at = time.monotonic()
    deadline = (
        started_at + max(time_budget_s, 0.0) if time_budget_s is not None else None
    )
    budget = _ProbeBudget(deadline=deadline)
    artifacts: list[DiscoveredSkillArtifact] = []
    native_home = home or Path.home()
    homes = (native_home, *extra_home_roots)
    normal_skill_prefixes = tuple(
        dict.fromkeys(_normal_skill_prefix(path) for path in normal_skill_paths)
    )
    windows_system_context = is_windows_system_context()
    symlink_policy = SymlinkFollowPolicy(
        scan_areas=(),
        max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
        windows_system_context=windows_system_context,
    )
    if hidden_candidates is None:
        remaining_time_budget = (
            max(deadline - time.monotonic(), 0.0) if deadline is not None else None
        )
        hidden_space_result = scan_hidden_spaces(
            home=native_home,
            extra_home_roots=extra_home_roots,
            include_files=True,
            temp_roots=() if home is not None else None,
            time_budget_s=remaining_time_budget,
            checkpoint=checkpoint,
        )
        candidates = hidden_space_result.files
        candidate_targets: Mapping[Path, Path] = hidden_space_result.file_targets
    else:
        candidates = list(hidden_candidates)
        candidate_targets = hidden_candidate_targets or {}
    if windows_system_context:
        candidate_targets = {}
    else:
        candidate_targets = _derive_hidden_candidate_targets(
            candidates,
            homes,
            targets=candidate_targets,
            symlink_policy=symlink_policy,
        )
    roots = _probe_roots(
        homes,
        budget=budget,
        checkpoint=checkpoint,
        symlink_policy=symlink_policy,
    )

    seen_directories: set[str] = set()
    candidate_iterators = deque(
        (
            root.path,
            (
                _candidate_paths(
                    root.path,
                    budget=budget,
                    checkpoint=checkpoint,
                    symlink_policy=symlink_policy,
                    seen_directories=seen_directories,
                )
                if root.is_directory
                else _candidate_path_stream(
                    (root.path,),
                    targets={},
                    symlink_policy=symlink_policy,
                )
            ),
        )
        for root in roots
    )
    if candidates:
        candidate_iterators.append(
            (
                native_home,
                _candidate_path_stream(
                    candidates,
                    targets=candidate_targets,
                    symlink_policy=symlink_policy,
                ),
            )
        )

    visited_candidates: set[str] = set()

    def _visit(_root: Path, candidate: _CandidatePath | None) -> None:
        if candidate is None:
            return
        candidate_path = candidate.path
        key = realpath_key(candidate_path)
        if key in visited_candidates or _is_covered_by_normal_skill(
            os.path.normcase(os.path.abspath(candidate_path)),
            normal_skill_prefixes,
        ):
            return
        visited_candidates.add(key)
        if candidate.followed_target is None:
            symlink_policy.mark_visited(candidate_path)
        artifact = _artifact_from_candidate(
            candidate_path,
            budget=budget,
            reported_path=candidate.reported_path,
        )
        if artifact is not None and (
            candidate.followed_target is None
            or symlink_policy.claim(candidate.followed_target)
        ):
            artifacts.append(artifact)

    drain_round_robin(
        candidate_iterators,
        visit=_visit,
        should_stop=lambda: _deadline_expired(budget),
        checkpoint=checkpoint,
    )
    logger.info(
        "Disguised skill probe complete",
        directories=budget.directories,
        entries=budget.entries,
        candidates=budget.candidates,
        bytes_read=budget.bytes_read,
        truncated=budget.truncated,
        elapsed_ms=round((time.monotonic() - started_at) * 1000),
    )
    return artifacts
