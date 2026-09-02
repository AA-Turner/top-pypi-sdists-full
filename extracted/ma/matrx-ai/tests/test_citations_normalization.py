"""Citations system — normalization + enable-gate + storage round-trip tests.

Fixtures under tests/fixtures/citations/ are TRIMMED live wire captures
(2026-07-17, real provider APIs) — the citation-bearing structures verbatim,
base64/HTML noise stripped. See docs/handoffs/citations-system.md
(matrx-frontend) for the ratified canonical schema these tests pin.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path

import pytest

from matrx_ai.config import DocumentContent, TextContent
from matrx_ai.config.citations import (
    NormalizedCitation,
    ensure_normalized_citations,
    normalize_anthropic_citation,
    normalize_google_grounding,
    normalize_openai_annotation,
    normalize_xai_citations,
    resolve_citations_disabled_reason,
)
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_content import reconstruct_content
from matrx_ai.db.message_parts import validate_message_content

FIXTURES = Path(__file__).parent / "fixtures" / "citations"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


# ---------------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------------


def test_anthropic_char_location_from_fixture():
    message = _load("anthropic_text_doc.json")
    cited_blocks = [b for b in message["content"] if b.get("citations")]
    assert cited_blocks, "fixture must carry citation-bearing text blocks"

    citation = normalize_anthropic_citation(cited_blocks[0]["citations"][0])
    assert citation.kind == "document_char"
    assert citation.provider == "anthropic"
    assert citation.cited_text == "The frontend is a Next.js application deployed on Vercel. "
    assert citation.title == "AI Matrx Platform Overview"
    assert citation.source_index == 0
    assert citation.source_start == 122
    assert citation.source_end == 180
    assert citation.page is None
    assert citation.answer_start is None
    # raw preserves the original payload verbatim
    assert citation.raw["type"] == "char_location"
    assert citation.raw["document_index"] == 0


def test_anthropic_page_location_from_fixture():
    message = _load("anthropic_pdf_doc.json")
    cited = next(b for b in message["content"] if b.get("citations"))
    citation = normalize_anthropic_citation(cited["citations"][0])
    assert citation.kind == "document_page"
    assert citation.page == 1
    assert citation.end_page == 2
    assert citation.title == "TM SEO Pricing Packages March 2022.pdf"
    assert citation.raw["type"] == "page_location"


def test_anthropic_search_result_location_from_fixture():
    message = _load("anthropic_search_result.json")
    cited = next(b for b in message["content"] if b.get("citations"))
    citation = normalize_anthropic_citation(cited["citations"][0])
    assert citation.kind == "search_result"
    assert citation.title == "AI Matrx Platform Overview"
    assert citation.url == "https://docs.aimatrx.com/platform"
    assert citation.source_index == 0
    assert citation.source_start == 0
    assert citation.source_end == 1


def test_anthropic_stream_citations_delta_from_fixture():
    events = _load("anthropic_stream_events.json")["events"]
    deltas = [
        e["delta"]["citation"]
        for e in events
        if e.get("type") == "content_block_delta"
        and e.get("delta", {}).get("type") == "citations_delta"
    ]
    assert len(deltas) == 2
    for raw in deltas:
        citation = normalize_anthropic_citation(raw)
        assert citation.kind == "document_char"
        assert citation.provider == "anthropic"
        assert citation.cited_text
        assert citation.raw == raw


def test_text_content_from_anthropic_normalizes_citations():
    message = _load("anthropic_text_doc.json")
    cited_block = next(b for b in message["content"] if b.get("citations"))
    content = TextContent.from_anthropic(cited_block)
    stored = content.metadata["citations"]
    assert stored and all("kind" in c and "provider" in c and "raw" in c for c in stored)
    assert stored[0]["kind"] == "document_char"


# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------


def test_openai_url_citation_annotations_from_fixture():
    response = _load("openai_web_search_annotations.json")
    message = next(o for o in response["output"] if o["type"] == "message")
    text_item = message["content"][0]
    annotations = text_item["annotations"]
    assert len(annotations) == 3

    citations = [normalize_openai_annotation(a, text_item["text"]) for a in annotations]
    first = citations[0]
    assert first.kind == "web"
    assert first.provider == "openai"
    assert first.url.startswith("https://www.anthropic.com/news/claude-sonnet-5")
    assert first.title == "Introducing Claude Sonnet 5 \\ Anthropic"
    assert first.answer_start == 147
    assert first.answer_end == 230
    assert first.cited_text is None
    assert first.source_start is None
    assert first.raw["type"] == "url_citation"


def test_text_content_from_openai_modified_captures_annotations():
    response = _load("openai_web_search_annotations.json")
    message = next(o for o in response["output"] if o["type"] == "message")
    text_item = message["content"][0]
    content = TextContent.from_openai_modified(
        {"content": text_item["text"], "annotations": text_item["annotations"]}
    )
    assert content.metadata["citations"]
    assert content.metadata["citations"][0]["provider"] == "openai"


# ---------------------------------------------------------------------------
# Google (Gemini grounding)
# ---------------------------------------------------------------------------


def test_google_grounding_join_from_fixture():
    response = _load("gemini_grounding.json")
    candidate = response["candidates"][0]
    answer_text = candidate["content"]["parts"][0]["text"]
    grounding = candidate["grounding_metadata"]

    citations = normalize_google_grounding(grounding, answer_text)
    assert len(citations) == 10  # 10 supports × 1 chunk each

    first = citations[0]
    assert first.kind == "grounding"
    assert first.provider == "google"
    assert first.source_index == 0
    assert first.title == "youtube.com"
    assert first.url.startswith("https://vertexaisearch.cloud.google.com/")
    # Gemini omits start_index on the first segment — normalized to 0.
    assert first.answer_start == 0
    assert first.answer_end == 121
    assert first.raw["support"]["segment"]["text"].startswith("Anthropic's latest")

    last = citations[-1]
    assert last.source_index == 2
    assert last.title == "mindstudio.ai"
    assert last.answer_start == 918
    assert last.answer_end == 1057


def test_google_grounding_none_is_empty():
    assert normalize_google_grounding(None, "text") == []


# ---------------------------------------------------------------------------
# xAI
# ---------------------------------------------------------------------------


def test_xai_url_list_normalization():
    urls = ["https://example.com/a", "https://example.com/b"]
    citations = normalize_xai_citations(urls)
    assert [c.url for c in citations] == urls
    assert all(c.kind == "web" and c.provider == "xai" for c in citations)
    assert [c.source_index for c in citations] == [0, 1]
    assert citations[0].raw == {"url": urls[0]}


# ---------------------------------------------------------------------------
# Legacy recovery
# ---------------------------------------------------------------------------


def test_ensure_normalized_citations_coerces_raw_anthropic_shape():
    raw = {
        "type": "char_location",
        "cited_text": "abc",
        "document_index": 1,
        "document_title": "Doc",
        "start_char_index": 0,
        "end_char_index": 3,
    }
    out = ensure_normalized_citations([raw])
    assert out[0]["kind"] == "document_char"
    assert out[0]["raw"]["type"] == "char_location"


def test_ensure_normalized_citations_passthrough():
    normalized = normalize_anthropic_citation(
        {"type": "char_location", "cited_text": "x", "document_index": 0}
    ).model_dump(exclude_none=True)
    assert ensure_normalized_citations([normalized]) == [normalized]


# ---------------------------------------------------------------------------
# Enable-by-default gate
# ---------------------------------------------------------------------------


def test_document_to_anthropic_enables_citations_on_all_three_shapes():
    pdf = DocumentContent(
        base64_data=base64.b64encode(b"%PDF-1.4 fake").decode(),
        mime_type="application/pdf",
        metadata={"title": "Quarterly Report.pdf"},
    )
    pdf_block = pdf.to_anthropic()
    assert pdf_block["source"]["type"] == "base64"
    assert pdf_block["citations"] == {"enabled": True}
    assert pdf_block["title"] == "Quarterly Report.pdf"

    text_doc = DocumentContent(
        base64_data=base64.b64encode("hello text doc".encode()).decode(),
        mime_type="text/plain",
        metadata={"file_name": "notes.txt", "citation_context": "User-attached notes"},
    )
    text_block = text_doc.to_anthropic()
    assert text_block["source"]["type"] == "text"
    assert text_block["citations"] == {"enabled": True}
    assert text_block["title"] == "notes.txt"
    assert text_block["context"] == "User-attached notes"

    url_doc = DocumentContent(url="https://example.com/x.pdf", mime_type="application/pdf")
    url_block = url_doc.to_anthropic()
    assert url_block["source"]["type"] == "url"
    assert url_block["citations"] == {"enabled": True}
    assert "title" not in url_block  # no name known — never invent one


def test_document_to_anthropic_explicit_per_document_opt_out():
    doc = DocumentContent(
        base64_data=base64.b64encode(b"%PDF-1.4 fake").decode(),
        mime_type="application/pdf",
        metadata={"citations_enabled": False},
    )
    block = doc.to_anthropic()
    assert "citations" not in block


def test_resolve_citations_disabled_reason():
    # Default: enabled.
    assert resolve_citations_disabled_reason(None, {}) is None
    # Structured output (machine-consumed) — disabled, with reason.
    reason = resolve_citations_disabled_reason({"type": "json_schema"}, {})
    assert reason and "structured-output" in reason
    # Explicit False — disabled.
    assert resolve_citations_disabled_reason(None, {"citations_enabled": False})
    # Explicit True overrides even structured output.
    assert (
        resolve_citations_disabled_reason({"type": "json_schema"}, {"citations_enabled": True})
        is None
    )


# ---------------------------------------------------------------------------
# Round-trip guard: ingest → storage → validate → reparse → reconstruct →
# provider resend, without loss.
# ---------------------------------------------------------------------------


def test_citation_round_trip_survives_storage_and_resend():
    message = _load("anthropic_text_doc.json")
    cited_block = next(b for b in message["content"] if b.get("citations"))

    # 1. Ingestion (translator path)
    content = TextContent.from_anthropic(cited_block)
    in_memory = content.metadata["citations"]
    assert in_memory[0]["kind"] == "document_char"

    # 2. Storage dict — citations emitted TOP-LEVEL
    stored = content.to_storage_dict()
    assert stored["citations"] == in_memory

    # 3. DB validation gate (cx_message.content write path) — strict TextPart
    validated = validate_message_content([stored])
    part = validated[0]
    assert part["citations"][0]["kind"] == "document_char"
    assert part["citations"][0]["raw"]["type"] == "char_location"
    assert part["text"] == cited_block["text"]

    # 4. Client/DB reparse (parse_content) folds citations back to metadata
    reparsed = UnifiedMessage.parse_content([part])
    assert len(reparsed) == 1
    assert reparsed[0].metadata["citations"][0]["kind"] == "document_char"
    assert reparsed[0].text == cited_block["text"]

    # 5. reconstruct_content (storage → in-memory) preserves them too
    reconstructed = reconstruct_content(part)
    assert reconstructed.metadata["citations"][0]["kind"] == "document_char"

    # 6. Provider resend — the assistant text block goes back out intact
    resend = reconstructed.to_anthropic()
    assert resend == {"type": "text", "text": cited_block["text"]}

    # 7. And a second full cycle is lossless (idempotent normalization)
    second = validate_message_content([reconstructed.to_storage_dict()])
    assert second[0]["citations"] == part["citations"]


def test_round_trip_recovers_legacy_raw_citations():
    """A stored/client-resent block carrying RAW provider citations (pre-
    normalization era) must be coerced — never crash the strict storage gate."""
    message = _load("anthropic_text_doc.json")
    cited_block = next(b for b in message["content"] if b.get("citations"))
    legacy_stored = {
        "type": "text",
        "text": cited_block["text"],
        "citations": cited_block["citations"],  # raw Anthropic shape
    }
    reparsed = UnifiedMessage.parse_content([legacy_stored])
    validated = validate_message_content([reparsed[0].to_storage_dict()])
    assert validated[0]["citations"][0]["kind"] == "document_char"


# ---------------------------------------------------------------------------
# Translator-level machine-run gate (whole outbound request)
# ---------------------------------------------------------------------------


def _anthropic_config(**overrides):
    from matrx_ai.config import UnifiedConfig

    doc = DocumentContent(
        base64_data=base64.b64encode(b"%PDF-1.4 fake").decode(),
        mime_type="application/pdf",
        metadata={"title": "Attached.pdf"},
    )
    return UnifiedConfig(
        model="claude-opus-4-5-20250929",
        messages=[
            UnifiedMessage(
                role="user",
                content=[TextContent(text="summarize"), doc],
            )
        ],
        **overrides,
    )


def _anthropic_profile():
    from matrx_ai.testing.profile_factory import make_profile

    return make_profile(
        model_name="claude-opus-4-5-20250929",
        wire_format="anthropic_chat",
        capabilities={
            "input": ["text", "document"],
            "output": ["text"],
            "features": ["function_calling", "structured_output"],
            "interaction": "turn",
        },
    )


def _document_blocks(request: dict) -> list[dict]:
    return [
        block
        for message in request["messages"]
        for block in message["content"]
        if isinstance(block, dict) and block.get("type") == "document"
    ]


def test_translator_keeps_citations_enabled_for_user_facing_run():
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    request = AnthropicTranslator().to_anthropic(_anthropic_config(), _anthropic_profile())
    docs = _document_blocks(request)
    assert docs, "document block must survive translation"
    assert docs[0]["citations"] == {"enabled": True}
    assert docs[0]["title"] == "Attached.pdf"


def test_translator_strips_citations_for_structured_output_run():
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    config = _anthropic_config(
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "Verdict",
                "schema": {
                    "type": "object",
                    "properties": {"passed": {"type": "boolean"}},
                    "required": ["passed"],
                    "additionalProperties": False,
                },
            },
        }
    )
    request = AnthropicTranslator().to_anthropic(config, _anthropic_profile())
    docs = _document_blocks(request)
    assert docs, "document block must survive translation"
    assert "citations" not in docs[0]
    assert "context" not in docs[0]


def test_web_search_pins_search_result_citations_on_structured_runs():
    """Run ae62da71 (2026-08-26): a structured-output agent with the hosted
    web_search tool was UNRUNNABLE — the strip gate removed `search_result`
    citations (right for extraction) and Anthropic then rejected the whole
    request ("When web search is enabled, citations must be enabled on all
    `search_result` blocks"). The provider's hard constraint wins: with
    internal_web_search on, search_result blocks KEEP citations while document
    blocks are still stripped."""
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "Verdict",
            "schema": {
                "type": "object",
                "properties": {"passed": {"type": "boolean"}},
                "required": ["passed"],
                "additionalProperties": False,
            },
        },
    }
    from matrx_ai.config import SearchResultContent
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent

    doc = DocumentContent(
        base64_data=base64.b64encode(b"%PDF-1.4 fake").decode(),
        mime_type="application/pdf",
        metadata={"title": "Attached.pdf"},
    )
    tool_result = ToolResultContent(
        tool_use_id="tu_1",
        call_id="tu_1",
        name="web_search",
        content=[SearchResultContent(texts=["hit"], title="Example", file_id="f-1", page=1)],
    )
    config = UnifiedConfig(
        model="claude-opus-4-5-20250929",
        messages=[
            UnifiedMessage(role="user", content=[TextContent(text="summarize"), doc]),
            # The sanitizer drops an orphan tool_result, so the matching
            # tool_use must exist for the block to reach the wire at all.
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id="tu_1", name="web_search", arguments={"q": "x"})],
            ),
            UnifiedMessage(role="user", content=[tool_result]),
        ],
        response_format=schema,
        internal_web_search=True,
    )
    request = AnthropicTranslator().to_anthropic(config, _anthropic_profile())

    docs = _document_blocks(request)
    assert docs and "citations" not in docs[0], "documents still stripped"

    search_results = [
        inner
        for message in request["messages"]
        for block in message["content"]
        if isinstance(block, dict) and block.get("type") == "tool_result"
        for inner in (block.get("content") or [])
        if isinstance(inner, dict) and inner.get("type") == "search_result"
    ]
    assert search_results, "search_result block must survive translation"
    assert all("citations" in sr and sr["citations"].get("enabled") for sr in search_results), (
        "web search demands citations enabled on every search_result block"
    )


def test_translator_strips_citations_for_explicit_pipeline_opt_out():
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    config = _anthropic_config(metadata={"citations_enabled": False})
    request = AnthropicTranslator().to_anthropic(config, _anthropic_profile())
    docs = _document_blocks(request)
    assert docs and "citations" not in docs[0]


def test_document_ref_tool_result_carries_title_for_citations():
    from matrx_ai.tools.models import _build_document_ref_blocks

    blocks = _build_document_ref_blocks(
        {
            "kind": "document_ref",
            "media_ref": {"file_id": "file-123", "mime_type": "application/pdf"},
            "file_name": "Contract Draft.pdf",
        }
    )
    doc = blocks[0]
    assert isinstance(doc, DocumentContent)
    assert doc.file_id == "file-123"
    assert doc.metadata["title"] == "Contract Draft.pdf"


def test_normalized_citation_schema_is_strict():
    with pytest.raises(Exception):
        NormalizedCitation(kind="web", provider="openai", bogus_field=1)


# ---------------------------------------------------------------------------
# Reach: matrx:// identity sources, SearchResultContent, settle enrichment
# ---------------------------------------------------------------------------


def test_matrx_citation_source_round_trip():
    from matrx_ai.config.citations import (
        build_matrx_citation_source,
        parse_matrx_citation_source,
    )

    source = build_matrx_citation_source(file_id="f-1", page=26, document_id="d-1")
    assert source == "matrx://file/f-1?page=26&doc=d-1"
    assert parse_matrx_citation_source(source) == {
        "file_id": "f-1",
        "document_id": "d-1",
        "page": 26,
    }
    assert parse_matrx_citation_source("https://example.com") is None
    assert parse_matrx_citation_source(None) is None
    doc_only = build_matrx_citation_source(document_id="d-9")
    assert parse_matrx_citation_source(doc_only)["document_id"] == "d-9"


def test_normalize_anthropic_search_result_location_decodes_matrx_source():
    from matrx_ai.config.citations import normalize_anthropic_citation

    normalized = normalize_anthropic_citation(
        {
            "type": "search_result_location",
            "source": "matrx://file/f-42?page=7&doc=d-42",
            "title": "Contract.pdf — page 7",
            "cited_text": "the term is 36 months",
            "search_result_index": 2,
            "start_block_index": 0,
            "end_block_index": 0,
        }
    )
    assert normalized.kind == "search_result"
    assert normalized.file_id == "f-42"
    assert normalized.page == 7
    assert normalized.url is None, "matrx:// identity must never leak as a web url"
    assert normalized.source_index == 2
    # A real web source still lands in url.
    web = normalize_anthropic_citation(
        {
            "type": "search_result_location",
            "source": "https://docs.example.com/x",
            "title": "Doc",
            "search_result_index": 0,
        }
    )
    assert web.url == "https://docs.example.com/x" and web.file_id is None


def test_search_result_content_to_anthropic_is_citable():
    from matrx_ai.config import SearchResultContent

    block = SearchResultContent(
        texts=["passage one", "passage two"],
        title="Spec.pdf — page 3",
        file_id="f-7",
        document_id="d-7",
        page=3,
    )
    wire = block.to_anthropic()
    assert wire["type"] == "search_result"
    assert wire["source"] == "matrx://file/f-7?page=3&doc=d-7"
    assert wire["citations"] == {"enabled": True}
    assert [c["text"] for c in wire["content"]] == ["passage one", "passage two"]
    assert SearchResultContent(texts=[]).to_anthropic() is None
    silent = SearchResultContent(texts=["x"], citations_enabled=False).to_anthropic()
    assert "citations" not in silent


def test_translator_strips_search_result_citations_for_machine_runs():
    from matrx_ai.config import SearchResultContent, TextContent, UnifiedMessage
    from matrx_ai.config.tools_config import ToolResultContent
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator

    tool_result = ToolResultContent(
        tool_use_id="tu_1",
        call_id="tu_1",
        name="document_search",
        content=[
            SearchResultContent(texts=["hit"], title="Doc — page 1", file_id="f-1", page=1),
            TextContent(text="{}"),
        ],
    )
    config = _anthropic_config(metadata={"citations_enabled": False})
    config.messages.append(UnifiedMessage(role="user", content=[tool_result]))
    request = AnthropicTranslator().to_anthropic(config, _anthropic_profile())
    nested = [
        inner
        for message in request["messages"]
        for block in message["content"]
        if isinstance(block, dict) and block.get("type") == "tool_result"
        for inner in (block.get("content") if isinstance(block.get("content"), list) else [])
        if isinstance(inner, dict) and inner.get("type") == "search_result"
    ]
    assert nested, "search_result block must survive tool_result translation"
    assert all("citations" not in b for b in nested)


def test_enrich_document_citations_with_request_documents():
    from matrx_ai.config import TextContent, UnifiedMessage
    from matrx_ai.config.citations import (
        collect_request_document_identities,
        enrich_document_citations_with_request_documents,
    )
    from matrx_ai.config.media_config import DocumentContent

    doc = DocumentContent(base64_data="JVBERi0=", mime_type="application/pdf", file_id="f-doc-1")
    doc.metadata["title"] = "Attached.pdf"
    request_messages = [UnifiedMessage(role="user", content=[TextContent(text="q"), doc])]
    identities = collect_request_document_identities(request_messages)
    assert identities == [{"file_id": "f-doc-1", "title": "Attached.pdf"}]

    cited = TextContent(text="answer")
    cited.metadata["citations"] = [
        {
            "kind": "document_char",
            "provider": "anthropic",
            "source_index": 0,
            "file_id": None,
            "title": None,
        },
        {"kind": "web", "provider": "openai", "source_index": 0, "file_id": None},
    ]

    class _Response:
        messages = [UnifiedMessage(role="assistant", content=[cited])]

    enriched = enrich_document_citations_with_request_documents(identities, _Response())
    assert enriched == 1
    assert cited.metadata["citations"][0]["file_id"] == "f-doc-1"
    assert cited.metadata["citations"][0]["title"] == "Attached.pdf"
    assert cited.metadata["citations"][1]["file_id"] is None, "non-document kinds untouched"


def test_knowledge_search_hits_become_citable_blocks():
    from matrx_ai.tools.implementations.rag import _citable_blocks_for_hits

    hits = [
        {
            "chunk_id": "c1",
            "source_kind": "cld_file",
            "source_id": "f-9",
            "snippet": "the fee is $250",
            "page_numbers": [12],
            "processed_document_id": "d-9",
            "metadata": {"file_name": "Fees.pdf"},
        },
        {
            "chunk_id": "c2",
            "source_kind": "note",
            "source_id": "n-1",
            "snippet": "",
            "metadata": {},
        },
    ]
    blocks = _citable_blocks_for_hits(hits)
    assert blocks is not None
    search_blocks = [b for b in blocks if getattr(b, "type", "") == "search_result"]
    assert len(search_blocks) == 1
    block = search_blocks[0]
    assert block.file_id == "f-9" and block.page == 12
    assert block.title == "Fees.pdf — page 12"
    wire = block.to_anthropic()
    assert wire["citations"] == {"enabled": True}
    assert wire["source"].startswith("matrx://file/f-9")
    meta_block = blocks[-1]
    assert "the fee is $250" not in meta_block.text
    # Original hits untouched (storage keeps snippets).
    assert hits[0]["snippet"] == "the fee is $250"
    assert _citable_blocks_for_hits([]) is None


def test_tool_result_search_blocks_stay_homogeneous_for_anthropic():
    """Anthropic 400s a tool_result mixing search_result with other block types
    (live-verified 2026-08-08) AND 400s a mixture of enabled/disabled citations
    across search_result blocks (live-verified 2026-08-21). The serializer must
    satisfy both: one block type, one citations posture."""
    from matrx_ai.config import SearchResultContent, TextContent
    from matrx_ai.config.tools_config import ToolResultContent

    mixed = ToolResultContent(
        tool_use_id="tu_1",
        call_id="tu_1",
        name="document_search",
        content=[
            SearchResultContent(texts=["hit"], title="Doc — page 1", file_id="f-1", page=1),
            TextContent(text='{"meta": true}'),
        ],
    ).to_anthropic()
    types = [b["type"] for b in mixed["content"]]
    assert types == ["search_result", "search_result"], types
    meta = mixed["content"][1]
    assert meta["title"] == "Search metadata"
    # The wrapper is citations-ENABLED, uniform with the passage beside it —
    # a non-citable wrapper among citable passages is the 2026-08-21 400.
    assert meta["citations"] == {"enabled": True}
    assert mixed["content"][0]["citations"] == meta["citations"]
    assert meta["content"][0]["text"] == '{"meta": true}'

    # Pure search_result and pure text results pass through untouched.
    pure = ToolResultContent(
        tool_use_id="tu_2",
        call_id="tu_2",
        name="document_search",
        content=[SearchResultContent(texts=["hit"], title="T", file_id="f-1", page=1)],
    ).to_anthropic()
    assert [b["type"] for b in pure["content"]] == ["search_result"]
    assert pure["content"][0]["citations"] == {"enabled": True}


def test_tool_result_search_blocks_degrade_to_text_when_media_present():
    from matrx_ai.config import SearchResultContent
    from matrx_ai.config.tools_config import ToolResultContent

    result = ToolResultContent(
        tool_use_id="tu_3",
        call_id="tu_3",
        name="mixed_tool",
        content=[
            SearchResultContent(texts=["hit text"], title="Doc", file_id="f-1", page=2),
            {
                "type": "image",
                "source": {"type": "base64", "media_type": "image/png", "data": "AA=="},
            },
        ],
    ).to_anthropic()
    types = [b["type"] for b in result["content"]]
    assert "search_result" not in types
    assert types[0] == "text" and "hit text" in result["content"][0]["text"]
    assert types[1] == "image"


# ---------------------------------------------------------------------------
# OpenAI-compatible endpoints (generic_openai / Groq / Moonshot / Perplexity-style)
# ---------------------------------------------------------------------------


def test_openai_compatible_top_level_citations_list():
    from matrx_ai.config.citations import normalize_openai_compatible_citations

    response = {"citations": ["https://a.example/one", {"url": "https://b.example", "title": "B"}]}
    normalized = normalize_openai_compatible_citations(response, {}, "answer")
    assert [c.kind for c in normalized] == ["web", "web"]
    assert [c.provider for c in normalized] == ["openai", "openai"]
    assert normalized[0].url == "https://a.example/one"
    assert normalized[0].source_index == 0
    assert normalized[1].url == "https://b.example"
    assert normalized[1].title == "B"
    assert normalized[1].source_index == 1
    # raw always preserved
    assert normalized[0].raw == {"url": "https://a.example/one"}


def test_openai_compatible_nested_url_citation_annotation():
    from matrx_ai.config.citations import normalize_openai_compatible_citations

    # OpenAI Chat Completions dialect: payload nested under url_citation.
    message = {
        "annotations": [
            {
                "type": "url_citation",
                "url_citation": {
                    "url": "https://c.example",
                    "title": "C",
                    "start_index": 3,
                    "end_index": 9,
                },
            }
        ]
    }
    normalized = normalize_openai_compatible_citations({}, message, "the answer text")
    assert len(normalized) == 1
    c = normalized[0]
    assert c.kind == "web" and c.provider == "openai"
    assert c.url == "https://c.example" and c.title == "C"
    assert c.answer_start == 3 and c.answer_end == 9
    # raw keeps the ORIGINAL nested annotation, not the flattened copy.
    assert "url_citation" in c.raw


def test_openai_compatible_groq_document_and_function_citations():
    from matrx_ai.config.citations import normalize_openai_compatible_citations

    message = {
        "annotations": [
            {
                "type": "document_citation",
                "document_citation": {"document_id": "2", "start_index": 0, "end_index": 5},
            },
            {
                "type": "function_citation",
                "function_citation": {"tool_call_id": "tc_1", "start_index": 6, "end_index": 10},
            },
        ]
    }
    normalized = normalize_openai_compatible_citations(None, message, "answer text!")
    assert [c.kind for c in normalized] == ["document_char", "search_result"]
    doc, fn = normalized
    assert doc.source_index == 2
    assert doc.answer_start == 0 and doc.answer_end == 5
    assert fn.answer_start == 6 and fn.answer_end == 10
    assert fn.raw["function_citation"]["tool_call_id"] == "tc_1"


def test_openai_compatible_empty_inputs_yield_nothing():
    from matrx_ai.config.citations import normalize_openai_compatible_citations

    assert normalize_openai_compatible_citations(None, None, "") == []
    assert normalize_openai_compatible_citations({}, {}, "x") == []


def test_generic_openai_translator_attaches_compatible_citations():
    from types import SimpleNamespace

    from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator

    message = SimpleNamespace(
        content="cited answer",
        tool_calls=None,
        annotations=[
            {
                "type": "url_citation",
                "url_citation": {"url": "https://d.example", "title": "D"},
            }
        ],
    )
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=message, finish_reason="stop")],
        usage=None,
        id="resp_1",
        model="test-model",
        citations=["https://top.example"],
    )
    unified = GenericOpenAITranslator().from_generic_openai(response, "generic_openai")
    text_blocks = [b for m in unified.messages for b in m.content if isinstance(b, TextContent)]
    assert len(text_blocks) == 1
    citations = text_blocks[0].metadata["citations"]
    urls = {c["url"] for c in citations}
    assert urls == {"https://top.example", "https://d.example"}
    assert all(c["provider"] == "openai" for c in citations)


# ---------------------------------------------------------------------------
# Ratified machine-run exclusions (citations_enabled=False, explicit + loud)
# ---------------------------------------------------------------------------


def test_machine_run_agents_declare_citations_disabled():
    from matrx_ai.agent_runners.content_cleaner import PdfCleanerAgent
    from matrx_ai.agent_runners.podcast_generator import (
        _ContentExtractorAgent,
        _EducationalScriptAgent,
        _MultihostScriptAgent,
        _PodcastAgent,
        _PostPrepTranslationAgent,
    )
    from matrx_ai.agent_runners.research import (
        ResearchCondenser1Agent,
        ResearchCondenser2Agent,
    )
    from matrx_ai.agents.named import NamedAgent

    # Platform default: ON (None = no explicit policy).
    assert NamedAgent.citations_enabled is None
    # Every podcast stage inherits the machine-run exclusion from ONE base.
    assert _PodcastAgent.citations_enabled is False
    for agent_cls in (
        _EducationalScriptAgent,
        _MultihostScriptAgent,
        _ContentExtractorAgent,
        _PostPrepTranslationAgent,
        PdfCleanerAgent,
        ResearchCondenser1Agent,
        ResearchCondenser2Agent,
    ):
        assert agent_cls.citations_enabled is False, agent_cls.__name__
        # The explicit flag maps to the loud gate's disabled reason.
        reason = resolve_citations_disabled_reason(None, {"citations_enabled": False})
        assert reason is not None and "explicitly disabled" in reason


@pytest.mark.asyncio
async def test_run_agent_system_run_disables_citations():
    from types import SimpleNamespace

    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent
    from matrx_ai.config import UnifiedConfig

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id="citations-system-run-test"))
    config = UnifiedConfig.from_dict(
        {"model": "test-model", "messages": [{"role": "user", "content": "derive"}]}
    )

    async def execute(user_input=None):
        return SimpleNamespace(
            output="ok",
            assistant_response=None,
            config=config,
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = SimpleNamespace(
        name="internal-derive",
        config=config,
        output_schema=None,
        source_id=None,
        source_is_version=False,
        execute=execute,
    )
    result = await run_agent(
        agent,
        label="Internal Derive",
        source_app="test",
        source_feature="internal_derive",
        system_run=True,
        emit_lifecycle=False,
    )
    assert result.success is True
    assert config.metadata["citations_enabled"] is False


@pytest.mark.asyncio
async def test_run_agent_system_run_respects_explicit_force_enable():
    from types import SimpleNamespace

    from matrx_connect import ConsoleEmitter
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.agents.executor import run_agent
    from matrx_ai.config import UnifiedConfig

    set_app_context(AppContext(emitter=ConsoleEmitter(), user_id="citations-force-on-test"))
    config = UnifiedConfig.from_dict(
        {"model": "test-model", "messages": [{"role": "user", "content": "derive"}]}
    )
    config.metadata["citations_enabled"] = True  # explicit force-enable wins

    async def execute(user_input=None):
        return SimpleNamespace(
            output="ok",
            assistant_response=None,
            config=config,
            usage=None,
            usage_history=[],
            metadata={},
        )

    agent = SimpleNamespace(
        name="internal-derive",
        config=config,
        output_schema=None,
        source_id=None,
        source_is_version=False,
        execute=execute,
    )
    await run_agent(
        agent,
        label="Internal Derive",
        source_app="test",
        source_feature="internal_derive",
        system_run=True,
        emit_lifecycle=False,
    )
    assert config.metadata["citations_enabled"] is True


# ---------------------------------------------------------------------------
# Adversarial-review fixes: size budget, DB-rebuild citability, URI encoding
# ---------------------------------------------------------------------------


def test_matrx_citation_source_percent_encodes_ids():
    from matrx_ai.config.citations import (
        build_matrx_citation_source,
        parse_matrx_citation_source,
    )

    weird = "f/1?x#y"
    source = build_matrx_citation_source(file_id=weird, page=2)
    parsed = parse_matrx_citation_source(source)
    assert parsed["file_id"] == weird
    assert parsed["page"] == 2


def test_rebuilt_tool_result_regains_citability():
    """A DB-rebuilt (dict-content) citable tool result must re-emit
    homogeneous search_result wire blocks — not a JSON text blob."""
    from matrx_ai.config.tools_config import ToolResultContent

    stored_output = {
        "hits": [
            {
                "source_kind": "cld_file",
                "source_id": "f-77",
                "snippet": "clause 9 applies",
                "page_numbers": [9],
                "processed_document_id": "d-77",
                "metadata": {"file_name": "Contract.pdf"},
            }
        ]
    }
    wire = ToolResultContent(
        tool_use_id="tu_r1",
        call_id="tu_r1",
        name="knowledge_search",
        content=stored_output,
    ).to_anthropic()
    assert isinstance(wire["content"], list)
    types = {b["type"] for b in wire["content"]}
    assert types == {"search_result"}
    passage = wire["content"][0]
    assert passage["citations"] == {"enabled": True}
    assert passage["source"].startswith("matrx://file/f-77")
    # JSON-string content works too (some rebuild paths stringify).
    import json as _json

    wire2 = ToolResultContent(
        tool_use_id="tu_r2",
        call_id="tu_r2",
        name="document_search",
        content=_json.dumps(
            {"matches": [{"document_id": "d-1", "page_number": 3, "snippet": "hit"}]}
        ),
    ).to_anthropic()
    assert isinstance(wire2["content"], list)
    assert wire2["content"][0]["type"] == "search_result"
    # Non-citable tools keep the plain JSON path.
    wire3 = ToolResultContent(
        tool_use_id="tu_r3",
        call_id="tu_r3",
        name="shell_execute",
        content={"stdout": "ok"},
    ).to_anthropic()
    assert isinstance(wire3["content"], str)


def test_citable_wire_blocks_respect_char_budget():
    from matrx_ai.config.citations import citable_wire_blocks_from_output

    payload = {
        "hits": [
            {"processed_document_id": f"d-{i}", "snippet": "x" * 900, "page_numbers": [i + 1]}
            for i in range(40)
        ]
    }
    blocks = citable_wire_blocks_from_output("knowledge_search", payload, max_chars=5000)
    passages = [b for b in blocks if b["source"] != "matrx://metadata"]
    assert 0 < len(passages) <= 6
    meta_text = blocks[-1]["content"][0]["text"]
    assert "passages_dropped" in meta_text


def test_cap_citable_blocks_drops_lowest_ranked_first():
    from matrx_ai.config import SearchResultContent
    from matrx_ai.config.unified_content import cap_citable_blocks

    blocks = [SearchResultContent(texts=["y" * 900], title=f"B{i}") for i in range(40)]
    meta: dict = {}
    kept = cap_citable_blocks(blocks, meta)
    assert kept[0].title == "B0", "highest-ranked passage must survive"
    assert len(kept) < 40
    assert meta["passages_dropped"] == 40 - len(kept)


def test_absolute_ceiling_backstop_trims_runaway_passages():
    from matrx_ai.config import SearchResultContent, TextContent, UnifiedMessage
    from matrx_ai.config.message_config import MessageList
    from matrx_ai.config.tools_config import ToolResultContent

    huge = [SearchResultContent(texts=["z" * 60_000], title=f"P{i}") for i in range(12)]
    tool_result = ToolResultContent(
        tool_use_id="tu_c1", call_id="tu_c1", name="knowledge_search", content=huge
    )
    messages = MessageList(
        _messages=[UnifiedMessage(role="user", content=[TextContent(text="q"), tool_result])]
    )
    messages._enforce_absolute_tool_result_ceiling()
    remaining = [b for b in tool_result.content if getattr(b, "type", "") == "search_result"]
    assert len(remaining) < 12
    total = sum(len(b.get_output()) for b in remaining)
    assert total <= 500_000
