"""One output stream of a sandbox process, read as it is written."""

import atexit
import weakref
from collections.abc import AsyncIterator, Callable, Generator, Iterator
from typing import AnyStr, ClassVar, Generic

from labqoat.sandbox.sandbox_output_frame import SandboxOutputFrame
from labqoat.sandbox.sandbox_process_state import SandboxProcessState
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_transport import SandboxTransport
from labqoat.sandbox.sandbox_unavailable_error import SandboxUnavailableError


class SandboxStreamReader(Generic[AnyStr]):
    """Read a process's standard output or standard error: all of it, or line by line as lines arrive.

    The host keeps a process's output after it exits, so a stream can be read later and more than once from
    where this reader stopped. A connection lost while reading is opened again from the next unread byte. A
    stream that was discarded, or merged into standard output, has nothing to read and asks the host nothing.
    A loop over lines left before the process ended keeps its connection until it is collected, or until the
    interpreter exits, which closes it while that can still be done cleanly.
    """

    KINDS: ClassVar[dict[str, int]] = {"stdout": SandboxOutputFrame.STDOUT, "stderr": SandboxOutputFrame.STDERR}
    RESUMES: ClassVar[int] = 3
    QUIET_SECONDS: ClassVar[float] = 60.0
    CONNECTED: ClassVar["weakref.WeakSet[Generator[bytes, None, None]]"] = weakref.WeakSet()

    def __init__(
        self,
        transport: SandboxTransport,
        path: str,
        stream: str | None,
        decode: Callable[[bytes], AnyStr],
        exited: Callable[[SandboxProcessState], None],
    ) -> None:
        """Bind the output to read, the stream or none, how bytes become values, and who learns of the end."""
        self._transport = transport
        self._path = path
        self._stream = stream or ""
        self._decode: Callable[[bytes], AnyStr] = decode
        self._exited = exited
        self._offset = 0
        self._ended = stream is None

    def read(self) -> AnyStr:
        """Return everything from where this reader stopped until the process exits."""
        return self._decode(b"".join(self._received()))

    async def read_async(self) -> AnyStr:
        """Read the rest without blocking the event loop; see ``read``."""
        return self._decode(b"".join([chunk async for chunk in self._received_async()]))

    def __iter__(self) -> Iterator[AnyStr]:
        """Yield each line, ending with its newline, once it is complete; the last one may lack the newline."""
        pending = b""
        for chunk in self._received():
            *lines, pending = (pending + chunk).split(b"\n")
            yield from (self._decode(line + b"\n") for line in lines)
        if pending:
            yield self._decode(pending)

    async def __aiter__(self) -> AsyncIterator[AnyStr]:
        """Yield each line as it is complete without blocking the event loop; see ``__iter__``."""
        pending = b""
        async for chunk in self._received_async():
            *lines, pending = (pending + chunk).split(b"\n")
            for line in lines:
                yield self._decode(line + b"\n")
        if pending:
            yield self._decode(pending)

    def _received(self) -> Iterator[bytes]:
        """Yield this stream's bytes until the process exits, opening the stream again after a lost connection."""
        lost = 0
        while not self._ended:
            start = self._offset
            connection = self._connected()
            self.CONNECTED.add(connection)
            try:
                yield from connection
            except SandboxUnavailableError:
                lost = 0 if self._offset > start else lost + 1
                if lost >= self.RESUMES:
                    raise

    async def _received_async(self) -> AsyncIterator[bytes]:
        """Yield this stream's bytes without blocking the event loop; see ``_received``."""
        lost = 0
        while not self._ended:
            start = self._offset
            try:
                async for chunk in self._connected_async():
                    yield chunk
            except SandboxUnavailableError:
                lost = 0 if self._offset > start else lost + 1
                if lost >= self.RESUMES:
                    raise

    @classmethod
    def close_connections(cls) -> None:
        """Close every output connection a loop left open; the interpreter does this as it exits."""
        for connection in list(cls.CONNECTED):
            connection.close()

    def _connected(self) -> Generator[bytes, None, None]:
        """Read one connection's frames; a connection that closes before the exit frame was lost."""
        with self._transport.stream(self._request()) as body:
            for frame in SandboxOutputFrame.parse(body):
                if (chunk := self._taken(frame)) is not None:
                    yield chunk
        if not self._ended:
            raise SandboxUnavailableError(f"Sandbox host closed {self._path} before the process exited")

    async def _connected_async(self) -> AsyncIterator[bytes]:
        """Read one connection's frames without blocking the event loop; see ``_connected``."""
        async with self._transport.stream_async(self._request()) as body:
            async for frame in SandboxOutputFrame.parse_async(body):
                if (chunk := self._taken(frame)) is not None:
                    yield chunk
        if not self._ended:
            raise SandboxUnavailableError(f"Sandbox host closed {self._path} before the process exited")

    def _taken(self, frame: SandboxOutputFrame) -> bytes | None:
        """Keep this stream's bytes and the process's end; heartbeats and the other stream carry nothing here."""
        if frame.kind == SandboxOutputFrame.EXIT:
            self._exited(frame.state())
            self._ended = True
        if frame.kind != self.KINDS.get(self._stream):
            return None
        self._offset = frame.end
        return frame.payload

    def _request(self) -> SandboxRequest:
        """Ask for this stream from the next unread byte; quiet stretches are bounded by the host's heartbeats."""
        query = {self._stream: str(self._offset)}
        return SandboxRequest("GET", self._path, query, timeout=self.QUIET_SECONDS)


atexit.register(SandboxStreamReader.close_connections)
