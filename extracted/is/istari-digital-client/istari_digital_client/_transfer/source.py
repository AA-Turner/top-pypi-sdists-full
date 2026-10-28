"""Byte sources for uploads: bounded slice readers, part sources, fingerprints, hashing.

Readers expose ``read``/``readinto``/``seek``/``tell``/``__len__`` so the HTTP layer
can send an exact ``Content-Length`` and rewind on retry. A short read is an error,
never a silent under-send.
"""

from __future__ import annotations

import io
import os
import threading
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Protocol, Union, cast

from typing_extensions import Self

from istari_digital_client import native_crypto
from istari_digital_client._transfer.errors import (
    FileChangedDuringUploadError,
    SourceReadError,
    TransferCancelledError,
)
from istari_digital_client._transfer.events import (
    EventKind,
    ProgressCallback,
    TransferEvent,
    emit,
)

HASH_CHUNK = 8 * 1024 * 1024
PathLike = Union[str, "os.PathLike[str]", Path]

# Anything with is_set(); None means never cancelled.
CancelLike = threading.Event | None


def _check_cancel(*events: CancelLike) -> None:
    for event in events:
        if event is not None and event.is_set():
            raise TransferCancelledError("transfer cancelled")


@dataclass(frozen=True)
class Fingerprint:
    """Size and mtime (ns) of a file, taken before it is hashed.

    Both fields exist on Linux, macOS and Windows. mtime resolution is the
    filesystem's (1 s on HFS+/ext3, 2 s on FAT). A same-size rewrite with the same
    or restored mtime evades detection. This is not a digest guarantee: short-read
    checks detect truncation, not same-size content changes.
    """

    size: int
    mtime_ns: int

    def verify(self, path: PathLike) -> None:
        """Raise ``FileChangedDuringUploadError`` if ``path`` no longer matches."""
        current = fingerprint(path)
        if current != self:
            raise FileChangedDuringUploadError(
                f"{os.fspath(path)} changed during upload "
                f"(size {self.size}->{current.size}, mtime_ns {self.mtime_ns}->{current.mtime_ns})"
            )


def fingerprint(path: PathLike) -> Fingerprint:
    """Snapshot ``path``'s size and mtime."""
    try:
        st = os.stat(path)
    except OSError as exc:
        raise SourceReadError(os.fspath(path), exc) from exc
    return Fingerprint(size=st.st_size, mtime_ns=st.st_mtime_ns)


class Reader(Protocol):
    """A rewindable, sized byte reader handed to the HTTP layer as a request body."""

    def read(self, n: int = -1) -> bytes: ...

    def seek(self, pos: int, whence: int = io.SEEK_SET) -> int: ...

    def tell(self) -> int: ...

    def __len__(self) -> int: ...

    def close(self) -> None: ...


