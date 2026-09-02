"""Shared filesystem-scanner primitives for artifact inventory modules.

The plugin and disguised-skill scanners walk untrusted user directories under
hard bounds. The primitives here own the safety-critical parts they previously
copy-pasted (and let drift): symlink/reparse-safe path checks, bounded file
reads, fair round-robin draining with guaranteed generator cleanup, and the
storage-contract truncation of plugin metadata fields.

Must stay stdlib-only: this module is inside the AI Watch bundle's transitive
import closure.
"""

from __future__ import annotations

import json
import os
import stat
import threading
from collections import deque
from collections.abc import Callable, Generator, Iterable, Mapping
from pathlib import Path
from typing import Literal, TypedDict, TypeVar

from runlayer_cli.skill_identifier import SkillFileInput, compute_skill_identifier

MAX_PLUGIN_NAME_LENGTH = 255
MAX_PLUGIN_AUTHOR_LENGTH = 255
MAX_PLUGIN_VERSION_LENGTH = 100
MAX_PLUGIN_SOURCE_IDENTIFIER_LENGTH = 255
MAX_PATH_COMPONENTS = 64

_WINDOWS_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)

_CONTEXT = TypeVar("_CONTEXT")
_ITEM = TypeVar("_ITEM")
PluginArtifactKind = Literal["jetbrains_plugin", "vscode_extension"]


class _SymlinkTargetDetails(TypedDict):
    key: str
    is_directory: bool


_PLUGIN_IDENTIFIER_SPECS: dict[PluginArtifactKind, tuple[str, str]] = {
    "jetbrains_plugin": ("plugin_id", "jetbrains-plugin.json"),
    "vscode_extension": ("extension_id", "vscode-extension.json"),
}


def _normalize_realpath_key(realpath: str) -> str:
    return os.path.normcase(os.path.normpath(realpath))


class SymlinkFollowBudget:
    """Share one unique-target follow cap across related policies."""

    def __init__(self, max_followed: int) -> None:
        self._max_followed = max(0, max_followed)
        self._targets: set[str] = set()
        self._lock = threading.Lock()

    def can_claim(self, target_key: str) -> bool:
        with self._lock:
            return (
                target_key in self._targets or len(self._targets) < self._max_followed
            )

    def claim(self, target_key: str) -> bool:
        return self.claim_many((target_key,))

    def claim_many(self, target_keys: Iterable[str]) -> bool:
        unique_keys = set(target_keys)
        with self._lock:
            new_keys = unique_keys - self._targets
            if len(self._targets) + len(new_keys) > self._max_followed:
                return False
            self._targets.update(new_keys)
            return True


