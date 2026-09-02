"""Bounded, read-only artifact access through ``/proc/<pid>/root``."""

from __future__ import annotations

import io
import os
import posixpath
import stat
import tarfile
import time
from collections import deque
from pathlib import Path
from typing import Callable

import structlog

from runlayer_cli.scan.containers.inspect_parse import _container_path_within
from runlayer_cli.scan.containers.tar_walk import (
    MAX_DOCKER_TREE_MATCHED_FILES,
    MAX_DOCKER_TREE_PRIORITY_FILES,
    MAX_DOCKER_TREE_STREAM_BYTES,
    _path_has_skipped_directory,
    _TarWalkResult,
)
from runlayer_cli.scan.file_collector import (
    MAX_SINGLE_FILE_BYTES,
    MAX_TOTAL_BYTES,
)
from runlayer_cli.scan.skip_dirs import CONTENT_SKIP_DIRS

_READ_CHUNK_BYTES = 64 * 1024
_MAX_CGROUP_BYTES = 64 * 1024
# crictl reports full 64-hex container ids; require enough of one to make the
# cgroup substring match unambiguous before trusting pid->container identity.
_MIN_CONTAINER_ID_MATCH_CHARS = 8
# Per-directory breadth cap. A live (possibly adversarial) container rootfs can
# list an unbounded number of entries in one directory; os.walk materializes
# them, then _walk_proc_tree sorts and lstats (is_symlink) each subdir with no
# interleaved deadline check, so one pathological fanout could burn the whole
# wall-clock budget inside a single os.walk step. Bail out (mark truncated)
# before that work rather than after it. tar_walk needs no analogue: its
# byte-stream cap already bounds total work.
MAX_PROC_TREE_DIR_ENTRIES = 50_000

logger = structlog.get_logger(__name__)


def _read_proc_cgroup(proc_root: Path, pid: int) -> bytes | None:
    flags = os.O_RDONLY
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor: int | None = None
    try:
        descriptor = os.open(proc_root / str(pid) / "cgroup", flags)
        return os.read(descriptor, _MAX_CGROUP_BYTES)
    except (FileNotFoundError, ProcessLookupError, PermissionError, OSError):
        return None
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass


def _pid_matches_container(
    *,
    proc_root: Path,
    pid: int,
    container_id: str,
) -> bool:
    """Whether the live pid still belongs to the expected container.

    Guards PID reuse: between inspect and these reads a container can exit and
    the kernel can recycle its pid to an unrelated (possibly host) process,
    which would misattribute that process's rootfs to a container that no
    longer exists. Every process in a k3s/containerd container carries the full
    container id in its cgroup path (``.../<id>`` for the cgroupfs driver,
    ``.../cri-containerd-<id>.scope`` for systemd), and that cgroup is torn down
    on exit, so a recycled pid owned by anything else will not carry the id.
    Fail-closed: an unreadable/absent cgroup (the process already exited) skips
    the read rather than risk misattribution.
    """
    if pid <= 0 or len(container_id) < _MIN_CONTAINER_ID_MATCH_CHARS:
        return False
    cgroup = _read_proc_cgroup(proc_root, pid)
    if cgroup is None:
        return False
    return container_id.encode("utf-8", "surrogateescape") in cgroup


def _procfs_container_path(
    *,
    proc_root: Path,
    pid: int,
    container_path: str,
) -> Path | None:
    if (
        pid <= 0
        or not container_path.startswith("/")
        or "\x00" in container_path
        or ".." in container_path.split("/")
    ):
        return None
    normalized = posixpath.normpath(container_path)
    if not _container_path_within(normalized, "/"):
        return None
    return proc_root / str(pid) / "root" / normalized.lstrip("/")


