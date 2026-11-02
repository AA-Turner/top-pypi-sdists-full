"""Client construction, context managers, env key, and async run (SPEC 3.1)."""

from __future__ import annotations

import httpx
import pytest

from getanyapi import AnyAPI, AnyAPIError, AsyncAnyAPI
from conftest import (
    json_response,
    make_async_client,
    make_sync_client,
    run_envelope,
)


def test_api_key_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANYAPI_API_KEY", "env-key")
    client = AnyAPI()
    assert client._api_key == "env-key"
    client.close()


def test_missing_api_key_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANYAPI_API_KEY", raising=False)
    with pytest.raises(AnyAPIError):
        AnyAPI()


def test_sync_context_manager() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope({"ok": True}))

    client, _ = make_sync_client(respond)
    with client as c:
        result = c.run("x.y", {})
    assert result.output.found is True


def test_generic_run_returns_typed_envelope() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(
            200, run_envelope({"count": 2}, cost_usd=0.02, items=2)
        )

    client, _ = make_sync_client(respond)
    result = client.run("x.y", {"a": 1})
    assert result.output.found is True
    assert result.output.data == {"count": 2}
    assert result.cost_usd == 0.02
    assert result.items == 2


def test_unknown_namespace_raises_attribute_error() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope({}))

    client, _ = make_sync_client(respond)
    with pytest.raises(AttributeError):
        _ = client.nonexistent_platform


async def test_async_run_and_context_manager() -> None:
    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope({"ok": True}, items=1))

    client, _ = make_async_client(respond)
    async with client as c:
        result = await c.run("x.y", {"a": 1})
    assert result.output.found is True
    assert result.items == 1


async def test_async_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ANYAPI_API_KEY", raising=False)
    with pytest.raises(AnyAPIError):
        AsyncAnyAPI()


def test_namespace_attachment_via_registry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Emulate the emitter contract: REGISTRY -> module -> Namespace class."""
    import sys
    import types

    import getanyapi.platforms as platforms

    # Build a fake generated platform module with sync+async namespaces.
    mod = types.ModuleType("getanyapi.platforms.demo")

    class DemoNamespace:
        def __init__(self, client: object) -> None:
            self._client = client

        def ping(self) -> object:
            return self._client.run("demo.ping", {})

    class AsyncDemoNamespace:
        def __init__(self, client: object) -> None:
            self._client = client

        async def ping(self) -> object:
            return await self._client.run("demo.ping", {})

    mod.DemoNamespace = DemoNamespace  # type: ignore[attr-defined]
    mod.AsyncDemoNamespace = AsyncDemoNamespace  # type: ignore[attr-defined]
    sys.modules["getanyapi.platforms.demo"] = mod
    monkeypatch.setitem(
        platforms.REGISTRY,
        "demo",
        ("demo", "DemoNamespace", "AsyncDemoNamespace"),
    )

    def respond(_req: httpx.Request) -> httpx.Response:
        return json_response(200, run_envelope({"pong": True}))

    client, _ = make_sync_client(respond)
    ns = client.demo
    assert isinstance(ns, DemoNamespace)
    # Cached on second access.
    assert client.demo is ns
    result = ns.ping()
    assert result.output.data == {"pong": True}
    sys.modules.pop("getanyapi.platforms.demo", None)
