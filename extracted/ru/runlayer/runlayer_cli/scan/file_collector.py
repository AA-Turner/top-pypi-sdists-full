"""Shared file-walk logic for collecting text files from artifact directories."""

from __future__ import annotations

import os
import stat
from collections import deque
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

import structlog

from runlayer_cli.scan.scanner_primitives import (
    SymlinkFollowPolicy,
    is_link_or_reparse,
    read_bounded,
)
from runlayer_cli.scan.skip_dirs import CONTENT_SKIP_DIRS
from runlayer_cli.scan.windows_users import is_windows_system_context

logger = structlog.get_logger(__name__)

MAX_SINGLE_FILE_BYTES = 1_048_576  # 1 MB
MAX_TOTAL_BYTES = 5_242_880  # 5 MB
MAX_FOLLOWED_SYMLINK_TARGETS = 64

# Minimal artifact-content skip set (canonical home: scan.skip_dirs). Kept
# narrow on purpose so a skill/plugin payload keeps its files.
SKIP_DIRS = set(CONTENT_SKIP_DIRS)


def _path_key(path: Path) -> str:
    return os.path.normcase(os.path.normpath(os.path.realpath(path)))


@dataclass
class CollectedFile:
    """A single text file collected from an artifact directory."""

    title: str
    content: str


@dataclass(frozen=True)
class _WalkRoot:
    actual_root: Path
    logical_prefix: PurePosixPath


