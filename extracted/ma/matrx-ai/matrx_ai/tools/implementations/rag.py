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
from matrx_ai.tools.output_caps import self_bounded_result

# ---------------------------------------------------------------------------
# Model-facing size caps (knobs, feature ``agents.knowledge_search``)
# ---------------------------------------------------------------------------
# Benchmark P6 (2026-11-02, conversations 34756283 / a4f1287f): 20 calls at limit=3
# stored 10k-43k chars each — the passages were ~4.5k; the rest was per-hit indexing
# metadata (4-5k per image hit), the entity_map (9k) and full section JSON (10k), and the
# model was handed most of it on every iteration. The model now gets a VIEW of the
# result: each hit as a ranked window around the query's words (with chunk/source id and
# title), the sections as one line per item, and the whole view held to a per-call
# budget. The stored ``output`` stays complete for the UI and lineage.
KNOWLEDGE_SEARCH_KNOB_FEATURE = "agents.knowledge_search"
SNIPPET_WINDOW_KNOB = (KNOWLEDGE_SEARCH_KNOB_FEATURE, "snippet_window_chars")
OUTPUT_BUDGET_KNOB = (KNOWLEDGE_SEARCH_KNOB_FEATURE, "output_budget_chars")
# KNOB MIRROR — the standalone (no host) values; the seeded rows carry the same numbers
# (db/migrations/ai_137_knowledge_search_output_caps.sql).
SNIPPET_WINDOW_CHARS = 700
OUTPUT_BUDGET_CHARS = 12_000
# The stored hit keeps a wider window (what the person's result card shows).
STORED_SNIPPET_CHARS = 1500

#: ``async (organization_id) -> {"snippet_window_chars": int, "output_budget_chars": int}``.
_CAPS_RESOLVER: Any = None


def set_knowledge_search_caps_resolver(resolver: Any) -> None:
    """Install the host's per-organization knob reader (``None`` = standalone)."""
    global _CAPS_RESOLVER
    _CAPS_RESOLVER = resolver


async def knowledge_search_caps(organization_id: str | None) -> dict[str, int]:
    """This organization's caps. A resolver failure is announced; the search never fails over it."""
    caps = {"snippet_window_chars": SNIPPET_WINDOW_CHARS, "output_budget_chars": OUTPUT_BUDGET_CHARS}
    if _CAPS_RESOLVER is None:
        return caps
    try:
        got = await _CAPS_RESOLVER(organization_id)
        for key in caps:
            if got and got.get(key) is not None:
                caps[key] = max(1, int(got[key]))
    except Exception as exc:  # noqa: BLE001 — announced, never a failed search
        import sys

        print(
            f"[matrx_ai] knowledge_search caps knob read failed ({exc!r}); using the mirrored "
            f"defaults {caps}",
            file=sys.stderr,
        )
    return caps


_STOP = frozenset(
    "the and for with from that this what which who whom whose are was were has have had "
    "not but all any can its into onto out our their them they you your about over under".split()
)


def _query_terms(query: str) -> list[str]:
    import re

    seen: list[str] = []
    for word in re.findall(r"[\w'-]+", (query or "").lower()):
        if len(word) >= 3 and word not in _STOP and word not in seen:
            seen.append(word)
    return seen


