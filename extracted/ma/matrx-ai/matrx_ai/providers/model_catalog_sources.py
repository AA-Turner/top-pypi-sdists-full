"""Public model-catalog sources — models.dev, OpenRouter, Vercel AI Gateway.

These are the machine-readable catalogs that publish per-model PARAMETER truth
(output maximum, reasoning efforts / thinking budgets, sampling support, media
sizes/durations) that most providers' own ``/v1/models`` do not. They live in
the provider layer for the same reason ``model_listing.py`` does: reaching a
model host from application code is a D20 bypass whether or not a prompt is
sent. This module only FETCHES — it never chooses a model, never sends a prompt,
never spends, never sends a credential. Projection into facts and conflict
resolution belong to the catalog side
(``aidream/services/ai_catalog/parameter_facts.py``).

Sources and their terms (checked 2026-10-02):

- ``models.dev`` — ``GET https://models.dev/api.json``. Repo anomalyco/models.dev,
  MIT license. Keyed ``{provider_id: {models: {model_id: {...}}}}``.
- ``openrouter`` — ``GET https://openrouter.ai/api/v1/models`` and
  ``/api/v1/models/{author}/{slug}/endpoints``. Public, documented, no key. We
  store facts for internal translation only and never redistribute the catalog.
- ``vercel_gateway`` — ``GET https://ai-gateway.vercel.sh/v1/models`` and
  ``/v1/models/{author}/{slug}/endpoints``. Public,
  documented, no key. Same internal-only use.

Every fetch is bounded (size + timeout) and fails loudly with
:class:`ModelCatalogSourceError`; one source's outage never hides another's.
"""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

import httpx

MODELS_DEV_URL = "https://models.dev/api.json"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
OPENROUTER_ENDPOINTS_URL = "https://openrouter.ai/api/v1/models/{model_id}/endpoints"
VERCEL_GATEWAY_MODELS_URL = "https://ai-gateway.vercel.sh/v1/models"
VERCEL_GATEWAY_ENDPOINTS_URL = "https://ai-gateway.vercel.sh/v1/models/{model_id}/endpoints"

#: Per-model, per-host endpoint URL templates, keyed on the source name.
MODEL_ENDPOINTS_URLS: dict[str, str] = {
    "openrouter": OPENROUTER_ENDPOINTS_URL,
    "vercel_gateway": VERCEL_GATEWAY_ENDPOINTS_URL,
}

_USER_AGENT = "AI-Matrx/1.0 (+https://aimatrx.com)"

#: models.dev's api.json is ~5 MB today; a 10x growth headroom is still bounded.
_MAX_CATALOG_BYTES = 64_000_000
_MAX_ENDPOINTS_BYTES = 2_000_000


class ModelCatalogSourceError(RuntimeError):
    """A public catalog answered with something we refuse to trust."""


@dataclass(frozen=True)
class CatalogSource:
    """One public catalog: its stable name (stored with every fact), URL, terms."""

    name: str
    url: str
    terms: str
    fetch: Callable[[httpx.AsyncClient], Awaitable[Any]]


async def _get_bounded_json(http: httpx.AsyncClient, url: str, *, max_bytes: int, label: str) -> Any:
    try:
        async with http.stream(
            "GET", url, headers={"Accept": "application/json", "User-Agent": _USER_AGENT}
        ) as response:
            if response.status_code != 200:
                raise ModelCatalogSourceError(f"{label} returned HTTP {response.status_code}")
            body = bytearray()
            async for chunk in response.aiter_bytes():
                if len(body) + len(chunk) > max_bytes:
                    raise ModelCatalogSourceError(f"{label} returned more than {max_bytes} bytes")
                body.extend(chunk)
    except httpx.HTTPError as exc:
        raise ModelCatalogSourceError(f"{label} request failed — {type(exc).__name__}: {exc}") from exc
    try:
        return json.loads(bytes(body))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ModelCatalogSourceError(f"{label} returned invalid JSON") from exc


async def fetch_models_dev(http: httpx.AsyncClient) -> dict[str, Any]:
    payload = await _get_bounded_json(http, MODELS_DEV_URL, max_bytes=_MAX_CATALOG_BYTES, label="models.dev")
    if not isinstance(payload, dict) or not payload:
        raise ModelCatalogSourceError("models.dev returned no providers")
    return payload


