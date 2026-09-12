"""``providers/model_listing.py`` — normalizers, pagination, and the bounded OpenRouter read.

The fixtures are trimmed but SHAPE-EXACT copies of what each provider's models
API actually returns — captured from the live 2026-09-11 refresh, not invented.
A normalizer that agrees with an imagined payload proves nothing.

Also here: the guard that keeps this module the ONE home for provider model
listings — every provider host the fetchers reach must be one the mandate
scanner knows, so a fetcher for a host the scanner has never heard of cannot
land here and silently widen the sanctioned surface.
"""

from __future__ import annotations

import ast
from pathlib import Path

import httpx
import pytest

from matrx_ai.providers import model_listing as ml

# --- fixtures: real payload shapes ------------------------------------------

OPENAI_PAGE = {
    "object": "list",
    "data": [
        {"id": "gpt-5.6-sol", "object": "model", "created": 1_770_000_000, "owned_by": "system"},
        {"id": "gpt-4o", "object": "model", "created": 1_715_367_049, "owned_by": "system"},
    ],
}

XAI_PAGE = {
    "object": "list",
    "data": [{"id": "grok-4", "object": "model", "created": 1_751_500_000, "owned_by": "xai"}],
}

GROQ_PAGE = {
    "object": "list",
    "data": [
        {
            "id": "openai/gpt-oss-safeguard-20b",
            "object": "model",
            "created": 1_761_708_789,
            "owned_by": "OpenAI",
            "active": True,
            "context_window": 131_072,
            "pricing": {"prompt": "0.000000075", "completion": "0.0000003"},
        }
    ],
}

ANTHROPIC_PAGE_1 = {
    "data": [
        {
            "type": "model",
            "id": "claude-opus-4-5-20251101",
            "display_name": "Claude Opus 4.5",
            "created_at": "2025-11-01T00:00:00Z",
        }
    ],
    "has_more": True,
    "first_id": "claude-opus-4-5-20251101",
    "last_id": "claude-opus-4-5-20251101",
}

ANTHROPIC_PAGE_2 = {
    "data": [
        {
            "type": "model",
            "id": "claude-sonnet-4-5-20250929",
            "display_name": "Claude Sonnet 4.5",
            "created_at": "2025-09-29T00:00:00Z",
        }
    ],
    "has_more": False,
    "last_id": None,
}

GOOGLE_PAGE = {
    "models": [
        {
            "name": "models/gemini-3.8-flash",
            "displayName": "Gemini 3.8 Flash",
            "inputTokenLimit": 1_048_576,
            "outputTokenLimit": 65_536,
            "supportedGenerationMethods": ["generateContent"],
        }
    ],
    "nextPageToken": None,
}


# --- normalizers -------------------------------------------------------------


def test_openai_entries_get_display_name_and_iso_created_at():
    entries = ml.normalize_openai_page(OPENAI_PAGE)
    assert [e["id"] for e in entries] == ["gpt-5.6-sol", "gpt-4o"]
    assert entries[0]["display_name"] == "gpt-5.6-sol"
    assert entries[1]["created_at"] == "2024-05-10T18:50:49Z"
    # the provider's own fields survive verbatim
    assert entries[0]["owned_by"] == "system"
    assert entries[0]["created"] == 1_770_000_000


def test_xai_uses_the_openai_shape():
    entries = ml.normalize_xai_page(XAI_PAGE)
    assert entries[0]["id"] == "grok-4"
    assert entries[0]["display_name"] == "grok-4"
    assert entries[0]["created_at"].endswith("Z")


def test_groq_keeps_its_per_token_pricing_and_context_window():
    entries = ml.normalize_groq_page(GROQ_PAGE)
    assert entries[0]["pricing"] == {"prompt": "0.000000075", "completion": "0.0000003"}
    assert entries[0]["context_window"] == 131_072
    assert entries[0]["active"] is True


def test_anthropic_keeps_the_display_name_and_iso_date_it_already_serves():
    entries = ml.normalize_anthropic_page(ANTHROPIC_PAGE_1)
    assert entries[0]["display_name"] == "Claude Opus 4.5"
    assert entries[0]["created_at"] == "2025-11-01T00:00:00Z"