def _read_proc_file(
    *,
    proc_root: Path,
    pid: int,
    path: str,
    deadline: float,
    max_bytes: int = MAX_SINGLE_FILE_BYTES,
    container_id: str | None = None,
) -> bytes | None:
    """Read one regular file without following its final symlink.

    When ``container_id`` is supplied, the pid is re-validated against the
    container's cgroup immediately before opening, so a pid recycled since
    inspect never contributes another process's file content.
    """
    proc_path = _procfs_container_path(
        proc_root=proc_root,
        pid=pid,
        container_path=path,
    )
    if proc_path is None or time.monotonic() >= deadline:
        return None
    if container_id is not None and not _pid_matches_container(
        proc_root=proc_root,
        pid=pid,
        container_id=container_id,
    ):
        return None

    flags = os.O_RDONLY
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    flags |= getattr(os, "O_NONBLOCK", 0)
    descriptor: int | None = None
    try:
        descriptor = os.open(proc_path, flags)
        file_stat = os.fstat(descriptor)
        if not stat.S_ISREG(file_stat.st_mode) or file_stat.st_size > max_bytes:
            return None

        content = bytearray()
        while True:
            if time.monotonic() >= deadline:
                return None
            chunk = os.read(
                descriptor,
                min(_READ_CHUNK_BYTES, max_bytes + 1 - len(content)),
            )
            if not chunk:
                return bytes(content)
            content.extend(chunk)
            if len(content) > max_bytes:
                return None
    except (FileNotFoundError, ProcessLookupError, PermissionError, OSError):
        return None
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass


def _copy_proc_file_archive(
    *,
    proc_root: Path,
    pid: int,
    path: str,
    deadline: float,
    container_id: str | None = None,
) -> bytes | None:
    """Wrap one procfs-backed file for the existing tar extraction contract."""
    content = _read_proc_file(
        proc_root=proc_root,
        pid=pid,
        path=path,
        deadline=deadline,
        container_id=container_id,
    )
    if content is None or time.monotonic() >= deadline:
        return None

    archive = io.BytesIO()
    try:
        with tarfile.open(fileobj=archive, mode="w") as copied:
            info = tarfile.TarInfo(name=posixpath.basename(path) or "artifact")
            info.size = len(content)
            copied.addfile(info, io.BytesIO(content))
    except (OSError, tarfile.TarError):
        return None
    return archive.getvalue()