class SymlinkFollowPolicy:
    """Decide whether a symlink target needs a separate bounded scan."""

    def __init__(
        self,
        *,
        scan_areas: Iterable[tuple[Path, int | None]],
        max_followed: int = 64,
        windows_system_context: bool = False,
        follow_budget: SymlinkFollowBudget | None = None,
        scan_area_file_depth_delta: int = 0,
    ) -> None:
        self._scan_areas = [
            (_normalize_realpath_key(os.path.realpath(root)), max_depth)
            for root, max_depth in scan_areas
        ]
        self._follow_budget = follow_budget or SymlinkFollowBudget(max_followed)
        self._scan_area_file_depth_delta = max(0, scan_area_file_depth_delta)
        self._windows_system_context = windows_system_context
        self._visited: set[str] = set()
        self._artifact_visited: set[str] = set()
        self._lock = threading.Lock()

    def mark_visited(
        self,
        path: Path,
        *,
        target_is_walk_root: bool = True,
    ) -> None:
        """Record a canonical path already covered by another scan."""
        key = _normalize_realpath_key(os.path.realpath(path))
        with self._lock:
            self._visited.add(key)
            if not target_is_walk_root:
                self._artifact_visited.add(key)

    def _was_visited(self, target_key: str, *, target_is_walk_root: bool) -> bool:
        """Whether this target was visited in a role that blocks this check."""
        visited = self._visited if target_is_walk_root else self._artifact_visited
        return target_key in visited

    def add_scan_area(self, root: Path, max_depth: int | None) -> None:
        """Register a newly approved root before its bounded scan begins."""
        area = (_normalize_realpath_key(os.path.realpath(root)), max_depth)
        with self._lock:
            if area not in self._scan_areas:
                self._scan_areas.append(area)

    def _covered_by_scan_area(
        self,
        target_key: str,
        *,
        target_is_directory: bool,
        include_root: bool = True,
        include_ancestors: bool = True,
    ) -> bool:
        for root_key, max_depth in self._scan_areas:
            try:
                relative = os.path.relpath(target_key, root_key)
            except ValueError:
                continue
            if relative == os.curdir:
                if include_root:
                    return True
                continue
            if relative == os.pardir or relative.startswith(os.pardir + os.sep):
                if not include_ancestors:
                    continue
                try:
                    root_relative = os.path.relpath(root_key, target_key)
                except ValueError:
                    continue
                if root_relative != os.pardir and not root_relative.startswith(
                    os.pardir + os.sep
                ):
                    return True
                continue
            depth = len(relative.split(os.sep))
            effective_max_depth = max_depth
            if effective_max_depth is not None and not target_is_directory:
                effective_max_depth += self._scan_area_file_depth_delta
            if effective_max_depth is None or depth <= effective_max_depth:
                return True
        return False

    def _resolve_link_target(self, link_path: Path) -> Path | None:
        if self._windows_system_context:
            return None
        try:
            return Path(os.path.realpath(link_path.resolve(strict=True)))
        except (OSError, RuntimeError):
            return None

    def _inspect_target_details(
        self,
        target: Path,
    ) -> _SymlinkTargetDetails | None:
        try:
            target_key = _normalize_realpath_key(str(target))
            target_info = target.stat()
        except OSError:
            return None
        target_is_directory = stat.S_ISDIR(target_info.st_mode)
        access_mode = os.R_OK | (os.X_OK if target_is_directory else 0)
        if not os.access(target, access_mode):
            return None
        return {
            "key": target_key,
            "is_directory": target_is_directory,
        }

    def inspect(
        self,
        link_path: Path,
        *,
        target_is_walk_root: bool = True,
    ) -> Path | None:
        """Resolve an eligible target without consuming the follow cap.

        A single-directory check does not treat scan-area roots or their
        ancestors as covered because the root directory itself is not visited.
        """
        target = self._resolve_link_target(link_path)
        if target is None:
            return None
        return self.inspect_target(
            target,
            target_is_walk_root=target_is_walk_root,
        )

    def inspect_covered_link(self, link_path: Path) -> Path | None:
        """Resolve a usable link only when another scan already covers it."""
        target = self._resolve_link_target(link_path)
        if target is None:
            return None
        target_details = self._inspect_target_details(target)
        if target_details is None:
            return None
        with self._lock:
            covered = target_details["key"] in self._visited or (
                self._covered_by_scan_area(
                    target_details["key"],
                    target_is_directory=target_details["is_directory"],
                    include_ancestors=False,
                )
            )
        return target if covered else None

    def inspect_target(
        self,
        target: Path,
        *,
        target_is_walk_root: bool = True,
    ) -> Path | None:
        """Inspect an already resolved target without consuming capacity."""
        if self._windows_system_context:
            return None
        target_details = self._inspect_target_details(target)
        if target_details is None:
            return None

        with self._lock:
            if (
                self._covered_by_scan_area(
                    target_details["key"],
                    target_is_directory=target_details["is_directory"],
                    include_root=target_is_walk_root,
                    include_ancestors=target_is_walk_root,
                )
                or self._was_visited(
                    target_details["key"],
                    target_is_walk_root=target_is_walk_root,
                )
                or not self._follow_budget.can_claim(target_details["key"])
            ):
                return None
        return target

    def claim(
        self,
        target: Path,
        *,
        target_is_walk_root: bool = True,
    ) -> bool:
        """Atomically consume one follow slot for an inspected target."""
        try:
            target_realpath = os.path.realpath(target)
            target_key = _normalize_realpath_key(target_realpath)
            target_is_directory = stat.S_ISDIR(Path(target_realpath).stat().st_mode)
        except OSError:
            return False
        with self._lock:
            if (
                self._covered_by_scan_area(
                    target_key,
                    target_is_directory=target_is_directory,
                    include_root=target_is_walk_root,
                    include_ancestors=target_is_walk_root,
                )
                or self._was_visited(
                    target_key,
                    target_is_walk_root=target_is_walk_root,
                )
                or not self._follow_budget.claim(target_key)
            ):
                return False
            self._visited.add(target_key)
            if not target_is_walk_root:
                self._artifact_visited.add(target_key)
            return True

    def admit_targets(self, targets: Iterable[Path]) -> bool:
        """Claim uncovered targets, accepting ones already covered or visited."""
        target_details: list[tuple[str, bool]] = []
        try:
            for target in targets:
                target_realpath = os.path.realpath(target)
                target_details.append(
                    (
                        _normalize_realpath_key(target_realpath),
                        stat.S_ISDIR(Path(target_realpath).stat().st_mode),
                    )
                )
        except OSError:
            return False

        with self._lock:
            new_keys = {
                target_key
                for target_key, target_is_directory in target_details
                if target_key not in self._visited
                and not self._covered_by_scan_area(
                    target_key,
                    target_is_directory=target_is_directory,
                )
            }
            if not self._follow_budget.claim_many(new_keys):
                return False
            self._visited.update(new_keys)
            return True

    def evaluate(self, link_path: Path) -> Path | None:
        """Return and claim a resolved target only when another scan is needed."""
        target = self.inspect(link_path)
        return target if target is not None and self.claim(target) else None


