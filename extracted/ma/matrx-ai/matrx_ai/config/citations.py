"""Canonical normalized citation schema + per-provider normalizers.

This module is the single source of truth for the cross-provider citation
contract ratified 2026-07-17 (docs/handoffs/citations-system.md in
matrx-frontend). Every provider's citation/annotation/grounding payload is
normalized into ``NormalizedCitation`` at INGESTION (translator / from_*
classmethods) so that:

  - ``TextContent.metadata["citations"]`` (in-memory) and the top-level
    ``citations`` array on the stored text part (cx_message.content) always
    hold ONE shape, regardless of provider.
  - ``TextPart.citations`` (db/message_parts.py) types the stored shape, so
    the generated TypeScript gives the FE a real interface.
  - The ``citation`` stream event carries the same shape live.

Tier-1 leaf module: imports ONLY pydantic + matrx_utils.vcprint. Both
``matrx_ai.config`` and ``matrx_ai.db.message_parts`` import it — keep it
dependency-free so the standalone type-generation load of message_parts.py
stays cheap and cycle-free.

Provider mapping (ratified):
  - Anthropic ``char_location``          → ``document_char``
  - Anthropic ``page_location``          → ``document_page``
  - Anthropic ``content_block_location`` → ``document_block``
  - Anthropic ``search_result_location`` → ``search_result``
  - Anthropic web-search citations       → ``web``
  - OpenAI ``url_citation`` annotations  → ``web`` (answer offsets)
  - Gemini grounding supports × chunks   → ``grounding`` (answer offsets)
  - xAI response-level URL list          → ``web``

The original provider payload is ALWAYS preserved in ``raw``.
"""

from __future__ import annotations

from typing import Any, Literal

from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict, Field

CitationKind = Literal[
    "document_char",
    "document_page",
    "document_block",
    "search_result",
    "web",
    "grounding",
]

CitationProvider = Literal["anthropic", "openai", "google", "xai"]