async def fetch_openrouter_models(http: httpx.AsyncClient) -> list[dict[str, Any]]:
    payload = await _get_bounded_json(
        http, OPENROUTER_MODELS_URL, max_bytes=_MAX_CATALOG_BYTES, label="OpenRouter models"
    )
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, list) or not data:
        raise ModelCatalogSourceError("OpenRouter models returned no data")
    return [m for m in data if isinstance(m, dict)]


async def fetch_model_endpoints(http: httpx.AsyncClient, source_name: str, model_id: str) -> dict[str, Any]:
    """Per-host endpoints for ONE model (``author/slug``) — OpenRouter or Vercel.

    Both catalogs serve the same shape: ``{"data": {..., "reasoning": {...},
    "endpoints": [{"provider_name", "max_completion_tokens",
    "supported_parameters", "context_length", ...}]}}``. Returns ``data``.
    """
    template = MODEL_ENDPOINTS_URLS.get(source_name)
    if template is None:
        raise ModelCatalogSourceError(f"No per-endpoint URL for source {source_name!r}")
    payload = await _get_bounded_json(
        http,
        template.format(model_id=model_id),
        max_bytes=_MAX_ENDPOINTS_BYTES,
        label=f"{source_name} endpoints {model_id}",
    )
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        raise ModelCatalogSourceError(f"{source_name} endpoints {model_id} returned no data object")
    return data


async def fetch_vercel_gateway_models(http: httpx.AsyncClient) -> list[dict[str, Any]]:
    payload = await _get_bounded_json(
        http, VERCEL_GATEWAY_MODELS_URL, max_bytes=_MAX_CATALOG_BYTES, label="Vercel AI Gateway models"
    )
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, list) or not data:
        raise ModelCatalogSourceError("Vercel AI Gateway returned no data")
    return [m for m in data if isinstance(m, dict)]


CATALOG_SOURCES: tuple[CatalogSource, ...] = (
    CatalogSource("models.dev", MODELS_DEV_URL, "MIT (github.com/anomalyco/models.dev)", fetch_models_dev),
    CatalogSource(
        "openrouter",
        OPENROUTER_MODELS_URL,
        "public documented API, no key; internal use, not redistributed",
        fetch_openrouter_models,
    ),
    CatalogSource(
        "vercel_gateway",
        VERCEL_GATEWAY_MODELS_URL,
        "public documented API, no key; internal use, not redistributed",
        fetch_vercel_gateway_models,
    ),
)

CATALOG_SOURCES_BY_NAME: dict[str, CatalogSource] = {s.name: s for s in CATALOG_SOURCES}

#: The provider's OWN listing endpoint per ``ai.provider.slug`` — provenance only
#: (the fetch itself is ``model_listing.PROVIDER_FETCHERS``). Kept here so the
#: catalog side can cite a URL for a provider-own fact without naming a host.
PROVIDER_LISTING_URLS: dict[str, str] = {
    "openai": "https://api.openai.com/v1/models",
    "anthropic": "https://api.anthropic.com/v1/models",
    "groq": "https://api.groq.com/openai/v1/models",
    "google": "https://generativelanguage.googleapis.com/v1beta/models",
    "xai": "https://api.x.ai/v1/models",
    "cerebras": "https://api.cerebras.ai/v1/models",
    "together": "https://api.together.xyz/v1/models",
    "moonshot-ai": "https://api.moonshot.ai/v1/models",
    "typesafe": "https://api.typesafe.ai/v1/models",
}

__all__ = [
    "CATALOG_SOURCES",
    "CATALOG_SOURCES_BY_NAME",
    "MODELS_DEV_URL",
    "OPENROUTER_ENDPOINTS_URL",
    "OPENROUTER_MODELS_URL",
    "PROVIDER_LISTING_URLS",
    "VERCEL_GATEWAY_MODELS_URL",
    "CatalogSource",
    "ModelCatalogSourceError",
    "MODEL_ENDPOINTS_URLS",
    "VERCEL_GATEWAY_ENDPOINTS_URL",
    "fetch_model_endpoints",
    "fetch_models_dev",
    "fetch_openrouter_models",
    "fetch_vercel_gateway_models",
]