def test_google_strips_the_models_prefix_and_maps_the_limits():
    entries = ml.normalize_google_page(GOOGLE_PAGE)
    assert entries[0]["id"] == "gemini-3.8-flash"
    assert entries[0]["display_name"] == "Gemini 3.8 Flash"
    assert entries[0]["max_input_tokens"] == 1_048_576
    assert entries[0]["max_tokens"] == 65_536
    # the original keys stay on the entry
    assert entries[0]["name"] == "models/gemini-3.8-flash"
    assert entries[0]["inputTokenLimit"] == 1_048_576


def test_normalizers_ignore_a_payload_with_no_models():
    assert ml.normalize_openai_page({"object": "list"}) == []
    assert ml.normalize_anthropic_page({"data": None}) == []
    assert ml.normalize_google_page({}) == []
    assert ml.normalize_openai_page({"data": ["not-a-dict", 3]}) == []


def test_iso_from_epoch_refuses_non_numbers_and_bools():
    assert ml.iso_from_epoch(True) is None
    assert ml.iso_from_epoch("1715367049") is None
    assert ml.iso_from_epoch(None) is None
    assert ml.iso_from_epoch(1_715_367_049) == "2024-05-10T18:50:49Z"


# --- fetchers: pagination and failure --------------------------------------------


class _StubResponse:
    def __init__(self, payload):
        self.status_code = 200
        self.text = ""
        self._payload = payload

    def json(self):
        return self._payload


class _StubClient:
    """Answers GETs from a scripted list of payloads, recording the params."""

    def __init__(self, payloads):
        self._payloads = list(payloads)
        self.calls: list[dict] = []

    async def get(self, url, headers=None, params=None):
        self.calls.append({"url": url, "headers": dict(headers or {}), "params": dict(params or {})})
        return _StubResponse(self._payloads.pop(0))


async def test_anthropic_follows_has_more_until_it_stops():
    http = _StubClient([ANTHROPIC_PAGE_1, ANTHROPIC_PAGE_2])
    entries = await ml.fetch_anthropic(http, "key")
    assert [e["id"] for e in entries] == [
        "claude-opus-4-5-20251101",
        "claude-sonnet-4-5-20250929",
    ]
    assert http.calls[1]["params"]["after_id"] == "claude-opus-4-5-20251101"
    assert http.calls[0]["headers"]["x-api-key"] == "key"


async def test_google_follows_next_page_token_until_it_stops():
    page_1 = {"models": GOOGLE_PAGE["models"], "nextPageToken": "TOKEN"}
    http = _StubClient([page_1, GOOGLE_PAGE])
    entries = await ml.fetch_google(http, "key")
    assert len(entries) == 2
    assert http.calls[0]["params"] == {"pageSize": "200"}
    assert http.calls[1]["params"]["pageToken"] == "TOKEN"
    assert http.calls[0]["headers"]["x-goog-api-key"] == "key"


async def test_a_runaway_pagination_stops_loudly(monkeypatch):
    monkeypatch.setattr(ml, "MAX_PAGES", 3)
    forever = {"data": [], "has_more": True, "last_id": "x"}
    http = _StubClient([forever] * 10)
    with pytest.raises(ml.ProviderModelsApiError) as exc:
        await ml.fetch_anthropic(http, "key")
    assert "did not stop paginating" in str(exc.value)
    assert len(http.calls) == 3


async def test_a_non_200_is_raised_with_the_provider_and_status():
    class _Failing:
        async def get(self, url, headers=None, params=None):  # noqa: ARG002
            r = _StubResponse(None)
            r.status_code = 401
            r.text = "invalid api key"
            return r

    with pytest.raises(ml.ProviderModelsApiError) as exc:
        await ml.fetch_openai(_Failing(), "bad")
    assert "OpenAI" in str(exc.value) and "401" in str(exc.value)


async def test_a_non_object_payload_is_refused():
    http = _StubClient([["a", "list"]])
    with pytest.raises(ml.ProviderModelsApiError) as exc:
        await ml.fetch_groq(http, "key")
    assert "expected an object" in str(exc.value)