class NormalizedCitation(BaseModel):
    """The canonical cross-provider citation shape — the FE contract.

    Offsets come in two flavours and are never conflated:
      - ``source_start`` / ``source_end``: char/block offsets INTO THE SOURCE
        document (Anthropic char/content_block locations).
      - ``answer_start`` / ``answer_end``: char offsets INTO THE ANSWER TEXT
        (OpenAI url_citation annotations, Gemini grounding segment offsets).
    ``page`` / ``end_page`` are 1-based (Anthropic page_location).
    """

    model_config = ConfigDict(extra="forbid")

    kind: CitationKind
    provider: CitationProvider
    cited_text: str | None = None
    title: str | None = None
    url: str | None = None
    source_index: int = 0
    file_id: str | None = None
    page: int | None = None
    end_page: int | None = None
    source_start: int | None = None
    source_end: int | None = None
    answer_start: int | None = None
    answer_end: int | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_plain(value: Any) -> Any:
    """Best-effort conversion of a provider SDK object to plain JSON-able data."""
    if value is None or isinstance(value, str | int | float | bool):
        return value
    if isinstance(value, dict):
        return {k: _to_plain(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [_to_plain(v) for v in value]
    if hasattr(value, "model_dump"):
        try:
            return value.model_dump(mode="json", exclude_none=True)
        except Exception:
            pass
    if hasattr(value, "to_json_dict"):
        try:
            return value.to_json_dict()
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        return {k: _to_plain(v) for k, v in vars(value).items() if not k.startswith("_")}
    return str(value)


def _get(obj: Any, key: str, default: Any = None) -> Any:
    """Read ``key`` from a dict OR an SDK object attribute."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _loud_unknown(provider: str, payload: Any, guessed_kind: str) -> None:
    vcprint(
        {"provider": provider, "guessed_kind": guessed_kind, "payload": _to_plain(payload)},
        f"[citations] UNKNOWN {provider} citation shape — normalized best-effort "
        f"as kind='{guessed_kind}' (raw preserved). Register the new shape in "
        "matrx_ai/config/citations.py.",
        color="red",
    )


# ---------------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------------

_ANTHROPIC_KIND_BY_TYPE: dict[str, CitationKind] = {
    "char_location": "document_char",
    "page_location": "document_page",
    "content_block_location": "document_block",
    "search_result_location": "search_result",
    "web_search_result_location": "web",
}


def is_normalized_citation(item: Any) -> bool:
    """True when ``item`` already carries the canonical shape's discriminators.

    The discriminators are ``kind`` + ``provider`` — the only two REQUIRED
    fields of ``NormalizedCitation``. ``raw`` must NOT be part of this test:
    it is optional (default ``{}``), so a canonical citation that carries no
    provider payload — one the FE built, or one a client resent — failed the
    check, got re-normalized down the "unknown legacy shape" branch, and was
    rebuilt from only ``cited_text``/``title``/``url``. That SILENTLY DROPPED
    ``source_start`` / ``source_end`` / ``page`` / offsets on every read-write
    cycle, so a cited message degraded a little each time it round-tripped.
    Normalization MUST be idempotent; pinned by
    ``tests/test_content_deserializer_parity.py``.
    """
    return isinstance(item, dict) and "kind" in item and "provider" in item


def normalize_anthropic_citation(citation: dict[str, Any]) -> NormalizedCitation:
    """Normalize ONE Anthropic citation object (final message or citations_delta).

    ``file_id`` is OUR platform file id — Anthropic's own ``file_id`` (their
    Files API id) is NOT ours, so it stays in ``raw`` only. Mapping
    ``document_index`` back to our request's document order (to recover our
    file_id/title) is a documented follow-up; ``source_index`` carries the
    provider's index verbatim.
    """
    raw = _to_plain(citation)
    ctype = raw.get("type") or ""
    kind = _ANTHROPIC_KIND_BY_TYPE.get(ctype)
    if kind is None:
        guessed: CitationKind = "web" if raw.get("url") else "document_char"
        _loud_unknown("anthropic", raw, guessed)
        kind = guessed

    source_index = raw.get("document_index")
    if source_index is None:
        source_index = raw.get("search_result_index", 0)

    # `source` on a search_result_location echoes whatever we sent — for our
    # own tool results that is a matrx:// identity URI carrying file/page,
    # which closes the click-through loop (FE opens the PDF at that page).
    # A matrx:// URI is identity, not a web address: it must land in
    # file_id/page, never in `url`.
    source = raw.get("url") or raw.get("source")
    file_id: str | None = None
    page = raw.get("start_page_number")
    url: str | None = source
    matrx_ref = parse_matrx_citation_source(source)
    if matrx_ref is not None:
        url = None
        file_id = matrx_ref.get("file_id")
        if page is None:
            page = matrx_ref.get("page")
        if source == MATRX_METADATA_SOURCE:
            # The metadata wrapper IS citations-enabled — wire invariant 2
            # (uniform citations across every search_result block) leaves no
            # other legal option — so the model may legitimately cite it. It
            # carries match metadata, not a passage: normalize it (it stays
            # non-linkable in the UI — no file_id/page to open) and note it.
            # A run where the model prefers this block over the real passages
            # means the passages were unhelpful; worth seeing, not an alarm.
            vcprint(
                "[citations] the model cited the 'Search metadata' wrapper block "
                f"({MATRX_METADATA_SOURCE}) rather than a passage — the citation "
                "normalizes but has no source to open.",
                color="yellow",
            )

    return NormalizedCitation(
        kind=kind,
        provider="anthropic",
        cited_text=raw.get("cited_text"),
        title=raw.get("document_title") or raw.get("title"),
        url=url,
        source_index=int(source_index or 0),
        file_id=file_id,
        page=page,
        end_page=raw.get("end_page_number"),
        source_start=raw.get("start_char_index", raw.get("start_block_index")),
        source_end=raw.get("end_char_index", raw.get("end_block_index")),
        raw=raw,
    )


# ---------------------------------------------------------------------------
# OpenAI (Responses API annotations)
# ---------------------------------------------------------------------------


def normalize_openai_annotation(annotation: dict[str, Any], answer_text: str) -> NormalizedCitation:
    """Normalize ONE OpenAI Responses annotation.

    ``url_citation`` carries offsets into the ANSWER text (start_index /
    end_index) — never source offsets. ``answer_text`` is used only to
    bound-check offsets; OpenAI provides no verbatim source text, so
    ``cited_text`` stays None.
    """
    raw = _to_plain(annotation)
    atype = raw.get("type") or ""

    if atype == "url_citation":
        kind: CitationKind = "web"
    elif atype in ("file_citation", "container_file_citation", "file_path"):
        kind = "document_char"
    else:
        kind = "web" if raw.get("url") else "document_char"
        _loud_unknown("openai", raw, kind)

    answer_start = raw.get("start_index")
    answer_end = raw.get("end_index")
    if isinstance(answer_end, int) and answer_text and answer_end > len(answer_text):
        # Offsets that overrun the answer are provider drift — keep them (raw
        # has the originals) but flag loudly so the FE mis-highlight is traceable.
        vcprint(
            f"[citations] OpenAI annotation end_index {answer_end} overruns the "
            f"answer text (len={len(answer_text)}) — offsets kept, check provider drift.",
            color="yellow",
        )

    return NormalizedCitation(
        kind=kind,
        provider="openai",
        cited_text=None,
        title=raw.get("title") or raw.get("filename"),
        url=raw.get("url"),
        source_index=int(raw.get("index") or 0),
        file_id=None,
        answer_start=answer_start,
        answer_end=answer_end,
        raw=raw,
    )


# ---------------------------------------------------------------------------
# Google (Gemini grounding metadata)
# ---------------------------------------------------------------------------


def normalize_google_grounding(
    grounding_metadata: Any, answer_text: str
) -> list[NormalizedCitation]:
    """Join ``grounding_supports`` × ``grounding_chunks`` into one flat list.

    Each support segment (answer-text char range) may cite several chunks —
    one ``NormalizedCitation`` is emitted per (support, chunk_index) pair, so
    the FE can highlight every span/source association. Accepts the SDK
    object or a plain dict. Segment ``start_index`` is None for the first
    segment in the Gemini wire shape — normalized to 0.
    """
    if grounding_metadata is None:
        return []

    chunks = _get(grounding_metadata, "grounding_chunks") or []
    supports = _get(grounding_metadata, "grounding_supports") or []
    citations: list[NormalizedCitation] = []

    for support in supports:
        segment = _get(support, "segment")
        answer_start = _get(segment, "start_index") if segment is not None else None
        answer_end = _get(segment, "end_index") if segment is not None else None
        if answer_start is None and answer_end is not None:
            answer_start = 0
        chunk_indices = _get(support, "grounding_chunk_indices") or []
        for chunk_index in chunk_indices:
            title = None
            url = None
            if isinstance(chunk_index, int) and 0 <= chunk_index < len(chunks):
                chunk = chunks[chunk_index]
                web = _get(chunk, "web")
                retrieved = _get(chunk, "retrieved_context")
                source = web if web is not None else retrieved
                if source is not None:
                    title = _get(source, "title")
                    url = _get(source, "uri") or _get(source, "url")
                chunk_raw = _to_plain(chunk)
            else:
                chunk_raw = None
                vcprint(
                    f"[citations] Gemini grounding support references chunk index "
                    f"{chunk_index!r} but only {len(chunks)} chunks exist — "
                    "citation kept without url/title (raw preserved).",
                    color="red",
                )
            citations.append(
                NormalizedCitation(
                    kind="grounding",
                    provider="google",
                    cited_text=None,
                    title=title,
                    url=url,
                    source_index=int(chunk_index) if isinstance(chunk_index, int) else 0,
                    answer_start=answer_start,
                    answer_end=answer_end,
                    raw={"support": _to_plain(support), "chunk": chunk_raw},
                )
            )
    return citations


# ---------------------------------------------------------------------------
# xAI (response-level URL list from web_search / x_search)
# ---------------------------------------------------------------------------


def normalize_xai_citations(citations: list[Any]) -> list[NormalizedCitation]:
    """Normalize xAI's response-level citations list (URL strings, or dicts)."""
    normalized: list[NormalizedCitation] = []
    for index, item in enumerate(citations or []):
        if isinstance(item, str):
            normalized.append(
                NormalizedCitation(
                    kind="web",
                    provider="xai",
                    url=item,
                    source_index=index,
                    raw={"url": item},
                )
            )
            continue
        raw = _to_plain(item)
        if not isinstance(raw, dict):
            raw = {"value": raw}
        url = raw.get("url") or raw.get("uri")
        if not url:
            _loud_unknown("xai", raw, "web")
        normalized.append(
            NormalizedCitation(
                kind="web",
                provider="xai",
                title=raw.get("title"),
                url=url,
                source_index=index,
                raw=raw,
            )
        )
    return normalized