def link_or_reparse_status(path: Path) -> bool | None:
    """Return link status, or ``None`` when metadata cannot be inspected."""
    try:
        info = path.lstat()
    except OSError:
        return None
    attributes = getattr(info, "st_file_attributes", 0)
    return stat.S_ISLNK(info.st_mode) or bool(attributes & _WINDOWS_REPARSE_POINT)


def is_link_or_reparse(path: Path) -> bool:
    """Whether ``path`` is a symlink or Windows reparse point."""
    return link_or_reparse_status(path) is True


def has_link_or_reparse_component(
    path: Path,
    *,
    anchor: Path | None = None,
    max_components: int = MAX_PATH_COMPONENTS,
) -> bool:
    """Check bounded ancestry root-first, stopping before linked descendants."""
    absolute_path = path.absolute()
    absolute_anchor = (
        anchor.absolute() if anchor is not None else Path(absolute_path.anchor)
    )
    try:
        relative = absolute_path.relative_to(absolute_anchor)
    except ValueError:
        return True
    if len(relative.parts) + 1 > max_components:
        return True
    current = absolute_anchor
    if is_link_or_reparse(current):
        return True
    for part in relative.parts:
        current /= part
        if is_link_or_reparse(current):
            return True
    return False


def read_bounded(path: Path, *, max_bytes: int) -> bytes | None:
    """Read one regular file without following its final symlink."""
    descriptor: int | None = None
    try:
        flags = (
            os.O_RDONLY
            | getattr(os, "O_BINARY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_NONBLOCK", 0)
        )
        descriptor = os.open(path, flags)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_size > max_bytes:
            return None
        with os.fdopen(descriptor, "rb") as file:
            descriptor = None
            value = file.read(max_bytes + 1)
    except OSError:
        return None
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
    return value if len(value) <= max_bytes else None


def environment_value(
    environment: Mapping[str, str],
    key: str,
    *,
    system: str,
) -> str | None:
    """Look up an environment variable, case-insensitively on Windows."""
    value = environment.get(key)
    if value is not None or system != "Windows":
        return value
    folded = key.casefold()
    return next(
        (item for name, item in environment.items() if name.casefold() == folded),
        None,
    )


def is_regular_file(path: Path) -> bool:
    """Whether ``path`` is a regular file (symlinks excluded via ``lstat``)."""
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False


def is_real_directory(path: Path) -> bool:
    """Whether ``path`` is a directory that is neither a symlink nor a
    Windows reparse point (junctions report ``S_ISDIR`` on ``lstat``)."""
    try:
        path_stat = path.lstat()
    except OSError:
        return False
    attributes = getattr(path_stat, "st_file_attributes", 0)
    return stat.S_ISDIR(path_stat.st_mode) and not (attributes & _WINDOWS_REPARSE_POINT)


