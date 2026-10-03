"""Public model-catalog sources: bounded fetches and the scanner-vocabulary guard.

No network: transport is a scripted ``httpx.MockTransport``.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import httpx
import pytest

from matrx_ai.providers import model_catalog_sources as mcs


def _client(handler) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


@pytest.mark.asyncio
async def test_models_dev_payload_is_returned_verbatim():
    payload = {"groq": {"models": {"qwen/qwen3.8-27b": {"limit": {"output": 16384}}}}}
    async with _client(lambda req: httpx.Response(200, json=payload)) as http:
        assert await mcs.fetch_models_dev(http) == payload


@pytest.mark.asyncio
async def test_a_non_200_is_a_loud_error():
    async with _client(lambda req: httpx.Response(503, text="down")) as http:
        with pytest.raises(mcs.ModelCatalogSourceError, match="HTTP 503"):
            await mcs.fetch_openrouter_models(http)


@pytest.mark.asyncio
async def test_an_empty_catalog_is_refused():
    async with _client(lambda req: httpx.Response(200, json={"data": []})) as http:
        with pytest.raises(mcs.ModelCatalogSourceError, match="no data"):
            await mcs.fetch_vercel_gateway_models(http)


@pytest.mark.asyncio
async def test_per_host_endpoints_url_and_shape():
    seen: list[str] = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen.append(str(req.url))
        return httpx.Response(200, json={"data": {"id": "qwen/qwen3.8-27b", "endpoints": [{"provider_name": "Groq"}]}})

    async with _client(handler) as http:
        data = await mcs.fetch_model_endpoints(http, "openrouter", "qwen/qwen3.8-27b")
        await mcs.fetch_model_endpoints(http, "vercel_gateway", "alibaba/qwen3.8-27b")
    assert data["endpoints"][0]["provider_name"] == "Groq"
    assert seen == [
        "https://openrouter.ai/api/v1/models/qwen/qwen3.8-27b/endpoints",
        "https://ai-gateway.vercel.sh/v1/models/alibaba/qwen3.8-27b/endpoints",
    ]


@pytest.mark.asyncio
async def test_an_oversized_body_is_refused_before_decoding(monkeypatch):
    monkeypatch.setattr(mcs, "_MAX_ENDPOINTS_BYTES", 10)
    body = json.dumps({"data": {"endpoints": [{"provider_name": "x" * 100}]}})
    async with _client(lambda req: httpx.Response(200, text=body)) as http:
        with pytest.raises(mcs.ModelCatalogSourceError, match="more than 10 bytes"):
            await mcs.fetch_model_endpoints(http, "openrouter", "a/b")


def test_every_llm_host_reached_here_is_in_the_mandate_scanner_vocabulary():
    """Same guard as test_model_listing: the provider-layer path exemption is honest
    only while every completion-serving host named here is one the scanner polices.
    models.dev serves no completions (a static MIT catalog) and is not a provider host."""
    vocabulary = pytest.importorskip("matrx_mandate_scan.provider_vocabulary")
    tree = ast.parse(Path(mcs.__file__).read_text(encoding="utf-8"))
    reached = {
        n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and "://" in n.value
    }
    reached = {u for u in reached if "aimatrx.com" not in u and "models.dev" not in u}
    assert reached
    unpoliced = sorted(u for u in reached if not any(h in u for h in vocabulary.PROVIDER_HOSTS))
    assert not unpoliced, f"add these hosts to PROVIDER_HOSTS first: {unpoliced}"