# ---------------------------------------------------------------------------
# OpenAI-COMPATIBLE endpoints (generic_openai / Groq / Moonshot / ...)
# ---------------------------------------------------------------------------


def normalize_openai_compatible_citations(
    response: Any, message: Any, answer_text: str
) -> list[NormalizedCitation]:
    """Best-effort capture for OpenAI-compatible Chat Completions endpoints.

    Two citation dialects exist in the wild (verified against the SDK models
    we actually receive — openai + groq, 2026-08-08):

      - A TOP-LEVEL ``citations`` list on the response (Perplexity dialect —
        URL strings or ``{url,title}`` dicts). The OpenAI SDK models allow
        extra fields, so this survives ``client.chat.completions.create``.
      - ``annotations`` on the message/delta. OpenAI Chat Completions nests
        the payload under ``url_citation``; Groq nests under
        ``document_citation`` (``{document_id,start_index,end_index}``) or
        ``function_citation`` (``{tool_call_id,start_index,end_index}``).
        ``start_index``/``end_index`` are offsets INTO THE ANSWER.

    ``provider`` is stamped ``"openai"`` — it identifies the WIRE DIALECT
    (this whole family speaks OpenAI's), and ``raw`` preserves the exact
    payload. Unknown shapes normalize best-effort and scream (``_loud_unknown``).
    Never raises — citations are a side-channel to the answer.
    """
    normalized: list[NormalizedCitation] = []

    for index, item in enumerate(_get(response, "citations", None) or []):
        if isinstance(item, str):
            normalized.append(
                NormalizedCitation(
                    kind="web",
                    provider="openai",
                    url=item,
                    source_index=index,
                    raw={"url": item},
                )
            )
            continue
        raw = _to_plain(item)
        if not isinstance(raw, dict):
            raw = {"value": raw}
        url = raw.get("url") or raw.get("uri")
        if not url:
            _loud_unknown("openai_compatible", raw, "web")
        normalized.append(
            NormalizedCitation(
                kind="web",
                provider="openai",
                title=raw.get("title"),
                url=url,
                source_index=index,
                raw=raw,
            )
        )

    for annotation in _get(message, "annotations", None) or []:
        raw = _to_plain(annotation)
        if not isinstance(raw, dict):
            _loud_unknown("openai_compatible", raw, "web")
            continue
        nested_url = raw.get("url_citation")
        nested_doc = raw.get("document_citation")
        nested_fn = raw.get("function_citation")
        if isinstance(nested_url, dict):
            # OpenAI Chat Completions nests url_citation — flatten to the
            # Responses-API field layout normalize_openai_annotation reads.
            flat = {**nested_url, "type": "url_citation"}
            citation = normalize_openai_annotation(flat, answer_text)
            citation.raw = raw
            normalized.append(citation)
        elif isinstance(nested_doc, dict):
            normalized.append(
                NormalizedCitation(
                    kind="document_char",
                    provider="openai",
                    source_index=int(nested_doc.get("document_id") or 0)
                    if str(nested_doc.get("document_id") or "").isdigit()
                    else 0,
                    answer_start=nested_doc.get("start_index"),
                    answer_end=nested_doc.get("end_index"),
                    raw=raw,
                )
            )
        elif isinstance(nested_fn, dict):
            # Cites a tool call's output — the closest canonical kind is
            # search_result (a citation into tool-provided content).
            normalized.append(
                NormalizedCitation(
                    kind="search_result",
                    provider="openai",
                    answer_start=nested_fn.get("start_index"),
                    answer_end=nested_fn.get("end_index"),
                    raw=raw,
                )
            )
        else:
            # Flat Responses-style annotation (or unknown — that path screams).
            normalized.append(normalize_openai_annotation(raw, answer_text))

    return normalized


