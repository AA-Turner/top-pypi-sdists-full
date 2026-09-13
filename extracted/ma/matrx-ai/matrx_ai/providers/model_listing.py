"""Provider model-listing contracts — the ONE home for ``GET /v1/models``.

**Why this lives in the provider layer and nowhere else.** Reaching a provider
host is provider access whether the request is a completion or a model list
(``ROLLOUT.md`` 45-50, D20). The mandate scanner measures host reach, not
intent, and it is right to: the layer that owns a provider's wire contract is
this one, and every other place that wrote ``https://api.openai.com/...`` was a
second copy of that contract waiting to drift. On 2026-09-11 two such copies
existed outside this layer — aidream's catalog refresh (five hosts) and the
OpenRouter public-metadata service (one host) — and both reported as
``NEW_BYPASS`` the moment they landed. They now call in here.

What this module is NOT: it never chooses a model, never sends a prompt, never
spends. It is catalog infrastructure below the Agent runtime. Callers that need
a mandate are the ones that *run* models; a caller of this module only learns
which models exist.

Two contracts:

1. **Authenticated model listings** — :data:`PROVIDER_FETCHERS`, one
   :class:`ProviderFetcher` per ``ai.provider.slug`` (openai, anthropic, groq,
   google, xai). Each fetcher takes an ``httpx.AsyncClient`` and a resolved
   API key and returns the provider's own entries, normalized only as far as
   adding the three fields every consumer depends on: ``id`` (the wire id an
   offering's ``provider_model_id`` stores), ``display_name`` and ``created_at``
   (ISO-8601; derived from the ``created`` epoch where that is all the API
   gives). Every other provider field stays verbatim — Groq's ``pricing`` /
   ``context_window`` survive because nobody flattened them.

2. **OpenRouter's public (no-auth) model metadata** —
   :func:`read_openrouter_public_model`, a bounded read of
   ``/api/v1/model/<id>`` that refuses oversized bodies before decoding them.

Key resolution is the caller's job (``matrx_ai.providers.keys.resolve_api_key``
with :attr:`ProviderFetcher.env_names`), so a host that injects its own key
store keeps working unchanged.
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol

import httpx

ProviderEntry = dict[str, Any]

#: Hard stop on pagination loops — a provider that never stops returning
#: ``has_more`` must fail loudly, not spin forever inside a scheduled run.
MAX_PAGES = 50


class ProviderModelsApiError(RuntimeError):
    """A provider's models API answered with something we refuse to trust."""


# --- normalizers ---------------------------------------------------------------


def iso_from_epoch(created: Any) -> str | None:
    """``created`` (unix seconds, as OpenAI/Groq/xAI give it) → ISO-8601 UTC."""
    if isinstance(created, bool) or not isinstance(created, (int, float)):
        return None
    if created <= 0:
        # Cerebras serves ``"created": 0`` for every model — that is "unknown",
        # not 1970-01-01, and 1970 would silently trip the sync cutoff.
        return None
    try:
        return datetime.fromtimestamp(float(created), tz=UTC).isoformat().replace("+00:00", "Z")
    except (OverflowError, OSError, ValueError):
        return None


def _openai_shaped_entry(raw: ProviderEntry) -> ProviderEntry:
    """Normalize one entry from an OpenAI-shaped ``/v1/models`` payload.

    OpenAI, Groq and xAI all serve ``{"data": [{"id", "created", ...}]}``. The
    provider's own fields are kept verbatim; we only ADD ``display_name`` and an
    ISO ``created_at``.
    """
    entry = dict(raw)
    entry.setdefault("display_name", entry.get("id"))
    if not entry.get("created_at"):
        iso = iso_from_epoch(entry.get("created"))
        if iso:
            entry["created_at"] = iso
    return entry


def normalize_openai_page(payload: ProviderEntry) -> list[ProviderEntry]:
    """OpenAI ``GET /v1/models`` → entries."""
    return [_openai_shaped_entry(m) for m in payload.get("data") or [] if isinstance(m, dict)]


def normalize_cerebras_page(payload: ProviderEntry) -> list[ProviderEntry]:
    """Cerebras ``GET /v1/models`` → entries (OpenAI shape, ``created`` is 0)."""
    return [_openai_shaped_entry(m) for m in payload.get("data") or [] if isinstance(m, dict)]


