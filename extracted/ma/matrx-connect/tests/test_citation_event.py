"""CITATION stream event — payload registry, build_event, emitter surface."""

from __future__ import annotations

import asyncio

import pytest

from matrx_connect.context.events import (
    PAYLOAD_REGISTRY,
    VALID_EVENT_TYPES,
    CitationPayload,
    EventType,
    build_event,
)
from matrx_connect.emitters.silent_emitter import SilentEmitter
from matrx_connect.emitters.stream_emitter import StreamEmitter

_CITATION = {
    "kind": "document_char",
    "provider": "anthropic",
    "cited_text": "The frontend is a Next.js application deployed on Vercel. ",
    "title": "AI Matrx Platform Overview",
    "source_index": 0,
    "source_start": 122,
    "source_end": 180,
    "raw": {"type": "char_location"},
}


def test_citation_event_registered():
    assert "citation" in VALID_EVENT_TYPES
    assert PAYLOAD_REGISTRY[EventType.CITATION] is CitationPayload


def test_build_citation_event():
    payload = CitationPayload(block_index=3, citation=_CITATION)
    event = build_event(EventType.CITATION, payload)
    assert event.event == "citation"
    assert event.data["block_index"] == 3
    assert event.data["citation"]["kind"] == "document_char"


def test_citation_payload_forbids_extras():
    with pytest.raises(Exception):
        CitationPayload(block_index=0, citation=_CITATION, extra_field=True)


def test_stream_emitter_send_citation_queues_event():
    async def _run():
        emitter = StreamEmitter()
        await emitter.send_citation(CitationPayload(block_index=None, citation=_CITATION))
        items = []
        while not emitter.queue.empty():
            items.append(emitter.queue.get_nowait())
        return items

    items = asyncio.run(_run())
    # The event must have entered the outbound wire queue.
    assert items, "send_citation must enqueue a wire event"
    wire = b"".join(i if isinstance(i, bytes) else str(i).encode() for i in items if i)
    assert b'"citation"' in wire
    assert b"document_char" in wire


def test_silent_emitter_send_citation_is_noop():
    async def _run():
        emitter = SilentEmitter()
        await emitter.send_citation(CitationPayload(block_index=1, citation=_CITATION))

    asyncio.run(_run())
