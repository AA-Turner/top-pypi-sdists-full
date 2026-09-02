"""Bounded, in-memory walking of Docker ``cp`` tar streams."""

from __future__ import annotations

import io
import posixpath
import subprocess
import tarfile
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import IO, Callable

import structlog

from runlayer_cli.scan.containers.docker_cli import (
    _kill_and_reap,
    _kill_process,
)
from runlayer_cli.scan.containers.inspect_parse import _container_path_within
from runlayer_cli.scan.file_collector import (
    MAX_SINGLE_FILE_BYTES,
    MAX_TOTAL_BYTES,
)
from runlayer_cli.scan.skip_dirs import CONTENT_SKIP_DIRS

MAX_DOCKER_TREE_STREAM_BYTES = 256 * 1024 * 1024
MAX_DOCKER_TREE_MATCHED_FILES = 128
# Sparse identity files admitted from skipped dependency trees must not lose
# their slots to broad content collection earlier in archive order.
MAX_DOCKER_TREE_PRIORITY_FILES = 64

logger = structlog.get_logger(__name__)


@dataclass
class _TarWalkResult:
    files: dict[str, bytes] = field(default_factory=dict)
    truncated: bool = False
    stream_bytes: int = 0


class _TarWalkLimitExceeded(Exception):
    pass


class _BoundedTarStream(io.RawIOBase):
    def __init__(
        self,
        stream: IO[bytes],
        *,
        deadline: float,
        max_stream_bytes: int,
    ) -> None:
        self._stream = stream
        self._deadline = deadline
        self._max_stream_bytes = max_stream_bytes
        self.bytes_read = 0

    def readable(self) -> bool:
        return True

    def read(self, size: int = -1) -> bytes:
        if time.monotonic() >= self._deadline:
            raise _TarWalkLimitExceeded
        remaining = self._max_stream_bytes - self.bytes_read
        if remaining <= 0:
            raise _TarWalkLimitExceeded
        read_size = remaining if size < 0 else min(size, remaining)
        chunk = self._stream.read(read_size)
        if not isinstance(chunk, bytes):
            raise OSError
        self.bytes_read += len(chunk)
        if (
            self.bytes_read > self._max_stream_bytes
            or time.monotonic() >= self._deadline
        ):
            raise _TarWalkLimitExceeded
        return chunk


def _tar_member_path(member_name: str, root_path: str) -> str | None:
    root_path = posixpath.normpath(root_path)
    if not root_path.startswith("/") or member_name.startswith("/"):
        return None
    while member_name.startswith("./"):
        member_name = member_name[2:]
    raw_parts = member_name.split("/")
    if ".." in raw_parts:
        return None
    normalized = posixpath.normpath(member_name)
    if normalized in {"", ".", ".."} or normalized.startswith("../"):
        return None
    relative_parts = normalized.split("/")
    root_name = posixpath.basename(root_path)
    if root_name and relative_parts[0] == root_name:
        relative_parts = relative_parts[1:]
    path = posixpath.normpath(posixpath.join(root_path, *relative_parts))
    if not _container_path_within(path, root_path):
        return None
    return path


def _path_has_skipped_directory(path: str, root_path: str) -> bool:
    relative = posixpath.relpath(path, root_path)
    return any(part in CONTENT_SKIP_DIRS for part in relative.split("/")[:-1])


