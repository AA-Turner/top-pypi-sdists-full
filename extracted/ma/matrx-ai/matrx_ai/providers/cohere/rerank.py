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
        self, query: str, documents: list[str], *, model: str, max_retries: int | None = None
    ) -> list[float]:
        """``max_retries`` overrides the SDK's retry policy. A latency-bounded caller passes
        0: the SDK's default backoff on a 429 took 3.9 s (measured 2026-09-27), so a refused
        call surfaced as "slow" instead of as the refusal it was."""
        from types import SimpleNamespace

        from matrx_ai.providers.errors import mark_billing_checked
        from matrx_ai.providers.unified_client import UnifiedAIClient

        client = await asyncio.to_thread(lambda: self.client)

        async def _rerank() -> Any:
            try:
                return await client.rerank(
                    model=model,
                    query=query,
                    documents=documents,
                    top_n=len(documents),
                    **({"request_options": {"max_retries": max_retries}} if max_retries is not None else {}),
                )
            except BaseException as exc:
                # A refused rerank returns no billed search units: the adapter
                # looked, so LAYER 2 must not report a forgotten capture.
                mark_billing_checked(exc)
                raise

        # The shared dispatch seam: admission on the Cohere pool, the
        # out-of-credit alarm and LAYER 2.
        response = await UnifiedAIClient._dispatch_with_billing_net(
            _rerank,
            profile=SimpleNamespace(
                vendor="cohere",
                model_name=model,
                endpoint_id="cohere-rerank",
                base_url="",
                offering_metadata={},
            ),
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