def is_contained_real_directory(home: Path, candidate: Path) -> bool:
    """Require every candidate path component to be real and inside ``home``."""
    try:
        relative = candidate.relative_to(home)
    except ValueError:
        return False
    if os.pardir in relative.parts:
        return False

    try:
        current = home
        if not is_real_directory(current):
            return False
        for part in relative.parts:
            current /= part
            if not is_real_directory(current):
                return False
        candidate.resolve(strict=True).relative_to(home.resolve(strict=True))
    except (OSError, RuntimeError, ValueError):
        return False
    return True


class SymlinkLayoutResolver:
    """Resolve links only inside an allowlisted layout under shared bounds."""

    def __init__(
        self,
        *,
        policy: SymlinkFollowPolicy,
        windows_system_context: bool,
        max_intermediate_links: int = 64,
    ) -> None:
        self._policy = policy
        self._windows_system_context = windows_system_context
        self._max_intermediate_links = max(0, max_intermediate_links)
        self._policy_links: dict[tuple[Path, bool], Path | None] = {}
        self._policy_targets: dict[tuple[str, bool], Path] = {}
        self._intermediate_links: dict[Path, Path | None] = {}
        self._intermediate_targets: dict[str, Path] = {}
        self._claimed_final_targets: dict[str, Path] = {}

    def _inspect_directory_link(
        self,
        link_path: Path,
        *,
        current: Path,
    ) -> Path | None:
        """Resolve a usable directory link without consuming any capacity."""
        if self._windows_system_context:
            return None
        try:
            target = Path(os.path.realpath(link_path.resolve(strict=True)))
            current_actual = current.resolve(strict=True)
        except (OSError, RuntimeError):
            return None
        if current_actual.is_relative_to(target):
            return None
        if not is_real_directory(target) or not os.access(target, os.R_OK | os.X_OK):
            return None
        return target

    def _inspect_file_link(self, link_path: Path) -> Path | None:
        """Resolve a regular-file link without consuming follow capacity."""
        if self._windows_system_context:
            return None
        target = self._policy._resolve_link_target(link_path)
        return target if target is not None and is_regular_file(target) else None

    def _admit_policy_targets(self, targets: Iterable[Path]) -> bool:
        """Commit validated metadata follows to the shared policy budget."""
        return self._policy.admit_targets(targets)

    def resolve_policy_link(
        self,
        link_path: Path,
        *,
        current: Path,
        target_is_walk_root: bool = True,
        register_current_area: bool = True,
        is_target_covered: Callable[[Path], bool] | None = None,
        target_is_usable: Callable[[Path], bool] | None = None,
    ) -> Path | None:
        """Resolve and policy-claim one link, caching aliases by target and role."""
        link_cache_key = (link_path, target_is_walk_root)
        if link_cache_key in self._policy_links:
            return self._policy_links[link_cache_key]
        if self._windows_system_context:
            self._policy_links[link_cache_key] = None
            return None
        candidate_target = self._inspect_directory_link(link_path, current=current)
        if candidate_target is None:
            self._policy_links[link_cache_key] = None
            return None
        try:
            current_actual = current.resolve(strict=True)
        except (OSError, RuntimeError):
            self._policy_links[link_cache_key] = None
            return None
        if target_is_usable is not None and not target_is_usable(candidate_target):
            self._policy_links[link_cache_key] = None
            return None
        if is_target_covered is not None and is_target_covered(candidate_target):
            self._policy_links[link_cache_key] = None
            return None

        target_key = _normalize_realpath_key(os.path.realpath(candidate_target))
        target_cache_key = (target_key, target_is_walk_root)
        target = self._policy_targets.get(target_cache_key)
        if target is None:
            if register_current_area:
                self._policy.add_scan_area(current_actual, 0)
            inspected = self._policy.inspect(
                link_path,
                target_is_walk_root=target_is_walk_root,
            )
            if (
                inspected is not None
                and _normalize_realpath_key(os.path.realpath(inspected)) == target_key
                and self._policy.claim(
                    inspected,
                    target_is_walk_root=target_is_walk_root,
                )
            ):
                target = inspected
                self._policy_targets[target_cache_key] = target
        self._policy_links[link_cache_key] = target
        return target

    def resolve_intermediate_link(
        self,
        link_path: Path,
        *,
        current: Path,
    ) -> Path | None:
        """Resolve one layout-intermediate link without claiming its leaf yet."""
        if link_path in self._intermediate_links:
            return self._intermediate_links[link_path]
        if self._windows_system_context:
            self._intermediate_links[link_path] = None
            return None
        try:
            target = Path(os.path.realpath(link_path.resolve(strict=True)))
            current_actual = current.resolve(strict=True)
        except (OSError, RuntimeError):
            self._intermediate_links[link_path] = None
            return None
        if current_actual.is_relative_to(target):
            self._intermediate_links[link_path] = None
            return None
        if not is_real_directory(target) or not os.access(target, os.R_OK | os.X_OK):
            self._intermediate_links[link_path] = None
            return None

        target_key = _normalize_realpath_key(os.path.realpath(target))
        resolved = self._intermediate_targets.get(target_key)
        if resolved is None:
            if len(self._intermediate_targets) >= self._max_intermediate_links:
                self._intermediate_links[link_path] = None
                return None
            self._intermediate_targets[target_key] = target
            resolved = target
        self._intermediate_links[link_path] = resolved
        return resolved

    def resolve_directory(
        self,
        approved_root: Path,
        relative: Path,
        *,
        claim_final: bool = False,
        final_is_intermediate: bool = False,
    ) -> Path | None:
        """Resolve one fixed relative layout without following root ancestors."""
        if relative.is_absolute() or os.pardir in relative.parts:
            return None
        try:
            current = approved_root.resolve(strict=True)
        except (OSError, RuntimeError):
            return None
        if not is_real_directory(current):
            return None

        followed_intermediate = claim_final
        final_link_claimed = False
        for index, part in enumerate(relative.parts):
            candidate = current / part
            if is_link_or_reparse(candidate):
                if index < len(relative.parts) - 1 or final_is_intermediate:
                    target = self.resolve_intermediate_link(
                        candidate,
                        current=current,
                    )
                    followed_intermediate = target is not None
                else:
                    target = self.resolve_policy_link(
                        candidate,
                        current=current,
                        register_current_area=False,
                    )
                    final_link_claimed = target is not None
                if target is None or not is_real_directory(target):
                    return None
                current = target
            elif is_real_directory(candidate):
                try:
                    current = candidate.resolve(strict=True)
                except (OSError, RuntimeError):
                    return None
            else:
                return None

        if (
            followed_intermediate
            and not final_link_claimed
            and not final_is_intermediate
        ):
            final_key = _normalize_realpath_key(os.path.realpath(current))
            if not os.access(current, os.R_OK | os.X_OK):
                return None
            if final_key not in self._claimed_final_targets:
                if not self._policy.admit_targets((current,)):
                    return None
                self._claimed_final_targets[final_key] = current
        return current


