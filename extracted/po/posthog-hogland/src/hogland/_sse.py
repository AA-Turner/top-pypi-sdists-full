"""Server-Sent Events parsing + stream helpers for
``POST /v1/hogboxes/{id}/exec/stream``.

The streaming-exec endpoint isn't typed in ``openapi.yaml`` (see
``docs/PYTHON_SDK_CODEGEN_RESEARCH.md`` §4 — Huma doesn't register it,
so no codegen client can emit it). The facade owns the wire format.

Wire format, from the research doc:

.. code-block:: text

    event: stdout
    data: hello world\\n

    event: stderr
    data: warning: foo

    event: exit
    data: {"code": 0, "duration_ms": 1234}

We parse with ``httpx-sse`` (just frames the bytes) and emit typed
:class:`hogland._models.ExecEvent` instances. The ``exit`` frame closes
the stream; we surface it as a final event rather than swallowing it so
callers can read ``.exit_code`` / ``.duration_ms`` without a second
``GET``.

:class:`StreamResult` / :class:`AsyncStreamResult` wrap that event
iterator with the ergonomic shape every adapter ends up writing: yield
stdout chunks as they arrive, buffer stderr in the background, surface
exit info after the stream closes. Without this helper every consumer
re-implements the same stderr-buffer + exit-capture dance.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from ._models import ExecEvent

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

    from httpx_sse import ServerSentEvent


def parse_event(sse: ServerSentEvent) -> ExecEvent:
    """Turn one SSE frame into a typed :class:`ExecEvent`.

    Raises :class:`ValueError` on an unrecognised event kind, on the
    assumption that an unknown frame is a server bug we'd rather surface
    than silently drop.
    """
    kind = sse.event
    if kind == "stdout":
        return ExecEvent(kind="stdout", data=sse.data)
    if kind == "stderr":
        return ExecEvent(kind="stderr", data=sse.data)
    if kind == "exit":
        payload = json.loads(sse.data) if sse.data else {}
        return ExecEvent(
            kind="exit",
            exit_code=payload.get("code"),
            duration_ms=payload.get("duration_ms"),
        )
    msg = f"unknown SSE event kind from hogplane: {kind!r}"
    raise ValueError(msg)


class StreamResult:
    """Sync helper wrapping :meth:`Hogbox.exec_stream` for typical use.

    The raw ``exec_stream`` iterator yields all three event kinds
    interleaved — stdout, stderr, exit. Every consumer wants the same
    thing: stdout streamed line-by-line, stderr buffered for the post-
    mortem, exit_code + duration_ms at the end. Writing that loop by
    hand is repetitive and easy to get wrong (forgetting the exit
    branch, dropping stderr, double-iterating the generator).

    Usage:

    .. code-block:: python

        stream = StreamResult(box.exec_stream(["bash", "-c", "..."]))
        for chunk in stream.stdout():
            print(chunk, end="")
        # After stdout() exhausts, the trailing exit event has been read
        # and stderr/exit_code/duration_ms are populated.
        print(f"exit={stream.exit_code} stderr={stream.stderr}")

    Or, when the caller doesn't need the streamed stdout (e.g. they
    just want the captured stderr + exit), :meth:`drain` consumes the
    stream silently:

    .. code-block:: python

        result = StreamResult(box.exec_stream(argv)).drain()
        print(result.exit_code, result.stderr)
    """

    def __init__(self, events: Iterator[ExecEvent]) -> None:
        self._events = events
        self._stderr_parts: list[str] = []
        self._consumed = False
        self.exit_code: int | None = None
        self.duration_ms: int | None = None
        self.stderr: str = ""

    def stdout(self) -> Iterator[str]:
        """Yield stdout chunks as they arrive.

        Single-use — calling twice raises :class:`RuntimeError` because
        the underlying SSE iterator can only be walked once.
        """
        if self._consumed:
            msg = "StreamResult.stdout() already consumed"
            raise RuntimeError(msg)
        self._consumed = True
        for event in self._events:
            if event.kind == "stdout":
                yield event.data
            elif event.kind == "stderr":
                self._stderr_parts.append(event.data)
            elif event.kind == "exit":
                self.exit_code = event.exit_code
                self.duration_ms = event.duration_ms
                break
        # Drain any remaining events after the inner loop exits (either
        # exhausted, or broken on the `exit` event) so stderr/exit_code
        # still populate if the server sends post-exit frames. If the
        # *caller* breaks early from `for chunk in stream.stdout()`,
        # GeneratorExit is thrown here instead and this loop never
        # runs — the connection still closes cleanly via GeneratorExit
        # propagation, but exit_code/stderr won't be populated.
        for event in self._events:
            if event.kind == "stderr":
                self._stderr_parts.append(event.data)
            elif event.kind == "exit":
                self.exit_code = event.exit_code
                self.duration_ms = event.duration_ms
        self.stderr = "".join(self._stderr_parts)

    def drain(self) -> StreamResult:
        """Consume the stream, discarding stdout chunks.

        Useful when the caller only cares about exit_code + stderr —
        e.g. a fire-and-check exec. Returns ``self`` for chaining.
        """
        for _ in self.stdout():
            pass
        return self


class AsyncStreamResult:
    """Async equivalent of :class:`StreamResult` — same shape, async iter.

    Usage:

    .. code-block:: python

        stream = AsyncStreamResult(box.exec_stream(argv))
        async for chunk in stream.stdout():
            print(chunk, end="")
        print(stream.exit_code, stream.stderr)
    """

    def __init__(self, events: AsyncIterator[ExecEvent]) -> None:
        self._events = events
        self._stderr_parts: list[str] = []
        self._consumed = False
        self.exit_code: int | None = None
        self.duration_ms: int | None = None
        self.stderr: str = ""

    async def stdout(self) -> AsyncIterator[str]:
        if self._consumed:
            msg = "AsyncStreamResult.stdout() already consumed"
            raise RuntimeError(msg)
        self._consumed = True
        async for event in self._events:
            if event.kind == "stdout":
                yield event.data
            elif event.kind == "stderr":
                self._stderr_parts.append(event.data)
            elif event.kind == "exit":
                self.exit_code = event.exit_code
                self.duration_ms = event.duration_ms
                break
        # See StreamResult.stdout for the drain rationale + the
        # GeneratorExit caveat (here it's `aclose()` propagating through
        # `async for`, but the shape is identical).
        async for event in self._events:
            if event.kind == "stderr":
                self._stderr_parts.append(event.data)
            elif event.kind == "exit":
                self.exit_code = event.exit_code
                self.duration_ms = event.duration_ms
        self.stderr = "".join(self._stderr_parts)

    async def drain(self) -> AsyncStreamResult:
        """Consume the stream, discarding stdout chunks. Returns self."""
        async for _ in self.stdout():
            pass
        return self
