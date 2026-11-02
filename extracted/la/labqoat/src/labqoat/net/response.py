"""An answer: status and fields at once, the body whole or as it arrives."""

from __future__ import annotations

import json as json_module
import zlib
from collections.abc import AsyncIterable, AsyncIterator, Iterable, Iterator, Mapping
from typing import TYPE_CHECKING, cast

from labqoat.json_document import JsonValue
from labqoat.net.headers import Headers

if TYPE_CHECKING:
    from zlib import _Decompress

    from labqoat.net.request import Request


class Response:
    """Status, header fields and a body that is either already in memory or read on demand.

    The body reads back decoded from a ``gzip`` or ``deflate`` content encoding; the raw iterators give it
    exactly as sent.
    """

    def __init__(
        self,
        status_code: int,
        *,
        headers: Mapping[str, str] | Iterable[tuple[str, str]] | None = None,
        content: bytes | None = None,
        json: object = None,
        text: str | None = None,
        stream: Iterable[bytes] | AsyncIterable[bytes] | None = None,
        request: Request | None = None,
    ) -> None:
        """Answer with ``content``, a ``json`` document, ``text``, or a ``stream`` of body chunks."""
        self.status_code = status_code
        self.headers = Headers(headers)
        self.request = request
        if json is not None:
            content = json_module.dumps(json).encode()
            self.headers = self.headers.merged({"content-type": "application/json"})
        if text is not None:
            content = text.encode()
            self.headers = self.headers.merged({"content-type": "text/plain; charset=utf-8"})
        self._raw: bytes | None = (content or b"") if stream is None else None
        self._stream = stream
        self.is_closed = False

    @property
    def content(self) -> bytes:
        """The whole decoded body, reading it first if it is still to arrive."""
        return self.read()

    @property
    def text(self) -> str:
        """The body as text in the charset the content type names, UTF-8 otherwise."""
        charset = "utf-8"
        for parameter in self.headers.get("content-type", "").split(";")[1:]:
            name, _, value = parameter.strip().partition("=")
            if name.lower() == "charset" and value:
                charset = value.strip('"')
        return self.content.decode(charset, errors="replace")

    def json(self) -> JsonValue:
        """The body parsed as JSON."""
        return cast("JsonValue", json_module.loads(self.content))

    def read(self) -> bytes:
        """Read the rest of a blocking body and return all of it decoded."""
        if self._raw is None:
            self._raw = b"".join(self._sync_stream())
        return self._decode_whole(self._raw)

    async def aread(self) -> bytes:
        """Read the rest of an asynchronous body and return all of it decoded."""
        if self._raw is None:
            self._raw = b"".join([chunk async for chunk in self._async_stream()])
        return self._decode_whole(self._raw)

    def iter_raw(self) -> Iterator[bytes]:
        """Yield the body as sent, as it arrives."""
        if self._raw is not None:
            yield from (self._raw,) if self._raw else ()
            return
        for chunk in self._sync_stream():
            if chunk:
                yield chunk

    def iter_bytes(self) -> Iterator[bytes]:
        """Yield the decoded body as it arrives."""
        decoder = self._decoder()
        for chunk in self.iter_raw():
            if piece := chunk if decoder is None else decoder.decompress(chunk):
                yield piece

    async def aiter_raw(self) -> AsyncIterator[bytes]:
        """Yield the body as sent, as it arrives, without blocking the event loop."""
        if self._raw is not None:
            if self._raw:
                yield self._raw
            return
        async for chunk in self._async_stream():
            if chunk:
                yield chunk

    async def aiter_bytes(self) -> AsyncIterator[bytes]:
        """Yield the decoded body as it arrives, without blocking the event loop."""
        decoder = self._decoder()
        async for chunk in self.aiter_raw():
            if piece := chunk if decoder is None else decoder.decompress(chunk):
                yield piece

    def close(self) -> None:
        """Give up the rest of a blocking body."""
        self.is_closed = True
        close = getattr(self._stream, "close", None)
        if close is not None:
            close()

    async def aclose(self) -> None:
        """Give up the rest of an asynchronous body."""
        self.is_closed = True
        close = getattr(self._stream, "aclose", None)
        if close is not None:
            await close()

    def _sync_stream(self) -> Iterable[bytes]:
        """The blocking body source; an asynchronous one must be read with the asynchronous methods."""
        if isinstance(self._stream, AsyncIterable):
            raise RuntimeError("An asynchronous response body must be read asynchronously")
        return cast("Iterable[bytes]", self._stream)

    def _async_stream(self) -> AsyncIterable[bytes]:
        """The asynchronous body source; a blocking one must be read with the blocking methods."""
        if not isinstance(self._stream, AsyncIterable):
            raise RuntimeError("A blocking response body must be read without awaiting")
        return self._stream

    def _decode_whole(self, raw: bytes) -> bytes:
        """Decode a complete body."""
        decoder = self._decoder()
        return raw if decoder is None else decoder.decompress(raw)

    def _decoder(self) -> _Decompress | None:
        """A decompressor for the content encoding, or nothing for an identity body."""
        encoding = self.headers.get("content-encoding", "").strip().lower()
        if encoding == "gzip":
            return zlib.decompressobj(16 + zlib.MAX_WBITS)
        if encoding == "deflate":
            return zlib.decompressobj()
        return None
