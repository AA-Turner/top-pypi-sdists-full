"""Package-owned typed stream-event payloads for matrx-rag.

Every event this package emits through a matrx-connect ``Emitter`` is one of
the Pydantic models below — ``emitter.send_data(<dict>)`` is banned. The
models preserve the historical wire shapes byte-for-byte:

* the discriminator field is ``kind`` (NOT ``type`` — these events predate
  the matrx-connect ``DataPayload`` registry, which discriminates on
  ``type``; renaming would break every FE consumer), and
* per-event null-key semantics match the old dict literals exactly:
  ``rag.ingest.progress`` OMITS unset optional keys (the old dict only added
  keys when a value was present), while ``rag.ingest.error`` always ships
  every key, ``null`` included.

The per-hit ``rag.citation`` / ``rag.citation.summary`` search events were
DELETED 2026-08-08: they were a parallel citation channel with zero live
consumers (the FE only reads the terminal ``rag.search.result``), superseded
by provider-native citations — RAG tool results are emitted as citable
``search_result`` blocks, so answer citations flow through the unified
``citation`` stream event. Do not reintroduce a second citation vocabulary.

matrx-rag cannot import matrx-connect (package boundary), so these are plain
``BaseModel``s — the emitter serializes them via ``model_dump()``. The host
(aidream) guards these schemas with a checked-in snapshot test
(``aidream/api/tests/test_rag_event_schemas.py``) so hand-written FE types
have a drift alarm.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

Stage = Literal[
    "fetch",
    "extract",
    "classify",
    "cleanup",
    "chunk",
    "enrich",
    "embed",
    "upsert",
    "graph",
    "complete",
    "error",
]


class RagIngestProgress(BaseModel):
    """Per-stage telemetry for ``ingest_source`` / ``ingest_pdf`` /
    ``ingest_image`` (emitted by :class:`matrx_rag.progress.ProgressEmitter`).

    ``extra="allow"`` because callers may attach ad-hoc keys via the
    ``extra=`` kwarg of ``ProgressEmitter.stage`` — those historically merged
    flat into the event dict and must keep doing so.
    """

    model_config = ConfigDict(extra="allow")

    kind: Literal["rag.ingest.progress"] = "rag.ingest.progress"
    source_kind: str
    source_id: str
    stage: Stage
    elapsed_ms: int
    message: str | None = None
    pages_total: int | None = None
    pages_done: int | None = None
    chunks_total: int | None = None
    chunks_done: int | None = None
    error: str | None = None

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        # Wire parity: the historical dict literal only included optional
        # keys when set. The emitter serializes via model_dump(), so default
        # to exclude_none here (callers can still override explicitly).
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(**kwargs)


class RagIngestError(BaseModel):
    """Structured ingest failure (today: unsupported MIME) so the FE can tell
    the user why a document will never leave ``status=pending``. All keys are
    always present (``null`` when unknown) — historical wire shape."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["rag.ingest.error"] = "rag.ingest.error"
    error_type: str
    source_kind: str
    source_id: str
    mime_type: str | None = None
    file_name: str | None = None
    message: str
    hint: str | None = None


RAG_EVENT_MODELS: tuple[type[BaseModel], ...] = (
    RagIngestProgress,
    RagIngestError,
)

__all__ = [
    "RAG_EVENT_MODELS",
    "RagIngestError",
    "RagIngestProgress",
    "Stage",
]