def normalize_together_page(payload: Any) -> list[ProviderEntry]:
    """Together ``GET /v1/models`` → entries.

    Together answers with a bare JSON ARRAY (not ``{"data": [...]}``) of
    ``{"id", "display_name", "created", "type", "context_length", "pricing"}``
    across every modality it serves (chat, image, video, audio, transcribe,
    embedding, rerank). Everything is kept verbatim — ``type`` is what the sync
    agent uses to defer audio/video, ``pricing`` is per-1M-token USD — and only
    the ISO ``created_at`` is added.
    """
    models = payload if isinstance(payload, list) else (payload.get("data") if isinstance(payload, dict) else None)
    return [_openai_shaped_entry(m) for m in models or [] if isinstance(m, dict)]


def normalize_groq_page(payload: ProviderEntry) -> list[ProviderEntry]:
    """Groq ``GET /openai/v1/models`` → entries (OpenAI-shaped, plus pricing)."""
    return normalize_openai_page(payload)


def normalize_xai_page(payload: ProviderEntry) -> list[ProviderEntry]:
    """xAI ``GET /v1/models`` → entries (OpenAI-shaped)."""
    return normalize_openai_page(payload)


def normalize_anthropic_page(payload: ProviderEntry) -> list[ProviderEntry]:
    """Anthropic ``GET /v1/models`` → entries.

    Anthropic already gives ``display_name`` and an ISO ``created_at``; both are
    left exactly as served. Pagination (``has_more`` / ``last_id``) is the
    fetcher's job, not the normalizer's.
    """
    entries: list[ProviderEntry] = []
    for raw in payload.get("data") or []:
        if not isinstance(raw, dict):
            continue
        entry = dict(raw)
        entry.setdefault("display_name", entry.get("id"))
        if not entry.get("created_at"):
            iso = iso_from_epoch(entry.get("created"))
            if iso:
                entry["created_at"] = iso
        entries.append(entry)
    return entries


def normalize_google_page(payload: ProviderEntry) -> list[ProviderEntry]:
    """Google ``GET /v1beta/models?pageSize=200`` → entries.

    Google names a model ``models/gemini-3.8-flash``; the WIRE id — what an
    offering's ``provider_model_id`` stores — is the part after the slash.
    ``displayName`` / ``inputTokenLimit`` / ``outputTokenLimit`` are also mapped
    onto our vocabulary (``display_name`` / ``max_input_tokens`` /
    ``max_tokens``) because nothing downstream speaks camelCase; the original
    keys stay on the entry.
    """
    entries: list[ProviderEntry] = []
    for raw in payload.get("models") or []:
        if not isinstance(raw, dict):
            continue
        name = raw.get("name") or ""
        model_id = name[len("models/") :] if name.startswith("models/") else name
        entry = dict(raw)
        entry["id"] = model_id
        entry["display_name"] = raw.get("displayName") or model_id
        entry["max_input_tokens"] = raw.get("inputTokenLimit")
        entry["max_tokens"] = raw.get("outputTokenLimit")
        entries.append(entry)
    return entries


# --- transport -----------------------------------------------------------------


class _JsonResponse(Protocol):
    status_code: int
    text: str

    def json(self) -> Any: ...


class _GetClient(Protocol):
    """The slice of ``httpx.AsyncClient`` the fetchers use — so a test can hand
    in a scripted stub without faking the whole client."""

    async def get(
        self, url: str, *, headers: dict[str, str] | None = None, params: dict[str, str] | None = None
    ) -> Any: ...


async def _get_json(
    http: _GetClient,
    url: str,
    *,
    label: str,
    headers: dict[str, str],
    params: dict[str, str] | None = None,
) -> ProviderEntry:
    response: _JsonResponse = await http.get(url, headers=headers, params=params)
    if response.status_code != 200:
        body = response.text[:400]
        raise ProviderModelsApiError(f"{label} models API returned {response.status_code}: {body}")
    payload = response.json()
    if not isinstance(payload, dict):
        raise ProviderModelsApiError(
            f"{label} models API returned a {type(payload).__name__}, expected an object"
        )
    return payload


async def _get_json_any(
    http: _GetClient,
    url: str,
    *,
    label: str,
    headers: dict[str, str],
) -> Any:
    """Like :func:`_get_json` but accepts an object OR an array (Together)."""
    response: _JsonResponse = await http.get(url, headers=headers, params=None)
    if response.status_code != 200:
        body = response.text[:400]
        raise ProviderModelsApiError(f"{label} models API returned {response.status_code}: {body}")
    payload = response.json()
    if not isinstance(payload, (dict, list)):
        raise ProviderModelsApiError(
            f"{label} models API returned a {type(payload).__name__}, expected an object or an array"
        )
    return payload