# ---------------------------------------------------------------------------
# Recovery — legacy / client-resent citation lists
# ---------------------------------------------------------------------------


def ensure_normalized_citations(items: list[Any]) -> list[dict[str, Any]]:
    """Coerce a citations list to canonical dicts, normalizing legacy shapes.

    Storage validation (TextPart.citations → NormalizedCitation) is strict, so
    any raw provider citation that sneaks back in (a client resending a
    pre-normalization stored message) is normalized here instead of failing
    the write. Already-normalized items pass through untouched.
    """
    out: list[dict[str, Any]] = []
    for item in items or []:
        if is_normalized_citation(item):
            out.append(item)
        elif isinstance(item, dict) and item.get("type") in _ANTHROPIC_KIND_BY_TYPE:
            out.append(normalize_anthropic_citation(item).model_dump(exclude_none=True))
        elif isinstance(item, dict):
            guessed: CitationKind = "web" if item.get("url") else "document_char"
            _loud_unknown("legacy/unknown", item, guessed)
            out.append(
                NormalizedCitation(
                    kind=guessed,
                    provider="anthropic",
                    cited_text=item.get("cited_text"),
                    title=item.get("title") or item.get("document_title"),
                    url=item.get("url"),
                    raw=_to_plain(item),
                ).model_dump(exclude_none=True)
            )
        else:
            vcprint(
                f"[citations] Dropping non-dict citation item {item!r} — cannot normalize.",
                color="red",
            )
    return out