class _ResolvedSafeRelativeFile(TypedDict):
    path: Path
    followed_targets: tuple[Path, ...]


def _resolve_safe_relative_file(
    install_root: Path,
    relative: Path,
    *,
    resolver: SymlinkLayoutResolver,
    max_components: int = MAX_PATH_COMPONENTS,
    follow_final_symlink: bool = False,
) -> _ResolvedSafeRelativeFile | None:
    """Resolve fixed links and return a canonical non-symlink file leaf."""
    if (
        relative.is_absolute()
        or not relative.parts
        or len(relative.parts) > max_components
        or any(part in {"", os.curdir, os.pardir} for part in relative.parts)
    ):
        return None
    try:
        current = install_root.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    if not is_real_directory(current):
        return None

    followed_targets: list[Path] = []
    for part in relative.parts[:-1]:
        candidate = current / part
        link_status = link_or_reparse_status(candidate)
        if link_status is None:
            return None
        if link_status:
            target = resolver._inspect_directory_link(candidate, current=current)
            if target is None:
                return None
            followed_targets.append(target)
            current = target
        elif is_real_directory(candidate):
            try:
                current = candidate.resolve(strict=True)
            except (OSError, RuntimeError):
                return None
        else:
            return None

    candidate = current / relative.parts[-1]
    link_status = link_or_reparse_status(candidate)
    if link_status is None:
        return None
    if link_status:
        if not follow_final_symlink:
            return None
        target = resolver._inspect_file_link(candidate)
        if target is None:
            return None
        followed_targets.append(target)
        candidate = target
    elif not is_regular_file(candidate):
        return None
    return {
        "path": candidate,
        "followed_targets": tuple(followed_targets),
    }


