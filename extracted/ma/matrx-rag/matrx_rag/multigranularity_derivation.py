"""
U7 — Multi-granularity chunking (a Knowledge Asset derivation).

Premium retrieval gives the reranker more than one window onto the same content:
a COARSE lane (panoramic, ~page-level) and a FINE lane (precise, tight matches),
each its own `derivation_kind='chunked_{coarse,fine}'` chunk set. The cross-
encoder reranker then picks the granularity that best answers each query —
coarse for "explain section X", fine for "what is the exact value of Y".

A thin *generator* on `matrx_rag.derivation.derive_chunk_set`: per page, split
the page text at each granularity's token window and hand the blocks over. Pages
are chunked independently so every chunk stays page-anchored (verification +
section faceting). Re-running replaces the chunk set for that granularity only.

Prefers `cleaned_text` per page, falls back to `raw_text` — so it works on a
clean asset OR a raw library-profile ingest (the AMA Guides). `page_numbers`
lets a curator re-derive just part of a doc (incremental / cost-bounded).
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass, field

from langchain_text_splitters import RecursiveCharacterTextSplitter

from matrx_rag._ext import NotFoundError, get_db_model
from matrx_rag.chunking import _tok_len
from matrx_rag.derivation import ChunkSpec, DeriveResult, derive_chunk_set
from matrx_rag.stages import ProgressCb, StageEvent, _noop

log = logging.getLogger(__name__)

# (token window, token overlap) per granularity. "normal" is intentionally
# omitted — the default ingest chunker already produces a ~normal set; coarse +
# fine are the lanes that add reranker choice.
GRANULARITIES: dict[str, tuple[int, int]] = {
    "coarse": (1200, 120),
    "fine": (320, 64),
}


@dataclass
class MultiGranularityResult:
    processed_document_id: str
    pages_used: int
    per_granularity: dict[str, int] = field(default_factory=dict)  # granularity -> chunks written

    @property
    def chunks_written(self) -> int:
        """Total chunks written across all granularities.

        Uniform contract: every derive-runner result exposes ``chunks_written``
        so the generic derive-stream handler (rag.py::_run_derive_stream) can
        settle the derive_runs row without special-casing this result type —
        it previously crashed with AttributeError here.
        """
        return sum(self.per_granularity.values())


async def derive_multigranularity_chunks(
    processed_document_id: str,
    *,
    granularities: Iterable[str] | None = None,
    page_numbers: set[int] | None = None,
    embedding_model: str | None = None,
    rag_boost: int = 0,
    on_progress: ProgressCb = _noop,
) -> MultiGranularityResult:
    """Build coarse + fine `chunked_{g}` derivation sets for the doc.

    Each granularity is one derive_chunk_set call (one derivative doc). Returns
    per-granularity chunk counts.
    """
    kinds = list(granularities) if granularities is not None else list(GRANULARITIES)
    for g in kinds:
        if g not in GRANULARITIES:
            raise ValueError(f"unknown granularity {g!r}; known: {sorted(GRANULARITIES)}")

    ProcessedDocuments = get_db_model("ProcessedDocuments")
    doc_rows = await ProcessedDocuments.filter(id=processed_document_id).values("id", "name")
    doc = doc_rows[0] if doc_rows else None
    if doc is None:
        raise NotFoundError(f"processed_document {processed_document_id} not found")
    pages = await (
        get_db_model("ProcessedDocumentPages")
        .filter(processed_document_id=processed_document_id)
        .order_by("page_index")
        .values("page_number", "cleaned_text", "raw_text")
    )

    # (page_number, text) — prefer cleaned, fall back to raw; skip blank pages.
    page_texts: list[tuple[int, str]] = []
    for p in pages:
        pn = int(p["page_number"])
        if page_numbers is not None and pn not in page_numbers:
            continue
        text = (p["cleaned_text"] or p["raw_text"] or "").strip()
        if text:
            page_texts.append((pn, text))

    result = MultiGranularityResult(
        processed_document_id=processed_document_id,
        pages_used=len(page_texts),
    )
    if not page_texts:
        log.info("[multigranularity] doc=%s: no page text", processed_document_id)
        await on_progress(
            StageEvent(
                stage="multigranularity",
                phase="done",
                message="No page text to chunk",
                current=0,
                total=len(kinds),
                extra={"granularity": None, "pages_used": 0, "chunks_written": 0},
            )
        )
        return result

    total_g = len(kinds)
    await on_progress(
        StageEvent(
            stage="multigranularity",
            phase="started",
            message=f"Building {total_g} granularity lane(s) over {len(page_texts)} page(s)",
            current=0,
            total=total_g,
            extra={"granularities": kinds, "pages_used": len(page_texts)},
        )
    )

    for g_idx, g in enumerate(kinds, start=1):
        size, overlap = GRANULARITIES[g]
        # Per granularity: emit BEFORE building/writing this lane. This await
        # is also the cooperative cancel point.
        await on_progress(
            StageEvent(
                stage="multigranularity",
                phase="progress",
                message=f"Chunking granularity {g!r} ({g_idx} / {total_g})",
                current=g_idx,
                total=total_g,
                extra={"granularity": g, "pages_used": len(page_texts)},
            )
        )
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            chunk_overlap=overlap,
            length_function=_tok_len,
            is_separator_regex=False,
        )
        specs: list[ChunkSpec] = []
        idx = 0
        for pn, text in page_texts:
            for block_i, block in enumerate(splitter.split_text(text)):
                block = block.strip()
                if not block:
                    continue
                specs.append(
                    ChunkSpec(
                        content_text=block,
                        chunk_index=idx,
                        page_numbers=[pn],
                        primary_page_number=pn,
                        chunk_kind=f"chunked_{g}",
                        metadata={
                            "role": "multigranularity",
                            "granularity": g,
                            "page_number": pn,
                            "block_index": block_i,
                        },
                    )
                )
                idx += 1

        res: DeriveResult = await derive_chunk_set(
            parent_processed_id=processed_document_id,
            derivation_kind=f"chunked_{g}",
            chunks=specs,
            identity={"granularity": g, "source": "multigranularity"},
            name=f"{doc['name']} ({g} chunks)",
            rag_boost=rag_boost,
            embedding_model=embedding_model,
            chunker_name=f"multigranularity:{g}",
            metadata={"granularity": g, "pages_used": len(page_texts)},
        )
        result.per_granularity[g] = res.chunks_written
        log.info(
            "[multigranularity] doc=%s granularity=%s chunks=%d",
            processed_document_id,
            g,
            res.chunks_written,
        )

    total_chunks = sum(result.per_granularity.values())
    await on_progress(
        StageEvent(
            stage="multigranularity",
            phase="done",
            message=f"Built {total_g} lane(s), {total_chunks} chunk(s)",
            current=total_g,
            total=total_g,
            extra={
                "granularities": kinds,
                "pages_used": len(page_texts),
                "per_granularity": dict(result.per_granularity),
                "chunks_written": total_chunks,
            },
        )
    )

    return result


__all__ = ["derive_multigranularity_chunks", "MultiGranularityResult", "GRANULARITIES"]
