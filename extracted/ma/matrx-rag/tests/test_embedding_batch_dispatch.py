from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_rag.embeddings import (
    DefaultOpenAIVoyageProvider,
    EmbeddingSpec,
    _OffLoopOpenAI,
    _OffLoopVoyage,
)


@pytest.mark.asyncio
async def test_openai_embedding_payload_batches_dispatch_together() -> None:
    entered = 0
    all_entered = asyncio.Event()

    class Embeddings:
        async def create(self, *, model: str, input: list[str]):
            nonlocal entered
            entered += 1
            if entered == 3:
                all_entered.set()
            await asyncio.wait_for(all_entered.wait(), timeout=1)
            return SimpleNamespace(
                data=[SimpleNamespace(embedding=[float(len(text))]) for text in input],
                usage=SimpleNamespace(total_tokens=len(input)),
            )

    provider = DefaultOpenAIVoyageProvider()
    provider._openai_client = SimpleNamespace(embeddings=Embeddings())
    spec = EmbeddingSpec(
        name="openai:test",
        dim=1,
        table="rag.test_embeddings",
        batch_size=2,
    )

    vectors = await provider._embed_openai(["a", "bb", "c", "dd", "e"], spec)

    assert entered == 3
    assert vectors == [[1.0], [2.0], [1.0], [2.0], [1.0]]


@pytest.mark.asyncio
async def test_voyage_embedding_runs_off_the_event_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    """The Voyage SDK parses the response and decodes every base64 vector
    inside ``embed``; on the loop a large batch froze the worker ~2s
    (event_loop_stall 0772f6de). The call must run on a worker thread."""
    import threading

    loop_thread = threading.get_ident()
    seen_threads: list[int] = []

    class SyncVoyage:
        def embed(self, texts: list[str], *, model: str, input_type: str | None):
            seen_threads.append(threading.get_ident())
            return SimpleNamespace(
                embeddings=[[float(len(text))] for text in texts],
                total_tokens=len(texts),
            )

    provider = DefaultOpenAIVoyageProvider()
    # The key is read per call and the client rebuilt when it changed, so the injected client
    # must be paired with the key it was "built" for; no real key and no real SDK client.
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key-not-real")
    provider._voyage_key = "test-key-not-real"
    provider._voyage_client = _OffLoopVoyage(SyncVoyage())
    spec = EmbeddingSpec(
        name="voyage:test-model",
        dim=1,
        table="rag.test_embeddings",
        batch_size=2,
    )

    vectors = await provider._embed_voyage(["a", "bb", "c"], spec, input_type="document")

    assert vectors == [[1.0], [2.0], [1.0]]
    assert len(seen_threads) == 2
    assert loop_thread not in seen_threads


def test_the_live_voyage_client_is_the_off_loop_adapter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key-not-real")
    assert isinstance(DefaultOpenAIVoyageProvider()._voyage(), _OffLoopVoyage)


@pytest.mark.asyncio
async def test_openai_embedding_runs_off_the_event_loop() -> None:
    """The OpenAI SDK parses and base64-decodes every vector inside ``create``;
    on the loop that is the same stall class as Voyage. Must run on a worker thread."""
    import threading

    loop_thread = threading.get_ident()
    seen_threads: list[int] = []

    class SyncEmbeddings:
        def create(self, *, model: str, input: list[str]):
            seen_threads.append(threading.get_ident())
            return SimpleNamespace(
                data=[SimpleNamespace(embedding=[float(len(t))]) for t in input],
                usage=SimpleNamespace(total_tokens=len(input)),
            )

    provider = DefaultOpenAIVoyageProvider()
    provider._openai_client = _OffLoopOpenAI(SimpleNamespace(embeddings=SyncEmbeddings()))
    spec = EmbeddingSpec(name="openai:test-model", dim=1, table="rag.test_embeddings", batch_size=2)

    vectors = await provider._embed_openai(["a", "bb", "c"], spec)

    assert vectors == [[1.0], [2.0], [1.0]]
    assert len(seen_threads) == 2
    assert loop_thread not in seen_threads


def test_the_live_openai_client_is_the_off_loop_adapter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-real")
    assert isinstance(DefaultOpenAIVoyageProvider()._openai(), _OffLoopOpenAI)
