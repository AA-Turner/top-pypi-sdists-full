from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_rag.embeddings import DefaultOpenAIVoyageProvider, EmbeddingSpec


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