# ---------------------------------------------------------------------------
# Enable-by-default gate (ratified: ON for user-facing, OFF for machine runs,
# every exclusion explicit and LOUD — never silent)
# ---------------------------------------------------------------------------


def resolve_citations_disabled_reason(
    response_format: Any, metadata: dict[str, Any] | None
) -> str | None:
    """Resolve whether citations must be stripped from this request's documents.

    Returns a human-readable reason string when disabled, else None (enabled —
    the default). Precedence:
      1. An explicit ``metadata["citations_enabled"]`` boolean always wins
         (True force-enables even a structured-output run; False disables).
      2. ``response_format`` set → machine-consumed structured-output run.
      3. Default: enabled.
    """
    explicit = (metadata or {}).get("citations_enabled")
    if explicit is True:
        return None
    if explicit is False:
        return "explicitly disabled via config.metadata['citations_enabled']=False"
    if response_format:
        return "structured-output (machine-consumed) run — response_format is set"
    return None


def log_citations_disabled(reason: str, document_count: int) -> None:
    """The mandatory loud line for every citations exclusion."""
    vcprint(
        f"[citations] DISABLED for {document_count} document block(s) this "
        f"request — {reason}. Citations are default-ON for user-facing runs; "
        "this exclusion is deliberate and must stay loud.",
        color="yellow",
    )


# ---------------------------------------------------------------------------
# matrx:// citation sources — carrying OUR file identity through the provider
# ---------------------------------------------------------------------------
#
# Anthropic echoes a search_result block's `source` string VERBATIM into every
# search_result_location citation (verified live 2026-08-08). Encoding our file
# identity there means the citation round-trips with click-through data and no
# request-side bookkeeping. A matrx:// URI is identity, not a web address —
# normalization decodes it into file_id/page and never exposes it as `url`.

MATRX_CITATION_SCHEME = "matrx"


def build_matrx_citation_source(
    *,
    file_id: str | None = None,
    page: int | None = None,
    document_id: str | None = None,
) -> str:
    """Build the identity URI for a citable tool-result passage.

    Shape: ``matrx://file/<file_id>?page=<n>&doc=<processed_document_id>``
    (``matrx://document/<document_id>`` when only the processed doc is known).
    """
    from urllib.parse import urlencode

    from urllib.parse import quote

    params: dict[str, str] = {}
    if page is not None:
        params["page"] = str(int(page))
    if file_id:
        if document_id:
            params["doc"] = document_id
        base = f"{MATRX_CITATION_SCHEME}://file/{quote(str(file_id), safe='')}"
    elif document_id:
        base = f"{MATRX_CITATION_SCHEME}://document/{quote(str(document_id), safe='')}"
    else:
        return ""
    return f"{base}?{urlencode(params)}" if params else base


