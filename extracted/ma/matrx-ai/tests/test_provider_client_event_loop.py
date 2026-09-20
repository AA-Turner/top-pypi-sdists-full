from __future__ import annotations

import asyncio
import threading
import time
from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest
import xai_sdk

from matrx_ai.providers import unified_client as uc
from matrx_ai.providers.keys import keyed_provider_client, prepare_provider_clients
from matrx_ai.providers.xai.xai_api import XAIChat
from matrx_ai.providers.xai.xai_image_api import XAIImageGeneration
from matrx_ai.providers.xai.xai_video_api import XAIVideoGeneration


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
    resolver_threads: list[int] = []
    factory_threads: list[int] = []

    class Provider:
        client = keyed_provider_client(
            "EVENT_LOOP_TEST_KEY",
            factory=lambda api_key: _slow_sdk_factory(
                api_key, built, factory_threads
            ),
        )

    def _resolve(*names, required=False):
        resolver_threads.append(threading.get_ident())
        return current["key"]

    monkeypatch.setattr(
        "matrx_ai.providers.keys.resolve_api_key",
        _resolve,
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
    assert resolver_threads == factory_threads
    assert all(thread_id != threading.get_ident() for thread_id in resolver_threads)


def _slow_sdk_factory(
    api_key: str | None,
    built: list[str | None],
    factory_threads: list[int] | None = None,
) -> dict[str, str | None]:
    time.sleep(0.15)
    built.append(api_key)
    if factory_threads is not None:
        factory_threads.append(threading.get_ident())
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


@pytest.mark.asyncio
async def test_xai_dispatch_preflight_resolves_off_loop_and_builds_native_sdk(monkeypatch):
    """xAI gRPC setup is loop-bound but performs no provider call here."""
    resolver_threads: list[int] = []
    current_key = {"value": "first-test-xai-key"}

    def _resolve(*names, required=False):
        resolver_threads.append(threading.get_ident())
        return current_key["value"]

    @asynccontextmanager
    async def _admit(profile):
        yield

    monkeypatch.setattr("matrx_ai.providers.keys.resolve_api_key", _resolve)
    monkeypatch.setattr("matrx_ai.providers.admission.admit_provider_call", _admit)
    provider = XAIChat()

    async def _dispatch() -> object:
        return provider.client

    client = await uc.UnifiedAIClient._dispatch_with_billing_net(
        _dispatch,
        profile=SimpleNamespace(vendor="xai", model_name="grok-test"),
        provider_client=provider,
    )
    current_key["value"] = "rotated-test-xai-key"
    await prepare_provider_clients(provider)
    rotated_client = provider.client
    try:
        assert isinstance(client, xai_sdk.AsyncClient)
        assert isinstance(rotated_client, xai_sdk.AsyncClient)
        assert rotated_client is not client
        assert resolver_threads
        assert all(thread_id != threading.get_ident() for thread_id in resolver_threads)
    finally:
        await client.close()
        await rotated_client.close()


@pytest.mark.asyncio
async def test_xai_image_and_video_preflight_build_native_sdk_without_network(monkeypatch):
    monkeypatch.setattr(
        "matrx_ai.providers.keys.resolve_api_key",
        lambda *names, required=False: "test-xai-key",
    )
    image = XAIImageGeneration()
    video = XAIVideoGeneration()

    await prepare_provider_clients(image)
    await prepare_provider_clients(video)
    try:
        assert isinstance(image.client, xai_sdk.AsyncClient)
        assert isinstance(video.client, xai_sdk.AsyncClient)
        assert XAIChat.client._event_loop_bound is True
        assert XAIImageGeneration.client._event_loop_bound is True
        assert XAIVideoGeneration.client._event_loop_bound is True
    finally:
        await image.client.close()
        await video.client.close()


@pytest.mark.asyncio
async def test_pinned_loop_bound_client_skips_resolution(monkeypatch):
    class Provider:
        client = keyed_provider_client(
            "EVENT_LOOP_TEST_KEY",
            factory=lambda api_key: object(),
            event_loop_bound=True,
        )

    provider = Provider()
    pinned = object()
    provider.client = pinned
    monkeypatch.setattr(
        "matrx_ai.providers.keys.resolve_api_key",
        lambda *names, required=False: pytest.fail("pinned client resolved credentials"),
    )

    await prepare_provider_clients(provider)
    assert provider.client is pinned


def test_loop_bound_clients_are_retained_per_event_loop(monkeypatch):
    built: list[object] = []

    class Provider:
        client = keyed_provider_client(
            "EVENT_LOOP_TEST_KEY",
            factory=lambda api_key: _record_loop_client(built),
            event_loop_bound=True,
        )

    monkeypatch.setattr(
        "matrx_ai.providers.keys.resolve_api_key",
        lambda *names, required=False: "test-key",
    )
    provider = Provider()

    async def _prepare_and_read():
        await prepare_provider_clients(provider)
        return provider.client

    first = asyncio.run(_prepare_and_read())
    second = asyncio.run(_prepare_and_read())

    assert first is not second
    assert built == [first, second]
    state = provider.__dict__["__keyed_client_client"]
    # The second preparation evicts the first closed asyncio.run() loop.
    assert len(state[3]) == 1


def test_loop_bound_clients_survive_overlapping_event_loop_preflights(monkeypatch):
    built: list[object] = []
    factory_barrier = threading.Barrier(2)

    def _factory(api_key):
        factory_barrier.wait(timeout=2)
        return _record_loop_client(built)

    class Provider:
        client = keyed_provider_client(
            "EVENT_LOOP_TEST_KEY",
            factory=_factory,
            event_loop_bound=True,
        )

    monkeypatch.setattr(
        "matrx_ai.providers.keys.resolve_api_key",
        lambda *names, required=False: "test-key",
    )
    provider = Provider()
    results: list[object] = []

    def _run_in_own_loop():
        async def _prepare_and_read():
            await prepare_provider_clients(provider)
            return provider.client

        results.append(asyncio.run(_prepare_and_read()))

    first = threading.Thread(target=_run_in_own_loop)
    second = threading.Thread(target=_run_in_own_loop)
    first.start()
    second.start()
    first.join(timeout=5)
    second.join(timeout=5)

    assert not first.is_alive()
    assert not second.is_alive()
    assert len(results) == 2
    assert results[0] is not results[1]
    assert set(built) == set(results)
    state = provider.__dict__["__keyed_client_client"]
    assert len(state[3]) == 2


def _record_loop_client(built: list[object]) -> object:
    client = object()
    built.append(client)
    return client
