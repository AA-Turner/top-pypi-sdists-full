"""Shared bounded POSIX symlink target identity resolution."""

from __future__ import annotations

import os
import stat
from collections import deque
from collections.abc import Callable, Collection
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from runlayer_cli.scan.scanner_primitives import MAX_PATH_COMPONENTS

MAX_IDENTITY_DIRECTORIES = 64
MAX_IDENTITY_ENTRIES_PER_DIRECTORY = 4096
MAX_IDENTITY_CANDIDATES = 4096
MAX_IDENTITY_CHAIN_LINKS = 64

IdentityLimit = Literal["directories", "entries_per_directory", "candidates"]


@dataclass(frozen=True)
class ResolvedSymlinkIdentity:
    """One regular final target and its optional executable identity."""

    target_path: Path
    executable_basename: str | None


class SymlinkIdentityScanBudget:
    """Shared directory, entry, and candidate governor for identity sweeps."""

    def __init__(
        self,
        *,
        on_limit: Callable[[IdentityLimit], None] | None = None,
    ) -> None:
        self._on_limit = on_limit
        self._seen_directories: set[str] = set()
        self._candidates = 0

    @property
    def directory_capacity_reached(self) -> bool:
        return len(self._seen_directories) >= MAX_IDENTITY_DIRECTORIES

    @property
    def candidate_capacity_reached(self) -> bool:
        return self._candidates >= MAX_IDENTITY_CANDIDATES

    def _limit(self, reason: IdentityLimit) -> None:
        if self._on_limit is not None:
            self._on_limit(reason)

    def claim_directory(self, key: str) -> bool:
        if key in self._seen_directories:
            return False
        if self.directory_capacity_reached:
            self._limit("directories")
            return False
        self._seen_directories.add(key)
        return True

    def claim_entry(self, *, directory_entries: int) -> bool:
        if directory_entries >= MAX_IDENTITY_ENTRIES_PER_DIRECTORY:
            self._limit("entries_per_directory")
            return False
        return True

    def claim_candidate(self) -> bool:
        if self.candidate_capacity_reached:
            self._limit("candidates")
            return False
        self._candidates += 1
        return True


def logical_path_key(path: Path) -> str:
    """Normalize a path without following attacker-controlled links."""
    return os.path.normcase(os.path.abspath(path))


def canonical_path_key(path: Path) -> str:
    """Normalize an existing directory after canonicalization."""
    return os.path.normcase(os.path.realpath(path))


def _checkpoint_allows(checkpoint: Callable[[], bool | None] | None) -> bool:
    return checkpoint is None or checkpoint() is not False


def _prepend_target(
    pending: deque[str],
    raw_target: Path,
    *,
    current: Path,
) -> Path:
    if raw_target.is_absolute():
        anchor = Path(raw_target.anchor)
        target_parts = raw_target.relative_to(anchor).parts
        current = anchor
    else:
        target_parts = raw_target.parts
    pending.extendleft(reversed(target_parts))
    return current


def resolve_posix_symlink_identity(
    link_path: Path,
    *,
    known_basenames: Collection[str],
    checkpoint: Callable[[], bool | None] | None = None,
) -> ResolvedSymlinkIdentity | None:
    """Resolve one POSIX symlink chain under explicit component/link caps."""
    absolute_link = Path(os.path.abspath(link_path))
    anchor = Path(absolute_link.anchor)
    pending = deque(absolute_link.relative_to(anchor).parts)
    current = anchor
    seen_links: set[str] = set()
    inspected_components = 0
    followed_links = 0

    while pending:
        if not _checkpoint_allows(checkpoint):
            return None
        inspected_components += 1
        if inspected_components > MAX_PATH_COMPONENTS:
            return None
        part = pending.popleft()
        if part in {"", os.curdir}:
            continue
        if part == os.pardir:
            current = current.parent
            continue

        candidate = current / part
        try:
            candidate_info = candidate.lstat()
        except OSError:
            return None
        if not stat.S_ISLNK(candidate_info.st_mode):
            current = candidate
            continue

        link_key = logical_path_key(candidate)
        if link_key in seen_links or followed_links >= MAX_IDENTITY_CHAIN_LINKS:
            return None
        seen_links.add(link_key)
        followed_links += 1
        try:
            raw_target = candidate.readlink()
        except (OSError, RuntimeError):
            return None
        if not _checkpoint_allows(checkpoint):
            return None
        current = _prepend_target(pending, raw_target, current=current)

    if followed_links == 0:
        return None
    try:
        target_info = current.lstat()
    except OSError:
        return None
    if not stat.S_ISREG(target_info.st_mode):
        return None
    basename = (
        current.name
        if current.name in known_basenames and os.access(current, os.X_OK)
        else None
    )
    return ResolvedSymlinkIdentity(
        target_path=current,
        executable_basename=basename,
    )