def parse_matrx_citation_source(source: Any) -> dict[str, Any] | None:
    """Decode a matrx:// citation source. Returns None for anything else.

    Never raises — a malformed matrx URI returns the parts it can recover
    (citations are a side-channel; identity decode must not break ingestion).
    """
    if not isinstance(source, str) or not source.startswith(f"{MATRX_CITATION_SCHEME}://"):
        return None
    try:
        from urllib.parse import parse_qs, unquote, urlsplit

        parts = urlsplit(source)
        path_bits = [unquote(p) for p in parts.path.split("/") if p]
        entity = parts.netloc  # "file" | "document"
        entity_id = path_bits[0] if path_bits else None
        query = {k: v[0] for k, v in parse_qs(parts.query).items() if v}
        page_raw = query.get("page")
        page = int(page_raw) if page_raw and page_raw.lstrip("-").isdigit() else None
        return {
            "file_id": entity_id if entity == "file" else None,
            "document_id": query.get("doc") or (entity_id if entity == "document" else None),
            "page": page,
        }
    except Exception:  # pragma: no cover — malformed URI, recover what we can
        return {"file_id": None, "document_id": None, "page": None}


# ---------------------------------------------------------------------------
# Settle-time enrichment — document_index → our file identity
# ---------------------------------------------------------------------------


def collect_request_document_identities(messages: Any) -> list[dict[str, Any]]:
    """Walk request messages in wire order and collect one identity dict per
    document block, in the SAME order the Anthropic translator serializes them
    (message order → content order, including documents nested in tool-result
    typed content). Anthropic's ``document_index`` counts documents in exactly
    this order.
    """
    docs: list[dict[str, Any]] = []

    def _identity_of(item: Any) -> dict[str, Any] | None:
        if type(item).__name__ != "DocumentContent":
            return None
        meta = getattr(item, "metadata", None) or {}
        title = (
            meta.get("title")
            or meta.get("file_name")
            or meta.get("filename")
            or meta.get("name")
            or getattr(item, "file_name", None)
        )
        return {"file_id": getattr(item, "file_id", None) or None, "title": title or None}

    for message in messages or []:
        for item in getattr(message, "content", None) or []:
            identity = _identity_of(item)
            if identity is not None:
                docs.append(identity)
                continue
            nested = getattr(item, "content", None)
            if isinstance(nested, list):
                for sub in nested:
                    sub_identity = _identity_of(sub)
                    if sub_identity is not None:
                        docs.append(sub_identity)
    return docs


def enrich_document_citations_with_request_documents(
    documents: list[dict[str, Any]], response: Any
) -> int:
    """Stamp ``file_id`` (and a missing ``title``) onto normalized DOCUMENT
    citations in a UnifiedResponse, using the request's wire-ordered document
    identity list. Mutates citations in place; returns how many were enriched.
    Never raises — enrichment is best-effort on a side-channel.
    """
    if not documents or response is None:
        return 0
    enriched = 0
    try:
        for message in getattr(response, "messages", None) or []:
            for item in getattr(message, "content", None) or []:
                metadata = getattr(item, "metadata", None)
                if not isinstance(metadata, dict):
                    continue
                for citation in metadata.get("citations") or []:
                    if not isinstance(citation, dict):
                        continue
                    if not str(citation.get("kind") or "").startswith("document_"):
                        continue
                    index = citation.get("source_index")
                    if not isinstance(index, int) or not (0 <= index < len(documents)):
                        continue
                    identity = documents[index]
                    if not citation.get("file_id") and identity.get("file_id"):
                        citation["file_id"] = identity["file_id"]
                        enriched += 1
                    if not citation.get("title") and identity.get("title"):
                        citation["title"] = identity["title"]
    except Exception as exc:  # pragma: no cover
        vcprint(f"[citations] document-identity enrichment failed (skipped): {exc}", color="red")
    return enriched


# ---------------------------------------------------------------------------
# Citable wire blocks — rebuilding citability for DB-rebuilt tool results
# ---------------------------------------------------------------------------
#
# ToolResult.provider_content (the live typed SearchResultContent blocks) is
# deliberately never persisted; a conversation rebuilt from cx_tool_call.output
# would resend those tool results as plain JSON text — readable, but no longer
# citable, silently re-opening the Reach gap for every multi-turn conversation.
# This pure-dict rebuilder runs at the Anthropic wire boundary
# (ToolResultContent.to_anthropic): it recognizes the stored payload shapes of
# the citable search tools and re-emits homogeneous `search_result` blocks.

MATRX_METADATA_SOURCE = f"{MATRX_CITATION_SCHEME}://metadata"