def _walk_proc_tree(
    *,
    proc_root: Path,
    pid: int,
    root_path: str,
    wanted_file: Callable[[str], bool],
    allow_file_in_skipped_directory: Callable[[str], bool] | None = None,
    deadline: float,
    max_stream_bytes: int = MAX_DOCKER_TREE_STREAM_BYTES,
    max_matched_files: int = MAX_DOCKER_TREE_MATCHED_FILES,
    max_single_file_bytes: int = MAX_SINGLE_FILE_BYTES,
    max_total_bytes: int = MAX_TOTAL_BYTES,
    max_dir_entries: int = MAX_PROC_TREE_DIR_ENTRIES,
    container_id: str | None = None,
) -> _TarWalkResult:
    """Collect bounded regular-file matches from a container mount namespace.

    When ``container_id`` is supplied, the pid is validated against the
    container's cgroup before traversal and again before each matched-file read,
    so a pid recycled since inspect cannot have its rootfs walked or attributed.
    """
    result = _TarWalkResult()
    normalized_root = posixpath.normpath(root_path)
    proc_path = _procfs_container_path(
        proc_root=proc_root,
        pid=pid,
        container_path=normalized_root,
    )
    if proc_path is None:
        return result
    if container_id is not None and not _pid_matches_container(
        proc_root=proc_root,
        pid=pid,
        container_id=container_id,
    ):
        return result
    if time.monotonic() >= deadline:
        result.truncated = True
        return result
    try:
        root_stat = os.stat(proc_path)
    except (FileNotFoundError, ProcessLookupError, PermissionError, OSError):
        return result
    if not stat.S_ISDIR(root_stat.st_mode):
        return result

    walk_failed = False

    def _onerror(_error: OSError) -> None:
        nonlocal walk_failed
        walk_failed = True

    matched_files = 0
    priority_files = 0
    matched_bytes = 0
    normal_paths: deque[str] = deque()
    quota_truncated = False
    try:
        for directory, directory_names, file_names in os.walk(
            proc_path,
            topdown=True,
            onerror=_onerror,
            followlinks=False,
        ):
            if time.monotonic() >= deadline:
                result.truncated = True
                break
            # Enforce the breadth cap before the sort + per-subdir is_symlink()
            # lstat storm below, which otherwise run unbounded between this
            # deadline check and the per-file one. len() is O(1) on the lists
            # os.walk already materialized, so an over-cap directory costs no
            # per-entry work; we stop the walk and report truncation.
            if len(directory_names) + len(file_names) > max_dir_entries:
                result.truncated = True
                break

            directory_names.sort()
            directory_names[:] = [
                name
                for name in directory_names
                if not (Path(directory) / name).is_symlink()
                and (
                    allow_file_in_skipped_directory is not None
                    or name not in CONTENT_SKIP_DIRS
                )
            ]
            for filename in sorted(file_names):
                if time.monotonic() >= deadline:
                    result.truncated = True
                    break
                host_path = Path(directory) / filename
                relative = host_path.relative_to(proc_path)
                container_path = posixpath.normpath(
                    posixpath.join(normalized_root, *relative.parts)
                )
                if not _container_path_within(container_path, normalized_root):
                    continue
                allowed_skipped = (
                    allow_file_in_skipped_directory is not None
                    and allow_file_in_skipped_directory(container_path)
                )
                if (
                    _path_has_skipped_directory(container_path, normalized_root)
                    and not allowed_skipped
                ):
                    continue
                if not wanted_file(container_path):
                    continue
                if container_path in result.files:
                    quota_truncated = True
                    continue

                try:
                    file_stat = os.lstat(host_path)
                except (
                    FileNotFoundError,
                    ProcessLookupError,
                    PermissionError,
                    OSError,
                ):
                    result.truncated = True
                    continue
                # Skip non-regular entries (symlinks, sockets, ...) before they
                # consume the matched-file cap, matching tar_walk._walk_tar_stream.
                if not stat.S_ISREG(file_stat.st_mode):
                    continue

                if allowed_skipped:
                    priority_files += 1
                    if priority_files > MAX_DOCKER_TREE_PRIORITY_FILES:
                        quota_truncated = True
                        continue
                else:
                    matched_files += 1
                    if matched_files > max_matched_files:
                        quota_truncated = True
                        continue
                if file_stat.st_size > max_single_file_bytes:
                    continue
                remaining_stream_bytes = max_stream_bytes - result.stream_bytes
                if remaining_stream_bytes <= 0:
                    result.truncated = True
                    break
                if file_stat.st_size > remaining_stream_bytes:
                    result.stream_bytes = max_stream_bytes
                    result.truncated = True
                    break
                content = _read_proc_file(
                    proc_root=proc_root,
                    pid=pid,
                    path=container_path,
                    deadline=deadline,
                    max_bytes=min(max_single_file_bytes, remaining_stream_bytes),
                    container_id=container_id,
                )
                if content is None:
                    result.truncated = True
                    continue
                result.stream_bytes += len(content)
                if allowed_skipped:
                    while (
                        matched_bytes + len(content) > max_total_bytes and normal_paths
                    ):
                        removed = result.files.pop(normal_paths.popleft())
                        matched_bytes -= len(removed)
                        quota_truncated = True
                if matched_bytes + len(content) > max_total_bytes:
                    quota_truncated = True
                    continue
                matched_bytes += len(content)
                result.files[container_path] = content
                if not allowed_skipped:
                    normal_paths.append(container_path)
            if result.truncated:
                break
    except (
        FileNotFoundError,
        ProcessLookupError,
        PermissionError,
        OSError,
        ValueError,
    ):
        result.truncated = True
    except Exception as exc:
        logger.warning(
            "Unexpected error walking container proc tree",
            error_type=type(exc).__name__,
        )
        result.truncated = True
    if walk_failed:
        result.truncated = True
    if quota_truncated:
        result.truncated = True
    return result