class _SliceReader:
    """Shared cursor logic over a ``length``-byte window."""

    def __init__(self, length: int, *cancel: CancelLike) -> None:
        if length < 0:
            raise ValueError("length must be non-negative")
        self._length = length
        self._pos = 0
        self._cancel = cancel

    def __len__(self) -> int:
        return self._length

    def tell(self) -> int:
        """Current offset within the slice."""
        return self._pos

    def seek(self, pos: int, whence: int = io.SEEK_SET) -> int:
        """Move within the slice (absolute, relative, or from its end)."""
        if whence == io.SEEK_SET:
            target = pos
        elif whence == io.SEEK_CUR:
            target = self._pos + pos
        elif whence == io.SEEK_END:
            target = self._length + pos
        else:
            raise ValueError(f"invalid whence {whence}")
        if target < 0:
            raise ValueError("negative seek position")
        self._pos = min(target, self._length)
        return self._pos

    def _remaining(self) -> int:
        return self._length - self._pos

    def _want(self, n: int) -> int:
        _check_cancel(*self._cancel)
        return self._remaining() if n is None or n < 0 else min(n, self._remaining())

    def close(self) -> None:
        """Release underlying resources (no-op by default)."""

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class FileSliceReader(_SliceReader):
    """Reads ``length`` bytes of ``path`` starting at ``offset``; short reads raise."""

    def __init__(
        self, path: PathLike, offset: int, length: int, *cancel: CancelLike
    ) -> None:
        """Open ``path`` and position the window; the file stays open until ``close``."""
        super().__init__(length, *cancel)
        self._path = os.fspath(path)
        self._offset = offset
        # Unbuffered: a BufferedReader (128 KiB on 3.14) would serve stale bytes after
        # the file is truncated, hiding the short read this class exists to detect.
        _check_cancel(*self._cancel)
        try:
            self._file: io.FileIO | None = open(self._path, "rb", buffering=0)  # noqa: SIM115 - closed in close()
        except OSError as exc:
            raise SourceReadError(self._path, exc) from exc

    def _short(self, wanted: int, got: int) -> FileChangedDuringUploadError:
        return FileChangedDuringUploadError(
            f"{self._path}: short read at offset {self._offset + self._pos} "
            f"(wanted {wanted}, got {got}); the file changed during upload"
        )

    def readinto(self, buffer: bytearray | memoryview) -> int:
        """Fill ``buffer`` from the slice; returns bytes copied (0 at end of slice)."""
        if self._file is None:
            raise ValueError("reader is closed")
        view = memoryview(buffer)
        want = self._want(view.nbytes)
        if want == 0:
            return 0
        target = view[:want]
        filled = 0
        try:
            self._file.seek(self._offset + self._pos)
            while filled < want:
                _check_cancel(*self._cancel)
                got = self._file.readinto(target[filled:])
                if not got:
                    raise self._short(want, filled)
                filled += got
        except OSError as exc:
            raise SourceReadError(self._path, exc) from exc
        self._pos += filled
        return filled

    def read(self, n: int = -1) -> bytes:
        """Read up to ``n`` bytes (all remaining when negative)."""
        want = self._want(n)
        if want == 0:
            return b""
        buf = bytearray(want)
        self.readinto(buf)
        return bytes(buf)

    def close(self) -> None:
        """Close the underlying file."""
        if self._file is not None:
            self._file.close()
            self._file = None


class BytesSliceReader(_SliceReader):
    """Reads from an in-memory buffer (properties JSON, secret ciphertext, buffered parts)."""

    def __init__(
        self, data: bytes | bytearray | memoryview, *cancel: CancelLike
    ) -> None:
        """Wrap ``data`` without copying."""
        self._view = memoryview(data)
        super().__init__(self._view.nbytes, *cancel)

    def readinto(self, buffer: bytearray | memoryview) -> int:
        """Copy the next bytes of the buffer into ``buffer``."""
        view = memoryview(buffer)
        want = self._want(view.nbytes)
        if want == 0:
            return 0
        view[:want] = self._view[self._pos : self._pos + want]
        self._pos += want
        return want

    def read(self, n: int = -1) -> bytes:
        """Read up to ``n`` bytes (all remaining when negative)."""
        want = self._want(n)
        if want == 0:
            return b""
        chunk = self._view[self._pos : self._pos + want].tobytes()
        self._pos += want
        return chunk


class PartSource(Protocol):
    """Where upload parts come from.

    Contract: the engine opens each part exactly once, in ascending order, from a
    single dispatcher thread, keeps at most ``concurrency + k`` parts alive, and
    rewinds the returned reader (``seek(0)``) on retry. Part numbers need not be
    contiguous: a resumed upload skips the parts that already landed. A source may
    also define ``drain()``: the engine calls it before a ``before_complete`` hook to
    read whatever the upload skipped (landed parts, or all of an object that exists).
    """

    @property
    def size(self) -> int: ...

    def open_part(self, part_number: int, offset: int, length: int) -> Reader: ...


def _drain_reader(reader: Reader, *cancel: CancelLike) -> None:
    """Read and discard a whole source in bounded, cancellable chunks."""
    _check_cancel(*cancel)
    remaining = len(reader) - reader.tell()
    while remaining:
        _check_cancel(*cancel)
        got = len(reader.read(min(HASH_CHUNK, remaining)))
        if not got:
            raise FileChangedDuringUploadError(
                f"source ended with {remaining} bytes still expected"
            )
        remaining -= got
    _check_cancel(*cancel)


class BytesPartSource:
    """Parts are windows of an in-memory buffer."""

    def __init__(
        self, data: bytes | bytearray | memoryview, *cancel: CancelLike
    ) -> None:
        """Wrap ``data`` and retain all supplied cancellation events."""
        self._view = memoryview(data)
        self._cancel = cancel

    @property
    def size(self) -> int:
        """Size of the source buffer."""
        return self._view.nbytes

    def open_part(self, part_number: int, offset: int, length: int) -> BytesSliceReader:
        """Open a reader over one buffer window."""
        if offset < 0 or length < 0 or offset + length > self.size:
            raise ValueError("part range is outside the source buffer")
        return BytesSliceReader(self._view[offset : offset + length], *self._cancel)

    def drain(self, cancel: CancelLike = None) -> None:
        """Check cancellation before a whole-source hook; bytes are already resident."""
        _check_cancel(*self._cancel, cancel)


