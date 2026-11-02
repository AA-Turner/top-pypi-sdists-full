"""A file inside a sandbox, used like a local one."""

import contextlib
import io
import tempfile
from collections.abc import Iterator
from typing import IO, AnyStr, ClassVar, Generic, cast

from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_transport import SandboxTransport


class SandboxFile(Generic[AnyStr]):
    """A sandbox file opened by ``Sandbox.open`` for reading (``r``), writing (``w``) or appending (``a``).

    Reading downloads the whole file when it is opened, into memory while it is small and into a local
    temporary file beyond that, so a large file costs local disk rather than memory, and reads never wait for
    the host. Writing collects what is written locally and sends it on ``flush`` and ``close``, and by itself
    every 64 MiB. ``w`` empties the file as it opens and ``a`` keeps what it holds; both create a missing
    file. Text modes read and write UTF-8; a ``b`` mode reads and writes bytes.
    """

    MODES: ClassVar[frozenset[str]] = frozenset({"r", "rb", "w", "wb", "a", "ab"})
    PIECE_BYTES: ClassVar[int] = 67_108_864
    SPOOL_BYTES: ClassVar[int] = 8_388_608
    TRANSFER_SECONDS: ClassVar[float] = 600.0

    def __init__(self, transport: SandboxTransport, files: str, path: str, mode: str, kind: type[AnyStr]) -> None:
        """Bind the sandbox's file path on its host, the file, the mode and whether values are text or bytes."""
        if mode not in self.MODES:
            raise ValueError(f"mode must be one of {', '.join(sorted(self.MODES))}, not {mode!r}")
        self.path = path
        self.mode = mode
        self._transport = transport
        self._files = files
        self._kind: type[AnyStr] = kind
        with contextlib.ExitStack() as copies:
            self._spool = copies.enter_context(tempfile.SpooledTemporaryFile(max_size=self.SPOOL_BYTES))
            self._copies = copies.pop_all()
        self._reader: IO[AnyStr] | None = None
        self._sent = 0
        self._closed = False

    def prepare(self) -> "SandboxFile[AnyStr]":
        """Download a file opened for reading, or create one opened for writing, emptying it for ``w``."""
        if self.mode.startswith("r"):
            with self._transport.stream(self._read_request()) as body:
                for chunk in body:
                    self._spool.write(chunk)
            return self._downloaded()
        self._transport.send(self._write_request(b"", self.mode.startswith("a")))
        return self

    async def prepare_async(self) -> "SandboxFile[AnyStr]":
        """Download or create the file without blocking the event loop; see ``prepare``."""
        if self.mode.startswith("r"):
            async with self._transport.stream_async(self._read_request()) as body:
                async for chunk in body:
                    self._spool.write(chunk)
            return self._downloaded()
        await self._transport.send_async(self._write_request(b"", self.mode.startswith("a")))
        return self

    def read(self, size: int = -1) -> AnyStr:
        """Return up to ``size`` characters or bytes, or the rest of the file."""
        return self._readable().read(size)

    def readline(self, size: int = -1) -> AnyStr:
        """Return the next line, with its newline."""
        return self._readable().readline(size)

    def readlines(self) -> list[AnyStr]:
        """Return the remaining lines."""
        return self._readable().readlines()

    def __iter__(self) -> Iterator[AnyStr]:
        """Yield the remaining lines."""
        return iter(self._readable())

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        """Move the reading position as a local file does."""
        return self._readable().seek(offset, whence)

    def tell(self) -> int:
        """Return the reading position."""
        return self._readable().tell()

    def write(self, data: AnyStr) -> int:
        """Add text or bytes to the file, sending what has collected once it reaches 64 MiB."""
        if self._collected(data) >= self.PIECE_BYTES:
            self.flush()
        return len(data)

    async def write_async(self, data: AnyStr) -> int:
        """Write without blocking the event loop when collected bytes are sent; see ``write``."""
        if self._collected(data) >= self.PIECE_BYTES:
            await self.flush_async()
        return len(data)

    def flush(self) -> None:
        """Send what was written since the last flush to the end of the sandbox file."""
        for piece in self._pieces():
            self._transport.send(self._write_request(piece, True))

    async def flush_async(self) -> None:
        """Send what was written without blocking the event loop; see ``flush``."""
        for piece in self._pieces():
            await self._transport.send_async(self._write_request(piece, True))

    def close(self) -> None:
        """Send what is left to write and let go of the local copy; closing again does nothing."""
        if self._closed:
            return
        try:
            self.flush()
        finally:
            self._release()

    async def close_async(self) -> None:
        """Close without blocking the event loop; see ``close``."""
        if self._closed:
            return
        try:
            await self.flush_async()
        finally:
            self._release()

    def __enter__(self) -> "SandboxFile[AnyStr]":
        """Use the file for the length of a block."""
        return self

    def __exit__(self, *_failure: object) -> None:
        """Close the file when the block ends, however it ends."""
        self.close()

    async def __aenter__(self) -> "SandboxFile[AnyStr]":
        """Use the file for the length of an asynchronous block."""
        return self

    async def __aexit__(self, *_failure: object) -> None:
        """Close the file when the asynchronous block ends, however it ends."""
        await self.close_async()

    def _downloaded(self) -> "SandboxFile[AnyStr]":
        """Read the downloaded copy from its start, decoding it when the mode is text."""
        self._spool.seek(0)
        text = self._kind is str
        decoded = (
            self._copies.enter_context(io.TextIOWrapper(self._spool, encoding="utf-8", errors="replace"))
            if text
            else None
        )
        self._reader = cast("IO[AnyStr]", decoded or self._spool)
        return self

    def _readable(self) -> IO[AnyStr]:
        """Return the downloaded copy; a file opened for writing has none to read."""
        if self._reader is None:
            raise io.UnsupportedOperation(f"{self.path} is open for writing ({self.mode!r}), not reading")
        return self._reader

    def _collected(self, data: AnyStr) -> int:
        """Keep written data at the end of what is waiting to be sent and return how many bytes wait."""
        if self.mode.startswith("r"):
            raise io.UnsupportedOperation(f"{self.path} is open for reading ({self.mode!r}), not writing")
        self._spool.seek(0, io.SEEK_END)
        self._spool.write(data.encode() if isinstance(data, str) else data)
        return self._spool.tell() - self._sent

    def _pieces(self) -> Iterator[bytes]:
        """Yield what waits to be sent in pieces, counting each one sent once the next is asked for."""
        if self.mode.startswith("r"):
            return
        self._spool.seek(self._sent)
        while piece := self._spool.read(self.PIECE_BYTES):
            yield piece
            self._sent += len(piece)
        self._spool.seek(0)
        self._spool.truncate()
        self._sent = 0

    def _release(self) -> None:
        """Discard the local copy, in memory or on disk."""
        self._closed = True
        self._copies.close()

    def _read_request(self) -> SandboxRequest:
        """Ask for the whole file."""
        return SandboxRequest("GET", self._files, {"path": self.path}, timeout=self.TRANSFER_SECONDS)

    def _write_request(self, content: bytes, append: bool) -> SandboxRequest:
        """Replace the file with bytes, or add them to its end."""
        query = {"path": self.path, **({"append": "true"} if append else {})}
        return SandboxRequest("PUT", self._files, query, content=content, timeout=self.TRANSFER_SECONDS)
