"""Compresses whole JSON and text replies, and event streams, with zstd for clients that ask for it."""

import anyio
import zstandard
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from langgraph_api.config import JSON_THREAD_POOL_MINIMUM_SIZE_BYTES

# Smaller replies fit in one TCP segment with their headers either way.
MINIMUM_SIZE_BYTES = 1024

# A stream holds its compressor until it ends: about 100 KB with an 8 KB window and 4 KB
# output chunks (a compressobj keeps a 128 KB output buffer). The window still covers the
# last few token events, whose repeated metadata is most of a streamed reply. A `values`
# event bigger than the window compresses only within itself.
# No checksum: a heartbeat cancelled as its stream ends drops a block it already
# compressed, and a checksum would fail the frame on it.
STREAM_PARAMETERS = zstandard.ZstdCompressionParameters.from_level(
    1, window_log=13, hash_log=12
)
STREAM_CHUNK_BYTES = 4096


# No gzip: it spends several times zstd's CPU for about the same size, and Node's fetch
# asks for gzip on every version (for zstd only on recent ones, over HTTPS), so a proxy
# that passes fetch's decoded body on under the upstream Content-Encoding would break on all.
def accepts_zstd(accept_encoding: str) -> bool:
    for item in accept_encoding.split(","):
        coding, *params = item.split(";")
        if coding.strip().lower() != "zstd":
            continue
        for param in params:
            name, _, value = param.partition("=")
            if name.strip().lower() == "q":
                try:
                    return float(value) > 0
                except ValueError:
                    return False
        return True
    return False


def _media_type(headers: Headers) -> str:
    return headers.get("content-type", "").partition(";")[0].strip().lower()


def _compressible(headers: Headers) -> bool:
    # Streams (SSE, `/runs/wait` heartbeats) have no Content-Length, so their headers go out at once.
    length = headers.get("content-length", "")
    media_type = _media_type(headers)
    return (
        length.isdigit()
        and int(length) >= MINIMUM_SIZE_BYTES
        and "content-encoding" not in headers
        and "content-range" not in headers
        and (media_type == "application/json" or media_type.startswith("text/"))
    )


def _compressible_stream(headers: Headers) -> bool:
    return (
        _media_type(headers) == "text/event-stream"
        and "content-length" not in headers
        and "content-encoding" not in headers
    )


async def _compress(body: bytes) -> bytes:
    if len(body) > JSON_THREAD_POOL_MINIMUM_SIZE_BYTES:
        return await run_in_threadpool(zstandard.compress, body)
    return zstandard.compress(body)


def _compress_part(
    compressor: "zstandard.ZstdCompressionChunker", message: Message
) -> bytes:
    # A flush per message sends every event as it comes instead of when a block fills.
    end = compressor.flush if message.get("more_body", False) else compressor.finish
    return b"".join([*compressor.compress(message.get("body", b"")), *end()])


class CompressionMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # In-process SDK clients would compress and decompress in the same process.
        if scope["type"] != "http" or scope.get("root_path", "").startswith("/noauth"):
            await self.app(scope, receive, send)
            return
        zstd = accepts_zstd(Headers(scope=scope).get("accept-encoding", ""))
        held_start: Message | None = None
        compressor: zstandard.ZstdCompressionChunker | None = None
        # An SSE reply sends its heartbeats from another task: a compressed part decodes
        # only after every part compressed before it, and a big part compresses in a
        # worker thread that must have the compressor to itself.
        stream_lock = anyio.Lock()

        async def send_compressed(message: Message) -> None:
            nonlocal held_start, compressor
            if message["type"] == "http.response.start":
                headers = MutableHeaders(raw=list(message.get("headers", [])))
                if _compressible(headers):
                    headers.add_vary_header("Accept-Encoding")
                    message = {**message, "headers": headers.raw}
                    if zstd:
                        held_start = message
                        return
                elif zstd and _compressible_stream(headers):
                    headers.add_vary_header("Accept-Encoding")
                    headers["content-encoding"] = "zstd"
                    message = {**message, "headers": headers.raw}
                    compressor = zstandard.ZstdCompressor(
                        compression_params=STREAM_PARAMETERS
                    ).chunker(chunk_size=STREAM_CHUNK_BYTES)
                await send(message)
                return
            if compressor is not None and message["type"] == "http.response.body":
                async with stream_lock:
                    if (
                        len(message.get("body", b""))
                        > JSON_THREAD_POOL_MINIMUM_SIZE_BYTES
                    ):
                        body = await run_in_threadpool(
                            _compress_part, compressor, message
                        )
                    else:
                        body = _compress_part(compressor, message)
                    await send({**message, "body": body})
                return
            if held_start is not None:
                start, held_start = held_start, None
                headers = MutableHeaders(raw=start["headers"])
                body = message.get("body", b"")
                # Not `more_body`: BaseHTTPMiddleware sends a whole body with more_body=True, then an empty end.
                if len(body) == int(headers["content-length"]):
                    body = await _compress(body)
                    headers["content-encoding"] = "zstd"
                    headers["content-length"] = str(len(body))
                    message = {**message, "body": body}
                await send(start)
            await send(message)

        await self.app(scope, receive, send_compressed)