class _FileCollector:
    def __init__(
        self,
        *,
        root: Path,
        supported_extensions: set[str],
        max_single: int,
        max_total: int,
        skip_dirs: set[str],
        windows_system_context: bool,
    ) -> None:
        self._root = root
        self._supported_extensions = supported_extensions
        self._max_single = max_single
        self._max_total = max_total
        self._skip_dirs = skip_dirs
        self._windows_system_context = windows_system_context
        self._files: list[CollectedFile] = []
        self._symlinks: list[str] = []
        self._symlink_paths_seen: set[str] = set()
        self._regular_paths_seen: set[str] = set()
        self._primary_directory_roots: list[str] = []
        self._followed_directory_roots: list[str] = []
        self._completed_directory_roots: list[str] = []
        self._pending: deque[_WalkRoot] = deque()
        self._oversized = False
        self._stop_current_root = False
        self._total_bytes = 0
        self._symlink_policy = SymlinkFollowPolicy(
            scan_areas=[],
            max_followed=MAX_FOLLOWED_SYMLINK_TARGETS,
            windows_system_context=windows_system_context,
        )

    def collect(self) -> tuple[list[CollectedFile], list[str], bool]:
        if self._windows_system_context and is_link_or_reparse(self._root):
            return self._files, self._symlinks, self._oversized
        try:
            actual_root = self._root.resolve(strict=True)
            root_mode = actual_root.stat().st_mode
        except (OSError, RuntimeError):
            return self._files, self._symlinks, self._oversized
        if not stat.S_ISDIR(root_mode):
            return self._files, self._symlinks, self._oversized

        self._primary_directory_roots.append(_path_key(actual_root))
        self._pending.append(
            _WalkRoot(actual_root=actual_root, logical_prefix=PurePosixPath())
        )
        while self._pending:
            walk_root = self._pending.popleft()
            if self._covered_by_completed_directory(walk_root.actual_root):
                continue
            self._walk_root(walk_root)
        return self._files, self._symlinks, self._oversized

    def _walk_root(self, walk_root: _WalkRoot) -> None:
        self._stop_current_root = False
        for dirpath, dirnames, filenames in os.walk(
            walk_root.actual_root,
            topdown=True,
            followlinks=False,
        ):
            if self._stop_current_root:
                break

            directory = Path(dirpath)
            try:
                relative_directory = directory.relative_to(walk_root.actual_root)
            except ValueError:
                continue
            logical_directory = walk_root.logical_prefix.joinpath(
                *relative_directory.parts
            )

            entries: list[tuple[str, Path, bool]] = []
            real_directories: list[str] = []
            for name in sorted(dirnames):
                path = directory / name
                if is_link_or_reparse(path):
                    entries.append((name, path, True))
                elif name not in self._skip_dirs:
                    real_directories.append(name)
            dirnames[:] = real_directories

            for name in filenames:
                path = directory / name
                entries.append((name, path, is_link_or_reparse(path)))

            for name, path, is_link in sorted(entries, key=lambda item: item[0]):
                logical_path = logical_directory / name
                if is_link:
                    self._surface_link(path, logical_path)
                else:
                    self._collect_regular_file(path, logical_path)
                if self._stop_current_root:
                    break
        if not self._stop_current_root:
            self._completed_directory_roots.append(_path_key(walk_root.actual_root))

    def _surface_link(self, link_path: Path, logical_path: PurePosixPath) -> None:
        reported_path = str(link_path)
        if reported_path not in self._symlink_paths_seen:
            self._symlink_paths_seen.add(reported_path)
            self._symlinks.append(reported_path)
        if link_path.name in self._skip_dirs:
            return
        if self._windows_system_context:
            return
        try:
            candidate = Path(os.path.realpath(link_path.resolve(strict=True)))
            candidate_mode = candidate.stat().st_mode
        except (OSError, RuntimeError):
            return
        access_mode = os.R_OK | (os.X_OK if stat.S_ISDIR(candidate_mode) else 0)
        if candidate.name in self._skip_dirs or not os.access(candidate, access_mode):
            return

        if self._contains_primary_directory(candidate):
            return
        covered_by_primary_root = self._covered_by_primary_directory(candidate)
        covered_by_followed_root = self._covered_by_followed_directory(candidate)
        if covered_by_primary_root:
            return
        if (
            not covered_by_followed_root
            and self._symlink_policy.inspect_target(candidate) is None
        ):
            return

        if stat.S_ISREG(candidate_mode):
            self._collect_regular_file(
                candidate,
                logical_path,
                followed_target=None if covered_by_followed_root else candidate,
            )
        # Scheduling a subtree is itself a follow, even if filtering finds no files.
        elif stat.S_ISDIR(candidate_mode):
            target_key = _path_key(candidate)
            if any(
                _path_key(pending.actual_root) == target_key
                for pending in self._pending
            ):
                return
            if covered_by_followed_root or self._symlink_policy.claim(candidate):
                if not covered_by_followed_root:
                    self._followed_directory_roots.append(target_key)
                self._pending.append(
                    _WalkRoot(actual_root=candidate, logical_prefix=logical_path)
                )

    def _covered_by_directory_roots(
        self,
        target: Path,
        root_keys: list[str],
    ) -> bool:
        target_key = _path_key(target)
        for root_key in root_keys:
            try:
                relative = os.path.relpath(target_key, root_key)
            except ValueError:
                continue
            if relative == os.curdir:
                return True
            if relative == os.pardir or relative.startswith(os.pardir + os.sep):
                continue
            # A skipped component means the parent walk will not reach this target.
            if not any(part in self._skip_dirs for part in Path(relative).parts):
                return True
        return False

    def _covered_by_primary_directory(self, target: Path) -> bool:
        return self._covered_by_directory_roots(
            target,
            self._primary_directory_roots,
        )

    def _contains_primary_directory(self, target: Path) -> bool:
        target_key = _path_key(target)
        for root_key in self._primary_directory_roots:
            try:
                relative = os.path.relpath(root_key, target_key)
            except ValueError:
                continue
            if relative == os.curdir:
                return True
            if relative != os.pardir and not relative.startswith(os.pardir + os.sep):
                return True
        return False

    def _covered_by_followed_directory(self, target: Path) -> bool:
        return self._covered_by_directory_roots(
            target,
            self._followed_directory_roots,
        )

    def _covered_by_completed_directory(self, target: Path) -> bool:
        return self._covered_by_directory_roots(
            target,
            self._completed_directory_roots,
        )

    def _collect_regular_file(
        self,
        read_path: Path,
        logical_path: PurePosixPath,
        *,
        followed_target: Path | None = None,
    ) -> None:
        if logical_path.suffix.lower() not in self._supported_extensions:
            return

        # Dedup attempts here because policy claims intentionally happen after reads.
        path_key = os.path.normcase(os.path.normpath(os.path.realpath(read_path)))
        if path_key in self._regular_paths_seen:
            return
        self._regular_paths_seen.add(path_key)
        if followed_target is None:
            self._symlink_policy.mark_visited(read_path)

        try:
            file_info = read_path.stat()
        except OSError:
            return
        if not stat.S_ISREG(file_info.st_mode):
            return
        if file_info.st_size > self._max_single:
            self._oversized = True
            return
        if self._total_bytes + file_info.st_size > self._max_total:
            self._oversized = True
            self._stop_current_root = True
            return

        raw = read_bounded(read_path, max_bytes=self._max_single)
        if raw is None:
            try:
                if read_path.stat().st_size > self._max_single:
                    self._oversized = True
            except OSError:
                pass
            return
        if self._total_bytes + len(raw) > self._max_total:
            self._oversized = True
            self._stop_current_root = True
            return
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            return
        # Claim file targets last so filtered or unreadable files consume no capacity.
        if followed_target is not None and not self._symlink_policy.claim(
            followed_target
        ):
            return

        self._total_bytes += len(raw)
        self._files.append(
            CollectedFile(title=logical_path.as_posix(), content=content)
        )


def collect_files(
    root: Path,
    supported_extensions: set[str],
    *,
    max_single: int | None = None,
    max_total: int | None = None,
    skip_dirs: set[str] | None = None,
    windows_system_context: bool | None = None,
) -> tuple[list[CollectedFile], list[str], bool]:
    """Walk *root* and collect text files matching *supported_extensions*.

    Returns:
        (files, symlinks_found, oversized)
    """
    if max_single is None:
        max_single = MAX_SINGLE_FILE_BYTES
    if max_total is None:
        max_total = MAX_TOTAL_BYTES
    if skip_dirs is None:
        skip_dirs = SKIP_DIRS
    if windows_system_context is None:
        windows_system_context = is_windows_system_context()
    collector = _FileCollector(
        root=root,
        supported_extensions=supported_extensions,
        max_single=max_single,
        max_total=max_total,
        skip_dirs=skip_dirs,
        windows_system_context=windows_system_context,
    )
    return collector.collect()
