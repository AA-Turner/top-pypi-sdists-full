"""HTTP/1.1 framing for the proxy's own side (stdlib asyncio streams): read one request, write a response head, a
body whole or chunked. Body bytes are never changed; only the framing around them is the proxy's."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from http import HTTPStatus

#: A request head at most (the stream's buffer limit too).
MAX_HEAD_BYTES = 64 * 1024
#: A request body at most; a bigger one answers 413.
MAX_BODY_BYTES = 64 * 1024 * 1024
#: Headers that describe one hop, never passed on (RFC 9110 §7.6.1), plus the framing this side redoes.
HOP_HEADERS = frozenset({"connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "proxy-connection",
                         "te", "trailer", "transfer-encoding", "upgrade", "host", "content-length", "expect"})  # fmt: skip
CHUNKED_END = b"0\r\n\r\n"


class FramingError(Exception):
    """A request this side cannot read; `status` is the answer."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status


@dataclass
class Request:
    method: str
    target: str
    version: str
    headers: list[tuple[str, str]]
    body: bytes = b""

    def get_header(self, name: str) -> str | None:
        name = name.lower()
        return next((value for key, value in self.headers if key.lower() == name), None)

    @property
    def is_keep_alive(self) -> bool:
        connection = (self.get_header("connection") or "").lower()
        if self.version == "HTTP/1.0":
            return "keep-alive" in connection
        return "close" not in connection


async def read_request(reader: asyncio.StreamReader) -> Request | None:
    """The next request on the connection, its body read whole; None when the client closed between requests."""
    try:
        head = await reader.readuntil(b"\r\n\r\n")
    except asyncio.IncompleteReadError as exc:
        if not exc.partial.strip():
            return None
        raise FramingError(400, "the request head ended early") from None
    except asyncio.LimitOverrunError:
        raise FramingError(431, "the request head is too large") from None
    lines = head[:-4].decode("latin-1").split("\r\n")
    parts = lines[0].split(" ")
    if len(parts) != 3 or not parts[2].startswith("HTTP/1."):
        raise FramingError(400, "not an HTTP/1.x request line")
    headers = []
    for line in lines[1:]:
        name, sep, value = line.partition(":")
        if not sep or not name.strip():
            raise FramingError(400, "a header line has no name")
        headers.append((name.strip(), value.strip()))
    request = Request(parts[0].upper(), parts[1], parts[2], headers)
    request.body = await _read_body(reader, request)
    return request


async def _read_body(reader: asyncio.StreamReader, request: Request) -> bytes:
    if "chunked" in (request.get_header("transfer-encoding") or "").lower():
        return await _read_chunked(reader)
    length = request.get_header("content-length")
    if not length:
        return b""
    if not length.isdigit():
        raise FramingError(400, "content-length is not a number")
    if int(length) > MAX_BODY_BYTES:
        raise FramingError(413, "the request body is too large")
    return await reader.readexactly(int(length))


async def _read_chunked(reader: asyncio.StreamReader) -> bytes:
    body = bytearray()
    while True:
        line = await reader.readuntil(b"\r\n")
        try:
            size = int(line.split(b";", 1)[0].strip(), 16)
        except ValueError:
            raise FramingError(400, "a chunk size is not hex") from None
        if size == 0:
            while (await reader.readuntil(b"\r\n")) != b"\r\n":  # trailers, dropped
                pass
            return bytes(body)
        if len(body) + size > MAX_BODY_BYTES:
            raise FramingError(413, "the request body is too large")
        body += await reader.readexactly(size)
        await reader.readexactly(2)


def make_head(status: int, headers: list[tuple[str | bytes, str | bytes]]) -> bytes:
    """A response's status line and headers; a header given as bytes goes out as those bytes."""
    try:
        phrase = HTTPStatus(status).phrase
    except ValueError:
        phrase = ""
    lines = [f"HTTP/1.1 {status} {phrase}".encode()]
    lines += [_to_bytes(name) + b": " + _to_bytes(value) for name, value in headers]
    return b"\r\n".join(lines) + b"\r\n\r\n"


def _to_bytes(value: str | bytes) -> bytes:
    return value if isinstance(value, bytes) else value.encode("latin-1")


def make_chunk(data: bytes) -> bytes:
    return b"%x\r\n" % len(data) + data + b"\r\n"


def make_json_response(status: int, payload: dict, *, extra: list[tuple[str, str]] = (),
                       is_keep_alive: bool = True) -> bytes:  # fmt: skip
    """A whole JSON response: head and body."""
    body = json.dumps(payload).encode()
    headers = [("content-type", "application/json"), ("content-length", str(len(body))), *extra]
    if not is_keep_alive:
        headers.append(("connection", "close"))
    return make_head(status, headers) + body


def has_no_body(method: str, status: int) -> bool:
    """A response that carries no body whatever its headers say (RFC 9112 §6.3)."""
    return method == "HEAD" or status < 200 or status in (204, 304)