# ── THE ANTHROPIC `search_result` WIRE INVARIANTS ──────────────────────────
#
# Two rules, BOTH live-verified against the real API, and they compound:
#
#   1. A tool_result carrying `search_result` blocks may carry NOTHING else
#      (400 "all blocks must be of that type", 2026-08-08). That is why a
#      citable tool result's trailing metadata JSON has to be wrapped as a
#      `search_result` block instead of staying a `text` block.
#   2. "Citations must be either enabled or disabled on all `search_result`
#      blocks. A mixture of enabling and disabling is not supported."
#      (400, live 2026-08-21 — request 74ef776d, knowledge_search follow-up).
#
# Rule 2 means the wrapper rule 1 forces us to emit CANNOT be left
# non-citable: passages carry citations:{enabled:true}, so the metadata
# wrapper must too. Every producer of a search_result wire block stamps
# ``search_result_citations()``, and the Anthropic translator enforces
# uniformity across the whole request as the last line of defense.


def search_result_citations() -> dict[str, Any]:
    """The citations config every citable `search_result` wire block carries.

    A fresh dict per call — wire blocks are cached/shared across requests and
    must never alias a mutable literal.
    """
    return {"enabled": True}


def _search_result_citations_enabled(block: dict[str, Any]) -> bool:
    """Anthropic treats an absent `citations` key as DISABLED."""
    citations = block.get("citations")
    return bool(isinstance(citations, dict) and citations.get("enabled"))


def enforce_search_result_citation_uniformity(messages: list[dict[str, Any]]) -> int:
    """Make every `search_result` block in one Anthropic request agree on
    citations (wire invariant 2), returning the number of blocks corrected.

    Direction is deterministic: if ANY block is citations-enabled, enable them
    ALL — a valid, fully-citable request. Enabling never invalidates anything
    (the model may simply cite one more block), while disabling would silently
    destroy the citability the citable-tool path exists to provide. An
    all-disabled request (the machine-run strip below) is already uniform and
    is left untouched.

    Blocks are copied before mutation: ``to_anthropic_blocks`` dicts are shared
    across calls (same rule as the cache helpers in the translator).

    A non-zero return means a producer emitted a non-uniform block and MUST be
    fixed — the caller screams. This backstop exists so a new citable tool can
    never take chat down with a 400.
    """

    def _walk(blocks: list[Any], collect: list[tuple[list[Any], int, dict[str, Any]]]) -> None:
        for index, block in enumerate(blocks):
            if not isinstance(block, dict):
                continue
            if block.get("type") == "search_result":
                collect.append((blocks, index, block))
            elif block.get("type") == "tool_result" and isinstance(block.get("content"), list):
                inner = list(block["content"])
                blocks[index] = {**block, "content": inner}
                _walk(inner, collect)

    found: list[tuple[list[Any], int, dict[str, Any]]] = []
    for message in messages:
        content = message.get("content")
        if isinstance(content, list):
            _walk(content, found)

    if not found:
        return 0
    if not any(_search_result_citations_enabled(block) for _, _, block in found):
        return 0

    corrected = 0
    for owner, index, block in found:
        if _search_result_citations_enabled(block):
            continue
        owner[index] = {**block, "citations": search_result_citations()}
        corrected += 1
    return corrected


CITABLE_SEARCH_TOOLS = frozenset({"document_search", "knowledge_search"})

# Total citable passage chars a single tool result may put on the wire. The
# builders (live) and this rebuilder (resend) both enforce it — passages beyond
# the budget are dropped whole, lowest-ranked first, and the drop is announced
# in the metadata block so the model knows recall was bounded.
MAX_CITABLE_TEXT_CHARS = 24_000


def _metadata_wire_block(payload: dict[str, Any]) -> dict[str, Any]:
    import json as _json

    return {
        "type": "search_result",
        "source": MATRX_METADATA_SOURCE,
        "title": "Search metadata",
        "content": [
            {"type": "text", "text": _json.dumps(payload, ensure_ascii=False, default=str)}
        ],
        # Invariant 2: uniform with the passage blocks it ships beside.
        "citations": search_result_citations(),
    }


def _passage_wire_block(
    *,
    texts: list[str],
    title: str,
    file_id: str | None,
    document_id: str | None,
    page: int | None,
) -> dict[str, Any]:
    return {
        "type": "search_result",
        "source": build_matrx_citation_source(
            file_id=file_id or None, page=page, document_id=document_id or None
        )
        or "matrx://unknown",
        "title": title or "Search result",
        "content": [{"type": "text", "text": t} for t in texts if t],
        "citations": search_result_citations(),
    }


