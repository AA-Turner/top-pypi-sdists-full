"""Image → indexed chunks pipeline.

Mirrors the PDF pipeline: when a ``cld_files`` row's mime type is an
image we recognize, we route through here:

    fetch (S3 / URL → local bytes)
      → vision-LLM analysis → structured metadata
        (alt_text, caption, title, description, keywords, dominant_colors)
      → persist to cld_files.metadata.image
      → build retrieval chunk from alt_text + caption + description + keywords
      → embed + upsert

The output schema follows the FE team's original 2026-04 image-metadata spec
verbatim so the existing Metadata tab UI renders without translation. (That
spec doc was consolidated away 2026-08-25 — do not change these field names
without checking the Metadata tab.)

ONE vision path, through the host seam (2026-09-25)
--------------------------------------------------
There used to be two: ``analyze_image`` built a raw OpenAI client (borrowed
from the embeddings module) and ran ``gpt-4o`` with the prompt below, while the
PDF figure path went through the host-injected ``llm_provider`` seam. The raw
path was a mandate bypass the raw-client guard could not see (it rode an
allowlisted embeddings helper). Both now go through
:func:`analyze_image_unified` → ``llm_provider.chat(purpose="image_caption")``.
In aidream that seam resolves the ``rag.image_caption`` mandate and runs the
Holder's model and instructions. The package sends no instructions of its own: the
host provider (``configure(llm_provider=...)``) owns them per ``purpose``.
"""

from __future__ import annotations

import base64
import asyncio
import hashlib
import json
import logging
import uuid
from pathlib import Path
from typing import Any

from matrx_rag.chunking import CHUNKER_VERSION, Chunk, _tok_len
from matrx_rag.embeddings import (
    default_text_model,
    embed,
)
from matrx_rag.ingestion import (
    IngestionResult,
    _embed_text_for,
    attach_context_prefixes,
    contextual_retrieval_enabled,
    upsert_chunks,
)
from matrx_rag.sources import ResolvedSource

logger = logging.getLogger(__name__)


IMAGE_MIMES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp",
    "image/gif",
    "image/heic",
    "image/heif",
    "image/bmp",
}


async def _read_local_bytes(local_path: str) -> bytes | None:
    path = Path(local_path)
    if not await asyncio.to_thread(path.exists):
        return None
    return await asyncio.to_thread(path.read_bytes)


def _normalize_vision_payload(parsed: dict[str, Any]) -> dict[str, Any]:
    """Normalize a raw vision JSON object into the canonical enrichment shape.

    The ONE normalizer for the vision seam's reply, so every caller gets the
    SAME dict:
    ``alt_text, caption, title, description, keywords[], dominant_colors[],
    ocr_text``. Missing keys default; keywords are lowercased + de-duped
    (order-preserving) and capped at 20.
    """
    normalised = {
        "alt_text": str(parsed.get("alt_text", "")).strip(),
        "caption": str(parsed.get("caption", "")).strip(),
        "title": str(parsed.get("title", "")).strip(),
        "description": str(parsed.get("description", "")).strip(),
        "keywords": [
            str(k).strip().lower() for k in (parsed.get("keywords") or []) if str(k).strip()
        ],
        "dominant_colors": [
            str(c).strip() for c in (parsed.get("dominant_colors") or []) if str(c).strip()
        ],
        "ocr_text": str(parsed.get("ocr_text", "")).strip(),
    }
    # Dedup keywords while preserving order.
    seen: set[str] = set()
    deduped: list[str] = []
    for k in normalised["keywords"]:
        if k not in seen:
            seen.add(k)
            deduped.append(k)
    normalised["keywords"] = deduped[:20]
    return normalised


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


# The default vision model for the provider-agnostic path is HOST-SUPPLIED —
# ``matrx_rag.configure(default_vision_model=...)``, read via
# ``_ext.get_default_vision_model()``. This used to be a literal
# ``ai.model_definition`` row UUID from OUR database, which meant nothing in
# any other install. The host names the model; the package just uses it.


class VisionAnalysisError(RuntimeError):
    """The image could not be analyzed. Never an empty enrichment in disguise:
    an image indexed with no caption is unsearchable, and that must be said."""


async def _record_vision_failure(exc: BaseException, *, context: dict[str, Any]) -> None:
    logger.error("rag.image_pipeline: vision analysis FAILED — %s", exc)
    try:
        from matrx_utils import capture_error

        await capture_error(exc, kind="rag_vision_analysis_failed", context=context)
    except Exception as capture_exc:  # noqa: BLE001 — the scream above already fired
        logger.error("rag.image_pipeline: could not record the vision failure: %s", capture_exc)


