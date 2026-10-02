"""
This module defines :class:`StreamResponse`, the return type used to make a
User Data Function return a **fully streamed** HTTP response instead of a single
buffered body.

Import it from ``fabric.functions`` and return it from a function decorated with
:meth:`fabric.functions.UserDataFunctions.streaming_function`::

    import fabric.functions as fn

    udf = fn.UserDataFunctions()

    @udf.streaming_function()
    def stream_numbers(count: int) -> fn.StreamResponse:
        def gen():
            for i in range(count):
                yield f"chunk {i}\\n".encode()
        return fn.StreamResponse(gen(), media_type="text/plain")

Unlike the classic return types (``dict``, ``str``, a pandas ``DataFrame`` ...)
which the worker materializes in full before replying, a ``StreamResponse``
wraps an *iterator* (or async iterator) of chunks that are flushed to the
client as they are produced. This is what enables true HTTP streaming end to
end (e.g. relaying an Apache Arrow stream from Power BI ``executeDaxQueries``).

.. important::
    Streaming relies on the Azure Functions **HTTP streams** feature
    (``azurefunctions-extensions-http-fastapi``). When any streaming function is
    present the function app runs in ASGI mode app-wide, so a streaming app
    cannot also host classic buffered User Data Functions. See
    :meth:`fabric.functions.UserDataFunctions.streaming_function`.
"""

from typing import (Any, AsyncIterable, AsyncIterator, Iterable, Iterator,
                    Mapping, Optional, Union)

# A streaming body may be a sync or async iterable of bytes or str chunks.
StreamContent = Union[
    Iterable[bytes],
    Iterator[bytes],
    AsyncIterable[bytes],
    AsyncIterator[bytes],
    Iterable[str],
    AsyncIterable[str],
]

DEFAULT_MEDIA_TYPE = "application/octet-stream"


class StreamResponse:
    """
    Wraps a streaming body for a User Data Function.

    :param content: An iterator/iterable (sync or async) yielding ``bytes`` or
        ``str`` chunks. Each chunk is flushed to the client as it is produced.
    :type content: Iterable[bytes] | AsyncIterable[bytes] | Iterable[str] | AsyncIterable[str]
    :param media_type: The ``Content-Type`` of the streamed body. Defaults to
        ``application/octet-stream`` (suitable for an Apache Arrow IPC stream).
    :type media_type: str
    :param status_code: The HTTP status code. Defaults to ``200``.
    :type status_code: int
    :param headers: Optional extra response headers.
    :type headers: Mapping[str, str]
    """

    def __init__(
        self,
        content: StreamContent,
        *,
        media_type: str = DEFAULT_MEDIA_TYPE,
        status_code: int = 200,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        if not (_is_iterable(content) or _is_async_iterable(content)):
            raise TypeError(
                "StreamResponse content must be a (sync or async) iterable of "
                f"bytes/str chunks, got {type(content).__name__!r}."
            )
        self.content: StreamContent = content
        self.media_type: str = media_type
        self.status_code: int = status_code
        self.headers: dict = {}
        if headers:
            self.headers = dict(headers)

    @staticmethod
    def from_arrow_batches(
        batches: Any,
        *,
        schema: Any = None,
        media_type: str = DEFAULT_MEDIA_TYPE,
        status_code: int = 200,
        headers: Optional[Mapping[str, str]] = None,
    ) -> "StreamResponse":
        """
        Build a :class:`StreamResponse` that emits an Apache Arrow IPC **stream**
        incrementally, one record batch at a time, without buffering the whole
        table in memory.

        :param batches: An iterable of ``pyarrow.RecordBatch`` (or a
            ``pyarrow.RecordBatchReader``). When a reader is passed its schema is
            used automatically.
        :param schema: The ``pyarrow.Schema`` to write. Required when ``batches``
            is a plain iterable of record batches and ``schema`` cannot be
            inferred from the first batch.
        """
        import io

        import pyarrow as pa  # imported lazily so non-streaming installs stay light

        def _incremental_gen() -> Iterator[bytes]:
            iterator = iter(batches)
            resolved_schema = schema
            first_batch = None

            if isinstance(batches, pa.RecordBatchReader):
                resolved_schema = batches.schema
            elif resolved_schema is None:
                # Pull the first batch to learn the schema.
                first_batch = next(iterator, None)
                if first_batch is None:
                    return  # empty stream
                resolved_schema = first_batch.schema

            # Emit ONE canonical Arrow IPC stream (a single schema message,
            # then one message per record batch, then the EOS marker) so a
            # standard ``pyarrow.ipc.open_stream`` reader consumes every batch
            # from a single stream. We write into a BytesIO sink and reset it
            # after each flush, yielding only the bytes written since the
            # previous batch so each batch flushes to the client as it is
            # produced instead of buffering the whole table.
            sink = io.BytesIO()
            writer = pa.ipc.new_stream(sink, resolved_schema)

            def take_new() -> bytes:
                # Return only the bytes written since the last flush, then reset
                # the sink so it never retains the whole stream. Without the
                # reset the BytesIO grows with the full response size and
                # ``getvalue()`` re-copies all previously emitted bytes on every
                # batch (O(n^2) memory and copying). ``getvalue()`` is evaluated
                # before ``finally`` runs and returns an independent copy, so
                # truncating the buffer afterward is safe.
                try:
                    return sink.getvalue()
                finally:
                    sink.seek(0)
                    sink.truncate(0)

            # Opening the writer emits the schema message; flush it first so the
            # client can build its reader before any batch arrives.
            schema_chunk = take_new()
            if schema_chunk:
                yield schema_chunk

            if first_batch is not None:
                writer.write_batch(first_batch)
                chunk = take_new()
                if chunk:
                    yield chunk
            for batch in iterator:
                writer.write_batch(batch)
                chunk = take_new()
                if chunk:
                    yield chunk

            writer.close()  # writes the EOS marker
            final_chunk = take_new()
            if final_chunk:
                yield final_chunk

        return StreamResponse(
            _incremental_gen(),
            media_type=media_type,
            status_code=status_code,
            headers=headers,
        )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"StreamResponse(media_type={self.media_type!r}, "
            f"status_code={self.status_code}, headers={self.headers!r})"
        )


def _is_iterable(obj: Any) -> bool:
    return hasattr(obj, "__iter__")


def _is_async_iterable(obj: Any) -> bool:
    return hasattr(obj, "__aiter__")
