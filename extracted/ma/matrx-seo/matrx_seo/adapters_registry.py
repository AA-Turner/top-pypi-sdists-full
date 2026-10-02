"""The package-owned provider adapter registry (M-12 / WS-13).

Providers whose adapters the PACKAGE can construct on its own (default HTTP
transports; credentials resolve per-request through the secrets battery).
``gsc`` / ``ga4`` / ``bing_webmaster`` / ``pagespeed_insights`` require a
host-injected client factory (central Google OAuth, PSI client) and are
host-only until the package owns a standalone client for them — an unknown
provider is a 422 naming this exact list, never a silent fallback.

Host (aidream) and standalone (``matrx_seo.standalone.app``) both import
``ADAPTER_FACTORIES`` from here — neither owns its own copy, and the host
service never reaches into ``standalone.app`` for it.
"""

from __future__ import annotations

from collections.abc import Callable

from matrx_seo.adapters import SeoProviderAdapter
from matrx_seo.providers import BraveSeoRankAdapter, DataForSeoAdapter, SerpApiGoogleRankAdapter

_BRAVE_ADAPTER: BraveSeoRankAdapter | None = None
_SERPAPI_ADAPTER: SerpApiGoogleRankAdapter | None = None


def brave_adapter() -> BraveSeoRankAdapter:
    """ONE Brave adapter per process. A fresh instance per collection run
    (the old ``"brave": BraveSeoRankAdapter`` class-as-factory) meant every
    run got its own semaphore and ZERO pacing (``min_interval_seconds=0``),
    so concurrent rank checks burst straight into Brave 429s and surfaced
    them as user errors. Rate limits must queue, never error. The host
    (aidream) overrides this factory to share matrx_scraper's process-wide
    Brave limiter; standalone gets internal adaptive pacing seeded for a
    1 req/sec key and re-tuned from Brave's own headers."""
    global _BRAVE_ADAPTER
    if _BRAVE_ADAPTER is None:
        from matrx_seo.providers.brave import BRAVE_DEFAULT_MIN_INTERVAL_SECONDS

        _BRAVE_ADAPTER = BraveSeoRankAdapter(
            max_concurrency=2,
            min_interval_seconds=BRAVE_DEFAULT_MIN_INTERVAL_SECONDS,
        )
    return _BRAVE_ADAPTER


def serpapi_adapter() -> SerpApiGoogleRankAdapter:
    """ONE SerpAPI adapter per process, for the same reason Brave has one.

    ``"serpapi": SerpApiGoogleRankAdapter`` as a class-factory gave every run
    its own SerpApiClient — its own semaphore, its own unpaced queue — against
    a SINGLE monthly search allowance. Concurrent rank checks then burst
    straight through the hourly rate limit and, worse, spent the month faster
    than anything measured it. The host (aidream) overrides this factory to
    share the same client its generic ``/serp_search`` surface uses, so ONE
    allowance sits behind ONE queue."""
    global _SERPAPI_ADAPTER
    if _SERPAPI_ADAPTER is None:
        _SERPAPI_ADAPTER = SerpApiGoogleRankAdapter(
            max_concurrency=2,
            min_interval_seconds=0.5,
        )
    return _SERPAPI_ADAPTER


ADAPTER_FACTORIES: dict[str, Callable[[], SeoProviderAdapter]] = {
    "brave": brave_adapter,
    "dataforseo": DataForSeoAdapter,
    "serpapi": serpapi_adapter,
}

__all__ = ["ADAPTER_FACTORIES", "brave_adapter", "serpapi_adapter"]
