import inspect
from http import HTTPStatus
from types import SimpleNamespace

import pytest

from novita_sandbox.core import AsyncSandbox, Sandbox
from novita_sandbox.core.api.client.models import Sandbox as ClientSandbox
from novita_sandbox.core.api.client.types import Response
from novita_sandbox.core.sandbox_sync import sandbox_api as sync_sandbox_api
from novita_sandbox.core.sandbox_async import sandbox_api as async_sandbox_api


def test_create_accepts_auto_pause_for_compatibility():
    assert "auto_pause" in inspect.signature(Sandbox.create).parameters
    assert "auto_pause" in inspect.signature(AsyncSandbox.create).parameters


def test_pause_does_not_expose_sync_argument():
    assert "sync" not in inspect.signature(Sandbox.pause).parameters
    assert "sync" not in inspect.signature(AsyncSandbox.pause).parameters
    assert "sync" in inspect.signature(Sandbox.beta_pause).parameters
    assert "sync" in inspect.signature(AsyncSandbox.beta_pause).parameters


def test_create_accepts_node_id_for_compatibility():
    assert "node_id" in inspect.signature(Sandbox.create).parameters
    assert "node_id" in inspect.signature(AsyncSandbox.create).parameters


def test_connect_accepts_secure_and_public_traffic_for_compatibility():
    assert "secure" in inspect.signature(Sandbox.connect).parameters
    assert "secure" in inspect.signature(AsyncSandbox.connect).parameters
    assert "allow_public_traffic" in inspect.signature(Sandbox.connect).parameters
    assert "allow_public_traffic" in inspect.signature(AsyncSandbox.connect).parameters
    assert "network" in inspect.signature(Sandbox.connect).parameters
    assert "network" in inspect.signature(AsyncSandbox.connect).parameters


def test_reset_accepts_secure_and_public_traffic_for_compatibility():
    assert "secure" in inspect.signature(Sandbox.reset).parameters
    assert "secure" in inspect.signature(AsyncSandbox.reset).parameters
    assert "allow_public_traffic" in inspect.signature(Sandbox.reset).parameters
    assert "allow_public_traffic" in inspect.signature(AsyncSandbox.reset).parameters
    assert "network" in inspect.signature(Sandbox.reset).parameters
    assert "network" in inspect.signature(AsyncSandbox.reset).parameters


def test_connect_model_keeps_deprecated_network_and_new_option():
    from novita_sandbox.core.api.client.models import (
        ConnectSandbox,
        SandboxNetworkConfig,
    )

    legacy = ConnectSandbox(
        timeout=300,
        network=SandboxNetworkConfig(allow_public_traffic=False),
    )
    assert legacy.to_dict()["network"] == {"allowPublicTraffic": False}

    preferred = ConnectSandbox(
        timeout=300,
        allow_public_traffic=True,
        network=SandboxNetworkConfig(allow_public_traffic=False),
    )
    assert preferred.to_dict()["allowPublicTraffic"] is True


def test_sandbox_clone_and_reset_compatibility_methods_exist():
    assert hasattr(Sandbox, "clone")
    assert hasattr(AsyncSandbox, "clone")
    assert hasattr(Sandbox, "reset")
    assert hasattr(AsyncSandbox, "reset")


def test_sandbox_clone_uses_sandbox_id_when_client_id_missing(monkeypatch):
    class FakeHttpxClient:
        def post(self, path, json, timeout):
            return SimpleNamespace(
                status_code=HTTPStatus.OK,
                json=lambda: {
                    "sandboxes": [
                        {
                            "sandboxID": "sandbox-id",
                            "envdVersion": "0.5.7",
                            "envdAccessToken": "envd-token",
                            "trafficAccessToken": "traffic-token",
                        }
                    ],
                    "snapshotTemplateId": "snapshot-template",
                },
            )

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_httpx_client=lambda: FakeHttpxClient()),
    )

    result = sync_sandbox_api.SandboxApi._cls_clone_sandboxes("source-id")

    assert result["sandboxes"][0]["sandbox_id"] == "sandbox-id"


def test_sandbox_clone_uses_full_sandbox_id_only_for_legacy_domain(monkeypatch):
    class FakeHttpxClient:
        def post(self, path, json, timeout):
            return SimpleNamespace(
                status_code=HTTPStatus.OK,
                json=lambda: {
                    "sandboxes": [
                        {
                            "sandboxID": "sandbox-id",
                            "clientID": "client-id",
                            "envdVersion": "0.5.7",
                            "envdAccessToken": "envd-token",
                            "trafficAccessToken": "traffic-token",
                        }
                    ],
                    "snapshotTemplateId": "snapshot-template",
                },
            )

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_httpx_client=lambda: FakeHttpxClient()),
    )

    modern_result = sync_sandbox_api.SandboxApi._cls_clone_sandboxes("source-id")
    legacy_result = sync_sandbox_api.SandboxApi._cls_clone_sandboxes(
        "source-id", domain="sandbox.novita.ai"
    )

    assert modern_result["sandboxes"][0]["sandbox_id"] == "sandbox-id"
    assert legacy_result["sandboxes"][0]["sandbox_id"] == "sandbox-id-client-id"


