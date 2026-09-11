"""Cohere's cross-encoder rerank endpoint behind the provider boundary."""

from __future__ import annotations

import asyncio
from typing import Any

from matrx_ai.providers.keys import keyed_provider_client


def _make_client(api_key: str | None) -> Any:
    """Construct lazily; callers keep cold SDK setup off the event loop."""
    from cohere import AsyncClientV2

    return AsyncClientV2(api_key)


def _make_legacy_client(api_key: str | None) -> Any:
    """Construct the synchronous compatibility client only at a real call."""
    from cohere import Client

    return Client(api_key)


class CohereReranker:
    """Provider-owned adapter for Cohere reranking.

    The key resolver and keyed client cache are shared with every other
    matrx-ai provider, so host vaults, AppContext keys, and key rotation work
    without a RAG-specific environment read.
    """

    client = keyed_provider_client("COHERE_API_KEY", factory=_make_client, required=True)

    async def rerank(
        self, query: str, documents: list[str], *, model: str
    ) -> list[float]:
        client = await asyncio.to_thread(lambda: self.client)
        response = await client.rerank(
            model=model,
            query=query,
            documents=documents,
            top_n=len(documents),
        )
        scores = [0.0] * len(documents)
        for result in response.results:
            scores[result.index] = float(result.relevance_score)
        return scores


class CohereLegacyClient:
    """Lazy generic Cohere facade for compatibility callers.

    Older host modules exposed the Cohere SDK client itself as ``co``.  Keep
    that public call shape without allowing the host to resolve credentials or
    import the SDK: provider ownership, key rotation, and unloaded imports all
    stay here.
    """

    client = keyed_provider_client("COHERE_API_KEY", factory=_make_legacy_client, required=True)

    def __getattr__(self, name: str) -> Any:
        # Looking up ``co.chat`` must be as cold as importing the compatibility
        # export.  The old public surface is used as method calls, so defer the
        # keyed-client descriptor (and therefore both key resolution and the
        # SDK import) until that call actually happens.
        def call(*args: Any, **kwargs: Any) -> Any:
            return getattr(self.client, name)(*args, **kwargs)

        return call