class SafeRelativeFileRead(TypedDict):
    path: Path
    content: bytes


def read_safe_relative_file(
    install_root: Path,
    relative: Path,
    *,
    resolver: SymlinkLayoutResolver,
    max_bytes: int,
    max_components: int = MAX_PATH_COMPONENTS,
    follow_final_symlink: bool = False,
) -> SafeRelativeFileRead | None:
    """Resolve and read a fixed file, then admit every followed target.

    Admission intentionally follows the bounded read so missing, oversized, or
    unreadable files cannot consume follow capacity.
    """
    resolved_file = _resolve_safe_relative_file(
        install_root,
        relative,
        resolver=resolver,
        max_components=max_components,
        follow_final_symlink=follow_final_symlink,
    )
    if resolved_file is None:
        return None
    content = read_bounded(resolved_file["path"], max_bytes=max_bytes)
    if content is None or not resolver._admit_policy_targets(
        resolved_file["followed_targets"]
    ):
        return None
    return {
        "path": resolved_file["path"],
        "content": content,
    }


def realpath_key(path: Path) -> str:
    """Normalize a path after resolving links."""
    return _normalize_realpath_key(os.path.realpath(path))


def logical_path_key(path: Path) -> str:
    """Normalize a logical path without resolving links."""
    return os.path.normcase(os.path.normpath(str(path)))


def _is_contained_resolved_path(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=True).relative_to(root.resolve(strict=True))
    except (OSError, RuntimeError, ValueError):
        return False
    return True


def resolve_relative_components(
    root: Path,
    components: Iterable[str],
    *,
    policy: SymlinkFollowPolicy,
    approved_links: dict[str, Path],
    max_components: int = MAX_PATH_COMPONENTS,
    follow_final_symlink: bool = True,
) -> Path | None:
    """Resolve fixed components, re-anchoring after each approved link."""
    parts = tuple(components)
    if len(parts) > max_components or any(part in {"", ".", ".."} for part in parts):
        return None
    try:
        current = root.resolve(strict=True)
    except (OSError, RuntimeError):
        return None
    containment_root = current
    for index, part in enumerate(parts):
        candidate = current / part
        if is_link_or_reparse(candidate):
            if index == len(parts) - 1 and not follow_final_symlink:
                return None
            key = logical_path_key(candidate)
            target = approved_links.get(key)
            if target is None:
                target = policy.evaluate(candidate)
                if target is not None:
                    approved_links[key] = target
            if target is None:
                return None
            current = target
            containment_root = target
            continue
        try:
            resolved = candidate.resolve(strict=True)
        except (OSError, RuntimeError):
            return None
        if not _is_contained_resolved_path(resolved, containment_root):
            return None
        current = resolved
    return current


def resolve_approved_path(
    path: Path,
    *,
    policy: SymlinkFollowPolicy,
    approved_links: dict[str, Path],
    max_components: int = MAX_PATH_COMPONENTS,
    follow_final_symlink: bool = True,
) -> Path | None:
    """Resolve one absolute path through explicitly policy-approved links."""
    components = (path, *path.parents)
    if not path.is_absolute() or len(components) > max_components:
        return None
    anchor = Path(path.anchor)
    try:
        relative_parts = path.relative_to(anchor).parts
    except ValueError:
        return None
    return resolve_relative_components(
        anchor,
        relative_parts,
        policy=policy,
        approved_links=approved_links,
        max_components=max_components,
        follow_final_symlink=follow_final_symlink,
    )