class FilePartSource:
    """Parts are windows of one file on disk."""

    def __init__(self, path: PathLike, *cancel: CancelLike) -> None:
        """Record the path; the size is taken now."""
        self._path = Path(path)
        self._cancel = cancel
        _check_cancel(*self._cancel)
        self._fingerprint = fingerprint(self._path)
        self._size = self._fingerprint.size

    @property
    def path(self) -> Path:
        """The source file."""
        return self._path

    @property
    def size(self) -> int:
        """Size of the file when the source was created."""
        return self._size

    def open_part(self, part_number: int, offset: int, length: int) -> FileSliceReader:
        """Open a fresh reader over one part."""
        return FileSliceReader(self._path, offset, length, *self._cancel)

    def drain(self, cancel: CancelLike = None) -> None:
        """Read and discard the whole file before a hook, using bounded memory."""
        _check_cancel(*self._cancel, cancel)
        with self.open_part(1, 0, self.size) as reader:
            _drain_reader(reader, *self._cancel, cancel)


def replay_source(source: PartSource, cancel: CancelLike = None) -> PartSource | None:
    """Prepare only known built-in sources for another bounded-memory attempt.

    Never infer replay safety from a custom source's methods, even a subclass of
    a built-in source. File replay checks the original fingerprint; readers and
    cancellation events are retained, with no whole-content copy or spool.
    """
    _check_cancel(cancel)
    if type(source) is FilePartSource:
        _check_cancel(*source._cancel)
        source._fingerprint.verify(source.path)
        return source
    if type(source) is BytesPartSource:
        _check_cancel(*source._cancel)
        return source
    return None


class BufferedStreamPartSource:
    """Parts are read sequentially from a non-seekable stream into part-sized buffers.

    Buffers are pooled: a reader's ``close()`` hands its buffer back for the next
    part. The dispatcher retains at most ``2 x concurrency`` part buffers; while
    producing a new reader it may temporarily hold one additional buffer. Memory
    is bounded by roughly ``part_size x (2 x concurrency + 1)`` plus read/copy
    overhead, not by total object size. The stream must deliver exactly ``size`` bytes: a
    short read raises ``FileChangedDuringUploadError`` and extra bytes after the last
    part are also rejected.
    """

    def __init__(self, stream: BinaryIO, size: int, *cancel: CancelLike) -> None:
        """Wrap ``stream`` (anything with ``readinto`` or ``read``) declaring ``size`` bytes."""
        if size < 0:
            raise ValueError("size must be non-negative")
        self._stream = stream
        self._size = size
        self._cancel = cancel
        self._next_offset = 0
        self._at_eof = False
        self._pool: list[bytearray] = []
        self._pool_lock = threading.Lock()

    @property
    def size(self) -> int:
        """Declared stream length."""
        return self._size

    def _take_buffer(self, length: int) -> bytearray:
        with self._pool_lock:
            for i, buf in enumerate(self._pool):
                if len(buf) >= length:
                    return self._pool.pop(i)
        return bytearray(length)

    def _release(self, buf: bytearray) -> None:
        with self._pool_lock:
            self._pool.append(buf)

    def _readinto(self, view: memoryview) -> int:
        """Use the stream's supported read method, including for the EOF probe."""
        _check_cancel(*self._cancel)
        readinto = getattr(self._stream, "readinto", None)
        if callable(readinto):
            got = cast(Callable[[memoryview], int | None], readinto)(view)
        else:
            chunk = self._stream.read(len(view))
            got = len(chunk)
            view[:got] = chunk
        _check_cancel(*self._cancel)
        return got or 0

    def _read_exact(self, view: memoryview) -> None:
        filled = 0
        while filled < len(view):
            got = self._readinto(view[filled:])
            if not got:
                raise FileChangedDuringUploadError(
                    f"stream ended after {self._next_offset + filled} bytes; expected {self._size}"
                )
            filled += got

    def _skip(self, count: int) -> None:
        # Landed parts of a resumed upload: consume them off the stream and drop them.
        # Going through _read_exact keeps the short-stream error for a truncated resume.
        scratch = memoryview(bytearray(min(count, HASH_CHUNK)))
        while count > 0:
            view = scratch[: min(count, len(scratch))]
            self._read_exact(view)
            self._next_offset += len(view)
            count -= len(view)

    def open_part(self, part_number: int, offset: int, length: int) -> BytesSliceReader:
        """Read the next part off the stream; parts must be requested in ascending order."""
        if offset < self._next_offset:
            raise ValueError(
                f"parts must be opened in ascending order (stream is at offset {self._next_offset}, got {offset})"
            )
        _check_cancel(*self._cancel)
        if length < 0 or offset + length > self._size:
            raise ValueError("part range is outside the declared stream size")
        if offset > self._next_offset:
            self._skip(offset - self._next_offset)
        buf = self._take_buffer(length)
        try:
            self._read_exact(memoryview(buf)[:length])
            self._next_offset += length
            if self._next_offset == self._size:
                self._check_eof()
        except BaseException:
            self._release(buf)
            raise
        return _PooledSliceReader(buf, length, self._release, *self._cancel)

    def _check_eof(self) -> None:
        _check_cancel(*self._cancel)
        if not self._at_eof:
            if self._readinto(memoryview(bytearray(1))):
                raise FileChangedDuringUploadError(
                    f"stream has more than the declared {self._size} bytes"
                )
            self._at_eof = True

    def drain(self) -> None:
        """Read and drop the rest of the stream, checking it ends at the declared size."""
        self._skip(self._size - self._next_offset)
        self._check_eof()


