"""Host-injected durable transport journal seam.

The connect package owns wire framing, but must not know whether a host uses
Postgres, a test double, or another durable transport. A sink accepts exact
already-encoded NDJSON bytes and invokes ``publish`` only after they commit.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Protocol

from matrx_connect.context.app_context import AppContext


CommittedPublisher = Callable[[bytes], Awaitable[None]]


class StreamJournalSink(Protocol):
    """One bounded, ordered sink for one immutable stream segment."""

    stream_id: str

    async def enqueue(
        self, *, sequence: int, wire: bytes, publish: CommittedPublisher
    ) -> None:
        """Accept one frame and arrange its commit-before-publish delivery."""

    async def close(self, *, status: str, last_seq: int) -> None:
        """Flush all accepted frames and durably terminalize the segment."""


StreamJournalSinkFactory = Callable[[AppContext], Awaitable[StreamJournalSink | None]]

_sink_factory: StreamJournalSinkFactory | None = None


def configure_stream_journal_sink_factory(factory: StreamJournalSinkFactory | None) -> None:
    """Install the host seam once at startup; ``None`` disables journaling."""
    global _sink_factory
    _sink_factory = factory


async def create_stream_journal_sink(ctx: AppContext) -> StreamJournalSink | None:
    factory = _sink_factory
    return await factory(ctx) if factory is not None else None