def citable_wire_blocks_from_output(
    tool_name: str, payload: Any, *, max_chars: int = MAX_CITABLE_TEXT_CHARS
) -> list[dict[str, Any]] | None:
    """Rebuild homogeneous Anthropic `search_result` wire blocks from a stored
    citable-search-tool output payload. Returns None when the payload doesn't
    carry passages (caller falls back to plain JSON). Never raises.

    Identity is best-effort from the payload itself: knowledge_search hits
    carry source_kind/source_id (full file click-through); document_search
    entries carry document_id/page (document identity — the FE still shows a
    titled, non-web source). Passages beyond ``max_chars`` are dropped whole,
    lowest-ranked first, and announced in the metadata block.
    """
    if tool_name not in CITABLE_SEARCH_TOOLS or not isinstance(payload, dict):
        return None
    try:
        import copy

        meta = copy.deepcopy(payload)
        passages: list[dict[str, Any]] = []

        def _identity_title(document_id: Any, page: Any, name: Any) -> str:
            base = str(name) if name else "Document"
            return f"{base} — page {page}" if page is not None else base

        for hit in meta.get("hits") or []:
            if not isinstance(hit, dict):
                continue
            snippet = hit.pop("snippet", "")
            if not snippet:
                continue
            pages = hit.get("page_numbers") or []
            page = int(pages[0]) if pages else None
            hit_meta = hit.get("metadata") or {}
            name = (
                hit_meta.get("title")
                or hit_meta.get("file_name")
                or hit_meta.get("name")
                or hit_meta.get("source_label")
            )
            file_id = (
                str(hit["source_id"])
                if hit.get("source_kind") == "cld_file" and hit.get("source_id")
                else None
            )
            passages.append(
                _passage_wire_block(
                    texts=[snippet],
                    title=_identity_title(hit.get("document_id"), page, name),
                    file_id=file_id,
                    document_id=str(
                        hit.get("processed_document_id") or hit.get("document_id") or ""
                    )
                    or None,
                    page=page,
                )
            )
        for match in meta.get("matches") or []:
            if not isinstance(match, dict):
                continue
            snippet = match.pop("snippet", "")
            if not snippet:
                continue
            page_raw = match.get("page_number")
            page = int(page_raw) if page_raw is not None else None
            passages.append(
                _passage_wire_block(
                    texts=[snippet],
                    title=_identity_title(match.get("document_id"), page, None),
                    file_id=None,
                    document_id=str(match.get("document_id") or "") or None,
                    page=page,
                )
            )
        for group in meta.get("by_page") or []:
            if not isinstance(group, dict):
                continue
            texts: list[str] = []
            for entry in list(group.get("semantic") or []) + list(group.get("string") or []):
                if isinstance(entry, dict):
                    snippet = entry.pop("snippet", "")
                    if snippet:
                        texts.append(snippet)
            if not texts:
                continue
            page_raw = group.get("page_number")
            page = int(page_raw) if page_raw is not None else None
            passages.append(
                _passage_wire_block(
                    texts=texts,
                    title=_identity_title(group.get("document_id"), page, None),
                    file_id=None,
                    document_id=str(group.get("document_id") or "") or None,
                    page=page,
                )
            )

        if not passages:
            return None

        kept: list[dict[str, Any]] = []
        total = 0
        dropped = 0
        for block in passages:
            block_chars = sum(len(c.get("text") or "") for c in block["content"])
            if kept and total + block_chars > max_chars:
                dropped += 1
                continue
            kept.append(block)
            total += block_chars
        if dropped:
            meta["passages_dropped"] = dropped
            vcprint(
                f"[citations] {tool_name}: dropped {dropped} citable passage block(s) "
                f"over the {max_chars}-char budget (kept {len(kept)}, {total} chars).",
                color="yellow",
            )
        meta["passages_note"] = (
            "The passages above are citable search results (quote them and citations "
            "attach automatically). This JSON is the match metadata; snippets were "
            "moved into the passage blocks."
        )
        kept.append(_metadata_wire_block(meta))
        return kept
    except Exception as exc:  # pragma: no cover — rebuild is best-effort
        vcprint(
            f"[citations] citable wire-block rebuild failed for {tool_name} "
            f"(falling back to plain JSON): {exc}",
            color="red",
        )
        return None