async def fetch_openai(http: _GetClient, api_key: str) -> list[ProviderEntry]:
    payload = await _get_json(
        http,
        "https://api.openai.com/v1/models",
        label="OpenAI",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return normalize_openai_page(payload)


async def fetch_groq(http: _GetClient, api_key: str) -> list[ProviderEntry]:
    payload = await _get_json(
        http,
        "https://api.groq.com/openai/v1/models",
        label="Groq",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return normalize_groq_page(payload)


async def fetch_xai(http: _GetClient, api_key: str) -> list[ProviderEntry]:
    payload = await _get_json(
        http,
        "https://api.x.ai/v1/models",
        label="xAI",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return normalize_xai_page(payload)


async def fetch_cerebras(http: _GetClient, api_key: str) -> list[ProviderEntry]:
    payload = await _get_json(
        http,
        "https://api.cerebras.ai/v1/models",
        label="Cerebras",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return normalize_cerebras_page(payload)


async def fetch_together(http: _GetClient, api_key: str) -> list[ProviderEntry]:
    payload = await _get_json_any(
        http,
        "https://api.together.xyz/v1/models",
        label="Together",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return normalize_together_page(payload)


async def fetch_moonshot(http: _GetClient, api_key: str) -> list[ProviderEntry]:
    """Moonshot ``GET /v1/models`` — OpenAI shape plus ``context_length`` and
    ``supports_image_in`` / ``supports_video_in`` / ``supports_reasoning`` flags."""
    payload = await _get_json(
        http,
        "https://api.moonshot.ai/v1/models",
        label="Moonshot",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    return normalize_openai_page(payload)


async def fetch_anthropic(http: _GetClient, api_key: str) -> list[ProviderEntry]:
    headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
    entries: list[ProviderEntry] = []
    after_id: str | None = None
    for _ in range(MAX_PAGES):
        params = {"limit": "100"}
        if after_id:
            params["after_id"] = after_id
        payload = await _get_json(
            http, "https://api.anthropic.com/v1/models", label="Anthropic", headers=headers, params=params
        )
        entries.extend(normalize_anthropic_page(payload))
        if not payload.get("has_more") or not payload.get("last_id"):
            return entries
        after_id = str(payload["last_id"])
    raise ProviderModelsApiError(f"Anthropic models API did not stop paginating after {MAX_PAGES} pages")


async def fetch_google(http: _GetClient, api_key: str) -> list[ProviderEntry]:
    headers = {"x-goog-api-key": api_key}
    entries: list[ProviderEntry] = []
    page_token: str | None = None
    for _ in range(MAX_PAGES):
        params = {"pageSize": "200"}
        if page_token:
            params["pageToken"] = page_token
        payload = await _get_json(
            http,
            "https://generativelanguage.googleapis.com/v1beta/models",
            label="Google",
            headers=headers,
            params=params,
        )
        entries.extend(normalize_google_page(payload))
        next_token = payload.get("nextPageToken")
        if not next_token:
            return entries
        page_token = str(next_token)
    raise ProviderModelsApiError(f"Google models API did not stop paginating after {MAX_PAGES} pages")


# --- the fetcher table -----------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ProviderFetcher:
    """One provider's models-API contract.

    ``slug`` is ``ai.provider.slug`` — the stable join key. The display NAME has
    already drifted once (matrx-frontend matched on ``"OpenAi"`` while the row
    says ``"OpenAI"``), which is exactly the class of bug a slug prevents.
    ``env_names`` are the key names to hand ``resolve_api_key``, in order.
    """

    slug: str
    label: str
    env_names: tuple[str, ...]
    fetch: Callable[[Any, str], Awaitable[list[ProviderEntry]]]


PROVIDER_FETCHERS: tuple[ProviderFetcher, ...] = (
    ProviderFetcher("openai", "OpenAI", ("OPENAI_API_KEY",), fetch_openai),
    ProviderFetcher("anthropic", "Anthropic", ("ANTHROPIC_API_KEY",), fetch_anthropic),
    ProviderFetcher("groq", "Groq", ("GROQ_API_KEY",), fetch_groq),
    ProviderFetcher(
        "google",
        "Google",
        ("GEMINI_API_KEY", "GOOGLE_GENERATIVE_AI_API_KEY", "GOOGLE_API_KEY"),
        fetch_google,
    ),
    ProviderFetcher("xai", "xAI", ("XAI_API_KEY",), fetch_xai),
    # Serving vendors (they host other makers' models). Their snapshot is
    # matched by ai.provider_sync_candidates against the vendor's endpoint
    # offerings + aliases (ai_080/081), not against maker rows.
    ProviderFetcher("cerebras", "Cerebras", ("CEREBRAS_API_KEY",), fetch_cerebras),
    ProviderFetcher("together", "Together", ("TOGETHER_API_KEY",), fetch_together),
    ProviderFetcher("moonshot-ai", "Moonshot AI", ("MOONSHOT_API_KEY",), fetch_moonshot),
)

FETCHERS_BY_SLUG: dict[str, ProviderFetcher] = {f.slug: f for f in PROVIDER_FETCHERS}


# --- OpenRouter public model metadata ---------------------------------------------

OPENROUTER_PUBLIC_MODEL_URL = "https://openrouter.ai/api/v1/model/"
OPENROUTER_AUTO_ROUTER_ID = "openrouter/auto"
OPENROUTER_AUTO_ROUTER_URL = OPENROUTER_PUBLIC_MODEL_URL + OPENROUTER_AUTO_ROUTER_ID
_OPENROUTER_USER_AGENT = "AI-Matrx/1.0 (+https://aimatrx.com)"


class OpenRouterPublicModelError(RuntimeError):
    """OpenRouter's public model endpoint answered with something we refuse to trust.

    Messages are complete sentences a caller may surface as-is; they never carry
    the response body.
    """


async def _bounded_body(chunks: AsyncIterator[bytes], max_bytes: int) -> bytes:
    body = bytearray()
    async for chunk in chunks:
        if len(body) + len(chunk) > max_bytes:
            raise OpenRouterPublicModelError("OpenRouter returned oversized model metadata")
        body.extend(chunk)
    return bytes(body)


async def read_openrouter_public_model(
    model_id: str = OPENROUTER_AUTO_ROUTER_ID,
    *,
    http: httpx.AsyncClient | None = None,
    max_bytes: int = 64_000,
    timeout_seconds: float = 15.0,
) -> Any:
    """``GET https://openrouter.ai/api/v1/model/<model_id>`` — anonymous, bounded.

    Returns the decoded JSON payload verbatim; identity and capability
    projection are the caller's job. Refuses a non-200, a declared or streamed
    body over ``max_bytes`` (checked BEFORE decoding, so an oversized answer
    never reaches the JSON parser), and invalid JSON. Never sends credentials.
    """
    owns_client = http is None
    client = http or httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=False)
    try:
        async with client.stream(
            "GET",
            OPENROUTER_PUBLIC_MODEL_URL + model_id,
            headers={"Accept": "application/json", "User-Agent": _OPENROUTER_USER_AGENT},
        ) as response:
            if response.status_code != 200:
                raise OpenRouterPublicModelError(f"OpenRouter returned HTTP {response.status_code}")
            declared = response.headers.get("content-length")
            if declared is not None:
                try:
                    declared_size = int(declared)
                except ValueError as exc:
                    raise OpenRouterPublicModelError("OpenRouter returned invalid content length") from exc
                if declared_size < 0 or declared_size > max_bytes:
                    raise OpenRouterPublicModelError("OpenRouter returned oversized model metadata")
            body = await _bounded_body(response.aiter_bytes(), max_bytes)
    except httpx.HTTPError as exc:
        raise OpenRouterPublicModelError("OpenRouter model request failed") from exc
    finally:
        if owns_client:
            await client.aclose()
    try:
        return json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise OpenRouterPublicModelError("OpenRouter returned invalid JSON") from exc


__all__ = [
    "FETCHERS_BY_SLUG",
    "MAX_PAGES",
    "OPENROUTER_AUTO_ROUTER_ID",
    "OPENROUTER_AUTO_ROUTER_URL",
    "OPENROUTER_PUBLIC_MODEL_URL",
    "OpenRouterPublicModelError",
    "PROVIDER_FETCHERS",
    "ProviderEntry",
    "ProviderFetcher",
    "ProviderModelsApiError",
    "fetch_anthropic",
    "fetch_google",
    "fetch_groq",
    "fetch_openai",
    "fetch_xai",
    "iso_from_epoch",
    "normalize_anthropic_page",
    "normalize_google_page",
    "normalize_groq_page",
    "normalize_openai_page",
    "normalize_xai_page",
    "read_openrouter_public_model",
]
