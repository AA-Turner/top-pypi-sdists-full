"""Knowledge retrieval tool — `knowledge_search` (was `rag_search` until 2026-07-18).

Server-side native tool the agent can call to query the user's indexed
content (notes, code files, cloud files, library docs) via the hybrid
vector + lexical + RRF + rerank pipeline.

The package can't import aidream's RAG service directly (Package
Independence Rule). The host (aidream/package_integration.py) injects a
``rag_search`` callable through ``matrx_ai.configure(rag_search=...)``;
this handler resolves it lazily via ``get_ext`` and calls it with the
authenticated ctx.user_id. No client-side fanout, no httpx round-trip
back to /rag/search — same process, direct function call.

Returns hits as native dicts so the agent can cite them. The FE renders
them via the tool-call visualization registry (see the separate ticket
for clickable deep-links).
"""

from __future__ import annotations

import time
from typing import Any

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import RagSearchArgs
from matrx_ai.tools.document_validation import (
    PHYSICAL_PAGE_VALIDATION_GUIDANCE,
    build_physical_page_ref,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult


def _get_rag_search():
    from matrx_ai._ext import get_ext

    return get_ext("rag_search")


def _stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "knowledge_search"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _hit_to_dict(h: Any) -> dict[str, Any]:
    # The injected SearchHit exposes the chunk body as ``content_text``;
    # reading only ``snippet``/``content`` (neither of which exists) is what
    # silently handed the agent empty snippets — a "reference to a PDF" with
    # no readable text. ``content_text`` MUST stay first in this fallback.
    snippet_text = (
        getattr(h, "content_text", None)
        or getattr(h, "snippet", None)
        or getattr(h, "content", None)
        or ""
    )
    processed_document_id = getattr(h, "processed_document_id", None)
    page_numbers = getattr(h, "page_numbers", None) or []
    result = {
        "chunk_id": getattr(h, "chunk_id", None),
        "source_kind": getattr(h, "source_kind", None),
        "source_id": getattr(h, "source_id", None),
        "snippet": snippet_text[:1500],
        "score": getattr(h, "score", None),
        "vector_rank": getattr(h, "vector_rank", None),
        "lexical_rank": getattr(h, "lexical_rank", None),
        "rerank_score": getattr(h, "rerank_score", None),
        "metadata": getattr(h, "metadata", None) or {},
        "entities": getattr(h, "entities", []) or [],
        "entity_rank": getattr(h, "entity_rank", None),
        # Lineage handle (v0): the engine already computes these on every hit —
        # surfacing them lets the agent drill to the exact page/document/sibling
        # derivations without re-searching (the dream's §5a "lineage handle").
        "processed_document_id": processed_document_id,
        "primary_page_id": getattr(h, "primary_page_id", None),
        "page_numbers": page_numbers,
        "derivation_kind": getattr(h, "derivation_kind", None),
    }
    physical_page_ref = build_physical_page_ref(processed_document_id, page_numbers)
    if physical_page_ref is not None:
        result["physical_page_ref"] = physical_page_ref
    return result


def _entity_map_entry_to_dict(e: Any) -> dict[str, Any]:
    linked_raw = getattr(e, "linked", None) or []
    linked = [
        {
            "entity_id": getattr(lnk, "entity_id", None),
            "name": getattr(lnk, "name", None),
            "kind": getattr(lnk, "kind", None),
            "weight": getattr(lnk, "weight", None),
        }
        for lnk in linked_raw
    ]
    return {
        "entity_id": getattr(e, "entity_id", None),
        "name": getattr(e, "name", None),
        "kind": getattr(e, "kind", None),
        "mention_count": getattr(e, "mention_count", None),
        "artifact_count": getattr(e, "artifact_count", None),
        "source_kind_counts": dict(getattr(e, "source_kind_counts", None) or {}),
        "top_chunk_id": getattr(e, "top_chunk_id", None),
        "importance": getattr(e, "importance", None),
        "is_concept": getattr(e, "is_concept", False),
        "linked": linked,
    }


async def knowledge_search(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()

    try:
        parsed = RagSearchArgs(**args)
    except ValidationError as exc:
        return _stamp(
            ToolResult(
                success=False,
                error=ToolError(
                    error_type="invalid_args",
                    message=format_args_error(exc),
                ),
            ),
            started_at,
            ctx,
        )

    user_id = ctx.user_id
    if not user_id:
        return _stamp(
            ToolResult(
                success=False,
                error=ToolError(
                    error_type="unauthenticated",
                    message="knowledge_search requires an authenticated user.",
                ),
            ),
            started_at,
            ctx,
        )

    try:
        search_fn = _get_rag_search()
    except Exception as exc:
        return _stamp(
            ToolResult(
                success=False,
                error=ToolError(
                    error_type="unavailable",
                    message=(
                        f"RAG search backend not configured in this host: {exc}. "
                        "The host must call matrx_ai.configure(rag_search=...)."
                    ),
                ),
            ),
            started_at,
            ctx,
        )

    # The caller's active org rides the ToolContext (resolved from the live
    # AppContext). Forwarding it is what lets the search ACL's org branch
    # match org-shared chunks owned by teammates; hardcoding None here
    # silently hid ALL org-shared content from agents (2026-06-10 audit fix).
    organization_id = ctx.organization_id

    include_sources: list[dict[str, str]] | None = None
    if parsed.data_store_id:
        from matrx_ai._ext import get_ext, has_ext

        if has_ext("rag_materialize_member_filter"):
            materialize = get_ext("rag_materialize_member_filter")
            scoped = await materialize(
                store_id=parsed.data_store_id,
                user_id=user_id,
                organization_id=organization_id,
            )
            if not scoped:
                return _stamp(
                    ToolResult(
                        success=True,
                        output={
                            "query": parsed.query,
                            "hits": [],
                            "total_candidates": 0,
                            "data_store_id": parsed.data_store_id,
                            "note": (
                                "Data store is empty or not visible to this user; "
                                "no scope to search."
                            ),
                        },
                    ),
                    started_at,
                    ctx,
                )
            include_sources = scoped

    try:
        response = await search_fn(
            parsed.query,
            user_id=user_id,
            organization_id=organization_id,
            source_kinds=parsed.source_kinds,
            include_sources=include_sources,
            limit=parsed.limit,
            rerank=parsed.rerank,
            use_mmr=parsed.use_mmr,
            multi_query=parsed.multi_query,
            use_hyde=parsed.use_hyde,
            scope_ids=parsed.scope_ids,
            source_ids=parsed.source_ids,
        )
    except Exception as exc:
        return _stamp(
            ToolResult(
                success=False,
                error=ToolError.from_exception(
                    exc,
                    error_type="search_failed",
                    message=f"RAG search failed: {exc}",
                ),
            ),
            started_at,
            ctx,
        )

    hits = [_hit_to_dict(h) for h in getattr(response, "hits", [])]
    entity_map_raw = getattr(response, "entity_map", None) or []
    entity_map = [_entity_map_entry_to_dict(e) for e in entity_map_raw]
    matched_entities = list(getattr(response, "matched_entities", None) or [])
    result = ToolResult(
        success=True,
        output={
            "query": getattr(response, "query", parsed.query),
            "hits": hits,
            "total_candidates": int(getattr(response, "total_candidates", len(hits))),
            "embedding_model": getattr(response, "embedding_model", "") or "",
            "reranker_model": getattr(response, "reranker_model", None),
            "latency_ms": int(getattr(response, "latency_ms", 0) or 0),
            "matched_entities": matched_entities,
            "entity_map": entity_map,
            "validation_guidance": PHYSICAL_PAGE_VALIDATION_GUIDANCE,
        },
    )
    # CITABLE passages: the model-facing result carries each hit as a
    # SearchResultContent block (Anthropic `search_result` + citations enabled,
    # matrx:// identity source) so quotes come back as REAL citations with
    # file/page click-through. `output` (storage/trace/UI) stays unchanged.
    provider_blocks = _citable_blocks_for_hits(hits)
    if provider_blocks is not None:
        result.provider_content = provider_blocks
    return _stamp(result, started_at, ctx)


def _citable_blocks_for_hits(hits: list[dict[str, Any]]) -> list[Any] | None:
    """One citable SearchResultContent per snippet-bearing hit + a trailing
    TextContent with the metadata JSON (snippets removed — they live in the
    citable blocks; sending both would double the tokens)."""
    import copy
    import json

    from matrx_ai.config import SearchResultContent, TextContent

    meta_hits = copy.deepcopy(hits)
    blocks: list[Any] = []
    for hit in meta_hits:
        snippet = hit.pop("snippet", "")
        if not snippet:
            continue
        metadata = hit.get("metadata") or {}
        pages = hit.get("page_numbers") or []
        page = int(pages[0]) if pages else None
        name = (
            metadata.get("title")
            or metadata.get("file_name")
            or metadata.get("name")
            or metadata.get("source_label")
            or (hit.get("source_kind") or "Knowledge source")
        )
        title = f"{name} — page {page}" if page is not None else str(name)
        file_id = (
            str(hit["source_id"])
            if hit.get("source_kind") == "cld_file" and hit.get("source_id")
            else ""
        )
        blocks.append(
            SearchResultContent(
                texts=[snippet],
                title=title,
                file_id=file_id,
                document_id=str(hit.get("processed_document_id") or ""),
                page=page,
            )
        )
    if not blocks:
        return None
    payload_meta: dict[str, Any] = {"hits": meta_hits}
    from matrx_ai.config.unified_content import cap_citable_blocks

    blocks = cap_citable_blocks(blocks, payload_meta)
    payload_meta.update(
        passages_note=(
            "The passages above are citable search results (quote them and "
            "citations attach automatically). This JSON is the match metadata; "
            "snippets were moved into the passage blocks."
        ),
    )
    blocks.append(TextContent(text=json.dumps(payload_meta, ensure_ascii=False, default=str)))
    return blocks
