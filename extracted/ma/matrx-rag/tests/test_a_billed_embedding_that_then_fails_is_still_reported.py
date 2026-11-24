"""An embeddings call the provider ANSWERED is billed even when reading its answer then raises (cost adversary pass 7,
embeddings residual: ``announce_embedding_call`` re-raised without reporting, so the spend reached no ledger).

Real: ``DefaultOpenAIVoyageProvider.embed`` (its OpenAI adapter), ``announce_embedding_call``, the host spend sink seam
(``embedding_spend_sink``). Double: the OpenAI client (returns a billed response whose vector rows are unreadable),
and the sink (records what it is handed)."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_rag import _ext
from matrx_rag.embeddings import DefaultOpenAIVoyageProvider


class _Embeddings:
    def __init__(self, data: list[Any]) -> None:
        self.data = data

    async def create(self, **kwargs: Any) -> Any:
        return SimpleNamespace(data=self.data, usage=SimpleNamespace(total_tokens=42))


def _provider(data: list[Any]) -> DefaultOpenAIVoyageProvider:
    provider = DefaultOpenAIVoyageProvider()
    provider._openai_client = SimpleNamespace(embeddings=_Embeddings(data))
    return provider


@pytest.fixture
def reported(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    seen: list[dict[str, Any]] = []
    monkeypatch.setitem(_ext._registry, "embedding_spend_sink", lambda **spend: seen.append(spend))
    return seen


async def test_a_billed_call_whose_answer_cannot_be_read_is_reported(reported: list[dict[str, Any]]) -> None:
    unreadable = [SimpleNamespace()]  # no .embedding: raises AFTER the provider billed the call
    with pytest.raises(AttributeError):
        await _provider(unreadable).embed("openai:text-embedding-3-small", ["hello world"])
    assert len(reported) == 1, "a billed embeddings call that then failed reached no ledger"
    assert reported[0]["tokens"] == 42 and reported[0]["provider"] == "openai"


async def test_a_good_call_is_reported_once(reported: list[dict[str, Any]]) -> None:
    good = [SimpleNamespace(embedding=[0.0] * 1536)]
    await _provider(good).embed("openai:text-embedding-3-small", ["hello world"])
    assert len(reported) == 1 and reported[0]["tokens"] == 42


async def test_a_call_that_never_returned_is_not_reported(reported: list[dict[str, Any]]) -> None:
    provider = DefaultOpenAIVoyageProvider()

    async def refused(**kwargs: Any) -> Any:
        raise RuntimeError("401 unauthorized")

    provider._openai_client = SimpleNamespace(embeddings=SimpleNamespace(create=refused))
    with pytest.raises(RuntimeError):
        await provider.embed("openai:text-embedding-3-small", ["hello world"])
    assert reported == []
