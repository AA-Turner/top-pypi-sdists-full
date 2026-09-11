from __future__ import annotations

import asyncio
import time

import pytest

from matrx_ai.providers.cohere.rerank import CohereLegacyClient, CohereReranker


class _Response:
    class _Result:
        index = 0
        relevance_score = 0.8

    results = [_Result()]


class _Client:
    async def rerank(self, **kwargs):
        return _Response()


@pytest.mark.asyncio
async def test_cohere_cold_client_build_does_not_block_event_loop(monkeypatch):
    def slow_factory(api_key: str | None):
        time.sleep(0.15)
        return _Client()

    monkeypatch.setenv("COHERE_API_KEY", "test-key")
    monkeypatch.setattr(CohereReranker.client, "_factory", slow_factory)
    reranker = CohereReranker()
    task = asyncio.create_task(reranker.rerank("query", ["document"], model="test"))
    await asyncio.sleep(0.02)

    assert not task.done()
    assert await task == [0.8]


def test_cohere_legacy_client_keeps_generic_calls_at_provider_boundary(monkeypatch):
    class _LegacyClient:
        def chat(self, message: str, **kwargs):
            return {"message": message, "kwargs": kwargs}

    factory_calls: list[str | None] = []

    monkeypatch.setenv("COHERE_API_KEY", "test-key")
    monkeypatch.setattr(
        CohereLegacyClient.client,
        "_factory",
        lambda api_key: factory_calls.append(api_key) or _LegacyClient(),
    )

    client = CohereLegacyClient()
    chat = client.chat
    unknown = client.not_an_sdk_method

    # Neither a known nor unknown attribute lookup may resolve the key or
    # import/build the SDK client.  Unknown names still fail naturally if used.
    assert factory_calls == []

    assert chat("hello", connectors=[{"id": "web-search"}]) == {
        "message": "hello",
        "kwargs": {"connectors": [{"id": "web-search"}]},
    }
    assert factory_calls == ["test-key"]
    with pytest.raises(AttributeError):
        unknown()
