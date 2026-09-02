"""Tests for the Fastino GLiNER2 information-extraction provider.

Covers the wire contract end-to-end against ``httpx.MockTransport`` (no network,
no API key) — request shape, response parsing across the formatted/raw shapes,
HTTP error mapping, the missing-key guard, and capability registration. The
exact response shape is pinned by the live spike; the parser is intentionally
tolerant, and these tests lock that tolerance down.
"""

from __future__ import annotations

import asyncio
import gzip
import json
import threading
import time
from collections.abc import AsyncIterator

import httpx
import pytest

import matrx_ai.providers.fastino.fastino_api as fastino_api
from matrx_ai.providers.fastino import (
    ExtractedSpan,
    FastinoAuthError,
    FastinoExtraction,
    FastinoValidationError,
    SpanExtractionResult,
    parse_spans,
)
from matrx_ai.providers.fastino.client import resolve_fastino_api_key

# ---------------------------------------------------------------------------
# parse_spans — shape tolerance
# ---------------------------------------------------------------------------


def test_parse_spans_grouped_with_offsets():
    result = {
        "entities": {
            "company": [{"text": "Apple Inc.", "confidence": 0.95, "start": 0, "end": 10}],
            "person": [{"text": "Tim Cook", "confidence": 0.92, "start": 16, "end": 24}],
        }
    }
    spans = parse_spans(result)
    by_label = {s.label: s for s in spans}
    assert set(by_label) == {"company", "person"}
    assert by_label["company"].start == 0 and by_label["company"].end == 10
    assert by_label["company"].score == 0.95
    assert by_label["person"].text == "Tim Cook"


def test_parse_spans_bare_strings_have_no_offsets():
    spans = parse_spans({"entities": {"concept": ["osmosis", "diffusion"]}})
    assert [s.text for s in spans] == ["osmosis", "diffusion"]
    assert all(s.start == -1 and s.end == -1 and s.score is None for s in spans)


def test_parse_spans_unwrapped_and_list_forms():
    # bare {label: [...]} without the "entities" wrapper
    s1 = parse_spans({"person": [{"text": "Arman", "start": 3, "end": 8, "score": 0.7}]})
    assert s1 and s1[0].label == "person" and s1[0].score == 0.7
    # list of dicts carrying their own label
    s2 = parse_spans({"entities": [{"label": "url", "text": "a.com", "start": 1, "end": 6}]})
    assert s2 and s2[0].label == "url" and s2[0].text == "a.com"


def test_parse_spans_drops_empty_and_nondict():
    assert parse_spans(None) == []
    assert parse_spans({"entities": {"x": [{"text": "  "}, 42, None]}}) == []


# ---------------------------------------------------------------------------
# FastinoExtraction.extract — full request/response via MockTransport
# ---------------------------------------------------------------------------


def _completion(entities: dict) -> dict:
    """Wrap an entity payload as the gateway's chat-completion shape: the entity
    JSON lives as a *string* in ``choices[0].message.content``."""
    return {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "model": "fastino/gliner2-large-v1",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": json.dumps({"entities": entities})},
                "finish_reason": "stop",
            }
        ],
    }


def _mock_transport(capture: dict) -> httpx.MockTransport:
    def _handle(request: httpx.Request) -> httpx.Response:
        capture["url"] = str(request.url)
        capture["headers"] = dict(request.headers)
        capture["body"] = json.loads(request.content)
        return httpx.Response(
            200,
            json=_completion(
                {
                    "company": [{"text": "OpenAI", "confidence": 0.97, "start": 0, "end": 6}],
                    "person": [{"text": "Sam Altman", "confidence": 0.9, "start": 11, "end": 21}],
                }
            ),
        )

    return httpx.MockTransport(_handle)


async def test_extract_builds_request_and_parses_response(monkeypatch):
    monkeypatch.setenv("PIONEER_API_KEY", "test-key-123")
    monkeypatch.delenv("FASTINO_API_KEY", raising=False)
    monkeypatch.delenv("GLINER2_API_BASE_URL", raising=False)
    monkeypatch.delenv("PIONEER_API_BASE_URL", raising=False)
    capture: dict = {}

    async with httpx.AsyncClient(transport=_mock_transport(capture)) as client:
        extractor = FastinoExtraction(client=client)
        res = await extractor.extract(
            "OpenAI CEO Sam Altman announced GPT-5.",
            ["company", "person", "product"],
            threshold=0.4,
            model_class="fastino/gliner2-large-v1",
        )

    # Request shape (Pioneer OpenAI-compatible contract).
    assert capture["url"] == "https://api.pioneer.ai/v1/chat/completions"
    assert capture["headers"]["authorization"] == "Bearer test-key-123"
    body = capture["body"]
    assert body["model"] == "fastino/gliner2-large-v1"
    assert body["messages"] == [
        {"role": "user", "content": "OpenAI CEO Sam Altman announced GPT-5."}
    ]
    assert body["schema"] == {"entities": ["company", "person", "product"]}
    assert body["threshold"] == 0.4
    assert body["include_spans"] is True and body["include_confidence"] is True

    # Response parsed into a flat, typed span list.
    assert isinstance(res, SpanExtractionResult)
    assert res.model == "fastino/gliner2-large-v1"
    labels = {s.label for s in res.spans}
    assert labels == {"company", "person"}
    assert all(isinstance(s, ExtractedSpan) for s in res.spans)
    assert res.raw is not None


