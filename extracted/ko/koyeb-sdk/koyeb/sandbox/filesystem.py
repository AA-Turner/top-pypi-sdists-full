# coding: utf-8

"""
Filesystem operations for Koyeb Sandbox instances
Using SandboxClient HTTP API
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import os
import shlex
import shutil
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    BinaryIO,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from .executor_client import AsyncSandboxClient, SandboxClient
from .sync import (
    SYNC_BATCH_BYTES,
    SyncDiff,
    build_archive,
    clean_path,
    diff,
    extract_archive,
    hash_candidates,
    join_local,
    open_nofollow,
    path_excluded,
    plan_batches,
    prune_descendants,
    relative_remote,
    remote_join,
    walk_local,
)
from .errors import (
    SandboxError,
    SandboxRequestError,
    SandboxServiceError,
    SandboxTimeoutError,
)

if TYPE_CHECKING:
    from .exec import AsyncSandboxExecutor, SandboxExecutor
    from .sandbox import Sandbox


ERROR_MESSAGES = {
    "NO_SUCH_FILE": ["No such file", "not found", "No such file or directory"],
    "FILE_EXISTS": ["exists", "already exists"],
    "DIR_NOT_EMPTY": ["not empty", "Directory not empty"],
}


def check_error_message(error_msg: str, error_type: str) -> bool:
    """
    Check if an error message matches a specific error type.
    Uses case-insensitive matching against known error patterns.

    Args:
        error_msg: The error message to check
        error_type: The type of error to check for (key in ERROR_MESSAGES)

    Returns:
        True if error message matches the error type
    """
    if error_type not in ERROR_MESSAGES:
        return False

    error_msg_lower = error_msg.lower()
    patterns = ERROR_MESSAGES[error_type]
    return any(pattern.lower() in error_msg_lower for pattern in patterns)


def escape_shell_arg(arg: str) -> str:
    """
    Escape a shell argument for safe use in shell commands.

    Args:
        arg: The argument to escape

    Returns:
        Properly escaped shell argument
    """
    return shlex.quote(arg)


class SandboxFilesystemError(SandboxError):
    """Base exception for filesystem operations"""


class SandboxFileNotFoundError(SandboxFilesystemError):
    """Raised when file or directory not found"""


class SandboxFileExistsError(SandboxFilesystemError):
    """Raised when file already exists"""


def _executor_error(
    error_msg: str,
    what: str,
    not_found_msg: Optional[str] = None,
    exists_msg: Optional[str] = None,
    not_empty_msg: Optional[str] = None,
) -> SandboxFilesystemError:
    """The one place executor error strings classify into the SDK taxonomy.

    Typed subclasses map only where the operation makes sense; message
    text stays the historical wording.
    """
    if not_found_msg and check_error_message(error_msg, "NO_SUCH_FILE"):
        return SandboxFileNotFoundError(not_found_msg)
    if exists_msg and check_error_message(error_msg, "FILE_EXISTS"):
        return SandboxFileExistsError(exists_msg)
    if not_empty_msg and check_error_message(error_msg, "DIR_NOT_EMPTY"):
        return SandboxFilesystemError(not_empty_msg)
    return SandboxFilesystemError(f"Failed to {what}: {error_msg}")


def _put_body(
    content: Union[str, bytes, BinaryIO, Iterable[bytes]], encoding: str
) -> Union[bytes, BinaryIO, Iterable[bytes]]:
    """Content to send on the streamed /files routes: real bytes on disk.

    encoding="base64" is a transport detail: the content is base64 text and
    the decoded bytes land on disk — the documented behavior change vs the
    legacy routes, which wrote the base64 text itself.
    """
    if isinstance(content, str):
        if encoding == "base64":
            return base64.b64decode(content)
        return content.encode(encoding)
    if isinstance(content, bytes) and encoding == "base64":
        return base64.b64decode(content)
    return content


def _read_content(raw: bytes, encoding: Optional[str]) -> Union[str, bytes]:
    """Interpret raw file bytes per the requested encoding (streamed routes)."""
    if encoding is None:
        return raw
    if encoding == "base64":
        return base64.b64encode(raw).decode("ascii")
    return raw.decode(encoding)


def _files_error(
    e: SandboxRequestError, what: str, path: str
) -> SandboxFilesystemError:
    """A streamed-route status error classified into the filesystem taxonomy.

    The /files routes answer with real status codes: the code is the
    contract, the JSON body's error text only adds detail.
    """
    msg = ""
    try:
        msg = json.loads(e.body).get("error", "") if e.body else ""
    except (AttributeError, ValueError):
        pass
    if e.status_code == 404:
        return SandboxFileNotFoundError(f"File not found: {path}")
    if e.status_code == 409:
        return SandboxFileExistsError(msg or f"Conflict at: {path}")
    detail = msg or (e.body if e.body else f"HTTP {e.status_code}")
    return SandboxFilesystemError(f"Failed to {what}: {detail}")


@contextmanager
def _translating_files_errors(what: str, path: str):
    """Translate streamed-route failures once, for every filesystem operation.

    Real status codes classify through _files_error; anything else wraps as
    "Failed to <what>" — the filesystem taxonomy is what callers catch.
    """
    try:
        yield
    except SandboxServiceError:
        raise
    except SandboxRequestError as e:
        raise _files_error(e, what, path) from e
    except SandboxFilesystemError:
        raise
    except Exception as e:
        raise SandboxFilesystemError(f"Failed to {what}: {str(e)}") from e


class _ProgressReporter:
    """progress(done, total) at most every 100 ms, plus a guaranteed final call."""

    def __init__(self, progress: Optional[Callable[[int, int], None]], total: int):
        self._progress = progress
        self._total = total
        self._last_time = 0.0
        self._last_done = None

    def update(self, done: int) -> None:
        if self._progress is None:
            return
        now = time.monotonic()
        if now - self._last_time >= 0.1:
            self._progress(done, self._total)
            self._last_time = now
            self._last_done = done

    def finish(self, done: int) -> None:
        if self._progress is not None and done != self._last_done:
            self._progress(done, self._total)


def _file_sha256(path: str) -> str:
    """sha256 of a local file, constant memory.

    A first pass before the streamed upload: the digest travels in the
    X-Content-SHA256 header, which precedes the body on the wire.
    """
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _progress_chunks(
    stream, reporter: _ProgressReporter, chunk_size: int = 65536
) -> Iterator[bytes]:
    """Read a binary stream in chunks, reporting progress as they go."""
    done = 0
    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        done += len(chunk)
        reporter.update(done)
        yield chunk
    reporter.finish(done)


# Multipart uploads: a file larger than one request's budget goes up as
# offset-addressed parts. The defaults follow the platform contract: 50 MiB
# parts (the executor caps at max_part_size), 4 in flight — memory holds at
# most part_size * concurrency.
UPLOAD_PART_SIZE = 50 * 1024 * 1024
UPLOAD_CONCURRENCY = 4

# A part that times out is split in half rather than failed: a smaller part
# needs less time on the wire. Below twice this floor a split cannot help —
# the connection is stalling, not slow.
_MIN_SPLIT_SIZE = 1024 * 1024

# The executor's sessions live in memory: a restart or the 1 h idle expiry
# loses them, and a 404 from a part or complete means starting over.
_LOST_SESSION_MESSAGE = (
    "Upload session was lost — the executor restarted or the session "
    "expired; restart the upload"
)


def _part_plan(start: int, end: int, part_size: int) -> List[Tuple[int, int]]:
    """(offset, length) parts covering [start, end) in part_size slices."""
    return [(o, min(part_size, end - o)) for o in range(start, end, part_size)]


def _read_part_with_digest(path: str, offset: int, length: int) -> Tuple[bytes, str]:
    """A part's bytes and digest, read from disk at its offset.

    Read per attempt — no part bytes are buffered between retries, so
    memory holds at most one part per worker.
    """
    with open(path, "rb") as f:
        f.seek(offset)
        data = f.read(length)
    return data, hashlib.sha256(data).hexdigest()


def _missing_ranges_from_409(body: Optional[str]) -> Optional[List[Tuple[int, int]]]:
    """The complete-409 body's missing spans, as (start, end) tuples.

    None means the body carried no usable ranges: the resume signal is
    absent and the failure is the caller's to report.
    """
    try:
        ranges = json.loads(body or "").get("ranges")
        if not isinstance(ranges, list) or not ranges:
            return None
        spans = []
        for r in ranges:
            start, end = r["start"], r["end"]
            if not isinstance(start, int) or not isinstance(end, int):
                return None
            if start < 0 or end <= start:
                return None
            spans.append((start, end))
        return spans
    except (AttributeError, KeyError, TypeError, ValueError):
        return None


def _split_worthy(e: BaseException) -> bool:
    """Whether a failed part should be retried as smaller halves.

    The transport already retries transient network errors; what it never
    retries is a fired timeout — the idle bound (SandboxTimeoutError) or
    Cloudflare's origin cap (524, surfaced as SandboxServiceError after
    the transport's own retries). Those are the fs layer's to split: a
    smaller part needs less time on the wire.
    """
    if isinstance(e, SandboxTimeoutError):
        return True
    return isinstance(e, SandboxServiceError) and e.status_code == 524


class _PartProgress:
    """Byte counter across concurrent parts: progress(done, total) as they land."""

    def __init__(self, progress: Optional[Callable[[int, int], None]], total: int):
        self._reporter = _ProgressReporter(progress, total)
        self._total = total
        self._done = 0
        self._lock = threading.Lock()

    def add(self, n: int) -> None:
        with self._lock:
            # A 409-fill re-sends already-counted bytes; done never
            # passes the file size.
            self._done = min(self._done + n, self._total)
            self._reporter.update(self._done)

    def finish(self) -> None:
        with self._lock:
            self._reporter.finish(self._done)


@dataclass
class FileInfo:
    """File information"""

    content: Union[str, bytes]
    encoding: Optional[str]


@dataclass
class FileStat:
    """File metadata from the streamed /files/stat route (executor v0.0.24+).

    type is one of file|dir|symlink|other; mode is the octal permission
    string (e.g. "0644"); mtime is RFC 3339 UTC with nanoseconds.
    """

    type: str
    size: int
    mode: str
    mtime: str
    sha256: Optional[str] = None


class SandboxFilesystem:
    """
    Synchronous filesystem operations for Koyeb Sandbox instances.
    Using SandboxClient HTTP API.

    For async usage, use AsyncSandboxFilesystem instead.
    """

    def __init__(self, sandbox: Sandbox) -> None:
        self.sandbox = sandbox
        self._executor = None

    def _get_client(self) -> SandboxClient:
        """Get or create SandboxClient instance, shared with the sandbox"""
        return self.sandbox._get_client()

    def _get_executor(self) -> "SandboxExecutor":
        """Get or create SandboxExecutor instance"""
        if self._executor is None:
            from .exec import SandboxExecutor

            self._executor = SandboxExecutor(self.sandbox)
        return self._executor

    def write_file(
        self,
        path: str,
        content: Union[str, bytes, BinaryIO, Iterable[bytes]],
        encoding: str = "utf-8",
        *,
        mode: Optional[str] = None,
    ) -> None:
        """
        Write content to a file synchronously.

        On executors v0.0.24+ the content streams through PUT /files,
        binary-safe: any byte sequence lands on disk as-is.
        encoding="base64" decodes str and bytes content to the real
        bytes; BinaryIO and iterables stream as-is, ignoring it. Older
        executors are detected once per handle and keep the legacy JSON behavior —
        which cannot carry streamed content (BinaryIO, an iterable of
        chunks): that raises and names v0.0.24.

        Args:
            path: Absolute path to the file
            content: Content to write — string, bytes, a file object or an
                iterable of bytes chunks (the last two require executor
                v0.0.24+)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.
            mode: Octal permission string, e.g. "0644" (streamed routes only;
                the legacy routes keep the destination's mode)
        """
        client = self._get_client()

        if client.has_files_routes():
            with _translating_files_errors("write file", path):
                client.files_put(path, _put_body(content, encoding), mode=mode)
            return

        if not isinstance(content, (str, bytes)):
            raise SandboxFilesystemError(
                "streamed content (BinaryIO or an iterable of chunks) requires "
                "the streamed /files routes (executor v0.0.24+)"
            )
        if isinstance(content, bytes):
            if encoding == "base64":
                content_str = base64.b64encode(content).decode("ascii")
            else:
                content_str = content.decode(encoding)
        else:
            content_str = content

        try:
            response = client.write_file(path, content_str)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"), "write file"
                )
        except (SandboxServiceError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise SandboxFilesystemError(f"Failed to write file: {str(e)}") from e

    def read_file(self, path: str, encoding: Optional[str] = "utf-8") -> FileInfo:
        """
        Read a file from the sandbox synchronously.

        On executors v0.0.24+ the bytes stream from GET /files,
        binary-safe: encoding=None returns the disk bytes, and
        encoding="base64" encodes the real bytes for transport. Older
        executors keep the legacy JSON behavior: encoding="base64"
        decodes the file's base64 text and returns bytes; encoding=None
        is not supported there and raises.

        Args:
            path: Absolute path to the file
            encoding: File encoding (default: "utf-8"). Streamed routes:
                None returns the disk bytes, "base64" encodes them.
                Legacy routes: "base64" decodes the file's base64 text;
                None raises.

        Returns:
            FileInfo: Object with content (str or bytes) and encoding
        """
        client = self._get_client()

        if client.has_files_routes():
            with _translating_files_errors("read file", path):
                raw = b"".join(client.files_read(path))
            return FileInfo(content=_read_content(raw, encoding), encoding=encoding)

        if encoding is None:
            raise SandboxFilesystemError(
                "reading raw bytes (encoding=None) requires the streamed "
                "/files routes (executor v0.0.24+)"
            )

        try:
            response = client.read_file(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "read file",
                    not_found_msg=f"File not found: {path}",
                )
            content_str = response.get("content", "")
            if encoding == "base64":
                content: Union[str, bytes] = base64.b64decode(content_str)
            else:
                content = content_str
            return FileInfo(content=content, encoding=encoding)
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "read file", not_found_msg=f"File not found: {path}"
            ) from e

    def open_read(self, path: str) -> Iterator[bytes]:
        """
        Stream a file's bytes from the sandbox, chunk by chunk.

        Constant memory on both sides (executor v0.0.24+). On legacy
        executors the file is read once as text and yielded as a single
        chunk — binary-safe streaming is not available there.

        Args:
            path: Absolute path to the file

        Yields:
            File content chunks
        """
        client = self._get_client()
        if not client.has_files_routes():
            yield self.read_file(path).content.encode("utf-8")
            return
        with _translating_files_errors("read file", path):
            for chunk in client.files_read(path):
                yield chunk

    def stat(self, path: str) -> FileStat:
        """
        Stat a file on the sandbox (executor v0.0.24+).

        Legacy executors have no stat route: this raises. Size comes from
        the filesystem, never from a HEAD — size-0 pseudo-files (e.g. under
        /proc) carry no length but have content.

        Args:
            path: Absolute path to the file

        Returns:
            FileStat with type (file|dir|symlink|other), size, mode (octal
            string) and mtime (RFC 3339 UTC, nanoseconds)
        """
        client = self._get_client()
        if not client.has_files_routes():
            raise SandboxFilesystemError(
                "stat requires the streamed /files routes (executor v0.0.24+)"
            )
        with _translating_files_errors("stat file", path):
            entry = client.files_stat(path)
            return FileStat(
                type=entry["type"],
                size=entry["size"],
                mode=entry["mode"],
                mtime=entry["mtime"],
                sha256=entry.get("sha256"),
            )

    def mkdir(self, path: str) -> None:
        """
        Create a directory synchronously.

        Note: Parent directories are always created automatically by the API.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_client()

        try:
            response = client.make_dir(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "create directory",
                    exists_msg=f"Directory already exists: {path}",
                )
        except (SandboxServiceError, SandboxFileExistsError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e),
                "create directory",
                exists_msg=f"Directory already exists: {path}",
            ) from e

    def list_dir(self, path: str = ".") -> List[str]:
        """
        List contents of a directory synchronously.

        Args:
            path: Path to the directory (default: current directory)

        Returns:
            List[str]: Names of files and directories within the specified path.
        """
        client = self._get_client()

        try:
            response = client.list_dir(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "list directory",
                    not_found_msg=f"Directory not found: {path}",
                )
            entries = response.get("entries", [])
            return entries
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "list directory", not_found_msg=f"Directory not found: {path}"
            ) from e

    def delete_file(self, path: str) -> None:
        """
        Delete a file synchronously.

        Args:
            path: Absolute path to the file
        """
        client = self._get_client()

        try:
            response = client.delete_file(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "delete file",
                    not_found_msg=f"File not found: {path}",
                )
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "delete file", not_found_msg=f"File not found: {path}"
            ) from e

    def delete_dir(self, path: str) -> None:
        """
        Delete a directory synchronously.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_client()

        try:
            response = client.delete_dir(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "delete directory",
                    not_found_msg=f"Directory not found: {path}",
                    not_empty_msg=f"Directory not empty: {path}",
                )
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e),
                "delete directory",
                not_found_msg=f"Directory not found: {path}",
                not_empty_msg=f"Directory not empty: {path}",
            ) from e

    def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Rename a file synchronously.

        Args:
            old_path: Current file path
            new_path: New file path
        """
        # Use exec since there's no direct rename in SandboxClient
        # Properly escape paths to prevent shell injection
        executor = self._get_executor()
        old_path_escaped = escape_shell_arg(old_path)
        new_path_escaped = escape_shell_arg(new_path)
        result = executor(f"mv {old_path_escaped} {new_path_escaped}")

        if not result.success:
            raise _executor_error(
                result.stderr,
                "rename file",
                not_found_msg=f"File not found: {old_path}",
            )

    def move_file(self, source_path: str, destination_path: str) -> None:
        """
        Move a file to a different directory synchronously.

        Args:
            source_path: Current file path
            destination_path: Destination path
        """
        # Use exec since there's no direct move in SandboxClient
        # Properly escape paths to prevent shell injection
        executor = self._get_executor()
        source_path_escaped = escape_shell_arg(source_path)
        destination_path_escaped = escape_shell_arg(destination_path)
        result = executor(f"mv {source_path_escaped} {destination_path_escaped}")

        if not result.success:
            raise _executor_error(
                result.stderr,
                "move file",
                not_found_msg=f"File not found: {source_path}",
            )

    def write_files(self, files: List[Dict[str, str]]) -> None:
        """
        Write multiple files in a single operation synchronously.

        Args:
            files: List of dictionaries, each with 'path', 'content', and optional 'encoding'.
        """
        for file_info in files:
            path = file_info["path"]
            content = file_info["content"]
            encoding = file_info.get("encoding", "utf-8")
            self.write_file(path, content, encoding)

    def exists(self, path: str) -> bool:
        """Check if file/directory exists synchronously"""
        executor = self._get_executor()
        path_escaped = escape_shell_arg(path)
        result = executor(f"test -e {path_escaped}")
        return result.success

    def is_file(self, path: str) -> bool:
        """Check if path is a file synchronously"""
        executor = self._get_executor()
        path_escaped = escape_shell_arg(path)
        result = executor(f"test -f {path_escaped}")
        return result.success

    def is_dir(self, path: str) -> bool:
        """Check if path is a directory synchronously"""
        executor = self._get_executor()
        path_escaped = escape_shell_arg(path)
        result = executor(f"test -d {path_escaped}")
        return result.success

    def upload_file(
        self,
        local_path: str,
        remote_path: str,
        encoding: str = "utf-8",
        *,
        progress: Optional[Callable[[int, int], None]] = None,
        timeout: Optional[float] = None,
        part_size: int = UPLOAD_PART_SIZE,
        concurrency: int = UPLOAD_CONCURRENCY,
    ) -> None:
        """
        Upload a local file to the sandbox synchronously.

        On executors v0.0.24+ the file streams from disk through PUT
        /files — binary-safe, constant memory — with optional progress
        callbacks. A file larger than part_size uploads as a multipart
        session: up to `concurrency` parts in flight, each read from disk
        at its offset, per-part sha256, timed-out parts split into
        halves, and a complete that reports missing ranges fills them
        and completes again. Older executors keep the legacy JSON
        behavior (the encoding parameter applies there only).

        Args:
            local_path: Path to the local file
            remote_path: Destination path in the sandbox
            encoding: Legacy executors only (default: "utf-8"); the
                streamed routes are binary-safe and ignore it
            progress: Optional callback(done, total), called at most every
                100 ms during the transfer plus a final call
            timeout: Seconds without progress before the transfer's
                requests fail (default: the 60 s idle bound)
            part_size: Bytes per multipart part (default 50 MiB, capped by
                the executor's max_part_size); a file at or below it takes
                the single streamed PUT
            concurrency: Parts in flight for a multipart upload (default 4;
                memory holds at most part_size x concurrency)

        Raises:
            SandboxFileNotFoundError: If local file doesn't exist
        """
        if not os.path.exists(local_path):
            raise SandboxFileNotFoundError(f"Local file not found: {local_path}")

        client = self._get_client()
        if client.has_files_routes():
            if part_size <= 0 or concurrency <= 0:
                raise SandboxFilesystemError(
                    "part_size and concurrency must be positive"
                )
            size = os.path.getsize(local_path)
            with _translating_files_errors("upload file", remote_path):
                if size > part_size:
                    self._upload_multipart(
                        client,
                        local_path,
                        remote_path,
                        size,
                        part_size=part_size,
                        concurrency=concurrency,
                        timeout=timeout,
                        progress=progress,
                    )
                else:
                    reporter = _ProgressReporter(progress, size)
                    digest = _file_sha256(local_path)
                    with open(local_path, "rb") as f:
                        reply = client.files_put(
                            remote_path,
                            _progress_chunks(f, reporter),
                            sha256=digest,
                            timeout=timeout,
                        )
                    if reply["sha256"] != digest:
                        raise SandboxFilesystemError(
                            f"Upload corrupted in transit: executor sha256 "
                            f"{reply['sha256']} != {digest}"
                        )
            return

        with open(local_path, "rb") as f:
            content_bytes = f.read()

        self.write_file(remote_path, content_bytes, encoding=encoding)

    def _upload_multipart(
        self,
        client: SandboxClient,
        local_path: str,
        remote_path: str,
        size: int,
        *,
        part_size: int,
        concurrency: int,
        timeout: Optional[float],
        progress: Optional[Callable[[int, int], None]],
    ) -> None:
        """The session flow: open, parts, complete — abort on any failure.

        Sessions live at the executor: a lost one (restart, idle expiry)
        cannot be resumed, only restarted.
        """
        digest = _file_sha256(local_path)
        session = client.files_upload_open(
            remote_path, size, sha256=digest, timeout=timeout
        )
        upload_id = session.get("upload_id")
        if not isinstance(upload_id, str) or not upload_id:
            raise SandboxFilesystemError(
                f"Upload session reply missing upload_id: {session}"
            )
        counter = _PartProgress(progress, size)
        try:
            # A valid id means the session lives at the executor; every
            # failure from here on must abort it.
            cap = session.get("max_part_size")
            if not isinstance(cap, int) or cap < 1:
                raise SandboxFilesystemError(
                    f"Upload session reply missing max_part_size: {session}"
                )
            effective = min(part_size, cap)
            self._put_parts(
                client,
                local_path,
                upload_id,
                [(0, size)],
                effective,
                concurrency,
                timeout,
                counter,
            )
            reply = self._complete_filling_gaps(
                client, local_path, upload_id, effective, concurrency, timeout, counter
            )
            # The contract marks complete's sha256 optional: a 200 has
            # already matched the open-payload digest at the executor.
            got = reply.get("sha256")
            if got is not None and got != digest:
                raise SandboxFilesystemError(
                    f"Upload corrupted in transit: executor sha256 "
                    f"{got} != {digest}"
                )
        except BaseException:
            try:
                client.files_upload_abort(upload_id, timeout=timeout)
            except SandboxError:
                pass  # never mask the failure that caused the abort
            raise
        counter.finish()

    def _put_parts(
        self,
        client: SandboxClient,
        local_path: str,
        upload_id: str,
        ranges: List[Tuple[int, int]],
        part_size: int,
        concurrency: int,
        timeout: Optional[float],
        counter: _PartProgress,
    ) -> None:
        """PUT the given ranges as parts, `concurrency` in flight, fail fast."""
        plan: List[Tuple[int, int]] = []
        for start, end in ranges:
            plan.extend(_part_plan(start, end, part_size))
        if not plan:
            return
        queue = iter(plan)
        stop = threading.Event()

        def work() -> None:
            while not stop.is_set():
                part = next(queue, None)
                if part is None:
                    return
                try:
                    self._put_one_part(
                        client,
                        local_path,
                        upload_id,
                        part[0],
                        part[1],
                        timeout,
                        counter,
                    )
                except BaseException:
                    stop.set()
                    raise

        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            first: Optional[BaseException] = None
            try:
                futures = [
                    pool.submit(work) for _ in range(min(concurrency, len(plan)))
                ]
                for future in futures:
                    try:
                        future.result()
                    except BaseException as e:
                        if first is None:
                            first = e
                        # The stored interrupt must stop the remaining
                        # parts now, not after the queue drains.
                        stop.set()
            finally:
                # The same stop covers an interrupt during submit.
                stop.set()
        if first is not None:
            raise first

    def _put_one_part(
        self,
        client: SandboxClient,
        local_path: str,
        upload_id: str,
        offset: int,
        length: int,
        timeout: Optional[float],
        counter: _PartProgress,
    ) -> None:
        """PUT one range; a timed-out part splits into halves and retries."""
        pending = [(offset, length)]
        while pending:
            off, ln = pending.pop()
            data, digest = _read_part_with_digest(local_path, off, ln)
            try:
                client.files_upload_part(
                    upload_id, off, data, sha256=digest, timeout=timeout
                )
            except SandboxError as e:
                # Split-worthy first: a 524 arrives as SandboxServiceError,
                # a subclass of SandboxRequestError.
                if _split_worthy(e) and ln >= 2 * _MIN_SPLIT_SIZE:
                    half = ln // 2
                    pending.append((off + half, ln - half))
                    pending.append((off, half))
                    continue
                if isinstance(e, SandboxRequestError) and e.status_code == 404:
                    raise SandboxFilesystemError(_LOST_SESSION_MESSAGE) from e
                raise
            counter.add(ln)

    def _complete_filling_gaps(
        self,
        client: SandboxClient,
        local_path: str,
        upload_id: str,
        part_size: int,
        concurrency: int,
        timeout: Optional[float],
        counter: _PartProgress,
    ) -> Dict[str, Any]:
        """Complete; a 409's missing ranges are filled and complete retried.

        The session stays live across a 409 — it is the resume signal.
        Every fill must shrink the missing bytes; a set that does not is
        the executor not recording the fills, and that loop is cut here
        rather than spun forever.
        """
        previous: Optional[int] = None
        while True:
            try:
                return client.files_upload_complete(upload_id, timeout=timeout)
            except SandboxRequestError as e:
                if e.status_code == 404:
                    raise SandboxFilesystemError(_LOST_SESSION_MESSAGE) from e
                if e.status_code != 409:
                    raise
                missing = _missing_ranges_from_409(e.body)
                if not missing:
                    raise SandboxFilesystemError(
                        f"Upload incomplete and the missing-ranges reply was "
                        f"unusable: {e.body!r}"
                    ) from e
                missing_bytes = sum(end - start for start, end in missing)
                if previous is not None and missing_bytes >= previous:
                    raise SandboxFilesystemError(
                        f"Upload made no progress filling missing ranges: {missing}"
                    ) from e
                previous = missing_bytes
                self._put_parts(
                    client,
                    local_path,
                    upload_id,
                    missing,
                    part_size,
                    concurrency,
                    timeout,
                    counter,
                )

    def download_file(
        self,
        remote_path: str,
        local_path: str,
        encoding: str = "utf-8",
        *,
        progress: Optional[Callable[[int, int], None]] = None,
        timeout: Optional[float] = None,
    ) -> None:
        """
        Download a file from the sandbox to a local path synchronously.

        On executors v0.0.24+ the size comes from stat (never a HEAD), the
        bytes stream into <local>.part and rename into place on success:
        a failed download leaves the destination exactly as it was.
        Older executors keep the legacy JSON behavior.

        Args:
            remote_path: Path to the file in the sandbox
            local_path: Destination path on the local filesystem
            encoding: Legacy executors only (default: "utf-8"); the
                streamed routes are binary-safe and ignore it
            progress: Optional callback(done, total), called at most every
                100 ms during the transfer plus a final call
            timeout: Seconds without progress before the transfer's stream
                fails (default: the 60 s idle bound)

        Raises:
            SandboxFileNotFoundError: If remote file doesn't exist
        """
        client = self._get_client()
        if client.has_files_routes():
            part_path = f"{local_path}.part"
            with _translating_files_errors("download file", remote_path):
                entry = client.files_stat(remote_path)
                reporter = _ProgressReporter(progress, entry["size"])
                done = 0
                renamed = False
                try:
                    with open_nofollow(part_path) as out:
                        for chunk in client.files_read(remote_path, timeout=timeout):
                            out.write(chunk)
                            done += len(chunk)
                            reporter.update(done)
                    reporter.finish(done)
                    os.replace(part_path, local_path)
                    renamed = True
                finally:
                    if not renamed:
                        try:
                            os.unlink(part_path)
                        except OSError:
                            pass
            return

        file_info = self.read_file(remote_path, encoding=encoding)

        if isinstance(file_info.content, bytes):
            content_bytes = file_info.content
        else:
            content_bytes = file_info.content.encode(encoding)

        with open(local_path, "wb") as f:
            f.write(content_bytes)

    def ls(self, path: str = ".") -> List[str]:
        """
        List directory contents synchronously.

        Args:
            path: Path to list

        Returns:
            List of file/directory names
        """
        return SandboxFilesystem.list_dir(self, path)

    def rm(self, path: str, recursive: bool = False) -> None:
        """
        Remove file or directory synchronously.

        Args:
            path: Path to remove
            recursive: Remove recursively
        """
        executor = self._get_executor()
        path_escaped = escape_shell_arg(path)

        if recursive:
            result = executor(f"rm -rf {path_escaped}")
        else:
            result = executor(f"rm {path_escaped}")

        if not result.success:
            raise _executor_error(
                result.stderr, "remove", not_found_msg=f"File not found: {path}"
            )

    def open(
        self, path: str, mode: str = "r", encoding: str = "utf-8"
    ) -> SandboxFileIO:
        """
        Open a file in the sandbox synchronously.

        Args:
            path: Path to the file
            mode: Open mode ('r', 'w', 'a', etc.)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.

        Returns:
            SandboxFileIO: File handle
        """
        return SandboxFileIO(self, path, mode, encoding)

    def sync(
        self,
        local: str,
        remote: Optional[str] = None,
        *,
        direction: str = "push",
        delete: bool = False,
        exclude: Sequence[str] = (),
        checksum: bool = False,
        dry_run: bool = False,
    ) -> Dict[str, int]:
        """
        Sync a directory with the sandbox, one way like ``rsync -r``.

        Both sides are listed (a local walk against the executor's
        NDJSON listing) and diffed on path, type, size and mtime —
        whole seconds, like rsync's default; ``checksum=True`` adds a
        sha256 comparison for files that pass that test. On push, the
        changed set travels as ~50 MiB gzip'd tar batches through
        /files/archive; on pull, the remote tree's archive streams down
        and only the changed set is extracted. Files larger than one
        batch go through upload_file/download_file instead (multipart
        on executors v0.0.24+, resumable downloads), and a pull's
        archive leaves them out so their bytes travel once.
        Symlinks travel as links, modes are kept, owners are not. A pull
        never writes outside local: a path that leaves it, or that goes
        through a symlink, fails the sync.

        A no-op sync sends nothing: nothing is transferred or deleted;
        beyond the listing only ``checksum=True`` asks more — one sha256
        stat per size-and-mtime-equal file. With ``delete=True`` the
        destination is pruned to match (a directory counts as one
        deletion); deletes ride the legacy routes, which every executor
        serves. ``dry_run=True`` computes the result without touching
        either side.

        Args:
            local: Local directory path
            remote: Destination path in the sandbox; relative paths
                resolve under the sandbox workdir. None uses local's
                relative form (its basename when absolute), rsync-style
            direction: "push" (local → sandbox) or "pull" (sandbox → local)
            delete: Remove destination entries absent from the source
            exclude: Glob patterns; a matching path (or any /-separated
                suffix of it) is skipped, a matching directory whole
            checksum: Compare sha256 for size-and-mtime-equal files
            dry_run: Compute the plan only, transfer nothing

        Returns:
            {"uploaded"|"downloaded", "deleted", "skipped", "bytes"}

        Raises:
            SandboxFilesystemError: On any failure, the filesystem taxonomy
        """
        if direction not in ("push", "pull"):
            raise ValueError(f"direction must be 'push' or 'pull', not {direction!r}")
        if remote is None:
            remote = relative_remote(local)
        client = self._get_client()
        if not client.has_files_routes():
            raise SandboxFilesystemError(
                "sync requires executor v0.0.24+ (the streamed /files "
                "routes); this sandbox's executor is older"
            )
        with _translating_files_errors(f"sync {direction}", local):
            if direction == "push":
                return self._sync_push(
                    local, remote, client, delete, exclude, checksum, dry_run
                )
            return self._sync_pull(
                local, remote, client, delete, exclude, checksum, dry_run
            )

    def _sync_push(
        self,
        local: str,
        remote: str,
        client: SandboxClient,
        delete: bool,
        exclude: Sequence[str],
        checksum: bool,
        dry_run: bool,
    ) -> Dict[str, int]:
        local_entries = walk_local(local, exclude)
        try:
            remote_entries = list(client.files_list(remote, recursive=True))
        except SandboxRequestError as e:
            # A missing remote tree is an empty one: the archive PUT
            # creates the root (MkdirAll), like rsync creating its dest.
            if e.status_code != 404:
                raise
            remote_entries = []
        # Excluded remote paths stay invisible to the diff: delete must
        # spare what exclude promised to skip.
        remote_entries = [
            e for e in remote_entries if not path_excluded(e["path"], exclude)
        ]

        hashes = self._sync_hashes(
            client, local, remote, checksum, False, local_entries, remote_entries
        )
        result = diff(local_entries, remote_entries, delete=delete, **hashes)
        batches, oversized = plan_batches(result.to_transfer, SYNC_BATCH_BYTES)
        if not dry_run:
            for batch in batches:
                fd, spool = tempfile.mkstemp(suffix=".koyeb-sync.tgz")
                os.close(fd)
                try:
                    build_archive(local, batch, spool)
                    with open(spool, "rb") as f:
                        client.files_archive_put(remote, f)
                finally:
                    with suppress(OSError):
                        os.unlink(spool)
            for entry in oversized:
                self.upload_file(
                    join_local(local, entry["path"]),
                    remote_join(remote, entry["path"]),
                )
            deleted = self._sync_remote_deletes(remote, result, delete)
        else:
            deleted = len(prune_descendants([e["path"] for e in result.deletes]))
        return {
            "uploaded": len(result.to_transfer),
            "deleted": deleted,
            "skipped": result.skipped,
            "bytes": result.bytes,
        }

    def _sync_remote_deletes(self, remote: str, result: SyncDiff, delete: bool) -> int:
        if not delete:
            return 0
        by_path = {e["path"]: e for e in result.deletes}
        count = 0
        for path in prune_descendants(list(by_path)):
            try:
                if by_path[path].get("type") == "dir":
                    self.delete_dir(remote_join(remote, path))
                else:
                    self.delete_file(remote_join(remote, path))
            except SandboxFileNotFoundError:
                # A type flip earlier in this sync may have replaced the
                # path's parent; being already gone is the wanted state.
                pass
            count += 1
        return count

    def _sync_hashes(
        self,
        client: SandboxClient,
        local: str,
        remote: str,
        checksum: bool,
        pull: bool,
        source_entries: List[Dict[str, Any]],
        dest_entries: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """diff()'s hash callables, with the executor side prefetched.

        In diff()'s terms the source is always `local_entries`: on push
        that is the local tree, on pull the remote one. The executor-side
        digests are prefetched in one pass — the pure, synchronous diff
        cannot await — and a vanished file (404) hashes as None:
        unprovable, not changed.
        """
        if not checksum:
            return {}
        stats: Dict[str, Optional[str]] = {}
        for path in hash_candidates(source_entries, dest_entries):
            try:
                entry = client.files_stat(remote_join(remote, path), hash="sha256")
            except SandboxRequestError as e:
                if e.status_code != 404:
                    raise
                stats[path] = None
            else:
                stats[path] = (entry or {}).get("sha256")

        def executor_sha(path: str) -> Optional[str]:
            return stats.get(path)

        def disk_sha(path: str) -> str:
            return _file_sha256(join_local(local, path))

        if pull:
            # The remote tree is diff()'s source side on pull.
            return {"local_hash": executor_sha, "remote_hash": disk_sha}
        return {"local_hash": disk_sha, "remote_hash": executor_sha}

    def _sync_pull(
        self,
        local: str,
        remote: str,
        client: SandboxClient,
        delete: bool,
        exclude: Sequence[str],
        checksum: bool,
        dry_run: bool,
    ) -> Dict[str, int]:
        # A missing destination root is an empty tree: extraction
        # creates it, like rsync creating its dest on pull.
        local_entries = walk_local(local, exclude) if os.path.isdir(local) else []
        remote_entries = list(client.files_list(remote, recursive=True))
        # The source listing gets the same filter as the local walk: an
        # excluded path is neither planned nor counted.
        remote_entries = [
            e for e in remote_entries if not path_excluded(e["path"], exclude)
        ]
        # The listing comes from the sandbox: refuse a path that would land
        # outside local before anything is written.
        for entry in remote_entries:
            clean_path(entry["path"])
        hashes = self._sync_hashes(
            client, local, remote, checksum, True, remote_entries, local_entries
        )
        result = diff(remote_entries, local_entries, delete=delete, **hashes)
        batches, oversized = plan_batches(result.to_transfer, SYNC_BATCH_BYTES)
        # Oversized files ride download_file; the archive leaves them out
        # so their bytes travel once.
        archive_exclude = tuple(exclude) + tuple(e["path"] for e in oversized)
        # Archive excludes are glob patterns: an oversized name would
        # also drop same-suffixed planned members — refuse loudly.
        oversized_patterns = tuple(e["path"] for e in oversized)
        colliding = sorted(
            {
                entry["path"]
                for batch in batches
                for entry in batch
                if path_excluded(entry["path"], oversized_patterns)
            }
        )
        if colliding:
            raise SandboxFilesystemError(
                f"sync pull cannot deliver {colliding}: the archive exclude "
                f"for oversized files would also drop them; rename or sync "
                f"them separately"
            )
        if not dry_run:
            if batches:
                fd, spool = tempfile.mkstemp(suffix=".koyeb-sync.tgz")
                os.close(fd)
                try:
                    with open(spool, "wb") as out:
                        for chunk in client.files_archive_get(remote, archive_exclude):
                            out.write(chunk)
                    keep = {entry["path"] for batch in batches for entry in batch}
                    extract_archive(spool, local, keep=keep)
                finally:
                    with suppress(OSError):
                        os.unlink(spool)
            for entry in oversized:
                self.download_file(
                    remote_join(remote, entry["path"]),
                    join_local(local, entry["path"]),
                )
            deleted = self._sync_local_deletes(local, result, delete)
        else:
            deleted = len(prune_descendants([e["path"] for e in result.deletes]))
        return {
            "downloaded": len(result.to_transfer),
            "deleted": deleted,
            "skipped": result.skipped,
            "bytes": result.bytes,
        }

    def _sync_local_deletes(self, local: str, result: SyncDiff, delete: bool) -> int:
        if not delete:
            return 0
        by_path = {e["path"]: e for e in result.deletes}
        count = 0
        for path in prune_descendants(list(by_path)):
            try:
                target = join_local(local, path)
            except ValueError:
                # A type flip's extract replaced a parent with a symlink:
                # the path is gone from the tree, never delete through it.
                count += 1
                continue
            try:
                if os.path.isdir(target) and not os.path.islink(target):
                    shutil.rmtree(target)
                else:
                    os.unlink(target)
            except (FileNotFoundError, NotADirectoryError):
                # A type flip's extract may have replaced the parent
                # already; being gone is the wanted state.
                pass
            count += 1
        return count


class AsyncSandboxFilesystem(SandboxFilesystem):
    """
    Async filesystem operations for Koyeb Sandbox instances.
    Uses native async I/O via AsyncSandboxClient.
    """

    def _get_async_client(self) -> AsyncSandboxClient:
        """Get AsyncSandboxClient instance from the sandbox."""
        return self.sandbox._get_async_client()

    def _get_async_executor(self) -> "AsyncSandboxExecutor":
        """Get or create AsyncSandboxExecutor instance."""
        if self._executor is None:
            from .exec import AsyncSandboxExecutor

            self._executor = AsyncSandboxExecutor(self.sandbox)
        return self._executor

    async def write_file(
        self,
        path: str,
        content: Union[str, bytes, BinaryIO, Iterable[bytes]],
        encoding: str = "utf-8",
        *,
        mode: Optional[str] = None,
    ) -> None:
        """
        Write content to a file asynchronously.

        On executors v0.0.24+ the content streams through PUT /files,
        binary-safe: any byte sequence lands on disk as-is.
        encoding="base64" decodes str and bytes content to the real
        bytes; BinaryIO and iterables stream as-is, ignoring it. Older
        executors are detected once per handle and keep the legacy JSON behavior —
        which cannot carry streamed content (BinaryIO, an iterable of
        chunks): that raises and names v0.0.24.

        Args:
            path: Absolute path to the file
            content: Content to write — string, bytes, a file object or an
                iterable of bytes chunks (the last two require executor
                v0.0.24+)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.
            mode: Octal permission string, e.g. "0644" (streamed routes only;
                the legacy routes keep the destination's mode)
        """
        client = self._get_async_client()

        if await client.has_files_routes():
            with _translating_files_errors("write file", path):
                await client.files_put(path, _put_body(content, encoding), mode=mode)
            return

        if not isinstance(content, (str, bytes)):
            raise SandboxFilesystemError(
                "streamed content (BinaryIO or an iterable of chunks) requires "
                "the streamed /files routes (executor v0.0.24+)"
            )
        if isinstance(content, bytes):
            if encoding == "base64":
                content_str = base64.b64encode(content).decode("ascii")
            else:
                content_str = content.decode(encoding)
        else:
            content_str = content

        try:
            response = await client.write_file(path, content_str)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"), "write file"
                )
        except (SandboxServiceError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise SandboxFilesystemError(f"Failed to write file: {str(e)}") from e

    async def read_file(self, path: str, encoding: Optional[str] = "utf-8") -> FileInfo:
        """
        Read a file from the sandbox asynchronously.

        On executors v0.0.24+ the bytes stream from GET /files,
        binary-safe: encoding=None returns the disk bytes, and
        encoding="base64" encodes the real bytes for transport. Older
        executors keep the legacy JSON behavior: encoding="base64"
        decodes the file's base64 text and returns bytes; encoding=None
        is not supported there and raises.

        Args:
            path: Absolute path to the file
            encoding: File encoding (default: "utf-8"). Streamed routes:
                None returns the disk bytes, "base64" encodes them.
                Legacy routes: "base64" decodes the file's base64 text;
                None raises.

        Returns:
            FileInfo: Object with content (str or bytes) and encoding
        """
        client = self._get_async_client()

        if await client.has_files_routes():
            with _translating_files_errors("read file", path):
                chunks = []
                async for chunk in client.files_read(path):
                    chunks.append(chunk)
                raw = b"".join(chunks)
            return FileInfo(content=_read_content(raw, encoding), encoding=encoding)

        if encoding is None:
            raise SandboxFilesystemError(
                "reading raw bytes (encoding=None) requires the streamed "
                "/files routes (executor v0.0.24+)"
            )

        try:
            response = await client.read_file(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "read file",
                    not_found_msg=f"File not found: {path}",
                )
            content_str = response.get("content", "")
            if encoding == "base64":
                content: Union[str, bytes] = base64.b64decode(content_str)
            else:
                content = content_str
            return FileInfo(content=content, encoding=encoding)
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "read file", not_found_msg=f"File not found: {path}"
            ) from e

    async def open_read(self, path: str) -> AsyncIterator[bytes]:
        """
        Stream a file's bytes from the sandbox, chunk by chunk.

        Constant memory on both sides (executor v0.0.24+). On legacy
        executors the file is read once as text and yielded as a single
        chunk — binary-safe streaming is not available there.

        Args:
            path: Absolute path to the file

        Yields:
            File content chunks
        """
        client = self._get_async_client()
        if not await client.has_files_routes():
            yield (await self.read_file(path)).content.encode("utf-8")
            return
        with _translating_files_errors("read file", path):
            async for chunk in client.files_read(path):
                yield chunk

    async def stat(self, path: str) -> FileStat:
        """
        Stat a file on the sandbox (executor v0.0.24+).

        Legacy executors have no stat route: this raises. Size comes from
        the filesystem, never from a HEAD — size-0 pseudo-files (e.g. under
        /proc) carry no length but have content.

        Args:
            path: Absolute path to the file

        Returns:
            FileStat with type (file|dir|symlink|other), size, mode (octal
            string) and mtime (RFC 3339 UTC, nanoseconds)
        """
        client = self._get_async_client()
        if not await client.has_files_routes():
            raise SandboxFilesystemError(
                "stat requires the streamed /files routes (executor v0.0.24+)"
            )
        with _translating_files_errors("stat file", path):
            entry = await client.files_stat(path)
            return FileStat(
                type=entry["type"],
                size=entry["size"],
                mode=entry["mode"],
                mtime=entry["mtime"],
                sha256=entry.get("sha256"),
            )

    async def mkdir(self, path: str) -> None:
        """
        Create a directory asynchronously.

        Note: Parent directories are always created automatically by the API.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_async_client()

        try:
            response = await client.make_dir(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "create directory",
                    exists_msg=f"Directory already exists: {path}",
                )
        except (SandboxServiceError, SandboxFileExistsError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e),
                "create directory",
                exists_msg=f"Directory already exists: {path}",
            ) from e

    async def list_dir(self, path: str = ".") -> List[str]:
        """
        List contents of a directory asynchronously.

        Args:
            path: Path to the directory (default: current directory)

        Returns:
            List[str]: Names of files and directories within the specified path.
        """
        client = self._get_async_client()

        try:
            response = await client.list_dir(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "list directory",
                    not_found_msg=f"Directory not found: {path}",
                )
            entries = response.get("entries", [])
            return entries
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "list directory", not_found_msg=f"Directory not found: {path}"
            ) from e

    async def delete_file(self, path: str) -> None:
        """
        Delete a file asynchronously.

        Args:
            path: Absolute path to the file
        """
        client = self._get_async_client()

        try:
            response = await client.delete_file(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "delete file",
                    not_found_msg=f"File not found: {path}",
                )
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e), "delete file", not_found_msg=f"File not found: {path}"
            ) from e

    async def delete_dir(self, path: str) -> None:
        """
        Delete a directory asynchronously.

        Args:
            path: Absolute path to the directory
        """
        client = self._get_async_client()

        try:
            response = await client.delete_dir(path)
            if response.get("error"):
                raise _executor_error(
                    response.get("error", "Unknown error"),
                    "delete directory",
                    not_found_msg=f"Directory not found: {path}",
                    not_empty_msg=f"Directory not empty: {path}",
                )
        except (SandboxServiceError, SandboxFileNotFoundError, SandboxFilesystemError):
            raise
        except Exception as e:
            raise _executor_error(
                str(e),
                "delete directory",
                not_found_msg=f"Directory not found: {path}",
                not_empty_msg=f"Directory not empty: {path}",
            ) from e

    async def rename_file(self, old_path: str, new_path: str) -> None:
        """
        Rename a file asynchronously.

        Args:
            old_path: Current file path
            new_path: New file path
        """
        executor = self._get_async_executor()
        old_path_escaped = escape_shell_arg(old_path)
        new_path_escaped = escape_shell_arg(new_path)
        result = await executor(f"mv {old_path_escaped} {new_path_escaped}")

        if not result.success:
            raise _executor_error(
                result.stderr,
                "rename file",
                not_found_msg=f"File not found: {old_path}",
            )

    async def move_file(self, source_path: str, destination_path: str) -> None:
        """
        Move a file to a different directory asynchronously.

        Args:
            source_path: Current file path
            destination_path: Destination path
        """
        executor = self._get_async_executor()
        source_path_escaped = escape_shell_arg(source_path)
        destination_path_escaped = escape_shell_arg(destination_path)
        result = await executor(f"mv {source_path_escaped} {destination_path_escaped}")

        if not result.success:
            raise _executor_error(
                result.stderr,
                "move file",
                not_found_msg=f"File not found: {source_path}",
            )

    async def write_files(self, files: List[Dict[str, str]]) -> None:
        """
        Write multiple files in a single operation asynchronously.

        Args:
            files: List of dictionaries, each with 'path', 'content', and optional 'encoding'.
        """
        for file_info in files:
            path = file_info["path"]
            content = file_info["content"]
            encoding = file_info.get("encoding", "utf-8")
            await self.write_file(path, content, encoding)

    async def exists(self, path: str) -> bool:
        """Check if file/directory exists asynchronously"""
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)
        result = await executor(f"test -e {path_escaped}")
        return result.success

    async def is_file(self, path: str) -> bool:
        """Check if path is a file asynchronously"""
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)
        result = await executor(f"test -f {path_escaped}")
        return result.success

    async def is_dir(self, path: str) -> bool:
        """Check if path is a directory asynchronously"""
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)
        result = await executor(f"test -d {path_escaped}")
        return result.success

    async def upload_file(
        self,
        local_path: str,
        remote_path: str,
        encoding: str = "utf-8",
        *,
        progress: Optional[Callable[[int, int], None]] = None,
        timeout: Optional[float] = None,
        part_size: int = UPLOAD_PART_SIZE,
        concurrency: int = UPLOAD_CONCURRENCY,
    ) -> None:
        """
        Upload a local file to the sandbox asynchronously.

        On executors v0.0.24+ the file streams from disk through PUT
        /files — binary-safe, constant memory — with optional progress
        callbacks. A file larger than part_size uploads as a multipart
        session: up to `concurrency` parts in flight, each read from disk
        at its offset, per-part sha256, timed-out parts split into
        halves, and a complete that reports missing ranges fills them
        and completes again. Older executors keep the legacy JSON
        behavior (the encoding parameter applies there only).

        Args:
            local_path: Path to the local file
            remote_path: Destination path in the sandbox
            encoding: Legacy executors only (default: "utf-8"); the
                streamed routes are binary-safe and ignore it
            progress: Optional callback(done, total), called at most every
                100 ms during the transfer plus a final call
            timeout: Seconds without progress before the transfer's
                requests fail (default: the 60 s idle bound)
            part_size: Bytes per multipart part (default 50 MiB, capped by
                the executor's max_part_size); a file at or below it takes
                the single streamed PUT
            concurrency: Parts in flight for a multipart upload (default 4;
                memory holds at most part_size x concurrency)

        Raises:
            SandboxFileNotFoundError: If local file doesn't exist
        """
        if not os.path.exists(local_path):
            raise SandboxFileNotFoundError(f"Local file not found: {local_path}")

        client = self._get_async_client()
        if await client.has_files_routes():
            if part_size <= 0 or concurrency <= 0:
                raise SandboxFilesystemError(
                    "part_size and concurrency must be positive"
                )
            size = os.path.getsize(local_path)
            with _translating_files_errors("upload file", remote_path):
                if size > part_size:
                    await self._upload_multipart(
                        client,
                        local_path,
                        remote_path,
                        size,
                        part_size=part_size,
                        concurrency=concurrency,
                        timeout=timeout,
                        progress=progress,
                    )
                else:
                    reporter = _ProgressReporter(progress, size)
                    digest = await asyncio.to_thread(_file_sha256, local_path)
                    with open(local_path, "rb") as f:
                        reply = await client.files_put(
                            remote_path,
                            _progress_chunks(f, reporter),
                            sha256=digest,
                            timeout=timeout,
                        )
                    if reply["sha256"] != digest:
                        raise SandboxFilesystemError(
                            f"Upload corrupted in transit: executor sha256 "
                            f"{reply['sha256']} != {digest}"
                        )
            return

        with open(local_path, "rb") as f:
            content_bytes = f.read()

        await self.write_file(remote_path, content_bytes, encoding=encoding)

    async def _upload_multipart(
        self,
        client: AsyncSandboxClient,
        local_path: str,
        remote_path: str,
        size: int,
        *,
        part_size: int,
        concurrency: int,
        timeout: Optional[float],
        progress: Optional[Callable[[int, int], None]],
    ) -> None:
        """The session flow: open, parts, complete — abort on any failure.

        Sessions live at the executor: a lost one (restart, idle expiry)
        cannot be resumed, only restarted.
        """
        digest = await asyncio.to_thread(_file_sha256, local_path)
        session = await client.files_upload_open(
            remote_path, size, sha256=digest, timeout=timeout
        )
        upload_id = session.get("upload_id")
        if not isinstance(upload_id, str) or not upload_id:
            raise SandboxFilesystemError(
                f"Upload session reply missing upload_id: {session}"
            )
        counter = _PartProgress(progress, size)
        try:
            # A valid id means the session lives at the executor; every
            # failure from here on must abort it.
            cap = session.get("max_part_size")
            if not isinstance(cap, int) or cap < 1:
                raise SandboxFilesystemError(
                    f"Upload session reply missing max_part_size: {session}"
                )
            effective = min(part_size, cap)
            await self._put_parts(
                client,
                local_path,
                upload_id,
                [(0, size)],
                effective,
                concurrency,
                timeout,
                counter,
            )
            reply = await self._complete_filling_gaps(
                client, local_path, upload_id, effective, concurrency, timeout, counter
            )
            # The contract marks complete's sha256 optional: a 200 has
            # already matched the open-payload digest at the executor.
            got = reply.get("sha256")
            if got is not None and got != digest:
                raise SandboxFilesystemError(
                    f"Upload corrupted in transit: executor sha256 "
                    f"{got} != {digest}"
                )
        except BaseException:
            try:
                await client.files_upload_abort(upload_id, timeout=timeout)
            except SandboxError:
                pass  # never mask the failure that caused the abort
            raise
        counter.finish()

    async def _put_parts(
        self,
        client: AsyncSandboxClient,
        local_path: str,
        upload_id: str,
        ranges: List[Tuple[int, int]],
        part_size: int,
        concurrency: int,
        timeout: Optional[float],
        counter: _PartProgress,
    ) -> None:
        """PUT the given ranges as parts, `concurrency` in flight, fail fast."""
        plan: List[Tuple[int, int]] = []
        for start, end in ranges:
            plan.extend(_part_plan(start, end, part_size))
        if not plan:
            return
        queue = iter(plan)
        stop = asyncio.Event()

        async def work() -> None:
            while not stop.is_set():
                part = next(queue, None)
                if part is None:
                    return
                try:
                    await self._put_one_part(
                        client,
                        local_path,
                        upload_id,
                        part[0],
                        part[1],
                        timeout,
                        counter,
                    )
                except BaseException:
                    stop.set()
                    raise

        results = await asyncio.gather(
            *[work() for _ in range(min(concurrency, len(plan)))],
            return_exceptions=True,
        )
        errors = [r for r in results if isinstance(r, BaseException)]
        if errors:
            raise errors[0]

    async def _put_one_part(
        self,
        client: AsyncSandboxClient,
        local_path: str,
        upload_id: str,
        offset: int,
        length: int,
        timeout: Optional[float],
        counter: _PartProgress,
    ) -> None:
        """PUT one range; a timed-out part splits into halves and retries."""
        pending = [(offset, length)]
        while pending:
            off, ln = pending.pop()
            data, digest = await asyncio.to_thread(
                _read_part_with_digest, local_path, off, ln
            )
            try:
                await client.files_upload_part(
                    upload_id, off, data, sha256=digest, timeout=timeout
                )
            except SandboxError as e:
                # Split-worthy first: a 524 arrives as SandboxServiceError,
                # a subclass of SandboxRequestError.
                if _split_worthy(e) and ln >= 2 * _MIN_SPLIT_SIZE:
                    half = ln // 2
                    pending.append((off + half, ln - half))
                    pending.append((off, half))
                    continue
                if isinstance(e, SandboxRequestError) and e.status_code == 404:
                    raise SandboxFilesystemError(_LOST_SESSION_MESSAGE) from e
                raise
            counter.add(ln)

    async def _complete_filling_gaps(
        self,
        client: AsyncSandboxClient,
        local_path: str,
        upload_id: str,
        part_size: int,
        concurrency: int,
        timeout: Optional[float],
        counter: _PartProgress,
    ) -> Dict[str, Any]:
        """Complete; a 409's missing ranges are filled and complete retried.

        The session stays live across a 409 — it is the resume signal.
        Every fill must shrink the missing bytes; a set that does not is
        the executor not recording the fills, and that loop is cut here
        rather than spun forever.
        """
        previous: Optional[int] = None
        while True:
            try:
                return await client.files_upload_complete(upload_id, timeout=timeout)
            except SandboxRequestError as e:
                if e.status_code == 404:
                    raise SandboxFilesystemError(_LOST_SESSION_MESSAGE) from e
                if e.status_code != 409:
                    raise
                missing = _missing_ranges_from_409(e.body)
                if not missing:
                    raise SandboxFilesystemError(
                        f"Upload incomplete and the missing-ranges reply was "
                        f"unusable: {e.body!r}"
                    ) from e
                missing_bytes = sum(end - start for start, end in missing)
                if previous is not None and missing_bytes >= previous:
                    raise SandboxFilesystemError(
                        f"Upload made no progress filling missing ranges: {missing}"
                    ) from e
                previous = missing_bytes
                await self._put_parts(
                    client,
                    local_path,
                    upload_id,
                    missing,
                    part_size,
                    concurrency,
                    timeout,
                    counter,
                )

    async def download_file(
        self,
        remote_path: str,
        local_path: str,
        encoding: str = "utf-8",
        *,
        progress: Optional[Callable[[int, int], None]] = None,
        timeout: Optional[float] = None,
    ) -> None:
        """
        Download a file from the sandbox to a local path asynchronously.

        On executors v0.0.24+ the size comes from stat (never a HEAD), the
        bytes stream into <local>.part and rename into place on success:
        a failed download leaves the destination exactly as it was.
        Older executors keep the legacy JSON behavior.

        Args:
            remote_path: Path to the file in the sandbox
            local_path: Destination path on the local filesystem
            encoding: Legacy executors only (default: "utf-8"); the
                streamed routes are binary-safe and ignore it
            progress: Optional callback(done, total), called at most every
                100 ms during the transfer plus a final call
            timeout: Seconds without progress before the transfer's stream
                fails (default: the 60 s idle bound)

        Raises:
            SandboxFileNotFoundError: If remote file doesn't exist
        """
        client = self._get_async_client()
        if await client.has_files_routes():
            part_path = f"{local_path}.part"
            with _translating_files_errors("download file", remote_path):
                entry = await client.files_stat(remote_path)
                reporter = _ProgressReporter(progress, entry["size"])
                done = 0
                renamed = False
                try:
                    with open_nofollow(part_path) as out:
                        async for chunk in client.files_read(
                            remote_path, timeout=timeout
                        ):
                            out.write(chunk)
                            done += len(chunk)
                            reporter.update(done)
                    reporter.finish(done)
                    os.replace(part_path, local_path)
                    renamed = True
                finally:
                    if not renamed:
                        try:
                            os.unlink(part_path)
                        except OSError:
                            pass
            return

        file_info = await self.read_file(remote_path, encoding=encoding)

        if isinstance(file_info.content, bytes):
            content_bytes = file_info.content
        else:
            content_bytes = file_info.content.encode(encoding)

        with open(local_path, "wb") as f:
            f.write(content_bytes)

    async def ls(self, path: str = ".") -> List[str]:
        """
        List directory contents asynchronously.

        Args:
            path: Path to list

        Returns:
            List of file/directory names
        """
        return await self.list_dir(path)

    async def rm(self, path: str, recursive: bool = False) -> None:
        """
        Remove file or directory asynchronously.

        Args:
            path: Path to remove
            recursive: Remove recursively
        """
        executor = self._get_async_executor()
        path_escaped = escape_shell_arg(path)

        if recursive:
            result = await executor(f"rm -rf {path_escaped}")
        else:
            result = await executor(f"rm {path_escaped}")

        if not result.success:
            raise _executor_error(
                result.stderr, "remove", not_found_msg=f"File not found: {path}"
            )

    def open(
        self, path: str, mode: str = "r", encoding: str = "utf-8"
    ) -> AsyncSandboxFileIO:
        """
        Open a file in the sandbox asynchronously.

        Args:
            path: Path to the file
            mode: Open mode ('r', 'w', 'a', etc.)
            encoding: File encoding (default: "utf-8"). Use "base64" for binary data.

        Returns:
            AsyncSandboxFileIO: Async file handle
        """
        return AsyncSandboxFileIO(self, path, mode, encoding)

    async def sync(
        self,
        local: str,
        remote: Optional[str] = None,
        *,
        direction: str = "push",
        delete: bool = False,
        exclude: Sequence[str] = (),
        checksum: bool = False,
        dry_run: bool = False,
    ) -> Dict[str, int]:
        """
        Sync a directory with the sandbox, one way like ``rsync -r``.

        Both sides are listed (a local walk against the executor's
        NDJSON listing) and diffed on path, type, size and mtime —
        whole seconds, like rsync's default; ``checksum=True`` adds a
        sha256 comparison for files that pass that test. On push, the
        changed set travels as ~50 MiB gzip'd tar batches through
        /files/archive; on pull, the remote tree's archive streams down
        and only the changed set is extracted. Files larger than one
        batch go through upload_file/download_file instead (multipart
        on executors v0.0.24+, resumable downloads), and a pull's
        archive leaves them out so their bytes travel once.
        Symlinks travel as links, modes are kept, owners are not. A pull
        never writes outside local: a path that leaves it, or that goes
        through a symlink, fails the sync.

        A no-op sync sends nothing: nothing is transferred or deleted;
        beyond the listing only ``checksum=True`` asks more — one sha256
        stat per size-and-mtime-equal file. With ``delete=True`` the
        destination is pruned to match (a directory counts as one
        deletion); deletes ride the legacy routes, which every executor
        serves. ``dry_run=True`` computes the result without touching
        either side.

        Args:
            local: Local directory path
            remote: Destination path in the sandbox; relative paths
                resolve under the sandbox workdir. None uses local's
                relative form (its basename when absolute), rsync-style
            direction: "push" (local → sandbox) or "pull" (sandbox → local)
            delete: Remove destination entries absent from the source
            exclude: Glob patterns; a matching path (or any /-separated
                suffix of it) is skipped, a matching directory whole
            checksum: Compare sha256 for size-and-mtime-equal files
            dry_run: Compute the plan only, transfer nothing

        Returns:
            {"uploaded"|"downloaded", "deleted", "skipped", "bytes"}

        Raises:
            SandboxFilesystemError: On any failure, the filesystem taxonomy
        """
        if direction not in ("push", "pull"):
            raise ValueError(f"direction must be 'push' or 'pull', not {direction!r}")
        if remote is None:
            remote = relative_remote(local)
        client = self._get_async_client()
        if not await client.has_files_routes():
            raise SandboxFilesystemError(
                "sync requires executor v0.0.24+ (the streamed /files "
                "routes); this sandbox's executor is older"
            )
        with _translating_files_errors(f"sync {direction}", local):
            if direction == "push":
                return await self._sync_push(
                    local, remote, client, delete, exclude, checksum, dry_run
                )
            return await self._sync_pull(
                local, remote, client, delete, exclude, checksum, dry_run
            )

    async def _sync_push(
        self,
        local: str,
        remote: str,
        client: AsyncSandboxClient,
        delete: bool,
        exclude: Sequence[str],
        checksum: bool,
        dry_run: bool,
    ) -> Dict[str, int]:
        local_entries = walk_local(local, exclude)
        try:
            remote_entries = [
                entry async for entry in client.files_list(remote, recursive=True)
            ]
        except SandboxRequestError as e:
            # A missing remote tree is an empty one: the archive PUT
            # creates the root (MkdirAll), like rsync creating its dest.
            if e.status_code != 404:
                raise
            remote_entries = []
        # Excluded remote paths stay invisible to the diff: delete must
        # spare what exclude promised to skip.
        remote_entries = [
            e for e in remote_entries if not path_excluded(e["path"], exclude)
        ]

        hashes = await self._sync_hashes(
            client, local, remote, checksum, False, local_entries, remote_entries
        )
        result = diff(local_entries, remote_entries, delete=delete, **hashes)
        batches, oversized = plan_batches(result.to_transfer, SYNC_BATCH_BYTES)
        if not dry_run:
            for batch in batches:
                fd, spool = tempfile.mkstemp(suffix=".koyeb-sync.tgz")
                os.close(fd)
                try:
                    build_archive(local, batch, spool)
                    with open(spool, "rb") as f:
                        await client.files_archive_put(remote, f)
                finally:
                    with suppress(OSError):
                        os.unlink(spool)
            for entry in oversized:
                await self.upload_file(
                    join_local(local, entry["path"]),
                    remote_join(remote, entry["path"]),
                )
            deleted = await self._sync_remote_deletes(remote, result, delete)
        else:
            deleted = len(prune_descendants([e["path"] for e in result.deletes]))
        return {
            "uploaded": len(result.to_transfer),
            "deleted": deleted,
            "skipped": result.skipped,
            "bytes": result.bytes,
        }

    async def _sync_pull(
        self,
        local: str,
        remote: str,
        client: AsyncSandboxClient,
        delete: bool,
        exclude: Sequence[str],
        checksum: bool,
        dry_run: bool,
    ) -> Dict[str, int]:
        # A missing destination root is an empty tree: extraction
        # creates it, like rsync creating its dest on pull.
        local_entries = walk_local(local, exclude) if os.path.isdir(local) else []
        remote_entries = [
            entry async for entry in client.files_list(remote, recursive=True)
        ]
        # The source listing gets the same filter as the local walk: an
        # excluded path is neither planned nor counted.
        remote_entries = [
            e for e in remote_entries if not path_excluded(e["path"], exclude)
        ]
        # The listing comes from the sandbox: refuse a path that would land
        # outside local before anything is written.
        for entry in remote_entries:
            clean_path(entry["path"])
        hashes = await self._sync_hashes(
            client, local, remote, checksum, True, remote_entries, local_entries
        )
        result = diff(remote_entries, local_entries, delete=delete, **hashes)
        batches, oversized = plan_batches(result.to_transfer, SYNC_BATCH_BYTES)
        # Oversized files ride download_file; the archive leaves them out
        # so their bytes travel once.
        archive_exclude = tuple(exclude) + tuple(e["path"] for e in oversized)
        # Archive excludes are glob patterns: an oversized name would
        # also drop same-suffixed planned members — refuse loudly.
        oversized_patterns = tuple(e["path"] for e in oversized)
        colliding = sorted(
            {
                entry["path"]
                for batch in batches
                for entry in batch
                if path_excluded(entry["path"], oversized_patterns)
            }
        )
        if colliding:
            raise SandboxFilesystemError(
                f"sync pull cannot deliver {colliding}: the archive exclude "
                f"for oversized files would also drop them; rename or sync "
                f"them separately"
            )
        if not dry_run:
            if batches:
                fd, spool = tempfile.mkstemp(suffix=".koyeb-sync.tgz")
                os.close(fd)
                try:
                    with open(spool, "wb") as out:
                        async for chunk in client.files_archive_get(
                            remote, archive_exclude
                        ):
                            out.write(chunk)
                    keep = {entry["path"] for batch in batches for entry in batch}
                    extract_archive(spool, local, keep=keep)
                finally:
                    with suppress(OSError):
                        os.unlink(spool)
            for entry in oversized:
                await self.download_file(
                    remote_join(remote, entry["path"]),
                    join_local(local, entry["path"]),
                )
            deleted = self._sync_local_deletes(local, result, delete)
        else:
            deleted = len(prune_descendants([e["path"] for e in result.deletes]))
        return {
            "downloaded": len(result.to_transfer),
            "deleted": deleted,
            "skipped": result.skipped,
            "bytes": result.bytes,
        }

    async def _sync_hashes(
        self,
        client: AsyncSandboxClient,
        local: str,
        remote: str,
        checksum: bool,
        pull: bool,
        source_entries: List[Dict[str, Any]],
        dest_entries: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """diff()'s hash callables, with the executor side prefetched.

        In diff()'s terms the source is always `local_entries`: on push
        that is the local tree, on pull the remote one. The executor-side
        digests are gathered in one pass — the pure, synchronous diff
        cannot await — and a vanished file (404) hashes as None:
        unprovable, not changed.
        """
        if not checksum:
            return {}

        async def fetch(path: str):
            try:
                entry = await client.files_stat(
                    remote_join(remote, path), hash="sha256"
                )
            except SandboxRequestError as e:
                if e.status_code != 404:
                    raise
                return path, None
            return path, (entry or {}).get("sha256")

        stats = dict(
            await asyncio.gather(
                *(fetch(path) for path in hash_candidates(source_entries, dest_entries))
            )
        )

        def executor_sha(path: str) -> Optional[str]:
            return stats.get(path)

        def disk_sha(path: str) -> str:
            return _file_sha256(join_local(local, path))

        if pull:
            # The remote tree is diff()'s source side on pull.
            return {"local_hash": executor_sha, "remote_hash": disk_sha}
        return {"local_hash": disk_sha, "remote_hash": executor_sha}

    async def _sync_remote_deletes(
        self, remote: str, result: SyncDiff, delete: bool
    ) -> int:
        if not delete:
            return 0
        by_path = {e["path"]: e for e in result.deletes}
        count = 0
        for path in prune_descendants(list(by_path)):
            try:
                if by_path[path].get("type") == "dir":
                    await self.delete_dir(remote_join(remote, path))
                else:
                    await self.delete_file(remote_join(remote, path))
            except SandboxFileNotFoundError:
                # A type flip earlier in this sync may have replaced the
                # path's parent; being already gone is the wanted state.
                pass
            count += 1
        return count

    def _sync_local_deletes(self, local: str, result: SyncDiff, delete: bool) -> int:
        """Local pruning is plain filesystem work — no await, but the
        signature matches the sync twin so the parity sweep holds."""
        if not delete:
            return 0
        by_path = {e["path"]: e for e in result.deletes}
        count = 0
        for path in prune_descendants(list(by_path)):
            try:
                target = join_local(local, path)
            except ValueError:
                # A type flip's extract replaced a parent with a symlink:
                # the path is gone from the tree, never delete through it.
                count += 1
                continue
            try:
                if os.path.isdir(target) and not os.path.islink(target):
                    shutil.rmtree(target)
                else:
                    os.unlink(target)
            except (FileNotFoundError, NotADirectoryError):
                # A type flip's extract may have replaced the parent
                # already; being gone is the wanted state.
                pass
            count += 1
        return count


class SandboxFileIO:
    """Synchronous file I/O handle for sandbox files"""

    def __init__(
        self,
        filesystem: SandboxFilesystem,
        path: str,
        mode: str,
        encoding: str = "utf-8",
    ):
        self.filesystem = filesystem
        self.path = path
        self.mode = mode
        self.encoding = encoding
        self._closed = False

    def read(self) -> Union[str, bytes]:
        """Read file content synchronously"""
        if "r" not in self.mode:
            raise ValueError("File not opened for reading")

        if self._closed:
            raise ValueError("File is closed")

        file_info = self.filesystem.read_file(self.path, encoding=self.encoding)
        return file_info.content

    def write(self, content: Union[str, bytes]) -> None:
        """Write content to file synchronously"""
        if "w" not in self.mode and "a" not in self.mode:
            raise ValueError("File not opened for writing")

        if self._closed:
            raise ValueError("File is closed")

        if "a" in self.mode:
            try:
                existing = self.filesystem.read_file(self.path, encoding=self.encoding)
                if isinstance(existing.content, bytes) and isinstance(content, bytes):
                    content = existing.content + content
                elif isinstance(existing.content, str) and isinstance(content, str):
                    content = existing.content + content
                else:
                    raise TypeError("Cannot mix bytes and str content in append mode")
            except SandboxFileNotFoundError:
                pass

        self.filesystem.write_file(self.path, content, encoding=self.encoding)

    def close(self) -> None:
        """Close the file"""
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncSandboxFileIO:
    """Async file I/O handle for sandbox files"""

    def __init__(
        self,
        filesystem: AsyncSandboxFilesystem,
        path: str,
        mode: str,
        encoding: str = "utf-8",
    ):
        self.filesystem = filesystem
        self.path = path
        self.mode = mode
        self.encoding = encoding
        self._closed = False

    async def read(self) -> Union[str, bytes]:
        """Read file content asynchronously"""
        if "r" not in self.mode:
            raise ValueError("File not opened for reading")

        if self._closed:
            raise ValueError("File is closed")

        file_info = await self.filesystem.read_file(self.path, encoding=self.encoding)
        return file_info.content

    async def write(self, content: Union[str, bytes]) -> None:
        """Write content to file asynchronously"""
        if "w" not in self.mode and "a" not in self.mode:
            raise ValueError("File not opened for writing")

        if self._closed:
            raise ValueError("File is closed")

        if "a" in self.mode:
            try:
                existing = await self.filesystem.read_file(
                    self.path, encoding=self.encoding
                )
                if isinstance(existing.content, bytes) and isinstance(content, bytes):
                    content = existing.content + content
                elif isinstance(existing.content, str) and isinstance(content, str):
                    content = existing.content + content
                else:
                    raise TypeError("Cannot mix bytes and str content in append mode")
            except SandboxFileNotFoundError:
                pass

        await self.filesystem.write_file(self.path, content, encoding=self.encoding)

    def close(self) -> None:
        """Close the file"""
        self._closed = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
