"""Streaming progress events for the RAG ingestion pipeline.

Why this matters
----------------
Large PDFs (workers'-comp files routinely run 200-500 pages) take many
seconds to ingest. Without per-stage telemetry the user sees a blank
spinner and assumes the system hung. This module gives every stage of
``ingest_pdf`` / ``ingest_image`` / ``ingest_source`` a structured
``rag.ingest.progress`` event the FE can render as a real-time progress
bar.

Event shape: :class:`matrx_rag.rag_events.RagIngestProgress` — a typed
Pydantic model sent via ``emitter.send_data(model)``. It travels as DATA
with the ``kind`` discriminator ``"rag.ingest.progress"``; unset optional
keys are omitted from the wire (historical dict parity).

Pass-through emitter
--------------------
A ``ProgressEmitter`` wraps an optional ``Emitter`` and degrades to a
no-op when none is supplied. Pipelines accept the wrapper rather than
the raw Emitter so:

  * Direct CLI / batch calls work without rigging up an emitter.
  * Streaming endpoints get full telemetry by passing the request emitter.
  * Unit tests can pass a stub recorder for assertions.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from matrx_rag.rag_events import RagIngestProgress, Stage

if TYPE_CHECKING:
    pass

__all__ = ["ProgressEmitter", "Stage", "from_emitter"]


@dataclass
class ProgressEmitter:
    """Optional wrapper around a matrx-connect ``Emitter``.

    All methods are async + best-effort: emitter failures are swallowed
    so a transient FE disconnect can never break ingestion. Use the
    ``recorded`` attribute in tests to assert the event sequence.
    """

    emitter: Any | None = None  # matrx_connect Emitter; Any avoids the import-time dep
    source_kind: str = ""
    source_id: str = ""
    started_at: float = field(default_factory=time.time)
    recorded: list[dict[str, Any]] = field(default_factory=list)

    def _elapsed_ms(self) -> int:
        return int((time.time() - self.started_at) * 1000)

    async def stage(
        self,
        stage: Stage,
        *,
        message: str | None = None,
        pages_total: int | None = None,
        pages_done: int | None = None,
        chunks_total: int | None = None,
        chunks_done: int | None = None,
        error: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        data: dict[str, Any] = {
            "source_kind": self.source_kind,
            "source_id": self.source_id,
            "stage": stage,
            "elapsed_ms": self._elapsed_ms(),
            "message": message,
            "pages_total": pages_total,
            "pages_done": pages_done,
            "chunks_total": chunks_total,
            "chunks_done": chunks_done,
            "error": error,
        }
        if extra:
            # Historical semantics: ad-hoc keys merge flat into the event,
            # and an explicit extra key wins over the named kwarg.
            data.update(extra)
        event = RagIngestProgress(**data)

        # ``recorded`` keeps the wire dict (exclude_none, extras flattened)
        # so test assertions see exactly what the FE sees.
        self.recorded.append(event.model_dump())
        if self.emitter is None:
            return
        try:
            await self.emitter.send_data(event)
        except Exception:
            # Streaming-side failures must not bubble — the ingestion is
            # the source of truth, telemetry is best-effort.
            pass

    async def info(self, code: str, message: str, **extra: Any) -> None:
        """Send a human-readable info event using the existing
        InfoPayload schema. Useful for "page 12 of 250 extracted" style
        per-batch updates that the FE may render as console output.
        """
        if self.emitter is None:
            return
        try:
            from matrx_connect.context.events import InfoPayload

            await self.emitter.send_info(
                InfoPayload(
                    code=code,
                    system_message=message,
                    user_message=message,
                    metadata={
                        "source_kind": self.source_kind,
                        "source_id": self.source_id,
                        **extra,
                    },
                )
            )
        except Exception:
            pass


def from_emitter(
    emitter: Any | None,
    *,
    source_kind: str,
    source_id: str,
) -> ProgressEmitter:
    return ProgressEmitter(
        emitter=emitter,
        source_kind=source_kind,
        source_id=source_id,
    )