async def test_async_sandbox_clone_uses_sandbox_id_when_client_id_missing(monkeypatch):
    class FakeAsyncHttpxClient:
        async def post(self, path, json, timeout):
            return SimpleNamespace(
                status_code=HTTPStatus.OK,
                json=lambda: {
                    "sandboxes": [
                        {
                            "sandboxID": "sandbox-id",
                            "envdVersion": "0.5.7",
                            "envdAccessToken": "envd-token",
                            "trafficAccessToken": "traffic-token",
                        }
                    ],
                    "snapshotTemplateId": "snapshot-template",
                },
            )

    monkeypatch.setattr(
        async_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_async_httpx_client=lambda: FakeAsyncHttpxClient()),
    )

    result = await async_sandbox_api.SandboxApi._cls_clone_sandboxes("source-id")

    assert result["sandboxes"][0]["sandbox_id"] == "sandbox-id"


async def test_async_sandbox_clone_uses_full_sandbox_id_only_for_legacy_domain(
    monkeypatch,
):
    class FakeAsyncHttpxClient:
        async def post(self, path, json, timeout):
            return SimpleNamespace(
                status_code=HTTPStatus.OK,
                json=lambda: {
                    "sandboxes": [
                        {
                            "sandboxID": "sandbox-id",
                            "clientID": "client-id",
                            "envdVersion": "0.5.7",
                            "envdAccessToken": "envd-token",
                            "trafficAccessToken": "traffic-token",
                        }
                    ],
                    "snapshotTemplateId": "snapshot-template",
                },
            )

    monkeypatch.setattr(
        async_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_async_httpx_client=lambda: FakeAsyncHttpxClient()),
    )

    modern_result = await async_sandbox_api.SandboxApi._cls_clone_sandboxes("source-id")
    legacy_result = await async_sandbox_api.SandboxApi._cls_clone_sandboxes(
        "source-id", domain="sandbox.novita.ai"
    )

    assert modern_result["sandboxes"][0]["sandbox_id"] == "sandbox-id"
    assert legacy_result["sandboxes"][0]["sandbox_id"] == "sandbox-id-client-id"


def test_sandbox_set_network_compatibility_methods_exist():
    assert hasattr(Sandbox, "set_network")
    assert hasattr(AsyncSandbox, "set_network")


def test_sandbox_set_network_puts_expected_payload(monkeypatch):
    calls = []

    class FakeHttpxClient:
        def put(self, path, json):
            calls.append((path, json))
            return Response(status_code=HTTPStatus.NO_CONTENT, content=b"", headers={}, parsed=None)

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_httpx_client=lambda: FakeHttpxClient()),
    )

    Sandbox.set_network(
        "sandbox-id",
        allow_out=["example.com", "8.8.8.8/32"],
        deny_out=["0.0.0.0/0"],
    )

    assert calls == [
        (
            "/sandboxes/sandbox-id/network",
            {"allowOut": ["example.com", "8.8.8.8/32"], "denyOut": ["0.0.0.0/0"]},
        )
    ]


async def test_async_sandbox_set_network_puts_expected_payload(monkeypatch):
    calls = []

    class FakeAsyncHttpxClient:
        async def put(self, path, json):
            calls.append((path, json))
            return Response(status_code=HTTPStatus.NO_CONTENT, content=b"", headers={}, parsed=None)

    monkeypatch.setattr(
        async_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_async_httpx_client=lambda: FakeAsyncHttpxClient()),
    )

    await AsyncSandbox.set_network(
        "sandbox-id",
        allow_out=["example.com", "8.8.8.8/32"],
        deny_out=["0.0.0.0/0"],
    )

    assert calls == [
        (
            "/sandboxes/sandbox-id/network",
            {"allowOut": ["example.com", "8.8.8.8/32"], "denyOut": ["0.0.0.0/0"]},
        )
    ]


def test_sandbox_connect_sends_secure_and_public_traffic(monkeypatch):
    calls = []

    def fake_sync_detailed(sandbox_id, client, body):
        calls.append((sandbox_id, body.to_dict()))
        return SimpleNamespace(
            status_code=HTTPStatus.OK,
            parsed=ClientSandbox.from_dict(
                {
                    "clientID": "",
                    "envdVersion": "0.5.7",
                    "sandboxID": sandbox_id,
                    "templateID": "template-id",
                    "trafficAccessToken": "traffic-token",
                }
            ),
        )

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config, **kwargs: SimpleNamespace(),
    )
    monkeypatch.setattr(
        sync_sandbox_api.post_sandboxes_sandbox_id_connect,
        "sync_detailed",
        fake_sync_detailed,
    )

    result = sync_sandbox_api.SandboxApi._cls_connect(
        "sandbox-id",
        timeout=321,
        secure=False,
        allow_public_traffic=False,
    )

    assert result.sandbox_id == "sandbox-id"
    assert result.traffic_access_token == "traffic-token"
    assert calls == [
        (
            "sandbox-id",
            {
                "timeout": 321,
                "secure": False,
                "allowPublicTraffic": False,
            },
        )
    ]


