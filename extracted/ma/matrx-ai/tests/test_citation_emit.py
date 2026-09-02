"""Settle-time citation emission — the shared provider helper.

Covers providers/citation_emit.py, the ONE settle-time ``citation`` event
emitter used by Google (grounding), xAI (response-level URL list), and the
OpenAI-compatible providers. A malformed citation must be skipped loudly and
must never abort emission of the remaining citations.
"""

from __future__ import annotations

import asyncio

from matrx_ai.config import TextContent, TokenUsage, UnifiedMessage, UnifiedResponse
from matrx_ai.providers.citation_emit import emit_citations_from_response


class _RecordingEmitter:
    def __init__(self, fail_on: set[int] | None = None):
        self.sent: list[object] = []
        self._fail_on = fail_on or set()
        self._count = 0

    async def send_citation(self, payload):
        index = self._count
        self._count += 1
        if index in self._fail_on:
            raise RuntimeError("boom")
        self.sent.append(payload)


def _response_with_citations(citations: list) -> UnifiedResponse:
    block = TextContent(text="answer")
    block.metadata["citations"] = citations
    return UnifiedResponse(
        messages=[UnifiedMessage(role="assistant", content=[block])],
        usage=TokenUsage(input_tokens=1, output_tokens=1),
    )


def test_emit_citations_sends_one_event_per_citation():
    citations = [
        {"kind": "web", "provider": "xai", "url": "https://a.example", "source_index": 0},
        {"kind": "web", "provider": "xai", "url": "https://b.example", "source_index": 1},
    ]
    emitter = _RecordingEmitter()
    asyncio.run(emit_citations_from_response(_response_with_citations(citations), emitter, "XAI"))
    assert len(emitter.sent) == 2
    assert emitter.sent[0].block_index is None
    assert emitter.sent[0].citation["url"] == "https://a.example"
    assert emitter.sent[1].citation["url"] == "https://b.example"


def test_emit_citations_failure_skips_that_citation_only():
    citations = [
        {"kind": "web", "provider": "xai", "url": "https://a.example", "source_index": 0},
        {"kind": "web", "provider": "xai", "url": "https://b.example", "source_index": 1},
        {"kind": "web", "provider": "xai", "url": "https://c.example", "source_index": 2},
    ]
    emitter = _RecordingEmitter(fail_on={1})
    # Must not raise — the failing send is skipped loudly.
    asyncio.run(emit_citations_from_response(_response_with_citations(citations), emitter, "XAI"))
    assert [p.citation["url"] for p in emitter.sent] == [
        "https://a.example",
        "https://c.example",
    ]


def test_emit_citations_ignores_non_dict_items_and_empty_response():
    emitter = _RecordingEmitter()
    asyncio.run(emit_citations_from_response(None, emitter, "XAI"))
    asyncio.run(
        emit_citations_from_response(_response_with_citations(["not-a-dict"]), emitter, "XAI")
    )
    assert emitter.sent == []