async def analyze_image_unified(
    *,
    bytes_b64: str,
    mime_type: str = "image/png",
    model: str,
    file_id: str | None = None,
) -> dict[str, Any]:
    """Provider-agnostic vision analysis via the unified model layer.

    Returns the normalized enrichment dict (``alt_text, caption, title,
    description, keywords[], dominant_colors[], ocr_text``), routed through the host-injected ``llm_provider`` seam
    (``matrx_rag.configure(llm_provider=...)``) so it works with ANY vision-capable
    model — notably Gemini, which the raw OpenAI client path can't reach. The host
    (aidream) injects a matrx-ai-backed provider; standalone installs fall back to
    the default OpenAI vision provider. matrx-rag NEVER imports matrx-ai directly
    (CLAUDE.md rule #1 — package independence). Used by the PDF figure-caption
    derivation.

    Used by BOTH the PDF figure-caption derivation and :func:`ingest_image`.

    On ANY exception or empty/unparseable output returns ``{}`` — callers treat
    an empty dict as "no caption" and isolate that page.
    """
    if not bytes_b64:
        return {}

    # Vision goes through the host-injected llm_provider seam, NEVER a direct
    # matrx-ai import (that would break standalone-first independence). The
    # provider receives OpenAI-style chat messages (the seam's lingua franca);
    # the matrx-ai-backed host adapter translates them + selects the registry
    # model, while the default OpenAI provider forwards them verbatim.
    from matrx_rag._ext import get_llm_provider, provider_call_kwargs

    data_uri = f"data:{mime_type};base64,{bytes_b64}"
    messages = [
        {
            "role": "user",
            # The image only: the Holder authors the instruction turn.
            "content": [
                {"type": "image_url", "image_url": {"url": data_uri}},
            ],
        },
    ]

    try:
        raw = await get_llm_provider().chat(
            messages,
            model=model,
            temperature=0,
            max_tokens=1500,
            response_format="json",
            purpose="image_caption",
            # The image BY NAME (a MediaRef — its file when known), so a
            # workflow Holder gets it as an input, not buried in a composed turn.
            **provider_call_kwargs(
                get_llm_provider().chat,
                {"image": {"file_id": str(file_id), "mime_type": mime_type}}
                if file_id
                else {"image": {"url": data_uri, "mime_type": mime_type}},
            ),
        )
    except Exception as exc:  # noqa: BLE001 — every cause is one refusal, named
        raise VisionAnalysisError(f"the caption call failed: {type(exc).__name__}: {exc}") from exc

    if not raw or not raw.strip():
        raise VisionAnalysisError("the caption model returned nothing")
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise VisionAnalysisError("the caption model did not return JSON") from exc
    if not isinstance(parsed, dict):
        raise VisionAnalysisError("the caption model returned JSON that is not an object")
    return _normalize_vision_payload(parsed)


def _build_image_chunk(
    *,
    enrichment: dict[str, Any],
    file_name: str | None,
    storage_uri: str | None,
) -> Chunk:
    """Compose the retrieval chunk text from the vision payload.

    Ordering: title → caption → alt → description → keywords → ocr.
    All fields are joined with double newlines so the chunk reads
    naturally and embeds well.
    """
    parts: list[str] = []
    title = enrichment.get("title")
    if title:
        parts.append(f"Title: {title}")
    if file_name:
        parts.append(f"File: {file_name}")
    if enrichment.get("caption"):
        parts.append(f"Caption: {enrichment['caption']}")
    if enrichment.get("alt_text"):
        parts.append(f"Alt text: {enrichment['alt_text']}")
    if enrichment.get("description"):
        parts.append(f"Description: {enrichment['description']}")
    if enrichment.get("keywords"):
        parts.append(f"Keywords: {', '.join(enrichment['keywords'])}")
    if enrichment.get("ocr_text"):
        parts.append(f"Text in image: {enrichment['ocr_text']}")
    body = "\n\n".join(parts).strip()
    return Chunk(
        chunk_id=str(uuid.uuid4()),
        parent_chunk_id=None,
        chunk_index=0,
        chunk_kind="image_caption",
        content_text=body,
        token_count=_tok_len(body),
        language=None,
        metadata={
            "role": "leaf",
            "file_name": file_name,
            "storage_uri": storage_uri,
            "image": enrichment,
        },
    )