class _PooledSliceReader(BytesSliceReader):
    """A ``BytesSliceReader`` whose ``close()`` returns its buffer to the source's pool."""

    def __init__(
        self,
        buf: bytearray,
        length: int,
        release: Callable[[bytearray], None],
        *cancel: CancelLike,
    ) -> None:
        """Wrap the first ``length`` bytes of ``buf``."""
        super().__init__(memoryview(buf)[:length], *cancel)
        self._buf: bytearray | None = buf
        self._release_fn = release

    def close(self) -> None:
        """Drop the view and hand the buffer back for reuse."""
        buf, self._buf = self._buf, None
        if buf is not None:
            self._view.release()
            self._release_fn(buf)

    def readinto(self, buffer: bytearray | memoryview) -> int:
        """Copy the next bytes into ``buffer``; a closed reader yields nothing."""
        if self._buf is None:
            return 0
        return super().readinto(buffer)

    def read(self, n: int = -1) -> bytes:
        """Read up to ``n`` bytes; a closed reader yields nothing."""
        if self._buf is None:
            return b""
        return super().read(n)


def hash_file(
    path: PathLike,
    salt: str | None,
    *,
    expected: Fingerprint | None = None,
    cancel: CancelLike = None,
    progress: ProgressCallback | None = None,
    between_chunks: Callable[[], None] | None = None,
) -> native_crypto.Token:
    """One streaming pass over ``path`` through ``native_crypto.Hasher``.

    Uses a single reused 8 MiB buffer. ``expected`` (the fingerprint taken before
    hashing) makes a size change fail loudly instead of hashing a moving target.
    ``between_chunks`` is a test hook.
    """
    hasher = native_crypto.Hasher(salt)
    _check_cancel(cancel)
    total = expected.size if expected is not None else fingerprint(path).size
    buf = bytearray(HASH_CHUNK)
    view = memoryview(buf)
    done = 0
    # Unbuffered: the 8 MiB readinto loop gains nothing from a BufferedReader.
    try:
        source_file = open(path, "rb", buffering=0)  # noqa: SIM115 - closed by context manager below
    except OSError as exc:
        raise SourceReadError(os.fspath(path), exc) from exc
    with source_file as f:
        while True:
            _check_cancel(cancel)
            try:
                got = f.readinto(view)
            except OSError as exc:
                raise SourceReadError(os.fspath(path), exc) from exc
            if not got:
                break
            hasher.update(view[:got])
            done += got
            emit(progress, TransferEvent(EventKind.HASH_PROGRESS, done, total))
            if between_chunks is not None:
                between_chunks()
    if done != total:
        raise FileChangedDuringUploadError(
            f"{os.fspath(path)}: hashed {done} bytes but expected {total}; the file changed"
        )
    return hasher.finalize()
