"""One HTTP/1.1 connection driven by asyncio streams."""

from __future__ import annotations

import asyncio
import ssl
from collections.abc import AsyncIterable, AsyncIterator, Awaitable
from typing import TypeAlias

from labqoat.net.failures import Failures
from labqoat.net.headers import Headers
from labqoat.net.http_error import HttpError
from labqoat.net.url import Url

AsyncBody: TypeAlias = bytes | AsyncIterable[bytes] | None


class AsyncConnection:
    """Write one request at a time and read its answer; a connection is reusable once an answer ends cleanly."""

    READ_BYTES = 65_536
    LINE_LIMIT = 65_536
    WITH_BODY = frozenset({"POST", "PUT", "PATCH"})

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Own both directions of an open connection."""
        self.reader = reader
        self.writer = writer
        self.reusable = False
        self.idle_since = 0.0
        self._keep = False

    @classmethod
    async def open(
        cls, target: Url, unix_socket: str | None, context: ssl.SSLContext | None, timeout: float | None
    ) -> AsyncConnection:
        """Connect to the socket path, or to the target's host over TLS for HTTPS."""
        with Failures.translated():
            async with asyncio.timeout(timeout):
                if unix_socket is not None:
                    reader, writer = await asyncio.open_unix_connection(unix_socket, limit=cls.LINE_LIMIT)
                else:
                    secure = target.scheme == "https"
                    reader, writer = await asyncio.open_connection(
                        target.host,
                        target.port or (443 if secure else 80),
                        ssl=context if secure else None,
                        server_hostname=target.host if secure else None,
                        limit=cls.LINE_LIMIT,
                    )
        return cls(reader, writer)

    async def send(self, method: str, target: Url, fields: Headers, content: AsyncBody, timeout: float | None) -> None:
        """Write the request line, its fields and its body, chunked when its length is not declared."""
        hop = Headers((name, value) for name, value in fields.multi_items() if name.lower() != "transfer-encoding")
        fields = hop.merged(self._framing(method, hop, content))
        lines = [f"{method} {target.target} HTTP/1.1"]
        if "host" not in fields:
            lines.append(f"Host: {target.authority}")
        lines.extend(f"{name}: {value}" for name, value in fields.multi_items())
        if any("\r" in line or "\n" in line for line in lines):
            raise ValueError("HTTP request lines cannot contain line breaks")
        head = ("\r\n".join(lines) + "\r\n\r\n").encode("latin-1")
        chunked = fields.get("transfer-encoding") == "chunked"
        with Failures.translated():
            async with asyncio.timeout(timeout):
                await self._write(head, content, chunked)

    async def _write(self, head: bytes, content: AsyncBody, chunked: bool) -> None:
        """Send the head with an in-memory body in one write, or follow it with the body's chunks."""
        if content is None or isinstance(content, bytes):
            self.writer.write(head + (content or b""))
        else:
            self.writer.write(head)
            async for chunk in content:
                if chunk:
                    self.writer.write(b"%X\r\n%s\r\n" % (len(chunk), chunk) if chunked else chunk)
                    await self.writer.drain()
            if chunked:
                self.writer.write(b"0\r\n\r\n")
        await self.writer.drain()

    def _framing(self, method: str, fields: Headers, content: AsyncBody) -> dict[str, str]:
        """How the body's end is marked: its length when known, otherwise chunked framing."""
        if isinstance(content, bytes):
            return {"content-length": str(len(content))}
        if content is not None:
            return {} if "content-length" in fields else {"transfer-encoding": "chunked"}
        declared = "content-length" in fields or "transfer-encoding" in fields
        return {"content-length": "0"} if method in self.WITH_BODY and not declared else {}

    async def receive(self, method: str, timeout: float | None) -> tuple[int, Headers, AsyncIterator[bytes]]:
        """Read the final answer's status and fields, skipping interim ones, and how to read its body."""
        status, fields = 100, Headers()
        while 100 <= status < 200 and status != 101:
            status, fields = self._head(await self._within(self.reader.readuntil(b"\r\n\r\n"), timeout))
        if method == "HEAD" or status in (101, 204, 304):
            return status, fields, self._sized(0, timeout)
        if "chunked" in fields.get("transfer-encoding", "").lower():
            return status, fields, self._chunked(timeout)
        if "content-length" in fields:
            return status, fields, self._sized(self._length(fields["content-length"]), timeout)
        return status, fields, self._until_closed(timeout)

    def _head(self, raw: bytes) -> tuple[int, Headers]:
        """Parse a status line and fields, remembering whether the server keeps the connection open."""
        lines = raw.decode("latin-1").split("\r\n")
        version, _, rest = lines[0].partition(" ")
        code = rest[:3]
        if not version.startswith("HTTP/1.") or not code.isdigit():
            raise HttpError(f"Not an HTTP/1.1 answer: {lines[0][:80]!r}")
        pairs = [line.partition(":") for line in lines[1:] if line]
        if any(not separator for _name, separator, _value in pairs):
            raise HttpError("Malformed HTTP header field")
        fields = Headers((name.strip(), value.strip()) for name, _separator, value in pairs)
        self._keep = version == "HTTP/1.1" and "close" not in fields.get("connection", "").lower()
        return int(code), fields

    @staticmethod
    def _length(value: str) -> int:
        """A declared body length."""
        if not value.strip().isdigit():
            raise HttpError("Malformed HTTP content length")
        return int(value)

    async def _sized(self, length: int, timeout: float | None) -> AsyncIterator[bytes]:
        """A body of a declared length, which is zero for an answer that has none."""
        async for piece in self._exactly(length, timeout):
            yield piece
        self.reusable = self._keep

    async def _chunked(self, timeout: float | None) -> AsyncIterator[bytes]:
        """A chunked body, read one bounded piece at a time; trailer fields are discarded."""
        while size := self._chunk_size(await self._within(self.reader.readuntil(b"\r\n"), timeout)):
            async for piece in self._exactly(size, timeout):
                yield piece
            if await self._within(self.reader.readexactly(2), timeout) != b"\r\n":
                raise HttpError("Malformed HTTP chunk")
        while await self._within(self.reader.readuntil(b"\r\n"), timeout) != b"\r\n":
            pass
        self.reusable = self._keep

    @staticmethod
    def _chunk_size(line: bytes) -> int:
        """The size a chunk line announces."""
        digits = line.split(b";", 1)[0].strip()
        try:
            return int(digits, 16)
        except ValueError:
            raise HttpError("Malformed HTTP chunk size") from None

    async def _exactly(self, length: int, timeout: float | None) -> AsyncIterator[bytes]:
        """Exactly ``length`` bytes, in pieces as they arrive."""
        while length > 0:
            piece = await self._within(self.reader.read(min(self.READ_BYTES, length)), timeout)
            if not piece:
                raise HttpError("HTTP connection closed before the answer ended")
            length -= len(piece)
            yield piece

    async def _until_closed(self, timeout: float | None) -> AsyncIterator[bytes]:
        """A body that ends when the server closes the connection."""
        while piece := await self._within(self.reader.read(self.READ_BYTES), timeout):
            yield piece

    @staticmethod
    async def _within(step: Awaitable[bytes], timeout: float | None) -> bytes:
        """Wait for one read, failing with the shared transport errors."""
        with Failures.translated():
            try:
                async with asyncio.timeout(timeout):
                    return await step
            except asyncio.LimitOverrunError as error:
                raise HttpError("HTTP answer line is too long") from error

    def close(self) -> None:
        """Close the connection without waiting for the peer."""
        self.reusable = False
        self.writer.close()