async def ingest_image(
    *,
    cld_file_id: str,
    organization_id: str | None,
    owner_id: str,
    local_path: str,
    file_name: str | None = None,
    storage_uri: str | None = None,
    mime_type: str = "image/png",
    embedding_model: str | None = None,
    force: bool = False,
    emitter: Any | None = None,
    allow_global_org: bool = False,
) -> IngestionResult:
    """End-to-end: fetch → vision analysis → persist enrichment →
    build a single chunk → embed → upsert.
    """
    from matrx_rag.progress import from_emitter

    progress = from_emitter(emitter, source_kind="cld_file", source_id=cld_file_id)
    await progress.stage("fetch", message=f"Reading image {file_name or local_path}")

    raw_bytes = await _read_local_bytes(local_path)
    if raw_bytes is None:
        await progress.stage("error", error="local_path_missing")
        return IngestionResult(
            source_kind="cld_file",
            source_id=cld_file_id,
            field_id=None,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model=embedding_model or default_text_model(),
            error="local_path_missing",
        )

    source_hash = hashlib.sha256(raw_bytes).hexdigest()
    embed_model = embedding_model or default_text_model()

    # Hash dedup before paying for vision call.
    if not force:
        from matrx_rag._ext import get_db_model

        KgChunks = get_db_model("KgChunks")
        rows = (
            await KgChunks.filter(
                source_kind="cld_file",
                source_id=cld_file_id,
                field_id__isnull=True,
            )
            .order_by("-created_at")
            .limit(1)
            .values("source_hash")
        )
        existing = rows[0]["source_hash"] if rows else None
        if existing == source_hash:
            await progress.stage("complete", message="Skipped (unchanged)")
            return IngestionResult(
                source_kind="cld_file",
                source_id=cld_file_id,
                field_id=None,
                chunks_written=0,
                embeddings_written=0,
                skipped_unchanged=True,
                embedding_model=embed_model,
            )

    # Vision analysis.
    await progress.stage("extract", message="Vision analysis")
    bytes_b64 = base64.b64encode(raw_bytes).decode("ascii")
    from matrx_rag._ext import get_default_vision_model

    failure: str | None = None
    try:
        enrichment = await analyze_image_unified(
            bytes_b64=bytes_b64,
            mime_type=mime_type,
            model=get_default_vision_model(),
            file_id=str(cld_file_id),
        )
        if not enrichment.get("alt_text"):
            raise VisionAnalysisError("the caption model returned no alt text")
    except VisionAnalysisError as exc:
        failure = str(exc)
        await _record_vision_failure(exc, context={"cld_file_id": cld_file_id})

    if failure is not None:
        error = f"vision_analysis_failed: {failure}"
        await progress.stage("error", error=error)
        return IngestionResult(
            source_kind="cld_file",
            source_id=cld_file_id,
            field_id=None,
            chunks_written=0,
            embeddings_written=0,
            skipped_unchanged=False,
            embedding_model=embed_model,
            error=error,
        )

    # Persist the enrichment to cld_files.metadata.image so the FE
    # Metadata tab can render it without re-running the vision call. Atomic
    # shallow merge (never clobbers sibling metadata keys) via the ORM's
    # JsonbMerge primitive — no read-modify-write race.
    from datetime import UTC, datetime

    from matrx_orm import JsonbMerge

    from matrx_rag._ext import get_db_model

    Files = get_db_model("Files")
    await Files.update_where(
        {"id": cld_file_id},
        metadata=JsonbMerge("metadata", {"image": enrichment}),
        updated_at=datetime.now(UTC),
    )

    chunk = _build_image_chunk(
        enrichment=enrichment,
        file_name=file_name,
        storage_uri=storage_uri,
    )
    chunks = [chunk]

    if contextual_retrieval_enabled():
        await attach_context_prefixes(chunks)

    vectors = await embed(
        embed_model,
        [_embed_text_for(c) for c in chunks],
        input_type="document",
        # Provenance on the shared embedding cache: this image's organization.
        organization_id=organization_id,
    )

    resolved = ResolvedSource(
        source_kind="cld_file",
        source_id=cld_file_id,
        field_id=None,
        owner_id=owner_id,
        organization_id=organization_id,
        text=chunk.content_text,
        mime_type=mime_type,
        language=None,
        source_hash=source_hash,
        metadata={
            "file_name": file_name,
            "storage_uri": storage_uri,
            "image": enrichment,
            "chunker": "image_vision_v1",
        },
    )
    await progress.stage("upsert", message="Persisting image chunk + embedding")
    write_result = await upsert_chunks(
        resolved=resolved,
        chunks=chunks,
        embedding_model=embed_model,
        embeddings=vectors,
        allow_global_org=allow_global_org,
    )
    written = write_result["chunks_written"]
    await progress.stage(
        "complete",
        message=f"Indexed image with {len(enrichment.get('keywords', []))} keywords",
        chunks_total=written,
        chunks_done=written,
    )
    return IngestionResult(
        source_kind="cld_file",
        source_id=cld_file_id,
        field_id=None,
        chunks_written=written,
        embeddings_written=written,
        skipped_unchanged=False,
        embedding_model=embed_model,
    )


# Silence unused-import warnings.
_ = (CHUNKER_VERSION,)


__all__ = [
    "IMAGE_MIMES",
    "analyze_image_unified",
    "ingest_image",
]
