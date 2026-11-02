"""Streaming hashes shared by local and OSS operations; SDK imports stay lazy."""

from __future__ import annotations

import base64
import binascii
import errno
import hashlib
import io
import os
import re
import stat
from copy import copy
from pathlib import Path

from .ossutil_io import OssOperationError, OssUsageError, safe_error

_CHUNK_SIZE = 1024 * 1024
_CRC64_MASK = (1 << 64) - 1
_CRC64_POLY = 0xC96C5795D7870F42


def _crc64_table() -> tuple[int, ...]:
    table = []
    for byte in range(256):
        value = byte
        for _ in range(8):
            value = (value >> 1) ^ (_CRC64_POLY if value & 1 else 0)
        table.append(value)
    return tuple(table)


_CRC64_TABLE = _crc64_table()


class _Crc64Xz:
    """Small streaming CRC-64/XZ accumulator independent of the OSS SDK."""

    def __init__(self) -> None:
        self._value = _CRC64_MASK

    def update(self, data: bytes) -> None:
        value = self._value
        for byte in data:
            value = _CRC64_TABLE[(value ^ byte) & 0xFF] ^ (value >> 8)
        self._value = value

    @property
    def crc(self) -> int:
        return self._value ^ _CRC64_MASK


def _validate_options(algorithm: str, base64_output: bool) -> None:
    if algorithm not in ("md5", "crc64"):
        raise OssUsageError("hash algorithm must be md5 or crc64")
    if base64_output and algorithm != "md5":
        raise OssUsageError("--base64 is only supported for md5")


def _metadata_hash(headers, algorithm: str, base64_output: bool = False) -> str | None:
    name = "content-md5" if algorithm == "md5" else "x-oss-hash-crc64ecma"
    value = next((v for k, v in headers.items() if k.lower() == name), None)
    if not isinstance(value, str):
        return None
    if algorithm == "crc64":
        if not re.fullmatch(r"[0-9]{1,20}", value) or int(value) >= 1 << 64:
            return None
        return str(int(value))
    try:
        digest = base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error):
        return None
    # Length and canonical encoding also reject nonzero padding bits.
    encoded = base64.b64encode(digest).decode("ascii")
    if len(digest) != 16 or encoded != value:
        return None
    return encoded if base64_output else digest.hex()


def _hash_stream(stream, algorithm: str, base64_output: bool = False) -> tuple[str, int]:
    accumulator = hashlib.md5() if algorithm == "md5" else _Crc64Xz()
    size = 0
    while data := stream.read(_CHUNK_SIZE):
        accumulator.update(data)
        size += len(data)
    if algorithm == "crc64":
        return str(accumulator.crc), size
    digest = accumulator.digest()
    return (base64.b64encode(digest).decode("ascii") if base64_output else digest.hex()), size


def _header(headers, name: str):
    if headers is None:
        return None
    return next((value for key, value in headers.items() if key.lower() == name), None)


class _StoredBytesStream:
    def __init__(self, raw) -> None:
        self._raw = raw

    def read(self, size: int):
        return self._raw.read(size, decode_content=False)


def _stored_content_stream(result, *, content_encoded: bool = False):
    """Return a read-only view of stored bytes, bypassing SDK HTTP decoding."""
    response = getattr(getattr(result, "resp", None), "response", None)
    raw = getattr(response, "raw", None)
    if callable(getattr(raw, "read", None)):
        return _StoredBytesStream(raw)
    headers = getattr(result, "headers", None)
    response_headers = getattr(response, "headers", None)
    encoded = content_encoded or bool(
        _header(headers, "content-encoding") or _header(response_headers, "content-encoding")
    )
    if encoded:
        raise OssOperationError("Encoded hash response does not expose a raw stored-byte stream")
    return result


def _close_result(result) -> None:
    response = getattr(getattr(result, "resp", None), "response", None)
    if response is not None:
        response.close()
    else:
        close = getattr(result, "close", None)
        if callable(close):
            close()


def _hash_request(bucket, method: str, key: str, **kwargs):
    """Isolate oss2's eager CRC parsing to this read, never mutate transfer buckets.

    Both HEAD and GET constructors parse CRC with int() before returning a
    response. Drop invalid CRC headers at their per-request response boundary;
    own that response so constructor failures cannot leak a connection.
    """
    raw = getattr(bucket, "bucket", bucket)
    do_object = getattr(raw, "_Bucket__do_object", None)
    if not callable(do_object):
        return getattr(bucket, method)(key, **kwargs)
    isolated = copy(raw)
    if raw is bucket:
        routed = isolated
    else:
        from .ossutil_io import _RoutingBucket

        routed = _RoutingBucket(isolated, bucket.owner, bucket._ossutil_endpoint)
    do_object = isolated._Bucket__do_object
    responses = []

    def request(*args, **options):
        response = do_object(*args, **options)
        responses.append(response)
        if _metadata_hash(response.headers, "crc64") is None:
            response.headers = copy(response.headers)
            for name in list(response.headers):
                if name.lower() == "x-oss-hash-crc64ecma":
                    del response.headers[name]
        return response

    isolated._Bucket__do_object = request
    try:
        return getattr(routed, method)(key, **kwargs)
    except Exception:
        for response in responses:
            response.response.close()
        raise