def _walk_tar_stream(
    stream: IO[bytes],
    *,
    root_path: str,
    wanted_file: Callable[[str], bool],
    allow_file_in_skipped_directory: Callable[[str], bool] | None = None,
    deadline: float,
    max_stream_bytes: int,
    max_matched_files: int,
) -> _TarWalkResult:
    """Collect only bounded regular-file matches from a streaming tar."""
    result = _TarWalkResult()
    matched_files = 0
    priority_files = 0
    matched_bytes = 0
    normal_paths: deque[str] = deque()
    bounded_stream = _BoundedTarStream(
        stream,
        deadline=deadline,
        max_stream_bytes=max_stream_bytes,
    )
    try:
        with tarfile.open(fileobj=bounded_stream, mode="r|") as archive:
            for member in archive:
                if time.monotonic() >= deadline:
                    raise _TarWalkLimitExceeded
                path = _tar_member_path(member.name, root_path)
                allowed_skipped = (
                    allow_file_in_skipped_directory is not None
                    and path is not None
                    and allow_file_in_skipped_directory(path)
                )
                if (
                    path is None
                    or not member.isfile()
                    or (
                        _path_has_skipped_directory(path, root_path)
                        and not allowed_skipped
                    )
                    or not wanted_file(path)
                ):
                    continue
                if path in result.files:
                    result.truncated = True
                    continue
                if allowed_skipped:
                    priority_files += 1
                    if priority_files > MAX_DOCKER_TREE_PRIORITY_FILES:
                        result.truncated = True
                        continue
                else:
                    matched_files += 1
                    if matched_files > max_matched_files:
                        result.truncated = True
                        continue
                if member.size < 0 or member.size > MAX_SINGLE_FILE_BYTES:
                    continue
                if allowed_skipped:
                    while (
                        matched_bytes + member.size > MAX_TOTAL_BYTES and normal_paths
                    ):
                        removed = result.files.pop(normal_paths.popleft())
                        matched_bytes -= len(removed)
                        result.truncated = True
                if matched_bytes + member.size > MAX_TOTAL_BYTES:
                    result.truncated = True
                    continue
                extracted = archive.extractfile(member)
                if extracted is None:
                    continue
                with extracted:
                    content = extracted.read(member.size + 1)
                if time.monotonic() >= deadline:
                    raise _TarWalkLimitExceeded
                if len(content) != member.size:
                    result.truncated = True
                    break
                matched_bytes += len(content)
                result.files[path] = content
                if not allowed_skipped:
                    normal_paths.append(path)
    except (tarfile.TarError, OSError, _TarWalkLimitExceeded):
        result.truncated = True
    except Exception as exc:
        logger.warning(
            "Unexpected error walking container tar stream",
            error_type=type(exc).__name__,
        )
        result.truncated = True
    result.stream_bytes = bounded_stream.bytes_read
    return result


def _copy_container_tree(
    *,
    docker: str,
    container_id: str,
    root_path: str,
    wanted_file: Callable[[str], bool],
    allow_file_in_skipped_directory: Callable[[str], bool] | None = None,
    deadline: float,
    max_stream_bytes: int = MAX_DOCKER_TREE_STREAM_BYTES,
    max_matched_files: int = MAX_DOCKER_TREE_MATCHED_FILES,
) -> _TarWalkResult:
    """Stream one container tree through the bounded tar walker."""
    if time.monotonic() >= deadline:
        return _TarWalkResult(truncated=True)
    try:
        process = subprocess.Popen(
            [docker, "cp", f"{container_id}:{root_path}", "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return _TarWalkResult()
    if process.stdout is None:
        _kill_and_reap(process)
        return _TarWalkResult()

    timed_out = threading.Event()

    def _expire() -> None:
        timed_out.set()
        _kill_process(process)

    watchdog = threading.Timer(max(deadline - time.monotonic(), 0), _expire)
    watchdog.daemon = True
    watchdog.start()
    result = _walk_tar_stream(
        process.stdout,
        root_path=root_path,
        wanted_file=wanted_file,
        allow_file_in_skipped_directory=allow_file_in_skipped_directory,
        deadline=deadline,
        max_stream_bytes=max_stream_bytes,
        max_matched_files=max_matched_files,
    )
    watchdog.cancel()
    watchdog.join(timeout=0.1)
    try:
        process.stdout.close()
    except OSError:
        pass

    if result.truncated or timed_out.is_set():
        result.truncated = True
        _kill_and_reap(process)
        return result

    remaining = deadline - time.monotonic()
    if remaining <= 0:
        result.truncated = True
        _kill_and_reap(process)
        return result
    try:
        process.wait(timeout=remaining)
    except subprocess.TimeoutExpired:
        result.truncated = True
        _kill_and_reap(process)
        return result
    except OSError:
        result.files.clear()
        _kill_and_reap(process)
        return result
    if process.returncode != 0:
        result.files.clear()
    return result


def _extract_copied_file(archive: bytes) -> bytes | None:
    """Read one regular file from a bounded ``docker cp`` tar stream."""
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as copied:
            for index, member in enumerate(copied):
                if index >= 8:
                    return None
                if not member.isfile() or member.size > MAX_SINGLE_FILE_BYTES:
                    continue
                extracted = copied.extractfile(member)
                if extracted is None:
                    continue
                content = extracted.read(MAX_SINGLE_FILE_BYTES + 1)
                if len(content) <= MAX_SINGLE_FILE_BYTES:
                    return content
    except (OSError, tarfile.TarError):
        return None
    return None