async def test_openai_shaped_fetchers_send_a_bearer_token():
    for fetch in (ml.fetch_openai, ml.fetch_groq, ml.fetch_xai):
        http = _StubClient([OPENAI_PAGE])
        await fetch(http, "secret")
        assert http.calls[0]["headers"] == {"Authorization": "Bearer secret"}


def test_the_fetcher_table_is_keyed_on_provider_slug():
    assert set(ml.FETCHERS_BY_SLUG) == {"openai", "anthropic", "groq", "google", "xai"}
    for fetcher in ml.PROVIDER_FETCHERS:
        assert fetcher.env_names, fetcher.slug
        assert ml.FETCHERS_BY_SLUG[fetcher.slug] is fetcher


# --- OpenRouter public read --------------------------------------------------------


def _openrouter_body() -> dict:
    return {"data": {"id": "openrouter/auto", "canonical_slug": "openrouter/auto", "name": "Auto Router"}}


async def test_openrouter_read_is_anonymous_and_returns_the_payload_verbatim():
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json=_openrouter_body())

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        payload = await ml.read_openrouter_public_model(http=client)

    assert str(requests[0].url) == ml.OPENROUTER_AUTO_ROUTER_URL
    assert "authorization" not in requests[0].headers
    assert requests[0].headers["accept"] == "application/json"
    assert payload == _openrouter_body()


@pytest.mark.parametrize("code", [301, 404, 429, 500])
async def test_openrouter_read_rejects_non_success(code: int):
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _: httpx.Response(code))
    ) as client:
        with pytest.raises(ml.OpenRouterPublicModelError, match=f"HTTP {code}"):
            await ml.read_openrouter_public_model(http=client)


async def test_openrouter_read_refuses_an_oversized_body_before_decoding():
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _: httpx.Response(200, content=b"x" * 101))
    ) as client:
        with pytest.raises(ml.OpenRouterPublicModelError, match="oversized"):
            await ml.read_openrouter_public_model(http=client, max_bytes=100)


async def test_openrouter_read_refuses_a_declared_oversized_length():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"{}", headers={"content-length": "999999"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ml.OpenRouterPublicModelError, match="oversized"):
            await ml.read_openrouter_public_model(http=client, max_bytes=100)


async def test_openrouter_read_refuses_invalid_json():
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda _: httpx.Response(200, content=b"not json"))
    ) as client:
        with pytest.raises(ml.OpenRouterPublicModelError, match="invalid JSON"):
            await ml.read_openrouter_public_model(http=client)


async def test_openrouter_read_wraps_transport_errors():
    def handler(_request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ml.OpenRouterPublicModelError, match="request failed"):
            await ml.read_openrouter_public_model(http=client)


# --- the guard: every host reached here is one the scanner polices ------------------


def test_every_host_reached_here_is_in_the_mandate_scanner_vocabulary():
    """This module is exempt from the provider-bypass scan BY PATH. That
    exemption is only honest while every host it reaches is one the scanner
    would have flagged anywhere else — otherwise the provider layer becomes
    the place to hide an unpoliced host. Proven failing: add
    ``"https://api.example-llm.com/v1/models"`` to a fetcher and this goes red."""
    vocabulary = pytest.importorskip(
        "matrx_mandate_scan.provider_vocabulary",
        reason="the scanner vocabulary ships with the monorepo; a standalone install has no scanner to agree with",
    )
    PROVIDER_HOSTS = vocabulary.PROVIDER_HOSTS

    source = Path(ml.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    reached: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and "://" in node.value:
            reached.add(node.value)
    # the User-Agent's contact URL is ours, not a provider's
    reached = {url for url in reached if "aimatrx.com" not in url}
    assert reached, "the fetchers must name their targets as literals — that is what the scanner reads"
    unpoliced = sorted(url for url in reached if not any(host in url for host in PROVIDER_HOSTS))
    assert not unpoliced, (
        f"model_listing.py reaches hosts the mandate scanner does not police: {unpoliced}. "
        "Add the host to matrx_mandate_scan.provider_vocabulary.PROVIDER_HOSTS first."
    )