def snippet_window(text: str, query: str, window: int) -> str:
    """The ``window``-char span of ``text`` that holds the most distinct query words
    (ties: the earliest), snapped to word boundaries and marked with an ellipsis where
    text was cut. Text that already fits is returned whole."""
    text = text or ""
    if window <= 0 or len(text) <= window:
        return text
    lower = text.lower()
    terms = _query_terms(query)
    positions: list[int] = []
    phrase = " ".join((query or "").lower().split())
    for needle in ([phrase] if len(phrase) >= 3 else []) + terms:
        start = lower.find(needle)
        while start != -1 and len(positions) < 400:
            positions.append(start)
            start = lower.find(needle, start + 1)
    best_start, best_score = 0, -1
    for pos in sorted(set(positions)):
        start = max(0, min(pos - window // 4, len(text) - window))
        span = lower[start : start + window]
        score = sum(1 for t in terms if t in span) + (2 if phrase and phrase in span else 0)
        if score > best_score:
            best_start, best_score = start, score
    start = best_start
    end = start + window
    if start > 0:
        space = text.find(" ", start, start + 40)
        start = space + 1 if space != -1 else start
    if end < len(text):
        space = text.rfind(" ", end - 40, end)
        end = space if space > start else end
    body = text[start:end].strip()
    return ("…" if start > 0 else "") + body + ("…" if end < len(text) else "")


_VIEW_HIT_FIELDS = (
    "chunk_id",
    "source_kind",
    "source_id",
    "processed_document_id",
    "page_numbers",
    "physical_page_ref",
    "score",
    "rerank_score",
)
_VIEW_TOP_FIELDS = (
    "query",
    "total_candidates",
    "relevance_verdict",
    "relevance_floor",
    "below_floor_dropped",
    "recall_lane_errors",
    "recall_lane_note",
    "no_relevant_matches",
    "note",
    "matched_entities",
    "scope_note",
    "searched_scope_ids",
    "searched_source_ids",
    "data_store_id",
    "sections_note",
    "section_errors",
)

READ_MORE_NOTE = (
    "Each passage is a window of its Segment around your query's words. Read a whole "
    "Segment with knowledge_open entity='segment' id=<chunk_id>, a whole Source with "
    "knowledge_open entity='processed_document' id=<processed_document_id>."
)


def model_view(
    output: dict[str, Any],
    *,
    window_chars: int = SNIPPET_WINDOW_CHARS,
    budget_chars: int = OUTPUT_BUDGET_CHARS,
) -> dict[str, Any]:
    """What the MODEL is handed for one knowledge_search result (pure; ``output`` untouched).

    Each hit → its ids, title and a ranked snippet window; the sections → one line per item;
    the entity_map and per-hit indexing metadata stay in the stored output only. The whole
    view (passages + JSON) is held to ``budget_chars``: section lines go first (last
    sections first), then the lowest-ranked hits whole; every cut is announced in
    ``output_budget`` with how to read more."""
    import json

    from matrx_ai.config.citations import passage_source_name

    query = str(output.get("query") or "")
    view: dict[str, Any] = {k: output[k] for k in _VIEW_TOP_FIELDS if output.get(k) not in (None, [], "")}
    hits: list[dict[str, Any]] = []
    for raw in output.get("hits") or []:
        if not isinstance(raw, dict):
            continue
        hit = {k: raw[k] for k in _VIEW_HIT_FIELDS if raw.get(k) not in (None, [], "")}
        title = passage_source_name(raw)
        if title:
            hit["title"] = " ".join(title.split())[:120]
        snippet = str(raw.get("snippet") or "")
        hit["snippet"] = snippet_window(snippet, query, window_chars)
        hits.append(hit)
    view["hits"] = hits
    sections_text = render_sections_for_model(output) if output.get("sections") or output.get("section_errors") else None
    lines = sections_text.split("\n") if sections_text else []

    budget: dict[str, Any] = {
        "budget_chars": budget_chars,
        "snippet_window_chars": window_chars,
        "read_more": READ_MORE_NOTE,
    }
    view["output_budget"] = budget
    note_reserve = 260  # the cut announcement written below, counted before cutting

    def size() -> int:
        return (
            len(json.dumps(view, ensure_ascii=False, default=str))
            + sum(len(x) + 1 for x in lines)
            + note_reserve
        )

    hits_dropped = 0
    lines_dropped = 0
    # Section lines go first — always the last item of the section with the most items left,
    # so every section (agents_workflows, records… at the end of the list too) keeps its
    # header and its best items. Headers stay.
    while size() > budget_chars:
        groups: list[list[int]] = []
        for idx, line in enumerate(lines):
            if line.startswith("- ") and groups:
                groups[-1].append(idx)
            else:
                groups.append([])
        biggest = max(groups, key=len, default=[])
        if not biggest:
            break
        lines.pop(biggest[-1])
        lines_dropped += 1
    while size() > budget_chars and len(hits) > 1:
        hits.pop()
        hits_dropped += 1
    if lines:
        view["sections_text"] = "\n".join(lines)
    if hits_dropped or lines_dropped:
        budget["hits_dropped"] = hits_dropped
        budget["section_lines_dropped"] = lines_dropped
        budget["note"] = (
            f"This result was held to {budget_chars:,} chars: "
            + (f"{lines_dropped} section line(s) " if lines_dropped else "")
            + ("and " if lines_dropped and hits_dropped else "")
            + (f"{hits_dropped} lowest-ranked hit(s) " if hits_dropped else "")
            + "were left out. Narrow the query or lower limit to see them."
        )
    # Keep the budget block last in the JSON (it reads as the footer).
    view["output_budget"] = view.pop("output_budget")
    return view


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


def _hit_to_dict(h: Any, query: str = "") -> dict[str, Any]:
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
        "snippet": snippet_window(snippet_text, query, STORED_SNIPPET_CHARS),
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


@self_bounded_result
async def knowledge_search(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()

    try:
        parsed = RagSearchArgs(**args)
    except ValidationError as exc:
        return _stamp(
            ToolResult(
                success=False,
                error=ToolError.declared(exc=exc, 
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
                    refusal=True,
                    error_type="unauthenticated",
                    message="knowledge_search requires an authenticated user.",
                ),
            ),
            started_at,
            ctx,
        )

    from matrx_ai._ext import get_ext, has_ext

    # The caller's active org rides the ToolContext. It ATTRIBUTES the search (spend,
    # audit); reach is the person's own access (2026-09-23). Hardcoding None here once
    # hid org-shared content from agents (2026-06-10), so it is still forwarded.
    organization_id = ctx.organization_id

    # Default narrowing to what the conversation is attached to — unless the agent
    # chose its own containers with `within` (then it searches exactly those).
    requested_scopes = parsed.scope_ids
    if requested_scopes is None and parsed.within:
        requested_scopes = []
    scope_ids, scope_document_ids, scope_note, searched_scope_ids = await _resolve_scope_ids(
        requested_scopes, ctx, user_id=user_id, organization_id=organization_id
    )

    sections_payload: dict[str, Any] | None = None
    segment_failure: dict[str, Any] | None = None
    if has_ext("knowledge_search_service"):
        # THE ONE SEARCH SERVICE (Knowledge Hub §3). Old fields map onto the query:
        # data_store_id → within a data store, source_ids → within those Sources,
        # scopes → within scopes; rerank/mmr/multi-query/HyDE ride the passage lane.
        within: list[dict[str, Any]] = [w.model_dump(exclude_none=True) for w in (parsed.within or [])]
        within += [{"type": "scope", "id": sid} for sid in (scope_ids or [])]
        if parsed.data_store_id:
            within.append({"type": "data_store", "id": parsed.data_store_id})
        within += [{"type": "source", "id": sid} for sid in (parsed.source_ids or [])]
        query: dict[str, Any] = {
            "text": parsed.query,
            "limit": parsed.limit,
            "types": parsed.types,
            "source_kinds": parsed.source_kinds,
            "within": within or None,
            "entities": parsed.entities,
            "captured_by": parsed.captured_by,
            "origin": parsed.origin,
            "date": parsed.date.model_dump(by_alias=True, exclude_none=True) if parsed.date else None,
            "state": parsed.state,
            "organizations": parsed.organizations,
            "sort": parsed.sort,
            "cursors": parsed.cursors,
        }
        try:
            conversation_id = ctx.conversation_id
        except Exception:
            conversation_id = None
        try:
            sections_payload, response = await get_ext("knowledge_search_service")(
                query={k: v for k, v in query.items() if v is not None},
                user_id=user_id,
                organization_id=organization_id,
                conversation_id=str(conversation_id) if conversation_id else None,
                segment_options={
                    "rerank": parsed.rerank,
                    "use_mmr": parsed.use_mmr,
                    "multi_query": parsed.multi_query,
                    "use_hyde": parsed.use_hyde,
                    "scope_document_ids": scope_document_ids,
                    "include_entity_map": True,
                },
            )
        except Exception as exc:
            return _stamp(
                ToolResult(
                    success=False,
                    error=ToolError.from_exception(
                        exc, error_type="search_failed", message=f"Knowledge search failed: {exc}"
                    ),
                ),
                started_at,
                ctx,
            )
        if response is None:
            segment_error = next(
                (e for e in sections_payload.get("errors") or [] if e.get("section") == "segments"), None
            )
            segments = next(
                (s for s in sections_payload.get("sections") or [] if s.get("section") == "segments"), None
            )
            # Only the passage lane failed (most often its time budget): the other sections answered, and the
            # person's search shows them — so does this result, with the passage failure named in section_errors.
            # The whole call fails only when nothing else answered (2026-11-17: a passage timeout used to discard
            # every answered section and file tool_execution_failed "the other sections are unaffected").
            if segment_error is not None and not _other_sections(sections_payload):
                return _stamp(
                    ToolResult(
                        success=False,
                        error=ToolError(reported_failure="the knowledge search", error_type="search_failed", message=str(segment_error.get("message") or "")),
                    ),
                    started_at,
                    ctx,
                )
            if parsed.data_store_id and segments is not None:
                return _stamp(
                    ToolResult(
                        success=True,
                        output_kind="knowledge_search_empty_result",
                        output={
                            "query": parsed.query,
                            "hits": [],
                            "total_candidates": 0,
                            "data_store_id": parsed.data_store_id,
                            "note": segments.get("note")
                            or "Data store is empty or not visible to this user; no scope to search.",
                            "sections": _other_sections(sections_payload),
                        },
                    ),
                    started_at,
                    ctx,
                )
            if segment_error is not None:
                segment_failure = segment_error
            response = _EmptyResponse(parsed.query)
    else:
        # A host without the Knowledge search service (matrx-ai standalone): passages
        # only, through the rag_search seam — and the result says so.
        try:
            search_fn = _get_rag_search()
        except Exception as exc:
            return _stamp(
                ToolResult(
                    success=False,
                    error=ToolError.declared(exc=exc, 
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
        include_sources: list[dict[str, str]] | None = None
        if parsed.data_store_id and has_ext("rag_materialize_member_filter"):
            scoped = await get_ext("rag_materialize_member_filter")(
                store_id=parsed.data_store_id, user_id=user_id, organization_id=organization_id
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
                            "note": "Data store is empty or not visible to this user; no scope to search.",
                        },
                    ),
                    started_at,
                    ctx,
                )
            include_sources = scoped
        search_scope_kwargs: dict[str, Any] = (
            {"scope_document_ids": scope_document_ids} if scope_document_ids else {}
        )
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
                scope_ids=scope_ids,
                source_ids=parsed.source_ids,
                **search_scope_kwargs,
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

    hits = [_hit_to_dict(h, parsed.query) for h in getattr(response, "hits", [])]
    entity_map_raw = getattr(response, "entity_map", None) or []
    entity_map = [_entity_map_entry_to_dict(e) for e in entity_map_raw]
    matched_entities = list(getattr(response, "matched_entities", None) or [])
    output: dict[str, Any] = {
        "query": getattr(response, "query", parsed.query),
        "hits": hits,
        "total_candidates": int(getattr(response, "total_candidates", len(hits))),
        "embedding_model": getattr(response, "embedding_model", "") or "",
        "reranker_model": getattr(response, "reranker_model", None),
        "latency_ms": int(getattr(response, "latency_ms", 0) or 0),
        "matched_entities": matched_entities,
        "entity_map": entity_map,
        "validation_guidance": PHYSICAL_PAGE_VALIDATION_GUIDANCE,
    }
    output.update(_relevance_report(response, hits))
    output.update(_recall_lane_report(response))
    if sections_payload is not None:
        output["sections"] = _other_sections(sections_payload)
        other_errors = [e for e in sections_payload.get("errors") or [] if e.get("section") != "segments"]
        if segment_failure is not None:
            other_errors.insert(0, segment_failure)
        if other_errors:
            output["section_errors"] = other_errors
        if sections_payload.get("chips"):
            output["chips"] = sections_payload["chips"]
    else:
        output["sections_note"] = (
            "Only passages were searched: this host has no Knowledge search service, so "
            "titles, chats and records were not part of this search."
        )
    announcements: dict[str, Any] = {}
    if scope_note:
        announcements["scope_note"] = scope_note
    if searched_scope_ids:
        announcements["searched_scope_ids"] = searched_scope_ids
    if scope_document_ids:
        announcements["searched_source_ids"] = scope_document_ids
    output.update(announcements)
    caps = await knowledge_search_caps(organization_id)
    # The resend path (a DB-rebuilt conversation) builds the same view from the stored
    # output, so the caps this call ran with ride on it.
    output["model_view_caps"] = caps
    result = ToolResult(
        success=True,
        output=output,
    )
    # The model is handed a bounded VIEW (``model_view``): CITABLE passages — each hit a
    # SearchResultContent block (Anthropic `search_result` + citations enabled, matrx://
    # identity source) so quotes come back as REAL citations with file/page click-through
    # — plus one line per item of every other section and the match metadata, all inside
    # the output budget. `output` (storage/trace/UI) stays complete.
    view = model_view(
        output,
        window_chars=caps["snippet_window_chars"],
        budget_chars=caps["output_budget_chars"],
    )
    from matrx_ai.config import TextContent

    provider_blocks = _citable_blocks_for_hits(view)
    if provider_blocks is None:
        import json

        provider_blocks = [TextContent(text=json.dumps(view, ensure_ascii=False, default=str))]
    result.provider_content = provider_blocks
    return _stamp(result, started_at, ctx)


_SECTION_LABELS = {
    "top_hit": "Top hit",
    "segments": "Segments",
    "sources": "Sources",
    "chats": "Chats",
    "messages": "Messages",
    "projects_tasks": "Projects & tasks",
    "notes": "Notes",
    "files": "Files",
    "agents_workflows": "Agents & workflows",
    "records": "Records",
}


def render_sections_for_model(output: dict[str, Any]) -> str | None:
    """One line per result of every non-passage section, with counts, withheld reasons
    and section errors — compact enough for the context, complete enough that the agent
    knows everything the person's search returned."""
    sections = output.get("sections")
    errors = output.get("section_errors") or []
    if not sections and not errors:
        return None
    lines = ["Every section of this search (what the person sees; open any with knowledge_open entity+id):"]
    # Segments ARE the citable passages above (`hits`) — named here so the list is complete.
    hits = output.get("hits") or []
    lines.append(f"Segments ({len(hits)}): the citable passages above" if hits else "Segments: none")
    for h in hits:
        meta = h.get("metadata") or {}
        name = meta.get("title") or meta.get("file_name") or h.get("source_kind") or "passage"
        pages = h.get("page_numbers") or []
        where = f" p. {pages[0]}" if pages else ""
        lines.append(f"- segment {h.get('chunk_id')} — {' '.join(str(name).split())[:80]}{where}")
    for sec in sections or []:
        label = _SECTION_LABELS.get(str(sec.get("section")), str(sec.get("section")))
        if sec.get("withheld"):
            lines.append(f"{label}: withheld — {sec['withheld']}")
            continue
        items = sec.get("items") or []
        more = " (more available)" if sec.get("has_more") else ""
        lines.append(f"{label} ({sec.get('count', len(items))}){more}:" if items else f"{label}: none")
        for it in items:
            title = " ".join(str(it.get("title") or "Untitled").split())[:100]
            extra = ""
            if it.get("matches"):
                extra = f" — “{' '.join(str(it['matches'][0].get('snippet') or '').split())[:90]}”"
            lines.append(f"- {it.get('entity')} {it.get('id')} — {title}{extra}")
    for err in errors:
        label = _SECTION_LABELS.get(str(err.get("section")), str(err.get("section")))
        lines.append(f"{label}: could not be searched — {err.get('message')}")
    return "\n".join(lines)


class _EmptyResponse:
    """The passage lane was not planned (e.g. ``types`` excluded every chunked kind)."""

    def __init__(self, query: str) -> None:
        self.query = query
        self.hits: list[Any] = []
        self.total_candidates = 0
        self.embedding_model = ""
        self.reranker_model = None
        self.latency_ms = 0


def _other_sections(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Every typed section except Segments (those are ``hits``, with citations)."""
    return [s for s in payload.get("sections") or [] if s.get("section") != "segments"]


def _recall_lane_report(response: Any) -> dict[str, Any]:
    """Say, in one sentence the model reads, that a retrieval lane timed out.

    ``recall_lane_errors`` (lane -> sentence) is set by the search when the database
    canceled a lane; the other lanes still answered, so the hits are real but may be
    incomplete. Empty when every lane answered — nothing is added then."""
    raw = getattr(response, "recall_lane_errors", None) or {}
    errors = {str(k): str(v) for k, v in raw.items()} if isinstance(raw, dict) else {}
    if not errors:
        return {}
    lanes = " and ".join(sorted(errors))
    return {
        "recall_lane_errors": errors,
        "recall_lane_note": (
            f"The {lanes} search lane timed out, so these results may be incomplete; "
            "retrying the same query may return more."
        ),
    }


def _relevance_report(response: Any, hits: list[dict[str, Any]]) -> dict[str, Any]:
    """State what the engine's relevance gate concluded — in the agent's words.

    The retrieval engine gates hits on a calibrated cross-encoder floor
    (``matrx_rag.search.RELEVANCE_FLOOR``), so an empty ``hits`` can mean "the
    corpus has nothing for this query" — a real answer. Saying that outright is
    the difference between an agent reporting the gap and an agent re-issuing
    the same call (knowledge_compare did it 19 times in one turn before the
    floor existed; feedback 2985b3aa). An unscored result says THAT, too, rather
    than implying the hits were vetted.
    """
    verdict = getattr(response, "relevance_verdict", "unscored")
    floor = getattr(response, "relevance_floor", None)
    dropped = int(getattr(response, "below_floor_dropped", 0) or 0)
    report: dict[str, Any] = {
        "relevance_verdict": verdict,
        "relevance_floor": floor,
        "below_floor_dropped": dropped,
    }
    if hits:
        if verdict == "unscored":
            report["note"] = (
                "These hits were ranked but NOT relevance-scored (the "
                "cross-encoder was unavailable), so no relevance floor was "
                "applied. Read the snippets before relying on them."
            )
        return report
    if verdict == "no_relevant_matches":
        floor_text = f"{floor:.2f}" if isinstance(floor, (int, float)) else "the relevance floor"
        candidates = int(getattr(response, "total_candidates", 0) or 0)
        report["no_relevant_matches"] = True
        report["note"] = (
            f"Nothing in the content you can see matched above the similarity "
            f"floor ({floor_text}) — {candidates} candidate chunk(s) were "
            f"retrieved and every one scored below it. This is an honest empty "
            f"result, not an error. Do NOT repeat this query; rephrase in the "
            f"vocabulary the records actually use, widen/narrow the filters, or "
            f"check knowledge_browse(action='sources') for what is indexed."
        )
    else:
        report["no_relevant_matches"] = True
        report["note"] = (
            "Nothing was retrieved for this query — either no such content is "
            "indexed or none is visible to you. Check "
            "knowledge_browse(action='sources') before retrying a reworded "
            "version of the same query."
        )
    return report


async def _resolve_scope_ids(
    requested: list[str] | None,
    ctx: ToolContext,
    *,
    user_id: str,
    organization_id: str | None,
) -> tuple[list[str] | None, list[str] | None, str | None, list[str]]:
    """Decide what the search runs within — and the sentence that says so.

    Returns ``(scope_ids, scope_document_ids, scope_note, auto_scope_ids)``.

    * The agent passed scope ids → used as given, nothing to announce.
    * The agent passed ``[]`` → search everything (the engine treats an empty
      list as "no valid scope" and returns nothing).
    * The agent passed nothing → what the conversation is attached to (host
      seam ``rag_conversation_scopes``): its scopes, and each project it works
      in (``conversation → project`` edges or the request's working project)
      expanded to that project's scopes and the Sources filed under it —
      searched as a union, announced by name with how to widen. A failed lookup
      is announced and the search runs unscoped — never a silent narrowing or
      widening.
    """
    if requested is not None:
        return (requested or None), None, None, []

    from matrx_ai._ext import get_ext, has_ext

    try:
        conversation_id = ctx.conversation_id
    except Exception:
        conversation_id = None
    try:
        project_id = ctx.project_id
    except Exception:
        project_id = None
    if not (conversation_id or project_id) or not has_ext("rag_conversation_scopes"):
        return None, None, None, []

    try:
        lookup = get_ext("rag_conversation_scopes")
        attached = await lookup(
            conversation_id=str(conversation_id) if conversation_id else None,
            user_id=user_id,
            organization_id=organization_id,
            project_id=str(project_id) if project_id else None,
        )
    except Exception as exc:
        return (
            None,
            None,
            (
                "Could not check what this conversation is attached to "
                f"({type(exc).__name__}: {exc}), so this search ran across everything "
                "you can see. Pass scope_ids=[...] to narrow it yourself."
            ),
            [],
        )

    if isinstance(attached, list):  # a host that reports scopes only
        attached = {"scopes": attached}
    attached = attached or {}
    ids: list[str] = []
    labels: list[str] = []
    for scope in attached.get("scopes") or []:
        scope_id = str((scope or {}).get("id") or "").strip()
        if not scope_id or scope_id in ids:
            continue
        ids.append(scope_id)
        name = str(scope.get("name") or scope_id)
        via = scope.get("via_project")
        labels.append(f"{name} ({scope_id})" + (f", via project {via}" if via else ""))
    document_ids = [
        str(d) for d in dict.fromkeys(attached.get("document_ids") or []) if str(d).strip()
    ]
    projects = [
        str((p or {}).get("name") or (p or {}).get("id"))
        for p in attached.get("projects") or []
        if (p or {}).get("id")
    ]
    if not ids and not document_ids:
        return None, None, None, []
    parts: list[str] = []
    if ids:
        parts.append(f"the scope(s) {', '.join(labels)}")
    if document_ids:
        where = f" project {', '.join(projects)}" if projects else " its project"
        parts.append(f"the {len(document_ids)} Source(s) filed under{where}")
    return (
        ids or None,
        document_ids or None,
        (
            "Searched what this conversation is attached to: "
            + " and ".join(parts)
            + ". Pass scope_ids=[] to search everything you can see, or "
            "scope_ids=[...] to choose other scopes."
        ),
        ids,
    )


def _citable_blocks_for_hits(view: dict[str, Any] | list[dict[str, Any]]) -> list[Any] | None:
    """One citable SearchResultContent per snippet-bearing hit of the model view (or a bare
    hit list), then the section lines and the rest of the view as JSON (snippets removed —
    they live in the citable blocks; sending both would double the tokens). ``None`` when
    no hit has text."""
    import copy
    import json

    from matrx_ai.config import SearchResultContent, TextContent
    from matrx_ai.config.citations import passage_page_and_label, passage_source_name

    meta = copy.deepcopy(view) if isinstance(view, dict) else {"hits": copy.deepcopy(view)}
    sections_text = meta.pop("sections_text", None)
    blocks: list[Any] = []
    for hit in meta.get("hits") or []:
        snippet = hit.pop("snippet", "")
        if not snippet:
            continue
        page, page_label = passage_page_and_label(hit.get("page_numbers"))
        name = passage_source_name(hit) or "Knowledge source"
        file_id = (
            str(hit["source_id"])
            if hit.get("source_kind") == "cld_file" and hit.get("source_id")
            else ""
        )
        blocks.append(
            SearchResultContent(
                texts=[snippet],
                title=f"{name}{page_label}",
                file_id=file_id,
                document_id=str(hit.get("processed_document_id") or ""),
                page=page,
            )
        )
    if not blocks:
        return None
    from matrx_ai.config.unified_content import cap_citable_blocks

    blocks = cap_citable_blocks(blocks, meta)
    meta["passages_note"] = (
        "The passages above are citable search results (quote them and citations attach "
        "automatically). This JSON is the match metadata; snippets were moved into the "
        "passage blocks."
    )
    from matrx_ai.config.citations import cap_search_metadata

    cap_search_metadata(meta)  # backstop for a bare hit list; the view is already in budget
    if sections_text:
        blocks.append(TextContent(text=sections_text))
    blocks.append(TextContent(text=json.dumps(meta, ensure_ascii=False, default=str)))
    return blocks
