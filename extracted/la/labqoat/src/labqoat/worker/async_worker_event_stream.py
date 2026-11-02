"""Bounded incremental completion frames for cancellable worker SSE connections."""

from collections.abc import AsyncGenerator, AsyncIterable, AsyncIterator
from contextlib import aclosing

from labqoat.json_document import JsonDocument
from labqoat.worker.worker_api_error import WorkerApiError
from labqoat.worker.worker_event_stream import WorkerEventStream


class AsyncWorkerEventStream:
    """Read push completion without buffering unbounded lines or depending on a blocking reader thread."""

    _MAX_BYTES = 4_194_304

    @staticmethod
    async def complete(chunks: AsyncIterable[bytes], kind: str) -> JsonDocument:
        """Preserve frame boundaries across arbitrary chunks and reject truncated terminal events."""
        async with aclosing(AsyncWorkerEventStream.events(chunks, kind)) as events:
            return await anext(events)

    @staticmethod
    async def events(
        chunks: AsyncIterable[bytes], kind: str, maximum: int | None = None, heartbeats: bool = False
    ) -> AsyncGenerator[JsonDocument, None]:
        """Yield bounded frames without closing a persistent stream after its first delivery."""
        limit = AsyncWorkerEventStream._MAX_BYTES if maximum is None else maximum
        event, data = b"message", b""
        async for line in AsyncWorkerEventStream._lines(chunks, limit):
            if not line:
                result = AsyncWorkerEventStream._result(event, data, kind)
                if result is not None:
                    yield result
                event, data = b"message", b""
            elif line.startswith(b"event:"):
                event = line[6:].strip()
            elif line.startswith(b"data:"):
                data += line[5:].lstrip() + b"\n"
                AsyncWorkerEventStream._bounded(data, limit)
            elif line == b": heartbeat" and heartbeats:
                yield JsonDocument(heartbeat=True)
        raise WorkerApiError("Worker stream closed before completion")

    @staticmethod
    async def _lines(chunks: AsyncIterable[bytes], maximum: int) -> AsyncIterator[bytes]:
        """Accumulate bounded partial lines and support both LF and CRLF across network chunks."""
        buffer = b""
        async for chunk in chunks:
            buffer += chunk
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                AsyncWorkerEventStream._bounded(line, maximum)
                yield line.rstrip(b"\r")
            AsyncWorkerEventStream._bounded(buffer, maximum)

    @staticmethod
    def _bounded(value: bytes, maximum: int) -> None:
        """Enforce a per-line and per-frame memory bound even when no delimiter arrives."""
        if len(value) > maximum:
            raise WorkerApiError("Worker stream frame is too large")

    @staticmethod
    def _result(event: bytes, data: bytes, kind: str) -> JsonDocument | None:
        """Ignore heartbeat frames while preserving explicit remote errors and strict JSON objects."""
        if not data:
            return None
        document = JsonDocument.expect_dict(WorkerEventStream._document(data))
        if event == f"{kind}.error".encode():
            raise WorkerApiError(f"{kind} stream failed: {document.get('error')}", code="stream_failed")
        if event == f"{kind}.complete".encode():
            return document
        return None