@pytest.mark.asyncio
async def test_async_sandbox_connect_sends_secure_and_public_traffic(monkeypatch):
    calls = []

    async def fake_asyncio_detailed(sandbox_id, client, body):
        calls.append((sandbox_id, body.to_dict()))
        return SimpleNamespace(
            status_code=HTTPStatus.OK,
            parsed=ClientSandbox.from_dict(
                {
                    "clientID": "",
                    "envdVersion": "0.5.7",
                    "sandboxID": sandbox_id,
                    "templateID": "template-id",
                    "trafficAccessToken": "traffic-token",
                }
            ),
        )

    monkeypatch.setattr(
        async_sandbox_api,
        "get_api_client",
        lambda config, **kwargs: SimpleNamespace(),
    )
    monkeypatch.setattr(
        async_sandbox_api.post_sandboxes_sandbox_id_connect,
        "asyncio_detailed",
        fake_asyncio_detailed,
    )

    result = await async_sandbox_api.SandboxApi._cls_connect(
        "sandbox-id",
        timeout=321,
        secure=True,
        allow_public_traffic=True,
    )

    assert result.sandbox_id == "sandbox-id"
    assert result.traffic_access_token == "traffic-token"
    assert calls == [
        (
            "sandbox-id",
            {
                "timeout": 321,
                "secure": True,
                "allowPublicTraffic": True,
            },
        )
    ]


def test_sandbox_reset_sends_secure_and_public_traffic(monkeypatch):
    calls = []

    class FakeHttpxClient:
        def post(self, path, json):
            calls.append((path, json))
            return Response(status_code=HTTPStatus.OK, content=b"", headers={}, parsed=None)

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_httpx_client=lambda: FakeHttpxClient()),
    )

    result = sync_sandbox_api.SandboxApi._cls_reset(
        "sandbox-id",
        resume=False,
        secure=True,
        network={"allow_public_traffic": True},
        allow_public_traffic=False,
        timeout=20,
    )

    assert result is True
    assert calls == [
        (
            "/sandboxes/sandbox-id/reset",
            {
                "resume": False,
                "secure": True,
                "allowPublicTraffic": False,
                "timeout": 20,
            },
        )
    ]


def test_sandbox_reset_parses_traffic_access_token(monkeypatch):
    class FakeHttpxClient:
        def post(self, path, json):
            return SimpleNamespace(
                status_code=HTTPStatus.CREATED,
                content=b'{"trafficAccessToken":"reset-token"}',
                json=lambda: {"trafficAccessToken": "reset-token"},
            )

    monkeypatch.setattr(
        sync_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_httpx_client=lambda: FakeHttpxClient()),
    )

    assert sync_sandbox_api.SandboxApi._cls_reset_with_token("sandbox-id") == (
        True,
        "reset-token",
    )


@pytest.mark.asyncio
async def test_async_sandbox_reset_sends_secure_and_public_traffic(monkeypatch):
    calls = []

    class FakeAsyncHttpxClient:
        async def post(self, path, json):
            calls.append((path, json))
            return Response(status_code=HTTPStatus.OK, content=b"", headers={}, parsed=None)

    monkeypatch.setattr(
        async_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(get_async_httpx_client=lambda: FakeAsyncHttpxClient()),
    )

    result = await async_sandbox_api.SandboxApi._cls_reset(
        "sandbox-id",
        resume=True,
        secure=False,
        network={"allow_public_traffic": False},
        allow_public_traffic=True,
        timeout=45,
    )

    assert result is True
    assert calls == [
        (
            "/sandboxes/sandbox-id/reset",
            {
                "resume": True,
                "secure": False,
                "allowPublicTraffic": True,
                "timeout": 45,
            },
        )
    ]


@pytest.mark.asyncio
async def test_async_sandbox_reset_parses_traffic_access_token(monkeypatch):
    class FakeAsyncHttpxClient:
        async def post(self, path, json):
            return SimpleNamespace(
                status_code=HTTPStatus.CREATED,
                content=b'{"trafficAccessToken":"reset-token"}',
                json=lambda: {"trafficAccessToken": "reset-token"},
            )

    monkeypatch.setattr(
        async_sandbox_api,
        "get_api_client",
        lambda config: SimpleNamespace(
            get_async_httpx_client=lambda: FakeAsyncHttpxClient()
        ),
    )

    assert await async_sandbox_api.SandboxApi._cls_reset_with_token(
        "sandbox-id"
    ) == (True, "reset-token")
