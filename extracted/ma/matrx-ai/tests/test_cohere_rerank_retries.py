"""A latency-bounded rerank call can turn the SDK's retries off (a retried 429 took 3.9 s)."""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.providers.cohere.rerank import CohereReranker


class _Client:
    def __init__(self):
        self.kwargs = None

    async def rerank(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(results=[SimpleNamespace(index=0, relevance_score=0.7)])


async def test_max_retries_rides_as_request_options(monkeypatch):
    client = _Client()
    reranker = CohereReranker.__new__(CohereReranker)
    monkeypatch.setattr(CohereReranker, "client", client, raising=False)
    assert await reranker.rerank("q", ["a"], model="m", max_retries=0) == [0.7]
    assert client.kwargs["request_options"] == {"max_retries": 0}
    await reranker.rerank("q", ["a"], model="m")
    assert "request_options" not in client.kwargs
