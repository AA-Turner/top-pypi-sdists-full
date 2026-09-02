from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest

from matrx_ai.providers import unified_client as uc
from matrx_ai.providers.keys import keyed_provider_client, prepare_provider_clients


@pytest.fixture(autouse=True)
def _clean_provider_cache():
    snapshot = dict(uc._provider_client_cache)
    uc.reset_provider_client_cache()
    yield
    uc.reset_provider_client_cache()
    uc._provider_client_cache.update(snapshot)


@pytest.mark.asyncio
async def test_cold_provider_construction_does_not_block_event_loop(monkeypatch):
    sentinel = object()

    def _slow_build(name: str, factory_name: str):
        time.sleep(0.15)
        uc._provider_client_cache[name] = sentinel
        return sentinel

    monkeypatch.setattr(uc.UnifiedAIClient, "_build_provider_client", staticmethod(_slow_build))
    client = uc.UnifiedAIClient()
    build = asyncio.create_task(client._get_provider_client("openai_chat"))
    await asyncio.sleep(0.02)

    assert not build.done()
    assert await build is sentinel
    assert client.openai_chat is sentinel


@pytest.mark.asyncio
async def test_concurrent_cold_requests_share_one_provider_client(monkeypatch):
    built = 0
    sentinel = object()

    def _counted_build(name: str, factory_name: str):
        nonlocal built
        with uc._provider_client_cache_lock:
            cached = uc._provider_client_cache.get(name)
            if cached is not None:
                return cached
            built += 1
            time.sleep(0.05)
            uc._provider_client_cache[name] = sentinel
            return sentinel

    monkeypatch.setattr(uc.UnifiedAIClient, "_build_provider_client", staticmethod(_counted_build))
    first, second = await asyncio.gather(
        uc.UnifiedAIClient()._get_provider_client("openai_chat"),
        uc.UnifiedAIClient()._get_provider_client("openai_chat"),
    )

    assert first is second is sentinel
    assert built == 1


@pytest.mark.asyncio
async def test_keyed_sdk_construction_and_rotation_stay_off_event_loop(monkeypatch):
    current = {"key": "first"}
    built: list[str | None] = []

    class Provider:
        client = keyed_provider_client(
            "EVENT_LOOP_TEST_KEY",
            factory=lambda api_key: _slow_sdk_factory(api_key, built),
        )

    monkeypatch.setattr(
        "matrx_ai.providers.keys.resolve_api_key",
        lambda *names, required=False: current["key"],
    )
    provider = Provider()

    with pytest.raises(RuntimeError, match="accessed cold on the asyncio event loop"):
        _ = provider.client

    preparation = asyncio.create_task(prepare_provider_clients(provider))
    await asyncio.sleep(0.02)
    assert not preparation.done()
    await preparation
    first = provider.client
    assert first == {"api_key": "first"}

    current["key"] = "second"
    rotation = asyncio.create_task(prepare_provider_clients(provider))
    await asyncio.sleep(0.02)
    assert provider.client is first
    await rotation
    assert provider.client == {"api_key": "second"}
    assert built == ["first", "second"]


def _slow_sdk_factory(api_key: str | None, built: list[str | None]) -> dict[str, str | None]:
    time.sleep(0.15)
    built.append(api_key)
    return {"api_key": api_key}


@pytest.mark.asyncio
async def test_dispatch_preflights_lazy_sdk_client(monkeypatch):
    built: list[str | None] = []

    class Provider:
        client = keyed_provider_client(
            "EVENT_LOOP_TEST_KEY",
            factory=lambda api_key: _slow_sdk_factory(api_key, built),
        )

    @asynccontextmanager
    async def _admit(profile):
        yield

    monkeypatch.setattr(
        "matrx_ai.providers.keys.resolve_api_key",
        lambda *names, required=False: "dispatch-key",
    )
    monkeypatch.setattr("matrx_ai.providers.admission.admit_provider_call", _admit)
    provider = Provider()

    async def _dispatch() -> object:
        return provider.client

    result = await uc.UnifiedAIClient._dispatch_with_billing_net(
        _dispatch,
        profile=SimpleNamespace(vendor="test", model_name="test-model"),
        provider_client=provider,
    )

    assert result == {"api_key": "dispatch-key"}
    assert built == ["dispatch-key"]