async def test_base_url_override(monkeypatch):
    monkeypatch.setenv("PIONEER_API_KEY", "k")
    monkeypatch.setenv("GLINER2_API_BASE_URL", "https://self-hosted.example.com/")
    capture: dict = {}
    async with httpx.AsyncClient(transport=_mock_transport(capture)) as client:
        await FastinoExtraction(client=client).extract("hi", ["x"])
    assert capture["url"] == "https://self-hosted.example.com/v1/chat/completions"


async def test_extract_accepts_dict_content(monkeypatch):
    monkeypatch.setenv("PIONEER_API_KEY", "k")

    def _handle(request: httpx.Request) -> httpx.Response:
        # Defensive path: content already a dict rather than a JSON string.
        completion = _completion({"date": [{"text": "2026", "start": 0, "end": 4}]})
        completion["choices"][0]["message"]["content"] = {
            "entities": {"date": [{"text": "2026", "start": 0, "end": 4}]}
        }
        return httpx.Response(200, json=completion)

    async with httpx.AsyncClient(transport=httpx.MockTransport(_handle)) as client:
        res = await FastinoExtraction(client=client).extract("2026", ["date"])
    assert len(res.spans) == 1 and res.spans[0].label == "date"


async def test_default_client_construction_keeps_event_loop_responsive(monkeypatch):
    monkeypatch.setenv("PIONEER_API_KEY", "k")
    construction_started = threading.Event()
    allow_construction = threading.Event()
    capture: dict = {}

    def blocking_client_constructor() -> httpx.AsyncClient:
        construction_started.set()
        assert allow_construction.wait(timeout=1.0)
        return httpx.AsyncClient(transport=_mock_transport(capture))

    monkeypatch.setattr(fastino_api, "build_fastino_client", blocking_client_constructor)

    extraction = asyncio.create_task(FastinoExtraction().extract("hello", ["topic"]))
    assert await asyncio.to_thread(construction_started.wait, 0.5)
    allow_construction.set()
    result = await extraction

    assert result.model == "fastino/gliner2-large-v1"


async def test_extract_decodes_compressed_response(monkeypatch):
    monkeypatch.setenv("PIONEER_API_KEY", "k")
    compressed = gzip.compress(json.dumps(_completion({"date": ["2026"]})).encode())

    class CompressedStream(httpx.AsyncByteStream):
        async def __aiter__(self) -> AsyncIterator[bytes]:
            yield compressed

    def _handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"content-encoding": "gzip", "content-type": "application/json"},
            stream=CompressedStream(),
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(_handle)) as client:
        result = await FastinoExtraction(client=client).extract("2026", ["date"])

    assert [span.text for span in result.spans] == ["2026"]


@pytest.mark.parametrize("stage", ["_handle_response", "_entities_from_completion"])
async def test_response_decode_does_not_block_event_loop(monkeypatch, stage):
    monkeypatch.setenv("PIONEER_API_KEY", "k")
    original = getattr(fastino_api, stage)

    def _slow_stage(*args, **kwargs):
        time.sleep(0.1)
        return original(*args, **kwargs)

    monkeypatch.setattr(fastino_api, stage, _slow_stage)
    capture: dict = {}
    async with httpx.AsyncClient(transport=_mock_transport(capture)) as client:
        extraction = asyncio.create_task(FastinoExtraction(client=client).extract("hi", ["x"]))
        started = time.perf_counter()
        await asyncio.sleep(0.01)
        heartbeat_elapsed = time.perf_counter() - started
        assert heartbeat_elapsed < 0.08
        assert not extraction.done()
        await extraction


# ---------------------------------------------------------------------------
# Error mapping
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "status,exc",
    [(401, FastinoAuthError), (422, FastinoValidationError), (400, FastinoValidationError)],
)
async def test_http_errors_map_to_typed_exceptions(monkeypatch, status, exc):
    monkeypatch.setenv("PIONEER_API_KEY", "k")

    def _handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json={"detail": "nope"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(_handle)) as client:
        with pytest.raises(exc):
            await FastinoExtraction(client=client).extract("x", ["y"])


def test_missing_api_key_raises_clean_error(monkeypatch):
    monkeypatch.delenv("PIONEER_API_KEY", raising=False)
    monkeypatch.delenv("FASTINO_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="PIONEER_API_KEY"):
        resolve_fastino_api_key()


# ---------------------------------------------------------------------------
# Capability registration
# ---------------------------------------------------------------------------


def test_extraction_models_are_identified_by_capability_data():
    """An extraction model is one whose capabilities jsonb declares
    ``interaction == "extraction"`` — never an api_class. It is NOT a chat-dispatch
    target: the catalog routes it to the ``extraction`` client_attr, which
    UnifiedAIClient.execute intercepts before the chat gates."""
    from types import SimpleNamespace

    from matrx_ai.catalog.resolve import client_attr_for_wire_format
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities
    from matrx_ai.providers.unified_client import UnifiedAIClient

    caps = resolve_model_capabilities(
        SimpleNamespace(
            name="gliner2-large",
            capabilities={
                "input": ["text"],
                "output": ["entities"],
                "features": ["ner"],
                "interaction": "extraction",
            },
        )
    )
    assert caps.interaction == "extraction"
    assert caps.supports_function_calling is False

    assert client_attr_for_wire_format("extraction_gliner") == "extraction"
    assert "extraction_gliner" not in UnifiedAIClient._PROVIDER_FACTORIES
    assert "extraction" not in UnifiedAIClient._PROVIDER_FACTORIES


def test_top_level_lazy_exports_resolve():
    import matrx_ai

    assert callable(matrx_ai.extract_spans)
    assert matrx_ai.SpanExtractionResult is SpanExtractionResult
    assert matrx_ai.ExtractedSpan is ExtractedSpan