_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
_DIRECTORY = getattr(os, "O_DIRECTORY", 0)
_CLOEXEC = getattr(os, "O_CLOEXEC", 0)
_DIR_FLAGS = os.O_RDONLY | _DIRECTORY | _NOFOLLOW | _CLOEXEC
_FILE_FLAGS = os.O_RDONLY | os.O_NONBLOCK | _NOFOLLOW | _CLOEXEC
_SECURE_LOCAL_HASH_SUPPORTED = bool(
    _NOFOLLOW
    and _DIRECTORY
    and hasattr(os, "fwalk")
    and os.open in os.supports_dir_fd
    and os.stat in os.supports_dir_fd
)


def _require_secure_local_hash() -> None:
    if not _SECURE_LOCAL_HASH_SUPPORTED:
        raise OssUsageError(
            "Secure local hash is not supported on this platform; use ans:// remote hash"
        )


def _open_error(exc: OSError):
    if exc.errno in (errno.ELOOP, errno.ENOTDIR):
        raise OssUsageError(
            "Hash input cannot contain symlinks or non-directory path components"
        ) from exc
    raise exc


def _open_path(path: Path, flags: int = _FILE_FLAGS) -> int:
    """Open every lexical path component relative to a stable parent dirfd."""
    parts = path.parts
    absolute = path.is_absolute()
    components = parts[1:] if absolute else parts
    try:
        current = os.open(path.anchor if absolute else ".", _DIR_FLAGS)
    except OSError as exc:
        _open_error(exc)
    try:
        for component in components[:-1]:
            try:
                child = os.open(component, _DIR_FLAGS, dir_fd=current)
            except OSError as exc:
                _open_error(exc)
            os.close(current)
            current = child
        if not components:
            return current
        try:
            target = os.open(components[-1], flags, dir_fd=current)
        except OSError as exc:
            _open_error(exc)
        os.close(current)
        return target
    except BaseException:
        os.close(current)
        raise


def _check_local(path: Path) -> None:
    fd = _open_path(path)
    os.close(fd)


def _hash_open_file(fd: int, display_path: Path, algorithm: str, base64_output: bool) -> dict:
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise OssUsageError("Hash input must be a regular file")
        stream = io.FileIO(fd, "rb", closefd=True)
        fd = -1
        with stream:
            value, size = _hash_stream(stream, algorithm, base64_output)
    finally:
        if fd >= 0:
            os.close(fd)
    return {
        "path": str(display_path),
        "algorithm": algorithm,
        "hash": value,
        "source": "content",
        "size": size,
    }


def _hash_file_at(
    parent_fd: int, name: str, display_path: Path, algorithm: str, base64_output: bool
) -> dict:
    try:
        fd = os.open(name, _FILE_FLAGS, dir_fd=parent_fd)
    except OSError as exc:
        _open_error(exc)
    return _hash_open_file(fd, display_path, algorithm, base64_output)


def _hash_file(path: Path, algorithm: str, base64_output: bool) -> dict:
    return _hash_open_file(_open_path(Path(path)), Path(path), algorithm, base64_output)


def hash_local(
    path: str | Path,
    algorithm: str,
    *,
    base64_output: bool = False,
    recursive: bool = False,
) -> dict:
    """Hash a regular file, or each file under a directory with recursive=True."""
    _validate_options(algorithm, base64_output)
    _require_secure_local_hash()
    local = Path(path)
    root_fd = _open_path(local)
    try:
        mode = os.fstat(root_fd).st_mode
        if stat.S_ISREG(mode):
            fd, root_fd = root_fd, -1
            return _hash_open_file(fd, local, algorithm, base64_output)
        if not stat.S_ISDIR(mode):
            raise OssUsageError("Hash input must be a regular file")
        if not recursive:
            raise OssUsageError("Hashing a directory requires -r/--recursive")
        entries, failed = [], []

        def failure(failed_path, exc):
            failed.append({"path": str(failed_path), "error": safe_error(exc)})

        def walk_error(exc):
            failure(local / (exc.filename or ""), exc)

        for relative, dirs, files, parent_fd in os.fwalk(
            ".",
            topdown=True,
            onerror=walk_error,
            follow_symlinks=False,
            dir_fd=root_fd,
        ):
            current = local if relative == "." else local / relative
            dirs.sort()
            files.sort()
            for name in list(dirs):
                child = current / name
                try:
                    child_mode = os.stat(name, dir_fd=parent_fd, follow_symlinks=False).st_mode
                except OSError as exc:
                    dirs.remove(name)
                    failure(child, exc)
                else:
                    if stat.S_ISLNK(child_mode):
                        dirs.remove(name)
                        failure(child, OssUsageError("Hash input cannot contain symlinks"))
            for name in files:
                child = current / name
                try:
                    entries.append(_hash_file_at(parent_fd, name, child, algorithm, base64_output))
                except Exception as exc:
                    failure(child, exc)
        return {"entries": entries, "failed": failed, "failed_count": len(failed)}
    finally:
        if root_fd >= 0:
            os.close(root_fd)
