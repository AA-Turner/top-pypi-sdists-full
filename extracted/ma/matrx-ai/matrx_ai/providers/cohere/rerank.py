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


def rerank_search_units_at_most(documents: list[str]) -> int:
    """The most search units one rerank of ``documents`` can bill: Cohere counts one per query and 100 documents,
    a document over 500 tokens counting once per 500-token chunk (~1,500 characters taken as the chunk)."""
    chunks = sum(max(1, -(-len(doc or "") // 1500)) for doc in documents)
    return max(1, -(-chunks // 100))


#: The catalog ``api`` a rerank call is priced under (search units are its billed quantity).
COHERE_RERANK_API = "cohere_rerank"


def rerank_route(model: str) -> Any:
    """The dispatch route of a rerank of ``model``: what the admission pool, the run budget's quote
    (``guardrail_gate.quote_units``) and the settle all name. ``vendor`` is the catalog endpoint's (``cohere``), so
    the price is the model's ``ai.offering`` (``component_prices["search_units"]``)."""
    from types import SimpleNamespace

    return SimpleNamespace(
        vendor="cohere",
        model_name=model,
        endpoint_id="cohere-rerank",
        base_url="",
        offering_metadata={},
    )


def rerank_usage(response: Any, *, model: str, documents: list[str]) -> Any:
    """The billed usage of one rerank response: Cohere's ``billed_units.search_units`` (the most the call could
    bill, ``rerank_search_units_at_most``, when the vendor reports none), priced by the catalog like any call."""
    from matrx_ai.config.usage_config import TokenUsage

    billed = getattr(getattr(response, "meta", None), "billed_units", None)
    units = getattr(billed, "search_units", None)
    units = int(units) if units is not None else rerank_search_units_at_most(documents)
    return TokenUsage(
        input_tokens=units,
        output_tokens=0,
        matrx_model_name=model,
        provider_model_name=model,
        api=COHERE_RERANK_API,
        response_id=str(getattr(response, "id", "") or ""),
        billing_components={"search_units": units},
    )


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
        route = rerank_route(model)
        from matrx_ai.providers.guardrail_gate import quote_units

        from matrx_ai.orchestrator.executor import metered_one_shot

        # BOOKED through the one one-shot path (cost adversary pass 4, 2026-11-17: the dispatch net let it through
        # and nothing booked it, while inside a run the backstop read it as metered): inside a run the call is
        # metered live onto the run that owns it; outside one a one-shot ledger opens and settles it.
        async with metered_one_shot(None, feature="rag.rerank", label="cohere.rerank") as billed:
            response = await UnifiedAIClient._dispatch_with_billing_net(
                _rerank,
                profile=route,
                # Worst case in search units: one per 100 documents, a document over ~500 tokens (~1,500 chars)
                # counting once per chunk (Cohere's billing rule), priced at the route's catalog unit price.
                quote=quote_units(route, rerank_search_units_at_most(documents)),
            )
            billed.append(rerank_usage(response, model=model, documents=documents))
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
