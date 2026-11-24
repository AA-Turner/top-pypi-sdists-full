"""Answer offsets on every normalized citation are UTF-16 code units — the unit every client slices by.

The web (``@ai-matrx/agents`` presentation/citations.ts, a JS string) and the iPhone (Kit
``MessageCitations.swift``, ``text.utf16``) both cut the answer text at ``answer_start`` /
``answer_end`` as UTF-16 offsets. Providers count differently: Gemini grounding and the Gemini
Interactions API count UTF-8 bytes, OpenAI counts characters (code points), and our own regex
offsets are code points. Before the fix each was passed through unconverted, so markers drifted
mid-word after the first non-ASCII character (CGU-09 item 7, chat.message 4575fe87…: 26 of 41
offsets mid-word). Each test cuts the text by UTF-16 units and must land exactly on the cited words.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config.citations import (
    normalize_google_grounding,
    normalize_google_interaction_annotations,
    normalize_markdown_link_citations,
    normalize_openai_annotation,
    normalize_openai_compatible_citations,
)

# é (2 UTF-8 bytes, 1 UTF-16 unit), — (3 bytes, 1 unit), 🚀 (4 bytes, 2 units, 1 code point).
PREFIX = "Café crème — the 🚀 launch. "
CLAIM = "Rockets fly fast."
ANSWER = PREFIX + CLAIM + " Done."


def _u16_slice(text: str, start: int, end: int) -> str:
    units = text.encode("utf-16-le")
    return units[2 * start : 2 * end].decode("utf-16-le")


def test_gemini_grounding_byte_offsets_become_utf16() -> None:
    start = len(PREFIX.encode("utf-8"))
    end = start + len(CLAIM.encode("utf-8"))
    metadata = {
        "grounding_chunks": [{"web": {"uri": "https://a.example", "title": "a"}}],
        "grounding_supports": [
            {"segment": {"start_index": start, "end_index": end, "text": CLAIM}, "grounding_chunk_indices": [0]}
        ],
    }
    [citation] = normalize_google_grounding(metadata, ANSWER)
    assert _u16_slice(ANSWER, citation.answer_start, citation.answer_end) == CLAIM
    # raw keeps the provider's own byte offsets
    assert citation.raw["support"]["segment"]["start_index"] == start


def test_gemini_grounding_first_segment_without_start() -> None:
    text = "Ünïcode first. Then more."
    end = len("Ünïcode first.".encode())
    metadata = {
        "grounding_chunks": [{"web": {"uri": "https://a.example"}}],
        "grounding_supports": [{"segment": {"end_index": end}, "grounding_chunk_indices": [0]}],
    }
    [citation] = normalize_google_grounding(metadata, text)
    assert _u16_slice(text, citation.answer_start, citation.answer_end) == "Ünïcode first."


def test_openai_character_offsets_become_utf16() -> None:
    start = len(PREFIX)  # OpenAI counts characters (code points)
    annotation = {"type": "url_citation", "url": "https://a.example", "start_index": start, "end_index": start + len(CLAIM)}
    citation = normalize_openai_annotation(annotation, ANSWER)
    assert _u16_slice(ANSWER, citation.answer_start, citation.answer_end) == CLAIM
    assert citation.raw["start_index"] == start


def test_openai_compatible_annotations_become_utf16() -> None:
    start = len(PREFIX)
    message = SimpleNamespace(
        annotations=[
            {"type": "url_citation", "url_citation": {"url": "https://a.example", "start_index": start, "end_index": start + len(CLAIM)}},
            {"type": "document_citation", "document_citation": {"document_id": "1", "start_index": start, "end_index": start + len(CLAIM)}},
            {"type": "function_citation", "function_citation": {"tool_call_id": "t", "start_index": start, "end_index": start + len(CLAIM)}},
        ]
    )
    citations = normalize_openai_compatible_citations(SimpleNamespace(), message, ANSWER)
    assert len(citations) == 3
    for citation in citations:
        assert _u16_slice(ANSWER, citation.answer_start, citation.answer_end) == CLAIM


def test_interactions_byte_offsets_in_a_later_part_become_utf16() -> None:
    first = "Prélude — 🚀 intro.\n\n"
    part = "Über " + CLAIM
    start = len("Über ".encode())
    end = start + len(CLAIM.encode())
    citations = normalize_google_interaction_annotations(
        [{"type": "url_citation", "url": "https://a.example", "start_index": start, "end_index": end}],
        text=part,
        offset=len(first.encode("utf-16-le")) // 2,  # the part's position, in UTF-16 units
    )
    report = first + part
    [citation] = citations
    assert _u16_slice(report, citation.answer_start, citation.answer_end) == CLAIM


def test_markdown_link_offsets_become_utf16() -> None:
    link = "[Source](https://a.example/x)"
    text = PREFIX + link + " end"
    [citation] = normalize_markdown_link_citations(text, provider="google")
    assert _u16_slice(text, citation.answer_start, citation.answer_end) == link