def resolved_directory_candidate(
    path: Path,
    *,
    windows_system_context: bool,
    max_components: int = MAX_PATH_COMPONENTS,
) -> Path | None:
    """Validate one directory path without spending a caller's follow budget."""
    policy = SymlinkFollowPolicy(
        scan_areas=[],
        max_followed=max_components,
        windows_system_context=windows_system_context,
    )
    resolved = resolve_approved_path(
        path,
        policy=policy,
        approved_links={},
        max_components=max_components,
    )
    return resolved if resolved is not None and is_real_directory(resolved) else None


def commit_approved_links(
    committed_links: dict[str, Path],
    committed_targets: set[str],
    attempt_links: dict[str, Path],
    *,
    max_followed: int,
) -> bool:
    """Commit one attempt's links if its unique targets fit the shared cap."""
    new_links = {
        key: target
        for key, target in attempt_links.items()
        if key not in committed_links
    }
    new_targets = {
        logical_path_key(target)
        for target in new_links.values()
        if logical_path_key(target) not in committed_targets
    }
    if len(committed_targets) + len(new_targets) > max(0, max_followed):
        return False
    committed_links.update(new_links)
    committed_targets.update(new_targets)
    return True


def iter_directory_entries(directory: Path) -> Generator[Path, None, None]:
    """Yield directory entries, treating unreadable directories as empty."""
    try:
        yield from directory.iterdir()
    except OSError:
        return


def plugin_artifact_identifier(
    kind: PluginArtifactKind,
    source_identifier: str,
    version: str | None,
) -> str:
    """Build the stable content identity shared by marketplace scanners."""
    identifier_key, synthetic_filename = _PLUGIN_IDENTIFIER_SPECS[kind]
    canonical = json.dumps(
        {identifier_key: source_identifier, "version": version},
        separators=(",", ":"),
        sort_keys=True,
    )
    return compute_skill_identifier(
        [SkillFileInput(name=synthetic_filename, content=canonical)]
    ).root


def drain_round_robin(
    iterators: deque[tuple[_CONTEXT, Generator[_ITEM, None, None]]],
    *,
    visit: Callable[[_CONTEXT, _ITEM], None],
    max_entries: int | None = None,
    should_stop: Callable[[], bool] | None = None,
    checkpoint: Callable[[], None] | None = None,
) -> int:
    """Interleave generators fairly, visiting one item per turn.

    Stops when every generator is exhausted, ``max_entries`` items were
    consumed, or ``should_stop`` returns True. Generators left suspended by an
    early stop are always closed, so ``os.scandir`` handles held inside them
    never leak. Returns the number of items consumed.
    """
    consumed = 0
    try:
        while iterators:
            if max_entries is not None and consumed >= max_entries:
                break
            if should_stop is not None and should_stop():
                break
            context, candidates = iterators.popleft()
            try:
                item = next(candidates)
            except StopIteration:
                continue
            iterators.append((context, candidates))
            consumed += 1
            if checkpoint is not None:
                checkpoint()
            visit(context, item)
    finally:
        for _context, candidates in iterators:
            candidates.close()
    return consumed


class BoundedPluginMetadata(TypedDict):
    """Plugin metadata truncated to the backend storage contract."""

    source_identifier: str
    name: str
    version: str | None
    author: str | None


def bound_plugin_metadata(
    *,
    source_identifier: str,
    name: str,
    version: str | None,
    author: str | None,
) -> BoundedPluginMetadata | None:
    """Apply the shared storage-contract bounds to plugin metadata.

    The source identifier is the product identity and must not be silently
    truncated into a different identity, so an overlong one rejects the
    plugin (returns None). Display-oriented fields are truncated instead.
    """
    if len(source_identifier) > MAX_PLUGIN_SOURCE_IDENTIFIER_LENGTH:
        return None
    return {
        "source_identifier": source_identifier,
        "name": name[:MAX_PLUGIN_NAME_LENGTH],
        "version": (
            version[:MAX_PLUGIN_VERSION_LENGTH] if version is not None else None
        ),
        "author": author[:MAX_PLUGIN_AUTHOR_LENGTH] if author is not None else None,
    }
