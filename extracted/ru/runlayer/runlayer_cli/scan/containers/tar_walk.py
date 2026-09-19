"""Bounded, in-memory walking of Docker ``cp`` tar streams."""

from __future__ import annotations

import io
import os
import posixpath
import subprocess
import tarfile
import tempfile
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import IO, Callable, Literal

import structlog

from runlayer_cli.scan.containers.docker_cli import (
    _docker_copy_path_absent,
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
_TRUNCATED_COPY_REAP_GRACE_SECONDS = 0.05
_MAX_DOCKER_COPY_STDERR_BYTES = 8 * 1024

logger = structlog.get_logger(__name__)


@dataclass
class _TarWalkResult:
    files: dict[str, bytes] = field(default_factory=dict)
    truncated: bool = False
    stream_bytes: int = 0
    failure_reason: str | None = None
    stream_aborted: bool = False


@dataclass(frozen=True)
class _CopyProcessResult:
    returncode: int | None = None
    failure: Literal["timeout", "wait"] | None = None


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
                    result.truncated = True
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
                    result.truncated = True
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
        result.failure_reason = "container_artifact_tar_walk_failed"
        result.stream_aborted = True
    except Exception as exc:
        logger.warning(
            "Unexpected error walking container tar stream",
            error_type=type(exc).__name__,
        )
        result.truncated = True
        result.failure_reason = "container_artifact_tar_walk_failed"
        result.stream_aborted = True
    result.stream_bytes = bounded_stream.bytes_read
    return result


def _reap_copy_process(
    process: subprocess.Popen[bytes],
    *,
    deadline: float,
    walked_truncated: bool,
    expired: bool,
) -> _CopyProcessResult:
    """Wait once within budget, then terminate and reap incomplete producers."""
    if expired:
        _kill_and_reap(process)
        return _CopyProcessResult(failure="timeout")

    remaining = deadline - time.monotonic()
    if remaining <= 0:
        _kill_and_reap(process)
        return _CopyProcessResult(failure="timeout")
    wait_timeout = (
        min(remaining, _TRUNCATED_COPY_REAP_GRACE_SECONDS)
        if walked_truncated
        else remaining
    )
    try:
        return _CopyProcessResult(returncode=process.wait(timeout=wait_timeout))
    except subprocess.TimeoutExpired:
        _kill_and_reap(process)
        return _CopyProcessResult(failure="timeout")
    except OSError:
        _kill_and_reap(process)
        return _CopyProcessResult(failure="wait")


def _classify_copy_outcome(
    walked: _TarWalkResult,
    process_result: _CopyProcessResult,
    *,
    stderr: bytes,
) -> _TarWalkResult:
    """Purely combine tar-walk evidence with the producer's terminal state."""
    if process_result.failure == "wait":
        return _TarWalkResult(
            files=dict(walked.files),
            truncated=walked.truncated,
            stream_bytes=walked.stream_bytes,
            failure_reason="container_artifact_copy_wait_failed",
            stream_aborted=walked.stream_aborted,
        )
    if process_result.failure == "timeout":
        return _TarWalkResult(
            files=dict(walked.files),
            truncated=True,
            stream_bytes=walked.stream_bytes,
            failure_reason=walked.failure_reason,
            stream_aborted=walked.stream_aborted,
        )
    if process_result.returncode in {None, 0}:
        return walked

    absent = _docker_copy_path_absent(stderr)
    if absent and not walked.files:
        return _TarWalkResult(stream_bytes=walked.stream_bytes)
    if walked.truncated and (walked.files or not walked.stream_aborted):
        if not (absent and walked.failure_reason is None):
            return walked
    if walked.truncated and not walked.files:
        return _TarWalkResult(
            stream_bytes=walked.stream_bytes,
            failure_reason="container_artifact_copy_nonzero",
        )
    return _TarWalkResult(
        files=dict(walked.files),
        truncated=True,
        stream_bytes=walked.stream_bytes,
        failure_reason="container_artifact_copy_nonzero",
        stream_aborted=walked.stream_aborted,
    )


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
    with tempfile.TemporaryFile() as stderr_file:
        try:
            process = subprocess.Popen(
                [docker, "cp", f"{container_id}:{root_path}", "-"],
                stdout=subprocess.PIPE,
                stderr=stderr_file,
                start_new_session=os.name != "nt",
            )
        except OSError:
            return _TarWalkResult(failure_reason="container_artifact_copy_spawn_failed")
        if process.stdout is None:
            _kill_and_reap(process)
            return _TarWalkResult(
                failure_reason="container_artifact_copy_stdout_missing"
            )

        timed_out = threading.Event()

        def _expire() -> None:
            timed_out.set()
            _kill_process(process)

        watchdog = threading.Timer(max(deadline - time.monotonic(), 0), _expire)
        watchdog.daemon = True
        watchdog.start()
        try:
            try:
                result = _walk_tar_stream(
                    process.stdout,
                    root_path=root_path,
                    wanted_file=wanted_file,
                    allow_file_in_skipped_directory=allow_file_in_skipped_directory,
                    deadline=deadline,
                    max_stream_bytes=max_stream_bytes,
                    max_matched_files=max_matched_files,
                )
            finally:
                watchdog.cancel()
                watchdog.join(timeout=0.1)
                try:
                    process.stdout.close()
                except OSError:
                    pass

            process_result = _reap_copy_process(
                process,
                deadline=deadline,
                walked_truncated=result.truncated,
                expired=timed_out.is_set(),
            )
        except BaseException:
            if process.poll() is None:
                _kill_and_reap(process)
            raise
        stderr_file.seek(0)
        stderr = stderr_file.read(_MAX_DOCKER_COPY_STDERR_BYTES)
        return _classify_copy_outcome(result, process_result, stderr=stderr)


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
